---
title: "Tracking Implementation and QA - us-ca_reddit_leads_hostfully-pms_apr26"
campaign: "us-ca_reddit_leads_hostfully-pms_apr26"
platform: "reddit"
month: "Apr 2026"
status: "Draft"
---

# Tracking Implementation and QA - us-ca_reddit_leads_hostfully-pms_apr26 (Apr 2026)

## Tracking Architecture

- **Client-side:** Reddit Pixel (live)
- **Server-side:** Event API / server-side events (live)
- **Offline:** CRM conversion imports (live)
- **Attribution:** 7-day click + 1-day view

## Required Events

1. `PageVisit`
2. `ViewContent` (product/demo pages)
3. `Lead` (form submit baseline)
4. `qualified_demo_submit` (custom conversion for optimization)

## QA Checklist

- [ ] Pixel events fire on landing and submit confirmation pages.
- [ ] Server-side events map with consistent event IDs for deduplication.
- [ ] Qualified demo custom conversion receives stable daily signal.
- [ ] CRM records persist UTM and click identifiers.
- [ ] Offline conversion uploads match campaign/ad group/ad level dimensions.
- [ ] Test conversion is visible in Reddit reporting and CRM attribution views.

## UTM Governance

Keep existing convention and enforce these parameters:

```text
utm_source=reddit
utm_medium=paid-social
utm_campaign={campaign_name}
utm_content={ad_name}
utm_term={adgroup_name}
```

## Reporting Cadence

- **Daily:** spend, CTR, CPC, LPV rate
- **Weekly:** CPL and cost per qualified demo
- **Monthly:** SQL rate and opportunity value by campaign theme

## Open Questions

- Confirm canonical attribution dashboard owner for Reddit-specific reporting.
