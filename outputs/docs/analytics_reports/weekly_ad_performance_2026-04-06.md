# TLDR Ad Performance Report — Week of April 6, 2026

**Reporting Period:** March 30 – April 5, 2026
**Prior Week:** March 23 – March 29, 2026
**Generated:** Monday, April 6, 2026

---

## Headlines

1. **Meta lead volume nearly doubled WoW** — 51 leads this week vs. 26 last week (+96%), despite a 17.6% drop in spend. The efficiency gain is driven by better CTR (1.05% vs. 0.49% prior week).
2. **Google Ads data unavailable** — The Google Ads API returned HTTP 404 for all queries. This is likely a Customer ID configuration issue. Google Ads metrics are excluded from this report. Immediate action is needed to restore Google Ads API access.
3. **CPC edging toward the 20% WoW flag** — Meta CPC rose 19.7% WoW ($4.80 → $5.75). Not yet over the anomaly threshold, but worth monitoring closely as the prospecting campaign in CA-US drives a $7.12 CPC.

---

## Cross-Platform Summary

| Metric | Meta (This Week) | Google (This Week) | Combined | WoW Change |
|---|---|---|---|---|
| **Spend** | $5,305.20 | N/A | $5,305.20 | -17.6% |
| **Impressions** | 87,440 | N/A | 87,440 | -68.2% |
| **Clicks** | 922 | N/A | 922 | -31.3% |
| **CTR** | 1.054% | N/A | 1.054% | +116.4% |
| **CPC** | $5.75 | N/A | $5.75 | +19.7% |
| **Results** | 130 | N/A | 130 | — |
| **Leads (account-level)** | 51 | N/A | 51 | +96.2% |
| **CPL** | $104.02 | N/A | $104.02 | — |
| **Cost per Result** | $40.81 | N/A | $40.81 | — |

> **Note:** Google Ads API returned HTTP 404 for all endpoints this week. All combined metrics reflect Meta only. Prior-week Google Ads data is also unavailable for comparison.

**Meta Results (from results-summary):** 130 total (124 lead_email-valid, 6 onsite conversion post unsave). This is lead results only, excluding Post engagements.

---

## Anomalies & Flags

| Flag | Detail | Severity |
|---|---|---|
| **CPC +19.7% WoW** | $4.80 → $5.75. Just under the 20% threshold. ca-us_pms_prospecting drives a $7.12 CPC. | ⚠️ Watch |
| **Spend -17.6% WoW** | $6,438 → $5,305. More than 10% under weekly pace. Budgets may need reallocation or the engagement campaign scaled down. | ⚠️ Flag |
| **Impressions -68.2% WoW** | 275K → 87K. Massive drop likely driven by reduced [Post Promovido] engagement campaign delivery and lower prospecting reach. | ⚠️ Flag |
| **Google Ads API Down** | All Google Ads queries returned HTTP 404. Entire platform missing from report. | 🔴 Critical |
| **au-uk_pms_retargeting: $0 leads this week** | Campaign spent $133.61 but generated 0 leads in the 7-day performance window. Results-summary attributes 4 lead results to it (different aggregation window). | ⚠️ Watch |

---

## Meta Ads Detail

### Campaign Performance Table (March 30 – April 5)

| Campaign | Status | Spend | Impressions | Clicks | CTR | CPC | Leads | CPL |
|---|---|---|---|---|---|---|---|---|
| ca-us_pms_prospecting_website-conv | ACTIVE | $4,395.50 | 64,824 | 617 | 0.95% | $7.12 | 33 | $133.20 |
| ca-us_pms_retargeting_website-conv | ACTIVE | $354.02 | 5,058 | 77 | 1.52% | $4.60 | 8 | $44.25 |
| au-uk_pms_prospecting_website-conv | ACTIVE | $280.34 | 5,074 | 79 | 1.56% | $3.55 | 3 | $93.45 |
| au-uk_pms_retargeting_website-conv | ACTIVE | $133.61 | 1,574 | 25 | 1.59% | $5.34 | 0 | — |
| [Leads] hostfully pt-br — meeting | ACTIVE | $120.56 | 6,537 | 121 | 1.85% | $1.00 | 7 | $17.22 |
| [Post Promovido] pt-br | ACTIVE | $21.17 | 4,373 | 3 | 0.07% | $7.06 | — | — |
| **TOTAL** | | **$5,305.20** | **87,440** | **922** | **1.05%** | **$5.75** | **51** | **$104.02** |

### Results Summary (from results-summary endpoint)

| Campaign | Result Type | Result Value |
|---|---|---|
| ca-us_pms_prospecting_website-conv | lead_email-valid | 79 |
| ca-us_pms_retargeting_website-conv | lead_email-valid | 23 |
| [Leads] hostfully pt-br — meeting | lead_email-valid | 12 |
| au-uk_pms_prospecting_website-conv | lead_email-valid | 6 |
| au-uk_pms_retargeting_website-conv | lead_email-valid | 4 |
| [Post Promovido] pt-br | onsite conversion post unsave | 6 |
| **TOTAL** | | **130** |

### Top Campaign Ad Set Breakdown

#### 1. ca-us_pms_prospecting_website-conv ($4,395.50 spend)

| Ad Set | Audience | Spend (30d) | Impressions (30d) | CTR | CPC |
|---|---|---|---|---|---|
| ca-us_lal_1pct-ideal-5to30_pms | LAL 1% PMS Customers (Hatchlings) — US/CA | $11,843.71 | 204,151 | 0.91% | $6.35 |
| ca-us_lal_1pct-ideal-5to30-demolayered_pms | LAL 1% PMS Customers + Interest/Job Overlay | $6,841.90 | 151,476 | 0.77% | $5.84 |
| ca-us_lal_1-pct-conf-attendees | LAL 1% Conference Attendees — US/CA | $4,081.51 | 69,736 | 0.84% | $6.94 |

> Interest overlay includes: Airbnb, VRBO, Booking.com, Holiday Rental, Property Management, Boutique Hotel. Job titles: Owner/Property Manager, Rental Agent, Rental Manager.

#### 2. au-uk_pms_prospecting_website-conv ($280.34 spend)

| Ad Set | Audience | Targeting |
|---|---|---|
| au-uk_lal_conf-attendees | LAL 1% Conference Attendees | AU/UK, Ages 25-64 |

#### 3. ca-us_pms_retargeting_website-conv ($354.02 spend)

| Ad Set | Audience | Spend (30d) | Impressions (30d) | CTR | CPC |
|---|---|---|---|---|---|
| ca-us_rtg_90d-visitors_pms | Website Visitors (90d), Churned Customers, GB Users, Conference Attendees, Social Engagers — US/CA | $2,042.22 | 38,970 | 1.07% | $4.90 |

### Notable Audiences

- **Strongest CPL:** [Leads] hostfully pt-br at $17.22/lead — the lowest CPL across all campaigns, running on the Brazilian market for meeting bookings.
- **Largest Spender:** ca-us_pms_prospecting at $4,395.50/wk (83% of total Meta spend). The LAL 1% PMS Customers ad set drives the most volume.
- **Retargeting Efficiency:** ca-us retargeting delivers $44.25 CPL on an audience of website visitors, churned customers, and conference attendees. Good efficiency vs. prospecting at $133.20.
- **Audience Overlap Risk:** Conference attendees LAL is excluded from other ad sets in ca-us_pms_prospecting, reducing overlap.

---

## Google Ads Detail

**Google Ads API is currently unavailable.** All queries returned HTTP 404 (Not Found). This prevents pulling account summary, campaign data, and keyword performance.

**Action Required:** Verify the `GOOGLE_ADS_CUSTOMER_ID` and `GOOGLE_ADS_MANAGER_ID` environment variables. The configured customer ID may be incorrect or the API version (v18) may need updating.

---

## Recommendations

1. **Restore Google Ads API access immediately.** The 404 errors suggest a misconfigured Customer ID or an expired API version. Without Google Ads data, we're flying blind on half the paid media portfolio. Check that `GOOGLE_ADS_CUSTOMER_ID` matches the active account and that API v18 is still supported.

2. **Monitor ca-us_pms_prospecting CPC closely.** At $7.12/click it's the highest CPC campaign and drives 83% of total spend. The conference attendees ad set ($6.94 CPC) and demo-layered set ($5.84 CPC) are the most efficient within this campaign — consider shifting budget toward the demo-layered set which has the lowest CPC.

3. **Investigate au-uk_pms_retargeting performance.** The campaign spent $133.61 but generated 0 leads in the 7-day window (though results-summary attributes 4 results from a broader window). If retargeting audiences are exhausted in AU/UK, consider refreshing the custom audience lists or pausing to reallocate budget to the prospecting campaign that has a lower CPC ($3.55).

---

## Appendix: WoW Calculation Method

| Metric | 14-Day Total | This Week (7d) | Prior Week (derived) | WoW Δ |
|---|---|---|---|---|
| Spend | $11,743.62 | $5,305.20 | $6,438.42 | -17.6% |
| Impressions | 362,644 | 87,440 | 275,204 | -68.2% |
| Clicks | 2,263 | 922 | 1,341 | -31.3% |
| CTR | 0.624% | 1.054% | 0.487% | +116.4% |
| CPC | $5.19 | $5.75 | $4.80 | +19.7% |
| Leads | 77 | 51 | 26 | +96.2% |
