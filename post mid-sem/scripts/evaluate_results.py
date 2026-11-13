"""Prompt 13: audit and present archived Prompt 12 results.
Reproduction status: retrospective; no training or threshold fitting.
Dependencies: numpy, pandas, matplotlib, scikit-learn (Colab CPU default).
"""
from pathlib import Path
import os, json, hashlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support

LABELS = ["NOT_ACCURATE", "NEI", "ACCURATE"]
SHA256 = {
    "claims_dev.jsonl": "52ea0785d06e6b4843ec8b44cf8ee52c1f5d419403ef37f1de499677c154a180",
    "claims_test.jsonl": "ab0692fae3dc6a2cd37f7c7569d077d77e4813574023e38f4c1f0aa58909d495",
    "pred_dev.jsonl": "bc2e54e4701b82f3fc4c4f9890a3e5064e03c92c00b1a832c15c2d1249d55de2",
    "pred_test.jsonl": "6185d47a0f920399ef4b64d8add527e0dd8b58e7f644d05bfc790c6e664e989b"
}

def paths():
    candidates = [Path(os.environ.get('CITATION_PROJECT_ROOT', '/content/drive/MyDrive/CitationIntegrityStudy')), Path('/mnt/data')]
    for root in candidates:
        data = root / 'data' if (root/'data'/'pred_test.jsonl').exists() else root
        p12 = root/'results'/'prompt12'
        if not p12.exists(): p12 = root/'prompt12_results'
        if all((data/name).exists() for name in SHA256) and (p12/'experiment_manifest.json').exists():
            p13 = root/'results'/'prompt13' if (root/'data').exists() else root/'prompt13_results'
            p13.mkdir(parents=True, exist_ok=True)
            (p13/'figures').mkdir(parents=True, exist_ok=True)
            return data,p12,p13
    raise FileNotFoundError('Mount Google Drive and check MyDrive/CitationIntegrityStudy/data and results/prompt12; or use a local copy of the Prompt12 results.')

def load_jsonl(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def raw_map(data, split):
    claims=load_jsonl(data/f'claims_{split}.jsonl')
    preds=load_jsonl(data/f'pred_{split}.jsonl')
    p_by_id={p['id']:p for p in preds}
    assert len(claims)==len(preds)==len(p_by_id), f'{split} duplicate/missing claim ids'
    assert set(p_by_id)=={c['id'] for c in claims}
    rows=[]
    for i,c in enumerate(claims):
        assert len(c['cited_doc_ids'])==1
        doc=str(c['cited_doc_ids'][0]); c_id=c['id']
        pred=p_by_id[c_id]['evidence'][doc]
        probs=np.asarray(pred['label_probs'],dtype=float)
        assert probs.shape==(3,) and np.isfinite(probs).all() and ((probs>=0)&(probs<=1)).all()
        assert np.isclose(probs.sum(),1,atol=.001)
        assert pred['label']==LABELS[probs.argmax()]
        evidence=c['evidence']
        if evidence:
            assert set(evidence)=={doc}
            glabels={e['label'] for e in evidence[doc]}
            assert len(glabels)==1
            gold=next(iter(glabels)); provisional=False
        else:
            gold='NEI'; provisional=True
        assert gold in LABELS
        rows.append({'split':split,'claim_id':c_id,'doc_id':doc,'source_row':i,
                     'gold':gold,'pred':pred['label'],'provisional_nei':provisional,
                     'p_not_accurate':probs[0],'p_nei':probs[1],'p_accurate':probs[2],
                     'correct':int(gold==pred['label']),'confidence':float(probs.max())})
    return pd.DataFrame(rows)

def draw_and_save(fig, folder, basename):
    fig.savefig(folder/f'{basename}.png', dpi=220, bbox_inches='tight')
    fig.savefig(folder/f'{basename}.pdf', bbox_inches='tight')
    plt.close(fig)

def main():
    data,p12,out=paths()
    actual={name:hashlib.sha256((data/name).read_bytes()).hexdigest() for name in SHA256}
    assert actual==SHA256, 'Input hash mismatch: stop; do not compare against archived Prompt 12'
    manifest=json.loads((p12/'experiment_manifest.json').read_text())
    assert manifest['source_sha256']==actual
    assert manifest['sample_count_test']==606 and manifest['primary_coverage']==.8
    assert manifest['bootstrap_reps']==2000 and manifest['random_reps']==1000
    assert manifest['bootstrap_seed']==2026 and manifest['random_seed']==42

    dev=raw_map(data,'dev'); test=raw_map(data,'test')
    assert len(dev)==316 and len(test)==606
    assert int(dev.correct.sum())==215 and int(test.correct.sum())==338
    assert int(dev.provisional_nei.sum())==24 and int(test.provisional_nei.sum())==50
    # IDs by themselves are not globally unique; use a combination of split, claim, cited doc.
    assert not pd.concat([dev,test]).duplicated(['split','claim_id','doc_id']).any()
    assert not set(dev.doc_id)&set(test.doc_id), 'Cross-split cited-document overlap; investigate before proceeding'

    ranked=pd.read_csv(p12/'per_case_selection.csv', dtype={'doc_id':str})
    assert len(ranked)==606 and not ranked.duplicated(['split','claim_id','doc_id']).any()
    keys=['split','claim_id','doc_id','source_row']
    for frame in [test,ranked]:
        for k in ['split','doc_id']: frame[k]=frame[k].astype(str)
    merged=ranked.merge(test[keys+['gold','pred','correct','confidence','provisional_nei']],on=keys,
                        validate='one_to_one',how='outer',indicator=True,suffixes=('_saved','_raw'))
    assert merged['_merge'].eq('both').all(), 'Saved selection misaligned with raw prediction IDs'
    assert (merged['gold_saved']==merged['gold_raw']).all()
    assert (merged['pred_saved']==merged['pred_raw']).all()
    assert np.array_equal(merged.correct_saved.astype(int),merged.correct_raw.astype(int))
    assert np.allclose(merged.confidence_saved,merged.confidence_raw,atol=1e-6)
    assert (merged.provisional_nei_saved.astype(str)==merged.provisional_nei_raw.astype(str)).all()
    assert ranked['confidence_rank'].tolist()==list(range(1,607))
    assert (np.diff(ranked.confidence.to_numpy())<=1e-10).all()
    assert not ranked[['gold','pred','confidence','correct']].isna().any().any()

    policy=pd.read_csv(p12/'policy_summary.csv')
    curve=pd.read_csv(p12/'risk_coverage.csv')
    boots=pd.read_csv(p12/'bootstrap_effects.csv')
    draws=pd.read_csv(p12/'random_retention_draws.csv')
    alt=pd.read_csv(p12/'alternative_scores_exploratory.csv')
    explicit=pd.read_csv(p12/'explicit_label_sensitivity.csv')
    assert len(policy)==4 and len(curve)==606 and len(boots)==2000 and len(draws)==1000
    assert not pd.concat([policy,curve,boots,draws],ignore_index=True).empty
    for name, df in [('policy',policy),('curve',curve),('bootstrap',boots),('random',draws),('alternative',alt),('explicit',explicit)]:
        assert not df.isna().any().any(), f'{name}: missing data'
    expected=1-test.correct.mean()
    assert np.isclose(expected,manifest['baseline_risk'],atol=1e-10)
    assert np.isclose(curve.selective_risk.iloc[-1],expected,atol=1e-10)
    assert np.isclose(np.mean(curve.selective_risk), manifest['aurc'],atol=1e-10)
    assert np.isclose(draws.risk.mean(),manifest['random_mc_risk_mean'],atol=1e-10)
    ci=np.percentile(boots.delta,[2.5,97.5]); assert np.allclose(ci,manifest['bootstrap_ci_95'],atol=1e-10)
    assert (policy['k'].astype(int).to_list()==[424,485,545,606])
    assert np.isclose(policy.loc[policy.k==485,'risk'].iloc[0],manifest['confidence_risk'],atol=1e-10)
    assert np.isclose(policy.loc[policy.k==485,'gain_over_random_pp'].iloc[0],100*manifest['delta'],atol=1e-10)
    assert ((policy.coverage_realized-policy.k/606).abs()<1e-12).all()

    # Named sample collections: original baseline vs accepted primary subset.
    retained=ranked[ranked['accepted_80pct'].astype(str).str.lower().isin(['true','1'])].copy()
    assert len(retained)==485 and int((1-retained.correct).sum())==195
    full_f1=float(f1_score(test.gold,test.pred,labels=LABELS,average='macro',zero_division=0))
    accepted_f1=float(f1_score(retained.gold,retained.pred,labels=LABELS,average='macro',zero_division=0))
    assert np.isclose(accepted_f1,policy.loc[policy.k==485,'macro_f1'].iloc[0])

    # Formal tables derived only from archived files.
    table1=policy[['coverage_target','k','coverage_realized','risk','random_expected_risk','gain_over_random_pp','macro_f1']].copy()
    table1.insert(0,'policy','top_max_probability')
    table1['rejected']=606-table1['k']
    table1['errors_accepted']=((table1['risk']*table1['k']).round()).astype(int)
    table1.to_csv(out/'results.csv',index=False)

    p_full,r_full,f_full,s_full=precision_recall_fscore_support(test.gold,test.pred,labels=LABELS,zero_division=0)
    p_sel,r_sel,f_sel,s_sel=precision_recall_fscore_support(retained.gold,retained.pred,labels=LABELS,zero_division=0)
    class_table=pd.DataFrame({'label':LABELS,'support_full':s_full,'f1_full':f_full,'precision_full':p_full,'recall_full':r_full,
                              'support_accepted80':s_sel,'f1_accepted80':f_sel,'precision_accepted80':p_sel,'recall_accepted80':r_sel})
    class_table['f1_change']=class_table['f1_accepted80']-class_table['f1_full']
    class_table.to_csv(out/'classwise_comparison.csv',index=False)
    ci_stats={'baseline_error_rate':float(expected),'selected_error_rate':float(manifest['confidence_risk']),
             'improvement_pp':float(100*manifest['delta']),'bootstrap_ci_pp_low':float(ci[0]*100),
             'bootstrap_ci_pp_high':float(ci[1]*100),'bootstrap_repetitions':2000,
             'random_draws':1000,'monte_carlo_mean_error':float(draws.risk.mean()),'macro_f1_full':full_f1,
             'macro_f1_accepted80':accepted_f1,'n_test':606,'n_accepted80':485,'n_provisional_nei_test':50,
             'aurc':float(curve.selective_risk.mean()),'n_dev':316}
    pd.DataFrame([ci_stats]).to_csv(out/'uncertainty_and_primary.csv',index=False)
    explicit.to_csv(out/'provisional_label_sensitivity.csv',index=False)
    alt.to_csv(out/'alternative_scores_exploratory.csv',index=False)
    # Copy selected cases with traceable IDs and no invented diagnoses.
    retained[retained.correct.eq(0)].sort_values('confidence',ascending=False).head(10).to_csv(out/'high_confidence_errors_for_manual_review.csv',index=False)

    # Figures: PDF vector + PNG raster, no handcrafted graph values.
    f,ax=plt.subplots(figsize=(7.4,4.7))
    ax.plot(curve.coverage*100,curve.selective_risk*100, linewidth=1.6,label='Confidence-ranked acceptance')
    ax.axhline(expected*100,linestyle='--',linewidth=1.3,label='Random acceptance (expected error)')
    ax.plot(policy.coverage_realized*100,policy.risk*100,'o',markersize=5,label='Reported coverage levels')
    ax.set(xlabel='Coverage: predictions accepted (%)',ylabel='Error rate among accepted predictions (%)',title='Selective risk versus coverage')
    ax.set_xlim(0,101); ax.grid(alpha=.23);ax.legend(loc='best',fontsize=9)
    f.tight_layout();draw_and_save(f,out/'figures','risk_coverage')

    f,ax=plt.subplots(figsize=(7.2,4.3))
    idx=np.arange(len(LABELS)); width=.34
    ax.bar(idx-width/2,class_table.f1_full,width,label='All predictions')
    ax.bar(idx+width/2,class_table.f1_accepted80,width,label='Accepted at 80%')
    ax.set_xticks(idx,LABELS);ax.set_ylim(0,1);ax.set(ylabel='F1 score',title='Class-wise F1: full baseline versus selective subset')
    ax.legend();ax.grid(axis='y',alpha=.2)
    f.tight_layout();draw_and_save(f,out/'figures','classwise_f1')

    f,ax=plt.subplots(figsize=(7.2,4.3))
    ax.hist(boots.delta*100,bins=35,alpha=.75)
    ax.axvline(100*manifest['delta'],linewidth=1.8,linestyle='-',label='Observed gain')
    ax.axvline(ci[0]*100,linestyle='--',label='Bootstrap 95% bounds')
    ax.axvline(ci[1]*100,linestyle='--')
    ax.set(xlabel='Random expected error minus confidence error (percentage points)',ylabel='Bootstrap replicates',title='Descriptive bootstrap distribution of gain')
    ax.legend();ax.grid(axis='y',alpha=.2)
    f.tight_layout();draw_and_save(f,out/'figures','bootstrap_gain')

    cm=confusion_matrix(retained.gold,retained.pred,labels=LABELS)
    pd.DataFrame(cm,index=LABELS,columns=LABELS).to_csv(out/'accepted_80pct_confusion_matrix.csv')
    f,ax=plt.subplots(figsize=(6.5,5))
    im=ax.imshow(cm)
    ax.set_xticks(range(3),LABELS,rotation=28,ha='right')
    ax.set_yticks(range(3),LABELS)
    for i in range(3):
        for j in range(3): ax.text(j,i,str(cm[i,j]),ha='center',va='center',color='white' if cm[i,j]>cm.max()/2 else 'black')
    ax.set(xlabel='Predicted label',ylabel='Gold label',title='Accepted predictions at 80% coverage')
    f.colorbar(im,ax=ax,label='Count');f.tight_layout();draw_and_save(f,out/'figures','accepted_confusion')

    summary={
      'sources_verified':{x:actual[x] for x in SHA256},'prompt12_outputs_checked':8,
      'split_overlap_on_cited_doc_ids':False,
      'possible_training_or_model_selection_leakage':'Not ruled out by file checks; development may have been in training and test used for model validation',
      'provisional_label_note':'Empty evidence is mapped to NEI for these analyses; original IRRELEVANT labels are not individually certified',
      'random_comparator':'Expected random matched-k error equals full population error; simulated 1000 draws verify',
      'confidence_policy':'Select top k from the test pool based on max predicted class probability without gold labels',
      'classwise_f1_caution':'Accepted subset class distribution differs from full population',
      'statistical_inference_caution':'95% bootstrap interval is descriptive/pairwise only; exploratory prior analyses and article clustering limit formal inference',
      'no_training_or_model_loading':True,
      'primary':ci_stats,
    }
    (out/'audit_summary.json').write_text(json.dumps(summary,indent=2))
    md=f'''# Prompt 13 - Evaluation using genuine outputs\n\n## Purpose and data\n\nEvaluate the archived Sarol-style citation-integrity predictions, not an independently retrained model. Checked SHA-256 digests against the frozen source files; joined the saved Prompt 12 case table to 606 original test examples by split + claim ID + cited document ID + source row. All pairs matched with no missing probability/label values. The 316 development examples were used only in structural checks; no thresholds were tuned.\n\n## Primary outcomes\n\n- Full test baseline: **{100*expected:.2f}%** error (338 correct, 268 incorrect out of 606).\n- Highest confidence 80% selection: **{100*manifest['confidence_risk']:.2f}%** error (485 retained, 195 incorrect, 121 abstained).\n- Random matched-coverage expected error: **{100*expected:.2f}%** (1,000 archived draws had mean {100*draws.risk.mean():.2f}%).\n- Difference: **{100*manifest['delta']:+.2f} percentage points**, 2,000-pair bootstrap descriptive percentile interval **[{100*ci[0]:+.2f}, {100*ci[1]:+.2f}] pp**.\n- Test macro-F1 full sample **{full_f1:.4f}**; 80%-selected subset **{accepted_f1:.4f}**.\n- Curve AURC **{curve.selective_risk.mean():.5f}** (discrete average across 606 prefix risks).\n- Explicit-label-only (556 examples) difference **{100*explicit.delta.iloc[0]:+.2f} pp**.\n\n## Traceability\n\n- `results.csv`: all archived coverage levels, subset sizes and measured risks.\n- `classwise_comparison.csv`, `accepted_80pct_confusion_matrix.csv`: class counts, precision, recall, F1.\n- `uncertainty_and_primary.csv`: primary estimate, 95% descriptive interval and exact counts.\n- `provisional_label_sensitivity.csv`: 50 provisional NEI test rows excluded.\n- `alternative_scores_exploratory.csv`: secondary scores only; not the primary frozen policy.\n- `high_confidence_errors_for_manual_review.csv`: examples; no claims about root causes without reading source papers.\n- `figures/`: PNG and vector-PDF plots.\n\n## Integrity limits\n\n- Earlier notebooks viewed exploratory abstention results; these are **not prospective preregistered confirmatory findings**.\n- Model-checkpoint training/validation/test provenance is unresolved; no claim of unseen-domain generalization.\n- Pair-level bootstrap ignores citing-article clustering; confidence intervals are descriptive.\n- Selecting top-k across this specific test pool is not a deployment threshold fixed independently on a clean holdout.\n- `NEI` on empty-evidence rows is **provisional**, not individually verified as the original paper's `IRRELEVANT` label.\n- Macro-F1 on the accepted subset is conditional on selection and should not be described as a direct model-quality improvement on identical examples.\n'''
    (out/'prompt13_evaluation_report.md').write_text(md)
    print('PROMPT 13 VALIDATION: PASSED')
    print('Source file hashes: 4/4 matched; 606 test ID/document pairs matched; no missing labels or probabilities')
    print('Coverage 80%: accepted 485 / 606; incorrect accepted 195')
    print('Full baseline error: %.4f; confidence error: %.4f' % (expected, manifest['confidence_risk']))
    print('Improvement: %.3f pp; descriptive bootstrap 95%% CI [%.3f, %.3f] pp' % (100*manifest['delta'],100*ci[0],100*ci[1]))
    print('Figures created: risk_coverage, classwise_f1, bootstrap_gain, accepted_confusion (PNG + PDF)')
    print('Output directory:', out)
    return out

if __name__=='__main__':
    main()
