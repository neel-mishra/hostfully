---
title: "AB Test Plan - us-ca_reddit_leads_hostfully-pms_apr26"
campaign: "us-ca_reddit_leads_hostfully-pms_apr26"
platform: "reddit"
month: "Apr 2026"
status: "Draft"
---

# AB Test Plan - us-ca_reddit_leads_hostfully-pms_apr26 (Apr 2026)

## Objective

Lower cost per qualified demo and improve downstream lead quality from Reddit cold traffic.

## Test 1: Targeting Mode

- **Hypothesis:** Community-first targeting yields higher qualified lead rate than interest-first.
- **Variant A:** Subreddit/community weighted ad groups
- **Variant B:** Interest/context weighted ad groups
- **Primary metric:** Cost per qualified demo

## Test 2: Format Mix

- **Hypothesis:** Short practical video outperforms static in qualified lead rate.
- **Variant A:** Static image post
- **Variant B:** Short native video
- **Primary metric:** Qualified demo conversion rate

## Test 3: Tone Framing

- **Hypothesis:** No-hype practical framing improves conversion quality vs feature-list framing.
- **Variant A:** Operator pain/solution narrative
- **Variant B:** Feature-led narrative
- **Primary metric:** SQL rate from submitted demos

## Decision Rules

- Keep winner only if CPQD improves by at least 15% or SQL rate improves by at least 10%.
- Require 7+ days runtime and stable spend before declaring test outcome.
