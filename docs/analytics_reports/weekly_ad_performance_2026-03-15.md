# Weekly Ad Performance Dashboard
**Week of March 8–14, 2026**
*Generated 2026-03-15 (Monday)*

---

## 1. Headlines

1. **Meta spend surged +75% WoW** — $6,709 this week vs $3,826 prior week. Several high-budget campaigns (PMS_Conversions-Manual, Guidebook_Conversions, PMS_Conversions-Retargeting) ran during this window before being paused, driving the spike.
2. **183 total results** — Consistent with last week's results-summary. Meta-Leads-PMS_Conversions-Manual (94) and Guidebook_Conversions (48) produced the majority.
3. **Google Ads API unavailable** — The Google Ads API endpoint (v18) returned 404 errors. Google Ads data is excluded from this report. Recommend upgrading the API wrapper to v19 before next Monday's pull.

---

## 2. Cross-Platform Summary

| Metric | Meta (Mar 8–14) | Google Ads | Combined | WoW Change (Meta) |
|--------|-----------------|------------|----------|-------------------|
| **Spend** | $6,708.73 | *unavailable* | $6,708.73 | **+75.3%** |
| **Impressions** | 159,347 | *unavailable* | 159,347 | **+100.7%** |
| **Clicks** | 1,541 | *unavailable* | 1,541 | +44.7% |
| **CTR** | 0.97% | *unavailable* | 0.97% | **−27.6%** |
| **CPC** | $4.35 | *unavailable* | $4.35 | **+21.2%** |
| **Results** | 183 | *unavailable* | 183 | — |
| **Cost / Result** | $36.66 | *unavailable* | $36.66 | — |
| **Pixel Leads** | 9 | *unavailable* | 9 | −66.7% |

*Prior week derived: Mar 1–7. Spend $3,826.31 · 79,382 imp · 1,065 clicks · 1.34% CTR · $3.59 CPC · 27 pixel leads.*

---

## 3. Anomalies & Flags

| # | Flag | Detail | Threshold |
|---|------|--------|-----------|
| 1 | ⚠️ CPC +21.2% WoW | $4.35 vs $3.59 prior week | >20% |
| 2 | ⚠️ CTR −27.6% WoW | 0.97% vs 1.34% prior week | >15% |
| 3 | ⚠️ Spend +75.3% over weekly pace | $6,709 vs $3,826 prior week | >10% |
| 4 | ⚠️ Pixel leads dropped −66.7% | 9 this week vs 27 prior week | Conversion drop |
| 5 | ℹ️ Google Ads API outage | v18 endpoint returning 404 | Platform gap |

**No campaigns** triggered the 2× CPC-above-account-average flag. Highest campaign CPC was ca-us_pms_prospecting at $4.93 (1.13× the $4.35 account average).

---

## 4. Results by Conversion Action

*From `results-summary --date-preset last_7d` — campaigns with delivery, one primary conversion per campaign.*

| Conversion Action | Count |
|-------------------|-------|
| lead_email-valid | 175 |
| custom_conversion | 5 |
| onsite conversion messaging block | 2 |
| onsite conversion post unsave | 1 |
| **Total (one_row_total)** | **183** |

---

## 5. Meta Ads Detail — Campaign Table (Last 7 Days)

### Active Campaigns with Spend

| Campaign | Spend | Impressions | Clicks | CTR | CPC | Results | Result Type |
|----------|-------|-------------|--------|-----|-----|---------|-------------|
| ca-us_pms_prospecting_website-conv | $3,996.66 | 76,979 | 811 | 1.05% | $4.93 | 7 | lead_email-valid |
| au-uk_pms_prospecting_website-conv | $1,345.15 | 27,714 | 334 | 1.21% | $4.03 | 3 | custom_conversion |
| ca-us_pms_retargeting_website-conv | $813.13 | 22,168 | 169 | 0.76% | $4.81 | 2 | custom_conversion |
| au-uk_pms_retargeting_website-conv | $381.60 | 7,009 | 143 | 2.04% | $2.67 | 2 | lead_email-valid |
| [Leads] hostfully pt-br — meeting | $122.26 | 6,468 | 64 | 0.99% | $1.91 | 3 | lead_email-valid |
| [Post Promovido] pt-br | $49.93 | 19,009 | 20 | 0.11% | $2.50 | 2 | messaging block |
| **Total (active campaigns)** | **$6,708.73** | **159,347** | **1,541** | **0.97%** | **$4.35** | **19** | |

### Paused Campaigns with Results Attributed This Period

These campaigns were active earlier in the window before being paused, and results are still being attributed:

| Campaign | Results | Result Type |
|----------|---------|-------------|
| Meta-Leads-PMS_Conversions-Manual | 94 | lead_email-valid |
| Meta-Leads-Guidebook_Conversions | 48 | lead_email-valid |
| Meta-Sales-PMS_Conversions-Retargeting | 14 | lead_email-valid |
| Meta-Sales-Industry Report_Prospecting | 7 | lead_email-valid |
| Meta-Engagement-Boosted_Posts | 1 | onsite conversion post unsave |

---

## 6. Notable Audiences — Ad Set Detail

### ca-us_pms_prospecting_website-conv (Top spender: $3,996.66)

| Ad Set | Status | Spend (30d) | Impressions (30d) | Clicks (30d) | CTR | CPC | Targeting |
|--------|--------|-------------|-------------------|--------------|-----|-----|-----------|
| ca-us_lal_1pct-ideal-5to30-demolayered_pms | ACTIVE | $2,534.89 | 49,081 | 495 | 1.01% | $5.12 | LAL 1% ideal customers + interest targeting (vacation rentals, property mgmt, Airbnb, VRBO) |
| ca-us_lal_1pct-ideal-5to30_pms | ACTIVE | $1,390.80 | 26,643 | 306 | 1.15% | $4.55 | LAL 1% ideal customers (5-30 properties) |
| ca-us_lal_1-pct-conf-attendees | PAUSED | $70.97 | 1,255 | 10 | 0.80% | $7.10 | LAL 1% conference attendees |

The **demolayered** ad set (LAL + interest-based targeting) consumes 63% of the campaign budget but has a 12.5% higher CPC than the pure LAL ad set. The **conference attendees** LAL was paused after $71 spend with a $7.10 CPC — reasonable given the small sample, but the low volume suggests this audience is exhausted at scale.

---

## 7. Google Ads Detail

**⚠️ Google Ads API unavailable.** The `google_ads_api.py` wrapper is configured for API v18, which returned HTTP 404 for all endpoints. This likely indicates v18 has been deprecated. Action required: update the wrapper to Google Ads API v19 before the next weekly pull.

No Google Ads data is included in this report.

---

## 8. Recommendations

1. **Update Google Ads API to v19** — The v18 endpoint is returning 404 errors, blocking all Google Ads reporting. Update the `GAQL_URL` in `automations/lib/google_ads_api.py` from `v18` to `v19` and test before next Monday.

2. **Investigate the CPC + CTR divergence** — CPC rose 21% while CTR dropped 28% WoW. This combination indicates the newly active campaigns (or ad sets scaled up) are reaching less engaged audiences at higher cost. Review the ca-us_pms_prospecting demolayered ad set, which has the highest CPC ($5.12) and largest budget share. Consider tightening interest targeting or shifting budget to the pure LAL ad set with lower CPC ($4.55).

3. **Reactivate high-performing paused campaigns selectively** — Meta-Leads-PMS_Conversions-Manual produced 94 lead results and Meta-Leads-Guidebook_Conversions produced 48 lead results before being paused. If budget allows, reactivating these at reduced daily budgets could recover lead volume while controlling the spend surge.

---

## 9. Data Gaps & Notes

- **Google Ads**: API unavailable (HTTP 404 on v18 endpoints). Full Google Ads data missing from this report.
- **Google Sheets**: Authentication credential parsing error prevented updating the tracker sheet. Data saved locally only.
- **Google Docs**: OAuth token refresh failed (missing client ID). Report saved locally only.
- **Results WoW comparison**: The results-summary returned identical data (183 results) for both last_7d and last_14d date presets, making a WoW delta unreliable for the results metric. Used account-level pixel leads (9 vs 27) for directional WoW lead comparison.
- **Prior week derivation**: Prior week (Mar 1–7) was derived by subtracting last_7d from last_14d account-summary metrics.

---

*Report saved locally at `docs/analytics_reports/weekly_ad_performance_2026-03-15.md`*
*Sheets/Docs push failed — see Data Gaps above.*
