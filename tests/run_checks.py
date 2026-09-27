"""Run independent tests and audit the saved files; write a machine-readable log.

Run after ``python -m src.run_simulations`` from the repository root:
    python tests/run_checks.py
"""

from __future__ import annotations

import csv
import hashlib
import io
import json
import platform
import sys
import unittest
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy
from scipy.integrate import quad

from test_model_independent import (
    DIFFUSIVITY, DIRECTIONS, POSITION, PROBE_WIDTH, SOURCE_WIDTH,
    reference_concentration, reference_cumulative, reference_exposure,
    reference_finite_source_integral, reference_kernel, reference_release,
)


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def check_relative(actual, expected, tolerance, absolute=0):
    np.testing.assert_allclose(actual, expected, rtol=tolerance, atol=absolute)
    return abs(float(actual) - float(expected)) / max(abs(float(expected)), 1e-300)


def audit_saved_outputs():
    summary_path = ROOT / "results/summary.json"
    summary = json.loads(summary_path.read_text())
    config = json.loads((ROOT / "config/model_config.json").read_text())
    expected_paths = {
        "config_sha256": ROOT / "config/model_config.json",
        "model_code_sha256": ROOT / "src/model.py",
        "driver_code_sha256": ROOT / "src/run_simulations.py",
    }
    for key, path in expected_paths.items():
        if digest(path) != summary[key]:
            raise AssertionError(f"Saved results have a stale {key}")
    if config["history"]["time_step_s"] != 0.0125:
        raise AssertionError("This review is tied to canonical dt=0.0125 s")

    rates_by_source = {"fast": (0.5, 0.25), "slow": (0.1, 0.05)}
    velocities = {name: np.asarray(value) for name, value in summary["scenarios"].items()}
    stored_summary = {
        (record["source_id"], record["scenario_id"]): record
        for record in summary["results"]
    }
    summary_checks = []
    for key, record in stored_summary.items():
        source_name, scenario = key
        velocity = velocities[scenario]
        rates = rates_by_source[source_name]
        independent_finite = reference_exposure(120, velocity, rates)
        independent_infinite = reference_finite_source_integral(
            POSITION, velocity, DIFFUSIVITY, np.hypot(SOURCE_WIDTH, PROBE_WIDTH)
        )
        finite_error = check_relative(
            record["exposure_120s_s_per_m3"], independent_finite, 3e-6
        )
        check_relative(record["exposure_120s_quad_reference_s_per_m3"],
                       independent_finite, 2e-9)
        infinite_error = check_relative(record["infinite_exposure_s_per_m3"],
                                        independent_infinite, 2e-8)
        check_relative(record["emitted_fraction_by_120s"],
                       reference_cumulative(120, *rates), 2e-12)
        summary_checks.append({
            "source_id": source_name, "scenario_id": scenario,
            "independent_exposure_120s_s_per_m3": independent_finite,
            "independent_infinite_exposure_s_per_m3": independent_infinite,
            "history_exposure_relative_error": finite_error,
            "infinite_exposure_relative_error": infinite_error,
        })

    # Audit CSV serialization, peak selections, and accumulated integrals.
    histories = defaultdict(list)
    for record in rows(ROOT / "results/time_histories.csv"):
        histories[(record["source_id"], record["scenario_id"])].append(record)
    if set(histories) != set(stored_summary):
        raise AssertionError("History and summary scenarios differ")
    history_count = 0
    for key, records in histories.items():
        history_count += len(records)
        time = np.array([float(row["time_s"]) for row in records])
        concentration = np.array([float(row["concentration_per_m3"]) for row in records])
        accumulated = np.array([float(row["cumulative_exposure_s_per_m3"])
                                for row in records])
        if not (np.isfinite(concentration).all() and np.all(concentration >= 0)):
            raise AssertionError(f"Invalid concentration history in {key}")
        np.testing.assert_allclose(np.diff(time), 0.0125, rtol=0, atol=1e-12)
        record = stored_summary[key]
        maximum_index = int(np.argmax(concentration))
        check_relative(record["peak_concentration_per_m3"],
                       concentration[maximum_index], 2e-13)
        check_relative(record["peak_time_s"], time[maximum_index], 2e-13)
        check_relative(record["exposure_120s_s_per_m3"],
                       np.trapezoid(concentration, time), 2e-12)
        check_relative(accumulated[-1], record["exposure_120s_s_per_m3"], 2e-13)

    source_records = rows(ROOT / "results/source_histories.csv")
    source_mass_errors = []
    for record in source_records:
        inventories = [float(record[column]) for column in
                       ("precursor_fraction", "retained_fraction", "emitted_fraction")]
        source_mass_errors.append(abs(sum(inventories) - 1))
        if min(inventories) < -1e-13 or source_mass_errors[-1] > 2e-12:
            raise AssertionError("Source history violates unit material balance")

    # The finite-width closed form checks values much smaller than ordinary
    # absolute integration tolerances in the high-Peclet upwind cases.
    sensitivity = rows(ROOT / "results/sensitivity.csv")
    max_sensitivity_error = 0.0
    for record in sensitivity:
        diffusion = float(record["diffusivity_m2_s"])
        radius = float(record["distance_m"])
        speed = float(record["flow_speed_m_s"])
        angle = np.deg2rad(float(record["angle_deg"]))
        direction = POSITION / np.linalg.norm(POSITION)
        position = radius * direction
        velocity = speed * (np.cos(angle) * direction
                            + np.sin(angle) * np.array([0, 1, 0]))
        expected = reference_finite_source_integral(
            position, velocity, diffusion, np.hypot(SOURCE_WIDTH, PROBE_WIDTH)
        )
        error = check_relative(float(record["infinite_exposure_s_per_m3"]),
                               expected, 2e-8, absolute=1e-50)
        max_sensitivity_error = max(max_sensitivity_error, error)
        finite = quad(
            lambda age: reference_kernel(
                age, position=position, velocity=velocity, diffusivity=diffusion
            ) * reference_cumulative(120 - age),
            0, 120, epsabs=1e-300, epsrel=2e-10, limit=300,
        )[0]
        check_relative(float(record["exposure_120s_s_per_m3"]), finite, 2e-8,
                       absolute=1e-50)

    max_loss_error = 0.0
    loss_rows = rows(ROOT / "results/loss_sensitivity.csv")
    for record in loss_rows:
        loss_rate = float(record["assumed_loss_rate_per_s"])
        expected = reference_finite_source_integral(
            POSITION, velocities[record["scenario_id"]], DIFFUSIVITY,
            np.hypot(SOURCE_WIDTH, PROBE_WIDTH), loss_rate,
        )
        error = check_relative(float(record["infinite_exposure_s_per_m3"]),
                               expected, 2e-8)
        max_loss_error = max(max_loss_error, error)

    # Verify stored animation samples against independent quadrature. The
    # archive stores pointwise y=0 fields as float32, unlike the smoothed probe.
    fields = np.load(ROOT / "results/animation_fields.npz")
    if fields["config_sha256"].item() != summary["config_sha256"]:
        raise AssertionError("Animation archive has a different config hash")
    if not bool(fields["field_is_pointwise"]):
        raise AssertionError("Expected pointwise field in animation archive")
    values = fields["concentration_per_m3"]
    if not (np.isfinite(values).all() and np.all(values >= 0)):
        raise AssertionError("Nonfinite or negative animation field")
    field_errors = []
    sample_points = [(0, 0), (0.3, 0.4), (-0.2, 0.1)]
    for scenario_index, scenario in enumerate(fields["scenario_ids"]):
        for time in (1, 10, 30, 60):
            time_index = int(np.argmin(abs(fields["times_s"] - time)))
            for x_target, z_target in sample_points:
                xi = int(np.argmin(abs(fields["x_m"] - x_target)))
                zi = int(np.argmin(abs(fields["z_m"] - z_target)))
                position = np.array([fields["x_m"][xi], 0, fields["z_m"][zi]])
                expected = quad(
                    lambda age: reference_kernel(
                        age, position=position, velocity=velocities[str(scenario)],
                        probe_width=0,
                    ) * reference_release(time - age),
                    0, time, epsabs=1e-14, epsrel=2e-10, limit=300,
                )[0]
                actual = float(values[scenario_index, time_index, zi, xi])
                relative_error = check_relative(actual, expected, 2e-6, absolute=1e-12)
                if expected > 1e-8:
                    field_errors.append(relative_error)

    snapshot_errors = []
    for scenario, velocity in DIRECTIONS.items():
        mapped_scenario = "no_mean_drift" if scenario == "no_drift" else scenario
        records = histories[("fast", mapped_scenario)]
        for time in (3, 10, 30, 120):
            expected = reference_concentration(time, velocity)
            actual = float(records[int(round(time / 0.0125))]["concentration_per_m3"])
            error = abs(actual - expected)
            snapshot_errors.append({
                "scenario_id": mapped_scenario, "time_s": time,
                "absolute_error_per_m3": error,
                "relative_error": error / max(abs(expected), 1e-300),
                "relative_error_is_resolved": expected > 1e-8,
            })
    return {
        "status": "passed",
        "summary_cases_checked": len(summary_checks),
        "history_rows_checked": history_count,
        "source_history_rows_checked": len(source_records),
        "maximum_source_inventory_mass_error": max(source_mass_errors),
        "sensitivity_cases_checked": len(sensitivity),
        "loss_sensitivity_cases_checked": len(loss_rows),
        "animation_samples_checked": 48,
        "maximum_history_exposure_relative_error": max(
            row["history_exposure_relative_error"] for row in summary_checks
        ),
        "maximum_sensitivity_infinite_exposure_relative_error": max_sensitivity_error,
        "maximum_loss_infinite_exposure_relative_error": max_loss_error,
        "maximum_animation_sample_relative_error_above_1e_minus8": max(field_errors),
        "summary_cases": summary_checks,
        "history_snapshot_errors": snapshot_errors,
        "production_hashes": {key: summary[key] for key in expected_paths},
    }


def main():
    output = io.StringIO()
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), pattern="test_*.py")
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    audit = {"status": "not_run_because_tests_failed"}
    audit_failure = None
    if result.wasSuccessful():
        try:
            audit = audit_saved_outputs()
        except Exception as error:
            audit_failure = f"{type(error).__name__}: {error}"
            audit = {"status": "failed", "error": audit_failure}
    report = {
        "schema_version": 1,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "status": "passed" if result.wasSuccessful() and audit["status"] == "passed" else "failed",
        "review_scope": "Numerical verification and saved-output consistency; no empirical onion or physiological validation.",
        "software": {"python": platform.python_version(), "numpy": np.__version__,
                     "scipy": scipy.__version__},
        "unit_tests": {"run": result.testsRun, "failures": len(result.failures),
                       "errors": len(result.errors), "skipped": len(result.skipped)},
        "saved_output_audit": audit,
        "reviewer_file_sha256": {
            path.relative_to(ROOT).as_posix(): digest(path) for path in (
                ROOT / "tests/test_model_independent.py", Path(__file__).resolve()
            )
        },
    }
    log = output.getvalue() + "\nSaved-output audit: " + audit["status"] + "\n"
    if audit_failure:
        log += audit_failure + "\n"
    (ROOT / "qa/test_log.txt").write_text(log, encoding="utf-8")
    (ROOT / "qa/check_results.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(log, end="")
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    sys.exit(main())
