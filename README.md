# The Science of Why Onions Make Us Cry

A complete article and reproducible computational companion for **The Serious Science of Small Annoyances**, by Sam Vaseghi. Version 1.1.0, 27 September 2026.

Start with [the article](article.md). The [TK export](article_tk.md) contains the same complete text with conservative punctuation. The diagrams and animation are embedded using relative paths, so keep the `assets/` folder beside either Markdown file.

This project follows the chemistry from damaged onion tissue to exposure near the eyes, assesses common kitchen remedies, and calculates two conditional transport comparisons. All numerical outputs are model results. No original onion experiment, measured kitchen flow, or human-subject trial is claimed.

## What is included

| Location | Contents |
| --- | --- |
| `article.md`, `article_tk.md` | Complete article, captions and eight numbered references |
| `assets/` | Five numbered figures, a featured painting, the exposure table, GIF/MP4 animation, static fallback, editable SVGs for original static assets, and image-source records |
| `src/` | Source and transport equations implemented in Python; result and visual generation |
| `config/model_config.json` | Canonical geometry, rates, transport parameters and numerical resolution |
| `data/parameters.csv` | Parameter units, meanings and provenance; illustrative inputs clearly marked |
| `results/` | Saved source histories, concentrations, exposures, sensitivities and convergence checks |
| `docs/technical_supplement.md` | Equations, derivations, assumptions, numerical method and full interpretation |
| `research/` | Evidence review, claim ledger, bibliography, citation crosswalk and search/access record |
| `tests/` | Independent mathematical tests and saved-output audit |
| `qa/` | Numerical, scientific and release reviews, machine-readable checks and test log |
| `scripts/` | Reproduction, article preflight, TK export and archive-integrity tools |
| `CITATION.cff` | Citation metadata, with no invented repository URL or DOI |
| `MANIFEST.sha256` | Hashes of all released files except the manifest itself |

[Publication integration notes](docs/publication_update.md) describe the final manuscript import, numbering changes and preserved results. The original received manuscript is retained in `provenance/author_manuscript_2026-09-27.md` as a historical source, including its original numbering.

[Provenance](docs/provenance.md) explains the AI-assisted workflow, separate production/review roles, source-access limitations and third-party materials. The [original plan](docs/original_project_plan.md) is retained as a dated historical document; the delivered model's actual scope is defined in the technical supplement and review reports.

## Read or inspect without running code

The figures, animation, Markdown and CSV files are already included. The article uses the LFS structure illustration in Figure 1, the reaction schematic in Figure 2, the sulfur pathway in Figure 3, the source/exposure comparison in Figure 4, and the remedy assessment in Figure 5. Animation 1 uses its own numbering; the exposure table and featured painting are unnumbered. The MP4 is an alternative to the embedded GIF. [Visual notes](docs/visual_notes.md) document scales, timing, field slices and editable formats.

All inputs are disclosed. The calculations assume uniform prescribed flow and an effective mixing coefficient in unbounded three-dimensional space. They illustrate exposure at a fixed mathematical observer. They cannot assign a universal percentage reduction in crying to refrigeration, a knife, a fan or goggles.

## Reproduce everything

The delivered run used Python 3.12.14, NumPy 2.3.5, SciPy 1.17.0, Matplotlib 3.10.8 and Pillow 12.3.0. Python 3.12 is recommended. MP4 rendering also requires a system installation of **FFmpeg with the libx264 encoder** available on `PATH`. No network is used by the model or rendering code after dependencies are installed.

From the extracted project folder:

```bash
python -m venv .venv
```

Activate the environment with `source .venv/bin/activate` on macOS/Linux, or `.venv\Scripts\Activate.ps1` in Windows PowerShell. Then run:

```bash
python -m pip install -r requirements.txt
python scripts/verify_manifest.py
python scripts/reproduce.py
```

The full reproduction regenerates the result tables, sampled fields, all generated figures, both animation formats, the TK export, and executable QA records. It overwrites generated files in this working copy. Extract a second copy first if you want to preserve the delivered files for comparison. `MANIFEST.sha256` identifies the delivered version, so check it **before** regeneration; new report timestamps and rendering metadata can change hashes without changing the numerical results.

The stages can also be run separately:

```bash
python -m src.run_simulations
python -m src.make_visuals
python scripts/export_tk.py
python tests/run_checks.py
python scripts/validate_package.py
```

For a quicker audit of the saved results, without regenerating figures or video:

```bash
python scripts/reproduce.py --check-only
```

For new scenarios, use a copied configuration with `python -m src.run_simulations --config path/to/config.json --output-dir path/to/new-results`. The delivered article, plotting script and numerical audit refer to the canonical configuration and output locations; updating a scientific scenario also requires updating the corresponding figures, interpretation and checks. Canonical output column names containing `120s` assume the canonical 120-second history window.

## What the checks establish

The numerical reviewer independently checks source inventories, Gaussian mass and moments, limiting cases, symmetries and integrations. The saved-output audit checks all eight canonical source/flow combinations, 189 transport sensitivities, 24 loss-sensitivity entries and 48 animation samples, as well as serialized histories and configuration/source hashes. The article preflight checks rounded headline values, citations, local links, equation delimiters and consistency with the TK export.

Read [the numerical review](qa/numerical_review.md), [the scientific review](qa/scientific_review.md) and [the release review](qa/release_review.md) for executed results and their scope. Independent checks here were performed by separate agents in the same AI-assisted project. They are not external peer review or experimental validation.

For exact numerical comparison, use saved CSV/JSON values and the tolerances in the independent checks. Across machines, font rendering, image metadata, video encoding and archive timestamps need not be byte-identical. The input parameters, equations, plotted scales and numerical conclusions should agree within the stated tolerances.

## Publication and private GitHub repository

Extract the ZIP and put the contents of `onion-tears-lab/` at the root of your GitHub repository. Preserve the relative paths, source files, saved results and review records. No credentials or third-party paper PDFs are included. The final manuscript's three third-party images are bundled with source records. The original investigators' datasets remain linked at their sources.

For Medium/TK, use the complete `article_tk.md`; upload the accompanying images and animation through the publishing editor as needed. The Markdown syntax has been locally checked. An actual TK import has not been tested in this project. The GIF can be replaced by `assets/animation_01_transport_static.png` where animation is unsuitable, with the MP4 linked separately. The repository is intended to remain private. Readers may request access from the author; access is considered individually. The article includes this policy, and no public repository URL is required.

No general reuse licence has been selected. Add your chosen article, asset and code terms before inviting reuse. Citation information is provided in `CITATION.cff`. No repository URL or archival DOI is assumed.

To produce a new archive after intentional changes, rerun the relevant scientific and numerical checks, update the release review and version metadata, then run `python scripts/build_archive.py`. This refreshes the manifest and creates a ZIP beside the project folder.
