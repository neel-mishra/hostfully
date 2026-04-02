# Format Systems and Safe-Zone Thesis

## Scope
- Source set: `126` attached paid-ad creatives copied into `00_source_images`.
- Clustered formats:
  - `square_feed` (`1080x1080`) - 23 files
  - `portrait_feed` (`1080x1350`) - 20 files
  - `vertical_story_reel` (`1080x1920`) - 17 files
  - `landscape_feed` (`1200x628`) - 22 files
  - `general_pms_portrait` - 29 files
  - `general_pms_square` - 12 files
  - `general_pms_landscape` - 3 files

## Master Layout Principle
Hostfully's paid ads use a two-anchor architecture:
1. **Trust anchor** in the top-left (`Hostfully` wordmark + mark).
2. **Conversion anchor** in the lower-left or lower-third (high-contrast rounded CTA).

The visual storytelling region sits between these anchors and carries product UI, scenario image, proof claim, or mascot.

## Safe-Zone Rules by Format

### 1) `1080x1080` (Square Feed)
- **Primary text zone:** `x: 7-10%`, `y: 18-52%`, width up to `48-54%`.
- **Logo zone:** `x: 6-10%`, `y: 6-12%`.
- **CTA zone:** `x: 10-16%`, `y: 70-84%`.
- **Hero media zone:** right-half dominant (`x: 45-95%`, `y: 20-92%`) or center-weighted for UI mockups.
- **Design intent:** balance readability with feed-stop impact in mixed social placements.

### 2) `1080x1350` (Portrait Feed)
- **Primary text zone:** `x: 7-10%`, `y: 14-45%`, width `42-50%`.
- **Logo zone:** slightly inset (`x: 7-10%`, `y: 6-11%`).
- **CTA zone:** usually above bottom edge by `9-14%`.
- **Hero media zone:** mid-to-lower right with controlled overflow.
- **Design intent:** maximize narrative copy while preserving product visual credibility.

### 3) `1080x1920` (Stories/Reels)
- **Primary text zone:** top half concentration (`y: 14-43%`).
- **No critical text** in very top notch region or lowest `14%`.
- **CTA zone:** lower-middle, not flush bottom, to avoid UI collisions.
- **Hero media zone:** center-to-lower frame with heavier negative space at top-left.
- **Design intent:** immediate hook legibility within first second of story consumption.

### 4) `1200x628` (Landscape Feed/Link Ads)
- **Split composition:** common `45/55` or `50/50` left copy / right product-image pattern.
- **Logo + headline stack** in left panel for fast horizontal scan.
- **CTA placement:** lower-left quadrant with high contrast from background field.
- **Hero media:** right-half UI screenshot or contextual scene.
- **Design intent:** desktop and feed preview optimization with clear value prop read.

### 5) `general_PMS` Variants (Mixed Aspect Portfolio)
- Predominantly pain-point ads (`spreadsheet friction`) and mascot-led emotional concepts.
- **Top-left identity lock** preserved consistently across variants.
- **Large copy card** or **headline stack** occupies left/top-left.
- CTA remains a strong pill with yellow base; alternate label colors used for hierarchy tests.
- **Design intent:** campaign-level rapid varianting without changing core brand signature.

## Composition Grammar

## A. Scan Path (Z/F Hybrid)
- Eye entry: top-left logo.
- First cognitive stop: bold keyword in headline (`double`, `2x`, `scaled 350x`, etc.).
- Second stop: product proof visual (calendar/grid/guidebook/planner/real-life scene).
- Final stop: CTA with action framing (`Let us help`, `Read the Story`, `View the Blueprint`).

## B. Hierarchy Weighting
- Strongest weight is always on one of:
  - a numeric proof token (`2x`, `350x`, `718`)
  - a high-emotion claim (`support system you deserve`)
  - a pain question (`stuck in spreadsheets?`)
- Supporting UI or imagery never outranks the headline+CTA pair.

## C. Layer Stack Pattern
1. Background gradient or context photo.
2. Product UI / hero object (calendar, cards, mascot, person at desk).
3. Optional floating badges/icons/cards for dimensionality.
4. Headline text block.
5. CTA button with subtle shadow.
6. Logo lockup.

## Format-Specific Conversion Implications
- **Square (`1:1`)**: best for balanced information density and broad distribution.
- **Portrait (`4:5`)**: best for narrative framing + mobile scroll dominance.
- **Story (`9:16`)**: best for interruptive hooks and bold compact messaging.
- **Landscape (`1.91:1`)**: best for split-layout clarity and click-oriented campaigns.

## Non-Negotiable Layout Constraints
- Keep logo clearspace at least `0.75x` logo height around all sides.
- Never let CTA touch frame edges; keep at least `6%` margin in all directions.
- Preserve at least one high-contrast text block against a simplified local background.
- Avoid placing small, thin text over high-frequency imagery without overlay or blur.

## Recommended Future Layout Tokens
- `token.logo.topLeftInset = 8%`
- `token.copy.maxWidth.square = 52%`
- `token.copy.maxWidth.portrait = 50%`
- `token.copy.maxWidth.story = 54%`
- `token.cta.minHeight = 10% of short edge`
- `token.cta.cornerRadius = 9999` (pill)
- `token.copyToCta.verticalGap = 4-8%`

