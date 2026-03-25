# Copywriting Agent — Implementation Guide

## Classification
- Type: agent
- Domain Group: Content & Copy Agents
- Canonical Path: `ai system/agents/content/copywriting-agent.md`

## Purpose
Canonical content-writing agent for page copy, long-form content, and conversion-oriented rewrites.

## System Architecture
```mermaid
flowchart TD
  A[Context and Brief Inputs] --> B[Copywriting Agent]
  B --> C[Processing and Reasoning Layer]
  C --> D[Structured Outputs]
  D --> E[Downstream Workflows or Storage]
```

## Functional Responsibilities
- Interpret incoming context and constraints relevant to this domain.
- Execute the core workflow implied by the canonical spec.
- Produce reusable artifacts for downstream GTM/product/content operations.

## Inputs
Page type, audience, offer, product marketing context, brand voice preferences.

## Outputs
Structured page/long-form copy drafts, alternatives, and conversion-focused edits.

## Execution Pattern
- Trigger: On-demand invocation from Cursor workflows.
- Core Flow: Ingest context -> reason against domain rules -> produce artifacts.
- Dependencies: Shared context in `commands/`, datasets in `data/`, and outputs in `docs/` when applicable.

## Integration Points
- Upstream: Context briefs, CSV exports, MCP data pulls, and related agent outputs.
- Downstream: Reports, briefs, trackers, and handoffs to other agents/automations.

## Related Implementation Plans
- `ad_creative_agent_expansion_8e339288.plan.md` — 8/8 completed todo items.

## Reference Notes
- This guide is generated from the canonical roster and matched implementation plans.
- Use this alongside the canonical markdown spec for step-level operating detail.
