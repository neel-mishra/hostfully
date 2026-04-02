---
title: "Tracking Implementation & QA – us_linkedin_leads_hostfully-pms_apr26"
campaign: "us_linkedin_leads_hostfully-pms_apr26"
agent: "analytics-tracking-agent"
status: "Draft"
date_created: "2026-03-31"
---

# Tracking Implementation & QA – us_linkedin_leads_hostfully-pms_apr26

<!--
To be populated by analytics-tracking-agent.
Specify events, UTMs, pixels/tags, server-side tracking,
data flow into GA4/CRM, and QA steps.
-->

## Event Architecture

| Layer | Event | Trigger | Destination |
|---|---|---|---|
| LinkedIn | `Lead` | Demo form completion | LinkedIn Campaign Manager |
| Website | `demo_request_submit` | Thank-you page or submit callback | GA4 |
| Website | `schedule_click` | Calendar booking CTA click | GA4 |
| CRM | `MQL` / `SQL` / `Opportunity` | Lifecycle stage changes | CRM + attribution reports |

## UTM Mapping

- `utm_source=linkedin`
- `utm_medium=paid_social`
- `utm_campaign=us_linkedin_leads_hostfully-pms_apr26`
- `utm_content={creative_id}`
- `utm_term={audience_segment}`

## QA Checklist

- [ ] LinkedIn Insight Tag loaded on all campaign landing pages
- [ ] Demo submit event fires exactly once per conversion
- [ ] GA4 event params include source, medium, campaign, content
- [ ] CRM lead records retain original UTM fields
- [ ] Test lead appears in attribution report within expected SLA

## Open Questions

- Confirm offline conversion upload frequency (daily or weekly).
- Confirm canonical conversion event name if multiple demo forms exist.
