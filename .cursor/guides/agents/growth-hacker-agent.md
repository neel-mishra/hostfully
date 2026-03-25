# Growth Hacker Agent — Implementation Guide

## Classification
- Type: agent
- Domain Group: Persona & Role Agents
- Canonical Path: `ai system/agents/personas/growth-hacker-agent.md`

## Purpose
Persona preset for scrappy growth ideation layered on top of CRO and product strategy agents.

## System Architecture
```mermaid
flowchart TD
  A[Context and Brief Inputs] --> B[Growth Hacker Agent]
  B --> C[Processing and Reasoning Layer]
  C --> D[Structured Outputs]
  D --> E[Downstream Workflows or Storage]
```

## Functional Responsibilities
- Interpret incoming context and constraints relevant to this domain.
- Execute the core workflow implied by the canonical spec.
- Produce reusable artifacts for downstream GTM/product/content operations.

## Inputs
Growth goals, current channels, constraints, audience.

## Outputs
Experiment backlogs and playbooks to be run via canonical CRO/experimentation flows.

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
