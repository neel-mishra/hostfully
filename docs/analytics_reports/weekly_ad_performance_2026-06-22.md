# TLDR Ad Performance — Week of June 15, 2026

**Report Date:** Monday, June 22, 2026
**Reporting Period:** June 15–21, 2026
**Prior Week:** June 8–14, 2026
**Data Sources:** Meta Ads (live) | Google Ads (unavailable — see note below)

---

## Headlines

1. **Meta CPC spiked +123% WoW to $2.29** — driven by impressions dropping 48% while spend climbed 16%. The ca-us prospecting campaign alone ran a $5.16 CPC, more than double the account average.
2. **115 lead results tracked in Meta results-summary** — 6 active campaigns with delivery all generated lead_email-valid conversions. Top performers: mx_pms_prospecting (36), ca-us_pms_prospecting (32), ca-us_pms_retargeting (18), and pt-br meeting (18).
3. **Google Ads data gap this week** — the Google Ads API returned "invalid_grant / Account has been deleted" on token refresh. All Google metrics are unavailable. Immediate investigation is required to restore access.

---

## Cross-Platform Summary

| Metric | Meta (This Week) | Meta (Prior Week) | WoW Change | Google | Combined |
|---|---|---|---|---|---|
| Spend | $11,051.80 | $9,553.06 | +15.7% | N/A | $11,051.80 |
| Impressions | 383,315 | 731,855 | -47.6% | N/A | 383,315 |
| Clicks | 4,827 | 9,323 | -48.2% | N/A | 4,827 |
| CTR | 1.26% | 1.27% | -0.8% | N/A | 1.26% |
| CPC | $2.29 | $1.02 | +123.4% | N/A | $2.29 |
| Leads (account) | 37 | 31 | +19.4% | N/A | 37 |
| CPL | $298.70 | $308.16 | -3.1% | N/A | $298.70 |
| **Results** | **115 lead_email-valid** | — | — | N/A | **115** |

> **Results line (from results-summary):** Results (lead results only, excl. post engagement): 115 lead_email-valid
>
> **Note on prior-week derivation:** Prior week = last_14d account-summary minus last_7d account-summary. Results-summary returned identical totals (115) for both 7d and 14d windows, indicating a possible API date-scoping issue with campaign-level embedded insights. Account-summary data is used for reliable WoW comparison.

---

## Anomalies & Flags

| Flag | Threshold | Actual | Severity |
|---|---|---|---|
| CPC increased WoW | >20% | **+123.4%** | HIGH |
| Spend over weekly pace | >10% | **+15.7%** | MEDIUM |
| ca-us_pms_prospecting CPC vs account avg | >2x ($4.58) | **$5.16 (2.25x)** | HIGH |
| ca-us_pms_retargeting CPC vs account avg | >2x ($4.58) | **$6.02 (2.63x)** | HIGH |
| au-uk_pms_retargeting CPC vs account avg | >2x ($4.58) | **$5.51 (2.41x)** | MEDIUM |
| au-uk_pms_retargeting: 0 leads from campaign-perf | 0 conversions | **0 leads** | MEDIUM |
| Impressions dropped 48% WoW | Not flagged by ruleset | **-47.6%** | WATCH |
| Google Ads API unavailable | — | Token refresh failed | CRITICAL |

### Detailed Flag Notes

- **CPC spike explanation:** Impressions collapsed 48% (383K vs 732K) while spend grew 16% ($11.1K vs $9.6K). Fewer impressions being served at higher cost points to audience saturation or bid competition in the US/CA geo. The ca-us_pms_prospecting campaign is the primary offender at $5.16 CPC.
- **au-uk_pms_retargeting** generated $137.81 in spend with 1,705 impressions and 25 clicks but 0 tracked leads in campaign-performance. Results-summary reports 2 lead_email-valid, suggesting attribution-window differences. At $5.51 CPC on a retargeting campaign, efficiency is poor.
- **Google Ads outage:** The OAuth refresh token for Google Ads returned `invalid_grant` with message "Account has been deleted." This may indicate the refresh token was revoked, the OAuth app credentials changed, or the ads account was suspended. Requires immediate remediation.

---

## Meta Ads Detail

### Campaign Performance Table (June 15–21)

| Campaign | Spend | Impressions | Clicks | CTR | CPC | Leads | CPL | Results (summary) |
|---|---|---|---|---|---|---|---|---|
| ca-us_pms_prospecting_website-conv | $5,494.15 | 77,594 | 1,065 | 1.37% | $5.16 | 8 | $686.77 | 32 |
| [Leads] hostfully pt-br — meeting | $2,256.53 | 118,908 | 1,179 | 0.99% | $1.91 | 8 | $282.07 | 18 |
| mx_pms_prospecting_website-conv | $1,750.16 | 126,759 | 1,786 | 1.41% | $0.98 | 11 | $159.11 | 36 |
| eu_pms_prospecting_website-conv | $835.03 | 50,747 | 676 | 1.33% | $1.24 | 3 | $278.34 | 9 |
| ca-us_pms_retargeting_website-conv | $578.12 | 7,602 | 96 | 1.26% | $6.02 | 7 | $82.59 | 18 |
| au-uk_pms_retargeting_website-conv | $137.81 | 1,705 | 25 | 1.47% | $5.51 | 0 | N/A | 2 |
| **Total** | **$11,051.80** | **383,315** | **4,827** | **1.26%** | **$2.29** | **37** | **$298.70** | **115** |

### Notable Audiences (from ad-set data, top 3 campaigns)

**ca-us_pms_prospecting_website-conv:**
- LAL 1% Ideal 5-30 properties (US/CA): $1,005.59 spend, 17K impressions, CPC $8.18
- Broad PMS Interest (US/CA age 25-64): multiple ad sets running
- LAL1% Conference Attendees: active
- Excluded: PMS customer list, churned customers, retargeting lists, IG/FB followers

**[Leads] hostfully pt-br — meeting:**
- Multiple pt-br language ad sets targeting Brazil
- LAL audiences based on PMS customer lists (Brazil geo)
- Messaging-optimized ad sets (WhatsApp/Messenger): generating conversation starts

**mx_pms_prospecting_website-conv:**
- Mexico-targeted PMS prospecting
- Best CPL this week at $159.11 on $1,750 spend
- Strong CTR at 1.41%

### Results Detail (from results-summary)

All 6 active campaigns with delivery produced **lead_email-valid** results:
- mx_pms_prospecting_website-conv: 36 leads
- ca-us_pms_prospecting_website-conv: 32 leads
- ca-us_pms_retargeting_website-conv: 18 leads
- [Leads] hostfully pt-br — meeting: 18 leads
- eu_pms_prospecting_website-conv: 9 leads
- au-uk_pms_retargeting_website-conv: 2 leads

---

## Google Ads Detail

**UNAVAILABLE** — Google Ads API token refresh failed with `invalid_grant` ("Account has been deleted"). No Google Ads data could be retrieved for this reporting period.

**Action required:** Verify the Google Ads OAuth credentials, re-authorize the refresh token, or check the Google Ads account status in the Google Ads console.

---

## Recommendations

1. **Investigate and fix the ca-us_pms_prospecting CPC** — at $5.16 (2.25x the account average), this campaign is consuming 50% of total spend but delivering only 8 leads at $686.77 CPL. Consider tightening audience targeting, refreshing creatives, or reallocating budget to the mx_pms_prospecting campaign which delivers leads at $159 CPL.

2. **Restore Google Ads API access immediately** — the "Account has been deleted" error on OAuth token refresh is a critical blocker for cross-platform reporting and spend tracking. Re-generate the refresh token via the Google Ads OAuth flow, or verify the Google Ads account status in the admin console. This gap means we have zero visibility into Google Ads spend, conversions, and keyword performance.

3. **Double down on mx_pms_prospecting** — this campaign has the lowest CPC ($0.98), highest CTR (1.41%), and best CPL ($159.11) across the portfolio. With only $1,750 in weekly spend vs $5,494 for the underperforming ca-us prospecting campaign, there's clear room to scale the Mexico geo while optimizing the US/CA spend.

---

*Report generated by TLDR Ad Performance Automation (04) on 2026-06-22. Data sourced from Meta Marketing API v23.0. Google Ads data unavailable this week.*
