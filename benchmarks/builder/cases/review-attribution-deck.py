"""Review a quarterly budget deck built on GA4 attribution (Bluefin Pet Supply, Q3 2026).

Planted problems (5): "data-driven attribution" credit for Paid Social while the
purchase key event is far below the DDA volume threshold and every DDA column
equals last click (MUST); YouTube viewers vs non-viewers sold as a 3x ad effect
to justify +40% budget (MUST); a 13-month funnel exploration while data
retention is 2 months; engagement jump credited to content while scroll became
a key event that day; 18% market share of the served (three-region) market.
Decoys (2): display CTR ~0.4% called normal and judged on reach; GA4
purchases a few % under Shopify orders, Shopify used as the revenue total."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv
from datetime import date, timedelta

NAME = "review-attribution-deck"
rng = random.Random(77314)

# ---------- Shopify (truth for revenue) ----------
months = ["2026-07", "2026-08", "2026-09"]
shop = []
for m in months:
    orders = rng.randint(238, 262)
    rev = round(orders * rng.uniform(66, 72), 2)
    shop.append([m, orders, rev])
shop_orders = sum(r[1] for r in shop)
shop_rev = sum(r[2] for r in shop)

# ---------- GA4 channel attribution, Q3: DDA identical to last click (fallback) ----------
CH = {"Organic Search": 0.27, "Paid Search": 0.22, "Paid Social": 0.15, "Email": 0.13,
      "Direct": 0.11, "Paid Video": 0.05, "Display": 0.03, "Organic Social": 0.02, "Referral": 0.02}
ga_purch = int(round(shop_orders * 0.938))
attr = {}
for c, s in CH.items():
    n = int(round(ga_purch * s * rng.uniform(0.95, 1.05)))
    attr[c] = (n, round(n * rng.uniform(64, 73), 2))
attr_rows = []
for model in ["Data-driven", "Last click"]:
    for c, (n, v) in attr.items():
        attr_rows.append([c, model, n, v])
ga_rev = sum(v for _, v in attr.values())
ga_purch = sum(n for n, _ in attr.values())

# key events, last 30 days (to 30 Sep)
purch_30d = int(round(shop[2][1] * 0.938))
key_rows = [["purchase", "true", purch_30d, "2024-03-02"],
            ["generate_lead", "false", 412, ""],
            ["add_to_cart", "false", 2210, ""],
            ["scroll", "true", 41870, "2026-08-18"],
            ["newsletter_signup", "false", 655, ""]]
assert purch_30d < 300

settings_rows = [["property_name", "Bluefin Pet Supply - Web"], ["reporting_attribution_model", "Data-driven"],
                 ["key_event_lookback_window", "90 days"], ["data_retention_event_data", "2 months"],
                 ["data_retention_user_data", "2 months"], ["enhanced_measurement", "on"],
                 ["reporting_currency", "EUR"], ["time_zone", "Europe/Dublin"]]

# ---------- spend ----------
spend = {"Paid Search": 6200.0, "Paid Social": 6400.0, "Paid Video": 3100.0, "Display": 2300.0}
spend = {k: round(v * rng.uniform(0.96, 1.04), 2) for k, v in spend.items()}
imps = {"Paid Search": 118000, "Paid Social": 690000, "Paid Video": 410000, "Display": 1520000}
ctrs = {"Paid Search": 0.061, "Paid Social": 0.0121, "Paid Video": 0.0044, "Display": 0.0042}
spend_rows = []
clk = {}
for k in spend:
    im = int(imps[k] * rng.uniform(0.97, 1.03))
    clk[k] = int(round(im * ctrs[k] * rng.uniform(0.97, 1.03)))
    imps[k] = im
    spend_rows.append([k, spend[k], im, clk[k]])
disp_ctr = clk["Display"] / imps["Display"]
ps_rev = attr["Paid Social"][1]
ps_roas = ps_rev / spend["Paid Social"]
q2_ps_rev = round(ps_rev / 1.19, 0)
ps_uplift = ps_rev / q2_ps_rev - 1

# ---------- YouTube exposed vs unexposed ----------
v_users = rng.randint(5000, 5400)
v_conv = int(round(v_users * rng.uniform(0.044, 0.048)))
n_users = rng.randint(29000, 30500)
n_conv = int(round(n_users * rng.uniform(0.0145, 0.0158)))
yt_rows = [["saw_youtube_ad", v_users, v_conv], ["did_not_see_youtube_ad", n_users, n_conv]]
v_cr, n_cr = v_conv / v_users, n_conv / n_users
yt_ratio = v_cr / n_cr

# ---------- engagement daily, Aug-Sep ----------
eng_rows = []
d = date(2026, 8, 1)
STEP = date(2026, 8, 18)
while d <= date(2026, 9, 30):
    s = int(rng.gauss(2900, 220)) + (350 if d.weekday() >= 5 else 0)
    rate = (rng.uniform(0.535, 0.555) if d < STEP else rng.uniform(0.725, 0.745))
    eng_rows.append([d.isoformat(), s, int(round(s * rate))])
    d += timedelta(days=1)
pre = [r for r in eng_rows if r[0] < "2026-08-18"]
post = [r for r in eng_rows if r[0] >= "2026-09-01"]
pre_er = sum(r[2] for r in pre) / sum(r[1] for r in pre)
post_er = sum(r[2] for r in post) / sum(r[1] for r in post)
aug_late = [r for r in eng_rows if "2026-08-04" <= r[0] < "2026-08-18"]
aug_late_er = sum(r[2] for r in aug_late) / sum(r[1] for r in aug_late)

# market share
mkt_served, mkt_national = 1.12e6, 21.5e6
annual_rev = shop_rev * 4
share_served = annual_rev / mkt_served
share_nat = annual_rev / mkt_national

# ---------- asserts ----------
assert all(r[2] == attr[r[0]][0] for r in attr_rows)          # DDA == last click
assert 0.15 < share_served < 0.22 and share_nat < 0.012, (share_served, share_nat)
assert yt_ratio > 2.7 and v_conv + n_conv < ga_purch
assert post_er - pre_er > 0.15 and abs(aug_late_er - pre_er) < 0.02
assert 0.0035 < disp_ctr < 0.0048
assert 0.9 < ga_purch / shop_orders < 0.97
assert ps_uplift > 0.15

eur = lambda x: f"€{x:,.0f}"
pc = lambda x, dd=1: f"{100 * x:.{dd}f}%"

deck = f"""# Bluefin Pet Supply: Q3 2026 Performance and Q4 Budget Proposal

Deck for the leadership meeting. Period: 1 July to 30 September 2026.

---

## Slide 1. Q3 in one line

Shopify revenue {eur(shop_rev)} from {shop_orders:,} orders. Paid spend {eur(sum(spend.values()))}.

GA4 recorded {ga_purch:,} purchases, {pc(1 - ga_purch / shop_orders)} fewer than Shopify's {shop_orders:,} orders. A gap of this size is normal (consent banners, ad blockers), so all revenue totals in this deck use Shopify and GA4 is used only to split credit between channels.

---

## Slide 2. Paid Social is under-credited: proposal +25%

Our GA4 property uses **data-driven attribution**, which gives credit to every touch on the path, not only the last click.

| Channel | Q3 purchases (data-driven) | Q3 revenue (data-driven) | Q3 spend | ROAS |
|---|---|---|---|---|
| Paid Search | {attr['Paid Search'][0]} | {eur(attr['Paid Search'][1])} | {eur(spend['Paid Search'])} | {attr['Paid Search'][1] / spend['Paid Search']:.2f}x |
| Paid Social | {attr['Paid Social'][0]} | {eur(ps_rev)} | {eur(spend['Paid Social'])} | {ps_roas:.2f}x |

Under data-driven attribution Paid Social is credited with {eur(ps_rev)}, {pc(ps_uplift, 0)} more than the {eur(q2_ps_rev)} it received under last click in Q2. This is the assist value last click was hiding. **We propose raising Paid Social budget by 25% in Q4.**

---

## Slide 3. YouTube triples conversion: proposal +40%

| Group (Q3) | Users | Purchasers | Conversion rate |
|---|---|---|---|
| Saw a YouTube ad | {v_users:,} | {v_conv} | {pc(v_cr, 2)} |
| Did not see a YouTube ad | {n_users:,} | {n_conv:,} | {pc(n_cr, 2)} |

People who saw our YouTube ads converted at {yt_ratio:.1f} times the rate of people who did not. **YouTube triples conversion. We propose raising the YouTube budget by 40% in Q4.**

---

## Slide 4. Display: judged on reach, not clicks

Display had a CTR of {pc(disp_ctr, 2)} on {imps['Display']:,} impressions. That is in line with normal display click rates, so we judge display on reach and cost per thousand impressions, not on clicks. No change proposed.

---

## Slide 5. The funnel is getting better

Funnel exploration in GA4, September 2025 to September 2026 (13 months): product view to purchase rose from 2.1% to 2.9%. The checkout changes are paying off.

---

## Slide 6. Content refresh lifted engagement

We refreshed the blog and care guides in early August. Engagement rate rose from {pc(pre_er)} (1-17 August) to {pc(post_er)} (September). The new content is keeping visitors on the site.

---

## Slide 7. Our position

**We hold {pc(share_served, 0)} of the pet supply market** (annualised Q3 revenue {eur(annual_rev)}).

Footnote: market size {eur(mkt_served)} = online pet supply sales in our three delivery regions. The national online pet supply market is {eur(mkt_national)}.

---

## Slide 8. Q4 asks

1. Paid Social +25%.
2. YouTube +40%.
3. Keep display and search flat.
"""

files = {
    "resources/q3_budget_deck.md": deck,
    "resources/ga4_property_settings.csv": to_csv(["setting", "value"], settings_rows),
    "resources/ga4_key_events_last_30_days.csv": to_csv(
        ["event_name", "is_key_event", "event_count_last_30_days", "marked_as_key_event_on"], key_rows),
    "resources/ga4_channel_attribution_q3.csv": to_csv(
        ["default_channel_group", "attribution_model", "purchases", "purchase_revenue"], attr_rows),
    "resources/ad_spend_by_channel_q3.csv": to_csv(["channel", "spend", "impressions", "clicks"], spend_rows),
    "resources/youtube_exposure_q3.csv": to_csv(["group", "users", "purchasers"], yt_rows),
    "resources/ga4_engagement_daily.csv": to_csv(["date", "sessions", "engaged_sessions"], eng_rows),
    "resources/shopify_orders_monthly_q3.csv": to_csv(["month", "orders", "total_sales"], shop),
}

prompt = """
I'm presenting our Q3 results and Q4 budget asks to leadership next week. The deck is resources/q3_budget_deck.md and the GA4, ad spend and Shopify exports behind it are in resources/. Can you check it before I present? Tell me if anything is wrong or would get me into trouble, and what to change. Put it in report.md.
"""

g_recall = f"""
The deck under review (q3_budget_deck.md) contains 5 planted problems. Answer key:

1. Data-driven attribution is not really active. Slide 2 credits Paid Social with {eur(ps_rev)} "under data-driven attribution" and asks for +25%. But the purchase key event had only {purch_30d} conversions in the last 30 days (GA4 needs roughly 400 per key event per 30 days for data-driven to work), and in ga4_channel_attribution_q3.csv the Data-driven rows are identical to the Last click rows for every channel. GA4 has fallen back to last click, so there is no hidden assist value; the rise on Q2 is just Q3 vs Q2. Counts as found if report.md says the data-driven model is not in effect / falls back to last click, citing the low purchase volume or the identical columns, and that the +25% rationale does not hold.
2. Exposed vs unexposed sold as an ad effect. Slide 3: viewers converted {pc(v_cr, 2)} vs {pc(n_cr, 2)} for non-viewers, "YouTube triples conversion", +40%. Ads are targeted at likely buyers, so the gap is selection, not effect; only a randomised holdout or lift test can show what YouTube caused. Counts as found if report.md says the comparison does not show causation (selection, targeting, no control group) and the +40% needs a holdout or lift test.
3. Impossible exploration window. Slide 5 shows a 13-month funnel exploration, but ga4_property_settings.csv sets data retention to 2 months, so explorations cannot look back 13 months. Counts as found if report.md points out the 2-month retention contradicts the 13-month exploration (and/or recommends setting retention to 14 months).
4. Engagement jump is a definition change. Slide 6 credits the content refresh for engagement rising from {pc(pre_er)} to {pc(post_er)}. The step happens on 18 August, the day scroll was marked as a key event (ga4_key_events_last_30_days.csv); any session with a key event counts as engaged, so the rate jumped mechanically. Engagement from 4 to 17 August, after the refresh, was {pc(aug_late_er)}, unchanged. Counts as found if report.md links the jump to scroll becoming a key event on 18 August.
5. Market share of a served market. Slide 7's {pc(share_served, 0)} share uses the three delivery regions ({eur(mkt_served)}) as the market; against the national online market ({eur(mkt_national)}) it is {pc(share_nat, 1)}. Counts as found if report.md says the share must be labelled as share of the served/three-region market, or gives the national share (about {pc(share_nat, 1)}).

List which ones were found in your reasoning.
PASS if report.md identifies at least 4 of the 5 problems, each with its substance (a vague mention such as "double-check attribution" does not count).
FAIL if it identifies fewer than 4.
"""

g_rank = f"""
Two of the problems are Must-fix because each drives a Q4 budget ask:
- A. Slide 2: Paid Social +25% justified by "data-driven attribution" while GA4 is effectively on last click (purchase key event {purch_30d} in 30 days; Data-driven rows identical to Last click).
- B. Slide 3: YouTube +40% justified by viewers {pc(v_cr, 2)} vs non-viewers {pc(n_cr, 2)}, an exposed vs unexposed comparison that cannot show causation.
The lesser problems are: the 13-month exploration vs 2-month retention, the engagement jump from scroll becoming a key event, and the served-market share.

PASS if report.md flags both A and B, places each in its highest-severity group (Must fix, critical, or equivalent) or, if it uses no groups, lists both before the lesser problems, AND its verdict does not say the deck can be presented as is.
FAIL if A or B is missing, labelled lower severity (Should fix, Nice to have, minor), or listed after one of the lesser problems, or if the verdict approves the deck unchanged.
"""

g_decoy = f"""
The deck contains two statements that are correct and must not be flagged:
- D1. Slide 4: display CTR {pc(disp_ctr, 2)} called normal, display judged on reach and cost per thousand impressions rather than clicks. A display CTR around 0.3-0.6% is normal and judging display on reach is sound.
- D2. Slide 1: GA4 purchases {ga_purch:,} are {pc(1 - ga_purch / shop_orders)} below Shopify orders {shop_orders:,}, called normal, with Shopify used for revenue totals. A gap of a few percent is expected (consent, blockers) and using the store as the revenue total is correct.

PASS if report.md does not present D1 or D2 as an error, a tracking problem, or something to fix. Mentioning either as checked and fine, or as normal, is a PASS.
FAIL if it says display is underperforming on CTR or should be cut for its CTR, or flags the GA4 vs Shopify gap as a tracking loss to fix, or says Shopify should not be the revenue total.
"""

write_case(NAME, files, prompt, [("planted-recall", 3, g_recall), ("must-fix-first", 2, g_rank), ("decoys-left-alone", 2, g_decoy)])
print(f"{NAME}: purchase 30d {purch_30d}; PS rev {ps_rev:,.0f} (+{ps_uplift:.2f} vs Q2); YT {v_cr:.4f} vs {n_cr:.4f} ({yt_ratio:.1f}x); "
      f"ER {pre_er:.3f}->{post_er:.3f} (4-17 Aug {aug_late_er:.3f}); share {share_served:.3f} vs national {share_nat:.4f}; "
      f"display CTR {disp_ctr:.4f}; GA4/shop {ga_purch}/{shop_orders}")
