---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth. With one content person and domain authority 34, the work that moves traffic is pushing keywords already ranking in positions 4-20 (page 1 lower half / page 2, mostly low difficulty) into the top 3. Those keywords are: how to clean running shoes (pos 17, vol 6,600); trail running vest (pos 9, vol 5,400); best trail running shoes for beginners (pos 7, vol 4,400); waterproof trail running shoes (pos 14, vol 3,600); trail running shoes wide toe box (pos 11, vol 2,900); trail running shoes sale (pos 6, vol 2,400); zero drop trail shoes (pos 5, vol 1,900); trail running gaiters (pos 13, vol 1,600); trail shoe size guide (pos 4, vol 1,300).
Wrong targets that a sort by volume picks: running shoes (pos 64, vol 201,000, KD 91); trail running shoes (pos 57, vol 49,500, KD 78); marathon training plan (pos 72, vol 40,500, KD 84); northpeak running (pos 1, vol 14,800, KD 22); running socks (pos 88, vol 12,100, KD 62); northpeak shoes (pos 2, vol 9,900, KD 18); carbon plate running shoes (pos 41, vol 9,900, KD 58); how to start trail running (pos 3, vol 8,100, KD 35). Head terms at positions 41-88 with difficulty 58-91 are out of reach for a DA-34 site in one quarter; brand terms and "how to start trail running" already rank in the top 3.

PASS if at least 6 of the keywords report.md chooses as focus keywords currently rank in positions 4-20, AND none of these is chosen as a focus keyword: running shoes, trail running shoes, marathon training plan, running socks, northpeak running, northpeak shoes.
FAIL otherwise (e.g. the focus list is mostly the highest-volume keywords, or includes any of the excluded keywords as a focus target). Mentioning excluded keywords only to explain why they were NOT chosen is fine.
