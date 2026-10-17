---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth. Send the credit when expected margin saved beats the credit cost:
- Cost of a wasted credit (sent to someone who would have stayed) = $15. Cost of NOT sending to a churner = 0.40 save rate x $180 margin = $72.
- Cut-off probability = c/(1+c) with c = 15/72 -> 0.172; covers 1,080 of 2,000 subscribers.
- Acceptable variants: netting the credit from the margin (cut-off 0.185, 1,023 subscribers); 'offer if p x 0.4 x margin >= $15' (cut-off 0.208, 919); a per-customer rule using each row's annual_margin (984 or 801 subscribers).
Naive wrong answers: churn probability above 0.5 (172 subscribers), top decile (200), or any cut-off chosen without the costs.

PASS if report.md's rule uses a probability cut-off between 0.15 and 0.22 (or an equivalent per-customer expected-value rule as above) AND the number covered is between 720 and 1,188.
FAIL if the cut-off is 0.5, a top-N / top-decile / top-X% choice without cost logic, any cut-off above 0.3, or the count is below 720.
