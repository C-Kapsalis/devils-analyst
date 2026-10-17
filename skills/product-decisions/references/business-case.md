# Business case: market size, NPV, break-even, recommendation

The business case is the last gate before major spending (engineering,
manufacturing, launch). The product lead recommends go, conditional go or
no-go; leadership decides go, conditional go, hold, kill or recycle.

## Market analysis

### Sizing

| Level | Definition | Estimate from |
|---|---|---|
| TAM | All potential customers x average annual revenue per customer | Census, industry reports |
| SAM | TAM after geography and niche filters | Constraints applied to TAM |
| SOM | Share of SAM realistically captured | Competition, budget, adoption; industry entry benchmarks (often 1-2% in year 1, range 1-10%) or concept-test P |

- Top-down: industry total x segment share. Good where data exists; inflates
  when categories are broad. Bottom-up: count customers x revenue each; more
  defensible because each number has a source. Do both. Within 2x:
  converging. Around 10x: re-examine assumptions.
- Concept-test forecasts are units and specific to your concept; SOM is
  revenue from benchmarks. If the two disagree a lot, find out why.
- Common errors: TAM quoted as a target, unsourced numbers, broad category
  data for a niche product, unrealistic adoption, math not shown. Data given
  that is irrelevant to the size (distractors) should be left out explicitly.
- Early-stage firms: 1-5% of SAM in years 1-3 is realistic; leaders reach
  20-40% over years. More than 5% early signals an unrealistic plan.

### Adoption (who buys first, how fast)

Adopter groups: innovators 2.5%, early adopters 13.5%, early majority 34%,
late majority 34%, laggards 16%. Launch targets the first two; the gap to the
early majority (the chasm) is crossed by winning one scalable niche with a
repeatable mainstream use case, then expanding. Rate the five product factors
H/M/L through the target segment's eyes: relative advantage, compatibility,
complexity (higher is slower), trialability, observability. Each low factor
gets a fix (quantify the gain, simplify or onboard, free trial or guarantee,
visible packaging or referral). A revenue ramp with no adoption story behind
it is the most common reason cases break.

### Industry attractiveness

Five forces, each H/M/L with a reason: rivalry, substitutes, new entrants
(horizontal); supplier power, buyer power (vertical). Highly competitive
markets need a defensible niche.

## Financial analysis

| Concept | Formula or rule |
|---|---|
| Present value | `PV = C / (1 + r)^t` |
| NPV | `sum over t of CF_t / (1 + r)^t`, outflows negative; t = 0 undiscounted |
| Quarterly rate | `(1 + r_annual)^(1/4) - 1` |
| Discount rate | Opportunity cost of capital; firms commonly use 5-15%; larger firms lower (cheaper capital, less risk on distant flows) |
| Sunk cost | Spent and unrecoverable: excluded. The only question is whether the next dollar creates value |
| Contribution margin | price - variable cost per unit (use the price the firm receives, after channel margins) |
| Break-even quantity | fixed costs / contribution margin |

Cash-flow table: one column per period (quarters for launches), rows for each
revenue and cost line (development, tooling, ramp-up, launch marketing,
ongoing marketing, unit production cost, overhead), period cash flow, period
PV, NPV. Early periods are all outflows.

NPV reading: well above 0 strong go; above 0 go; near 0 marginal or
conditional; below 0 no-go. NPV also depends on the rate: show the result at
the low and high end of the plausible rate.

Break-even checks:
1. Feasibility: BEQ as % of SAM (same units); within SOM? If not: raise price
   (only with elasticity evidence), cut cost, or widen SAM through more
   channels.
2. Timeline: time to BEQ at the adoption ramp vs funding runway.
3. Sensitivity: price -10%, costs +20%.

## Recommendation

| Outcome | When |
|---|---|
| Go | Demand validated, NPV > 0, BEQ achievable within SOM, risks mitigated |
| Conditional go | Promising, but a metric is borderline or a key assumption untested: phased pilot |
| No-go or pivot | Market too small, unit economics fail, risks unmanageable |

Five parts: the decision; the evidence (intent, WTP, SOM, NPV, BEQ); the risks
(market, operational, financial, technical, legal) on a likelihood x impact
grid (high-high is top priority, low-likelihood high-impact gets a
contingency, high-likelihood low-impact is monitored, low-low accepted); the
success criteria; next steps with dates.

Success criteria (they double as kill conditions): specific metric and
threshold, a deadline, tied to viability, spread across volume, satisfaction
(NPS above 40 typical for early products, above 50 strong), retention (repeat
rate) and money (LTV:CAC at least 3:1, break-even by a date). Agreed before
launch so that stopping is not an emotional decision.

## After the gate

Confidence builds through prototype (concept risk; not usable by customers),
MVP (demand risk), alpha (internal; technical risk), beta (external real use;
usability and fit risk), launch (scale risk). Post-launch, track adoption,
retention and revenue against the case's own projections.
