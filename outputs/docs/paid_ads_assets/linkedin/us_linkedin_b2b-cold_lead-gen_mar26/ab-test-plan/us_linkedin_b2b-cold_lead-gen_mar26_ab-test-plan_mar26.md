---
title: "Experiment Plan – us_linkedin_b2b-cold_lead-gen_mar26"
campaign: "us_linkedin_b2b-cold_lead-gen_mar26"
agent: "ab-test-agent"
status: "Draft"
date_created: "2026-03-31"
---

# Experiment Plan – us_linkedin_b2b-cold_lead-gen_mar26

<!--
To be populated by ab-test-agent.
Define sequential tests (creative, audience, bidding, landing page),
KPIs, guardrails, and decision rules.
-->

## 1. Experiment Framework

- **Primary KPI:** Cost per qualified lead (CPL to MQL threshold)
- **Secondary KPIs:** CTR, CPC, landing page CVR, cost per qualified lead

## Test Roadmap (First 4 Weeks)

1. **Creative angle test (Week 1-2)**
   - Compare 3 core angles from creative file.
   - Success rule: winner must beat baseline CPL by >= 15%.
2. **CTA test (Week 2-3)**
   - `Book Demo` vs `Learn More`.
   - Success rule: statistically directional lift with no quality drop.
3. **Audience expansion test (Week 3-4)**
   - Core role targeting vs broader skill/interest cluster.
   - Success rule: maintain lead quality while expanding volume.

## Guardrails

- Do not change more than one major variable inside a single ad group during a test window.
- Keep budget shifts <= 20% every 3-4 days during active tests.
- Pause variants only after minimum impression/click threshold is reached.

## Open Questions

- Confirm minimum sample threshold for internal decisioning.
- Confirm quality metric source of truth (MQL rate vs SQL rate).
