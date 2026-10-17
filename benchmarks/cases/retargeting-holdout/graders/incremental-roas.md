---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth from the September lift study (Retargeting - Cart & Site 14d):
- Test: 182,400 users, 4,247 conversions (2.328%); control: 45,600 users, 1,011 conversions (2.217%)
- Incremental conversions = test conversions - control rate x test users = 4,247 - 2.217% x 182,400 = 203 (lift 5.0%)
- September spend 19,919; incremental revenue = 203 x AOV 76 = 15,428
- Incremental ROAS (iROAS) = 0.77; cost per incremental purchase = 98
Compare: Meta reports 2,139 purchases and ROAS 8.05 for September (Q3 8.29). Only about 9% of the reported purchases are incremental.

Also acceptable: applying the incrementality factor (incremental / test conversions = 4.8%) to Meta-reported purchases, giving about 102 incremental purchases and iROAS about 0.38.

PASS if report.md computes incremental conversions of about 203 (within 15%) and/or an incremental ROAS of about 0.77 (within 15%), or the incrementality-factor version above (within 15%), and states that true (incremental) return is far below the reported ROAS 8 (iROAS below 1).
FAIL if it treats ROAS 8.0 (or any figure above 2) as the campaign's real return, or never computes an incremental figure from the lift study.
