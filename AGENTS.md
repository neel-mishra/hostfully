# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is

A collection of standalone Python CLI scripts and Cursor Automation prompts powering TLDR's GTM (Go-To-Market) workflows: marketing, sales, SEO, paid ads intelligence, content pipeline, and customer success. There is **no web server, no database, and no build step**.

### Python environment

- Python 3.12+ is required.
- Dependencies are spread across **7 separate `requirements.txt` files** in different subdirectories. The update script installs all of them. See `automations/README.md` § "First-Time Setup" for the canonical list.

### Running scripts

- All utility CLI scripts live in `automations/lib/` and accept `--help`. They wrap external APIs (Ahrefs, Google Sheets, Google Docs, Meta Ads, Google Ads, FB Ad Library, GSC).
- Agent scripts live under `python scripts/<agent name>/` and most accept `--help` or `--dry-run`.
- Paths contain spaces (e.g. `python scripts/sales agent/`), so always quote them in shell commands.

### API keys

Most scripts require external API keys loaded from a `.env` file at the workspace root via `python-dotenv`. Without keys, scripts either error or fall back to mock data. See `automations/lib/ENV_SETUP.md` for the full variable list.

The two most broadly needed keys are `ANTHROPIC_API_KEY` and `GEMINI_API_KEY`.

### Linting

No project-level linter config exists. Use `ruff check "python scripts/" automations/lib/` for quick lint checks. Critical error rules: `ruff check --select E9,F63,F7,F82`.

### Testing

No formal test framework. Two ad-hoc test scripts exist:
- `python scripts/content pipeline agent/planning/test_typing.py` — type-annotation smoke test (runs locally, no API keys needed).
- `python scripts/paid ads intelligence agent/qa_test_run.py` — QA test for Meta Ads (requires `META_ACCESS_TOKEN` and `META_AD_ACCOUNT_ID`).

### Useful local-only script

`python scripts/auto_context.py "<query>"` scores and ranks workspace markdown files by relevance to a prompt — works without any API keys.
