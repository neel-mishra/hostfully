# Connector Backlog

Prioritized implementation backlog for eliminating manual input dependencies while preserving zero-breakage fallbacks.

## Priority Model

- **P0**: Reliability and safety prerequisites
- **P1**: Highest-impact input automation connectors
- **P2**: Inter-workflow orchestration and scaling

## Backlog Table

| Priority | Connector / Capability | Primary Dependencies Replaced | Target Components | Effort | Owner Suggestion | Fallback Strategy | Exit Criteria |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P0 | Preflight health gate | Manual discovery of missing creds/paths/schema | `ai system/automations/lib/*.py`, orchestration wrappers | M | Platform/Infra | Skip connector and run manual pathway | All workflows fail fast with actionable diagnostics |
| P0 | Canonical path resolver (`docs` vs `outputs/docs`) | Manual path syncing/copying | `ai system/python scripts/*`, `ai system/automations/*` | M | Platform/Infra | Dual-read path resolution | No file-not-found due to path drift for 3 cycles |
| P0 | Run ledger + idempotency keys | Duplicate writes/manual rerun cleanup | all scheduled workflows | M | Platform/Infra | Manual rerun with unique run_id | Duplicate output rate near zero |
| P0 | Atomic artifact writer | Partial/corrupt output files | report and CSV generators | S | Platform/Infra | Retain previous artifact on write failure | No partial artifacts in QA runs |
| P1 | Advertiser performance ingestion connector | Manual `data/advertiser_performance` seeding | CS scripts (`advertiser_health.py`, `qbr_generator.py`, `churn_analyzer.py`) | M | CS Data + Ads Data | Manual CSV import remains enabled | 100% CS workflows consume canonical ingested dataset |
| P1 | Campaign resolver service | Manual `CAMPAIGN_ID` placeholder substitution | automations 4, 6, 9 and ads scripts | M | Paid Ads Eng | Operator override list | Placeholder-based runs no longer needed |
| P1 | Date/period resolver utility | Manual date placeholder substitutions | automations 1, 5, 7, 8, 9, 10 | S | Platform | Manual date CLI override | No literal date placeholders in live runs |
| P1 | Competitor entity registry | Manual competitor list curation duplication | automations 3, 5, 7, 10 + tracker scripts | M | Marketing Ops | Static yaml fallback | Single canonical competitor source adopted everywhere |
| P1 | Transcript/ticket ingestion queue | Manual transcript and ticket file drops | sales/customer success analyzers | L | RevOps + CS Ops | Manual drop folder remains active | Auto ingestion pipeline handles >=80% of weekly volume |
| P1 | Non-interactive creative intake mode | `input()` prompts in creative flow | `meta_creative_agent.py` and paid creative chain | M | Paid Creative Eng | Interactive CLI mode retained | Creative pipeline runs unattended from JSON brief |
| P1 | Deterministic KPI calculator layer | Prompt-only KPI math in reports | weekly/monthly analytics automations | M | Data Eng | Narrative-only fallback with KPI source labels | KPI drift eliminated across reruns |
| P2 | Event contract emitter (`artifact.ready`) | Manual/downstream polling by latest file | all producing workflows | M | Platform | Polling fallback mode | >=70% downstream runs triggered automatically |
| P2 | Watcher trigger service | Manual starts after upstream outputs | content, SEO, sales, CS chains | M | Platform | Scheduled polling fallback | Downstream kickoff latency reduced significantly |
| P2 | Manifest DAG orchestration | Implicit folder dependency assumptions | cross-automation handoffs | L | Platform Architecture | Existing schedule/manual orchestrators | Dependency failures become explicit and recoverable |
| P2 | Retrieval cache with freshness policy | Repeated manual reruns on flaky APIs | Ahrefs/Meta/Google pull consumers | M | Data Platform | Last-known-good snapshot + freshness warnings | Reduced API failure impact and faster reruns |
| P2 | Progressive enrichment layer | Full stop when one source missing | convergence, GTM commander, sales intelligence | M | Platform + Domain Owners | Degraded mode with missing-source annotations | Pipelines continue with confidence-marked outputs |

## Contract Backlog (Cross-Workflow)

| Contract | Producer | Consumers | Minimal Required Fields |
| --- | --- | --- | --- |
| `campaign_performance_snapshot` | ad data ingestion + dashboards | health monitor, GTM commander, ad reports | account_id, campaign_id, date, spend, impressions, clicks, ctr, conversions |
| `content_pipeline_item` | daily content pipeline | weekly execution, SEO intelligence, CRO audit | item_id, topic, score, source_url, created_at, logical_period |
| `advertiser_health_score` | bi-weekly health monitor | GTM commander, CS summaries | advertiser_id, risk_level, risk_factors, score_date, source_snapshot_ref |
| `sales_prospect_score` | weekly sales intelligence | battlecards, pipeline sheet | company_domain, company_name, score, tier, reasons, generated_at |
| `competitor_entity` | registry service | ad intelligence, SEO intelligence, convergence report | competitor_id, name, domain, channels, active_flag |
| `cro_page_observation` | weekly CRO audit | product/sprint planning | url, capture_ts, issue_type, confidence, recommendation |
| `gtm_plan_artifact` | monthly GTM commander | execution workflows | month, priorities, owners, dependencies, source_refs |

## Rollout Sequence

1. P0 controls before any connector cutover.
2. P1 ingestion connectors by highest manual burden.
3. P2 interlinking/event architecture once data contracts stabilize.

## Operational Safeguards (Always-On)

- Manual source remains available until cutover criteria pass.
- Dual-read migration for every new connector.
- Circuit breaker + snapshot fallback + degraded-mode labeling.
- Rollback pointer to previous connector version.
- Weekly regression checks between new and legacy outputs.
