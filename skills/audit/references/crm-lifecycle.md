# CRM lifecycle, retention and CLV

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| C1 | CLV formula | Built on revenue; no margin, no servicing cost, no discount rate | Overstates value and the acquisition ceiling; overspends on CAC | Margin net of service cost x survival per period, discounted, summed; subtract acquisition cost for net CLV | 1 |
| C2 | Churn applied twice | Survival factor R^t and a discount rate rho = (1 + i - R) / R in the same term | Understates CLV and the allowable CAC | Use V_t R^t / (1 + i)^t, or V_t / (1 + rho)^t, not both | 1 |
| C3 | CLV:CAC with a CLV already net of CAC | Ratio computed on net CLV | Acquisition cost counted twice | State the definition; compare gross NPV of future margin with CAC | 1 |
| C4 | Retention input precision | CLV quoted to the cent while retention is rough | At a 10% discount rate the multiple r / (1 + d - r) is 2.67 at r 0.80 and 4.50 at 0.90 | Report CLV as a range over plausible retention | 3 |
| C5 | CLV:CAC by channel | Below 1:1 (losing money per customer) or far above 3:1 (under-investing) | Wrong channels scaled or starved | Reject channels where CAC exceeds CLV minus a buffer | 3 |
| C6 | Churn in a buy-when-you-like business | A simple observed churn rate | Churn is inferred from purchase gaps there | Probabilistic models (purchase count and value) | 4 |
| C7 | Cohort CLV after an acquisition change | Projecting new cohorts from old ones after the channel mix changed | Contaminated forecast | Re-estimate on recent cohorts | 4 |
| C8 | "Active customer" definition | Changed between periods or undocumented | Retention moves with the definition | One documented definition | 1 |
| C9 | Segment ranking | By ticket size or sales; low-survival segments kept on full contact cost | Later-year NPV can turn negative | Rank by discounted profit after service and acquisition cost | 3 |
| C10 | Repeat rate credited to a loyalty program or CRM team | No size benchmark, no control | Bigger brands show higher repeat almost mechanically | Compare with what a brand of that size should show | 5 |
| C11 | Inflow vs outflow | Acquisition spend rising while the net base is flat | The bucket leaks | Fix the leak before turning up the tap | 3 |
| C12 | NPS as the only loyalty measure | No retention or share of wallet | Stated, not revealed, loyalty | Pair with repeat rate and share of wallet | 4 |
| C13 | Lifecycle stages counted by today's stage | Leads counted by current lifecycle stage, not by the date each stage was entered | Funnel conversion by month is wrong | Count by stage-entry date; compare leads created in the same month | 1 |
| C14 | Win-back with no exit | Lapsed contacts mailed forever | Deliverability risk | Exit and delete rule | 2 |
| C15 | Promo judged on one period | Intro offer killed or kept without later retention | Wrong call on customers the promo creates | Judge on cohort CLV | 4 |
| C16 | Folklore figures | "5% retention = 25-95% profit" as the forecast | Plan built on someone else's arithmetic | Use the company's own retention and margin | 4 |
| C17 | CAC ceiling | Set equal to the point estimate of CLV | No buffer for model error | Subtract a safety margin | 3 |

## Decoys

A CLV:CAC around 3:1 for subscription businesses; repeat rate rising with
market share; switching to rivals in proportion to their size.
