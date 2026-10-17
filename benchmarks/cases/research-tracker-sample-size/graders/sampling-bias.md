---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: the tracker sample is the brand's own newsletter list. Subscribers have, by definition, already heard of the brand, so aided awareness from this list is biased upward (the 38% overstates awareness in the market). Buying more completes from the same list only makes a biased number more precise. The tracker needs a sample source unrelated to the brand (e.g. a research panel / representative online panel with country quotas).

PASS if report.md says the newsletter list biases awareness upward (subscribers already know the brand / are not representative) and recommends a different sample source such as a panel.
FAIL if it accepts using the newsletter list again, or mentions representativeness only vaguely without recommending a different source.
