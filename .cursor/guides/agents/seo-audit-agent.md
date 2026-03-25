# SEO Audit Agent (Technical/Deep) — Implementation Guide

## Classification
- Type: agent
- Domain Group: SEO & AEO Agents
- Canonical Path: `ai system/agents/seo-aeo/seo-audit-agent.md`

## Purpose
Deep technical + content SEO auditor integrated with `seo_auditor.py`.

## System Architecture
```mermaid
flowchart TD
  A[Context and Brief Inputs] --> B[SEO Audit Agent (Technical/Deep)]
  B --> C[Processing and Reasoning Layer]
  C --> D[Structured Outputs]
  D --> E[Downstream Workflows or Storage]
```

## Functional Responsibilities
- Interpret incoming context and constraints relevant to this domain.
- Execute the core workflow implied by the canonical spec.
- Produce reusable artifacts for downstream GTM/product/content operations.

## Inputs
Company name, sitemap, crawl limit, flags for PSI/headless, GSC credentials (optional).

## Outputs
URL inventories, CSVs, high-level and detailed audit reports, prioritized action plans.

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
