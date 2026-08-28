# Awesome Detecting Misinterpreted but Genuine Citations

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of papers, tools, datasets, and resources for detecting citations that are **real and verifiable** but whose meaning, claim, or context has been **misquoted, misrepresented, or misinterpreted** — as distinct from fabricated or "hallucinated" citations that don't exist at all.

Most existing citation-checking work focuses on one failure mode: does this reference exist? A separate, subtler failure mode gets far less attention: the reference is completely genuine, but the claim attributed to it does not match what the source actually says. This list tracks work on that second problem.

## Contents

- [Papers](paper/Detecting_Misinterpreted_Genuine_Citations.pdf)
- [Tools & Frameworks](tools/tools.md)
- [Datasets & Benchmarks](datasets/datasets_report.md)
- [Related Awesome Lists](github repositories/github_repositories.md)

- [License](LICENSE)

## Motivation

Citation problems generally fall into a few buckets:

1. **Fabricated / hallucinated references** — the cited work does not exist.
2. **Metadata errors** — wrong year, authors, venue, or DOI for a real work.
3. **Misinterpreted but genuine citations** — the source is real and correctly identified, but the claim attributed to it is not actually supported by (or is a distortion of) what the source says.

Bucket 3 is easy for both humans and automated checkers to miss, since a lookup against a bibliographic database (CrossRef, Semantic Scholar, OpenAlex, arXiv) will succeed — the reference "checks out" even though the citation is misleading. This repository focuses on that gap.

## Papers

- [**Source or It Didn't Happen: A Multi-Agent Framework for Citation Hallucination Detection**](https://arxiv.org/html/2605.08583v1) — introduces a benchmark that explicitly separates fabricated citations from genuine ones incorrectly flagged as suspicious, and reports that LLM judges have a well-known tendency to flag genuine citations as suspicious. Code: [aaFrostnova/CiteTracer](https://github.com/aaFrostnova/CiteTracer).
- [**Detecting Hallucinated and Suspicious Citations: What Current Tools Can and Cannot Do**](https://arxiv.org/html/2607.22693v1) — a survey covering non-existent sources, incorrect DOIs, author/title/venue inconsistencies, and citations that look convincing but can't be verified.

*(Add papers as you find them — see [Contributing](#contributing).)*

## Tools & Frameworks

See [`github_repositories.md`](github_repositories.md) for the full curated list of related GitHub repositories and codebases.

## Datasets & Benchmarks

- Benchmarks that label citations by failure type (non-academic source routing, fabricated reference, peripheral-metadata error, genuine-but-misjudged) are the most directly relevant, since they let tools be scored on false positives against genuine citations, not just recall on fabrications.

*(Add datasets/benchmarks as you find them.)*

## Related Awesome Lists

- [awesome-hallucination-detection](https://github.com/EdinburghNLP/awesome-hallucination-detection) — papers on hallucination detection in LLMs generally.
- [Awesome_papers_on_LLMs_detection](https://github.com/Xianjun-Yang/Awesome_papers_on_LLMs_detection) — papers on detecting LLM-generated text and code.

## Contributing

Contributions welcome! Please read the [awesome list guidelines](https://github.com/sindresorhus/awesome/blob/main/contributing.md) before submitting a pull request. In general:

- One item per line, with a short, neutral description.
- Prefer primary sources (paper, official repo) over aggregators.
- Keep new entries scoped to *misinterpreted-but-genuine* citation detection, not citation-checking in general.

## License

[MIT](LICENSE)
