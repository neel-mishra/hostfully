# GTM Sprint Plan — March 2026 <!-- pragma: allowlist secret -->
**Sprint:** CPL Recovery & Creative Refresh
**Target Persona:** Property Managers & Vacation Rental Operators (US/CA primary, LATAM expansion)
**Hypothesis:** Lead-form campaigns with fresh testimonial creative will recover CPL below $120, reversing February's creative-fatigue-driven regression
**Generated:** 2026-03-16

---

## Priorities This Month

### Double Down
1. **Meta-Leads-PMS_Conversions-Manual** — Reactivate immediately. $78.81 CPA in Feb, best-performing campaign. Target 120+ leads at sub-$80 CPA.
2. **Meta-Leads-Guidebook_Conversions** — Reactivate. $92.05 CPA with 44 leads. Test 2-3 new guidebook creative angles.
3. **Google Ads Brand (Hostfully - Search - Brand)** — Maintain. 97.72% impression share, $201.95 CPL. Fix PAUSED status anomaly.
4. **Content pipeline acceleration** — Ship 4+ articles targeting weighted score >= 3.2 items.

### Fix
1. **ca-us_pms_prospecting_website-conv** — Burning $5.1K for 7 leads ($735 CPA). Pause and restructure with new creative and tighter targeting before re-launch.
2. **au-uk_pms_prospecting_website-conv** — $1.7K spend, zero leads. Either pause or overhaul audience/creative.
3. **Creative fatigue** — CTR declined 26% WoW. Launch 3-5 new ad creative variants: testimonial-based, video, UGC-style.
4. **Site performance** — 87% Lighthouse score needs to hit 90%. Prioritize LCP optimization.
5. **Google Ads API access** — Resolve 404 errors. Likely auth or endpoint configuration issue.
6. **Ahrefs API key** — Configure AHREFS_API_KEY environment variable for organic keyword tracking.

### Test
1. **LATAM expansion (Brazil pt-br)** — $1.47 CPC is 3x cheaper than US/CA. Scale from $527/mo to $1,500/mo and measure meeting-booked rate.
2. **Dedicated landing pages** — A/B test campaign-specific LPs for guidebook and PMS conversion funnels vs. generic hostfully.com.
3. **Non-brand Google Ads** — Reactivate paused non-brand campaigns with new ad copy targeting "property management software" and "vacation rental management" terms.
4. **Striking distance SEO content** — Target 6 keywords at positions 11-20 with on-page optimization (FAQ, H1 refresh, internal links).

---

## Agent Execution Status (March 16 Run)

| Agent | Vertical | Status | Notes |
|-------|----------|--------|-------|
| programmatic_seo_agent.py | Content & SEO Pipeline | SUCCESS | Completed in ~55s |
| content_ideation_agent.py | Content & SEO Pipeline | SUCCESS | Completed in ~15s |
| traffic_analytics_agent.py | Content & SEO Pipeline | SUCCESS | Completed in <1s |
| search_ranking_agent.py | Content & SEO Pipeline | SUCCESS | Completed in <1s |
| site_performance_agent.py | Content & SEO Pipeline | SUCCESS | Completed in ~3s |
| creative_direction_agent.py | Content & SEO Pipeline | TIMEOUT | Exceeded 60s limit — likely waiting on external API |
| search_ads_agent.py | Paid Acquisition | SUCCESS | Completed in ~18s |
| social_ads_agent.py | Paid Acquisition | TIMEOUT | Exceeded 60s limit — Meta API latency |
| landing_page_agent.py | Paid Acquisition | SUCCESS | Completed in ~21s |
| outbound_sequence_agent.py | B2B Outbound | TIMEOUT | Exceeded 60s limit — likely external dependency |
| cro_hypothesis_agent.py | CRO Intelligence | SUCCESS | Completed in ~32s |

**Result:** 8/11 agents succeeded (72.7%). 3 timeouts on agents with external API dependencies.

---

## KPI Targets — March 2026

Derived from February actuals and strategic adjustments.

| KPI | Feb Actual | March Target | Change |
|-----|-----------|--------------|--------|
| **Meta Ads Spend** | $29,290 | $28,000 | −4.4% (shift to efficient campaigns) |
| **Meta Ads Leads** | 166 | 220 | +32.5% (reactivate top campaigns) |
| **Meta Blended CPL** | $176.44 | <$130 | −26% (recover toward Jan levels) |
| **Google Ads Spend** | ~$8,700/mo est. | $8,000 | Maintain |
| **Google Ads Leads** | ~28/mo est. | 35 | +25% (reactivate non-brand) |
| **Google Blended CPL** | $310.40 | <$250 | −19% |
| **Content Published** | 3 | 6 | +100% |
| **Pipeline Completion Rate** | 15% | 35% | +20pp |
| **Site Performance Score** | 87% | 90%+ | +3pp |
| **Weekly Sessions** | 7,830 | 8,500 | +8.5% |
| **Conversion Rate** | 3.22% | 3.5% | +0.28pp |

---

## Weekly Checkpoint Schedule

| Week | Focus | Deliverable |
|------|-------|-------------|
| Mar 16–22 | Campaign reactivation + creative refresh kick-off | New creative briefs, PMS Manual + Guidebook back online |
| Mar 23–29 | LATAM scale test + non-brand Google Ads launch | pt-br at $1.5K budget, 2 new Google campaigns live |
| Mar 30 – Apr 5 | SEO sprint + landing page A/B tests | 3 striking-distance pages optimized, 2 LP variants live |
| Apr 6–12 | Month-end review + April sprint prep | Performance check, creative fatigue audit |

---

## API & Data Pipeline Fixes Required

| Issue | Impact | Owner | Priority |
|-------|--------|-------|----------|
| Google Ads API 404 | Cannot pull monthly campaign data programmatically | Engineering/Ops | Critical |
| AHREFS_API_KEY not set | No organic keyword tracking, domain rating, or backlink data | Engineering/Ops | High |
| creative_direction_agent.py timeout | Creative analysis not completing | Agent Dev | Medium |
| social_ads_agent.py timeout | Social ads analysis blocked by API latency | Agent Dev | Medium |
| outbound_sequence_agent.py timeout | Outbound execution not completing | Agent Dev | Medium |

---

*Next retrospective scheduled: April 13, 2026 (first Monday after month end)*
