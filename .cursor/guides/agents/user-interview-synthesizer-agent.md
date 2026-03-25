# User Interview Synthesizer Agent — Implementation Guide

## Classification
- Type: agent
- Domain Group: GTM Team — Product Agents
- Canonical Path: `ai system/agents/gtm team/product/user-interview-synthesizer-agent.md`

## Purpose
Summarizes and synthesizes user interviews into insights and opportunities.

## System Architecture
```mermaid
flowchart TD
  A[Context and Brief Inputs] --> B[User Interview Synthesizer Agent]
  B --> C[Processing and Reasoning Layer]
  C --> D[Structured Outputs]
  D --> E[Downstream Workflows or Storage]
```

## Functional Responsibilities
- Interpret incoming context and constraints relevant to this domain.
- Execute the core workflow implied by the canonical spec.
- Produce reusable artifacts for downstream GTM/product/content operations.

## Inputs
Raw interview transcripts or notes, segment/goal metadata.

## Outputs
Interview summaries, theme maps, jobs-to-be-done, and opportunity lists.

## Execution Pattern
- Trigger: On-demand invocation from Cursor workflows.
- Core Flow: Ingest context -> reason against domain rules -> produce artifacts.
- Dependencies: Shared context in `commands/`, datasets in `data/`, and outputs in `docs/` when applicable.

## Integration Points
- Upstream: Context briefs, CSV exports, MCP data pulls, and related agent outputs.
- Downstream: Reports, briefs, trackers, and handoffs to other agents/automations.

## Related Implementation Plans
- `google_ads_mcp_server_496b3202.plan.md` — 0/7 completed todo items.

## Reference Notes
- This guide is generated from the canonical roster and matched implementation plans.
- Use this alongside the canonical markdown spec for step-level operating detail.
