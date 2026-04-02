---
title: "Reddit Build Sheet - us-ca_reddit_leads_hostfully-pms_apr26"
campaign: "us-ca_reddit_leads_hostfully-pms_apr26"
platform: "reddit"
status: "Draft"
date_created: "2026-03-31"
---

# Reddit Build Sheet - `us-ca_reddit_leads_hostfully-pms_apr26`

## 1. Prerequisites

- Reddit Ads account access and billing active
- Reddit Pixel verified
- Server-side event integration verified
- Custom conversion `qualified_demo_submit` configured
- CRM offline conversion mapping ready

## 2. Campaign Creation

1. Create campaign: `us-ca_reddit_leads_hostfully-pms_conv-qualified-demo_apr26`
2. Objective: Conversions
3. Optimization event: `qualified_demo_submit`
4. Attribution: 7-day click + 1-day view
5. Budget: 70% monthly allocation

## 3. Ad Group Setup (Conversion Campaign)

- Create ad groups:
  - `community_prospecting_apr26`
  - `interest_prospecting_apr26`
  - `keyword-context_prospecting_apr26`
- Geo: US + Canada
- Audience exclusions: existing customers where available

## 4. Traffic Learning Campaign

1. Create campaign: `us-ca_reddit_leads_hostfully-pms_traffic-learning_apr26`
2. Objective: Traffic
3. Budget: 30% monthly allocation
4. Build mirrored ad groups for audience learning and creative discovery

## 5. Ad Setup

- Upload mixed creatives (image + video)
- Apply naming standard and UTM parameters
- Align ad text with targeted subreddit/context relevance

## 6. QA Before Launch

- [ ] Events fire correctly in Reddit dashboard
- [ ] Custom conversion selected in conversion campaign
- [ ] UTMs populate final URLs
- [ ] Test leads appear in CRM with campaign metadata
- [ ] Landing page message matches ad angle
