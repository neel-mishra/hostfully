# TLDR Ad Performance Report — Week of June 15, 2026

**Reporting Period:** June 8–14, 2026  
**Prior Period:** June 1–7, 2026  
**Generated:** Monday, June 15, 2026

---

## Headlines

1. **Meta spend jumped +29.7% WoW** ($9,544 vs. $7,357) as impressions surged +152%. CPC dropped from $1.91 to $1.02 — efficiency improved significantly despite the spend increase.
2. **Lead volume flat at 102 results both weeks** — higher spend hasn't yet translated into incremental conversions. CPL rose 30% to $93.57.
3. **Google Ads data unavailable** — the refresh token returned "Account has been deleted." Needs immediate attention from the team.

---

## Cross-Platform Summary

| Metric | Meta (This Week) | Meta (Prior Week) | WoW Change |
|--------|-------------------|--------------------|-----------:|
| Spend | $9,544.39 | $7,357.17 | +29.7% |
| Impressions | 731,697 | 290,175 | +152.2% |
| Clicks | 9,322 | 3,856 | +141.7% |
| CTR | 1.27% | 1.33% | -4.1% |
| CPC | $1.02 | $1.91 | -46.3% |
| Results (Leads) | 102 | 102 | 0.0% |
| CPL | $93.57 | $72.13 | +29.7% |

> **Note:** Google Ads data is not available this week. The GOOGLE_ADS_REFRESH_TOKEN returned an "invalid_grant / Account has been deleted" error. This report covers Meta Ads only.

---

## Anomalies & Flags

| Flag | Detail | Severity |
|------|--------|----------|
| ⚠️ Spend >10% over weekly pace | Meta spend up +29.7% WoW ($9,544 vs $7,357) | Medium |
| ⚠️ CPC 2x+ above account avg | ca-us_pms_prospecting: $4.55 CPC (4.4x avg $1.02) | High |
| ⚠️ CPC 2x+ above account avg | ca-us_pms_retargeting: $6.75 CPC (6.6x avg) | High |
| ⚠️ CPC 2x+ above account avg | au-uk_pms_retargeting: $6.25 CPC (6.1x avg) | Medium |
| 🔴 Google Ads API down | Token refresh failed — "Account has been deleted" | Critical |

---

## Meta Ads Detail

### Campaign Performance (Jun 8–14)

| Campaign | Spend | Impressions | Clicks | CTR | CPC | Results |
|----------|------:|------------:|-------:|----:|----:|--------:|
| ca-us_pms_prospecting_website-conv | $4,611.36 | 59,928 | 1,013 | 1.69% | $4.55 | 27 |
| [Leads] hostfully pt-br — meeting | $1,966.95 | 507,721 | 6,026 | 1.19% | $0.33 | 13 |
| mx_pms_prospecting_website-conv | $1,412.52 | 106,884 | 1,520 | 1.42% | $0.93 | 34 |
| eu_pms_prospecting_website-conv | $835.21 | 48,878 | 655 | 1.34% | $1.28 | 7 |
| ca-us_pms_retargeting_website-conv | $580.82 | 6,788 | 86 | 1.27% | $6.75 | 19 |
| au-uk_pms_retargeting_website-conv | $137.53 | 1,498 | 22 | 1.47% | $6.25 | 2 |
| **Total** | **$9,544.39** | **731,697** | **9,322** | **1.27%** | **$1.02** | **102** |

### Results Summary (from results-summary)

- **Results (lead results only, excl. post engagement): 102 lead_email-valid**
- 6 campaigns with delivery, all 6 produced results
- All results classified as `lead_email-valid`

### Notable Audiences (Top 3 Campaigns by Spend)

**ca-us_pms_prospecting_website-conv** ($4,611 spend)
- Active ad sets: LAL 2% ideal 5-to-30 PMS (paused), LAL 2% conference attendees (paused), others
- Geo: US, CA
- Age: 25–64

**[Leads] hostfully pt-br — meeting** ($1,967 spend)
- Highest impressions (507K) with lowest CPC ($0.33)
- Messaging-focused (2 messaging connections, 2 first replies)
- Strong engagement (5,988 post engagements)

**mx_pms_prospecting_website-conv** ($1,413 spend)
- Active ad set: "sitio web abril" — targeting property managers in MX, CO
- Ages 21–65, interests: Property management, Landlord, Facility management
- Advantage Audience enabled

---

## Google Ads Detail

> ❌ **Google Ads API unavailable this week.**  
> Error: Token refresh returned `invalid_grant` — "Account has been deleted."  
> Action required: Re-authenticate or reconnect the Google Ads API credentials in Cursor Dashboard > Secrets.

---

## Recommendations

1. **Fix Google Ads API access immediately.** The refresh token is invalid. Re-generate OAuth credentials and update `GOOGLE_ADS_REFRESH_TOKEN` in environment secrets to restore reporting visibility.

2. **Investigate rising CPCs on US/CA retargeting campaigns.** Both `ca-us_pms_retargeting` ($6.75 CPC) and `ca-us_pms_prospecting` ($4.55 CPC) are 4–7x above the account average of $1.02. Consider refreshing creative, tightening audience exclusions, or pausing underperforming ad sets.

3. **Audit spend-to-results efficiency.** Spend rose 30% WoW but lead volume stayed flat at 102. The additional budget is driving impressions (+152%) but not conversions. Evaluate whether scale is being pushed too aggressively before the funnel can absorb it — look at landing page conversion rates and form completion rates.

---

*Report generated automatically by TLDR Ad Performance Automation.*
