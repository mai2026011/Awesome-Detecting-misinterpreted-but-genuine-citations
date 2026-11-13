"""Prompt 12: retrospective selective classification experiment.
Uses only saved citation-integrity outputs, without loading model weights.
Derived from predeclared Prompt 7 protocol; exploratory data caveats apply.
"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score, precision_recall_fscore_support

LABELS = ["NOT_ACCURATE", "NEI", "ACCURATE"]
HASHES = {
    "claims_dev.jsonl": "52ea0785d06e6b4843ec8b44cf8ee52c1f5d419403ef37f1de499677c154a180",
    "claims_test.jsonl": "ab0692fae3dc6a2cd37f7c7569d077d77e4813574023e38f4c1f0aa58909d495",
    "pred_dev.jsonl": "bc2e54e4701b82f3fc4c4f9890a3e5064e03c92c00b1a832c15c2d1249d55de2",
    "pred_test.jsonl": "6185d47a0f920399ef4b64d8add527e0dd8b58e7f644d05bfc790c6e664e989b",
}

def find_data():
    """Find source files in an optional local root or the original Colab Drive workspace."""
    roots = []
    if os.environ.get("CITATION_PROJECT_ROOT"):
        roots.append(Path(os.environ["CITATION_PROJECT_ROOT"]))
    roots += [Path("/content/drive/MyDrive/CitationIntegrityStudy"), Path("/mnt/data")]
    for root in roots:
        data = root / "data" if (root / "data" / "pred_test.jsonl").exists() else root
        if all((data / name).exists() for name in HASHES):
            out = root / "results" / "prompt12" if data != root else root / "prompt12_results"
            return data, out
    raise FileNotFoundError(
        "Missing source files. Put all four JSONL files in <project>/data/, "
        "set CITATION_PROJECT_ROOT to <project>, or mount Colab Drive."
    )

def read_jsonl(path):
    with path.open(encoding="utf-8") as f:
        return [json.loads(x) for x in f if x.strip()]

def load_split(folder, split):
    claims = read_jsonl(folder / f"claims_{split}.jsonl")
    preds = read_jsonl(folder / f"pred_{split}.jsonl")
    pmap = {p["id"]: p for p in preds}
    assert len(pmap) == len(preds) == len(claims)
    assert set(pmap) == {c["id"] for c in claims}
    rows = []
    for row_pos, c in enumerate(claims):
        assert len(c["cited_doc_ids"]) == 1
        doc = str(c["cited_doc_ids"][0]); cid = c["id"]
        pe = pmap[cid]["evidence"][doc]
        probs = np.array(pe["label_probs"], dtype=float)
        assert probs.shape == (3,) and np.isfinite(probs).all()
        assert (probs >= 0).all() and (probs <= 1).all()
        assert abs(sum(probs) - 1) < 0.001
        assert LABELS[int(np.argmax(probs))] == pe["label"]
        ge = c["evidence"]
        if ge:
            assert set(ge) == {doc}
            g = {item["label"] for item in ge[doc]}
            assert len(g) == 1 and next(iter(g)) in LABELS
            gold = next(iter(g)); provisional = False
        else:
            gold = "NEI"; provisional = True
        rows.append({
            "split": split, "claim_id": cid, "doc_id": doc, "source_row": row_pos,
            "claim": c["claim"], "gold": gold, "pred": pe["label"],
            "provisional_nei": provisional,
            "p_not_accurate": probs[0], "p_nei": probs[1], "p_accurate": probs[2],
            "correct": int(gold == pe["label"]), "confidence": float(probs.max()),
            "margin": float(np.sort(probs)[-1] - np.sort(probs)[-2]),
            "negative_entropy": float(np.sum(np.where(probs > 0, probs * np.log(np.clip(probs, 1e-30, 1)), 0)))
        })
    result = pd.DataFrame(rows)
    assert not result.duplicated(["split","claim_id","doc_id"]).any()
    return result

def ordered(df, score):
    return df.sort_values([score, "claim_id", "doc_id", "source_row"],
                          ascending=[False,True,True,True], kind="mergesort").reset_index(drop=True)

def k_for(n, coverage):
    return int(math.floor(n * coverage + 0.5))

def selective_stats(df, coverage, score="confidence"):
    sorted_df = ordered(df, score)
    k = k_for(len(df), coverage)
    accepted = sorted_df.iloc[:k]
    error = float(1 - accepted["correct"].mean())
    return accepted, {"policy": score, "n":len(df), "coverage_target":coverage,
                      "k":k, "coverage_realized": k/len(df),
                      "risk": error, "macro_f1": f1_score(accepted["gold"],accepted["pred"],labels=LABELS,average="macro",zero_division=0)}

def main():
    data_dir, out = find_data()
    out.mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(exist_ok=True)
    actual = {n: hashlib.sha256((data_dir/n).read_bytes()).hexdigest() for n in HASHES}
    assert actual == HASHES, "Input file hash changed relative to frozen Prompt 7; stop and review"
    dev = load_split(data_dir,"dev")
    df = load_split(data_dir,"test")
    assert (len(dev),len(df)) == (316,606)
    assert (int(dev["provisional_nei"].sum()), int(df["provisional_nei"].sum())) == (24,50)
    assert (int(dev["correct"].sum()), int(df["correct"].sum())) == (215,338)
    baseline = 1 - df["correct"].mean()
    grid = [0.7,0.8,0.9,1.0]
    summaries = []
    for c in grid:
        a, stat = selective_stats(df,c)
        stat["random_expected_risk"] = float(baseline)
        stat["gain_over_random_pp"] = 100 * (baseline - stat["risk"])
        summaries.append(stat)
    summary = pd.DataFrame(summaries)
    summary.to_csv(out/"policy_summary.csv",index=False)

    # Primary comparison, 1000 uniform random matched-k subsets
    k = k_for(len(df), .8)
    accepted, chosen = selective_stats(df,.8)
    rng = np.random.default_rng(42)
    errors = 1 - df["correct"].to_numpy(dtype=float)
    random_risks = np.array([errors[rng.choice(len(df),size=k,replace=False)].mean() for _ in range(1000)])
    pd.DataFrame({"draw":np.arange(1,1001), "risk":random_risks}).to_csv(out/"random_retention_draws.csv", index=False)

    # 2000 percentile bootstrap CI of expected random risk minus confidence-selected risk
    rng = np.random.default_rng(2026)
    deltas = []
    confidences = df["confidence"].to_numpy()
    claimids = df["claim_id"].to_numpy()
    docids = df["doc_id"].astype(int).to_numpy()
    for b in range(2000):
        draw = rng.integers(0,len(df),size=len(df))
        # final tie-break by bootstrap draw position, not original source index
        ranks = np.lexsort((np.arange(len(df)), docids[draw], claimids[draw], -confidences[draw]))
        full_risk = errors[draw].mean()
        selected_risk = errors[draw[ranks[:k]]].mean()
        deltas.append(full_risk - selected_risk)
    ci_lo,ci_hi = np.percentile(deltas,[2.5,97.5])
    pd.DataFrame({"replicate":np.arange(1,2001), "delta":deltas}).to_csv(out/"bootstrap_effects.csv", index=False)

    # Per-case selection and risks at every prefix size
    sorted_df = ordered(df,"confidence").copy()
    sorted_df["confidence_rank"] = np.arange(1,len(df)+1)
    sorted_df["cumulative_risk"] = (1 - sorted_df["correct"]).cumsum() / sorted_df["confidence_rank"]
    sorted_df["coverage"] = sorted_df["confidence_rank"]/len(df)
    for c in grid:
        sorted_df[f"accepted_{round(c*100)}pct"] = sorted_df["confidence_rank"] <= k_for(len(df),c)
    sorted_df.to_csv(out/"per_case_selection.csv",index=False)
    riskcurve = sorted_df[["confidence_rank","coverage","cumulative_risk"]].rename(columns={"cumulative_risk":"selective_risk"})
    riskcurve.to_csv(out/"risk_coverage.csv",index=False)
    aurc = riskcurve["selective_risk"].mean()

    # Class-level diagnostics (accepted at 80%)
    p,r,f,s = precision_recall_fscore_support(accepted["gold"], accepted["pred"], labels=LABELS, zero_division=0)
    classrows=[]
    for j,label in enumerate(LABELS):
        gold_rows = accepted[accepted.gold.eq(label)]
        classrows.append({"label":label,"gold_accepted":int(s[j]),"wrong_among_gold_accepted":int((1-gold_rows.correct).sum()),
                          "precision":p[j],"recall":r[j],"f1":f[j]})
    classwise = pd.DataFrame(classrows)
    classwise.to_csv(out/"classwise_errors.csv",index=False)
    accepted[accepted.correct.eq(0)].head(5).to_csv(out/"five_high_confidence_mistakes.csv",index=False)

    # Analyses defined as secondary only; never replace primary conclusion
    extra=[]
    for score in ["margin","negative_entropy"]:
        _,z = selective_stats(df,.8,score)
        extra.append({"score":score,"risk_80pct":z["risk"],"gain_vs_random_pp":100*(baseline-z["risk"])})
    pd.DataFrame(extra).to_csv(out/"alternative_scores_exploratory.csv",index=False)
    explicit = df[~df.provisional_nei].copy()
    explicit_baseline = 1-explicit.correct.mean()
    exp_accepted,exp_z = selective_stats(explicit,.8)
    sensitivity = {"n_explicit":len(explicit),"k_80pct":len(exp_accepted),"full_risk":explicit_baseline,
                   "confidence_risk":exp_z["risk"],"delta":explicit_baseline-exp_z["risk"]}
    pd.DataFrame([sensitivity]).to_csv(out/"explicit_label_sensitivity.csv",index=False)

    fig,ax = plt.subplots(figsize=(7,4.5))
    ax.plot(riskcurve.coverage,riskcurve.selective_risk,label="Confidence selection")
    ax.axhline(baseline,linestyle="--",label="Expected random selection")
    ax.set(xlabel="Coverage (accepted fraction)",ylabel="Selective error rate",title="Risk vs coverage: archived test predictions")
    ax.legend(); ax.grid(alpha=0.3); fig.tight_layout(); fig.savefig(out/"figures"/"risk_coverage.png",dpi=180);plt.close(fig)
    fig,ax = plt.subplots(figsize=(6,4))
    ax.bar(classwise.label, classwise.wrong_among_gold_accepted)
    ax.set(ylabel="Wrong accepted predictions", title="Errors by gold class at 80% coverage")
    fig.tight_layout();fig.savefig(out/"figures"/"classwise_errors.png",dpi=180);plt.close(fig)

    delta = float(baseline - chosen["risk"])
    success = delta >= .03 and ci_lo > 0
    manifest = {
        "source_sha256": actual,"sample_count_test":len(df),"provisional_nei_test_count":int(df.provisional_nei.sum()),
        "primary_coverage":.8,"selected_k":k,"baseline_risk":float(baseline),
        "confidence_risk":chosen["risk"],"delta":delta,
        "random_mc_risk_mean":float(random_risks.mean()),"random_expected_risk":float(baseline),
        "bootstrap_ci_95":[float(ci_lo),float(ci_hi)],"bootstrap_reps":2000,"bootstrap_seed":2026,
        "random_reps":1000,"random_seed":42,"aurc":float(aurc),
        "success_3pp_and_positive_ci":bool(success),"research_status":"Retrospective descriptive; earlier exploratory access and test-validation risk prevent prospective significance claims"
    }
    (out/"experiment_manifest.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    report=f"""# Prompt 12 — Retrospective confidence-abstention experiment\n\n**Study type:** frozen archived predictions, no neural-model training. This is an exploratory/retrospective comparison: old notebook already contained exploratory analyses and the original test fold may have been used as model validation.\n\n## Primary 80%-coverage result\n\n- Examples: 606 test claim-document pairs; accept {k}, reject {len(df)-k}.\n- Full-classifier error = exact expected 80%-random-selection error: **{baseline:.4%}**.\n- Confidence-selected error: **{chosen['risk']:.4%}**.\n- Gain (random expected error − confidence error): **{delta*100:+.2f} percentage points**.\n- Random 1000-run mean error: **{random_risks.mean():.4%}** (simulation sanity check).\n- 2,000 bootstrap percentile 95% interval on gain: **[{ci_lo*100:+.2f}, {ci_hi*100:+.2f}] percentage points**. Pair-level, descriptive only.\n- Frozen practical success rule: gain ≥ 3pp **and** CI lower bound > 0: **{'met' if success else 'NOT met'}**.\n\n## Supporting findings\n\n- Discrete AURC: {aurc:.5f}.\n- Explicit-label-only sensitivity (n={len(explicit)}, k={len(exp_accepted)}): gain {100*sensitivity['delta']:+.2f}pp.\n- Avoid interpreting NEI as verified IRRELEVANT: 50 test rows use provisional NEI mapping.\n- Main caveats: non-independent test possible; original training/validation provenance unresolved; multiple claims may be clustered by citing article; repeated exploratory study means no valid prospective pre-registration assertion.\n- Confidence selection is based on top-{k} over the actual test pool, not a deployable fixed threshold.\n\nSee `policy_summary.csv`, `classwise_errors.csv`, `five_high_confidence_mistakes.csv`, `risk_coverage.csv`, and `experiment_manifest.json` for traceable raw outputs.\n"""
    (out/"prompt12_results_summary.md").write_text(report,encoding="utf-8")
    print("INPUT FILE HASHES: VERIFIED")
    print("TEST BASELINE: 338 correct / 606; error =",round(float(baseline),5))
    print("PRIMARY 80%: accepted",k,"confidence risk",round(chosen["risk"],5))
    print("EXPECTED RANDOM risk",round(float(baseline),5),"Monte Carlo mean",round(float(random_risks.mean()),5))
    print("GAIN (percentage points)",round(delta*100,3),"bootstrap 95% CI",[round(100*ci_lo,3),round(100*ci_hi,3)])
    print("Frozen success rule met?",success)
    print("Results folder:",out)
    print("--- Other coverage results ---")
    print(summary[["coverage_target","k","risk","gain_over_random_pp","macro_f1"]].round(4).to_string(index=False))
    print("--- Explicit labels sensitivity ---")
    print(sensitivity)
    return manifest

if __name__ == "__main__":
    main()
