---
title: "Tracking Implementation and QA – us-ca_google-search_leads_hostfully-guidebooks_mar26"
campaign: "us-ca_google-search_leads_hostfully-guidebooks_mar26"
platform: "google_ads"
status: "Draft"
month: "Mar 2026"
---

# Tracking Implementation and QA – us-ca_google-search_leads_hostfully-guidebooks_mar26

## Tracking Stack

- GA4
- GTM
- Google Ads conversion tracking

## Conversion Taxonomy

- Primary: `demo_booked`
- Secondary: `demo_form_start`, `demo_form_submit`

## Implementation Notes

- Fire primary conversion only on confirmed booking state.
- Keep secondary form milestones non-primary for bidding.
- Validate one conversion per successful booking event.

## UTM Convention

- `utm_source=google`
- `utm_medium=cpc`
- `utm_campaign=us-ca_google-search_leads_hostfully-guidebooks_mar26`
- `utm_content={adgroup_or_asset}`
- `utm_term={keyword}`

## QA Checklist

- Verify tags in GTM preview mode.
- Confirm GA4 event receipt and parameter integrity.
- Confirm Google Ads conversion action receives data.
- Confirm no duplicate primary conversion fires.
- Validate desktop and mobile form paths.

## Reporting Slice (Weekly)

- Spend, clicks, CTR, CPC
- Conversions, CVR, CPA
- Search term quality and negative additions
- Top ad asset performance
