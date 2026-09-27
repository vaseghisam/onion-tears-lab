"""Rebuild the article's deterministic numerical outputs.

Run from the repository root: python -m src.run_simulations
No external data, internet access, random sampling or specialist solver is
required. The configuration records deliberately illustrative inputs.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import scipy
from scipy.integrate import cumulative_trapezoid

from .model import (
    concentration_history, field_at_time, finite_exposure_quad,
    integrated_kernel, point_source_integral, source_cumulative,
    source_inventory, source_rate,
)


ROOT = Path(__file__).resolve().parents[1]


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config/model_config.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results")
    parser.add_argument("--skip-animation", action="store_true",
                        help="Only recompute tables; leave existing animation data untouched")
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)
    geometry = config["geometry"]
    source_position = np.asarray(geometry["source_position_m"], dtype=float)
    observer = np.asarray(geometry["observation_position_m"], dtype=float)
    position = observer - source_position
    distance = float(np.linalg.norm(position))
    unit_toward = position / distance
    # The canonical source/observer separation lies in the x-z plane.
    transverse = np.array([0.0, 1.0, 0.0])
    if abs(np.dot(unit_toward, transverse)) > 1e-12:
        raise ValueError("Configured observation must lie in the x-z plane")
    speed = config["flow_speed_m_s"]
    sigma_s = geometry["source_sigma_m"]
    sigma_o = geometry["observation_sigma_m"]
    diffusivity = config["diffusivity_m2_s"]
    scenarios = {
        "no_mean_drift": np.zeros(3),
        "toward": speed * unit_toward,
        "away": -speed * unit_toward,
        "transverse": speed * transverse,
    }
    dt = config["history"]["time_step_s"]
    end = config["history"]["end_time_s"]
    times = np.linspace(0, end, round(end / dt) + 1)
    history_rows = []
    source_rows = []
    summary_rows = []
    convergence_rows = []
    tail_rows = []
    profiles = config["sources"]
    for source_id, rates in profiles.items():
        a, b = rates["k_production_per_s"], rates["k_release_per_s"]
        q = source_rate(times, a, b)
        precursor, retained, released = source_inventory(times, a, b)
        for i, time in enumerate(times):
            source_rows.append({
                "source_id": source_id, "time_s": float(time),
                "emission_rate_per_s": float(q[i]),
                "precursor_fraction": float(precursor[i]),
                "retained_fraction": float(retained[i]),
                "emitted_fraction": float(released[i]),
            })
        for scenario_id, velocity in scenarios.items():
            concentration = concentration_history(times, q, position, velocity,
                                                   diffusivity, sigma_s, sigma_o)
            exposure = cumulative_trapezoid(concentration, times, initial=0)
            infinite = integrated_kernel(position, velocity, diffusivity, sigma_s, sigma_o)
            exact_finite = finite_exposure_quad(end, a, b, position, velocity,
                                                diffusivity, sigma_s, sigma_o)
            peak_index = int(np.argmax(concentration))
            summary_rows.append({
                "source_id": source_id, "scenario_id": scenario_id,
                "peak_concentration_per_m3": float(concentration[peak_index]),
                "peak_time_s": float(times[peak_index]),
                "exposure_120s_s_per_m3": float(exposure[-1]),
                "exposure_120s_quad_reference_s_per_m3": exact_finite,
                "infinite_exposure_s_per_m3": infinite,
                "fraction_of_infinite_exposure_by_120s": float(exposure[-1] / infinite),
                "emitted_fraction_by_120s": float(source_cumulative(end, a, b)),
                "finite_exposure_relative_numerical_error": float(abs(exposure[-1] - exact_finite) / exact_finite),
            })
            for i, time in enumerate(times):
                history_rows.append({
                    "source_id": source_id, "scenario_id": scenario_id,
                    "time_s": float(time), "emission_rate_per_s": float(q[i]),
                    "concentration_per_m3": float(concentration[i]),
                    "cumulative_exposure_s_per_m3": float(exposure[i]),
                })
            for check_dt in [0.1, 0.05, 0.025, 0.0125]:
                check_t = np.linspace(0, end, round(end / check_dt) + 1)
                check_q = source_rate(check_t, a, b)
                check_c = concentration_history(check_t, check_q, position, velocity,
                                                diffusivity, sigma_s, sigma_o)
                check_e = float(np.trapezoid(check_c, check_t))
                convergence_rows.append({
                    "source_id": source_id, "scenario_id": scenario_id,
                    "time_step_s": check_dt,
                    "exposure_120s_s_per_m3": check_e,
                    "peak_concentration_per_m3": float(check_c.max()),
                    "relative_error_against_adaptive_quad": abs(check_e - exact_finite) / exact_finite,
                })
            for horizon in [30, 60, 120, 300, 1200, 10000]:
                exact_horizon = finite_exposure_quad(horizon, a, b, position,
                                                     velocity, diffusivity, sigma_s, sigma_o)
                tail_rows.append({
                    "source_id": source_id, "scenario_id": scenario_id,
                    "horizon_s": horizon,
                    "finite_exposure_s_per_m3": exact_horizon,
                    "infinite_exposure_s_per_m3": infinite,
                    "fraction_of_infinite_exposure": exact_horizon / infinite,
                })
    by_case = {(row["source_id"], row["scenario_id"]): row for row in summary_rows}
    for row in summary_rows:
        baseline = by_case[(row["source_id"], "no_mean_drift")]
        row["exposure_120s_ratio_to_same_source_no_mean_drift"] = (
            row["exposure_120s_s_per_m3"] / baseline["exposure_120s_s_per_m3"])
        row["infinite_exposure_ratio_to_no_mean_drift"] = (
            row["infinite_exposure_s_per_m3"] / baseline["infinite_exposure_s_per_m3"])

    # Scenario sweeps have no probability distribution or confidence meaning.
    sensitivity_rows = []
    sensitivity = config["sensitivity"]
    fast = profiles["fast"]
    a, b = fast["k_production_per_s"], fast["k_release_per_s"]
    for diffusion in sensitivity["diffusivity_m2_s"]:
        for radius in sensitivity["distance_m"]:
            displacement = radius * unit_toward
            baseline_finite = finite_exposure_quad(end, a, b, displacement, np.zeros(3),
                                                    diffusion, sigma_s, sigma_o)
            baseline_infinite = integrated_kernel(displacement, np.zeros(3), diffusion,
                                                   sigma_s, sigma_o)
            for sweep_speed in sensitivity["flow_speed_m_s"]:
                for angle in sensitivity["angle_deg"]:
                    theta = np.deg2rad(angle)
                    velocity = sweep_speed * (np.cos(theta) * unit_toward +
                                              np.sin(theta) * transverse)
                    finite = finite_exposure_quad(end, a, b, displacement, velocity,
                                                   diffusion, sigma_s, sigma_o)
                    infinite = integrated_kernel(displacement, velocity, diffusion,
                                                   sigma_s, sigma_o)
                    sensitivity_rows.append({
                        "diffusivity_m2_s": diffusion, "distance_m": radius,
                        "flow_speed_m_s": sweep_speed, "angle_deg": angle,
                        "effective_peclet_number": sweep_speed * radius / diffusion,
                        "exposure_120s_s_per_m3": finite,
                        "infinite_exposure_s_per_m3": infinite,
                        "exposure_120s_ratio_to_no_mean_drift": finite / baseline_finite,
                        "infinite_exposure_ratio_to_no_mean_drift": infinite / baseline_infinite,
                        "point_source_infinite_reference_s_per_m3": point_source_integral(
                            displacement, velocity, diffusion),
                    })

    loss_rows = []
    for loss_rate in sensitivity["loss_rate_per_s"]:
        for scenario_id, velocity in scenarios.items():
            infinite = integrated_kernel(position, velocity, diffusivity, sigma_s,
                                          sigma_o, loss_rate=loss_rate)
            for source_id, rates in profiles.items():
                finite = finite_exposure_quad(end, rates["k_production_per_s"],
                                              rates["k_release_per_s"], position,
                                              velocity, diffusivity, sigma_s, sigma_o,
                                              loss_rate=loss_rate)
                loss_rows.append({
                    "source_id": source_id, "scenario_id": scenario_id,
                    "assumed_loss_rate_per_s": loss_rate,
                    "exposure_120s_s_per_m3": finite,
                    "infinite_exposure_s_per_m3": infinite,
                    "point_source_infinite_reference_s_per_m3": point_source_integral(
                        position, velocity, diffusivity, loss_rate=loss_rate),
                })

    spatial_checks = []
    probe_points = np.array([[0, 0, 0], [.03, 0, 0], [.3, 0, .4],
                             [-.3, 0, -.4], [0, .3, .1]], dtype=float)
    for scenario_id, velocity in scenarios.items():
        for time in [1.0, 10.0, 30.0, 60.0]:
            finer = field_at_time(time, probe_points, velocity, diffusivity,
                                  sigma_s, a, b, quadrature_order=256)
            canonical = field_at_time(time, probe_points, velocity, diffusivity,
                                      sigma_s, a, b, quadrature_order=128)
            for i, point in enumerate(probe_points):
                spatial_checks.append({
                    "scenario_id": scenario_id, "time_s": time,
                    "x_m": point[0], "y_m": point[1], "z_m": point[2],
                    "concentration_order128_per_m3": canonical[i],
                    "concentration_order256_per_m3": finer[i],
                    "absolute_difference_per_m3": abs(canonical[i] - finer[i]),
                    "relative_difference": abs(canonical[i] - finer[i]) / max(abs(finer[i]), 1e-30),
                })

    write_csv(out / "time_histories.csv", history_rows)
    write_csv(out / "source_histories.csv", source_rows)
    write_csv(out / "summary.csv", summary_rows)
    write_csv(out / "time_convergence.csv", convergence_rows)
    write_csv(out / "tail_convergence.csv", tail_rows)
    write_csv(out / "sensitivity.csv", sensitivity_rows)
    write_csv(out / "loss_sensitivity.csv", loss_rows)
    write_csv(out / "field_quadrature_convergence.csv", spatial_checks)

    animation_info = None
    if not args.skip_animation:
        anim = config["animation"]
        x = np.linspace(*anim["x_range_m"], anim["nx"])
        z = np.linspace(*anim["z_range_m"], anim["nz"])
        xx, zz = np.meshgrid(x, z, indexing="xy")
        positions = np.stack([xx, np.zeros_like(xx), zz], axis=-1) - source_position
        frame_times = np.linspace(0, anim["end_time_s"],
                                  round(anim["end_time_s"] / anim["frame_step_s"]) + 1)
        fields = np.empty((len(scenarios), len(frame_times), len(z), len(x)), dtype=np.float32)
        for scenario_index, (scenario_id, velocity) in enumerate(scenarios.items()):
            for frame_index, time in enumerate(frame_times):
                fields[scenario_index, frame_index] = field_at_time(
                    time, positions, velocity, diffusivity, sigma_s, a, b,
                    quadrature_order=anim["quadrature_order"])
            print(f"Computed animation data: {scenario_id}", flush=True)
        np.savez_compressed(
            out / "animation_fields.npz", times_s=frame_times, x_m=x, z_m=z,
            scenario_ids=np.array(list(scenarios)), concentration_per_m3=fields,
            velocity_m_s=np.array(list(scenarios.values())),
            observation_position_m=observer, source_position_m=source_position,
            diffusivity_m2_s=diffusivity, source_sigma_m=sigma_s,
            observation_sigma_m=sigma_o, total_emitted_amount=1.0,
            source_id=np.array("fast"), field_is_pointwise=np.array(True),
            config_sha256=np.array(sha256(args.config)),
        )
        animation_info = {
            "frames": len(frame_times), "physical_end_time_s": float(frame_times[-1]),
            "shape": list(fields.shape), "maximum_pointwise_concentration_per_m3": float(fields.max()),
            "quadrature_order": anim["quadrature_order"],
            "plane": "y=0; 3D solution, pointwise field (not observation average)",
            "display_window_is_boundary": False,
            "float_storage": "float32; quadrature uses float64",
        }

    fast_toward = by_case[("fast", "toward")]
    slow_toward = by_case[("slow", "toward")]
    comparison = {
        "toward_slow_to_fast_peak_ratio": slow_toward["peak_concentration_per_m3"] / fast_toward["peak_concentration_per_m3"],
        "toward_slow_to_fast_exposure_120s_ratio": slow_toward["exposure_120s_s_per_m3"] / fast_toward["exposure_120s_s_per_m3"],
        "toward_slow_to_fast_infinite_exposure_ratio": 1.0,
        "no_mean_drift_fast_tail_fraction_after120s": 1 - by_case[("fast", "no_mean_drift")]["fraction_of_infinite_exposure_by_120s"],
        "maximum_canonical_finite_exposure_relative_numerical_error": max(
            row["finite_exposure_relative_numerical_error"] for row in summary_rows),
        "maximum_field_order128_vs256_absolute_difference_per_m3": max(
            row["absolute_difference_per_m3"] for row in spatial_checks),
        "sensitivity_cases": len(sensitivity_rows),
        "sensitivity_toward_120s_ratio_range": [
            min(r["exposure_120s_ratio_to_no_mean_drift"] for r in sensitivity_rows if r["angle_deg"] == 0),
            max(r["exposure_120s_ratio_to_no_mean_drift"] for r in sensitivity_rows if r["angle_deg"] == 0)],
        "sensitivity_transverse_120s_ratio_range": [
            min(r["exposure_120s_ratio_to_no_mean_drift"] for r in sensitivity_rows if r["angle_deg"] == 90),
            max(r["exposure_120s_ratio_to_no_mean_drift"] for r in sensitivity_rows if r["angle_deg"] == 90)],
        "sensitivity_away_120s_ratio_range": [
            min(r["exposure_120s_ratio_to_no_mean_drift"] for r in sensitivity_rows if r["angle_deg"] == 180),
            max(r["exposure_120s_ratio_to_no_mean_drift"] for r in sensitivity_rows if r["angle_deg"] == 180)],
    }
    summary = {
        "schema_version": 1, "model_id": config["model_id"],
        "config_sha256": sha256(args.config),
        "model_code_sha256": sha256(ROOT / "src/model.py"),
        "driver_code_sha256": sha256(Path(__file__)),
        "software": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "units": {"concentration": "m^-3 per unit total emitted amount", "exposure": "s m^-3 per unit total emitted amount"},
        "normalization": "Each source emits one unit over infinite time; no measured molar scale or tear conversion.",
        "geometry": geometry, "distance_m": distance,
        "diffusivity_m2_s": diffusivity, "flow_speed_m_s": speed,
        "effective_peclet_number": speed * distance / diffusivity,
        "source_parameters": profiles,
        "scenarios": {key: value.tolist() for key, value in scenarios.items()},
        "results": summary_rows, "comparison": comparison,
        "animation": animation_info, "assumptions": config["assumptions"],
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(comparison, indent=2), flush=True)
    print(f"Saved numerical outputs in {out}", flush=True)


if __name__ == "__main__":
    main()
