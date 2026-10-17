# Measuring brand equity per customer

Contents: [Flaw of averages](#flaw) · [Method](#method) · [Three equities](#three) · [Customer equity](#ce) · [Attitude vs behaviour](#gap)

<a id="flaw"></a>
## 1. The flaw of averages

A brand-equity index averaged across all respondents ("our brand score is
7.1") describes nobody. A customer who rates awareness 9 and ethics 2 and
one who rates them 2 and 9 both average to 5.5, and any investment chosen
from 5.5 fits neither. The same flaw makes a stable average hide a falling
high-value segment when the respondent mix shifts.

Rule: compute per customer (or per segment), decide on that, and roll up
only at the end for portfolio reporting.

<a id="method"></a>
## 2. Method for a tracker or brand survey

1. Keep respondent-level rows: wave, segment, customer status, scores.
2. Per wave and segment: n, mean score, share of top scores.
3. Composition: compare each segment's share of respondents across waves.
   If the mix moved, recompute the total at a fixed mix (first wave's
   shares) so mix and score changes separate.
4. Value weighting: join segment CLV or revenue from the CRM; compute the
   value-weighted score change `sum(segment score change x segment share of
   CLV)`. This is the number for decisions.
5. Test each segment change for sampling error before calling it.
6. Verdict on the segment that carries the value, then the total.

Typical finding: the total is flat because a growing low-value segment
rates the brand higher while the core, high-CLV segment rates it lower.
That is a decline in the customers who pay for the brand.

<a id="three"></a>
## 3. The three equities

Brand choice is driven by three equities, measured per customer:

| Equity | What it is | Drivers |
|---|---|---|
| Value equity | objective judgement of what you get for what you pay | quality, price, convenience |
| Brand equity | subjective worth above objective value | awareness, attitude, brand ethics, corporate citizenship |
| Relationship equity | reluctance to switch | switching costs, loyalty programmes, community, personal relationships |

Their weights differ by category: low-involvement and luxury goods are
brand-led; airlines, rental cars and subscriptions are relationship-led;
B2B commodities and utilities are value-led. Step 1 is to establish which
leg drives choice here (key-driver analysis: regress choice or CLV on the
driver ratings per customer). Investing in the wrong leg (advertising in a
relationship-led business) wastes budget.

Brand-equity sub-drivers chosen for analysis must be tied to a spending
line, perceivable by customers, and ratable by them.

<a id="ce"></a>
## 4. Customer equity above brand equity

Customer equity = sum of CLV across all customers and all of the firm's
brands. Brand equity is one input into it. The two can diverge: brand
scores can rise while the customer base shrinks or shifts to lower value.
When they disagree, the customer number wins for decisions.

Consequences:
- A customer moving from one of our brands to another is not a loss.
- Judge retire, milk or extend decisions by the change in customer equity,
  not by the brand's own scores.
- Model a brand investment before spending: "raising perceived quality by
  X in segment Y lifts customer equity by Z; does Z exceed the cost?" and
  validate it afterwards.

<a id="gap"></a>
## 5. Attitude vs behaviour

Attitude models (multi-attribute scores, intention, social norms,
perceived control) explain why people feel as they do, but they predict
purchase poorly: habit, price, availability and competitors intervene.
Rules:
- Pair every attitude metric with a behavioural one for the same people or
  period (repeat rate, share of wallet, baseline sales).
- If they disagree, trust behaviour and report the attitude as unconfirmed.
- Use relative rankings, not absolute points; calibrate across people.
- High intention with low purchase can mean low perceived control (price,
  availability, effort): check the barriers before the message.
