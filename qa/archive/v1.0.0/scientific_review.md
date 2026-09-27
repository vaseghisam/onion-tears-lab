# Independent scientific review

Status: complete after correction and recheck; no unresolved scientific-interpretation blocker.

Review date: 24 September 2026. Reviewer: a separate scientific-review agent, distinct from the research, modelling, numerical-review, and visual-production agents. This record concerns the article's scientific interpretation and reader-facing claims. Numerical verification has its own report.

## Review criteria established before the manuscript

1. **Reaction sequence.** The account must distinguish isoalliin, the sulfenic-acid intermediate, and lachrymatory factor (LF). Alliinase and LF synthase perform different steps. Garlic's allicin cannot replace either onion intermediate. A schematic must identify omitted coproducts and cannot look like a complete balanced chemical equation if it is not one.
2. **Physiology.** An LF exposure study can establish a tear response under its stated conditions. It cannot establish a universal kitchen concentration threshold. No named molecular receptor or sulfuric-acid explanation should be asserted without direct evidence for that claim.
3. **Measured endpoints.** Droplet count, droplet volume, LF concentration in air, eye-region exposure, and tear production are separate quantities. Captions and practical advice must retain those distinctions.
4. **Cutting experiment.** Describe the published mechanical intervention using its actual cutting conditions. Its droplet findings support a sharp-knife recommendation as a mechanical inference; they do not supply a measured percentage reduction in tears.
5. **Temperature.** Do not turn one mechanical cooling comparison into a conclusion about net LF exposure or tears. Temperature can alter tissue mechanics, chemical production, partition, and the time of release. Distinguish absent evidence from evidence of no effect.
6. **Air transport.** A free-space Gaussian transport calculation is a conditional test of source-to-observer geometry. It is not kitchen CFD, a measured fan installation, or an onion emission model. Prescribed constant velocity, source width, effective mixing, normalization, eye position, and averaging must be explicit.
7. **Exposure.** A concentration-time integral is an exposure proxy, not absorbed dose, tear volume, injury, or discomfort. State its units and observation interval. Any delayed-release comparison must check the longer-time integral.
8. **Protection.** A sealed barrier and directed airflow have physical rationales. In the absence of relevant intervention trials, label practical recommendations as physical inference and avoid numerical efficacy. Ordinary open spectacles and a face shield do not enclose the eyes against vapour. Do not recommend contact lenses as protective equipment.
9. **Folklore.** A wet surface beside a board does not automatically intercept the route to the eyes. A lack of controlled evidence located for a method must not become proof that it never works. Keep soaking, rinsing, and cutting under water distinct.
10. **Plots and animation.** Numerical plots must match saved output, normalization, time windows, and scales. Any slice of a 3D field must state the slice and any projection of points outside it. A tracer image must not be presented as visible experimental fumes or tears.
11. **Sensitivity.** A scenario envelope is not a confidence interval. Rankings conditional on selected geometry cannot become universal remedy rankings. An exactly equal result caused by symmetry should be explained.
12. **Transparency.** The article must identify which work was done for this package, what was taken from the literature, which checks were completed, and which empirical measurements were not made.

## Early source checks

The published version of Wu et al., *Droplet outbursts from onion cutting* (2025), DOI [10.1073/pnas.2512779122](https://doi.org/10.1073/pnas.2512779122), was read independently at the publisher, including its methods and temperature discussion. The methods establish droplet and mechanical endpoints; they do not report an LF assay at the eyes or a human tearing comparison. The cooling experiment used 1°C for 12 h. Its velocity comparison was nonsignificant; its larger-volume observation was qualitative and accompanied by a call for further controlled work. These findings must not be recast as proof that refrigeration worsens crying.

The earlier arXiv manuscript, [2505.06016](https://arxiv.org/abs/2505.06016), was inspected as a version comparison; the published paper governs the article's attribution.

The review also located the 2004 ARVO abstract on human tear secretion. The lead editor identified the later peer-reviewed Higashihara et al. article, DOI [10.1007/s10384-009-0786-0](https://doi.org/10.1007/s10384-009-0786-0), whose publisher abstract was then independently read. Its 91-volunteer study supports reflex tearing after synthesized-LF exposure and variation with age; it does not provide a general household dose-response calibration. The published article should govern the physiology discussion instead of the meeting abstract.

## Final manuscript and visual audit

The complete first `article.md` draft was read, including the displayed equations, results table, and every caption. After revision, the complete manuscript and all eight references were read again. The full `docs/technical_supplement.md` was also read. Mathematical claims about stationary linear transport, source normalization, and the infinite-time integral were checked against the stated model and the independent numerical-review specification. The completed visual checks are recorded below.

The draft consistently distinguishes published observations, this project's conditional calculations, and practical inferences. Its discussion of molecular vapour versus liquid spray, hypothetical release rates versus actual refrigeration, and exposure versus human tears passes the conceptual check. The source bibliography agrees with the independently checked published records. The title promises help rather than guaranteed prevention.

The following corrections were requested before release:

| Location | Required correction | Reason | Status |
| --- | --- | --- | --- |
| Physiology study paragraph | Replace “increase in the tear meniscus” with “increase in the curvature radius of the tear meniscus” | Preserve the actual measured observable | Corrected and rechecked |
| Eady paragraph | Replace the claim about “material released from damaged tissue” with a statement about LF formation after tissue damage | Avoid suggesting an airborne emission measurement | Corrected and rechecked |
| First transport-comparison paragraph | Define the Gaussian widths as coordinate standard deviations | A Gaussian “width” has several conventions | Corrected and rechecked |
| Before transport results | Identify the baseline source as the 2 s and 4 s release history introduced below | Establish the source before interpreting its finite-time result | Corrected and rechecked |
| Eye-protection recommendation and closing routine | Use “well-sealed” rather than simply “close-fitting” | Vented goggles may fit closely while allowing vapour entry | Corrected and rechecked |
| Chilling paragraph | Mark the volume observation as qualitative and preserve its limited experimental status | Do not imply a settled net-exposure result | Corrected and rechecked |
| Folklore paragraph and Figure 3 gum row | Acknowledge limited patent evidence or narrow the absence claim to adequate peer-reviewed evidence | Patent EP2014333A1 reports a small controlled menthol-gum comparison, so an unrestricted “no controlled evidence” statement is false | Corrected and rechecked |

The regenerated Figure 1 and Figure 3 were inspected and contain the requested corrections, including Figure 3's qualified gum/patent row. Figure 2 and the transport static fallback were inspected at full size. The GIF was decoded and frames at physical times 0, 18, 30, and 60 seconds were inspected; the common logarithmic scale, observation centre, plane labels, and source/flow behavior agree with the article. MP4 metadata confirms a 6 fps, H.264-compatible yuv420p display with 70 encoded frames, including holds. The pointwise field image remains distinct from the Gaussian observation average. The article's four rounded exposure-table values and its approximately 55% no-drift accumulation fraction agree with `results/summary.json` and `results/summary.csv`. The article now identifies the preliminary patent report, limits the absence claim appropriately, and cites it as reference 8. The additional Figure 2 sentence was checked against the saved output: the reported normalized peaks 3.61 and 1.21 m^-3 and the 120-second exposure ratio 0.992 are correctly rounded. No scientific-interpretation blocker remains in the reviewed version.

The patent lead was supplied by the research agent and independently checked at [EP2014333A1, Test Examples, Test 1 and Table 1](https://patents.google.com/patent/EP2014333A1/en). It describes ten adults and a menthol-gum comparison with a preparation lacking the cooling agent. Sparse protocol reporting and the absence of independent confirmation in this search prevent a reliable household recommendation. Neither its formulations nor its effect sizes are adopted as advice.

## Final scope and conclusion

The article, captions, and visuals agree about what is measured, inferred, and simulated. The package supports an explanatory article with conditional transport calculations. It does not establish experimentally calibrated prevention percentages, actual kitchen flow, droplet-versus-vapour dominance at the eyes, or a universal human dose-response law. These limits are retained in the article and supplement. Independent numerical execution and release-integrity checks remain the responsibility of their separate reports. This scientific review is an AI team check, not external peer review.

Reviewed manuscript SHA-256: `8bcecb8cacbf63e406d61039f33b96d2e8ad1d2d012350203237c36d5dca567d`.
