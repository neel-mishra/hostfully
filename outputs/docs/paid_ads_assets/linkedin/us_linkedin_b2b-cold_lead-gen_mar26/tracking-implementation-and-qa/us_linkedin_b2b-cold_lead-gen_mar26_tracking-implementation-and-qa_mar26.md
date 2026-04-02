---
title: "Tracking Implementation & QA – us_linkedin_b2b-cold_lead-gen_mar26"
campaign: "us_linkedin_b2b-cold_lead-gen_mar26"
agent: "analytics-tracking-agent"
status: "Draft"
date_created: "2026-03-31"
---

# Tracking Implementation & QA – us_linkedin_b2b-cold_lead-gen_mar26

<!--
To be populated by analytics-tracking-agent.
Specify events, UTMs, pixels/tags, server-side tracking,
data flow into GA4/CRM, and QA steps.
-->

## Event Architecture

| Layer | Event | Source | Destination |
|---|---|---|---|
| LinkedIn | `Lead` conversion event | Insight Tag + conversion rule | LinkedIn Campaign Manager |
| Website | `generate_lead` | Front-end form submit | GA4 |
| CRM | `MQL`, `SQL`, `Opportunity` | CRM stage updates | Reporting layer |

## UTM and Attribution

- **UTM convention:** Use existing team convention.
- **Required params:** `utm_source=linkedin`, `utm_medium=paid_social`, `utm_campaign=us_linkedin_b2b-cold_lead-gen_mar26`, `utm_content={creative_id}`, `utm_term={audience_segment}`.
- **Attribution view:** LinkedIn platform + GA4 session reports + CRM stage progression.

## QA Checklist

- [ ] Insight Tag present on all landing pages.
- [ ] Primary conversion fires once per valid form submit.
- [ ] GA4 `generate_lead` event includes campaign and content parameters.
- [ ] UTM parameters persist through redirects.
- [ ] CRM lead records capture source/medium/campaign.

## Open Questions

- Confirm exact event names currently used in GA4 property.
- Confirm offline conversion import cadence (daily vs weekly).
