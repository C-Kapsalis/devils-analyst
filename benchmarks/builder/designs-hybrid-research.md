# hybrid-research: eval case designs

Format follows benchmarks/cases/*/ (prompt.md with frontmatter, scaffold.sh
writing resources/, graders/*.md). Each case also gets a `skill-fired` grader
that accepts `hybrid-research` or `evidence-check`. All brands are fictional
(`.example` domains). Output file: `report.md` in the working directory.

---

## 1. synthetic-variance-compressed

**Prompt.** "We ran our brand-attitude tracker (wave 7) with real panelists
and, in parallel, the same 8 questions with 300 AI personas built from the
wave 7 demographics. Files are in resources/. Does the synthetic panel match
well enough that we can replace the human panel for wave 8 and save the
budget? Write report.md."

**Data.**
- `human_wave7.csv`: 300 rows, `respondent_id, age_band, gender, region, q1..q8` (1-5 Likert). Item SDs 1.05-1.20. Items q1-q4 form one cluster (pairwise r 0.55-0.70), q5-q8 another (r 0.45-0.60), cross-cluster r about 0.2.
- `synthetic_wave7.csv`: 300 rows, same demographics 1:1, `q1..q8`. Means within 0.1-0.4 of human (MAE about 0.25); item SDs 0.55-0.65 (mostly 4s and 5s); pairwise r between -0.08 and 0.12.
- `generation_notes.md`: zero-shot, persona = demographics only, temperature 0.3, no response history.

**Ground truth.** MAE 0.25 passes (< 0.5), but variance ratio = synthetic var / human var is about 0.25-0.35 on every item (fails 0.7-1.3), correlation MAE about 0.45 (fails < 0.2), chi-square on distributions p < .001 on most items. The panel fails; it cannot replace wave 8. Causes in the notes: demographics-only persona, low temperature, no history. Fix: attitudinal priors, temperature 1.0, response history, RAG from past qual; re-validate against a human wave before any substitution, and even then keep humans for decisions that matter.

**Naive answer.** "Means differ by only 0.25 points on average, direction matches on all 8 items, so the synthetic panel tracks well; switch wave 8 to synthetic."

**Graders.**
- *spread-detected* (w3): PASS if report.md compares variance or SD between human and synthetic (any form: variance ratio, SD table) AND says synthetic spread is much lower (roughly a third or a quarter of human variance, or SDs about half). FAIL if it judges the match on means or direction only.
- *correlation-detected* (w2): PASS if it reports that the item correlations in the synthetic data are near zero vs clear positive human correlations (or a correlation MAE above 0.2). FAIL if correlations are not checked or are called similar.
- *decision* (w3): PASS if it recommends not replacing the human wave now, names at least one fix (response history, richer personas, higher temperature, RAG) and a re-validation. FAIL if it endorses switching wave 8 to synthetic, even with caveats.

---

## 2. synthetic-launch-evidence

**Prompt.** "Our insights team tested two concepts for Verdeo, a self-watering smart planter pod that reads soil chemistry and reorders nutrient capsules. They used 1,000 AI respondents (500 per concept). Results are in resources/. Concept B clearly wins. Write the launch recommendation for Thursday's leadership meeting: we want to commit the €2.4M launch budget to B at a €49 price point."

**Data.**
- `concept_test_synthetic.csv`: 1,000 rows, `persona_id, arm, age, income, urbanicity, purchase_intent_7pt, price_acceptable_49 (0/1)`. B top-2-box 68% vs A 51%; mean intent 5.6 vs 4.9 (t about 9, p < 0.001); price acceptable 72% vs 58%.
- `method.md`: GPT-class model, zero-shot, demographic personas, no human benchmark, no validation history for this category.

**Ground truth.** Synthetic results are not market evidence for a launch: the product is new to the world (the model cannot have seen it), the decision is high-stakes (budget and price), and the panel has no human benchmark or calibration. The p-value is not meaningful because the analyst chose n (more personas would shrink it further) and synthetic answers lean extreme and low-variance. Willingness to pay from an LLM panel is uncalibrated. Correct use: treat B as a hypothesis, use the synthetic run to refine the concept wording and survey, and field a human concept test (with a sample size from the synthetic SD treated as a floor) or an in-market test before committing.

**Naive answer.** "B wins with 68% vs 51% top-2-box (p < 0.001) and 72% price acceptance at €49; launch B." Possibly with a one-line "synthetic data has limitations" caveat.

**Graders.**
- *not-evidence* (w3): PASS if report.md states the synthetic results cannot by themselves justify the launch or price decision and names at least one reason from: new-to-world product, high-stakes decision, no human validation. FAIL if it recommends committing the budget to B on these results, with or without caveats.
- *significance-caveat* (w1): PASS if it notes that the p-value or "significance" from synthetic respondents does not carry its usual meaning (n is chosen, not sampled). FAIL if p < 0.001 is presented as proof.
- *next-step* (w2): PASS if it proposes a human concept test or in-market test before commitment, ideally with a sample size. FAIL if no verification step is named.

---

## 3. persona-matrix-missing-segment

**Prompt.** "Brief and persona file attached for FreshCrate (meal kits). Please run a synthetic survey with these 200 personas on our three win-back offers and tell me which one to send in the October campaign. Write report.md."

**Data.**
- `research_brief.md`: objective: win back subscribers who cancelled in the last 6 months; questions: why they left, which of three offers (40% off first box, free dessert for 3 months, pause-instead-of-cancel) would bring them back.
- `personas.csv`: 200 rows, `persona_id, age, gender, region, household_size, income, subscription_status, tenure_months, boxes_per_month`. `subscription_status` = `active` on all 200; tenure 3-30 months.
- `offers.md`: the three offers.

**Ground truth.** The matrix contains no lapsed or cancelled subscribers, the exact population the brief targets. Any synthetic answer from active subscribers about why they left or what would bring them back answers a different question. Correct: stop before generating, rebuild the matrix with cancelled-subscriber personas (cancellation reasons, tenure at cancel, time since cancel) and confirm with the human; since this picks a live offer, verify with a randomised email holdout across the offers, not the synthetic ranking.

**Naive answer.** Generates answers (or simulates them) and recommends one offer, e.g. "40% off wins with 61% likely to resubscribe."

**Graders.**
- *segment-gap* (w3): PASS if report.md notes that all personas are active subscribers and the brief targets cancelled/lapsed ones, and treats this as invalidating the run. FAIL if it does not mention the mismatch, or mentions it but still ranks the offers as the answer.
- *fix* (w2): PASS if it proposes rebuilding the persona matrix with lapsed-subscriber variables and/or asks the user to confirm the population. FAIL otherwise.
- *verify* (w1): PASS if it proposes a real test (email A/B or holdout across offers) before choosing. FAIL if a synthetic ranking is the final basis.

---

## 4. survey-double-barrelled-leading

**Prompt.** "Here is our customer survey draft for the Lumo app and a 40-respondent synthetic pilot we ran on it. The pilot looks clean, no weird answers. Is the survey ready to field to 800 customers next week? Write report.md with anything we should change."

**Data.**
- `survey_draft.md`: 12 items. Embedded problems: Q3 "How much did you enjoy our new, faster checkout?" (1-5); Q5 "The app is fast and easy to use." (1-5 agree); Q7 "Do you follow the latest tech trends? Yes/No"; Q9 "Rank these five features from most to least important"; the rest are clean single-attribute 5-point items.
- `synthetic_pilot.csv`: 40 rows. Q3 is 5 for 38 of 40; Q5 mean 4.3; Q7 92% yes; Q9 rankings parse; clean items show SD 0.7-0.9.

**Ground truth.** Not ready. Q3 is leading (presumes enjoyment and praises the change) and its near-zero variance is the symptom; rewrite neutrally ("How would you rate the checkout?"). Q5 is double-barrelled (fast vs easy); split it. Q7 binary on an attitude; use a 7-point agreement item. Q9 rank order; replace with ratings per feature. Also: the pilot's low SD on clean items is expected compression, so the pilot cannot certify the survey on its own; a small human soft launch is advisable.

**Naive answer.** "Pilot answers are consistent and parse well; the survey is ready", or only "drop Q3 because it has no variance".

**Graders.**
- *double-barrel* (w2): PASS if Q5 is flagged as asking two things and split. FAIL otherwise.
- *leading* (w2): PASS if Q3 is flagged as leading/loaded/presumptive and rewritten neutrally (dropping it without naming the wording problem is FAIL).
- *format-items* (w1): PASS if at least one of Q7 (binary) or Q9 (ranking) is flagged with the fix. FAIL if neither.
- *verdict* (w2): PASS if the report says the survey is not ready as is. FAIL if it says ready to field.

---

## 5. backward-sample-size

**Prompt.** "We piloted our two packaging concepts with 200 synthetic respondents (resources/). Purchase intent SD came out around 0.6. How many real respondents per concept do we need to detect a 0.2-point difference? Put the number in report.md."

**Data.**
- `synthetic_pilot.csv`: 200 rows, `arm, purchase_intent_5pt`; SD 0.60 in both arms.
- `validation_repository.csv`: 9 past studies in the same category, `study, config, item, var_human, var_synthetic`; variance ratio (synthetic / human) for purchase-intent items 0.30-0.40, median 0.35, same configuration as the pilot.

**Ground truth.** n per arm = 16 x sigma^2 / delta^2. Naive with synthetic variance: 16 x 0.36 / 0.04 = 144. Synthetic variance is compressed; the repository says var_synthetic is about 0.35 of human, so sigma^2_human is about 0.36 / 0.35 = 1.03 and n = 16 x 1.03 / 0.04 = about 412 per arm (range about 360-480 using ratios 0.40-0.30).

**Naive answer.** 144 per arm (or 288 total).

**Graders.**
- *inflated-n* (w3): PASS if the recommended n per arm is between 350 and 500 and the report explains synthetic variance understates human variance (using the repository ratio). FAIL if the answer is about 144 per arm, or 144 with only a vague "add a buffer".
- *method* (w1): PASS if the formula or a standard power calculation is shown. FAIL otherwise.

---

## 6. synthetic-theme-pooling

**Prompt.** "We did 8 customer interviews and topped them up with 20 AI interviews to save time. Theme codes are in resources/. Write the insights summary for the brand team: what are customers telling us, ranked by how many interviews mention each theme."

**Data.**
- `themes_human.csv`: 8 interviews x theme flags. Themes: delivery delays (6/8), price vs supermarket (5/8), packaging waste (4/8), recipe repetition (3/8).
- `themes_synthetic.csv`: 20 interviews x flags. "Desire for app-based meal planning AI" (17/20), price (14/20), recipe repetition (12/20), packaging waste (6/20); delivery delays 2/20.
- `method.md`: synthetic interviews used Hybrid 4, no human moderator.

**Ground truth.** Sources must be analysed separately, then merged by status, not pooled. High-confidence (in both): price, packaging waste, recipe repetition. Human-only: delivery delays (6/8 real customers, the strongest real signal, nearly absent in synthetic). Synthetic-only: AI meal planning (17/20), which is a hypothesis to test, not something customers said. Pooled counts would rank AI meal planning first (17/28) and push delivery delays down (8/28): wrong.

**Naive answer.** A pooled ranking over 28 interviews with "AI meal planning" as the top customer theme and delivery delays mid-table.

**Graders.**
- *no-pooling* (w3): PASS if the report keeps human and synthetic counts separate (or tags source per theme) and does not present AI meal planning as something customers said. FAIL if the top-ranked "customer" theme is AI meal planning or counts are pooled without source labels.
- *delivery-signal* (w2): PASS if delivery delays are reported as a leading theme among the real customers. FAIL if they are ranked low or omitted.
- *hypothesis-label* (w1): PASS if the synthetic-only theme is labelled a hypothesis or proposed for validation with humans. FAIL otherwise.
