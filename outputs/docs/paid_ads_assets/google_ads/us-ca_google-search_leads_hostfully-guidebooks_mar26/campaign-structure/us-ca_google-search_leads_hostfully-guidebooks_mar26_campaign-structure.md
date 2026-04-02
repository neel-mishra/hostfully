---
title: "Campaign Structure: us-ca_google-search_leads_hostfully-guidebooks_mar26"
date_created: "2026-03-31"
last_updated: "2026-03-31"
status: "Draft"
platform: "google_ads"
objective: "Leads – Demo Booked"
description: "Google Search lead-generation campaign promoting Hostfully Digital Guidebooks in the US and Canada."
---

# Campaign Structure: us-ca_google-search_leads_hostfully-guidebooks_mar26

## Metadata

| Field | Value |
|-------|-------|
| Platform | google_ads |
| Objective | Leads - Demo Booked |
| Geo | US + Canada |
| Landing page | https://www.hostfully.com/digital-guidebooks/ |
| Channel scope | Search only |
| Budget range | $3,000-$10,000 monthly |

## Core Differentiators to Lead With

1. Extra revenue from guidebooks (upsells, add-ons, referral opportunities).
2. Fast setup plus easy scale across one or many properties.
3. Better guest experience with less repetitive support overhead.

## Campaign Layout

1. `GS_USCA_Guidebooks_Brand_mar26`
   - `AG_Brand_Guidebooks_Core`
2. `GS_USCA_Guidebooks_Nonbrand_HighIntent_mar26`
   - `AG_Digital_Guidebook_Software`
   - `AG_Vacation_Rental_Guidebook`
3. `GS_USCA_Guidebooks_Nonbrand_Outcome_mar26`
   - `AG_Guest_Experience_Improvement`
   - `AG_Upsell_And_Addon_Revenue`
4. `GS_USCA_Guidebooks_RLSA_mar26`
   - `AG_RLSA_HighIntent_Keywords`

## Budget Allocation

- Brand: 20%
- Nonbrand High Intent: 45%
- Nonbrand Outcome: 25%
- RLSA layer: 10%

## Bidding and Delivery

- Initial strategy: Maximize Conversions.
- Optimization event: `demo_booked` (primary conversion).
- Transition to tCPA after stable conversion volume.
- Search network only at launch.

## Match Type and Query Control

- Launch with exact and phrase match only.
- Weekly search query reviews for negatives.
- Expand to broad only after query quality is stable.

## Negative Keyword Baseline

- jobs, career, salary
- pdf, free pdf, template (review weekly before broad blocking)
- definition, meaning
- tour guide jobs

## Tracking and Naming

- Primary conversion: confirmed demo booked.
- Secondary conversions: form start and form submit.
- Stack: GA4 + GTM + Google Ads conversion tag.
- Naming convention: `GS_{Geo}_{Theme}_{Intent}_{Month}`.

## Guardrails

- Follow Hostfully brand voice.
- Do not reference or name competitors.
- Keep claims specific and supportable from landing page content.
