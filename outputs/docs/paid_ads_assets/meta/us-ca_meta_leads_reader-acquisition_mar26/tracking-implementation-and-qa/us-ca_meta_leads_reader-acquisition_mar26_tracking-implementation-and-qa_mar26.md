---
title: "Tracking Implementation & QA – us-ca_meta_leads_reader-acquisition_mar26"
campaign: "us-ca_meta_leads_reader-acquisition_mar26"
agent: "analytics-tracking-agent"
status: "Draft"
date_created: "2026-03-16"
---

# Tracking Implementation & QA – TLDR Reader Acquisition (Meta)

Output of the **analytics-tracking-agent** for the `us-ca_meta_leads_reader-acquisition_mar26` campaign. This document specifies required events, UTMs, data flow, and QA steps.

---

## 1. Event Architecture

### 1.1 Meta Events

- **PageView** – all pages.
- **ViewContent (optional)** – newsletter signup page view.
- **Lead / CompleteRegistration / custom `newsletter_subscribe`** – fired on signup completion (thank-you page).

Recommended:

- Use a **custom event** name like `newsletter_subscribe` mapped to `Lead` or `CompleteRegistration` in Events Manager.
- Configure this event as **primary** or high-priority in Aggregated Event Measurement.

### 1.2 GA4 Events

- `page_view` – default.
- `newsletter_view` – newsletter landing page (optional).
- `newsletter_subscribe` – on successful signup (align with Meta event).

Parameters for `newsletter_subscribe`:

- `source`
- `medium`
- `campaign`
- `content`
- `term`
- `page_location`

### 1.3 Internal / CRM Fields

At minimum, capture and store with each subscriber:

- `utm_source`
- `utm_medium`
- `utm_campaign`
- `utm_term`
- `utm_content`
- `first_touch_at`
- `signup_landing_url`

---

## 2. UTM & URL Configuration

### 2.1 Ad-Level Parameters

All Meta ads in this campaign should use:

```text
?utm_source=facebook&utm_medium=paid-social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}&utm_term={{adset.name}}
```

Rules:

- All lowercase.
- Hyphens for separators within values; no spaces.
- Applied consistently to every destination URL.

### 2.2 Landing Page Handling

On the landing page:

- Read UTMs from the query string.
- Store them in:
  - First-party cookie or session storage (for multi-page paths).
  - Hidden form fields bound to newsletter signup.
- When the form submits, pass UTM values along to:
  - Backend subscription service.
  - CRM or ESP (e.g., fields like `ft_utm_source`, `ft_utm_campaign`).

---

## 3. Pixel, CAPI, and GA4 Implementation

### 3.1 Meta Pixel

- Ensure the base Pixel code is loaded via:
  - Direct script on the page, or
  - Google Tag Manager (recommended).
- Fire `newsletter_subscribe` (or chosen event) when:
  - Thank-you page loads, or
  - Form submission callback confirms success (avoid double-fires).

### 3.2 Conversions API (CAPI)

- Implement via:
  - GTM server-side, or
  - Native partner integration.
- Use the same `event_id` for:
  - Browser (Pixel) event.
  - Server-side CAPI event.
- Send:
  - Event name, time, event_id.
  - Hashed identifiers (email).
  - UTM parameters if available.

### 3.3 GA4

- Implement via GA4 tag in GTM.
- Trigger `newsletter_subscribe`:
  - On same condition as Meta conversion event (thank-you page or successful submit).
- Map UTMs into GA4 for analysis; ensure default channel grouping recognizes `paid-social`.

---

## 4. QA Checklist

### 4.1 UTM QA

- [ ] Click a preview of each Meta ad.
- [ ] Verify final landing URL contains full UTM string.
- [ ] Navigate within the site, then convert; confirm:
  - UTM values persisted and were attached to the submission.
- [ ] Check that internal links do **not** carry UTMs.

### 4.2 Pixel & CAPI QA

- [ ] Use Events Manager **Test Events**:
  - Load landing page → confirm Pixel events appear.
  - Complete signup → confirm `newsletter_subscribe` received.
- [ ] Verify CAPI events appear with matching `event_id`.
- [ ] Confirm no duplicate events (one browser + one server, deduped).

### 4.3 GA4 QA

- [ ] Open GA4 Realtime:
  - Click ad preview → confirm active user from `source=facebook`, `medium=paid-social`.
- [ ] Complete signup:
  - Confirm `newsletter_subscribe` event in Realtime stream.
- [ ] Later, verify in standard reports:
  - Conversions attributed to `facebook / paid-social` for this campaign.

### 4.4 CRM / ESP QA

- [ ] Submit a test lead via the live form.
- [ ] In the CRM/ESP:
  - Confirm UTM fields populated.
  - Confirm email address, timestamp, and campaign tags look correct.
- [ ] Trace a record through to downstream stages (if applicable) to ensure attribution is preserved.

---

## 5. Reporting Hooks for Downstream Agents

To support weekly ad performance and paid_ads_intelligence_agent:

- Ensure all campaign names, ad set names, and ad names follow the conventions used in:
  - `us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md`.
- Confirm:
  - Reporting scripts can filter by `campaign.name` matching `us-ca_meta_leads_reader-acquisition_mar26`.
  - GA4 and CRM exports include the UTM values specified here.

