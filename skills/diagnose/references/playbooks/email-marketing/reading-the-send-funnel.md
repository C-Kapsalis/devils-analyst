---
title: Reading the send funnel
question: Where in the sent-to-clicked sequence is a campaign actually leaking
order: 2
---

Every email runs the same four-step journey: sent, delivered, opened, clicked. A 25% open rate reads like a win, but it describes one step and stays silent on the three around it. Read the campaign as one chain and ask which transition thinned: the diagnosis is then almost automatic, because each drop-off has a different cause and a different fix.

## The framework

Walk the chain in order and stop at the first transition that breaks, because a leak upstream caps everything below it:

1. **Sent → delivered.** Delivery under 95%, or bounces climbing at steady volume, is a deliverability problem: authentication, list hygiene, reputation. Nothing downstream is worth reading yet; see the deliverability playbook.
2. **Delivered → opened.** Strong delivery but a falling open trend is an attention problem: subject line, sender name, timing. The cheapest failure to carry and often the cheapest to fix.
3. **Opened → clicked.** Strong opens but few clicks is the expensive failure: you paid full freight to reach an engaged reader and gave them nothing worth acting on. Suspects: the offer, the call to action, and the match between subject and body.

Lead with the click when judging the campaign, then walk back up to find what capped it.

A worked example: a 28,000-recipient send delivers 27,000 (96.4%, gate holds), 6,750 open (25%, in line with trend), 540 click. That is an 8% click-to-open against a ~10% average and a 2.0% CTR at the floor of the 2-5% band. Read as four numbers it logs as a win; read as a chain it says spend the next hour on the offer and CTA, not the subject line that was already working.

## Metrics that matter, and their traps

- **Deliverability rate**: the gate, held above 95%. Since Google and Yahoo made SPF/DKIM/DMARC [mandatory for bulk senders](https://support.google.com/a/answer/14229414) in February 2024, a slipping delivery rate signals a reputation problem, not a formatting one.
- **Open rate**: directional only. It fires on previews and image loads, and privacy features mask opens; act on a sustained trend across campaigns, never one soft send.
- **Click rate (CTR)**: clicks / delivered, judged per send against the 2-5% band. The trap: reading it without the steps above it; a fine CTR on 60% delivery still describes a broken campaign.
- **Click-to-open rate (CTOR)**: clicks / opens, ~10% average, 14-17% in the strongest industries ([Mailchimp](https://mailchimp.com/resources/email-marketing-benchmarks/)). Isolates the body and offer from how many happened to open.
- **The transition, not the endpoint**: the drop between two adjacent steps is what localizes a leak; the trap is reading four isolated numbers and missing which one broke.

## Interview prep

**"A campaign posted a 25% open rate. Was it a good campaign?"**
A strong candidate calls the question unanswerable from one step. They ask for the full chain (delivery, then clicks), noting opens are directional at best. The real question is how far down the chain the campaign got.

**"Opens are steady but clicks dropped by half. What is your diagnosis?"**
Attention held, so the subject line and timing aren't the suspects. They look inside the message: offer relevance, CTA clarity, and whether the subject over-promised what the body delivered. They also check the segment: a broader audience dilutes clicks.

**"Delivery dropped from 98% to 91% this month. What do you check first?"**
Not the creative. Authentication records, bounce trend (hygiene), and complaint rate (reputation), in that order. They know downstream metrics are meaningless until the gate holds again.

**"Why do you read the funnel top-down instead of optimizing every step at once?"**
Because each step gates the next: a brilliant subject line cannot rescue a send that never reached the inbox. Fixing the first broken transition re-prices everything below it.
