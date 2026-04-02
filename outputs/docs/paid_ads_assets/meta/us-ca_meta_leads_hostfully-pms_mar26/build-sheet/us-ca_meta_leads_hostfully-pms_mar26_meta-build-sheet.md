---
title: "Meta Build Sheet - us-ca_meta_leads_hostfully-pms_mar26"
campaign: "us-ca_meta_leads_hostfully-pms_mar26"
platform: "meta"
status: "Draft"
date_created: "2026-03-31"
---

# Meta Build Sheet - `us-ca_meta_leads_hostfully-pms_mar26`

## 1. Prerequisites

- Meta ad account access + billing active
- Pixel installed and verified
- CAPI connected and deduplication tested
- CRM offline conversion pipeline connected
- Existing UTM convention documented

## 2. Campaign Build Steps

1. Create campaign: `us-ca_meta_leads_hostfully-pms_prospecting-advplus_mar26`
2. Objective: Leads
3. Conversion location: Website (custom conversion target)
4. Optimization event: custom conversion (qualified demo)
5. Attribution setting: 7-day click + 1-day view
6. Budget: CBO daily budget aligned to monthly plan

## 3. Secondary Control Campaign

1. Create campaign: `us-ca_meta_leads_hostfully-pms_prospecting-control_mar26`
2. Objective/event/attribution same as campaign A
3. Build segmented ad sets by portfolio size proxy and behavior inputs
4. Keep budget split at 60/40 (A/B) until first optimization cycle

## 4. Ads Setup

- Load angle-based creative set:
  - connected-ops
  - automation-control
  - direct-growth
  - guest-experience
- Use 1:1 and 4:5 for static; optional 9:16 for Reels
- Add URL params using existing UTM schema

## 5. QA Before Publish

- [ ] Conversion event selected correctly in each campaign
- [ ] Naming conventions match structure doc
- [ ] Exclusions include existing customers where required
- [ ] Landing page load speed and form tracking verified
- [ ] Test leads validated in Meta + CRM + analytics dashboard
