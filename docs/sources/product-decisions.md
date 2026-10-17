# product-decisions: sources

Paths are relative to `~/Documents/tost/`. PBK = `Brain
Knowledge/Product Brain Knowledge/`, DMK = `Brain Knowledge/Digital Marketing
Brain Knowledge/`, PB = `theoretical brains/Product Brain.md`. Worked examples
in the notes (EmPower scooter, CampusBrew, AB-100, FreshBlend, snack box,
syringe, DAZI) were not copied; eval data is newly generated.

| Rule in the skill | Source |
|---|---|
| Human owns question and decision; LLM proposes, human disposes | DMK/ai-human-hybrid-marketing-research.md (core premise, adoption framework); DMK/llm-hybrid-qualitative-research-guide.md (Step 1) |
| Adversary per move: propose, validate, retry | DMK/ai-human-hybrid-marketing-research.md (validation checks, retry loop) |
| Gate: score clarity, relevance, depth, insightfulness 0-100, threshold 80, probe, cap 2 probes | DMK/ai-human-hybrid-marketing-research.md (Pattern 3); DMK/llm-hybrid-qualitative-research-guide.md (Step 8d, pitfalls table: cap probes at 2) |
| Screener removal, incomplete rows, range and rank checks, n >= 50 | PBK/Analyzing Concept Testing Survey Data.md (Part 2); PBK/Concept Testing.md (Step 2) |
| Verify coding direction; STDEV.S; top-box, top-two-box, ranked-first | PBK/Analyzing Concept Testing Survey Data.md (Part 3) |
| Paired t-test when same respondents rate all concepts; df = n - 1; top vs 2nd and 3rd; alpha 0.10 in course | PBK/Analyzing Concept Testing Survey Data.md (Part 4) |
| Two-sample test for distinct groups only | DMK/Online Experiments & AB Testing.md (t-test section: not for same group on two occasions) |
| 80-90% favourable norm; average definitely ~19%; benchmarks from own history first | PBK/Concept Testing.md (Step 5, interpreting PI) |
| Same format and tone for all concepts; visual adds ~20 points; persuasive inflates | PBK/Concept Testing.md (Step 4) |
| Quadrant analysis (important and poorly rated) | PBK/Concept Testing.md (Step 5) |
| P = C_def F_def + C_prob F_prob; constants 0.4 / 0.2 typical with ranges; Q = N x A x P; A = awareness x availability | PBK/Concept Testing.md (Step 6) |
| PI predicts trial not repeat; frequency for nondurables; inflation sources | PBK/Concept Testing.md (Step 5, Step 6, discussion) |
| Q is units, SOM is revenue | PBK/Building the Business Case.md (Linking to concept testing) |
| Conjoint design rules (3-5 attributes, 2-4 levels, similar counts, no ranges or subjective levels) | PBK/Conjoint Analysis and Feature Optimization.md (Steps 1-2) |
| Importance = range / sum of ranges; exchange rate; WTP = PW / ER; pair nearest target price | PBK/Conjoint Analysis and Feature Optimization.md (Attribute importance, WTP) |
| Individual part-worths, segment WTP, k-means elbow, variants over averages | PBK/Conjoint Analysis and Feature Optimization.md (Segmentation) |
| WTP > cost profitable; feasibility deviation from optimal profile | PBK/Conjoint Analysis and Feature Optimization.md (Why WTP matters, optimal profile) |
| Additivity and sample caveats for conjoint | diagnose playbook product-management/validating-with-data.md (already in repo); PBK/Conjoint Analysis and Feature Optimization.md (key idea: total value = sum of part-worths) |
| Screening +/0/-, equal weights, net score keep/drop rules | PBK/Concept Screening Matrix.md; PBK/Concept Selection.md |
| Scoring 1-5, reference 3.00, customer weights, segment matrices, sensitivity, lower-uncertainty choice | PBK/Concept Scoring Matrix.md; PBK/Sensitivity Analysis.md; PBK/Concept Selection.md |
| Combine and improve; independent criteria; include cost; scale compression | PBK/Concept Selection.md |
| More concepts generated, better outcomes; hybrid individual-group ideation | PBK/Concept Generation.md; PBK/Edison Principle.md; PBK/Brainstorming Rules (Osborn).md |
| TAM/SAM/SOM, top-down vs bottom-up within 2x / 10x, 1-5% of SAM, >5% red flag, sizing mistakes | PBK/Building the Business Case.md (Market sizing) |
| Adopter shares, chasm, five product factors H/M/L with fixes | PBK/Building the Business Case.md (Diffusion of innovation) |
| Five forces | PBK/Building the Business Case.md (Porter) |
| PV, NPV, discount rate 5-15%, quarterly rate, sunk costs excluded, NPV decision bands | PBK/Building the Business Case.md (Financial analysis) |
| BEQ = fixed / CM; % of SAM; feasibility, timeline, sensitivity (price -10%, cost +20%) | PBK/Building the Business Case.md (Break-even) |
| Go / conditional go / no-go table; five-part recommendation; risk grid | PBK/Building the Business Case.md (Recommendation, Risk assessment) |
| Success criteria as kill conditions; NPS > 40 / > 50; LTV:CAC >= 3:1 | PBK/Building the Business Case.md (Defining success criteria) |
| Prototype, MVP, alpha, beta, launch confidence ladder | PBK/Building the Business Case.md; PBK/Milestone Prototypes.md |
| Opportunity as hypothesis; 6-step process; single-criterion screen; >= 6, preferably > 10 judgments; uncertainty-per-cost | PBK/Opportunity Identification.md; PBK/Opportunity.md |
| RWW; desirable / viable / feasible | PBK/RWW Analysis.md; PBK/Three Innovation Challenges.md |
| Horizons H1-H3 | PBK/Horizon Framework.md |
| Quality of best opportunity drivers; source shares | PBK/Opportunity.md |
| Need types, lead users, interviews 10-50 per segment, need statements | PBK/Three Types of Customer Needs.md; PBK/Lead Users.md; PBK/The 5-Step Customer Needs Analysis Process.md; PBK/Need Statements.md |
| 5-user test (~85%), 3 of 5 rule, critical/major/minor; fidelity rule | PBK/Digital Product Prototyping.md; PBK/Prototype Fidelity Spectrum.md |
| Service pilot 5-10 users, preset success criteria | PBK/Service Prototyping.md |
| Core path 5-8 steps, mark drop-offs; biggest drop first | PBK/Digital Product Prototyping.md (Step 2); PBK/Paktor Case Study.md (funnel question) |
| Synthetic respondents: uses, biases (0.5-0.7 extremity, low variance, near-zero correlations), recovery targets, when not to use | DMK/llm-hybrid-quantitative-research-guide.md (Phases 3-6, recovery table); DMK/ai-human-hybrid-marketing-research.md (When NOT to use) |
