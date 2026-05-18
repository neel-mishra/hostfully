# TLDR Ad Performance Report — Week of May 11-17, 2026

*Generated: Monday, May 18, 2026 | Reporting Period: May 11 – May 17, 2026*

---

## Headlines

1. **Meta spend surged 62% WoW to $10,065** — driven by ca-us_pms_prospecting ramping up to $5,039 (50% of total Meta spend). Despite higher spend, blended CPC actually improved from $2.36 to $1.80, a 24% decrease.

2. **132 Meta Results generated (lead results only)** — 127 lead_email-valid conversions plus 5 onsite conversions across 7 active campaigns. The mx_pms_prospecting campaign led with 42 results on just $1,301 spend ($31 cost per result).

3. **Google Ads data unavailable this week** — the Google Ads API returned a 404 error during data pull. This report covers Meta Ads only. Google Ads data gap should be investigated before next week's report.

---

## Cross-Platform Summary

| Metric | Meta (This Week) | Meta (Prior Week) | WoW Change | Google | Combined |
|---|---|---|---|---|---|
| Spend | $10,064.97 | $6,200.78 | +$3,864.19 (+62.3%) | N/A | $10,064.97 |
| Impressions | 416,568 | 165,080 | +251,488 (+152.3%) | N/A | 416,568 |
| Clicks | 5,586 | 2,632 | +2,954 (+112.3%) | N/A | 5,586 |
| CTR | 1.34% | 1.59% | -0.25pp (-15.7%) | N/A | 1.34% |
| CPC | $1.80 | $2.36 | -$0.56 (-23.5%) | N/A | $1.80 |
| Leads (action) | 44 | 28 | +16 (+57.1%) | N/A | 44 |
| Results | 132 | — | — | N/A | 132 |
| CPL | $228.75 | $221.46 | +$7.29 (+3.3%) | N/A | $228.75 |
| Cost/Result | $76.25 | — | — | N/A | $76.25 |

*Prior week = derived from 14-day minus 7-day account summary. Results prior week unavailable (API returned identical totals for both periods).*

---

## Anomalies & Flags

### CTR Dropped 15.7% WoW
- This week: 1.34% vs. prior week: 1.59%
- Exceeds the 15% threshold. The drop is likely a mix effect: the massive increase in impressions (+152%) from scaled spend diluted click-through rates, particularly in the high-impression ca-us_pms_prospecting campaign (CTR 1.66%) and hostfully pt-br (CTR 0.87%).

### Spend 62.3% Above Prior Week Pace
- This week: $10,064.97 vs. prior week: $6,200.78
- Significantly exceeds the 10% threshold. The ca-us_pms_prospecting campaign alone accounted for $5,039 in spend (81% of the increase). Verify this is intentional budget scaling.

### Retargeting Campaigns CPC 2x+ Above Account Average
- **ca-us_pms_retargeting**: CPC $5.00 (2.78x the $1.80 account average)
- **au-uk_pms_retargeting**: CPC $4.82 (2.68x the $1.80 account average)
- Retargeting CPCs are structurally higher due to smaller audiences, but worth monitoring. The au-uk campaign generated 0 leads this week despite $106 in spend.

### au-uk_pms_retargeting: 0 Leads from Campaign-Level Data
- Campaign-performance returned 0 lead actions for this campaign in the 7d window, though results-summary attributed 3 lead_email-valid results. The discrepancy may be a timing/attribution difference. Worth verifying in Ads Manager directly.

### Google Ads API Unavailable
- The Google Ads API returned HTTP 404 on all queries. This may indicate an endpoint version mismatch (v18) or account access issue. No Google Ads data is available for this reporting period.

---

## Meta Ads Detail

### Campaign Performance (May 11-17)

| Campaign | Spend | Impressions | Clicks | CTR | CPC | Leads | Results | Result Type |
|---|---|---|---|---|---|---|---|---|
| ca-us_pms_prospecting_website-conv | $5,039.08 | 86,282 | 1,435 | 1.66% | $3.51 | 11 | 27 | lead_email-valid |
| [Leads] hostfully pt-br — meeting | $2,243.92 | 145,336 | 1,259 | 0.87% | $1.78 | 6 | 22 | lead_email-valid |
| mx_pms_prospecting_website-conv | $1,300.91 | 115,695 | 1,881 | 1.63% | $0.69 | 16 | 42 | lead_email-valid |
| eu_pms_prospecting_website-conv | $919.82 | 59,809 | 898 | 1.50% | $1.02 | 4 | 15 | lead_email-valid |
| ca-us_pms_retargeting_website-conv | $455.26 | 7,713 | 91 | 1.18% | $5.00 | 7 | 18 | lead_email-valid |
| au-uk_pms_retargeting_website-conv | $106.05 | 1,735 | 22 | 1.27% | $4.82 | 0 | 3 | lead_email-valid |
| [Post Promovido] pt-br | ~$0* | ~0* | ~0* | — | — | — | 5 | onsite conv |
| **TOTAL** | **$10,064.97** | **416,568** | **5,586** | **1.34%** | **$1.80** | **44** | **132** | — |

*Post Promovido returned no 7d campaign-performance data but contributed 5 results per results-summary.*

### Results Summary (from results-summary endpoint)
- **Total Results (lead only, excl. post engagements): 132**
- 127 lead_email-valid + 5 onsite conversion post net comment
- 7 campaigns with delivery contributed results

### Notable Audiences & Ad Sets (Top 3 Campaigns by Spend)

**ca-us_pms_prospecting_website-conv ($5,039)**
- Multiple ad sets targeting US/CA with Lookalike audiences (2% of PMS customer list), interest-based (Property management, Landlord, Facility management), and broad targeting
- Key excluded audiences: existing customers, churned users, retargeting pools

**[Leads] hostfully pt-br — meeting ($2,244)**
- Extensive Brazilian market targeting across major cities (São Paulo, Rio, Florianópolis, Belo Horizonte, etc.)
- Behavioral targeting: Frequent international travelers, Property management interests
- Multiple ad sets across Instagram and Facebook placements

**mx_pms_prospecting_website-conv ($1,301)**
- 2 active ad sets: "sitio web Mayo S&P" ($1,410 / 30d) and "sitio web abril" ($2,297 / 30d)
- Targeting Mexico + Colombia, ages 21-65, Property management interests
- Advantage Audience enabled for age/gender expansion

---

## Google Ads Detail

**DATA UNAVAILABLE** — Google Ads API returned HTTP 404 on all queries this week. The endpoint `https://googleads.googleapis.com/v18/customers/{id}/googleAds:searchStream` may require a version update or credential refresh.

Environment check confirmed all 5 required Google Ads credentials are set (CLIENT_ID, CLIENT_SECRET, DEVELOPER_TOKEN, REFRESH_TOKEN, CUSTOMER_ID). MANAGER_ID is not configured.

**Action Required**: Investigate the 404 error — possible causes include API version deprecation (v18), developer token restrictions, or customer ID mismatch.

---

## Recommendations

1. **Investigate the Google Ads API failure** — The 404 error needs resolution before next week. Try downgrading to API v17, verify the developer token access level, and confirm the customer ID maps to an active account. Without Google Ads data, we have an incomplete picture of paid performance.

2. **Monitor ca-us_pms_prospecting efficiency at higher spend** — This campaign absorbed 50% of Meta budget ($5,039) with a $3.51 CPC (nearly 2x account average). While it generated 27 results, the cost per result ($186.63) is significantly higher than mx_pms_prospecting ($30.97/result). Consider shifting budget toward the MX campaign which delivers 6x better cost efficiency.

3. **Evaluate au-uk_pms_retargeting_website-conv** — At $106 spend with 0 leads from campaign-level data and a $4.82 CPC (2.7x account average), this campaign may need creative refresh or audience expansion. If performance doesn't improve next week, consider pausing and reallocating budget to higher-performing geos.

---

*Report generated automatically by TLDR Ad Performance Dashboard. Google Ads data gap noted — next report should include both platforms.*
