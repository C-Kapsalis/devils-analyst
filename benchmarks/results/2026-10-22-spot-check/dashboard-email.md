# dashboard-email

Spot check of 2026-10-22. Skill arm A read `hooks/core.md`, `skills/marketing-dashboard/SKILL.md` and the references it names; arm B had no skill. Both arms: Claude Haiku, one run each, the case prompt and the fixture files written by the case's `scaffold.sh`. Graded by the author against [the case's graders](../../cases/dashboard-email/graders/) as written. Method and limits: [README.md](README.md).

## Prompt

> resources/email_sends.csv has our email sends for August and September 2026 (one row per campaign send to one segment). Build me a dashboard as a single self-contained HTML file, dashboard.html (inline CSS and JS, no external requests), that shows how email did in September compared with August, why, and what we should do next. My team will look at it in our Monday meeting.
> 
> Save dashboard.html in the current working directory, not inside resources/.

## Grades

| Grader | A (with skill) | B (without) | Why |
|---|---|---|---|
| `bridge-adds-up` | PASS | FAIL | A: waterfall 28,900 -4,960 -2,212 +10,400 = 32,128; B: segment table without a change column, the split is in words only |
| `headline-answer` | PASS | PASS | A: title states it; B: the opening answer card states it (the page title is a topic) |
| `hypotheses-and-checks` | PASS | FAIL | A: each action has Action and Verify, causes tagged hypothesis; B: "The main driver is fewer opens" stated as fact, "Report VIP separately" has no check |
| `mix-vs-rate` | PASS | FAIL | A: blended 4.32% next to like-for-like 3.52%, says VIP lifts the blend; B: shows only like-for-like rates, no blended rate or mix split (borderline) |
| `no-good-news-on-mix` | PASS | PASS | A: CTR tile neutral grey with the mix note on the tile; B: no blended CTR tile |

## Arm A answer (with skill)

````html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Email: September vs August</title>
<style>
:root {
  --bg: #f7f7f5; --panel: #ffffff; --ink: #1d1d1b; --muted: #66665f; --line: #e2e2dc;
  --grey: #b9b9b3; --blue: #1f5fa8; --orange: #c8741e; --purple: #6b4fa0; --red: #b3261e;
  --tile-note: #66665f;
}
:root[data-theme="dark"] {
  --bg: #161614; --panel: #1f1f1c; --ink: #ededE8; --muted: #a3a39b; --line: #33332f;
  --grey: #6d6d67; --blue: #6fa6e8; --orange: #e9a25c; --purple: #a890e0; --red: #ff8a80;
  --tile-note: #a3a39b;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #161614; --panel: #1f1f1c; --ink: #ededE8; --muted: #a3a39b; --line: #33332f;
    --grey: #6d6d67; --blue: #6fa6e8; --orange: #e9a25c; --purple: #a890e0; --red: #ff8a80;
    --tile-note: #a3a39b;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0; background: var(--bg); color: var(--ink);
  font: 15px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}
main { max-width: 1080px; margin: 0 auto; padding: 24px 16px 48px; }
h1 { font-size: 24px; line-height: 1.25; margin: 0 0 6px; }
h2 { font-size: 18px; margin: 0 0 10px; }
.sub { color: var(--muted); margin: 0 0 20px; font-size: 14px; }
section { margin: 28px 0; }
.tiles { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; }
.tile { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px; }
.tile .label { font-size: 13px; color: var(--muted); }
.tile .value { font-size: 26px; font-weight: 600; margin: 2px 0; }
.tile .change { font-size: 14px; font-weight: 600; }
.tile .note { font-size: 12.5px; color: var(--tile-note); margin-top: 6px; }
.grey { color: var(--muted); }
.bad { color: var(--red); }
.panel { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 16px; }
svg { width: 100%; height: auto; display: block; }
svg text { fill: var(--ink); font-size: 13px; }
svg .small { fill: var(--muted); font-size: 12px; }
.table-wrap { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 14px; background: var(--panel); }
th, td { padding: 8px 10px; border-bottom: 1px solid var(--line); text-align: right; white-space: nowrap; }
th:first-child, td:first-child { text-align: left; }
th { font-weight: 600; color: var(--muted); font-size: 12.5px; }
tbody tr:hover { background: var(--bg); }
tfoot td { font-weight: 600; }
.finding { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px 16px; margin-bottom: 12px; }
.finding h3 { font-size: 15px; margin: 0 0 6px; }
.finding p { margin: 6px 0; }
.finding .tag { font-size: 12px; color: var(--muted); text-transform: uppercase; letter-spacing: .04em; }
.legend { display: flex; flex-wrap: wrap; gap: 14px; font-size: 13px; color: var(--muted); margin-top: 8px; }
.legend span::before { content: ""; display: inline-block; width: 10px; height: 10px; border-radius: 2px; margin-right: 6px; vertical-align: -1px; background: var(--c); }
details { background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 12px 16px; }
summary { cursor: pointer; font-weight: 600; }
details dl { display: grid; grid-template-columns: max-content 1fr; gap: 6px 14px; font-size: 14px; margin: 12px 0 0; }
details dt { font-weight: 600; }
details dd { margin: 0; color: var(--muted); }
@media (max-width: 480px) {
  main { padding: 16px 16px 40px; }
  h1 { font-size: 21px; }
  .tile .value { font-size: 22px; }
}
</style>
</head>
<body>
<main>

<header>
  <h1>September email revenue rose 11%, but only the new VIP send grew it; the two existing segments fell 25%</h1>
  <p class="sub">September 2026 vs August 2026. Four sends per month, one row per send and segment. Source: resources/email_sends.csv (20 rows, sends 4 Aug to 22 Sep 2026). Revenue is the platform-attributed figure; the file does not state its currency or attribution window.</p>
</header>

<section aria-labelledby="kpi">
  <h2 id="kpi">Five numbers for the meeting</h2>
  <div class="tiles">
    <div class="tile">
      <div class="label">Revenue, September vs August</div>
      <div class="value">32,128</div>
      <div class="change grey">+3,228 (+11.2%)</div>
      <div class="note">Vs 28,900 in August. Same segments only: 21,728, down 7,172 (-24.8%). The VIP send adds 10,400.</div>
    </div>
    <div class="tile">
      <div class="label">Revenue per delivered email</div>
      <div class="value">0.192</div>
      <div class="change grey">+0.007 (+3.8%)</div>
      <div class="note">Vs 0.185 in August. Same segments: 0.137, down 25.9%. The gain is the VIP mix.</div>
    </div>
    <div class="tile">
      <div class="label">Click rate (unique clicks / delivered)</div>
      <div class="value">4.32%</div>
      <div class="change grey">+0.36 pts</div>
      <div class="note">Vs 3.96%. Same segments: 3.52%, down 0.44 pts. The VIP segment clicks at 19.0% and lifts the blend.</div>
    </div>
    <div class="tile">
      <div class="label">Orders per 1,000 delivered</div>
      <div class="value">4.32</div>
      <div class="change bad">-0.41 (-8.6%)</div>
      <div class="note">Vs 4.73 in August. Same segments: 3.30, down 30.2%. Orders are the leak.</div>
    </div>
    <div class="tile">
      <div class="label">Unsubscribe rate (unsubscribes / delivered)</div>
      <div class="value">0.148%</div>
      <div class="change grey">flat (Aug 0.148%)</div>
      <div class="note">248 unsubscribes on 167,416 delivered, vs 232 on 156,360. No list-health alarm.</div>
    </div>
  </div>
</section>

<section aria-labelledby="changed">
  <h2 id="changed">What changed: August revenue to September revenue</h2>
  <div class="panel">
    <svg viewBox="0 0 660 272" role="img" aria-label="Bridge from August revenue 28,900 to September 32,128: newsletter subscribers minus 4,960, active customers minus 2,212, VIP repeat buyers plus 10,400.">
      <line x1="0" y1="240" x2="660" y2="240" stroke="currentColor" stroke-opacity=".25"/>
      <!-- August total -->
      <rect x="20" y="60.8" width="100" height="179.2" fill="var(--grey)"/>
      <text x="70" y="52" text-anchor="middle">28,900</text>
      <!-- Newsletter subscribers -4,960 -->
      <rect x="150" y="60.8" width="100" height="30.8" fill="var(--red)"/>
      <text x="200" y="52" text-anchor="middle">-4,960</text>
      <!-- Active customers -2,212 -->
      <rect x="280" y="91.6" width="100" height="13.7" fill="var(--red)"/>
      <text x="330" y="84" text-anchor="middle">-2,212</text>
      <!-- VIP +10,400 -->
      <rect x="410" y="40.8" width="100" height="64.5" fill="var(--purple)"/>
      <text x="460" y="34" text-anchor="middle">+10,400</text>
      <!-- September total -->
      <rect x="540" y="40.8" width="100" height="199.2" fill="var(--blue)"/>
      <text x="590" y="34" text-anchor="middle">32,128</text>
      <!-- Category labels -->
      <text class="small" x="70" y="258" text-anchor="middle">August total</text>
      <text class="small" x="200" y="258" text-anchor="middle">Newsletter subscribers</text>
      <text class="small" x="330" y="258" text-anchor="middle">Active customers</text>
      <text class="small" x="460" y="258" text-anchor="middle">VIP repeat buyers (new)</text>
      <text class="small" x="590" y="258" text-anchor="middle">September total</text>
    </svg>
    <p class="sub" style="margin:10px 0 0">Read left to right. Red bars cut revenue; the purple bar is the only growth. Same-segment change: -7,172.</p>
  </div>
</section>

<section aria-labelledby="where">
  <h2 id="where">Where: by segment, sorted by contribution to the change</h2>
  <div class="table-wrap">
  <table>
    <thead>
      <tr>
        <th>Segment</th>
        <th>Delivered Aug</th>
        <th>Delivered Sep</th>
        <th>Click rate Aug</th>
        <th>Click rate Sep</th>
        <th>Orders per 1,000 Aug</th>
        <th>Orders per 1,000 Sep</th>
        <th>Revenue Aug</th>
        <th>Revenue Sep</th>
        <th>Revenue change</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>VIP repeat buyers (new in Sep)</td>
        <td>none</td>
        <td>8,712</td>
        <td>none</td>
        <td>19.0%</td>
        <td>none</td>
        <td>22.96</td>
        <td>none</td>
        <td>10,400</td>
        <td>+10,400</td>
      </tr>
      <tr>
        <td>Newsletter subscribers</td>
        <td>120,900</td>
        <td>122,848</td>
        <td>3.60%</td>
        <td>3.00%</td>
        <td>3.97</td>
        <td>2.70</td>
        <td>18,240</td>
        <td>13,280</td>
        <td class="bad">-4,960 (-27.2%)</td>
      </tr>
      <tr>
        <td>Active customers</td>
        <td>35,460</td>
        <td>35,856</td>
        <td>5.20%</td>
        <td>5.30%</td>
        <td>7.33</td>
        <td>5.35</td>
        <td>10,660</td>
        <td>8,448</td>
        <td class="bad">-2,212 (-20.8%)</td>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <td>Total</td>
        <td>156,360</td>
        <td>167,416</td>
        <td>3.96%</td>
        <td>4.32%</td>
        <td>4.73</td>
        <td>4.32</td>
        <td>28,900</td>
        <td>32,128</td>
        <td>+3,228 (+11.2%)</td>
      </tr>
    </tfoot>
  </table>
  </div>
  <p class="sub" style="margin-top:10px">Revenue per order: newsletter 38.00 to 40.00; active customers 41.00 to 44.00; VIP 52.00. Order value rose in both existing segments while the number of orders fell.</p>
  <p class="sub">Opens (trend only, inflated by privacy protection): newsletter 40.0% to 33.3%; active customers 40.0% to 40.8%.</p>
</section>

<section aria-labelledby="todo">
  <h2 id="todo">What to do</h2>

  <div class="finding">
    <div class="tag">Check first, before Monday</div>
    <h3>Every week in each month repeats the same numbers</h3>
    <p>Each segment has identical sent, delivered, click, order and revenue values in all four August sends, and again in all four September sends. Real weekly sends rarely match to the unit. The file cannot show whether the decline is steady or one bad send.</p>
    <p><strong>Action:</strong> ask whoever exported the file to confirm these are per-send figures. If each row is a monthly total copied four times, the revenue totals above are four times too high. The percentages do not change.</p>
    <p><strong>Verify:</strong> the send-level report in the platform shows different numbers for at least two of the four September sends.</p>
  </div>

  <div class="finding">
    <div class="tag">Hypothesis, not proven</div>
    <h3>Both existing segments buy less per click, and the newsletter also gets fewer clicks</h3>
    <p>Same segments, revenue down 7,172 (-24.8%). Orders per click fell from 11.0% to 9.0% for newsletter subscribers and from 14.1% to 10.1% for active customers. The newsletter's click rate fell from 3.60% to 3.00%, which is 668 fewer clicks on a larger list.</p>
    <p><strong>Likely cause (hypothesis):</strong> September offers or landing pages converted fewer of the people who clicked, or the VIP send, which went out on the same day each week, took attention or buyers from the other segments. The file has no offer, subject line or landing-page data to tell these apart.</p>
    <p><strong>Action:</strong> compare the September newsletter and active-customer offers, subject lines and landing pages with August's.</p>
    <p><strong>Verify:</strong> on the next send, hold out 10% of each existing segment and send it the August-style version. A gap in orders per click that holds across the split is evidence; a gap that disappears is not.</p>
  </div>

  <div class="finding">
    <div class="tag">Hypothesis, not proven</div>
    <h3>The VIP send's 10,400 is the whole September gain, and the file cannot show it is new money</h3>
    <p>VIP repeat buyers earned 2,600 per send, 1.19 per delivered email, at 52.00 per order. Without them, September revenue would be 21,728, down 24.8%.</p>
    <p><strong>Likely cause (hypothesis):</strong> VIP repeat buyers are probably also active customers or newsletter subscribers. Their orders may be counted in more than one segment's attribution, or they may have bought anyway. The file has no customer IDs, so overlap cannot be measured here.</p>
    <p><strong>Action:</strong> before presenting VIP as a gain, count unique customers and orders across the three segments in the platform or the order system, and report the de-duplicated revenue.</p>
    <p><strong>Verify:</strong> hold out 10% of VIP repeat buyers from one send. If their orders hold up against the holdout, the send is working; if not, the 10,400 is partly attribution.</p>
  </div>
</section>

<section aria-labelledby="defs">
  <h2 id="defs">Definitions and data notes</h2>
  <details>
    <summary>Metric dictionary, sources and checks</summary>
    <dl>
      <dt>Delivered rate</dt><dd>delivered / sent. Aug 97.7%, Sep 97.8%. Above the 95% line.</dd>
      <dt>Click rate</dt><dd>unique clicks / delivered. Unique clicks as reported by the platform. Totals are recomputed from summed parts, not averaged.</dd>
      <dt>Orders per 1,000 delivered</dt><dd>orders / delivered x 1,000. Orders as attributed by the platform.</dd>
      <dt>Revenue per delivered</dt><dd>attributed revenue / delivered. Currency and attribution window are not stated in the file.</dd>
      <dt>Revenue per order</dt><dd>attributed revenue / orders.</dd>
      <dt>Unsubscribe rate</dt><dd>unsubscribes / delivered.</dd>
      <dt>Opens</dt><dd>unique opens / delivered. Inflated by privacy protection and image prefetching; shown as a trend only, never as a KPI.</dd>
      <dt>Same segments</dt><dd>newsletter subscribers plus active customers, the two segments sent in both months. Used for every like-for-like figure.</dd>
      <dt>Colour</dt><dd>Blue is September, grey is August, purple is VIP repeat buyers, orange is active customers. Red marks money lost.</dd>
      <dt>Exclusions</dt><dd>none. All 20 rows are included; no send is incomplete.</dd>
      <dt>Reconciliation</dt><dd>August revenue 18,240 + 10,660 = 28,900. September revenue 13,280 + 8,448 + 10,400 = 32,128. Both match the totals. Delivered and clicks sum to the totals in the table.</dd>
      <dt>Sample size</dt><dd>four sends per segment per month, two months. No prior-year comparison is in the file, so seasonality cannot be ruled out.</dd>
      <dt>Mix note</dt><dd>the blended click rate and revenue per delivered rose only because the VIP segment, with a higher click rate and revenue per email, joined in September.</dd>
    </dl>
  </details>
</section>

</main>
<script>
document.querySelectorAll('tbody tr').forEach(function (row) {
  row.addEventListener('click', function () { row.classList.toggle('picked'); });
});
</script>
</body>
</html>
````

## Arm B answer (without skill)

````html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Email Dashboard: Sep vs Aug 2026</title>
<style>
:root{--bg:#f6f7f9;--card:#ffffff;--ink:#1d2330;--muted:#5b6474;--line:#e2e6ec;--good:#1f7a4d;--bad:#b42318;--aug:#8fa3bf;--sep:#2f5fd0;--note:#fff8e6;--notebd:#f0d78c;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#12151c;--card:#1b2029;--ink:#e8ebf1;--muted:#a3acbb;--line:#2a313d;--good:#4ccf8f;--bad:#ff8a80;--aug:#5d6f8c;--sep:#7aa2ff;--note:#2b2513;--notebd:#5c4b1c;}}
:root[data-theme="dark"]{--bg:#12151c;--card:#1b2029;--ink:#e8ebf1;--muted:#a3acbb;--line:#2a313d;--good:#4ccf8f;--bad:#ff8a80;--aug:#5d6f8c;--sep:#7aa2ff;--note:#2b2513;--notebd:#5c4b1c;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
main{max-width:980px;margin:0 auto;padding:24px 16px 48px}
h1{font-size:24px;margin:0 0 4px}
h2{font-size:18px;margin:32px 0 12px}
.sub{color:var(--muted);margin:0 0 20px;font-size:14px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:16px}
.answer{background:var(--note);border-color:var(--notebd)}
.answer p{margin:0 0 8px;font-weight:600}
ul,ol{margin:8px 0 0;padding-left:20px}
li{margin-bottom:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.tile .k{color:var(--muted);font-size:13px}
.tile .v{font-size:22px;font-weight:700;margin:2px 0}
.tile .c{font-size:13px}
.up{color:var(--good)} .down{color:var(--bad)} .muted{color:var(--muted)}
.table-wrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;min-width:720px;font-size:14px}
th,td{padding:9px 10px;text-align:right;border-bottom:1px solid var(--line);white-space:nowrap}
th:first-child,td:first-child{text-align:left}
th{color:var(--muted);font-weight:600;font-size:13px}
tr:last-child td{border-bottom:none}
.bars{display:grid;gap:10px}
.bar-row{display:grid;grid-template-columns:150px 1fr;gap:10px;align-items:center}
.bar-label{font-size:14px}
.bar-track{position:relative;height:22px}
.bar{height:10px;border-radius:4px;margin:2px 0}
.bar.aug{background:var(--aug)} .bar.sep{background:var(--sep)}
.bar-val{font-size:12px;color:var(--muted);margin-left:6px}
.legend{font-size:13px;color:var(--muted);margin-top:8px}
.sw{display:inline-block;width:10px;height:10px;border-radius:2px;margin:0 4px 0 10px;vertical-align:middle}
.note{font-size:13px;color:var(--muted)}
@media (max-width:560px){.bar-row{grid-template-columns:1fr}}
</style>
</head>
<body>
<main>
<h1>Email: September vs August 2026</h1>
<p class="sub">Source: resources/email_sends.csv, 20 sends (8 in August, 12 in September). Each row is one send to one segment. Rates are totals divided by totals.</p>

<section class="card answer">
<p>September email brought in fewer orders and less revenue than August to the same audiences. Total revenue is up only because a VIP segment was added in September.</p>
<ul>
<li>Like-for-like (newsletter subscribers + active customers): orders 740 to 524 (-29.2%), revenue 28,900 to 21,728 (-24.8%).</li>
<li>All sends, including VIP: orders 740 to 724 (-2.2%), revenue 28,900 to 32,128 (+11.2%). VIP alone accounts for 200 orders and 10,400 revenue.</li>
<li>The main driver is fewer opens. Newsletter open rate fell from 40.0% to 33.3%, while click-to-open stayed at 9.0%.</li>
<li>Active customers opened slightly more (40.0% to 40.8%) but ordered less per click: 14.1% of clicks became orders in August, 10.1% in September.</li>
</ul>
</section>

<h2>Like-for-like headline numbers</h2>
<p class="note" style="margin-top:-4px">Newsletter subscribers and active customers only, the two segments that ran in both months.</p>
<div class="grid">
<div class="tile"><div class="k">Delivered</div><div class="v">158,812</div><div class="c muted">Aug 156,360 &middot; <span class="up">+1.6%</span></div></div>
<div class="tile"><div class="k">Open rate</div><div class="v">35.0%</div><div class="c muted">Aug 40.0% &middot; <span class="down">-5.0 pts</span></div></div>
<div class="tile"><div class="k">Click rate</div><div class="v">3.52%</div><div class="c muted">Aug 3.96% &middot; <span class="down">-0.44 pts</span></div></div>
<div class="tile"><div class="k">Orders</div><div class="v">524</div><div class="c muted">Aug 740 &middot; <span class="down">-29.2%</span></div></div>
<div class="tile"><div class="k">Revenue</div><div class="v">21,728</div><div class="c muted">Aug 28,900 &middot; <span class="down">-24.8%</span></div></div>
<div class="tile"><div class="k">Revenue per delivered</div><div class="v">0.137</div><div class="c muted">Aug 0.185 &middot; <span class="down">-26.0%</span></div></div>
</div>

<h2>Where the drop comes from</h2>
<div class="card">
<div class="bars">
<div class="bar-row">
<div class="bar-label">Newsletter open rate</div>
<div>
<div class="bar aug" style="width:80%"></div><span class="bar-val">Aug 40.0%</span>
<div class="bar sep" style="width:66.6%"></div><span class="bar-val">Sep 33.3%</span>
</div>
</div>
<div class="bar-row">
<div class="bar-label">Active customer open rate</div>
<div>
<div class="bar aug" style="width:80%"></div><span class="bar-val">Aug 40.0%</span>
<div class="bar sep" style="width:81.6%"></div><span class="bar-val">Sep 40.8%</span>
</div>
</div>
<div class="bar-row">
<div class="bar-label">Newsletter orders per 1,000 delivered</div>
<div>
<div class="bar aug" style="width:39.7%"></div><span class="bar-val">Aug 4.0</span>
<div class="bar sep" style="width:27%"></div><span class="bar-val">Sep 2.7</span>
</div>
</div>
<div class="bar-row">
<div class="bar-label">Active customer orders per 1,000 delivered</div>
<div>
<div class="bar aug" style="width:73.3%"></div><span class="bar-val">Aug 7.3</span>
<div class="bar sep" style="width:53.5%"></div><span class="bar-val">Sep 5.4</span>
</div>
</div>
</div>
<p class="legend"><span class="sw" style="background:var(--aug)"></span>August<span class="sw" style="background:var(--sep)"></span>September. Bar scale: 50% = full width for rates; orders per 1,000 use the same scale for comparison.</p>
</div>

<div class="table-wrap">
<table>
<thead>
<tr>
<th>Segment</th><th>Delivered</th><th>Open rate</th><th>Click rate</th><th>Click-to-open</th><th>Orders per delivered</th><th>Orders</th><th>Revenue</th><th>Revenue per order</th><th>Unsubscribes</th>
</tr>
</thead>
<tbody>
<tr><td>Newsletter subscribers, Aug</td><td>120,900</td><td>40.0%</td><td>3.60%</td><td>9.0%</td><td>0.40%</td><td>480</td><td>18,240</td><td>38.00</td><td>180</td></tr>
<tr><td>Newsletter subscribers, Sep</td><td>122,848</td><td>33.3%</td><td>3.00%</td><td>9.0%</td><td>0.27%</td><td>332</td><td>13,280</td><td>40.00</td><td>184</td></tr>
<tr><td>Active customers, Aug</td><td>35,460</td><td>40.0%</td><td>5.20%</td><td>13.0%</td><td>0.73%</td><td>260</td><td>10,660</td><td>41.00</td><td>52</td></tr>
<tr><td>Active customers, Sep</td><td>35,856</td><td>40.8%</td><td>5.30%</td><td>13.0%</td><td>0.54%</td><td>192</td><td>8,448</td><td>44.00</td><td>52</td></tr>
<tr><td>VIP repeat buyers, Sep only</td><td>8,712</td><td>63.4%</td><td>19.0%</td><td>30.0%</td><td>0.23%</td><td>200</td><td>10,400</td><td>52.00</td><td>12</td></tr>
</tbody>
</table>
</div>
<p class="note">Revenue is as given in the source file; the file does not state a currency. Revenue per order is revenue divided by orders.</p>

<h2>What we should do next</h2>
<div class="card">
<ol>
<li><strong>Find out why newsletter opens fell</strong> from 40.0% to 33.3% while click-to-open held at 9.0%. Compare subject lines, send times and sender name for August and September, and check inbox placement or deliverability reports (not in this file).</li>
<li><strong>Check the click-to-order step for active customers.</strong> Clicks held and opens rose, but orders per 1,000 delivered fell from 7.3 to 5.4. Review landing pages, offers, stock and price changes, and the September promotion calendar.</li>
<li><strong>Test before the next newsletter send.</strong> Run a subject-line or send-time split with a holdout group so the next open-rate change can be attributed.</li>
<li><strong>Report VIP separately.</strong> Keep VIP out of the month-over-month totals. Its 63.4% open rate and 52.00 revenue per order are a benchmark, not a like-for-like comparison.</li>
<li><strong>Check the data before drawing conclusions.</strong> Every week within a month has identical numbers for each segment, so this file cannot show a weekly trend. Confirm the export holds actual per-send results.</li>
<li><strong>Watch unsubscribes.</strong> Like-for-like unsubscribes are almost flat (232 to 236), so list fatigue is not the visible cause of the drop.</li>
</ol>
</div>

<h2>Notes on the numbers</h2>
<div class="card note">
<ul>
<li>August has 8 sends (2 segments, 4 weeks). September has 12 sends (3 segments, 4 weeks), including the VIP segment added on 1 September.</li>
<li>Rates are summed counts divided by summed delivered, not averages of weekly rates. Open and click counts are unique.</li>
<li>The file has no spend, list size, subject lines or inbox-placement data, so the causes above are hypotheses to check, not conclusions.</li>
</ul>
</div>
</main>
</body>
</html>
````
