# Hostfully PMS Paid Ads Campaign (Q2 2026)

## Campaign Goal

Generate qualified demo requests for Hostfully Property Management Software (PMS) from vacation rental operators, with a focus on Tier B-C portfolios (5-30 properties) in the US.

## Primary KPI

- Demo form submissions (qualified)

## Secondary KPIs

- Cost per qualified demo (CPQD)
- Sales accepted lead rate
- Demo-to-opportunity rate
- Pipeline created from paid ads

## ICP and Segment Focus

Use portfolio-size segmentation from `business dna/core/ideal_customer_profile.md`.

- **Tier B (5-15 properties):** High MRR contribution, strong growth motion
- **Tier C (16-30 properties):** Higher average MRR, strong fit for automation and control messaging
- **Tier A (1-4 properties):** Included as expansion traffic, lower budget priority

Geo priority:

- **Primary:** United States (majority of count and MRR concentration)
- **Secondary test markets:** Canada, UK

## Messaging Pillars for This Campaign

Based on `business dna/identity/messaging_pillars.md`:

1. **Operational Clarity:** One connected operating system for bookings, inbox, tasks
2. **Revenue and Direct Growth:** Reduce OTA dependence and improve direct demand control
3. **Automation That Fits Real Workflows:** Save time on repetitive work while keeping teams in control

## Offer and Conversion Path

- **Primary offer:** Book a personalized Hostfully PMS demo
- **Secondary offer (retargeting):** "PMS evaluation checklist" download
- **Primary CTA:** Book demo
- **Landing page requirement:** Dedicated PMS page with segmented proof blocks by portfolio size

## Budget and Channel Mix (Starting Monthly Budget: $18,000)

- **Google Search:** 45% ($8,100)
- **Meta (Facebook/Instagram):** 30% ($5,400)
- **LinkedIn:** 20% ($3,600)
- **Retargeting reserve/testing:** 5% ($900)

If budget must start smaller, keep proportions and begin at $9,000 with the same structure.

## Channel Build

## 1) Google Search (High Intent Core)

### Campaigns

- `GG_US_PMS_HighIntent_BrandPlus_Q226`
- `GG_US_PMS_Competitor_Alt_Q226` (careful, respectful positioning only)
- `GG_US_PMS_FeatureIntent_Q226` (automation, direct booking, channel management)

### Ad Groups

- `vacation rental pms`
- `property management software`
- `short term rental software`
- `direct booking software`
- `guest communication software`

### Match Types

- Start with exact and phrase for control
- Add broad only after search term quality is stable

### Bidding

- Launch with Maximize Conversions
- Move to tCPA once at least 30 conversion events are stable

### Starting Guardrails

- Target CPC range benchmark: $4-$15 (monitor weekly)
- Pause terms with high spend and no qualified leads after sufficient clicks
- Add negatives weekly from search term reports

## 2) Meta (Pain-Point Creative + Retargeting Engine)

### Campaigns

- `META_US_PMS_Prospecting_TierBC_Q226`
- `META_US_PMS_Retargeting_AllSite_Q226`

### Prospecting Audiences

- Interests: vacation rental management, STR tools, property operations
- Lookalikes: qualified leads and demos (if seed quality is sufficient)
- Broad + creative testing for scale once baseline is found

### Retargeting Pools

- 30-day site visitors
- 30-day pricing page visitors
- 30-day form starters not submitted

### Creative Angles

- "Too many tools, too many tabs" (operational unification)
- "OTA dependence squeezes margins" (direct booking/control)
- "Scale portfolio without operational chaos" (automation + workflow reliability)

## 3) LinkedIn (Mid-Market Operator Decision Makers)

### Campaign

- `LI_US_PMS_Demo_MidMarket_Q226`

### Targeting

- Titles/functions: Operations Manager, Director of Operations, Revenue Manager, Property Manager, Founder/Owner-Operator (qualified company size only)
- Industry filters: Vacation Rentals, Hospitality, Real Estate Services (test subsets)
- Company size: prioritize SMB-midmarket bands aligned with Tier B-C operator profile

### Objective

- Website conversions (demo submit)

### Use Case

Highest-value channel for quality filtering, not top volume.

## Funnel Architecture

- **Top of funnel:** Meta prospecting + non-brand Google terms
- **Middle of funnel:** Meta retargeting + LinkedIn role-based conversion campaigns
- **Bottom of funnel:** Brand search capture + high-intent remarketing to demo

## Creative and Copy Starter Set

## Google RSA Headlines

- Property Management Software for Vacation Rentals
- Run Bookings, Messages, and Tasks in One Place
- Scale Your Portfolio Without Operational Chaos
- Reduce Manual Work Across Your Team
- Turn More Demand Into Direct Bookings
- Built for Short-Term Rental Operators

## Google Descriptions

- Hostfully PMS helps vacation rental teams run bookings, communication, and workflows in one connected platform.
- Save time with automation, improve visibility, and support direct booking growth with software built for real operators.

## Meta Primary Text Variants

1. Managing 5 to 30 properties should not require five disconnected tools. Hostfully PMS brings bookings, guest communication, and workflows into one operating layer. Book a demo.
2. If your team is buried in inbox volume and manual handoffs, your systems are costing you growth. Hostfully helps vacation rental operators automate repetitive work and stay in control.
3. OTA-heavy revenue can limit margin and control. Hostfully PMS gives operators the tools to strengthen direct booking strategy while keeping operations clean.

## LinkedIn Ad Copy Variant

Vacation rental operators do not need more software noise. They need one system that keeps operations reliable as portfolios grow. Hostfully PMS centralizes booking operations, communication, and workflow automation so your team can execute faster with fewer breakdowns. Book a demo.

## Measurement Plan

## Core Events

- `demo_submit` (primary)
- `demo_start` (secondary diagnostic)
- `pricing_page_view` (mid-funnel intent)
- `checklist_download` (secondary conversion)

## Attribution and Tracking

- Use standardized UTMs across channels:
  - `utm_source`: google, meta, linkedin
  - `utm_medium`: cpc, paid_social
  - `utm_campaign`: channel_geo_offer_audience_q226
  - `utm_content`: creative-angle_variant
  - `utm_term`: keyword (search only)
- Sync conversion events into CRM and report by:
  - Channel
  - Campaign
  - Portfolio tier (if captured on form)
  - Sales stage progression

## 30-Day Launch Plan

## Week 1 (Build and QA)

- Build campaigns, ad groups, audiences, and conversion events
- Launch with 2-3 creatives per ad set/ad group
- QA UTMs, event firing, form mapping, CRM routing

## Week 2 (Stabilize)

- No major restructuring during learning period
- Add negative keywords and placements controls
- Pause underperforming creatives with weak CTR and no lead quality

## Week 3 (Optimize)

- Shift 10-20% budget from weakest to strongest campaigns
- Promote top-performing creative angle into all channels
- Test one new headline cluster and one new meta visual concept

## Week 4 (Scale and Decide)

- Scale winners by 15-25% budget increments
- Evaluate CPQD and pipeline contribution by channel
- Decide keep/kill for each audience and creative angle

## Exclusions and Hygiene

- Exclude current customers from cold prospecting
- Exclude job seekers and irrelevant low-intent segments where possible
- Maintain competitor-safe, respectful comparison language
- Do not use hard ROI promises without validated case-study constraints

## What to Build Next

1. Channel-specific build sheets for Google, Meta, and LinkedIn
2. Dedicated PMS landing page with segment-specific proof blocks (Tier A vs B-C)
3. Monthly creative rotation file (`apr26`) with 6-9 net new variants
