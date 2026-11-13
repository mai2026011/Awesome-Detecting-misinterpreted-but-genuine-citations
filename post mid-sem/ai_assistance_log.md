# Prompt 18 — AI-Assistance and Research-Integrity Report

**Project:** Confidence-Based Abstention for Biomedical Citation Verification: A Retrospective Evaluation of Archived Predictions  
**Related prior work:** *Detecting Misinterpreted but Genuine Citations through Automated Claim Verification* (literature-review paper)  
**Student:** Apurv Sharma  
**Repository:** https://github.com/mai2026011/Awesome-Detecting-misinterpreted-but-genuine-citations/tree/main/post%20mid-sem  
**Record prepared:** 13 November 2026  
**Status:** Drafted from the conversation, experiment files, research decisions, and user-reported Colab outputs. The student should inspect and approve this disclosure before submitting it.  

## 1. Scope and AI-use disclosure

I used ChatGPT across research planning, reviewing related literature, choosing a feasible experiment, drafting and debugging Python, interpreting numeric results, creating figures, revising the ACM LaTeX manuscript, and preparing repository documentation. The model helped propose procedures and draft text; its responses were not treated as evidence by themselves. I ran the evaluation code in Google Colab, examined the printed results and figures, maintained the processed input files in Google Drive, compiled the manuscript in Overleaf, and ran the GitHub versions of the analysis scripts. The original Longformer citation classifier was **not retrained** in the final experiment; the research analyzes archived predictions from an earlier workflow.

**Prompt provenance:** Activity identifiers below are the assignment's prompt numbers (P03–P17). Representative user requests are quoted where present, otherwise paraphrased. These entries are a reconstruction from the available chat and saved artifacts, **not** a verbatim export of every message, a verified list of GitHub commits, or a record of the model version used on every historical turn. ChatGPT was the AI assistant; its per-prompt model/runtime versions were not preserved in the research archive.

## 2. Significant AI-assisted activities and human verification

### A1 — Feasibility and study selection (P03–P07)
- **Task / prompt:** Restart at Prompt 3, work one prompt at a time, and select a study feasible on limited Colab resources. The user explicitly requested, “let's start this assignment again from prompt 3 and only do one prompt at a time.”
- **AI proposal:** Reuse existing biomedical citation-verification predictions to evaluate confidence-ranked abstention, rather than rerun a memory-intensive full-document verifier. Compare full acceptance, matched-size random retention, and confidence ranking; preserve uncertainties about labels and data splits.
- **Human decision:** Accepted the narrower retrospective study and supplied saved prediction and claim files.
- **Verification:** Checked whether 316 development and 606 test predictions aligned with the corresponding claim–document records; subsequently reproduced the baseline in Colab.
- **Change / outcome:** The objective changed from fine-tuning or rerunning a large verifier to evaluating a frozen prediction archive on CPU. This is an application of existing selective-classification methods, **not** an invented new algorithm.

### A2 — Colab setup, failures and data recovery (P08)
- **Task / prompt:** Recover from the earlier high-RAM Colab failure and establish a usable environment.
- **AI proposal:** Use a CPU-only Python workflow, test imports and JSON processing, locate data in Drive, then upload four small JSONL files if necessary; verify Drive backup copies with SHA-256 hashes.
- **Human decision:** Ran the environment checks, manually uploaded the four inputs after the first proposed Drive path failed, and saved backups under `MyDrive/CitationIntegrityStudy/data/`.
- **Verification:** Colab printed Python 3.13.16; NumPy 2.4.6; pandas 2.2.3; scikit-learn 1.6.1; 12.67 GB of RAM; `JSON sanity test: PASSED`; and four `BACKUP VERIFIED` messages.
- **Change / outcome:** Recovered the experiment without loading Longformer. `environment_record.json` and four backed-up data files were created. The original RAM-related model run was **not** rerun or proved fixed end to end.

### A3 — Dataset alignment and label construction (P08–P10)
- **Task / prompt:** Join original claim files to saved predictions and derive analysis labels.
- **AI proposal:** Use claim/document identifiers, confirm three valid probabilities and argmax agreement, and mark records with empty evidence as provisional `NEI`.
- **Human decision:** Ran the validation and data-loading cells, inspected row samples and class counts, and retained the provisional-label caveat.
- **Verification:** 316/316 development and 606/606 test records matched. Label audit: development 191 `ACCURATE`, 101 `NOT_ACCURATE`, 24 empty evidence; test 386, 170, 50 respectively.
- **Change / outcome:** Produced joined records and baseline CSVs. **Unresolved:** an empty evidence field is not independent proof that the original dataset annotated the citation `IRRELEVANT`; 50 test labels are provisional.

### A4 — Baseline reproduction and audit (P09–P10)
- **Task / prompt:** Evaluate archived classifier outputs and compare them with the published baseline.
- **AI proposal:** Calculate accuracy, micro/macro-F1, per-class metrics and confusion matrices using scikit-learn; record rather than hide publication differences.
- **Human decision:** Ran the code and shared actual console output.
- **Verification:** Test: 338 correct / 606; accuracy and micro-F1 0.5578; macro-F1 0.4438; 102 of 170 `NOT_ACCURATE` cases predicted `ACCURATE`. The paper's top-five reference was reported as 0.58 micro-F1 and 0.50 macro-F1; exact evaluation equivalence was not confirmed.
- **Change / outcome:** Saved `baseline_metrics.json`, confusion matrices, and class-audit tables. The claim is **saved-prediction evaluation reproduced**, not complete neural-model training reproduced.

### A5 — Abstention experiment (P12)
- **Task / prompt:** “Test whether confidence-based rejection reduces citation-verification errors.”
- **AI proposal:** Rank predictions by maximum class probability, accept the top 485 of 606 for nominal 80% coverage, compare to full acceptance and expected uniform random retention, and calculate a pair-level bootstrap interval. Use 1,000 random selections (seed 42) and 2,000 bootstrap resamples (seed 2026).
- **Human decision:** Executed the supplied experiment notebook in Colab and returned its outputs.
- **Verification:** Colab reported `INPUT FILE HASHES: VERIFIED`; 338 correct / 606 at baseline; 485 accepted with 0.40206 risk; 4.018 percentage-point gain; descriptive 95% interval approximately [1.913, 5.914] percentage points. Excluding 50 provisional test labels preserved a 3.39-point gain.
- **Change / outcome:** Saved policy summary, per-case selection, random-retention draws, bootstrap effects, and risk–coverage data. No model parameters were changed. **Caution:** earlier exploratory abstention results predated the later protocol, so it cannot be described as clean prospective preregistration.

### A6 — Figure checking and class-wise analysis (P13–P14)
- **Task / prompt:** Create and interpret actual tables and figures.
- **AI proposal:** Plot the risk–coverage curve, report class-wise F1, and zoom the main figure to 70–100% coverage after the near-zero-coverage prefix created an unstable spike.
- **Human decision:** Executed the code, noticed the graph issue, ran the replacement plotting cell, and shared the corrected plot.
- **Verification:** At 80% coverage the accepted set contains 195 errors in 485 records; 73 errors and 48 correct predictions were withheld. Macro-F1 on the accepted subset was 0.4634, but `NOT_ACCURATE` F1 **decreased** from 0.3123 to 0.2788.
- **Change / outcome:** Saved final PNG/PDF figures and result tables. The selected-subset F1 values were described as *conditional subset metrics*, not an improvement in the frozen classifier's weights or general ability.

### A7 — Paper writing, ACM conversion and editing (P15)
- **Task / prompt:** Draft the second research paper from the earlier literature review and measured experiment; use ACM format; revise prose to sound more natural.
- **AI proposal:** Draft the abstract, related work, methods, results, limitations and bibliography; convert from IEEE to ACM `acmart` format; rephrase repetitive writing.
- **Human decision:** Confirmed which prior literature-review paper was the correct source, chose ACM formatting, uploaded the ZIP to Overleaf, compiled it, requested stylistic revision, and provided the resulting PDF.
- **Verification:** The user confirmed successful compilation; the PDF visibly included the actual numbers, figures, references, and limitations. No Turnitin AI-score reduction was measured or guaranteed.
- **Change / outcome:** A seven-page ACM-formatted research draft was revised and compiled. AI assisted with drafting and rewording and must be disclosed; stylistic rewriting alone does not establish originality.

### A8 — Technical peer review and revisions (P16)
- **Task / prompt:** Critically review the paper and correct scientific positioning.
- **AI proposal:** Identify split leakage/provenance risks, provisional-label interpretation, test-exploration concerns, insufficient comparison with NLP selective-prediction work, and presentation issues. Add relevant published selective-prediction references and make the contribution claim narrower.
- **Human decision:** Applied updated Overleaf files and corrected author/affiliation details.
- **Verification:** The student reported successful recompilation; the revision documents record the changes. The underlying data-split and annotation uncertainties remain unresolved, and the paper must keep those disclosures.
- **Change / outcome:** Strengthened Related Work and limitations without modifying measured results.

### A9 — Repository packaging and reproduction check (P17)
- **Task / prompt:** Prepare a reproducible GitHub package and verify it in Colab.
- **AI proposal:** Supply `run_abstention.py`, `evaluate_results.py`, configuration, dependencies, README, aggregate results and `.gitignore`; keep original JSONL inputs and checkpoint weights out of the public repository pending rights review.
- **Human decision:** Uploaded the package to the existing GitHub repository and ran a Colab cell that cloned the repository and executed both scripts with existing Google Drive inputs.
- **Verification:** Screenshot/output showed `GitHub scripts: VERIFIED`, successful invocations of `run_abstention.py` and `evaluate_results.py`, and `GITHUB REPRODUCIBILITY TEST: PASSED`. Numerical results had also been separately reproduced during P12–P13.
- **Change / outcome:** A public code path with instructions was established. This demonstrates successful execution in the student's Colab environment, **not** a complete independent clean-room reproduction without access to the four matching processed inputs.

## 3. Real AI limitations, errors and corrections

| Observed issue | Evidence available | Response and remaining limitation |
|---|---|---|
| Original Longformer workflow exceeded usable Colab resources / required fragile historical dependencies | Earlier notebook and decision log record high-memory failure, old PyTorch/Transformers environment and local patches | Switched to frozen probability outputs and CPU-only evaluation. Did **not** claim the original full training setup was repaired. |
| Proposed Google Drive location was wrong | The user's console printed `NOT FOUND` for all four inputs in the guessed backup folder | Human manually uploaded the four files; later SHA-256-verified Drive copies. |
| Gold labels were not included in prediction exports | Predictions contained class probabilities but not ground-truth labels | User supplied matching claims files; empty-evidence entries were marked *provisional* rather than silently assumed correct. |
| The baseline did not exactly match Sarol et al.'s published top-five scores | Saved prediction evaluation: 0.5578/0.4438 vs published reference 0.58/0.50 | Documented the mismatch; did not represent the archive as an exact independent replication of that configuration. |
| Earlier notebook had already explored abstention | Research decision log and paper describe exploratory analyses before later protocol documentation | Reframed the analysis as retrospective/descriptive; avoided claims of prospective preregistration or an untouched final test. |
| Initial risk–coverage plot had an unstable low-coverage spike | User supplied original plot and the 70–100% corrected plot | Replotted only the presentation window; kept numerical results and complete curve unchanged. |
| Separate notebooks and artifact download links added avoidable workflow friction | User challenged duplicate notebook creation and reported failed download links | Consolidated code into the existing notebook where practical, and provided alternative ZIPs. No unverified claim that failed links worked. |

## 4. Human decisions and critical reasoning

The student chose to resume from Prompt 3, prioritized feasibility after observing the RAM problem, made the processed data accessible, executed the Colab validation code, checked the empirical outputs, chose the ACM format, reviewed the generated PDF, and ran the GitHub-hosted scripts. The empirical findings are supported by the actual saved prediction files and executed scripts, not by AI-proposed numbers alone. However, AI proposed much of the analysis framework and wrote substantial portions of code and prose; this report should not imply the research design or manuscript were developed independently of AI assistance.

The key research judgment is to distinguish an improved **error rate among accepted predictions** from a generally safer citation-verification model. At 80% nominal coverage, 4.02 percentage points of selective error reduction coexisted with worse detection F1 for `NOT_ACCURATE`. The latter is a negative finding, and it is included rather than omitted for a more favorable headline.

## 5. Remaining risks and incomplete checks

1. **Checkpoint provenance:** The original train/dev/test use, checkpoint selection, and potential exposure of test data during training/validation are not fully reconstructed.
2. **Provisional annotation mapping:** Fifty test rows with empty evidence are mapped to `NEI`; correspondence with the published `IRRELEVANT` category is not verified at record level.
3. **Limited generalization:** One archived prediction set, one model, and pair-level rather than article-clustered bootstrap; the 80% top-*k* rule is not a deployed numerical threshold for unseen citations.
4. **Limited controls and qualitative review:** Random rejection is an informative matched-coverage control but not a trained alternative. The source passages for high-confidence misclassifications were not manually audited to determine mechanisms.
5. **License and release conditions:** The permission to redistribute processed claim text, original articles, and weights needs confirmation. The public repository intentionally omits the four raw/processed JSONL inputs and model checkpoint; exact-hash inputs must be obtained separately.
6. **Paper and bibliographic checks:** Major cited papers were checked during earlier prompts, but a final line-by-line verification of every bibliographic field and claim against the originals remains the submitting author's responsibility.
7. **AI similarity/authorship:** AI materially assisted the prose. A rewrite was performed for clarity and natural flow, but there is no verified Turnitin AI-detection outcome. Text similarity alone does not determine originality or academic integrity.

## 6. What the workflow taught me about AI-assisted coding

AI made it easier to turn a broad research gap into a small executable study and to write checks, tables and documentation quickly. It was less reliable when it inferred file locations, treated an analysis plan as fully prospective, or moved to new notebooks before considering the existing workflow. Running the code, comparing saved artifacts, reporting class-wise failures, and checking the source of each claim were essential. In this project, a modest and reproducible analysis of an existing prediction archive was more defensible than claiming a new model or rebuilding a memory-intensive verifier without the required resources.

## 7. Evidence index and submission actions

**Primary local artifacts:** `claims_dev.jsonl`, `claims_test.jsonl`, `pred_dev.jsonl`, `pred_test.jsonl` (private matching inputs); `environment_record.json`; `baseline_metrics.json`; Prompt 12 `experiment_manifest.json`, `policy_summary.csv`, `bootstrap_effects.csv`, `risk_coverage.csv`; Prompt 13 `results.csv`, class-wise table and figures; `research_decisions.md`; latest ACM PDF and source; Prompt 16 review and revision log; GitHub `scripts/`, `config/`, `results/`, README and requirements. Exact file paths may differ between the private Drive workspace and public GitHub repository.

**Before submission:** The student should verify the first-person statements above, add or correct any missing prompt history, cite or attach actual output screenshots as needed, include the repository path, and make sure the assignment submission includes the final paper/LaTeX, code, reproducible instructions, saved experimental evidence, provenance log, and any required demonstration. No claims about independent model training, numerical improvements beyond those measured, or data redistribution permissions should be added without evidence.
