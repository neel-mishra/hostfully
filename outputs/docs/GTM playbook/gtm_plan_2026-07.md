# GTM Sprint Plan — July 2026

**Sprint:** Month 4 - Scale Efficient Channels & Fix Visibility Gaps  
**Generated:** June 22, 2026  
**Target Persona:** Property Manager scaling from 5-30 units (MX, CA-US retargeting)

---

## Priorities This Month

### Double Down
1. **Mexico Prospecting** — Increase daily budget from $250 to $400. Best CPL among prospecting ($140.41) with strong volume. Test expanded interest audiences in MX market.
2. **CA-US + AU-UK Retargeting** — Increase retargeting budget allocation. CA-US retargeting at $106.76 CPL is 5x more efficient than CA-US prospecting. Scale retargeting audiences with fresh creative.
3. **Content Pipeline Velocity** — Push to complete 5+ additional articles from backlog, prioritizing Milk Road deep dive and Gmail Promotions strategies.

### Fix
1. **Google Ads Credential Refresh** — Token refresh failing ("Account has been deleted" error). Regenerate OAuth refresh token and validate access.
2. **Ahrefs API Key Configuration** — Add `AHREFS_API_KEY` to Cloud Agent secrets to restore SEO visibility.
3. **CA-US Prospecting Restructure** — $17K spend at $532 CPL is unsustainable. Test new lookalike seeds (webinar registrants, guidebook downloaders) or pause and reallocate to retargeting.

### Test
1. **Advantage+ Audiences (CA-US)** — Meta's AI-driven targeting may find efficient pockets without manual LAL constraints.
2. **EU Market Messaging Variants** — Current EU campaign shows high impressions but low conversion. Test localized messaging per country (UK vs DE vs FR).
3. **Video-to-Lead Attribution** — With 204K video views, implement view-through conversion tracking to understand video's true contribution to pipeline.

---

## Agent Execution Status

| Vertical | Agent | Status | Notes |
|----------|-------|--------|-------|
| Content & SEO Pipeline | programmatic_seo_agent.py | Succeeded | — |
| Content & SEO Pipeline | content_ideation_agent.py | Succeeded | — |
| Content & SEO Pipeline | traffic_analytics_agent.py | Succeeded | — |
| Content & SEO Pipeline | search_ranking_agent.py | Succeeded | — |
| Content & SEO Pipeline | site_performance_agent.py | Succeeded | — |
| Content & SEO Pipeline | creative_direction_agent.py | Succeeded | — |
| Paid Acquisition | search_ads_agent.py | Succeeded | — |
| Paid Acquisition | social_ads_agent.py | Succeeded | — |
| Paid Acquisition | landing_page_agent.py | Succeeded | — |
| B2B Outbound | outbound_sequence_agent.py | Skipped | Disabled — refocusing on paid + content |
| CRO Intelligence | cro_hypothesis_agent.py | Succeeded | — |

**Summary:** 10/10 enabled agents succeeded. B2B Outbound paused to concentrate resources on higher-performing channels.

---

## KPI Targets — July 2026

Derived from June actuals with channel-mix optimization applied.

| Metric | June Actual | July Target | Change |
|--------|-------------|-------------|--------|
| Meta Spend | $34,627 | $32,000 | -8% (reallocate from CA-US prospecting) |
| Total Leads | 115 | 145 | +26% (retargeting + MX scale) |
| Blended CPL | $301.10 | <$225 | -25% target |
| MX Leads | 36 | 50 | +39% |
| Retargeting Leads | 20 | 35 | +75% |
| Content Published | 9 | 14 | +56% (clear backlog) |
| Video Views | 204K | 220K | +8% |

### Channel Budget Allocation (Proposed)

| Channel | June Spend | July Proposed | Rationale |
|---------|-----------|---------------|-----------|
| CA-US Prospecting | $17,036 | $10,000 | Reduce; test new audiences |
| CA-US Retargeting | $1,922 | $5,000 | Scale 2.5x; best CPL |
| MX Prospecting | $5,055 | $8,000 | Scale 1.6x; efficient market |
| EU Prospecting | $2,973 | $2,000 | Reduce; test new messaging |
| AU-UK Retargeting | $469 | $1,500 | Scale 3x; promising CPL |
| pt-br Meeting | $7,173 | $5,500 | Maintain; watch CPL |
| **Total** | **$34,627** | **$32,000** | — |

---

## Data Gaps to Resolve

| Gap | Impact | Action | Owner |
|-----|--------|--------|-------|
| Google Ads unavailable | Cannot assess search performance or cross-channel attribution | Regenerate OAuth tokens | Marketing Ops |
| Ahrefs unavailable | No SEO visibility — can't correlate content to organic traffic | Add AHREFS_API_KEY to secrets | Marketing Ops |
| Video attribution unclear | 204K views but lead path unknown | Implement view-through conversion window | Paid Media |
| MoM comparison unavailable | First full data pull — no baseline for trend analysis | This month's data becomes baseline | Auto (next run) |
