# Confidence-Based Abstention for Biomedical Citation Verification

Reproducible **retrospective analysis of archived predictions**, performed for a post-mid-semester research assignment. The underlying citation classifier is not retrained here. The original scientific literature and model/data authors should be cited separately; this repository does not claim the classifier or dataset as our own.

## Main result (606 archived test claim–document pairs)

| Decision policy | Accepted | Errors in accepted set | Selective error |
| --- | ---: | ---: | ---: |
| Full classifier (100% coverage) | 606 | 268 | 44.22% |
| Confidence-ranked (80% coverage) | 485 | 195 | 40.21% |
| Random matched-size acceptance (expected) | 485 | — | 44.22% |

Error difference at 80%: **4.02 percentage points** (descriptive pair-level bootstrap 95% interval: **1.91–5.91 pp**, 2,000 replicates). However, **NOT_ACCURATE F1 decreased from 0.3123 to 0.2788** in the selected group. The 50 test cases with inferred/provisional NEI labels are treated separately in sensitivity analysis.

## What is in this repository

- `scripts/run_abstention.py`: verify inputs and calculate confidence selection, uniform-random controls, bootstrap, sensitivity, and plots.
- `scripts/evaluate_results.py`: independently audit outputs and make per-class tables and figures.
- `config/frozen_experiment.json`: recorded protocol and original input SHA-256 hashes.
- `results/`: aggregate numerical summaries and experiment manifest (not the original per-case data).
- `requirements.txt`: CPU-only Python dependencies.

## Inputs (not bundled)

You must have **all four** matching processed JSONL files:

```
<project-root>/data/claims_dev.jsonl
<project-root>/data/claims_test.jsonl
<project-root>/data/pred_dev.jsonl
<project-root>/data/pred_test.jsonl
```

These are *processed experiment inputs*. They are **not interchangeable** with any arbitrary download of the original study's dataset. The scripts check exact SHA-256 hashes to avoid silent mismatch. See `config/frozen_experiment.json` for the expected hashes. The underlying biomedical corpus was introduced by Sarol et al. (2024), *Assessing citation integrity in biomedical publications: corpus annotation and NLP models* (Bioinformatics; doi:10.1093/bioinformatics/btae420). Please consult the original release and its license before reusing or redistributing any content.

Do **not** commit source JSONL files, checkpoint weights, copied scientific articles, secrets, or claim text derived from non-redistributable works without checking rights.

## Run locally

Tested in Google Colab with Python 3.13.16, NumPy 2.4.6, pandas 2.2.3, and scikit-learn 1.6.1. A CPU runtime is sufficient for the evaluation.

```bash
python -m pip install -r requirements.txt
export CITATION_PROJECT_ROOT=/absolute/path/to/project-root
python scripts/run_abstention.py
python scripts/evaluate_results.py
```

The first script writes to `<project-root>/results/prompt12/`; the second writes to `<project-root>/results/prompt13/`. The path must contain the `data/` folder with the four specified inputs.

## Run in Google Colab

1. Mount Google Drive and keep the verified four JSONL files in `MyDrive/CitationIntegrityStudy/data/`.
2. Clone/download this repository into the runtime and install `requirements.txt` if needed.
3. Run `python scripts/run_abstention.py` and then `python scripts/evaluate_results.py`. The default paths target the existing Google Drive project, and no Longformer checkpoint or GPU is needed.
4. Compare the printed baseline, 80%-coverage gain and bootstrap interval with the numbers above.

## Methodology and limitations

- **No new neural-model training**; results are conditional on one archived prediction set.
- The 80% policy selects the highest-confidence 485 predictions *after viewing the batch size*. It is not a validated threshold for future citations.
- The original checkpoint’s training/validation/test provenance is not completely established. Earlier exploratory abstention analyses occurred before the documented final protocol; this is **not** a clean prospective preregistered test.
- Empty gold-evidence rows are provisionally mapped to NEI; they have not been certified to equal the publication's IRRELEVANT annotation.
- Pair-level bootstrap does not account for citations clustered by article. The interval is **descriptive**, not a guaranteed generalization interval.
- Accepted-subset F1 describes a selected population and is not a gain in the original model’s ability on the same records.

## Attribution

See the paper's bibliography for Geifman & El-Yaniv (2017), SciFact (Wadden et al., 2020), MultiVerS (Wadden et al., 2022), and Sarol et al. (2024). A license for this new repository has not yet been selected.
