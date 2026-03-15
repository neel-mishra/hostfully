# Cursor Automations Setup Guide

Use this table when creating each automation at **[cursor.com/automations](https://cursor.com/automations)**. For each row: create a new automation, set **Name** and **Trigger** from the table, paste the full prompt from the matching `.md` file into **Instructions**, set **Model** and **Tools/MCP** as below, turn **Use Configured Environment** ON, add the required env vars (see `lib/ENV_SETUP.md`), then **Enable**.

---

| # | Automation name | Trigger | Model | Tools or MCP |
|---|-----------------|---------|--------|----------------|
| 1 | Daily Content Pipeline Orchestrator | **Daily** at **08:00** | Use Cursor’s recommended model for Automations (e.g. **Codex 5.3 High** or current default) | **None.** Instructions use shell commands and workspace scripts only. |
| 2 | Weekly Content Execution + Repurposing Chain | **Weekly** **Monday** at **09:00** | Same as above | **None.** |
| 3 | Monthly Competitive Ad Intelligence | **Monthly** **last day of month** at **08:00** | Same as above | **None.** |
| 4 | Weekly Ad Performance Dashboard | **Weekly** **Monday** at **07:00** | Same as above | **None.** |
| 5 | Weekly SEO Intelligence Report | **Weekly** **Tuesday** at **08:00** | Same as above | **None.** |
| 6 | Bi-Weekly Advertiser Health Monitor | **Every other Monday** at **10:00** | Same as above | **None.** |
| 7 | Weekly Sales Intelligence Package | **Weekly** **Wednesday** at **08:00** | Same as above | **None.** |
| 8 | Weekly CRO + Landing Page Audit | **Weekly** **Thursday** at **09:00** | Same as above | **None.** |
| 9 | Monthly GTM Execution Commander | **Monthly** **1st** at **09:00** | Same as above | **None.** |
| 10 | Monthly Competitor Creative + Content Convergence Report | **Monthly** **5th** at **08:00** | Same as above | **None.** |

---

## Notes

- **Instructions:** Copy the entire body of the matching file (e.g. `01_daily_content_pipeline.md`) into the automation’s Instructions field — everything from the `#` title to the end, including all code blocks. Do not copy the frontmatter (`---` and `name:`/`schedule:`).
- **Model:** If “Codex 5.3 High” is not available, choose the current default or most capable model recommended for Automations (one that can run shell commands and follow long prompts).
- **Tools/MCP:** Do **not** add any MCP servers or extra tools. These automations are written to run `python3 automations/lib/...` and `python3 "python scripts/..."` via shell; all API access is through those scripts and the **Configured Environment** (env vars).
- **Configured Environment:** Add the API keys and variables listed in `automations/lib/ENV_SETUP.md` (and `docs/GSC_GA4_SETUP.md` if you use GSC/GA4). The same environment can be shared across all 10 automations.
