## TLDR Agents Roster

High-level index of TLDR’s Cursor agents so you can quickly see what to use, what they expect in, and what they produce out. Grouped by function and use case.

---

### GTM Team — Sales Agents

- **Advertiser Prospect Intelligence Agent** (`ai system/agents/gtm team/sales/advertiser-prospect-agent.md`)
  - **Synopsis**: Finds and scores ideal advertisers based on funding, ad spend, and fit with TLDR newsletters. Used for building outbound prospect lists.
  - **Inputs**: Ideal customer profile, TLDR business context, competitor landscape, external ad/SEO signals (Ahrefs, Meta/Google ads, ad libraries).
  - **Outputs**: Ranked CSV prospect lists with scores and signals, plus optional per-company prospect briefs with suggested outreach angles.

- **Sales Call Transcript Analyzer** (`ai system/agents/gtm team/sales/call-transcript-analyzer-agent.md`)
  - **Synopsis**: Processes sales call transcripts to extract objections, competitor mentions, buying signals, and follow-ups.
  - **Inputs**: Folders of call transcripts (txt/md/json), ICP and competitor landscape context.
  - **Outputs**: Structured CSV per call and aggregated insight reports (top objections, competitor mentions, deal signals, action items).

- **Competitive Battlecard Agent** (`ai system/agents/gtm team/sales/battlecard-agent.md`)
  - **Synopsis**: Generates sales battlecards against key competitors using existing competitive trackers and fresh research.
  - **Inputs**: Competitor landscape, TLDR positioning and messaging, competitor content/ad trackers, web research.
  - **Outputs**: Per-competitor battlecards summarizing positioning, strengths/weaknesses, objections and counters, proof points, and killer questions.

- **Deal Risk Agent** (`ai system/agents/gtm team/sales/deal-risk-agent.md`)
  - **Synopsis**: Reviews opportunity notes, emails, and call summaries to assess deal risk and next best actions.
  - **Inputs**: Deal CRM notes, call summaries/transcripts, email threads, pipeline context.
  - **Outputs**: Risk rating per deal, specific risk factors, and recommended remediation steps.

---

### GTM Team — Marketing Agents

- **Content Performance Agent** (`ai system/agents/gtm team/marketing/content-performance-agent.md`)
  - **Synopsis**: Analyzes newsletter and blog performance to identify top topics, formats, and timing patterns.
  - **Inputs**: Newsletter performance CSVs, blog traffic/analytics exports, competitor content tracker data.
  - **Outputs**: Content performance reports with topic and headline patterns, send time insights, benchmarks, and next-topic recommendations.

- **Content Repurposing Agent** (`ai system/agents/gtm team/marketing/content-repurposing-agent.md`)
  - **Synopsis**: Converts long-form pieces (blogs, newsletters, webinars) into multi-channel content kits.
  - **Inputs**: Source content (text or transcript), brand voice/style guides, target channels and audience.
  - **Outputs**: Social posts, email subject lines, threads, blurbs, executive summaries, and metadata per source.

---

### GTM Team — Marketing Agents (Paid Ads System)

- **Paid Ads Structure Agent** (`ai system/agents/gtm team/marketing/paid ads/paid-ads-structure-agent.md`)
  - **Synopsis**: Designs and audits account/campaign/ad set structures for paid channels across Google, Meta, LinkedIn, TikTok, and X.
  - **Inputs**: Current account structure, objectives, budgets, audiences, tracking setup.
  - **Outputs**: Campaign structure blueprints, naming conventions, UTM schemas, and launch checklists.

- **Competitor Ad Intelligence Agent** (`ai system/agents/gtm team/marketing/paid ads/competitor-ad-intelligence-agent.md`)
  - **Synopsis**: Tracks competitor ads across platforms and summarizes creative patterns, spend signals, and trends.
  - **Inputs**: List of competitor brands/accounts, ad library/portfolio data sources, tracking config.
  - **Outputs**: Competitive ad logs, volume trackers, and narrative briefs on creative strategy and positioning.

- **Ad Creative Agent** (`ai system/agents/gtm team/marketing/paid ads/ad-creative-agent.md`)
  - **Synopsis**: Generates paid ads creative in two modes: Copy-Only and Copy + Concepts for downstream briefing.
  - **Inputs**: Offer, audience, channel, campaign goal, positioning, competitor context.
  - **Outputs**: Ad variants (primary text, headlines, descriptions), optional creative concepts, and rotation plans.

- **Visual Creative Brief Agent** (`ai system/agents/gtm team/marketing/paid ads/visual-creative-brief-agent.md`)
  - **Synopsis**: Turns ad-creative concepts into production-ready creative briefs with platform-specific specs and safe zones.
  - **Inputs**: Ad creative outputs, campaign structure, creative direction, brand guidelines.
  - **Outputs**: Designer-ready briefs per concept (sizes, safe zones, Nano Banana prompts, Figma/Canva instructions).

---

### GTM Team — Customer Success Agents

- **QBR Generator Agent** (`ai system/agents/gtm team/customer success/qbr-generator-agent.md`)
  - **Synopsis**: Builds Quarterly Business Review documents for advertisers using campaign performance data and benchmarks.
  - **Inputs**: Advertiser performance history (impressions, CTR, conversions, spend), placement history, TLDR benchmarks/context.
  - **Outputs**: Per-advertiser QBR markdown docs or decks with exec summaries, performance sections, benchmarks, and recommended next plans.

- **Support Ticket Analyzer Agent** (`ai system/agents/gtm team/customer success/support-ticket-analyzer-agent.md`)
  - **Synopsis**: Clusters and summarizes support tickets to find common issues and improvement opportunities.
  - **Inputs**: Exported support tickets (CSV or text), tags/categories (if any), product areas.
  - **Outputs**: Thematic summaries, top issue lists, root cause hypotheses, and suggested fixes or docs.

- **Churn Analyzer Agent** (`ai system/agents/gtm team/customer success/churn-analyzer-agent.md`)
  - **Synopsis**: Reviews churned accounts and feedback to understand why they left and how to prevent similar churn.
  - **Inputs**: Churned account lists, notes, feedback forms, performance history pre-churn.
  - **Outputs**: Churn post-mortem reports, common churn drivers, and playbook recommendations.

- **Advertiser Health Agent** (`ai system/agents/gtm team/customer success/advertiser-health-agent.md`)
  - **Synopsis**: Canonical advertiser success/health agent with modes for monthly audits, pre-renewal prep, and triage.
  - **Inputs**: Advertiser performance data, spend trends, communication logs, renewal timelines, benchmarks.
  - **Outputs**: Health-scored account lists (Green/Yellow/Red), renewal-prep briefs, and prioritized action plans.

---

### GTM Team — Product Agents

- **Sprint Planner Agent** (`ai system/agents/gtm team/product/sprint-planner-agent.md`)
  - **Synopsis**: Turns product inputs (backlog, signals) into structured sprint plans.
  - **Inputs**: Backlog items, customer feedback, performance signals, sprint capacity.
  - **Outputs**: Sprint plans with prioritized work, owners, and rationales.

- **Competitive Feature Matrix Agent** (`ai system/agents/gtm team/product/competitive-feature-matrix-agent.md`)
  - **Synopsis**: Builds and updates feature comparison matrices across TLDR and competitors.
  - **Inputs**: Product features, competitor research, pricing/packaging info.
  - **Outputs**: Competitive feature matrices and narrative commentary.

- **User Interview Synthesizer Agent** (`ai system/agents/gtm team/product/user-interview-synthesizer-agent.md`)
  - **Synopsis**: Summarizes and synthesizes user interviews into insights and opportunities.
  - **Inputs**: Raw interview transcripts or notes, segment/goal metadata.
  - **Outputs**: Interview summaries, theme maps, jobs-to-be-done, and opportunity lists.

- **Release Notes Agent** (`ai system/agents/gtm team/product/release-notes-agent.md`)
  - **Synopsis**: Drafts customer-facing release notes from internal changelogs.
  - **Inputs**: Changelogs, PR descriptions, product context, tone guidelines.
  - **Outputs**: Structured release notes in user-friendly language and formats.

- **Feature Request Prioritizer Agent** (`ai system/agents/gtm team/product/feature-request-prioritizer-agent.md`)
  - **Synopsis**: Prioritizes feature requests based on impact, effort, and alignment.
  - **Inputs**: Feature request backlog (with metadata like account size, frequency), strategy context.
  - **Outputs**: Prioritized list with scoring and rationale.

- **Engagement Behavior Agent** (`ai system/agents/gtm team/product/engagement-behavior-agent.md`)
  - **Synopsis**: Analyzes user behavior/engagement data to identify patterns and risks.
  - **Inputs**: Analytics exports (events, sessions, engagement), segment definitions.
  - **Outputs**: Behavior insights, segment breakdowns, and recommended product experiments.

- **PRD Task Breakdown Agent** (`ai system/agents/gtm team/product/prd-task-breakdown-agent.md`)
  - **Synopsis**: Converts a PRD into an engineering task breakdown.
  - **Inputs**: PRD document, engineering constraints, team structure.
  - **Outputs**: Task lists/epics, dependencies, and rough estimates.

---

### Execution Commander Agents

- **Workflow Orchestration Agent** (`ai system/agents/execution commander/workflow-orchestration-agent.md`)
  - **Synopsis**: High-level orchestrator that chains multiple ai system/agents/scripts into end-to-end workflows.
  - **Inputs**: Desired workflow description, list of component agents, scheduling/context.
  - **Outputs**: Orchestrated run plans, status summaries, and combined output artifacts.

- **Skill Builder Agent** (`ai system/agents/execution commander/skill-builder-agent.md`)
  - **Synopsis**: Helps design or refine Cursor skills/agents based on your workflows.
  - **Inputs**: Description of desired capability, existing scripts or prompts, constraints.
  - **Outputs**: Draft skill/agent specs and suggested file structures.

- **Feedback Synthesizer Agent (Execution Commander)** (`ai system/agents/execution commander/feedback-synthesizer-agent.md`)
  - **Synopsis**: Meta-synthesizer that rolls up feedback from multiple agents or workflows.
  - **Inputs**: Outputs from other agents (reports, CSVs, logs), goals or questions.
  - **Outputs**: Consolidated summaries and cross-agent insights.

---

### Content & Copy Agents

- **Copywriting Agent** (`ai system/agents/content/copywriting-agent.md`)
  - **Synopsis**: Canonical content-writing agent for page copy, long-form content, and conversion-oriented rewrites.
  - **Inputs**: Page type, audience, offer, product marketing context, brand voice preferences.
  - **Outputs**: Structured page/long-form copy drafts, alternatives, and conversion-focused edits.

- **Email Sequence Agent** (`ai system/agents/content/email-sequence-agent.md`)
  - **Synopsis**: Canonical email agent with modes for Cold Outbound, Warm Nurture, Lifecycle, and Product Updates.
  - **Inputs**: Campaign objective, audience, triggers, content themes.
  - **Outputs**: Mode-specific sequenced emails with timing, purpose, and CTA strategy per touch.

- **Social Media Agent** (`ai system/agents/content/social-media-agent.md`)
  - **Synopsis**: Social repurposing-first agent that converts existing assets into platform-native posts and calendars.
  - **Inputs**: Source content or theme, platform, tone and constraints.
  - **Outputs**: Repurposed post sets, threads, captions, hooks, and light calendar plans.

### SEO & AEO Agents

- **SEO Agent (General)** (`ai system/agents/seo-aeo/seo-agent.md`)
  - **Synopsis**: General-purpose SEO assistant for strategy, keyword mapping, and on-page optimization.
  - **Inputs**: Site URL, business goals, priority topics, competitor list.
  - **Outputs**: Keyword maps, on-page recommendations, content outlines, and GEO-localized keyword sets (GEO mode).

- **SEO Audit Agent (Technical/Deep)** (`ai system/agents/seo-aeo/seo-audit-agent.md`)
  - **Synopsis**: Deep technical + content SEO auditor integrated with `seo_auditor.py`.
  - **Inputs**: Company name, sitemap, crawl limit, flags for PSI/headless, GSC credentials (optional).
  - **Outputs**: URL inventories, CSVs, high-level and detailed audit reports, prioritized action plans.

- **AEO Audit Agent** (`ai system/agents/seo-aeo/aeo-audit-agent.md`)
  - **Synopsis**: Focuses on Answer Engine Optimization (AEO) and AI citation readiness.
  - **Inputs**: Key URLs or sitemap, target questions/queries, existing content.
  - **Outputs**: AEO-specific recommendations, structured QA content suggestions, and schema hints.

---

### Product Strategy & Packaging Agents

- **Product Strategy Agent** (`ai system/agents/product/product-strategy-agent.md`)
  - **Synopsis**: Canonical product strategy agent with modes for vision, roadmap, pricing/packaging, and GTM/channel strategy.
  - **Inputs**: Market context, customer insights, current product scope, goals.
  - **Outputs**: Strategic narratives, opportunity areas, roadmap themes, and GTM strategy frameworks.

- **Pricing & Packaging Agent** (`ai system/agents/product/pricing-packaging-agent.md`)
  - **Synopsis**: Explores pricing and packaging options, tradeoffs, and messaging.
  - **Inputs**: Current pricing, segments, competitor pricing, value metrics.
  - **Outputs**: Pricing models, packaging options, and messaging recommendations.

- **PRD Agent** (`ai system/agents/product/prd-agent.md`)
  - **Synopsis**: Drafts full Product Requirement Documents from high-level problem/solution briefs.
  - **Inputs**: Problem statement, goals, constraints, stakeholder notes.
  - **Outputs**: Structured PRDs (background, requirements, UX, success metrics).

---

### Technical & Growth Engineering Agents

- **CRO Agent** (`ai system/agents/technical/cro-agent.md`)
  - **Synopsis**: Canonical CRO agent for page diagnostics and experiment planning (including A/B and landing-page test modes).
  - **Inputs**: Page URLs, analytics snapshots, funnels, qualitative feedback.
  - **Outputs**: CRO audits, prioritized experiment backlogs, and test-ready plans with metrics guidance.

- **Growth Interactive Tool Agent** (`ai system/agents/technical/growth-interactive-tool-agent.md`)
  - **Synopsis**: Designs interactive tools or calculators as growth assets.
  - **Inputs**: Growth goal, target audience, existing content and assets.
  - **Outputs**: Specs for tools (flows, inputs/outputs, UX notes).

- **Analytics Tracking Agent** (`ai system/agents/technical/analytics-tracking-agent.md`)
  - **Synopsis**: Designs tracking plans and instrumentation for analytics.
  - **Inputs**: Product flows, KPIs, current tracking setup.
  - **Outputs**: Tracking plans, event schemas, tagging recommendations.

- **n8n Workflow Agent** (`ai system/agents/technical/n8n-workflow-agent.md`)
  - **Synopsis**: Designs automation workflows for n8n (or similar) based on your processes.
  - **Inputs**: Desired automation description, tools/APIs involved, triggers and outputs.
  - **Outputs**: Workflow diagrams, node-by-node specs, and suggested error handling.

---

### UI & UX Agents

- **UX Researcher Agent** (`ai system/agents/ui-ux/ux-researcher-agent.md`)
  - **Synopsis**: Canonical UX research agent with modes for discovery, diagnostics, validation, and synthesis.
  - **Inputs**: Research goals, target users, existing insights, product/flow context.
  - **Outputs**: Right-sized research plans, artifacts (guides, scripts), and decision-ready synthesis.

- **UI Designer Agent** (`ai system/agents/ui-ux/ui-designer-agent.md`)
  - **Synopsis**: Canonical UI design agent with modes for new flows, refreshes, design systems, and dev-ready handoff.
  - **Inputs**: Product requirements, brand guidelines, constraints, and desired fidelity.
  - **Outputs**: Layout descriptions, component specs, system tokens, and implementation notes.

---

### Persona & Role Agents

- **Competitive Creative Tracker Agent** (`ai system/agents/personas/competitive-creative-tracker-agent.md`)
  - **Synopsis**: Persona preset for deep competitive ad/creative tracking across channels, feeding insights into paid ads and creative agents.
  - **Inputs**: Competitor list, creative logs, ad library data.
  - **Outputs**: Updated creative trackers, monthly audit CSVs, and pattern summaries for use by canonical paid ads agents.

- **Presentation Builder Agent** (`ai system/agents/personas/presentation-builder-agent.md`)
  - **Synopsis**: Persona preset for turning any agent’s outputs into markdown-based presentations with timing and slide structure.
  - **Inputs**: Goal of the presentation, key points/data, audience.
  - **Outputs**: Slide-by-slide outlines and narrative flows built from existing reports/briefs.

- **Trend Researcher Agent** (`ai system/agents/personas/trend-researcher-agent.md`)
  - **Synopsis**: Persona preset for trend-hunting across social, app stores, and culture, to layer on top of product, SEO, CRO, or paid ads work.
  - **Inputs**: Topic areas, sources, timeframe.
  - **Outputs**: Trend reports, curated examples, and opportunity briefs to feed canonical agents.

- **IT Agent** (`ai system/agents/personas/IT-agent.md`)
  - **Synopsis**: Enterprise integration / IT persona preset for infra and tooling/integration questions alongside core technical agents.
  - **Inputs**: Current stack details, requirements, constraints.
  - **Outputs**: Integration designs, recommendations, runbooks, and configuration guidance.

- **Growth Hacker Agent** (`ai system/agents/personas/growth-hacker-agent.md`)
  - **Synopsis**: Persona preset for scrappy growth ideation layered on top of CRO and product strategy agents.
  - **Inputs**: Growth goals, current channels, constraints, audience.
  - **Outputs**: Experiment backlogs and playbooks to be run via canonical CRO/experimentation flows.

- **Growth Engineer Agent** (`ai system/agents/personas/growth-engineer-agent.md`)
  - **Synopsis**: Persona preset combining engineering + growth lens to design technical growth projects alongside CRO/analytics agents.
  - **Inputs**: Growth goals, product surface area, available engineering capacity.
  - **Outputs**: Project specs, implementation plans, and measurement setups.

- **Data Engineer Agent** (`ai system/agents/personas/data-engineer-agent.md`)
  - **Synopsis**: Persona preset for data infrastructure/pipelines to support analytics, experimentation, and reporting work.
  - **Inputs**: Source systems, questions to answer, current data model.
  - **Outputs**: Data flow diagrams, table schemas, and pipeline specs.

---

### Standalone Python Utilities (Non-Agent)

- **Paid Ads Budget Tracker** (`ai system/python scripts/paid-ads_budget_tracker/main.py`)
  - **Synopsis**: Standalone paid media budget allocation utility that joins campaign mapping + performance inputs and computes daily budget recommendations.
  - **Inputs**: Campaign playbook (`docs/paid_ads_assets/campaign_playbook_monthly.csv`; Hostfully March 2026 = **$60k** / 15 campaigns, source workbook in `docs/paid_ads_assets/`), campaign mapping (`data/config/campaign_mapping.csv`), daily performance data.
  - **Outputs**: Daily budget tracker CSVs and budget-change recommendation files under `docs/analytics_reports`.
  - **Classification**: Python utility package, not an agent or automation spec.

- **VibeHype Video Pipeline** (`ai system/video/`)
  - **Synopsis**: Remotion-based video production toolchain for paid ads creative, used to render 9:16 and 16:9 hype/trailer assets from storyboarded UI compositions.
  - **Inputs**: Storyboard/compositions in `ai system/video/src/`, render target (`COMP`), output path (`OUT`), and optional music/post edits in downstream tooling.
  - **Outputs**: Rendered MP4 assets (for Reels/TikTok/Shorts and horizontal variants) under `ai system/video/out/`.
  - **Classification**: JS/TS production tool, not an agent, automation spec, or Python script.

---

### Quick Usage Pattern

- **Inputs (in practice)**: Usually markdown briefs in `commands/` or exported CSVs from tools/analytics.
- **Outputs (in practice)**: Markdown reports and briefs in `docs/`, CSV trackers, and sometimes downstream Google Sheets/Docs via MCP tools.

