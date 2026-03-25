# Paid Ads Intelligence — NLP Chat Implementation Plan

**Goal:** A Platon-style experience ([platonagent.ai](https://platonagent.ai/)): *“Every insight is one conversation away.”* You ask in plain language (e.g. “How did Meta perform in January?” or “Break down Google Ads by campaign for last month”) and get accurate performance data without opening Meta Ads Manager or Google Ads each time.

**Scope:** Google Ads + Meta Ads first. Output = conversational, on-demand answers with tables/summaries that you can trust.

---

## 1. How We Retrieve Performance Data

### 1.1 Recommendation: **Direct APIs** (not MCP) as the source of truth

| Criteria | Direct API (Meta Graph, Google Ads API) | MCP (user-meta_ads_portfolio, user-google_ads_portfolio) |
|----------|-------------------------------------------|----------------------------------------------------------|
| **Date range** | Full control: any `since`/`until` (e.g. Jan 1–31 2026). | Meta MCP in your setup only accepted presets (e.g. `last_30d`), not custom ranges — we couldn’t get August 2025. |
| **Accuracy** | Same data as the platforms when we call the same endpoints and use account-level or campaign-level insights consistently. | Depends on MCP implementation; we’d need to verify and possibly extend your MCPs to pass custom ranges and return raw metrics. |
| **Maintainability** | One codebase (your existing agent); we control fields, pagination, and logic. | Two surfaces: MCP server code + chat; harder to debug “wrong number” without tracing MCP. |
| **Lightest build** | Reuse and slim the current script into a **data + query layer**; chat calls that layer. | Chat calls MCP; to match platform numbers we’d still need to fix/extend MCPs and possibly duplicate logic. |

**Conclusion:** Use **direct APIs** for retrieving data. Keep the chat layer thin: it parses the user’s question (date range, platform, level, metrics) and calls your API-based data layer. If you later add MCP tools that **wrap the same API layer** (same code, same date handling), you can expose the same behavior via MCP without a second source of truth.

### 1.2 Meta Ads — retrieval

- **Endpoint:** Meta Marketing API (Graph API) `https://graph.facebook.com/v24.0/`.
- **Calls used today (keep these):**
  - **Account-level:** `GET act_{ad_account_id}/insights` with `time_range={since,until}` and fields: `spend`, `impressions`, `reach`, `clicks`, `actions`, `conversions` → gives the **single account-level row** Meta Ads Manager uses for the account.
  - **Campaign-level:** `GET act_{ad_account_id}/campaigns` with `insights` and same `time_range`; plus per-campaign `GET {campaign_id}/insights` so we have one row per campaign with spend, actions, conversions.
- **Lead/results logic:** Use **account-level** when available: take the `lead` value from the account-level `actions` array and the `spend` from that same insights row. If the account-level insights row is missing, fall back to summing campaign-level spend and campaign-level “lead” (one conversion event per campaign, standard over custom). That way we match Ads Manager when it shows one number for the account.
- **No MCP for Meta in the critical path:** Your Meta MCP doesn’t support custom date ranges today. So “retrieve performance data” = this API flow only. Optional later: MCP tool that calls this same logic with a `time_range` argument.

### 1.3 Google Ads — retrieval

- **Endpoint:** Google Ads API (REST), e.g. `v23` (or current supported version), with OAuth2 and developer token.
- **Calls used today (keep these):**
  - **Account-level:** GAQL over `customer` or `campaign` with `segments.date` in range → metrics: `metrics.cost_micros`, `metrics.conversions`, `metrics.clicks`, `metrics.impressions`, etc., for the chosen date range.
  - **Campaign-level:** Same API, break down by `campaign.id` / `campaign.name`; optional: ad group and keyword for “every possible angle.”
- **Accuracy:** Use the same metrics and date filter the Google Ads UI uses (e.g. “Results” = the conversion metric you care about; spend = cost). Store the GAQL and date range so we can document “Source: Google Ads API, 2026-01-01 to 2026-01-31.”
- **MCP:** Your Google Ads MCP has `get_account_summary(dateRange)` and campaign/keyword tools. If we confirm it accepts a custom `dateRange` and returns the same numbers as the UI, we could eventually call MCP from chat — but the **canonical source** should still be the same API semantics (same metrics, same date range) so the lightest accurate build is: one Google Ads API data layer, then chat (or MCP) calls that layer.

---

## 2. How We QA So You Don’t Have to Check the Platforms

### 2.1 One-time calibration (per account / per platform)

- Pick **2–3 date ranges** (e.g. last month, a full month in the past, and a week).
- For each range, record in the doc:
  - **Meta:** Account-level “Results” (leads) and “Amount spent” from Ads Manager (exact dates, account).
  - **Google:** Account-level cost and conversions (or your primary metric) from Google Ads UI (same dates).
- Run our data layer for the same ranges. Compare:
  - Meta: our `account_summary.data[0].spend` and the `lead` action value vs Manager.
  - Google: our account-level cost and conversions vs UI.
- Document the rule (e.g. “We use account-level insights only; if missing we use campaign sum”) and any known edge cases (e.g. optimization map failure → we fall back to campaign sum; document that so you know when to expect a mismatch).

### 2.2 Every response cites source and range

- Every answer from the chat should include a short line like:  
  **Source: Meta Ads API, account-level insights, 2026-01-01–2026-01-31.**  
  (And for Google: **Source: Google Ads API, 2026-01-01–2026-01-31.**)
- That way you can, when you want, open the platform for that exact range and spot-check. No guessing which date range or level we used.

### 2.3 Stored raw responses (optional but recommended)

- For each “pull” (platform + date range), store the raw API response (or a hash + key fields) in a small JSON or DB. If a number ever looks wrong, we can re-run the same request and compare, or show you the raw row we used for “amount spent” and “leads.”

### 2.4 Optional: reconciliation job

- A weekly or on-demand job that pulls the same range (e.g. “last 7 days”) and compares account-level spend (and leads if available) to the previous run or to a baseline. If the delta is beyond a threshold (e.g. >5% with no known change), flag for review. That keeps the build light but adds a safety net.

---

## 3. Lightest Accurate Build That Supports “Every Possible Angle”

### 3.1 Architecture (three layers)

1. **Data layer (APIs only)**  
   - **Meta:** One function: `get_meta_performance(since, until, level='account'|'campaign'|'campaign_with_ads')` returning normalized dict: account spend/leads/impressions/clicks and, if requested, list of campaigns (and optionally ad sets/ads) with the same metrics.  
   - **Google:** One function: `get_google_performance(since, until, level='account'|'campaign'|'ad_group'|'keyword')` returning normalized dict: account cost/conversions/clicks/impressions and, if requested, breakdown by campaign, ad group, or keyword.  
   - All dates as `YYYY-MM-DD`. No NLP here — only API calls and normalization.

2. **Query layer (no NLP, only “what to fetch”)**  
   - Input: structured request, e.g. `{ "platform": "meta"|"google", "since": "2026-01-01", "until": "2026-01-31", "level": "campaign", "metrics": ["spend", "leads", "impressions"] }`.  
   - Output: the same normalized structures + a **source tag** (e.g. “Meta Ads API, account-level, 2026-01-01–2026-01-31”).  
   - This is what the chat (or an MCP server) will call. One place to add validation (e.g. max date range) and logging.

3. **Chat / NLP layer**  
   - User types: “How did Meta do in January?” or “Google Ads by campaign for last month.”  
   - LLM (or a small classifier) parses: platform, date range, level (account vs campaign vs keyword), and which metrics.  
   - Calls the query layer with that structured request; gets back the data + source tag.  
   - LLM formats the answer in natural language + table and **always includes the source line** so you can QA.

### 3.2 “Every possible angle” without bloat

- **Angles we support from day one:**  
  - Account-level totals (spend, leads/conversions, impressions, clicks) for a date range.  
  - Campaign-level breakdown for that same range.  
  - (Optional) Meta: ad set / ad level; Google: ad group, keyword.  
- **How we keep it light:** We don’t pre-aggregate every possible slice. We only add **one more “level”** when needed (e.g. `level=keyword` for Google). The data layer stays a thin wrapper over the APIs; the query layer stays a single entry point; the chat only translates “by campaign” vs “by keyword” into the `level` parameter.  
- **Extending later:** New angles = new `level` or new metric in the same two API wrappers (Meta + Google). No new systems.

### 3.3 API vs MCP — final recommendation

- **Use API for data.** Implement the data layer and query layer above using direct Meta and Google Ads APIs. That gives you full control over dates, fields, and logic, and one place to QA and fix discrepancies (as we did for Meta account-level vs campaign-sum).
- **Use chat for the interface.** The “NLP chat” can be:  
  - Cursor + this repo (you ask in the chat; the AI has access to the query layer or to scripts that call it), or  
  - A small app (e.g. Streamlit or a simple backend) where you type a question and the app calls the query layer and an LLM to format the answer.  
- **MCP later, if useful.** Once the query layer is stable and calibrated, we can add MCP tools that call the **same** query layer (same functions, same date handling). Then the AI can use either “run script” or “call MCP” and get the same numbers. MCP then becomes just another client of the same source of truth, not a second implementation.

---

## 4. Summary Table

| Question | Answer |
|----------|--------|
| How do we retrieve Meta data? | Direct Meta Graph API: account-level insights + campaign-level insights with explicit `time_range`; use account-level spend and `lead` when present so we match Meta Ads Manager. |
| How do we retrieve Google data? | Direct Google Ads API (GAQL): account and campaign (and optionally ad group/keyword) for the same date range and metrics. |
| How do we QA accuracy? | (1) One-time calibration vs platform UI for 2–3 ranges; (2) every answer cites “Source: [API], [level], [date range]”; (3) optional stored raw responses; (4) optional reconciliation job. |
| API or MCP? | **API** for retrieval and as single source of truth; **chat** for NLP interface; **MCP** later only as a thin client to the same API-backed query layer if desired. |
| Lightest accurate build? | Three layers: **data** (Meta + Google API wrappers) → **query** (structured request → normalized data + source tag) → **chat** (NLP → query → formatted answer with source). Add levels (e.g. keyword) only when needed. |

---

## 5. Next Steps

1. **Lock the data contract:** Finalize the normalized output shape for Meta and Google (account + campaign, and optionally ad set/ad group/keyword) so the query layer has a stable interface.  
2. **Implement the query layer:** One module that accepts `platform`, `since`, `until`, `level`, and optional `metrics`, and returns the normalized dict + source tag; internally it calls the existing (or slimmed) Meta and Google API code.  
3. **Calibrate:** Run for 2–3 ranges and document “expected” account-level spend and leads/conversions vs platform; adjust logic if needed.  
4. **Add the chat:** Wire Cursor (or a small app) so that a natural-language question is parsed into a structured request, the query layer is called, and the answer is formatted with the source line.  
5. **(Optional)** Add MCP tools that call the same query layer so the same data is available via MCP without reimplementing retrieval.

This gives you a Platon-like experience (“ask and get exactly what you need”) with data you can trust and a single, auditable path from platform APIs to the numbers we show.
