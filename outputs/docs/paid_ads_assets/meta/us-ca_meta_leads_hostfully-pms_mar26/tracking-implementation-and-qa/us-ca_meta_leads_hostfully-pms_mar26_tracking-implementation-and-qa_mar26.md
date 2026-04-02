---
title: "Tracking Implementation and QA - us-ca_meta_leads_hostfully-pms_mar26"
campaign: "us-ca_meta_leads_hostfully-pms_mar26"
platform: "meta"
month: "Mar 2026"
status: "Draft"
---

# Tracking Implementation and QA - us-ca_meta_leads_hostfully-pms_mar26 (Mar 2026)

## Tracking Architecture

- **Client-side:** Meta Pixel (active)
- **Server-side:** Conversions API (active)
- **Downstream:** Offline conversion imports from CRM (active)
- **Attribution window:** 7-day click + 1-day view

## Required Events

1. `PageView`
2. `ViewContent` (pricing/demo pages)
3. `Lead` or custom event for form submit
4. **Custom conversion:** `qualified_demo_submit` (to be finalized)

## QA Checklist

- [ ] Pixel Helper confirms event firing on landing page and form submit.
- [ ] CAPI events received with event_id deduplication matching browser events.
- [ ] Lead IDs pass to CRM with campaign/ad metadata.
- [ ] Offline conversion schema maps to lead stages (MQL, SQL, Opportunity).
- [ ] UTMs persist through form submit and CRM record.
- [ ] Test lead appears in Meta Events Manager and CRM with matching timestamps.

## UTM Governance

Use existing org convention; minimum fields required:

```text
utm_source=meta
utm_medium=paid-social
utm_campaign={campaign_name}
utm_content={ad_name}
utm_term={audience_name}
```

## Reporting Cadence

- **Daily:** spend, CTR, CPC, CPL
- **Weekly:** cost per qualified lead, lead-to-SQL rate
- **Monthly:** pipeline value, win-rate by campaign/audience

## Open Questions

- Confirm final custom conversion trigger condition.
- Confirm canonical dashboard for source-of-truth attribution.
