# Automation QA and What’s Left for Full Functionality

This doc covers: (1) what’s still remaining to be fully functional, (2) how to QA that scripts run as defined, (3) how to QA output content, and (4) how to QA that outputs reach the right destinations.

---

## 1. What’s still remaining

Use this checklist. Details live in **VERIFICATION_AND_NEXT_STEPS.md** and **ENV_SETUP.md**.

| Item | Status / action |
|------|------------------|
| **All 10 automations created** in cursor.com/automations with correct name, schedule, repo, branch | Create any missing; Instructions = body only (no frontmatter). |
| **Instructions** | Paste only from `# Title` to end of each `0X_....md`. Never include the `---` frontmatter. |
| **Configured Environment** | All required API keys and vars set (Sheets, Docs, Meta, Google Ads, Ahrefs, ScrapeCreators, LLM keys). See **ENV_SETUP.md**. |
| **Use Configured Environment** | Toggle ON for each automation. |
| **Timezone** | Confirm trigger times (08:00, 09:00, etc.) are in the timezone you want. |
| **Enabled** | All automations toggled On. |
| **Run Test passed** | At least once per automation (or a representative set) so env + repo + first steps are verified. |
| **Optional: commit/push after run** | By default, workspace files (e.g. `docs/...`) are written in the cloud run only. To see them in GitHub, add a final step that commits and pushes, or run scripts locally and push yourself. See **OUTPUT_DESTINATIONS.md**. |

Once the above are done, automations are **fully functional** for scheduled runs; remaining items are optional (GSC/GA4 live data, real advertiser CSVs, etc.).

---

## 2. QA that the scripts work as defined

Goal: confirm the **scripts and APIs** used by each automation run correctly before relying on scheduled runs.

### 2.1 Run from repo root with local `.env`

All commands below assume you’re in the **TLDR repo root** and have a working `.env` (same vars as Configured Environment). Load deps once:

```bash
cd "/path/to/TLDR"   # your repo root
pip install -r ai system/automations/lib/requirements.txt
```

### 2.2 Script QA by automation (smoke tests)

Run the **first API/script step** (or a minimal set) for each automation. If it runs and returns expected data, the script part is OK.

| # | Automation | What to run (smoke test) | Expected |
|---|------------|--------------------------|----------|
| **1** | Daily Content Pipeline | `python3 ai system/automations/lib/gsheets_api.py list` then `create --title "Content Pipeline Daily Log"` (or skip create if it exists) | JSON list of sheets; or new sheet created. |
| **2** | Weekly Content Execution | `python3 ai system/automations/lib/gdocs_api.py list` then `create --title "TLDR Weekly Content Review - 2026-03-10"` | JSON list of docs; or new doc created. |
| **3** | Monthly Competitive Ads | `python3 ai system/automations/lib/meta_ads_api.py account-summary --date-preset last_7d` (or fb_ad_library / ScrapeCreators if that’s step 1) | Meta account summary JSON or ad library data. |
| **4** | Weekly Ad Performance | `python3 ai system/automations/lib/meta_ads_api.py results-summary --date-preset last_7d` and `python3 ai system/automations/lib/google_ads_api.py account-summary --date-range LAST_7_DAYS` | Meta + Google Ads summary output. |
| **5** | Weekly SEO | `python3 ai system/automations/lib/ahrefs_api.py domain-rating --target tldr.tech` (or gsc_api search-analytics if GSC configured) | Ahrefs domain rating JSON or GSC data. |
| **6** | Bi-Weekly Advertiser Health | `python3 "ai system/python scripts/customer success agent/advertiser_health.py"` (with sample data in `data/advertiser_performance/`) | Health report or CSV output. |
| **7** | Weekly Sales Intelligence | `python3 ai system/automations/lib/gsheets_api.py list` and optionally run prospect_intelligence / battlecard scripts | Sheets list; script outputs if run. |
| **8** | Weekly CRO Audit | `python3 ai system/automations/lib/ahrefs_api.py domain-rating --target tldr.tech` and/or `python3 ai system/automations/lib/gsc_api.py search-analytics --start-date YYYY-MM-DD --end-date YYYY-MM-DD` (if GSC configured) | Ahrefs/GSC output; Playwright step needs browser in env. |
| **9** | Monthly GTM | `python3 ai system/automations/lib/gdocs_api.py list`; run gtm_commander script if present | Docs list; commander output. |
| **10** | Monthly Competitor Convergence | `python3 ai system/automations/lib/gdocs_api.py create --title "Convergence Test"` (then delete the test doc if you want) | Doc created in your Docs folder. |

If any command fails (auth, missing env, path error), fix that before trusting the automation. The **Run Test** in cursor.com/automations runs the **full** instructions (including agent steps); the table above is a quick **script/API** check.

### 2.3 Full flow QA (optional)

For one or two automations, run the **entire** automation via **Run Test** in the UI and watch the run log. Confirm:

- `pip install` and each `python3` step complete without errors.
- The agent follows the steps (e.g. lists files, calls APIs, writes content).  
Then check outputs (next section).

---

## 3. QA the output (content and structure)

Goal: confirm that **what** is produced matches the automation’s design (files, doc/sheet content, structure).

### 3.1 Workspace / repo outputs

After a Run Test or scheduled run, outputs under the repo are in the **run’s workspace** (cloud). You’ll see them in run artifacts if Cursor exposes them, or in GitHub if the run commits and pushes.

| Output type | What to check |
|-------------|----------------|
| **CSV updates** | e.g. `docs/competitor content tracker/blogs/content_pipeline.csv` — new rows, correct columns. |
| **Blog posts** | `docs/blogs/YYYY-MM-DD/*.md` — files exist, contain expected sections (title, body, meta). |
| **Repurposed assets** | `docs/content_assets/repurposed/*.md` — LinkedIn, email subjects, video script files. |
| **Fallback markdown** | e.g. `docs/analytics_reports/weekly_ad_performance_YYYY-MM-DD.md` — present when Docs/Sheets API is skipped or fails; has the expected sections. |

Use the **OUTPUT_DESTINATIONS.md** table (“Workspace / repo output paths”) for the exact paths per automation.

### 3.2 Google Docs output

- Open the **Doc** (from Drive or from the run log link). Check:
  - **Title** matches the pattern (e.g. “TLDR Weekly Content Review - 2026-03-10”, “TLDR SEO Intelligence - Week of …”).
  - **Content** matches the instructions: sections, bullet lists, data (dates, numbers, file paths) that the automation was supposed to insert.

### 3.3 Google Sheets output

- Open the **Sheet** (from Drive or run log). Check:
  - **Title** (e.g. “Content Pipeline Daily Log”, “TLDR Ad Performance Tracker”).
  - **Headers** and **one or more data rows** with the expected columns (dates, metrics, etc.).

If content is empty or wrong, the issue is in the automation steps (agent didn’t substitute placeholders, or an API step failed and the agent didn’t fall back correctly). Re-run and inspect the run log.

---

## 4. QA that outputs go to the desired destinations

Goal: confirm that **where** outputs land matches your configuration (Drive folders and workspace paths).

### 4.1 Google Drive folders

Your **Configured Environment** (and `.env`) define:

- **Docs folder:** `DRIVE_FOLDER_ID_DOCS` (or `DEFAULT_GOOGLE_DOCS_FOLDER_ID`)
- **Sheets folder:** `DRIVE_FOLDER_ID_SHEETS` (or `DEFAULT_GOOGLE_SHEETS_FOLDER_ID`)

**QA steps:**

1. Resolve folder IDs to URLs (you can open the folder in Drive and copy the URL, or use the IDs you set).
   - Example Docs: `https://drive.google.com/drive/folders/<DRIVE_FOLDER_ID_DOCS>`
   - Example Sheets: `https://drive.google.com/drive/folders/<DRIVE_FOLDER_ID_SHEETS>`
2. After a run that creates a Doc or Sheet, open that folder and confirm:
   - A **new file** with the expected title (e.g. “TLDR Weekly Content Review - 2026-03-10”) appears in the **Docs** folder.
   - A **new sheet** (e.g. “Content Pipeline Daily Log” or “TLDR Ad Performance Tracker”) appears in the **Sheets** folder (or was updated if it already existed).

If files appear in a different folder or in “My Drive” root, the script is using the wrong folder ID or the env var isn’t set in the run environment. Fix the Configured Environment and re-run.

### 4.2 Workspace / repo paths

- **OUTPUT_DESTINATIONS.md** lists, per automation, the **workspace paths** (e.g. `docs/analytics_reports/...`, `docs/content_assets/repurposed/...`).
- In **cloud runs**, those paths are inside the run’s clone. To QA:
  - Check **Run History** (or artifacts) for that automation and confirm the listed paths exist and have content, or
  - If you added a “commit and push” step, pull the branch and check the same paths in your local repo.

### 4.3 Fallback paths

When the instructions say “if Google Docs/Sheets API fails, save to …”, the agent should write to the **fallback** path in OUTPUT_DESTINATIONS (e.g. `docs/analytics_reports/seo_intelligence_YYYY-MM-DD.md`). To QA fallback:

- Temporarily break the Docs or Sheets env (e.g. wrong folder ID or invalid token), run the automation, and confirm a file appears at the fallback path with the expected content. Then restore the env.

---

## 5. Quick QA checklist (copy and use)

- [ ] **Remaining setup:** All 10 automations exist; Instructions = body only; Configured Environment complete; timezone and Enabled confirmed.
- [ ] **Script QA:** Ran at least one script/API command per automation from repo root with `.env` (or Run Test) and got expected output.
- [ ] **Output content:** For 1–2 full runs, checked that generated Docs/Sheets and any workspace files have the right structure and data.
- [ ] **Destinations:** Confirmed new Docs appear in the Docs Drive folder and new/updated Sheets in the Sheets Drive folder; workspace paths match OUTPUT_DESTINATIONS.md.
- [ ] **Optional:** Tested fallback path by forcing a Docs/Sheets failure and checking the fallback file is created.

Once this checklist is done, automations are QA’d for script behavior, output content, and delivery to the desired destinations. For full paths and env details, keep using **OUTPUT_DESTINATIONS.md**, **ENV_SETUP.md**, and **VERIFICATION_AND_NEXT_STEPS.md**.
