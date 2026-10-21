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

## Next actions
1. Attach the primary papers above.
2. Answer the Stage 0 constraint questions.
3. Proceed to Stage 1: evidence-based gap identification.
