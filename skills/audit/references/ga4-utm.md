# GA4 setup and UTMs

## GA4

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| GA1 | Admin > Data settings > Data retention | 2 months (the default) | Explorations, funnels and paths cannot look back further; year-over-year in explorations is impossible; the setting is not retroactive | Set 14 months now | 1 |
| GA2 | Reporting attribution model and 30-day count per key event | Data-driven selected while a key event has a few hundred conversions a month (the notes cite about 400 per 30 days) | GA4 falls back to last click without telling anyone; budget and bidding signals are last click | Report the model in effect; for low volume, pick an explicit rule-based model; check current Google guidance on the threshold | 1 |
| GA3 | Key events list | One business outcome split over several key events (purchase, purchase_app, checkout_complete), each under the threshold | Fragmentation alone pushes every type into silent last click, and totals double count | One key event with a parameter for the variant | 1 |
| GA4 | Key events vs business model | Shop without purchase as a key event; lead-gen without phone calls | Every CPA is about a proxy | Map key events to the business: purchase; form plus call; subscription | 1 |
| GA5 | Micro actions marked as key events (scroll, file_download, video plays, newsletter) and the engagement rate trend around the date | Engagement rate steps up on the day a low-effort event became a key event | An engaged session is over 10 seconds, 2+ pages, or a key event, so engagement rises with no change in behaviour | Keep micro actions as plain events; annotate the change date | 1 |
| GA6 | Enhanced measurement toggles | Off, or site search off on a catalogue site | Search terms and outbound clicks are lost for good | Enable | 3 |
| GA7 | E-commerce funnel events | A step missing (view_item, add_to_cart, begin_checkout, add_shipping_info, add_payment_info, purchase) or firing at implausible ratios | The funnel cannot locate the drop-off | Implement all steps; validate in a funnel exploration | 2 |
| GA8 | Cart abandonment far outside about 60-80% | Near 0% or above 95% | Usually an event-firing problem, not a business result | Audit add_to_cart and purchase firing before acting | 1 |
| GA9 | Direct share and its trend vs the campaign calendar | Direct spikes on send or launch dates while banners, bio links or QR codes are live | Untagged campaign traffic lands in Direct and its revenue is credited to nobody | Tag every off-site link | 2 |
| GA10 | Unassigned channel | Non-trivial Unassigned sessions or revenue | Credit you paid for but cannot route | Use channel-type words in utm_medium so default grouping can classify them | 2 |
| GA11 | Exploration sampling | Segment claims from sampled explorations | Detail is unreliable | Shorter ranges or unsampled sources | 4 |
| GA12 | A trend crossing the old analytics cutover | Bounce rate step at the migration month | Different bounce definitions | Break the series | 4 |

## UTMs and campaign naming

| # | Look at | Red flag | Why it costs money | Fix | Tier |
|---|---|---|---|---|---|
| U1 | Distinct utm_campaign values, normalised (lowercase, trim, unify - and spaces to _) | More than one raw spelling per key (spring_sale, Spring_Sale, spring-sale, "spring sale ") | One campaign split over rows; revenue under-credited and reconciled by hand | One house style; a link builder; no improvisation | 1 |
| U2 | utm_medium values | Platform names in medium (facebook, google, mailchimp) or channel types in source | Breaks channel grouping and feeds Unassigned | Controlled vocabulary: medium = channel type, source = platform | 1 |
| U3 | utm_content on multi-creative campaigns | Blank | Cannot tell which creative earned revenue | Require utm_content | 3 |
| U4 | Ad platform campaign names vs the shared key | Paid campaigns named off-scheme | Paid becomes a silo in cross-channel reads | Align names to the shared key | 3 |
| U5 | Display spend vs display sessions | Spend with near-zero display sessions and a Direct lift in the same weeks | Banners untagged; display looks worthless and gets cut | Tag every banner click URL | 2 |
| U6 | Organic social links, partner links, QR codes | Plain URLs | Clicks land in Direct; print shows as an unexplained spike | Tag them; hand partners pre-tagged links | 3 |
| U7 | Campaigns with clicks but no revenue, and revenue in (not set) or unnamed buckets | Both lists non-empty | The fingerprint of tagging drift | Track "share of revenue reconciled to a named campaign" | 2 |
| U8 | AI assistant referrals | Filter on the source field when the referrer lands in medium (or the reverse); stale referrer list | AI traffic reported as zero | Contains-match on both fields; recheck quarterly | 4 |

## Decoys

Stable Direct of 10-25%; (not set) under about 1%; GA4 sessions a few percent
under ad clicks; engagement rate changes with no key-event change on that date.
