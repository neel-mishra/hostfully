# Competitive Ad Intelligence — March 2026

**Generated:** 2026-03-16  
**Period:** Last 30 days (Feb 14 – Mar 15, 2026); tracker snapshot 2026-03-16

---

## 1. Executive Summary

- **LinkedIn remains the dominant competitor ad channel** — The 2026-03-16 tracker run found 85 total competitor ads; 78 (92%) are on LinkedIn. Meta accounts for the remaining 7 (Playwright-scraped entries). Google, TikTok, and X returned zero ads across all competitors.
- **Beehiiv emerges as a major ad spender** — Beehiiv now runs 15 LinkedIn ads (up from 0 on 2026-03-10), primarily thought-leader promotion and "newsletter platform built for growth" positioning. This marks a significant week-over-week increase in competitor activity.
- **The Hustle is iterating aggressively on email performance messaging** — New creatives this week focus on domain reputation recovery ("From 'Bad' to 'High' Domain Reputation — In 6 Weeks") and open rate case studies ("2,500 Emails. One Click. Here's the Real Problem."), a shift from the broader "build email revenue" angle seen in prior weeks.
- **TLDR Meta performance is solid** — Last 30d: $29.3K spend, 592K impressions, 1.17% CTR, $4.24 CPC, 167 lead-valid results, 23 complete registrations across 11 campaigns with delivery. Cost per lead is ~$176.
- **Data gaps** — ScrapeCreators (Meta Ad Library API) returns 404; competitor Meta ad detail relies on Playwright. Google Ads API returns 404; own Google performance unavailable. TikTok and X ad libraries yielded no results via Playwright scraping.

---

## 2. Competitor Ad Volume

From `ad_volume_tracker.csv` (audit 2026-03-16):

| Competitor          | Meta | Google | LinkedIn | TikTok | X  | Total | Notes                        |
|---------------------|------|--------|----------|--------|----|-------|------------------------------|
| Morning Brew        | 1    | 0      | 15       | 0      | 0  | 16    | Highest volume (tied)        |
| The Hustle          | 1    | 0      | 15       | 0      | 0  | 16    | New email perf. creatives    |
| Hacker News (YC)    | 1    | 0      | 3        | 0      | 0  | 4     |                              |
| Stratechery         | 0    | 0      | 0        | 0      | 0  | 0     | No active paid ads detected  |
| Lenny's Newsletter  | 0    | 0      | 0        | 0      | 0  | 0     | No active paid ads detected  |
| Bytes.dev           | 0    | 0      | 0        | 0      | 0  | 0     | No active paid ads detected  |
| LinkedIn Ads        | 1    | 0      | 0        | 0      | 0  | 1     |                              |
| Meta for Business   | 1    | 0      | 15       | 0      | 0  | 16    | WhatsApp focus continues     |
| Paved               | 1    | 0      | 15       | 0      | 0  | 16    | Mixed: Pave comp + AG Paving |
| Beehiiv             | 1    | 0      | 15       | 0      | 0  | 16    | **New entrant** — up from 0  |
| **Total**           | **7**| **0**  | **78**   | **0**  | **0** | **85** | Top platform: LinkedIn (92%) |

**Week-over-week changes (vs. 2026-03-14):**
- Beehiiv: 15 → 15 LinkedIn ads (stable after entering last week)
- The Hustle: 15 → 15 LinkedIn ads (8 new creatives replacing older ones)
- Paved: 15 → 15 LinkedIn ads (some new AG Paving/retaining wall ads)
- Total competitor ads: 78 → 85 (Meta Playwright now capturing 7 entries)

---

## 3. Creative Trend Analysis

### Format mix
- **LinkedIn:** 100% single-image ads across all competitors. No video, carousel, or document ads detected.
- **Meta:** Playwright captures show video creatives for most competitors, but without ScrapeCreators API, copy/headline detail is limited.

### Messaging themes by competitor segment

**Reader-side newsletters:**
- **Morning Brew:** Unchanged playbook — "Business news doesn't have to be boring," "4M+ professionals," social proof + benefit framing. 194 total active ads on LinkedIn (per ad library count).
- **The Hustle (new this week):** Pivoting hard into email performance proof points:
  - "Most coaches think 2% open rates mean their audience is tired" → case study hook
  - "Google keeps a reputation score for every email domain" → domain reputation angle
  - "2,500 Emails. One Click. Here's the Real Problem." → pain-point-first copy
  - Still running "Build an email revenue channel designed to scale in 2026" and workshop/Canva training ads
  - 302 total active LinkedIn ads (up from 294)
- **Y Combinator / Hacker News:** 3 LinkedIn ads — YC startup promotions (Clicks, Nexus) and CFO events. Not newsletter-focused.
- **Stratechery, Lenny's, Bytes.dev:** No active paid ads detected on any platform.

**Advertiser-side / platforms:**
- **Meta for Business:** WhatsApp Business remains the headline product — Forrester TEI study (275% ROI), WhatsApp Business Summit invites, Marketing Pro demos. 590 total active LinkedIn ads.
- **Paved:** Mixed signal — "Paved" search captures Pave (comp platform), PAVE Manufacturing, and AG Paving alongside the actual Paved newsletter ad network. Genuine Paved ads are diluted. 819 total active on LinkedIn.
- **Beehiiv:** Thought-leader amplification strategy — promoting newsletter creators' personal brands ("Revenue Operations Strategist," "Newsletter Startup Founder," "Growth Unhinged") with "Promoted by beehiiv" attribution. Also running "beehiiv — The newsletter platform built for growth" and Reuters coverage of revenue doubling. 327 total active LinkedIn ads.

### CTA patterns
- "Try for free" / "Join X million" (Morning Brew)
- "TALK TO OUR EXPERTS" / "GET A FREE CONSULTATION" (The Hustle)
- "Talk to your Marketing Pro" (Meta for Business)
- "Reserve Your Slots" / "Limited Slots Only" (The Hustle workshops)
- "Promoted by beehiiv" — soft brand awareness, no hard CTA (Beehiiv)
- "FREE Preliminary Design Service" / "Get In Touch Today" (Paved/AG)

### Visual style
- LinkedIn: Universally static single-image. No competitors running video or carousel on LinkedIn.
- Meta: Video-heavy based on Playwright detection, but creative details not available without API access.

---

## 4. TLDR Performance Context

### Meta Ads (last 30d: Feb 14 – Mar 15, 2026)

| Metric                | Value        |
|-----------------------|-------------|
| Spend                 | $29,289.68  |
| Impressions           | 591,959     |
| Reach                 | 203,524     |
| Clicks                | 6,906       |
| CTR                   | 1.17%       |
| CPC                   | $4.24       |
| Link clicks           | 3,781       |
| Landing page views    | 567         |
| Leads (email-valid)   | 167         |
| Complete registrations| 23          |
| Video views           | 18,293      |
| Post engagement       | 31,646      |
| Cost per lead         | $176.44     |

**Campaign breakdown (by results):**

| Campaign                                  | Result Type       | Results |
|-------------------------------------------|-------------------|---------|
| Meta-Leads-PMS_Conversions-Manual         | lead_email-valid  | 91      |
| Meta-Leads-Guidebook_Conversions          | lead_email-valid  | 44      |
| Meta-Sales-PMS_Conversions-Retargeting    | lead_email-valid  | 11      |
| ca-us_pms_prospecting_website-conv        | lead_email-valid  | 8       |
| Meta-Sales-Industry Report_Prospecting    | lead_email-valid  | 7       |
| au-uk_pms_prospecting_website-conv        | custom_conversion | 4       |
| [Leads] hostfully pt-br — meeting         | lead_email-valid  | 3       |
| au-uk_pms_retargeting_website-conv        | lead_email-valid  | 2       |
| ca-us_pms_retargeting_website-conv        | lead_email-valid  | 1       |

**Active campaigns:** 11 with delivery out of 11 total (ACTIVE + PAUSED with spend).

### Google Ads

Own performance data unavailable — Google Ads API returned 404 (configuration issue persists from prior runs).

---

## 5. Strategic Recommendations

1. **Test LinkedIn ads aligned with competitor creative patterns** — Morning Brew's "Join X million professionals" and social-proof framing works at scale (194 active ads). TLDR can run a similar playbook: "Join 5M+ tech professionals who start their day with TLDR" + single-image format. Cost of entry is low since all competitors use static images.

2. **Counter The Hustle's email performance messaging** — The Hustle is aggressively targeting brands with email deliverability pain ("2% to 22% open rates," domain reputation recovery). TLDR should develop case-study creatives showing advertiser ROI and engagement metrics to compete for the same B2B email marketing buyer.

3. **Watch Beehiiv's thought-leader play** — Beehiiv's LinkedIn strategy (promoting individual creators' profiles with "Promoted by beehiiv" tags) is a platform-level brand awareness tactic. If this proves effective, TLDR could sponsor thought-leader content on LinkedIn to build newsletter brand awareness.

4. **Double down on Meta lead gen** — PMS_Conversions-Manual (91 leads) and Guidebook_Conversions (44 leads) are the top-performing campaigns. Continue scaling these while testing new creative formats (the guidebook angle is a clear winner).

5. **Explore video on LinkedIn** — Zero competitors are running video on LinkedIn. This represents a format gap and potential first-mover advantage for TLDR. Repurpose top-performing Meta video creatives for LinkedIn Sponsored Content.

6. **Fix data pipeline issues for next run:**
   - ScrapeCreators API: endpoint returns 404 — verify API key validity and endpoint URL with provider.
   - Google Ads API: returns 404 — check customer ID, developer token, and API version (currently v18).
   - Paved search noise: LinkedIn results for "Paved" capture unrelated brands (Pave, PAVE Manufacturing, AG Paving). Consider refining the search term in `config.py` to "Paved newsletter" or using a LinkedIn company ID.

---

## 6. Raw Ad Samples (Notable Competitor Ads)

### 1. The Hustle — Domain Reputation Recovery (LinkedIn, NEW 2026-03-16)
- **Copy angle:** Email deliverability pain point → case study proof
- **Primary text:** "Google keeps a reputation score for every email domain."
- **Headline:** "From 'Bad' to 'High' Domain Reputation — In 6 Weeks"
- **Format:** Single image
- **Why it matters:** Concrete, specific claim with urgency. Good model for TLDR advertiser-side messaging about email performance metrics.

### 2. The Hustle — Open Rate Turnaround (LinkedIn, NEW 2026-03-16)
- **Copy angle:** Pain-point opener → outcome
- **Primary text:** "Most coaches think 2% open rates mean their audience is tired."
- **Headline:** "We fixed email performance for a coaching brand and actual opens went from 2% to 22% in 6 weeks."
- **Format:** Single image
- **Why it matters:** Story-driven hook that challenges assumptions. The Hustle is iterating rapidly on email performance proof points — 4 new variations in one week.

### 3. Beehiiv — Platform Growth Story (LinkedIn, 2026-03-14)
- **Copy angle:** Third-party press validation
- **Primary text:** "Reuters tech reporter | Signal: jaspreet.55"
- **Headline:** "Substack challenger beehiiv expects revenue to nearly double on newsletter boom"
- **Format:** Single image (thought-leader promotion)
- **Why it matters:** Beehiiv is leveraging press coverage as social proof on LinkedIn. The "Promoted by beehiiv" tag turns every thought-leader post into a brand impression. Novel strategy worth monitoring.

### 4. Morning Brew — Social Proof Classic (LinkedIn, recurring)
- **Copy angle:** Social proof + benefit + soft CTA
- **Primary text:** "In case you didn't know—business news doesn't have to be boring. That's why over 4 million professionals read Morning Brew…"
- **Headline:** "Join 4M+ Pros Reading Morning Brew"
- **Format:** Single image
- **Why it matters:** This template has been running consistently since at least 2026-03-10. The "X million" social proof + "doesn't have to be boring" value prop is a proven formula TLDR can adapt.

---

## Data & Automation Notes

- **ScrapeCreators (Meta Ad Library):** API returned 404 for `/v2/meta-ad-library/search-page` — all competitor Meta data comes from Playwright browser scraping (limited to 1 entry per competitor).
- **Google Ads API:** Returned 404 — TLDR Google metrics not available this run.
- **Google Ads Transparency Center:** No ads found for any competitor via Playwright scraping.
- **TikTok Commercial Content Library:** No ads found for any competitor via Playwright scraping.
- **X Ads Transparency Center:** No ads found for any competitor via Playwright scraping.
- **Competitive tracker:** Full 5-platform run completed 2026-03-16. 85 total ads found (7 Meta, 78 LinkedIn). 12 new ads appended to `ad_creative_log.csv`.
- **Local path:** `docs/competitor content tracker/competitive_brief_2026-03.md`
- **CSV data:** `docs/competitor content tracker/paid ads creatives/ad_creative_log.csv` (108 rows) and `ad_volume_tracker.csv` (9 audit rows).
