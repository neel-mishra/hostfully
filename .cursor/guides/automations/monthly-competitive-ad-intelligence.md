# Monthly Competitive Ad Intelligence — Implementation Guide

## Classification
- Type: automation
- Tier/Group: Tier 1 — LaunchAgent Replacements (Core Schedulers)
- Schedule: Monthly, last day of month.

## Purpose
Replaces `com.tldr.tech.competitivetracker.monthly.plist`. Consolidates cross-platform competitor ad intelligence and TLDR’s own performance.

## System Architecture
```mermaid
flowchart LR
  T[Scheduled Trigger: Monthly, last day of month.] --> I[Data and Context Ingestion]
  I --> O[Monthly Competitive Ad Intelligence Orchestration]
  O --> R[Reports, Trackers, and Documents]
  R --> F[Team Review and Follow-up Actions]
```

## Functional Responsibilities
- Execute the recurring workflow at the configured cadence.
- Pull required MCP/script/context dependencies.
- Produce operational artifacts for GTM, product, content, and CS teams.

## Inputs
- Competitor brand/account lists.
- Meta Ad Library MCP (platform ID + ads endpoints).
- Meta Ads Portfolio MCP (accounts, campaigns, performance).
- Google Ads Portfolio MCP (accounts, campaigns, performance).
- Paths to `ad_creative_log.csv` and `ad_volume_tracker.csv`.

## Outputs
- Refreshed competitor ad creative and volume trackers (CSVs).
- Narrative creative brief comparing competitor strategies vs your performance.
- Google Doc report for monthly review.

## Execution Pattern
- Trigger: Scheduler-based execution.
- Core Flow: Collect signals -> run orchestration -> emit reports and artifacts.
- Dependencies: MCP servers, Python scripts, CSV trackers, and Google Docs/Sheets endpoints.

## Integration Points
- Upstream: MCP data sources, internal trackers, and prior automation outputs.
- Downstream: Planning reviews, campaign updates, content roadmap decisions, and account actions.

## Related Implementation Plans
- `update_paths_for_docs_reorg_b0f5c8bd.plan.md` — 7/7 completed todo items.
- `ad_creative_agent_expansion_8e339288.plan.md` — 8/8 completed todo items.
- `paid-budget-spend-tracker_a431b9c4.plan.md` — 4/7 completed todo items.

## Reference Notes
- This guide is generated from your automation roster and matched implementation plans.
- Pair this with runbooks/config files for step-level operating instructions.
