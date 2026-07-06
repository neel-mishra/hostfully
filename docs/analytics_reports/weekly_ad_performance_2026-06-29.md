# TLDR Ad Performance Report — Week of June 29, 2026

**Report Period:** June 29 – July 5, 2026
**Generated:** July 6, 2026

---

## Headlines

1. **Lead volume collapsed 95% WoW** — Only 1 tracked lead conversion this week vs. 21 last week. Two high-volume campaigns (mx_pms_prospecting and hostfully pt-br) went to PAUSED status, removing the bulk of lead-generating spend.
2. **CPC surged 54% WoW ($2.35 → $3.63)** — With the lower-CPC campaigns paused, remaining spend concentrated in higher-cost US/Canada prospecting and retargeting, driving blended CPC well above the 20% anomaly threshold.
3. **Google Ads data unavailable** — The Google Ads API returned an authentication error ("invalid_grant — Account has been deleted"). This report covers Meta Ads only. Google Ads data gap must be resolved before next week.

---

## Cross-Platform Summary

| Metric | Meta (This Week) | Meta (Prior Week) | WoW Change | Google | Combined |
|---|---|---|---|---|---|
| Spend | $6,163.14 | $6,685.94 | -7.8% | N/A | $6,163.14 |
| Impressions | 140,179 | 256,037 | -45.3% | N/A | 140,179 |
| Reach | 72,739 | — | — | N/A | 72,739 |
| Clicks | 1,697 | 2,841 | -40.3% | N/A | 1,697 |
| CTR | 1.21% | 1.11% | +9.0% | N/A | 1.21% |
| CPC | $3.63 | $2.35 | +54.5% 🔴 | N/A | $3.63 |
| Lead Conversions | 1 | 21 | -95.2% 🔴 | N/A | 1 |
| Custom Conversions | 36 | 76 | -52.6% 🔴 | N/A | 36 |
| Results (leads, 30d roll-up) | 94 | — | — | N/A | 94 |

> **Note on Results:** The results-summary endpoint reports 94 lead_email-valid results. This figure reflects the broader campaign lifetime window due to how the Meta campaigns API returns insights sub-fields; the accurate 7-day lead count from the account-level insights endpoint is 1.

---

## Anomalies & Flags

| # | Flag | Detail | Severity |
|---|---|---|---|
| 1 | 🔴 CPC +54.5% WoW | $2.35 → $3.63. Threshold: >20%. Driven by paused low-CPC campaigns shifting mix to higher-cost segments. | High |
| 2 | 🔴 Lead conversions -95% | 21 → 1. Two lead-generating campaigns paused mid-period. | Critical |
| 3 | 🟡 Impressions -45.3% WoW | Significant volume drop from paused campaigns. | Medium |
| 4 | 🟡 Custom conversions -53% | 76 → 36. Correlates with reduced impression volume. | Medium |
| 5 | 🟡 Campaigns with $0 conversions | eu_pms_prospecting ($690 spend, 0 leads), ca-us_pms_retargeting ($528 spend, 0 leads), au-uk_pms_retargeting ($156 spend, 0 leads). All had leads in the prior period. | Medium |
| 6 | 🔴 Google Ads API outage | Token refresh failed: "Account has been deleted." No Google Ads data available. | Critical |
| 7 | 🟡 Spend -7.8% under pace | $6,163 vs. $6,686 prior week, though within 10% threshold. | Low |

---

## Meta Ads Detail

### Campaign Performance (June 29 – July 5)

| Campaign | Status | Spend | Impressions | Clicks | CTR | CPC | Leads |
|---|---|---|---|---|---|---|---|
| ca-us_pms_prospecting_website-conv | ACTIVE | $4,788.19 | 80,246 | 1,155 | 1.44% | $4.15 | 1 |
| eu_pms_prospecting_website-conv | ACTIVE | $690.45 | 49,315 | 438 | 0.89% | $1.58 | 0 |
| ca-us_pms_retargeting_website-conv | ACTIVE | $528.04 | 8,064 | 77 | 0.95% | $6.86 | 0 |
| au-uk_pms_retargeting_website-conv | ACTIVE | $156.46 | 2,554 | 27 | 1.06% | $5.79 | 0 |
| mx_pms_prospecting_website-conv | PAUSED | $0.00 | — | — | — | — | — |
| [Leads] hostfully pt-br — meeting | PAUSED | $0.00 | — | — | — | — | — |
| **Total** | | **$6,163.14** | **140,179** | **1,697** | **1.21%** | **$3.63** | **1** |

### Campaign CPC vs. Account Average ($3.63)

| Campaign | CPC | vs. Avg |
|---|---|---|
| ca-us_pms_retargeting_website-conv | $6.86 | 1.89x |
| au-uk_pms_retargeting_website-conv | $5.79 | 1.60x |
| ca-us_pms_prospecting_website-conv | $4.15 | 1.14x |
| eu_pms_prospecting_website-conv | $1.58 | 0.44x |

No campaign exceeded the 2x account-average CPC threshold, though both retargeting campaigns are trending toward it.

### Notable Audiences & Ad Sets

**ca-us_pms_prospecting_website-conv** (77.7% of total spend):
- Multiple LAL ad sets (1% lookalike based on ideal customer profiles, 5-30 property managers)
- World Cup promo ad sets paused mid-period
- Geo: US + Canada, Ages 25-64

**eu_pms_prospecting_website-conv** (11.2% of spend):
- EU LAL (1% lookalike, demo-layered)
- Broad prospecting ad set also active
- Geo: Multiple EU countries, Ages 25-64

**ca-us_pms_retargeting_website-conv** (8.6% of spend):
- Single ad set: 90-day website visitors retargeting
- Custom audiences: churned PMS customers, GB users w/o PMS, webinar warm leads, conference attendees
- Exclusions: existing PMS customers, IG/FB followers

### Results Summary (30-Day Roll-Up from results-summary)

| Campaign | Result Type | Count |
|---|---|---|
| mx_pms_prospecting_website-conv | lead_email-valid | 31 |
| ca-us_pms_prospecting_website-conv | lead_email-valid | 25 |
| ca-us_pms_retargeting_website-conv | lead_email-valid | 16 |
| [Leads] hostfully pt-br — meeting | lead_email-valid | 15 |
| eu_pms_prospecting_website-conv | lead_email-valid | 5 |
| au-uk_pms_retargeting_website-conv | lead_email-valid | 2 |
| **Total** | | **94** |

---

## Google Ads Detail

**⚠️ UNAVAILABLE** — The Google Ads API refresh token returned `invalid_grant` with message "Account has been deleted." No campaign, keyword, or conversion data could be retrieved for this period.

**Action Required:** Re-authenticate the Google Ads API credentials in the Cursor Dashboard (Cloud Agents > Secrets). Verify the `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_CLIENT_ID`, and `GOOGLE_ADS_CLIENT_SECRET` environment variables are current.

---

## Recommendations

1. **Investigate paused campaigns immediately.** The mx_pms_prospecting and hostfully pt-br campaigns were responsible for 46 of the 94 rolling results (49%). Their pause is the primary driver of this week's lead volume collapse. If paused intentionally, ensure replacement campaigns are ready; if accidental, re-enable ASAP.

2. **Fix Google Ads API authentication.** The `invalid_grant` error means the refresh token has been revoked or the associated account deleted. Re-generate OAuth credentials and update `GOOGLE_ADS_REFRESH_TOKEN` in the Cloud Agent secrets. Without Google Ads data, cross-platform reporting is incomplete and blended metrics are unreliable.

3. **Review retargeting CPC efficiency.** Both retargeting campaigns (ca-us at $6.86 CPC, au-uk at $5.79) are delivering 0 leads this week at 1.6-1.9x the account average CPC. Consider refreshing retargeting creative or tightening audience windows to improve conversion rates before CPCs breach the 2x threshold.

---

*Report generated by TLDR Weekly Ad Performance Dashboard automation.*
*Data sources: Meta Marketing API (Graph API v23.0). Google Ads API unavailable.*
