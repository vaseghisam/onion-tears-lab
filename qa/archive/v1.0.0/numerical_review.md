# Independent numerical review

Status: passed on 24 September 2026. All 18 independent test methods passed, and the saved-output audit passed. No unresolved numerical issue was found in the released scenarios. The exact code and configuration hashes appear in `qa/check_results.json`.

This review concerns the numerical implementation and mathematical consequences of the stated transport model. It does not validate onion emission rates, effective mixing coefficients, household airflow, ocular dose, or tear production against measurements.

## Reviewer independence

The numerical reviewer has responsibility for `tests/`, this report, and `qa/check_results.json`. The modelling agent has responsibility for the production model and result-generation code. The review uses analytic identities and independent SciPy adaptive quadrature, rather than a second copy of the production time-discretization method.

## Mathematical checks specified before execution

For a normalized, isotropic Gaussian source and a normalized Gaussian observation weight, the variances add. If their standard deviations are $a_s$ and $a_e$, put $a^2=a_s^2+a_e^2$. The impulse response at displacement $\mathbf r$ and age $\tau\geq0$ is

$$H(\mathbf r,\tau)=\frac{\exp[-|\mathbf r-\mathbf u\tau|^2/(2(a^2+2D\tau))-\lambda\tau]}{[2\pi(a^2+2D\tau)]^{3/2}}.$$

Here $D>0$ is a prescribed effective diffusivity, $\mathbf u$ a constant velocity, and $\lambda\geq0$ a prescribed first-order loss rate. A finite Gaussian source already removes the point-source singularity. Gaussian observation weighting is a spatial average with infinite support; it must not be described as a sharply bounded eye-sized volume.

The kernel has spatial integral $e^{-\lambda\tau}$, mean displacement $\mathbf u\tau$, and covariance $(a^2+2D\tau)\mathbf I$ after normalization by its remaining mass. These are independent mass and moment checks.

For zero flow and zero loss, its infinite-time integral at $r=|\mathbf r|>0$ is

$$\int_0^\infty H(\mathbf r,\tau)\,d\tau=\frac{\operatorname{erf}[r/(\sqrt{2}a)]}{4\pi Dr}.$$

At $r=0$, the continuous limit is $1/[(2\pi)^{3/2}Da]$. At positive distance and $a\rightarrow0$, this becomes $1/(4\pi Dr)$.

For a point source, constant flow, and nonnegative loss, a second independent benchmark is

$$\int_0^\infty H_0(\mathbf r,\tau)\,d\tau=\frac{\exp[(\mathbf u\cdot\mathbf r-r\sqrt{|\mathbf u|^2+4D\lambda})/(2D)]}{4\pi Dr}.$$

The familiar opposite-flow exposure ratio $\exp(\mathbf u\cdot\mathbf r/D)$ applies to this point-source expression. A finite Gaussian source does not generally preserve that ratio. For the finite source, reflection gives $H(\mathbf r,\tau;\mathbf u)=H(-\mathbf r,\tau;-\mathbf u)$, while the same-position instantaneous ratio is $\exp[2\tau\mathbf u\cdot\mathbf r/(a^2+2D\tau)]$.

For a nonnegative emission history $q(t)$ and stationary transport,

$$c_e(t)=\int_0^t q(s)H(\mathbf r,t-s)\,ds.$$

Changing the order of integration gives

$$E_\infty=\left(\int_0^\infty q(s)\,ds\right)\left(\int_0^\infty H(\mathbf r,\tau)\,d\tau\right).$$

Equal emitted amounts therefore give equal infinite-time concentration integrals at the same position and under the same transport conditions. This conclusion needs time-independent transport and complete integration; it does not imply equal peaks, equal exposure during preparation, or equal tearing.

For a unit initial precursor amount and two lossless first-order stages with rates $k_1$ and $k_2$, the release history is

$$q(t)=\frac{k_1k_2}{k_2-k_1}(e^{-k_1t}-e^{-k_2t}).$$

Its total is one. At $k_1=k_2=k$, the continuous limit is $k^2t e^{-kt}$. These rate constants are scenario inputs unless supported by measured release data.

## Physical interpretation checks

The domain is all of three-dimensional space. No board, wall, human body, thermal plume, extraction hood, or room boundary is represented. A displayed plane is a slice through that three-dimensional field, not a two-dimensional transport solution. A prescribed uniform flow does not solve kitchen fluid dynamics. Any finite plotting extent crops the display; it is not a computational boundary and has no domain-convergence test.

An airflow described as directed toward the observation point must align with the complete source-to-observer displacement. For the proposed $(0.3,0,0.4)$ m position, horizontal flow along $x$ does not point toward the observer. The distinction matters because advective alignment controls the comparison.

Ideal no-flow diffusion has an algebraic concentration tail. In three dimensions and at zero loss, the exposure omitted after a late cutoff decreases only as the inverse square root of that cutoff. A finite-duration comparison and an infinite-time comparison must therefore have distinct labels and numbers.

## Independent finite-source formula for the sensitivity audit

The production code uses adaptive quadrature for the infinite-time finite-source integral with nonzero flow or loss. For an independent comparison, define $t_0=a^2/(2D)$, $\mathbf R=\mathbf r+\mathbf u t_0$, $A=|\mathbf R|^2/(4D)$, $B=|\mathbf u|^2/(4D)+\lambda$, and $C=\lambda t_0+\mathbf u\cdot\mathbf R/(2D)$. Substitution of $t=\tau+t_0$ gives, for $|\mathbf R|>0$,

$$\int_0^\infty H(\mathbf r,\tau)\,d\tau=\frac{e^{C-2\sqrt{AB}}\operatorname{erfc}(\sqrt{Bt_0}-\sqrt{A/t_0})-e^{C+2\sqrt{AB}}\operatorname{erfc}(\sqrt{Bt_0}+\sqrt{A/t_0})}{8\pi D|\mathbf R|}.$$

This formula checks all 189 saved angle, distance, speed, and diffusivity cases, including very small upwind values at large effective Péclet number. It also checks the 24 saved cases with the assumed loss rates $0$, $0.02$, and $0.1$ per second. These loss rates are sensitivity inputs, not measurements of the lifetime of onion lachrymatory factor in air.

## Execution results

Run from the repository root:

```bash
python -m unittest discover -s tests -v
python tests/run_checks.py
```

The second command runs the test suite and checks the saved files, then writes `qa/check_results.json` and `qa/test_log.txt`. The production files must already exist; regenerate them with `python -m src.run_simulations` if necessary. A mismatch between the recorded configuration or code hashes and the current files fails the saved-output audit.

| Check | Method and tolerance | Result |
| --- | --- | --- |
| Two-stage release, including equal and nearly equal rates | Independent integration of precursor, retained, and emitted inventories with SciPy `solve_ivp`; relative tolerance $2\times10^{-8}$ with stated small absolute floors | Passed |
| Source yield and mean release time | Adaptive integration to infinity; total one and mean $1/k_1+1/k_2$ | Passed |
| Spatial mass, mean, and covariance | Three-dimensional tensor Gauss–Legendre integration over seven standard deviations; mass tolerance $2\times10^{-9}$ | Passed |
| Kernel values and Gaussian observation averaging | SciPy normalized multivariate-normal density and variance-addition identity | Passed |
| Reflection and opposite-flow relation | Analytic finite-source identities | Passed |
| Infinite-time exposure | Zero-flow error-function expression, point-source limit, and finite-source complementary-error-function expression | Passed |
| Fixed first-order loss | Remaining mass $e^{-\lambda t}$ and analytic point-source limit | Passed |
| Time convolution | Independent adaptive quadrature at 3, 10, 30, and 120 seconds in four flow directions; relative tolerance $3\times10^{-4}$ and absolute tolerance $10^{-11}$ | Passed |
| Constant source and quadrature endpoints | Analytic concentration at the source; checks both nonzero endpoint contributions | Passed |
| Zero source, linear scaling, delayed-source causality, and nonnegative concentration | Direct limiting-case checks | Passed |
| Temporal refinement | Step sizes 0.05, 0.025, and 0.0125 seconds compared with independent adaptive exposure integrals | Passed |
| Figure-field quadrature | 128- and 256-node Gaussian quadrature versus adaptive integration at the source, observer, and off-axis points; also compare field and history with the same observation weight | Passed |
| Source scheduling | Equal infinite-time exposure for equal total source, with different finite-window exposure | Passed |

The canonical time step is 0.0125 seconds. An initial 0.025-second run differed from the independent concentration integral by up to approximately 0.040% at 3 seconds, narrowly above a preliminary 0.03% target; halving the step brought that maximum below 0.010%. This was ordinary quadrature error, and the step change was made before the saved production results were generated.

The largest relative error in the eight saved 120-second exposure integrals is $1.66\times10^{-6}$, or about 0.000166%. The 189 saved infinite-time sensitivity values differ from the independent closed expression by at most $1.70\times10^{-14}$ relative. These tolerances concern arithmetic and quadrature, not uncertainty in physical parameters.

The saved-output audit also checks all 76,808 history rows for finite nonnegative concentrations, uniform timestamps, correct maxima, and agreement between the final accumulated exposure and the summary. The 19,202 source-history rows satisfy the unit-inventory balance. All eight reported 120-second and infinite-time exposures were checked independently. The array archive was sampled at 48 scenario, time, and grid-position combinations; its largest relative discrepancy above a concentration of $10^{-8}$ per cubic metre per emitted unit was $5.60\times10^{-8}$, consistent with its float32 storage. The complete archive was checked for finite nonnegative values.

No finite-difference spatial solver is used. A finer display grid does not change an observation history or a saved exposure integral, because those are evaluated directly at the specified observation position with Gaussian weighting. Temporal quadrature and field quadrature were refined; a mesh-refinement claim for the transport solution would describe a computation that was not performed.

## Checked values and implications for the article

The following independent values use a unit total emission, source width 0.03 m, observation width 0.01 m, $D=0.003$ square metres per second, an observation displacement of $(0.3,0,0.4)$ m, flow speed 0.05 m/s where nonzero, and the fast release rates $(0.5,0.25)$ per second.

| Prescribed flow | Exposure through 120 s, s/m³ per emitted unit | Infinite-time exposure, s/m³ per emitted unit |
| --- | ---: | ---: |
| No mean drift | 28.9422623 | 53.0516477 |
| Toward the observer | 52.1819485 | 52.1819486 |
| Away from the observer | 0.01490034 | 0.01490034 |
| Transverse | 0.88102099 | 0.88102099 |

These are independent adaptive or closed-form reference values. The stored time-history integrations differ in their last few digits as quantified above. No mean drift has accumulated approximately 54.5549% of its infinite-time exposure by 120 seconds. Thus the large increase from flow toward the observer in the 120-second comparison must retain that time-window qualification. In this finite-source example, the infinite-time toward-flow integral is slightly below the no-drift integral.

For flow toward the observer, changing the source rates from $(0.5,0.25)$ to $(0.1,0.05)$ per second reduces the saved peak from 3.60565 to 1.21410 per cubic metre per emitted unit. The slower-to-faster peak ratio is approximately 0.33672, whereas the 120-second exposure ratio is approximately 0.99156. Their infinite-time exposures coincide. The slower source has emitted approximately 99.5049% of its eventual amount by 120 seconds. These source histories are hypothetical timing comparisons and are not a calibration of chilled and room-temperature onions.

## Limits of this approval

The numerical review supports the reproducibility and mathematical consistency of the supplied model and saved values. Parameter provenance and practical onion claims require the separate scientific review. The calculation does not establish the absolute airborne amount of lachrymatory factor, its chemical lifetime, the fraction carried by droplets, the uptake at an eye, or a percentage reduction in human tearing.

No household airflow has been measured or solved. The scenario sweep preserves the same free-space, linear, constant-coefficient transport assumptions and is not a statistical confidence interval. Any universal numerical recommendation about fan position, chilling, goggles, or tear prevention would exceed what these calculations check.
