---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

Over the whole test, new users show essentially no lift (-3.0%, p=0.55); the early lift is concentrated in returning users (week 1 +32.0%, week 2 +14.8%, week 3 +5.0%, week 4 +3.2%).

PASS if report.md splits the result by user_type and notes that new users show no meaningful lift (or that the lift came from returning users and faded).
FAIL if report.md does not break the result down by user_type at all, or claims new users improved meaningfully.
