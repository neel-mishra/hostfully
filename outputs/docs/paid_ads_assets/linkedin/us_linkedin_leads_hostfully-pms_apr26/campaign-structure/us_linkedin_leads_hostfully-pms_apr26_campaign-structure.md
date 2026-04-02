---
title: "Campaign Structure: us_linkedin_leads_hostfully-pms_apr26"
date_created: "2026-03-31"
last_updated: "2026-03-31"
status: "Draft"
platform: "linkedin"
objective: "Leads – PMS Demo Requests"
description: "LinkedIn lead-generation campaign promoting Hostfully PMS to short-term rental operators and property managers."
---

# Campaign Structure: us_linkedin_leads_hostfully-pms_apr26

<!--
This file is intended to be populated by paid-ads-structure-agent.
Fill in platform-specific campaign/ad set/ad group structure,
bidding, budgets, audiences, placements, tracking, and checklists.
-->

## Metadata

| Field | Value |
|-------|-------|
| **Platform** | linkedin |
| **Objective** | Leads – PMS Demo Requests |
| **Monthly Budget** | $12,000 |
| **Date Created** | 2026-03-31 |
| **Status** | Draft |

## Companion Assets

| Asset | Link |
|-------|------|
| **Ad Creative (current)** | [ad-creative/us_linkedin_leads_hostfully-pms_apr26_ad-creative_apr26.md](ad-creative/us_linkedin_leads_hostfully-pms_apr26_ad-creative_apr26.md) |
| **Creative Briefs (current)** | [creative-briefs/apr26/](creative-briefs/apr26/_index.md) |
| **Creative deliverables (current)** | [creative-deliverables/apr26/](creative-deliverables/apr26/_index.md) |
| **Campaign Master Index** | [_index.md](_index.md) |

## Recommended LinkedIn Structure

- **Objective:** Website conversions (PMS demo requests)
- **Campaign architecture:** Role-based core audiences + expansion audiences
- **Budget split:** 70% core, 20% expansion, 10% retargeting
- **Geo:** United States

### Campaign Layout

1. `LI_US_PMS_Leads_Core_apr26`
   - `AG1_RevOps_And_Marketing_Leaders_US`
   - `AG2_Property_Managers_And_Ops_US`
2. `LI_US_PMS_Leads_Expansion_apr26`
   - `AG3_Broad_Industry_Skills_US`
3. `LI_US_PMS_Leads_Retargeting_apr26`
   - `AG4_Site_Visitors_30d_US`
   - `AG5_High_Intent_Pages_14d_US`

### Bidding and Delivery

- **Bid strategy:** Maximize conversions (manual CPC cap fallback if CPC spikes)
- **Optimization event:** `demo_request_submit`
- **Placement scope:** LinkedIn feed first, then right rail after week 1
- **Frequency guardrail:** Prospecting ad groups target <= 4.5 weekly frequency

### Audience Framework

- **Primary personas:** STR operators, property management leaders, RevOps/marketing decision-makers
- **Company size focus:** 11-500 employees (primary), 501-2000 (test)
- **Exclusions:** Existing customers, active opportunities, recent demo submitters

### Tracking and Naming

- **Analytics:** GA4 + CRM attribution backfill
- **UTMs:** Existing convention with strict `utm_campaign=us_linkedin_leads_hostfully-pms_apr26`
- **Naming pattern:** `LI_{Geo}_{Theme}_{Stage}_{Month}`

## Open Questions

- Final approved account list for ABM overlay (if added in wave 2).
- Which CRM stage defines a qualified lead for optimization feedback?
- Should retargeting include video-engagers from non-PMS campaigns?

## Next Data Needed

- Current benchmark CPL and MQL rate for PMS demo campaigns.
- Exact negative audience lists for exclusions sync.
- Confirm if server-side conversion relay is enabled for LinkedIn conversion API.
