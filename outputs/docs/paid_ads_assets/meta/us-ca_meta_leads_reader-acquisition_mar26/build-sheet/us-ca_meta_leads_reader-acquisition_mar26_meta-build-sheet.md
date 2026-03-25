---
title: "Meta Build Sheet – us-ca_meta_leads_reader-acquisition_mar26"
campaign: "us-ca_meta_leads_reader-acquisition_mar26"
platform: "Meta (Facebook + Instagram)"
objective: "Leads – Newsletter Signups"
status: "Draft"
---

# Meta Build Sheet – `us-ca_meta_leads_reader-acquisition_mar26`

Field-by-field instructions to build the TLDR reader-acquisition campaign in Meta Ads Manager, based on the campaign structure and ad-creative files.

Companion docs:
- Campaign structure: `us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md`
- Ad creative: `us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md`
- Creative briefs: `creative-briefs/mar26/`

---

## 1. Prerequisites

- Meta Business Manager and ad account with billing set up.
- TLDR Pixel installed on:
  - Newsletter signup landing page (`/signup` or equivalent).
  - Thank-you / confirmation page.
- Conversion event configured:
  - `Subscribe` or `CompleteRegistration` firing on the thank-you page.
  - Event added to Aggregated Event Measurement with appropriate priority.
- Landing page live, fast, and mobile-optimized.

---

## 2. Create the Campaign

1. In Ads Manager, click **Create**.
2. Choose **Leads** as the campaign objective.
3. Click **Continue**.
4. In the **Campaign** tab:
   - **Campaign name**: `us-ca_meta_leads_reader-acquisition_mar26`
   - **Buying type**: Auction.
   - **A/B Test**: Off (run tests via naming + reporting).
   - **Campaign budget optimization (CBO)**: Off (we are starting with ad set budgets / ABO).
   - **Special ad categories**: None.
5. Save the campaign.

---

## 3. Create Ad Sets (ABO)

From the campaign view, click **New ad set** and configure each of the four ad sets below.

### Ad Set 1 – Broad / Advantage+ Audience

- **Ad set name**: `broad_advantageplus_readers_prospecting`
- **Conversion location**: Website.
- **Pixel & event**:
  - Select the TLDR Pixel.
  - Choose `Subscribe` / `CompleteRegistration` as the conversion event.
- **Dynamic creative**: Off (we’ll control variants explicitly).
- **Budget & schedule**:
  - Daily budget: **$120**.
  - Schedule: Start date = desired launch; end date = none (ongoing).
- **Audience**:
  - Locations: United States, Canada.
  - Age: 22–55.
  - Gender: All.
  - Advantage+ Audience: **On**.
    - Hard controls: location + age.
    - Suggestions: interests like technology, startups, AI, software, business, productivity.
- **Custom audiences (exclusions)**:
  - Exclude existing subscribers (customer list).
  - Exclude recent converters (thank-you page visitors / conversion event).
- **Placements**:
  - Choose **Advantage+ placements (recommended)**.
- **Optimization & delivery**:
  - Optimization goal: Conversions.
  - Conversion window: 7-day click, 1-day view (per account defaults).

### Ad Set 2 – Interest Stack (Tech & Business)

- **Ad set name**: `interests_tech-biz-news_prospecting`
- Duplicate Ad Set 1 and then edit:
  - **Budget**: set to **$90/day**.
  - **Audience**:
    - Keep locations, age, gender the same.
    - Turn **Advantage+ Audience** off.
    - In Detailed Targeting, add interests such as:
      - Technology
      - Startups
      - Online advertising
      - Software as a service (SaaS)
      - Business and industry
      - Entrepreneurship
    - Turn **Detailed targeting expansion** off.
  - Keep exclusions, placements, and optimization the same.

### Ad Set 3 – Lookalike of Subscribers (1%)

- **Ad set name**: `lal_subscribers-1pct_usca_prospecting`
- Duplicate Ad Set 1 and then edit:
  - **Budget**: set to **$80/day**.
  - **Audience**:
    - Remove Advantage+ Audience.
    - Add a **Lookalike audience** based on:
      - Source: customer list of existing TLDR newsletter subscribers (or high-quality “newsletter_signup” custom audience).
      - Location: United States and Canada.
      - Size: 1%.
    - Age: 22–55, Gender: All.
  - Keep exclusions, placements, and optimization the same.

### Ad Set 4 – Warm Retargeting

- **Ad set name**: `retargeting_site-visitors30_engagers90`
- Duplicate any existing ad set and then edit:
  - **Budget**: set to **$40/day**.
  - **Audience**:
    - Clear existing targeting.
    - Add custom audiences:
      - Website visitors (last 30 days) – all site visitors.
      - Facebook Page engagers (last 90 days).
      - Instagram profile engagers (last 90 days).
    - Exclude:
      - Recent converters (thank-you page visitors / conversion event).
      - Existing subscriber list.
    - Keep locations (US, CA) and age (22–55) as defaults if required.
  - **Placements**: keep Advantage+ placements on.

Verify total daily budget across ad sets ≈ **$330/day**.

---

## 4. Create Ads

For each ad set, create multiple ads using the creative IDs and copy from the ad-creative and visual-brief files.

### Common Settings

For all ads:

- **Ad name pattern**: `{format}_{hook}_{date}_{version}`  
  Examples:
  - `static_time-saved_mar26_v1`
  - `static_social-proof_mar26_v1`
  - `static_discovery-tools_mar26_v1`
  - `static_noise-vs-signal_mar26_v1`
- **Identity**:
  - Use the main TLDR Facebook Page and linked Instagram account.
- **Destination**:
  - Website URL: `https://tldr.newsletter/signup` (or your live signup URL).
  - URL parameters (add once; Meta will append dynamically):
    - `?utm_source=facebook&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}`
- **Call to action**:
  - Button: **Sign Up**.

### Map Creative to Ad Sets

Use at least 3–5 ads per ad set:

- `broad_advantageplus_readers_prospecting`:
  - `static_time-saved_mar26_v1`
  - `static_social-proof_mar26_v1`
  - `static_noise-vs-signal_mar26_v1`
- `interests_tech-biz-news_prospecting`:
  - `static_discovery-tools_mar26_v1`
  - `static_time-saved_mar26_v1`
  - `static_social-proof_mar26_v1`
- `lal_subscribers-1pct_usca_prospecting`:
  - `static_social-proof_mar26_v1`
  - `static_discovery-tools_mar26_v1`
- `retargeting_site-visitors30_engagers90`:
  - Warm variants from the creative file:
    - `static_retarg-social-proof_mar26_v1`
    - `static_retarg-fomo_mar26_v1`

For each ad:

1. **Upload image** according to its visual-creative-brief file in `creative-briefs/mar26/`.
2. **Primary text**:
   - Copy from the corresponding section in `us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md` (prospecting or retargeting version depending on ad set).
3. **Headline**:
   - Choose one of the headline options associated with that angle.
4. **Description** (optional):
   - Use the short description from the creative file.

---

## 5. Tracking & QA

Before publishing:

1. Use **Preview** to send each ad to your phone.
2. Click through and confirm:
   - Landing page loads quickly and correctly on mobile.
   - URL includes UTMs and correct query string.
3. In Events Manager, use **Test Events** to:
   - Trigger a test page view and signup.
   - Confirm Meta receives the `Subscribe` / `CompleteRegistration` event.
4. In GA4, verify:
   - Session from `source=facebook` / `medium=paid-social`.
   - Conversion event logged after form submission.

---

## 6. Launch & First Optimization Loop

After launch:

- Let the campaign run for at least **7 days** with minimal changes.
- Monitor:
  - Spend per ad set.
  - CTR, conversion rate, and CPA per ad + ad set.
- Turn off:
  - Creative that underperforms significantly after a reasonable number of impressions (e.g., 2k–3k impressions) relative to peers.
- Reallocate budget:
  - Gradually shift budget from weak audiences to strong ones (e.g., from broad to LAL or vice versa depending on data).

Once stable performance is reached and you have consistent weekly conversions:

- Consider:
  - Enabling CBO with a campaign-level budget.
  - Testing **Cost Cap** bidding with a target slightly above your current blended CPA.

