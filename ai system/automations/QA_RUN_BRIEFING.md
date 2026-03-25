# Automation QA Run Briefing

**Date:** 2026-03-15  
**Scope:** Smoke tests per `ai system/automations/QA_AND_REMAINING.md` (script/API checks for all 10 automations).

---

## Summary

| # | Automation | Smoke test result | Status |
|---|------------|-------------------|--------|
| 1 | Daily Content Pipeline Orchestrator | `gsheets_api.py list` | **OK** — Sheets list returned. |
| 2 | Weekly Content Execution and Repurposing Chain | `gdocs_api.py list` | **OK** — Docs list returned. |
| 3 | Monthly Competitive Ad Intelligence | `meta_ads_api.py account-summary` | **OK** — Meta account summary returned. |
| 4 | Weekly Ad Performance Dashboard | Meta `results-summary` **OK**. Google Ads `account-summary` | **FAIL** — Google Ads API returned HTTP 404. |
| 5 | Weekly SEO Intelligence Report | `ahrefs_api.py domain-rating` | **FAIL** — Ahrefs API returned HTTP 401 Unauthorized. |
| 6 | Bi-Weekly Advertiser Health Monitor | `advertiser_health.py` | **DEGRADED** — Script runs and writes CSV + action plan; Anthropic API returned "credit balance too low" (LLM analysis skipped). |
| 7 | Weekly Sales Intelligence Package | `gsheets_api.py list` | **OK** — Same as #1. |
| 8 | Weekly CRO + Landing Page Audit | `gsc_api.py search-analytics` | **NOT CONFIGURED** — GSC_SITE_URL not set; automations 5/8 use mock/sitemap fallback when GSC unset. |
| 9 | Monthly GTM Execution Commander | `gdocs_api.py list` | **OK** — Same as #2. |
| 10 | Monthly Competitor Convergence Report | `gdocs_api.py create` | **OK** — Test doc created in Docs folder. |

---

## Components not working (or degraded)

### 1. Google Ads API (Automation 4 — Weekly Ad Performance)

- **Symptom:** `python3 ai system/automations/lib/google_ads_api.py account-summary --date-range LAST_7_DAYS` returns **HTTP 404**.
- **Likely causes:** Invalid or inaccessible `GOOGLE_ADS_CUSTOMER_ID`, or account under an MCC without `GOOGLE_ADS_MANAGER_ID` set. 404 can also indicate wrong API version or resource path.
- **Action:** Verify `GOOGLE_ADS_CUSTOMER_ID` (format 123-456-7890). If the account is under a Manager (MCC), set `GOOGLE_ADS_MANAGER_ID` in `.env` to the manager account ID. Confirm the customer ID has API access in Google Ads.

### 2. Ahrefs API (Automations 1, 5, 7, 8, 9, 10 — SEO and content pipeline steps)

- **Symptom:** `python3 ai system/automations/lib/ahrefs_api.py domain-rating --target tldr.tech` returns **HTTP 401 Unauthorized**.
- **Likely cause:** `AHREFS_API_KEY` in `.env` is placeholder or invalid/expired.
- **Action:** Replace with a valid Ahrefs API key (Ahrefs account → API section). Ensure the key has the required endpoints enabled.

### 3. ScrapeCreators / Meta Ad Library (Automations 3, 7, 10)

- **Symptom:** `python3 ai system/automations/lib/fb_ad_library_api.py search --brand "TLDR"` returns **HTTP 404** on `/v2/meta-ad-library/search-page`.
- **Likely cause:** ScrapeCreators API endpoint or version changed, or plan does not include this endpoint.
- **Action:** Check ScrapeCreators docs/dashboard for current base URL and endpoints; update `ai system/automations/lib/fb_ad_library_api.py` if the API has moved. Confirm your plan includes Meta Ad Library access.

### 4. Anthropic API — credit balance (Automation 6 and any agent using Claude)

- **Symptom:** Advertiser health script ran but reported: **"Your credit balance is too low to access the Anthropic API"**. CSV and action plan files were still generated; LLM-based analysis was skipped.
- **Impact:** Automation 6 (and any automation/agent that calls Anthropic) will have degraded or failing LLM steps until credits are added.
- **Action:** Add credits or upgrade plan at Anthropic (Plans & Billing). No code change required.

### 5. Google Search Console (Automations 5, 8 — optional)

- **Symptom:** `gsc_api.py search-analytics` exits with **"GSC_SITE_URL not set in .env"**.
- **Impact:** By design, automations 5 and 8 use mock data or sitemap-only fallbacks when GSC is not configured. So they still run; only live GSC data is missing.
- **Action:** To use live GSC data: set `GSC_SITE_URL` (e.g. `https://tldr.tech`) and `GOOGLE_APPLICATION_CREDENTIALS` (path to GSC service account JSON) in `.env`. See `docs/GSC_GA4_SETUP.md`.

---

## What is working

- **Google Sheets** (automations 1, 4, 6, 7): list and create OK.
- **Google Docs** (automations 2, 3, 4, 5, 6, 7, 8, 9, 10): list and create OK.
- **Meta Ads** (automations 3, 4, 6, 9): account-summary and results-summary OK.
- **Advertiser health script** (automation 6): runs and writes files; only LLM step is blocked by Anthropic credits.

---

## Recommended fix order

1. **Anthropic credits** — Restore LLM steps for automation 6 and any other Claude-using agents.
2. **Ahrefs API key** — Restore SEO and content-pipeline steps that depend on Ahrefs.
3. **Google Ads** — Fix customer/manager ID or API access so automation 4’s Google Ads step succeeds.
4. **ScrapeCreators** — Align `fb_ad_library_api.py` with current ScrapeCreators API (or confirm plan includes the endpoint).
5. **GSC (optional)** — Configure for live search data in automations 5 and 8 if desired.

---

## QA doc correction

In `QA_AND_REMAINING.md`, the smoke test for automations 5 and 8 was updated: the Ahrefs command is **`domain-rating --target tldr.tech`** (there is no `overview` subcommand). GSC requires **`search-analytics --start-date YYYY-MM-DD --end-date YYYY-MM-DD`**.
