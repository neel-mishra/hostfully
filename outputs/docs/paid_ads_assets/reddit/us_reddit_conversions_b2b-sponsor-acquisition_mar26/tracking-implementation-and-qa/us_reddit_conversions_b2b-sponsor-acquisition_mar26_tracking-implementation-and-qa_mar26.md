---
title: "Tracking Implementation & QA – us_reddit_conversions_b2b-sponsor-acquisition_mar26"
campaign: "us_reddit_conversions_b2b-sponsor-acquisition_mar26"
agent: "analytics-tracking-agent"
status: "Draft"
date_created: "2026-03-16"
---

# Tracking Implementation & QA – us_reddit_conversions_b2b-sponsor-acquisition_mar26

<!--
To be populated by analytics-tracking-agent.
Specify events, UTMs, pixels/tags, server-side tracking,
data flow into GA4/CRM, and QA steps.
-->

## Event Architecture

### Reddit

- Conversion event: newsletter signup (thank-you page or JS event).
- Pixel/tag: Reddit tracking pixel on signup + thank-you page.

### GA4

- `page_view` and `newsletter_subscribe` events, with `source=reddit`, `medium=paid-social` via UTMs.

