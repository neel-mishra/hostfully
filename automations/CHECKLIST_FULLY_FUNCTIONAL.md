# Making All 10 Automations Fully Functional

## Do I need to create these in cursor.com/automations?

**Yes.** The `.md` files in this folder are **prompt instructions** for the Cursor Automation agent. They do not run by themselves. To have them run on a schedule you must:

1. Go to **[cursor.com/automations](https://cursor.com/automations)** and sign in.
2. For **each** of the 10 automations, click **New Agent** (or similar).
3. **Name** — use the `name` from the frontmatter (e.g. "Daily Content Pipeline").
4. **Trigger** — Add Trigger → Schedule → set the day/time from the frontmatter (e.g. Daily 08:00, Weekly Monday 09:00).
5. **Instructions** — Copy the **entire contents** of the corresponding `.md` file (from the `#` title down to the end, including all code blocks and steps) into the automation’s Instructions / Prompt.
6. **Environment** — Turn **Use Configured Environment** ON and add the required API keys and variables (see below).
7. **Enable** the automation.

The workspace scripts (`automations/lib/*.py`, `python scripts/...`) are what the agent runs when it executes the instructions. The agent runs in the **cloud** with access to your workspace (or a linked repo), so those scripts must be present where the automation runs and dependencies must be installable (`pip install -r automations/lib/requirements.txt`).

---

## What is missing for each automation to be fully functional?

### 1. Create the 10 automations in the UI

| # | File | Name (from frontmatter) | Schedule |
|---|------|-------------------------|----------|
| 1 | `01_daily_content_pipeline.md` | Daily Content Pipeline Orchestrator | Daily 08:00 |
| 2 | `02_weekly_content_execution.md` | Weekly Content Execution + Repurposing Chain | Weekly Mon 09:00 |
| 3 | `03_monthly_competitive_ads.md` | Monthly Competitive Ad Intelligence | Monthly 28th |
| 4 | `04_weekly_ad_performance.md` | Weekly Ad Performance Dashboard | Weekly Mon 07:00 |
| 5 | `05_weekly_seo_intelligence.md` | Weekly SEO Intelligence Report | Weekly Tue 08:00 |
| 6 | `06_biweekly_advertiser_health.md` | Bi-Weekly Advertiser Health Monitor | Every other Mon 10:00 |
| 7 | `07_weekly_sales_intelligence.md` | Weekly Sales Intelligence Package | Weekly Wed 08:00 |
| 8 | `08_weekly_cro_audit.md` | Weekly CRO + Landing Page Audit | Weekly Thu 09:00 |
| 9 | `09_monthly_gtm_commander.md` | Monthly GTM Execution Commander | Monthly 1st |
| 10 | `10_monthly_competitor_convergence.md` | Monthly Competitor Creative + Content Convergence Report | Monthly 5th |

---

### 2. Configure environment variables (one place powers all)

Set these in **Cursor Automations → Manage → Configured Environment** (and/or in the workspace `.env` so local runs work). The agent runs in the cloud, so **Cloud Agent Environment** is what matters for scheduled runs.

| Variable | Used by automations | Notes |
|----------|---------------------|--------|
| **AHREFS_API_KEY** | 1, 5, 7, 8, 9, 10 | Ahrefs API |
| **GSC_SITE_URL** | 5, 8 | e.g. `https://tldr.tech` — optional; scripts use mock if unset |
| **GOOGLE_APPLICATION_CREDENTIALS** | 5, 8 | Path to service account JSON — optional |
| **GA4_PROPERTY_ID** | (traffic scripts if used) | Optional |
| **GSHEETS_CLIENT_EMAIL** | 1, 4, 6, 7 | Google Sheets |
| **GSHEETS_PRIVATE_KEY** | 1, 4, 6, 7 | PEM string (often multiline in env) |
| **DRIVE_FOLDER_ID_SHEETS** | 1, 4, 6, 7 | Folder for new sheets |
| **GOOGLE_CLIENT_ID** | 2–10 | Google Docs OAuth |
| **GOOGLE_CLIENT_SECRET** | 2–10 | |
| **GOOGLE_REFRESH_TOKEN** | 2–10 | |
| **DRIVE_FOLDER_ID_DOCS** | 2–10 | Folder for new docs |
| **META_ACCESS_TOKEN** | 3, 4, 6, 9 | Meta Marketing API |
| **META_AD_ACCOUNT_ID** | 3, 4, 6, 9 | |
| **GOOGLE_ADS_*** | 3, 4, 6, 9 | Client ID, Secret, Developer Token, Refresh Token, Customer ID, etc. |
| **SCRAPECREATORS_API_KEY** | 3, 7, 10 | Meta Ad Library (ScrapeCreators) |
| **ANTHROPIC_API_KEY** | 2, 6, 7 | Blog humanizer, advertiser health, sales agents |
| **GEMINI_API_KEY** | 2, (others as needed) | Blog/social/content agents |
| **OPENROUTER_API_KEY** | 2 (social/video) | Optional |

Full list and where to get values: **`automations/lib/ENV_SETUP.md`** and **`docs/GSC_GA4_SETUP.md`**.

---

### 3. Date placeholders the agent must replace

The prompts tell the agent to use “today” or “this week”. Where you see placeholders, the **agent** is expected to substitute real values when it runs:

- **TODAY_DATE** / **90_DAYS_AGO_DATE** / **14_DAYS_AGO** — agent should compute from run date (e.g. `2026-03-10`).
- **DATE** / **WEEK_DATE** — e.g. week of `2026-03-10`.
- **MONTH YEAR** / **PREV_MONTH** / **CURRENT_MONTH** — e.g. `March 2026`, `February`, `March`.
- **CAMPAIGN_ID** / **PROSPECT_DOMAIN** / **COMPETITOR_DOMAIN** / **COMPANY_NAME** / **ADVERTISER_NAME** — agent fills from prior step output (e.g. from API or script results).

No code change is required for these; the automation instructions already say to replace them. If an automation fails, check that the agent is actually substituting dates and IDs from the context.

---

### 4. Script and data dependencies (already in workspace)

| Dependency | Status |
|------------|--------|
| `automations/lib/*.py` | Present (ahrefs, gsc, gsheets, gdocs, meta_ads, google_ads, fb_ad_library) |
| `python scripts/competitor scrapers/competitor-blog-scraper.py` | Present |
| `python scripts/content pipeline agent/planning/pipeline_agent.py` | Present |
| `python scripts/content pipeline agent/execution/execution_commander.py` | Present |
| `python scripts/content pipeline agent/repurposing/repurpose_agent.py` | Present |
| `python scripts/competitive creative tracker/competitive_tracker.py` | Present (path fixed in 03) |
| `python scripts/customer success agent/advertiser_health.py` | Present (needs `data/advertiser_performance/*.csv` for full run) |
| `python scripts/customer success agent/churn_analyzer.py` | Present |
| `python scripts/sales agent/prospect_intelligence.py` | Present |
| `python scripts/sales agent/battlecard_generator.py` | Present |
| `python scripts/cro and website intelligence agent/cro_hypothesis_agent.py` | Present |
| `python scripts/gtm execution commander/gtm_commander.py` | Present |
| Playwright (for 08) | `pip install playwright` + `playwright install chromium` in Step 1 of 08 |

Sample advertiser data under `data/advertiser_performance/` is present so automation 06 can run the health agent; replace with real data for production.

---

### 5. Optional vs required

- **Without any credentials**: Automations will fail at API steps (Ahrefs, Meta, Google, etc.) or use mock/fallback where we added it (e.g. GSC, GA4, advertiser health).
- **Minimum to “run without errors”**: Set at least the credentials used in the steps that run first (e.g. Ahrefs for 01/05, Meta/Google for 04, etc.). See table in section 2.
- **Fully functional**: Set all variables listed in **ENV_SETUP.md** (and GSC/GA4 if you want live search/traffic data). Then create all 10 automations in the UI with the correct schedule and instructions.

---

## Summary

| Gap | Action |
|-----|--------|
| Automations not created in UI | Create 10 agents at cursor.com/automations; paste each `.md` prompt; set schedule; enable. |
| Env vars not set in cloud | In Automations UI, open Configured Environment and add all keys from ENV_SETUP.md (and GSC_GA4_SETUP.md if using GSC/GA4). |
| Date/ID placeholders | No change needed; the agent is instructed to substitute dates and IDs when it runs. |
| Script paths | Fixed (e.g. 03 uses `competitive creative tracker` folder). |
| Advertiser / GSC / GA4 data | Optional: add real advertiser CSVs, GSC/GA4 credentials, for full behavior. |

Once the 10 automations exist in the UI and the configured environment has the required keys, updating credentials in that one place is enough for all scripts and automations that use them.
