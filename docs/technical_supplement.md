# Technical supplement: source timing and transport of a normalized irritant

This supplement defines the computations used in *Why Onions Make Us Cry and Which Tricks Actually Help*. Their purpose is to distinguish the timing of chemical emission, transport through air, concentration near an observer, and the duration of that exposure. The calculations have no measured molar emission scale and no conversion from concentration to tear volume. The source time constants, dispersion coefficient, flow speeds, and geometry are illustrative inputs, recorded in `config/model_config.json` and `data/parameters.csv`.

The article's chemical and experimental findings come from the cited primary literature. None of the numerical parameters below was fitted to those studies. In particular, the two source profiles do not represent measured effects of refrigeration, blade sharpness, or cutting speed.

## 1. A unit source with two release stages

Let $P(t)$ be an accessible precursor inventory and $L(t)$ a retained irritant inventory, each divided by the eventual emitted amount. We impose two consecutive first-order stages with rates $a>0$ and $b>0$ and unit yield:

$$\frac{dP}{dt}=-aP,\qquad \frac{dL}{dt}=aP-bL,\qquad q(t)=bL(t),\qquad P(0)=1,\quad L(0)=0.$$

The rates have units $\mathrm{s}^{-1}$ and the normalized emission rate $q$ has units $\mathrm{s}^{-1}$. This is a reduced timing model. It does not identify individual enzyme reactions, saturation, volatile partition coefficients, or tissue losses. For unequal rates,

$$P(t)=e^{-at},\qquad L(t)=\frac{a}{b-a}(e^{-at}-e^{-bt}),\qquad q(t)=\frac{ab}{b-a}(e^{-at}-e^{-bt}),\qquad t\geq0.$$

The limiting expression at $a=b$ is $q(t)=a^2te^{-at}$. The implementation uses `expm1` to evaluate the unequal-rate expression without subtracting nearly equal exponentials. The released fraction $F_q(t)=\int_0^tq(s)\,ds$ satisfies

$$P(t)+L(t)+F_q(t)=1,\qquad \int_0^\infty q(t)\,dt=1.$$

For the fast profile, $a=0.5\,\mathrm{s}^{-1}$ and $b=0.25\,\mathrm{s}^{-1}$, which give time constants of 2 and 4 seconds. The slow profile uses $a=0.1\,\mathrm{s}^{-1}$ and $b=0.05\,\mathrm{s}^{-1}$, with time constants of 10 and 20 seconds. Thus $q_{\mathrm{slow}}(t)=q_{\mathrm{fast}}(t/5)/5$. Both eventually emit the same amount; the second spreads that release over five times as long. At 120 seconds the fast profile has released essentially all of its amount and the slow profile has released 99.5049%.

## 2. A three-dimensional field in unbounded air

Write the normalized concentration as $C(\mathbf x,t)=c(\mathbf x,t)/M$, where $M$ is the total amount eventually emitted. If a measured $M$ in moles were available, multiplication by $M$ would recover concentration in $\mathrm{mol}\,\mathrm{m}^{-3}$. Here $M$ remains unspecified, and the reported $C$ has units $\mathrm{m}^{-3}$ per unit total emitted amount. The transport equation is

$$\frac{\partial C}{\partial t}+\mathbf u\cdot\nabla C=D_{\mathrm{eff}}\nabla^2C-\lambda C+q(t)\phi_{\sigma_s}(\mathbf x),\qquad C(\mathbf x,0)=0.$$

The velocity $\mathbf u$ is spatially uniform and fixed in time. The effective dispersion coefficient $D_{\mathrm{eff}}>0$ has units $\mathrm{m}^2\,\mathrm{s}^{-1}$. It represents an imposed isotropic spread, not a measured molecular diffusivity for the onion lachrymatory factor. The field describes a passive vapour-like scalar; it does not model liquid ejection, droplet inertia, or settling. The optional loss coefficient $\lambda\geq0$ has units $\mathrm{s}^{-1}$; the main calculation sets it to zero. The normalized spatial source is

$$\phi_{\sigma_s}(\mathbf x)=\frac{1}{(2\pi\sigma_s^2)^{3/2}}\exp\left(-\frac{|\mathbf x|^2}{2\sigma_s^2}\right),\qquad \int_{\mathbb R^3}\phi_{\sigma_s}\,d^3x=1.$$

The Gaussian has finite width and infinite support. Its coordinate standard deviation $\sigma_s=0.03\,\mathrm{m}$ is not a hard source radius. Its centre is the origin. The mathematical domain is all of $\mathbb R^3$, and the field decays at spatial infinity. There is no floor, cutting board, impermeable wall, body, exhaust inlet, return flow, or buoyant thermal plume in this model. The window shown in the animation is a crop of the field and imposes no boundary conditions. The nonzero velocities below describe transport directions relative to an observer; they are not a computed arrangement of a kitchen fan.

The comparison with $\mathbf u=0$ is called **no mean drift**, since the imposed effective dispersion still spreads the scalar. Calling this physically still molecular air would misidentify the coefficient.

For a unit instantaneous emission, the solution after an age $\tau\geq0$ is a Gaussian whose centre has moved by $\mathbf u\tau$ and whose coordinate variance has grown by $2D_{\mathrm{eff}}\tau$. A Gaussian observation weight of coordinate standard deviation $\sigma_o$ adds its variance to that of the source. The resulting observation kernel is

$$K(\mathbf r,\tau)=\frac{\exp\left[-\frac{|\mathbf r-\mathbf u\tau|^2}{2(\sigma_s^2+\sigma_o^2+2D_{\mathrm{eff}}\tau)}-\lambda\tau\right]}{\left[2\pi(\sigma_s^2+\sigma_o^2+2D_{\mathrm{eff}}\tau)\right]^{3/2}}.$$

The displayed spatial field uses $\sigma_o=0$, so each pixel samples the pointwise three-dimensional field in the plane $y=0$. The concentration history used for exposure uses $\sigma_o=0.01\,\mathrm{m}$, a normalized mathematical spatial average about $\mathbf r=(0.3,0,0.4)\,\mathrm m$. This weight describes neither the surface area of an eye nor uptake by a tear film. These two forms of output are deliberately identified in the saved data and captions.

Convolution over the earlier source history gives the observation concentration:

$$C_e(t)=\int_0^tq(s)K(\mathbf r,t-s)\,ds.$$

The field is nonnegative. With no transport loss its spatial integral equals the amount emitted by that time. For a fixed loss coefficient,

$$\int_{\mathbb R^3}C(\mathbf x,t)\,d^3x=\int_0^tq(s)e^{-\lambda(t-s)}\,ds.$$

Uniform advection redistributes this amount without creating or removing it. The loss term removes material only when $\lambda>0$.

## 3. The four transport comparisons

The centre-to-centre distance is $r=|\mathbf r|=0.5\,\mathrm m$. The main inputs are $D_{\mathrm{eff}}=0.003\,\mathrm{m}^2\,\mathrm{s}^{-1}$ and a nonzero-flow speed $U=0.05\,\mathrm{m}\,\mathrm{s}^{-1}$. The effective Peclet number $Ur/D_{\mathrm{eff}}$ is 8.3333. Because the denominator is an effective dispersion coefficient, this number describes the chosen coarse transport model rather than molecular transport alone.

| Scenario | Velocity $(u_x,u_y,u_z)$ in m/s | Relation to observation point |
| --- | --- | --- |
| No mean drift | $(0,0,0)$ | Effective dispersion alone |
| Toward | $(0.03,0,0.04)$ | Parallel to source-to-observer displacement |
| Away | $(-0.03,0,-0.04)$ | Opposite to source-to-observer displacement |
| Transverse | $(0,0.05,0)$ | Perpendicular to displacement, out of the displayed slice |

All four use the same fast source and the same dispersion coefficient. In particular, an added mean flow does not increase turbulent mixing or alter evaporation in this comparison. Such couplings would require another model and appropriate data.

## 4. Finite exposure and eventual exposure

The exposure proxy through a time $T$ is

$$E(T)=\int_0^TC_e(t)\,dt.$$

It has units $\mathrm{s}\,\mathrm{m}^{-3}$ per unit eventual emitted amount. Neither its integral nor its peak concentration is an absorbed ocular dose, an irritation score, or a tear count. Interchanging the finite integrals yields a second expression useful for numerical verification:

$$E(T)=\int_0^TK(\mathbf r,\tau)F_q(T-\tau)\,d\tau.$$

The eventual exposure is especially useful for the source-timing comparison. Since $q$ and $K$ are nonnegative, Tonelli's theorem permits the interchange of integration, and the unit source normalization gives

$$E(\infty)=\int_0^\infty\int_0^tq(s)K(\mathbf r,t-s)\,ds\,dt=\left(\int_0^\infty q(s)\,ds\right)\left(\int_0^\infty K(\mathbf r,\tau)\,d\tau\right)=\int_0^\infty K(\mathbf r,\tau)\,d\tau.$$

The slow and fast profiles therefore have the same eventual exposure whenever the source amount, transport kernel, observation position, and loss rule are fixed. This identity also holds for the optional stationary first-order loss. It does not hold as a general claim about onions: a treatment may change total release, a person may finish and leave, airflow may vary, and the biological response may depend on concentration history rather than its integral.

For the point-source limit $\sigma_s=\sigma_o=0$ and $r>0$, the time integral can be evaluated in closed form:

$$E_{\mathrm{point}}(\infty)=\frac{1}{4\pi D_{\mathrm{eff}}r}\exp\left[\frac{\mathbf u\cdot\mathbf r-r\sqrt{|\mathbf u|^2+4D_{\mathrm{eff}}\lambda}}{2D_{\mathrm{eff}}}\right].$$

To obtain it, expand $|\mathbf r-\mathbf u\tau|^2$, take the factor $\exp[\mathbf u\cdot\mathbf r/(2D_{\mathrm{eff}})]$ outside the integral, and evaluate the remaining integral of $\tau^{-3/2}\exp[-A/\tau-B\tau]$, with $A=r^2/(4D_{\mathrm{eff}})$ and $B=|\mathbf u|^2/(4D_{\mathrm{eff}})+\lambda$. This identity is an analytic benchmark; the production calculation retains the nonzero Gaussian widths.

For no mean drift and no loss, the finite-width result is also explicit. With $\sigma^2=\sigma_s^2+\sigma_o^2$,

$$E_0(\infty)=\frac{\operatorname{erf}[r/(\sqrt{2}\sigma)]}{4\pi D_{\mathrm{eff}}r},\qquad r>0.$$

At the source centre its continuous limit is $1/[(2\pi)^{3/2}D_{\mathrm{eff}}\sigma]$. These expressions check the source regularization and avoid a singular point-source value.

## 5. Results used in the article

The following entries use the fast source. The reported finite-window values come from the saved concentration histories; the adaptive-integral reference agrees to the accuracy described below. Values are normalized per unit total emission.

| Scenario | Peak concentration, $\mathrm{m}^{-3}$ | Peak time, s | $E(120)$, $\mathrm{s}\,\mathrm{m}^{-3}$ | $E(120)$ relative to no mean drift | $E(\infty)$, $\mathrm{s}\,\mathrm{m}^{-3}$ |
| --- | ---: | ---: | ---: | ---: | ---: |
| No mean drift | 0.538203 | 21.6875 | 28.9422 | 1.00000 | 53.0516 |
| Toward | 3.60565 | 12.6750 | 52.1819 | 1.80297 | 52.1819 |
| Away | 0.00104174 | 12.3375 | 0.0149003 | 0.000514830 | 0.0149003 |
| Transverse | 0.0612298 | 12.5000 | 0.881020 | 0.0304406 | 0.881021 |

The very small away-flow and transverse ratios follow from the imposed uniform direction and the selected ratio of drift to dispersion. They are not percentages measured for a household fan. Changing dispersion, geometry, source motion, or return flow can substantially change them.

The toward case increases exposure over the first two minutes while bringing material past the observation position sooner. Its eventual exposure is slightly below the no-drift value in the finite-width model. The point-source, zero-loss limit has equal eventual exposures for no drift and flow directly toward the observer; their different time histories still give different finite-window exposures. Reporting only one integration window would conceal this distinction.

For no mean drift, the impulse kernel has a $t^{-3/2}$ long-time tail, and its remaining time integral decreases as $T^{-1/2}$. The fast-source exposure captured by 120 seconds is only 54.5549% of the eventual value. Adaptive integration gives captured fractions of 70.6629% by 300 seconds, 85.1822% by 1,200 seconds, and 94.8518% by 10,000 seconds. These long tails belong to an unbounded, lossless, fixed-observer model and should not be read as a prediction of lingering irritation in a ventilated room.

For the toward-flow source-timing comparison:

| Quantity | Fast profile | Slow profile |
| --- | ---: | ---: |
| Peak concentration, $\mathrm{m}^{-3}$ | 3.60565 | 1.21410 |
| Peak time, s | 12.6750 | 25.3125 |
| Exposure through 120 s, $\mathrm{s}\,\mathrm{m}^{-3}$ | 52.1819 | 51.7413 |
| Eventual exposure, $\mathrm{s}\,\mathrm{m}^{-3}$ | 52.1819 | 52.1819 |

The slower release lowers the computed peak to 33.6722% of the fast-profile peak, but preserves eventual exposure. Its slightly lower 120-second exposure reflects release and transport still in progress. This comparison demonstrates why a lower peak does not by itself establish less accumulated exposure or fewer tears.

## 6. Sensitivity calculations

`results/sensitivity.csv` contains 189 cases formed from $D_{\mathrm{eff}}\in\{0.001,0.003,0.01\}\,\mathrm{m}^2\,\mathrm{s}^{-1}$, $U\in\{0.02,0.05,0.1\}\,\mathrm{m}\,\mathrm{s}^{-1}$, $r\in\{0.3,0.5,0.8\}\,\mathrm m$, and seven angles from $0^\circ$ to $180^\circ$. Every finite exposure uses the same fast source and 120-second window. Each ratio uses a no-drift denominator at the same dispersion and distance.

Across the 27 combinations of speed, distance, and dispersion, the toward-flow two-minute ratio ranges from 1.1650 to 10.4385. Transverse ratios range from approximately $5.05\times10^{-16}$ to 0.86685, and away-flow ratios from approximately $3.02\times10^{-32}$ to 0.64502. Extreme small values occur where the model imposes persistent drift against a remote observation point with weak dispersion. Real flow fluctuations and return paths are not represented, so these numbers cannot establish near-perfect protection. The ranges disclose how strongly the numerical effect depends on assumed transport; they are not confidence intervals.

`results/loss_sensitivity.csv` repeats the four directions and both source profiles at illustrative loss rates of 0, 0.02, and $0.1\,\mathrm{s}^{-1}$. These are not measurements of lachrymatory-factor degradation. They test the effect of removing older material during transport. Source-timing invariance of eventual exposure remains valid because the same stationary kernel is used for both profiles.

No probability distribution is assigned to any parameter. No unsupported reduction factor is assigned to goggles, chilling, water, blade sharpness, or a domestic extractor. Their evidence is assessed in the article and research ledger.

## 7. Numerical procedure and checks

The calculation evaluates an analytic spatial kernel and integrates over release time. It is not a discretized computational-fluid-dynamics simulation. There is no pressure solver, spatial transport mesh, or finite computational box whose walls could affect the solution.

Concentration histories use a 0.0125-second grid, a discrete convolution evaluated by FFT, and endpoint corrections that make the convolution a composite trapezoidal integral. Accumulated exposure uses the same quadrature. Small negative roundoff from the FFT is clipped only after a tolerance check; the kernel and source themselves are nonnegative. Peak times are sampled grid maxima, not continuous optimization results.

The driver recomputes histories at steps of 0.1, 0.05, 0.025, and 0.0125 seconds and compares each finite exposure with the independently evaluated expression $\int_0^TK(\tau)F_q(T-\tau)\,d\tau$. The largest relative error in a canonical 120-second exposure is $1.66\times10^{-6}$, or approximately 0.000166%. The full table is `results/time_convergence.csv`. That small integration error describes numerical agreement within the assumed equations and says nothing about experimental accuracy.

Spatial fields use 128-point Gauss–Legendre quadrature in release age at each saved time. Repeating selected source, observer, and off-axis locations with 256 points changes concentration by at most $1.71\times10^{-12}\,\mathrm{m}^{-3}$ across the saved checks. The sampled positions and times appear in `results/field_quadrature_convergence.csv`. Fields are computed in double precision and stored in the animation archive as single-precision arrays. The observation histories and summary tables retain double precision.

The independent numerical reviewer supplies the separate tests and report under `tests/` and `qa/`; those checks include source inventories, equal-rate and near-equal-rate limits, Gaussian mass and moments, analytic integrated-kernel limits, adaptive time integration, and transport symmetries. The review record, rather than this description of the numerical design, states which checks passed in the delivered package.

## 8. Reproduction and data files

From the repository root, run:

```bash
python -m src.run_simulations
```

An alternate output directory can be set with `--output-dir`. The driver uses `config/model_config.json` by default and accepts `--config` for another input file. The canonical run used Python 3.12.14, NumPy 2.3.5, and SciPy 1.17.0. It requires no internet connection or external dataset and contains no random sampling. The figure-production command is documented in the main README.

| File | Contents |
| --- | --- |
| `results/time_histories.csv` | Both source profiles and all four scenarios; concentration and cumulative exposure on the canonical grid |
| `results/source_histories.csv` | Emission rate, precursor, retained amount, and cumulative release |
| `results/summary.csv` | Peaks, 120-second exposures, eventual exposures, normalizations, and quadrature errors |
| `results/summary.json` | Machine-readable results, inputs, software versions, assumptions, and input/code hashes |
| `results/animation_fields.npz` | Pointwise 3D field sampled in the $y=0$ plane, frame times, coordinates, velocities, and metadata |
| `results/time_convergence.csv` | Temporal refinement against adaptive-integral exposure references |
| `results/field_quadrature_convergence.csv` | 128-versus-256-node field checks |
| `results/tail_convergence.csv` | Finite observation windows through 10,000 seconds and their fractions of eventual exposure |
| `results/sensitivity.csv` | The 189 dispersion, speed, distance, and direction comparisons |
| `results/loss_sensitivity.csv` | Optional stationary-loss comparisons |

These files contain model outputs and parameter provenance, not experimental measurements. The saved configuration and code hashes identify the calculation that produced the numbers cited in the article.
