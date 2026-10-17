# Sources

Vault root: `~/Documents/tost/`. Abbreviations:
- **F** = `Brain Knowledge/Digital Marketing Brain Knowledge/ai-human-hybrid-marketing-research.md`
- **QN** = `Brain Knowledge/Digital Marketing Brain Knowledge/llm-hybrid-quantitative-research-guide.md`
- **QL** = `Brain Knowledge/Digital Marketing Brain Knowledge/llm-hybrid-qualitative-research-guide.md`
- **HUB** = `theoretical brains/Digital Marketing Brain.md` (section "AI-Human Hybrids for Marketing Research")
- **AB** = `Brain Knowledge/Digital Marketing Brain Knowledge/Online Experiments & AB Testing.md`
- **AD** = `Brain Knowledge/Digital Marketing Brain Knowledge/ad-effectiveness-measurement.md`
- **SP** = `.../Statistical Power.md`; **SS** = `.../Statistical Significance.md`

Linked notes read but not used (no rule drawn): content-marketing-strategy.md
(only general human-AI governance, consistent with F), data-analysis-tools.md,
conversion-optimization.md, social-listening.md.

| Rule in the skill | Source |
|---|---|
| Problem definition and research design are human-led; LLM proposes, human disposes | F "core premise", "adoption framework"; QL Step 1-2 |
| Adoption grid (study design, sample, collection, analysis by exploratory/descriptive/causal) | F "adoption framework" |
| When not to use LLMs: new-to-world, culturally sensitive, ethical edge cases/vulnerable groups, PII, high-stakes on synthetic alone | F "When NOT to use LLMs" |
| Synthetic informs, never replaces evidence for high-stakes decisions; preview/refine only, field humans | F "When NOT"; QN decision tree, pitfall "treating synthetic as ground truth" |
| B2B / hard-to-reach: synthetic as prior and supplement, report agreement and divergence | QN "The B2B advantage" |
| LLM1/LLM2/LLM3 configurations and their recovery profile | QN Phase 3-4, summary table; HUB |
| Response history non-negotiable | QN pitfalls table |
| RAG K = 3-5, curated KB, snippets not transcripts, irrelevant context hurts | QN Step 9, pitfalls |
| Start qual with Hybrid 3; four hybrid configs; decision tree for qual | QL Step 7, decision tree |
| Instrument co-creation split (LLM drafts, human refines and signs off) | QN Steps 1-2; QL Steps 3-4 |
| Double-barrelled items split; LLM answers one half | QN Appendix B note, Appendix D Rule 5 |
| Likert not binary; no rank order; fixed options; items must spread, pre-test ~20 synthetic answers | QN Appendix D Rules 1-4 |
| Balanced, anchored scales; face validity; redundancy | QN Step 2 |
| **Leading/loaded wording check** | **Not stated in the notes.** Added at the caller's request as standard survey practice; tied to QN Step 2 "scales balanced and anchored". Flagged in references/instrument.md |
| A/B survey flow; outcomes right after stimulus, identical across arms; assignment in code | QN Appendix A, Appendix E Step 2 |
| Outcome item families; characteristic batteries double as balance variables | QN Appendix B, C (paraphrased, items not copied) |
| Balance check: t-test numeric, chi-square categorical, p >= .05 | AB (balance checks); AD "Balance Checks" |
| Persona layers (demographics, category qualifiers, attitudinal priors); quant persona factual, no narrative | QN Steps 3-4 |
| Replication: match human sample demographics 1:1; new sample: quotas | QN Step 3 |
| LLM spots missing segments; push for niche/edge cases; human approves | F Pattern 2; QL Step 5, Template C |
| Qual persona uniqueness, quirks, conflicting attitudes | QL Step 6, pitfalls |
| Sensitivity analysis by swapping demographics to detect stereotyping | F "bias and hallucination" |
| Prompt = context + system role + user role; never skip context | F Pattern 1 |
| Rigid answer format with example ("single number only... format: 3") | F Pattern 4; QN Step 5 |
| Validation (format, completeness, plausibility), resend on failure, up to 3 attempts | F "Validation checks"; QN Step 6 |
| Missing after retries logged, never filled | derived from F/QN validation loop (no imputation is described) |
| Temperature 1.0, fixed seed | QN Step 6, pitfalls |
| Natural-language heterogeneity prompts in chat UIs | F "Temperature control through natural language prompting" |
| Keep a prompt library; staged prompting; ask LLM to refine prompt | F "General prompt engineering tips" |
| Backward research: zero-variance item, missing item, dominant concept, sample size from synthetic variance | QN Phase 5 Steps 10-12 |
| Synthetic SD is a floor; divide synthetic variance by the repository variance ratio before n = 16 sigma^2 / delta^2 | **Derived**: QN 7b (synthetic variance consistently lower) + QN Step 11 (use synthetic variance for power) + AB sample size formula n ~ 16 sigma^2 / delta^2; correction uses QN Step 13-15 calibration idea |
| Recovery metrics and thresholds (MAE < 0.5 on 5 pts; variance ratio 0.7-1.3; correlation MAE < 0.2; chi-square p > .05; winner match; Spearman >= .80) | QN "Recovery metrics reference table" |
| Zero-shot pattern: direction right, ~0.5-0.7 more extreme, low variance, correlations near zero; context fixes structure not level | QN 7a-7c, Step 9 key insight |
| Compare full distributions, not only means | QN pitfalls "Ignoring distribution shape" |
| 7-point rescaling of the 0.5 MAE threshold (x 4/6) | **Derived** (linear rescale); notes only state the 5-point threshold |
| Mean correction only from calibrated repository rules | QN Steps 13-15 |
| Historical replication and validation repository | QN Steps 13-14; QL Step 15 |
| Self-moderation: 4 dimensions 0-100, average, threshold 80, probe, cap 2, probe rate < 20% means too lenient | F Pattern 3; QL Step 8d, pitfalls |
| Stay in character; re-run refusals/off-topic | QL Step 8e, pitfalls |
| Qual metrics: readability, information density, LDA coherence, cosine >= .5, UMAP, blind rating with mixed-effects model | F "four evaluation criteria"; QL Steps 9-10 |
| Theme recovery >= 80%; new themes are a feature; cosine of highlights ~.78 | QL Steps 11-12 |
| Consolidation: both = high confidence; human-only = lived experience; LLM-only = expansion insight | QL Step 14 |
| Hybrid pipelines produce best summaries | F criterion 4; QL Step 13; HUB |
| Triangulate; never decide on synthetic alone | QL pitfalls |
| Label every number by source; never "customers say" for synthetic | **Derived** from QL Step 14 "clear attribution" and F "inform, not replace" |
| P-values from synthetic panels are not evidence (n is chosen) | **Derived** from SS (significance is not importance) + QN (synthetic for preview, n set by the analyst in Appendix E). Used in eval 2 and the report rule |
| Significant is not important; consider practical significance | SS; AB step 6-7 |
| Score-and-probe gate (clarity, relevance, depth, insightfulness, < 80 probe, 2 loops) | skill contract, from F Pattern 3 and QL Step 8d |
| Commercial synthetic panels exist; you need to know what to check | F "Commercial implementations" |
