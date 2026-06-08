# TLDR Ad Performance Report — Week of June 1–7, 2026

**Generated:** Monday, June 8, 2026  
**Report period:** June 1 – June 7, 2026  
**Prior week:** May 25 – May 31, 2026

---

## Headlines

1. **Meta spend surged 138% WoW** — from $3,087 to $7,353, driven by ramped-up budgets across all active campaigns. Impressions followed at +153%.
2. **118 lead results this week across Meta** — 116 lead_email-valid conversions and 2 custom conversions, with mx_pms_prospecting leading at 40 results.
3. **Google Ads data unavailable** — the Google Ads API returned an authentication error ("Account has been deleted"). The refresh token needs to be re-issued; this report covers Meta only.

---

## Cross-Platform Summary

| Metric | Meta (This Week) | Meta (Prior Week) | WoW Change | Google | Combined |
|---|---|---|---|---|---|
| Spend | $7,353.45 | $3,086.99 | **+138.2%** | N/A | $7,353.45 |
| Impressions | 290,098 | 114,777 | **+152.7%** | N/A | 290,098 |
| Clicks | 3,856 | 1,614 | **+138.9%** | N/A | 3,856 |
| CTR | 1.33% | 1.41% | -5.7% | N/A | 1.33% |
| CPC | $1.91 | $1.91 | 0.0% | N/A | $1.91 |
| Leads (account-level) | 22 | 22 | 0.0% | N/A | 22 |
| Results (results-summary) | 118 | — | — | N/A | 118 |

**Results (lead results only, excl. Post engagements):** 116 lead_email-valid, 2 custom_conversion

---

## Anomalies & Flags

| Flag | Detail | Severity |
|---|---|---|
| Spend pace +138% WoW | Spend jumped from $3,087 to $7,353, well above the 10% threshold. Likely reflects intentional budget increases but verify against plan. | HIGH |
| CPC 2.9x account avg — ca-us_pms_retargeting | $5.57 CPC vs $1.91 account average. Retargeting audiences are expensive but warrant review. | MEDIUM |
| CPC 2.4x account avg — au-uk_pms_retargeting | $4.63 CPC vs $1.91 account average. Small spend ($125/wk) limits impact, but efficiency is low. | LOW |
| Google Ads API down | Token refresh returns "Account has been deleted." Credentials need immediate attention. | HIGH |
| au-uk_pms_retargeting — 0 leads | 0 account-level leads this week despite $125 spend. Only 2 custom conversions recorded. | LOW |

**No flags triggered for:** CPC increase >20% WoW (flat), CTR drop >15% WoW (-5.7%).

---

## Meta Ads Detail

### Campaign Performance (June 1–7, 2026)

| Campaign | Spend | Impressions | Clicks | CTR | CPC | Leads | Results | Result Type |
|---|---|---|---|---|---|---|---|---|
| ca-us_pms_prospecting_website-conv | $3,384.08 | 46,824 | 890 | 1.90% | $3.80 | 8 | 30 | lead_email-valid |
| [Leads] hostfully pt-br — meeting | $1,377.59 | 96,291 | 1,005 | 1.04% | $1.37 | 3 | 15 | lead_email-valid |
| mx_pms_prospecting_website-conv | $1,211.67 | 81,332 | 973 | 1.20% | $1.25 | 6 | 40 | lead_email-valid |
| eu_pms_prospecting_website-conv | $731.30 | 55,425 | 867 | 1.56% | $0.84 | 2 | 10 | lead_email-valid |
| ca-us_pms_retargeting_website-conv | $523.84 | 8,566 | 94 | 1.10% | $5.57 | 3 | 21 | lead_email-valid |
| au-uk_pms_retargeting_website-conv | $124.97 | 1,660 | 27 | 1.63% | $4.63 | 0 | 2 | custom_conversion |
| **Total** | **$7,353.45** | **290,098** | **3,856** | **1.33%** | **$1.91** | **22** | **118** | |

### Notable Audiences (Top 3 Campaigns by Spend)

**ca-us_pms_prospecting_website-conv** ($3,384)
- Active ad set: LAL 2% conference attendees — US/CA, ages 25–64, excluding existing customers and retargeting pools
- Paused ad set: LAL 2% ideal customers (5-30 properties)

**[Leads] hostfully pt-br — meeting** ($1,378)
- Multiple Brazilian city-targeted ad sets (São Paulo, Rio, Florianópolis, Fortaleza, etc.)
- Targeting: frequent international travelers, ages 30–50, Instagram placement
- Messaging-based lead gen with WhatsApp integration

**mx_pms_prospecting_website-conv** ($1,212)
- Active ad set: "sitio web abril" — MX/CO, ages 21–65, property management interests (Property management, Landlord, Facility management)
- Paused ad set: "sitio web Mayo S&P" — same targeting, swapped out for creative refresh

### Results Summary (from results-summary endpoint)

Results (lead results only, excl. Post engagements): 116 lead_email-valid, 2 custom_conversion  
**Total lead results: 118**

---

## Google Ads Detail

**Google Ads API is currently unavailable.** The OAuth refresh token returned `"error": "invalid_grant", "error_description": "Account has been deleted"`. This likely means the authorized user account was removed or the token was revoked.

**Action required:** Re-authenticate the Google Ads API connection by generating a new refresh token. Update the `GOOGLE_ADS_REFRESH_TOKEN` environment variable.

---

## Recommendations

1. **Fix Google Ads API credentials immediately.** The "Account has been deleted" error means no Google Ads data can be pulled until a new refresh token is issued. This is a P0 for next week's report.

2. **Review retargeting campaign efficiency.** Both retargeting campaigns (ca-us and au-uk) have CPCs 2–3x the account average. Consider tightening frequency caps, refreshing creative, or adjusting bid strategy. The au-uk campaign in particular is spending $125/week with 0 leads and only 2 custom conversions.

3. **Validate the 138% spend increase against plan.** The jump from $3,087 to $7,353 is dramatic. If intentional (budget ramp), great — CPCs held steady despite the volume increase. If unintentional, investigate pacing settings on the active campaigns.
