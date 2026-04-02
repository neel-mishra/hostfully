# Creative Agent Reference Playbook

## Role
This playbook converts the paid ads design bible into operational instructions for the creative agent when generating briefs or production-ready creative specs.

## Required Inputs (Agent Must Collect)
- Campaign objective (`awareness`, `consideration`, `conversion`)
- Target persona (`property manager`, `multi-unit operator`, etc.)
- Primary pain statement
- Desired outcome claim
- Proof asset availability (case metric, testimonial, product screenshot)
- Placement formats requested
- Terminology preference (`vacation rental` vs `holiday letting`)
- CTA goal (`story`, `demo`, `help`, `blueprint`)

## Retrieval Priority
1. `04_design_system/DESIGN_BIBLE.md`
2. `02_format_clusters/FORMAT_SYSTEMS.md`
3. `03_creative_families/CREATIVE_FAMILY_THESIS.md`
4. `05_copy_frameworks/COPY_AND_MESSAGE_SYSTEM.md`
5. `06_canva_execution/CANVA_PRODUCTION_PLAYBOOK.md`
6. `01_catalog/image_catalog.csv` for references

## Brief Generation Output Schema
Agent output should include:
- `concept_name`
- `creative_family`
- `funnel_stage`
- `primary_hook`
- `supporting_proof`
- `visual_direction`
- `layout_spec`
- `color_spec`
- `typography_spec`
- `cta_spec`
- `variant_plan` (3-5 variants)
- `canva_build_steps`
- `quality_checklist`

## Creative Family Selection Logic
- If objective is broad CTR lift and product familiarity: choose `Calendar / Availability UI`.
- If objective is pain capture and quick conversion: choose `Spreadsheet Pain / PMS Relief`.
- If objective is trust + intent deepening: choose `Proof / Scale Story`.
- If objective is monetization narrative: choose `Guidebook / Add-On Revenue`.
- If objective is pattern interrupt and memorability: choose `Mascot / Support System`.
- If objective is operational automation proof: choose `Smart Locks / Automation`.

## Prompt Contract for Creative Generation
Use this structure:
1. State audience and pain.
2. State target outcome and numeric token.
3. Select one creative family and one format.
4. Enforce logo/headline/CTA anchors.
5. Require one strong high-contrast text block.
6. Require CTA from approved taxonomy.
7. Require 3 controlled variants with only one major variable changed per variant.

## Guardrails
- Never output visuals that break top-left brand lock convention unless explicitly instructed.
- Never produce low-contrast headline over complex imagery.
- Never omit CTA in conversion-intent placements.
- Avoid copy that is generic, abstract, or not tied to a concrete visual proof.

## Scoring Rubric (Agent Self-Evaluation)
- Brand fidelity (0-2)
- Message clarity (0-2)
- Visual hierarchy (0-2)
- Format-safe execution (0-2)
- Conversion intent alignment (0-2)

Minimum score to ship: `8/10`.

## Example Agent Task Packet
- Audience: mid-size property managers in spreadsheet workflows
- Goal: conversion
- Formats: `1080x1350`, `1080x1920`
- Hook: `Is your vacation rental business stuck in spreadsheets?`
- CTA: `Let us help`
- Family: `Spreadsheet Pain / PMS Relief`
- Variants:
  - A: blue headline
  - B: gradient headline
  - C: mint headline

## Asset Referencing Pattern
When recommending visual references, cite file paths from `00_source_images` and include:
- format class
- family guess
- relevant motif
- why reference is appropriate

