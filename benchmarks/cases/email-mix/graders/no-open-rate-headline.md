---
type: llm
weight: 1
focus: { source: file, path: report.md }
---

PASS if report.md does not use open rate as a primary success metric, or if it uses open rate it caveats that opens are unreliable (privacy protection, machine opens, image loading).
FAIL if open rate is presented as a key result without any caveat.
