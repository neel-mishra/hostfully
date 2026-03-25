---
title: "Experiment Plan – us-ca_meta_leads_reader-acquisition_mar26"
campaign: "us-ca_meta_leads_reader-acquisition_mar26"
agent: "ab-test-agent"
status: "Draft"
date_created: "2026-03-16"
---

# Experiment Plan – TLDR Reader Acquisition (Meta)

Output of the **ab-test-agent** for the `us-ca_meta_leads_reader-acquisition_mar26` campaign. This document defines the first wave of experiments, guardrails, and success criteria.

---

## 1. Experiment Framework

- **Primary KPI:** Cost per newsletter signup (CPA) from Meta.
- **Secondary KPIs:** CTR, landing-page conversion rate, volume of signups.
- **Budget:** ~$330/day across four ad sets.
- **Testing principle:** One major variable per test; avoid overlapping conflicting tests.

---

## 2. Test 1 – Creative Concept Test (Prospecting)

**Goal:** Identify which creative angle (Time Saved, Social Proof, Discovery/Tools, Noise vs Signal) drives the lowest CPA and highest CTR with cold audiences.

- **Population:**  
  - Ad sets: `broad_advantageplus_readers_prospecting`, `interests_tech-biz-news_prospecting`.
- **Variants:**  
  - V1: `static_time-saved_mar26_v1` (Time Saved).  
  - V2: `static_social-proof_mar26_v1` (Social Proof).  
  - V3: `static_discovery-tools_mar26_v1` (Discovery/Tools).  
  - V4: `static_noise-vs-signal_mar26_v1` (Noise vs Signal).
- **Setup:**  
  - Each ad set runs all four creatives with:
    - Same primary text (prospecting version for that angle).
    - Same destination URL and UTMs.
  - No dynamic creative; use separate ads per concept.
- **Runtime:**  
  - Minimum 7 days **and** at least ~75 conversions across variants (if budget allows).
- **Success metric:**  
  - Primary: CPA per variant.  
  - Tie-breakers: CTR and landing-page conversion rate.
- **Decision rule:**  
  - Pause the worst-performing concept(s); keep top 2 concepts and feed them into future tests and rotations.

---

## 3. Test 2 – Audience Test (After Creative Winner)

**Goal:** Determine which prospecting audience delivers best CPA using the winning creative angle(s).

- **Trigger:** Run after Test 1 identifies 1–2 winning concepts.
- **Population:**  
  - Ad sets:
    - `broad_advantageplus_readers_prospecting`
    - `interests_tech-biz-news_prospecting`
    - `lal_subscribers-1pct_usca_prospecting`
- **Variants:**  
  - Same winning creative set across all three ad sets.
- **Runtime:**  
  - Minimum 7 days; maintain similar budgets across these ad sets (or proportional to audience size).
- **Success metric:**  
  - CPA per ad set.
- **Decision rule:**  
  - Shift incremental budget toward the best-performing audience(s).  
  - Consider duplicating winning ad set(s) and scaling budgets gradually (20–30% increments).

---

## 4. Test 3 – Landing Page Variant (CRO)

**Goal:** Improve landing-page conversion rate without changing traffic quality.

- **Population:**  
  - All traffic from campaign (or at least from winning ad sets).
- **Variants:**  
  - Control: current landing page hero and layout.  
  - Variant: updated hero section (per landing-page-and-cro doc):
    - Headline: “The 5‑Minute Tech & Startup Briefing.”
    - Subhead: “One email with the most important stories, tools, and ideas in tech. Free, no fluff.”
    - Social-proof line in hero band.
- **Setup:**  
  - Use server-side A/B testing or client-side split (50/50) for visitors from this campaign.
- **Runtime:**  
  - Until each variant has at least 500–1,000 visits and 50+ conversions, or until statistical significance is reached.
- **Success metric:**  
  - Landing-page → signup conversion rate; derived campaign CPA.
- **Decision rule:**  
  - If variant beats control with statistical confidence and no negative downstream effects, promote variant to new default.

---

## 5. Guardrails & Operational Notes

- Avoid changing budgets, bids, or major structure mid-test; if necessary, note dates and changes in reporting.
- Keep test naming consistent in Meta:
  - Append `_t1-concept` or `_t2-audience` etc. to ad or ad set names if needed.
- Only run one major test type at a time (e.g., don’t launch a brand-new LP test while also overhauling audiences).
- Document decisions:
  - After each test, add a short summary and decision note at the bottom of this file (e.g., “Test 1 outcome: Time Saved + Noise vs Signal won. Social Proof underperformed by +40% CPA.”).

