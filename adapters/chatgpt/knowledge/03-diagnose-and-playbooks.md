# Skill: diagnose

---
name: diagnose
description: >-
  Turn a marketing number that moved into a diagnosis a consultant would sign, covering
  the likely cause, the evidence for and against it, the next action and how to verify it.
  Uses the Cohortica funnel diagnostic (acquisition, activation, revenue, retention, each
  declining, flat or inefficient), the brand strategy diagnostic, and 59 practitioner
  playbooks across email, paid search, Performance Max, SEO, GA4, paid and organic social,
  customer analytics, attribution, GEO and product. Use after a dashboard or the whats-
  changed skill finds a real movement, or when the user asks why performance is down, what
  to do next, or for recommendations.
---

# diagnose

A dashboard says *what* moved. A diagnosis says *why it probably moved, what to
check to be sure, and what to do*. This skill turns the first into the second
without inventing causes the data cannot support.

## 1. Start from a measured movement

Only diagnose a change that survived the `whats-changed` noise screen, and know
its driver: "revenue down 12%, driven by conversion rate (-15%), concentrated
in paid social". Without a driver, you are guessing which journey broke.

## 2. Place it on the funnel

Map the driver to one journey and one state in
section "File: diagnose/references/funnel-diagnostic.md" in 03-diagnose-and-playbooks.md:

| The driver that moved | Journey |
|---|---|
| sessions, new users, reach, impressions, branded search | Acquisition |
| engagement, add-to-cart, checkout start, lead form completion, CVR | Activation |
| AOV, revenue per session, margin, ROAS, CAC | Revenue |
| repeat rate, time between orders, churn, unsubscribes, list erosion | Retention |

| Pattern over the comparison | State |
|---|---|
| clear fall | Declining |
| no movement while effort or spend rose | Flat |
| volume holds but cost per outcome rises, or quality falls | Inefficient |

Read only that journey's section of the file, not the whole file.

The diagnostic is written for e-commerce (stores, collections, orders). For B2B
or lead generation, read *order* as qualified lead or opportunity, *AOV* as
average deal size, and *repeat purchase* as expansion or renewal, and say you
made that mapping.

## 3. Test the signals against the data you have

Each state lists signals in four kinds: *observed*, *diagnostic*, *outcome*,
*context*. For each signal, mark it:

- **confirmed**: you checked it in the data (cite the number);
- **contradicted**: you checked it and it is not so (cite the number);
- **unchecked**: the data to check it is not connected. Say which source would
  check it ("needs Search Console branded queries").

**Market or us, before any cause on our side.** For any acquisition or
volume drop, first ask whether the market moved: competitors' estimates,
category or non-brand search volume, impressions at unchanged position and
click-through, the same weeks last year. If the comparison set fell by about
the same share and your share of it held, the leading hypothesis is lower
demand in the category (seasonal or market-wide), not a fault in your SEO,
ads or site. Say so first, and verify it with the same period last year or
a category demand source. Check tracking and site changes first only when
your series moved and the comparison set did not; when both moved together,
a measurement fault on your side cannot explain the competitors' drop, so it
is a secondary check, not the lead.

A diagnosis with only unchecked signals is a hypothesis list, and must be
labelled so. Pull the data for the cheapest unchecked signals before writing
the diagnosis, when a connector for them is available.

## 4. Go deeper with the playbook

section "File: diagnose/references/playbook-index.md" in 03-diagnose-and-playbooks.md lists 59 playbooks
by discipline with the question each answers. Open the one that matches the
driver (for a paid search CPA rise, `paid-search/conversions-cpa-and-return.md`;
for an email click-to-order fall, `email-marketing/click-to-revenue.md`). Use its
*framework* and *metrics and their traps* sections; ignore its interview-prep
section. Cite the playbook by title when you use its reasoning.

For brand questions (positioning, architecture, equity, messaging, repositioning)
use section "File: diagnose/references/brand-diagnostic.md" in 03-diagnose-and-playbooks.md the same way.

## 5. Write the diagnosis

Write by the `marketing-dashboard` skill's `references/writing.md`: answer first, one point per paragraph, plain words.

Use this shape for each finding (at most three per report; rank by money at
stake):

```
**[Journey] is [state]: [the measured movement, one sentence with numbers].**
Likely cause: [cause] ([confirmed / partly confirmed / hypothesis]).
Evidence: [confirmed signals with numbers]; against: [contradicted signals].
Do next: [one or two actions from the state's action list, made specific to this data].
Verify in: [the source and the exact cut that would confirm or kill the cause].
```

Rules:

- **Never state a cause as fact unless a confirmed signal shows it.** "Likely",
  plus the evidence, is the honest default.
- **Specific beats generic.** "Shift 20% of Meta prospecting budget to the two
  ad sets with CPA under $40" beats "optimize budget allocation".
- **One action per finding should be doable this week.**
- Compare the account with its own history first. A benchmark from a playbook
  (for example "deliverability above 95%", "complaints past 0.1% is a
  warning") may be cited as a labelled heuristic with the playbook it came
  from, never as a target and never as the only evidence.

## 6. In a dashboard

Add a "What to do" panel under the KPIs: the findings in the shape above,
collapsed to the bold first line plus "Do next", and a link or toggle to the
evidence. Color the state (declining, flat, inefficient) with one muted tone
each; reserve red for findings with money at stake.

## Adversary pass

Every move above has a challenger. Run the attack, settle it with the check, and act on a failure before moving on.

| Move | Adversary asks | Check that settles it | If it fails |
|---|---|---|---|
| Start from a movement | "Did this movement survive the noise screen and have a driver?" | whats-changed output with a driver | go back and decompose first |
| Place it on the funnel | "Could the same pattern sit in another journey (a tracking change looks like an activation drop), or outside the business (the whole category moved)?" | check tagging and data changes for the period; compare with competitors, category demand and last year | rule out measurement before behaviour when only your series moved; lead with demand when the market moved with you |
| Name the cause | "What rival cause produces the same pattern?" | for each rival, the data that rules it out | keep the survivors, labelled hypotheses |
| Recommend | "What does it cost if this is wrong, and what would the CFO ask?" | downside sized; a test or metric that verifies | add a test, or shrink the action |
| Rank findings | "Is the top finding the one with the most money at stake?" | findings ordered by value at stake | reorder |

**Score and probe before handing over.** First the gate: every check in the
table above passed; if one did not, fix it before scoring. Then score the
draft 0-100 on four dimensions: clarity (unambiguous, easy to follow),
relevance (answers the question asked, for this reader), depth (explains the
why with numbers, not only the what) and insightfulness (says something the
reader did not already know, and what to do about it). If any score is below
80, write the probe question that would raise it, answer it from the data,
revise, and score again (two loops at most). The question and the decision belong to the person asking: when either
is unclear, ask instead of assuming.

---

## File: diagnose/references/brand-diagnostic.md

# Brand strategy diagnostic

Five phases of brand strategy (positioning, architecture, equity, communication, evolution), each with diagnosable states. Built on 3C analysis, points of parity and difference, and Keller's CBBE. Source: the Cohortica Brand Strategy Diagnostic (cohortica.studio/brand).

Contents: [Brand Positioning](#positioning) · [Brand Architecture](#architecture) · [Brand Equity](#equity) · [Brand Communication](#communication) · [Brand Evolution](#evolution)

<a id="positioning"></a>
## Brand Positioning: Mental Real Estate + Differentiation + Value Claim

**Question:** How clearly does your brand occupy a distinctive, valuable position in the minds of your target customers, relative to alternatives?

**How to read it:** Focus on whether you have a clear positioning statement, whether your POD is truly distinctive (not just 'better'), whether your claim ladders up from features to values, and whether the 3C requirements are met.

**Method:** positioning

### No positioning: the brand is undefined or generic

*The brand has no articulated position. It competes on price, availability, or founder hustle rather than a clear value claim.*

The brand exists as a product, not a position. There is no documented positioning statement, no clear POD, and no consistent story across touchpoints. The team cannot articulate in one sentence why a customer should choose them over alternatives.

**Signals**

- *Observed:*
    - No documented positioning statement exists.
    - Team members describe the brand differently when asked.
    - Marketing messages change frequently with no consistent theme.
    - Competing primarily on price or promotions.
- *Diagnostic:*
    - Target market is defined too broadly ('everyone who needs X').
    - Value claims are feature-level, not benefit- or value-level.
    - No clear competitive frame of reference; unclear what category the brand belongs to.
    - No reasons to believe are articulated beyond 'our product is good'.
- *Outcome:*
    - Low brand recall and recognition.
    - Difficulty justifying premium pricing.
    - Marketing spend generates traffic but not brand equity.
    - High customer acquisition cost with low repeat rates.
- *Context:*
    - Common in early-stage brands that grew on product-market fit without strategic branding.
    - Also appears when a brand has been managed by execution-focused teams without strategic oversight.

**Actions**

1. Define your target market with behavioral and needs-based specificity, not just demographics.
1. Identify your competitive frame: what alternatives do customers consider when deciding?
1. Ladder your strongest product feature up to a benefit and then to a personal value.
1. Write a positioning statement using the template: For [target], [brand] is the only [frame] that [POD] because [RTB].
1. Validate the statement against the 3C framework: Consumer (3R's), Competitive (3D's), Company (3F's).

**Verify in**

- **Internal Alignment Test:** Ask 5 team members to describe the brand in one sentence. If answers diverge, positioning is absent.
- **Customer Perception Check:** Survey or interview 10 customers: Why did you choose us? What would you tell a friend? What is different about us?
- **Competitive Mapping:** List the top 5 alternatives your customers considered. Map attributes. Where are you genuinely different?

**Playbook BP-01: Build Your First Positioning Statement.** Use the 3C analysis to develop a positioning statement grounded in consumer relevance, competitive distinctiveness, and company capability.

- [ ] Complete consumer needs mapping (jobs-to-be-done)
- [ ] Map competitive landscape using perceptual mapping
- [ ] Identify your strongest POD and validate it is truly distinctive
- [ ] Draft positioning statement and test with target customers

### Positioning exists but is NOT resonating with the market

*A positioning statement or brand story exists, but it is not translating into differentiation, preference, or premium pricing.*

The brand has attempted positioning, but the claim isn't landing. This could be because the POD is feature-level (easy to copy), the value claim does not resonate emotionally, the competitive frame is wrong, or the reasons to believe are insufficient. The positioning statement exists on paper but not in customers' minds.

**Signals**

- *Observed:*
    - Brand awareness exists but preference is low, considered but not chosen.
    - Customers describe the brand in generic terms ('they are fine,' 'similar to X').
    - Marketing generates engagement but not conversion or loyalty.
    - Price sensitivity is high despite positioning claims.
- *Diagnostic:*
    - POD is feature-based rather than benefit- or value-based.
    - Positioning claim is 'best' rather than 'only': vertical instead of horizontal differentiation.
    - Competitive frame may be wrong; brand is being compared to the wrong alternatives.
    - RTBs are vague or unverifiable.
- *Outcome:*
    - Stuck in the middle of the market; neither premium nor value leader.
    - Marketing ROI is flat despite spend increases.
    - Team struggles to create compelling content because the strategic foundation is weak.
- *Context:*
    - Often happens when the team develops positioning internally without customer validation.
    - Also common when the market has shifted but positioning has not been updated.

**Actions**

1. Test your current POD: is it 'only' territory or 'best' territory? If 'best,' you need to find horizontal differentiation.
1. Ladder your value claim UP: are you stuck at feature level? Move to benefit, then to value level.
1. Validate resonance: does your claim address a job-to-be-done your target actually cares about?
1. Check your competitive frame: are you being compared to the right alternatives? Consider breakaway positioning.
1. Strengthen RTBs: replace vague claims with specific, verifiable evidence.

**Verify in**

- **Resonance Test:** Show your positioning claim to 10 target customers. Rate: relevant? meaningful? believable? If <7/10 on any, the claim needs work.
- **Distinctiveness Audit:** Can any competitor credibly make your same claim? If yes, your POD is not distinctive enough.
- **Laddering Analysis:** Map your current claim on the feature → benefit → value ladder. Where does it sit? Can it go higher?

**Playbook BP-02: Strengthen Your Positioning Claim.** Move from 'best' to 'only' positioning by finding horizontal differentiation and laddering claims to value level.

- [ ] Audit competitive claims to find unclaimed territory
- [ ] Conduct laddering interviews with customers to find value-level claims
- [ ] Rebuild RTBs with specific, verifiable evidence
- [ ] Test revised positioning with target segment

### Brand needs REPOSITIONING: market or brand has shifted

*The current position was once effective but no longer fits the market, the competitive landscape, or the brand's evolution.*

Markets change, competitors move, and brands evolve. The current positioning may have been right at launch but is now outdated, outflanked, or misaligned. Repositioning is needed but must be approached carefully, because identity brands tie customers' self-concept to the brand.

**Signals**

- *Observed:*
    - Market share declining despite stable or increased investment.
    - New competitors have claimed similar or adjacent positions.
    - Customer demographics or needs have shifted since positioning was set.
    - The brand's product/service offering has evolved beyond original positioning.
- *Diagnostic:*
    - Perceptual map shows brand position overlapping with competitors.
    - Original target segment is shrinking or changing values.
    - Brand associations in customer research do not match intended positioning.
    - Internal team feels positioning is 'stale' or does not represent what the brand does now.
- *Outcome:*
    - Acquisition efficiency declining.
    - Premium pricing power eroding.
    - Best talent harder to attract.
    - Growth stalling despite product improvements.
- *Context:*
    - Category-wide shift (e.g., sustainability becoming table stakes).
    - Major competitor entered or repositioned.
    - Brand itself expanded into new categories or markets.

**Actions**

1. Conduct a current-state brand audit: where does the brand actually sit in customers' minds today?
1. Map the repositioning using the 4 components: change target? change value claim? change evidence? change competitive frame?
1. Assess identity risk: is this an identity brand? If so, take evolutionary (not revolutionary) approach.
1. Consider brand architecture solutions: can a sub-brand or endorser brand handle the new position without disrupting core?
1. Plan communication transition: gradual shift in messaging, not overnight change.

**Verify in**

- **Current Perceptual Map:** Where does the brand sit today vs competitors? Where does it need to move?
- **Identity Risk Assessment:** How central is this brand to customers' identity? High ego involvement = narrow latitude of acceptance for change.
- **Social Judgment Theory Check:** Will the new positioning fall within the target's latitude of acceptance? Or will it be rejected?

**Playbook BP-03: Repositioning Strategy.** Develop a repositioning plan that moves the brand to a more valuable position while managing customer and market risk.

- [ ] Audit current brand associations vs intended
- [ ] Define target position on perceptual map
- [ ] Choose repositioning lever (target, value, evidence, or frame)
- [ ] For identity brands: design evolutionary transition path
- [ ] Consider brand architecture solutions for expanded positioning

<a id="architecture"></a>
## Brand Architecture: Portfolio Structure + Extensions + Brand Relationships

**Question:** How well does your brand portfolio structure support your business strategy, and does each brand have a clear, non-overlapping role?

**How to read it:** Assess whether you need a house of brands, branded house, or hybrid. Check for brand overlap, cannibalization, and whether extensions make strategic sense.

**Method:** architecture

### Single brand: need to decide on expansion approach

*You have one brand and are considering extending into new products, categories, or markets.*

The brand has reached a point where expansion is needed. The key decision: extend the existing brand (branded house / umbrella) or create new brands (house of brands). This depends on brand permission, target overlap, and economic efficiency. Getting this wrong creates brand erosion or wasted investment.

**Signals**

- *Observed:*
    - Revenue growth from core product line is flattening.
    - Customers are asking for adjacent products or services.
    - New market segments are attractive but may not fit current brand image.
    - Competitors are expanding into your adjacent space.
- *Diagnostic:*
    - Current brand has high equity and broad permission (range brand potential).
    - OR current brand is narrowly defined and extension would create cognitive dissonance.
    - Target segments for expansion differ substantially from current core.
    - Price points of expansion products differ substantially from core.
- *Outcome:*
    - Need clear go/no-go framework for extensions.
    - Need to decide: umbrella vs new brand vs sub-brand.
    - Need to protect core brand equity during expansion.
- *Context:*
    - Consider Toyota → Lexus model: when brand permission ceiling is hit, create new brand.
    - Consider BMW model: when brand permission is broad enough, extend within branded house.
    - Consider P&G model: when targeting fundamentally different segments, house of brands.

**Actions**

1. Assess brand permission: what product categories can your brand credibly enter?
1. Map target segment overlap: do expansion targets differ enough to warrant separate brands?
1. Calculate economics: cost of building new brand vs cost of potential brand erosion from over-extension.
1. Apply the range brand test: is your brand purpose statement broad enough to cover expansion?
1. If expanding: decide between line extension (same category) vs category extension (new category).

**Verify in**

- **Brand Permission Survey:** Test with customers: 'How likely would you be to buy [product X] from [your brand]?' If <6/10, brand permission is limited.
- **Brand Purpose Breadth:** Is your brand purpose broad enough to be a range brand? Or is it anchored to a specific product?
- **Economic Analysis:** Compare: cost of new brand launch (~$1-5M+) vs risk of equity dilution from extension.

**Playbook BA-01: Brand Extension Decision Framework.** Determine whether to extend, sub-brand, or create new brand using brand permission, economic, and strategic analysis.

- [ ] Assess brand permission across potential categories
- [ ] Map target segment overlap
- [ ] Calculate extension economics vs new brand economics
- [ ] If extending: choose line vs category extension
- [ ] Design brand architecture diagram for next 3 years

### Multiple brands: need to structure and clarify roles

*You operate multiple brands but the portfolio lacks clear structure, roles are overlapping, or efficiency is low.*

Multiple brands exist but without clear portfolio logic. Brands may overlap in targeting, cannibalize each other, or lack sufficient investment. The portfolio needs rationalization.

**Signals**

- *Observed:*
    - Multiple brands competing for same customers.
    - Unclear to team which brand serves which segment.
    - Marketing budget spread thin across too many brands.
- *Diagnostic:*
    - No documented brand architecture decision.
    - Brand roles not defined (flagship, flanker, fighter, cash cow).
- *Outcome:*
    - Inefficient marketing spend.
    - Customer confusion.
    - Weak equity across all brands.
- *Context:*
    - Common after acquisitions or organic growth without strategic portfolio planning.

**Actions**

1. Map all brands on a single perceptual map to identify overlap.
1. Define role for each brand: flagship, flanker, fighter, extension, or candidate for pruning.
1. Allocate resources based on role: flagship gets most investment.
1. Consider consolidation: can 2+ brands be merged without losing customers?
1. Document the portfolio architecture and share across organization.

**Verify in**

- **Portfolio Overlap Analysis:** Map all brands by target segment and positioning claim. Where do they overlap?
- **Brand Role Clarity:** Can each team member name the role of each brand in the portfolio?

**Playbook BA-02: Portfolio Rationalization.** Clarify roles, eliminate overlap, and optimize resource allocation across brand portfolio.

- [ ] Map portfolio on perceptual grid
- [ ] Assign roles to each brand
- [ ] Identify pruning candidates
- [ ] Reallocate investment to highest-ROI brands

### Architecture does not match market reality

*The brand structure was designed for a market that has changed, or the structure never matched the strategy.*

Brand architecture decisions made years ago no longer serve current business strategy or market reality. Extensions that made sense now create confusion. Sub-brands that were differentiated now overlap. The architecture itself needs restructuring.

**Signals**

- *Observed:*
    - Customers confuse brands within the portfolio.
    - Channel partners struggle to explain brand differences.
    - Some brands in portfolio are under-invested but too risky to kill.
- *Diagnostic:*
    - Architecture was inherited, not designed.
    - Market has shifted; segments that were separate now overlap.
    - Brand purpose statements across portfolio have converged.
- *Outcome:*
    - Inefficient go-to-market.
    - Difficulty launching new products; unclear which brand they belong to.
    - Talent spread across too many brand teams.
- *Context:*
    - Post-acquisition integration challenges.
    - Market consolidation making previous segmentation obsolete.

**Actions**

1. Conduct full brand architecture audit: map every brand, sub-brand, and endorsed product.
1. Compare architecture to current market segmentation: where is the mismatch?
1. Design target-state architecture based on current strategy.
1. Plan migration path: which brands merge, which get repositioned, which get retired.
1. Communicate changes internally before external rollout.

**Verify in**

- **Architecture-Strategy Fit:** Does the current brand structure support the business strategy for the next 3 years?
- **Customer Mental Model:** How do customers actually organize your brands in their minds? Does it match your intended architecture?

**Playbook BA-03: Architecture Redesign.** Restructure brand portfolio to align with current market reality and business strategy.

- [ ] Audit current state architecture
- [ ] Map to current market segmentation
- [ ] Design target state
- [ ] Plan migration timeline
- [ ] Manage internal and external communication

<a id="equity"></a>
## Brand Equity: Awareness + Loyalty + Quality + Associations + Assets

**Question:** Where does your brand sit on the equity spectrum, from basic awareness to deep loyalty, and which dimension needs the most attention?

**How to read it:** Use Keller's CBBE pyramid. Start from bottom: is salience strong? Is meaning clear? Are responses positive? Is resonance deep? Identify which level is the bottleneck.

**Method:** equity

### Low awareness: brand is invisible to target market

*Target customers do not know the brand exists or cannot recall it when the need arises.*

The brand fails at Level 1 of Keller's CBBE pyramid (Salience). Without awareness, nothing else matters; you cannot build associations, quality perceptions, or loyalty for a brand people do not know about.

**Signals**

- *Observed:*
    - Low unaided brand recall in target market.
    - High dependence on paid channels; no organic demand.
    - Branded search volume is minimal.
- *Diagnostic:*
    - Insufficient marketing investment for category.
    - Touchpoints too few or too narrow.
    - Brand elements (name, logo) not distinctive enough to be memorable.
- *Outcome:*
    - Cannot enter consideration set.
    - No halo effect for new products.
    - High CAC because every customer must be acquired from scratch.
- *Context:*
    - Common for new brands or brands entering new markets.
    - Also happens when a brand has been under-invested for extended periods.

**Actions**

1. Audit current mental availability: how many category entry points does your brand own?
1. Increase brand element distinctiveness: is the name memorable? Is the visual identity recognizable?
1. Build reach before frequency; prioritize breadth of audience exposure.
1. Invest in consistent brand assets across all touchpoints.
1. Use content and thought leadership to build organic awareness.

**Verify in**

- **Awareness Benchmarking:** Measure unaided and aided recall vs top 3 competitors. What is the gap?
- **Brand Element Audit:** Are your name, logo, colors, and tagline distinctive enough to be remembered after one exposure?

**Playbook BE-01: Build Brand Salience.** Establish mental availability through distinctive brand assets and broad reach.

- [ ] Strengthen brand elements for distinctiveness
- [ ] Identify and own category entry points
- [ ] Prioritize reach over frequency in media
- [ ] Consistent brand asset usage across all channels

### Awareness exists but loyalty is absent

*People know the brand but do not prefer it or repeat-purchase consistently.*

The brand has Level 1 (Salience) but is stuck at Level 2-3. Meaning is unclear or responses are neutral. Customers consider the brand but do not choose it, or choose it once but not again.

**Signals**

- *Observed:*
    - Decent awareness but low preference scores.
    - Trial rate is acceptable but repeat purchase rate is weak.
    - Customers can name the brand but cannot articulate what makes it different.
- *Diagnostic:*
    - Brand meaning (performance + imagery) is underdeveloped.
    - Associations are generic, not distinctive.
    - Customer experience does not exceed expectations enough to build commitment.
- *Outcome:*
    - Stuck in the 'parity zone'; interchangeable with competitors.
    - Vulnerable to price competition.
    - Cannot command premium.
- *Context:*
    - Common in categories where functional parity is high.
    - Also happens when brand communication is inconsistent.

**Actions**

1. Strengthen brand associations through consistent, distinctive communication.
1. Focus on building quality perception through experience delivery, not just messaging.
1. Develop emotional connections; move beyond functional to relationship and symbolic value.
1. Create loyalty mechanisms: community, exclusivity, recognition.
1. Measure and optimize the full Keller pyramid; identify which level is the bottleneck.

**Verify in**

- **Keller Pyramid Audit:** Rate your brand 1-10 on each level: Salience, Meaning, Response, Resonance. Where is the drop-off?
- **Association Distinctiveness:** What comes to mind when customers think of your brand? Is it distinctive from competitors?

**Playbook BE-02: Build Brand Preference.** Move from awareness to active preference by strengthening meaning and building emotional connections.

- [ ] Audit associations vs competitors
- [ ] Develop distinctive brand personality
- [ ] Build 2-3 strong, unique associations
- [ ] Create memorable brand experiences
- [ ] Implement loyalty/community program

### Brand loyalty is ERODING: equity under threat

*The brand once had strong loyalty but it is weakening. Repeat rates are down, NPS is declining, or customers are switching.*

Something is breaking the brand-customer relationship. This could be product quality decline, a trust violation, competitive disruption, or cultural irrelevance. The brand is losing the top of Keller's pyramid (Resonance) and potentially the levels below it.

**Signals**

- *Observed:*
    - NPS or satisfaction scores declining.
    - Repeat purchase rates falling.
    - Negative sentiment increasing in reviews or social.
    - Share of wallet decreasing among existing customers.
- *Diagnostic:*
    - Product or service quality may have slipped.
    - Brand promise is no longer being delivered consistently.
    - Competitor has captured attention with better execution.
    - Brand feels 'dated' or misaligned with evolving customer values.
- *Outcome:*
    - Customer lifetime value declining.
    - Word-of-mouth turning negative.
    - Brand value (financial) at risk.
    - Best customers leaving first (canary in the coal mine).
- *Context:*
    - Often happens during rapid scaling when quality controls loosen.
    - Also triggered by leadership changes, cost-cutting, or neglect.

**Actions**

1. Diagnose the root cause: is this a product problem, a communication problem, or a relevance problem?
1. Read support tickets, reviews, and churn surveys: what are customers actually saying?
1. Assess whether the brand promise is still being delivered at every touchpoint (feasibility check).
1. Check cultural relevance: has the market moved and the brand stayed still?
1. Prioritize fixing the root cause before investing in win-back marketing.

**Verify in**

- **Churn Analysis:** Why are the best customers leaving? Segment churn by customer value and tenure.
- **Promise vs Delivery Audit:** Walk the full customer journey. Where does the experience fail to deliver the brand promise?
- **Competitive Comparison:** What are switching customers going to? What does the alternative offer that you do not?

**Playbook BE-03: Recover Brand Loyalty.** Diagnose and fix the root cause of loyalty erosion before it becomes irreversible.

- [ ] Identify root cause (product, service, relevance, or trust)
- [ ] Fix delivery gaps at key touchpoints
- [ ] Re-engage highest-value at-risk customers
- [ ] Rebuild brand associations through consistent positive experiences
- [ ] Monitor recovery metrics weekly

<a id="communication"></a>
## Brand Communication: Message Consistency + Resonance + Channel Strategy

**Question:** Is your brand communication consistent, resonant, and reaching the right people through the right channels?

**How to read it:** Check message consistency across touchpoints, whether communication ladders up from features to values, and whether channels match where your target market actually is.

**Method:** attitudeManagement

### Inconsistent messaging across touchpoints

*The brand says different things on different channels, or different team members communicate different brand stories.*

The brand lacks a consistent communication framework. Without a positioning statement guiding all messaging, each touchpoint tells a different story.

**Signals**

- *Observed:*
    - Website, social, ads, and sales pitch tell different stories.
    - Visual identity is inconsistent across channels.
    - Tone of voice varies from formal to casual unpredictably.
- *Diagnostic:*
    - No documented brand guidelines or positioning statement.
    - Multiple team members or agencies creating content without coordination.
    - No annual brand plan governing communication.
- *Outcome:*
    - Confused brand associations in customer minds.
    - Weak brand recall despite high touchpoint frequency.
    - Marketing spend wasted; impressions do not compound into equity.
- *Context:*
    - Almost universal in brands scaling from founder-led to team-led communication.

**Actions**

1. Document a brand communication framework anchored in the positioning statement.
1. Create a message hierarchy: primary claim, supporting messages, proof points.
1. Develop brand guidelines: voice, tone, visual standards.
1. Audit all active touchpoints for consistency.
1. Assign brand guardian role to ensure ongoing alignment.

**Verify in**

- **Touchpoint Consistency Audit:** Screenshot every brand touchpoint. Lay them side by side. Does it look and sound like one brand?

**Playbook BC-01: Build Communication Consistency.** Create a brand communication framework that ensures every touchpoint tells the same story.

- [ ] Derive messaging from positioning statement
- [ ] Create message hierarchy and brand guidelines
- [ ] Audit all touchpoints
- [ ] Train team on guidelines
- [ ] Establish review process for all external communications

### Message not resonating: not driving preference

*Communications are consistent but aren't creating the emotional connection or behavioral change needed.*

The brand is communicating, but at the wrong level. Claims may be feature-based when they need to be value-based. Or the message is rational when the category demands emotional resonance.

**Signals**

- *Observed:*
    - High impression/reach but low engagement.
    - Content gets seen but does not get shared or commented on.
    - Aided awareness is decent but preference is low.
- *Diagnostic:*
    - Claims stuck at feature level; not laddered to benefits/values.
    - Rational messaging in an emotional category (or vice versa).
    - Message does not connect to customer's cultural context or identity.
- *Outcome:*
    - Marketing spend generates awareness but not preference.
    - Brand is 'known but not loved.'
    - Competitors with better stories win despite similar products.
- *Context:*
    - Often seen in B2B or technical brands that over-index on features.
    - Also common when brand was built by product people, not brand strategists.

**Actions**

1. Apply laddering: move claims from feature → benefit → value level.
1. Assess category: does it require rational (USP) or emotional positioning?
1. Research customer cultural context: what tensions can the brand help bridge?
1. Test message variants at different ladder levels with target segment.
1. Consider culture brand opportunity: can you bridge an actual vs desired state?

**Verify in**

- **Message Level Audit:** Categorize your top 10 marketing messages: feature, benefit, or value level? Where is the mix?
- **Emotional Response Test:** Show communications to target customers. Measure emotional response, not just comprehension.

**Playbook BC-02: Build Message Resonance.** Move brand communication from informing to inspiring by laddering claims and connecting to customer values.

- [ ] Map current claims on feature/benefit/value ladder
- [ ] Conduct laddering interviews with target customers
- [ ] Develop value-level messaging
- [ ] Test rational vs emotional balance for your category
- [ ] Explore culture brand opportunity

### Right message, wrong channels or wrong audience

*Brand communication may be strong but it is not reaching the target segment effectively.*

The message and positioning may be sound, but distribution of that message is misaligned. Either the channels do not reach the target, the media weight is insufficient, or the message is reaching the wrong people.

**Signals**

- *Observed:*
    - Strong engagement from non-target audiences.
    - High impressions but low conversion from target segment.
    - Brand tracked in wrong competitive set by customers.
- *Diagnostic:*
    - Media plan not aligned with target media consumption.
    - Organic channels attracting wrong audience.
    - Paid targeting too broad or mis-segmented.
- *Outcome:*
    - Marketing efficiency is low despite good creative.
    - Brand associations forming in wrong segment.
    - Growth stalls because right people aren't seeing the brand.
- *Context:*
    - Common when media strategy is inherited rather than derived from positioning.
    - Also happens when a brand repositions but media strategy does not follow.

**Actions**

1. Map your target segment's actual media consumption and information sources.
1. Audit current channel performance by target segment overlap.
1. Reallocate budget toward channels with highest target-segment concentration.
1. Consider whether organic content strategy attracts the right vs any audience.
1. Align paid, owned, and earned media around the same positioning.

**Verify in**

- **Target Segment Reach Analysis:** What % of your marketing impressions actually reach your defined target market?
- **Channel-Positioning Alignment:** Does each channel reinforce your positioning? Or do some channels attract a different audience?

**Playbook BC-03: Realign Channel Strategy.** Ensure brand communication reaches the right people through the right channels.

- [ ] Map target segment media consumption
- [ ] Audit current channel performance vs target overlap
- [ ] Reallocate budget to highest-overlap channels
- [ ] Align organic content strategy to attract target segment
- [ ] Set up channel-level tracking by target segment metrics

<a id="evolution"></a>
## Brand Evolution: Extensions + Growth + Lifecycle Management

**Question:** Is your brand strategy evolving with the market, or standing still while the market moves around it?

**How to read it:** Assess brand lifecycle stage, extension opportunities, and whether repositioning or portfolio pruning is needed. Use maturity and decline stage frameworks.

**Method:** evolution

### Growth opportunity: brand equity supports extension

*Brand has strong equity and market opportunity for extension into new products, categories, or markets.*

The brand has built sufficient equity (awareness, loyalty, perceived quality) to leverage into adjacent opportunities. The key question is: which extensions will build equity further, and which will dilute it?

**Signals**

- *Observed:*
    - Strong brand equity metrics.
    - Customers request adjacent products/services.
    - Category growth opportunity visible.
    - Brand purpose is broad enough for range brand.
- *Diagnostic:*
    - Brand permission testing shows positive reception.
    - Core equity is strong enough to survive extension risk.
    - Economic case for extension is sound.
- *Outcome:*
    - Revenue growth potential from new products under existing brand.
    - Opportunity to strengthen brand associations through breadth.
    - Competitive defensive value from occupying adjacent positions.
- *Context:*
    - Best timing: when core business is healthy and brand equity is high.
    - Riskiest: when extending to compensate for core business weakness.

**Actions**

1. Test brand permission in target extension categories.
1. Choose: line extension (same category) vs category extension (new category) vs market development (new geography).
1. Assess cannibalization risk: will extension steal from core?
1. Define success metrics for extension before launch.
1. Protect core equity: do not let extension distract from primary brand promise.

**Verify in**

- **Brand Permission Test:** Survey target: 'If [brand] offered [extension product], would you consider it?'
- **Cannibalization Analysis:** Will the extension steal from core business, or is it truly incremental?

**Playbook BV-01: Strategic Extension Plan.** Develop a brand extension strategy that builds equity while managing dilution risk.

- [ ] Test brand permission
- [ ] Choose extension type
- [ ] Assess cannibalization
- [ ] Define success metrics
- [ ] Plan launch and protect core

### Brand is stagnating: growth has stalled

*The brand has reached maturity. Growth is flat despite effort. Needs repositioning, innovation, or market development.*

The brand has hit its ceiling in the current position. The market may be saturated, the positioning may be stale, or competitors may have caught up. The brand needs evolution, not just execution.

**Signals**

- *Observed:*
    - Revenue flat for 2+ consecutive quarters.
    - Market share stable but not growing.
    - New customer acquisition is declining.
    - Brand feels 'established' but not 'exciting.'
- *Diagnostic:*
    - Product lifecycle at maturity stage.
    - Positioning has not been refreshed in 3+ years.
    - Competitors have matched or exceeded your POD.
    - Target segment may have evolved.
- *Outcome:*
    - Risk of slow decline if not addressed.
    - Team morale affected by flat growth.
    - Investor/stakeholder pressure building.
- *Context:*
    - Natural lifecycle stage; all brands face this.
    - The question is whether to revitalize, extend, or begin managed decline.

**Actions**

1. Determine lifecycle stage: is this true maturity or premature stagnation?
1. Assess repositioning opportunity: can the brand move to a more valuable position?
1. Evaluate extension opportunities: can growth come from new products or markets?
1. Consider fighter brand strategy: is a lower-priced flanker needed?
1. Explore market development: are there geographies or segments not yet served?

**Verify in**

- **Lifecycle Stage Assessment:** Is this maturity (natural) or stagnation (fixable)? What would growth require?
- **Repositioning Viability:** Is there a more valuable position available? Can the brand credibly claim it?

**Playbook BV-02: Brand Revitalization.** Move the brand from stagnation back to growth through repositioning, extension, or market development.

- [ ] Assess true lifecycle stage
- [ ] Identify highest-impact growth lever
- [ ] Develop revitalization plan
- [ ] Set timeline and investment requirements
- [ ] Monitor early indicators weekly

### Brand is DECLINING: strategic decision needed

*The brand is losing relevance, share, and value. A strategic decision is needed: reinvest, milk, or divest.*

The brand is in decline. This may be due to category decline, competitive displacement, or brand erosion. The strategic choice is between reinvestment (if there is a viable path back), milking (minimize costs, maximize remaining cash flow), or divestiture (sell the brand assets).

**Signals**

- *Observed:*
    - Revenue declining year-over-year.
    - Customer base shrinking.
    - Brand recall declining.
    - Best talent leaving the brand team.
- *Diagnostic:*
    - Category itself may be declining.
    - Brand has accumulated negative associations.
    - Product quality or relevance has degraded.
    - Competitive alternatives are superior.
- *Outcome:*
    - Financial drag on the portfolio.
    - Opportunity cost of resources tied up in declining brand.
    - Risk of brand erosion affecting parent company.
- *Context:*
    - Decline is not always terminal; some brands can be revitalized.
    - But resources spent on revitalization have opportunity cost against healthier brands.

**Actions**

1. Determine: is this brand decline or category decline? Different diagnosis, different treatment.
1. If brand-specific: is the root cause fixable within acceptable investment and timeframe?
1. If category decline: consider milking strategy: minimize costs, harvest remaining equity.
1. Evaluate divestiture: is the brand name, trademark, or customer base worth more than the operating business?
1. If milking: reduce marketing spend, maintain quality enough to retain base, maximize margin.

**Verify in**

- **Decline Diagnosis:** Brand decline vs category decline: which is it? Check if competitors in same category are also declining.
- **Reinvestment Case:** What would it cost to reverse decline? What is the probability of success? Is there a better use for those resources?

**Playbook BV-03: Decline Management.** Make the strategic decision: reinvest, milk, or divest, and execute with discipline.

- [ ] Diagnose brand vs category decline
- [ ] Build financial model for each scenario (reinvest/milk/divest)
- [ ] If milking: identify minimum viable investment to maintain
- [ ] If divesting: prepare brand assets for sale
- [ ] If reinvesting: develop revival plan with clear milestones and kill criteria

---

## File: diagnose/references/funnel-diagnostic.md

# Funnel diagnostic

Four customer journeys, each in one of three states: declining, flat or inefficient. Each state lists the signals that identify it, the actions that address it, where to verify, and a micro-playbook. Source: the Cohortica Funnel Diagnostic (cohortica.studio/engine).

Contents: [Acquisition](#acquisition) · [Activation](#activation) · [Revenue](#revenue) · [Retention](#retention)

<a id="acquisition"></a>
## Acquisition: Traffic + Discovery + Qualified Entry

**Question:** How effectively is your brand attracting the right shoppers into the store through channels that can scale profitably?

**How to read it:** Look beyond top-line traffic. Check whether qualified shoppers are reaching hero collections and best-converting PDPs, whether branded demand is stable, and whether merchandising or inventory is weakening effective demand capture.

### Acquisition is DECLINING

*Fewer qualified shoppers are entering the store, or your strongest traffic sources are weakening.*

Qualified demand is softening. The drop may come from lower reach, weaker branded search, channel underdelivery, poorer landing-page relevance, reduced visibility of hero products, or inventory issues that make traffic less productive.

**Signals**

- *Observed:*
    - Sessions and new users are down in GA4 or Shopify, with the sharpest drop in priority channels.
    - Traffic to hero collections and top PDP entry pages is down versus the prior period.
    - Branded search clicks or impressions are down in Search Console.
    - Paid reach, impression share, or spend delivery is down in Meta or Google Ads.
- *Diagnostic:*
    - Landing-page engagement is weakening: lower engaged sessions, higher bounce, or poorer scroll depth.
    - Traffic mix has shifted toward lower-intent audiences, placements, or geographies.
    - Hero SKUs, bestsellers, or promoted variants are low stock, out of stock, or less visible on site.
    - Campaign creative-message match to category or offer has weakened.
- *Outcome:*
    - New-customer orders are down.
    - Channel spend is no longer translating into proportional first-order revenue.
    - Pipeline into add-to-cart and checkout-start is thinning at the top of funnel.
- *Context:*
    - Competitors are running heavier promotions or capturing more search/share of voice.
    - Seasonality, retail calendar timing, or a promo gap is suppressing category demand.
    - Homepage, collection ranking, or campaign landing destinations changed recently.

**Actions**

1. Pull a 4-week trend for sessions, new users, spend, and first-order revenue by channel.
1. Separate volume problems from quality problems by comparing click growth with engaged sessions and checkout starts.
1. Review landing pages for top campaigns and confirm they route to in-stock hero products or strongest collections.
1. Reallocate spend toward the top channels, audiences, and keywords that still drive qualified entry and downstream conversion.
1. Pause or cap sources inflating visits without contribution to add-to-cart, checkout start, or first-order revenue.

**Verify in**

- **GA4 / Shopify Analytics:** Sessions, new users, engaged sessions, landing-page entry, channel mix, and first-session conversion paths.
- **Meta Ads / Google Ads / TikTok Ads:** Reach, spend delivery, CPM, CTR, CPC, impression share, audience shifts, and destination URLs.
- **Search Console:** Branded and non-branded demand, click-through changes, and landing-page search visibility.
- **Catalog / Inventory / Merchandising:** Hero SKU availability, collection visibility, homepage placement, and promo routing.

**Playbook PB-01: Recover Qualified Traffic.** Stabilize top-of-funnel by restoring demand volume in the channels that still produce real commerce contribution.

- [ ] Concentrate spend on the top audiences, keywords, and creatives that still drive checkout starts.
- [ ] Route traffic to highest-converting, in-stock collections instead of generic pages.
- [ ] Restore branded demand capture before expanding prospecting again.
- [ ] Remove low-intent placements and audiences that pad traffic without downstream value.

**Playbook PB-02: Fix Message-to-Landing Match.** Improve conversion quality by matching acquisition promise to product, offer, and merchandising reality.

- [ ] Audit campaign headlines and visuals against landing-page hero copy and product proof.
- [ ] Align each ad set to one clear category, hero SKU set, or use case.
- [ ] Add stronger social proof, reviews, and offer clarity above the fold.

### Acquisition is FLAT: you expected growth but it is not happening

*Traffic is stable, but top-of-funnel is not expanding in a meaningful or efficient way.*

The brand is still attracting shoppers, but scale is constrained. Demand may be saturating within current audiences, channels may be too narrow, creative may have gone stale, or the business is buying more of the same traffic without widening profitable reach.

**Signals**

- *Observed:*
    - Sessions and new users are stable period over period despite higher spend or more campaigns.
    - Branded search is flat and non-branded acquisition is not creating incremental demand.
    - Top landing pages capture most new traffic, but entry breadth across collections or categories is not expanding.
- *Diagnostic:*
    - Creative fatigue is rising: frequency is up while CTR or thumb-stop metrics soften.
    - Prospecting audience breadth is narrow or overlaps heavily with existing converters.
    - SEO or content acquisition is not expanding high-intent discovery around key categories.
    - Acquisition campaigns depend too heavily on discounts or retargeting-like audiences.
- *Outcome:*
    - New-customer revenue is flat.
    - First-order customer growth is not keeping up with media spend or growth targets.
    - Traffic growth is not creating more high-quality cart starts.
- *Context:*
    - Category demand may be mature or seasonally soft.
    - Competitors may be outspending on discovery channels or dominating branded-adjacent terms.
    - The assortment or hero story has not meaningfully changed.

**Actions**

1. Break acquisition into existing-demand capture versus true incrementality.
1. Audit audience overlap, frequency, and creative fatigue across major paid platforms.
1. Expand top-performing product stories into adjacent use cases, formats, and prospecting audiences.
1. Test new landing-page angles tied to category education, bundles, or hero-SKU proof.
1. Shift budget from repetitive spend into experiments that can widen profitable reach.

**Verify in**

- **GA4 / Shopify Analytics:** New-user trends, source/medium growth, landing-page breadth, and first-order conversion by channel.
- **Paid Media Platforms:** Frequency, audience overlap, creative fatigue, prospecting mix, and incremental reach.
- **Search Console / SEO Tools:** Category query coverage, content visibility, and branded vs non-branded search expansion.
- **Creative / Merchandising Calendar:** Refresh cadence, campaign themes, and whether new demand hooks were actually introduced.

**Playbook PB-03: Break Through Reach Saturation.** Open new qualified demand by widening the brand story, audience breadth, and entry points into the catalog.

- [ ] Launch new creative themes tied to distinct buyer motives or product use cases.
- [ ] Open new landing experiences around category problems, gifting, bundles, or bestsellers.
- [ ] Use paid media and SEO together to widen discovery instead of leaning on one channel.

### Acquisition is UP, but it is costing too much relative to results

*You are buying traffic, but too much of it is weak, overpriced, or poorly aligned with commercial outcomes.*

Top-of-funnel metrics may look healthy, but the economics do not. Costs may be rising faster than qualified sessions, checkout starts, or first-order contribution. The business may be overpaying for reach, overusing expensive channels, or sending traffic to weak destinations.

**Signals**

- *Observed:*
    - Traffic and spend are both up, but CAC, blended CPC, or CPM has risen materially.
    - Engaged sessions and checkout starts are not increasing proportionally with clicks.
    - A larger share of visits comes from high-cost channels with weaker downstream conversion.
- *Diagnostic:*
    - Audience targeting is broad but not sufficiently qualified.
    - Creative drives clicks but not the right expectations for product, price point, or offer.
    - Landing destinations emphasize low-converting categories or low-stock products.
    - Retargeting or branded capture is subsidizing apparently efficient acquisition reporting.
- *Outcome:*
    - First-order contribution margin is thinning.
    - New-customer revenue growth trails spend growth.
    - Payback period is worsening even while top-line traffic grows.
- *Context:*
    - Auction pressure is up due to seasonality or competitor spend.
    - Promotional expectations in category are increasing.
    - Media mix is skewed toward channels that are hard to scale profitably for this price point.

**Actions**

1. Compare click growth, engaged sessions, checkout starts, and first-order contribution in one view.
1. Re-rank channels by downstream efficiency, not by platform-reported performance alone.
1. Tighten audience and keyword strategy around segments with stronger conversion and lower refund risk.
1. Route spend toward in-stock hero products and away from weak landing-page destinations.
1. Reduce investment in channels whose incremental traffic is not improving contribution or payback.

**Verify in**

- **GA4 / Shopify Analytics:** Engaged sessions, PDP views, checkout starts, and new-customer conversion by source.
- **Ad Platforms:** CAC proxies, CPM/CPC inflation, placement mix, audience efficiency, and creative-level performance.
- **Orders / Margin / Returns:** Contribution, refund drag, and first-order quality by acquisition source.
- **Inventory / Merchandising:** Whether traffic is being pushed toward the products that can actually monetize efficiently.

**Playbook PB-04: Reduce Wasted Acquisition Spend.** Stop buying expensive traffic that does not become healthy first-order revenue.

- [ ] Set channel guardrails using downstream conversion and contribution metrics.
- [ ] Collapse fragmented campaigns into fewer high-signal structures.
- [ ] Remove weak placements and audiences before raising spend again.

<a id="activation"></a>
## Activation: Product Fit + Merchandising + First-Order Conversion

**Question:** Once shoppers arrive, how effectively does the store convert interest into add-to-cart, checkout start, and a first order?

**How to read it:** Focus on PDP quality, category relevance, review proof, offer clarity, cart friction, checkout friction, and whether the right products are being surfaced to the right audiences.

### Activation is DECLINING

*Shoppers are arriving, but fewer are progressing toward purchase than before.*

Interest is not converting into action. Product pages may be weaker, merchandising may be routing traffic to the wrong products, offer clarity may have slipped, reviews may be weaker, or friction may have increased in cart or checkout.

**Signals**

- *Observed:*
    - Add-to-cart rate, checkout-start rate, or session-to-order CVR is down.
    - PDP engagement has weakened: fewer size or variant selections, lower scroll depth, or fewer image interactions.
    - Bounce or exit rates are up on key landing pages, PDPs, or cart.
- *Diagnostic:*
    - Traffic is landing on weaker categories, less relevant SKUs, or low-stock variants.
    - Offer and value proposition are less obvious above the fold.
    - Review quality, quantity, or trust signals are insufficient for the price point.
    - Checkout friction increased due to shipping surprises, payment issues, or promo-code confusion.
- *Outcome:*
    - Orders and first-order revenue are down even when traffic is stable.
    - Media efficiency worsens because too few visitors convert downstream.
    - Cart creation is not turning into healthy checkout progression.
- *Context:*
    - Recent price changes, promo rollbacks, or shipping-threshold adjustments may have reduced buyer confidence.
    - A site redesign, theme update, or app conflict may have introduced friction.

**Actions**

1. Identify the sharpest drop points across PDP view, add-to-cart, checkout start, and payment completion.
1. Audit hero PDPs for value proposition clarity, variant availability, shipping message, and review proof.
1. Check whether acquisition traffic is landing on the most conversion-ready products and collections.
1. Simplify cart and checkout friction: remove surprises, clarify delivery promise, and tighten promo mechanics.
1. Restore focus on highest-converting offers, bundles, and merchandising placements.

**Verify in**

- **GA4 / Shopify Funnel Reports:** PDP view-to-cart, cart-to-checkout, checkout completion, and device-specific drop-offs.
- **Hotjar / Clarity / Session Replay:** Actual friction patterns on PDPs, cart, and checkout.
- **Reviews / UGC / PDP Content:** Proof quality, objection handling, and conversion-supporting content.
- **Inventory / Variant Data:** Whether top-converting sizes, colors, or packs are unavailable.

**Playbook PB-05: Repair the PDP-to-Checkout Path.** Remove the frictions that prevent interested shoppers from becoming first-time buyers.

- [ ] Strengthen product promise, proof, and variant clarity above the fold.
- [ ] Prioritize high-converting products in merchandising and campaign routing.
- [ ] Cut unnecessary checkout steps and surface shipping information earlier.

### Activation is FLAT: traffic is there, but conversion is stuck

*The store converts at a stable level, but not well enough to unlock growth.*

The proposition is adequate, but not strong enough to create step-change improvement. The business may be relying on average-performing PDPs, generic merchandising, weak offer structure, or undifferentiated product proof.

**Signals**

- *Observed:*
    - Add-to-cart and checkout-start rates are stable but unimpressive.
    - High-traffic pages have middling conversion compared with top-performing products.
    - Session replay shows browsing without decisive progression.
- *Diagnostic:*
    - Hero products are not surfaced strongly enough.
    - Bundles, compare-at pricing, or threshold incentives are not being used strategically.
    - PDP content is informative but not persuasive for the category.
    - Collections are organized for browsing, not for conversion intent.
- *Outcome:*
    - Traffic growth yields only modest revenue growth.
    - Acquisition efficiency remains capped by an average conversion experience.
    - Too many shoppers stall before commit signals such as cart or checkout.
- *Context:*
    - Competitors may present stronger proof, pricing architecture, or offer framing.
    - The category may require more education, comparison, or trust-building than the site provides.

**Actions**

1. Benchmark top PDPs and collections against the site median to locate hidden winners.
1. Promote best-converting products, bundles, and review-rich offers more aggressively.
1. Test stronger above-the-fold copy, visual proof, and objection handling on hero pages.
1. Re-merchandise collections around shopper intent, not just catalog structure.
1. Experiment with cart-builder, bundle, or threshold offers that increase shopper commitment.

**Verify in**

- **Shopify / GA4 Product Performance:** PDP CVR, add-to-cart rate, cart entry, and purchase rate by product, collection, and landing page.
- **Session Replay / Heatmaps:** Whether shoppers are seeing and responding to the strongest proof and offer elements.
- **Merchandising Rules / Searchandising:** Ranking logic, filters, featured slots, and recommendation placement.

**Playbook PB-06: Raise the Conversion Ceiling.** Turn a functional storefront into a decisively persuasive one by concentrating attention on the products and pages that already show conversion strength.

- [ ] Scale visual and copy patterns from the best PDPs into the rest of the conversion path.
- [ ] Use bundles and threshold mechanics to create momentum toward checkout.
- [ ] Reorder collections so the most conversion-ready products appear first.

### Activation is UP, but it depends too much on discounts or heavy incentives

*Conversion is rising, but too much of the gain depends on promotions that may not be healthy.*

The site is converting, but not cleanly. The lift may come from rising discounts, bundle giveaways, shipping subsidies, or aggressive offers that weaken unit economics or train customers to wait for deals.

**Signals**

- *Observed:*
    - Conversion rate is up while discount rate or promo-code usage also rises.
    - Orders skew toward discounted SKUs, bundles, or promo periods.
    - AOV may be stable or down despite stronger order conversion.
- *Diagnostic:*
    - Non-discounted PDPs or categories still underperform.
    - Offer framing, not underlying product persuasion, may be doing most of the work.
    - Free-shipping thresholds or sitewide sales are driving behavior that would not persist without incentives.
- *Outcome:*
    - Gross margin per order is under pressure.
    - Customers acquired during promos may repeat less or churn faster.
    - Activation looks improved in the dashboard but less attractive financially.
- *Context:*
    - Category is promotion-heavy or competitor discounting is elevated.
    - Inventory pressure may have triggered broader discounting than the brand can sustain.

**Actions**

1. Split conversion gains into discounted vs non-discounted paths.
1. Measure margin and repeat behavior for promo-driven first orders.
1. Strengthen baseline PDP persuasion so fewer orders depend on heavy incentives.
1. Narrow promotions to targeted SKUs, segments, or threshold mechanics instead of broad blanket discounts.
1. Use merchandising and proof improvements to preserve conversion while lowering subsidy intensity.

**Verify in**

- **Orders / Discount Reporting:** Discount rate, promo-code usage, contribution, and promo dependency by product and channel.
- **Product / PDP Analytics:** Whether non-discounted hero pages convert well enough on their own.
- **Cohort / Repeat Purchase Data:** Quality and follow-on value of customers activated under heavy promotions.

**Playbook PB-07: Reduce Promo Dependency.** Keep the conversion win while rebuilding healthier gross profit and customer quality.

- [ ] Constrain blanket discounts and favor targeted offers instead.
- [ ] Lift PDP proof so product desire does more of the conversion work.
- [ ] Track promo-acquired cohorts separately before scaling that tactic.

<a id="revenue"></a>
## Revenue: AOV + Mix + Margin Quality

**Question:** When orders happen, how healthy is the commercial output in terms of revenue quality, product mix, discounting, and contribution?

**How to read it:** Revenue is not just sales. Check AOV, units per order, product mix, discount rate, return drag, and whether the business is growing through strong economics or through expensive volume.

### Revenue quality is DECLINING

*Orders may still be happening, but the economic quality of those orders is worsening.*

Commercial output is weakening. Lower AOV, worse product mix, rising discounting, or higher returns may be dragging revenue quality and contribution even if demand has not collapsed.

**Signals**

- *Observed:*
    - AOV, units per order, or revenue per visitor is down.
    - Bestselling or premium SKUs contribute less to the revenue mix.
    - Refunds, returns, or canceled orders are up.
- *Diagnostic:*
    - Merchandising favors lower-value SKUs or lower-margin bundles.
    - Customers are converting via deeper discounts than before.
    - Cross-sell and upsell placements are weak or absent.
    - Inventory gaps are forcing the basket toward lower-value substitutes.
- *Outcome:*
    - Contribution margin per order is down.
    - Revenue can look stable while profit quality weakens.
    - Media and operating costs consume a larger share of gross sales.
- *Context:*
    - Competitor pricing pressure or category discount cycles may be changing buyer expectations.
    - Assortment changes, shipping-cost changes, or return policy shifts may be distorting order value.

**Actions**

1. Decompose revenue change into traffic, conversion, AOV, mix, and return effects.
1. Identify which product, channel, or cohort shifts are lowering order quality.
1. Re-merchandise bundles, premium SKUs, and cross-sell placements to raise order value.
1. Reduce needless discounting where baseline demand remains healthy.
1. Check whether stockouts in premium or hero items are pushing the basket downward.

**Verify in**

- **Shopify / Orders Reporting:** AOV, units per order, revenue per session, discount rate, and refund impact.
- **SKU / Variant Mix:** Mix shifts by category, hero product contribution, and premium-vs-entry item balance.
- **Returns / Support Themes:** Whether quality, fit, or expectation mismatch is eroding net revenue.
- **Merchandising / Bundles:** Upsell exposure, collection ordering, and attach-rate opportunities.

**Playbook PB-08: Restore Order Value and Mix.** Lift revenue quality by steering demand toward healthier baskets, better products, and more profitable order structures.

- [ ] Promote premium and hero items more visibly where conversion remains strong.
- [ ] Improve attach-rate with bundles, accessories, and post-add-to-cart upsells.
- [ ] Reduce discounts on products that do not require incentive to sell.

### Revenue is FLAT: sales are happening, but the business is not compounding

*The storefront is producing revenue, but commercial productivity is not improving.*

The business may have reached a revenue plateau because order value, product mix, or merchandising leverage is not progressing. Growth is being capped by average baskets, limited upsell architecture, or insufficient premiumization.

**Signals**

- *Observed:*
    - Revenue is steady while order count or traffic fluctuates modestly.
    - AOV and units per order show little movement despite promotions or merchandising efforts.
    - The same products do most of the work, with little expansion into healthier mix.
- *Diagnostic:*
    - Cross-sell and upsell surfaces exist but do not materially influence baskets.
    - Collections are not organized to steer shoppers toward high-value sets or routines.
    - Premium products lack enough proof, education, or merchandising support.
- *Outcome:*
    - Each incremental traffic gain adds only limited commercial leverage.
    - The brand depends on volume growth because basket quality is not improving.
- *Context:*
    - Category norms may anchor baskets unless the store creates stronger routines, sets, or replenishment logic.
    - Assortment breadth may be outpacing merchandising clarity.

**Actions**

1. Analyze which products and bundles lift AOV without hurting conversion.
1. Rebuild collection and cart architecture around routines, sets, and logical attachments.
1. Promote high-value products with stronger proof, comparison, and role in the basket.
1. Test threshold offers that increase units per order without excessive subsidy.
1. Segment basket-building tactics by traffic source and customer type.

**Verify in**

- **Orders / Basket Analysis:** AOV, units per order, attach rate, bundle take-up, and revenue per visitor.
- **Cart / Upsell Tools:** Which suggestions are shown, accepted, or ignored.
- **Product / Category Reporting:** Where premiumization opportunities exist by collection and cohort.

**Playbook PB-09: Build Higher-Value Baskets.** Create more revenue from the demand you already have by redesigning how the basket gets built.

- [ ] Feature routines, bundles, and complementary products more intentionally.
- [ ] Use thresholds and offers that increase units per order, not just order count.
- [ ] Teach premium value rather than assuming shoppers will self-upgrade.

### Revenue is UP, but margin quality is too weak

*Top-line sales are growing, but profitability is not keeping pace.*

The business is generating revenue, but too much of that growth is driven by discounting, weak mix, returns, shipping subsidy, or rising acquisition cost. This is growth without enough commercial quality.

**Signals**

- *Observed:*
    - Gross sales are up while contribution margin percentage is flat or down.
    - Discounts, promotions, shipping subsidy, or marketplace fees are rising.
    - High-volume products are not the healthiest products economically.
- *Diagnostic:*
    - Growth is concentrated in channels or SKUs with weaker economics.
    - AOV lift is coming from unprofitable bundles or over-incentivized carts.
    - Repeat purchases are not strong enough to justify current first-order economics.
- *Outcome:*
    - Cash efficiency and payback worsen despite higher sales.
    - Operational load rises without a matching lift in contribution.
- *Context:*
    - Peak-season competition or channel shifts may be encouraging lower-quality growth.
    - Freight, fulfillment, or return costs may be distorting what looks like healthy revenue.

**Actions**

1. Build one margin-quality view combining revenue, discounting, returns, shipping subsidy, and acquisition cost.
1. Rank channels, SKUs, and promotions by contribution, not gross sales.
1. Tighten promotional depth where demand is resilient.
1. Favor products, bundles, and cohorts with better payback and lower return drag.
1. Treat gross revenue growth as secondary until commercial quality stabilizes.

**Verify in**

- **Finance / Margin Reporting:** Contribution, blended margin, shipping subsidy, and return-adjusted economics.
- **Orders / Promo Reporting:** Discount and bundle dependency by product, source, and cohort.
- **Acquisition / Cohort Data:** Whether higher first-order cost is justified by longer-term value.

**Playbook PB-10: Clean Up Revenue Growth.** Preserve top-line performance while rebuilding the commercial economics underneath it.

- [ ] Separate profitable growth from merely visible growth.
- [ ] Reduce discounts where they are not truly incremental.
- [ ] Scale the mixes and channels that generate the healthiest net outcome.

<a id="retention"></a>
## Retention: Repeat Purchase + Loyalty + Post-Purchase Health

**Question:** After the first order, how effectively does the brand create repeat purchasing, loyalty, and durable customer value?

**How to read it:** Retention for physical-product brands is shaped by product satisfaction, reorder cadence, support quality, returns, replenishment logic, loyalty design, and whether first-time buyers were acquired in the right way.

### Retention is DECLINING

*Customers are not coming back at the rate they used to, or repeat value is weakening.*

The post-purchase engine is under strain. Customers may be less satisfied, less clearly guided to reorder, more return-prone, or increasingly acquired through low-quality promotional tactics that do not create durable loyalty.

**Signals**

- *Observed:*
    - Repeat purchase rate, reorder rate, or subscription retention is down.
    - Time-to-second-order is lengthening.
    - Support contacts, complaints, or return rates are rising.
- *Diagnostic:*
    - First-order cohorts from certain channels or promos repeat materially worse.
    - Customers are not receiving timely replenishment, education, or cross-sell prompts.
    - Product satisfaction issues appear in reviews, tickets, or return reasons.
    - Loyalty mechanics are weak or not salient enough to change behavior.
- *Outcome:*
    - LTV is softening.
    - Payback periods worsen because fewer customers generate later orders.
    - The brand becomes increasingly dependent on reacquiring new customers.
- *Context:*
    - Competitor promotions or substitutes may be increasing switching.
    - Operational issues such as delays, packaging problems, or damaged orders may be depressing loyalty.

**Actions**

1. Split repeat behavior by first-order source, product, and promo exposure.
1. Read return reasons, support tickets, and negative reviews for recurring friction themes.
1. Audit post-purchase messaging, replenishment timing, and cross-sell logic.
1. Strengthen retention flows around the products and cohorts that already show healthy reorder patterns.
1. Address operational or product-quality drivers before increasing win-back spend.

**Verify in**

- **Klaviyo / CRM / Cohort Reporting:** Repeat purchase rate, time to second order, and cohort retention by source, product, and offer type.
- **Reviews / Support / Returns:** Satisfaction, quality issues, expectation mismatch, and churn clues.
- **Subscription / Loyalty Data:** Retention mechanics, engagement, and lapse patterns.
- **Fulfillment / Delivery Data:** Late shipments, damaged deliveries, and service failures affecting repeat value.

**Playbook PB-11: Recover Repeat Purchase.** Rebuild customer value by fixing the product, service, and lifecycle signals that drive a second order.

- [ ] Identify which first-order experiences produce the strongest repeat behavior and replicate them.
- [ ] Repair the support, quality, or fulfillment issues hurting satisfaction.
- [ ] Time replenishment and win-back flows to real reorder windows, not generic schedules.

### Retention is FLAT: customers are buying once, but loyalty is not compounding

*The brand gets some repeat behavior, but not enough to create a stronger value engine.*

Customers are reasonably satisfied, but the business is not actively shaping repeat purchase. The lifecycle program may be generic, the catalog may not invite clear next purchases, or the brand may not be building a strong enough habit or routine.

**Signals**

- *Observed:*
    - Repeat purchase rate is stable but modest.
    - Second-order conversion is acceptable for a small subset of products or cohorts but not broadly.
    - Email and SMS engagement exists, but lifecycle flows do not materially lift retained revenue.
- *Diagnostic:*
    - Cross-sell and reorder flows are too broad rather than product- and timing-specific.
    - Loyalty value is unclear or too weak to change behavior.
    - Customers are not being guided into routines, subscriptions, or replenishment cadence.
- *Outcome:*
    - LTV remains capped.
    - The brand relies too much on first-order acquisition to grow.
- *Context:*
    - The category may require stronger education or regimen-building to earn repeats.
    - Product assortment may not clearly map the next logical purchase.

**Actions**

1. Map the strongest repeat paths by first-order SKU and customer type.
1. Rewrite lifecycle messaging around real product journeys, not generic campaign calendars.
1. Use bundles, subscriptions, and next-best-product recommendations to create a clearer repeat path.
1. Make loyalty value tangible at the moment it can influence the next order.
1. Prioritize cohorts with the highest plausible LTV lift.

**Verify in**

- **Lifecycle Platform:** Flow conversion, retained revenue, time-window performance, and SKU-linked retention journeys.
- **Cohort / Product Repeat Analysis:** Which first-order products and source combinations produce the best repeat behavior.
- **Loyalty / Subscription Data:** Participation, redemption, skip/churn, and repeat influence.

**Playbook PB-12: Turn One-Time Buyers into a Retention Engine.** Move beyond generic lifecycle marketing by designing clear, product-led reasons to come back.

- [ ] Tie lifecycle content to actual consumption or replenishment logic.
- [ ] Create better next-order suggestions based on what was purchased first.
- [ ] Use loyalty and subscriptions where they genuinely strengthen habit, not as decoration.

### Retention is UP, but it is overly dependent on incentives or win-back pressure

*Customers are returning, but too much of the repeat behavior is purchased rather than earned.*

Repeat activity exists, but it may be fragile. The business might be relying on frequent discounts, win-back campaigns, or loyalty subsidy rather than genuine product satisfaction and habit strength.

**Signals**

- *Observed:*
    - Repeat revenue rises alongside promo dependence or frequent win-back messaging.
    - Subscription or loyalty participation is up, but net economics remain unclear.
    - Repeat orders cluster around discount windows rather than organic reorder timing.
- *Diagnostic:*
    - Customers may not buy again without an incentive.
    - The brand is using retention campaigns to compensate for weak satisfaction or weak next-product relevance.
    - Discount-driven repeat cohorts may have lower margin and weaker long-term value.
- *Outcome:*
    - Retained revenue looks stronger than retained profit.
    - Lifecycle spend and incentives erode repeat-order quality.
- *Context:*
    - Competitor discounting may be training customers to price-shop between brands.
    - Inventory or seasonality may have encouraged reactive win-back pressure.

**Actions**

1. Separate incentive-driven repeat orders from organic repeats.
1. Measure margin and long-run value of win-back, loyalty, and subscription cohorts.
1. Improve satisfaction, replenishment timing, and next-best-product logic so fewer repeats require discounts.
1. Use incentives more selectively, focusing on at-risk cohorts with high latent value.
1. Treat repeat quality, not repeat volume alone, as the main retention KPI.

**Verify in**

- **CRM / Lifecycle / Loyalty Data:** Incentive exposure, repeat conversion, retained revenue, and promotion dependency.
- **Margin / Cohort Reporting:** Net value of retained cohorts after discounting and service cost.
- **Reviews / Support:** Whether product or service issues are being masked by win-back pressure.

**Playbook PB-13: Improve Retention Quality.** Shift repeat purchase from subsidy-heavy behavior to healthier loyalty rooted in product satisfaction and relevance.

- [ ] Track organic and incentivized repeats separately.
- [ ] Reserve offers for cohorts where the incremental value is genuinely attractive.
- [ ] Use better product sequencing and post-purchase experience to reduce win-back dependency.

---

## File: diagnose/references/insight-patterns.md

# Insight patterns

"If you see X, it usually means Y; check Z." About seventy recurring readings from the playbooks, by discipline. Use them to propose a likely cause, then confirm it in the data before writing it as a finding. Paths in parentheses name the Cohortica playbook a definition comes from; the playbooks themselves ship in the `diagnose` skill (`references/playbooks/`). **[std]** marks a standard industry definition added where the playbooks are silent; **GAP** marks what neither covers.


## Web / on-site
- Huge sessions, engagement rate far below peers -> "attention that evaporates on arrival"; fix creative, targeting or landing page, not more traffic (web-analytics/ga4-fundamentals.md).
- Engagement rate collapsed MoM -> traffic-mix change, landing-page change, or tagging change, "in that order" (web-analytics/ga4-fundamentals.md).
- High sessions, low engagement -> "a landing-page or intent-match problem, not a traffic problem" (web-analytics/on-site-funnel.md).
- Long duration with pages/visit near 1.0 -> "people are stuck, not absorbed" (web-analytics/on-site-funnel.md).
- Total revenue up, revenue per user down -> "you bought growth" (web-analytics/on-site-funnel.md).
- Site CVR fell 2.4% -> 2.1% -> refuse the blend; check mix shift by channel and named action (web-analytics/on-site-funnel.md).
- Channel gains big credit under DDA vs last-click -> contributes along the path but rarely lands last; check volume threshold (web-analytics/on-site-funnel.md).
- Traffic up 30%, revenue flat -> walk hand-offs; locate the first transition that broke (web-analytics/marketing-funnel-overview.md).
- Plenty of impressions with low CTR -> "a message problem no extra budget fixes" (web-analytics/marketing-funnel-overview.md).
- Direct spiked after a campaign -> untagged links first, not brand lift (web-analytics/utm-tagging.md).
- Paid social engagement fine, conversion zero -> checkout or offer; bounces on every page -> buying the wrong audience, pull spend (web-analytics/on-site-funnel.md).

## SEO
- Soft CTR at strong position -> title/snippet problem; soft CTR at position 12 -> ranking problem (seo/insight-roadmap.md).
- Top-3 query with ~1% CTR -> cheapest win; rewrite title/meta, not links (seo/search-console-queries.md).
- Great CTR, no conversion -> landing page/intent match, not ranking (seo/insight-roadmap.md).
- Clicks fine, engagement low -> content/UX; engagement fine, conversion near zero -> CRO window; high conversion, low sessions -> starved winner, feed it (seo/search-console-and-ga4.md).
- Blog post with big impressions on commercial term -> drill queries; thin explainer can't close; point the right page at the intent (seo/landing-page-performance.md).
- Low CTR page -> drill to queries: own intent = snippet; other page's intent or sibling = cannibalization/mismatch (seo/search-console-landing-pages.md).
- One query, two of your URLs -> cannibalization; consolidate (seo/query-level-data.md).
- Organic sessions declining with no ranking losses -> zero-click compression; check impressions vs clicks and AI-referral stream (emerging/llm-traffic-and-organic-search.md).
- Steady clicks, no new pages/queries underneath -> "coasting toward decline" (seo/new-and-newly-ranking-pages.md).
- Clicks growing faster than impressions -> CTR improving, not just visibility (seo/seo-overview.md).
- New page with high impressions at pos 27 from browsing queries -> awareness churn; note it, do not fund (seo/new-and-newly-ranking-pages.md).
- Existing page newly ranking for new query -> deepen, not a rival page (seo/new-and-newly-ranking-pages.md).
- Query converts well in paid, organic absent/20+ -> content bet; 4-20 -> leverage zone; 1-3 -> "why still paying?" test the bid (seo/organic-paid-overlap.md).
- Organic traffic drop -> split country/device, then position drop vs CTR drop at stable position, then brand vs non-brand (seo/seo-overview.md).

## Paid search
- Healthy blended CTR, cheap CPC -> may be pure brand halo hiding a bleeding generic program (paid-search/brand-vs-generic.md).
- Generic campaign looks brilliant -> check forward leakage of brand queries (paid-search/brand-vs-generic.md).
- Spectacular CVR, CPA of pennies -> micro-conversions scoped; re-read on purchases (paid-search/conversions-cpa-and-return.md).
- Strong CTR, weak conversion -> landing page: message match, speed, checkout friction (paid-search/conversions-cpa-and-return.md).
- Low impression share -> split rank vs budget before acting (paid-search/impression-share-and-quality-score.md).
- Converting campaign with high IS lost to budget -> "the clearest raise-the-cap signal" (paid-search/budget-pacing.md).
- 34% spent on the 20th -> serious under-pace, likely capped winners (paid-search/budget-pacing.md).
- Uncapped generic over budget at poor CPA while brand campaign pinned at cap -> fix caps before keywords (paid-search/account-structure.md).
- Rising CPC on core terms -> crowding auctions; look for competitor terms where you have zero IS (competitive-research/competitive-and-keyword-research.md).
- Mobile cheap CPC -> compute value: 2x CPC at half CVR = ~1/4 desktop value (paid-search/device-and-timing.md).
- Bid modifier did nothing -> automated bidding (paid-search/device-and-timing.md).
- Account "up 20% on conversions" -> check scoping, brand leakage, concentration in one branch (paid-search/insight-roadmap.md).

## Paid media / social
- Clicks up with rising CPC -> bought growth; check conversions keep pace (paid-media/auditing-pmax.md).
- PMax 6x ROAS -> apply purchase lens, check branded overlap, clicks vs CPC (paid-media/performance-max.md).
- Lowest CPM and biggest budget -> interrogate viewability, MFA placements, downstream demand (paid-media/display-advertising.md).
- Rising cost of reach or falling engagement at flat spend -> creative fatigue; refresh cadence (paid-media/demand-gen.md).
- Quartile cliff after first 25% -> hook past skip button (paid-media/video-and-youtube.md).
- Retargeting 5-6x, prospecting <1x -> don't shift; retargeting harvests prospecting's demand (paid-social/paid-social-overview.md; paid-media/display-advertising.md).
- Frequency climbing + CTR falling -> creative burnout, rotate before raising budget (paid-social/paid-social-overview.md).
- Rising CPC with steady CTR -> auction competition (paid-social/paid-social-overview.md).
- Rising CPM at flat reach -> audience too narrow or creative fatiguing (paid-social/paid-social-overview.md).
- Meta conversions > GA4 -> likely view-through on Meta's window (hypothesis until the account's attribution setting is checked); set one window (paid-social/paid-social-overview.md).
- Display worst on last-click ROAS -> floor lowest for upper funnel; model or holdout before cutting (paid-media/true-roas.md).
- Platforms' ROAS sum exceeds finance revenue -> double-counting; one shared denominator (paid-media/true-roas.md).

## Email
- Healthy opens, flat revenue -> walk delivery, CTR, on-site conversion, net list growth (email-marketing/email-marketing-overview.md).
- Fine CTOR, low CTR -> sent too broadly; narrow audience, don't rewrite (email-marketing/engagement-and-the-click.md).
- Opens steady, clicks halved -> offer, CTA, subject over-promise, broadened segment (email-marketing/reading-the-send-funnel.md).
- Bounce rate rising at steady volume -> lapsed hygiene, before delivery falls (email-marketing/deliverability-and-inbox-placement.md).
- Complaints past 0.1% -> consent/frequency; cut volume (email-marketing/email-marketing-overview.md).
- Best-clicking send earned least -> low-intent volume; check revenue per purchaser and page match (email-marketing/click-to-revenue.md).
- Clicks but zero revenue -> instrumentation first (untagged links) (email-marketing/click-to-revenue.md).
- Sessions far below clicks on one send -> broken or untagged link (email-marketing/click-to-revenue.md).
- All campaign metrics stable for a year -> check net list growth sign (email-marketing/list-health-and-reputation.md).

## Customer analytics
- Blended repeat rate fell -> composition trap; re-read at matched age plus new vs returning mix (customer-analytics/reading-acquisition-quality.md).
- December cohort retains worse -> seasonality; compare to last December (customer-analytics/reading-acquisition-quality.md).
- Payback stretching 3 -> 6 months -> growth bought at quality's expense (customer-analytics/reading-acquisition-quality.md).
- 80% still active -> pulse not flow; check order gap and basket size (customer-analytics/cohort-analysis.md).
- Decline shapes: seasonal recurring quiet / stop after refund or ticket = experience problem / steady erosion with no incident = competitor / hard stop = goodbye (customer-analytics/cohort-analysis.md).
- LTV €340 on dashboard -> ask churn model, horizon, discounting; place between floor and ceiling (customer-analytics/clv-vs-cac.md).
- Two LTVs 3x apart -> likely different horizons/decisions (customer-analytics/clv-vs-cac.md).

## Attribution / GEO
- Viewers 20% vs non-viewers 9% -> proves targeting, not effect (attribution-experiments/controlled-experiments.md).
- Model contradicts holdouts -> miscalibrated (attribution-experiments/attribution-and-mmm.md).
- LLM traffic converts below organic baseline -> answer set an expectation the page doesn't meet; fix page (emerging/llm-traffic-and-organic-search.md).
- Page drops out of LLM cited set while organic holds -> competitor displaced you in answers (emerging/measuring-llm-traffic-in-ga4.md).
- Named in AI answers, no traffic lift -> zero-click by design; watch branded demand (emerging/geo-getting-cited-in-ai-answers.md).

## Pricing and promotions (from the author's notes)

- Falling baseline sales with rising promo lift -> customers learning to wait for deals, not better promotions; check baseline trend, full-price share, time to repeat.
- More than ~40% of revenue on promotion -> training deal-seekers; check repeat rate at full price by cohort.
- Promotion lifted units -> not yet a win; net out margin cost, pull-forward (post-promo dip) and repeat.
- Price up and revenue up, or price down and revenue down -> demand is inelastic; test whether price is below its profit optimum.
- Loss-leader item with negative margin -> judge its spillover (traffic, basket) before cutting it.

## Demand, share and loyalty (from the author's notes)

- Flat sales -> decompose into category demand x share first; flat can hide share loss in a growing category.
- Small brand repeats less than the leader -> expected (double jeopardy), not evidence of a weaker product.
- Loyalty-programme members repeat more -> mostly buyers who would have stayed anyway; growth comes from penetration.
- High aided awareness, low unaided -> a salience problem, not a reach problem.
- Raw "+65%" jump -> deseasonalize first; it may be "+5% real".
- Worst segment improves right after you intervene -> regression to the mean; check against a control or the segment's own history.

## Attribution and experiments (from the author's notes)

- Channel worthless on last-click, strong on first-click -> an introducer, not a closer; compare models, then run a holdout.
- Frequency vs lift is an inverted U -> check lift by frequency band before raising frequency caps.
- A/B split drifts from the intended ratio -> sample ratio mismatch; do not ship, check assignment and logging.
- Big early lift that fades -> novelty effect; split new vs returning users.
- Metric moved right after a tracking change -> instrumentation, not customers.
- Direct traffic spikes -> tagging first; a sustained high direct share can be brand strength.
- New/returning user ratio falling sharply -> acquisition is falling behind.
- Branded searches climb the week after AI-answer mentions -> the closest thing to a GEO scoreboard.

---

## File: diagnose/references/playbook-index.md

# Playbook index

59 playbooks by discipline. Each has an opener, *The framework*, *Metrics that matter, and their traps*, and *Interview prep*. Read the one that matches the finding; quote its framework, not its interview section.

## attribution-experiments

- Attribution and marketing mix modelling (section "File: diagnose/references/playbooks/attribution-experiments/attribution-and-mmm.md" in 03-diagnose-and-playbooks.md): How do you get from a last-click ROAS floor to an estimate of what each channel truly contributed
- Controlled experiments for ad effectiveness (section "File: diagnose/references/playbooks/attribution-experiments/controlled-experiments.md" in 03-diagnose-and-playbooks.md): How do you prove an ad actually caused sales, rather than harvesting buyers who would have bought anyway

## competitive-research

- Keyword research and competitive analysis (section "File: diagnose/references/playbooks/competitive-research/competitive-and-keyword-research.md" in 03-diagnose-and-playbooks.md): How do I decide which search demand is worth chasing before spending on it
- Marketing personas that earn their keep (section "File: diagnose/references/playbooks/competitive-research/marketing-personas.md" in 03-diagnose-and-playbooks.md): How do you build a persona that is worth spending real budget against

## customer-analytics

- Customer lifetime value vs CAC (section "File: diagnose/references/playbooks/customer-analytics/clv-vs-cac.md" in 03-diagnose-and-playbooks.md): How do you compare what a customer is worth against what they cost, honestly
- Cohort analysis, measure before you model (section "File: diagnose/references/playbooks/customer-analytics/cohort-analysis.md" in 03-diagnose-and-playbooks.md): When should you model customer value, and when should you simply measure it
- Reading acquisition quality with cohorts (section "File: diagnose/references/playbooks/customer-analytics/reading-acquisition-quality.md" in 03-diagnose-and-playbooks.md): Did the customers a given month's marketing bought actually turn out to be good ones

## email-marketing

- Email marketing, from send to revenue (section "File: diagnose/references/playbooks/email-marketing/email-marketing-overview.md" in 03-diagnose-and-playbooks.md): How do you judge whether an email program is actually working
- Reading the send funnel (section "File: diagnose/references/playbooks/email-marketing/reading-the-send-funnel.md" in 03-diagnose-and-playbooks.md): Where in the sent-to-clicked sequence is a campaign actually leaking
- Deliverability and inbox placement (section "File: diagnose/references/playbooks/email-marketing/deliverability-and-inbox-placement.md" in 03-diagnose-and-playbooks.md): Why are my emails not reaching the inbox, and what do I fix first
- Engagement and the click (section "File: diagnose/references/playbooks/email-marketing/engagement-and-the-click.md" in 03-diagnose-and-playbooks.md): How do you measure whether email content actually drove action
- List health and reputation (section "File: diagnose/references/playbooks/email-marketing/list-health-and-reputation.md" in 03-diagnose-and-playbooks.md): Is the list underneath my campaigns growing or quietly eroding
- From the click to the revenue (section "File: diagnose/references/playbooks/email-marketing/click-to-revenue.md" in 03-diagnose-and-playbooks.md): How do you know what an email campaign actually earned, not just what it got clicked

## emerging

- Generative engine optimization: getting cited in AI answers (section "File: diagnose/references/playbooks/emerging/geo-getting-cited-in-ai-answers.md" in 03-diagnose-and-playbooks.md): How do you earn citations inside AI-generated answers, and what can you honestly measure
- LLM traffic and its effect on organic search (section "File: diagnose/references/playbooks/emerging/llm-traffic-and-organic-search.md" in 03-diagnose-and-playbooks.md): What do answer engines do to your organic channel, and how do you read the traffic they send
- Measuring LLM traffic in GA4 (section "File: diagnose/references/playbooks/emerging/measuring-llm-traffic-in-ga4.md" in 03-diagnose-and-playbooks.md): How do you build a monthly read of the traffic AI answer engines send you

## organic-social

- Organic social performance (section "File: diagnose/references/playbooks/organic-social/organic-social-overview.md" in 03-diagnose-and-playbooks.md): How do you measure organic social when it rarely converts directly, and what does its work actually feed

## paid-media

- The paid media insight roadmap (section "File: diagnose/references/playbooks/paid-media/insight-roadmap.md" in 03-diagnose-and-playbooks.md): In what order should you read a paid media account beyond search and social, and why does the order matter
- Display advertising (section "File: diagnose/references/playbooks/paid-media/display-advertising.md" in 03-diagnose-and-playbooks.md): How do you read a display line so cheap reach is judged on what it actually buys, and verify the reach was real
- Demand Gen campaigns (section "File: diagnose/references/playbooks/paid-media/demand-gen.md" in 03-diagnose-and-playbooks.md): How do you run and read Demand Gen when there are no keywords and the payoff lands after the last click
- Video and YouTube advertising (section "File: diagnose/references/playbooks/paid-media/video-and-youtube.md" in 03-diagnose-and-playbooks.md): How do you buy and read video advertising when the attention lands now and the demand shows up later
- Performance Max (section "File: diagnose/references/playbooks/paid-media/performance-max.md" in 03-diagnose-and-playbooks.md): What is Performance Max, when does it earn its place, and how do you read past its black-box reporting
- Auditing a Performance Max campaign (section "File: diagnose/references/playbooks/paid-media/auditing-pmax.md" in 03-diagnose-and-playbooks.md): What is the step-by-step read that tells you whether Performance Max is actually working
- True ROAS across every paid channel (section "File: diagnose/references/playbooks/paid-media/true-roas.md" in 03-diagnose-and-playbooks.md): How do you compare return across paid channels when every platform claims the same sale

## paid-search

- Paid search, read as a chain (section "File: diagnose/references/playbooks/paid-search/paid-search-overview.md" in 03-diagnose-and-playbooks.md): How do I judge whether a paid search account is actually performing
- Read your account in order (section "File: diagnose/references/playbooks/paid-search/insight-roadmap.md" in 03-diagnose-and-playbooks.md): In what order should I read a paid search account so the numbers tell the truth
- Account structure and clusters (section "File: diagnose/references/playbooks/paid-search/account-structure.md" in 03-diagnose-and-playbooks.md): How do I localize a paid search problem instead of averaging the whole account
- Branded vs generic (section "File: diagnose/references/playbooks/paid-search/brand-vs-generic.md" in 03-diagnose-and-playbooks.md): Why split branded from generic search before trusting any account average
- Match types and wasted spend (section "File: diagnose/references/playbooks/paid-search/match-types-and-wasted-spend.md" in 03-diagnose-and-playbooks.md): How do I find and cut the spend that was never going to convert
- Query performance and new queries (section "File: diagnose/references/playbooks/paid-search/query-performance.md" in 03-diagnose-and-playbooks.md): Which new search queries deserve their own ad group
- Impression share and quality score (section "File: diagnose/references/playbooks/paid-search/impression-share-and-quality-score.md" in 03-diagnose-and-playbooks.md): How do I read the visibility layer that sits above the click
- Conversions, CPA and return (section "File: diagnose/references/playbooks/paid-search/conversions-cpa-and-return.md" in 03-diagnose-and-playbooks.md): How do I tell whether a paid click actually pays back
- Device and timing (section "File: diagnose/references/playbooks/paid-search/device-and-timing.md" in 03-diagnose-and-playbooks.md): When and how should device, day-part, and geo bid adjustments come into play
- Budget pacing (section "File: diagnose/references/playbooks/paid-search/budget-pacing.md" in 03-diagnose-and-playbooks.md): How do I catch over- or under-spend while there is still budget left to move

## paid-social

- Paid social performance (section "File: diagnose/references/playbooks/paid-social/paid-social-overview.md" in 03-diagnose-and-playbooks.md): How do you read a paid social account so prospecting and retargeting are judged on the jobs they actually do

## product-management

- What product management actually is (section "File: diagnose/references/playbooks/product-management/what-product-management-is.md" in 03-diagnose-and-playbooks.md): What does a product manager own, and how is it different from product development?
- Screening opportunities before you build (section "File: diagnose/references/playbooks/product-management/screening-opportunities.md" in 03-diagnose-and-playbooks.md): How do you decide which product ideas deserve investment, and which to kill early?
- Discovering customer needs (section "File: diagnose/references/playbooks/product-management/discovering-customer-needs.md" in 03-diagnose-and-playbooks.md): How do you find out what customers actually need, including what they can't articulate?
- Generating and selecting concepts (section "File: diagnose/references/playbooks/product-management/generating-and-selecting-concepts.md" in 03-diagnose-and-playbooks.md): How do you go from a pile of ideas to the one concept worth building, without groupthink?
- Validating concepts with data (section "File: diagnose/references/playbooks/product-management/validating-with-data.md" in 03-diagnose-and-playbooks.md): How do you test whether people would actually buy, and which features they would pay for?
- Defining the product: the modern PRD (section "File: diagnose/references/playbooks/product-management/defining-the-product.md" in 03-diagnose-and-playbooks.md): How do you write a product definition that aligns a team without prescribing the solution?
- Prototyping to learn, not to impress (section "File: diagnose/references/playbooks/product-management/prototyping-to-learn.md" in 03-diagnose-and-playbooks.md): What should you prototype, at what fidelity, and what is each prototype for?
- Building the business case (section "File: diagnose/references/playbooks/product-management/building-the-business-case.md" in 03-diagnose-and-playbooks.md): How do you prove, before major investment, that a product can become a viable business?

## seo

- Reading SEO performance stage by stage (section "File: diagnose/references/playbooks/seo/seo-overview.md" in 03-diagnose-and-playbooks.md): How do you judge SEO performance beyond a single traffic number
- Read your organic search in order (section "File: diagnose/references/playbooks/seo/insight-roadmap.md" in 03-diagnose-and-playbooks.md): In what order should you read organic search data so each answer narrows the next question
- Query-level data: why aggregates mislead (section "File: diagnose/references/playbooks/seo/query-level-data.md" in 03-diagnose-and-playbooks.md): What does the aggregate organic number hide, and at what level does the truth live
- Landing-page performance: earning the impressions (section "File: diagnose/references/playbooks/seo/landing-page-performance.md" in 03-diagnose-and-playbooks.md): Which pages earn the impressions they get, and which waste them
- New and newly ranking pages (section "File: diagnose/references/playbooks/seo/new-and-newly-ranking-pages.md" in 03-diagnose-and-playbooks.md): How do you catch emerging organic demand before it converts
- Organic clicks and on-site behavior (section "File: diagnose/references/playbooks/seo/organic-and-on-site-behaviour.md" in 03-diagnose-and-playbooks.md): Does the organic click pay back once it lands
- Organic and paid overlap: the content gap (section "File: diagnose/references/playbooks/seo/organic-paid-overlap.md" in 03-diagnose-and-playbooks.md): Which demand converts in paid search that organic could win for free
- Search Console: build a query worklist (section "File: diagnose/references/playbooks/seo/search-console-queries.md" in 03-diagnose-and-playbooks.md): How do you turn Search Console query data into this month's SEO worklist
- Search Console: coverage gaps and the snippet shortlist (section "File: diagnose/references/playbooks/seo/search-console-landing-pages.md" in 03-diagnose-and-playbooks.md): Which pages need work, and what work
- Search Console: newly ranking pages into a content plan (section "File: diagnose/references/playbooks/seo/search-console-new-pages.md" in 03-diagnose-and-playbooks.md): Where is new organic demand appearing, and what should you build
- Search Console and GA4: find your CRO windows (section "File: diagnose/references/playbooks/seo/search-console-and-ga4.md" in 03-diagnose-and-playbooks.md): Where is organic traffic being wasted on-site
- Search Console and paid search: mine content bets (section "File: diagnose/references/playbooks/seo/search-console-and-sem.md" in 03-diagnose-and-playbooks.md): What should next quarter's content target, backed by conversion evidence

## web-analytics

- Reading the marketing funnel end to end (section "File: diagnose/references/playbooks/web-analytics/marketing-funnel-overview.md" in 03-diagnose-and-playbooks.md): How do you read a marketing funnel from awareness to action and find where it leaks
- The on-site funnel in GA4 (section "File: diagnose/references/playbooks/web-analytics/on-site-funnel.md" in 03-diagnose-and-playbooks.md): How do you read on-site behavior from session to revenue, and where does the money leak
- GA4 fundamentals, ranking channels by quality (section "File: diagnose/references/playbooks/web-analytics/ga4-fundamentals.md" in 03-diagnose-and-playbooks.md): Which channels actually earn engaged, buying traffic, not just the most sessions
- UTM tagging (section "File: diagnose/references/playbooks/web-analytics/utm-tagging.md" in 03-diagnose-and-playbooks.md): How do you group one campaign across every channel and trace it from click to revenue

---

## File: diagnose/references/playbooks/attribution-experiments/attribution-and-mmm.md

---
title: Attribution and marketing mix modelling
question: How do you get from a last-click ROAS floor to an estimate of what each channel truly contributed
order: 1
---

A measured, last-click return (the on-site value your analytics recorded per line, against what it cost) is honest and comparable across channels, but it is a floor. Awareness and upper-funnel channels earn much of their sale through a later search or direct visit, and last-click credits that final step, not the reach that started the journey. To see what each channel actually contributed, you model the data.

## The framework

1. **Start from a clean spend-and-outcome table**: one row per campaign, reconciled across sources by campaign name, with cost, impressions, and clicks per line; the recorded on-site value (key events, transactions, revenue) matched to the same line; all of it drillable from account service down through account, campaign type, and campaign, over time. That tidy table is exactly what an attribution or mix model consumes.
2. **Understand what each model adds.** A data-based attribution model spreads a sale's credit across the touches that actually moved the buyer, instead of handing everything to the final one. A marketing-mix model goes further: it estimates how sales respond to spend per channel over time, including awareness reach that never earns a click at all.
3. **Pick the model for the shape of the business.** There is no single right model; the appropriate approach depends on factors like sales cycle, channel mix, and data granularity, and different business shapes call for different (often Bayesian) formulations.
4. **Keep the division of labor honest**: the data layer assembles the measured floor and the modeling input; choosing the model, setting the priors, and reading the result is analytical work done on top of it.

## Metrics that matter, and their traps

- **Last-click ROAS per campaign**: the measured floor and the model's calibration point. Trap: treating the floor as the verdict and cutting the upper-funnel lines it structurally understates.
- **Multi-touch attributed credit**: a fairer split of recorded touches. Trap: it still only sees recorded touches, and it is credit reassignment, not causal proof.
- **MMM channel-response estimates**: the only observational read that includes click-less reach. Trap: presenting a model's estimate with false precision; it is an estimate to validate against experiments, not a measurement.

## Interview prep

**"What data would you need to stand up a mix model?"**
A per-campaign, per-period table of spend and recorded outcome value, reconciled across every paid channel on one denominator, with enough history and spend variation for the model to learn from. A strong candidate flags that inconsistent campaign naming or platform self-reported conversions poison the input.

**"When is multi-touch attribution enough, and when do you need MMM?"**
Multi-touch helps when the journey is digitally tracked end to end; MMM is needed when meaningful contribution never earns a click (display, video, offline) or when tracking loss breaks the touch record. They are complements, not competitors.

**"How do you know your model is right?"**
You do not know, from the model alone; attribution is credit, not proof. Validate against controlled experiments where possible, and treat a model whose estimates keep contradicting holdout tests as miscalibrated.

---

## File: diagnose/references/playbooks/attribution-experiments/controlled-experiments.md

---
title: Controlled experiments for ad effectiveness
question: How do you prove an ad actually caused sales, rather than harvesting buyers who would have bought anyway
order: 2
---

A dashboard can say a campaign converted at 10%; it cannot say how many of those shoppers would have bought anyway, because a dashboard only records the world that happened. A randomized controlled experiment, run in the ad platform's own experiment tools, supplies the counterfactual, and for awareness spend whose sale closes days later through a search or direct visit, it is the only method that settles the causal question.

## The framework

1. **Respect the natural-buyer trap.** Regular customers buy after seeing an ad that changed nothing. Worse, comparing ad-viewers against non-viewers is biased by design: platforms aim ads at the people most likely to buy, so a 20% vs 9% gap proves targeting, not effect.
2. **Build the PSA holdout.** Split one target audience at random: treatment sees the branded ad; control sees a neutral public service announcement in the same slots. The PSA is a receipt: it proves the control shopper was actually reachable, and the neutral spend is the fee for a clean answer.
3. **Count shoppers, not clicks**, across an impression-based attribution window, so a control shopper who buys days later via search still counts to the control baseline.
4. **Read lift, not the raw gap**, then convert to incremental conversions and incremental value.
5. **Check balance, then segment.** Verify the randomization held, then break the average down by day, device, and frequency, and confirm eye-catching splits formally before betting budget on them.

## Metrics that matter, and their traps

- **Lift**: (treatment rate − control rate) / control rate. A 9.0% control against a 20.3% treatment is not "up 11 points"; it is +125% against the natural baseline. Trap: raw point gaps flatter small numbers.
- **Incremental conversions**: treatment conversions minus (control rate × treatment size). If 400 treated shoppers convert 81 times against a 9% baseline (~36 natural buyers), the ad caused ~45. Trap: banking all 81 as the campaign's work.
- **Incremental value**: the recorded on-site value of those incremental orders. Trap: calling it profit; that needs margin data.
- **Balance-check p-values**: high is good news: above 0.05 means the groups are indistinguishable on that variable, so the ad is the only explanation left for the gap.
- **Segment lift**: averages hide sign flips: an ad can run +188% lift on weekdays and roughly zero on weekends. Frequency follows an inverted U, negligible at 1–10 exposures, peaking mid-range, sagging where the ad reads as spam. Trap: comparing segments on raw rate gaps, and trusting a dramatic split before it clears significance.

## Interview prep

**"Ad viewers converted at 20%, non-viewers at 9%. The ad works, right?"**
No, the platform hand-picked the viewers for intent, so the crowds were never comparable. A strong candidate proposes a randomized holdout, where random assignment makes the ad the sole difference between groups.

**"Why show the control group a PSA instead of nothing?"**
The PSA proves the control shopper was online and reachable in that slot, keeping the groups comparable moment for moment. With "nothing" you cannot distinguish a genuine non-converter from someone who was never advertisable, and the PSA cost is the price of the clean answer.

**"Your test shows +125% average lift. What do you check before reporting it?"**
Balance first (the split held on age, prior purchases, visit depth), then segments: where lift is at or below zero the ad is not working, and where a split looks dramatic, a formal test decides whether it is proven or merely suggestive.

**"How would you use an experiment to set a frequency cap?"**
Read lift by exposure band and find the inverted-U peak: too few exposures and nobody notices, too many and you pay to annoy people already sold.

---

## File: diagnose/references/playbooks/competitive-research/competitive-and-keyword-research.md

---
title: Keyword research and competitive analysis
question: How do I decide which search demand is worth chasing before spending on it
order: 1
---

Every other discipline measures effort already committed: the email sent, the page built, the budget spent. Keyword research and competitive analysis come first: they decide which demand is worth chasing and who already owns it. Get this stage right and everything downstream is efficient; get it wrong and you spend the year capturing demand that was never going to pay back.

## The framework

One job: which demand exists, who owns it, and where is the gap you can take?

1. **Sort candidate queries by depth of intent.** Informational ("what coat for a cold commute") is high volume, low purchase intent. Comparison ("best white t-shirt that lasts") is researchers building a shortlist. Transactional ("wool overcoat sale") is low volume, high intent, usually worth bidding on. Cover the full depth: rank only for transactional and you starve the pipeline; rank only for informational and you collect traffic that never buys.
2. **Score each query on four factors**: intent (which depth), volume (monthly demand, from keyword-planner data), competition (can you realistically rank or bid), and your current ranking. Current ranking is the highest-leverage factor most teams skip. A query you already sit in positions four to twenty for is one push from clickable territory, worth more than a bigger term started from scratch.
3. **Build the competitive keyword gap** (the to-do list): high-volume queries where you have impressions but no clicks or rank, and terms the field is visible for that you are absent from. It plans next quarter's content and names the auctions worth contesting now.
4. **Cluster, do not list.** A flat sheet of 4,000 keywords is noise; grouped by intent and theme, the demand themes worth a quarter's work surface on sight.

## Metrics that matter, and their traps

- **Search volume**. Trap: intent first, volume second. A 50,000-search informational term is worth less to a small site than a 2,000-search transactional one it can actually rank for and convert.
- **The long tail**. Roughly 70% of all searches are long-tail ([Ahrefs](https://ahrefs.com/blog/long-tail-keywords/)). Lower volume, lower competition: where a smaller site wins.
- **Position**. The top three organic results take 68.7% of clicks, so targeting decides most of the outcome before a page is written. Trap: chasing fat-head keywords dominated by high-authority players when you are small; that effort is sunk.
- **Share of voice vs share of market**. Never read voice alone; 30% is dominant in a fragmented field and feeble in a duopoly. Binet and Field's rule: voice above market share primes future gains; voice below it means share is quietly at risk.

## Interview prep

**"How would you build next quarter's keyword target list?"**
A strong candidate gives the four-factor frame (intent, volume, competition, current ranking), covers all three intent depths, and starts from queries already ranking in positions 4–20 as the cheapest wins.

**"Our CPCs on core terms keep creeping up. What is the competitive read?"**
Crowding auctions. They look for terms competitors bid on where you have zero impression share (demand bought around you) and use the gap list to decide which auctions to contest versus concede. The same gap explains creeping CPC on your existing terms.

**"A term has 50,000 monthly searches. Do we go after it?"**
Not on volume alone. What is the depth of intent, who holds the top three, and where do you rank today? Often the honest answer is a cluster of capturable long-tail variations.

**"How do you judge whether the brand is investing enough in visibility?"**
Share of voice against share of market: voice ahead of market share is the leading edge of growth; trailing it is decline you can still see coming.

---

## File: diagnose/references/playbooks/competitive-research/marketing-personas.md

---
title: Marketing personas that earn their keep
question: How do you build a persona that is worth spending real budget against
order: 2
---

Most personas are invented from a demographic and a stock photo, then quietly ignored because nobody believes them. The useful ones are built the other way round: segment the market on how people actually behave, choose which segments are worth serving, describe the person at the heart of each, then prove that person against what your marketing actually converts.

## The framework

A persona is the profile of a typical customer in a segment you have deliberately chosen to serve. It is the last step of a chain, not the first:

1. **Segment**. Split the market into groups with distinct needs. Four bases: geographic, demographic (age, income, life stage), psychographic (values, interests), behavioral (benefits sought, usage, loyalty). Behavioral predicts purchase: start from the benefit a person is buying, then use the others to sharpen the picture.
2. **Target**. Rank segments by attractiveness (size, growth, competitive crowding, fit with what you are actually good at) and sort into tiers: the primary segment you build for first, a secondary you keep warm, the rest set aside.
3. **Profile**. Describe the person at the center of each chosen segment: demographics, values, how and how often they buy, and above all the benefit they are really after. Each profile should read as a targeting instruction: a durability-led repeat buyer is an in-market, retargeting-friendly audience; a style-led occasion buyer is an affinity and seasonal-campaign audience. Two personas, two different media buys, from one catalog.
4. **Prove**: the step most persona decks never take. A whiteboard persona is a hypothesis; what actually converts, by audience, campaign, product, and repeat rate, either confirms it or quietly retires it.

## Metrics that matter, and their traps

- **Demographic fit**: popular because it is easy to measure. Trap: people break their demographic mold; demographics alone are rarely predictive of what someone will buy.
- **Benefits sought and usage rate**: the behavioral signals that actually predict purchase. Rule of thumb: a small share of customers usually drives most of the value, so a persona that ignores how heavily someone buys misses the customers who matter most.
- **Conversion and repeat rate by audience**: the evidence that separates a data-backed profile from a flattering story. A persona you can measure is a targeting instruction; one you cannot is a character.
- **The average customer** (the flaw of averages): a persona built for the average satisfies no one, because the average customer does not exist. Build sharply for the primary segment instead.

## Interview prep

**"Marketing hands you three personas from a workshop. How do you evaluate them?"**
A strong candidate asks what segmentation they came from (behavioral or just demographic) and tests each against performance data: does an audience matching this profile actually convert and repeat? Personas untraceable to converting behavior are hypotheses, not assets.

**"Which segmentation base matters most, and why?"**
Behavioral (benefits sought, usage, loyalty) because it predicts what people will buy. Demographics and geography sharpen the picture but rarely carry it alone.

**"Why not build one persona for our typical customer?"**
The flaw of averages: the average customer does not exist, so a persona built for them satisfies no one. Segment first, then build sharply for the primary segment.

**"How do personas translate into an actual media plan?"**
Each persona is a targeting instruction: which audience type, which channels, which message. If a persona does not change who you reach or what you say, it is decoration.

**"When would you retire a persona?"**
When the behavioral evidence says so: a segment that never converts or repeats gets demoted before it eats more budget, however good its story was.

---

## File: diagnose/references/playbooks/customer-analytics/clv-vs-cac.md

---
title: Customer lifetime value vs CAC
question: How do you compare what a customer is worth against what they cost, honestly
order: 1
---

Every business wants one number: what is a customer worth? Spend less to win them than they bring you over time and you grow; spend more and you slowly bleed out. Most teams treat lifetime value as a fact to look up. It isn't: in a non-subscription business it is a guess about silence, and treating the guess as fact is how teams overpay for acquisition.

## The framework

1. **Understand the unknowable half.** Customer value is spend per order, times how many more times they buy, minus cost to serve (future money discounted). The first half is receipts; the second is the problem. A subscriber cancels; a shop customer just goes quiet, and the same three months of silence could mean "gone" or "between purchases." Every LTV number is a particular guess about what that silence means.
2. **Fence the guess.** The floor is the margin a customer has actually generated to date, money in the bank. The ceiling assumes the relationship runs forever. Report floor, ceiling and your honest estimate between them, so no single number poses as the truth. Ceiling-only reporting manufactures phantom value; floor-only reporting starves your best channels.
3. **Keep worth and cost at their honest levels.** Worth is personal: one customer's spend can be traced and totaled. Cost is shared: a campaign buys a crowd (some who would have come anyway, some nudged, some free via word of mouth), so a per-person acquisition price is a number you invented and then rounded. CAC is only real for a group won in the same stretch of time: total spend over the crowd it brought in. The honest question is never "did this customer pay back?" but "did the group we won in March pay back, and how fast?"
4. **Pick the number by the decision.** "How much can I afford to spend to acquire?" wants a near-term, conservative figure; "what is our loyal base strategically worth?" wants a longer, carefully discounted one. Letting the decision choose the horizon dissolves the which-formula-wins argument.
5. **Backtest before you trust.** Hide the last year of data, ask the model to predict it, compare. A model that cannot retro-predict the past has no business forecasting the future.

## Metrics that matter, and their traps

- **Realized margin to date (the floor):** the only assumption-free customer value. Trap: under-investing because you ignored real future value.
- **Projected LTV (the estimate):** only as good as its churn assumption. Trap: the classic one-steady-churn-rate-forever formula, undiscounted (the ceiling wearing an estimate's clothes).
- **CAC:** total spend over customers won, per group and period. Trap: dragging it down to the individual, which manufactures precision that was never there.
- **LTV:CAC ratio:** meaningful only when both sides are computed at their honest level (group worth against that same group's spend) and matched in horizon.
- **Cohort payback period:** the month a group's accumulated margin repays what it cost to win. The cleanest, most decision-ready form of the comparison, with no invented per-person cost anywhere.

## Interview prep

**"Our dashboard says LTV is €340. Is that a fact?"**
A strong candidate asks which assumption about silence produced it (what churn model, what horizon, discounted or not) and where it sits between the realized floor and the never-churn ceiling.

**"Finance wants CAC per individual customer to compare against their order history. Do you build it?"**
No: cost is shared across a crowd; any per-person allocation is invented. They reframe to the cohort: this group's total worth against this group's total spend, and payback in months.

**"Two teams computed LTV and got numbers 3x apart. Who is right?"**
Probably both, for different questions: one a near-term acquisition-budget number, the other a long-horizon strategic one. Match each number to its decision instead of crowning a formula.

**"How would you validate an LTV model before putting it in the plan?"**
Holdout backtesting: hide a year, predict it, compare. The method that survives earns the headline; the others stay as second opinions with their assumptions stated.

---

## File: diagnose/references/playbooks/customer-analytics/cohort-analysis.md

---
title: Cohort analysis, measure before you model
question: When should you model customer value, and when should you simply measure it
order: 2
---

Once a team accepts that lifetime value is a guess, the instinct is to reach for a better guess: more model, more parameters, applied to every customer on the books, including the ones who were never silent in the first place. That is the trap. Whether you can know a customer's future comes down to how often they tell you they are still there, and the method should be decided by that signal density before any math.

## The framework

1. **Sort customers by how loudly they tell you they are there.** Three settings: **contract** (subscription customers: they pay every cycle and cancellation is an event with a date; lifetime is bookkeeping), **heartbeat** (replenishment buyers: coffee, pet food, skincare on a rhythm; nobody cancels, but a stopped drumbeat is loud all by itself), and **silence** (considered purchases: apparel, furniture, a coat every other winter; quiet between orders means two opposite things you cannot tell apart).
2. **Measure where the signal is dense; model only where it is sparse.** A subscriber's lifetime is read off renewal history; a replenishment buyer's churn is watched in the order rhythm. Only the genuinely silent customer needs buy-till-you-die mathematics. A fancy model applied to data you could have counted isn't rigor: it replaces a fact you owned with an estimate you invented, and a measured number you can defend beats a modeled one you have to caveat.
3. **Measure the flow, not just the pulse.** A heartbeat can keep beating while the customer quietly leaves: the coffee order still arrives, so "are they active?" says yes, but the gap has stretched from three weeks to six and the basket is half the size. Meaningful churn in a split-wallet business is erosion, not a clean death.
4. **Read the shape of the decline, because it names the action.** Quiet every summer is seasonal, not lost. A drop that starts with a refund or support ticket is a fixable experience problem. Steady erosion with no incident is a competitor eating your lunch. A hard stop is a goodbye. Four futures, four actions.
5. **Keep the guess and the fact in different boxes.** A measured lifetime and an inferred one aren't the same kind of number; never average them into one figure that hides which is which.

## Metrics that matter, and their traps

- **Repeat rate by cohort:** holding cohort after cohort is health; slipping a little with every cohort is quiet erosion. Trap: one pooled rate hides the trend.
- **Order frequency (gap between orders):** a stretching gap is churn in progress that an activity flag will never show.
- **Average order value:** a still-"active" customer with shrinking baskets has moved their wallet elsewhere. Trap: counting them as retained.
- **"Active customer" flags:** the easy question ("are they alive?") and the wrong one. The real question is "how much of them do we still have?"
- **Modeled LTV on dense-signal customers:** a red flag in itself: if the order history could answer the question by counting, the model is dressing a fact as an estimate.

## Interview prep

**"Would you build a probabilistic churn model for our subscription customers?"**
No: subscribers have a cancel event; lifetime is read off renewals. A strong candidate reserves modeling for silent, considered-purchase customers: the simplest honest method the signal allows wins.

**"Retention looks fine, 80% of last year's customers are still active. What is wrong with that read?"**
It measures the pulse, not the flow. They would check order frequency and basket size by cohort: customers can stay "active" while wallet share erodes to a competitor.

**"A replenishment customer's orders went quiet for three months. Lost?"**
Depends on the shape: seasonal quiet recurs on schedule; a stop after a refund is an experience problem; steadily stretching gaps suggest a competitor. Each future gets a different action.

**"How do you present measured and modeled customer value together?"**
In separate, labeled boxes (measured lifetimes for contract and heartbeat customers, modeled estimates with stated uncertainty for the silent), never averaged into one figure that hides which is which.

---

## File: diagnose/references/playbooks/customer-analytics/reading-acquisition-quality.md

---
title: Reading acquisition quality with cohorts
question: Did the customers a given month's marketing bought actually turn out to be good ones
order: 3
---

Repeat purchase rate drops two points and the room splits into two camps: retention is decaying, or nothing is wrong and the store simply acquired a big batch of new customers who have not had time to come back yet. A pooled average cannot tell those stories apart. Cohort analysis can: group customers by the month of their first purchase, follow each group forward, and the blend resolves into curves you can act on. The stakes are real: improving retention 5% lifts profits 25-95%, and acquiring a customer costs five to twenty-five times keeping one ([HBR, on Bain's research](https://hbr.org/2014/10/the-value-of-keeping-the-right-customers)).

## The framework

The discipline has one canonical shape: the cohort matrix. Rows are acquisition months, columns are months since first order (cohort age), cells hold retention or revenue at that age.

1. **Compare down the columns, never across the diagonal.** Every comparison must be at matched age: month three against month three. A two-month-old cohort against a year-old one is a sapling against a tree.
2. **Beware the composition trap.** A pooled metric is a blend of cohorts at different ages; it moves when the mix moves even if no customer changed behavior. A fast-growing store is mostly month-zero customers, so its blended repeat rate falls while every individual cohort improves.
3. **Watch the plateau, not the first month.** Nearly every retention curve cliffs after the first purchase, then flattens. The height of that flat section is the loyal core: a cohort that settles at 12% is worth dramatically more than one settling at 6%, even from the same month-one start.
4. **Read quality in the first ninety days.** Month-one and month-three repeat behavior at matched age tells you early whether a campaign bought customers who come back. Read each cohort's early curve next to that month's acquisition spend, and marketing gets judged on cohort quality, not size.
5. **Compare seasons to seasons.** A December cohort is acquired by gifting demand (bought once, for someone else) and will always retain worse than October's. The honest year-over-year read is December against last December, at matched age.

## Metrics that matter, and their traps

- **Retention rate by cohort age:** the curve itself. Trap: reading young cohorts' empty cells as decline; they have not lived long enough.
- **Repeat purchase rate, cohort over cohort:** the earliest acquisition-quality signal. Trap: the pooled version, which the composition trap owns.
- **New vs returning revenue mix:** the context that defuses the trap: how much of this month's revenue is fresh acquisition versus the base you own.
- **Revenue per customer by cohort age:** what a cohort is worth as it matures; the value half of payback.
- **Cohort payback period:** the month cumulative revenue per customer crosses acquisition cost. Its trend is the most decision-ready number here: payback stretching from three to six months is the earliest warning that growth is being bought at quality's expense.
- **First order value and full-price share:** do discounted first orders build cohorts that return, or cohorts that only bought the discount?

## Interview prep

**"Blended repeat rate fell two points this quarter. Retention problem?"**
A strong candidate names the composition trap before conceding a problem: fast acquisition dilutes the blend with month-zero customers. They re-read repeat rate down the cohort columns at matched age, plus the new-vs-returning mix.

**"How soon can you judge whether last month's campaign bought good customers?"**
Within ninety days: month-one and month-three repeat behavior at matched age against older cohorts, read next to that month's spend. No need to wait a year.

**"December's cohort retains worse than October's. Is acquisition quality falling?"**
Probably seasonality: gift buyers behave like gift buyers. The fair comparison is December against last December at matched age; only a decline there signals real quality loss.

**"What single cohort number would you show the CFO?"**
Cohort payback period and its trend: it bridges customer behavior to spend with no invented per-customer cost anywhere in it.

---

## File: diagnose/references/playbooks/email-marketing/click-to-revenue.md

---
title: From the click to the revenue
question: How do you know what an email campaign actually earned, not just what it got clicked
order: 6
---

The click is the last thing an email platform can see. When a reader clicks, they leave the inbox and land on the site, and from that moment the story belongs to web analytics: the session, the transaction, the revenue. Put the two sides together (reconciled per campaign on the campaign name the link carried) and the funnel finally closes on the only question a finance director asks about email: what did it make?

## The framework

1. **Reconcile per campaign.** The campaign name the email platform stamped on the send must match the name web analytics reads off the link the visitor followed. That reconciliation turns a click count into a revenue figure.
2. **Read each send's pull next to what it earned** (clicks and CTOR on one side; sessions, transactions, revenue and revenue per purchaser on the other) and hunt for divergence, because clicks and revenue do not move together.
3. **Judge the send on revenue, not clicks.** Worked example: a whole-list clearance blast pulls ~3,600 clicks and earns ~£1,540 at ~£70 per purchaser; a tight new-arrivals segment pulls ~1,050 clicks and earns ~£5,760 at ~£120 per purchaser. Judged on clicks, you would protect the blast and question the segment: precisely backwards.
4. **Tag every link.** Revenue only ties to a send where UTM tags make the campaign name reconcile on both sides. Where tagging drifts, buyers arrive looking like ordinary traffic and revenue lands in a nameless bucket. Nothing breaks; money just goes uncredited to the work that earned it. See the UTM tagging playbook.

## Metrics that matter, and their traps

- **Email-attributed revenue**: the on-site revenue credited back to the send whose link carried the visitor. The trap: coverage depends entirely on tagging discipline; untagged links understate a send's true earnings.
- **Sessions from a send**: the first thing web analytics records after the click. Sessions running a little under clicks on every row is the normal signature of imperfect tagging; a large gap on one send flags a broken or untagged link.
- **Transactions and revenue per send**: the verdict metrics. The trap: ranking sends by clicks, which rewards low-intent crowd-pullers and punishes sharp offers to small segments.
- **Revenue per purchaser**: revenue / transactions. Separates a fat-basket send from one whose visitors bought the cheapest thing. A high-click, thin-basket send is a promise the landing page or offer did not keep.
- **Attribution coverage**: the share of email revenue that reconciles to a named send. It rises with tagging discipline and never depends on the reporting tool.

## Interview prep

**"Your best-clicking campaign earned the least revenue. Explain how that happens and what you would do."**
A strong candidate reads it as low-intent volume: a broad discount blast pulls curiosity clicks that bounce or buy the cheapest item. They check revenue per purchaser and landing-page match, then either tighten the audience or fix the offer-to-page promise before killing the send.

**"How would you prove email's revenue contribution to a skeptical CFO?"**
They describe the per-campaign reconciliation: tagged links carry the campaign name into web analytics, so each send lines up with the sessions, transactions and revenue it produced. They also disclose coverage honestly: untagged clicks mean the figure is a floor, not the total.

**"Some sends show clicks but zero revenue. Is email failing?"**
First hypothesis is instrumentation, not performance: untagged or mistyped links make buyers arrive as ordinary web traffic. They audit tag coverage before judging the sends.

**"Marketing celebrates clicks; finance only counts orders. Which is right?"**
Both, in sequence: clicks tell you attention showed up; revenue tells you the attention was worth having. A send is a bet that attention turns into money, and only the revenue side settles the bet.

---

## File: diagnose/references/playbooks/email-marketing/deliverability-and-inbox-placement.md

---
title: Deliverability and inbox placement
question: Why are my emails not reaching the inbox, and what do I fix first
order: 3
---

Deliverability is the gate every other email number sits behind: the share of what you sent that actually arrived. Get it wrong and every downstream rate measures a smaller, quieter audience than you think, because opens and clicks can only count the people the email reached. A brilliant campaign delivered to 88% of the list is not a brilliant campaign; it is a reputation problem wearing a good open rate.

## The framework

Hold delivery above 95%. When it slips, three causes drag it down, and you work them in this order:

1. **Authentication gaps: binary, fix once.** SPF (which servers may send for your domain), DKIM (a cryptographic signature per message), and DMARC (the policy when the first two fail). Google and Yahoo [made all three mandatory for bulk senders](https://support.google.com/a/answer/14229414) in February 2024; a domain missing any of them is filtered or rejected outright. Set the records, confirm each actually passes.
2. **A dirty list: ongoing hygiene.** Dead addresses announce themselves through bounces. Hard bounces go onto a suppression list the moment they bounce; use a list-verification service to flag invalid addresses proactively instead of learning from the bounce.
3. **Complaints: a relevance problem.** A complaint-tripped filter is the fastest way to lose the inbox. The fix is fewer, better-targeted sends, never more volume through a cracking reputation.

Then quarantine risk: pull long-dormant subscribers (no open or click in ~12 months) into their own segment, run a dedicated win-back campaign, and delete the non-responders. Dormant addresses turn into spam traps; their risk never belongs inside the main send.

## Metrics that matter, and their traps

- **Deliverability rate** (delivered / sent): hold above 95%. The trap: reading anything downstream before this gate holds; a leak here shrinks the base every other rate is computed on.
- **Bounce rate**: keep under 2%. The trap is watching the level instead of the trend: a bounce rate rising while send volume holds steady is the early warning that hygiene has lapsed, long before delivery itself falls through the floor.
- **Complaint rate**: 0.1% is a warning shot; 0.3% is critical and gets your domain throttled or blocked. Complaints almost always mean a consent or frequency problem, not a creative one.
- **Authentication pass status**: not a rate, a checklist; SPF, DKIM, DMARC each verified as passing. The trap is assuming a published record validates.
- **Win-back send performance**: read the dormant segment on its own. Blended into the main campaign, a risky segment hides its true bounce and complaint rates inside a healthy average.

## Interview prep

**"Deliverability dropped from 97% to 90%. Walk me through your triage."**
Strong candidates go in cause order: verify SPF/DKIM/DMARC pass (binary, cheapest fix), then check the bounce trend at steady volume (hygiene), then complaint rate against 0.1%/0.3% (reputation). They explicitly refuse to discuss subject lines until the gate holds.

**"Marketing wants to re-mail the whole lapsed list to hit a revenue target. What do you say?"**
They flag the reputation risk: dormant addresses carry high bounce and complaint rates and some are spam traps. The compromise is a quarantined win-back segment with a dedicated offer, then deleting non-responders, containing the risk away from the engaged list.

**"Is cleaning 3,000 dead addresses off the list losing audience?"**
No. Those addresses were never reachable revenue, and mailing them is exactly what convinces providers the list is stale. Cleaning protects the deliverability of the audience that is still listening.

**"What changed for bulk senders in February 2024?"**
Google and Yahoo made SPF, DKIM and DMARC mandatory and enforce explicit complaint thresholds. Authentication moved from best practice to a hard requirement; unauthenticated bulk mail is now rejected, not just disadvantaged.

---

## File: diagnose/references/playbooks/email-marketing/email-marketing-overview.md

---
title: Email marketing, from send to revenue
question: How do you judge whether an email program is actually working
order: 1
---

Email is the highest-return channel a company owns, around $36 back per dollar spent ([Litmus](https://www.litmus.com/resources/email-marketing-roi)), because it reaches an audience you already own and can contact again for nothing. But one headline number hides which step is failing, and the most dangerous account is the one whose per-send metrics look fine while the list underneath quietly shrinks.

## The framework

Read an email program as a sequence, in this order, because each answer sets up the next:

1. **Deliverability first.** Are sends even reaching the inbox? Nothing downstream counts if delivery slips below 95%.
2. **The send funnel.** Sent → delivered → opened → clicked. Localize which transition leaks; each has a different cause and fix.
3. **Engagement and the click.** Judge campaigns on clicks, never opens: an open only says the message surfaced; a click proves intent.
4. **List health.** Is the list growing on net, and are complaints and opt-outs inside safe bounds? The list is the asset every send either compounds or erodes.
5. **Click to revenue.** Follow the click on-site to sessions, transactions and revenue, and judge the send on what it earned.

Across every step, lifecycle beats blast: segmented, automated flows out-convert one-size-fits-all sends because they reach the subscriber at a known moment.

## Metrics that matter, and their traps

- **Deliverability rate** (delivered / sent): the gate. Hold above 95%; below it, stop optimizing subject lines and fix authentication, hygiene or reputation instead.
- **Bounce rate**: keep under 2%. The trap: a bounce rate climbing while volume holds steady is the early warning of lapsed list hygiene, well before delivery falls.
- **Open rate**: directional only. It fires on previews and image loads and privacy masking makes it noisier every year; watch the trend, never a single send's absolute value.
- **CTR** (clicks / delivered): roughly 2-5% per send. The trap: pooling it across sends of different sizes lets one big low-intent blast swamp the average.
- **CTOR** (clicks / opens): ~10% average, 14-17% in the strongest industries ([Campaign Monitor](https://www.campaignmonitor.com/resources/knowledge-base/what-are-good-email-metrics/)). Read at the program aggregate; it isolates message quality from open volume.
- **Unsubscribe rate**: keep under ~0.5% per send. Complaint rate alarms at 0.1% (warning) and 0.3% (critical, domain throttled or blocked).
- **Net list growth**: new minus unsubscribes minus cleaned, over the starting list. The trap: campaign rates only measure whoever is left. A 30,000-member list adding 800 and losing 650 a month is running to stand still, and no per-send metric will ever flag it.

## Interview prep

**"Our open rates are healthy but email revenue is flat. Where do you look?"**
A strong candidate refuses to treat opens as a verdict. They walk the sequence: check deliverability held above 95%, then CTR against the 2-5% band, then whether clicks convert on-site, then net list growth: a shrinking list keeps rates stable while the sellable audience contracts.

**"What single email metric would you put on a monthly dashboard, and why?"**
Not open rate. They argue for clicks (intent) plus net list growth (the asset), and explain that deliverability is a gate to alarm on, not a KPI to celebrate.

**"A send got a 0.2% spam complaint rate. What do you do?"**
They recognize this is past the 0.1% warning and heading toward the 0.3% critical line. The fix is less volume, not more: cut frequency, tighten segmentation, check consent; never push more sends through a cracking reputation.

**"Why do lifecycle flows out-perform promotional blasts?"**
They reason from relevance: a flow reaches a subscriber at a known moment (welcome, nurture, win-back), which lifts clicks and lowers complaints simultaneously; the same lever protects the list and grows it.

---

## File: diagnose/references/playbooks/email-marketing/engagement-and-the-click.md

---
title: Engagement and the click
question: How do you measure whether email content actually drove action
order: 4
---

An open only tells you a message surfaced in an inbox; it is ambient. The click is the signal that proves the content matched what the reader wanted, and it is the only part of engagement you can spend. Email engagement is really two questions wearing one label (how many people you reached acted, and how well the message worked on the people who saw it) and reading them at the wrong level is how engagement reports quietly lie.

## The framework

1. **Lead with the click.** Judge campaigns on clicks, never opens.
2. **Read click rate per send.** CTR (clicks / delivered) is reach-weighted: a 30,000-recipient catch-all at 1% contributes far more pooled weight than a 2,000-recipient segment at 6%, and the blend describes neither. Judge each send against the 2-5% band.
3. **Read click-to-open at the program aggregate.** CTOR (clicks / opens) conditions on the people who showed up, so it pools fairly and tells you whether bodies, offers and CTAs are broadly working, against the ~10% average, 14-17% in the strongest industries ([Campaign Monitor](https://www.campaignmonitor.com/resources/knowledge-base/what-are-good-email-metrics/), [Mailchimp](https://mailchimp.com/resources/email-marketing-benchmarks/)).
4. **Drill into individual sends.** A weak blast hides under a healthy aggregate: a program can post 13% CTOR while its biggest send (a 29,500-recipient weekly catch-all at 1.1% CTR) drags the pooled click rate to 1.6%. The fix is that one send: tighten its audience, sharpen its single CTA, or split it into the lifecycle segments the other sends already prove work.
5. **Match the lever to the rate.** Opens lagging: work the subject line, sender name and timing. Clicks lagging: work the body, offer, CTA and segment.

## Metrics that matter, and their traps

- **Click rate (CTR)**: clicks / delivered, the share of everyone reached who acted. Read per send against 2-5%. The trap: pooling across sends of wildly different sizes.
- **Click-to-open rate (CTOR)**: clicks / opens, message quality among openers. Read at the aggregate. The trap: judging a single small send's CTOR as a verdict, or letting a healthy aggregate excuse skipping the per-send drill-down.
- **Open rate**: directional only; a trend signal for subject line, sender name and timing, never an absolute score.
- **The lanes rule**: read a reach-weighted rate (CTR) per send, a quality rate that conditions on openers (CTOR) at the aggregate. Swapping the lanes is the most common way an engagement report misleads.
- **Divergence between the two**: a send with fine CTOR but low CTR worked on openers but was sent too broadly; narrow the audience rather than rewrite the message.

## Interview prep

**"Our program CTOR is 13%, above benchmark. Is engagement solved?"**
A strong candidate refuses the aggregate as a verdict and asks for per-send CTR. The bigger the weak blast, the harder the good sends work to disguise it; they hunt for the large send sitting under the 2-5% band.

**"Would you A/B test the subject line or the CTA first, and how do you decide?"**
They decide from the rates: open trend lagging means test the subject line, sender name or send time; opens fine but CTOR lagging means the message is the suspect: body, offer, single CTA, segment.

**"One send has 5% CTOR but a 1% CTR. What happened?"**
The message worked on the people who opened; the problem is reach or relevance to the wider list. The move is narrowing who receives it, not rewriting content that already converts its openers.

**"How would you report engagement to a CMO in three numbers?"**
Aggregate CTOR versus the ~10% benchmark (message quality), the worst large send's CTR versus the 2-5% band (the fix), and the click trend over time, with a one-line reminder that opens are excluded on purpose.

---

## File: diagnose/references/playbooks/email-marketing/list-health-and-reputation.md

---
title: List health and reputation
question: Is the list underneath my campaigns growing or quietly eroding
order: 5
---

Every per-campaign email rate is calculated over whoever is left on the list, so a program can read perfectly while the audience it is measured against shrinks every month. List health is the read that watches the asset itself rather than the campaigns drawn from it; the list is the one marketing asset you actually own and can reach again for nothing. Erode it and you are spending down the principal your returns compound on.

## The framework

1. **Track net list growth:** new subscribers minus unsubscribes minus cleaned addresses, over the starting list, read monthly. There is no universal "grow X%" benchmark; the signal is the trend against your own baseline and, above all, the sign. Worked example: a 30,000-member list adds 800 and loses 650 in March (+0.5%, running to stand still); two months later the list contracts at −0.2%, while every per-campaign rate reads unchanged.
2. **Guard the reputation alarms:** unsubscribe rate under ~0.5% per send is the healthy sound of a list self-selecting; complaint rate has hard lines at 0.1% (warning) and 0.3% (critical, domain throttled or blocked, per [Google's sender guidelines](https://support.google.com/a/answer/14229414)). When either drifts, cut frequency and tighten segmentation. Never push more volume through a cracking reputation.
3. **Grow with lifecycle, not louder blasts.** Automated flows (welcome, nurture, win-back) out-convert one-size-fits-all sends because they reach the subscriber at a known moment. Segmentation is the one lever that lifts growth and lowers complaints at the same time.

The two failures compound: a reputation slip drives deliverability down, which shrinks the delivered base every rate is measured over, which flatters the survivors and hides the erosion.

## Metrics that matter, and their traps

- **Net list growth**: positive and steady is the asset compounding; flat means acquisition only replaces attrition; negative is invisible revenue loss. The trap: no per-campaign metric will ever flag it, because opens and clicks only measure whoever remains.
- **Unsubscribe rate** (unsubscribes / delivered): the honest opt-out cost of a send; keep under ~0.5%. The trap: celebrating a low rate on a list that isn't growing; low churn on a stagnant list is still standing still.
- **Complaint rate**: scored by the provider, not by you. 0.1% warning, 0.3% critical. The trap: treating it as a creative problem; it is almost always consent or frequency.
- **Cleaned addresses**: removals of invalid or long-dormant subscribers. The trap: counting cleaning as loss; those addresses were dragging deliverability, not producing revenue.
- **Per-campaign rates as list proxies**, the composition trap of email: a shrinking list flatters engagement rates by leaving only the loyal behind.

## Interview prep

**"Every campaign metric has been stable for a year. Is the email program healthy?"**
A strong candidate asks the question the campaign report cannot answer: what did the list do? They compute net growth and check its sign, knowing stable per-send rates are fully compatible with a contracting sellable audience.

**"Unsubscribes spiked after we doubled send frequency. Keep the frequency for the revenue, or cut it?"**
They frame it as spending the asset: extra sends earn short-term revenue while attrition and complaint risk compound. They would check complaint rate against the 0.1% line, segment by engagement, and keep frequency only for segments that sustain it.

**"How do you grow a list without renting reputation problems?"**
Consent-first sourcing plus lifecycle segmentation: a welcome flow that sets expectations, and never mailing a day-one subscriber and a lapsed customer the same message. Bought or incentivized lists show up later as complaints and spam traps.

**"Which single number tells you the list is in trouble before revenue does?"**
The sign of net list growth flipping negative: months of reachable-audience loss show there before any revenue line moves.

---

## File: diagnose/references/playbooks/email-marketing/reading-the-send-funnel.md

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

---

## File: diagnose/references/playbooks/emerging/geo-getting-cited-in-ai-answers.md

---
title: Generative engine optimization: getting cited in AI answers
question: How do you earn citations inside AI-generated answers, and what can you honestly measure
order: 1
---

A growing share of discovery now ends inside an AI answer, not on a results page: someone asks ChatGPT, Google AI Overviews, Gemini, or Perplexity a question and gets a synthesized reply with a handful of sources named, often with no click to anyone's site. SEO earns a ranking; generative engine optimization (GEO) earns a citation: being the source the model quotes when it writes the answer. AI-referred sessions jumped 527% year over year in the first five months of 2025, off a tiny base, which is exactly when to start measuring.

## The framework

Getting cited rests on three levers, in this order: structure gets you parsed, authority gets you trusted, community grounds you in the model's sense of consensus.

1. **Authority: be the source worth quoting.** AI engines favor earned media (authoritative third-party sources) over brand-owned content. Press references, research citations, quotes from named experts: each teaches the model to treat you as quotable. The failure mode is pouring budget into a polished owned blog while staying absent from every source the model actually trusts.
2. **Community: show up where the model learns.** Models are grounded on where people genuinely discuss things: Reddit, forums, review sites, Q&A threads. A brand absent from the discussion is invisible to the answer, however good its own site looks. The move is participation, not a press release.
3. **Structure: make your content trivial to extract.** The lever you control fastest: answer first (the direct answer in the first 40-60 words of a section); question-style headings that phrase-match how people ask; bullet lists as liftable units; high fact density (a verifiable statistic every 150-200 words); schema markup and clean HTML. Every GEO structure rule is just good writing for a reader in a hurry; the page a skimming human loves is the page a skimming model lifts.
4. **Run GEO alongside SEO, never instead of it.** The pages that already rank are the pages models cite; the top three organic results take 68.7% of all clicks ([Backlinko](https://backlinko.com/google-ctr-stats)), and those same authoritative pages are disproportionately what engines retrieve and quote. One motion, not two budgets.

## Metrics that matter (and their traps)

Be honest: no platform has a clean citation-share metric yet. What you read today are proxies.

- **Branded query volume**: how often people search your name, the closest free GEO scoreboard you already own. When an AI mentions you, demand shows up here weeks before it shows as traffic. Trap: read its growth *relative to* non-branded, or general SEO gains masquerade as GEO wins.
- **Organic visibility on priority queries**: a top-three position is what makes a page citable. Your organic rank is now a leading indicator of citation odds, not just a search number.
- **AI-referral traffic**: the click-throughs that do happen, identified by referrer (chatgpt, perplexity, gemini). Trap: it undercounts the channel badly, because the defining GEO event is the zero-click impression: real reach, real exposure, no session in your analytics at all.
- **Citation share** is the true GEO metric: the share of relevant AI answers naming you. Not cleanly measurable anywhere today; any vendor claiming a clean count is overselling.

## Interview prep

**"How would you measure whether a GEO effort is working, given citations aren't directly trackable?"**
A strong candidate names the honest proxies (branded-query growth against non-branded, organic position on priority terms, and the AI-referral trickle) and states the zero-click measurement gap unprompted. Claiming a citation-share dashboard exists is the fail.

**"Is GEO a replacement for SEO?"**
No, one motion. Engines cite pages that already rank and carry authority, so the SEO investment is the eligibility ticket and GEO layers extraction-friendliness, earned media, and community presence on top.

**"What on-page changes make content more likely to be cited?"**
Answer-first sections, question-style headings, bullets, a concrete verifiable statistic every 150-200 words, schema markup. Then point out the irony as a feature: these are the same edits that help a hurried human, so there is no trade-off to negotiate.

**"A brand gets named in AI answers but sees no traffic lift. Failure?"**
Not necessarily: the exposure is zero-click by design; the buyer can walk into a store having never touched the site. Watch branded-query demand as the earliest visible echo, and judge the AI-referred visits that do arrive on conversion quality, since the engine pre-qualified them.

---

## File: diagnose/references/playbooks/emerging/llm-traffic-and-organic-search.md

---
title: LLM traffic and its effect on organic search
question: What do answer engines do to your organic channel, and how do you read the traffic they send
order: 2
---

Two curves are crossing. The classic organic click is compressing (Gartner projects traditional search volume falling 25% by 2026 as people take answers from AI instead of results pages) while referrals from generative AI tools grew 357% year over year in mid-2025 off a tiny base. LLM traffic is that second stream: sessions an answer engine refers to your site, and it behaves nothing like the organic traffic it is quietly replacing.

## The framework

1. **Understand the two opposing forces.** Subtraction: when an AI summary sits on a results page, users click a traditional result just 8% of the time versus 15% without one, and a link inside the summary only ~1% of the time ([Pew Research Center](https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/)). Addition: the clicks that do come through arrive pre-convinced: the engine read your page, judged it quotable, and handed the user a reason to trust you before landing.
2. **Judge the channel on four things, never its size.** It will be a rounding error in the channel mix for a while; judging by volume says ignore it, exactly the wrong call on a channel doubling yearly. Read the slope, the cited-page set, engagement quality, and conversion quality.
3. **Treat the cited pages as a recommendation list.** The landing pages receiving LLM traffic are the pages engines choose to quote: rarely the homepage or best-seller, usually explainers, guides, and comparisons. A new entrant means a page just got recommended; a dropout means a competitor displaced you in the answers. A never-prioritized how-to guide can turn out to be your most quotable asset, making its internal links to product pages the most valuable links on the site.
4. **Do not fight the compression; feed it.** The move is to become the source the answer quotes rather than the link it replaces; the LLM traffic you measure here is how you tell whether that generative-engine work is paying off.

## Metrics that matter (and their traps)

- **The slope**: LLM sessions as a share of total, month over month. 0.2% to 0.4% is a doubling that a volume bar chart hides next to organic and paid. Trap: filtering the channel out of reporting because it is small, and missing the one accelerating curve on the page.
- **The cited-page set**: which pages the engines send people to, read for entrants and dropouts. Trap: expecting it to mirror your SEO priorities; it skews to content that answers a question cleanly.
- **Engagement quality**: pre-convinced visitors should behave at or above your organic baseline, not below it.
- **Conversion quality** is the whole reason to watch: one ecommerce analysis found ChatGPT referrals converting 31% higher than non-branded organic ([Search Engine Land](https://searchengineland.com/chatgpt-vs-non-branded-organic-search-conversions-470321)). Treat that as a signal, not a promise; the lift varies by industry and some studies find no difference once query type is controlled. Compare against your *organic-search* baseline, not the site average; below baseline means the answer set an expectation the landing page does not meet, and the fix is the page, not the channel.

## Interview prep

**"Organic sessions are declining with no ranking losses. What is your hypothesis?"**
Zero-click compression: AI summaries satisfying queries on the results page. A strong candidate checks impressions against clicks (visibility holding while CTR erodes) and then looks for the compensating AI-referral stream rather than chasing a penalty that isn't there.

**"LLM referrals are 0.2% of traffic. Why would you spend any time on them?"**
Because the honest read is share-over-time, and 0.2% to 0.4% is a doubling: the fastest-growing curve in the account. Plus the visitors are pre-qualified, so per-session value can far exceed organic.

**"Which pages would you expect AI engines to cite, and what would you do with that list?"**
Explainers and comparison content, not product pages, so treat the cited set as a recommendation list and strengthen the internal links from those pages to the money pages. Entrants and dropouts are the competitive signal.

**"AI-referred traffic converts below your organic baseline. What does that tell you?"**
The answer engine set an expectation the landing page does not keep: an intent mismatch, fixed on the page. The trap is concluding the channel is low quality when its defining property is arriving warmer than cold organic.

---

## File: diagnose/references/playbooks/emerging/measuring-llm-traffic-in-ga4.md

---
title: Measuring LLM traffic in GA4
question: How do you build a monthly read of the traffic AI answer engines send you
order: 3
---

Use this when the question is "are the AI answer engines sending us anyone, and what do we do about it?" The goal is a monthly read of the traffic ChatGPT, Perplexity, Gemini, and Claude send: how fast it is growing, which pages they cite, and whether it engages and buys. The volume is small; the slope and the cited-page set are the story.

## The framework

1. **Build the filter.** In a GA4 Exploration, isolate sessions whose traffic source matches the answer-engine referrers (chatgpt, perplexity, gemini, claude, and variants). Use contains-matching on the core names rather than an exact list: the engine set drifts as new tools appear, and an exact list silently goes stale. Check both the source and medium dimensions when you first build it: AI referrers do not always land in the field you expect.
2. **Set the rows and columns.** Landing page as the row; sessions, engaged sessions, engagement rate, conversions/transactions, and revenue as the metrics. Each row is one cited page's funnel.
3. **Read the slope.** Track LLM sessions as a share of total traffic, month over month. A move from 0.2% to 0.4% is a doubling a volume chart hides.
4. **Read the cited-page set.** The pages receiving this traffic are the pages the engines quote. New entrants mean a page just got recommended; dropouts mean a competitor's page displaced yours in the answers.
5. **Read the quality.** Answer-engine visitors arrive pre-convinced. Engagement and conversion at or above your organic-search baseline is the channel working as designed; below it means the answer set an expectation the page does not meet: fix the page, not the channel.

## Metrics that matter (and their traps)

- **Share of total sessions, over time**: the only honest size read for a small channel. Trap: the raw session count invites you to dismiss a stream that is doubling.
- **Engagement rate under the filter** is a quality gate: a tiny channel at 61% engagement is telling you something a big channel at 40% is not.
- **Conversion vs the organic baseline**: AI-referred sessions converting at a multiple of the organic rate (2x is not unusual on small volumes) is the finding that changes internal-linking priorities. Trap: small denominators; read the multiple over several months before acting on it.
- **Top cited page**: often an explainer, not the homepage or a product page. Its internal links to your commercial pages just became highly valuable links on the site.
- **The filter itself** is the biggest trap: maintenance, since a hardcoded referrer list drifts as new engines and domain variants appear. Re-verify it quarterly, and prefer contains-matching.

## Interview prep

**"How would you set up AI-referral tracking in GA4?"**
An Exploration filtered to sessions whose source contains the core engine names, landing page as the row, engagement and conversion as metrics. A strong candidate flags the maintenance problem unprompted (exact referrer lists go stale) and mentions checking which dimension the referrer actually lands in.

**"The channel is 0.2% of sessions but converts at twice the organic rate. What do you report?"**
The share trend and the per-session value, not the volume, and the cited-page set as an action list: strengthen internal links from the quoted explainers to the commercial pages. Also the small-denominator caveat: confirm the conversion multiple holds over several months.

**"How would you detect that a competitor displaced you in AI answers?"**
A page dropping out of the cited-page set: sessions from AI referrers to a page falling to zero while its organic performance holds. That is the closest thing to rank tracking this channel currently offers.

---

## File: diagnose/references/playbooks/organic-social/organic-social-overview.md

---
title: Organic social performance
question: How do you measure organic social when it rarely converts directly, and what does its work actually feed
order: 1
---

Organic social does the early visibility-and-warmth work, not the closing. A post earns reach, the reach earns engagement, and the engagement compounds into an audience that paid retargeting and email convert later. Judging it on last-click sales is the classic mistake. It was never going to close, and the numbers say so out loud: the all-industry median Facebook engagement rate is roughly 0.06% of followers per post, Instagram about 0.43%, TikTok about 2.63% ([RivalIQ 2024](https://www.rivaliq.com/blog/social-media-industry-benchmark-report/)).

## The framework

1. **Read reach against the follower base, not in raw numbers.** A reach of 10,000 means different things at 2,000 versus 200,000 followers. Share-driven reach is the only kind that grows you; on video, views growing faster than subscribers means the content is being discovered, not just served to loyalists.
2. **Read engagement rate against the platform median.** Beating the Facebook median two-to-three times is genuinely strong, but it is a content signal, not a goal. If the rate is weak, change the content, not the cadence: posting more often into a dead rate dilutes.
3. **Weight engagement by intent**: a share is advocacy, a save is intent to return, a like is almost nothing. Rank content by saves and shares and produce more of what wins. Comments are conversations to answer: half the community-building work.
4. **On video, watch time is the verdict, not views.** 3,000 views holding two minutes beats 10,000 views at twenty seconds; the algorithm rewards retention.
5. **Read the downstream contribution side by side, never as attribution**: organic reach and engagement next to what retargeting pays for warm audiences (say, a $12 CPA on engaged audiences versus $20 on cold lookalikes). That adjacency (cheaper paid, a warmer email list) is organic's payoff made visible.

## Metrics that matter (and their traps)

- **Reach vs impressions**: reach counts unique heads, impressions count displays. Trap: a big impression number on a small reach means the same loyal fans are seeing the post repeatedly, not that you are finding new people.
- **Engagement rate**: reactions + comments + shares over followers. Trap: reading raw engagement instead of the rate; 50 reactions on a 200-follower page beats 500 on half a million.
- **Saves and shares per post**: the intent-weighted signals. Trap: optimizing for likes, the cheapest signal a viewer can give.
- **Watch time / average view duration**: what video algorithms actually reward. Trap: celebrating view counts on videos nobody finishes.
- **Last-click revenue on posts**, the trap itself: putting last-click revenue next to organic posts and concluding the channel "does not work."

## Interview prep

**"Leadership asks whether the free posts are doing anything. How do you answer?"**
A strong candidate refuses the last-click frame and shows the side-by-side: reach and engagement trends where organic works, then retargeting CPA on engaged audiences versus cold ones, and list growth. The claim is adjacency and warming, never a hard attribution verdict.

**"Engagement rate is stuck below the platform median. Do you post more?"**
No: a dead rate at fine reach is a content problem, and a heavier schedule dilutes further. Fewer, better posts that earn a save, share, or comment; then rank formats by those intent-weighted signals.

**"A post got 100k impressions but reached 12k people. Interpret that."**
Frequency to a loyal core: the same followers saw it repeatedly. Fine for reinforcement, but it is not discovery; check the share-driven portion of reach for actual growth.

**"How would you brief the video team on success metrics?"**
Average view duration and total watch time as the primary targets, with subscriber growth as the lagging confirmation of a relationship, explicitly not raw views.

---

## File: diagnose/references/playbooks/paid-media/auditing-pmax.md

---
title: Auditing a Performance Max campaign
question: What is the step-by-step read that tells you whether Performance Max is actually working
order: 6
---

Performance Max exposes no keywords and no real ad groups (its asset groups report as a single `performance_max` pseudo ad group), so the disciplined audit is deliberately narrow: volume at what unit price, then what the campaign actually converts into. That thinness is also what makes it a clean, repeatable review.

## The framework

1. **Isolate the campaign type structurally.** Filter your reporting on the ad group type (or campaign type) enum `performance_max` rather than on campaign names. The enum is set by the platform, so the filter works on any account; name-based filters break the moment naming conventions change.
2. **Read the trend: clicks against CPC by month.** Volume at what unit price. Clicks up with flat or falling CPC is healthy scaling; clicks up with rising CPC is bought growth, acceptable only if the conversion read in step 4 keeps pace.
3. **Read the campaign table.** Per campaign: impressions, clicks, CTR, CPC, conversions, conversion value. This is the whole picture PMax allows, so read it carefully rather than wishing for the query-level detail Google withholds.
4. **Choose your conversion lens deliberately.** Conversion columns should start blank until you pick one value event: a purchase, not a blended total that mixes a signup with a large order. Read the campaigns through that single lens.

## Metrics that matter, and their traps

- **Clicks vs CPC over time**: the cleanest efficiency read available. Trap: celebrating click growth that was simply bought with a rising unit price.
- **CTR at the campaign-type level**: a scaling plausibility check (an account might show, say, millions of impressions at a ~2% CTR and a low CPC). Trap: comparing it against search-campaign CTRs; the inventory mix is different.
- **Conversions under one lens**: under a purchase lens the split gets stark: one feed-driven campaign can carry thousands of orders while a "new acquisition" campaign carries a few hundred. Trap: reading legitimate sparsity as a broken number; a campaign type that never fires a given event is telling you something, not failing to report.
- **Conversion value per campaign**: weigh campaigns on revenue returned, not on the conversion count the platform chose to headline.

## Interview prep

**"Walk me through how you would check whether PMax is working, in five minutes."**
A strong candidate names the sequence: filter to the PMax campaign type structurally, read clicks against CPC for scaling health, then the campaign table, then apply a single purchase lens. They resist the urge to hunt for keyword detail that does not exist.

**"Conversions are blank on half your PMax report. Broken data?"**
Ask which conversion lens is applied first; a blended default hides more than a blank column. And a campaign that never fires a given event is legitimate sparsity, not a pipeline bug.

**"Clicks doubled month over month. Good news?"**
Only alongside the unit price and the conversion side: doubled clicks at a doubled CPC with flat purchases is bought growth, the shape that precedes a quiet ROAS collapse.

---

## File: diagnose/references/playbooks/paid-media/demand-gen.md

---
title: Demand Gen campaigns
question: How do you run and read Demand Gen when there are no keywords and the payoff lands after the last click
order: 3
---

Demand Gen is Google's awareness-to-consideration format: visual ads running across the feeds people open to browse (Discover, Gmail, the YouTube feed), reaching up to 3 billion people a month ([Google](https://support.google.com/google-ads/answer/13695777)). Its job is to create interest among people not yet looking for you, which means the last-click sales column will look almost empty by design. Pausing it for that is the classic mistake of reading a demand generator on a demand capturer's numbers.

## The framework

1. **Hold the core distinction**: demand generation creates new interest among people not searching yet; demand capture harvests interest that already exists. Grading a generator on a capturer's numbers is how good spend gets cut.
2. **Read reach and its price first**: cheap reach at scale is the product being bought.
3. **Read the measured floor**: last-click on-site revenue matched to the line by campaign name. It will be thin; that is expected, not broken.
4. **Estimate the rest honestly**: the warming that pays back later through search or a store visit is real demand the last click cannot see; model it with attribution and mix models, prove it with holdout experiments, never read it off a platform column.

## Metrics that matter, and their traps

- **Cost of reach (CPM)**: the honest unit price of a discovery buy, watched for staying cheap as it scales. Trap: judging the line on clicks or last-click sales instead.
- **Last-click revenue by campaign name**: the measured floor. Trap: treating the floor as the whole return and cutting a line that is warming buyers other channels close. Google reports 87% of viewers say the format helps them decide what to buy.
- **Rising cost of reach or falling engagement at flat spend**: the tell of creative fatigue. The fix is a scheduled refresh cadence with a bench of assets in reserve, not a bidding change.
- **Asset and audience breakdown**: the trap is pretending to know it: which image or seeded segment did the work is often not cleanly in the data, so steer hard on both levers and treat the question as unanswered rather than guessed.

The craft levers, since there are no keywords: the creative *is* the targeting; a sunlit lifestyle shot finds a different person than a studio flat-lay, so swapping the image changes who you reach more than any setting; supply every aspect ratio. Decide whether Demand Gen or an all-surface automated campaign owns the discovery job, or they cannibalize each other on the same inventory.

## Interview prep

**"Your Demand Gen line has near-zero last-click sales after a month. Kill it?"**
A strong candidate expects that column to be thin: nobody buys on the spot from a discovery feed. They check reach and its price, whether view-through and assisted signals are climbing as reach compounds, and they route the incrementality question to modeling or a holdout test before touching the budget.

**"You are a search marketer taking over Demand Gen. What changes?"**
Every search reflex (query mining, negatives, match types) is gone; there is no search-terms report because nobody typed a query. The two dials left are the audience seed and the creative set, and the discipline shifts to asset production and refresh cadence.

**"How would you build the lookalike audience for this format?"**
Seed with the sharpest first-party signal (highest-value customers, not every buyer including one-time discount chasers) because the machine expands whatever you show it and the quality of the expansion is the quality of the seed.

**"A healthy Demand Gen line went cold with all settings unchanged. First suspect?"**
Creative fatigue: frequency climbed, response decayed. Rotate fresh assets: a production-calendar fix, not a bidding one.

---

## File: diagnose/references/playbooks/paid-media/display-advertising.md

---
title: Display advertising
question: How do you read a display line so cheap reach is judged on what it actually buys, and verify the reach was real
order: 2
---

Display is image, text, and video placements bought in front of people who are not searching for anything, so its whole job is cheap reach and awareness. The reflexive read (see a near-zero click-through rate, hover over pause) is the single most expensive mistake in attention media: it kills a line for failing at a job it was never hired to do.

## The framework

1. **Read the price of reach first**: spend, cost per thousand impressions (CPM), and the impressions and reach bought, by campaign and by cluster. The cheapest, biggest line is the one to question first: that is exactly how cheap reach swells unseen.
2. **Hold the two targeting dials apart**: who you reach (affinity → in-market → life events → custom intent → retargeting, in rising warmth) and where the ad runs (hand-picked placements, contextual match, or broad topics). Affinity finds the person who loves the category; in-market finds the person buying this week.
3. **Match the bidding model to the job**: CPM for awareness, CPC for traffic, CPA for a performance play. An awareness line bought and judged on clicks misleads before you read a number.
4. **Tie reach to downstream demand**: on-site sessions and revenue matched by campaign name, plus view-through, estimated via mix modeling and proven via holdout experiments, never faked from a click count.
5. **Verify the reach was real, seen, safe, and fresh**: the hygiene discipline below.

## Metrics that matter, and their traps

- **CPM**: the awareness price. Trap: an unbeatably low CPM is often cheap precisely because the impressions were never seen or were minted by bots.
- **CTR**: display averages about 0.46% at roughly $0.63 CPC ([WordStream](https://www.wordstream.com/blog/ws/2022/05/19/display-advertising-benchmarks)); meaningful for search, misleading as a display verdict.
- **Viewable rate**: the Media Rating Council counts an ad viewable only when at least half its pixels are on screen for one continuous second. Trap: reading raw served impressions; a pricier placement that is actually seen can be the cheaper buy.
- **Invalid-traffic signature**: absurdly low CPM, a mountain of impressions, nothing downstream. Trap: letting a seductive price keep drawing budget into bot and made-for-advertising inventory.
- **Frequency**: past a handful of exposures, extra impressions convert no better and start to irritate. Cap frequency and rotate creative.
- **Retargeting return**: the warmest, highest-returning display play. Trap: it scales recapture, never discovery; it only reaches an audience you already have. Manage recency, membership duration, and exclude past converters.

## Interview prep

**"Our broad prospecting line has the lowest CPM in the account and the biggest budget. Healthy?"**
A strong candidate treats that shape as the first thing to interrogate, not celebrate: check viewable rate, pull the placement report for made-for-advertising junk, and look for on-site demand behind the reach. Cheap is a claim to verify, not a fact to trust.

**"How do you prove display is working if nobody clicks it?"**
Tie campaign names to on-site sessions and revenue, read view-through as the concept, then go past correlation: mix modeling to estimate the missed demand, holdout experiments to prove lift. They avoid dressing clicks up as an awareness verdict.

**"Retargeting posts a 6x return. Should we move most of the budget there?"**
No, retargeting harvests demand that prospecting created and has a hard ceiling: the existing audience. Feeding it while starving prospecting dries up the warm pool. Also check converter exclusion and frequency caps before trusting the 6x.

**"What is the biggest lever you control on display?"**
Usually the creative: strong assets across the responsive formats, refreshed before wear-out.

---

## File: diagnose/references/playbooks/paid-media/insight-roadmap.md

---
title: The paid media insight roadmap
question: In what order should you read a paid media account beyond search and social, and why does the order matter
order: 1
---

Display, video, and the awareness feeds run on a different logic from search: a search ad earns its click from someone already looking, while an awareness channel puts the brand in front of someone who is not, then waits to see who comes back. The leak in this bucket is almost never a low click-through rate inside one format: it is buying reach the wrong way, or judging awareness by an action yardstick it was never built to move. Reading the account in a fixed order is what keeps cheap reach from being mistaken for wasted reach.

## The framework

Two rules set the sequence: read allocation before drilling any single format, because a format in isolation cannot say whether it deserves its budget share; and judge awareness on view-through and on-site value, not clicks.

1. **Where the budget goes.** Reach is cheap and abundant: the display network alone reaches over 90% of internet users ([Google](https://support.google.com/google-ads/answer/2404190)), so a bucket of cheap reach swells quietly. The allocation split tells you which format to drill first.
2. **Display.** The cheapest reach; read it on cost per thousand impressions and the reach it bought, never the click.
3. **Video and YouTube.** Priced by the view; read cost per view, view rate, and view-through conversions.
4. **Demand Gen.** The awareness-to-consideration bridge; read whether cheap reach is warming people, via climbing view-through and assisted traffic.
5. **Performance Max.** The automated black box; read it downstream of the readable formats, never first, and on incremental contribution rather than its self-reported total.
6. **ROAS across every channel.** Zoom out: every channel's cost against one shared on-site value, matched by campaign name, read as an honest last-click floor and then modeled for true contribution.

## Metrics that matter, and their traps

- **Budget allocation by channel and cluster**: which format deserves the first drill. Trap: with no allocation view, cheap reach drifts unseen.
- **Cost per thousand impressions (CPM)**: the awareness price, what a display or video buy actually charges for. Trap: grading these formats on clicks instead; display averages roughly a 0.46% click-through rate, a fraction of search, so a clicks read always condemns it.
- **View-through conversions**: buyers who saw the ad, never clicked, and returned later; the proxy for awareness landing. Trap: expecting the platform to hand this to you cleanly, or dressing a click count up as an awareness verdict.
- **Blended ROAS on one denominator**: each channel's cost against the value your own analytics recorded. Trap: stacking each platform's self-reported return double-counts the same sale and flatters every channel at once.

## Interview prep

**"Display CTR is 0.4% and leadership wants to cut it. What do you say?"**
A strong candidate reframes the yardstick: display buys reach from people who are not searching, so the honest price is CPM, not CTR. They ask for the retargeting pool's return, view-through signals, and on-site demand tied to the campaign, and they warn that cutting top-of-funnel quietly defunds the demand search later harvests.

**"How would you audit a paid account you have never seen?"**
Allocation first (the channel and campaign split) before opening any single format, because a format in isolation cannot justify its budget share. Then each format on its own yardstick, automated campaigns with suspicion, and one blended return read last on a shared denominator.

**"Why cannot you just add up each platform's reported ROAS?"**
Each platform grades its own homework on its own attribution, so the same sale is claimed twice. The fix is one shared value (what your analytics recorded) matched to each line by campaign name, read as a last-click floor that understates upper-funnel channels.

---

## File: diagnose/references/playbooks/paid-media/performance-max.md

---
title: Performance Max
question: What is Performance Max, when does it earn its place, and how do you read past its black-box reporting
order: 5
---

Performance Max is Google's most automated campaign type: you hand it a goal, creative assets, and a budget, and its AI places ads across Search, Shopping, YouTube, Display, Discover, Gmail, and Maps to hit that goal. The trade is real reach and real efficiency for real opacity: no keywords, no ad groups you recognize, no full list of the searches that triggered your ads. It spans the whole funnel at once and reports it as one blended number, which is exactly why it is so easy to over-credit.

## The framework

Know the quirks, then read the few honest signals the black box cannot hide.

The quirks: no keywords (search themes are hints, up to 50 per asset group, not controls); asset groups instead of ad groups, reported as one pseudo-row; blended reporting across seven kinds of inventory; brand-demand cannibalization; and a limited search-terms report.

The reads, in order:

1. **Volume against unit price**: clicks against cost per click over time. Clicks rising with flat or falling CPC is healthy scaling; clicks rising only because CPC climbs is bought growth.
2. **One deliberate conversion lens**: the blended total mixing a newsletter signup with a €200 order is close to meaningless; read through the single value action (a purchase) alone.
3. **The brand cannibalization check**: compare branded and non-branded conversions; a campaign leaning on branded search inflates its own scorecard.
4. **Mine the search terms**: every converting non-branded query it surfaces is demand you can go earn with an SEO page or a dedicated search campaign.

## Metrics that matter, and their traps

- **Blended conversions**: the headline number. Trap: it mixes actions worth wildly different amounts and hides which funnel band did the work; the cheap-to-convert channels (branded search chief among them) absorb the credit.
- **Branded vs non-branded split**: the incrementality tell. An [Optmyzr study of 503 accounts](https://www.optmyzr.com/blog/is-pmax-cannibalizing-search/) found Search/PMax keyword overlap in 91% of them, with the plain Search campaign winning on conversion performance nearly twice as often in those overlaps.
- **Clicks vs CPC trend**: the cleanest efficiency read the campaign allows. Trap: reading click growth alone and missing that it was bought with a rising unit price.
- **Asset-group performance under a value lens**: often one feed-driven group carries nearly all real orders while a broad "new acquisition" group drives almost none; that is the campaign telling you where the money is, not a broken number.

Use it with a single, well-instrumented conversion action, a rich product feed or strong creative, and a defended-brand strategy, to expand the mix, never to replace the high-intent search campaigns whose credit it absorbs.

## Interview prep

**"PMax reports a 6x ROAS. Do you scale it?"**
Not on the self-report. A strong candidate applies a purchase-only lens, checks how much of the credited volume overlaps branded search the account already owns, and reads clicks-vs-CPC to separate real scaling from bought growth, then scales only the incremental part.

**"How can PMax hurt an account that already runs strong search campaigns?"**
By winning branded and high-intent queries those campaigns (or organic rank) would have captured anyway, blended into a total that hides the substitution. The defense: brand exclusions plus a standing branded/non-branded comparison.

**"You cannot see keywords in PMax. How do you still extract query intelligence?"**
The limited search-terms report shows real converting queries; each non-branded one is a candidate for an SEO page or dedicated search campaign. Paid discovers the demand; organic keeps it.

**"When would you recommend PMax, and with what guardrails?"**
Catalog businesses with a clean product feed and one instrumented value event. Guardrails: cap it, one conversion lens, a standing cannibalization check, and judge incremental contribution before scaling.

---

## File: diagnose/references/playbooks/paid-media/true-roas.md

---
title: True ROAS across every paid channel
question: How do you compare return across paid channels when every platform claims the same sale
order: 7
---

Close one sale and by Monday every platform has claimed it: Google reports its return on Google's attribution, Meta on Meta's, each telling the truth about itself and nothing about the others. Their ROAS figures can never simply be stacked: you would be double-counting the same orders and flattering every channel at once. The honest cross-channel return needs one shared denominator.

## The framework

1. **Build the measured read**: every paid channel's cost against one shared value (the on-site value your own web analytics recorded, matched to each line by campaign name), drillable from account service down through account, campaign type, and individual campaign.
2. **Read it as an honest floor, not the truth.** The shared read is last-click: it credits the value to the final recorded touch. That makes it real and comparable, but it systematically understates upper-funnel lines, whose sale usually closes through a later search or direct visit.
3. **Model past the floor.** Attribution is credit, not proof: last-click is a rule for splitting a sale, not evidence a channel caused it. A data-based attribution model spreads credit across the touches that moved the buyer; a marketing-mix model estimates how sales respond to spend per channel over time, including reach that never earns a click. The same per-campaign spend-and-value table that produced the measured read is the model's input.

## Metrics that matter, and their traps

- **Platform-reported ROAS**: each platform's self-graded homework on its own attribution and window. Trap: stacking them across platforms; the same sale is counted twice and every channel looks like it paid for itself.
- **Measured ROAS on one denominator**: recorded on-site value over cost, matched by campaign name. Trap: forgetting it is a floor, and cutting awareness lines whose contribution arrives sideways through a later click.
- **Campaign-name matching**: the join that makes cross-channel comparison possible at all. Trap: sloppy or inconsistent campaign naming silently breaks the reconciliation, and the "comparable" view stops being comparable.
- **Modeled contribution**: the estimate of what each channel truly caused. Trap: treating any attribution model's output as proof; the causal check is a controlled experiment, and the model choice itself depends on the shape of the business.

## Interview prep

**"Google says 5x ROAS, Meta says 4x, and finance says total revenue does not support either. Explain."**
Both platforms credit the same conversions on their own attribution, so their claims overlap. A strong candidate proposes one shared denominator (the value the site's own analytics recorded, matched per campaign) and expects each platform's number to shrink once the double-count collapses.

**"On the shared last-click read, display shows the worst ROAS in the account. Cut it?"**
Not on that number alone: last-click is a conservative floor that is lowest precisely for upper-funnel lines. They would flag it for a mix model or a holdout experiment before reallocating, because the measured floor and the true contribution diverge most at the top of the funnel.

**"What is the difference between attribution and incrementality?"**
Attribution is a rule for splitting credit among recorded touches; incrementality is whether the sale would have happened without the channel. A model reassigns credit; only an experiment proves cause. Strong candidates never present a reassigned credit split as proof.

**"How would you set up the data to make channels comparable?"**
One cost row per campaign per channel, one recorded on-site value matched by campaign name, consistent naming enforced upstream, and a drill path from the whole program down to a single campaign: the tidy spend-and-outcome table a mix model can consume later.

---

## File: diagnose/references/playbooks/paid-media/video-and-youtube.md

---
title: Video and YouTube advertising
question: How do you buy and read video advertising when the attention lands now and the demand shows up later
order: 4
---

Video is paid attention bought by the view: short films running before, during, or alongside content, in front of people who came to watch something else. It is the paid line that punishes a clicks-first read hardest, because nobody watches a brand film and then clicks a banner; they watch, remember, and some come back days later. It is also the one channel where the media buy and the creative cannot be separated: attention is won or lost in the edit.

## The framework

1. **Know what a view costs and what counts as one.** A skippable in-stream view counts only when someone watches at least 30 seconds, the whole ad if shorter, or clicks to engage ([Google](https://support.google.com/google-ads/answer/2375464)). You are renting watched attention, not a click.
2. **Pick the right rung on the format ladder.** Skippable in-stream and in-feed are priced by the view; non-skippable, bumper (6s), and masthead by impressions. The common mistake is buying non-skippable or masthead for a job skippable does cheaper.
3. **Win the first five seconds.** On skippable, most viewers skip, so brand, product, and hook must sit in front of the skip button, not at a reveal at second twelve nobody reaches.
4. **Design for sound-off and vertical.** Burn in captions, put the brand in the frame not the voiceover. Sequence exposures into a story (bumper → longer spot → reminder) rather than looping one film.
5. **Read cost per view, then the retention curve, then on-site value** tied back by campaign name; run a brand-lift study for a real awareness verdict.

## Metrics that matter, and their traps

- **Cost per view**: the awareness price; a few cents is normal for cheap watched attention. Trap: cheap views the creative cannot hold are the most expensive line on the report; you pay for attention and buy a skip.
- **Quartile completion (25/50/75/100%)**: the retention curve, read as edit notes. A cliff after the first quarter usually means the hook is buried past the skip button.
- **Frequency**: rising frequency with flat retention and flat on-site demand means the creative has worn out; refresh or cap before spend turns into annoyance.
- **View-through conversions**: the buyer who watched, never clicked, and returned. Trap: no platform hands the true incremental version cleanly; model it and prove it with a holdout, do not proxy it with clicks.
- **Brand lift**: the measured rise in awareness or consideration from comparing an exposed group with a held-back group; the video-native controlled experiment.
- **Placement quality**: exclude made-for-kids and sensitive inventory; cheap reach in the wrong place is spend working against the brand.

## Interview prep

**"The video campaign got almost no clicks. Did it fail?"**
Wrong yardstick: video is priced by the view and pays back on a delay. Read cost per view, the retention curve, view-through signals, and on-site demand tied to the campaign name; offer a brand-lift study or holdout for the causal answer.

**"Retention collapses after the first quarter of the film. Diagnosis?"**
The creative, not the media buy: the hook is likely past the skip button. Front-load brand and promise into the guaranteed first five seconds, and check the cut works muted and vertical.

**"When do you buy a bumper versus a skippable in-stream?"**
Bumper buys top-of-mind frequency in a single six-second beat, priced by impressions, best paired with a longer format; skippable is the workhorse with a readable retention curve, priced by the view. Match the rung to the message, not the other way around.

**"How would you set a frequency cap?"**
Not by guessing: watch where response peaks and decays; when frequency climbs while retention and demand flatten, you are past the peak.

---

## File: diagnose/references/playbooks/paid-search/account-structure.md

---
title: Account structure and clusters
question: How do I localize a paid search problem instead of averaging the whole account
order: 3
---

A soft number at the top of an account is never evenly spread underneath; it sits in one branch, and the structure is the map that takes you there. Reading by structure turns "the account softened" into "one market's generic-outerwear ad group softened"; without it you average everything and learn nothing.

## The framework

Every account carries the same four-level skeleton, readable with zero setup. Work top down:

1. **Service**: Google Ads next to Microsoft Advertising. The same terms rarely cost the same on both; Microsoft's cheaper inventory often converts at a lower CPA, so ignoring it leaves money on the table.
2. **Account**: brands commonly run one per market or label. Reading account by account stops a strong home market from masking a weak one it quietly subsidizes in the blended total.
3. **Campaign**: holds the budget and targeting. This is where you find an uncapped generic campaign running 28% over budget at a poor cost per sale while a cheaply converting brand campaign sits pinned at its cap. Fix the caps before touching a keyword.
4. **Ad group**: a set of closely related keywords and the ads that answer them.

On top of the native structure, an optional **cluster overlay** groups campaigns and queries by the categories the business actually thinks in (product line, region, intent). A healthy-looking category aggregate can hide one line burning budget at 1.3x return while another quietly carries it; only the line-level read surfaces that.

## Metrics that matter (and their traps)

- **Ad group size**: Google's guidance is one narrow theme per group, commonly five to fifteen closely related keywords ([Google Ads Help](https://support.google.com/google-ads/answer/6372655)). Trap: the one giant ad group (fifty loose keywords under one generic ad) sags CTR and pays more per click for worse placement. Splitting a grab-bag into tight themed groups can roughly triple CTR at under half the CPC, purely from relevance.
- **Quality score**: fed directly by tight theming. A top score can roughly halve CPC; a bottom score can multiply it nearly fivefold.
- **Category-level aggregates**: useful, but never a verdict. Trap: reading the aggregate and stopping; the leak lives one level down.
- **Search-term visibility**: since a 2020 privacy change, the platform only reports terms searched by a significant number of users. Measured visibility of click-driving queries dropped from roughly 75–85% to around 40–60%. Trap: treating the search-terms report as a census. It is a strong sample; act on it directionally and lean on campaign and ad-group levels, which are complete, for spend decisions.

## Interview prep

**"CTR softened account-wide. How do you find where?"**
A strong candidate drills the hierarchy (service, account, campaign, ad group) rather than tuning the account average, and asks whether multiple markets or engines are blended in the top-line figure.

**"What is wrong with a fifty-keyword ad group, concretely?"**
One ad must answer every keyword, so it answers none: relevance drops, CTR sags, quality score falls, and every click costs more. They cite the fix: tight themes of five to fifteen keywords with copy mirroring the query.

**"Would you trust a query-level analysis of wasted spend?"**
Directionally yes, exhaustively no. They know the visible terms are real and actionable, but a meaningful chunk of spend pools in the hidden long tail, so "these are all the terms we spent on" is a claim the data no longer supports.

**"Why compare Google and Microsoft side by side?"**
Same terms, different auctions. Cheaper clicks that convert on the smaller engine justify shifting a slice of budget, but only if the comparison uses consistently defined metrics, not two exports with mismatched conversion scoping.

---

## File: diagnose/references/playbooks/paid-search/brand-vs-generic.md

---
title: Branded vs generic
question: Why split branded from generic search before trusting any account average
order: 4
---

A branded query names you; a generic query names the need. The two behave so differently (brand terms can post a click-through rate near 45% at a few cents a click while generic terms crawl under 2% at forty times the cost) that a blended average describes a business that does not exist. Split them before you trust a single number; every downstream ratio inherits the distortion.

## The framework

Three jobs, in order:

1. **Split first.** Classify every query as branded or generic. The branded half is demand capture: cheap, high-intent, mostly demand your name already earned elsewhere. The generic half is the prospecting engine you actually manage, judged on its own numbers against your break-even ceiling.
2. **Read the leakage the split reveals.** Cross campaign type against query type in a two-by-two. **Forward leakage**: a generic campaign catching brand queries, so its numbers look brilliant on demand it never earned and you scale a mirage. **Reverse leakage**: a brand campaign paying premium defensive rates for generic queries with no brand word in them. Both have the same fix: negative keywords that wall the campaigns off from each other.
3. **Ask the incrementality question.** Should you bid on your own name at all? If your organic listing already tops the results, a paid brand click may be one you would have won for free.

## Metrics that matter (and their traps)

- **Brand vs generic CTR and CPC**: the gap is structural, not a quirk: the brand searcher already knows you and is close to purchase. Trap: the branded halo (a healthy blended CTR and low blended CPC can both be pure brand, hiding a generic program that is bleeding).
- **Share of spend by segment**: commonly ~15% brand / ~85% generic. Trap: congratulating the account for cheap brand volume instead of interrogating the 85% where prospecting money and waste both live.
- **Leakage impressions**: a single broad generic keyword can quietly serve tens of thousands of brand-query impressions. Trap: the search-term data behind this read is sampled, not a census; route the clear pattern, do not chase a rounding artifact.
- **Brand incrementality**: Google's Search Ads Pause studies (2011) found most paid clicks incremental; eBay's large-scale experiment ([Blake, Nosko and Tadelis, 2015](https://www.nber.org/papers/w20171)) found the opposite for a strong brand: pausing brand keywords barely dented traffic. Trap: treating either study as your answer. Incrementality depends on your own organic strength on your own name; the only honest read is a holdout: pause brand terms for some regions or traffic and watch whether total conversions fall.

## Interview prep

**"The account CTR is 8% and CPC looks cheap. Is the account healthy?"**
A strong candidate refuses to answer until brand and generic are split, explains the branded halo, and asks what generic looks like on its own line against the break-even ceiling.

**"What is forward leakage and why is it expensive?"**
Brand demand landing in a generic campaign. It is expensive twice: you overpay for clicks the brand campaign would win for cents, and the flattered generic numbers cause you to scale spend on performance that was never real.

**"Should we bid on our own brand name?"**
The right answer is a test design, not an opinion. They cite the conflicting evidence, note that a competitor bidding on your name forces some defensive spend, and propose a geo holdout measuring total conversions, not ad-attributed ones.

**"How do you fix brand/generic crossover mechanically?"**
Negative keywords in both directions: brand terms as negatives in generic campaigns, generic terms as negatives in brand campaigns, so campaigns stop bidding against your own demand.

---

## File: diagnose/references/playbooks/paid-search/budget-pacing.md

---
title: Budget pacing
question: How do I catch over- or under-spend while there is still budget left to move
order: 10
---

A monthly report tells you that you overspent; a pace read tells you that you are *going* to, while there is still a cap to lower on a bleeding campaign or raise on a converting one. The value is entirely in the timing: once the month closes, none of it is fixable.

## The framework

Pacing is a triangle of three numbers, each answering a different question:

1. **Actual spend month-to-date**: where you are. On its own it lies in both directions: $4,080 spent of a $12,000 plan sounds calm until you notice the month is two-thirds gone.
2. **Average daily spend, trailing 7 days**: your current speed. The trailing week, not the whole month, because early-month days often run cooler while campaigns learn; you want the rate you are actually travelling at now.
3. **Projected end-of-month spend**: where you land if nothing changes: spend so far plus the trailing rate carried across the days remaining. The gap between projection and plan is the pace read.

Then read the pace **per campaign or campaign group, not just the account**. A 3% account overshoot can be two branches pulling opposite ways: a converting line worth feeding running 15% hot, a bleeding one running 20% hot. Raise the first cap, trim the second, and the account lands on plan with better sales inside it.

Finally, pair pacing with **impression share lost to budget**. A campaign converting well with high budget-lost share is the clearest "raise the cap here" signal in the channel: pacing says the money is off track; lost-to-budget names the exact starved campaign.

## Metrics that matter (and their traps)

- **Daily spend**: the platform does not hold a steady line for you: Google Ads can spend up to twice your average daily budget on any single day, promising only that the month stays under daily budget × 30.4 ([Google Ads Help](https://support.google.com/google-ads/answer/2375423)). Trap: a week of high-demand days can burn the month's budget by the 20th, invisible in any single daily number.
- **Projection method**: straight-line from day one vs trailing seven days give different answers. Trap: everyone computing it slightly differently in their own spreadsheet, so the pacing meeting becomes an argument about method instead of a decision.
- **Under-spend**: the quieter, more expensive failure. Over-spend is visible and self-correcting (the platform throttles you); a profitable campaign pausing at noon daily because its cap is too low leaves sales on the table and nothing flags it. Hunt for it deliberately.
- **Account-level pace**: trap: a calm average hiding a starving winner and a hot bleeder that cancel out.

## Interview prep

**"It is the 20th and you have spent 34% of the monthly budget. Good or bad?"**
Neither, until compared with time elapsed and run rate. A strong candidate projects from the trailing daily rate and reads the gap to plan: a third spent with two-thirds of the month gone is a serious under-pace, likely capped winners.

**"Why is under-spend worse than over-spend?"**
Over-spend self-corrects when the platform throttles; under-spend is a converting campaign silently starved by its cap, costing sales no report flags. Active in-month reallocation is where returns come from.

**"How do you find which campaign to give more budget to?"**
Cross two reads: pacing under plan plus strong conversion performance plus high impression share lost to budget. That triple names the campaign that would spend more profitably tomorrow.

**"Why project from the trailing seven days instead of the month so far?"**
The month-to-date average is polluted by the slow start; the trailing week reflects present demand, which is what the remaining days will look like if nothing changes.

---

## File: diagnose/references/playbooks/paid-search/conversions-cpa-and-return.md

---
title: Conversions, CPA and return
question: How do I tell whether a paid click actually pays back
order: 8
---

A campaign can report nine hundred conversions and a "healthy" return while revenue barely moves, because a conversion that counts a newsletter sign-up next to a completed sale is a number, not money. A paid click pays back only when the conversion is the action that means money, its cost sits below a ceiling set from your own margin, and the sales value beats the spend.

## The framework

Profitability is a chain, read in one pass:

1. **Convert**: did the click become an outcome at all? A strong CTR feeding a weak conversion rate is the most expensive failure in the channel.
2. **Scope**: is the outcome a sale or a sign-up? Decide which conversion action means money and read everything against it alone. Scoped to sign-ups, one account showed ~89,000 "conversions" at pennies each; scoped to purchases, ~32,000 sales. Same month, two stories sharing no digits.
3. **Cost**: cost per acquisition, per campaign, never blended.
4. **Ceiling**: is that cost below what margin allows? Break-even click cost = margin per conversion times conversion rate: $40 margin at 5% conversion means $2.00 a click. A $1.80 click wins; a "cheap" $2.40 click loses.
5. **Pay back**: return on ad spend against a target, per campaign, because the blended figure averages winners and bleeders.
6. **Page**: if it did not pay back, the leak is almost always the landing page: message match first, speed second, checkout friction third. A page tweak is a hypothesis, not a fix, until an A/B test proves it moved conversion rate.

Scope wrong at step two and every downstream number is computed on a fiction. Start there.

## Metrics that matter (and their traps)

- **Conversion count**: trap: micro-conversions (sign-ups) are real signals but not revenue; blended into one total, the profitability math runs on sales mixed with email addresses.
- **Conversion rate**: cross-industry search median around 7%, but heavily category-dependent; judge against your vertical, not the average.
- **CPA**: meaningless without the ceiling. Keep it below the margin the average sale earns, per campaign and per product line; a comfortable blended CPA hides the line running over its own margin.
- **ROAS**: comes in two flavors. Revenue-based divides conversion value by spend; profit-based nets out margin first and reads truest on low-margin lines, where a healthy revenue ROAS can still lose money. Know which one you are quoting. And remember last-click ROAS credits the paid click with the whole sale.
- **Page speed**: as mobile load time goes from one second to three, bounce probability rises 32% ([Think with Google](https://www.thinkwithgoogle.com/marketing-strategies/app-and-mobile/page-load-time-statistics/)). Median landing-page conversion clusters in the low single digits, so there is real room to move.

## Interview prep

**"The account shows a spectacular conversion rate and a CPA of pennies. What is your first question?"**
Which conversion action is scoped. A strong candidate suspects micro-conversions and re-reads the account against completed purchases only.

**"Is a $2.40 CPC expensive?"**
Unanswerable without the ceiling. They ask for margin per sale and conversion rate, compute break-even, and judge against it; the sticker price alone never tells you which clicks lose money.

**"ROAS is 4:1 on a 20%-margin product line. Are we profitable?"**
No: 4:1 revenue-based on 20% margin is $0.80 of profit per dollar spent, a loss. Strong candidates distinguish revenue ROAS from profit ROAS unprompted.

**"Clicks are strong but the campaign converts poorly. The ads look great. Now what?"**
The ad did its job; the leak is downstream. They decompose the page: message match against the ad's promise, load speed, checkout friction, then insist any fix is proven with a test, not shipped on intuition.

---

## File: diagnose/references/playbooks/paid-search/device-and-timing.md

---
title: Device and timing
question: When and how should device, day-part, and geo bid adjustments come into play
order: 9
---

A blended cost per click quietly averages a phone click that browses and a desktop click that buys into a single price you pay for both. Device and timing analysis undoes that error: read performance split by device and by time, then set bid adjustments so you pay more where the click is worth more. It is the fine-tuning pass: deliberately the last read, never the first.

## The framework

1. **Only tune a clean account.** A device gap read on top of an unfixed leak (brand leakage, wasted search terms) is partly an artifact of the mess, and a bid adjustment is a multiplier on a bid you must have already set correctly against the break-even ceiling.
2. **Device first**: the gap is usually widest and the data cleanest. In retail, mobile often takes the larger share of clicks at a higher CPC while desktop converts at more than double the rate: phones are where people compare, desktops are where considered purchases close. The move is a bid adjustment, not a device ban; mobile is most of the demand and much of it converts later.
3. **Day of week next**, then hour of day where volume supports it. Retail has a rhythm: weekday lunch-hour browsing, weekend-evening closing. Lift bids on days that pay back, trim days that window-shop.
4. **Geography last, and only where it resolves.** Where location data resolves cleanly to a real market you serve, adjust; where it pools to one organization-level row, leave it alone.

One caveat: device and schedule modifiers are manual-bidding levers. Automated bidding toward a target CPA or ROAS already folds these signals into every auction, so under automation, read the splits as diagnosis, not dials.

## Metrics that matter (and their traps)

- **Conversion rate and CPC by device**: the pair that sets the adjustment. Trap: a phone click costing twice as much and converting at half the rate is worth roughly a quarter of the desktop click; its low absolute CPC makes it look like a bargain.
- **Bid adjustment range**: device modifiers run from -100% to +900% ([Google Ads Help](https://support.google.com/google-ads/answer/2732132)), the same range by day and hour through ad scheduling.
- **Conversion rate by day/hour**: real signal, but demand a stable pattern across weeks before scheduling against it.
- **Geo performance**: the read that most tempts you into a confident, false number. Trap: a geo chart drawn on pooled data is one number wearing a map; performance in a country you do not ship to is noise.
- **Ad frequency**: follows an inverted-U in display and video, but search is a pull channel; frequency lives on the display and social side.

## Interview prep

**"Mobile is 60% of our clicks. Should we bid it up?"**
Share of clicks is not value. A strong candidate asks for CPC and conversion rate by device, computes what a mobile click is worth relative to desktop, and adjusts price to value without banning mobile.

**"Why is device tuning the last step of an account audit?"**
Splits read on a dirty account are artifacts, and adjustments multiply a base bid that must already be right. Hygiene, waste, and the break-even ceiling come first.

**"You set a -20% mobile modifier and nothing changed. Why?"**
The campaign likely runs automated bidding, which treats manual modifiers as advisory. Check the bid strategy before blaming the data.

**"Regional conversion rates look wildly different. Do you set location adjustments?"**
Only after confirming the location data resolves per region rather than pooling, and only for markets the business serves. Better a device adjustment you can trust than a geo adjustment you cannot.

---

## File: diagnose/references/playbooks/paid-search/impression-share-and-quality-score.md

---
title: Impression share and quality score
question: How do I read the visibility layer that sits above the click
order: 7
---

Standard reports start counting at the click, but the richest diagnostics sit one step earlier: of all the searches you were eligible to appear on, what fraction did you show up for, and why did you miss the rest? Optimize the click without reading the eligibility behind it and you are tuning a number downstream of the real leak.

## The framework

1. **Impression share first**: impressions received divided by impressions you were eligible for. It answers the blunt question underneath everything else: are we even showing up? An account showing for 11% of eligible searches lets nine in ten winnable searches go by unseen; no CTR tuning recovers them.
2. **Split the loss.** Lost share divides into two causes with opposite fixes. Lost to **rank**: ad rank (bid times quality) too low to enter the auction; lift quality score or raise the bid. Lost to **budget**: competitive but the daily cap ran dry; raise the cap on a campaign already paying back. This is the cleanest diagnostic in the channel; one half says fix quality, the other says spend more.
3. **Read quality score by component**, not the rolled-up 1–10 number: expected CTR points at the headline and offer; ad relevance at tighter ad groups and keyword-in-copy; landing-page experience at message match, speed, and mobile.
4. **Premium placement**: top impression rate (above organic results) and absolute top rate (the first ad slot) answer "are we showing *well*?" Position matters most on mobile.
5. **Auction insights**: when share is lost to rank, someone specific took it. This report names the competitor overlapping and outranking you.

Above these sit the harder disciplines: which creative earned the click (a rolling ad-and-asset test), whether the ad caused the sale (a holdout experiment), and how credit splits across touchpoints (a modeling choice: compare last-click against data-driven attribution on the same conversions).

## Metrics that matter (and their traps)

- **Impression share**: core terms should sit high; Google's guidance points to the high tens of a percent on queries that matter ([Google Ads Help](https://support.google.com/google-ads/answer/2497703)). Trap: the platform buckets extreme values (under 10%, over 90%), clamping the finest slices.
- **Share lost to rank vs budget**: the two sum with impression share to the full eligible pool. Trap: pouring quality work into a budget-starved account, or raising caps on one being outranked.
- **Quality score**: a top score can roughly halve CPC; a bottom score can multiply it nearly fivefold. Trap: reading the single number instead of the component distribution; you need to know *which* component drags.
- **Aggregation**: account-level figures must be weighted by eligible impressions, or a tiny keyword counts as much as a flagship one.

## Interview prep

**"Impression share on our core terms is 11%. What do you do?"**
A strong candidate asks how the lost 89% splits: rank or budget. If mostly budget on a converting campaign, the move is cap money, not quality work; if rank, quality-score components or bids.

**"Quality score is 4/10 account-wide. Where do you start?"**
With the components as distributions: what share of keywords grade below average on each. A run of poor landing-page grades sends you to the site, not the auction.

**"How is a conversion counted different from a conversion caused?"**
Counted means a conversion followed a click; caused means it would not have happened without the ad. The gap is the money you could stop spending, and only a randomized holdout measures it.

**"A competitor started outranking us. How do you confirm and respond?"**
Auction insights for overlap and outranking share, then the rank equation: raise quality before raising bids.

---

## File: diagnose/references/playbooks/paid-search/insight-roadmap.md

---
title: Read your account in order
question: In what order should I read a paid search account so the numbers tell the truth
order: 2
---

You can answer forty questions about a search account; the mistake is answering them in the wrong order, so a branded vanity number flatters the whole account while a budget-capped campaign that would pay back sits starved. An account gives up its story in a sequence; read it at random and you chase the loudest metric instead of the one that moves money.

## The framework

Two rules set the sequence. First, split branded from generic, because the two behave so differently that a blended average describes neither. Second, clean the account before you optimize it: a wasted-spend term or a leaking brand campaign distorts every downstream ratio until you cut it. Hygiene before growth.

1. **Account funnel overview**: which transition leaks: showing up, earning the click, or paying back? This tells you which later step to open.
2. **Account and campaign drilldown**: localize the leak: which account, campaign, ad group? Works on every account with zero setup.
3. **Branded vs non-branded**: split before trusting any average. Brand terms can run CTR near 45% at cents per click while generic crawls under 2% at forty times the cost.
4. **Brand bid hygiene and leakage**: find campaigns catching the wrong kind of query, both directions, and wall them off with negatives.
5. **Match type and search-term waste**: cut the terms that spend without converting.
6. **New and newly-converting queries**: with the account clean, find demand worth its own ad group.
7. **Conversions, CPA, and return**: only now, on clean and correctly scoped traffic, judge payback against the break-even ceiling (margin times conversion rate).
8. **Budget pacing**: time-sensitive; act while budget is still left to move.
9. **Device and geography**: fine-tuning, last, once the account reads clean.

One cross-discipline read rounds it out: query themes converting in paid where you have no organic presence are demand you are renting that a page could win for free.

## Metrics that matter (and their traps)

- **Blended CTR / CPC**: the numbers most likely to lie. Trap: averaging a 45% brand CTR with a 2% generic CTR describes a business that does not exist, and credits the account for demand the brand already earned.
- **Mid-single-digit CTR**: the typical search median; a reasonable gate for generic terms, far too low a bar for brand.
- **Break-even ceiling**: margin times conversion rate. Trap: judging CPA or ROAS before conversions are scoped to the action that means a sale, so profitability is computed on sign-ups.
- **Incrementality of brand spend**: Google's Search Ads Pause studies (2011) found most paid clicks incremental, but "most" is not "yours"; the honest answer is a holdout test, not an opinion.

## Interview prep

**"Walk me through your first week auditing an unfamiliar account."**
Strong candidates give a sequence, not a metric list: overview to localize the leak, brand split, hygiene, waste, then payback; each read cleans the data the next one depends on.

**"Why does the brand/generic split come before everything else?"**
Because every account-level average inherits the distortion. They cite the intent gap: a brand searcher is comparing at the point of purchase; a generic searcher is exploring: different demand, different economics.

**"The account is 'up 20% on conversions.' What do you check before celebrating?"**
Conversion scoping (sales or newsletter sign-ups?), whether brand leakage is flattering generic campaigns, and whether the gain concentrates in one branch or spreads.

**"When would you look at device performance?"**
Last. A device split read on top of an unfixed leak is partly an artifact of the mess, and a bid adjustment is a multiplier on a bid that must already be set correctly.

---

## File: diagnose/references/playbooks/paid-search/match-types-and-wasted-spend.md

---
title: Match types and wasted spend
question: How do I find and cut the spend that was never going to convert
order: 5
---

A match type decides, before any bid fires, how loosely your keyword matches what people actually type: broad casts the widest net, exact the tightest, phrase sits between. That one setting routes your money and decides where intent concentrates and where waste leaks in, and the account average is built to hide it.

## The framework

1. **Split spend by match type before judging anything**, the same way you split branded from generic. The three types behave so differently that a blended number describes none of them.
2. **Read cost against conversions by match type.** Expect exact to win twice (precision earns a higher CTR and a better cost per sale) while broad brings reach and noise: the cheapest clicks and the worst cost per sale. Check phrase rather than assuming it is the safe middle; it can post the highest CPC of the three.
3. **Mine the search terms.** A keyword is what you bid on; a search term is what a person typed, and broad match widens the gap. Sort terms by cost, filter to zero conversions, and everything left is a negative-keyword candidate: "wool coat care" is a laundry question eating budget meant for checkouts.
4. **Cluster, do not cut row by row.** Group thousands of terms by intent with simple text rules (purchase, informational (care, how-to, repair), off-target) and negative the non-converting clusters as a batch.

Do not kill broad. Around 15% of daily searches are ones Google has never seen before ([Google](https://blog.google/products/search/how-we-keep-google-search-relevant-and-useful/)); exact only shows you demand you already predicted, broad finds the demand you did not. Keep it for discovery, tightened with negatives.

## Metrics that matter (and their traps)

- **CPC by match type**: broad's low CPC is the trap: a cheap click that never converts is waste at a discount, not a bargain.
- **CTR by match type**: search median sits in the mid-single digits; a match type dragging well below is showing for queries that are not really yours. Exact routinely runs several times broad's CTR on the same theme.
- **Cost per sale by match type**: the column that settles the argument. Broad cheapest per click and worst per sale; exact priciest per click and best per sale.
- **Spend with zero conversions, by search term**: the single highest-return read of a paid-search week. Trap: **search-term neglect** (leaving the report unread for a quarter while one broad keyword funds an informational cluster). Second trap: the **exact-match cage** (going all-exact to feel safe and cutting yourself off from new demand).
- **Sampling**: search-term data is a platform sample, not a census; read clusters and trends, not single rows.

## Interview prep

**"Broad match CPC is our cheapest. Should we shift budget into it?"**
A strong candidate rejects CPC as the deciding metric and asks for cost per sale by match type. Cheap clicks that do not convert are the most expensive thing in the account.

**"How would you clean up a broad-match campaign without losing its discovery value?"**
Mine the search-terms report: read cost against conversions per term, group by intent, and negative the informational and off-target clusters in bulk. Reach kept, waste cut.

**"What is the difference between a keyword and a search term, and why does it matter?"**
The keyword is what you bought; the term is what you got. Under broad match the gap is where money goes missing, and only the search-terms report shows it.

**"Why not run everything on exact match?"**
Because a meaningful share of searches are brand new every day; all-exact starves you of converting queries you would never have thought to add. The discipline is broad-plus-negatives, not retreat.

---

## File: diagnose/references/playbooks/paid-search/paid-search-overview.md

---
title: Paid search, read as a chain
question: How do I judge whether a paid search account is actually performing
order: 1
---

Paid search meets the customer at the exact moment they have decided to buy, which is why it is the single largest line in digital ad spend (just over 40% of the US total). The measure of a search program is whether the click converts profitably, not whether the ad showed. The leak is almost always in a transition between steps, not in any single step.

## The framework

Read the account as a three-step chain, in order, and diagnose the transition that breaks:

1. **Showing up**: are we appearing at all, and for which queries? Read impression share and the queries you newly show for.
2. **Earning the click**: did appearing earn a click, and at what cost? Read click-through rate and cost per click against your break-even ceiling.
3. **Paying back**: did the click convert profitably? Read conversion rate, cost per acquisition, and return on ad spend against target.

Two pieces of arithmetic anchor the reads. The **break-even click cost** is margin per conversion times conversion rate: $40 of margin at a 5% conversion rate means $2.00 is the most you can pay per click. And **ad rank** is bid times quality score, so a great quality score can out-rank a bigger budget.

## Metrics that matter (and their traps)

- **Impression share**: your impressions divided by eligible impressions; aim above roughly 80% on core terms. Trap: lost share splits into rank-lost (fix quality or bids) and budget-lost (raise the cap on converting campaigns), opposite fixes, and confusing them wastes money both ways.
- **Click-through rate**: [benchmark reports](https://www.wordstream.com/blog/ws/2022/05/19/search-advertising-benchmarks) put the search median in the mid-single digits; brand terms run far higher. Trap: a blended CTR flattered by brand terms hides a weak generic program.
- **Cost per click**: meaningless on its own. Trap: a "cheap" click above your break-even ceiling is a losing click; the sticker price never tells you which.
- **Conversion rate**: cross-industry search median around 7%, but heavily category-dependent; judge against your vertical. Trap: high CTR with low conversion rate is the most expensive failure mode in the channel; you pay full freight for clicks a broken landing page then wastes.
- **Quality score**: a 1–10 rating from expected CTR, ad relevance, and landing-page experience. A score of 10 can roughly halve your CPC; a 1 can multiply it nearly fivefold. It is the cheapest lever in the channel: fix the page before you raise the budget.

## Interview prep

**"Our CPC has crept up all quarter but every campaign looks green. Where do you start?"**
A strong candidate walks the chain instead of judging single numbers: showing up, earning the click, paying back. They ask for the break-even ceiling before declaring any CPC high or low, and hunt the transition that leaks rather than the step that looks fine.

**"How would you decide the maximum you can pay for a click?"**
Margin per conversion times conversion rate. They also note this is a first-order read; a customer who reorders raises the ceiling, which is where lifetime-value math takes over.

**"Impressions are strong, CTR is strong, conversions are weak. What is broken?"**
Not the campaign: the hand-off. They decompose it to landing page, message match, or price, and avoid the trap of rewriting ads when the ad already did its job.

**"You have budget to either raise bids or improve quality score. Which first, and why?"**
Quality score, because it is a multiplier on rank: it cuts cost and raises position at the same time, while bidding only buys position at higher cost.

---

## File: diagnose/references/playbooks/paid-search/query-performance.md

---
title: Query performance and new queries
question: Which new search queries deserve their own ad group
order: 6
---

Budget is committed at the keyword level but spent at the query level, and the gap between the two holds both your waste and your next winner. A keyword with a healthy blended conversion rate can still be two-thirds junk and one-third gold; you only find out by reading the terms underneath it, at the grain where intent lives.

## The framework

Three reads, stacked:

1. **Keyword**: which themes you chose to bid on, blended. A starting point, never a verdict.
2. **Search term (query)**: which actual phrases each keyword caught, and which earned the sale. Cut the terms that spend without converting first (see the match-types playbook); junk queries hide a keyword's best terms until you clear them.
3. **New query**: phrases you are newly showing for that you never bid on directly. This is the growth read: a term that arrives under a broad keyword, converts, and has no ad group of its own is a promotion waiting to happen.

The promotion rule is strict, because promoting noise rebuilds the mess:

- **It converts, not just clicks.** Clicks without conversions make a negative candidate, not a promotion candidate.
- **It is specific enough to write an ad for.** "Packable wool overcoat" earns a group; "coat" does not.
- **It has enough volume to justify a group's upkeep**, or enough margin per sale for a small one.

Promoted into its own tightly themed ad group with its own ad and landing page, the term gains relevance, and the platform rewards relevance with better placement at lower cost. The report holds both directions: read only the top and you promote the winner while still paying for the questions; read only the bottom and you miss the group waiting to be built.

## Metrics that matter (and their traps)

- **Conversion rate of a new term vs its parent keyword**: a query worth promoting converts at or above the keyword that caught it, sometimes nearly double.
- **The long tail**: Ahrefs' study of 1.9 billion keywords found about 95% get ten or fewer monthly searches ([Ahrefs](https://ahrefs.com/blog/long-tail-keywords/)). Trap: dismissing individual terms as too small; collectively the tail is most of search demand, and where the most specific, least-competed queries hide.
- **New-term impressions without conversions**: high-impression informational queries ("are wool coats warm enough") are negative candidates, however much traffic they draw.
- **Report completeness**: the platform only reports terms above a data-volume threshold. Trap: reading the list as "everything we spent on" rather than "the significant new terms."

## Interview prep

**"You find a converting query under a broad keyword. What do you do with it?"**
A strong candidate applies the promotion rule: does it convert (not just click), is it specific enough for a dedicated ad, is there enough volume or margin? If yes, its own tight ad group and landing page; if it only clicks, a negative candidate.

**"Why read at the query grain instead of the keyword average?"**
The average blends different buyers: "wool overcoat" and "how to store a wool overcoat" are one keyword's problem and two different intents. The distribution inside a keyword is the truth its average hides.

**"How do keyword research and search-term mining relate?"**
A loop: research scores demand you have never run (volume, competition, bid estimates); the search-terms report shows what actually arrived; converting new queries feed the next research pass.

**"How much would you trust a search-terms export for a spend audit?"**
As a strong sample. The visible terms are real and actionable, but the platform withholds the sub-threshold tail, so some spend always pools in terms you cannot itemize.

---

## File: diagnose/references/playbooks/paid-social/paid-social-overview.md

---
title: Paid social performance
question: How do you read a paid social account so prospecting and retargeting are judged on the jobs they actually do
order: 1
---

Paid social is the one paid channel that works the whole funnel: it introduces you to cold audiences, earns the consideration click, and closes the sale, all inside one ad account, reported into one dashboard. That breadth is its trap. A single blended return number hides which job is paying off, and the classic failure is a fine-looking blended ROAS concealing a burned-out prospecting set that the retargeting line had been quietly carrying.

## The framework

1. **Split the account by job before reading any number**: prospecting (cold reach that creates demand) versus retargeting (closing people who already engaged). They do opposite work and cannot share a scorecard.
2. **Judge prospecting on CPM, reach, and frequency**, never on return. Rising CPM at flat reach means the audience is too narrow or the creative is fatiguing.
3. **Read the click as the transition**: CTR is the most diagnostic prospecting signal. Lots of reach with weak CTR is a creative or targeting problem; more budget makes it worse.
4. **Judge retargeting on ROAS and CPA, apart from prospecting.** It will almost always post the higher return because it closes warm demand prospecting created.
5. **Judge the account on the blended conversion count** (the one view that stops either campaign taking credit for the other's work) and set one attribution window before comparing anything.

## Metrics that matter and their traps

- **CPM**: the price of reach; watch it stable, not climbing. Trap: holding a prospecting line to a return target, which starves the top of the funnel.
- **Frequency**: the most-watched fatigue signal; a working heuristic is roughly 2–4 exposures per person per week before fatigue. Trap: when frequency climbs and CTR falls in the same window, the creative is burning out, not the audience; rotate creative before raising budget.
- **CTR**: a Meta feed rate near 1.5% or higher reads healthy as a heuristic; Facebook averaged around 0.90% in [WordStream's 2022 benchmarks](https://www.wordstream.com/blog/ws/2022/04/19/facebook-advertising-benchmarks). Trap: incidental taps inflating it; filter to real link clicks.
- **CPC**: prices the visit. Rising CPC with steady CTR usually means auction competition rose, not a worse ad.
- **Conversion rate**: Facebook landing-page conversion ran roughly 8–9% in the same benchmarks. Strong CTR feeding an expensive CPA means the click was wasted downstream: landing page, offer, or audience-message fit.
- **ROAS**: read prospecting and retargeting apart, never on one blended number. Trap: Meta marks its own homework; in-platform return counts view-through on Meta's window and routinely reports more conversions than your analytics will confirm.

## Interview prep

**"Retargeting returns 5x, prospecting 0.9x. The obvious move is to shift budget. Do you?"**
No: retargeting's return is largely demand prospecting created, and cutting prospecting dries up the warm pool, collapsing the retargeting return a quarter later. A strong candidate judges each job on its own metrics and keeps the pipeline fed.

**"CTR is falling on a campaign that used to perform. Walk me through the diagnosis."**
Check frequency in the same window first: climbing frequency with sliding CTR is creative fatigue, fixed by rotation, not budget. If frequency is flat, look at audience saturation and auction competition via CPC.

**"Why do Meta's reported conversions exceed what GA4 shows?"**
Meta counts view-through conversions on its own attribution window; your analytics counts last-click on yours. Neither is a lie, but comparing campaigns on different windows is comparing different questions: set one window and reconcile against a source of truth you can sign.

**"Reach is strong, CTR healthy, but CPA is terrible. Where do you look?"**
After the click: landing page, offer, audience-message fit. The ad did its job; the funnel leaked downstream.

---

## File: diagnose/references/playbooks/product-management/building-the-business-case.md

---
title: Building the business case
question: How do you prove, before major investment, that a product can become a viable business?
order: 8
---

The business case is the "money gate": the last checkpoint before engineering, manufacturing, and launch spend begins. It is an evidence-based decision document, and it is the product manager's primary cross-functional leadership deliverable: the PM recommends go / conditional go / no-go, and leadership decides.

## The framework

Market analysis runs through three lenses. **Diffusion of innovation** asks who adopts first: innovators and early adopters come before the chasm that separates them from the early majority, so launch messaging and channel choices target the front of the curve; the product itself is assessed on the five adoption factors (relative advantage, compatibility, complexity, trialability, observability). **Five-forces analysis** asks how attractive the industry is: rivalry, entrants, substitutes, plus supplier and buyer power. **Market sizing** asks how big the prize is: TAM (total customers × average annual spend), narrowed to SAM (geography and niche), narrowed to SOM (realistic capture, for a startup on the order of 1-5% of SAM). Projecting more than ~5% of SAM in the early years is the classic tell of an unrealistic model.

Financial analysis then runs a two-question sequence. **NPV: should we launch?** Build the full cash-flow table (revenue model, cost model, discounting); NPV above zero clears the bar. **Break-even: would it survive?** Break-even quantity = fixed costs ÷ contribution margin, expressed as a percent of SAM, with three checks: is it achievable within the SOM, how long until it is reached, and how sensitive is it to a price cut or a cost rise.

The recommendation itself has five parts: state the decision, summarize the evidence, acknowledge the risks (market, operational, financial, technical, legal; plotted on likelihood × impact), define pre-set success criteria that double as kill conditions, and outline next steps. After the gate, confidence builds through the progression prototype → MVP → alpha → beta → launch, each stage retiring a different class of risk.

## Metrics that matter (and their traps)

- **TAM / SAM / SOM**: sized top-down *and* bottom-up. The trap: quoting TAM as if it were the opportunity; the decision rides on SOM.
- **NPV**: discounted value of the full cash-flow picture. The trap: sunk costs smuggled into the model, and hockey-stick revenue with no adoption logic behind it.
- **Break-even as % of SAM**: survivability in one number. The trap: a break-even that requires implausible share, hidden behind an aggressive price assumption.
- **Pre-set kill conditions**: thresholds agreed before launch. The trap: a case with only success scenarios; no case should be unfalsifiable.

## Interview prep

**"Size the market for this product."**
Do it both directions: top-down (population × spend, narrowed twice) and bottom-up (unit economics × achievable accounts), and say which you trust more and why. Ending on SOM, not TAM, is the credibility move.

**"The NPV is positive. Why might you still say no?"**
Break-even may sit outside the plausible SOM, risk may be concentrated in one untested assumption, or the opportunity cost of the team may exceed the return. Positive NPV is necessary, not sufficient.

**"How would you present a case you are only 60% sure of?"**
Conditional go: state the uncertainty, propose the cheapest test that resolves it, and attach kill conditions. Interviewers reward calibrated confidence over forced conviction.

**"What breaks most business cases in practice?"**
Adoption speed. Models assume the market moves at spreadsheet pace; the diffusion curve says the early majority waits for proof. Tying the revenue ramp to an explicit adoption story is the fix.

---

## File: diagnose/references/playbooks/product-management/defining-the-product.md

---
title: Defining the product: the modern PRD
question: How do you write a product definition that aligns a team without prescribing the solution?
order: 6
---

Product definition answers two questions with equal weight: what are we building, and what are we *not* building. The output (a product brief or PRD) is the bridge between validated market insight and the design and engineering work that follows. Its failure modes are famous: the 50-page novel nobody reads, and the one-line wish that aligns nobody.

## The framework

The industry has moved through three PRD eras: **traditional** heavyweight specifications (20-50+ pages, everything pre-specified, still right for regulated, catastrophic-failure domains), **agile** user stories and acceptance criteria (iterate rather than pre-specify), and the **modern 1-3 page brief**: collaborative, living, and focused on defining *problems* rather than prescribing solutions.

A modern brief has three movements. **Problem alignment**: the customer problem, why it matters and why it exists, the high-level approach, and goals with success metrics (both measurable KPIs and qualitative goals). **Solution alignment**: key features tied back to validated needs, key user flows, and open issues with decisions pending. **Launch readiness**: milestones and the cross-functional checklist (support, marketing, legal, data).

Two disciplines make or break it. First, **clarity is non-negotiable**: hunt down "should probably," "if... then we could," and "our product does everything"; each one is deferred conflict. Second, **out-of-scope is as important as in-scope**: the explicit not-building list is what protects the team from scope creep, and it should trace back to evidence (a feature the conjoint valued at near zero belongs there, in writing).

The document is a tool, not a deliverable. It exists to align the team and guide decisions; it gets updated as the team learns, and it earns its keep in the arguments it prevents.

## Metrics that matter (and their traps)

- **A pre-committed success metric with a target**: one number, agreed before launch, above which the product is a success. The trap: shipping without one, then narrating success from whatever moved.
- **Features traced to validated needs**: every capability linked to discovery or test evidence. The trap: the executive pet feature entering the brief without a need behind it.
- **Length and freshness**: 1-3 pages, edited after every major learning. The trap: the brief as bureaucratic artifact, written once and filed.

## Interview prep

**"Write a one-page brief for feature X. What goes in it?"**
The three-movement structure: problem and evidence, goals with a success metric, solution outline with flows, explicit out-of-scope, open questions. Leading with the problem rather than the feature is the tell interviewers look for.

**"How do you keep stakeholders from expanding scope mid-build?"**
The out-of-scope list, agreed at sign-off, is the tool: additions require re-opening the brief and trading something out. Scope discipline is a document property before it is a personality trait.

**"Engineering says the spec is too vague; sales says it is too rigid. Who is right?"**
Possibly both: the modern brief defines the problem tightly and leaves the solution space open. Check whether the vagueness is in the problem (fix it) or in the implementation detail (leave it to the builders).

**"How would marketing input show up in a PRD?"**
Through the evidence layer: personas, needs research, WTP data, and positioning constraints on the goals. Marketers who can cite where their input lands in the brief demonstrate they understand the artifact, not just the meeting.

---

## File: diagnose/references/playbooks/product-management/discovering-customer-needs.md

---
title: Discovering customer needs
question: How do you find out what customers actually need, including what they can't articulate?
order: 3
---

Discovery is where product work either earns its keep or silently fails: everything downstream (concepts, specs, positioning, messaging) inherits the quality of the needs it was built on. Marketers are often the best-placed people in the building to do this well, because customer listening is already their trade.

## The framework

Run needs analysis as a five-step process: **define the scope** with a mission statement (what problem space, which target, what is out of bounds), **gather data** through observation, interviews, and focus groups, **interpret** the raw data into need statements, **organize** the needs into a hierarchy (primary needs with clusters of secondary ones), and **reflect** on what the process missed.

Two distinctions carry most of the weight. First, the **three types of needs**: *explicit* needs are table stakes, meet them or you are not even considered; *unfulfilled* needs are the differentiation opportunity, known pains no current solution handles; *latent* needs are the ones customers cannot articulate because they have never imagined the solution. Interviews surface explicit needs; observation and lead users surface latent ones.

Second, **who to listen to**. The primary market is the main target with the highest willingness to pay; the secondary market finds value but does not drive the design; stakeholders impose constraints without being users. **Lead users** (the heaviest, most demanding users, often already improvising their own workarounds) act as an early-warning system for what the mainstream will want years later.

A need statement should describe what the product must do for the customer, in the customer's terms, without prescribing a solution. "The user can charge the device without carrying a cable" is a need; "add wireless charging" is a design decision smuggled into discovery.

## Metrics that matter (and their traps)

- **Coverage of need types**: how many unfulfilled and latent needs the research surfaced, not just explicit ones. The trap: a survey-only process that can only ever return what customers already know how to say.
- **Sample composition**: lead users and extreme cases included, not just the average customer. The trap: averaging away the signal; the median user rarely reveals the next opportunity.
- **Needs traced to evidence**: every need statement linked to observed data. The trap: the team's own preferences dressed up as "customer needs."

## Interview prep

**"How would you figure out what to build next for this product?"**
Structure beats brainstorm: define scope, choose data-gathering methods per need type (interviews for explicit, observation and lead users for latent), turn findings into solution-free need statements, then prioritize. Naming the latent-need problem, that customers cannot request what they cannot imagine, separates strong candidates.

**"Customers keep asking for feature X. Do you build it?"**
Treat the request as data about a need, not a spec. Ask what job the customer is hiring X for; often a different solution serves the underlying need better. The trap avoided: shipping the literal request and still leaving the pain in place.

**"What is wrong with relying on surveys for discovery?"**
Surveys measure stated importance of things respondents already understand. They miss latent needs entirely and overweight articulate segments. Pair them with observation and behavioral data.

**"Who would you interview first, and why?"**
Lead users and recent churners before average customers: the former preview the future, the latter explain the present failure. A candidate who only says "our target persona" is sampling for confirmation.

---

## File: diagnose/references/playbooks/product-management/generating-and-selecting-concepts.md

---
title: Generating and selecting concepts
question: How do you go from a pile of ideas to the one concept worth building, without groupthink?
order: 4
---

Concept work has a ceiling property: you cannot optimize your way to a great product from a mediocre concept. The quality of what you generate, and the discipline of how you select, set the upper bound on everything that follows.

## The framework

Generation runs on two principles: the **Edison principle** (volume leads to quality, so generate many concepts before judging any) and the **Dots principle** (more knowledge means more creative connections, so search externally, using benchmarks, lead users, and patents, before brainstorming internally). Research backs the hybrid approach: individuals generate more ideas alone, groups generate more diverse ones. So ideate solo first, then combine in the group, then return to solo refinement.

Selection is a two-stage funnel:

1. **Concept screening**: coarse and early. Rate every concept +/0/− against a well-understood reference concept on 5-10 independent criteria (customer needs plus enterprise needs like manufacturing cost), all criteria equally weighted. Net score ranks the field; keep the top 3-5.
2. **Concept scoring**: fine and late. Rate the survivors 1-5 against the reference, but now weight the criteria by *customer-derived* importance (from research, not the team's intuition). Weighted totals rank the finalists, and niche excellence often beats broad mediocrity, which is exactly what the weights are there to catch.

The step most teams skip is **combine and improve**: the goal is not to select the best existing concept but to *create* the best concept, which may not exist yet. A concept ranked fifth can carry one excellent feature worth grafting onto the leader. Before selecting, ask what makes each concept score well anywhere, and whether a hybrid preserves the pluses while cancelling the minuses.

Finally, **check sensitivity**: if a small change in a weight or one uncertain rating flips the ranking, the decision is not robust, and it can be rational to pick a slightly lower-scoring concept with far less uncertainty.

## Metrics that matter (and their traps)

- **Concepts generated before selection**: teams that generate more produce better final products. The trap: three concepts, one of which was always the favorite.
- **Criteria independence**: each criterion measures something distinct. The trap: three flavors of "quality" triple-counting one dimension.
- **Weight provenance**: scoring weights sourced from customer research. The trap: the loudest voice in the room setting the weights.

## Interview prep

**"How would you choose between three campaign or product concepts?"**
Name the mechanics: shared criteria from customer needs, a reference point, structured ratings, then combine-and-improve rather than a beauty contest. Adding a sensitivity check ("would the winner survive a 1-point rating error?") signals real practice.

**"Your team is split between two directions. What do you do?"**
The screening matrix is a consensus tool as much as an analysis tool: it converts a personality clash into a criteria conversation. Discussion of ratings is often more valuable than the final score.

**"Why not just A/B test the options?"**
Testing settles what users prefer among what you built; selection determines what deserves building. A test cannot rescue a concept space that was never explored, and it costs far more per option than a scoring matrix.

**"Tell me about a time an idea got better by combining it with another."**
Interviewers are probing for the create-do-not-just-select instinct: the strongest answers show a weak concept's single excellent feature transplanted into the winner.

---

## File: diagnose/references/playbooks/product-management/prototyping-to-learn.md

---
title: Prototyping to learn, not to impress
question: What should you prototype, at what fidelity, and what is each prototype for?
order: 7
---

A prototype is an approximation of the product along one or more dimensions of interest; anything that exhibits even one aspect of the eventual product counts. The craft is choosing the *cheapest* approximation that answers the question in front of you, instead of building the impressive one.

## The framework

Every prototype serves one of **four purposes**: **learning** (will it work, does it meet the need; test assumptions cheaply), **communication** (a visual aligns team, stakeholders, and backers far better than words), **integration** (do the pieces work together; forcing functions across disciplines), and **milestones** (demonstrating progress at gates). Declare the purpose first; a prototype without one is decoration.

Fidelity is a spectrum with a rule of thumb: do not jump to high fidelity too early. **Low** (minutes to hours: paper sketches, whiteboard flows) explores; **medium** (hours to days: wireframes, clickable mockups) tests flows and layout; **high** (days to weeks: coded front-ends, functional hardware) supports user testing and demos. Each step up buys realism at the cost of speed and the willingness to throw it away.

For digital products the six-step sequence is: define 1-2 personas from real research data, map the user flow goal-first (5-8 steps, mark the decision points), sketch a paper prototype, build wireframes (structure, not style), wire a clickable prototype, and test with users. Five users uncover roughly 85% of usability issues, so small tests iterated beat big tests delayed. The governing principle: every design choice traces back to a core pain point, because design choices shape user behavior.

Services need a different kit: map the customer experience cycle, blueprint frontstage and backstage, storyboard the moments of truth, then pilot with 5-10 real users, because you cannot hand someone a service to try.

## Metrics that matter (and their traps)

- **Question answered per prototype**: the assumption each artifact tested. The trap: the "hardware swamp," prototypes that consume weeks without contributing to any project decision.
- **Time-to-first-user-contact**: how quickly a testable artifact reached a real user. The trap: polishing in private; fidelity rises while learning stays at zero.
- **Issues found per test round**: the 5-user cadence, prioritized critical → major → minor. The trap: testing once at the end, when the findings are too expensive to act on.

## Interview prep

**"How would you test this idea without building it?"**
Name the assumption first, then the cheapest artifact that tests it: a landing page for demand, a paper flow for comprehension, a concierge version for the service. Candidates who start with the question, not the artifact, pass.

**"When is a high-fidelity prototype a mistake?"**
Early: it anchors the team on one solution, costs too much to discard, and makes testers critique pixels instead of the concept. High fidelity belongs where the remaining risk is interaction detail or stakeholder confidence.

**"How many users do you need for a usability test?"**
Five per round uncovers most issues; the budget is better spent on more rounds than more users per round. Knowing this number, and its iterate-fast implication, signals hands-on experience.

**"Marketing built a clickable demo for a feature that does not exist. Good or bad?"**
Good if it is honestly framed as a learning or communication prototype (demand testing, stakeholder alignment); bad if it quietly becomes a commitment engineering never scoped. The purpose declaration is the difference.

---

## File: diagnose/references/playbooks/product-management/screening-opportunities.md

---
title: Screening opportunities before you build
question: How do you decide which product ideas deserve investment, and which to kill early?
order: 2
---

Most product failures were knowable before a line of code was written. Opportunity screening is the discipline of treating every idea as a hypothesis about how it might create value, and testing the hypothesis before committing the team.

## The framework

An **opportunity** is an idea for a new product expressed as a hypothesis about value creation. The screening sequence: establish a charter (what game are we playing), generate and sense many opportunities, screen out the unlikely ones, develop the 3-5 most promising, then select the exceptional few using a structured test.

The workhorse test is **RWW: Real, Win, Worth it**:

1. **Is it Real?** Is there a genuine need, a market that can and will buy, and a viable product concept that satisfies it within social and legal norms? This is the desirability check.
2. **Can we Win?** Do we have a sustainable competitive advantage (performance, patents, barriers, brand fit)? Do we know this market as well as or better than competitors, and do we have the management commitment to see it through?
3. **Is it Worth it?** Is the expected return attractive at acceptable risk? Do we have the cash and the people, and does it fit the strategy?

Classify surviving opportunities by risk with the **Horizon framework**: Horizon 1 is low-risk improvement and extension of what exists; Horizon 2 changes one dimension (new market or new offering); Horizon 3 is new-category, high-risk exploration. A healthy pipeline holds a deliberate mix rather than drifting entirely into safe Horizon 1 work.

## Metrics that matter (and their traps)

- **Number of opportunities generated before selection**: volume precedes quality. The trap: falling in love with the first idea and "screening" it against strawmen.
- **Explicit kill criteria**: thresholds set before development that trigger a stop. The trap: sunk-cost reasoning; the project continues because it already consumed budget.
- **Portfolio mix across horizons**: share of investment in H1/H2/H3. The trap: judging every idea by H1 payback rules, which kills all exploration by default.

## Interview prep

**"We have five feature ideas and budget for one. How do you choose?"**
Run RWW out loud: which need is most real, where can we win against alternatives, which return justifies the effort. A strong candidate also asks what evidence exists for each, and proposes cheap tests for the gaps rather than a debate.

**"How would you kill a project the founder loves?"**
Pre-agreed criteria beat personal arguments. The candidate who says "define success thresholds and kill conditions at the gate, then let the data make the case" shows they understand governance, not just analysis.

**"Is this a good market to enter?"**
Decompose: is the need real and growing, who already serves it, what advantage would we bring, and what would winning cost. The trap to avoid is answering with market size alone: a huge market you cannot win is a worse bet than a niche you can own.

**"What is a product idea you would bet against, and why?"**
The framework gives the structure: name which of Real / Win / Worth-it fails and why. Failing exactly one axis cleanly is the mark of a candidate who evaluates rather than opines.

---

## File: diagnose/references/playbooks/product-management/validating-with-data.md

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

---

## File: diagnose/references/playbooks/product-management/what-product-management-is.md

---
title: What product management actually is
question: What does a product manager own, and how is it different from product development?
order: 1
---

Marketing roles increasingly shade into product: growth marketers propose features, lifecycle marketers shape onboarding, brand managers own portfolio decisions. Interviewers probe whether you understand the product function you would be collaborating with, or stepping into.

## The framework

Product management stands at the interface between customers and companies. Customers have needs, wants, and frustrations; companies have resources, capabilities, and competitive advantages. The PM's job is matching one to the other, repeatedly and commercially.

A useful decomposition is the **Four S's**: **Sensing** (spot disequilibrium: unmet needs in the market, or an adequate solution you could beat with better technology), **Solving** (ship a first version against that opportunity), **Scaling** (broaden to a viable customer base and serve the bulk of the market well), and **Sustaining** (refine for cost and advantage once the base exists).

The cleanest boundary line: product **management** owns the *what* and *why* from a customer perspective: what should we build, for whom, why does it matter, how do we measure success. Product **development** owns the *how* and *when*: architecture, stack, timeline, quality. Marketers who cross into product usually enter through the management side: research, needs, prioritization, lifecycle.

Underneath every product decision sit the **three innovation challenges**: is it **desirable** (do people want it, does it solve a real problem), **viable** (can the business make money from it sustainably), and **feasible** (can it actually be built). All three must hold at once; two out of three fails completely. A subscription that customers love but that loses money on every transaction fails on viability. A technically impressive gadget nobody wants to be seen using fails on desirability. A dream product the infrastructure cannot yet support fails on feasibility.

## Metrics that matter (and their traps)

- **Success metric defined before launch**: a concrete threshold agreed in advance. The trap: retrofitting whatever number went up as "success."
- **Adoption vs projections**: post-launch tracking against the business case. The trap: celebrating absolute growth while running far below the plan that justified the investment.
- **Development capability**: whether the team is better at building products after this project. The trap: it never appears on a dashboard, yet it is a real asset that compounds.

## Interview prep

**"What is the difference between product management and product marketing?"**
A strong candidate anchors on the interface: PM decides what gets built and why, product marketing decides how it reaches and persuades the market. Both start from customer needs; they diverge at the artifact they own (roadmap vs go-to-market).

**"Tell me about a product you think is well managed. Why?"**
Reason through desirable/viable/feasible rather than listing features. The impressive answer shows the trade-offs: what the product deliberately does not do, and how its business model reinforces the customer value rather than fighting it.

**"A feature you love was killed. Walk me through why that might have been right."**
Show you can argue the other two axes: desirability alone does not carry a decision. Perhaps the unit economics were negative at scale, or the maintenance cost crowded out higher-leverage work.

**"Where does marketing end and product begin in a growth role?"**
The candid answer: at the data. Both share the funnel; marketing owns demand into the product, product owns what happens inside it, and the strongest operators read both sides of that handoff as one system.

---

## File: diagnose/references/playbooks/seo/insight-roadmap.md

---
title: Read your organic search in order
question: In what order should you read organic search data so each answer narrows the next question
order: 2
---

Organic search hands you one of the richest datasets in marketing and almost dares you to read it wrong: every query, page, and impression is in there, so it is easy to sort by clicks, feel busy, and learn nothing. The data gives up its story in a sequence: are you showing up, are you earning the click, is the click worth anything once it lands. Read it by whichever column is tallest and you optimize the page that was already fine.

## The framework

Read organic search in this order; each step narrows the next question.

1. **Property funnel, by country and device.** Never stop at the property total: position and CTR swing hard by market and device, and the blended average describes none of them. Scope to the markets you sell into and the devices your buyers use. This step only decides where to look next.
2. **Query performance.** The grain where SEO is won or lost. One page ranks for hundreds of queries, so its page-level average blends a few strong terms with a long tail of unclickable impressions.
3. **Landing-page performance.** With the queries understood, find the pages behind them: which earn their impressions, which under-click a strong rank, which rank for queries they cannot serve.
4. **New and newly ranking pages.** Once the core estate reads clean, catch emerging demand; new impressions arrive well before clicks, while a rising term is still cheap to nurture.
5. **Organic and on-site behavior.** A click is a hand-off, not a finish line. Cross organic landing pages with engagement and conversion to find the intent mismatch.
6. **Organic and paid overlap.** Only after both channels read clean: find query themes that convert in paid but have no organic power (demand you are renting that an evergreen page could own). The brand-cannibalization check rides along for free.
7. **AI answers and LLM traffic.** The newest surface, read on top of a clean organic base: are you cited in AI answers, and what does that referral traffic do?

Two rules set the sequence. Read at the grain (query, country, device), never the aggregate. And read organic on its own before crossing it with anything else.

## Metrics that matter, and their traps

- **Impressions and average position, per country and device**: the "are we showing up" read. Trap: the same query can sit third on desktop at home and fifteenth on mobile abroad; the blend hides both.
- **Click-through rate against position**: the leak is almost always in a transition. CTR collapses below the first few positions ([Backlinko](https://backlinko.com/google-ctr-stats)), so a soft CTR at a strong position is a title problem; a soft CTR at position twelve is a ranking problem.
- **On-site engagement and conversion per organic page**: great CTR with no conversion is a landing-page or intent-match problem, not a ranking problem.
- **Paid conversion rate on shared queries**: the prioritizer organic data cannot supply. Trap: running ads does not lift organic rank; paid is a demand-discovery instrument, the organic build is a separate bet.

## Interview prep

**"You get access to a company's Search Console and GA4 on day one. What do you look at first?"**
A strong candidate names an order, not a metric: property funnel split by country and device to pick where to look, then the query grain, then the pages, then on-site payback. They explain that reading by the tallest column confirms whatever story you went looking for.

**"Why is the property-level average dangerous?"**
Because it blends markets, devices, and intents that behave nothing alike: a strong home market subsidizes an invisible second one, and the average describes neither. The trap is acting on a number that is true of nothing.

**"When would you cross organic data with paid search, and why not earlier?"**
Last among the channel reads, once both read clean on their own; otherwise you cannot tell which queries and pages you are actually comparing. The payoff is the content gap: paid-proven converting demand with no organic ranking.

**"How do you know if a leak is a content problem or a ranking problem?"**
Locate it in a transition: huge impressions with tiny CTR is title-and-position; strong CTR with no conversion is intent match on the page. Naming the transition names the owner of the fix.

---

## File: diagnose/references/playbooks/seo/landing-page-performance.md

---
title: Landing-page performance: earning the impressions
question: Which pages earn the impressions they get, and which waste them
order: 4
---

Ahrefs studied a billion pages and found 90.6% of them get no organic search traffic from Google at all ([Ahrefs](https://ahrefs.com/blog/search-traffic-study/)). The pages that do earn traffic carry the whole estate, so knowing exactly which ones, and why the rest do not, is the entire job. A page-level average will not tell you: it is two averages stacked on top of each other, one blending queries, the other blending countries and devices, and both of them lie.

## The framework

1. **Take the page, drop to country, then device, then read the four numbers together**: impressions, clicks, CTR, position. The same position earns a different share of clicks per device and market, so a page can look healthy on desktop at home and be near-invisible on mobile abroad, with the average sitting comfortably between.
2. **Scope to your business.** Geography is where your audience lives and which markets you serve; device is where they are active. Filter out countries you do not ship to, or the read is noise.
3. **Name which of the three stories the page tells**, then apply that story's fix, and refuse the other fixes:
   - **Earning its impressions**: CTR in line with position, on the queries it was built for. Feed it (depth, internal links); do not audit it.
   - **Strong position, weak click**: good rank, CTR well below what the position should pull. Rewrite title and snippet; do not build links. The expensive part, the rank, is already paid for.
   - **Ranking for what it cannot serve**: impressions on a valuable query the page does not answer (a fabric explainer collecting buying-term impressions). Build or point the right page at the intent; a title tweak fixes nothing.
4. **Drill any suspect page to its queries** to confirm the story: an informational query served fine at position three can coexist with 40k+ impressions on transactional terms the same page has no way to satisfy.

## Metrics that matter, and their traps

- **Impressions per page**: visibility earned. Trap: high impressions on a mismatched intent look like success at property level and are a trap dressed as a win.
- **CTR against position**: the #1 organic result pulls about 27.6% CTR ([Backlinko](https://backlinko.com/google-ctr-stats)); a page at position two or three converting a fraction of that is leaving clicks on the table no link-building recovers. Google's own guidance: the title link and meta description are what earn the click at a rank you already hold.
- **Average position**: impression-weighted, hides the distribution; lags two to three days and samples the long tail. Read as a trend and pair with CTR before acting.
- **CTR as a ratio**: recompute from totals (clicks over impressions) at whatever grain you read; averaging each row's rate gives a number true of nothing.
- **Cannibalization signal**: two of your pages surfacing for the same valuable query split the signal, a common cause of pages stalling below the position they could reach.

## Interview prep

**"A page holds position 2.8 and converts under 1% of impressions into clicks. What do you do?"**
Rewrite the title and meta description: nothing about the ranking is broken; searchers see the result and scroll past. A strong candidate says explicitly what the fix is *not*: link-building. One snippet rewrite here beats a quarter of links on a worse-ranked page.

**"A blog post shows big impressions on a high-value commercial term. Good news?"**
Only after drilling to the queries. If a thin explainer is collecting impressions on buying terms it cannot close, the demand belongs on a product or category page: the fix is pointing the right page at the intent, not polishing the wrong one.

**"Why split a page's numbers by country and device?"**
Because CTR at a given position is not a constant: it shifts by device and market, so a strong home market subsidizes a weak overseas one and the page total hides both. Then scope the split to markets and devices that carry the business case.

**"How would you triage a thousand-page site?"**
Group pages into meaningful sets (sections, templates, product lines) and read at that grain first: a category that looks fine in total can hide one line gaining impressions while its CTR falls. Then apply the three-stories triage per page inside the offending set.

---

## File: diagnose/references/playbooks/seo/new-and-newly-ranking-pages.md

---
title: New and newly ranking pages
question: How do you catch emerging organic demand before it converts
order: 5
---

The new edge of your organic search (URLs just collecting their first impressions, old pages suddenly surfacing for phrases you never targeted) is the part of the report most teams skip, because it is small, noisy, and pays back later. It is also where next quarter's traffic is hiding. Google has said 15% of the searches it handles daily are ones it has never seen before, so demand is not a fixed list you rank against once.

## The framework

1. **Run this check late**, after the core estate reads clean; new demand is only worth chasing once existing pages aren't leaking.
2. **Separate the two signals people lump together.** A *genuinely new page* earning first impressions is your content pipeline showing up: a build-or-watch call. An *existing page newly ranking for a new query* found demand you did not know it could serve: almost always a *deepen* call; the page is already indexed and trusted, so a paragraph and a heading beat building a rival page that cannibalizes it.
3. **Read at the query grain, never the page average**: it bites hardest here, where a new page's average blends one strong term with a tail at position twenty-two, and one query can swing the blend.
4. **Lead with impressions, then rank by intent, then check position last.** Impressions say demand is arriving; the query text says whether it is worth serving; position says how far you have to go. Clicks are supposed to lag: that is the opportunity, not the failure.
5. **Check pipeline health.** If genuinely new pages per month trend toward zero, your clicks are being propped up by a shrinking set of old pages. Raise that alarm the moment you see it.

## Metrics that matter, and their traps

- **Impressions on new pages/queries**: the earliest demand signal, rising months before clicks. Trap: high impressions are not automatically demand; a seasonal mood piece catching browsing queries at position twenty-seven is awareness churn; note it, do not fund it.
- **Average position at low volume**: an average across search instances that swing on location, device, and personalization; a few-hundred-impression query bounces month to month on almost nothing. Read the trend arrow, not the decimal, and give a fresh URL time to settle before judging it.
- **The workable zone**: roughly positions 10-20, the page-two contenders one content pass from clickable. A page at thirty-five is not one edit from page one; effort in the deep tail is effort a page-two query would repay many times over.
- **Clicks lag by design**: the top position takes roughly 27-39% of clicks and CTR falls off a cliff by the bottom of page one ([Backlinko](https://backlinko.com/google-ctr-stats)), so a rising term at fourteen earning nothing is normal.
- **Base rates**: 90.63% of pages get no Google organic traffic at all, and only 22% of top-ten pages were created within the past year ([Ahrefs](https://ahrefs.com/blog/how-long-does-it-take-to-rank/)). A new URL at a handful of impressions is the base rate, not a failure; you are hunting the rare one climbing with intent behind it.

## Interview prep

**"How do you decide whether a rising term deserves a new page or an edit to an existing one?"**
By which signal it is: a genuinely new page finding demand gets nurtured or built out; a new query on an established, already-ranking page gets a deepen (new section, sharper heading), never a rival page competing for the same term. Confusing the two either builds an unneeded page or ignores a needed one.

**"A three-week-old page has 4,000 impressions and 38 clicks at position 14. Worth funding?"**
Yes, if the query text carries intent: drill past the page average to the pulling query. Demand arriving, a thin page underneath, and page two within one content pass is the strongest cheap-to-move signal there is. The clicks are absent by design at that position.

**"What is the trap in a new page with the highest impressions on the sheet?"**
Awareness churn: browsing queries that were never going to convert. A strong candidate ranks by intent, not impressions, and can say "note and move on" about a big number.

**"How would you spot a site coasting toward decline?"**
Steady clicks carried by a handful of old pages with no new-query or new-page discovery underneath. The pipeline trend, genuinely new pages per month, is the alarm most reports never chart.

---

## File: diagnose/references/playbooks/seo/organic-and-on-site-behaviour.md

---
title: Organic clicks and on-site behavior
question: Does the organic click pay back once it lands
order: 6
---

A page can rank well, earn a strong click-through rate, and still be a failure, because the click only proves the searcher chose you on the results page. Whether the page kept the promise the search made is a separate question, and it lives in a separate dataset. Reading organic landing pages against what their sessions do next is how you tell a page that earns traffic from a page that earns traffic and pays it back.

## The framework

1. **Treat the click as a hand-off, not a finish line.** The searcher arrives with an expectation already formed by the query and your snippet; the page has seconds to prove the match.
2. **Join the two systems.** Clicks live in Search Console; sessions, engagement, and conversions live in GA4 (or equivalent). Neither dashboard shows both against the same page until you join them, which is why the intent-mismatch page hides for months.
3. **Walk each high-traffic page left to right and find where it narrows too fast:**
   - Clicks fine, engagement low → the page did not match the query. Content or snippet problem, not ranking.
   - Engagement fine, conversion near zero → the page held them but the offer, price, or path failed. A CRO problem.
   - High conversion, few sessions → a starved winner. Feed it traffic; do not "optimize" it.
4. **Name the intent mismatch when you see it:** a page ranking for a query it does not serve: an informational query landing on a hard product grid, a buying query landing on a thin blog post. A strong CTR on such a page is not success; it is traffic the page is built to disappoint.
5. **Read by page group, not one URL at a time.** One mismatched guide is often a whole section's pattern (content that ranks and engages but routes nobody toward a purchase), and the section-wide linking fix is worth far more than tweaking one URL.

## Metrics that matter, and their traps

- **Engagement rate**: the first payback signal, read before conversion, because pages lose people well before checkout. GA4 counts a session engaged when it lasts a meaningful moment, loads a second page, or fires a conversion ([Google Analytics Help](https://support.google.com/analytics/answer/11109416)); everything else bounced. Cross-industry bounce sits around 40-60%, so roughly half of hard-won clicks walking straight out is the base rate.
- **Conversion rate against a real benchmark**: ecommerce averages roughly 1.5-2.5%, fashion at the low end. A page at 0.2% is not merely below your best; it is below the floor, which is what turns "interesting" into "fix this."
- **Clicks vs sessions**: two measurement systems, counted differently, lagging differently. They will never foot as arithmetic. Read each page's *shape* (clicks → engaged sessions → conversion) and each column against itself over time; never add across.
- **Sessions on high-converting pages**: the trap is symmetric: teams "optimize" starved winners and ignore high-click pages with pinhole bottoms. The page to fix is the one with the most clicks and the least payback.

## Interview prep

**"Our highest-click organic page barely converts. Walk me through your diagnosis."**
Read it left to right: if engagement is also low, it is an intent mismatch: check which queries feed it and whether the page answers them; if engagement is fine, it is the offer or path. A strong candidate asks what the page ranks *for* before touching the page.

**"Search Console clicks and GA4 sessions for the same page do not match. Which do you trust?"**
Both, for different questions: different systems on different sides of the click. The trap is the reconciliation project; the skill is reading the funnel shape per page and each column against itself over time.

**"How do you decide which organic pages get CRO attention?"**
Sort by sessions, keep pages where engagement holds but conversion collapses: those are true CRO windows. Route snippet breaks to SEO and engagement breaks to content/UX; a shortlist without owners is just a chart.

**"What would make you deliberately not optimize a page?"**
High conversion with low traffic: it is starved, not broken. It needs the ranking effort a mismatched page is wasting, not another audit.

---

## File: diagnose/references/playbooks/seo/organic-paid-overlap.md

---
title: Organic and paid overlap: the content gap
question: Which demand converts in paid search that organic could win for free
order: 7
---

The content gap is the set of query themes that convert in your paid campaigns while your site has little or no organic ranking on them: proven demand you are renting every month instead of owning. Found and ranked, it turns "what should we write next" from an opinion into a shortlist ordered by conversions that already happened, with the brand-cannibalization check riding along for free.

## The framework

1. **Run this read only after both channels read clean on their own.** It is the one read that needs both open on the desk at once: paid knows which queries convert because it spent money finding out; organic knows which of those you already rank for.
2. **Pick your ranking metric: a business-model choice.** A store ranks paid converters by conversions and CVR; a publisher or ad-supported site ranks by clicks and CTR, because the visit is the product. Sort by the wrong one and you prioritize the wrong pages.
3. **Read every high-value query against organic position:**
   - Converts well, organic absent or 20+ → **the content bet**: build the evergreen page and start compounding.
   - Converts well, position 4-20 → **leverage zone**: push organic while ads hold the demand.
   - Converts well, position 1-3 → **you already own it**: why still paying? The cannibalization check.
   - Converts poorly at any rank → informational; awareness only, never a store's conversion priority (a publisher would rank it near the top).
4. **Group the gap by theme, not query by query.** Nobody briefs a content team off row 214; roll queries into product lines to see where the rented demand concentrates, and brief the biggest pocket first.
5. **Keep the caveat that stops this becoming magical thinking:** running ads on a query does not lift its organic ranking. Paid is a demand-discovery instrument; the organic build is a separate, compounding investment.

## Metrics that matter, and their traps

- **Paid conversions and CVR per query**: the money-proven demand signal. Trap: big paid click volume at low CVR is informational demand crowding out the real bets.
- **Organic position on the same query**: clicks collapse off the top of page one (the first result earns roughly 27% of clicks, falling steeply below the top three, per [Backlinko](https://backlinko.com/google-ctr-stats)), so position fourteen is effectively absent in click terms: exactly how a query converts on paid while contributing nothing organically.
- **Brand-term spend**: eBay's large-scale experiment found ads on brand keywords added almost no incremental traffic where the company already ranked first ([Blake, Nosko & Tadelis, NBER](https://www.nber.org/papers/w20171)); Google's counter-study found ~89% of paid clicks are not recovered by organic when ads pause. The lesson is neither "cut all brand spend" nor "never touch it": it is *test it* on the exact terms where your organic result owns the top spot.
- **Share of rented demand per theme**: the brief-writer: two thirds of converting spend sitting in one category with weak organic tells you where the first content sprint goes.

## Interview prep

**"How would you build next quarter's content plan with evidence instead of opinion?"**
Pull paid converters, rank by the metric the business optimizes, filter to weak or absent organic rank, group by theme, and brief the pocket where rented demand concentrates. Every surviving row is a page backed by conversions that already happened.

**"Should we stop bidding on our brand terms?"**
Test, do not decree. Cite both sides: near-zero incrementality on brand terms where you rank first (eBay), but most paid clicks not recovered by organic on pause (Google). The candidate who knows both studies avoids the blanket answer in either direction.

**"If we rank a page for a query we are bidding on, will the ads help it rank faster?"**
No: the two are separate investments, and saying so unprompted is the credibility test. Paid proves the demand converts; organic ranking is earned separately and then compounds after you stop paying.

**"A query converts at 11% on paid and we sit at organic position 14. What is the move?"**
That is the leverage zone bordering on a content bet: a dedicated page plus title work can lift it into clickable territory while ads keep the demand warm. The trap is treating the paid CVR as a promise: it is an estimate from tuned landing pages and a different audience.

---

## File: diagnose/references/playbooks/seo/query-level-data.md

---
title: Query-level data: why aggregates mislead
question: What does the aggregate organic number hide, and at what level does the truth live
order: 3
---

"Organic converted at 2.2%" survives every meeting precisely because no one can interrogate it. The channel total is an average over things that should never be averaged: brand and non-brand demand, ten different intents, pages competing with each other. Read at the query level, the same month's data starts answering back.

## The framework

1. **Know why your two dashboards disagree.** Search Console counts clicks on Google's results page; GA4 counts sessions your own tag recorded, after consent banners and blockers took their cut. Clicks are not sessions; neither tool is lying. Each holds exactly the half the other is missing: Search Console knows queries but not conversions, GA4 knows conversions but not queries. Do not spend a week reconciling them.
2. **Read the three levels apart.** Property level describes, never explains. Query level counts one impression per search: a true read of demand. Query-page level counts one impression per page shown, so when two of your pages rank for the same search, summing the rows double-counts the demand. Read the query level for demand, the query-page level for which page answers it, and treat the double listing itself as a finding: keyword cannibalization, two pages splitting clicks and link equity.
3. **Cut brand from non-brand before reading any rate.** A blended 2.2% conversion rate can decompose into brand at 6% and non-brand at 0.7%: brand demand lending its warmth to hide a weak growth engine. Non-brand is the only part of organic that acquires new customers.
4. **Gather variants into clusters.** Search Console reports literal strings, so one intent arrives shattered into dozens of spellings, plurals, and misspellings. A top query can be under half of its own intent's demand; read the cluster and the demand roughly doubles without the market changing at all.
5. **Use the paid query as your organic crystal ball.** An organic conversion rate per query exists nowhere in your stack, but if you bid on the same queries, paid search has measured conversion per query at full price. Use that as the query's theoretical CVR to rank organic opportunities by conversion quality instead of raw volume.

## Metrics that matter, and their traps

- **Query-level impressions**: real demand, counted once per search. Trap: query-page rows double-count whenever two of your pages appear together.
- **Blended organic conversion rate**: against the ~2-3% ecommerce session average it can look healthy while the non-brand engine is broken. Split first, judge second.
- **Query-level position**: the topmost rank you held per search, so one strong page quietly masks how weakly a second page shows for the same term.
- **Theoretical CVR (paid CVR on the same query)**: an estimate for prioritization, never a measurement: ad clicks land on tuned pages and skewed audiences. High paid CVR with weak organic rank is where next quarter's content belongs; low paid CVR at any rank is informational demand: awareness, never the conversion priority. Cross-industry, search clicks convert around 7% ([WordStream](https://www.wordstream.com/blog/ws/2022/05/19/search-advertising-benchmarks)), but the per-query spread is the point.
- **Ranking metric choice**: a store ranks queries by conversion; an ad-supported publisher ranks by CTR and click volume, because the visit is what it sells. Business-model choice, not a default.

## Interview prep

**"Search Console shows 134k clicks and GA4 shows 127k organic sessions. Which is right?"**
Both: they measure different events in different places, on different sides of the click, with different losses. A strong candidate refuses the reconciliation project and reads each column against itself over time.

**"How would you find keyword cannibalization?"**
At the query-page level, the only level that sees it: one query, two of your URLs each logging impressions. The fix is consolidating intent onto one page, not tweaking two titles.

**"Why might a keyword-by-keyword read understate demand?"**
One intent fragments into dozens of string variants, each too small to matter when sorted by clicks. Cluster the variants and the demand often doubles; the reading changed, not the market.

**"How do you prioritize organic content bets without per-query conversion data?"**
Borrow the paid side: rank queries by their paid conversion rate as a theoretical CVR, then filter to weak organic rank. State the caveat unprompted: it ranks opportunities, it does not promise outcomes.

---

## File: diagnose/references/playbooks/seo/search-console-and-ga4.md

---
title: Search Console and GA4: find your CRO windows
question: Where is organic traffic being wasted on-site
order: 11
---

Use this when the question is "where is organic traffic being wasted on-site?" The goal is a shortlist of pages that earn organic traffic and engagement but lose the sale, each routed to the right owner: snippet, content/UX, or CRO.

## The framework

1. **Assemble the joined view.** Pull impressions, clicks, and position per page from Search Console's Performance report; pull sessions, engagement rate, conversions, and revenue per landing page from GA4, filtered to the Organic Search channel. Join on landing page (a spreadsheet works; the URL sets will not match perfectly (that is fine)). Each row now reads as one funnel: impressions → clicks → sessions → engagement → conversions → revenue.
2. **Sort by organic sessions descending.** You want the pages that already earn traffic.
3. **Walk each high-traffic page left to right and name where it breaks:**
   - Huge impressions, tiny clicks → **snippet** break. Owner: SEO (title/meta).
   - Clicks fine, low engagement → **content/UX** break. Owner: content or design.
   - Engagement fine, conversions near zero → **CRO window**. Owner: CRO (offer, CTA, checkout path).
   - High conversion, low sessions → not a problem: a starved winner. Feed it traffic; do not "optimize" it.
4. **Keep only the CRO-window pages** for a CRO sprint; route the others to their owners.

## Metrics that matter, and their traps

- **Clicks vs sessions**: different measurement systems (results-page counting vs on-site tagging after consent and blockers); the columns will never foot as arithmetic. Read the funnel *shape* per page and each column against itself over time; never sum across systems.
- **Engagement rate**: GA4 counts a session engaged after meaningful time, a second page, or a conversion event. It is the gate between an SEO problem and a CRO problem: low engagement means the page broke the query's promise; healthy engagement with no conversion means the page held them and the offer failed.
- **Conversions and revenue**: the pinhole detector. A page with hundreds of thousands of impressions, tens of thousands of sessions, healthy engagement, and a handful of transactions is the definition of a CRO window (often something as concrete as price display or size guidance below the fold).
- **The healthy-shape reference**: keep one page on the list that converts well, as proof the site *can* turn organic traffic into sales when the page earns it. It calibrates every other read.

## Interview prep

**"How do you connect Search Console and GA4, given they do not share metrics?"**
Join per landing page: SC brings impressions/clicks/position, GA4 (filtered to organic) brings engagement and conversion, and read each row as one funnel shape. A strong candidate volunteers that the columns will not reconcile and refuses to add across systems.

**"What separates a CRO problem from an SEO problem on the same page?"**
Where the funnel breaks: impressions-to-clicks is snippet (SEO), clicks-to-engagement is content/UX, engagement-to-conversion is CRO. Naming the transition names the owner; a shortlist without owners is just a chart.

**"A page has 9,400 organic sessions, 47% engagement, and 14 transactions. Diagnose it."**
Giant funnel, pinhole bottom: traffic and attention are earned, the purchase path fails: a CRO window, not a ranking or content job. Ask what changed on the page and what sits below the fold before proposing anything upstream.

---

## File: diagnose/references/playbooks/seo/search-console-and-sem.md

---
title: Search Console and paid search: mine content bets
question: What should next quarter's content target, backed by conversion evidence
order: 12
---

Use this when the question is "what should next quarter's content target, backed by evidence?" The goal is to find the queries your paid search has *proven* convert but that your organic side barely owns: the shortlist of content to build, ranked by the metric your business actually optimizes.

One caveat keeps the whole exercise honest: running ads on a query does not move its organic ranking. Ads here are a demand-discovery instrument: they prove, with money, which queries convert. The organic investment is a separate bet that then compounds.

## The framework

1. **Assemble the joined view.** Export the paid search terms report (with clicks, conversions, CVR) from your ads platform, and query-level impressions, clicks, and position from Search Console's Performance report. Match on query; the strings will not line up perfectly: normalize what you can and accept the rest.
2. **Pick your ranking metric: a business-model choice.** A store ranks by CVR, and only after choosing which conversion counts as the value event (purchase, subscription), or the rate means nothing. A publisher or ad-supported site ranks by CTR and click volume instead: a visit is the outcome it sells.
3. **Read each high-value query against its organic strength:**
   - High CVR (or CTR), organic empty or weak → **the content bet**: build the page and start compounding.
   - High CVR, organic position 4-20 → **leverage-zone push** while ads hold the fort.
   - High CVR, organic position 1-3 → you own it: why still paying? The brand-leakage check.
   - Low CVR at any rank → informational; awareness only, never the conversion priority.
4. **Group the survivors by theme** so the brief targets the pocket where rented demand concentrates, not row 214 of a flat export.

## Metrics that matter, and their traps

- **Paid CVR per query**: the best available estimate of what an organic click on the same query would be worth. Trap: it is an estimate, not a measurement: ad clicks land on tuned pages with a skewed audience. It ranks opportunities; it does not promise outcomes.
- **CVR before a conversion definition**: blank or meaningless until you pin which conversion event counts. Ranking by an unpinned CVR is the fastest way to a wrong brief.
- **Paid click volume at low CVR**: the informational trap for a store: a how-to query with huge volume and ~1% CVR drops to the bottom of a conversion-ranked list, even though a publisher would put it near the top, because for them the click *is* the revenue.
- **Organic position on converting queries**: an 11% CVR query stuck at organic position 14 is the first content bet: proven demand, page two, one dedicated page from clickable ([click-through collapses below the top results](https://backlinko.com/google-ctr-stats)).
- **Brand terms converting at #1 organic**: the "why still paying?" row. Test the bid rather than cutting it untested.

## Interview prep

**"How do you decide what content to build when organic data has no conversion column?"**
Borrow the paid side's per-query conversion rates as the prioritizer, filter to weak organic rank, and group by theme. State unprompted that the paid CVR is an estimate and that ads do not lift organic rank: those two caveats are the credibility test.

**"Would you rank the opportunity list the same way for a store and a publisher?"**
No: the ranking metric is a business-model choice. A store sorts by CVR against its chosen value event; an attention business sorts by CTR and click volume. Sorting by the wrong metric prioritizes the wrong pages for a quarter.

**"Paid shows a brand query converting at 14.8% and you rank #1 organically for it. What do you recommend?"**
A holdout test on the brand bid, not a decree: on exact terms where organic already owns the top spot the ad may buy a click you would get free, but pausing without a test risks the clicks organic does not recover. Frame it as spend to test, not spend to cut.

---

## File: diagnose/references/playbooks/seo/search-console-landing-pages.md

---
title: Search Console: coverage gaps and the snippet shortlist
question: Which pages need work, and what work
order: 9
---

Use this when the question is "which pages need work, and what work?" The goal is two page-level fix lists: pages that never surface (coverage gaps) and pages that surface but nobody clicks (the snippet shortlist), each with a concrete action attached.

## The framework

1. Open Search Console's **Performance report** and switch to the **Pages** tab, with impressions, clicks, CTR, and average position enabled.
2. **Coverage gaps first.** Compare your sitemap against the pages appearing here: any page in your sitemap with zero or absent impressions never surfaces at all: it is not indexed, blocked, or so off-target Google never shows it. Fix path: confirm indexability (check for stray `noindex`, use URL Inspection), give it real content, and point descriptive internal links at it.
3. **Snippet shortlist.** Sort by impressions descending and scan CTR. High-impression, low-CTR pages are the highest-ROI rewrites on the site: the ranking is already won, only the title and meta description are failing.
4. **Drill each shortlisted page to its queries** (filter by page, then view queries) to confirm it surfaces for what it was built for. If it ranks for another page's intent, you have keyword cannibalization: consolidate to one page per intent rather than rewriting two snippets.

## Metrics that matter, and their traps

- **Zero-impression sitemap pages**: the silent failure almost nobody checks. Trap: Search Console will not volunteer the list; you have to bring the sitemap and find the absences. A classic cause is a `noindex` left on after a launch.
- **Impressions × CTR per page**: a page at 210,000 impressions, position 4.7, and 0.2% CTR is the top of the snippet shortlist; one meta rewrite there beats a quarter of link-building.
- **Position 4-20 on a page's target query**: the rank-push list: content depth and internal anchors, not snippet work.
- **Page-to-query match**: a page can earn impressions on an intent it cannot serve; the CTR looks like a snippet problem but the fix is a different page. Always drill before prescribing.

## Interview prep

**"How do you find pages that are invisible in search?"**
Diff the sitemap against pages earning impressions: Search Console never volunteers the absences. Then triage each gap: indexability first (noindex, blocks), then thin content, then internal linking. These pages cost nothing to find and a lot to ignore.

**"What makes a page the highest-ROI fix on a site?"**
High impressions, decent position, terrible CTR: the rank is paid for and the snippet is refusing the click. A title and meta rewrite is hours of work against a quarter of link-building for the same click gain.

**"A page's CTR is low. How do you know whether it is the snippet or the page?"**
Drill to its queries. If it surfaces for its own intent, rewrite the snippet. If it surfaces for another page's intent, or alongside a sibling page, it is cannibalization or a mismatch, and the fix is consolidating or building the right page.

---

## File: diagnose/references/playbooks/seo/search-console-new-pages.md

---
title: Search Console: newly ranking pages into a content plan
question: Where is new organic demand appearing, and what should you build
order: 10
---

Use this when the question is "where is new organic demand appearing, and what should I build?" The goal is to rank the pages you have *started* ranking for by the demand they are catching, and decide which pockets deserve a dedicated page, more depth, or nothing.

## The framework

1. In Search Console's **Performance report (Pages tab)**, use a **date comparison** (this period against the previous one) and look for pages with impressions now that had none (or almost none) before. Those are your newly ranking pages.
2. **Check the pipeline is flowing.** Track how many genuinely new pages appear per month. If that trends toward zero, your clicks are being propped up by old pages: a separate alarm worth raising immediately.
3. **Sort the new entrants by clicks descending.** Demand that is already earning clicks is demand you are under-serving with dedicated content.
4. **Read each row against position and the page behind it:**
   - High new clicks, no dedicated page → **build** one (in commerce, sometimes: stock the thing). Searchers are arriving on approximations.
   - High new clicks, page exists, position 4-20 → **deepen** it and add internal links; it is almost competitive.
   - New demand in a low-value area → discovery, not obligation. Note it and move on.

## Metrics that matter, and their traps

- **Impressions on new pages**: the earliest signal content is finding demand, arriving well before clicks. Trap: high impressions from browsing queries is awareness churn, not a build order.
- **Clicks from new pages**: the strongest build signal when they land on a thin stub: real demand, a page that barely answers it, one content pass from competitive.
- **Position on new entrants**: noisy at low volume; each search instance returns a different position, so a fresh URL's average bounces on almost nothing. Read the direction of travel and give new pages time to settle before judging.
- **New pages per month**: pipeline health at a glance. The failure state is not a bad month; it is a flat line while old pages carry everything.

## Interview prep

**"How do you tell which new content is working before it earns traffic?"**
By impressions, not clicks: impressions rise months first, and clicks lag by design at page-two positions. A strong candidate says the lag is the opportunity: the demand is proven and the click is still on the table.

**"A newly ranking guide has 3,200 clicks at position 6.4 and it is a thin stub. What now?"**
That is an unmistakable build/deepen signal: demand arriving on a page that barely answers it. Deepen the page and add internal links rather than building a rival that splits the term.

**"What does a healthy content pipeline look like in Search Console?"**
A steady flow of new pages entering the report each month, some fraction climbing toward positions 10-20. Steady clicks with no new entrants underneath is a site coasting toward decline: the check most reports skip.

---

## File: diagnose/references/playbooks/seo/search-console-queries.md

---
title: Search Console: build a query worklist
question: How do you turn Search Console query data into this month's SEO worklist
order: 8
---

Use this when the question is "where do I point this month's SEO effort?" The goal is to leave with a query worklist in three buckets: snippet rewrites, rank pushes, and leave-alone, decided from one report in under fifteen minutes.

## The framework

1. Open Search Console's **Performance report** and switch to the **Queries** tab, with impressions, clicks, CTR, and average position all enabled. Read the columns in diagnostic order: impressions, position, CTR, clicks.
2. **Sort by impressions descending.** Demand leads. Ignore anything with a handful of impressions: that is sampling dust.
3. **Bucket each high-demand query** by comparing position against CTR:
   - Strong position (1-3), weak CTR → **snippet rewrite**. You rank; people scroll past.
   - Position 4-20 → **rank push** (content depth plus internal links). The leverage zone.
   - Position 1-3 with healthy CTR → **leave alone**. Defend, do not invest.
   - Position 50+ → **leave alone**. Too far to move without a rebuild.
4. **Drill any commercial query before committing effort:** filter to the query and its close variants (spellings, plurals) to confirm the pattern holds across the whole intent, not just the one string you sorted on.

## Metrics that matter, and their traps

- **Impressions**: the demand ranking that orders your worklist. Trap: tiny-impression rows are noise; bucketing them wastes the fifteen minutes.
- **CTR against position**: the bucketing signal. Top-three positions should pull roughly a 10-40% CTR band; a top-three query far below it is a snippet failure, the cheapest win on the board because the ranking is already won.
- **Average position**: an impression-weighted average, not a fixed slot. A query at 6.4 with heavy impressions and ~1% CTR is a textbook rank push; a brand term at 1.0 and 34% CTR is a leave-alone.
- **Clicks**: the outcome column, read last. Trap: sorting by clicks first optimizes pages that were already fine and buries the high-impression, low-click rows where the work is.

## Interview prep

**"You have fifteen minutes in Search Console. What do you produce?"**
A bucketed worklist, not observations: sort queries by impressions, split snippet rewrites (rank 1-3, weak CTR) from rank pushes (4-20) from leave-alones. A strong candidate names the action per bucket (title/meta rewrite versus content-and-links) and what they deliberately ignore.

**"A query ranks third with a 0.9% CTR. Cheap win or hard problem?"**
The cheapest win available: the ranking is won and the snippet is losing the click, so rewrite title and meta to the query's intent. The trap is prescribing links or content for what is a results-page relevance problem.

**"Why not work the whole query list evenly?"**
Because effort past position fifty rarely pays without a rebuild, and top-three healthy queries need defending, not investment. Concentrating on positions 4-20 is where a modest gain crosses into clickable territory.

---

## File: diagnose/references/playbooks/seo/seo-overview.md

---
title: Reading SEO performance stage by stage
question: How do you judge SEO performance beyond a single traffic number
order: 1
---

Organic search drives 60-77% of total site traffic for many businesses, and it is the one channel where the traffic keeps arriving after you stop paying for it. But "organic traffic is up 8%" is a verdict that hides which stage actually moved: pages falling out of the rankings, pages ranking lower, or pages holding position while the snippet stopped earning the click. Reading SEO stage by stage is the only way to tell those stories apart.

## The framework

1. **Reach.** Are you visible to the right searchers? Impressions and average ranking position. A page ranking eighth gets impressions but almost no clicks.
2. **The click.** Did visibility earn the click? High impressions with low click-through is a relevance or snippet problem, not a reach problem: the fix is a better title and meta description, not more rankings.
3. **Reach expansion.** Are you becoming visible for more searches over time? New queries widen the top of the funnel and are the demand-discovery signal most dashboards miss.
4. **Never read the property total.** Split by country, then device. A blended 3.6% CTR can hide a strong home-market desktop story carrying a second market that is seen and scrolled past on mobile.
5. **Make two honest splits.** Brand versus non-brand separates discovery from demand your other marketing created. And map each target query to exactly one page, covering informational, comparison, and transactional intent, so your pages never compete with each other.

## Metrics that matter, and their traps

- **Organic impressions**: the reach signal. Trap: impressions are ambient; they prove visibility, not interest.
- **Average position**: an impression-weighted average that hides the distribution; a query "averaging" eight may swing between three and fifteen. Read it as a trend. Working heuristic: positions 4-20 are the highest-leverage zone; defend the top three, ignore anything past fifty without a rebuild.
- **Click-through rate**: the real intent signal. Top-three positions should pull roughly 10-40% CTR ([Sistrix](https://www.sistrix.com/blog/why-almost-everything-you-knew-about-google-ctr-is-no-longer-valid/)); the top three take 68.7% of all clicks. A third-ranked page at 2% has a snippet problem, not a ranking problem.
- **Organic clicks, split brand vs non-brand**: clicks growing faster than impressions means CTR is improving, not just visibility expanding. Trap: a site coasting on brand clicks looks healthy while acquiring nobody new.
- **New queries**: the leading indicator. Trap in reverse: flat clicks propped up by a handful of old pages, with no new-query discovery underneath, is a site coasting toward decline.
- **Zero-impression sitemap pages**: silent failures: not indexed, blocked, or so off-target they never surface. Cheap to find, expensive to ignore.

Provenance caveat: Search Console lags two to three days, samples the long tail, and reports queries, not people, which is why the honest split is by query type, not by visitor.

## Interview prep

**"Organic traffic dropped 6% this month. How do you diagnose it?"**
A strong candidate refuses the aggregate: they split by country and device first, then separate position drops (ranking loss) from CTR drops at stable position (snippet mismatch), then check whether the loss is brand or non-brand. They avoid the trap of treating one blended number as one cause.

**"Where would you concentrate SEO effort across a large keyword set?"**
Positions 4-20 (page two and the bottom of page one) where a modest gain moves you into clickable territory. Top-three rankings need defending, not investing; past fifty is a rebuild. Spreading effort evenly is how teams work hard and move nothing.

**"A page ranks third but converts almost no impressions into clicks. What is your fix?"**
Rewrite the title tag and meta description to match query intent: the ranking is already won and links will not recover clicks the snippet is losing. The trap is prescribing link-building for what is a relevance problem on the results page.

**"What leading indicator would you watch for next quarter's organic growth?"**
New queries and newly ranking pages: they show demand being captured before it shows up as traffic. Also zero-impression sitemap pages, the coverage gap almost nobody checks.

---

## File: diagnose/references/playbooks/web-analytics/ga4-fundamentals.md

---
title: GA4 fundamentals, ranking channels by quality
question: Which channels actually earn engaged, buying traffic, not just the most sessions
order: 3
---

The default GA4 channel report sorts by sessions, and sessions are the easiest number to buy and the least meaningful to rank on. A channel ranking your budget conversation can stand on reads three lenses in order (attention, then how real it is, then what it is worth) and names the channel that is big but hollow.

## The framework

Work GA4's channel groups (Google's universal classification: Direct, Organic Search, Paid Search, Paid Social, Cross-network, Email, and so on) through three lenses:

1. **Attention: sessions.** Sort descending and note the giants. This is the starting order, never the verdict.
2. **Quality: engaged sessions and engagement rate.** The signature to hunt is a channel with huge sessions and an engagement rate far below the others: attention that evaporates on arrival. GA4 counts a session as engaged if it lasts over ten seconds, fires two or more pageviews, or triggers a key action.
3. **Value: transactions and revenue, read per engaged session.** Revenue per engaged session is the honest value-for-attention comparison across channels; it prices the traffic that actually stuck around.

A worked example: paid social tops the board at 410,000 sessions but engages at 23%, while direct, organic search and paid search all sit near 55%. Email, at a tenth of the volume, engages at 49% and carries €7,100 of revenue. The read writes itself: paid social is buying attention that mostly bounces, and email punches far above its volume. Neither fact is visible on a sessions-only chart.

One boundary: this ranks channel quality, not ROI. GA4 carries traffic and revenue by channel, not ad cost; true ROI needs spend reconciled from the ad platforms. Until then, read quality here and cost in the spend tools. Never approximate ROI by dividing revenue by raw sessions across channels with wildly different engagement rates.

## Metrics that matter, and their traps

- **Sessions by channel**: the attention lens. The trap: ranking on it. Volume is the cheapest thing a channel can deliver, and paid channels can top it indefinitely while converting nothing.
- **Engagement rate by channel**: the reality check on the giants. The trap: reading one channel's rate in isolation; the signal is the spread: one channel far below its peers is hollow.
- **Engaged sessions**: the honest denominator for value math; it filters out the ten-second bounces you paid for.
- **Revenue per engaged session**: the value-for-attention ratio the channel comparison can actually stand on. The trap: substituting revenue per raw session, which punishes high-engagement channels and flatters bouncy ones.
- **Revenue by channel**: the trap is treating GA4's revenue split as ROI; without cost per channel it says what a channel earned, not whether it paid.

## Interview prep

**"Paid social sends 4x more sessions than any other channel. Should it get more budget?"**
A strong candidate asks for engagement rate before answering. If it engages at 23% against ~55% for the rest, most of that volume evaporates on arrival: the next spend goes to fixing creative, targeting or the landing page, not to more traffic.

**"How would you compare email against paid search when email has a tenth of the traffic?"**
Per engaged session, not in totals: engagement rate to establish the traffic is real, then revenue per engaged session for value. Small channels with dense quality routinely beat giants on that read.

**"Can you compute channel ROI from GA4 alone?"**
No: GA4 carries traffic and revenue but not cost. They would reconcile ad spend from each platform beside the GA4 data, and refuse the revenue-over-raw-sessions shortcut.

**"A channel's engagement rate collapsed month over month. What are your hypotheses?"**
A traffic-mix change (a new campaign buying cheaper clicks), a landing-page change breaking the intent match, or a tagging change reclassifying traffic, in that order, each checkable in a day.

---

## File: diagnose/references/playbooks/web-analytics/marketing-funnel-overview.md

---
title: Reading the marketing funnel end to end
question: How do you read a marketing funnel from awareness to action and find where it leaks
order: 1
---

Reach can look great while revenue stays flat, and nobody can say which step broke: the data lives in six tools that disagree about what a conversion even is. A full-funnel read refuses to judge any stage in isolation: it measures every band of the funnel and, more importantly, every hand-off between them, because the transitions are where budget leaks and where almost no dashboard looks.

## The framework

The funnel has three bands, and the money leaks at the hand-offs:

1. **Awareness**: the right people learn you exist. Measure reach, impressions, and the click-through rate that proves the message landed. The hand-off question: did visibility earn a click and a visit?
2. **Consideration**: they weigh you against alternatives. Measure engaged visits, depth, return visits, email opens and clicks. The hand-off: did engagement become a conversion?
3. **Action**: they convert, then stay. Measure conversion rate, order value, ROAS, repeat purchase and lifetime value. The hand-off: did the spend pay back, and does value compound? A 5% lift in retention can raise profit 25-95% ([Reichheld, HBR](https://hbr.org/2014/10/the-value-of-keeping-the-right-customers)).

Then climb the value pyramid on every question: data → insight (what happened, in context) → diagnosis (why) → decision (what to do) → outcome (did it work). Most reporting stops at insight; the levels that change a quarter sit above it.

Finally, let the business pick the metric on top. A store optimizes for the sale (conversion rate, ROAS, LTV); a publisher sells attention and optimizes for sessions, depth and return visits. Same analytics, different number on top, and the ranking of every opportunity follows from that choice.

## Metrics that matter, and their traps

- **Click-through rate (awareness)**: separates a reach problem from a relevance problem. Plenty of impressions with low CTR means people saw you and scrolled past, a message problem no extra budget fixes.
- **Engagement rate (consideration)**: a click is only a promise; a visitor who bounces in two seconds never had a chance to convert. The lever is the landing page, targeting or relevance, not the budget.
- **Conversion rate (action)**: healthy rate on thin volume says scale the channel; fat top with a collapsing rate says fix the offer or page before spending another euro.
- **ROAS and payback**: whether the spend that won the customer comes back, and how fast. The trap: judging it before conversions are trustworthy across platforms that each define "conversion" differently.
- **Retention / LTV**: repeat purchase decides whether you have a business or a treadmill. The trap: comparing cohorts of different ages (an older cohort always has more cumulative revenue by definition).
- **Any band-level metric read alone**: a campaign with great reach and a dead landing page reads as "good awareness" on a vanity dashboard; across the funnel it is a broken awareness-to-consideration hand-off.

## Interview prep

**"Traffic is up 30% and revenue is flat. Walk me through your investigation."**
A strong candidate walks the hand-offs: did the new traffic engage (or bounce), did engagement convert, did conversions carry normal order values? They locate the first transition that broke rather than blaming the last band.

**"Brand and performance marketing are fighting over budget. How does measurement settle it?"**
They reject judging each in isolation: performance is easy to count, so budgets skew there and the top starves, even though emotionally-connected customers are more loyal. They propose one interlinked KPI set, each stage judged by how it lifts the next.

**"Why do most dashboards miss the leak?"**
Dashboards are built per data source, so each reports its own band; the leak lives between sources. The fix starts with unified definitions (one meaning of "conversion") so hand-off rates become computable.

**"Your CEO asks for one metric to run the company on. What do you say?"**
The overall evaluation criterion follows the business model (sale-based for a store, attention-based for a publisher) while the upper-funnel bands remain the diagnosis, not the goal.

---

## File: diagnose/references/playbooks/web-analytics/on-site-funnel.md

---
title: The on-site funnel in GA4
question: How do you read on-site behavior from session to revenue, and where does the money leak
order: 2
---

Every channel you run (SEO, search ads, social, email) ends in the same place: your site. GA4 owns that back half of the buyer's path, where a visit either engages, converts and spends, or leaks away the money you paid to earn it. Read it as a sequence of transitions, because traffic up 10% means nothing if the share of visits that convert fell by the same amount at the same time.

## The framework

Read on-site behavior as a chain, and cut every ratio two ways: by channel and by landing page, never blended:

1. **The session arrives**, tagged with the channel, campaign, source and medium that produced it.
2. **Does it engage?** GA4 counts a session as engaged if it lasts over ten seconds, fires two or more pageviews, or triggers a key action (the event-based successor to bounce rate). High sessions with low engagement is a landing-page or intent-match problem, not a traffic problem.
3. **Does engagement become a key action?** When conversion rate leaks, the fix lives in the path to the action (offer, form, checkout friction), not in more traffic.
4. **Was the action worth money?** Purchasers, transactions, revenue, and revenue per user.

On attribution: GA4 assigns conversion credit by model. Last-click overcredits closers (branded search, direct); first-click overcredits discovery; data-driven (the default) weighs each touch by measured contribution. Compare last-click against data-driven before touching a budget: the credit deltas are a sized fund-more/fund-less order. And credit is not cause: only an experiment (geo holdout, lift study) proves a channel drove conversions that would not have happened anyway.

## Metrics that matter, and their traps

- **Sessions**: volume that arrives with a falling engagement rate is the wrong kind of growth; never celebrate a session spike before checking engagement held.
- **Engagement rate**: healthy sites sit around 55-63%; below ~40% on a channel, the traffic and the landing page disagree. Trap: it can read high for structural reasons, since a one-page site clears the ten-second bar on almost every visit.
- **Average engagement time and pages per visit**: read together. Long duration with pages-per-visit near 1.0 usually means people are stuck, not absorbed.
- **Conversion rate**: ecommerce averages roughly 2-3% per session ([Statista](https://www.statista.com/statistics/439576/online-shopper-conversion-rate-worldwide/)). Trap: a site-wide blended rate describes no real visitor; direct converts far better than cold paid social. Cut by channel, and name the action you are counting.
- **Revenue per user**: the cleanest single health signal, folding engagement, conversion and order value into one number. Total revenue up while revenue per user falls means you bought growth: more traffic, thinner value per head.
- **Data-driven attribution**: needs roughly 400 conversions per conversion type over 28 days; below that GA4 silently falls back to last-click without telling you.

## Interview prep

**"Paid social sends thousands of sessions but conversion is near zero. Diagnose it."**
A strong candidate checks the session-to-engagement transition first: bounces inside ten seconds mean the ad and landing page disagree; engagement without conversion points at the checkout or offer. If the channel's visitors bounce on every page, the channel is buying the wrong audience: pull spend, do not rewrite pages.

**"Our site-wide conversion rate fell from 2.4% to 2.1%. Should we panic?"**
They refuse the blended number: a mix shift toward a low-converting channel moves it with no behavior change. They re-cut by channel and by named key action before concluding anything.

**"A channel gains 40% credit under data-driven versus last-click. What does that mean?"**
The channel contributes along the path but rarely lands last, so last-click habit was underfunding it. They also check the volume threshold, and note big reallocation bets still deserve an experiment.

**"Which single on-site number would you track weekly?"**
Revenue per user, with engagement rate by landing page as the diagnostic underneath: one says whether value per head is improving, the other names the page to fix.

---

## File: diagnose/references/playbooks/web-analytics/utm-tagging.md

---
title: UTM tagging
question: How do you group one campaign across every channel and trace it from click to revenue
order: 4
---

"What did the spring sale earn across every channel?" is a simple question that routinely costs a day, because each platform names the same campaign its own way and there is no shared key to group on. UTM tagging is the boring, upstream discipline that gives the day back: five parameters stamped identically on every link, on every channel, so one campaign is one groupable, traceable thing instead of three things you hand-match in a spreadsheet.

## The framework

1. **Know the five parameters.** `utm_source` = the specific platform (google, meta, your email tool). `utm_medium` = the channel type (paid search, paid social, display, email). `utm_campaign` = the theme that ties one effort together across platforms (the shared key you group on). `utm_content` = which creative or placement earned the click. `utm_term` = the paid keyword. Google Analytics reads them straight off the landing URL ([Google Analytics Help](https://support.google.com/analytics/answer/10917952)).
2. **Make the campaign key boring and identical everywhere.** One house style (lowercase, underscores, never improvised) so `spring_sale` collapses into a single row no matter which channel carried the click. The shared key is the join every cross-channel read depends on, and it exists only because you wrote it consistently.
3. **Read at altitude.** Consistent tags let you cluster campaigns hierarchically: channel, then objective, then theme, then creative. The blended top is on-target and unactionable; the euro to move shows up a level down, where an over-fed prospecting push and a starved retargeting cluster stop hiding in each other's averages.
4. **Trace click to revenue.** The tags survive from the platform to the till: web analytics names the visit by the campaign, then records the session, the transaction, the revenue. In a four-channel trace, display can pull ~7,800 sessions and earn ~£5,100 while email pulls ~2,400 and earns ~£14,900: a click ranking that inverts on revenue, visible only because the key matched on every link.
5. **Tag every channel**: auto-tagged paid search must still match the house scheme; untagged banner and bio links vanish into "direct"; hand partners tagged links; even a QR code on a poster can carry UTMs.

## Metrics that matter, and their traps

- **utm_campaign consistency**: the one parameter that must be written identically everywhere. One mistyped name splinters a campaign into unmatchable rows.
- **Sessions / transactions / revenue by campaign key**: the cross-channel read itself. The trap: judging channels on sessions; the click ranking often inverts on revenue.
- **Revenue by utm_content**: which creative actually carried the campaign; without it, a winning variant hides inside the channel total.
- **The "direct" and untagged bucket**: the tell of tagging drift: buyers look like anonymous traffic and revenue lands nameless. Nothing is broken, the money is just uncredited.
- **Tagging coverage**: the share of traffic and revenue reconciling to a named campaign. A scheme is only as good as its least disciplined link.

## Interview prep

**"Design a UTM scheme for a multi-channel launch. What matters most?"**
A strong candidate makes it dull: source = platform, medium = channel type, campaign = one theme in one house style. They emphasize the campaign key's cross-platform consistency over any clever naming, because grouping is the whole point.

**"Direct traffic spiked after the campaign started. What is your first hypothesis?"**
Untagged links: banners, bio links, or a partner sending traffic under whatever they pleased. They audit link tagging before inventing a story about brand lift.

**"Paid search auto-tags. Do you still need UTMs there?"**
The campaign name still has to match the house scheme, or paid search sits in its own silo instead of grouping with the same theme on email and social.

**"How do you answer 'what did the campaign earn' when finance asks?"**
Group every tagged link on the campaign key, read on-site transactions and revenue per channel, and disclose coverage: where tagging drifted, the figure is a floor, and the fix is discipline, not a different tool.
