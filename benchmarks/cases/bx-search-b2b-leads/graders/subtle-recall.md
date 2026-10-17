---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

The exports contain 4 planted problems. Answer key (computed from the files):

1. The CPA improvement is an artefact. pricing_page_view was added as a primary Google conversion on 2026-08-01, so August and September conversions include page views. Platform CPA fell 29% (€79 to €56), but cost per CRM demo request rose 12% (€89 to €99). Found if report.md says the pricing_page_view goal change inflates conversions / invalidates the CPA trend.
2. Microsoft conversions double-count. The Microsoft demo goal counts "every"; Microsoft reported 285 conversions vs 125 demo requests in the CRM from Bing (2.28x). Microsoft's platform CPA €49 becomes €112 per CRM lead (Google €92). Found if report.md flags the count=every setting or that Microsoft conversions exceed CRM leads.
3. Free CRM is cheap leads, expensive pipeline. Generic - Free CRM has the lowest cost per lead among generic campaigns (€43) but an SQL rate of 3.3%, giving the highest cost per SQL (€1,293) vs €677 for Generic - Sales Pipeline Tool. Found if report.md judges Free CRM on SQLs/cost per SQL and says it is the worst or should not be scaled.
4. Germany is hidden in the blend. Blended cost per SQL is €465 (within the €900 ceiling), but DE generic campaigns run at €2,313 per SQL while UK is €400. Found if report.md splits by market and says DE (generic) is above the ceiling.

List which ones were found in your reasoning.
PASS if report.md identifies at least 3 of the 4 with the specific evidence.
FAIL if fewer than 3.
