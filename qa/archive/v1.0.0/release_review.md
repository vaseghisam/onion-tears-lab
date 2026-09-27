# Release review

Status: complete. Version 1.0.0, 24 September 2026.

The coordinating editor assembled the article, calculations, visuals, source record and separate review reports. The following checks were executed before delivery.

| Check | Executed result |
| --- | --- |
| Scientific interpretation | Separate reviewer read the complete revised article, eight references and technical supplement; requested corrections were applied and rechecked. No unresolved scientific-interpretation finding remained. |
| Numerical implementation | All 18 independent test methods passed. |
| Saved output | Audit passed eight summary cases, 76,808 concentration-history rows, 19,202 source-history rows, 189 transport sensitivities, 24 loss-sensitivity cases and 48 sampled animation values. |
| Article/data agreement | Four displayed exposure values, two peak values, the source-comparison ratio and the no-drift tail fraction match the saved calculation after rounding. |
| Visual agreement | All three static figures and the animation fallback were inspected. Production and scientific reviewers inspected representative decoded animation frames; the coordinator inspected all static figures. Scales, labels, normalization, observation geometry and captions agree. |
| Markdown and references | Both complete article files pass local syntax preflight. All eight references match the bibliography crosswalk. Local links resolve, display equations occupy single source lines, and the TK version preserves the complete article. |
| Clean extraction | A ZIP was extracted into a separate directory and its manifest verified before reproduction. `python scripts/reproduce.py` completed successfully in 44.4 seconds in the tested environment. |
| Reproduced results | All eight CSV files and `summary.json` were byte-identical. Every saved NPZ array was exactly equal. Configuration, production source, test source and manuscript were unchanged. |
| Reproduced visuals | All PNGs, the GIF and the MP4 were byte-identical in this environment. SVG and visual metadata were regenerated and retained. Byte identity across different platforms is not required. |
| Release integrity | The final archive contains the reproduced outputs and review records. Its manifest is regenerated after final assembly; the release process verifies each archived file against that manifest and checks ZIP integrity. |

The reproducibility run used the installed, pinned dependency versions in a newly extracted project directory. It did not test a fresh package installation, an alternative operating system, or every supported Python version. The complete run log is `reproduction_log.txt`; exact comparisons are in `reproduction_comparison.json`. Executable QA results are in `check_results.json` and `article_checks.json`.

The local Markdown preflight is not a live TK import test. No GitHub repository was created or published. The code uses no online data during reproduction; the cited source papers and original investigators' datasets remain external linked materials.

This review verifies internal agreement, numerical implementation and reproducibility of the stated model. The emission rates, effective mixing, source geometry and uniform flow are illustrative. No original onion experiment or human tearing trial was performed. Separate agents supplied the independent checks within this AI-assisted project; this is not external peer review.
