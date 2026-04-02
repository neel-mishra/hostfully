---
title: "Campaign Structure: us-ca_meta_leads_hostfully-pms_mar26"
date_created: "2026-03-31"
last_updated: "2026-03-31"
status: "Draft"
platform: "meta"
objective: "Leads - Hostfully PMS"
description: "Paid Meta campaign for Hostfully PMS lead generation in US and Canada."
---

# Campaign Structure: us-ca_meta_leads_hostfully-pms_mar26

## Metadata

| Field | Value |
|-------|-------|
| **Platform** | Meta (Facebook + Instagram) |
| **Objective** | Qualified PMS demo leads |
| **Monthly Budget** | $5,000-$15,000 |
| **Geo** | US + Canada |
| **Status** | Draft |

## Intake Snapshot

- **Campaign type:** Net-new campaign
- **Funnel priority:** Cold prospecting
- **Audience:** B2B owner-operators / property managers
- **Budget control:** CBO
- **Setup preference:** Advantage+
- **Special ad category:** None
- **Primary conversion event:** Custom conversion
- **Attribution window:** 7-day click + 1-day view
- **Data foundation:** Customer list + Pixel + CAPI + offline conversions live
- **UTM convention:** Existing convention
- **Analytics source of truth:** Other/multi-tool (to confirm exact platform owner)

## Campaign Architecture

## 1) Campaign A: Prospecting - Advantage+ Leads

- **Name:** `us-ca_meta_leads_hostfully-pms_prospecting-advplus_mar26`
- **Objective:** Leads (optimized to custom conversion: qualified demo intent)
- **Budget model:** CBO
- **Daily budget starting point:** $120/day (scale band up/down based on monthly budget)
- **Audience logic:** Broad + lookalike expansion with Advantage+ audience controls
- **Placements:** Advantage+ placements (all), with quality review after first 7 days

### Ad Set Layer (inside Advantage+ logic)

- **Audience seed 1:** CRM lead/customer list lookalike (1-3%)
- **Audience seed 2:** Website high-intent event lookalike (pricing/demo/page-depth cohorts)
- **Geo:** US + CA
- **Age:** 25-60 (expand if delivery constrained)
- **Language:** English

## 2) Campaign B: Prospecting - Control Segment Test

- **Name:** `us-ca_meta_leads_hostfully-pms_prospecting-control_mar26`
- **Objective:** Leads (same custom conversion)
- **Budget model:** CBO
- **Daily budget starting point:** $80/day
- **Purpose:** Keep one structured control campaign to compare against Advantage+ automation

### Core Audience Segments

1. **Small PM Operators (1-15 units)**
2. **Growing PM Operators (16-30 units)**
3. **Business decision-maker proxy targeting** (property management + STR software behaviors where available)

## Budget Allocation (initial)

- **Campaign A (Advantage+):** 60%
- **Campaign B (Control):** 40%
- Rebalance weekly based on cost per qualified lead and CRM stage progression.

## Bidding + Optimization

- Start with **Highest Volume** (no cap) until conversion baseline stabilizes.
- Introduce cost controls only after at least 30-50 qualified conversion signals.
- Prioritize lead quality over in-platform CPL by using offline stage feedback.

## Naming Convention

- **Campaign:** `{geo}_meta_leads_hostfully-pms_{theme}_{mmmyy}`
- **Ad set:** `{audience}_{funnel}_{placement}_{mmmyy}`
- **Ad:** `{format}_{angle}_{persona}_{mmmyy}_v{N}`

## UTM Pattern (using existing convention)

```text
utm_source=meta&utm_medium=paid-social&utm_campaign={campaign_name}&utm_content={ad_name}&utm_term={audience_name}
```

## Pre-Launch Checklist

- [ ] Custom conversion finalized and mapped to qualified demo action.
- [ ] Pixel + CAPI deduplication tested.
- [ ] Offline conversion upload mapping validated (lead -> SQL -> opportunity stages).
- [ ] Customer list hashed and uploaded for lookalike seeds.
- [ ] UTMs confirmed against existing reporting taxonomy.
- [ ] Landing page message match aligned to ad angle.

## Open Questions

- Exact **custom conversion definition** (event + URL rule + CRM qualifier) is still pending.
- Confirm **primary analytics owner** (GA4 vs BI tool vs CRM dashboard) for final attribution governance.
