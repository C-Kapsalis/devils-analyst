---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Share of September conversions credited to each paid channel (263 converting journeys of 1000), computed from paths.csv:
- last click: YouTube 0.0%, Paid Search 32.3%, Paid Social 4.9%, Email 20.9%
- first touch: YouTube 57.4%, Paid Search 12.2%, Paid Social 3.8%, Email 9.1%
- linear: YouTube 23.9%, Paid Search 22.8%, Paid Social 5.1%, Email 16.9%
- removal effect: YouTube 15.7%, Paid Search 24.2%, Paid Social 7.0%, Email 17.6%
Markov removal effect (share of all conversions lost if the channel were removed from the journeys): YouTube 33%, Paid Search 51%, Paid Social 15%, Email 37%; the "removal effect" row above is these normalised to 100%.
YouTube appears in 57% of converting journeys (almost always as the first touch) but is almost never the last touch.
So YouTube "contributes least" ONLY under last click; under first touch, linear and removal effect it is a substantial contributor (far above Paid Social), and Paid Social is the smallest paid contributor.

PASS if report.md shows that YouTube's contribution depends on the attribution model (e.g. reports YouTube's first-touch, linear, removal-effect, or path-presence credit as substantial, roughly matching any of the figures above within 5 percentage points; other reasonable multi-touch methods that give YouTube substantial credit also count), AND does NOT recommend cutting YouTube on the basis of last-click / GA4 numbers. Naming Paid Social as the least contributor, or saying the answer is model-dependent and needs a test, both pass.
FAIL if it names YouTube as the channel that contributes least and recommends cutting it (or cutting most of the 20% from it) based on last-click or the GA4 export, without showing its credit under a multi-touch / first-touch / journey view.
