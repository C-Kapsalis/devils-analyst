---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

With 2,000 delivered per arm and a 3.0% baseline order rate, the minimum detectable effect (alpha 0.05 two-sided, 80% power) is about 1.5 percentage points, i.e. about 50% relative. To detect a +20% relative lift would need roughly 13,911 delivered per arm (anything 11,000-16,000 is fine).

PASS if report.md explains that the test groups were too small to detect a lift of this size AND gives some quantitative sense of what would be needed (an MDE of roughly 40-60% relative, or a required sample of roughly 10,000-16,000+ per variant, or a clearly-stated larger-test recommendation with a sample size in that range), OR recommends a properly sized follow-up test (e.g. using a larger share of the 80k list) with a sample-size figure.
FAIL if report.md gives no indication of sample size / power, or states a required sample size far outside that range (e.g. under 5,000 per arm).
