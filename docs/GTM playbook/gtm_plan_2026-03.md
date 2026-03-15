# GTM Sprint Plan — March 2026

**Sprint:** Month 2 — Scale Winners, Fix Measurement
**Target Persona:** Property Managers scaling from 5–50 vacation rental units (US/CA primary, BR expansion test)
**Hypothesis:** Social proof-driven creative (testimonials) outperforms feature-based messaging for PMS conversions; Guidebook lead magnets deliver efficient mid-funnel conversions
**Generated:** March 15, 2026

---

## Priorities This Month

### Double Down

1. **PMS Manual Prospecting — Testimonials ad set:** Scale budget. This is the best-performing combination at $79.88 CPA and $3.79 CPC. Test new testimonial creative variations to avoid fatigue.
2. **Guidebook Conversions campaign:** Reactivate and scale. $85.49 CPA with 48 leads shows strong demand for educational lead magnets. Test new guidebook topics (pricing optimization, guest communication).
3. **Content pipeline — high-priority articles:** Ship "How To Start a Newsletter for Local Communities" and "Turn Newsletter Swaps Into Your Best Free Acquisition Channel" (both scored 3.2).

### Fix

1. **Google Ads API integration:** API returning HTTP 404. Verify GOOGLE_ADS_CUSTOMER_ID, refresh token, and endpoint URLs. Cross-platform visibility is critical.
2. **Ahrefs API key:** Configure AHREFS_API_KEY environment variable. Without organic data, we cannot measure content ROI or SEO progress.
3. **Landing page drop-off:** CA-US PMS prospecting shows 21% drop from link click to LPV (423 clicks → 90 LPVs). Audit page load speed, mobile experience, and messaging alignment.
4. **Retargeting audience freshness:** Both PMS and AU-UK retargeting campaigns have elevated CPAs. Refresh audiences, check frequency caps, rotate creative.

### Test

1. **Brazilian market conversion campaign:** Engagement data shows strong interest at $0.51 CPC. Launch a small-budget conversion campaign (R$50/day) targeting Brazilian property managers.
2. **Testimonials creative expansion:** Apply the social proof format from PMS Manual to Guidebook and Industry Report campaigns.
3. **Content-to-lead pipeline:** Use completed blog posts as retargeting content for Meta campaigns. Test blog reader → guidebook download → demo request funnel.

---

## Agent Execution Status

All agents were executed via GTM Commander on March 15, 2026.

| Vertical | Agent | Status |
|----------|-------|--------|
| Content & SEO Pipeline | programmatic_seo_agent.py | Succeeded |
| Content & SEO Pipeline | content_ideation_agent.py | Succeeded |
| Content & SEO Pipeline | traffic_analytics_agent.py | Succeeded |
| Content & SEO Pipeline | search_ranking_agent.py | Succeeded |
| Content & SEO Pipeline | site_performance_agent.py | Succeeded |
| Content & SEO Pipeline | creative_direction_agent.py | Succeeded |
| Paid Acquisition | search_ads_agent.py | Succeeded |
| Paid Acquisition | social_ads_agent.py | Succeeded |
| Paid Acquisition | landing_page_agent.py | Succeeded |
| B2B Outbound | outbound_sequence_agent.py | Skipped (disabled) |
| CRO Intelligence | cro_hypothesis_agent.py | Succeeded |

**B2B Outbound** was disabled for this sprint. The paid acquisition and content/SEO verticals are higher priority given current performance data. Outbound will be re-evaluated when retargeting CPAs improve and content pipeline catches up.

---

## KPI Targets for March 2026

Targets derived from February actuals with improvement targets where underperformance was identified.

| KPI | Feb Actual | March Target | Change |
|-----|-----------|-------------|--------|
| **Total Meta Spend** | $28,365 | $25,000–$30,000 | Rebalance, not necessarily increase |
| **Total Leads (Meta)** | 175 | 220+ | +26% via reallocation to best performers |
| **Blended CPA (Lead)** | $162.09 | <$130 | -20% by shifting spend from underperformers |
| **PMS Manual Leads** | 94 | 120+ | Scale Testimonials ad set |
| **Guidebook Leads** | 48 | 60+ | Reactivate and scale |
| **Content Items Completed** | 3 | 8+ | Clear backlog, ship high-priority items |
| **Content Completion Rate** | 15% | 40%+ | Minimum viable pipeline velocity |
| **Google Ads Data** | Unavailable | Operational | Fix API integration |
| **Ahrefs/SEO Data** | Unavailable | Operational | Configure API key |
| **Retargeting CPA** | $284 | <$200 | Audience refresh + creative rotation |
| **Landing Page View Rate** | 21% (CA-US) | 35%+ | Page speed + UX optimization |

---

## Budget Allocation Recommendation

| Campaign Type | Feb Spend | March Recommendation | Rationale |
|--------------|-----------|---------------------|-----------|
| PMS Manual Prospecting | $7,508 | $10,000 | Best performer — scale |
| Guidebook Conversions | $4,104 | $5,000 | Strong CPA — reactivate and scale |
| PMS Retargeting (all) | $5,170 | $3,000 | Reduce until audiences refreshed |
| Industry Report | $4,977 | $1,500 | Reduce sharply; test new creative |
| CA-US PMS Prospecting | $3,997 | $2,500 | Reduce until LP optimized |
| Engagement (Boosted + pt-br) | $740 | $1,000 | Slight increase for brand building |
| BR Conversion Test | $0 | $1,000 | New test budget |
| **Total** | **$28,365** | **$24,000** | Tighter, more efficient allocation |

---

## Key Dates & Milestones

- **March 15:** Sprint plan published, agents executed
- **March 22:** Google Ads + Ahrefs API fix deadline
- **March 22:** First content sprint review (target: 3 articles shipped)
- **March 29:** Mid-month paid performance check
- **April 1:** Retargeting audience refresh complete
- **April 1:** BR conversion test launch
- **April 14:** End of sprint — next retrospective
