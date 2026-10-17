---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth. Of 240 qualified respondents, 17.9% said "definitely" and 27.1% "probably" would buy. Stated intent must be calibrated before it is used as a purchase probability: typical weights are about 0.4 for "definitely" and 0.2 for "probably" (documented ranges roughly 0.1-0.5 and 0-0.25), giving P = 0.126.
Availability-adjusted reach = awareness 0.50 x distribution 0.60 = 0.30.
Forecast = 400,000 households x 0.30 x 0.126 = about 15,100 units (revenue about $1.34M). Any calibration within the documented ranges gives roughly 2,150 to 18,875 units.
Naive wrong forecasts: top-two-box share as the probability, 400,000 x 0.30 x 0.45 = 54,000 (or 180,000 ignoring awareness and distribution); top-box share as the probability, 21,500.

PASS if the base-case forecast in report.md is between 2,000 and 19,000 units AND is built from households x awareness x availability x a purchase probability that discounts the "definitely" and "probably" answers.
FAIL if it uses the raw top-box or top-two-box share as the purchase probability, omits awareness or distribution, or the base forecast is above 19,000 units.
