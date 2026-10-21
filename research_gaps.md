# Candidate Research Gaps

Project: Detecting Misinterpreted but Genuine Citations through Automated Claim Verification
Source: the literature review (main__1_.pdf), analysed in Stage 1
Status: candidate gaps only. No novelty is claimed until a documented literature search (queries and dates recorded) is done in Stage 2.

Evidence labels
- VERIFIED: the review states it.
- Review-attributed: the review attributes it to an original paper; the original wording is UNKNOWN until that paper is attached.
- INFERRED: my reasoning, not yet checked.
- UNKNOWN: no evidence yet.

---

## G1. Where do end-to-end errors originate?

- Review passages: Sec. 4.3 (diagnostic protocol), Sec. 3.6, Sec. 6.2
- Source type: the review's own proposal, plus the review-attributed difficulty of evidence retrieval. That this is untested for the chosen pipeline is INFERRED.
- Experimental question: For a Sarol-style pipeline, what share of misclassifications is caused by context extraction, retrieval, or verification?
- Test: oracle ablations (gold vs. automatic context, gold vs. retrieved evidence). Report recall@k and MRR for retrieval, and macro-F1 per condition.
- Needs: dataset with annotated evidence spans and access to reference full texts (both UNKNOWN).

## G2. Sensitivity of the verifier to the evidence it is shown

- Review passages: Sec. 3.7 (Zhang and Abernethy), Sec. 6.4 and 7.4 (OpenScholar), Sec. 6.4 (retrieval failure vs. source non-support)
- Source type: review-attributed findings (original wording UNKNOWN); the experimental design is INFERRED.
- Experimental question: How does accuracy change as evidence moves from abstract, to top-k passages, to oracle spans, to full text? Can the verifier separate retrieval failure from true non-support?
- Test: fixed verifier and prompts, controlled context conditions. Measure macro-F1, error-class recall, and rate of "insufficient evidence" outputs.
- Needs: same data as G1, plus model access (cost UNKNOWN).

## G3. Recovering fine-grained error types

- Review passages: Table 1, Sec. 7.2
- Source type: the taxonomy is the review's own. Whether Sarol et al. annotate subtypes is UNKNOWN.
- Experimental question: Can omission, overstatement, transformation, reversal and unsupported inference be predicted, and which are hardest?
- Test: if the original annotation has subtypes, map them to Table 1 and report per-type precision and recall. Otherwise run a small pilot annotation with inter-annotator agreement.
- Risk: may require new labelling; agreement may be low.

## G4. Calibration and abstention for subtle errors

- Review passages: Sec. 3.6 (GPT-4 better on accurate than erroneous citations), Sec. 7.4, Sec. 6.2
- Source type: review-attributed result plus the review's own recommendation. The reading that macro-F1 below micro-F1 signals weaker minority-class performance is INFERRED.
- Experimental question: Does confidence-based abstention improve error detection at acceptable coverage?
- Test: calibration (ECE), risk-coverage curves, precision at fixed recall for flagged errors, class-wise PR curves. Compare a fine-tuned verifier with an LLM.
- Needs: a reproducible baseline or its outputs.

## G5. Cross-domain transfer

- Review passages: Sec. 6.3, 7.1, 7.7
- Source type: the review's own claim that direct evidence is concentrated in biomedical literature. INFERRED until a documented search supports it.
- Experimental question: How much does a biomedical-trained verifier degrade on other domains?
- Test: out-of-domain evaluation on a non-biomedical citation-fidelity set. Isik and Guleryuzlu is relevance scoring, not fidelity labels, so it may not fit.
- Risk: likely no suitable labelled data; new annotation probably needed.

---

## Ranking (INFERRED)

Assumes a single researcher, limited compute and public data only. Resources are UNKNOWN. Scores 1 to 5, higher is better.

| Rank | Gap | Significance | Resources | Feasibility | Main dependency |
|---|---|---|---|---|---|
| 1 | G1 | 4 | 4 | 4 | Evidence spans and full texts available |
| 2 | G4 | 4 | 4 | 4 | Reproducible baseline or its outputs |
| 3 | G2 | 3 | 3 | 4 | Model access and cost |
| - | G3 | 4 | 2 | 2 | Label availability |
| - | G5 | 4 | 1 | 1 | New annotated data |

Suggested combination: treat G1 and G2 as one study (shared oracle-evidence design) and add G4 as an analysis layer on the same outputs.

## Claims to verify against original publications

1. Sarol et al.: 3,063 instances, 100 articles, 39.18% errors, 0.59 micro-F1, 0.52 macro-F1, the exact label set, and whether {accurate, not accurate, irrelevant} in Eq. (1) matches it.
2. Which Sarol pipeline produced the best score, and whether GPT-4 was zero- or few-shot.
3. Whether the Sarol dataset, evidence spans and code are public (UNKNOWN; no link assumed).
4. Zhang and Abernethy: "general domain" in the text vs. "general domain, with biomedical examples" in Table 2; dataset, models, venue.
5. OpenScholar: the 45M-paper figure and the retrieval-quantity claim.
6. Isik and Guleryuzlu: 121 articles, 5,615 pairs, expert validation method.
7. Huang et al.: dataset, metrics and findings (Table 2 is too vague to use as a baseline).
8. SciFact "about 1.4K" claims and MultiVerS dataset list.
9. Greenberg and Mogull: error-rate framing in the Introduction.

## Next actions

- [ ] Attach the Sarol et al. 2024 paper and data-availability section
- [ ] Share compute budget and supervisor or venue constraints
- [ ] Stage 2: documented literature search to test each gap for prior work
