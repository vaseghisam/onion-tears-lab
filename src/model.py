"""Normalized, free-space transport for the onion article.

This is a constant-coefficient three-dimensional advection-diffusion model,
not a measured kitchen-flow or physiological model. Source amount is one
arbitrary unit, so concentrations have units m^-3 per emitted unit.
"""

from __future__ import annotations

from functools import lru_cache
import math
import numpy as np
from scipy.integrate import quad
from scipy.signal import fftconvolve
from scipy.special import erf


def _positive(value: float, name: str) -> float:
    value = float(value)
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be finite and positive")
    return value


def _vector(value, name: str) -> np.ndarray:
    value = np.asarray(value, dtype=float)
    if value.shape != (3,) or not np.isfinite(value).all():
        raise ValueError(f"{name} must be a finite three-vector")
    return value


def source_rate(t, k_production: float, k_release: float):
    """Unit-yield two-stage release density, zero at negative times (s^-1).

    P'=-aP, L'=aP-bL, P(0)=1, L(0)=0 and q=bL. The stable symmetric
    formula handles equal or very nearly equal rates without subtraction
    of nearly equal exponentials. This is an illustrative source history.
    """
    a, b = sorted((_positive(k_production, "k_production"),
                   _positive(k_release, "k_release")))
    t = np.asarray(t, dtype=float)
    positive_t = np.maximum(t, 0.0)
    delta = b - a
    if delta == 0:
        density = a * a * positive_t * np.exp(-a * positive_t)
    else:
        density = a * b * np.exp(-a * positive_t) * (
            -np.expm1(-delta * positive_t) / delta)
    return np.where(t >= 0, density, 0.0)


def source_cumulative(t, k_production: float, k_release: float):
    """Exact cumulative released fraction for ``source_rate``."""
    a, b = sorted((_positive(k_production, "k_production"),
                   _positive(k_release, "k_release")))
    t = np.asarray(t, dtype=float)
    positive_t = np.maximum(t, 0.0)
    delta = b - a
    retained_part = (positive_t if delta == 0 else
                     -np.expm1(-delta * positive_t) / delta)
    fraction = -np.expm1(-a * positive_t) - (
        a * np.exp(-a * positive_t) * retained_part)
    return np.where(t >= 0, np.clip(fraction, 0.0, 1.0), 0.0)


def source_inventory(t, k_production: float, k_release: float):
    """Precursor, retained material and released fraction (all unitless)."""
    _positive(k_production, "k_production")
    _positive(k_release, "k_release")
    t = np.asarray(t, dtype=float)
    precursor = np.exp(-k_production * np.maximum(t, 0.0))
    retained = source_rate(t, k_production, k_release) / k_release
    released = source_cumulative(t, k_production, k_release)
    return precursor, retained, released


def transport_kernel(age, position, velocity, diffusivity: float,
                     sigma_source: float, sigma_observer: float = 0.0,
                     loss_rate: float = 0.0):
    """Impulse concentration at one position after the specified ages.

    ``position`` is measured from the source centre. Source and observation
    weights are normalized isotropic 3D Gaussians; their coordinate
    variances add. sigma_observer=0 gives a pointwise field value. Negative
    ages have zero concentration. The Gaussian's infinite spatial support
    is intentional: sigma is a standard deviation, not a hard boundary.
    """
    position = _vector(position, "position")
    velocity = _vector(velocity, "velocity")
    diffusivity = _positive(diffusivity, "diffusivity")
    sigma_source = _positive(sigma_source, "sigma_source")
    if not math.isfinite(float(sigma_observer)) or sigma_observer < 0:
        raise ValueError("sigma_observer must be finite and nonnegative")
    if not math.isfinite(float(loss_rate)) or loss_rate < 0:
        raise ValueError("loss_rate must be finite and nonnegative")
    age = np.asarray(age, dtype=float)
    nonnegative_age = np.maximum(age, 0.0)
    variance = sigma_source**2 + sigma_observer**2 + 2 * diffusivity * nonnegative_age
    displacement = position - nonnegative_age[..., None] * velocity
    distance_sq = np.sum(displacement * displacement, axis=-1)
    values = np.exp(-distance_sq / (2 * variance) - loss_rate * nonnegative_age) / (
        2 * np.pi * variance)**1.5
    return np.where(age >= 0, values, 0.0)


def concentration_history(times, emission, position, velocity,
                          diffusivity: float, sigma_source: float,
                          sigma_observer: float = 0.0, loss_rate: float = 0.0):
    """Causal convolution on a uniform grid by composite trapezoid + FFT.

    No spatial mesh, box boundary or CFD solve is used. Discrete
    convolution is corrected at both integration endpoints to implement
    the trapezoidal rule. Only negative FFT roundoff is clipped.
    """
    times = np.asarray(times, dtype=float)
    emission = np.asarray(emission, dtype=float)
    if times.ndim != 1 or len(times) < 2 or emission.shape != times.shape:
        raise ValueError("times and emission must be equal-length 1D arrays")
    if not np.isfinite(times).all() or not np.isfinite(emission).all():
        raise ValueError("times and emission must be finite")
    dt = times[1] - times[0]
    if dt <= 0 or abs(times[0]) > 1e-12 or not np.allclose(
            np.diff(times), dt, atol=1e-12, rtol=1e-10):
        raise ValueError("times must start at zero and be uniformly increasing")
    if emission.min() < 0:
        raise ValueError("emission must be nonnegative")
    kernel = transport_kernel(times, position, velocity, diffusivity,
                              sigma_source, sigma_observer, loss_rate)
    values = dt * fftconvolve(emission, kernel, mode="full")[:len(times)]
    values -= 0.5 * dt * (emission[0] * kernel + kernel[0] * emission)
    tolerance = 1e-12 * max(1.0, float(np.max(np.abs(values))))
    if np.min(values) < -tolerance:
        raise FloatingPointError("convolution produced material negative values")
    values = np.maximum(values, 0.0)
    values[0] = 0.0
    return values


def point_source_integral(position, velocity, diffusivity: float,
                          loss_rate: float = 0.0) -> float:
    """Exact infinite-time impulse integral, sigma=0, r>0 (s m^-3).

    exp[(u.r-|r|*sqrt(|u|^2+4D*loss_rate))/(2D)]/(4*pi*D*|r|).
    This is a verification limit, not the finite-source calculation.
    """
    position = _vector(position, "position")
    velocity = _vector(velocity, "velocity")
    diffusivity = _positive(diffusivity, "diffusivity")
    if not math.isfinite(float(loss_rate)) or loss_rate < 0:
        raise ValueError("loss_rate must be finite and nonnegative")
    radius = float(np.linalg.norm(position))
    if radius == 0:
        raise ValueError("point-source integral is singular at its origin")
    decay_speed = np.sqrt(np.dot(velocity, velocity) + 4 * diffusivity * loss_rate)
    exponent = (np.dot(velocity, position) - decay_speed * radius) / (2 * diffusivity)
    return float(np.exp(exponent) / (4 * np.pi * diffusivity * radius))


def integrated_kernel(position, velocity, diffusivity: float,
                      sigma_source: float, sigma_observer: float = 0.0,
                      loss_rate: float = 0.0) -> float:
    """Infinite-time exposure from unit total release (s m^-3).

    Zero drift with zero loss uses the closed Gaussian-regularized
    Newtonian potential. Other cases use adaptive quadrature over
    [0,infinity).
    """
    position = _vector(position, "position")
    velocity = _vector(velocity, "velocity")
    diffusivity = _positive(diffusivity, "diffusivity")
    sigma_source = _positive(sigma_source, "sigma_source")
    if not math.isfinite(float(sigma_observer)) or sigma_observer < 0:
        raise ValueError("sigma_observer must be finite and nonnegative")
    if not math.isfinite(float(loss_rate)) or loss_rate < 0:
        raise ValueError("loss_rate must be finite and nonnegative")
    sigma = float(np.hypot(sigma_source, sigma_observer))
    radius = float(np.linalg.norm(position))
    if np.linalg.norm(velocity) == 0 and loss_rate == 0:
        if radius == 0:
            return 1.0 / ((2 * np.pi)**1.5 * diffusivity * sigma)
        return float(erf(radius / (np.sqrt(2) * sigma)) /
                     (4 * np.pi * diffusivity * radius))
    integral, error = quad(
        lambda age: float(transport_kernel(age, position, velocity, diffusivity,
                                          sigma_source, sigma_observer, loss_rate)),
        0, np.inf, epsabs=1e-300, epsrel=2e-11, limit=250)
    if error > 1e-7 * max(integral, 1e-300):
        raise RuntimeError(f"infinite integral did not meet tolerance: {error}")
    return float(integral)


def finite_exposure_quad(end_time: float, k_production: float, k_release: float,
                         position, velocity, diffusivity: float,
                         sigma_source: float, sigma_observer: float = 0.0,
                         loss_rate: float = 0.0) -> float:
    """Independent-in-time expression E(T)=int_0^T K(a) F_q(T-a) da."""
    if end_time <= 0:
        return 0.0
    value, _ = quad(
        lambda age: float(transport_kernel(age, position, velocity, diffusivity,
                                          sigma_source, sigma_observer, loss_rate) *
                          source_cumulative(end_time - age, k_production, k_release)),
        0, end_time, epsabs=1e-300, epsrel=2e-10, limit=250)
    return float(value)


@lru_cache(maxsize=None)
def _legendre(order: int):
    return np.polynomial.legendre.leggauss(order)


def field_at_time(time: float, positions, velocity, diffusivity: float,
                  sigma_source: float, k_production: float, k_release: float,
                  quadrature_order: int = 128, sigma_observer: float = 0.0,
                  loss_rate: float = 0.0):
    """Gaussian-quadrature concentration at an array (...,3) of positions."""
    positions = np.asarray(positions, dtype=float)
    if positions.shape[-1] != 3 or not np.isfinite(positions).all():
        raise ValueError("positions must have finite final dimension 3")
    velocity = _vector(velocity, "velocity")
    diffusivity = _positive(diffusivity, "diffusivity")
    sigma_source = _positive(sigma_source, "sigma_source")
    if sigma_observer < 0:
        raise ValueError("sigma_observer must be nonnegative")
    if not math.isfinite(float(loss_rate)) or loss_rate < 0:
        raise ValueError("loss_rate must be finite and nonnegative")
    _positive(k_production, "k_production")
    _positive(k_release, "k_release")
    if quadrature_order < 2:
        raise ValueError("quadrature_order must be at least 2")
    if time <= 0:
        return np.zeros(positions.shape[:-1], dtype=float)
    original_shape = positions.shape[:-1]
    points = positions.reshape(-1, 3)
    nodes, weights = _legendre(int(quadrature_order))
    ages = (nodes + 1) * float(time) / 2
    weights = weights * float(time) / 2
    variance = sigma_source**2 + sigma_observer**2 + 2 * diffusivity * ages
    r2 = np.sum(points * points, axis=1)
    r_dot_u = points @ velocity
    u2 = np.dot(velocity, velocity)
    distance_sq = r2[None, :] - 2 * ages[:, None] * r_dot_u[None, :] + (
        u2 * ages[:, None]**2)
    distance_sq = np.maximum(distance_sq, 0.0)
    kernel = np.exp(-distance_sq / (2 * variance[:, None]) - loss_rate * ages[:, None]) / (
        2 * np.pi * variance[:, None])**1.5
    temporal_weight = weights * source_rate(time - ages, k_production, k_release)
    return np.sum(temporal_weight[:, None] * kernel, axis=0).reshape(original_shape)
