---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: ranked on contribution after ad spend (revenue ex VAT and delivery, minus landed cost, returns, pick/pack and ad cost), the order is Kitchen, Lighting, Bedding, Small Appliances, Phone & Tech Accessories. Phone & Tech Accessories LOSE money (-£2,774 in Q3, -0.33 per £) despite the best ROAS; Kitchen earns the most per £ (+0.24) despite the lowest ROAS. Even applying the margin to the VAT-inclusive conversion value would make accessories look profitable (£4,609), so only the ex-VAT view gets this right.

The naive answer (the draft plan) puts the extra budget into Accessories and the LED strip and trims Kitchen, because it ranks on ROAS.

PASS if report.md's main recommendation moves budget toward Kitchen (optionally also Lighting or other margin-positive lines) and away from, or at least not into, Phone & Tech Accessories, and rejects the draft's plan to trim Kitchen.
FAIL if it recommends adding budget to Accessories, trimming Kitchen, or scaling the LED strip as the main move, or if it ranks product types on ROAS alone.
