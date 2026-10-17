"""Pick SEO focus keywords for one content person on a DA-34 site. Sorting by
volume picks head terms ranking 50-90 on difficulty 60-90 and brand terms
already in the top 3. The striking-distance band (rank 4-20, low difficulty)
is where one person moves traffic; one keyword is split across two URLs."""
import sys, random, math; from pathlib import Path; sys.path.insert(0, str(Path(__file__).resolve().parents[1])); from common import write_case, to_csv

NAME = "channel-seo-keyword-focus"
KW = [  # keyword, volume, position, url, intent, kd
    ("running shoes", 201000, 64, "/running-shoes", "commercial", 91),
    ("trail running shoes", 49500, 57, "/trail-running-shoes", "commercial", 78),
    ("northpeak running", 14800, 1, "/", "navigational", 22),
    ("northpeak shoes", 9900, 2, "/", "navigational", 18),
    ("best trail running shoes for beginners", 4400, 7, "/blog/best-trail-shoes-beginners", "commercial", 31),
    ("trail running shoes wide toe box", 2900, 11, "/trail-running-shoes/wide", "commercial", 27),
    ("how to start trail running", 8100, 3, "/blog/start-trail-running", "informational", 35),
    ("waterproof trail running shoes", 3600, 14, "/trail-running-shoes/waterproof", "transactional", 33),
    ("waterproof trail running shoes", 3600, 19, "/blog/waterproof-vs-breathable", "transactional", 33),
    ("trail running shoes sale", 2400, 6, "/sale/trail", "transactional", 24),
    ("marathon training plan", 40500, 72, "/blog/marathon-plan", "informational", 84),
    ("running socks", 12100, 88, "/socks", "commercial", 62),
    ("trail running vest", 5400, 9, "/vests", "transactional", 29),
    ("best running shoes for flat feet", 6600, 24, "/blog/flat-feet", "commercial", 46),
    ("zero drop trail shoes", 1900, 5, "/trail-running-shoes/zero-drop", "commercial", 22),
    ("trail shoe size guide", 1300, 4, "/size-guide", "informational", 15),
    ("northpeak trail x2 review", 880, 2, "/products/trail-x2", "commercial", 12),
    ("how to clean running shoes", 6600, 17, "/blog/clean-shoes", "informational", 21),
    ("carbon plate running shoes", 9900, 41, "/road/carbon", "commercial", 58),
    ("trail running gaiters", 1600, 13, "/accessories/gaiters", "transactional", 19),
]
rows = [[k, p, v, kd, "https://www.northpeak.com" + u, i] for k, v, p, u, i, kd in KW]
csv_text = to_csv(["keyword", "position", "search_volume", "keyword_difficulty", "url", "intent"], rows)

uniq = {}
for k, v, p, u, i, kd in KW:
    uniq.setdefault(k, (v, p, kd))
by_vol = sorted(uniq, key=lambda k: -uniq[k][0])[:8]
band = sorted({k for k, (v, p, kd) in uniq.items() if 4 <= min(pp for kk, vv, pp, *_ in KW if kk == k) <= 20},
              key=lambda k: -uniq[k][0])
EXCL = ["running shoes", "trail running shoes", "marathon training plan", "running socks", "northpeak running", "northpeak shoes"]
assert len(set(by_vol) & set(band)) <= 2 and len(band) >= 8
assert all(k in by_vol for k in EXCL)
dup = [k for k in uniq if sum(1 for x in KW if x[0] == k) > 1]
assert dup == ["waterproof trail running shoes"]
print(f"{NAME}: naive top-8 by volume {by_vol}; band 4-20 {len(band)} kws")

prompt = """
resources/keyword_rankings.csv is our Semrush organic positions export for northpeak.com (domain authority 34). We have one content person this quarter. Which keywords should our SEO work focus on? Pick up to 8 and say what to do for each in report.md.
"""
desc = lambda k: f"{k} (pos {uniq[k][1]}, vol {uniq[k][0]:,}, KD {uniq[k][2]})"
g_band = f"""
Ground truth. With one content person and domain authority 34, the work that moves traffic is pushing keywords already ranking in positions 4-20 (page 1 lower half / page 2, mostly low difficulty) into the top 3. Those keywords are: {"; ".join(f"{k} (pos {min(x[2] for x in KW if x[0]==k)}, vol {uniq[k][0]:,})" for k in band)}.
Wrong targets that a sort by volume picks: {"; ".join(desc(k) for k in by_vol)}. Head terms at positions 41-88 with difficulty 58-91 are out of reach for a DA-34 site in one quarter; brand terms and "how to start trail running" already rank in the top 3.

PASS if at least 6 of the keywords report.md chooses as focus keywords currently rank in positions 4-20, AND none of these is chosen as a focus keyword: {", ".join(EXCL)}.
FAIL otherwise (e.g. the focus list is mostly the highest-volume keywords, or includes any of the excluded keywords as a focus target). Mentioning excluded keywords only to explain why they were NOT chosen is fine.
"""
g_can = """
Ground truth: "waterproof trail running shoes" (3,600/month, transactional intent) ranks with two different URLs: the category page /trail-running-shoes/waterproof at position 14 and the blog post /blog/waterproof-vs-breathable at position 19. The two pages compete with each other (keyword cannibalisation). One page should own the term (the category page, matching the transactional intent), with the blog post re-targeted to an informational angle and/or linking to the category page (or consolidated / canonicalised).

PASS if report.md notes that two URLs compete for "waterproof trail running shoes" and recommends that one page (ideally the category page) owns it.
FAIL if this is not mentioned.
"""
write_case(NAME, {"resources/keyword_rankings.csv": csv_text}, prompt, [("bands", 3, g_band), ("cannibal", 2, g_can)])
