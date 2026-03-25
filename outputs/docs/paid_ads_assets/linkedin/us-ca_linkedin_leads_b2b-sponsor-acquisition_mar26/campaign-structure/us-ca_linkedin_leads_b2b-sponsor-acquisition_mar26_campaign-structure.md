---
title: "Campaign Structure: us-ca_linkedin_leads_b2b-sponsor-acquisition_mar26"
date_created: "2026-03-16"
last_updated: "2026-03-16"
status: "Draft"
platform: "linkedin"
objective: "Leads – TLDR B2B Sponsors"
description: "Paid linkedin campaign for Leads – TLDR B2B Sponsors."
---

# Campaign Structure: us-ca_linkedin_leads_b2b-sponsor-acquisition_mar26

<!--
This file is intended to be populated by paid-ads-structure-agent.
Fill in platform-specific campaign/ad set/ad group structure,
bidding, budgets, audiences, placements, tracking, and checklists.
-->

## Metadata

| Field | Value |
|-------|-------|
| **Platform** | LinkedIn |
| **Objective** | SQL meetings with TLDR B2B sponsors |
| **Monthly Budget** | ~$10,000 |
| **Date Created** | 2026-03-16 |
| **Status** | Draft |

## Companion Assets

| Asset | Link |
|-------|------|
| **Ad Creative (current)** | [us-ca_linkedin_leads_b2b-sponsor-acquisition_mar26_ad-creative_mar26.md](us-ca_linkedin_leads_b2b-sponsor-acquisition_mar26_ad-creative_mar26.md) |
| **Creative Briefs (current)** | [creative-briefs/mar26/](creative-briefs/mar26/_index.md) |
| **Campaign Master Index** | [_index.md](_index.md) |

---

## LinkedIn Foundations (from questionnaire)

- **Platform:** LinkedIn (single-channel for this campaign)
- **Business objective:** Sales-qualified sponsor meetings booked
- **Monthly budget:** Around $10,000/month
- **Campaign type:** New (net-new LinkedIn sponsor program)

### Audience & Funnel

- **Target roles:**
  - Demand Gen / Growth / Performance marketers at B2B SaaS companies
  - VP Marketing / CMO / Head of Marketing at B2B SaaS
- **Company size focus:**
  - 50–500 employees (growth-stage SaaS)
  - 200–2000 employees (mid-market / light enterprise)
- **Funnel stage:**
  - Mixed: cold prospecting + warm (implemented as separate campaigns or ad sets)
  - This campaign will primarily cover **cold prospecting**, with warm audiences configured separately.
- **First-party data:**
  - Target account **company list** for ideal B2B sponsors
  - (Retargeting audiences can be layered later: website visitors to /advertise or /sponsors pages.)
- **Geo:**
  - United States only

---

## Campaign Group & Campaign Level

- **Campaign Group name:** `us_linkedin_sponsors_tldr_mar26`
  - Purpose: Group all sponsor-acquisition campaigns for reporting.

- **Campaign name:** `us-ca_linkedin_leads_b2b-sponsor-acquisition_mar26`

- **Objective:** Lead Generation or Website Conversions (depending on whether you use in-platform Lead Gen Forms or website forms for meetings).
  - Recommended starting point: **Website Conversions** → book a sponsor intro call on your site.

- **Budget:** ~$10,000/month
  - Approx daily: `$10,000 / 30.4 ≈ $330/day`.
  - Start with **campaign-level daily budget** and adjust based on performance.

- **Bidding strategy:** Maximum Delivery (auto) to start, then optionally Target Cost once CPA stabilizes.

- **Schedule:** Ongoing; ads run continuously.

---

## Ad Set / Audience Structure

LinkedIn uses “Campaigns” as the level where audiences are defined; we will model **three campaigns** inside this group, each targeting a distinct segment.

### 1) Campaign A – Demand Gen & Growth Marketers (Cold Prospecting)

- **Suggested name:** `us_linkedin_leads_sponsors_demand-gen_mar26`
- **Objective:** Website Conversions (book meeting / request sponsor kit).
- **Daily budget:** ~$140/day.

**Targeting:**

- **Location:** United States.
- **Company size:** 50–500 and 200–2000 employees.
- **Industries:** Software & IT Services, Internet, Computer Software, Information Technology & Services, Marketing & Advertising (for tools/agency sponsors).
- **Job functions:** Marketing, Growth, Demand Generation, Digital Marketing.
- **Seniority:** Manager, Senior, Director, VP, Head.
- **Job titles (examples, not exhaustive):**
  - “Demand Generation Manager”, “Growth Marketing Manager”, “Performance Marketing Manager”, “Head of Demand Gen”.
- **Interests / Groups (optional):**
  - Interests in “Online Advertising”, “Digital Marketing”, “B2B Marketing”.

### 2) Campaign B – Marketing Leadership (Cold Prospecting)

- **Suggested name:** `us_linkedin_leads_sponsors_marketing-leaders_mar26`
- **Objective:** Website Conversions.
- **Daily budget:** ~$120/day.

**Targeting:**

- **Location:** United States.
- **Company size:** 50–500 and 200–2000 employees.
- **Job functions:** Marketing, Business Development.
- **Seniority:** Director, VP, C-level, Owner, Partner, Head.
- **Job titles (examples):**
  - “VP Marketing”, “CMO”, “Head of Marketing”, “Director of Marketing”, “VP Growth”.
- **Industries:** Same as Campaign A (B2B SaaS-focused).

### 3) Campaign C – Target Account List (ABM)

- **Suggested name:** `us_linkedin_leads_sponsors_abm-target-accounts_mar26`
- **Objective:** Website Conversions.
- **Daily budget:** ~$70/day (scale up once performance validates).

**Targeting:**

- **Location:** United States.
- **Company list:** Upload your **ideal sponsor account list** as a Matched Audience.
- **Company size:** 50–500 and/or 200–2000 where known.
- **Job functions:** Marketing, Growth, Demand Gen, RevOps.
- **Seniority:** Manager → C-level.

---

## Creative & Ad Format Notes (Structural)

- **Ad formats:**
  - Single Image Ads (primary).
  - Document Ads for sponsor one-pagers / case studies.
  - Video Ads (short explainer or testimonial) as a secondary test.

- **Primary CTA buttons:**
  - “Book a demo”, “Learn more”, or “Contact us” depending on whether you send to a meeting-booking page or sponsor overview page.

- **Destination:**
  - Dedicated “Advertise with TLDR” or sponsor landing page with:
    - Clear value prop vs. LinkedIn / other paid channels.
    - Audience breakdown, case studies, pricing/starting-at info, and a **short form** to request a call.

---

## Tracking & Naming Standards (LinkedIn)

- **Naming convention:**
  - Campaign group: `us_linkedin_sponsors_tldr_{mmmyy}`.
  - Campaign: `{region}_linkedin_leads_sponsors_{segment}_{mmmyy}`.
  - Creative: `{format}_{angle}_{mmmyy}_v{N}` (e.g., `singleimg_vs-paid-social_mar26_v1`).

- **UTM template (example):**

  ```text
  ?utm_source=linkedin&utm_medium=paid-social&utm_campaign={campaign_name}&utm_content={creative_name}
  ```

  Replace `{campaign_name}` and `{creative_name}` with the actual LinkedIn name or macros.

---

## Pre-Launch Checklist (LinkedIn-Specific)

- [ ] Insight Tag installed and firing on sponsor landing + thank-you pages.
- [ ] Conversion action for “Sponsor meeting booked” or “Sponsor lead submitted” configured.
- [ ] All campaigns use consistent naming conventions.
- [ ] All destination URLs include UTMs.
- [ ] Audiences sized appropriately (20–500k where possible for prospecting; smaller, more targeted for ABM).
- [ ] Initial bids left on Maximum Delivery; no restrictive bid caps at launch.

