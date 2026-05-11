# TLDR Ad Performance Report — Week of May 4–10, 2026

**Generated:** Monday, May 11, 2026 01:02 UTC
**Reporting Period:** May 4 – May 10, 2026
**Prior Week:** April 27 – May 3, 2026

---

## Headlines

1. **Meta spend surged 35.6% WoW ($6,195 vs. $4,567)** — driven by ca-us and au-uk prospecting campaigns ramping up. Leads increased 75% (28 vs. 16), so efficiency held steady.
2. **129 total Meta results this week** (123 lead_email-valid + 6 onsite conversions) across 7 active campaigns with delivery.
3. **Google Ads data unavailable this week** — the API returned 404 errors (customer ID / endpoint configuration issue). Recommend verifying GOOGLE_ADS_CUSTOMER_ID and GOOGLE_ADS_MANAGER_ID in the Cloud Agent secrets. Report reflects Meta performance only.

---

## Cross-Platform Summary

| Metric | Meta (This Week) | Meta (Prior Week) | WoW Change | Google | Combined |
|---|---|---|---|---|---|
| Spend | $6,195.06 | $4,567.22 | +$1,627.84 (+35.6%) | N/A | $6,195.06 |
| Impressions | 164,967 | 132,667 | +32,300 (+24.3%) | N/A | 164,967 |
| Reach | 63,517 | — | — | N/A | 63,517 |
| Clicks | 2,632 | 2,015 | +617 (+30.6%) | N/A | 2,632 |
| CTR | 1.60% | 1.52% | +0.08pp (+5.0%) | N/A | 1.60% |
| CPC | $2.35 | $2.27 | +$0.09 (+3.7%) | N/A | $2.35 |
| Leads | 28 | 16 | +12 (+75.0%) | N/A | 28 |
| Complete Registrations | 7 | 5 | +2 (+40.0%) | N/A | 7 |
| **Results** | **129** | — | — | N/A | **129** |

*Results line (from results-summary, lead results only, excl. post engagements): 123 lead_email-valid, 6 onsite conversion post net comment*

---

## Anomalies & Flags

| Flag | Detail | Severity |
|---|---|---|
| **Spend >10% over weekly pace** | Meta spend up 35.6% WoW ($6,195 vs. $4,567). This is a significant jump — verify whether this reflects intentional budget increases on prospecting campaigns or an unplanned overshoot. | HIGH |
| **Google Ads API unavailable** | HTTP 404 on all Google Ads endpoints. Customer ID is set but returning not-found. No Google data available for this report period. | HIGH |
| CPC within normal range | CPC up only 3.7% WoW ($2.35 vs. $2.27) — below the 20% alert threshold. | OK |
| CTR improving | CTR improved 5.0% WoW (1.60% vs. 1.52%) — healthy trend. | OK |
| No zero-conversion campaigns | All campaigns with prior-week conversions maintained conversions this week. | OK |

---

## Meta Ads Detail

### Campaign Performance (Campaigns with Delivery)

| Campaign | Status | Objective | 30d Spend | 30d Clicks | 30d CPC | Results (7d) | Result Type |
|---|---|---|---|---|---|---|---|
| ca-us_pms_prospecting_website-conv | ACTIVE | LEADS | $15,880.22 | 2,582 | $6.15 | 38 | lead_email-valid |
| [Leads] \| hostfully \| pt-br — meeting | ACTIVE | LEADS | $6,704.90 | 2,181 | $3.07 | 25 | lead_email-valid |
| au-uk_pms_prospecting_website-conv | ACTIVE | LEADS | $3,204.72 | 706 | $4.54 | 12 | lead_email-valid |
| mx_pms_prospecting_website-conv | ACTIVE | LEADS | $2,405.16 | 2,930 | $0.82 | 26 | lead_email-valid |
| ca-us_pms_retargeting_website-conv | ACTIVE | LEADS | $2,292.64 | 397 | $5.77 | 19 | lead_email-valid |
| au-uk_pms_retargeting_website-conv | ACTIVE | LEADS | $618.55 | 117 | $5.29 | 3 | lead_email-valid |
| [Post Promovido] \| pt-br | PAUSED | ENGAGEMENT | $150.16 | 147 | $1.02 | 6 | onsite conversion |
| [Leads] LAL1% \| hostfully \| pt-br — meeting | PAUSED | LEADS | $74.19 | 43 | $1.73 | 0 | — |

### Campaign CPC Analysis (Anomaly Check: 2x Above Account Average)

Account average CPC: $2.35

| Campaign | CPC | vs. Account Avg |
|---|---|---|
| ca-us_pms_prospecting_website-conv | $6.15 | **2.6x** — FLAG |
| ca-us_pms_retargeting_website-conv | $5.77 | **2.5x** — FLAG |
| au-uk_pms_retargeting_website-conv | $5.29 | **2.3x** — FLAG |
| au-uk_pms_prospecting_website-conv | $4.54 | **1.9x** |
| [Leads] \| hostfully \| pt-br — meeting | $3.07 | 1.3x |
| [Leads] LAL1% \| hostfully \| pt-br — meeting | $1.73 | 0.7x |
| [Post Promovido] \| pt-br | $1.02 | 0.4x |
| mx_pms_prospecting_website-conv | $0.82 | 0.3x |

Three campaigns exceed 2x the account average CPC — all are US/CA/AU/UK market prospecting/retargeting campaigns targeting English-speaking audiences, which typically carry higher CPC than LATAM markets.

### Top Campaign Ad Sets (by Spend)

**ca-us_pms_prospecting_website-conv (ID: 6954321351868)**
- ca-us_lal_2pct-ideal-5to30_pms — Targeting US/CA, Ages 25-64, Lookalike 2% ideal customer list. Spend: $1,338.30 (30d), 154 clicks, CPC $8.69
- Multiple additional ad sets targeting various lookalike audiences and interest-based segments

**[Leads] | hostfully | pt-br — meeting (ID: 6896525103468)**
- Multiple ad sets targeting Brazilian cities (Balneário Camboriú, Belo Horizonte, Brasília, Cabo Frio, etc.)
- Conference attendee lookalike audiences (1% LAL)
- Ages 30-50, geographic targeting focused on major Brazilian vacation rental markets

**au-uk_pms_prospecting_website-conv (ID: 6954326744668)**
- au-uk_lal_2pct-ideal-5to30_pms — Targeting AU/UK, Ages 25-64, Lookalike 2% ideal customer list. Spend: $382.00 (30d), 84 clicks, CPC $4.55

### Notable Audiences
- **US/CA Prospecting**: Lookalike 2% of ideal PMS customers (5-30 properties), age 25-64, excluding current customers and retargeting lists
- **Brazil Meeting Campaign**: Brazilian city-level geo-targeting with conference attendee lookalikes, age 30-50
- **AU/UK**: Same lookalike model as US/CA, adapted for AU/UK geos

---

## Google Ads Detail

**UNAVAILABLE THIS WEEK**

The Google Ads API returned HTTP 404 errors on all endpoints (account-summary, campaigns). The GOOGLE_ADS_CUSTOMER_ID environment variable is set but the API endpoint is not resolving. Possible causes:
- Customer ID format issue (should be 10 digits, no dashes)
- Manager ID (MCC login-customer-id) may be required but is not set
- API version mismatch or account access issue

**Action Required:** Verify Google Ads credentials in the Cloud Agent Secrets dashboard.

---

## Recommendations

1. **Investigate the spend surge** — Meta spend jumped 35.6% WoW. If this reflects intentional budget scaling on prospecting campaigns, validate that CPL is holding at acceptable levels ($221/lead currently vs. prior week). If unintentional, review daily budget settings on ca-us and au-uk prospecting campaigns.

2. **Fix Google Ads API access** — The GOOGLE_ADS_MANAGER_ID appears to be unset. For MCC-managed accounts, this is required as the `login-customer-id` header. Set this in the Cloud Agent secrets to restore Google Ads reporting. Without Google data, we have an incomplete picture of blended paid media performance.

3. **Monitor high-CPC campaigns** — Three campaigns (ca-us prospecting, ca-us retargeting, au-uk retargeting) have CPCs 2.3–2.6x above account average. While this is expected for English-speaking markets, review ad creative freshness and audience saturation signals for these campaigns. Consider testing new creative or expanding lookalike seed lists.

---

*Report generated automatically by the TLDR Weekly Ad Performance Dashboard automation. Google Ads data gap noted — resolve API configuration for complete cross-platform reporting next week.*
