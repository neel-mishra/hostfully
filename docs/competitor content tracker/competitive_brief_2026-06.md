# Competitive Ad Intelligence Brief — June 2026

**Report Date:** June 15, 2026
**Reporting Period:** May 16 – June 14, 2026 (last 30 days)
**Prepared by:** TLDR Competitive Intelligence Automation

---

## 1. Executive Summary

- **LinkedIn dominates competitor ad activity.** All 79 competitor ads detected this period were on LinkedIn. No competitor showed active paid creatives on Google Ads Transparency Center, TikTok, or X/Twitter, suggesting newsletter and B2B competitors are concentrating paid spend on LinkedIn for professional audience acquisition.
- **beehiiv has shifted to employer branding on LinkedIn.** All 15 beehiiv ads feature employee title cards ("Creative Director at beehiiv," "COO @ beehiiv") rather than product-focused messaging — a deliberate play to attract talent and build brand credibility simultaneously.
- **Morning Brew continues high-volume social proof messaging.** With 115 total active LinkedIn ads and consistent "4M+ professionals" copy, Morning Brew runs the largest single-platform ad library among reader-side competitors. Their messaging is remarkably consistent: fun, accessible business news positioning.
- **TLDR's Meta Ads are performing well with $34.5K monthly spend** generating 1.7M impressions, 22.4K clicks (1.32% CTR), and 102 leads at $338 CPL. The active campaigns skew toward international PMS prospecting with the strongest efficiency in Mexico ($0.87 CPC).
- **Google Ads data was unavailable** due to an expired/deleted OAuth token ("Account has been deleted" error). Refreshing the `GOOGLE_ADS_REFRESH_TOKEN` is required before the next run.
- **ScrapeCreators API credits are exhausted** (HTTP 402), so Meta Ad Library data for competitors was not available this cycle. The API endpoint paths have been corrected from the deprecated v2 to the current v1 in `fb_ad_library_api.py`.

---

## 2. Competitor Ad Volume

### Current Period (June 15, 2026 audit)

| Competitor | Meta | Google | LinkedIn | TikTok | X | Total Active |
|---|---|---|---|---|---|---|
| Morning Brew | — | 0 | 15 | 0 | 0 | 115* |
| The Hustle | — | 0 | 15 | 0 | 0 | 376* |
| Y Combinator / HN | — | 0 | 4 | 0 | 0 | 4* |
| Stratechery | — | 0 | 0 | 0 | 0 | 0 |
| Lenny Rachitsky | — | 0 | 0 | 0 | 0 | 0 |
| Bytes.dev | — | 0 | 0 | 0 | 0 | 0 |
| LinkedIn Marketing Solutions | — | 0 | 0 | 0 | 0 | 0 |
| Meta for Business | — | 0 | 15 | 0 | 0 | 608* |
| Paved | — | 0 | 15 | 0 | 0 | 958* |
| beehiiv | — | 0 | 15 | 0 | 0 | 409* |

*\*"Total Active" = LinkedIn's reported total active ad count for that advertiser across all campaigns, not just sampled.*
*"—" = Meta Ad Library data unavailable (ScrapeCreators credits exhausted).*

### Trend vs. March 2026 Audit

| Competitor | Mar LinkedIn | Jun LinkedIn | Change |
|---|---|---|---|
| Morning Brew | 15 | 15 (115 total active) | Stable sample, but total active dropped from 194 to 115 |
| The Hustle | 15 | 15 (376 total active) | Total active surged from 292 to 376 (+29%) |
| Y Combinator / HN | 3 | 4 (4 total active) | Minimal presence, added 1 ad |
| Meta for Business | 15 | 15 (608 total active) | Up from 589 to 608 (+3%) |
| Paved | 14-15 | 15 (958 total active) | Surged from 810 to 958 (+18%) |
| beehiiv | 0-15 | 15 (409 total active) | Up from 327 to 409 (+25%) |

---

## 3. Creative Trend Analysis

### Messaging Themes by Competitor

**Morning Brew** — Relentlessly consistent messaging:
- "Business news doesn't have to be boring" (appears in 8+ ad variants)
- Social proof: "4M+ professionals" / "4M+ people reading"
- Tone: casual, fun, accessible ("Stay sharp, laugh a little, impress your boss")
- One new angle: Glassdoor job listing partnership ad

**The Hustle** — Has pivoted significantly from newsletter promotion:
- Now dominated by "Hustle" peer-to-peer SMS/texting platform ads (not the HubSpot newsletter)
- B2B SaaS messaging: "The Outreach Channel People Actually Answer"
- Retargeting copy with personalized %FIRSTNAME% tokens
- Corporate training ads (Canva, negotiation workshops)
- Email deliverability consulting ("40-60% of emails in spam")

**Y Combinator** — Minimal but focused:
- Event promotion (CFO events, AI sales events in SF)
- Portfolio company spotlights (Clicks, Nexus)
- Recruiting-adjacent positioning

**Meta for Business** — Highest total volume (608 active ads):
- Advantage+ Suite automation messaging
- AI creative tools positioning ("test, refresh and optimise faster")
- Measurement tools ("clarity to see exactly what's working")
- Meta Agency Awards promotion (deadline August 14)
- WhatsApp Business push continues but rotating to newer themes

**Paved** — Extremely noisy results (958 total active):
- Note: "Paved" search returns many false positives (Pave compensation platform, paving companies, Munson fencing)
- Actual Paved (newsletter ad network) signal is very low
- Pave (compensation): merit cycle, AI compensation surveys, 2026 budgets

**beehiiv** — Distinctive employer branding strategy:
- 100% of sampled ads are employee spotlight/thought leader cards
- Titles: Creative Director, COO, CMO, Chief Customer Officer, Controller, Head of Support
- "Promoted by beehiiv" and "something's cooking at beehiiv HQ" teaser copy
- No direct product/newsletter platform ads in current LinkedIn sample

### Visual & Format Patterns

| Pattern | Observation |
|---|---|
| **Format** | 100% Single Image Ads on LinkedIn — no carousel, video, or document ads detected |
| **Visual style** | All static images; no video ads across any LinkedIn competitor |
| **CTA patterns** | Most CTAs are soft: "Try for free," "Join," "Schedule a Demo," "Submit to win" |
| **Personalization** | The Hustle uses %FIRSTNAME% dynamic insertion in multiple ads |
| **Localization** | Meta for Business runs Spanish and Portuguese variants |

### Key Strategic Signals

1. **The Hustle has likely spun off or rebranded its ad presence** — the LinkedIn ad library now shows peer-to-peer texting platform "Hustle" ads, not HubSpot's The Hustle newsletter. This may mean HubSpot is running The Hustle newsletter ads under the HubSpot brand instead.
2. **beehiiv is investing heavily in employer brand** as a growth channel, possibly signaling aggressive hiring and using LinkedIn ads for both talent and brand awareness.
3. **No competitor is running detectable ads on Google, TikTok, or X** — LinkedIn is the clear channel of choice for B2B newsletter promotion.

---

## 4. TLDR Performance Context

### Meta Ads — Account Summary (May 16 – Jun 14, 2026)

| Metric | Value |
|---|---|
| **Total Spend** | $34,524.61 |
| **Impressions** | 1,700,365 |
| **Reach** | 566,258 |
| **Clicks** | 22,421 |
| **CTR** | 1.32% |
| **CPC** | $1.54 |
| **Link Clicks** | 14,830 |
| **Landing Page Views** | 1,566 |
| **Leads (Pixel)** | 102 |
| **Cost per Lead** | $338.48 |
| **Complete Registrations** | 9 |
| **Cost per Registration** | $3,836.07 |
| **Video Views** | 231,238 |
| **Post Engagement** | 248,883 |

### Meta Ads — Active Campaign Breakdown

| Campaign | Spend | Impressions | Clicks | CTR | CPC | Leads |
|---|---|---|---|---|---|---|
| mx_pms_prospecting_website-conv | $5,006.75 | 385,377 | 5,729 | 1.49% | $0.87 | 34 |
| eu_pms_prospecting_website-conv | $3,076.99 | 208,723 | 2,824 | 1.35% | $1.09 | 7 |
| au-uk_pms_retargeting_website-conv | $445.84 | 6,244 | 89 | 1.43% | $5.01 | 2 |
| ca-us_pms_retargeting_website-conv | $1,804.33 | 25,991 | 340 | 1.31% | $5.31 | 19 |
| ca-us_pms_prospecting_website-conv | $16,897.88 | 249,537 | 4,287 | 1.72% | $3.94 | 27 |
| [Leads] hostfully pt-br — meeting | $7,292.82 | 824,493 | 9,152 | 1.11% | $0.80 | 13 |

**Key observations:**
- CA-US prospecting is the largest campaign by spend ($16.9K) with the highest CTR (1.72%) but elevated CPC ($3.94)
- Mexico prospecting delivers the lowest CPC ($0.87) with strong CTR (1.49%)
- Brazil/Hostfully campaign runs highest volume (824K impressions) at lowest CPC ($0.80) but low lead conversion (13 leads)
- Retargeting campaigns show high CPCs ($5.01–$5.31) but strong lead conversion relative to clicks
- 44 of 50 total campaigns are paused, indicating significant historical testing

### Google Ads

**Status: UNAVAILABLE** — Token refresh failed with "Account has been deleted" error. The `GOOGLE_ADS_REFRESH_TOKEN` needs to be regenerated. Unable to pull account summary or campaign data this period.

---

## 5. Strategic Recommendations

### Immediate Actions

1. **Fix Google Ads API access.** Regenerate `GOOGLE_ADS_REFRESH_TOKEN` before the next reporting cycle to restore full cross-platform performance visibility.

2. **Replenish ScrapeCreators credits.** The Meta Ad Library API returned HTTP 402 (out of credits). This blocks competitor Meta ad monitoring, which is especially important given TLDR's own Meta spend.

3. **Test LinkedIn as a paid channel.** Every competitor with meaningful ad activity is running on LinkedIn. TLDR should run a small test budget ($2-5K) targeting professional audiences on LinkedIn, especially given the tech/developer ICP overlap.

### Creative & Messaging Tests

4. **Test Morning Brew-style social proof messaging.** "Join 1M+ tech professionals" or "5 million readers can't be wrong" — simple, high-volume social proof is clearly the dominant playbook among newsletter competitors.

5. **Experiment with employer branding ads (beehiiv's playbook).** Running employee spotlight ads on LinkedIn could serve dual purpose: employer branding for TLDR hiring and building professional credibility.

6. **Try personalized retargeting copy.** The Hustle/Hustle platform uses %FIRSTNAME% personalization in LinkedIn ads. TLDR could test personalized retargeting on Meta using similar approaches.

7. **Test "business news doesn't have to be boring" counter-positioning.** Morning Brew owns this angle — TLDR should consider counter-positioning around depth, technical credibility, or "actually useful" vs. "entertaining."

### Format & Channel Experiments

8. **Video ads are an untapped opportunity.** Zero competitors are running video ads on LinkedIn. TLDR's existing video content and Remotion pipeline could give a first-mover advantage on LinkedIn video ads.

9. **Consider TikTok for developer audiences.** No competitors are running TikTok ads. Dev-focused short-form content ("5 things I learned from reading TLDR this week") could reach younger tech professionals.

10. **Diversify beyond Meta prospecting.** With $34.5K/month concentrated on Meta, testing Google Ads (once access is restored) and LinkedIn could improve channel resilience and potentially lower blended CAC.

---

## 6. Notable Competitor Ad Samples

### Sample 1: Morning Brew — Classic Social Proof

> **Headline:** "Serious news. Seriously fun. Morning Brew makes business news so enjoyable, you might even look forward to Mondays."
> **CTA:** "Join over 4 million people reading Morning Brew for free!"
> **Platform:** LinkedIn | **Format:** Single Image Ad
> **Link:** [LinkedIn Ad Library](https://www.linkedin.com/ad-library/detail/987831586)

**Analysis:** This is Morning Brew's core playbook — pair an anti-boring positioning with massive social proof numbers. The copy is warm, conversational, and uses "free" as a friction reducer. This ad has been running since at least March 2026 (3+ months), suggesting strong performance.

### Sample 2: beehiiv — Employer Brand as Growth Channel

> **Headline:** "cmo @ beehiiv | ex-Calendly"
> **CTA:** "Promoted by beehiiv"
> **Platform:** LinkedIn | **Format:** Single Image Ad
> **Link:** [LinkedIn Ad Library](https://www.linkedin.com/ad-library/detail/1427598643)

**Analysis:** beehiiv is running 409 active LinkedIn ads, and virtually all of them are employee spotlight cards. This is an unusual strategy — using paid LinkedIn to amplify employee personal brands. It builds credibility ("our CMO came from Calendly") while making beehiiv appear as a desirable employer. Low-cost creative production with potentially high brand ROI.

### Sample 3: Meta for Business — AI Automation Positioning

> **Headline:** "Meta Advantage+ Suite helps automate campaign optimisation - so your team can spend less time running in circles, and more time driving results."
> **CTA:** "Stop mistaking constant motion for real performance progress"
> **Platform:** LinkedIn | **Format:** Single Image Ad
> **Link:** [LinkedIn Ad Library](https://www.linkedin.com/ad-library/detail/1314092864)

**Analysis:** Meta is aggressively pushing AI-powered ad tools on LinkedIn, targeting media buyers and agency professionals. The copy is aspirational with a hint of challenge ("stop mistaking constant motion for real progress"). With 608 total active ads, Meta for Business is the second-largest advertiser in our tracker. Their strategy of running massive variant volumes with consistent themes mirrors best-in-class performance marketing.

---

## Appendix: Data Sources & Methodology

| Source | Status | Notes |
|---|---|---|
| Meta Ad Library (ScrapeCreators) | FAILED (HTTP 402) | Account out of API credits |
| Meta Marketing API (TLDR) | SUCCESS | Full 30-day account summary + campaigns |
| Google Ads API (TLDR) | FAILED | OAuth token expired/deleted |
| Competitive Tracker (Playwright) | SUCCESS | 79 ads across LinkedIn for 6 competitors |
| Google Ads Transparency | No results | No competitor ads found via Playwright |
| TikTok Ad Library | No results | No competitor ads found via Playwright |
| X/Twitter Ad Library | No results | No competitor ads found via Playwright |
| Historical CSV Data | Available | March 2026 baseline from prior audits |

**API fixes applied this cycle:**
- Updated `fb_ad_library_api.py` from deprecated ScrapeCreators v2 endpoints to current v1 (`/v1/facebook/adLibrary/search/companies` and `/v1/facebook/adLibrary/company/ads`)
