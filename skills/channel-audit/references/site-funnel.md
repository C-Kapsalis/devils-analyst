# On-site funnel and conversion optimisation

Web analytics follows the journey in three acts: acquisition (who arrives,
from where), exploration (what they do), goal (did they convert). Always
optimise against the site's primary conversion.

## Definitions

| Term | Definition |
|---|---|
| Users | Distinct visitors (cookie-based) |
| New / returning | First visit in period vs seen before; the ratio shows acquisition vs retention balance |
| Session | Ends after 30 minutes inactive, at midnight, or on a return via a different source |
| Engaged session (GA4) | Over 10 seconds, or 2+ page views, or a key event |
| Engagement rate | engaged sessions / sessions |
| GA4 bounce rate | share of sessions not engaged (UA bounce was single-page sessions; not comparable) |
| Pageviews vs unique pageviews | every load vs sessions with the page at least once |
| Purchase conversion rate | purchases / sessions |

UA bounce benchmarks (ecommerce): 40% or lower good, 40-70% average, above 70%
high. Ecommerce conversion averages about 2.6% (Walmart about 5%; Amazon
non-Prime about 10%, Prime members far higher), so loyalty programmes move
the benchmark.

## Primary conversion by site type

Ecommerce: purchases. Lead generation: calls and form submissions. Media (ad
model): pageviews, time, visit duration. Media (subscription): paid sign-ups.
Revenue levers after conversion: AOV (upsell, cross-sell, bundles,
free-shipping thresholds, subscriptions, personalised recommendations).

## Traffic sources

Direct (typed URL, bookmarks, apps; strong brand), search (paid and organic),
referral (organic social, backlinks, earned media; paid display, social ads,
influencers, sponsored content). Not all visits are equal: judge sources on
engagement and conversion, not volume. Rising organic often lifts referral,
social and direct as knock-on effects.

## Funnel read

Steps: product view, add to cart, begin checkout, shipping, payment,
purchase. Cart abandonment benchmark about 70%; 60% would be very good.

1. Compute step-to-step completion; the largest absolute loss of would-be
   buyers is the first target.
2. Check whether the funnel is open (users can enter mid-way) or closed;
   step completion is not journey success.
3. Cut by device and channel before concluding (a mix shift moves blended
   rates; see `evidence-check` on Simpson's paradox).
4. Map causes to the step: hidden costs (shipping, tax), long or repeated
   forms, unexpected delivery time, security doubts, no guest checkout,
   complicated flow, missing payment method.
5. Every page fix is a hypothesis until tested (`evidence-check` for test
   reading).

CRO levers: landing page clarity, ad-to-page message match, speed, form and
checkout friction, trust signals, offer framing. More traffic is not a better
rate; landing-page clicks are not business value.

## Channel blend

Awareness: social, display, content. Consideration: search ads, retargeting,
email. Conversion: landing pages, checkout, remarketing to known contacts.
