"""Breadth: Q4 pipeline forecast before a CEO meeting (Brightlathe, B2B software, Oct 2026).

Planted problems (4): the deck applies the win rate by count to pipeline
value, but large deals (most of the Q4 value) win far less often, so expected
bookings fall well short of target (DECISION); a large share of Q4 pipeline
value is stale (no activity in 60+ days and close date pushed 3+ times);
coverage divides all open pipeline, including deals closing in 2027, by the
Q4 target; "pipeline generated in Q3" sums three month-end open-pipeline
snapshots (a stock counted as a flow).
Decoys (2): win rate computed as won / (won + lost), excluding open deals;
sales cycle quoted as a median."""
import sys, random, math, datetime as dt; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "bx-crm-q4-forecast"
rng = random.Random(82111)
TODAY = dt.date(2026, 10, 15)
TARGET = 2_400_000
BANDS = [("small", 15000, 50000, 0.40), ("mid", 50000, 100000, 0.27), ("large", 100000, 320000, 0.09)]
band_of = lambda a: "small" if a < 50000 else ("mid" if a < 100000 else "large")

# ---------- historical closed deals (Q3 2025 - Q3 2026) ----------
hist = []
mix = [("small", 140), ("mid", 70), ("large", 50)]
did = 1000
for b, n in mix:
    lo, hi, p = next((x[1], x[2], x[3]) for x in BANDS if x[0] == b)
    wins = int(round(n * p))
    outcomes = ["closedwon"] * wins + ["closedlost"] * (n - wins)
    rng.shuffle(outcomes)
    for o in outcomes:
        did += 1
        c = dt.date(2025, 7, 1) + dt.timedelta(days=rng.randint(0, 455))
        cyc = int(rng.lognormvariate(math.log(58 if b != "large" else 95), 0.5))
        hist.append([f"D{did}", int(rng.uniform(lo, hi) // 500 * 500), o, (c - dt.timedelta(days=cyc)).isoformat(), c.isoformat(), cyc])
won = [h for h in hist if h[2] == "closedwon"]
wr_count = len(won) / len(hist)
wr_value = sum(h[1] for h in won) / sum(h[1] for h in hist)
wr_band = {}
for b, _, _, _ in BANDS:
    hb = [h for h in hist if band_of(h[1]) == b]
    wr_band[b] = (sum(h[1] for h in hb if h[2] == "closedwon") / sum(h[1] for h in hb), sum(1 for h in hb if h[2] == "closedwon") / len(hb))
cycles = sorted(h[5] for h in won)
med_cycle = cycles[len(cycles) // 2]; mean_cycle = sum(cycles) / len(cycles)

# ---------- open deals ----------
STAGES = ["discovery", "demo", "proposal", "negotiation"]
open_deals = []
def mk(n, band, q4, stale_share):
    global did
    lo, hi = next((x[1], x[2]) for x in BANDS if x[0] == band)
    for _ in range(n):
        did += 1
        amt = int(rng.uniform(lo, hi) // 500 * 500)
        if q4:
            close = dt.date(2026, 10, 20) + dt.timedelta(days=rng.randint(0, 70))
        else:
            close = dt.date(2027, 1, 10) + dt.timedelta(days=rng.randint(0, 80))
        stale = rng.random() < stale_share
        last = TODAY - dt.timedelta(days=rng.randint(62, 140) if stale else rng.randint(1, 25))
        pushes = rng.randint(3, 5) if stale else rng.choice([0, 0, 0, 1, 1, 2])
        created = close - dt.timedelta(days=rng.randint(90, 240))
        open_deals.append([f"D{did}", f"{rng.choice(['Acme', 'Borealis', 'Cobalt', 'Delta', 'Ember', 'Fjord', 'Granite', 'Halcyon', 'Iris', 'Juniper'])} {rng.choice(['Foods', 'Logistics', 'Health', 'Retail', 'Energy', 'Labs', 'Group', 'Partners'])} {did % 97}",
                           amt, rng.choice(STAGES), close.isoformat(), created.isoformat(), last.isoformat(), pushes])
mk(34, "small", True, 0.15)
mk(16, "mid", True, 0.30)
mk(18, "large", True, 0.45)
mk(14, "small", False, 0.1)
mk(8, "mid", False, 0.1)
mk(6, "large", False, 0.1)
rng.shuffle(open_deals)
q4 = [d for d in open_deals if d[4] <= "2026-12-31"]
all_open = sum(d[2] for d in open_deals)
q4_val = sum(d[2] for d in q4)
is_stale = lambda d: (TODAY - dt.date.fromisoformat(d[6])).days >= 60 and d[7] >= 3
q4_stale = sum(d[2] for d in q4 if is_stale(d))
q4_live = [d for d in q4 if not is_stale(d)]
cov_deck = all_open / TARGET
cov_q4 = q4_val / TARGET
cov_live = sum(d[2] for d in q4_live) / TARGET
large_share = sum(d[2] for d in q4 if band_of(d[2]) == "large") / q4_val
exp_deck = all_open * wr_count
exp_band_all_q4 = sum(d[2] * wr_band[band_of(d[2])][0] for d in q4)
exp_band_live = sum(d[2] * wr_band[band_of(d[2])][0] for d in q4_live)

# ---------- month-end open pipeline snapshots ----------
snaps = [["2026-07-31", int(all_open * rng.uniform(0.90, 0.96))], ["2026-08-31", int(all_open * rng.uniform(0.96, 1.0))], ["2026-09-30", int(all_open * rng.uniform(0.99, 1.02))]]
snap_sum = sum(s[1] for s in snaps)
created_q3 = sum(d[2] for d in open_deals if "2026-07-01" <= d[5] <= "2026-09-30") + sum(h[1] for h in hist if "2026-07-01" <= h[3] <= "2026-09-30")

assert cov_deck > 3.0 and cov_q4 < 2.8 and cov_live < 2.0, (cov_deck, cov_q4, cov_live)
assert exp_deck > TARGET and exp_band_live < 0.5 * TARGET, (exp_deck, exp_band_live)
assert wr_count > 1.5 * wr_value
assert q4_stale / q4_val > 0.25
assert large_share > 0.5
assert snap_sum > 2.5 * created_q3
assert med_cycle < mean_cycle

usd = lambda x: f"${x:,.0f}"
pc = lambda x, d=0: f"{100 * x:.{d}f}%"

deck = f"""# Q4 2026 forecast (sales ops, for the CEO meeting)

- Q4 bookings target: {usd(TARGET)}.
- Open pipeline: {usd(all_open)}, **coverage {cov_deck:.1f}x** against target (healthy above 3x).
- Win rate (last 12 months): **{pc(wr_count)}** of closed deals won (won / (won + lost)).
- Expected Q4 bookings: {usd(all_open)} x {pc(wr_count)} = **{usd(exp_deck)}**, on track to beat target.
- Pipeline generated in Q3: **{usd(snap_sum)}** (July + August + September month-end pipeline).
- Median sales cycle: {med_cycle} days.

Ask: approve two new AE hires for Q1 on the back of the Q4 result.
"""

notes = f"""# Notes
- Brightlathe sells inspection software to manufacturers. Exports from the CRM on {TODAY.isoformat()}.
- open_deals.csv: all open deals. closed_deals_12m.csv: deals closed won or lost in the last ~15 months. pipeline_snapshots.csv: total open pipeline at each month end.
"""

files = {
    "resources/notes.md": notes,
    "resources/q4_forecast_deck.md": deck,
    "resources/open_deals.csv": to_csv(["deal_id", "deal_name", "amount", "deal_stage", "close_date", "create_date", "last_activity_date", "close_date_changes"], open_deals),
    "resources/closed_deals_12m.csv": to_csv(["deal_id", "amount", "deal_stage", "create_date", "close_date", "days_to_close"], hist),
    "resources/pipeline_snapshots.csv": to_csv(["snapshot_date", "open_pipeline_amount"], snaps),
}

prompt = """
I'm presenting the Q4 forecast (resources/q4_forecast_deck.md) to our CEO tomorrow, and asking for two new AE hires on the back of it. The CRM exports are in resources/. Anything I'm missing? What should I tell him? Please write it up in report.md.
"""

g_recall = f"""
The exports contain 4 planted problems. Answer key:

1. Win rate by count applied to value. {pc(wr_count)} is the share of deals won; by value it is {pc(wr_value)}. By deal size, value win rates are small {pc(wr_band['small'][0])}, mid {pc(wr_band['mid'][0])}, large (100k+) {pc(wr_band['large'][0])}, and large deals are {pc(large_share)} of Q4-closing pipeline. Counts as found if report.md says the count-based win rate overstates expected bookings because large deals win less often (or uses a value or size-band win rate).
2. Stale pipeline. {usd(q4_stale)} ({pc(q4_stale / q4_val)}) of Q4-closing pipeline has no activity in 60+ days and its close date changed 3+ times. Counts as found if report.md flags stale / repeatedly pushed deals with a number or deal list.
3. Coverage includes 2027 deals. The {cov_deck:.1f}x divides all open pipeline ({usd(all_open)}) by the Q4 target; deals with a Q4 close date total {usd(q4_val)} ({cov_q4:.1f}x), and about {cov_live:.1f}x without the stale deals. Counts as found if report.md recomputes coverage on Q4 close dates.
4. Pipeline generated summed from snapshots. {usd(snap_sum)} adds three month-end open-pipeline balances (a stock), so the same deals are counted up to three times; pipeline created in Q3 (deals with a Q3 create date) is about {usd(created_q3)}. Counts as found if report.md says the snapshots cannot be summed.

List which were found in your reasoning.
PASS if report.md identifies at least 3 of the 4, each with evidence.
FAIL if fewer than 3.
"""

g_decision = f"""
The correct message: Q4 is not on track. Using Q4-close deals only, excluding stale ones and applying value win rates by deal size, expected bookings are about {usd(exp_band_live)} (about {usd(exp_band_all_q4)} even keeping stale deals) against a {usd(TARGET)} target. So the forecast should be cut (or flagged at serious risk), and the AE hiring ask should not rest on this forecast (defer, or justify it differently).

Naive answer: present the deck as is ({cov_deck:.1f}x coverage, {usd(exp_deck)} expected, on track) and ask for the hires on that basis.

PASS if report.md concludes Q4 is likely to miss target (expected bookings well below {usd(TARGET)}) and advises against presenting the forecast as on track.
FAIL if report.md says Q4 is on track or endorses the {usd(exp_deck)} expected bookings, or supports the hires because of the forecast.
"""

g_decoy = f"""
Two things in the deck are correct and must not be presented as errors:
- D1. Win rate is computed as won / (won + lost), excluding open deals. That definition is correct (the problem is applying the count rate to value, not the definition).
- D2. The sales cycle is quoted as a median ({med_cycle} days; the mean of won deals is {mean_cycle:.0f}). The median is the right typical value.

PASS if report.md does not say open deals should be in the win-rate denominator and does not say the cycle should be the mean.
FAIL if either is presented as a mistake.
"""

write_case(NAME, files, prompt, [("subtle-recall", 3, g_recall), ("decision", 3, g_decision), ("no-false-alarms", 2, g_decoy)])
print(f"{NAME}: cov deck {cov_deck:.2f} q4 {cov_q4:.2f} live {cov_live:.2f}; wr count {wr_count:.3f} value {wr_value:.3f} bands {wr_band}; "
      f"exp deck {exp_deck:,.0f} band-live {exp_band_live:,.0f} band-q4 {exp_band_all_q4:,.0f}; stale {q4_stale / q4_val:.2f}; large {large_share:.2f}; snaps {snap_sum:,} created {created_q3:,}")
