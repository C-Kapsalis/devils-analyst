---
type: llm
weight: 3
focus: { source: file, path: report.md }
---

Ground truth: the two sources must be counted separately, because only the 8 human interviews are customers speaking. Human (8): delivery_delays 6/8, price_vs_supermarket 5/8, packaging_waste 4/8, recipe_repetition 3/8, portion_size 2/8, customer_service 1/8, ai_meal_planning_app 0/8. Synthetic (20): ai_meal_planning_app 17/20, price_vs_supermarket 10/20, recipe_repetition 10/20, packaging_waste 6/20, portion_size 3/20, delivery_delays 2/20, customer_service 1/20. "ai_meal_planning_app" appears in 0 of 8 real interviews; it is something the AI personas produced, not something customers said.

Naive answer: pooling all 28 interviews: ai_meal_planning_app 17/28, price_vs_supermarket 15/28, recipe_repetition 13/28, packaging_waste 10/28, delivery_delays 8/28, portion_size 5/28, customer_service 2/28, which ranks "AI meal planning app" as the top customer theme and pushes delivery delays to fifth.

PASS if report.md keeps human and synthetic counts separate (or clearly labels the source of each theme's count) AND does not present AI meal planning as something customers told us.
FAIL if report.md's top-ranked customer theme is AI meal planning, or presents counts pooled over 28 interviews without source labels.
