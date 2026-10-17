# Opportunity screening, needs, prototype tests and synthetic respondents

## Screening opportunities

An opportunity is a hypothesis about how value could be created. Process:
charter (goal, target user, context, stakeholders, kept broad) -> generate
many -> screen out the unlikely -> develop 3-5 -> select the exceptional few
-> reflect.

- Early screen uses one criterion only: is this worth a few days or weeks
  more investigation? Collect independent judgments (survey or workshop with
  multi-voting): at least 6, preferably more than 10.
- Develop the survivors by listing their biggest uncertainties, the task that
  would resolve each, and its cost; do the tasks that remove most
  uncertainty per unit of cost first.
- Final selection: Real (need, ability and willingness to buy, viable concept,
  acceptable risk to the customer), Win (sustainable advantage, resources,
  management commitment, market knowledge at least equal to rivals), Worth it
  (return at acceptable risk, cash and people, strategic fit). Name which of
  the three fails rather than giving an overall opinion.
- Desirable (people), viable (business), feasible (technical): all three are
  needed; two out of three still fails.
- Risk horizon: H1 known solution and known market (improvement, low risk);
  H2 new on one axis (adjacent technology or adjacent market, moderate);
  H3 new on both (high risk, breakthrough potential). Judge H3 ideas by H1
  payback rules and every exploration dies; keep a deliberate mix.
- Quality of the best opportunity rises with volume, mean quality, variance
  of ideas, and accuracy of evaluation. Customers are the single largest
  external source, then competitor products, then the sales force.

## Customer needs

- Explicit needs: table stakes. Unfulfilled needs: differentiation. Latent
  needs: breakthrough; found through lead users (heavy users who build
  workarounds), observation in the use environment, hacks and unintended
  uses, complaints about adjacent problems.
- Interviews per segment: at least 10, stop when two more rounds add no new
  needs; around 50 is usually too many. Cover purchasers and users when they
  differ.
- Need statements: what, not how; specific; positive; in product-attribute
  terms; no must/should. Organise into primary and secondary needs; weight
  importance by customer survey (1-5 importance plus a flag for
  unexpected or exciting features).

## Prototype and pilot tests as evidence

- Usability: about 5 users from the target audience uncover most usability
  issues (roughly 85%); 2-3 tasks, think-aloud, no help; issues seen in 3 or
  more of 5 users are real; rank critical (blocks the task), major (slows),
  minor (annoys).
- Service pilots: 1-2 scenarios, 5-10 target users, success criteria set in
  advance (for example share completing booking unaided), realistic setting,
  observer notes.
- Do not jump to high fidelity: each fidelity step filters bad ideas
  cheaply; a polished prototype can solve the wrong problem.
- Digital funnels designed around a pain point: map the core path in 5-8
  steps and mark drop-off points; the biggest drop is the first test target.

## Synthetic (LLM) respondents

Use for drafting the instrument, previewing results, spotting zero-variance
or redundant questions, and a first variance estimate for sample sizing.
Do not use as final evidence for launch or pricing.

Known behaviour versus human panels, from published hybrid-research work:

| Property | Zero-shot persona prompts | With response history | With history + retrieved prior research |
|---|---|---|---|
| Direction of means | Usually right | Same | Same |
| Level of means | More extreme, about 0.5-0.7 points on a 5-point scale | Not fixed | Not fixed |
| Variance | Too low | Improved | Improved |
| Correlations between items | Near zero | Positive, directional | Closest to human |

Recovery targets when comparing to a human benchmark: mean absolute error
below 0.5 on a 5-point scale, variance ratio 0.7-1.3, correlation error below
0.2, same winning concept, rank correlation at least 0.8. Avoid for
new-to-the-world products, culturally specific groups, PII, and vulnerable
populations. The research question and the design stay human.
