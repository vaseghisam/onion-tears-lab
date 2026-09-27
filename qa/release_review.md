# Release review

Version 1.1.0, 27 September 2026. This revision integrates the author's final publication manuscript. It does not revise the numerical model or results.

| Check | Result |
| --- | --- |
| Author's text | The supplied text and all six display formulas are preserved after the documented production transformations. The agreed private-access statement is the sole new prose paragraph; the supplied painting credit is made visible as a caption. |
| Figure sequence | Five figures numbered 1–5 in reading order, with corresponding filenames and captions. Animation 1 uses its own numbering; the exposure table and lead image are unnumbered. |
| Image completeness | All eight images in both repository article files use existing local paths. The added painting and research images were downloaded from the supplied URLs and visually inspected. Source records and checksums are included. |
| Numerical implementation | All 18 independent tests passed again. The saved-output audit passed. |
| Scientific-file preservation | Model source, simulation driver, configuration, parameter data, saved results, numerical tests and technical supplement match the original release byte for byte. |
| Article/data agreement | Four table values, two peak values, the finite-exposure ratio and the no-drift tail fraction agree with the saved results. The table's SVG text and rendering provenance are checked directly. |
| Original visuals | The three original figures and animation retain their original bytes; only figure filenames changed. The modified renderer reproduces the three renamed PNG figures byte for byte. |
| Added table | The table is generated from results/summary.json, has a checked source/output record and reproduces byte for byte in the tested environment. |
| Markdown | Both article files pass the package preflight. A separate Pandoc parse finds all eight images and six display equations in each file. All eight numbered references agree with the bibliography crosswalk. |
| Review history | The original review records and manifest are archived under qa/archive/v1.0.0/; original figure numbers and manuscript hashes are explicitly historical. |

Machine-readable evidence is in `article_checks.json`, `check_results.json` and `publication_integration_checks.json`. The execution log is `publication_check_log.txt`. A separate agent's integration review is in `publication_integration_review.md`.

The full numerical/animation reproduction was completed for version 1.0.0; its logs are retained. This update reran the numerical checks and reproduced the changed static-rendering path, without rerunning the unchanged simulation or re-encoding the unchanged animation. An actual TK import and a GitHub upload are outside this local package check.

The release archive is built after the review records are complete. Its refreshed SHA-256 manifest and ZIP integrity are checked after a clean extraction before delivery. The original received manuscript is retained for comparison, not as an alternative current article.

These checks establish internal consistency and implementation of the stated idealized model. They do not calibrate the model against kitchen measurements or establish quantitative protection against human tearing. The independent integration review was performed by another agent in the same AI-assisted project, not by an external peer reviewer.
