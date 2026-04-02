---
title: "Campaign Structure: us-ca_reddit_leads_hostfully-pms_apr26"
date_created: "2026-03-31"
last_updated: "2026-03-31"
status: "Draft"
platform: "reddit"
objective: "Leads - Hostfully PMS"
description: "Paid Reddit campaign for Hostfully PMS qualified demo leads in US and Canada."
---

# Campaign Structure: us-ca_reddit_leads_hostfully-pms_apr26

## Metadata

| Field | Value |
|-------|-------|
| **Platform** | Reddit Ads |
| **Objective** | Qualified PMS demo leads |
| **Monthly Budget** | $5,000-$15,000 |
| **Geo** | US + Canada |
| **Status** | Draft |

## Intake Snapshot

- **Campaign type:** New campaign from scratch
- **Audience:** B2B owner-operators / property managers
- **Funnel stage:** Cold prospecting
- **Buying model:** Hybrid (conversion + traffic learning support)
- **Targeting approach:** Mixed (communities + interests + keyword/contextual)
- **Creative format:** Mixed formats (image + video)
- **Conversion event:** Qualified demo submit (custom event)
- **Attribution:** 7-day click + 1-day view
- **Data foundation:** Reddit Pixel + server-side events + offline conversion imports live
- **UTM status:** Existing convention
- **Analytics source of truth:** Other/multi-tool

## Campaign Architecture

## 1) Campaign A: Conversion - Qualified Demo

- **Name:** `us-ca_reddit_leads_hostfully-pms_conv-qualified-demo_apr26`
- **Objective:** Conversions
- **Optimization event:** `qualified_demo_submit` custom conversion
- **Budget allocation:** 70% of total monthly budget
- **Bidding:** Lowest cost to start, then apply guardrails after signal volume

### Ad Group Structure

1. **Ad Group 1: Community-led Prospecting**
   - Subreddit clusters tied to property management and STR operations
2. **Ad Group 2: Interest-led Prospecting**
   - Business software, hospitality operations, entrepreneurship-related interests
3. **Ad Group 3: Keyword/Contextual**
   - Context signals around rental operations, guest communication, automation pain points

## 2) Campaign B: Traffic Learning + Qualification

- **Name:** `us-ca_reddit_leads_hostfully-pms_traffic-learning_apr26`
- **Objective:** Traffic
- **Budget allocation:** 30% of total monthly budget
- **Purpose:** Expand top-of-funnel learning and feed conversion campaign with better creative/audience signal

### Ad Group Structure

1. **Broad mixed targeting test**
2. **High-intent community test**
3. **Keyword-context variant test**

## Budget Framework

- If monthly budget is near **$5k**:
  - Conversion: ~$3.5k
  - Traffic learning: ~$1.5k
- If monthly budget is near **$15k**:
  - Conversion: ~$10.5k
  - Traffic learning: ~$4.5k

## Audience Guidance

- Start with broader community clusters, then prune by qualified lead rate (not CTR only).
- Exclude current customers where feasible.
- Refresh community lists every 2 weeks based on performance and moderation policies.

## Naming Convention

- **Campaign:** `{geo}_reddit_leads_hostfully-pms_{theme}_{mmmyy}`
- **Ad group:** `{targeting-type}_{funnel}_{mmmyy}`
- **Ad:** `{format}_{angle}_{persona}_{mmmyy}_v{N}`

## UTM Pattern (existing convention)

```text
utm_source=reddit&utm_medium=paid-social&utm_campaign={campaign_name}&utm_content={ad_name}&utm_term={adgroup_name}
```

## Pre-Launch Checklist

- [ ] Reddit Pixel firing on landing and thank-you pages
- [ ] Server-side events deduplicating correctly
- [ ] Custom conversion `qualified_demo_submit` verified in ads manager
- [ ] Offline conversion stage mapping validated in CRM
- [ ] UTM persistence confirmed through form submit
- [ ] Landing page message match aligned to top ad angles

## Open Questions

- Final approved subreddit inclusion/exclusion list.
- Final definition for "qualified demo" threshold in CRM (job role + portfolio signal + intent fields).
