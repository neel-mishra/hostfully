---
title: "Campaign Structure: us_linkedin_b2b-cold_lead-gen_mar26"
date_created: "2026-03-31"
last_updated: "2026-03-31"
status: "Draft"
platform: "linkedin"
objective: "Leads – Website Form Conversions"
description: "US B2B cold-prospecting LinkedIn lead generation campaign using website conversion forms."
---

# Campaign Structure: us_linkedin_b2b-cold_lead-gen_mar26

<!--
This file is intended to be populated by paid-ads-structure-agent.
Fill in platform-specific campaign/ad set/ad group structure,
bidding, budgets, audiences, placements, tracking, and checklists.
-->

## Metadata

| Field | Value |
|-------|-------|
| **Platform** | linkedin |
| **Objective** | Leads – Website Form Conversions |
| **Monthly Budget** | $5,000-$15,000 |
| **Date Created** | 2026-03-31 |
| **Status** | Draft |

## Companion Assets

| Asset | Link |
|-------|------|
| **Ad Creative (current)** | [ad-creative/us_linkedin_b2b-cold_lead-gen_mar26_ad-creative_mar26.md](ad-creative/us_linkedin_b2b-cold_lead-gen_mar26_ad-creative_mar26.md) |
| **Creative Briefs (current)** | [creative-briefs/mar26/](creative-briefs/mar26/_index.md) |
| **Creative deliverables (current)** | [creative-deliverables/mar26/](creative-deliverables/mar26/_index.md) |
| **Campaign Master Index** | [_index.md](_index.md) |

## Recommended LinkedIn Structure

- **Campaign objective:** Website Conversions (lead form submit on site)
- **Campaign type:** Manual Website Conversions (not Lead Gen Forms for this wave)
- **Budget model:** Campaign-level daily budget with ad-group guardrails
- **Suggested starting budget split:** 70% core prospecting, 30% expansion testing

### Campaign Layout

1. `LI_US_LeadGen_Cold_Core_Mar26`
   - Ad Group A: Job function + seniority (Ops/Marketing/Revenue, Manager+)
   - Ad Group B: Industry clusters (Vacation Rental, Hospitality Tech, PMS ecosystem)
2. `LI_US_LeadGen_Cold_Expansion_Mar26`
   - Ad Group C: Lookalike/Similar audiences from matched lists
   - Ad Group D: Interest/skill-based expansion

### Bidding, Delivery, and Guardrails

- **Bid strategy:** Maximize conversions (target CPC cap only if CPC inflation appears)
- **Optimization event:** Website lead submit (primary)
- **Placements:** LinkedIn feed + right rail (exclude audience network initially)
- **Frequency guardrail:** Keep weekly frequency < 5 on prospecting groups
- **Learning window:** No major structural edits for first 7 days

### Audience and Geography

- **Audience type:** B2B cold prospecting
- **Geo:** United States
- **Company list:** Not available for launch; use broad + role/industry targeting
- **First-party data available:** Email list + pixel data + CRM offline conversion capability

### Tracking and Naming

- **Analytics platform:** GA4
- **UTM convention:** Existing convention retained
- **Tracking state:** Healthy (tag/event implementation already validated)

## Open Questions

- Confirm precise ICP segments (title list, company size ranges, industries).
- Confirm monthly budget target inside $5k-$15k band.
- Confirm primary conversion event naming in both LinkedIn + GA4.

## Next Data Needed

- Existing UTM pattern example (`utm_campaign`, `utm_content`, `utm_term`).
- CRM stage mapping for offline conversion import.
- Negative audience exclusions (existing customers, competitors, job seekers).
