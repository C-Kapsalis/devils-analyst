# Attribution: choosing and reading a model

Attribution decides how conversion credit is split across touchpoints. It
drives budget, channel valuation, smart bidding and ROI claims, so a model
change changes every downstream number.

## Rule-based models

| Model | Credit | Fits | Blind spot |
|---|---|---|---|
| Last click (incl. direct) | 100% last touch | Short transactional cycles, closing campaigns | Ignores everything before |
| Last non-direct click | 100% last non-direct touch (Google default outside path reports) | Direct visits as already-won users | Same |
| Last Google Ads click | 100% last Ads click | Crediting Ads specifically | Same |
| First click | 100% first touch | Awareness, unknown brands, growth phase | Ignores closers |
| Linear | Equal | Long journeys, no stage believed stronger | Treats a weak touch like a decisive one |
| Time decay | Exponential, 7-day half-life default (credit proportional to 2^(-days/7)) | Short consideration, short promotions | Starves early discovery |
| Position (U) | 40% first, 40% last, 20% middle | Both demand creation and capture matter | Weights are a convention |
| W-shaped | 30% first, 30% lead creation, 30% last, 10% rest | B2B, long cycles | Same |

Conservative to growth-oriented: last click, time decay, linear, position,
first click. The same paths can make a channel worthless under one model and
the leader under another; no rule-based model can be shown most accurate.

Checks: each single-touch column sums to total conversions or value with one
winner per path; Google models give direct no credit unless the whole path is
direct.

## The core weakness and data-driven attribution

Rule-based models see only buyers' paths; most visitors never convert, so a
path that ends in a purchase half the time and in nothing the other half
looks like a pure win. Data-driven models use converting and non-converting
paths and assign credit by removal effect (how many fewer conversions without
this touch), via Shapley values (average marginal contribution across all
combinations) or Markov chains (removal from the transition graph).

GA4 DDA: default in GA4 and Google Ads; up to 50 touchpoints; 90-day lookback;
retrains continuously; adds a time-decay element. Needs about 400 conversions
per key event in 30 days and roughly 10,000 paths with 2+ interactions; below
that it silently uses last click. Custom builds need more: Markov 2,000+,
Shapley 5,000+, full ML 10,000+ monthly conversions; below these, a rule-based
model is safer than an overfit one. DDA is a black box run by the seller of
the ads it grades.

## Reading a model comparison

GA4: Advertising -> Attribution -> model comparison. Pick the key event, date
range and two models (last click vs DDA). Positive % change: the channel
assists more than it closes (last click underfunds it). Negative: it closes
journeys others started (last click overcredits it).

Diagnostics before believing the table:
1. Monthly conversions for that key event >= 400? If not, DDA fell back and
   identical columns are an artefact.
2. Unassigned rows: credit there is an artefact of paths GA4 could not
   connect, not a channel; it shrinks sharply under DDA.

## Credit is not causation

A channel with most last-click credit can be harvesting people who would have
bought anyway; a channel with little credit can create the demand others
close. Maturity needs three tools: attribution for allocation, experiments
(holdout, geo, lift) for whether a channel causes conversions, funnel reads
for where it leaks. Do not cut or scale a channel on attribution alone when
the decision is large; propose the test.
