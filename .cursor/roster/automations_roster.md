## Hostfully Automations Roster

Index of Cursor Automations you’ve designed, with purpose, schedules, expected inputs, and outputs. Grouped by priority tier.

---

### Tier 1 — LaunchAgent Replacements (Core Schedulers)

- **Daily Content Pipeline Orchestrator**
  - **Schedule**: Daily at 08:00.
  - **Synopsis**: `com.hostfully.contentpipeline.plist` — orchestrates competitor content scraping, pipeline scoring, SEO enrichment, and daily visibility for the team.
  - **Inputs**:
    - Competitor blog list and scraper config (`competitor-blog-scraper.py`).
    - Existing content pipeline CSVs.
    - Ahrefs MCP credentials (keywords explorer tools).
    - Google Sheets MCP config (target sheet for summaries).
  - **Outputs**:
    - Updated `competitor_content_tracker.csv`.
    - Updated `content_pipeline.csv` with search volume/difficulty enrichment.
    - Daily summary row in a Google Sheet for pipeline status.

- **Weekly Content Execution + Repurposing Chain**
  - **Schedule**: Weekly, Monday at 09:00.
  - **Synopsis**: `com.hostfully.contentpipeline.weekly.plist` — runs content execution, humanizer quality gate, repurposing, and pushes everything into Docs.
  - **Inputs**:
    - Content pipeline entries ready for execution.
    - `execution_commander.py` configuration.
    - Humanizer skill and thresholds (AI score cutoffs).
    - `repurpose_agent.py` and `video_script_agent.py` configs.
    - Google Docs MCP credentials and target folders.
  - **Outputs**:
    - Draft blog posts.
    - Humanizer-scored and optionally rewritten versions.
    - Repurposed assets (LinkedIn, X, email, newsletter blurbs, video scripts).
    - Google Docs containing final content sets per piece.

- **Monthly Competitive Ad Intelligence**
  - **Schedule**: Monthly, last day of month.
  - **Synopsis**: Replaces `com.hostfully.tech.competitivetracker.monthly.plist`. Consolidates cross-platform competitor ad intelligence and Hostfully’s own performance.
  - **Inputs**:
    - Competitor brand/account lists.
    - Meta Ad Library MCP (platform ID + ads endpoints).
    - Meta Ads Portfolio MCP (accounts, campaigns, performance).
    - Google Ads Portfolio MCP (accounts, campaigns, performance).
    - Paths to `ad_creative_log.csv` and `ad_volume_tracker.csv`.
  - **Outputs**:
    - Refreshed competitor ad creative and volume trackers (CSVs).
    - Narrative creative brief comparing competitor strategies vs your performance.
    - Google Doc report for monthly review.

---

### Tier 2 — High-Value Intelligence Loops

- **Weekly Ad Performance Dashboard**
  - **Schedule**: Weekly, Monday at 07:00.
  - **Synopsis**: Pure-MCP automation that builds a cross-channel ad performance snapshot before standup.
  - **Inputs**:
    - Google Ads Portfolio MCP (account summary, campaign, and keyword performance).
    - Meta Ads Portfolio MCP (account and campaign performance).
    - Config for which accounts/campaigns to track and comparison baselines.
  - **Outputs**:
    - Weekly narrative performance report (Google Doc).
    - Updated running tracker in Google Sheets with WoW metrics and anomaly flags.

- **Weekly SEO Intelligence Report**
  - **Schedule**: Weekly, Tuesday at 08:00.
  - **Synopsis**: Connects Ahrefs data to your content pipeline and SEO agents for consistent visibility.
  - **Inputs**:
    - Ahrefs MCP (organic keywords, top pages, metrics history, organic competitors, rank tracker).
    - `search_ranking_agent.py` and `site_performance_agent.py` configurations.
    - List of tracked domains/keywords.
  - **Outputs**:
    - Google Doc report with striking-distance keywords, top pages, and competitor moves.
    - Recommendations mapped back to your content pipeline.

- **Bi-Weekly Advertiser Health Monitor**
  - **Schedule**: Every other Monday at 10:00.
  - **Synopsis**: Operationalizes the Advertiser Health & Churn analysis stack as a recurring automation.
  - **Inputs**:
    - Meta Ads Portfolio + Google Ads Portfolio MCP data per advertiser.
    - `advertiser_health.py` and `churn_analyzer.py` scripts and configs.
    - Any external CSVs or Sheets with advertiser metadata and benchmarks.
  - **Outputs**:
    - Bi-weekly health-scored advertiser list (CSV and Google Sheet).
    - Google Doc narrative highlighting Yellow/Red accounts and recommended actions.

- **Weekly Sales Intelligence Package**
  - **Schedule**: Weekly, Wednesday at 08:00.
  - **Synopsis**: Bundles fresh prospecting and updated battlecards into a single weekly drop for Sales.
  - **Inputs**:
    - Ahrefs MCP (site metrics, paid pages) for prospect discovery.
    - Meta Ad Library MCP for ad presence checks.
    - `prospect_intelligence.py` and `battlecard_generator.py` scripts.
    - Existing competitor landscape and content trackers.
  - **Outputs**:
    - Fresh prospect list in Google Sheets with scores and signals.
    - Updated competitor battlecards in Google Docs.

- **Post-Blog CRO + Landing Page Audit**
  - **Schedule**: Weekly, Thursday at 09:00.
  - **Synopsis**: Ties new content and key landing pages into a recurring CRO audit loop.
  - **Inputs**:
    - Playwright MCP (navigation, screenshots, DOM snapshots).
    - Ahrefs MCP (top pages and traffic metrics).
    - `cro_hypothesis_agent.py` configuration and list of key pages.
  - **Outputs**:
    - Screenshots/snapshots of key pages.
    - CRO hypothesis backlogs and A/B test recommendations in Google Docs.

---

### Tier 3 — Advanced Compound Automations

- **Monthly GTM Execution Commander**
  - **Schedule**: Monthly, 1st of the month.
  - **Synopsis**: Closes the loop between performance data and GTM planning by powering `gtm_commander.py` with live data.
  - **Inputs**:
    - Previous month’s Google Ads and Meta Ads performance via MCPs.
    - SEO trends from Ahrefs MCP.
    - Content performance and pipeline data (from CSVs or Sheets).
    - `gtm_commander.py` sprint planning configuration.
  - **Outputs**:
    - Monthly GTM retrospective and next-month sprint plan in Google Docs.
    - Optionally, updated JSON/CSV planning artifacts for internal use.

- **Monthly Competitor Creative + Content Convergence Report**
  - **Schedule**: Monthly, 5th of the month.
  - **Synopsis**: Combines competitor ads, content, and SEO data into a single strategic intelligence report.
  - **Inputs**:
    - Meta Ad Library MCP (competitor ad pulls).
    - `competitor_content_tracker.csv` for blog/content.
    - Ahrefs MCP (competitor organic keywords, top pages).
    - `competitive_tracker.py` and any competitor blog scraper configs.
  - **Outputs**:
    - Google Doc strategic brief showing overlapping “bets” (topics with both ads + content), gaps vs Hostfully, and recommended responses.

---

### Common Automation Conventions

- **Inputs (typical)**: Existing Python agents, CSV trackers in `docs/`, Ahrefs/Ads/Meta/Sheets/Docs/Playwright MCP credentials and configs, and short natural-language prompts describing each workflow’s steps.
- **Outputs (typical)**: Updated CSV trackers, appended Google Sheets rows, Google Docs reports/briefs, and occasionally screenshots/snapshots via Playwright MCP.

