---
title: "Campaign Structure: us-ca_meta_leads_reader-acquisition_mar26"
date_created: "2026-03-16"
last_updated: "2026-03-16"
status: "Draft"
platform: "Meta (Facebook + Instagram)"
objective: "Leads – Newsletter Signups"
monthly_budget_usd: 10000
---

# Campaign Structure: us-ca_meta_leads_reader-acquisition_mar26

| Field | Value |
|-------|-------|
| **Platform** | Meta (Facebook + Instagram) |
| **Objective** | Leads – newsletter signups for TLDR tech |
| **Monthly Budget** | \$10,000 |
| **Date Created** | 2026-03-16 |
| **Last Updated** | 2026-03-16 |
| **Status** | Draft |

## Companion Assets

| Asset | Link |
|-------|------|
| **Ad Creative (current)** | [us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md](us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md) |
| **Creative Briefs (current)** | [creative-briefs/mar26/](creative-briefs/mar26/_index.md) |
| **Campaign Master Index** | [_index.md](_index.md) |

---

## Campaign Level

- **Campaign name**: `us-ca_meta_leads_reader-acquisition_mar26`
- **Platform**: Meta (Facebook + Instagram)
- **Business objective**: Acquire free TLDR tech newsletter subscribers
- **Meta objective**: Leads
- **Conversion location**: Website
- **Primary conversion event**: `Subscribe` / `CompleteRegistration` on newsletter thank-you page
- **Monthly budget**: \$10,000
- **Daily budget (approx.)**: \$330/day (10,000 ÷ 30.4)
- **Budget optimization**: Ad set budget optimization (ABO) to start
- **Bidding strategy**: Lowest Cost (no cap) for first 2–3 weeks; consider Cost Cap after stable CPA
- **Schedule**: Ongoing, starting once assets and tracking QA complete
- **Location**: United States, Canada
- **Language**: English
- **Placements**: Advantage+ placements (all) enabled
- **Attribution window**: 7-day click, 1-day view
- **Special ad category**: None
- **Naming convention**:
  - Campaign: `{region}_{platform}_{objective}_{audience}_{date}` → `us-ca_meta_leads_reader-acquisition_mar26`
  - Ad set: `{targeting-type}_{audience-segment}_{funnel-stage}`
  - Ad: `{format}_{hook}_{date}_{version}`

### Tracking & URL Options (Campaign-Level)

- **UTM template** (appended at ad level):
  - `?utm_source=facebook&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}`
- **Destination URL example**:
  - `https://tldr.newsletter/signup?utm_source=facebook&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}`
- **Analytics**: GA4 as primary analytics, with UTMs mapped into CRM where applicable
- **Conversion tracking**:
  - Meta Pixel installed on all landing pages and thank-you page
  - Conversions API (CAPI) enabled via GTM or native integration
  - `event_id` used to deduplicate client + server events
  - `Subscribe` / `CompleteRegistration` configured as highest-priority event in Aggregated Event Measurement

---

## Ad Set Structure

### Ad Set 1: Broad / Advantage+ Audience (Prospecting)

- **Ad set name**: `broad_advantageplus_readers_prospecting`
- **Funnel stage**: Cold prospecting
- **Budget**: \$120/day
- **Conversion location**: Website
- **Conversion event**: `Subscribe` / `CompleteRegistration`
- **Audience**:
  - Advantage+ Audience: ON
  - Locations: United States, Canada
  - Age: 22–55
  - Gender: All
  - Hard constraints: location + minimum age only
  - Soft suggestions in Advantage+ Audience: tech, startups, AI, software, business & finance, productivity, newsletters
- **Placements**: Advantage+ placements ON (all placements eligible)
- **Optimization goal**: Conversions
- **Bidding strategy**: Lowest Cost
- **Schedule**: Ongoing
- **Exclusions**:
  - Existing subscribers (customer list)
  - Recent converters (custom audience of thank-you page visitors / conversion event)

### Ad Set 2: Interest Stack – Tech & Business (Prospecting)

- **Ad set name**: `interests_tech-biz-news_prospecting`
- **Funnel stage**: Cold prospecting
- **Budget**: \$90/day
- **Conversion location**: Website
- **Conversion event**: `Subscribe` / `CompleteRegistration`
- **Audience**:
  - Locations: United States, Canada
  - Age: 22–55
  - Gender: All
  - Detailed targeting (interests):
    - Technology
    - Startups
    - Online advertising
    - Software as a service (SaaS)
    - Business & industry
    - Entrepreneurship
  - Detailed targeting expansion: OFF (keep this as a controlled interest test)
- **Placements**: Advantage+ placements ON
- **Optimization goal**: Conversions
- **Bidding strategy**: Lowest Cost
- **Schedule**: Ongoing
- **Exclusions**:
  - Existing subscribers (customer list)
  - Recent converters (thank-you page / conversion event)

### Ad Set 3: Lookalike of Subscribers – 1% (Prospecting)

- **Ad set name**: `lal_subscribers-1pct_usca_prospecting`
- **Funnel stage**: Cold prospecting, high-fit
- **Budget**: \$80/day
- **Conversion location**: Website
- **Conversion event**: `Subscribe` / `CompleteRegistration`
- **Audience**:
  - Source: customer list of existing TLDR newsletter subscribers
  - Lookalike: 1% in United States + Canada
  - Age: 22–55
  - Gender: All
- **Placements**: Advantage+ placements ON
- **Optimization goal**: Conversions
- **Bidding strategy**: Lowest Cost
- **Schedule**: Ongoing
- **Exclusions**:
  - Existing subscribers (source list)
  - Recent converters (thank-you page / conversion event)

### Ad Set 4: Warm Retargeting – Site Visitors & Engagers

- **Ad set name**: `retargeting_site-visitors30_engagers90`
- **Funnel stage**: Warm retargeting
- **Budget**: \$40/day
- **Conversion location**: Website
- **Conversion event**: `Subscribe` / `CompleteRegistration`
- **Audience**:
  - Website visitors (all pages) last 30 days, excluding converters
  - Facebook Page and Instagram profile engagers last 90 days, excluding converters
  - Optional: video viewers of TLDR creative (25%+ watched) last 90 days
- **Placements**: Advantage+ placements ON
- **Optimization goal**: Conversions
- **Bidding strategy**: Lowest Cost
- **Schedule**: Ongoing
- **Frequency control**:
  - Monitor frequency; if 5–7+ impressions per person per week, consider:
    - Additional creative variants
    - Frequency caps at ad set level (if available)
    - Expanding warm audiences (longer lookback windows)

---

## Ad Assets (Structural)

- **Ad formats**:
  - Static single image (email UI preview, mobile inbox screenshot, highlights from an issue)
  - Short vertical video (9:16) – founder/host style or UGC testimonial
  - Carousel optional – “What you get in TLDR” (news, tools, ideas)
- **Ad naming**:
  - `static_pain-point_mar26_v1`
  - `static_social-proof_mar26_v1`
  - `video_founder-explainer_mar26_v1`
  - `ugc_reader-testimonial_mar26_v1`
- **Tracking**:
  - All final URLs include the UTM template:
    - `?utm_source=facebook&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}`
- **Lead forms**:
  - Not used in this initial structure (primary conversion is on-site newsletter signup)
- **Creative direction pointer**:
  - Detailed copy, hooks, and visual directions are handled by `ad-creative-agent` and `visual-creative-brief-agent` for this campaign and saved into:
    - `us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md`
    - `creative-briefs/mar26/`

---

## Tracking Setup

- **Pixels & tags**:
  - Meta Pixel installed on:
    - Newsletter signup landing page (`/signup` or equivalent)
    - Thank-you / confirmation page
  - Conversion event:
    - `Subscribe` / `CompleteRegistration` fired on thank-you page
  - CAPI:
    - Implemented via GTM or native Meta integration
    - `event_id` shared between browser and server events for deduplication
- **UTMs**:
  - Full parameter set required on all ad destination URLs:
    - `utm_source=facebook`
    - `utm_medium=paid-social`
    - `utm_campaign={{campaign.name}}`
    - `utm_term={{adset.name}}`
    - `utm_content={{ad.name}}`
  - All lowercase, hyphens within values, no spaces
- **Analytics platform**:
  - GA4 as primary analytics destination
  - Events:
    - `page_view` on landing page and thank-you page
    - `generate_lead` or custom `newsletter_subscribe` aligned with Meta conversion event
  - Attribution:
    - Data-driven or last-click in GA4; ensure expectations are aligned with Meta’s 7-day click / 1-day view
- **CRM / downstream** (optional but recommended):
  - UTM parameters captured via hidden fields or cookies on signup forms
  - UTM values mapped into CRM contact fields

---

## Pre-Launch Checklist (Meta + Universal)

### Universal

- [ ] Conversion tracking pixel/tag installed on landing and thank-you pages
- [ ] Conversion event (`Subscribe` / `CompleteRegistration`) created and receiving test data
- [ ] All ad destination URLs contain full UTM parameter set
- [ ] UTMs tested by clicking preview ads and confirming parameters persist through redirects
- [ ] Daily budgets sum to approximately \$330/day (no unintended extra campaigns drawing spend)
- [ ] Audience sizes are sufficient:
  - Prospecting: at least 1–10M people per ad set where possible
  - Retargeting: large enough for learning but not so broad that it includes non-engaged users
- [ ] Naming convention applied consistently at campaign, ad set, and ad levels
- [ ] Landing page:
  - Fast on mobile (<3 seconds)
  - Clear value proposition above the fold
  - Minimal form friction (email-only preferred)
  - Privacy policy and compliance requirements met

### Meta-Specific

- [ ] Special ad category set correctly (None for this campaign)
- [ ] Conversions API configured and deduplicating with Pixel via `event_id`
- [ ] Advantage+ placements intentional; no unexpected manual exclusions
- [ ] Attribution window set to 7-day click, 1-day view in campaign settings
- [ ] Aggregated Event Measurement priority configured with `Subscribe` / `CompleteRegistration` at appropriate rank
- [ ] Dynamic creative decision:
  - Either ON for rapid creative mixing
  - Or OFF to maintain strict control of which combinations run (recommended for clean testing)
- [ ] Tested a full click-through from ad preview → signup → thank-you page and confirmed:
  - Meta conversion fires
  - GA4 event is recorded
  - UTMs appear in analytics and (if applicable) CRM

---

## Notes & Next Steps

1. Run `ad-creative-agent` for this campaign to generate March 2026 creative concepts and full copy into `us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md`.
2. Run `visual-creative-brief-agent` to produce designer-ready briefs under `creative-briefs/mar26/`.
3. Use this structure as the build guide for `social_ads_agent` when creating the campaign in Meta Ads Manager.
4. After 2–3 weeks of stable delivery, evaluate CPA and consider:
   - Shifting from ABO to CBO with heavier weighting toward winning audiences
   - Testing Cost Cap bidding using observed CPA as baseline.

