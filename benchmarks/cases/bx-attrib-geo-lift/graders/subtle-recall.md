---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 4 planted problems. Answer key (computed from the files):

1. Raw comparison ignores the pre-period gap. Test regions were already 12.3% above control in the pre-period (Meta live everywhere). The agency's +18.4% compares the groups during the test only. Difference-in-differences (test-period ratio over pre-period ratio, excluding the control holiday days) gives a lift of about 3.2%; incremental revenue about €9,737, iROAS about 1.06x vs break-even 2.86x (agency: 5.41x). Found if report.md uses the pre-period as a baseline (DiD or equivalent) and gets a lift within 2 points of 3.2% or an iROAS below break-even.
2. Control-region school holiday. The regional calendar shows a school autumn break in control regions 14-18 Sep; control revenue those days averaged €8,319 vs €9,862 on other test days. Found if report.md flags the holiday as depressing control (inflating the measured lift) and excludes/adjusts for it.
3. Control not fully dark. Control regions still had Meta spend during the test (€1,008, about 12% of their pre-period daily level). Found if report.md notes the leaked spend (contamination; it slightly understates the effect: adjusted lift about 3.6%, iROAS about 1.20x, still below break-even).
4. No uncertainty. The readout gives a point estimate only. From daily test/control log-ratios, the 90% interval for the lift is about 0.8% to 5.5%, i.e. iROAS about 0.28x to 1.80x, entirely below break-even. Found if report.md gives a confidence interval / significance assessment (any reasonable method) or states that the upper end stays below break-even.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 4 with the specific evidence.
FAIL if fewer than 3.
