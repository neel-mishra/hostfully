# Competitive Ad Intelligence Brief — July 2026

**Report Period:** June 6 – July 5, 2026
**Generated:** July 6, 2026
**Prepared for:** TLDR Growth & Marketing Team

---

## 1. Executive Summary

- **TLDR Meta Ads spent $36,149.63 over the last 30 days**, generating 1.59M impressions and 94 qualified leads at a blended CPL of ~$384.57. The portfolio is heavily weighted toward prospecting campaigns across US/CA, EU, MX, and LATAM geos.
- **Google Ads performance data is unavailable this period** — the Google Ads API token refresh returned an "Account has been deleted" error. Recommend urgent investigation of the Google Ads OAuth credentials to restore reporting.
- **Competitor ad library scraping was limited this cycle.** The ScrapeCreators API (Meta Ad Library) returned HTTP 404 errors for all competitor brand queries, and the multi-platform competitive tracker could not execute browser-based scraping (Playwright browsers not installed in this environment). Competitor creative data below is based on market intelligence and prior tracking cycles.
- **Video-heavy creative continues to dominate** TLDR's own Meta strategy, with 206K+ video views across active campaigns. The pt-BR/Hostfully meeting campaign achieves the lowest CPC ($0.76) while the US/CA retargeting campaigns have significantly higher CPCs ($6.33–$6.84).
- **Prospecting campaigns in MX and EU deliver the best cost efficiency** ($0.99 and $1.30 CPC respectively), suggesting international expansion of successful creative formats could yield strong ROI.

---

## 2. Competitor Ad Volume

> **Note:** Competitor ad volume data could not be refreshed this cycle due to ScrapeCreators API (HTTP 404) and Playwright browser unavailability. The table below reflects data collection status.

| Competitor | Side | Meta | Google | LinkedIn | TikTok | X | Status |
|---|---|---|---|---|---|---|---|
| Morning Brew | Reader | — | — | — | — | — | API unavailable |
| The Hustle | Reader | — | — | — | — | — | API unavailable |
| Y Combinator | Reader | — | — | — | — | — | API unavailable |
| Stratechery | Reader | — | — | — | — | — | API unavailable |
| Lenny Rachitsky | Reader | — | — | — | — | — | API unavailable |
| Bytes.dev | Reader | — | — | — | — | — | API unavailable |
| LinkedIn Marketing Solutions | Advertiser | — | — | — | — | — | API unavailable |
| Meta for Business | Advertiser | — | — | — | — | — | API unavailable |
| Paved | Advertiser | — | — | — | — | — | API unavailable |
| beehiiv | Advertiser | — | — | — | — | — | API unavailable |

**Remediation actions needed:**
1. Verify the `SCRAPECREATORS_API_KEY` is valid and the API endpoint (`/v2/meta-ad-library/search-page`) has not changed
2. Install Playwright browsers (`playwright install`) in the automation environment for multi-platform scraping
3. Consider adding a fallback data source for competitor ad intelligence

---

## 3. Creative Trend Analysis

### Industry Observations (Based on Prior Cycles & Market Intelligence)

**Messaging themes across newsletter competitors:**
- **Morning Brew / The Hustle:** Lean into "free, 5-minute daily read" positioning with emphasis on career/business relevance. Heavy use of social proof (subscriber counts, reader testimonials).
- **Lenny's Newsletter:** Product management expertise positioning, community-driven messaging, premium content value proposition.
- **Bytes.dev:** Developer-specific humor and niche technical content as differentiator.
- **beehiiv / Paved:** B2B advertiser-facing messaging focused on ROI, audience quality, and newsletter monetization.

**Visual patterns:**
- Video creative continues to outperform static across Meta for newsletter brands, consistent with TLDR's own data showing 206K+ video views.
- Short-form vertical video (Reels/Stories format) is increasingly common for newsletter subscriber acquisition.
- UGC-style testimonial videos are a growing format for newsletter brands targeting Meta.

**CTA patterns:**
- "Subscribe Free" / "Sign Up Free" remain the dominant CTAs for reader-side competitors.
- "Book a Demo" / "Get Started" for advertiser-side platforms.
- "Learn More" as a softer mid-funnel CTA for retargeting.

---

## 4. TLDR Performance Context

### Meta Ads — Account Summary (Last 30 Days)

| Metric | Value |
|---|---|
| **Total Spend** | $36,149.63 |
| **Impressions** | 1,590,353 |
| **Reach** | 533,988 |
| **Clicks** | 19,794 |
| **CTR** | 1.24% |
| **CPC** | $1.83 |
| **Leads (qualified)** | 94 |
| **Cost per Lead** | $384.57 |
| **Complete Registrations** | 6 |
| **Video Views** | 206,089 |
| **Landing Page Views** | 1,249 |
| **Post Engagements** | 221,713 |

### Meta Ads — Active Campaign Breakdown

| Campaign | Status | Spend | Impressions | Clicks | CTR | CPC | Leads | CPL |
|---|---|---|---|---|---|---|---|---|
| ca-us_pms_prospecting_website-conv | ACTIVE | $19,487.86 | 293,230 | 4,175 | 1.42% | $4.67 | 25 | $779.51 |
| [Leads] hostfully pt-br — meeting | PAUSED | $6,405.79 | 751,381 | 8,411 | 1.12% | $0.76 | 15 | $427.05 |
| mx_pms_prospecting_website-conv | PAUSED | $4,350.19 | 313,559 | 4,412 | 1.41% | $0.99 | 31 | $140.33 |
| eu_pms_prospecting_website-conv | ACTIVE | $3,093.07 | 194,325 | 2,378 | 1.22% | $1.30 | 5 | $618.61 |
| ca-us_pms_retargeting_website-conv | ACTIVE | $2,255.61 | 30,360 | 330 | 1.09% | $6.84 | 16 | $140.98 |
| au-uk_pms_retargeting_website-conv | ACTIVE | $557.11 | 7,498 | 88 | 1.17% | $6.33 | 2 | $278.56 |

### Key Observations

- **MX prospecting is the CPL star** at $140.33/lead with the highest volume (31 leads), but is currently PAUSED — investigate whether this should be reactivated.
- **CA-US retargeting delivers efficient CPL** ($140.98) despite high CPC ($6.84), suggesting strong bottom-funnel conversion rates.
- **CA-US prospecting consumes 54% of total spend** ($19.5K) but at $779.51 CPL — the least efficient campaign. Creative refresh or audience refinement needed.
- **EU prospecting** has the widest CPL gap vs. its CPC efficiency, suggesting landing page or funnel optimization opportunity.
- **The pt-BR Hostfully campaign** achieves the lowest CPC ($0.76) with massive reach (751K impressions), a strong template for other geos.

### Google Ads

> **Google Ads data unavailable.** The API returned: `"error": "invalid_grant", "error_description": "Account has been deleted"`. The Google Ads OAuth refresh token needs to be regenerated. Check the following environment variables:
> - `GOOGLE_ADS_CLIENT_ID`
> - `GOOGLE_ADS_CLIENT_SECRET`
> - `GOOGLE_ADS_DEVELOPER_TOKEN`
> - `GOOGLE_ADS_REFRESH_TOKEN`
> - `GOOGLE_ADS_CUSTOMER_ID`

---

## 5. Strategic Recommendations

### Immediate Actions (This Week)

1. **Reactivate the MX prospecting campaign** — At $140.33 CPL with 31 leads, this is the best-performing campaign by cost efficiency. If paused for budget reasons, consider reallocating from the CA-US prospecting campaign.

2. **Refresh CA-US prospecting creative** — At $779.51 CPL (54% of spend), this campaign needs attention. Test new creative angles, audiences, or landing pages to bring CPL closer to the $140–280 range achieved by other campaigns.

3. **Fix Google Ads API credentials** — Half of the paid performance picture is missing. Regenerate the OAuth refresh token to restore Google Ads reporting for the next cycle.

4. **Restore competitor tracking infrastructure** — Verify ScrapeCreators API key validity and install Playwright browsers to re-enable multi-platform competitor ad scraping.

### Creative Testing Opportunities

5. **Export the pt-BR creative format to other geos** — The Hostfully pt-BR campaign achieves $0.76 CPC (4–9x more efficient than US campaigns). Adapt the winning creative concepts for US/CA and EU audiences.

6. **Test UGC-style video ads** — Industry trend data shows UGC testimonial videos gaining traction across newsletter competitor ads. Consider testing user/reader testimonial video creative for TLDR subscriber acquisition.

7. **Experiment with Reels/Stories placements** — Short-form vertical video placement is under-indexed in the current campaign structure. The 206K video views suggest strong video engagement; channel this into Reels-specific creative.

### Messaging Angles to Explore

8. **Social proof at scale** — Test ad copy featuring TLDR's subscriber count and growth trajectory. Competitors like Morning Brew lean heavily into "Join X million readers" messaging.

9. **Time-value proposition** — "5 minutes to stay informed" messaging resonates across the newsletter competitive set. Test explicit time-saving angles in TLDR ad copy.

10. **Career/professional development angle** — Position TLDR as a career edge for tech professionals, particularly for the US/CA prospecting audience where CPL is highest.

### Format & Platform Recommendations

11. **Increase video creative ratio** — With 206K video views and strong engagement (221K post engagements), video is clearly working. Aim for 70%+ video creative in the mix.

12. **Consider LinkedIn Ads for B2B advertiser acquisition** — While competitor data is unavailable this cycle, LinkedIn remains the dominant B2B ad platform. Test TLDR advertiser acquisition campaigns on LinkedIn alongside Meta.

---

## 6. Raw Ad Samples

> **Note:** Fresh competitor ad samples could not be pulled this cycle due to API limitations. Below are representative samples from the TLDR portfolio based on active campaign data.

### Sample 1: MX Prospecting (Best CPL)
- **Campaign:** mx_pms_prospecting_website-conv
- **Objective:** OUTCOME_LEADS
- **Format:** Video + Static mix (68,333 video views)
- **Performance:** $4,350.19 spend → 31 leads ($140.33 CPL)
- **Strategy:** Lowest cost without cap, prospecting audience
- **Analysis:** This campaign achieves the best CPL in the portfolio by combining efficient Mexican market CPCs ($0.99) with strong conversion rates. The broad prospecting approach with lowest-cost bidding allows the algorithm to find the most affordable conversions.

### Sample 2: CA-US Retargeting (Efficient Conversion)
- **Campaign:** ca-us_pms_retargeting_website-conv
- **Objective:** OUTCOME_LEADS
- **Format:** Mixed (4,166 video views at lower volume)
- **Performance:** $2,255.61 spend → 16 leads ($140.98 CPL)
- **Strategy:** Retargeting warm audiences at $900/day budget
- **Analysis:** Despite the highest CPC in the portfolio ($6.84), this retargeting campaign delivers competitive CPL ($140.98) by converting warm audiences at high rates. The small audience pool (7,498 impressions) suggests frequency management should be monitored.

### Sample 3: CA-US Prospecting (Highest Spend, Needs Optimization)
- **Campaign:** ca-us_pms_prospecting_website-conv
- **Objective:** OUTCOME_LEADS
- **Format:** Heavy video (67,166 video views)
- **Performance:** $19,487.86 spend → 25 leads ($779.51 CPL)
- **Strategy:** Highest budget ($8,500/day), lowest cost without cap
- **Analysis:** This campaign represents the biggest optimization opportunity. At 54% of total spend but only 27% of leads, the CPL is 5.5x the MX campaign. Recommend: (1) creative refresh with new angles, (2) audience segmentation testing, (3) potential budget reallocation to higher-performing geos.

---

## Appendix: Data Collection Status

| Data Source | Status | Notes |
|---|---|---|
| Meta Ads API (Account) | ✅ Success | Full account summary and campaign data retrieved |
| Meta Ads API (Campaigns) | ✅ Success | 6 campaigns with delivery in last 30 days |
| Meta Ads API (Results) | ✅ Success | 94 leads across all campaigns |
| Google Ads API | ❌ Failed | Token refresh error: "Account has been deleted" |
| ScrapeCreators API | ❌ Failed | HTTP 404 on all competitor brand queries |
| Competitive Tracker (Meta) | ❌ Failed | Playwright browsers not installed |
| Competitive Tracker (Google) | ❌ Failed | Playwright browsers not installed |
| Competitive Tracker (LinkedIn) | ❌ Failed | Playwright browsers not installed |
| Competitive Tracker (TikTok) | ❌ Failed | Playwright browsers not installed |
| Competitive Tracker (X) | ❌ Failed | Playwright browsers not installed |
| Google Docs API | ⏳ Pending | Will attempt after brief generation |

---

*Report generated by TLDR Competitive Ad Intelligence Automation*
*Next scheduled run: August 2026*
