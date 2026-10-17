"""Breadth: email numbers dipped, team wants a subject-line testing programme
(Pebblecove Kids, Aug-Sep 2026).

Planted problems (5): the dip is Gmail only (opens and clicks collapse at
Gmail from 9 Sep while other providers are flat), with Gmail domain
reputation falling to Low/Bad, though the ESP shows 99%+ delivered (accepted
is not inboxed) (DECISION); Gmail's user-reported spam rate is above 0.3%
while the ESP complaint rate is about 0.03% (the ESP does not see Gmail
complaints); an 8 Sep reactivation blast to 2.5x normal volume precedes the
fall; one-click unsubscribe is off; hard-bounced addresses keep being mailed
(suppression not applied).
Decoys (2): Apple Mail open rates around 60% (privacy-proxy opens);
unsubscribes 0.15-0.3% per send."""
import sys, random, math, datetime as dt; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-email-gmail"
rng = random.Random(81808)
BREAK = dt.date(2026, 9, 9)
BLAST = dt.date(2026, 9, 8)

sends = []
d = dt.date(2026, 8, 4)
while d <= dt.date(2026, 9, 29):
    sends.append(d)
    d += dt.timedelta(days=3 if d.weekday() == 1 else 4)   # Tue and Fri
assert BLAST in sends

PROV = {"gmail": 0.48, "yahoo": 0.12, "outlook": 0.14, "apple_icloud": 0.18, "other": 0.08}
OPEN = {"gmail": 0.31, "yahoo": 0.27, "outlook": 0.24, "apple_icloud": 0.61, "other": 0.25}
CLK = {"gmail": 0.034, "yahoo": 0.028, "outlook": 0.027, "apple_icloud": 0.030, "other": 0.026}
camp, prov = [], []
names = ["new_in", "back_to_school", "bestsellers", "rainy_day_edit", "bundle_offer", "size_guide", "weekend_sale", "autumn_layers"]
for k, s in enumerate(sends):
    blast = s == BLAST
    sent = int(rng.uniform(60000, 62000)) if blast else int(rng.uniform(23500, 24500))
    bounce_rate = rng.uniform(0.045, 0.055) if blast else rng.uniform(0.004, 0.007)
    bounced = int(sent * bounce_rate)
    delivered = sent - bounced
    tot_o = tot_c = 0
    for p, sh in PROV.items():
        dv = int(delivered * sh)
        o_r, c_r = OPEN[p], CLK[p]
        if blast:
            o_r *= 0.35; c_r *= 0.30
        if p == "gmail" and s >= BREAK:
            o_r *= rng.uniform(0.26, 0.32); c_r *= rng.uniform(0.24, 0.30)
        o = int(dv * o_r * rng.uniform(0.96, 1.04)); c = int(dv * c_r * rng.uniform(0.95, 1.05))
        tot_o += o; tot_c += c
        prov.append([s.isoformat(), p, dv, o, c])
    unsub = int(delivered * rng.uniform(0.0016, 0.0029))
    comp = int(delivered * rng.uniform(0.00025, 0.00035))
    name = "reactivation_we_miss_you" if blast else f"{names[k % len(names)]}_{s.strftime('%m%d')}"
    camp.append([s.isoformat(), name, sent, delivered, bounced, tot_o, tot_c, unsub, comp])

pm = []
d = dt.date(2026, 8, 3)
while d <= dt.date(2026, 9, 30):
    if d < BLAST:
        rep, spam = "High", rng.uniform(0.0006, 0.0011)
    elif d < dt.date(2026, 9, 15):
        rep, spam = "Low", rng.uniform(0.0031, 0.0042)
    else:
        rep, spam = "Bad", rng.uniform(0.0033, 0.0045)
    pm.append([d.isoformat(), rep, "High" if d < BLAST else "Medium", round(spam, 4), 1.0, 1.0, 1.0])
    d += dt.timedelta(days=1)

settings = [["sending_domain", "mail.pebblecove.com"], ["spf", "pass"], ["dkim", "pass (2048-bit)"], ["dmarc", "p=quarantine; rua set"],
            ["list_unsubscribe_header", "mailto only"], ["one_click_unsubscribe_list_unsubscribe_post", "off"],
            ["hard_bounce_handling", "suppress after 3 hard bounces"], ["sunset_policy", "none"]]

# bounce log: addresses with repeated hard bounces
bl = []
for i in range(60):
    n = rng.choice([1, 1, 1, 2, 3, 3, 4])
    bl.append([f"user{i:04d}@{rng.choice(['gmail.com', 'yahoo.com', 'outlook.com', 'aol.com'])}", "hard", n, sends[-1 - rng.randint(0, 3)].isoformat()])
rep_bounces = sum(1 for r in bl if r[2] >= 2)

pre = [r for r in camp if dt.date.fromisoformat(r[0]) < BLAST]
post = [r for r in camp if dt.date.fromisoformat(r[0]) >= BREAK]
def rate(rows, i, j):
    return sum(r[i] for r in rows) / sum(r[j] for r in rows)
or_pre, or_post = rate(pre, 5, 3), rate(post, 5, 3)
cr_pre, cr_post = rate(pre, 6, 3), rate(post, 6, 3)
del_post = rate(post, 3, 2)
def prate(p, after, i):
    rows = [r for r in prov if r[1] == p and (dt.date.fromisoformat(r[0]) >= BREAK) == after and r[0] != BLAST.isoformat()]
    return sum(r[i] for r in rows) / sum(r[2] for r in rows)
g_or_pre, g_or_post = prate("gmail", False, 3), prate("gmail", True, 3)
y_or_pre, y_or_post = prate("yahoo", False, 3), prate("yahoo", True, 3)
o_or_pre, o_or_post = prate("outlook", False, 3), prate("outlook", True, 3)
apple_or = prate("apple_icloud", False, 3)
esp_comp = rate(post, 8, 3)
pm_spam_post = [r[3] for r in pm if r[0] >= BLAST.isoformat()]
normal_vol = sum(r[2] for r in pre) / len(pre)
blast_row = next(r for r in camp if r[0] == BLAST.isoformat())
unsubs = [r[7] / r[3] for r in camp]

assert or_post < or_pre * 0.75 and del_post > 0.99
assert g_or_post < g_or_pre * 0.4 and abs(y_or_post / y_or_pre - 1) < 0.06 and abs(o_or_post / o_or_pre - 1) < 0.06
assert min(pm_spam_post) > 0.003 and esp_comp < 0.0005
assert blast_row[2] > 2.4 * normal_vol
assert rep_bounces >= 15
assert 0.55 < apple_or < 0.67
assert all(0.0015 < u < 0.003 for u in unsubs)

pc = lambda x, d=1: f"{100 * x:.{d}f}%"

plan = f"""# Q4 email plan (CRM team draft)

September was soft: open rate fell from {pc(or_pre)} (August) to {pc(or_post)} and click rate from {pc(cr_pre, 2)} to {pc(cr_post, 2)}. Deliverability is fine ({pc(del_post)} delivered, complaint rate {pc(esp_comp, 2)}).

We think the creative has gone stale. Plan for Q4:
1. A subject-line testing programme: two variants on every send, winner by open rate after 2 hours.
2. New preheader and sender-name tests.
3. Increase frequency from two to three sends a week to recover volume.
"""

notes = """# Notes
- Pebblecove Kids sells children's clothing online. About 24,000 subscribers on the main list.
- Exports: ESP campaign report (Aug-Sep 2026), ESP opens and clicks by mailbox provider, Google Postmaster Tools for our sending domain, ESP deliverability settings, and a sample of the bounce log.
"""

files = {
    "resources/notes.md": notes,
    "resources/crm_q4_plan_draft.md": plan,
    "resources/esp_campaigns_aug_sep.csv": to_csv(["send_date", "campaign", "sent", "delivered", "bounced", "unique_opens", "unique_clicks", "unsubscribes", "spam_complaints"], camp),
    "resources/esp_by_mailbox_provider.csv": to_csv(["send_date", "mailbox_provider", "delivered", "unique_opens", "unique_clicks"], prov),
    "resources/google_postmaster_daily.csv": to_csv(["date", "domain_reputation", "ip_reputation", "user_reported_spam_rate", "spf_success_rate", "dkim_success_rate", "dmarc_success_rate"], pm),
    "resources/esp_deliverability_settings.csv": to_csv(["setting", "value"], settings),
    "resources/bounce_log_sample.csv": to_csv(["email", "bounce_type", "hard_bounce_count", "last_bounce_date"], bl),
}

prompt = """
Our CRM team drafted the Q4 email plan (resources/crm_q4_plan_draft.md) after a soft September. The ESP and Postmaster exports are in resources/. Do you agree with the plan, and what should we do in Q4? Please write it up in report.md.
"""

g_recall = f"""
The exports contain 5 planted problems. Answer key:

1. The dip is Gmail inbox placement. By mailbox provider, Gmail open rate fell from {pc(g_or_pre)} to {pc(g_or_post)} after 9 September, while Yahoo ({pc(y_or_pre)} to {pc(y_or_post)}) and Outlook ({pc(o_or_pre)} to {pc(o_or_post)}) are flat; Postmaster domain reputation dropped from High to Low and then Bad. "Delivered" ({pc(del_post)}) only means accepted, not inboxed. Counts as found if report.md isolates the drop to Gmail (or to spam-folder placement / domain reputation).
2. Gmail spam rate hidden from the ESP. Postmaster user-reported spam rate is {min(pm_spam_post) * 100:.2f}%-{max(pm_spam_post) * 100:.2f}% from 8 September, above Google's 0.3% limit, while the ESP shows complaints of {pc(esp_comp, 2)}. Counts as found if report.md cites the Postmaster spam rate above 0.3% (or says the ESP complaint figure misses Gmail complaints).
3. Volume spike. The 8 September reactivation send went to {blast_row[2]:,} addresses against about {normal_vol:,.0f} normally, with a {pc(blast_row[4] / blast_row[2])} bounce rate, the day before Gmail reputation fell. Counts as found if report.md links the reactivation blast (volume or old addresses) to the reputation drop.
4. One-click unsubscribe off. Settings show the List-Unsubscribe header as mailto only and one-click (List-Unsubscribe-Post) off, required for bulk senders by Gmail and Yahoo. Counts as found if report.md flags it.
5. Hard bounces not suppressed. Hard bounce handling is "suppress after 3 hard bounces"; the bounce log shows {rep_bounces} of 60 sampled addresses hard-bounced 2-4 times. Counts as found if report.md says to suppress on the first hard bounce.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 5, each with evidence.
FAIL if fewer than 3.
"""

g_decision = f"""
The correct recommendation: do not start with subject-line tests or more frequency. September's dip is a Gmail deliverability problem (reputation Low/Bad, spam rate above 0.3%), so Q4 starts with repairing it: stop mailing the reactivated / unengaged addresses, send to engaged Gmail recipients only and at steady volume, turn on one-click unsubscribe, suppress hard bounces on first bounce; re-read opens and clicks once reputation recovers.

Naive answer: accept the plan (subject-line and preheader tests, three sends a week) because "deliverability is fine" at {pc(del_post)} delivered.

PASS if report.md rejects or postpones the subject-line programme and the frequency increase, and makes Gmail reputation / deliverability repair the first priority.
FAIL if report.md endorses the subject-line tests or the frequency increase as the main Q4 action, or calls deliverability fine.
"""

g_decoy = f"""
Two things look odd but are fine and must not be presented as problems:
- D1. Apple Mail (apple_icloud) open rates around {pc(apple_or, 0)} are inflated by privacy-proxy opens. That is expected; it is neither a win nor a fault (it just means opens are not a reliable verdict).
- D2. Unsubscribe rates of {min(unsubs) * 100:.2f}%-{max(unsubs) * 100:.2f}% per send are in the normal range.

PASS if report.md does not present Apple's high open rate as a tracking error or as Apple being the best audience, and does not flag the unsubscribe rates as too high. Explaining Apple opens as privacy-proxy opens is fine.
FAIL if either is presented as a problem or a win to act on.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: OR {or_pre:.3f}->{or_post:.3f}; gmail {g_or_pre:.3f}->{g_or_post:.3f}; yahoo {y_or_pre:.3f}->{y_or_post:.3f}; delivered {del_post:.4f}; "
      f"pm spam {min(pm_spam_post):.4f}-{max(pm_spam_post):.4f} esp {esp_comp:.5f}; blast {blast_row[2]} vs {normal_vol:.0f}; rep bounces {rep_bounces}")
