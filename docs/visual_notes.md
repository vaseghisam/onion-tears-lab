# Visual production and interpretation

The original project diagrams, plots and table were generated with Matplotlib. Figures 1 and 3 and the unnumbered featured painting were supplied in the author's final manuscript and are included as third-party images; their source URLs and credits are recorded in `assets/asset_sources.json`. The animation is a display of saved numerical results, not experimental footage. No generative image model was used for the scientific assets.

## Assets and sources

| Asset | Input | Purpose |
| --- | --- | --- |
| `feature_peeling_onions.png` | Author-supplied image of Lilly Martin Spencer's painting | Unnumbered featured artwork |
| `figure_01_lfs_structure.png` | Author-supplied image attributed to reference [1] | LFS structure and reaction illustration |
| `figure_03_sulfur_pathway.png` | Author-supplied image attributed to reference [3] | Wider sulfur reaction pathway |
| `table_01_air_motion.png` and `.svg` | Four fast-source cases in `results/summary.json` | 120-second exposure comparison |
| `figure_02_chemistry.png` and `.svg` | Verified primary-source reaction pathway; research and scientific-review checks | Show the two enzyme-catalysed steps and the subsequent route to irritation |
| `figure_04_release_exposure.png` and `.svg` | `results/time_histories.csv`, `results/summary.csv`, `config/model_config.json` | Compare release, observation concentration and cumulative exposure for two equal-total-release histories |
| `figure_05_remedies.png` and `.svg` | Research-reviewed qualitative remedy assessment | Keep physical reasoning, measured outcomes and unresolved efficacy distinct |
| `animation_01_transport.gif` and `.mp4` | `results/animation_fields.npz` | Show the same three-dimensional source under four prescribed uniform velocities |
| `animation_01_transport_static.png` and `.svg` | The same saved field, at the nearest animation time to the toward-flow peak in `time_histories.csv` | Supply a static fallback for the animation |
| `visual_metadata.json` | Production settings extracted from the saved arrays | Record frame count, duration, colour limits and selected snapshot time |

## Chemistry figure

Alliinase and lachrymatory-factor synthase label catalysed reactions; neither enzyme is drawn as a reaction product. Coproducts and competing reactions are omitted. The diagram is not an atom-balanced chemical equation and does not depict molecular structures or cellular dimensions.

The checked pathway is isoalliin to 1-propenesulfenic acid to syn-propanethial S-oxide, followed by transport and eye irritation/reflex tearing. The research ledger identifies `Imai2002`, `Eady2008`, `Silvaroli2017` and `Higashihara2010`. No specific sensory receptor or sulfuric-acid mechanism is asserted.

## Source and exposure figure

The shorter and longer source histories have the same eventual total release. Their time constants come from the shared model configuration. Both use the same prescribed flow toward the observation centre and the same Gaussian spatial observation average.

The third panel divides cumulative exposure by the saved common infinite-time limit. Its dotted line is that mathematical limit, not the exposure measured by 120 seconds. The release histories are illustrative and must not be interpreted as measured effects of chilling or blade choice.

## Remedy table

The table contains qualitative findings rather than an efficacy ranking. The wording was reviewed against the claim ledger and the scientific-review comments. In particular:

- The physical barrier inference concerns well-sealed goggles. Ordinary spectacles and vented or poorly sealed goggles are not equivalent.
- The cutting study concerns droplet production. It does not measure gas-phase lachrymatory factor at the eye or tear reduction.
- The low-lachrymatory-factor cultivar study includes chemical measurements and a sensory procedure that involved chewing, not a chopping trial.
- The water, chilling, root and folklore rows retain the uncertainty of the documented search. Failure to locate a controlled trial is not a demonstration that a method never helps.
- A small menthol-gum comparison described in a patent is acknowledged in the final row; it does not provide adequate peer-reviewed support for a general remedy recommendation.

Study source IDs for the two experimental remedy rows are `Wu2025` and `Kato2016`; the article gives their numbered references.

## Air-transport display

Every panel displays the same $y=0$ slice of a three-dimensional field. The transverse velocity is perpendicular to that plane. A plume can leave the plane while remaining present elsewhere in three-dimensional space. The perpendicular-flow symbol uses $+y$ into the page when $x$ points right and $z$ points up.

The concentration scale is logarithmic, with one fixed minimum and maximum across all panels and animation frames. Values below the common display minimum appear white. There is no per-panel or per-frame normalization. Exact limits are recorded in `assets/visual_metadata.json`.

The source square and open observation marker identify Gaussian centres. The observation marker lies in the displayed plane and is not a hard-edged eye surface or finite sampling volume. The displayed field is the pointwise slice; concentration histories in Figure 4 use the Gaussian observation average.

The calculation occupies all of three-dimensional space. Negative plotted height is not a model of transport through a board or floor: no such boundary exists in this idealization. Effective mixing is prescribed, and the no-mean-drift panel is not a molecular-diffusion model of a motionless real kitchen.

The MP4 runs at six encoded frames per second, with equally spaced one-second physical snapshots plus opening and closing holds. GIF timing is rounded to the format's centisecond units and its playback duration differs slightly; the visible clock in both formats reports the same physical time. Actual GIF duration and frame count are recorded in the visual metadata. Image interpolation uses nearest cells, and plotting extents preserve the centres of the saved grid points.

## Reproduction and visual checks

After the numerical outputs have been generated, run:

```bash
python src/make_visuals.py
```

The command regenerates the project's PNG, SVG, GIF and MP4 assets. It preserves the three imported images, whose supplied bytes are retained rather than regenerated. The MP4 uses H.264 with a browser-compatible `yuv420p` pixel format; FFmpeg must be installed to reproduce it. `--no-animation` skips GIF/MP4 encoding while regenerating all static visuals. `--only chemistry`, `--only profiles`, `--only remedies`, `--only table` and `--only transport` select one production group.

The final visual review checks full-size figures, representative animation frames, common scales, physical-time labels, source and observation positions, the perpendicular-flow label, text overlap, and consistency with article captions. Numerical verification and physical-model limitations are reported separately in the project QA and technical documentation.

Completed checks: all four static figures were viewed at full resolution; animation frames at physical times 0, 5, 13, 25, 40 and 60 seconds were inspected. The selected static transport frame is at 13 seconds. The animation's logarithmic limits are $10^{-3}$ and $10^2$ per cubic metre per unit total release. H.264/yuv420p encoding, the complete 70-frame MP4 stream, and the GIF's complete 61 distinct-time frames were verified. The scientific reviewer independently inspected the source/exposure and transport figures and checked their interpretation against the saved summary.
