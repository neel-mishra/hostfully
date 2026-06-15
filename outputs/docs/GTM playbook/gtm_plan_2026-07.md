# GTM Sprint Plan — July 2026

**Sprint:** Geo Rebalance & Funnel Optimization  
**Generated:** June 15, 2026  
**Based On:** May 16 – June 14, 2026 performance data  
**Automation:** Monthly GTM Execution Commander (Automation #9)

---

## Priorities This Month

### Double Down
- **Mexico (MX) PMS prospecting**: Best CPL in portfolio at $147.26. Increase daily budget from $250 to $500 and test broader audience expansion.
- **CA-US retargeting**: $94.96 CPL with 7 complete registrations. Grow the retargeting pool by feeding warm audiences from prospecting campaigns.
- **Content production on high-weighted topics**: All completed items scored ≥ 2.6 — maintain prioritization discipline and accelerate production velocity.

### Fix
- **CA-US PMS prospecting funnel**: $625.85 CPL consuming 49% of budget. Audit landing page conversion rate, test new creatives, and tighten audience targeting before spending more.
- **Hostfully pt-br meeting campaign**: $561.06 CPL with low conversion despite high volume (824K impressions). Review landing page localization and test direct lead forms vs. website conversion.
- **Content pipeline velocity**: 40.9% completion rate is below target. Clear "Not Started" backlog or re-scope pipeline to achievable volume.
- **Data integrations**: Google Ads API credentials expired ("Account has been deleted"). Ahrefs API key not configured. Both must be fixed before next monthly run.

### Test
- **EU prospecting scale-up**: Currently at $121/day with only 7 leads. Test 2x budget to give Meta's algorithm enough data to optimize.
- **AU-UK retargeting expansion**: Small audience (6,244 impressions) but $222.92 CPL. Test whether growing the warm audience pool improves efficiency.
- **B2B Outbound re-enable**: Disabled this sprint. Consider re-enabling once landing page and CRO improvements are live to test outbound-driven demo bookings.

---

## Agent Execution Status (June 15, 2026 Run)

| Vertical | Agent | Status | Notes |
|----------|-------|--------|-------|
| Content & SEO Pipeline | programmatic_seo_agent.py | ✅ Success | Generated 2 SEO pages |
| Content & SEO Pipeline | content_ideation_agent.py | ✅ Success | Appended 8 briefs to tracker |
| Content & SEO Pipeline | traffic_analytics_agent.py | ✅ Success | Mock mode (GA4 not configured) |
| Content & SEO Pipeline | search_ranking_agent.py | ✅ Success | Mock mode; 6 striking-distance keywords |
| Content & SEO Pipeline | site_performance_agent.py | ✅ Success | Performance alerts: 87% score (below 90% threshold) |
| Content & SEO Pipeline | creative_direction_agent.py | ✅ Success | Generated visual prompts for 2 content files |
| Paid Acquisition | search_ads_agent.py | ✅ Success | Generated ad copy for 4 keywords |
| Paid Acquisition | social_ads_agent.py | ✅ Success | Generated Meta ad concepts |
| Paid Acquisition | landing_page_agent.py | ✅ Success | Drafted landing page wireframe |
| B2B Outbound | outbound_sequence_agent.py | ⏩ Skipped | Disabled in sprint config |
| CRO Intelligence | cro_hypothesis_agent.py | ❌ Not completed | Commander terminated (timeout) |

**Summary:** 9/10 enabled agents succeeded. 1 agent (cro_hypothesis_agent.py) did not complete due to commander timeout. 1 vertical (B2B Outbound) intentionally disabled.

---

## KPI Targets — July 2026

Derived from June actuals with improvement targets based on identified optimization opportunities.

### Meta Ads

| KPI | June Actual | July Target | Change | Driver |
|-----|-------------|-------------|--------|--------|
| Total Spend | $34,525 | $34,000 | -2% | Hold budget steady while optimizing allocation |
| Total Leads | 102 | 130 | +27% | Shift spend from high-CPL to efficient campaigns |
| Blended CPL | $338.48 | $262 | -23% | Geo rebalance + retargeting growth |
| MX Prospecting Leads | 34 | 55 | +62% | 2x budget increase at current CPL |
| MX Prospecting CPL | $147.26 | $140 | -5% | Algorithmic improvement with more budget |
| CA-US Retargeting Leads | 19 | 25 | +32% | Grow retargeting pool from prospecting |
| CA-US Retargeting CPL | $94.96 | $90 | -5% | Maintain efficiency at slightly higher volume |
| CA-US Prospecting Leads | 27 | 25 | -7% | Reduce budget while testing creative refresh |
| CA-US Prospecting CPL | $625.85 | $400 | -36% | Landing page optimization + new creatives |
| Complete Registrations | 9 | 15 | +67% | CRO improvements on mid-funnel pages |

### Google Ads

| KPI | June Actual | July Target | Notes |
|-----|-------------|-------------|-------|
| All metrics | N/A | TBD | Credentials must be renewed first |

### Content Pipeline

| KPI | June Actual | July Target | Change |
|-----|-------------|-------------|--------|
| Pipeline Completion Rate | 40.9% | 65% | +24pp |
| Completed Items | 9 | 14 | +5 |
| Items In Progress | 0 | 5 | Clear the "Not Started" backlog |

### SEO (Pending Ahrefs Configuration)

| KPI | June Actual | July Target | Notes |
|-----|-------------|-------------|-------|
| Organic Traffic | N/A | TBD | Configure AHREFS_API_KEY |
| Domain Rating | N/A | TBD | Configure AHREFS_API_KEY |
| Ranking Keywords | N/A | TBD | Configure AHREFS_API_KEY |

---

## Budget Reallocation Recommendation

Based on June CPL data, the following budget reallocation is recommended:

| Campaign | Current Daily Budget | Recommended Daily Budget | Change |
|----------|---------------------|-------------------------|--------|
| ca-us_pms_prospecting_website-conv | $750 | $500 | -$250/day |
| mx_pms_prospecting_website-conv | $250 | $500 | +$250/day |
| ca-us_pms_retargeting_website-conv | $85 | $150 | +$65/day |
| eu_pms_prospecting_website-conv | $121 | $200 | +$79/day |
| [Leads] hostfully pt-br — meeting | $320 | $250 | -$70/day |
| au-uk_pms_retargeting_website-conv | $20 | $40 | +$20/day |

**Net budget change:** ~+$44/day (+$1,320/month), within rounding of current spend.

---

## Infrastructure Action Items

| # | Item | Priority | Owner |
|---|------|----------|-------|
| 1 | Renew `GOOGLE_ADS_REFRESH_TOKEN` in Cloud Agent Secrets | 🔴 Critical | Ops |
| 2 | Add `AHREFS_API_KEY` to Cloud Agent Secrets | 🔴 Critical | Ops |
| 3 | Configure `GSC_SITE_URL` for Search Console integration | 🟡 Medium | Ops |
| 4 | Install `google-analytics-data` package for GA4 reporting | 🟡 Medium | Ops |
| 5 | Investigate `cro_hypothesis_agent.py` timeout | 🟢 Low | Dev |
| 6 | Migrate from deprecated `google.generativeai` to `google.genai` | 🟢 Low | Dev |

---

*Generated automatically by GTM Execution Commander. Next run: Monday, June 22, 2026.*
