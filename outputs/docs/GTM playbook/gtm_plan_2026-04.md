# GTM Sprint Plan — April 2026

**Sprint Name:** Retargeting Scale & Infrastructure Fix
**Period:** April 1 – April 30, 2026
**Generated:** April 6, 2026
**Based on:** March 2026 Retrospective Data

---

## Priorities This Month

### Double Down
1. **CA-US Retargeting** — Increase daily budget from $50/day to $100/day. CPA of $88.79 is well below the account average of $268.71. Expand retargeting audiences to include video viewers (75%+) and page engagers.
2. **Brazil (pt-br) Meeting Campaigns** — $112.28 CPA for meeting-qualified leads. Test new creative angles and expand targeting to similar LatAm markets (Mexico, Colombia).
3. **Content Pipeline Execution** — Prioritize the 12 remaining items by weighted score. Target 80%+ completion rate (vs 43% in March).
4. **Conference Attendee LAL** — Scale the conference attendee lookalike ad set. At $4,081 spend, it's underinvested relative to its differentiated audience source.

### Fix
1. **Google Ads API** — The API returned HTTP 404 on all calls. Likely causes: incorrect Customer ID format, wrong API version (v18), or expired credentials. Fix and verify by April 10.
2. **Ahrefs API Key** — Missing `AHREFS_API_KEY` env variable. Add to Cursor Dashboard secrets. Without this, zero organic/SEO measurement is possible.
3. **Agent Timeouts** — The `social_ads_agent.py` timed out and blocked downstream agents. Implement per-agent timeout (120s) in GTM Commander with graceful failure handling.
4. **GA4/GSC Credentials** — Traffic analytics and search ranking agents ran in mock mode. Configure `GA4_PROPERTY_ID` and `GSC_SITE_URL` for real data.

### Test
1. **AU-UK Prospecting Creative Refresh** — $1,008/lead is not viable. Before cutting budget, test 3 new creative variants (video testimonial, product demo, social proof). If CPA doesn't drop below $400 by mid-month, pause and reallocate.
2. **Post Engagement → Retargeting Funnel** — The pt-br engagement campaign generates 33K+ post engagements. Test whether building a retargeting audience from these engagers improves downstream conversion rates.
3. **Programmatic SEO Page Performance** — The SEO agent generated comparison and integration pages. Monitor indexing and early ranking signals (if Ahrefs is restored).

---

## Agent Execution Status

| Vertical | Agent | March Status | April Plan |
|---|---|---|---|
| Content & SEO | programmatic_seo_agent.py | Success | Enabled — run with new entity list |
| Content & SEO | content_ideation_agent.py | Success | Enabled — source from top competitors |
| Content & SEO | traffic_analytics_agent.py | Mock mode | Enabled — fix GA4 credentials |
| Content & SEO | search_ranking_agent.py | Mock mode | Enabled — fix GSC credentials |
| Content & SEO | site_performance_agent.py | Mock mode | Enabled — keep as canary |
| Content & SEO | creative_direction_agent.py | Success | Enabled |
| Paid Acquisition | search_ads_agent.py | Success | Enabled |
| Paid Acquisition | social_ads_agent.py | Timed out | Enabled — add timeout guard |
| Paid Acquisition | landing_page_agent.py | Not reached | Enabled — ensure execution |
| B2B Outbound | outbound_sequence_agent.py | Not reached | Disabled — focus resources on paid + content |
| CRO Intelligence | cro_hypothesis_agent.py | Not reached | Enabled — run with site performance data |

---

## KPI Targets — April 2026

Targets derived from March actuals with adjustments for planned optimizations.

| KPI | March Actual | April Target | Change |
|---|---|---|---|
| Meta Ads Spend | $33,320 | $30,000 | -10% (reallocate from AU-UK prospecting) |
| Total Leads (Meta) | 124 | 160 | +29% (retargeting scale + creative refresh) |
| Blended CPA (Lead) | $268.71 | $187.50 | -30% (retargeting mix shift) |
| CA-US Retargeting Leads | 23 | 40 | +74% (2x budget) |
| CA-US Retargeting CPA | $88.79 | <$100 | Maintain efficiency at higher spend |
| AU-UK Prospecting CPA | $1,008.54 | <$400 | Creative refresh or pause by mid-month |
| BR Meeting Leads | 12 | 20 | +67% (expand creative testing) |
| Content Items Completed | 9/21 (43%) | 17/21 (81%) | Focus on high-weighted-score items |
| Agent Success Rate | 7/11 (64%) | 10/11 (91%) | Fix timeouts and credentials |
| Google Ads Visibility | 0% | 100% | Fix API configuration |
| Ahrefs/SEO Visibility | 0% | 100% | Add API key |

---

## Budget Allocation — April 2026

| Campaign | March Spend | April Budget | Rationale |
|---|---|---|---|
| ca-us_pms_prospecting | $22,767 | $18,000 | Slight reduction; shift to retargeting |
| ca-us_pms_retargeting | $2,042 | $4,000 | 2x increase — best CPA in portfolio |
| au-uk_pms_prospecting | $6,051 | $3,000 | Cut 50% — test creative first, pause if no improvement |
| au-uk_pms_retargeting | $913 | $1,500 | Moderate increase — good efficiency |
| [Leads] hostfully pt-br | $1,347 | $2,500 | Scale — strong meeting lead CPA |
| [Post Promovido] pt-br | $199 | $200 | Maintain — evaluate retargeting pool impact |
| Google Ads | — | TBD | Pending API fix — budget to be determined once data visible |
| **Total Meta** | **$33,320** | **$29,200** | Tighter, more efficient allocation |

---

## Sprint Milestones

| Date | Milestone |
|---|---|
| Apr 7 | Sprint kickoff: budget reallocations go live |
| Apr 10 | Google Ads API + Ahrefs API keys configured and verified |
| Apr 10 | AU-UK creative refresh variants launched |
| Apr 14 | Mid-sprint check: AU-UK CPA evaluation (pause if >$400) |
| Apr 14 | GA4/GSC credentials configured for real-data agent runs |
| Apr 21 | Content pipeline check: 13+ items should be completed |
| Apr 28 | Pre-retro data pull: all platforms operational |
| May 5 | May retrospective generated with full cross-platform data |

---

## Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| Google Ads API remains broken | No search ads visibility; can't optimize SEM spend | Escalate to engineering; manual dashboard pull as fallback |
| Ahrefs key not added | Zero organic measurement for second consecutive month | Document in Cursor Dashboard; create setup checklist |
| AU-UK creative refresh doesn't improve CPA | $3K wasted at >$1K/lead | Hard pause trigger at Apr 14 if CPA >$400 |
| Retargeting audience exhaustion at higher budget | CPA rises as audience saturates | Monitor frequency; expand retargeting pool with video viewers |
| social_ads_agent continues timing out | Paid Acquisition vertical incomplete | Add 120s timeout + fallback in gtm_commander.py |
