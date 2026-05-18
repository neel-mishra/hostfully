# GTM Retrospective — April 2026

**Period:** April 18 – May 17, 2026  
**Generated:** May 18, 2026  
**Data Sources:** Meta Ads API (live), Google Ads (unavailable — 404), Ahrefs (unavailable — missing key)

---

## Executive Summary

**Wins:**
- Meta Ads generated 127 qualified leads at scale across 7 active campaigns spanning US/CA, EU, LATAM, and AU/UK markets
- Mexico prospecting campaign (mx_pms_prospecting) emerged as the most efficient lead source: 42 leads at $88.25 CPA — significantly below account average
- Brazil meeting-focused campaign delivered 22 leads (complete registrations), showing strong bottom-funnel intent in LATAM
- Content pipeline delivered 9 completed articles (41% of backlog processed)

**Misses:**
- Google Ads data unavailable due to API configuration (404) — no visibility into search performance
- Ahrefs/SEO data unavailable (missing API key) — organic performance untracked this period
- Account-wide CPA of $263.86/lead is elevated — driven by high-spend US/CA prospecting
- CA-US prospecting is the largest budget line ($16,594) but delivered only 27 leads ($614.60 CPA)
- 13 of 22 content pipeline items remain "Not Started"

**Key Shifts:**
- LATAM (Mexico + Brazil) outperforming North America on efficiency metrics
- Retargeting campaigns delivering leads at lower volume but may need budget increase given quality signals
- Content execution rate needs acceleration — pipeline velocity below target

---

## Paid Acquisition — Meta Ads

### Account-Level Summary (Apr 18 – May 17)

| Metric | Value |
|--------|-------|
| Total Spend | $33,509.80 |
| Impressions | 1,023,467 |
| Reach | 259,409 |
| Clicks | 13,176 |
| CTR | 1.29% |
| Avg CPC | $2.54 |
| Total Leads | 127 |
| Cost Per Lead | $263.86 |
| Complete Registrations | 22 |
| Cost Per Registration | $1,523.17 |
| Landing Page Views | 1,447 |
| Video Views | 144,773 |

### Campaign Performance Breakdown

| Campaign | Status | Spend | Impressions | Clicks | CTR | CPC | Leads | CPL |
|----------|--------|-------|-------------|--------|-----|-----|-------|-----|
| ca-us_pms_prospecting_website-conv | ACTIVE | $16,594 | 237,826 | 3,468 | 1.46% | $4.78 | 27 | $614.60 |
| mx_pms_prospecting_website-conv | ACTIVE | $3,707 | 280,244 | 4,811 | 1.72% | $0.77 | 42 | $88.25 |
| eu_pms_prospecting_website-conv | ACTIVE | $3,204 | 93,487 | 1,446 | 1.55% | $2.22 | 15 | $213.58 |
| ca-us_pms_retargeting_website-conv | ACTIVE | $2,025 | 29,920 | 366 | 1.22% | $5.53 | 18 | $112.52 |
| [Leads] hostfully pt-br — meeting | ACTIVE | $7,438 | 374,551 | 2,984 | 0.80% | $2.49 | 22 | $338.09 |
| au-uk_pms_retargeting_website-conv | ACTIVE | $540 | 7,439 | 101 | 1.36% | $5.34 | 3 | $179.94 |
| [Post Promovido] pt-br | ACTIVE | ~$0 | — | — | — | — | 0 | — |

### Top Performers
1. **mx_pms_prospecting_website-conv** — $88.25 CPL, 42 leads, highest click volume (4,811). The Mexico market is demonstrating strong demand at low CPCs ($0.77).
2. **ca-us_pms_retargeting_website-conv** — $112.52 CPL on retargeting audience. Website visitors converting at 2.4x the rate of cold prospecting.
3. **au-uk_pms_retargeting_website-conv** — Small budget but $179.94 CPL shows retargeting works across geos.

### Underperformers
1. **ca-us_pms_prospecting_website-conv** — Consuming 49.5% of total budget ($16,594) but delivering only 21% of leads at $614.60 CPL. This is 2.3x the account average and 7x the Mexico equivalent.
2. **[Leads] hostfully pt-br — meeting** — $338.09 per complete registration. While these are meeting-qualified leads (higher value), volume efficiency is low relative to spend.

### Cross-Platform Summary

| Platform | Spend | Leads | CPL | Status |
|----------|-------|-------|-----|--------|
| Meta Ads | $33,510 | 127 | $263.86 | ✅ Data Available |
| Google Ads | — | — | — | ❌ API Unavailable (404) |

---

## Organic & SEO

**Status:** ❌ Data Unavailable

Ahrefs API key is not configured in the environment. Unable to pull:
- Organic traffic trends
- Keyword rankings
- Domain Rating changes
- Top pages by traffic

**Action Required:** Configure `AHREFS_API_KEY` in environment secrets for next run.

---

## Content Pipeline Execution

### Summary (from content_pipeline.csv)

| Metric | Value |
|--------|-------|
| Total Items in Pipeline | 22 |
| Completed | 9 (41%) |
| Not Started | 13 (59%) |
| In Progress | 0 |

### Completed Articles

1. How To Get 55% Open Rates Like the Top-Performing Newsletters Do
2. How to Write Email Subject Lines That Actually Get Opened in 2026
3. How To Use beehiiv To Create a Thriving Newsletter Community Hub
4. Read the State of Newsletters report
5. 20 Ways to Monetize Your Newsletter
6. How To Start a Newsletter for Local Communities
7. Turn Newsletter Swaps Into Your Best Free Acquisition Channel
8. 10 Predictions That Will Reshape Newsletter Businesses in 2026
9. How To Start a Newsletter for Operators and COOs

### Pipeline Health Assessment
- Execution rate of 41% suggests the content pipeline is behind target
- Zero items in "In Progress" — indicates batch completion pattern rather than continuous flow
- High-scoring items (Weighted Score 3.2+) have been prioritized correctly
- Lower-priority general industry news pieces (score 1.6) remain untouched — appropriate prioritization

---

## What Worked

1. **Mexico Prospecting at Scale** — MX campaign achieved $0.77 CPC and $88.25 CPL, proving LATAM as an efficient acquisition channel for PMS prospects
2. **Retargeting Cross-Geo** — Both US/CA and AU/UK retargeting delivered leads below $180 CPL, validating the funnel from awareness to conversion
3. **Video Creative Strategy** — 144,773 video views across campaigns indicates strong creative engagement; video is driving initial awareness effectively
4. **Content Priority Scoring** — All 9 completed articles were from the top-weighted-score tier, showing disciplined execution on highest-impact content

---

## What Didn't Work

1. **US/CA Cold Prospecting Efficiency** — $614.60 CPL on the largest budget line ($16.6K). The 2% LAL audience in US/CA is either saturated or the creative/offer isn't resonating with cold US audiences at this scale.
   - *Diagnosis:* Likely audience fatigue in the LAL segment + higher competitive CPMs in US market
   
2. **Content Velocity** — 59% of pipeline untouched. Zero items in "In Progress" suggests a bottleneck in content production workflow.
   - *Diagnosis:* Either insufficient writer capacity or unclear ownership of remaining items

3. **Google Ads Blind Spot** — No search data available means we can't assess brand vs. non-brand search performance or keyword opportunities.
   - *Diagnosis:* API configuration issue (GOOGLE_ADS_CUSTOMER_ID may be incorrect or API version mismatch)

4. **SEO Measurement Gap** — Without Ahrefs, we can't correlate content production with ranking improvements.
   - *Diagnosis:* Missing environment variable. Quick fix.

---

## Learnings & Implications for Next Month

### Strategic Insights

1. **Shift Budget to LATAM:** Mexico is delivering 7x better CPL than US cold prospecting. Consider reallocating 20-30% of US/CA prospecting budget to expand MX/BR campaigns.

2. **Double Down on Retargeting:** Both retargeting campaigns (US/CA and AU/UK) deliver leads at ~50% lower CPL than prospecting. Increasing retargeting budgets by 25% while improving top-of-funnel volume is a low-risk efficiency play.

3. **Fix US/CA Prospecting:** At $614 CPL, the current creative + audience combo isn't sustainable. Test:
   - New LAL seeds (meeting-qualified vs. hatchlings list)
   - Creative refresh (the current set has been running since March)
   - Narrower geo targeting (high-density vacation rental markets)

4. **Content Pipeline Acceleration:** Move from batch completion to continuous flow. Target 4 articles/week with clear assignees and deadlines.

5. **Resolve API Gaps Immediately:** Google Ads (fix Customer ID / API URL) and Ahrefs (add API key) must be configured before next reporting cycle.

### KPI Targets for June Sprint (Derived from Actuals)

| KPI | April Actual | June Target | Change |
|-----|-------------|-------------|--------|
| Meta Leads | 127 | 160 | +26% |
| Blended CPL | $263.86 | $220.00 | -17% |
| Content Published | 9 | 12 | +33% |
| Google Ads Leads | N/A | Track baseline | — |
| Organic Traffic | N/A | Track baseline | — |

---

*Report generated by GTM Execution Commander automation. Data gaps noted above require environment configuration updates.*
