# Canva Production Playbook

## Purpose
Translate the design bible into deterministic Canva production steps so output quality is consistent across designers and agents.

## Template Stack to Maintain
- `Square Feed` - `1080x1080`
- `Portrait Feed` - `1080x1350`
- `Story/Reel` - `1080x1920`
- `Landscape` - `1200x628`

Each template should include:
- locked safe-zone guides
- predefined logo placeholder
- headline text style presets
- CTA component variant set

## Layer Order Standard (Top to Bottom)
1. Logo group
2. Headline group
3. CTA group
4. Supporting badges/icons/chips
5. Hero UI/object group
6. Background overlay/gradient
7. Base background image/color

## Build Recipe (Per Creative)
1. Select format template.
2. Drop in core background (flat, gradient, or photo).
3. Add hero visual (UI mockup, person, mascot, chart).
4. Set logo in top-left with required insets.
5. Place headline in approved text zone.
6. Bold only core proof/benefit token.
7. Insert CTA component from library.
8. Add optional supporting chips/icons if they reinforce message.
9. Run QA checklist.
10. Export using placement-specific settings.

## Component Specs

## Logo
- Keep as vector or transparent PNG at max quality.
- Do not skew/stretch.

## Headline Block
- Prefer left alignment.
- Use sentence-case, with bold token emphasis.
- Keep line breaks semantically intentional.

## CTA Button
- Pill shape, high contrast fill (yellow preferred).
- Text center aligned; no all caps unless campaign-specific.
- Add subtle shadow only.

## Icon/Badge Decorations
- Use sparingly.
- Keep to support narrative (integration logos, status hints, feature hints).

## Format Safe-Zone Cheatsheet
- `1080x1080`: reserve top-left logo and lower-left CTA lanes.
- `1080x1350`: protect lower CTA lane from feed crop overlays.
- `1080x1920`: avoid top notch and bottom UI zones; keep CTA off the bottommost band.
- `1200x628`: preserve left copy panel integrity for preview cuts.

## Export Settings
- File type: PNG for static master exports.
- Quality: max before platform compression.
- Keep source files editable in Canva with naming convention:
  - `{campaign}_{concept}_{format}_{version}`
  - Example: `pms_spreadsheetpain_1080x1350_v03`

## Naming Convention (Required)
- `campaign`: `pms` / `guidebook` / `calendar` / `case_study` / `automation`
- `concept`: short token (`pain`, `proof`, `support`, `2x`, `checkin`)
- `format`: `1080x1080`, `1080x1350`, `1080x1920`, `1200x628`
- `version`: `v01`, `v02`, etc.

## QA Gate Before Publish
- Headline readable at 25% zoom.
- CTA remains visible and not clipped in preview.
- Logo contrast is sufficient against local background.
- No element collisions.
- Claim and visual are semantically aligned.
- Export dimensions match target placement exactly.

## Fast Iteration Protocol
- Duplicate from nearest-performing creative.
- Change one major variable per variant batch:
  - hook
  - crop
  - accent color
  - CTA wording
- Keep structural anchors unchanged for test clarity.

