## TLDR Python Scripts Roster

Mapping of core Python scripts to the agents and/or automations they power.

### Legend

- **Agent**: The primary Cursor agent spec this script implements or extends.
- **Automation**: The Cursor Automation (from `automations_roster.md`) that schedules or orchestrates this script.

---

### Core GTM / Orchestration Scripts

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/gtm execution commander/gtm_commander.py` | `ai system/agents/gtm team/product/sprint-planner-agent.md`, `ai system/agents/product/product-strategy-agent.md` (used by GTM Commander) | Monthly GTM Execution Commander |
| `ai system/python scripts/auto_context.py` | (Utility script for agent context loading; no single agent spec) | Used ad-hoc by multiple automations as context helper |

---

### Content & SEO Pipeline Scripts

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/content pipeline agent/planning/pipeline_agent.py` | Content pipeline planners (e.g. `ai system/agents/content/email-sequence-agent.md`, `ai system/agents/content/copywriting-agent.md`) | Daily Content Pipeline Orchestrator |
| `ai system/python scripts/content pipeline agent/execution/blog_writer_agent.py` | `ai system/agents/content/copywriting-agent.md`, `ai system/agents/content/email-sequence-agent.md` (blog execution) | Weekly Content Execution + Repurposing Chain |
| `ai system/python scripts/content pipeline agent/repurposing/repurpose_agent.py` | `ai system/agents/gtm team/marketing/content-repurposing-agent.md` | Weekly Content Execution + Repurposing Chain |
| `ai system/python scripts/content and seo pipeline agent/search_ranking_agent.py` | `ai system/agents/seo-aeo/seo-agent.md`, `ai system/agents/seo-aeo/seo-audit-agent.md` | Weekly SEO Intelligence Report |
| `ai system/python scripts/content and seo pipeline agent/site_performance_agent.py` | `ai system/agents/seo-aeo/seo-agent.md` | Weekly SEO Intelligence Report |
| `ai system/python scripts/content and seo pipeline agent/content_performance_analyzer.py` | `ai system/agents/gtm team/marketing/content-performance-agent.md` | (Future) Content Performance Analyzer loop |
| `ai system/python scripts/content and seo pipeline agent/traffic_analytics_agent.py` | `ai system/agents/gtm team/marketing/content-performance-agent.md` | (Future) Content Performance Analyzer loop |
| `ai system/python scripts/content and seo pipeline agent/content_ideation_agent.py` | `ai system/agents/content/copywriting-agent.md` (Long-Form mode) | Used ad-hoc in content planning |
| `ai system/python scripts/content and seo pipeline agent/programmatic_seo_agent.py` | `ai system/agents/seo-aeo/seo-agent.md`, `ai system/agents/seo-aeo/aeo-audit-agent.md` | (Future) Programmatic SEO automation |
| `ai system/python scripts/content and seo pipeline agent/creative_direction_agent.py` | `ai system/agents/gtm team/marketing/paid ads/visual-creative-brief-agent.md`, `ai system/agents/gtm team/marketing/paid ads/ad-creative-agent.md` | Used ad-hoc in creative planning |
| `ai system/python scripts/seo agent/seo_auditor.py` | `ai system/agents/seo-aeo/seo-audit-agent.md` | Weekly SEO Intelligence Report (when run as part of audits) |

---

### Competitive Intelligence & Creative Tracking

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/competitive creative tracker/competitive_tracker.py` | `ai system/agents/personas/competitive-creative-tracker-agent.md`, `ai system/agents/gtm team/marketing/paid ads/competitor-ad-intelligence-agent.md` | Monthly Competitive Ad Intelligence; Monthly Competitor Creative + Content Convergence Report |
| `ai system/python scripts/competitive creative tracker/heartbeat_monthly.py` | `ai system/agents/personas/competitive-creative-tracker-agent.md` | Monthly Competitive Ad Intelligence (legacy plist, now automation trigger) |
| `ai system/python scripts/competitive creative tracker/config.py` | (Config for competitive tracker) | Used by Competitive Ad Intelligence-related automations |
| `ai system/python scripts/competitor scrapers/competitor-blog-scraper.py` | `ai system/agents/personas/competitive-creative-tracker-agent.md`, `ai system/agents/content/copywriting-agent.md` (Long-Form mode) | Daily Content Pipeline Orchestrator; Monthly Competitor Creative + Content Convergence Report |
| `ai system/python scripts/competitor scrapers/competitor-social-media-scraper.py` | `ai system/agents/gtm team/marketing/paid ads/competitor-ad-intelligence-agent.md` | Used ad-hoc or future social intelligence loops |

---

### Paid Ads Intelligence & Acquisition

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/paid ads intelligence agent/paid_ads_intelligence_agent.py` | `ai system/agents/gtm team/marketing/paid ads/competitor-ad-intelligence-agent.md`, `ai system/agents/gtm team/marketing/paid ads/paid-ads-structure-agent.md` | Monthly Competitive Ad Intelligence; Weekly Ad Performance Dashboard (logic source) |
| `ai system/python scripts/paid ads intelligence agent/paid_ads_mvp.py` | (Early version of the Paid Ads Intelligence agent) | Used manually for MVP runs |
| `ai system/python scripts/paid ads intelligence agent/heartbeat_weekly.py` | `ai system/agents/gtm team/marketing/paid ads/competitor-ad-intelligence-agent.md` | Legacy weekly heartbeat for ad intelligence, superseded by Cursor automations |
| `ai system/python scripts/paid ads intelligence agent/report_analyzers/base.py` | (Shared analyzer base for reports) | Weekly Ad Performance Dashboard; Monthly Competitive Ad Intelligence |
| `ai system/python scripts/paid ads intelligence agent/report_analyzers/google_ads_analyzer.py` | `ai system/agents/gtm team/marketing/paid ads/paid-ads-structure-agent.md` | Weekly Ad Performance Dashboard |
| `ai system/python scripts/paid ads intelligence agent/report_analyzers/meta_ads_analyzer.py` | `ai system/agents/gtm team/marketing/paid ads/paid-ads-structure-agent.md` | Weekly Ad Performance Dashboard |
| `ai system/python scripts/paid ads intelligence agent/report_analyzers/__init__.py` | (Package init) | Shared by ad intelligence automations |
| `ai system/python scripts/paid ads intelligence agent/qa_test_run.py` | (QA harness for paid ads intelligence) | Ad-hoc QA for ad intelligence automations |

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/paid acquisition agent/company_sourcer.py` | `ai system/agents/gtm team/sales/advertiser-prospect-agent.md`, `ai system/agents/content/email-sequence-agent.md` (Cold Outbound mode) | Used in prospecting workflows and Weekly Sales Intelligence Package (upstream of `prospect_intelligence.py`) |
| `ai system/python scripts/paid acquisition agent/icp_filter.py` | `ai system/agents/gtm team/sales/advertiser-prospect-agent.md` | Weekly Sales Intelligence Package (filtering step) |
| `ai system/python scripts/paid acquisition agent/buying_committee_enricher.py` | `ai system/agents/gtm team/sales/advertiser-prospect-agent.md`, `ai system/agents/personas/data-engineer-agent.md` | Weekly Sales Intelligence Package (enrichment step) |
| `ai system/python scripts/paid acquisition agent/audience_exporter.py` | `ai system/agents/technical/n8n-workflow-agent.md`, `ai system/agents/technical/analytics-tracking-agent.md` | Used ad-hoc in audience sync workflows |
| `ai system/python scripts/paid acquisition agent/creative_mapping.py` | `ai system/agents/gtm team/marketing/paid ads/ad-creative-agent.md` | Used ad-hoc in mapping creatives to campaigns/ad sets |
| `ai system/python scripts/paid acquisition agent/paid_ads_campaign_orchestrator.py` | `ai system/agents/gtm team/marketing/paid ads/paid-ads-structure-agent.md` | Future paid campaign orchestration automation |
| `ai system/python scripts/paid acquisition agent/migrate_paid_ads_asset_folders.py` | (Migration/maintenance script for ad assets) | One-off migration tasks |
| `ai system/python scripts/paid acquisition agent/landing_page_agent.py` | `ai system/agents/technical/cro-agent.md` (Landing Page Test mode) | Post-Blog CRO + Landing Page Audit (supporting analysis) |
| `ai system/python scripts/paid acquisition agent/social_ads_agent.py` | `ai system/agents/gtm team/marketing/paid ads/ad-creative-agent.md`, `ai system/agents/content/social-media-agent.md` | Used ad-hoc for social ads campaign builds |
| `ai system/python scripts/paid acquisition agent/search_ads_agent.py` | `ai system/agents/gtm team/marketing/paid ads/paid-ads-structure-agent.md` | Used ad-hoc in search campaign design and audits |

---

### Meta Ads Creative Agent Scripts

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/meta ads creative agent/meta_creative_agent.py` | `ai system/agents/gtm team/marketing/paid ads/ad-creative-agent.md`, `ai system/agents/gtm team/marketing/paid ads/visual-creative-brief-agent.md` | Supports Weekly Ad Performance Dashboard and Competitive Ad Intelligence when creative refresh is needed |
| `ai system/python scripts/meta ads creative agent/prompts.py` | (Prompt templates for meta creative agent) | Used by `meta_creative_agent.py` |
| `ai system/python scripts/meta ads creative agent/validator.py` | (Validation logic for creative outputs) | Used by `meta_creative_agent.py` in creative-related automations |
| `ai system/python scripts/meta ads creative agent/context_loader.py` | (Context loading helper for creative agent) | Used internally by the meta creative stack |
| `ai system/python scripts/meta ads creative agent/research.py` | (Research helpers for competitor/market insights) | Used by creative and competitive-intel workflows |

---

### Sales & CS Agent Scripts

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/sales agent/prospect_intelligence.py` | `ai system/agents/gtm team/sales/advertiser-prospect-agent.md` | Weekly Sales Intelligence Package |
| `ai system/python scripts/sales agent/transcript_analyzer.py` | `ai system/agents/gtm team/sales/call-transcript-analyzer-agent.md` | (Future) Sales call analysis automation |
| `ai system/python scripts/sales agent/battlecard_generator.py` | `ai system/agents/gtm team/sales/battlecard-agent.md` | Weekly Sales Intelligence Package |
| `ai system/python scripts/sales agent/deal_risk_analyzer.py` | `ai system/agents/gtm team/sales/deal-risk-agent.md` | (Future) Deal risk monitoring automation |

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/customer success agent/advertiser_health.py` | `ai system/agents/gtm team/customer success/advertiser-health-agent.md` | Bi-Weekly Advertiser Health Monitor |
| `ai system/python scripts/customer success agent/churn_analyzer.py` | `ai system/agents/gtm team/customer success/churn-analyzer-agent.md` | Bi-Weekly Advertiser Health Monitor |
| `ai system/python scripts/customer success agent/qbr_generator.py` | `ai system/agents/gtm team/customer success/qbr-generator-agent.md` | (Future) QBR-generation automation |
| `ai system/python scripts/customer success agent/feedback_synthesizer.py` | `ai system/agents/execution commander/feedback-synthesizer-agent.md` (Advertiser Feedback mode) | (Future) Advertiser Feedback Synthesizer automation |
| `ai system/python scripts/customer success agent/support_ticket_analyzer.py` | `ai system/agents/gtm team/customer success/support-ticket-analyzer-agent.md` | (Future) Support insights automation |

---

### Product Agent Scripts

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/product agent/sprint_planner.py` | `ai system/agents/gtm team/product/sprint-planner-agent.md` | Monthly GTM Execution Commander (sprint planning) |
| `ai system/python scripts/product agent/competitive_feature_matrix.py` | `ai system/agents/gtm team/product/competitive-feature-matrix-agent.md` | Used ad-hoc or in GTM/product planning runs |
| `ai system/python scripts/product agent/interview_synthesizer.py` | `ai system/agents/gtm team/product/user-interview-synthesizer-agent.md` | Used ad-hoc or in research synthesis workflows |
| `ai system/python scripts/product agent/release_notes_generator.py` | `ai system/agents/gtm team/product/release-notes-agent.md` | Used ad-hoc for release note generation |
| `ai system/python scripts/product agent/feature_request_prioritizer.py` | `ai system/agents/gtm team/product/feature-request-prioritizer-agent.md` | (Future) feature-prioritization automation |
| `ai system/python scripts/product agent/engagement_behavior.py` | `ai system/agents/gtm team/product/engagement-behavior-agent.md` | (Future) engagement behavior audit automation |

---

### CRO & Website Intelligence

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/cro and website intelligence agent/cro_hypothesis_agent.py` | `ai system/agents/technical/cro-agent.md` (Experiment Design + Landing Page Test modes) | Post-Blog CRO + Landing Page Audit |

---

### Social Media Agent Scripts

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/social media agent/social_media_agent.py` | `ai system/agents/content/social-media-agent.md` | Weekly Content Execution + Repurposing Chain (for social variants) |
| `ai system/python scripts/social media agent/team_social_drafts.py` | `ai system/agents/content/social-media-agent.md`, `ai system/agents/content/copywriting-agent.md` (Long-Form mode) | Used ad-hoc for team-specific drafts |
| `ai system/python scripts/social media agent/voice_memory_builder.py` | `ai system/agents/content/social-media-agent.md`, `ai system/agents/humanizer` (brand memory) | Used to build/refresh social voice memory |
| `ai system/python scripts/social media agent/uniqueness_gate.py` | (Uniqueness checker for social content) | Used as a quality gate in social content automations |

---

### Email Nurturing & Outbound

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/email nurturing agent/nurture_agent.py` | `ai system/agents/content/email-sequence-agent.md` (Warm Nurture/Lifecycle modes) | (Future) automated nurture sequence generation |
| `ai system/python scripts/outbound automation agent/outbound_sequence_agent.py` | `ai system/agents/content/email-sequence-agent.md` (Cold Outbound mode) | (Future) outbound automation and follow-up loops |

---

### Video & Visual Generators

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/automations/lib/run_video_script_for_blog.py` | `ai system/agents/content/copywriting-agent.md` (Long-Form mode), `ai system/agents/content/social-media-agent.md` | Weekly Content Execution + Repurposing Chain (video script step) |
| `ai system/python scripts/visual generators/images/merge_wireframes.py` | `ai system/agents/ui-ux/ui-designer-agent.md` | Used ad-hoc for visual/wireframe workflows |
| `Company Case Studies/TLDR/generate_tldr_wireframes.py` | `ai system/agents/ui-ux/ui-designer-agent.md`, `ai system/agents/personas/presentation-builder-agent.md` | Used ad-hoc for TLDR case study visuals and wireframes |

---

### Budget Tracker (Standalone Utility)

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/paid-ads_budget_tracker/main.py` | (Standalone budget tracker; potential future integration with GTM/Product agents) | None (runs standalone) |
| `ai system/python scripts/paid-ads_budget_tracker/allocation.py` | (Helper for budget allocation logic) | Used by `ai system/python scripts/paid-ads_budget_tracker/main.py` |
| `ai system/python scripts/paid-ads_budget_tracker/calculations.py` | (Helper for budget calculations) | Used by `ai system/python scripts/paid-ads_budget_tracker/main.py` |
| `ai system/python scripts/paid-ads_budget_tracker/aggregation.py` | (Helper for aggregating budget data) | Used by `ai system/python scripts/paid-ads_budget_tracker/main.py` |
| `ai system/python scripts/paid-ads_budget_tracker/sources_google.py` | (Google source integration for budget tracker) | Used by `ai system/python scripts/paid-ads_budget_tracker/main.py` |
| `ai system/python scripts/paid-ads_budget_tracker/sources_meta.py` | (Meta source integration for budget tracker) | Used by `ai system/python scripts/paid-ads_budget_tracker/main.py` |
| `ai system/python scripts/paid-ads_budget_tracker/io.py` | (I/O and persistence helpers) | Used by `ai system/python scripts/paid-ads_budget_tracker/main.py` |
| `ai system/python scripts/paid-ads_budget_tracker/config.py` | (Config for budget tracker) | Used by `ai system/python scripts/paid-ads_budget_tracker/main.py` |
| `ai system/python scripts/paid-ads_budget_tracker/__init__.py` | (Package init) | N/A |

---

### Automations Library (APIs & MCP Helpers)

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/automations/lib/ahrefs_api.py` | `ai system/agents/seo-aeo/seo-audit-agent.md`, `ai system/agents/gtm team/marketing/content-performance-agent.md`, `ai system/agents/gtm team/marketing/paid ads/competitor-ad-intelligence-agent.md` | Daily Content Pipeline Orchestrator; Weekly SEO Intelligence Report; Monthly Competitive Ad Intelligence; Monthly Competitor Creative + Content Convergence Report |
| `ai system/automations/lib/google_ads_api.py` | `ai system/agents/gtm team/marketing/paid ads/paid-ads-structure-agent.md`, `ai system/agents/gtm team/marketing/paid ads/competitor-ad-intelligence-agent.md` | Weekly Ad Performance Dashboard; Monthly Competitive Ad Intelligence; Monthly GTM Execution Commander |
| `ai system/automations/lib/meta_ads_api.py` | `ai system/agents/gtm team/marketing/paid ads/paid-ads-structure-agent.md`, `ai system/agents/gtm team/marketing/paid ads/competitor-ad-intelligence-agent.md` | Weekly Ad Performance Dashboard; Monthly Competitive Ad Intelligence; Monthly GTM Execution Commander |
| `ai system/automations/lib/fb_ad_library_api.py` | `ai system/agents/personas/competitive-creative-tracker-agent.md`, `ai system/agents/gtm team/marketing/paid ads/competitor-ad-intelligence-agent.md` | Monthly Competitive Ad Intelligence; Weekly Sales Intelligence Package (prospect signals) |
| `ai system/automations/lib/gsc_api.py` | `ai system/agents/seo-aeo/seo-audit-agent.md` | Weekly SEO Intelligence Report (when using GSC) |
| `ai system/automations/lib/gsheets_api.py` | (Shared Sheets helper for many agents) | Daily Content Pipeline Orchestrator; Weekly Ad Performance Dashboard; Bi-Weekly Advertiser Health Monitor; others |
| `ai system/automations/lib/gdocs_api.py` | (Shared Docs helper for many agents) | Weekly Content Execution + Repurposing Chain; Weekly SEO Intelligence Report; Monthly Competitive Ad Intelligence; GTM Commander; others |

---

### Google Ads MCP Server

| Script Path | Agent(s) | Automation(s) |
| --- | --- | --- |
| `ai system/python scripts/google_ads_mcp/google_ads_server.py` | (MCP server backing Google Ads Portfolio tools) | Weekly Ad Performance Dashboard; Monthly Competitive Ad Intelligence; Monthly GTM Execution Commander |
| `ai system/python scripts/google_ads_mcp/tests/test_google_ads_mcp.py` | (Tests for MCP server) | N/A (testing only) |
| `ai system/python scripts/google_ads_mcp/tests/test_token_refresh.py` | (Token refresh tests) | N/A (testing only) |
| `ai system/python scripts/google_ads_mcp/tests/test_smoke.py` | (Smoke tests) | N/A (testing only) |

---

If you add new Python scripts, mirror this table structure (script path, primary agent(s), and which automation, if any, calls it) so the roster stays your single source of truth.

