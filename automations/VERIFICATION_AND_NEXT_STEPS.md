# Automation Setup Verification & What’s Left to Run on Cadence

## Setup verification

Confirm in **cursor.com/automations** that each automation matches this:

| # | Name | Trigger (schedule) | Repo | Branch |
|---|------|--------------------|------|--------|
| 1 | Daily Content Pipeline Orchestrator | Daily at 08:00 | `tldr` | main or cursor-automations |
| 2 | Weekly Content Execution + Repurposing Chain | Weekly Monday at 09:00 | `tldr` | same |
| 3 | Monthly Competitive Ad Intelligence | Monthly, last day of month at 08:00 | `tldr` | same |
| 4 | Weekly Ad Performance Dashboard | Weekly Monday at 07:00 | `tldr` | same |
| 5 | Weekly SEO Intelligence Report | Weekly Tuesday at 08:00 | `tldr` | same |
| 6 | Bi-Weekly Advertiser Health Monitor | Every other Monday at 10:00 | `tldr` | same |
| 7 | Weekly Sales Intelligence Package | Weekly Wednesday at 08:00 | `tldr` | same |
| 8 | Weekly CRO + Landing Page Audit | Weekly Thursday at 09:00 | `tldr` | same |
| 9 | Monthly GTM Execution Commander | Monthly 1st at 09:00 | `tldr` | same |
| 10 | Monthly Competitor Creative + Content Convergence Report | Monthly 5th at 08:00 | `tldr` | same |

- **Instructions:** Each automation’s Instructions field should contain the full prompt from the matching `0X_...md` file (from the `#` title through the end, including all code blocks).
- **Model:** A capable model for Automations (e.g. Opus 4.6 High or the recommended default).
- **Tools/MCP:** None added.
- **Trigger:** Repo = `tldr`, branch = the one you selected (e.g. `main` or `cursor-automations`).

If any of the above differ, update that automation in the UI to match.

---

## What you need to do so they run on cadence

### 1. Configured environment (required for steps that call APIs)

The agent runs in the cloud and needs API keys in **Configured Environment**, not your local `.env`.

- In cursor.com/automations, open **Configured Environment** (or the environment linked to these automations).
- Add the variables used by the scripts each automation runs. Minimum set:
  - **Ahrefs:** `AHREFS_API_KEY` (automations 1, 5, 7, 8, 9, 10)
  - **Google Sheets:** `GSHEETS_CLIENT_EMAIL`, `GSHEETS_PRIVATE_KEY`, `DRIVE_FOLDER_ID_SHEETS` (1, 4, 6, 7)
  - **Google Docs:** `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN`, `DRIVE_FOLDER_ID_DOCS` (2–10)
  - **Meta Ads:** `META_ACCESS_TOKEN`, `META_AD_ACCOUNT_ID` (3, 4, 6, 9)
  - **Google Ads:** `GOOGLE_ADS_CLIENT_ID`, `GOOGLE_ADS_CLIENT_SECRET`, `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_REFRESH_TOKEN`, `GOOGLE_ADS_CUSTOMER_ID` (3, 4, 6, 9)
  - **ScrapeCreators (Meta Ad Library):** `SCRAPECREATORS_API_KEY` (3, 7, 10)
  - **LLMs (for script steps that use them):** `GEMINI_API_KEY`, `ANTHROPIC_API_KEY` (2, 6, 7 and related scripts)
- Optional: `GSC_SITE_URL`, `GOOGLE_APPLICATION_CREDENTIALS` (5, 8) and GA4 vars if you want live GSC/GA4 data.

Full list and where to get values: **`automations/lib/ENV_SETUP.md`** and **`docs/GSC_GA4_SETUP.md`**.

Without these, any step that calls an API will fail; the rest of the prompt may still run.

### 2. Timezone for schedules

- Confirm the **timezone** for the trigger (e.g. “08:00” is in your intended zone, e.g. GMT+8 or your local).
- If the UI lets you set timezone per automation or globally, set it once so all “at 08:00” / “at 09:00” match when you want runs.

### 3. Automations are enabled

- Each automation should be **Enabled** (toggle on). Disabled automations will not run on the cadence.

### 4. Repo and branch

- All 10 should use the same **repo** (`tldr`) and the same **branch** you got working (e.g. `main` or `cursor-automations`). The agent will run commands in that branch’s context.

### 5. Optional: run once manually

- For each automation (or at least 1–2), use **Run** / **Test run** if the UI offers it. That confirms: env vars load, repo/branch are correct, and the first few steps (e.g. `pip install`, first `python3` call) succeed. Fix any errors before relying on the schedule.

### 6. Keep the branch in sync (if you edit locally)

- If you change automation prompts or scripts in your local clone, push to the **same branch** the automations use (e.g. `main` or `cursor-automations`) so the next run uses the latest instructions and code.

---

## Quick checklist

- [ ] All 10 automations exist with the names and triggers in the table above.
- [ ] Each has the full prompt from the matching `0X_...md` in Instructions.
- [ ] Repo = `tldr`, branch = your chosen branch, for all.
- [ ] Configured Environment has the required API keys and vars (see ENV_SETUP.md).
- [ ] Timezone for “at 08:00” etc. is correct.
- [ ] All automations are Enabled.
- [ ] (Optional) At least one automation has been test-run successfully.

Once the checklist is done, the automations will run according to the cadence specified in each trigger.

---

## Troubleshooting: "Failed to start background composer: [failed_precondition]"

This error appears **before** any automation step runs. Cursor’s cloud runner is refusing to start the “background composer” that executes your instructions. Fix the preconditions below, then try **Run Test** again.

### 1. Repo connection (most common)

- **Repo** in the Run Test dialog must be a repo Cursor can access (e.g. **neel-mishra/tldr** or the exact name in your Cursor account).
- Your Cursor account must be connected to **GitHub** (or the host you use) with access to that repo.
- In **Cursor → Settings → Account / GitHub**, confirm the correct account is linked and has access to the `tldr` repo.
- If the repo is under an org, ensure the Cursor-linked account has access to that org/repo.

### 2. Configured Environment

- The automation must use a **Configured Environment** (toggle **Use Configured Environment** ON).
- Open **Manage** (or the env name) and confirm the environment exists and has the required vars (see ENV_SETUP.md). An empty or broken environment can cause startup to fail.

### 3. Branch and default remote

- **Branch** (e.g. `main`) must exist on the repo and be pushed.
- Some “failed_precondition” reports are tied to “no preferred remote” or git state. Ensure the repo has a default remote (e.g. `origin`) and the selected branch is pushed.

### 4. Cursor plan and features

- Automations (scheduled and test runs) may require a plan that includes **Background agents / Automations**. If you’re on a restricted plan, upgrade or confirm automations are enabled for your account.

### 5. One automation failing when others pass (e.g. only #2)

If **only** one automation fails with `[failed_precondition]` and the rest pass (same repo, env, account), the instructions for that automation may have content that Cursor’s backend rejects when starting the run (e.g. a very long or complex code block with nested quotes).

- **Re-copy the Instructions:** In cursor.com/automations, open that automation, **replace the entire Instructions** with a fresh copy from the matching `automations/0X_....md` file in the repo (from the `#` title to the end, no frontmatter). Save and run **Run Test** again.
- **Automation 02 (Weekly Content Execution):** The inline `python3 -c "..."` block in Step 5 was replaced with a single script call (`automations/lib/run_video_script_for_blog.py`) so the instructions no longer contain that block. After pulling the latest repo, re-copy the Instructions for automation 02 from `02_weekly_content_execution.md` and run the test again.

### 6. Retry and support

- Try **Run Test** again after fixing repo connection and environment (or after re-copying instructions).
- If it still fails, use **Cursor → Help → Report issue** or the [Cursor Community Forum](https://forum.cursor.com) and include: “Failed to start background composer: [failed_precondition]” when running a Run Test for automation X on repo Y, branch Z.
