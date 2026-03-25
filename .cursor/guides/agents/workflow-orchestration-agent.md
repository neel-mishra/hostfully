# Workflow Orchestration Agent — Implementation Guide

## Classification
- Type: agent
- Domain Group: Execution Commander Agents
- Canonical Path: `ai system/agents/execution commander/workflow-orchestration-agent.md`

## Purpose
High-level orchestrator that chains multiple ai system/agents/scripts into end-to-end workflows.

## System Architecture
```mermaid
flowchart TD
  A[Context and Brief Inputs] --> B[Workflow Orchestration Agent]
  B --> C[Processing and Reasoning Layer]
  C --> D[Structured Outputs]
  D --> E[Downstream Workflows or Storage]
```

## Functional Responsibilities
- Interpret incoming context and constraints relevant to this domain.
- Execute the core workflow implied by the canonical spec.
- Produce reusable artifacts for downstream GTM/product/content operations.

## Inputs
Desired workflow description, list of component agents, scheduling/context.

## Outputs
Orchestrated run plans, status summaries, and combined output artifacts.

## Execution Pattern
- Trigger: On-demand invocation from Cursor workflows.
- Core Flow: Ingest context -> reason against domain rules -> produce artifacts.
- Dependencies: Shared context in `commands/`, datasets in `data/`, and outputs in `docs/` when applicable.

## Integration Points
- Upstream: Context briefs, CSV exports, MCP data pulls, and related agent outputs.
- Downstream: Reports, briefs, trackers, and handoffs to other agents/automations.

## Related Implementation Plans
- `cursor_automations_brainstorm_97eb7e7d.plan.md` — 10/10 completed todo items.
- `google_ads_mcp_server_496b3202.plan.md` — 0/7 completed todo items.
- `claude_skill_builder_agent_52a1e919.plan.md` — 1/1 completed todo items.

## Reference Notes
- This guide is generated from the canonical roster and matched implementation plans.
- Use this alongside the canonical markdown spec for step-level operating detail.
