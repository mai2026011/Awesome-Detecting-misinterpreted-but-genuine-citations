# Tools Referenced in the Citation Detection Paper Collection

Named systems and toolkits introduced or used across the 21-paper collection for claim/citation verification.

---

## 1. Tool Overview

| Name | Source | Description | Application | Link |
|---|---|---|---|---|
| **VeriSci** | Wadden et al., 2020, EMNLP ("Fact or Fiction") | Three-module baseline pipeline released with SciFact: TF-IDF abstract retrieval → RoBERTa-large rationale selection → SUPPORT/REFUTE/NOINFO label prediction. | The original reference implementation for scientific claim verification; used as a baseline by nearly every later system in this space. | [github.com/allenai/scifact](https://github.com/allenai/scifact) |
| **MultiVerS** | Wadden et al., 2022, Findings of NAACL | Single model that jointly predicts a claim's label and its supporting rationale sentences using full-document context, trained with weak supervision across SciFact, CovidFact, and HealthVer. | Used by Sarol et al. (2024) as one of the claim-verification models for detecting misrepresented biomedical citations. | [github.com/dwadden/multivers](https://github.com/dwadden/multivers) |
| **CliVER** | Liu et al., 2024, JAMIA Open | End-to-end PICO-based claim-verification framework with four modules (document collection, retrieval, sentence selection, label prediction) built for clinical-trial literature. | Verifies drug/treatment claims against PubMed abstracts; also introduced the CoVERt evaluation dataset. | [academic.oup.com/jamiaopen (paper)](https://academic.oup.com/jamiaopen/article/7/1/ooae021/7612234) — no public code release found |
| **FactDetect** | Jafari & Allan, 2024, arXiv preprint | Uses an LLM to decompose evidence into short factual statements, each labeled for relevance to the claim, then folds this into a multitask verification model (and a zero-shot variant, AugFactDetect). | Improves robustness/explainability of claim-verification models — applicable to pinpointing exactly why a citation's claim diverges from its source. | [github.com/nazaninjafar/factdetect](https://github.com/nazaninjafar/factdetect) |
| **HalluCiteChecker** | Sakai, Kamigaito, Watanabe, 2026, arXiv preprint | Lightweight, offline, CPU-only Python toolkit that runs citation extraction → recognition → matching to flag hallucinated (non-existent) citations in seconds on a laptop. | Pre-submission / peer-review checks for authors, reviewers, and program organizers. | [github.com/yusuke1997/HalluCiteChecker](https://github.com/yusuke1997/HalluCiteChecker) |
| **CiteAudit** | Yuan, Shi, et al., 2026, arXiv preprint | Multi-agent framework (Extractor, Memory, Web Search, Scholar, Judge agents) that verifies reference existence and checks metadata/content consistency at scale. | Benchmarking and automated auditing of reference lists in LLM-era papers. | [arxiv.org/abs/2602.23452](https://arxiv.org/abs/2602.23452) — no public code release found |
| **CiteCheck** | 2026, arXiv preprint | Retrieval-grounded pipeline that compares a citation's claimed content against retrieved source text, classifying mismatches including a "minor hallucination" category (real paper, misrepresented content). | Detecting LLM-introduced citation hallucinations in scientific writing. | [arxiv.org/abs/2605.27700](https://arxiv.org/abs/2605.27700) — no public code release found |
| **SemanticCite** | Haan, 2025, arXiv preprint | Deep full-text semantic analysis system (rather than abstract-level/binary checking) that flags citations whose claims are only partially or weakly supported by the source. | Fine-grained, full-text citation verification rather than simple existence checking. | [arxiv.org/abs/2511.16198](https://arxiv.org/abs/2511.16198) — no public code release found |

---

## 2. Relevance to the Research Topic

*Topic: detecting citations that point to a real, existing source but misrepresent, oversimplify, or contradict what that source actually says.*

| Name | Relevant? | Why |
|---|---|---|
| **VeriSci** | 🟡 Foundational | General scientific claim-verification pipeline, not citation-specific — but its retrieval → rationale → label architecture is the template nearly every citation-checking tool below builds on. |
| **MultiVerS** | 🟢 Yes, directly | Directly used to detect misrepresented-but-real biomedical citations (Sarol et al., 2024) — a genuine content-verification model, not just an existence checker. |
| **CliVER** | 🟡 Adjacent | Verifies scientific/clinical claims against literature, but built for standalone claims rather than citation sentences specifically. |
| **FactDetect** | 🟢 Yes, directly | Explicitly designed to explain *why* a claim diverges from evidence — maps directly onto diagnosing how a citation misrepresents its source. |
| **HalluCiteChecker** | 🟡 Partial | Focused on whether a citation *exists at all* (hallucination), not whether an existing citation's content is misrepresented — adjacent but a different failure mode. |
| **CiteAudit** | 🟡 Partial | Primarily an existence/metadata checker; content-consistency checking is only one part of its pipeline. |
| **CiteCheck** | 🟢 Yes, directly | Its "minor hallucination" class (real paper, perturbed/misrepresented content) is exactly the misinterpreted-but-genuine citation problem. |
| **SemanticCite** | 🟢 Yes, directly | Purpose-built to catch "partially supported" citations — genuine citations whose claims are only weakly backed by the source. |

---

**Summary:** MultiVerS, FactDetect, CiteCheck, and SemanticCite are the tools most directly aimed at content-level citation misrepresentation. VeriSci and CliVER are general claim-verification systems that this line of work builds on. HalluCiteChecker and CiteAudit are closer neighbors focused on citation *existence* rather than content accuracy.
