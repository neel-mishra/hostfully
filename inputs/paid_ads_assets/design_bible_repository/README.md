# Paid Ads Design Bible Repository

This repository is the canonical creative-reference system for Hostfully paid ads.  
It combines visual references (all attached live ad images) with a structured design thesis for creative strategy, briefing, and Canva production.

## Folder Map

- `00_source_images/`
  - All attached ad images (`126`) copied as immutable reference assets.
- `01_catalog/`
  - `image_catalog.csv` - machine-readable metadata index for all source images.
- `02_format_clusters/`
  - Format-specific image groupings and `FORMAT_SYSTEMS.md`.
- `03_creative_families/`
  - `CREATIVE_FAMILY_THESIS.md` - recurring concept family playbook.
- `04_design_system/`
  - `DESIGN_BIBLE.md` - canonical design rules for layout, typography, color, CTA.
- `05_copy_frameworks/`
  - `COPY_AND_MESSAGE_SYSTEM.md` - copy architecture and hook/CTA systems.
- `06_canva_execution/`
  - `CANVA_PRODUCTION_PLAYBOOK.md` - implementation rules for Canva.
- `07_agent_playbooks/`
  - `CREATIVE_AGENT_REFERENCE.md` - agent prompt contracts and scoring rubric.
- `SYNTHESIZED_DESIGN_THESIS.md`
  - High-level strategic synthesis across all designs.

## How To Use (Human Designers)
1. Start with `SYNTHESIZED_DESIGN_THESIS.md`.
2. Pick your target format from `02_format_clusters/FORMAT_SYSTEMS.md`.
3. Pick a concept family from `03_creative_families/CREATIVE_FAMILY_THESIS.md`.
4. Build message framing from `05_copy_frameworks/COPY_AND_MESSAGE_SYSTEM.md`.
5. Execute in Canva via `06_canva_execution/CANVA_PRODUCTION_PLAYBOOK.md`.

## How To Use (Creative Agent)
1. Retrieve rules in this order:
   1. `04_design_system/DESIGN_BIBLE.md`
   2. `02_format_clusters/FORMAT_SYSTEMS.md`
   3. `03_creative_families/CREATIVE_FAMILY_THESIS.md`
   4. `05_copy_frameworks/COPY_AND_MESSAGE_SYSTEM.md`
   5. `06_canva_execution/CANVA_PRODUCTION_PLAYBOOK.md`
2. Pull image examples from `01_catalog/image_catalog.csv`.
3. Generate brief and variants using `07_agent_playbooks/CREATIVE_AGENT_REFERENCE.md`.

## Design Intent Summary
- Preserve high-recognition brand anchors (logo top-left + high-contrast CTA).
- Keep one clear claim and one dominant token (`2x`, `350x`, `8%`, etc.).
- Pair every claim with supporting visual evidence.
- Use controlled variation, not random redesigns.

## Integration with Existing Paid Ads Inputs
This folder is additive and does not replace planning assets in:
- `inputs/paid_ads_assets/campaign_playbook_monthly.csv`
- `inputs/paid_ads_assets/Hostfully_Campaign_Playbook_March2026_Campaign_Structure_and_Budget.csv`

Use both systems together:
- campaign playbook = media structure and budget allocation
- design bible repository = creative production intelligence

