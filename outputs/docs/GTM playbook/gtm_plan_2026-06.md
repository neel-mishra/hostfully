# GTM Sprint Plan - June 2026

**Sprint Name:** June 2026 - Geo Arbitrage & Funnel Optimization
**Generated:** June 8, 2026
**Prepared by:** GTM Execution Commander (Automation 9)

---

## Priorities This Month

### Double Down
1. **LATAM prospecting (MX/CO/BR)** — Mexico campaign delivered $115.82 CPL vs $568.31 in US/CA. Increase daily budget allocation for `mx_pms_prospecting_website-conv` and test expansion into additional LATAM geos (Chile, Peru, Argentina).
2. **CA-US retargeting** — $80.53 CPL. Maintain and grow retargeting pools by feeding more top-of-funnel traffic through video and engagement campaigns.
3. **High-score content execution** — All completed items scored 3.2+. Continue prioritizing high-impact content in the pipeline.

### Fix
1. **Google Ads credentials** — Re-authenticate OAuth tokens for the Google Ads API. The current `GOOGLE_ADS_REFRESH_TOKEN` returns "Account has been deleted." Search ads are a critical channel for capturing intent-based property management queries.
2. **AU-UK retargeting** — Pause immediately. $425 spent with zero leads. Rebuild the audience pool through prospecting before resuming retargeting.
3. **Hostfully pt-br campaign objective** — Pivot from meeting-focused to website-conversion optimization to match the structure that works in MX. Current $458.46 CPL is unsustainable.
4. **Ahrefs API integration** — Add `AHREFS_API_KEY` to Cloud Agent secrets to restore SEO tracking capability.

### Test
1. **Budget rebalance: shift 20% of US/CA prospecting budget to MX/CO/BR** — Test whether MX lead quality matches US/CA at 5x better CPL.
2. **Video-first creative in EU campaign** — EU CTR (1.40%) is solid but CPL ($307.21) has room to improve. Test video creatives that drove 48K views in the current MX campaign.
3. **Content-to-lead funnel** — Completed articles (55% open rates, newsletter swaps) should be gated for lead capture. Cross-reference with landing page CRO.
4. **LATAM landing page localization** — MX campaign sends to English landing pages. Test Spanish/Portuguese variants for improved conversion rates.

---

## Agent Execution Status

All agents ran successfully on June 8, 2026.

| Vertical | Agent | Status | Notes |
|----------|-------|--------|-------|
| Content & SEO Pipeline | programmatic_seo_agent.py | Success | |
| Content & SEO Pipeline | content_ideation_agent.py | Success | |
| Content & SEO Pipeline | traffic_analytics_agent.py | Success | |
| Content & SEO Pipeline | search_ranking_agent.py | Success | |
| Content & SEO Pipeline | site_performance_agent.py | Success | |
| Content & SEO Pipeline | creative_direction_agent.py | Success | |
| Paid Acquisition | search_ads_agent.py | Success | Google Ads credentials need re-auth for live execution |
| Paid Acquisition | social_ads_agent.py | Success | |
| Paid Acquisition | landing_page_agent.py | Success | |
| B2B Outbound | outbound_sequence_agent.py | Success | |
| CRO Intelligence | cro_hypothesis_agent.py | Success | |

**Summary:** 11/11 agents executed (100% success rate). 4/4 verticals active.

---

## KPI Targets - June 2026

Derived from May actuals with geo-rebalance assumptions.

| KPI | May Actual | June Target | Delta | Rationale |
|-----|-----------|-------------|-------|-----------|
| **Meta Ads Spend** | $33,737 | $33,000 | -2% | Hold flat while rebalancing geo mix |
| **Total Leads** | 116 | 155 | +34% | Shift budget to lower-CPL geos should increase lead volume |
| **Blended CPL** | $290.84 | $215.00 | -26% | Geo arbitrage from MX/CO + retargeting efficiency |
| **MX/CO Leads** | 40 | 60 | +50% | Increased budget allocation |
| **US/CA Prospecting CPL** | $568.31 | $450.00 | -21% | Creative refresh and audience optimization |
| **US/CA Retargeting CPL** | $80.53 | $75.00 | -7% | Maintain efficiency with growing pool |
| **Content Items Published** | 10 | 14 | +40% | Clear 4 mid-tier backlog items |
| **Content Pipeline Completion** | 48% | 67% | +19pp | Target 14/21 items completed |
| **Google Ads** | Offline | Reactivated | — | Re-auth credentials by Week 1 |
| **Ahrefs SEO Tracking** | Offline | Active | — | Add API key by Week 1 |

### Monthly Budget Allocation (Recommended)

| Geo/Campaign Type | May Allocation | June Recommended | Change |
|-------------------|---------------|-----------------|--------|
| CA-US Prospecting | $17,039 (50.5%) | $12,000 (36.4%) | -$5,039 |
| MX/CO Prospecting | $4,633 (13.7%) | $8,000 (24.2%) | +$3,367 |
| Hostfully pt-br | $6,877 (20.4%) | $5,500 (16.7%) | -$1,377 |
| EU Prospecting | $3,072 (9.1%) | $3,500 (10.6%) | +$428 |
| CA-US Retargeting | $1,691 (5.0%) | $3,500 (10.6%) | +$1,809 |
| AU-UK Retargeting | $425 (1.3%) | $0 (0%) | Paused |
| Google Ads (TBD) | $0 | $500 (1.5%) | Pilot |
| **Total** | **$33,737** | **$33,000** | **-$737** |

---

## Data Gaps & Required Actions

| Issue | Owner Action | Priority |
|-------|-------------|----------|
| Google Ads OAuth token invalid | Re-authenticate `GOOGLE_ADS_REFRESH_TOKEN` in Cursor Secrets | P0 |
| Ahrefs API key missing | Add `AHREFS_API_KEY` to Cursor Secrets | P1 |
| `GOOGLE_CLIENT_ID` missing | Add to Cursor Secrets for Google Docs push | P2 |
| AU-UK retargeting burning budget | Pause in Meta Ads Manager | P1 |
| Hostfully pt-br campaign objective | Switch from meeting to website-conv | P1 |

---

*Generated automatically by GTM Execution Commander. Next run: Monday, June 15, 2026.*
