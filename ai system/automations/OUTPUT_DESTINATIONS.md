# Where to Find Automation Outputs

Outputs go to **two places**: (1) **workspace/repo paths** (files in the run environment, e.g. `docs/...`), and (2) **Google Drive** (Docs and Sheets), when those APIs are used. When the automation runs in the **cloud**, workspace files are written in the cloud clone; they appear in your **local repo** or **GitHub** only if the run commits and pushes (or if Cursor surfaces run artifacts). Google Docs/Sheets appear in the Google Drive folder you configured (`DRIVE_FOLDER_ID_DOCS`, `DRIVE_FOLDER_ID_SHEETS`).

---

## By automation

| # | Automation | Workspace / repo output paths | Google Drive output |
|---|------------|-------------------------------|---------------------|
| **1** | Daily Content Pipeline Orchestrator | • `docs/competitor content tracker/blogs/competitor_content_tracker.csv` (updated)<br>• `docs/competitor content tracker/blogs/content_pipeline.csv` (updated)<br>• Fallback: `docs/analytics_reports/daily_pipeline_summary_YYYY-MM-DD.md` | **Sheet:** "Content Pipeline Daily Log" (in your Sheets folder) |
| **2** | Weekly Content Execution + Repurposing Chain | • `docs/blogs/YYYY-MM-DD/*.md` (blog posts)<br>• `docs/content_assets/repurposed/` (repurposed assets)<br>• `docs/content_assets/repurposed/video_script_*.md`<br>• Fallback: `docs/content_assets/weekly_review_YYYY-MM-DD.md` | **Doc:** "Hostfully Weekly Content Review - YYYY-MM-DD" (in your Docs folder) |
| **3** | Monthly Competitive Ad Intelligence | • `docs/competitor content tracker/paid ads creatives/ad_creative_log.csv` (updated)<br>• `docs/competitor content tracker/paid ads creatives/ad_volume_tracker.csv` (updated)<br>• Fallback: `docs/competitor content tracker/competitive_brief_YYYY-MM.md` | **Doc:** "Competitive Ad Intelligence - MONTH YEAR" |
| **4** | Weekly Ad Performance Dashboard | • Fallback: `docs/analytics_reports/weekly_ad_performance_YYYY-MM-DD.md` | **Sheet:** "Hostfully Ad Performance Tracker"<br>**Doc:** "Hostfully Ad Performance - Week of DATE" |
| **5** | Weekly SEO Intelligence Report | • Fallback: `docs/analytics_reports/seo_intelligence_YYYY-MM-DD.md` | **Doc:** "Hostfully SEO Intelligence - Week of DATE" |
| **6** | Bi-Weekly Advertiser Health Monitor | • `docs/advertiser_success/health_reports/` (CSV + action plan from script)<br>• Fallback: `docs/advertiser_success/health_reports/biweekly_YYYY-MM-DD.md` | **Sheet:** "Advertiser Health Tracker"<br>**Doc:** "Advertiser Health Report - DATE" |
| **7** | Weekly Sales Intelligence Package | • `docs/sales_assets/prospect_lists/`<br>• `docs/sales_assets/battlecards/`<br>• Fallback: `docs/sales_assets/weekly_intelligence_YYYY-MM-DD.md` | **Sheet:** "Hostfully Prospect Pipeline"<br>**Doc:** "Sales Intelligence - Week of DATE" |
| **8** | Weekly CRO + Landing Page Audit | • `docs/cro_reports/screenshot_*.png` (Playwright screenshots)<br>• Fallback: `docs/cro_reports/weekly_audit_YYYY-MM-DD.md` | **Doc:** "Hostfully CRO Audit - Week of DATE" |
| **9** | Monthly GTM Execution Commander | • (Script outputs depend on gtm_commander; may write to docs)<br>• Fallback: `docs/GTM playbook/gtm_retro_YYYY-MM.md`, `docs/GTM playbook/gtm_plan_YYYY-MM.md` | **Doc:** "GTM Retrospective - PREV_MONTH YEAR"<br>**Doc:** "GTM Sprint Plan - CURRENT_MONTH YEAR" |
| **10** | Monthly Competitor Convergence Report | • Fallback: `docs/competitor content tracker/convergence_report_YYYY-MM.md` | **Doc:** "Competitor Convergence Report - MONTH YEAR" |

---

## Where you actually find them

### Google Drive (Docs & Sheets)

- **Docs:** In the Google Drive folder whose ID is set as **`DRIVE_FOLDER_ID_DOCS`** in your Configured Environment. Open that folder in Drive; look for the doc titles in the table (e.g. "Hostfully SEO Intelligence - Week of 2026-03-10").
- **Sheets:** In the folder set as **`DRIVE_FOLDER_ID_SHEETS`**. Look for "Content Pipeline Daily Log", "Hostfully Ad Performance Tracker", "Advertiser Health Tracker", "Hostfully Prospect Pipeline".

### Workspace / repo files (`docs/` and others)

- **When runs are in the cloud:** Files are written inside the run’s workspace (the cloned repo). You will see them:
  - In **Cursor’s run log or artifacts** for that automation run, if Cursor exposes them, or
  - In your **GitHub repo** (e.g. `hostfully`), **only if** the automation is set up to commit and push after the run. By default, the prompts do not add a “commit and push” step.
- **If you want these in GitHub or locally:** Either (a) add a final step to the automation that commits and pushes the changed files, or (b) run the same scripts locally so they write into your local `docs/` and you can push yourself.

### Fallback paths

When the Google Docs or Sheets API fails, the instructions tell the agent to save locally at the “Fallback” paths in the table (e.g. `docs/analytics_reports/seo_intelligence_YYYY-MM-DD.md`). Those are still workspace paths in the run environment; same as above for where you find them (run artifacts or after commit/push).

---

## Quick reference: folders under `docs/`

| Folder | Used by automations |
|--------|----------------------|
| `docs/analytics_reports/` | 1 (fallback), 4 (fallback), 5 (fallback) |
| `docs/blogs/` | 2 |
| `docs/competitor content tracker/` (blogs + paid ads creatives) | 1, 3, 9, 10 |
| `docs/content_assets/repurposed/` | 2 |
| `docs/cro_reports/` | 8 |
| `docs/advertiser_success/health_reports/` | 6 |
| `docs/sales_assets/` (prospect_lists, battlecards) | 7 |
| `docs/paid_ads_assets/` | 8 (read), 10 (read) |
| `docs/GTM playbook/` | 9 (fallback) |

All paths are relative to the **repository root** (the `hostfully` repo).
