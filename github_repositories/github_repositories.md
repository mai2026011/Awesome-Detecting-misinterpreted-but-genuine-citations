# GitHub Repositories

A curated list of GitHub repositories related to citation verification, reference hallucination detection, and quote/claim-checking tools. Most existing tools target *fabricated* references; the ones most relevant to *misinterpreted-but-genuine* citations are noted below.

| Repository | Description |
|---|---|
| [aaFrostnova/CiteTracer](https://github.com/aaFrostnova/CiteTracer) | Multi-agent framework for citation hallucination detection. Directly relevant: it explicitly benchmarks against genuine citations that get incorrectly flagged as suspicious, and reports the false-positive rate of LLM judges on that failure mode. |
| [gianlucasb/hallucinator](https://github.com/gianlucasb/hallucinator) | Extracts references from academic PDFs and checks them against CrossRef, arXiv, DBLP, and OpenAlex to flag likely-fabricated citations. Existence-checking only; does not verify claim-to-source alignment. |
| [markrussinovich/refchecker](https://github.com/markrussinovich/refchecker) | Validates academic paper references — citation errors, fabricated references, and metadata mismatches — with a web UI, CLI, and desktop app. |
| [davidjurgens/hallucinated-reference-finder](https://github.com/davidjurgens/hallucinated-reference-finder) ("halref") | Tool for finding hallucinated (non-existent) references. |
| [EdinburghNLP/awesome-hallucination-detection](https://github.com/EdinburghNLP/awesome-hallucination-detection) | General curated list of papers on hallucination detection in LLMs (broader scope than citations alone). |
| [Xianjun-Yang/Awesome_papers_on_LLMs_detection](https://github.com/Xianjun-Yang/Awesome_papers_on_LLMs_detection) | Curated papers on detecting LLM-generated text and code. |

## Notes

- Most tools above solve **existence verification** (does the source exist, do the metadata match) rather than **claim verification** (does the source actually say what it's cited for). If you know of a tool that specifically checks whether a genuine citation's claim matches its source content, please add it here.
- Entries are ordered by relevance to the misinterpreted-but-genuine problem, not alphabetically.

*(Contributions welcome — see the main [README](README.md#contributing).)*
