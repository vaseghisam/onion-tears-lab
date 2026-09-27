"""Independent analytic, ODE, and adaptive-quadrature checks of the model.

Run from the repository root with ``python -m unittest discover -s tests -v``.
The production convolution uses a uniform temporal grid; reference integrals
here use adaptive quadrature. Source kinetics are also checked by integrating
the precursor/retained/emitted material-balance ODEs independently.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad, solve_ivp
from scipy.special import erf, erfc
from scipy.stats import multivariate_normal

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import model  # noqa: E402


POSITION = np.array([0.30, 0.0, 0.40])
DIFFUSIVITY = 0.003
SOURCE_WIDTH = 0.03
PROBE_WIDTH = 0.01
SPEED = 0.05
TOWARD = SPEED * POSITION / np.linalg.norm(POSITION)
DIRECTIONS = {
    "no_drift": np.zeros(3),
    "toward": TOWARD,
    "away": -TOWARD,
    "transverse": np.array([0.0, SPEED, 0.0]),
}


def reference_kernel(age, position=POSITION, velocity=None, diffusivity=DIFFUSIVITY,
                     source_width=SOURCE_WIDTH, probe_width=PROBE_WIDTH):
    """Independent use of SciPy's normalized 3-D normal probability density."""
    if age < 0:
        return 0.0
    if velocity is None:
        velocity = np.zeros(3)
    variance = source_width ** 2 + probe_width ** 2 + 2 * diffusivity * age
    return multivariate_normal.pdf(
        position, mean=np.asarray(velocity) * age, cov=variance * np.eye(3)
    )


def reference_release(time, first_rate=0.5, second_rate=0.25):
    if time < 0:
        return 0.0
    if first_rate == second_rate:
        return first_rate ** 2 * time * np.exp(-first_rate * time)
    return first_rate * second_rate * (
        np.exp(-first_rate * time) - np.exp(-second_rate * time)
    ) / (second_rate - first_rate)


def reference_cumulative(time, first_rate=0.5, second_rate=0.25):
    if time < 0:
        return 0.0
    if first_rate == second_rate:
        return 1 - (1 + first_rate * time) * np.exp(-first_rate * time)
    return 1 - (
        second_rate * np.exp(-first_rate * time)
        - first_rate * np.exp(-second_rate * time)
    ) / (second_rate - first_rate)


def reference_concentration(time, velocity, rates=(0.5, 0.25)):
    return quad(
        lambda emitted_at: reference_release(emitted_at, *rates)
        * reference_kernel(time - emitted_at, velocity=velocity),
        0, time, epsabs=1e-12, epsrel=2e-10, limit=300,
    )[0]


def reference_exposure(horizon, velocity, rates=(0.5, 0.25)):
    # Reversing integration order eliminates one integral and makes this
    # independent of the production concentration-history discretization.
    return quad(
        lambda age: reference_kernel(age, velocity=velocity)
        * reference_cumulative(horizon - age, *rates),
        0, horizon, epsabs=1e-12, epsrel=2e-10, limit=300,
    )[0]


def reference_finite_source_integral(position, velocity, diffusivity,
                                     effective_width, loss_rate=0.0):
    """Closed erfc expression independent of production adaptive integration.

    Substitute t = age + sigma**2/(2D) in the Gaussian kernel integral.
    The remaining integral is an incomplete inverse-Gaussian integral.
    Test cases avoid the removable R=0 singularity and extreme overflow.
    """
    shift_time = effective_width ** 2 / (2 * diffusivity)
    shifted_position = np.asarray(position) + np.asarray(velocity) * shift_time
    radius = np.linalg.norm(shifted_position)
    if radius == 0:
        raise ValueError("this reference formula requires shifted radius > 0")
    a = radius ** 2 / (4 * diffusivity)
    b = np.dot(velocity, velocity) / (4 * diffusivity) + loss_rate
    x = np.sqrt(b * shift_time)
    y = np.sqrt(a / shift_time)
    prefactor_exponent = (loss_rate * shift_time
                          + np.dot(velocity, shifted_position) / (2 * diffusivity))
    root_exponent = 2 * np.sqrt(a * b)
    return (
        np.exp(prefactor_exponent - root_exponent) * erfc(x - y)
        - np.exp(prefactor_exponent + root_exponent) * erfc(x + y)
    ) / (8 * np.pi * diffusivity * radius)


def production_kernel(age, position=POSITION, velocity=None,
                      diffusivity=DIFFUSIVITY, source_width=SOURCE_WIDTH,
                      probe_width=PROBE_WIDTH):
    if velocity is None:
        velocity = np.zeros(3)
    return model.transport_kernel(age, position, velocity, diffusivity,
                                  source_width, probe_width)


def production_history(step=0.0125, horizon=120.0, velocity=None,
                       rates=(0.5, 0.25), multiplier=1.0):
    if velocity is None:
        velocity = np.zeros(3)
    times = np.linspace(0, horizon, int(round(horizon / step)) + 1)
    emission = multiplier * model.source_rate(times, *rates)
    concentrations = model.concentration_history(
        times, emission, POSITION, velocity, DIFFUSIVITY,
        SOURCE_WIDTH, PROBE_WIDTH,
    )
    return times, emission, concentrations


class SourceChecks(unittest.TestCase):
    def test_release_against_independent_material_balance_ode(self):
        sample_times = np.linspace(0, 100, 151)
        for first_rate, second_rate in ((0.5, 0.25), (0.1, 0.05),
                                        (0.25, 0.25), (0.25, 0.250000000025)):
            with self.subTest(rates=(first_rate, second_rate)):
                def equations(_time, state):
                    precursor, retained, _emitted = state
                    conversion = first_rate * precursor
                    release = second_rate * retained
                    return [-conversion, conversion - release, release]

                solution = solve_ivp(
                    equations, (0, 100), [1.0, 0.0, 0.0],
                    t_eval=sample_times, rtol=1e-11, atol=2e-13,
                )
                self.assertTrue(solution.success)
                np.testing.assert_allclose(solution.y.sum(axis=0), 1,
                                           rtol=0, atol=3e-13)
                expected_emission = second_rate * solution.y[1]
                actual = model.source_rate(sample_times, first_rate, second_rate)
                np.testing.assert_allclose(actual, expected_emission,
                                           rtol=2e-8, atol=2e-11)
                cumulative = model.source_cumulative(
                    sample_times, first_rate, second_rate
                )
                np.testing.assert_allclose(cumulative, solution.y[2],
                                           rtol=2e-8, atol=2e-10)
                inventories = np.asarray(model.source_inventory(
                    sample_times, first_rate, second_rate
                ))
                np.testing.assert_allclose(inventories, solution.y,
                                           rtol=2e-8, atol=2e-10)
                np.testing.assert_allclose(inventories.sum(axis=0), 1,
                                           rtol=0, atol=2e-12)

    def test_unit_yield_and_mean_emission_time(self):
        for rates in ((0.5, 0.25), (0.1, 0.05), (0.2, 0.2)):
            with self.subTest(rates=rates):
                total = quad(lambda time: model.source_rate(time, *rates),
                             0, np.inf, epsabs=1e-11, epsrel=1e-11)[0]
                mean = quad(lambda time: time * model.source_rate(time, *rates),
                            0, np.inf, epsabs=1e-10, epsrel=1e-11)[0]
                self.assertAlmostEqual(total, 1.0, delta=2e-10)
                self.assertAlmostEqual(mean, sum(1 / rate for rate in rates),
                                       delta=2e-8)

    def test_nonnegative_release_and_finite_window_yield(self):
        times = np.linspace(0, 1000, 1001)
        self.assertTrue(np.all(model.source_rate(times, 0.1, 0.05) >= 0))
        self.assertAlmostEqual(float(model.source_rate(0, 0.1, 0.05)), 0.0)
        self.assertAlmostEqual(float(model.source_cumulative(120, 0.1, 0.05)),
                               0.9950486398590206, delta=2e-12)


class KernelChecks(unittest.TestCase):
    def test_spatial_mass_mean_and_variance(self):
        # Tensor-product Gauss-Legendre quadrature over seven standard
        # deviations loses less than 8e-12 Gaussian mass in three dimensions.
        nodes, weights = leggauss(32)
        xyz = np.array(np.meshgrid(nodes, nodes, nodes, indexing="ij"))
        xyz = xyz.reshape(3, -1).T
        mass_weights = np.einsum("i,j,k->ijk", weights, weights, weights).ravel()
        velocity = np.array([0.03, -0.02, 0.01])
        for age in (0.0, 8.0):
            with self.subTest(age=age):
                variance = SOURCE_WIDTH ** 2 + PROBE_WIDTH ** 2 + 2 * DIFFUSIVITY * age
                half_width = 7 * np.sqrt(variance)
                expected_mean = age * velocity
                points = expected_mean + half_width * xyz
                densities = np.array([
                    production_kernel(age, point, velocity) for point in points
                ])
                integrated_weights = mass_weights * half_width ** 3 * densities
                mass = integrated_weights.sum()
                self.assertAlmostEqual(float(mass), 1.0, delta=2e-9)
                mean = (integrated_weights[:, None] * points).sum(axis=0) / mass
                covariance = np.einsum(
                    "i,ij,ik->jk", integrated_weights,
                    points - expected_mean, points - expected_mean
                ) / mass
                np.testing.assert_allclose(mean, expected_mean, rtol=0, atol=2e-9)
                np.testing.assert_allclose(covariance, variance * np.eye(3),
                                           rtol=2e-8, atol=2e-10)

    def test_independent_probability_density_and_observation_averaging(self):
        for age in (0, 0.25, 1, 5, 20, 120):
            for velocity in DIRECTIONS.values():
                with self.subTest(age=age, velocity=velocity):
                    actual = production_kernel(age, velocity=velocity)
                    expected = reference_kernel(age, velocity=velocity)
                    np.testing.assert_allclose(actual, expected, rtol=3e-13, atol=1e-40)
        # A Gaussian observation average must add variance to the source width.
        effective_width = np.hypot(SOURCE_WIDTH, PROBE_WIDTH)
        actual = production_kernel(7, velocity=TOWARD)
        combined = production_kernel(7, velocity=TOWARD,
                                     source_width=effective_width, probe_width=0)
        self.assertAlmostEqual(float(actual), float(combined), delta=2e-12)

    def test_reflection_and_opposite_flow_ratio(self):
        for age in (0.5, 5, 20):
            forward = production_kernel(age, velocity=TOWARD)
            reflected = production_kernel(age, -POSITION, -TOWARD)
            reverse = production_kernel(age, velocity=-TOWARD)
            np.testing.assert_allclose(forward, reflected, rtol=2e-13)
            variance = SOURCE_WIDTH ** 2 + PROBE_WIDTH ** 2 + 2 * DIFFUSIVITY * age
            expected_ratio = np.exp(2 * age * np.dot(TOWARD, POSITION) / variance)
            np.testing.assert_allclose(forward / reverse, expected_ratio, rtol=2e-12)

    def test_zero_flow_infinite_integral_at_and_away_from_source(self):
        effective_width = np.hypot(SOURCE_WIDTH, PROBE_WIDTH)
        for distance in (0.0, 0.01, 0.5, 1.2):
            position = np.array([distance, 0, 0])
            if distance == 0:
                expected = 1 / ((2 * np.pi) ** 1.5 * DIFFUSIVITY * effective_width)
            else:
                expected = erf(distance / (np.sqrt(2) * effective_width)) / (
                    4 * np.pi * DIFFUSIVITY * distance
                )
            integrated = quad(
                lambda age: reference_kernel(age, position=position),
                0, np.inf, epsabs=1e-9, epsrel=1e-10, limit=300,
            )[0]
            actual = model.integrated_kernel(
                position, np.zeros(3), DIFFUSIVITY, SOURCE_WIDTH, PROBE_WIDTH
            )
            np.testing.assert_allclose(integrated, expected, rtol=3e-9)
            np.testing.assert_allclose(actual, expected, rtol=3e-9)

    def test_point_source_limit_and_flow_alignment(self):
        radius = np.linalg.norm(POSITION)
        for velocity in DIRECTIONS.values():
            expected = np.exp(
                (np.dot(velocity, POSITION) - radius * np.linalg.norm(velocity))
                / (2 * DIFFUSIVITY)
            ) / (4 * np.pi * DIFFUSIVITY * radius)
            actual = model.point_source_integral(POSITION, velocity, DIFFUSIVITY)
            finite = model.integrated_kernel(
                POSITION, velocity, DIFFUSIVITY, 1e-5, 0
            )
            np.testing.assert_allclose(actual, expected, rtol=2e-12)
            np.testing.assert_allclose(finite, expected, rtol=3e-7)
        # Point-source downstream infinite-time exposure equals no drift,
        # so a universal claim that flow always increases exposure would fail.
        self.assertAlmostEqual(
            model.point_source_integral(POSITION, TOWARD, DIFFUSIVITY),
            model.point_source_integral(POSITION, np.zeros(3), DIFFUSIVITY),
            delta=2e-11,
        )

    def test_finite_source_integral_independent_quadrature(self):
        expected_values = {
            "no_drift": 53.05164769729845,
            "toward": 52.18194855471978,
            "away": 0.014900337694556103,
            "transverse": 0.881020987083583,
        }
        for name, velocity in DIRECTIONS.items():
            actual = model.integrated_kernel(
                POSITION, velocity, DIFFUSIVITY, SOURCE_WIDTH, PROBE_WIDTH
            )
            np.testing.assert_allclose(actual, expected_values[name], rtol=2e-8)

    def test_fixed_loss_mass_and_point_source_limit(self):
        loss_rate = 0.03
        age = 20.0
        variance = SOURCE_WIDTH ** 2 + PROBE_WIDTH ** 2 + 2 * DIFFUSIVITY * age
        centre = TOWARD * age
        # Spherical integration about the transported centre directly checks
        # remaining mass for the isotropic kernel, including prescribed loss.
        mass = quad(
            lambda radius: 4 * np.pi * radius ** 2 * model.transport_kernel(
                age, centre + np.array([radius, 0, 0]), TOWARD,
                DIFFUSIVITY, SOURCE_WIDTH, PROBE_WIDTH, loss_rate=loss_rate
            ),
            0, 10 * np.sqrt(variance), epsabs=1e-11, epsrel=1e-11,
        )[0]
        self.assertAlmostEqual(mass, np.exp(-loss_rate * age), delta=2e-10)
        radius = np.linalg.norm(POSITION)
        for velocity in DIRECTIONS.values():
            expected = np.exp(
                (np.dot(velocity, POSITION)
                 - radius * np.sqrt(np.dot(velocity, velocity)
                                    + 4 * DIFFUSIVITY * loss_rate))
                / (2 * DIFFUSIVITY)
            ) / (4 * np.pi * DIFFUSIVITY * radius)
            actual = model.point_source_integral(
                POSITION, velocity, DIFFUSIVITY, loss_rate=loss_rate
            )
            finite = model.integrated_kernel(
                POSITION, velocity, DIFFUSIVITY, 1e-5, 0,
                loss_rate=loss_rate,
            )
            np.testing.assert_allclose(actual, expected, rtol=2e-12)
            np.testing.assert_allclose(finite, expected, rtol=4e-7)

    def test_finite_source_closed_form_across_parameter_sweep(self):
        direction = POSITION / np.linalg.norm(POSITION)
        for diffusivity in (0.001, 0.003, 0.01):
            for speed in (0.02, 0.05, 0.1):
                for distance in (0.3, 0.5, 0.8):
                    for sign in (-1, 0, 1):
                        position = direction * distance
                        velocity = direction * speed * sign
                        expected = reference_finite_source_integral(
                            position, velocity, diffusivity,
                            np.hypot(SOURCE_WIDTH, PROBE_WIDTH),
                        )
                        actual = model.integrated_kernel(
                            position, velocity, diffusivity,
                            SOURCE_WIDTH, PROBE_WIDTH,
                        )
                        with self.subTest(diffusivity=diffusivity, speed=speed,
                                          distance=distance, sign=sign):
                            np.testing.assert_allclose(actual, expected,
                                                       rtol=2e-8, atol=1e-50)


class FieldChecks(unittest.TestCase):
    def test_field_quadrature_at_source_observer_and_off_axis(self):
        positions = np.array([
            [0, 0, 0], POSITION, [-0.15, 0.1, 0.2], [0.4, 0.15, 0.5]
        ], dtype=float)
        for time, rates in ((10.0, (0.5, 0.25)), (60.0, (0.1, 0.05))):
            for velocity in (np.zeros(3), TOWARD, DIRECTIONS["transverse"]):
                expected = np.array([
                    quad(
                        lambda age: reference_kernel(
                            age, position=position, velocity=velocity,
                            probe_width=0,
                        ) * reference_release(time - age, *rates),
                        0, time, epsabs=1e-10, epsrel=1e-10, limit=300,
                    )[0] for position in positions
                ])
                values = model.field_at_time(
                    time, positions, velocity, DIFFUSIVITY, SOURCE_WIDTH,
                    *rates, quadrature_order=128, sigma_observer=0,
                )
                refined = model.field_at_time(
                    time, positions, velocity, DIFFUSIVITY, SOURCE_WIDTH,
                    *rates, quadrature_order=256, sigma_observer=0,
                )
                with self.subTest(time=time, velocity=velocity):
                    np.testing.assert_allclose(values, expected, rtol=3e-5, atol=1e-9)
                    np.testing.assert_allclose(refined, expected, rtol=3e-7, atol=1e-9)

    def test_figure_field_and_observation_history_agree(self):
        times, _, history = production_history(velocity=TOWARD)
        for time in (5, 10, 30, 60):
            field_average = model.field_at_time(
                time, POSITION, TOWARD, DIFFUSIVITY, SOURCE_WIDTH,
                0.5, 0.25, quadrature_order=128, sigma_observer=PROBE_WIDTH,
            )
            index = int(round(time / (times[1] - times[0])))
            np.testing.assert_allclose(history[index], field_average,
                                       rtol=3e-4, atol=1e-10)


class ConvolutionChecks(unittest.TestCase):
    def test_constant_emission_checks_both_quadrature_endpoints(self):
        # Unlike the article release history, constant release has q(0)>0.
        # An observation at the origin also has K(0)>0, so both trapezoid
        # endpoint corrections materially affect this test.
        times = np.linspace(0, 2, 4001)
        actual = model.concentration_history(
            times, np.ones_like(times), np.zeros(3), np.zeros(3),
            DIFFUSIVITY, SOURCE_WIDTH, PROBE_WIDTH,
        )
        sigma = np.hypot(SOURCE_WIDTH, PROBE_WIDTH)
        expected = (1 / sigma - 1 / np.sqrt(sigma ** 2 + 2 * DIFFUSIVITY * times)) / (
            (2 * np.pi) ** 1.5 * DIFFUSIVITY
        )
        np.testing.assert_allclose(actual[1:], expected[1:], rtol=4e-6, atol=1e-8)

    def test_history_against_adaptive_quadrature(self):
        for name, velocity in DIRECTIONS.items():
            times, _emission, actual = production_history(velocity=velocity)
            for time in (3.0, 10.0, 30.0, 120.0):
                with self.subTest(flow=name, time=time):
                    index = int(round(time / (times[1] - times[0])))
                    expected = reference_concentration(time, velocity)
                    np.testing.assert_allclose(actual[index], expected,
                                               rtol=3e-4, atol=1e-11)

    def test_finite_exposure_and_time_refinement(self):
        for name, velocity in DIRECTIONS.items():
            reference = reference_exposure(120, velocity)
            exposures = []
            for step in (0.05, 0.025, 0.0125):
                times, _emission, concentrations = production_history(
                    step=step, velocity=velocity
                )
                exposures.append(np.trapezoid(concentrations, times))
            with self.subTest(flow=name):
                np.testing.assert_allclose(exposures[-1], reference, rtol=3e-5)
                self.assertLess(abs(exposures[-1] - reference),
                                abs(exposures[0] - reference) + 1e-11)
                self.assertLess(abs(exposures[1] - exposures[-1]) / reference,
                                5e-4)

    def test_zero_source_scaling_nonnegativity_and_causality(self):
        times, _emission, positive = production_history(velocity=TOWARD)
        _, _, zero = production_history(velocity=TOWARD, multiplier=0)
        _, _, doubled = production_history(velocity=TOWARD, multiplier=2)
        np.testing.assert_allclose(zero, 0, rtol=0, atol=1e-15)
        np.testing.assert_allclose(doubled, 2 * positive, rtol=2e-13, atol=1e-13)
        self.assertGreaterEqual(float(np.min(positive)), -2e-12)
        self.assertAlmostEqual(float(positive[0]), 0.0, delta=2e-12)
        # A ten-second delay must not create any concentration beforehand.
        delayed_source = np.zeros_like(times)
        offset = int(round(10 / (times[1] - times[0])))
        delayed_source[offset:] = model.source_rate(times[:-offset], 0.5, 0.25)
        delayed = model.concentration_history(
            times, delayed_source, POSITION, TOWARD, DIFFUSIVITY,
            SOURCE_WIDTH, PROBE_WIDTH,
        )
        np.testing.assert_allclose(delayed[:offset], 0, rtol=0, atol=2e-12)
        np.testing.assert_allclose(delayed[offset:], positive[:-offset],
                                   rtol=2e-10, atol=2e-12)

    def test_equal_yield_timing_and_window_effect(self):
        fast_total = quad(lambda time: model.source_rate(time, 0.5, 0.25),
                          0, np.inf)[0]
        slow_total = quad(lambda time: model.source_rate(time, 0.1, 0.05),
                          0, np.inf)[0]
        infinite_response = model.integrated_kernel(
            POSITION, np.zeros(3), DIFFUSIVITY, SOURCE_WIDTH, PROBE_WIDTH
        )
        self.assertAlmostEqual(fast_total * infinite_response,
                               slow_total * infinite_response, delta=2e-8)
        fast_120 = reference_exposure(120, np.zeros(3), (0.5, 0.25))
        slow_120 = reference_exposure(120, np.zeros(3), (0.1, 0.05))
        self.assertLess(slow_120, fast_120)
        self.assertAlmostEqual(fast_120, 28.942262292893897, delta=2e-8)
        self.assertAlmostEqual(slow_120, 25.742278523107366, delta=2e-8)
        self.assertAlmostEqual(fast_120 / infinite_response,
                               0.545548791585767, delta=2e-9)


if __name__ == "__main__":
    unittest.main()
