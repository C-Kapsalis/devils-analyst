---
id: HR-002
area: ga4-utm
overrides: none
check: Sessions referred by the payment domain are a broken cross-domain setup, not a traffic source.
where_to_look: GA4 Reports > Acquisition > Traffic acquisition, session source pay.fernhill-supply.example; and Admin > Data streams > Configure tag settings > Configure your domains.
red_flag: Source pay.fernhill-supply.example above 1% of sessions, or above 0 purchases, in any week.
why_it_costs_money: A purchase that returns from the payment page starts a new session credited to the payment domain, so the campaign that brought the buyer loses the sale and looks worse than it is in channel reports and in bidding signals.
fix: Add the payment domain to the configured domains and to the unwanted referrals list, annotate the date, and break any trend that crosses it. Verify a week later that the source is under 0.1% of sessions.
source: Incident on 2026-03-12 (fictional): paid social CPA reported 30% too high for three weeks after a checkout migration.
owner: Web analytics lead (fictional)
date: 2026-09-15
---

Fictional example for Fernhill Supply Co. It shows a new check the shipped
GA4 checks cannot know about: the name of this team's payment domain and the
threshold they agreed on.
