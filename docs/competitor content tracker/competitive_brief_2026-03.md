# Competitive Ad Intelligence — March 2026

**Generated:** 2026-03-14  
**Period:** Last 30 days (Meta); tracker snapshot 2026-03-10

---

## 1. Executive Summary

- **LinkedIn dominates competitor paid presence** — Latest tracker run (2026-03-10) shows 69 total competitor ads across tracked brands; 62 of those are on LinkedIn. Reader-side and advertiser-side competitors (Morning Brew, The Hustle, Meta for Business, Paved, Beehiiv) all run heavily on LinkedIn with single-image, benefit-led copy.
- **TLDR’s own Meta performance is strong** — Last 30d: ~$27.9K spend, 573K impressions, 1.21% CTR, $4.04 CPC, 176 leads, 21 complete registrations. Video and link clicks are primary drivers; lead CPM ~$159.
- **Data gaps this run** — ScrapeCreators (Meta Ad Library) API returned 404; competitor pull via `fb_ad_library_api.py` was skipped. Google Ads API returned 404; own Google performance is unavailable. Multi-platform competitive tracker (Google, LinkedIn, TikTok, X) was started but ran long; this brief uses existing tracker CSVs from 2026-03-10.
- **Strategic takeaway** — Double down on Meta where TLDR already has conversion data; consider LinkedIn tests aligned with competitor creative patterns (single-image, “join X million” / social proof, clear CTAs). Revisit ScrapeCreators and Google Ads API config for next run.

---

## 2. Competitor Ad Volume

From `ad_volume_tracker.csv` (audit 2026-03-10):

| Competitor        | Meta | Google | LinkedIn | TikTok | X  | Notes                    |
|-------------------|------|--------|----------|--------|----|--------------------------|
| Morning Brew      | 1    | 0      | 15       | 0      | 0  | Highest volume (16 ads)  |
| The Hustle        | 1    | 0      | 15       | 0      | 0  |                          |
| Hacker News (YC)  | 1    | 0      | 3        | 0      | 0  |                          |
| Stratechery       | 0    | 0      | 0        | 0      | 0  |                          |
| Lenny's Newsletter| 0   | 0      | 0        | 0      | 0  |                          |
| Bytes.dev         | 0    | 0      | 0        | 0      | 0  |                          |
| LinkedIn Ads      | 1    | 0      | 0        | 0      | 0  |                          |
| Meta Ads          | 1    | 0      | 15       | 0      | 0  |                          |
| Paved             | 1    | 0      | 14       | 0      | 0  |                          |
| Beehiiv           | 1    | 0      | 0        | 0      | 0  |                          |
| **Total**         | **7**| **0**  | **62**   | **0**  | **0** | **Top platform: LinkedIn (62). Total: 69** |

---

## 3. Creative Trend Analysis

**Format mix:** Static single-image ads dominate on LinkedIn; Meta entries in the log are mostly video (IDs only; copy not scraped this run).

**Messaging themes:**
- **Reader newsletters (Morning Brew):** “Business news doesn’t have to be boring,” “4M+ professionals,” “Try Morning Brew for free,” “Stay sharp, laugh a little, impress your boss.” Tone: light, professional, social proof + benefit.
- **Advertiser / B2B (The Hustle):** Email revenue and performance (“1% to 22% open rates,” “email strategy,” “400+ brands”), workshops, UGC/product-in-use, free consultation CTAs.
- **Platforms (Meta for Business):** WhatsApp for Business (275% ROI, Forrester TEI), events (WhatsApp Business Summit), Meta Marketing Pro demos. Copy is stats- and event-led.
- **Paved (mix):** Compensation/HR (Pave comp platform, “How Big of a Raise in 2026?”), events (Future Proof Citywide), and some PAVE Manufacturing (unrelated brand in same log).

**CTA patterns:** “Try for free,” “Join 4M+…,” “Get a free consultation,” “Talk to your Marketing Pro,” “Limited slots only,” “Reserve your slots.”

**Visual style:** Log shows “Static image” for LinkedIn; Meta entries are video (no creative detail in this pull).

---

## 4. TLDR Performance Context

**Meta Ads (last 30d)** — Account-level:

| Metric              | Value      |
|---------------------|------------|
| Spend               | $27,922.98 |
| Impressions         | 572,790    |
| Reach               | 203,267    |
| Clicks              | 6,914      |
| CTR                 | 1.21%      |
| CPC                 | $4.04      |
| Link clicks         | 3,750      |
| Leads               | 176        |
| Complete registration | 21      |
| Video views         | 17,074     |
| Post engagement     | 31,387     |

**Google Ads:** Own performance data unavailable this run (API 404).

---

## 5. Strategic Recommendations

1. **Lean into Meta** — Strong lead and registration volume and known CPC/CPA; keep optimizing creative and audiences on Meta.
2. **Test LinkedIn with newsletter-style creative** — Competitors (especially Morning Brew) use single-image + “join X million” / “free, fast, fun” angles. Run a small LinkedIn test with similar social-proof and benefit framing.
3. **Reuse winning CTA patterns** — “Try for free,” “Join X people,” “Get the report/guide” are repeated across competitors; A/B test these on Meta and any LinkedIn tests.
4. **Fix data pipelines for next run** — Restore ScrapeCreators (Meta Ad Library) and Google Ads API access so next brief includes fresh competitor Meta creatives and TLDR Google performance.
5. **Let tracker complete or run with --dry-run** — For full Google/LinkedIn/TikTok/X refresh, run `competitive_tracker.py` with appropriate platforms and consider scheduling so it can finish (or run dry-run to validate).

---

## 6. Raw Ad Samples (Notable Competitor Ads)

**1. Morning Brew (LinkedIn)**  
- **Copy angle:** Business news made enjoyable; professional credibility.  
- **Primary text:** “Engaging. Insightful. Never snooze-worthy. Try Morning Brew for free and see why business news doesn’t have to be boring…”  
- **Headline/CTA:** “Get Morning Brew now ☕️ 🚀”  
- **Format:** Single image.  
- **Note:** Clear value prop + soft CTA; good template for TLDR “smart, brief, daily” positioning.

**2. The Hustle (LinkedIn)**  
- **Copy angle:** Email performance and scale.  
- **Primary text:** “From 1% to 22% open rates in just 6 weeks 📈, and that’s only the beginning!”  
- **Headline:** “From 1% to 22% Open Rates in 6 Weeks: How a Nurse Coaching Brand Rebuilt Inbox Trust”  
- **Format:** Single image.  
- **Note:** Concrete outcome + story hook; applicable to performance/case-study style ads for TLDR advertiser messaging.

**3. Meta for Business (LinkedIn)**  
- **Copy angle:** WhatsApp for Business ROI and research.  
- **Primary text:** “Transform customer interactions into business growth. Explore Forrester’s TEI study to see how WhatsApp for Business str…”  
- **Headline:** “275% ROI with WhatsApp—Forrester Research”  
- **Format:** Single image.  
- **Note:** Third-party stat (Forrester) + product benefit; model for any TLDR partner or research-backed creative.

---

## Data & Automation Notes

- **ScrapeCreators (Meta Ad Library):** Skipped — API returned 404 for `/v2/meta-ad-library/search-page`.
- **Google Ads API:** Skipped — 404; TLDR Google metrics not in this brief.
- **Competitive tracker:** Script started for `--platforms google linkedin tiktok x`; brief uses existing `ad_creative_log.csv` and `ad_volume_tracker.csv` from 2026-03-10.
- **Local path:** `docs/competitor content tracker/competitive_brief_2026-03.md`. Push to Google Docs when desired via `automations/lib/gdocs_api.py create/update`.
