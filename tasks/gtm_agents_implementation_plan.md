# GTM Agents Implementation Plan

**Source:** [Claude Code for GTM Teams — GTMnow](https://thegtmnewsletter.substack.com/p/claude-code-for-gtm-teams)  
**Date:** 2026-03-10  
**Status:** Planning

---

## Audit: Article Use Cases vs. Existing Agents

The article describes 25 use cases across 6 functions. Here's how they map to TLDR's existing agent ecosystem and what's net-new.

| # | Article Use Case | TLDR Relevance | Existing Coverage | Gap |
|---|---|---|---|---|
| **SALES** |
| 1 | Identify High-Quality Leads from Product | **High** — find ideal advertisers | None | Full build |
| 2 | Scrape Public Data for Prospect Lists | **High** — build advertiser pipeline | None | Full build |
| 3 | Analyze Call Transcripts at Scale | **High** — advertiser sales calls | None | Full build |
| 4 | Personalized Outreach Sequences | **High** | `outbound_sequence_agent.py`, `cold-email-agent.md` | Enhance existing |
| 5 | Competitive Battlecard Builder | **High** — arm sales team | `competitive-creative-tracker-agent.md` tracks ads only | Build battlecard layer |
| **MARKETING** |
| 6 | Competitor Ad Intelligence | **High** | `competitive_tracker.py` + agent ✅ | Mature — enhance with LLM analysis |
| 7 | Content Performance Analyzer | **High** | `traffic_analytics_agent.py`, `search_ranking_agent.py` partial | Build unified analyzer |
| 8 | SEO/GEO Keyword Research Pipeline | **High** | `seo-audit-agent.md`, `aeo-audit-agent.md`, `seo_auditor.py` ✅ | Enhance with GEO |
| 9 | Repurpose Content into Multi-Channel | **High** | Content pipeline exists but no repurposing agent | Full build |
| 10 | Self-Updating Competitive Tracker | **High** | `competitive_tracker.py` + heartbeat ✅ | Extend to website/pricing/jobs |
| **CUSTOMER SUCCESS (Advertiser Success)** |
| 11 | Renewal Risk Analyzer | **Critical** — advertiser retention | `customer_summary_intelligence.md` (template only) | Full build |
| 12 | QBR Deck Generator | **High** — advertiser QBRs | None | Full build |
| 13 | Synthesize Customer Feedback at Scale | **High** | None | Full build |
| 14 | Churn Post-Mortem Analyzer | **High** — understand advertiser churn | None | Full build |
| **PRODUCT** |
| 15 | Sprint Planning from Customer Signals | **Medium** | `gtm_commander.py`, `sprint_plan_template.json` partial | Enhance existing |
| 16 | User Behavior Audit from Analytics | **High** — newsletter engagement analytics | None | Full build |
| 17 | Self-Driving Documentation | **Low** | N/A | Skip for now |
| **PERSONAL/ADMIN** |
| 18 | Draft & Schedule Social Posts | **Medium** | `social-media-agent.md`, `social_media_agent.py` ✅ | Already covered |
| 19 | Personal CRM from Inbox | **Low** | N/A | Skip |
| **WILD ONES** |
| 20 | Voice Notes to Published Content | **Medium** | Content pipeline exists | Could enhance |
| 21 | Meeting Behavior Analyzer | **Low** | N/A | Skip |

---

## Priority Tiers

### Tier 1 — High Impact, Net-New (Build First)
These agents fill critical gaps in the TLDR GTM stack, particularly on the **advertiser side** which is currently under-served by the agent ecosystem.

1. **Advertiser Prospect Intelligence Agent** (Article: #1 + #2)
2. **Sales Call Transcript Analyzer** (Article: #3)
3. **Advertiser Health & Renewal Risk Agent** (Article: #11 + #14)
4. **Advertiser QBR Generator** (Article: #12)

### Tier 2 — High Impact, Enhance Existing
These extend agents that already exist but are incomplete.

5. **Competitive Battlecard Agent** (Article: #5 — extends competitive tracker)
6. **Content Repurposing Agent** (Article: #9)
7. **Content Performance Analyzer** (Article: #7 — unifies partial analytics agents)
8. **Advertiser Feedback Synthesizer** (Article: #13)

### Tier 3 — Medium Impact, Nice-to-Have
9. **Newsletter Engagement Behavior Audit** (Article: #16)
10. **GEO Enhancement for SEO Agent** (Article: #8)
11. **Competitive Tracker Website/Pricing Monitor Extension** (Article: #10)

---

## Detailed Implementation Specs

---

### Agent 1: Advertiser Prospect Intelligence Agent

**What it does:** Identifies ideal advertising prospects for TLDR newsletters by analyzing company signals — funding rounds, hiring patterns, tech stack, ad spend indicators, and industry fit.

**Why it matters:** TLDR's revenue is 100% ad-supported. Finding the right advertisers at the right time is the highest-leverage sales activity.

**Architecture:**
```
agents/sales/advertiser-prospect-agent.md          # Agent spec
python scripts/sales agent/prospect_intelligence.py # Execution script
docs/sales_assets/prospect_lists/                   # Output folder
```

**Data Sources:**
- Ahrefs MCP (existing) — identify companies spending on paid search in B2B tech
- Google Ads Portfolio MCP (existing) — companies running Google ads
- Meta Ads Portfolio MCP (existing) — companies running Meta ads
- Web search — funding announcements, hiring signals
- Competitor ad libraries — who's advertising on competitor newsletters

**Inputs:**
- `commands/core/ideal_customer_profile.md` — advertiser ICP
- `commands/core/business_context.md` — newsletter portfolio data
- `commands/core/competitor_landscape.md` — competitor advertisers to poach

**Outputs:**
- `prospect_list_{date}.csv` — Scored prospect list with columns: Company, Industry, Signal Type, Signal Detail, Estimated Budget, Newsletter Fit (which TLDR newsletters), Priority Score (1-10), Suggested Outreach Angle
- `prospect_brief_{company}.md` — Deep-dive brief per high-priority prospect

**Key Logic:**
1. Scan funding databases for recent B2B tech funding rounds ($5M+)
2. Check if funded companies are already advertising on competitor newsletters
3. Analyze their current ad spend patterns via ad transparency tools
4. Score each prospect on: budget signal strength, audience overlap with TLDR readers, newsletter vertical fit
5. Generate personalized outreach angles per prospect

---

### Agent 2: Sales Call Transcript Analyzer

**What it does:** Processes advertiser sales call transcripts (Gong/Fireflies exports) and extracts structured intelligence — objections, competitor mentions, budget signals, deal stage indicators.

**Why it matters:** Turns raw call data into actionable sales intelligence at scale. Identifies patterns across all calls that no individual AE would spot.

**Architecture:**
```
agents/sales/call-transcript-analyzer-agent.md
python scripts/sales agent/transcript_analyzer.py
docs/sales_assets/call_analysis/
```

**Inputs:**
- Folder of call transcripts (`.txt`, `.md`, `.json` from Gong/Fireflies/Otter)
- `commands/core/ideal_customer_profile.md`
- `commands/core/competitor_landscape.md`

**Outputs:**
- `call_analysis_{date}.csv` — Per-call extraction: Company, Date, Objections, Competitor Mentions, Budget Signals, Deal Stage, Key Quotes, Follow-Up Actions
- `call_insights_report_{date}.md` — Aggregate report:
  - Top 5 objections across all calls (with frequency + suggested rebuttals)
  - Most-mentioned competitors (with context)
  - Strongest buying signals (prioritized callback list)
  - Budget range patterns
  - Common feature requests / advertiser needs

**Key Logic:**
1. Parse transcripts (handle multiple formats)
2. Use LLM to extract structured fields per call
3. Aggregate across calls to find patterns
4. Cross-reference competitor mentions with `competitor_landscape.md`
5. Generate actionable insights report

---

### Agent 3: Advertiser Health & Renewal Risk Agent

**What it does:** Analyzes advertiser account health data to flag renewal risks and recommend retention interventions. Combines campaign performance data, communication frequency, and advertiser behavior signals.

**Why it matters:** Advertiser retention directly drives TLDR's revenue. Catching churn risk early is the highest-ROI CS activity.

**Architecture:**
```
agents/customer-success/advertiser-health-agent.md
python scripts/customer success agent/advertiser_health.py
docs/advertiser_success/health_reports/
```

**Inputs:**
- Advertiser performance data (CSV export from ad platform / CRM): campaign metrics, spend history, renewal dates
- Communication logs (email frequency, meeting cadence)
- `commands/core/business_context.md`

**Outputs:**
- `advertiser_health_{date}.csv` — Per-account health card:
  - Risk Level: Green / Yellow / Red
  - Days to Renewal
  - Spend Trend (increasing / stable / declining)
  - Last Contact Date
  - Campaign Performance vs. Benchmarks
  - Engagement Score
- `risk_action_plan_{date}.md` — Prioritized list of Red/Yellow accounts with:
  - Specific risk factors
  - Recommended intervention (e.g., "Schedule performance review", "Offer bonus placement", "Share case study from similar advertiser")
  - Urgency tier

**Key Logic:**
1. Ingest advertiser data (CSV or Google Sheets via MCP)
2. Score each account on: spend trend, campaign ROI, communication recency, renewal proximity
3. Apply risk thresholds calibrated to TLDR's advertiser base
4. Generate intervention playbook per at-risk account
5. Output both CSV dashboard and narrative action plan

---

### Agent 4: Advertiser QBR Generator

**What it does:** Auto-generates Quarterly Business Review documents for TLDR's advertisers, pulling campaign performance data, benchmarks, and strategic recommendations.

**Why it matters:** QBRs drive upsell and retention. Currently manual and time-intensive. Automation lets the team do QBRs for every advertiser, not just top accounts.

**Architecture:**
```
agents/customer-success/qbr-generator-agent.md
python scripts/customer success agent/qbr_generator.py
docs/advertiser_success/qbr_decks/
```

**Inputs:**
- Advertiser campaign performance data (impressions, clicks, CTR, conversions)
- Historical spend data
- Newsletter placement history
- Industry benchmarks from `commands/core/business_context.md`

**Outputs:**
- `qbr_{advertiser}_{quarter}.md` — Structured QBR document:
  - Executive Summary
  - Campaign Performance Highlights (with delta vs. previous quarter)
  - Audience Engagement Metrics (open rate, CTR for their placements)
  - ROI Analysis
  - Competitive Benchmarking (how their performance compares)
  - Strategic Recommendations (new newsletters to try, format experiments, timing optimization)
  - Proposed Next Quarter Plan (with budget recommendation)

---

### Agent 5: Competitive Battlecard Agent

**What it does:** Extends the existing competitive tracker to generate structured sales battlecards that AEs can use in advertiser pitches against LinkedIn Ads, Meta Ads, Paved, and Beehiiv.

**Architecture:**
```
agents/sales/battlecard-agent.md
python scripts/sales agent/battlecard_generator.py
docs/sales_assets/battlecards/
```

**Extends:** `agents/personas/competitive-creative-tracker-agent.md`

**Inputs:**
- `commands/core/competitor_landscape.md`
- `commands/core/business_context.md` (TLDR's positioning + metrics)
- `commands/identity/messaging_pillars.md`
- Current competitive tracker data from `docs/competitor content tracker/`
- Fresh web research on competitor pricing, features, case studies

**Outputs:**
- `battlecard_{competitor}.md` per competitor:
  - Their Pitch (how they position to advertisers)
  - Their Strengths (be honest)
  - Their Weaknesses (where TLDR wins)
  - Common Objections They Raise Against Us + Counter-Arguments
  - Win/Loss Scenarios
  - Killer Questions (questions AEs should ask to expose competitor weakness)
  - Proof Points (TLDR case studies, metrics, testimonials)

---

### Agent 6: Content Repurposing Agent

**What it does:** Takes a single long-form content piece (blog post, newsletter edition, webinar transcript) and generates a full multi-channel content kit.

**Architecture:**
```
agents/content/content-repurposing-agent.md
python scripts/content pipeline agent/repurposing/repurpose_agent.py
docs/content_assets/repurposed/
```

**Extends:** Existing content pipeline (`blog_writer_agent.py`, `social_media_agent.py`)

**Inputs:**
- Source content file (blog post, transcript, newsletter edition)
- `commands/identity/brand_voice_matrix.md`
- `commands/identity/style_guides.md`
- Target side: reader-facing or advertiser-facing

**Outputs per source piece:**
- 3x LinkedIn posts (different angles)
- 1x Twitter/X thread (8 tweets)
- 5x email subject lines for distribution
- 1x executive summary (1-pager)
- 1x newsletter blurb
- SEO meta description

---

### Agent 7: Content Performance Analyzer

**What it does:** Analyzes newsletter and blog content performance data to surface patterns — what topics, formats, headlines, and timing drive the best engagement.

**Architecture:**
```
agents/content/content-performance-agent.md
python scripts/content and seo pipeline agent/content_performance_analyzer.py
docs/content_assets/performance_reports/
```

**Unifies:** `traffic_analytics_agent.py` + `search_ranking_agent.py`

**Inputs:**
- Newsletter performance CSVs (open rates, CTR per edition per newsletter)
- Blog traffic data (CSV export from analytics)
- `docs/competitor content tracker/blogs/competitor_content_tracker.csv`

**Outputs:**
- `content_performance_report_{date}.md`:
  - Top-performing topics by open rate and CTR
  - Headline pattern analysis (what structures get highest opens)
  - Optimal send day/time correlations
  - Content length sweet spot per newsletter
  - Competitor content performance comparison
  - Recommended topics for next month

---

### Agent 8: Advertiser Feedback Synthesizer

**What it does:** Processes advertiser feedback from multiple sources (emails, call notes, survey responses, support tickets) and creates a structured synthesis.

**Architecture:**
```
agents/customer-success/feedback-synthesizer-agent.md
python scripts/customer success agent/feedback_synthesizer.py
docs/advertiser_success/feedback_reports/
```

**Inputs:**
- Advertiser feedback files (emails, survey exports, call notes)
- `commands/core/business_context.md`
- `commands/ops/customer_summary_intelligence.md`

**Outputs:**
- `feedback_synthesis_{date}.md`:
  - Top praise themes (what advertisers love)
  - Top friction points (what needs fixing)
  - Feature requests ranked by frequency and account size
  - Competitor switch triggers (why advertisers consider alternatives)
  - Net Promoter insights
  - Actionable recommendations for product, sales, and CS

---

## Implementation Order & Timeline

### Phase 1: Advertiser Revenue Protection (Week 1-2)
Build the agents that directly protect and grow advertiser revenue:

- [ ] **Agent 3:** Advertiser Health & Renewal Risk Agent
- [ ] **Agent 4:** Advertiser QBR Generator
- [ ] **Agent 8:** Advertiser Feedback Synthesizer

### Phase 2: Sales Pipeline (Week 3-4)
Build the agents that grow the advertiser pipeline:

- [ ] **Agent 1:** Advertiser Prospect Intelligence Agent
- [ ] **Agent 2:** Sales Call Transcript Analyzer  
- [ ] **Agent 5:** Competitive Battlecard Agent

### Phase 3: Content & Marketing (Week 5-6)
Enhance content operations:

- [ ] **Agent 6:** Content Repurposing Agent
- [ ] **Agent 7:** Content Performance Analyzer

### Phase 4: Extensions (Week 7+)
Nice-to-haves from Tier 3:

- [ ] Newsletter Engagement Behavior Audit
- [ ] GEO Enhancement for SEO Agent
- [ ] Competitive Tracker Website/Pricing Monitor Extension

---

## Implementation Pattern

Each agent follows the established workspace pattern:

### 1. Agent Spec (Markdown)
Located in `agents/{function}/` — defines persona, tools, inputs, outputs, workflows. Uses the existing frontmatter format:
```yaml
---
name: agent-name
description: "What it does"
color: blue
tools: Read, Write, Edit, WebFetch, WebSearch, Glob, Grep, Bash
model: inherit
---
```

### 2. Python Script
Located in `python scripts/{agent name}/` — executable automation:
- Loads context from `commands/` directory
- Uses Gemini API (consistent with `outbound_sequence_agent.py` pattern)
- Writes outputs to `docs/` directory
- Supports `--dry-run` flag
- Reads `.env` for API keys

### 3. Heartbeat / Scheduler (where applicable)
- `heartbeat_{cadence}.py` for recurring runs
- `.plist` file for macOS LaunchAgent scheduling
- Follows the `competitive_tracker.py` heartbeat pattern

### 4. Output Artifacts
Located in `docs/{domain}_assets/` — CSVs, markdown reports, structured data.

---

## MCP Tools to Leverage

| MCP Server | Use In Agents |
|---|---|
| `user-fb_ad_library` | Agent 1 (prospect identification via ad spend), Agent 5 (battlecards) |
| `user-google_ads_portfolio` | Agent 1 (prospect identification), Agent 5 (battlecards) |
| `user-meta_ads_portfolio` | Agent 1 (prospect identification), Agent 5 (battlecards) |
| `user-ahrefs` | Agent 1 (prospect SEO/paid search analysis), Agent 7 (content performance) |
| `user-gsheets` | Agent 3 (advertiser health data), Agent 4 (QBR data pull) |
| `user-google_docs` | Agent 4 (QBR output), Agent 8 (feedback docs) |
| `user-playwright` | Agent 5 (competitor website research), Agent 10 (website monitoring) |

---

## Decisions (Resolved 2026-03-10)

1. **Data availability:** No existing advertiser performance data. Created `data/advertiser_performance/` with schema and MCP placeholder. Future MCP will extract from native ad platforms and save to this folder.
2. **Call transcripts:** Not available yet. Created `docs/sales call transcripts/` for local storage. Supports .md, .txt, .json (Gong/Fireflies).
3. **Advertiser feedback:** Markdown file format.
4. **Priority:** Start with **pipeline growth agents** (Sales: Prospect Intel, Transcript Analyzer, Battlecards) before CS agents.
5. **Model choice:** **Claude API** (claude-sonnet-4-20250514) for all new agents. ANTHROPIC_API_KEY added to .env.

## Build Status

### Phase 2: Sales Pipeline (COMPLETE)
- [x] **Agent 1:** Advertiser Prospect Intelligence Agent — `agents/sales/advertiser-prospect-agent.md` + `python scripts/sales agent/prospect_intelligence.py`
- [x] **Agent 2:** Sales Call Transcript Analyzer — `agents/sales/call-transcript-analyzer-agent.md` + `python scripts/sales agent/transcript_analyzer.py`
- [x] **Agent 5:** Competitive Battlecard Agent — `agents/sales/battlecard-agent.md` + `python scripts/sales agent/battlecard_generator.py`

### Phase 1: Advertiser Revenue Protection (NEXT)
- [ ] **Agent 3:** Advertiser Health & Renewal Risk Agent
- [ ] **Agent 4:** Advertiser QBR Generator
- [ ] **Agent 8:** Advertiser Feedback Synthesizer

### Phase 3: Content & Marketing (LATER)
- [ ] **Agent 6:** Content Repurposing Agent
- [ ] **Agent 7:** Content Performance Analyzer
