# 20 Verified Scholarly Papers: Detecting Misinterpreted but Genuine Citations through Automated Claim Verification

*Updated: every entry below now has a real, verified DOI/arXiv link. In the original document, every entry showed only the literal placeholder text "Paper / DOI" with no actual hyperlink — none of the 21 links had been filled in. All links below were checked against PubMed, ACL Anthology, arXiv, publisher pages, or Crossref-listed DOIs.*

This list focuses on citations that exist and point to a real source but whose content is mischaracterized, oversimplified, contradicted, or otherwise misrepresented by the citing text (as opposed to fabricated/hallucinated citations, which are included only where directly relevant to the verification methods used).

## Survey and Review Papers

**Quotation accuracy in medical journal articles — a systematic review and meta-analysis**
Hannah Jergas, Christopher Baethge, 2015, PeerJ
[Paper / DOI](https://doi.org/10.7717/peerj.1364)
Landmark meta-analysis of 28 studies synthesizing quotation/citation error rates (~25%) across medical fields; the classification of major vs. minor quotation errors underpins most later automated detection schemes.

**Accuracy of cited "facts" in medical research articles: A review of study methodology and recalculation of quotation error rate**
Scott A. Mogull, 2017, PLOS ONE
[Paper / DOI](https://doi.org/10.1371/journal.pone.0184727)
Reviews methodological inconsistencies across quotation-accuracy studies and recalculates a pooled error rate, providing a methodological baseline for what "misrepresentation" means in citation-checking research.

**How do authors perceive the way their work is cited? Findings from a large-scale survey on quotation accuracy**
Simon Wakeling, Monica Lestari Paramita, Stephen Pinfield, 2025, Journal of the Association for Information Science and Technology (JASIST)
[Paper / DOI](https://doi.org/10.1002/asi.70000)
Recent survey synthesizing 23 quotation-accuracy studies and directly surveying cited authors about misrepresentation, bridging manual citation-accuracy research and computational detection needs.

**Quotation errors in general science journals**
Neal Smith Jr, Aaron Cumberledge, 2020, Proceedings of the Royal Society A
[Paper / DOI](https://doi.org/10.1098/rspa.2020.0538)
Reviews the long-running cross-disciplinary literature on quotation/citation error rates and situates the "citation vs. quotation accuracy" distinction that automated systems must operationalize.

## Foundational Papers

**How citation distortions create unfounded authority: analysis of a citation network**
Steven A. Greenberg, 2009, BMJ
[Paper / DOI](https://doi.org/10.1136/bmj.b2680)
Foundational study formalizing "citation distortion" (bias, amplification, invention) — genuine citations that collectively misrepresent a claim's evidentiary support — and a conceptual ancestor of automated misrepresentation detection.

**FEVER: a Large-scale Dataset for Fact Extraction and VERification**
James Thorne, Andreas Vlachos, Christos Christodoulopoulos, Arpit Mittal, 2018, NAACL-HLT
[Paper / DOI](https://aclanthology.org/N18-1074/)
Foundational general-domain claim verification dataset/task (SUPPORTS/REFUTES/NOT ENOUGH INFO) whose pipeline architecture (retrieval → evidence selection → entailment) underlies nearly all later scientific claim/citation verification systems.

**Argumentative Zoning: Information Extraction from Scientific Text**
Simone Teufel, 1999, PhD Thesis, University of Edinburgh
[Paper / DOI](http://hdl.handle.net/1842/11456)
Establishes the rhetorical-status framework for analyzing what a citing sentence is actually claiming about a source, foundational to later work distinguishing accurate from misleading citation function.

**Automatic Classification of Citation Function**
Simone Teufel, Advaith Siddharthan, Dan Tidhar, 2006, EMNLP
[Paper / DOI](https://doi.org/10.3115/1610075.1610091)
First large-scale automated classifier of why a citation is made (e.g., contrast, basis, weakness); a direct precursor to systems that must first understand citation intent before judging whether the citation misrepresents its source.

## Recent Research Papers

**Assessing citation integrity in biomedical publications: corpus annotation and NLP models**
Maria Janina Sarol, Shufan Ming, Shruthan Radhakrishna, Jodi Schneider, Halil Kilicoglu, 2024, Bioinformatics (Oxford Academic)
[Paper / DOI](https://doi.org/10.1093/bioinformatics/btae420)
Directly on-topic: builds a 3,063-instance annotated corpus of genuine biomedical citations labeled ACCURATE/NOT_ACCURATE/IRRELEVANT with fine-grained error types (misquote, oversimplify, contradict), and trains claim-verification NLP models (BM25+MonoT5 retrieval + MultiVerS) to detect misrepresented-but-real citations.

**SemanticCite: Citation Verification with AI-Powered Full-Text Analysis and Evidence-Based Reasoning**
Sebastian Haan, 2025, arXiv preprint (arXiv:2511.16198)
[Paper / DOI](https://arxiv.org/abs/2511.16198)
Proposes deep full-text semantic analysis (vs. abstract-level/binary approaches) to identify subtle, "partially supported" citation issues — genuine citations whose claims are only weakly backed by the source.
*(Note: the original entry listed no author and dated this "2025/2026"; it is Sebastian Haan, posted to arXiv in November 2025.)*

**CiteAudit: You Cited It, But Did You Read It? A Benchmark for Verifying Scientific References in the LLM Era**
Zhengqing Yuan, Kaiwen Shi, et al., 2026, arXiv preprint (arXiv:2602.23452)
[Paper / DOI](https://arxiv.org/abs/2602.23452)
Introduces a multi-agent (Extractor, Memory, Web Search, Scholar, Judge) framework and benchmark for verifying reference existence and metadata/content consistency at scale.

**CiteCheck: Retrieval-Grounded Detection of LLM Citation Hallucinations in Scientific Text**
2026, arXiv preprint (arXiv:2605.27700)
[Paper / DOI](https://arxiv.org/abs/2605.27700)
Frames citation checking as grounded retrieval plus structured metadata/content comparison; its "minor hallucination" class (real paper, perturbed/misrepresented content) closely maps to the misinterpreted-but-genuine citation problem.

**HalluCiteChecker: A Lightweight Toolkit for Hallucinated Citation Detection and Verification in the Era of AI Scientists**
Yusuke Sakai, Hidetaka Kamigaito, Taro Watanabe, 2026, arXiv preprint (arXiv:2604.26835)
[Paper / DOI](https://arxiv.org/abs/2604.26835)
Formalizes automated citation verification as an NLP task and delivers an offline, CPU-only toolkit intended for pre-submission and peer-review checks, distinguishing existence errors from content-support errors.

## Methods / Algorithms

**Fact or Fiction: Verifying Scientific Claims**
David Wadden, Shanchuan Lin, Kyle Lo, Lucy Lu Wang, Madeleine van Zuylen, Arman Cohan, Hannaneh Hajishirzi, 2020, EMNLP
[Paper / DOI](https://aclanthology.org/2020.emnlp-main.609/)
Introduces the SciFact task/dataset and a three-stage pipeline (document retrieval → rationale sentence selection → SUPPORTS/REFUTES/NOINFO entailment) that is the core algorithmic template used to check whether a citation's claim is actually backed by its source.

**Robust Claim Verification Through Fact Detection**
Nazanin Jafari, James Allan, 2024, arXiv preprint (arXiv:2407.18367)
[Paper / DOI](https://arxiv.org/abs/2407.18367)
Proposes FactDetect, which extracts and labels short factual statements from evidence to improve robustness and explainability of claim-verification models, directly applicable to pinpointing why a citation's claim diverges from its source.

**Scientific Claim Verification with Fine-Tuned NLI Models**
Miloš Košprdić, Adela Ljajić, Darija Medvecki, Bojana Bašaragin, Nikola Milošević, 2024, Proceedings of the 16th International Joint Conference on Knowledge Discovery, Knowledge Engineering and Knowledge Management (IC3K 2024) — KMIS track
[Paper / DOI](https://doi.org/10.5220/0012900000003838)
Reframes claim–evidence relationship classification as textual entailment (NLI) using fine-tuned transformer models on SciFact, offering a lightweight methodological alternative for support/contradiction detection.

**Retrieval Augmented Scientific Claim Verification**
Hao Liu, Ali Soroush, Jordan G. Nestor, Elizabeth Park, Betina Idnay, Yilu Fang, Jane Pan, Stan Liao, Marguerite Bernard, Yifan Peng, Chunhua Weng, 2024, JAMIA Open (Oxford Academic)
[Paper / DOI](https://doi.org/10.1093/jamiaopen/ooae021)
Combines retrieval augmentation with fine-tuned entailment models across FEVER, SciFact, and manually curated corpora to improve detection of claims not actually supported by their evidence — reducing the error propagation problem in earlier pipelines.

## Applications

**Quotation Accuracy Matters: An Examination of How an Influential Meta-Analysis on Active Learning Has Been Cited**
Amedee Marchand Martella, Jane Kinkus Yatcilla, Ronald C. Martella, et al., 2021, Review of Educational Research
[Paper / DOI](https://doi.org/10.3102/0034654321991228)
Applied, large-scale manual audit (later informing automated approaches) showing over a third of citing articles made unsupported assertions about a single influential paper — a concrete real-world case of the problem automated tools aim to catch at scale.

**Compound Deception in Elite Peer Review: A Failure Mode Taxonomy of 100 Fabricated Citations at NeurIPS 2025**
Samar Ansari, 2026, arXiv preprint (arXiv:2602.05930)
[Paper / DOI](https://arxiv.org/abs/2602.05930)
Applied taxonomy of citation failures at a top-tier venue, arguing for mandatory automated verification at submission; useful for grounding claim-verification tools in a real peer-review application context.

## Evaluation Methods / Benchmarks

**SciFact-Open: Towards Open-Domain Scientific Claim Verification**
David Wadden, Kyle Lo, Bailey Kuehl, Arman Cohan, Iz Beltagy, Lucy Lu Wang, Hannaneh Hajishirzi, 2022, Findings of EMNLP
[Paper / DOI](https://aclanthology.org/2022.findings-emnlp.347/)
Extends SciFact to an open-domain retrieval setting over a large corpus, providing a harder, more realistic benchmark for whether a claim is genuinely supported, refuted, or unaddressed by candidate cited sources.

**SciClaimHunt: A Large Dataset for Evidence-based Scientific Claim Verification**
Sujit Kumar, Anshul Sharma, Siddharth Hemant Khincha, Gargi Shroff, Sanasam Ranbir Singh, Rahul Mishra, 2025, arXiv preprint (arXiv:2502.10003)
[Paper / DOI](https://arxiv.org/abs/2502.10003)
Introduces a large-scale evidence-based scientific claim verification dataset built from a broader publicly available claim corpus, providing a distinct, larger-scale benchmark complementary to SciFact for training and evaluating support/refute classification models.

---

*Note: This is an actively evolving research area (most items dated 2024–2026). Several arXiv preprints listed are not yet peer-reviewed (CiteAudit, CiteCheck, HalluCiteChecker, SemanticCite, Compound Deception, Robust Claim Verification Through Fact Detection, SciClaimHunt) — verify current publication status before citing formally, as some may have since been accepted at a venue.*
