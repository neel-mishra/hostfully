# n8n Workflow Agent — Implementation Guide

## Classification
- Type: agent
- Domain Group: Technical & Growth Engineering Agents
- Canonical Path: `ai system/agents/technical/n8n-workflow-agent.md`

## Purpose
Designs automation workflows for n8n (or similar) based on your processes.

## System Architecture
```mermaid
flowchart TD
  A[Context and Brief Inputs] --> B[n8n Workflow Agent]
  B --> C[Processing and Reasoning Layer]
  C --> D[Structured Outputs]
  D --> E[Downstream Workflows or Storage]
```

## Functional Responsibilities
- Interpret incoming context and constraints relevant to this domain.
- Execute the core workflow implied by the canonical spec.
- Produce reusable artifacts for downstream GTM/product/content operations.

## Inputs
Desired automation description, tools/APIs involved, triggers and outputs.

## Outputs
Workflow diagrams, node-by-node specs, and suggested error handling.

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
- `vibehypevideopipeline_af86b17c.plan.md` — 0/6 completed todo items.

## Reference Notes
- This guide is generated from the canonical roster and matched implementation plans.
- Use this alongside the canonical markdown spec for step-level operating detail.
