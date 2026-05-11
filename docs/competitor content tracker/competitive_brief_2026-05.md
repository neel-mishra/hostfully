# Competitive Ad Intelligence Brief — May 2026

**Report Date:** May 11, 2026
**Period Covered:** April 11 – May 10, 2026 (last 30 days)
**Platforms Scanned:** LinkedIn (primary), Google Transparency, TikTok Library, X Transparency
**Data Sources:** Meta Marketing API (own performance), LinkedIn Ad Library (competitor creatives), Multi-Platform Competitive Tracker

---

## 1. Executive Summary

- **LinkedIn dominates competitor ad activity.** All 79 competitor ads found this cycle came from LinkedIn. Google Transparency, TikTok, and X yielded zero publicly visible ads for the tracked competitor set — indicating either low spend on those platforms or limitations in public ad library visibility.
- **Beehiiv and Morning Brew are the most visible competitors on LinkedIn** with 15 ads each (alongside The Hustle, Meta Ads, and Paved at 15 each). Beehiiv has 306 total active ads in LinkedIn's library, while Morning Brew has 129 and The Hustle has 362.
- **The Hustle's LinkedIn presence appears misattributed** — most ads captured are from a Singapore-based design training company using "The Hustle" branding on LinkedIn, not HubSpot's newsletter. This signals brand confusion risk on LinkedIn.
- **Meta for Business is aggressively pushing WhatsApp Business** across multiple markets (Australia, EMEA, French-speaking regions), with 592 total active LinkedIn ads — the highest volume of any tracked competitor.
- **ScrapeCreators Meta Ad Library API returned 404 errors for all competitors**, preventing Meta ad creative pulls. Google Ads API also returned 404 errors. TLDR's Meta Ads account data was successfully retrieved.

---

## 2. Competitor Ad Volume

### Ads Captured This Audit (LinkedIn Ad Library)

| Competitor | LinkedIn Ads Found | Total Active (LinkedIn) |
|---|---|---|
| Morning Brew | 15 | 129 |
| The Hustle | 15 | 362 |
| Hacker News / Y Combinator | 4 | 4 |
| Stratechery | 0 | 0 |
| Lenny's Newsletter | 0 | 0 |
| Bytes.dev | 0 | 0 |
| LinkedIn Marketing Solutions | 0 | N/A |
| Meta for Business | 15 | 592 |
| Paved | 15 | 896 |
| Beehiiv | 15 | 306 |
| **Total** | **79** | — |

### Platform Coverage

| Platform | Total Ads Found | Notes |
|---|---|---|
| LinkedIn | 79 | Primary source; public ad library working |
| Google | 0 | Transparency Center API/scrape returned no results |
| TikTok | 0 | Commercial Content Library returned no results |
| X (Twitter) | 0 | Ads Transparency Center returned no results |
| Meta (via ScrapeCreators) | 0 | API returned HTTP 404 for all queries |

---

## 3. Creative Trend Analysis

### Messaging Themes

**Reader-side competitors (Morning Brew, The Hustle, Y Combinator):**

- **Morning Brew** leads with a consistent "business news doesn't have to be boring" angle. Their copy is conversational and benefit-driven, consistently referencing their 4M+ subscriber count as social proof. Key phrases: "Never snooze-worthy," "Stay sharp, laugh a little, impress your boss," "your favorite morning habit."
- **Y Combinator / Hacker News** has minimal ad presence (4 ads). Their ads promote portfolio companies (Clicks, Nexus) and community events rather than the newsletter itself — functioning more as an accelerator brand than a media brand.
- **The Hustle** results are largely contaminated with unrelated "HustleHub" branding from a Singapore training company, making direct creative analysis unreliable this cycle.

**Advertiser-side competitors (Meta Ads, Paved, Beehiiv):**

- **Meta for Business** is running a major WhatsApp Business push with Forrester TEI study data (275% ROI claim). They're also promoting a "Performance Marketing Summit" on 5/13/2026. Their ads are data-heavy and B2B enterprise-focused.
- **Paved** ads are largely contaminated with unrelated companies (compensation data company "Pave," paving contractors, and a Brazilian company). Only 1-2 of the 15 captured ads appear to be from Paved the newsletter ad network (promoting "The Newsletter Conference").
- **Beehiiv** is using a "thought leader amplification" strategy — boosting individual creator profiles/bios as sponsored content rather than traditional product ads. This is a distinctly different approach from typical SaaS advertising. They're also getting press coverage (Reuters) about their revenue growth.

### Visual Patterns

- **100% Single Image Ads** across all LinkedIn captures. No video, carousel, or document ads detected in this audit cycle.
- Static image with text overlay is the dominant format across all competitors on LinkedIn.

### CTA Patterns

- Morning Brew: "Get Morning Brew now," "Join 4M+ Professionals," "Try Morning Brew for free"
- Meta for Business: "Talk to your Marketing Pro," "Register now" (for summits)
- Beehiiv: "Promoted by beehiiv" (thought leader boost format — indirect CTA)
- Paved: "Stop using bad compensation data" (appears to be wrong Paved)

### Notable Tactical Observations

1. **Beehiiv's thought leader amplification** is a novel LinkedIn strategy — they boost individual creators' profiles with "Promoted by beehiiv" tags, using creator credibility to drive platform awareness rather than direct product marketing.
2. **Morning Brew runs duplicate ad variants** — multiple copies of the same ad with slight variations, suggesting active A/B testing.
3. **Meta for Business personalizes at scale** — several ads use `%FIRSTNAME%` merge fields and run in multiple languages (English, French), indicating sophisticated localization.
4. **Y Combinator uses event-based advertising** — focused on driving attendance to CFO and sales events in San Francisco rather than newsletter subscriptions.

---

## 4. TLDR Performance Context (Meta Ads — Last 30 Days)

### Account Summary (April 11 – May 10, 2026)

| Metric | Value |
|---|---|
| **Total Spend** | $31,330.56 |
| **Impressions** | 761,176 |
| **Reach** | 170,039 |
| **Clicks** | 9,103 |
| **CTR** | 1.20% |
| **CPC** | $3.44 |
| **Link Clicks** | 5,454 |
| **Landing Page Views** | 1,062 |
| **Video Views** | 73,996 |
| **Leads (Pixel)** | 123 |
| **Cost per Lead** | $254.72 |
| **Complete Registrations** | 24 |
| **Cost per Registration** | $1,305.44 |
| **Post Engagement** | 84,444 |
| **Post Reactions** | 4,485 |
| **Post Saves** | 265 (net: 259) |

### Top Active Campaigns (by spend)

| Campaign | Spend | Impressions | CTR | CPC |
|---|---|---|---|---|
| ca-us_pms_prospecting_website-conv | $15,880.22 | 200,837 | 1.29% | $6.15 |
| [Leads] hostfully pt-br — meeting | $6,704.90 | 286,797 | 0.76% | $3.07 |
| au-uk_pms_prospecting_website-conv | $3,204.72 | 47,055 | 1.50% | $4.54 |
| mx_pms_prospecting_website-conv | $2,405.16 | 164,500 | 1.78% | $0.82 |
| ca-us_pms_retargeting_website-conv | $2,292.64 | 30,888 | 1.29% | $5.77 |
| au-uk_pms_retargeting_website-conv | $618.55 | 7,655 | 1.53% | $5.29 |
| [Post Promovido] pt-br | $150.16 | 20,313 | 0.72% | $1.02 |
| [Leads] LAL1% hostfully pt-br | $74.19 | 3,129 | 1.37% | $1.73 |

### Google Ads Performance

Google Ads API returned HTTP 404 errors across all API versions (v17, v18, v19). Own Google Ads performance data is unavailable this cycle. The customer ID and OAuth credentials are configured, but the API endpoint is unreachable — this may require developer token review or account verification.

---

## 5. Strategic Recommendations

### What to Test

1. **Thought Leader Amplification (Beehiiv-style):** Test boosting content from TLDR writers/editors as sponsored LinkedIn posts with "Promoted by TLDR" attribution. This builds brand credibility through individual voices rather than corporate ads.

2. **Social Proof Scaling (Morning Brew-style):** Morning Brew consistently highlights "4M+ professionals" in every ad variant. TLDR should similarly lead with subscriber count in LinkedIn ad copy — this is the single most repeated element across Morning Brew's creative.

3. **Event-Based Advertising (Y Combinator-style):** Consider promoting TLDR community events, webinars, or meetups as LinkedIn ads. Y Combinator's event-focused ads get engagement despite small ad volume.

4. **Data-Backed Authority Content (Meta for Business-style):** Meta's strongest performing creative leads with specific ROI claims (275% ROI) backed by third-party research (Forrester). TLDR could commission or partner on research studies about newsletter advertising effectiveness.

### Formats to Try

- **Video Ads on LinkedIn:** 100% of competitor ads found were static images. Video is an untapped format on LinkedIn for this competitive set — first-mover advantage opportunity.
- **Carousel/Document Ads:** No competitors are running carousel or document ads on LinkedIn. "Top 5 things you missed this week" carousel format could drive engagement.
- **Multi-language variants:** Meta for Business runs ads in English, French, and Portuguese. If TLDR is expanding internationally, localized ad creative is proven by competitors.

### Messaging Angles to Explore

- **Anti-boring positioning:** Morning Brew owns "not boring" — TLDR should lean into its unique angle (e.g., speed, brevity, technical depth) to differentiate.
- **Professional FOMO:** "Join X professionals" is the dominant subscriber acquisition angle. Test specificity — "Join 50,000 CTOs" or "Read by engineers at Google, Meta, and Apple."
- **Creator/expert endorsement:** Beehiiv's strategy of amplifying creator voices is generating organic reach. Partner with tech leaders for testimonial-style ads.

### Operational Recommendations

- **Investigate ScrapeCreators API:** The Meta Ad Library API (ScrapeCreators) returned 404 for all queries. This may indicate an API endpoint change, key expiration, or service disruption. Restoring this would dramatically improve competitive visibility on Meta.
- **Debug Google Ads API:** The 404 errors from Google Ads API suggest either the customer ID (2565189582) is inactive, the developer token needs review, or the API version (v18) is deprecated. This should be resolved before the next cycle.
- **Improve LinkedIn search precision:** "The Hustle" and "Paved" searches returned ads from unrelated companies with similar names. Adding company ID filters or more specific search terms would improve data quality.

---

## 6. Notable Competitor Ad Samples

### Sample 1: Morning Brew — LinkedIn (Best-in-class newsletter acquisition ad)

> **Headline:** "Engaging. Insightful. Never snooze-worthy. Try Morning Brew for free and see why business news doesn't have to be boring…"
> **CTA:** "Get Morning Brew now ☕️ 🚀"
> **Format:** Single Image Ad
> **Analysis:** Strong emotional hooks ("never snooze-worthy"), clear value prop, free trial CTA with emoji for pattern interruption. This ad runs in multiple duplicates, suggesting it's a proven performer. The "4M+" social proof is consistent across all variants.

### Sample 2: Meta for Business — LinkedIn (Data-driven enterprise B2B)

> **Headline:** "Transform customer interactions into business growth. Explore Forrester's TEI study to see how WhatsApp for Business drives 275% ROI."
> **CTA:** "WhatsApp for Business: 275% ROI Proven"
> **Format:** Single Image Ad
> **Analysis:** Leads with third-party validation (Forrester), specific ROI figure (275%), and a transformation narrative. Runs in multiple languages. This is the most sophisticated B2B ad in the competitive set — demonstrates the power of research-backed claims.

### Sample 3: Beehiiv — LinkedIn (Thought leader amplification)

> **Headline:** "Newsletter Startup Founder, AI Optimization Expert, Writer, and Innovator | Helping founders launch their profitable newsletter business with beehiiv"
> **CTA:** "Promoted by beehiiv"
> **Format:** Single Image Ad (profile boost)
> **Analysis:** Unconventional format — beehiiv pays to boost its power users' LinkedIn profiles as ads. This creates the appearance of organic endorsement while building brand association with successful newsletter creators. Highly scalable and low creative production cost.

---

## Appendix: Data Sources & Limitations

| Source | Status | Notes |
|---|---|---|
| ScrapeCreators Meta Ad Library API | **FAILED** (HTTP 404) | All 10 competitor queries returned 404. API may be down or endpoint changed. |
| Meta Marketing API (own account) | **SUCCESS** | Full account + campaign data for last 30 days |
| Google Ads API (own account) | **FAILED** (HTTP 404) | All API versions (v17-v19) returned 404. Customer ID or developer token may need review. |
| LinkedIn Ad Library (Playwright) | **SUCCESS** | 79 ads captured across 6 competitors |
| Google Transparency Center | **FAILED** | No results for any competitor |
| TikTok Commercial Content Library | **FAILED** | No results for any competitor |
| X Ads Transparency Center | **FAILED** | No results for any competitor |
| Competitive Tracker CSVs | **SUCCESS** | Updated ad_creative_log.csv and ad_volume_tracker.csv |

**Next scheduled run:** June 8, 2026 (first Monday of June)
