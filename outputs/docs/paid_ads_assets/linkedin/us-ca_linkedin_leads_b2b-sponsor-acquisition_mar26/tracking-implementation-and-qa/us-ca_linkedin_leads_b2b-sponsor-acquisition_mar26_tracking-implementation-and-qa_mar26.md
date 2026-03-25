---
title: "Tracking Implementation & QA – us-ca_linkedin_leads_b2b-sponsor-acquisition_mar26"
campaign: "us-ca_linkedin_leads_b2b-sponsor-acquisition_mar26"
agent: "analytics-tracking-agent"
status: "Draft"
date_created: "2026-03-16"
---

# Tracking Implementation & QA – us-ca_linkedin_leads_b2b-sponsor-acquisition_mar26

<!--
To be populated by analytics-tracking-agent.
Specify events, UTMs, pixels/tags, server-side tracking,
data flow into GA4/CRM, and QA steps.
-->

## Event Architecture

### LinkedIn

- **Lead Gen Form path (if used):**
  - LinkedIn Lead Gen Form submission event, synced to your CRM/ESP.
- **Website conversions path:**
  - Custom conversion for “Sponsor lead submitted” (form submission on advertise/sponsor page).

### GA4

- `page_view` for all pages.
- `sponsor_lp_view` for sponsor landing page.
- `sponsor_lead_submit` when form is successfully submitted.

Attach UTM parameters and key fields (company, role, ACV band) where possible.

### CRM

For each sponsor lead:

- Store UTM fields: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`.
- Store page URL and timestamp.
- Mark as “TLDR sponsor lead – LinkedIn”.

