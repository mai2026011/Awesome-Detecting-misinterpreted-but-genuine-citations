# Prompt 10 — Baseline reproduction / validation report

Date: 2026-11-12  |  Project: Detecting Misinterpreted but Genuine Citations through Automated Claim Verification

## Objective and scope
Validate the **archived prediction evaluator**, not a retrained reproduction of Sarol et al.'s neural network. Input data: `claims_dev.jsonl`, `claims_test.jsonl`, `pred_dev.jsonl`, `pred_test.jsonl`. All numerical results below were independently recalculated from those four uploaded files in this analysis environment and are consistent with the user-provided Colab outputs. Confidence-based abstention has **not** been evaluated yet.

## VERIFIED — File and evaluation integrity
- Development: **316** unique claim-document pairs; **215 correct**; **24** empty-evidence cases provisionally mapped to NEI; accuracy and micro-F1 **0.6804**; macro-F1 **0.6405**.
- Test: **606** unique claim-document pairs; **338 correct**; **50** empty-evidence cases provisionally mapped to NEI; accuracy and micro-F1 **0.5578**; macro-F1 **0.4438**.
- All archived predictions align to cited document IDs, have three finite probabilities summing to 1 (tolerance 0.001), and their stored predicted label equals argmax in order `[NOT_ACCURATE, NEI, ACCURATE]`.
- Test confusion matrix, actual rows × predicted columns, class order above: **[[47, 21, 102], [9, 22, 19], [75, 42, 269]]**. Of 170 `NOT_ACCURATE` items, 102 were predicted `ACCURATE`.
- Per-class test F1: `NOT_ACCURATE` **0.3123**; provisional `NEI` **0.3259**; `ACCURATE` **0.6933**.
- Saved checkpoint-derived config reports `scifact_10`, encoder `longformer-large-science`, 3 labels, learning rate 1e-05, 5 epochs, mixed precision 16, gradient accumulation 8, 2454 training instances; `git_checksum` is blank. Config metadata is not proof of which exact weights or preprocessing produced these files.

## Published-results reference (not exact reproduction claim)
- Sarol et al. (2024), Table 4, **top-5 retrieved sentences**: micro-F1 **0.58**, macro-F1 **0.50**; ACCURATE F1 **0.69**, NOT_ACCURATE **0.43**, IRRELEVANT **0.37**.
- Current archived test: micro-F1 **0.5578** (−0.0222), macro-F1 **0.4438** (−0.0562). Class-wise shortfall is greatest for NOT_ACCURATE (ours **0.3123**).
- Primary paper: https://pmc.ncbi.nlm.nih.gov/articles/PMC11231046/ ; official code/data: https://github.com/ScienceNLP-Lab/Citation-Integrity/
- These differences **must not** be attributed to a coding defect without establishing identical checkpoint, retrieval top-k, dataset version, context extraction, label mapping, and test protocol. The published top-20 model was stronger, at 0.59/0.52; do not confuse top-5 and top-20 references.

## UNCERTAIN / PROTOCOL DEVIATIONS
1. **NEI versus IRRELEVANT:** empty evidence is treated as NEI in local evaluation, but original source labels are not present for these 74 empty-evidence examples. Subset sensitivity analysis must exclude provisionally labelled cases.
2. **Development training overlap risk:** configuration reports 2,454 training instances; old work log counted 2,138 train plus 316 dev = 2,454. This is suggestive, not conclusive, of dev inclusion in training. Do not select thresholds or fit temperature on dev and claim an independent holdout without verifying provenance.
3. **Test as model validation risk:** old checkpoint log mentioned a test fold used as validation; it is unresolved whether the released checkpoint/parameters were selected using test scores. Independently held-out performance cannot be guaranteed.
4. **Checkpoint/pipeline provenance:** released checkpoint, exact top-5 retrieval, preprocessing, corpus version, seed, training environment and paper-level evaluation protocol have not been independently re-executed in the present notebook.
5. **Only prediction-level replication achieved:** no fresh neural inference or training performed. No article-clustered bootstrap inferential analysis yet.

## Required corrective actions / safeguards
- Preserve immutable backup and file hashes (Colab saved `environment_record.json`).
- Describe downstream study as **retrospective selective-prediction analysis on an archived classifier**, rather than a full reproduction of the published paper.
- For planned 80%-coverage analysis, use predeclared top-k ranking on **test** data without fitting a score threshold; compare with matched-coverage random rejection. Report coverage, selective risk, a risk–coverage curve, uncertainty, and 50-provisional-case sensitivity analysis.
- Do not use development data for calibration unless independence is documented. Treat statistical intervals as conditional on the archived model; note document/article clustering.
- Before claiming exact paper replication, recover and independently verify original checkpoint hash, retrieval output and train/validation/test usage. If unavailable, keep discrepancy **unresolved**, not corrected.

## Gate decision
**CONDITIONAL PASS for retrospective analysis. NOT VERIFIED as an exact replication of Sarol et al.** The saved-prediction evaluation implementation is validated. The original classifier and dataset protocol remain partially unaudited; restrictions above govern subsequent claims.

## Next
Prompt 11 is event-triggered debugging; no new code error has been reported for this lightweight evaluator. If no new failure occurs, proceed to Prompt 12 for the preplanned matched-coverage confidence-rejection experiment (or do a brief Prompt 11 retrospective debug note about the earlier Colab RAM problem).
