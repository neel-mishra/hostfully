# Feedback Synthesizer Agent (Execution Commander) — Implementation Guide

## Classification
- Type: agent
- Domain Group: Execution Commander Agents
- Canonical Path: `ai system/agents/execution commander/feedback-synthesizer-agent.md`

## Purpose
Meta-synthesizer that rolls up feedback from multiple agents or workflows.

## System Architecture
```mermaid
flowchart TD
  A[Context and Brief Inputs] --> B[Feedback Synthesizer Agent (Execution Commander)]
  B --> C[Processing and Reasoning Layer]
  C --> D[Structured Outputs]
  D --> E[Downstream Workflows or Storage]
```

## Functional Responsibilities
- Interpret incoming context and constraints relevant to this domain.
- Execute the core workflow implied by the canonical spec.
- Produce reusable artifacts for downstream GTM/product/content operations.

## Inputs
Outputs from other agents (reports, CSVs, logs), goals or questions.

## Outputs
Consolidated summaries and cross-agent insights.

## Execution Pattern
- Trigger: On-demand invocation from Cursor workflows.
- Core Flow: Ingest context -> reason against domain rules -> produce artifacts.
- Dependencies: Shared context in `commands/`, datasets in `data/`, and outputs in `docs/` when applicable.

## Integration Points
- Upstream: Context briefs, CSV exports, MCP data pulls, and related agent outputs.
- Downstream: Reports, briefs, trackers, and handoffs to other agents/automations.

## Related Implementation Plans
- `claude_skill_builder_agent_52a1e919.plan.md` — 1/1 completed todo items.
- `cursor_automations_brainstorm_97eb7e7d.plan.md` — 10/10 completed todo items.
- `meta-ads-mcp-server_8b920550.plan.md` — 4/4 completed todo items.

## Reference Notes
- This guide is generated from the canonical roster and matched implementation plans.
- Use this alongside the canonical markdown spec for step-level operating detail.
