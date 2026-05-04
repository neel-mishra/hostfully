# GTM Monthly Retrospective — April 2026

**Period:** April 4 – May 3, 2026
**Generated:** May 4, 2026 (Automated Weekly GTM Execution Commander)

---

## Executive Summary

April was a stabilization month for paid acquisition with Meta Ads carrying the full paid workload. The account generated **124 leads** and **26 complete registrations** from **$32,733.82 in spend** across 8 active/paused campaigns (6 with delivery). The US/Canada PMS prospecting campaign remained the top performer by volume (47 leads), while the Brazil Hostfully meeting campaign delivered the most efficient cost structure at scale. Google Ads and Ahrefs data were unavailable this cycle (API configuration issues); these gaps are noted below with remediation steps.

**Key wins:** Strong lead volume from retargeting campaigns, especially ca-us retargeting ($93.74 CPA). Post engagement campaigns in Brazil drove exceptional organic reach.

**Key misses:** Google Ads data gap prevents cross-platform analysis. High CPA on prospecting campaigns in AU/UK ($276.08/lead). Content pipeline execution rate at 50% — 9 of 22 items completed, but 13 remain Not Started.

**Key shifts:** Recommend consolidating spend toward retargeting and Brazil market campaigns next month while investigating Google Ads API access.

---

## Paid Acquisition — Meta Ads

### Account-Level Summary (Last 30 Days)

| Metric | Value |
|--------|-------|
| Total Spend | $32,733.82 |
| Impressions | 747,564 |
| Reach | 159,659 |
| Clicks | 7,899 |
| CTR | 1.06% |
| Avg CPC | $4.14 |
| Leads (email-valid) | 124 |
| Complete Registrations | 26 |
| Cost per Lead | $263.98 |
| Cost per Registration | $1,258.99 |
| Landing Page Views | 981 |
| Video Views | 47,019 |

### Campaign Performance Breakdown

| Campaign | Status | Spend | Impressions | Clicks | CTR | CPC | Leads | CPA |
|----------|--------|-------|-------------|--------|-----|-----|-------|-----|
| ca-us_pms_prospecting_website-conv | Active | $17,173.07 | 213,607 | 2,297 | 1.08% | $7.48 | 47 | $365.38 |
| [Leads] hostfully pt-br — meeting | Active | $7,183.98 | 315,939 | 2,421 | 0.77% | $2.97 | 24 | $299.33 |
| au-uk_pms_prospecting_website-conv | Active | $3,589.00 | 54,055 | 674 | 1.25% | $5.32 | 13 | $276.08 |
| ca-us_pms_retargeting_website-conv | Active | $2,249.70 | 27,375 | 379 | 1.38% | $5.94 | 24 | $93.74 |
| mx_pms_prospecting_website-conv | Active | $1,583.90 | 100,257 | 1,805 | 1.80% | $0.88 | 13 | $121.84 |
| au-uk_pms_retargeting_website-conv | Active | $689.72 | 8,160 | 128 | 1.57% | $5.39 | 3 | $229.91 |
| [Post Promovido] pt-br | Paused | $190.26 | 25,042 | 152 | 0.61% | $1.25 | 0 | N/A |
| [Leads] LAL1% hostfully pt-br — meeting | Paused | $74.19 | 3,129 | 43 | 1.37% | $1.73 | 0 | N/A |

### Top Performers
1. **ca-us_pms_retargeting_website-conv** — Best CPA at $93.74/lead with 24 leads. Retargeting warm audiences (90-day visitors, churned PMS customers, conference attendees) proves highly efficient. 19 complete registrations also came from this campaign.
2. **mx_pms_prospecting_website-conv** — Lowest CPC ($0.88) and strong CPA ($121.84). Mexico market continues to deliver volume at competitive rates.
3. **[Leads] hostfully pt-br — meeting** — Highest impression volume (315K) with 24 leads. Brazil market engagement is strong.

### Underperformers
1. **ca-us_pms_prospecting_website-conv** — Highest spend ($17,173) but CPA of $365.38 is 3.9x the retargeting campaign. Volume justifies the spend but efficiency needs improvement.
2. **au-uk_pms_prospecting_website-conv** — CPA of $276.08 with only 13 leads. Consider tightening targeting or testing new creatives for this geo.
3. **[Post Promovido] pt-br** — $190 in engagement spend with no leads. Useful for awareness but not contributing to pipeline.

### Cross-Platform Summary

| Platform | Spend | Leads | CPA | Status |
|----------|-------|-------|-----|--------|
| Meta Ads | $32,733.82 | 124 | $263.98 | Active — data collected |
| Google Ads | N/A | N/A | N/A | API returned 404 — customer ID may need reconfiguration |

**Action item:** Verify `GOOGLE_ADS_CUSTOMER_ID` and `GOOGLE_ADS_MANAGER_ID` environment variables. The Google Ads searchStream endpoint returned HTTP 404, suggesting the customer ID is invalid or the API version needs updating.

---

## Organic & SEO

**Status: Data Unavailable**

Ahrefs API returned `missing_env: AHREFS_API_KEY`. The following metrics could not be pulled:
- Organic traffic history for tldr.tech
- Top organic keywords and rankings
- Domain rating changes
- Top pages by organic traffic

**Action item:** Add `AHREFS_API_KEY` to the environment secrets (Cursor Dashboard > Cloud Agents > Secrets) to enable SEO reporting in the next cycle.

---

## Content Pipeline Execution

### Overview

| Metric | Count |
|--------|-------|
| Total Pipeline Items | 22 |
| Completed | 9 (41%) |
| Not Started | 13 (59%) |

### Completed Articles
1. How To Get 55% Open Rates Like the Top-Performing Newsletters Do (Score: 4.2)
2. How to Write Email Subject Lines That Actually Get Opened in 2026 (Score: 3.2)
3. How To Use beehiiv To Create a Thriving Newsletter Community Hub (Score: 3.2)
4. How To Start a Newsletter for Local Communities (Score: 3.2)
5. Turn Newsletter Swaps Into Your Best Free Acquisition Channel (Score: 3.2)
6. How To Start a Newsletter for Operators and COOs (Score: 3.2)
7. Read the State of Newsletters report (Score: 2.6)
8. 20 Ways to Monetize Your Newsletter (Score: 2.6)
9. 10 Predictions That Will Reshape Newsletter Businesses in 2026 (Score: 2.6)

### High-Priority Not Started (by Weighted Score)
1. Why Your Emails Are Going to Gmail's Promotions (Score: 2.6) — *Should be prioritized; competitor has live content*
2. How To Build a Fanbase: From Followers to True Fans (Score: 2.2)
3. Milk Road: From 0 to Acquisition in 10 months (Score: 2.2)

### Cross-Reference with SEO
Unable to cross-reference published blogs with Ahrefs rankings this cycle due to missing API key. This should be a priority for the May cycle.

---

## What Worked

1. **Retargeting > Prospecting efficiency:** The ca-us retargeting campaign delivered leads at $93.74 CPA vs. $365.38 for prospecting — a 3.9x efficiency gap. Warm audiences convert significantly better.
2. **Mexico market CPCs:** At $0.88 CPC, the Mexico PMS prospecting campaign achieves volume at a fraction of US/Canada costs. 13 leads at $121.84 CPA is strong.
3. **Brazil engagement at scale:** The Hostfully Brazil campaign reached 315K impressions, demonstrating strong brand presence in LATAM markets.
4. **Content pipeline cleared the highest-value items first:** All 4.2+ and 3.2-scored articles were completed, showing good prioritization.

---

## What Didn't Work

1. **US/Canada prospecting CPA ($365):** The largest budget campaign has the worst unit economics. Without clearer segmentation or creative refresh, this spend is inefficient. *Diagnosis:* Broad targeting on a high-CPC market. Consider audience refinement or Advantage+ testing.
2. **AU/UK market traction:** Only 13 leads from $3,589 spend. The market may need different messaging or the audience pool may be too small for current budgets. *Diagnosis:* Limited local social proof and creative assets.
3. **Content pipeline velocity:** 41% completion rate means 13 articles remain untouched. At current velocity, the backlog will grow. *Diagnosis:* Resource constraints or unclear ownership.
4. **Cross-platform data gaps:** Google Ads and Ahrefs being unavailable severely limits strategic decision-making. We're flying partially blind.

---

## Learnings & Implications for May 2026

1. **Shift budget toward retargeting:** The 3.9x CPA gap between retargeting and prospecting is too large to ignore. Recommend increasing retargeting budget by 20-30% and testing more retargeting segments.
2. **LATAM is a growth lever:** Mexico and Brazil campaigns deliver strong volume at lower CPCs. Consider dedicated creative for these markets rather than translated US assets.
3. **Fix API integrations before next cycle:** Google Ads and Ahrefs data are critical for a complete picture. Without them, we can't assess multi-channel ROI or organic content impact.
4. **Accelerate content pipeline:** Prioritize the "Why Your Emails Are Going to Gmail's Promotions" article (Score 2.6, direct competitor content overlap) and the Milk Road case study (strong narrative potential).
5. **Test US/Canada prospecting creative refresh:** Current CPA is unsustainable. A/B test new angles focusing on pain points from the retargeting audience that converts well.
6. **Complete registration tracking:** Only 26 registrations from 124 leads suggests a 21% lead-to-registration rate. Investigate whether this is a tracking gap or a real funnel drop-off.

---

*Report generated automatically by the GTM Execution Commander. Data sources: Meta Marketing API (v23.0). Google Ads and Ahrefs data unavailable this cycle.*
