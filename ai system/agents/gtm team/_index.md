# GTM Team Agent Suite

Agents organized by GTM function, inspired by [Claude Code for GTM Teams](https://thegtmnewsletter.substack.com/p/claude-code-for-gtm-teams). Each function folder contains agent specs; execution scripts live in `ai system/python scripts/`.

---

## Sales (`sales/`) — 6 use cases

Pipeline growth agents — find prospects, analyze calls, arm AEs with competitive intelligence.

| Agent | Script | What It Does |
|---|---|---|
| [advertiser-prospect-agent](sales/advertiser-prospect-agent.md) | `ai system/python scripts/sales agent/prospect_intelligence.py` | Identifies ideal advertising prospects via funding signals, ad spend patterns, and competitor newsletter activity. Scores and generates briefs. |
| [call-transcript-analyzer-agent](sales/call-transcript-analyzer-agent.md) | `ai system/python scripts/sales agent/transcript_analyzer.py` | Extracts objections, competitor mentions, budget signals, and deal stage from sales call transcripts. Batch or single-file. |
| [battlecard-agent](sales/battlecard-agent.md) | `ai system/python scripts/sales agent/battlecard_generator.py` | Generates competitive battlecards against LinkedIn Ads, Google Ads, Meta, Paved, Beehiiv, and podcasts. Includes talk tracks and killer questions. |
| [email-sequence-agent](../content/email-sequence-agent.md) | *(agent spec — manual execution)* | Canonical email engine for cold outbound, warm nurture, lifecycle, and product updates. Use Cold Outbound mode for sales outreach. |
| [deal-risk-agent](sales/deal-risk-agent.md) | `ai system/python scripts/sales agent/deal_risk_analyzer.py` | Analyzes deal notes/email threads to assess pipeline health. Flags at-risk deals with save actions. |

## Marketing (`marketing/`) — 6 use cases

Content optimization, competitive intelligence, and distribution agents.

| Agent | Script | What It Does |
|---|---|---|
| [competitor-ad-intelligence-agent](marketing/paid%20ads/competitor-ad-intelligence-agent.md) | `ai system/python scripts/competitor content tracker/competitive_tracker.py` | Monitors competitor ad activity across Meta, Google, LinkedIn, TikTok, X. Monthly automated scraping + deep dives. |
| [content-performance-agent](marketing/content-performance-agent.md) | `ai system/python scripts/content and seo pipeline agent/content_performance_analyzer.py` | Analyzes newsletter/blog metrics to find topic, headline, and timing patterns. |
| [seo-audit-agent](../seo-aeo/seo-audit-agent.md) | `ai system/python scripts/seo agent/seo_auditor.py` | Canonical technical + on-page SEO audit. Covers rankings, meta tags, and site health. |
| [content-repurposing-agent](marketing/content-repurposing-agent.md) | `ai system/python scripts/content pipeline agent/repurposing/repurpose_agent.py` | Turns one content piece into LinkedIn posts, Twitter threads, email subjects, newsletter blurbs, and summaries. |
| [seo-agent](../seo-aeo/seo-agent.md) | *(agent spec — manual execution)* | Canonical SEO strategy agent. Use GEO mode for localized and AI-search-focused keyword research. |
| [cro-agent](../technical/cro-agent.md) | *(agent spec — manual execution)* | Canonical CRO agent for page audits and experiments. Use Landing Page Test mode for landing-page A/B plans. |

## Customer Success (`customer success/`) — 5 use cases

Advertiser retention and intelligence agents.

| Agent | Script | What It Does |
|---|---|---|
| [advertiser-health-agent](customer%20success/advertiser-health-agent.md) | `ai system/python scripts/customer success agent/advertiser_health.py` | Scores advertiser accounts Green/Yellow/Red on 5 risk dimensions (Renewal Risk Analyzer). |
| [support-ticket-analyzer-agent](customer%20success/support-ticket-analyzer-agent.md) | `ai system/python scripts/customer success agent/support_ticket_analyzer.py` | Analyzes support ticket patterns to find systemic issues, product gaps, and process failures. |
| [churn-analyzer-agent](customer%20success/churn-analyzer-agent.md) | `ai system/python scripts/customer success agent/churn_analyzer.py` | Post-mortem analysis of churned advertisers + churn signal dashboard. Identifies drivers, assesses preventability, builds prevention playbook. |
| [qbr-generator-agent](customer%20success/qbr-generator-agent.md) | `ai system/python scripts/customer success agent/qbr_generator.py` | Auto-generates Quarterly Business Reviews from campaign performance data. |
| [feedback-synthesizer-agent](../execution%20commander/feedback-synthesizer-agent.md) | `ai system/python scripts/customer success agent/feedback_synthesizer.py` | Canonical feedback synthesizer. Use Advertiser Feedback mode for CS/sales/product recommendations. |

## Product (`product/`) — 5 use cases

Product intelligence from customer signals.

| Agent | Script | What It Does |
|---|---|---|
| [feature-request-prioritizer-agent](product/feature-request-prioritizer-agent.md) | `ai system/python scripts/product agent/feature_request_prioritizer.py` | Aggregates feature requests from all sources, deduplicates, scores on impact/effort/frequency, produces ranked backlog. |
| [release-notes-agent](product/release-notes-agent.md) | `ai system/python scripts/product agent/release_notes_generator.py` | Transforms raw release notes into advertiser-facing, reader-facing, and internal changelogs. |
| [user-interview-synthesizer-agent](product/user-interview-synthesizer-agent.md) | `ai system/python scripts/product agent/interview_synthesizer.py` | Extracts JTBD, pain points, feature wishes, competitor mentions from interview transcripts. Per-interview + cross-interview synthesis. |
| [prd-task-breakdown-agent](product/prd-task-breakdown-agent.md) | *(agent spec — manual execution)* | Creates comprehensive PRDs with technical architecture, user research, and implementation roadmaps. Breaks into tasks. |
| [competitive-feature-matrix-agent](product/competitive-feature-matrix-agent.md) | `ai system/python scripts/product agent/competitive_feature_matrix.py` | Feature-by-feature comparison matrix: Hostfully vs LinkedIn, Google, Meta, Paved, Beehiiv. Identifies gaps and roadmap recs. |

---

## Screenshot ↔ Agent Mapping

| Screenshot Use Case | Agent | Status |
|---|---|---|
| **Sales** | | |
| Identify Leads from Codebase | advertiser-prospect-agent | ✅ |
| Scrape Public Data for Prospects | advertiser-prospect-agent | ✅ |
| Analyze Call Transcripts at Scale | call-transcript-analyzer-agent | ✅ |
| Personalized Outreach Sequences | email-sequence-agent (Cold Outbound mode) | ✅ |
| Competitive Battlecard Builder | battlecard-agent | ✅ |
| Deal Risk Analysis from Notes | deal-risk-agent | ✅ |
| **Marketing** | | |
| Competitor Ad Intelligence | competitor-ad-intelligence-agent | ✅ |
| Content Performance Analyzer | content-performance-agent | ✅ |
| SEO / GEO Keyword Research | seo-audit-agent + seo-agent (GEO mode) | ✅ |
| Repurpose Content → 5 Channels | content-repurposing-agent | ✅ |
| Self-Updating Competitive Tracker | competitor-ad-intelligence-agent (heartbeat) | ✅ |
| Landing Page A/B Test Generator | cro-agent (Landing Page Test mode) | ✅ |
| **Customer Success** | | |
| Renewal Risk Analyzer | advertiser-health-agent | ✅ |
| QBR Deck Auto-Generator | qbr-generator-agent | ✅ |
| Support Ticket Pattern Analyzer | support-ticket-analyzer-agent | ✅ |
| Customer Feedback Synthesizer | feedback-synthesizer-agent (Advertiser Feedback mode) | ✅ |
| Churn Signal Dashboard Builder | churn-analyzer-agent | ✅ |
| **Product** | | |
| Feature Request Prioritizer | feature-request-prioritizer-agent | ✅ |
| Release Notes → Changelog | release-notes-agent | ✅ |
| User Interview Synthesizer | user-interview-synthesizer-agent | ✅ |
| PRD → Task Breakdown Generator | prd-task-breakdown-agent | ✅ |
| Competitive Feature Matrix | competitive-feature-matrix-agent | ✅ |

**22/22 use cases covered.**

---

## Agent Data Flow

```
                    ┌─────────────────┐
                    │  Signal Sources  │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
    │  Sales  │        │Marketing│        │   CS    │
    │  Calls  │        │ Content │        │Feedback │
    └────┬────┘        └────┬────┘        └────┬────┘
         │                   │                   │
    ┌────▼────┐        ┌────▼────┐        ┌────▼────┐
    │Transcript│       │Perf.    │        │Feedback │
    │Analyzer │        │Analyzer │        │Synth.   │
    └────┬────┘        └────┬────┘        └────┬────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
         ┌────▼────┐   ┌────▼────┐   ┌────▼────┐
         │Feature  │   │Sprint   │   │Comp.    │
         │Request  │   │Planner  │   │Feature  │
         │Prior.   │   │         │   │Matrix   │
         └─────────┘   └─────────┘   └─────────┘
```

## Quick Start

```bash
# Set API key
echo 'ANTHROPIC_API_KEY=sk-ant-...' >> .env

# Install deps (same for all agents)
pip install requests python-dotenv

# Run any agent
python "ai system/python scripts/sales agent/prospect_intelligence.py" --dry-run
python "ai system/python scripts/sales agent/transcript_analyzer.py" --dry-run
python "ai system/python scripts/sales agent/battlecard_generator.py" --dry-run
python "ai system/python scripts/sales agent/deal_risk_analyzer.py" --dir path/to/notes/ --dry-run
python "ai system/python scripts/customer success agent/advertiser_health.py" --dry-run
python "ai system/python scripts/customer success agent/qbr_generator.py" --advertiser "Example" --dry-run
python "ai system/python scripts/customer success agent/feedback_synthesizer.py" --dry-run
python "ai system/python scripts/customer success agent/churn_analyzer.py" --advertiser "Example" --dry-run
python "ai system/python scripts/customer success agent/support_ticket_analyzer.py" --dry-run
python "ai system/python scripts/content pipeline agent/repurposing/repurpose_agent.py" --file content.md --dry-run
python "ai system/python scripts/content and seo pipeline agent/content_performance_analyzer.py" --newsletter-data data.csv --dry-run
python "ai system/python scripts/product agent/engagement_behavior.py" --data engagement.csv --dry-run
python "ai system/python scripts/product agent/sprint_planner.py" --dry-run
python "ai system/python scripts/product agent/feature_request_prioritizer.py" --dry-run
python "ai system/python scripts/product agent/release_notes_generator.py" --file notes.md --dry-run
python "ai system/python scripts/product agent/interview_synthesizer.py" --dry-run
python "ai system/python scripts/product agent/competitive_feature_matrix.py" --dry-run
```
