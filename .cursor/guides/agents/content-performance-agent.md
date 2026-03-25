# Content Performance Agent — Implementation Guide

## Classification
- Type: agent
- Domain Group: GTM Team — Marketing Agents
- Canonical Path: `ai system/agents/gtm team/marketing/content-performance-agent.md`

## Purpose
Analyzes newsletter and blog performance to identify top topics, formats, and timing patterns.

## System Architecture
```mermaid
flowchart TD
  A[Context and Brief Inputs] --> B[Content Performance Agent]
  B --> C[Processing and Reasoning Layer]
  C --> D[Structured Outputs]
  D --> E[Downstream Workflows or Storage]
```

## Functional Responsibilities
- Interpret incoming context and constraints relevant to this domain.
- Execute the core workflow implied by the canonical spec.
- Produce reusable artifacts for downstream GTM/product/content operations.

## Inputs
Newsletter performance CSVs, blog traffic/analytics exports, competitor content tracker data.

## Outputs
Content performance reports with topic and headline patterns, send time insights, benchmarks, and next-topic recommendations.

## Execution Pattern
- Trigger: On-demand invocation from Cursor workflows.
- Core Flow: Ingest context -> reason against domain rules -> produce artifacts.
- Dependencies: Shared context in `commands/`, datasets in `data/`, and outputs in `docs/` when applicable.

## Integration Points
- Upstream: Context briefs, CSV exports, MCP data pulls, and related agent outputs.
- Downstream: Reports, briefs, trackers, and handoffs to other agents/automations.

## Related Implementation Plans
- No directly matching implementation plan found in `.cursor/plans`; guide synthesized from canonical roster/specs.

## Reference Notes
- This guide is generated from the canonical roster and matched implementation plans.
- Use this alongside the canonical markdown spec for step-level operating detail.
