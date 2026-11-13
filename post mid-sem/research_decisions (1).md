# research_decisions.md

Project: Detecting Misinterpreted but Genuine Citations through Automated Claim Verification
Goal: convert completed literature review into an implementation-based research paper
Evidence labels: VERIFIED (seen in a file/output you attached) | INFERRED (reasoned, not yet checked) | UNKNOWN (no evidence yet)

Rules for this log
- Never record a metric, dataset, repo link, or paper that is not backed by a file, output, or URL you have opened.
- Every decision needs: reason, evidence, label, next action.
- Append new entries; do not silently rewrite old ones. Mark superseded entries as SUPERSEDED BY D-xxx.

---

## D-001 | Stage 0 | Scope of existing review
- Decision: Treat the review as the starting artifact; scope = single-pair fidelity failures (omission, overstatement, transformation, reversal, unsupported inference) where the cited source is genuine. Existence/metadata errors are out of scope.
- Reason: stated explicitly in Sections 1 and 3.2 and Figure 1 of the review.
- Evidence: review PDF (main__1_.pdf), Sections 1, 3.2, 4.1. Label: VERIFIED (about what the review says, not about the literature itself).
- Next action: confirm the scope is also the scope of the experimental paper.

## D-002 | Stage 0 | Reported numbers are unverified against primary sources
- Decision: Treat all figures quoted in the review (3,063 instances; 100 reference articles; 39.18% errors; 0.59 micro-F1; 0.52 macro-F1; ~1.4K SciFact claims) as UNKNOWN until checked against the original papers.
- Reason: only secondary statements in the review are available in this log.
- Evidence: none yet beyond the review text. Label: UNKNOWN.
- Next action: attach Sarol et al. 2024 (Bioinformatics 40(7), btae420) and its supplementary/data-availability section; attach SciFact and MultiVerS papers.

## D-003 | Stage 0 | Central hypothesis candidate
- Decision (tentative): Citation-fidelity checking is a constrained case of evidence-grounded scientific claim verification where the source document is known.
- Reason: this is the review's own synthesis (Section 2.1), not an empirical result.
- Evidence: review Section 2.1. Label: INFERRED (conceptual, untested).
- Next action: turn into a testable research question in Stage 3.

## Open evidence requests
- [ ] Sarol et al. 2024 PDF + dataset/code availability statement
- [ ] Zhang & Abernethy 2024, Huang et al. 2026, Isik & Guleryuzlu 2026 PDFs (Table 2 has thin detail for Huang et al.)
- [ ] Your supervisor/venue constraints, deadline, compute available
- [ ] Any code, data, or outputs you already have

Repo: https://github.com/ScienceNLP-Lab/Citation-Integrity
Commit: e9823957bb263db9ae402351b76d88ff1a723712
Cloned on: 29 Oct 2026

## Gate 1 progress (29 Oct 2026)
- Env: Colab T4 15 GB, Python 3.13
- requirements.txt pins 2020-21 versions (torch 1.7.1, PL 1.2.1). Python 3.13 par install hoga ya nahi: UNTESTED
- predict.py label_probs save karta hai (code mein VERIFIED, abhi run nahi kiya)
- train_configs.json repo mein nahi hai, predict.py ko chahiye (VERIFIED)
- Test claims mein 9 evidence labels hain (ACCURATE 1001, OVERSIMPLIFY 106, NOT_SUBSTANTIATE 55, CONTRADICT 25, MISQUOTE 24, INDIRECT 17, INDIRECT_NOT_REVIEW 17, ETIQUETTE 8, IRRELEVANT 1). Paper ke 3 classes se mapping: UNKNOWN
- Gap choice (G1/G2/G4): abhi tay nahi

- Checkpoint hparams (VERIFIED): PL 1.2.1, scifact_10, longformer-large-science, num_labels=3, lr=1e-5, accumulate_grad_batches=8, max_epochs=5, precision=16, rationale_weight=0, label_threshold=None (argmax), timestamp 2024-01-07
- git_checksum khali: checkpoint kisi code commit se tied nahi
- train_configs.json checkpoint hparams (minus tpu_cores) se rebuild kiya, original file nahi mili

- Legacy env (VERIFIED): uv venv Python 3.8.20, torch 1.7.1+cu110, PL 1.2.1, transformers 4.2.2, tokenizers 0.9.4, numpy 1.19.4, pandas 1.1.5; CUDA True on T4
- Drive test claims: 606 total, 50 empty evidence, 386 ACCURATE + 170 NOT_ACCURATE (386+170=556, so 1 entry per non-empty claim: inferred)
- bertviz/focal_loss requirements.txt mein nahi; stubs se import ki koshish (UNTESTED)

- LOCAL PATCH (VERIFIED jab diff dekhoge): model.py:152, data_train.py:33, data.py:16 mein "allenai/longformer-large-4096" -> "/content/longformer-large-4096" (transformers 4.2.2 + current HF Hub redirect mismatch). Model snapshot_download(huggingface_hub) se liya, sirf json/txt/pytorch_model.bin
- tokenizer.json hataya (precaution, UNTESTED): purane tokenizers 0.9.4 ke liye
- longformer_large_science.ckpt: get_checkpoint.py se (S3 link live hai ya nahi: UNKNOWN)

- data_train/target/scifact_10 folder gayab tha (cause UNKNOWN), re-copy kiya; ab absolute paths use ho rahe hain
- 10-claim debug run: KeyError 'NOT ENOUGH INFO' in data_train._add_instance_weights (pandas .loc); debug subset mein NEI instance nahi tha (INFERRED). Full test set se retry

- GATE 1 (31 Oct 2026): full test inference chal gaya (VERIFIED), 606 predictions, 2m59.7s on T4, label_probs order [NOT_ACCURATE, NEI, ACCURATE]
- Deviations from documented setup: minimal deps (uv venv py3.8, torch 1.7.1+cu110, PL 1.2.1, transformers 4.2.2, tokenizers 0.9.4, numpy 1.19.4, pandas 1.1.5), bertviz/focal_loss stubs, local-path patch for longformer-large-4096, tokenizer.json removed, train_configs.json rebuilt from ckpt hparams
- Evidence sentence index: tail of log shows [[0]] only (UNVERIFIED, full count pending)
- F1 vs reported 0.59/0.52: pending; metric definition UNKNOWN, numbers from plan not paper

- pred_test.jsonl /content se gayab hua (cause UNKNOWN); regenerate kiya. Regression: pehli run ke claim 0/1 label_probs se compare
- Slim checkpoint: bestModel.ckpt se optimizer_states, lr_schedulers, callbacks hataye (inference ke liye RAM kam karne ke liye). Weights/hparams unchanged (UNTESTED jab tak regression check pass na ho). sha256: <upar ke output se>

- Colab VM sessions ke beech badal jaati hai (Nov 1 06:2x timestamps: pura env fresh VM mein rebuild hua). Drive backup (citation_integrity_work/) kaam aaya: pred_test.jsonl wapas mili
- predict.py output sirf end mein likhta hai; beech mein stop/interrupt karne par kuch save nahi hota

- Dev predictions (VERIFIED, 316 pairs): micro 0.68, macro 0.641, confusion [[39,11,51],[0,24,0],[28,11,152]]; test: 0.558/0.444. pred_dev.jsonl Drive mein
- Dev optimistic: checkpoint monitor = valid_sentence_label_f1 (dev par best epoch chuna gaya)
- UNVERIFIED: num_training_instances=2454 vs train 2137 + dev 316 = 2453 -> kya model train+dev par train hua? Code check pending. G4 ki calibration dev par tabhi valid hai jab dev held-out ho

- bestModel.ckpt (VERIFIED, ckpt metadata): epoch 5, global_step 1535 = 5 x 307 steps (2454 train entries / bs 8). ModelCheckpoint state: monitor valid_sentence_label_f1, best 0.1265 at epoch=1-step=613, this file 0.1203 -> released weights = final epoch, not monitor-best
- Monitor metric (~0.12) is sentence-level rationale F1; rationale head untrained (inference: not a label-quality signal)
- Limitation: validation fold = test; hyperparameter tuning on test cannot be ruled out (UNKNOWN)
- Training experiment dir name: exp4.7-finalExp-ccsent
- 2454 train entries vs 2137 claims: pending cited-doc count check

- VERIFIED: claims_train 2138 claims (wc -l undercounts by 1: no trailing newline), dev 316, test 606; every claim cites exactly 1 doc
- VERIFIED: 2138 + 316 = 2454 = num_training_instances in ckpt hparams (global_step 1535 = 5 x 307)
- Likely (UNVERIFIED): final model trained on train+dev (validation=test). Paper main text does not describe dev usage (supplement not read)
- Consequence: dev predictions probably in-sample -> dev cannot be used for calibration/threshold selection. Check: train vs dev vs test accuracy/confidence (pending)

## G4 protocol (locked 1 Nov 2026, before any abstention analysis on test)
Question: does confidence-based abstention reduce selective risk (error rate among accepted predictions) on test at fixed coverage, vs the unmodified classifier?
Model: unchanged released checkpoint; label_probs from existing predictions (order NOT_ACCURATE, NEI, ACCURATE).
Calibration: temperature scaling only (single T, grid 0.5-5.0 step 0.01, minimize NLL on log(probs)/T). Primary fit: dev. Sensitivity: fit on train.
Confidence score: max calibrated probability.
Abstention: accept if confidence >= tau. tau chosen on DEV as the quantile giving 90%, 80%, 70% dev coverage; applied unchanged to test; report REALIZED test coverage.
Metrics: ECE (10 equal-width bins), Brier, NLL; selective error rate and macro-F1 on accepted; risk-coverage curve. Bootstrap 95% CI over instances (ignores article clustering: limitation).
Success: selective error at 80% coverage lower than baseline error with CI excluding 0. Otherwise report as null/negative result.
Pre-stated hypothesis (from mean max-prob vs accuracy per split): test is more overconfident than dev, so T fitted on dev will under-correct test ECE.
Known limitations: dev likely in-sample (2138+316=2454=num_training_instances) but model barely fits train (acc 0.664); test was the validation fold during training (hyperparameter tuning on test not ruled out); Drive data is top-5 sentence variant; baseline below paper (0.558/0.444 vs 0.58/0.50); label noise (kappa 0.18-0.31); small NEI counts (24 dev, 50 test).


- Split-wise accuracy / mean max-prob (VERIFIED): train 0.664/0.803, dev 0.680/0.791, test 0.558/0.782. Train ~ dev > test. Cannot tell if dev was in-sample; model barely fits train, so in-sample inflation is small. Confidence flat while test accuracy drops: overconfident on test




## Next actions
1. Attach the primary papers above.
2. Answer the Stage 0 constraint questions.
3. Proceed to Stage 1: evidence-based gap identification.

---

## D-004 | Prompt 04 | Feasibility and novelty screen (12 Nov 2026)
- Decision: CONDITIONAL GO for CPU-only retrospective selective-prediction analysis of the previously saved Sarol-style citation predictions, not a new confidence-calibration algorithm and not yet an independent generalization result.
- Reason: All 922 saved predictions match the uploaded dataset claims; confidence-based rejection and temperature scaling are established methods; this avoids earlier Colab RAM/Longformer difficulties.
- Evidence: `pred_dev.jsonl`, `pred_test.jsonl`, `claims_dev.jsonl`, `claims_test.jsonl` individually parsed and matched (316+606 IDs/doc IDs). Original Sarol 2024, Wadden MultiVerS 2022, Geifman & El-Yaniv 2017, Guo et al. 2017, Xin et al. 2021; public GitHub code and license (links in `prompt04_feasibility_novelty.md`). Labels: VERIFIED for file integrity and established prior methods; INFERRED for applicability and dev-in-sample risk; UNKNOWN for a completely novel combination or independent validation.
- Major unresolved risks: original paper class `IRRELEVANT` vs saved `NEI` needs mapping audit; old `num_training_instances=2454` equals train+dev counts and the test may have been used for training-time validation; original source/model weight hashes and top-5 preprocessing protocol not matched.
- Next action: before Prompt 05/experiment protocol freeze, explicitly flag split and label semantics and define appropriate retrospective evaluation or obtain a clean holdout for stronger claims.
- Supporting artifact: `prompt04_feasibility_novelty.md`.

---

## D-005 | Prompt 05 | Predeclared research question and primary outcome (12 Nov 2026)
- **Decision:** Primary retrospective RQ: at top-80%-confidence acceptance of archived test predictions, is selective error lower than matched-coverage random rejection? Report full-coverage error alongside it. Fixed primary confidence score = max predicted probability, with no learned threshold. Secondary risk–coverage at 70/90/100%, margin/entropy sensitivity, class-wise audit and sensitivity excluding provisional NEI.
- **Reason:** Sarol-style baseline outputs are recovered, while running Longformer was RAM-intensive; confidence analysis is tractable with CPU. Previously proposed development-set calibration may leak because development examples could be included in model training. An archived test set may also have been touched during model validation.
- **Evidence and label:** `prompt05_research_brief.md`; uploaded 316 dev + 606 test matched records and three-class prediction probabilities (VERIFIED); `research_gaps.md` G4 and original D-xxx notes (VERIFIED as existing plans); suspected split contamination (INFERRED, audit pending).
- **Success criterion, predeclared:** At 80% retention, ≥3 absolute percentage points lower selective error than matched-coverage random rejection, and a descriptive 95% bootstrap interval for error reduction excluding 0. Otherwise report null/inconclusive, not a positive claim. Secondary analyses do not supersede primary.
- **Protocol revision:** The **1 Nov 2026 G4 plan** to fit temperature on dev and tune thresholds on dev is **SUSPENDED for the primary experiment**, not silently erased or represented as already performed. Rationale: unresolved dev contamination; change documented **before any Prompt 05 abstention outcome computations**. This D-005 protocol supersedes the earlier plan for the *new primary study only*.
- **Cautions:** Empty gold evidence provisionally maps to NEI for 24 dev/50 test, and paper `IRRELEVANT` vs model `NEI` is unresolved; archived test not proved independent of model development. One thousand fixed-seed random retentions and ≥2,000 bootstrap resamples are planned, not executed.
- **Next action:** Prompt 06 to audit official dataset, comparison controls, split history and label semantics; Prompt 07 to freeze detailed blueprint before primary result computation. Do not train, calibrate or report selective improvement yet.

---

## D-006 | Prompt 06 | Pair-level dataset and comparator audit (12 Nov 2026)
- **Decision:** CONDITIONAL GO for a retrospective fixed-predictor selective-risk study (not prospective calibration or exact published-score replication). Keep the two controls: (B0) forced prediction at 100% coverage and (B1) uniform random acceptance at the same 80% test coverage, against the proposed maximum-probability ranking policy. Secondary confidence-score choices remain diagnostics.
- **Reason:** Original prediction datasets align (316 dev, 606 test; 922 pair records). A matched random control separates abstention's sorting value from simply discarding cases. CPU-based evaluation avoids the Colab RAM problems experienced with Longformer.
- **Verified locally:** Uploaded `claims_dev/test.jsonl` and `pred_dev/test.jsonl` all align by (split, claim_id, cited_doc_id). 3-class probabilities are finite and normalized; argmax agrees with labels; no within-split duplicate IDs or cross-split repeated cited-document IDs or exact claim texts. **316 claim IDs occur in both splits**; never merge using claim ID alone. Explicit evidence labels: dev 191 ACCURATE, 101 NOT_ACCURATE; test 386 ACCURATE, 170 NOT_ACCURATE. Evidence empty for 24 dev + 50 test examples. Full audit and SHA-256 hashes: `prompt06_dataset_baseline_validation.md`.
- **Source verified publicly:** Sarol et al., *Bioinformatics* 2024 (DOI 10.1093/bioinformatics/btae420) maps original IRRELEVANT citations to MultiVerS's Not Enough Information category, but the 74 empty-evidence *processed pairs* have no explicit original IRRELEVANT label; identity is **UNKNOWN**. ScienceNLP-Lab/Citation-Integrity README documents reference-article train/dev/test split of 70/10/20 and public MIT code repository. The original upstream format is broader than the uploaded processed one-pair-per-record input.
- **Risks, unresolved:** Training-size coincidence (2454=2138+316) raises a dev-contamination possibility; archived test may have been validation; origins of expanded candidates and paper-level clustering unverified; model baseline 0.558/0.444 differs from paper's top-5 0.58/0.50. Source paper describes ACCURATE/NOT_ACCURATE/IRRELEVANT while our predictions use ACCURATE/NOT_ACCURATE/NEI. Do not imply exact equivalence or independence.
- **Next action (Prompt 07):** Freeze exact accepted counts/rounding, class order, source hashes, seeds, tie-breaking, random controls, bootstrap calculations and a sensitivity analysis excluding 74 provisionally labeled rows. Only **then** compute abstention outcomes. Do not fit temperature scaling or tune thresholds on contaminated dev/test.
- **Labels:** Uploaded-file integrity **VERIFIED**; paper/repository protocol **VERIFIED as documented**; correspondence of every empty-evidence pair to paper IRRELEVANT **UNKNOWN**; split-independence of trained checkpoint **UNKNOWN**; CPU feasibility **INFERRED** (not a profiled benchmark).

---

## D-007 | Prompt 07 | Frozen retrospective evaluation blueprint (12 Nov 2026)
- **Decision:** Freeze the exact primary retrospective experiment: saved Sarol-style test predictions only (`N=606`), compare confidence top-485 at 80% nominal coverage to the exact expected selective error of a uniform random matched-k policy, and report all 1,000 random draws as a sanity check. Preserve full acceptance as B0; 70/90/100% and score variants are secondary.
- **Reason:** Prevent post-result score/policy selection; minimize Colab RAM; account for suspected dev/model-selection leakage by avoiding new calibration and prospective claims.
- **Source/evidence:** Uploads `claims_dev/test.jsonl`, `pred_dev/test.jsonl`, and CSV SHA-256 rechecked against Prompt 06 (VERIFIED); previous D-005 success rule (VERIFIED as prior decision); dev/test independence (UNKNOWN). Exact input fingerprints in `prompt07_frozen_config.json`.
- **Detailed frozen choices:** Class order `[NOT_ACCURATE, NEI, ACCURATE]`; composite key `(split, claim_id, cited_doc_id)`; empty gold evidence provisionally maps to NEI (24 dev / 50 test). `k=floor(N*c+0.5)`; 80% accepts 485 of 606. Sort max probability descending; tie-break claim ID, cited-doc ID and original row order. Random seed 42 / 1,000 draws; bootstrap seed 2026 / 2,000 resamples; pair-level percentile 95% interval. Discrete full-range AURC and accepted-set macro-F1 as secondary metrics. Exact mathematical random expectation = full-sample error; this refines finite Monte Carlo mean in the earlier D-005 plan without changing the matched-coverage random comparator.
- **Success rule (unchanged from D-005):** Primary effect `expected random error − confidence-selected error` >= 0.03 and lower bootstrap 95% bound > 0. Report otherwise as negative/inconclusive. This is a practical course-level criterion, not an independent clinical or publication threshold.
- **Deeper analysis:** Coverage at 70/80/90/100; secondary score rankings by margin and entropy; class-wise error review; sensitivity excluding 50 provisionally NEI-labeled test examples. No temperature fitting or test-label threshold tuning.
- **Threats and honesty:** Archived test baseline was previously inspected; possible use of test during checkpoint validation and dev in training unresolved; baseline vs published top-5 score differs; row-level CIs cannot account for unknown source-article clustering; code rights do not automatically cover full-text redistribution. The freeze precedes new abstention analysis, not all model evaluation.
- **No experiment outcomes computed at Prompt 07.** This step is a specification and file-check only; no model loading or Colab work was required.
- **Next action:** Prompt 08 — small CPU-only environment/data sanity test; collect genuine console output before coding the full evaluation. **Artifacts:** `prompt07_frozen_experiment_blueprint.md`, `prompt07_frozen_config.json`.
- **Evidence labels:** protocol and file integrity VERIFIED; achievable RAM footprint INFERRED; provenance of split independence and original NEI equivalence UNKNOWN.


## D-010 | Prompt 10 | Baseline validation (2026-11-12)
- Decision: Conditional PASS for prediction-level retrospective evaluation only; NOT a verified full reproduction of Sarol et al.
- Reason: 922 archived predictions and labels align, scores recalculate exactly, but raw-source NEI mapping, pipeline provenance, and validation/test reuse remain unresolved.
- Evidence: prompt10_baseline_validation_report.md; four JSONL uploads and Colab logs supplied by user; train_configs.json; Sarol et al. (2024) primary paper Table 4. Label: VERIFIED for evaluation; UNKNOWN for exact neural replication.
- Next action: Preserve frozen protocol; skip retraining; move to isolated abstention experiment without test tuning or unverified dev calibration.


## D-012 | Prompt 12 | Retrospective selective-prediction results (2026-11-12)
- **Decision:** Use pathway A (reproduction-of-saved-prediction-evaluation + lightweight extension) with matched-coverage random selection as comparator and the original 100%-coverage classifier as baseline. No neural-model modification or retraining; secondary score variants are diagnostic only.
- **Evidence, VERIFIED on uploaded files:** SHA-256 checks matched Prompt 07. On 606 test pairs, baseline error 268/606 = 0.442244; confidence-selected top 485 had 195 errors/485 = 0.402062; absolute error reduction vs exact random expectation is 0.040182 (4.02 percentage points). 1,000 uniform random draws mean risk ~0.44205. 2,000 pair-level bootstraps produced 95% percentile interval for the reduction of approximately [0.01913, 0.05914]. 80%-coverage accepted-set macro-F1 ~0.4634. Original planned 3pp practical threshold and positive descriptive CI met.
- **Deeper analysis:** 70/90/100% coverage risk calculated; alternative margin/negative-entropy ranking (secondary); excluding 50 provisional NEI test labels leaves 556 explicit cases, top-445 risk ~0.39775 against baseline risk ~0.43165, gain ~3.39pp. NOT_ACCURATE class remains difficult in accepted predictions. See `prompt12_results` CSVs/figures/manifest.
- **Caveats:** The earlier `Untitled4.ipynb` already included exploratory calibration/abstention code, so the study is **not prospectively preregistered**. The test fold's independence from original model selection is unresolved; pair-level bootstrap ignores citing-article clustering; the fixed proportion (top 80% of this file) is not a deployable confidence threshold; empty evidence maps provisionally to NEI. A descriptive retrospective improvement does not prove new model generalization or novelty.
- **Next action:** Prompt 13 should independently audit alignment and numerical exports against the saved outputs, and develop figures/results tables with provenance. Do not cherry-pick alternative scores or change the primary endpoint after observing results.


## D-013 | Prompt 13 | Traceable evaluation outputs and figures (2026-11-12)
- **Decision:** Validate and present the frozen Prompt 12 retrospective selective-classification outcomes using source-hash checks, raw claim+document ID joins, and archived outputs; no refitting or substitution of primary results.
- **Evidence, VERIFIED on files:** Four SHA-256 digests match Prompt 7 and Prompt 12; 606 saved test predictions matched original claim-document IDs without missing values. Recomputed full error 268/606 (44.2244%), highest-confidence top-485 error 195/485 (40.2062%), improvement 4.018pp, archived 2,000 pair bootstrap interval [1.913,5.914]pp. Macro-F1 full ~0.4438 and accepted-80% ~0.4634; classwise NOT_ACCURATE F1 falls (0.3123→0.2788), so selective improvement is not uniformly distributed. Output artifacts in `prompt13_results/` and `Citation_Integrity_Prompt13.ipynb`.
- **Methods:** Primary comparison is confidence-selected test subset vs exact expected error of uniformly random matched-k acceptance, checked against 1,000 archived random draws; coverage chart from all archived prefixes; publication-usable PNG/vector PDF figures; success remains retrospective/descriptive.
- **Limits:** Test/model-selection independence unresolved; earlier exploration means not prospective; provisional NEI mapping for 50 test cases, row-level bootstrap ignores citing-article clustering; accepted subset has different label composition. No claim of a deployable calibrated threshold or a newly trained model.
- **Next action:** Confirm the Prompt 13 notebook output in the student's Colab Drive environment; Prompt 14 can then write an evidence-grounded interpretation of both improved overall selective risk and weaker retained NOT_ACCURATE F1.


## D-014 | Prompt 14 | Evidence-based outcome interpretation (2026-11-12)
- **Decision:** Report retrospective, accepted-set selective-error improvement at 80% coverage (+4.018pp, pair-bootstrap descriptive 95% interval +1.913 to +5.914pp), while emphasizing the decline in `NOT_ACCURATE` F1 from 0.3123 to 0.2788. Do not claim uniformly improved error detection or novel model training.
- **Reason:** Although 73/121 abstained cases were errors, 48 were correct; the classifier retains 77 `NOT_ACCURATE`→`ACCURATE` mistakes at 80% coverage. Confidence is informative in aggregate but cannot resolve all subtle citation errors.
- **Evidence:** Saved and independently audited Prompt 12/13 CSV files and original test JSONL; 606 cases, 485 accepted, 195 errors; provisional NEI excluded sensitivity gain +3.39pp. **VERIFIED** for descriptive outcomes; candidate error mechanisms **INFERRED**, not manually verified.
- **Limitations:** Legacy exploratory notebook may have exposed abstention results before newer freeze; checkpoint split/validation provenance uncertain; per-pair bootstrap not article-clustered; top-k acceptance not a calibrated deployable threshold; archived baseline not exact replication of reported paper metrics.
- **Next action:** Prompt 15 draft using this report, with no claims stronger than evidence. Optional follow-ups require clean holdout, paper-grounded error review, or newly held-out class-aware policy evaluation.
- **Artifact:** `prompt14_results_discussion.md`.


## D-015 | Prompt 15 | Evidence-grounded IEEE manuscript draft (2026-11-12)
- **Decision:** Produce one IEEE-style two-column LaTeX experimental manuscript with verified result tables, source-derived figures, a checked scholarly bibliography and explicit uncertainty/limitations. No new model training, invented experiments or unverified novelty claims.
- **Reason:** Prompt 15 requires an experimental paper traceable to the prior literature review and genuine Prompt 12–14 outputs; the user requests one coherent artifact instead of additional notebooks.
- **VERIFIED evidence:** `prompt12_results/experiment_manifest.json`, `prompt12_results/policy_summary.csv`, `prompt13_results/results.csv`, `prompt13_results/classwise_comparison.csv`, `prompt14_results_discussion.md`, four source JSONL files, original literature review, primary publisher/paper metadata for Sarol et al. 2024, Wadden et al. 2020/2022, Geifman & El-Yaniv 2017, Guo et al. 2017, Cohan et al. 2019, Greenberg 2009.
- **Manuscript claims:** 606 saved test cases (268 wrong), top-485 selective risk 195/485 = 40.206%, random-retention expectation 44.224%, +4.018pp difference, pair-level bootstrap descriptive CI +1.913 to +5.914pp; NOT_ACCURATE F1 full 0.3123 vs accepted 0.2788. Earlier exploratory abstention access and uncertain checkpoint split provenance are disclosed, not hidden.
- **UNKNOWN / TO VERIFY:** exact author identity/affiliation/email for submission; venue/instructor template approval; final public repository link; raw source rights; exact checkpoint/split independence; identity of each provisional NEI case.
- **Implementation and layout:** `prompt15_overleaf/main.tex` with `references.bib` and two SVG-independent vector PDF figures; compiled with pdfLaTeX+Biber; source checklist and outline included. No new Colab notebook generated.
- **Next:** Human verification of all placeholders and content; Prompt 16 technical peer review; Prompt 17 repository/readme; Prompt 18 AI provenance audit.

---

## D-015B | Prompt 15 | ACM manuscript revision and repository reference (13 Nov 2026)
- **Decision:** Use the ACM `acmart` two-column `sigconf,nonacm` format instead of the initial IEEE draft; retain all validated Prompt 12–14 numerical results. Revise prose for clarity and incorporate the confirmed institutional affiliation and actual GitHub project URL.
- **Evidence:** User confirmed the revised ACM paper compiled in Overleaf and uploaded its compiled PDF. The uploaded paper states the archived 606-pair evaluation, accepted count 485, error 44.22% versus 40.21%, and GitHub URL in Section 8. **VERIFIED as contents of the user-uploaded PDF and user's compilation confirmation**, not as independent peer-reviewed publication.
- **Caveat:** Public release of the *full* reproducibility package is separate from uploading a PDF. Original model-split independence and provisional labels remain unresolved.

## D-016 | Prompt 16 | Technical review and edits (13 Nov 2026)
- **Decision:** Preserve the bounded retrospective contribution and negative `NOT_ACCURATE` F1 result; expand related work with selective-prediction studies, clarify contributions and official affiliation, and retain explicit integrity caveats.
- **Evidence:** `Prompt16_Technical_Peer_Review.md`; user confirmed importing manuscript updates to Overleaf and completing the author-affiliation correction. **VERIFIED as reported user actions**; no new experimental performance was claimed.
- **Risks:** Source-label correspondence, checkpoint leakage possibilities, and external generalization remain **UNKNOWN**.

## D-017 | Prompt 17 | GitHub reproducibility verification (13 Nov 2026)
- **Decision:** Publish the lightweight CPU evaluation scripts/configuration/aggregate results without redistributing raw input JSONL data or pretrained checkpoints before checking rights.
- **Evidence:** User screenshot of `post mid-sem` repository folder includes `scripts/`, `config/`, `results/`, README, requirements and paper; user confirmed `run_abstention.py` and `evaluate_results.py` were present. A later Colab run cloned/pulled GitHub, executed both scripts successfully, and printed `GITHUB REPRODUCIBILITY TEST: PASSED`. **VERIFIED as user-supplied screenshots/output.**
- **Limit:** The final screenshot demonstrated successful script execution but did not separately print recalculated result metrics. The figures 44.22%, 40.21% and +4.018pp were verified earlier in Prompt 12/13 Colab output. Data access and public repository completeness should be independently checked before a third-party replication claim.
- **Repository:** https://github.com/mai2026011/Awesome-Detecting-misinterpreted-but-genuine-citations/tree/main/post%20mid-sem

## D-018 | Prompt 18 | AI-use and research-integrity provenance prepared (13 Nov 2026)
- **Decision:** Disclose AI support for literature synthesis, research planning, coding, debugging, plotting and manuscript drafting; document real correction cases, the Colab memory issue, the path recovery, scientific verification, and limitations.
- **Evidence:** `ai_assistance_log.md`, `Prompt18_AI_Assistance_Integrity_Report.pdf` and `Prompt18_Human_Reflection.pdf` prepared from conversation history and retained logs. **VERIFIED as generated report artifacts**, with personal reflection pending user's final review.
- **Pending:** User should personally confirm first-person statements and upload the log and final paper/source as required. Creating a report does not prove formal submission.
