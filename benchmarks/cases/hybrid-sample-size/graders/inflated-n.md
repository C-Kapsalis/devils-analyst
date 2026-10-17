---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: the pilot's purchase-intent SD is 0.61 (variance 0.369), but synthetic variance is compressed. validation_repository.csv shows, for purchase-intent items run with the same configuration (zs-demo-t03), synthetic/human variance ratios of 0.30-0.40 (median 0.35). So the expected human variance is about 0.369 / 0.35 = 1.05 (SD ~1.03), and n per concept = 2 x (1.96 + 0.84)^2 x 1.05 / 0.2^2 = about 414 (range ~363-483 across the repository ratios; the 16 x sigma^2 / delta^2 rule of thumb gives about the same).

Naive answer: plugging the synthetic SD straight in: 16 x 0.36 / 0.04 = 144 per concept (exact formula with the pilot variance: 145); 288 in total. Also wrong: pooling every item and configuration in the repository (median ratio 0.48) gives ~299.

PASS if report.md recommends a per-concept n between 340 and 500 AND explains that synthetic variance understates human variance, using the repository's purchase-intent ratio (~0.35) to inflate it.
FAIL if the recommended n is about 144 per concept (or ~288 total), or 144 with only a vague "add a buffer", or below 340 per concept.
