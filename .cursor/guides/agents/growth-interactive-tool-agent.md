# Growth Interactive Tool Agent — Implementation Guide

## Classification
- Type: agent
- Domain Group: Technical & Growth Engineering Agents
- Canonical Path: `ai system/agents/technical/growth-interactive-tool-agent.md`

## Purpose
Designs interactive tools or calculators as growth assets.

## System Architecture
```mermaid
flowchart TD
  A[Context and Brief Inputs] --> B[Growth Interactive Tool Agent]
  B --> C[Processing and Reasoning Layer]
  C --> D[Structured Outputs]
  D --> E[Downstream Workflows or Storage]
```

## Functional Responsibilities
- Interpret incoming context and constraints relevant to this domain.
- Execute the core workflow implied by the canonical spec.
- Produce reusable artifacts for downstream GTM/product/content operations.

## Inputs
Growth goal, target audience, existing content and assets.

## Outputs
Specs for tools (flows, inputs/outputs, UX notes).

## Execution Pattern
- Trigger: On-demand invocation from Cursor workflows.
- Core Flow: Ingest context -> reason against domain rules -> produce artifacts.
- Dependencies: Shared context in `commands/`, datasets in `data/`, and outputs in `docs/` when applicable.

## Integration Points
- Upstream: Context briefs, CSV exports, MCP data pulls, and related agent outputs.
- Downstream: Reports, briefs, trackers, and handoffs to other agents/automations.

## Related Implementation Plans
- `cursor_automations_brainstorm_97eb7e7d.plan.md` — 10/10 completed todo items.

## Reference Notes
- This guide is generated from the canonical roster and matched implementation plans.
- Use this alongside the canonical markdown spec for step-level operating detail.
