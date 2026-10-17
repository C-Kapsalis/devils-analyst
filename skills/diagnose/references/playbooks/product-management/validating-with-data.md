---
title: Validating concepts with data
question: How do you test whether people would actually buy, and which features they would pay for?
order: 5
---

Between "we like this concept" and "we should build this concept" sit two survey-shaped checkpoints: concept testing, which validates demand, and conjoint analysis, which optimizes the feature set. For marketers moving toward product, this is home turf: it is market research pointed at a build decision.

## The framework

**Concept testing** shows target customers a concept (description plus visual) and measures purchase intent. Clean the data, compute the descriptive statistics (mean purchase intent, top-box and top-two-box shares, percent ranked first), and run significance tests before declaring a winner between concepts. Demand then forecasts as *Q = N × A × P*: the number of target customers, times the awareness-and-availability fraction, times the surveyed purchase probability (conventionally discounted, since stated intent overstates behavior).

**Conjoint analysis** answers the finer question: which attributes drive preference, and what is each level worth? Pick 3-5 attributes with concrete levels, generate an experimental set of profiles, have respondents rate them, then regress to estimate part-worth utilities. From the part-worths you get attribute importance (which dimensions move choice), the optimal profile (best combination), and willingness to pay for each upgrade. Segment the respondents, using demographics plus clustering on preferences, and you often find distinct groups wanting different products at different prices, which is a portfolio decision, not an averaging problem.

The two steps bridge validated concept and final specification: the concept test says *whether* to proceed, the conjoint says *what exactly* to build and *what to charge*.

## Metrics that matter (and their traps)

- **Top-two-box purchase intent**: the share saying "definitely/probably would buy." The trap: reading stated intent as literal conversion; discount it, and mind the gap between survey enthusiasm and payment.
- **Attribute importance (%)**: how much each dimension moves preference. The trap: optimizing an attribute customers barely weigh because the team finds it interesting.
- **Willingness to pay per feature**: the dollar value of an upgrade from part-worths. The trap: pricing at the average WTP when segments diverge; the average customer may not exist.
- **Statistical significance between concepts**: a t-test before declaring a winner. The trap: crowning a concept on a 0.2-point difference that is pure noise.

## Interview prep

**"How would you forecast first-year sales for a new product?"**
Q = N × A × P, stated aloud with its caveats: define the target population, estimate realistic awareness and availability, and discount stated purchase intent. Candidates who name the discount step show they have seen surveys meet reality.

**"Marketing wants the premium feature set; finance wants the cheap one. How do you settle it?"**
Conjoint: measure what each feature is worth to customers in currency, then compare WTP against cost. The argument dissolves into arithmetic, and segmentation may reveal both sides are right for different segments.

**"What is the biggest mistake teams make with concept tests?"**
Treating a relative winner as an absolute green light. A concept can beat its alternatives and still fail the market; check intent levels against benchmarks and the economics, not just the horse race.

**"When would you not trust conjoint results?"**
When attributes interact (the method assumes additive utilities), when levels are unrealistic, or when the sample skews away from the buying population. Knowing the method's assumptions is what separates users from operators.
