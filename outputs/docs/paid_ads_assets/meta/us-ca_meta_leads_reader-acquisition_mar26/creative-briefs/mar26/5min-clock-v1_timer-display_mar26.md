# Visual Creative Brief

## 1. Brief Header

| Field | Value |
|-------|-------|
| **Brief ID** | meta-reader-acq-5min-clock-v1 |
| **Version** | v1 |
| **Date Created** | 2026-03-09 |
| **Status** | Draft |
| **Platform** | Meta (Facebook / Instagram) |
| **Ad Type** | Single Image |
| **Campaign** | us-ca_meta_leads_reader-acquisition_mar26 |
| **Ad Group** | lal_subscribers-1pct_us-ca / lal_subscribers-3pct_us-ca |
| **Ad Name** | single-img_5min-clock-v1 |
| **Placements** | Advantage+ (Feed, Stories, Reels, Right Column, Audience Network) |
| **Network Side** | Reader acquisition |
| **Target Persona** | R3: The Ambitious Builder |
| **Messaging Pillar** | Pillar 3: Professional Credibility (anchored by Pillar 1: Time Reclaimed) |
| **Ad Creative** | [us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md](../../us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md) |
| **Campaign Structure** | [us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md](../../us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md) |
| **Campaign Index** | [_index.md](../../_index.md) |

---

## 2. Concept Overview

**Concept Name:** The 5-Minute Clock

**Description:** A bold, oversized "5:00" in TLDR Blue (#2563EB) centered on a white background, styled like a timer display. Below: "That's all it takes to know everything in tech." TLDR logo bottom-center. Clean, graphic, impossible to scroll past.

**Visual Hook:** The massive "5:00" number — timer-styled typography that immediately communicates the time commitment before the brain processes the supporting text.

**On-Image Copy:**
- **Headline:** "5:00" (oversized, timer-styled)
- **Subhead/Body:** "All it takes to know everything in tech"
- **Stat/Number:** 5:00 (the entire concept revolves around this number)
- **CTA:** "Free — join 1.6M readers" (bottom-center)

**Emotional Tone:** Confident efficiency

---

## 3. Sizing Variants

| Priority | Size Name | Dimensions | Aspect Ratio | File Type | Max Size | Placement |
|----------|-----------|------------|--------------|-----------|----------|-----------|
| Hero | Feed Portrait | 1080 x 1350px | 4:5 | PNG | 30MB | Feed (mobile-optimized) |
| Adapt | Stories/Reels | 1080 x 1920px | 9:16 | PNG | 30MB | Stories, Reels |
| Adapt | Feed Square | 1080 x 1080px | 1:1 | PNG | 30MB | Feed fallback, Marketplace |
| Optional | Right Column | 1200 x 628px | 1.91:1 | PNG | 30MB | Right column (desktop only) |

**Export checklist:**
- [ ] All sizes exported at 2x resolution for retina displays
- [ ] File names follow convention: `meta-reader-acq-5min-clock-v1_{size-name}.png`
- [ ] File sizes within 30MB per placement

---

## 4. Safe Zones & Layout Grid

### Safe Zone Measurements (all sizes)

| Size | Dimensions | Safe Content Zone | Top Margin | Bottom Margin | Left/Right | Overlay Elements |
|------|------------|-------------------|------------|---------------|------------|------------------|
| 4:5 (Hero) | 1080 x 1350px | 1080 x 950px (center 70%) | 250px | 150px | 0px (full bleed) | Profile picture + page name (top-left), 3-dot menu (top-right) |
| 9:16 (Stories/Reels) | 1080 x 1920px | 880 x 1280px (center) | 320px | 320px | 100px | Profile/username (top), CTA button + reply bar (bottom), engagement icons (right edge on Reels) |
| 1:1 (Feed Square) | 1080 x 1080px | 864 x 864px (center 80%) | 108px (10%) | 108px (10%) | 108px (10%) | Minimal — headline/CTA render below image in feed |
| 1.91:1 (Right Column) | 1200 x 628px | 1080 x 508px (center 81%) | 60px | 60px | 60px | Renders small on desktop — keep text 40px+ minimum |

### Safe Zone Diagrams

**Feed Portrait — 4:5 (1080 x 1350px) — HERO:**

```
┌─────────────────────────────────┐
│  ▓ TOP 250px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Profile pic, page name
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│                                 │
│  ┌───────────────────────────┐  │
│  │         "5:00"            │  │  ← Oversized timer at ~40%
│  │      (center, 180px)      │  │    from top of safe zone
│  │                           │  │
│  │  "All it takes to know    │  │
│  │   everything in tech"     │  │  ← Subhead centered below
│  │                           │  │
│  │    [Free — join 1.6M]     │  │  ← CTA pill button
│  │                           │  │
│  │        TLDR logo          │  │  ← Bottom-center of safe zone
│  └───────────────────────────┘  │
│                                 │
│  ▓ BOTTOM 150px ▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Crop zone
└─────────────────────────────────┘
```

**Stories / Reels — 9:16 (1080 x 1920px):**

```
┌─────────────────────────────────┐
│  ▓ TOP 320px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Profile, "Sponsored",
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │    progress bars
│                                 │
│  ┌───────────────────────┐     │
│  │        "5:00"         │     │  ← Scale timer to 220px
│  │     (center, 220px)   │  ♡  │    for full-screen impact
│  │                       │  💬 │
│  │  "All it takes to     │  ↗  │  ← 100px right margin
│  │   know everything     │     │    for engagement icons
│  │   in tech"            │     │
│  │                       │     │
│  │  [Free — join 1.6M]   │     │
│  │                       │     │
│  │     TLDR logo         │     │
│  └───────────────────────┘     │
│                                 │
│  ▓ BOTTOM 320px ▓▓▓▓▓▓▓▓▓▓▓▓  │  ← CTA button, reply bar
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
└─────────────────────────────────┘
```

**Feed Square — 1:1 (1080 x 1080px):**

```
┌─────────────────────────────────┐
│  ▓ TOP 108px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│ ▓                             ▓ │
│ ▓ ┌───────────────────────┐  ▓ │
│ ▓ │       "5:00"          │  ▓ │  ← Scale timer to 140px
│ ▓ │    (center, 140px)    │  ▓ │    for tighter canvas
│ ▓ │                       │  ▓ │
│ ▓ │  "All it takes..."   │  ▓ │
│ ▓ │  [Free — join 1.6M]  │  ▓ │  ← Tighten spacing
│ ▓ │       TLDR logo       │  ▓ │
│ ▓ └───────────────────────┘  ▓ │
│ ▓                             ▓ │
│  ▓ BOTTOM 108px ▓▓▓▓▓▓▓▓▓▓▓▓  │
└─────────────────────────────────┘
```

**Right Column — 1.91:1 (1200 x 628px):**

```
┌─────────────────────────────────────────┐
│ ▓60px ┌───────────────────────┐  60px ▓ │
│ ▓     │                       │       ▓ │
│ ▓     │  "5:00"  TLDR         │       ▓ │  ← Timer 80px + logo
│ ▓     │  (left-center, 80px)  │       ▓ │    side by side. Remove
│ ▓     │                       │       ▓ │    subhead and CTA
│ ▓     └───────────────────────┘       ▓ │
│ ▓60px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  60px ▓ │
└─────────────────────────────────────────┘
```

### Recommended Layout (per size)

**4:5 (Hero):**
- **"5:00" timer:** Dead center horizontally, positioned at ~40% from top of canvas (within safe zone)
- **Subhead:** Center-aligned, 32px below timer
- **CTA pill:** Center-aligned, 48px below subhead
- **Logo:** Bottom-center of safe zone, 48px from bottom edge
- **Background:** Pure white (#FFFFFF) — zero visual competition

**9:16 (Stories/Reels):**
- Scale timer to 220px for full-screen drama
- Scale subhead to 36px, add 64px spacing between elements
- Move logo to bottom-center (away from right-edge icons)
- All content within 880x1280 safe zone

**1:1 (Feed Square):**
- Scale timer to 140px — still dominant but fits 864x864 safe zone
- Tighten spacing to 24px between elements
- Logo bottom-center at smaller size (80x22px)
- May abbreviate CTA to "Join free" for space

**1.91:1 (Right Column):**
- Simplify to just "5:00" at 80px + TLDR logo, side by side
- Remove subhead and CTA — canvas too small
- Let the bold timer + white background do the work

### Designer Notes

- **DO:** Verify "5:00" is fully inside the safe zone and visually dominant at every size
- **DO:** Maintain pure white background across all variants — contrast between emptiness and bold blue number is the entire concept
- **DO:** Scale timer proportionally: 180px (4:5) → 220px (9:16) → 140px (1:1) → 80px (1.91:1)
- **DO:** Test the 1:1 on both iOS and Android — safe zone cropping varies slightly
- **DON'T:** Place "5:00" in the top 250px on 4:5 or top 320px on 9:16 — must be below profile overlay
- **DON'T:** Add visual complexity to 1.91:1 — only timer + logo at right-column size
- **DON'T:** Use text-heavy CTA on 9:16 — bottom 320px consumed by platform CTA overlay
- **NOTE:** Meta may auto-crop 4:5 to 1:1 — verify center 1080x1080 still shows "5:00" prominently
- **NOTE:** Consider JetBrains Mono or SF Mono for the colon in "5:00" for true timer/monospace feel
- **NOTE:** Pure typographic concept — no Nano Banana base needed. Build in Figma/Canva for maximum crispness

---

## 5. Visual Design Specs

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | White | #FFFFFF | Full canvas background |
| Primary Text / Stat | TLDR Blue | #2563EB | "5:00" oversized number |
| Supporting Text | TLDR Black | #0F172A | Subhead text |
| CTA Background | TLDR Blue | #2563EB | Pill button |
| CTA Text | White | #FFFFFF | Button text |
| Accent (optional) | Signal Green | #10B981 | Subtle dot or colon separator in "5:00" |

### Typography

| Element | Font | Weight | Size | Color | Notes |
|---------|------|--------|------|-------|-------|
| Stat/Timer | Inter | 800 (ExtraBold) | 180px | #2563EB | Center-aligned, monospaced feel. Scale to 140px for 1:1, 220px for 9:16 |
| Subhead | Inter | 500 (Medium) | 28px | #0F172A | Center-aligned, 32px below stat. Max 1 line |
| CTA text | Inter | 600 (SemiBold) | 20px | #FFFFFF | Inside pill button |
| Social proof | Inter | 400 (Regular) | 16px | #94A3B8 | Optional small text above CTA: "1.6M readers" |

### Logo

- **File:** TLDR wordmark, TLDR Blue (#2563EB) on transparent
- **Placement:** Bottom-center of safe zone
- **Minimum size:** 100 x 28px
- **Clear space:** 24px margin

### Background Treatment

- **Type:** Solid color
- **Colors:** #FFFFFF (pure white)
- **Image treatment:** No Nano Banana base needed — pure typographic concept

---

## 6. Nano Banana Prompt

This is a purely typographic/graphic concept. No AI-generated base image is required. Build directly in Figma/Canva.

**Alternative — if you want a subtle textured background:**

**Prompt:**
```
Minimalist pure white background with very subtle soft radial gradient, slightly warmer in the center fading to cool white at edges. Clean, modern, advertising-quality. The texture should feel like premium paper or a softbox-lit white surface. No objects, no shadows, no elements — just a pristine white canvas with barely perceptible depth.
```

**Negative prompt:**
```
text, words, letters, numbers, logos, objects, shadows, patterns, colors, busy, cluttered, dark, low quality, blurry
```

**Settings:**
- **Aspect ratio:** 4:5
- **Style:** Photographic / minimal

**Post-generation notes:**
- This background is optional — a solid #FFFFFF works perfectly
- If using Nano Banana, the result should be indistinguishable from white at first glance
- All visual impact comes from the typography overlay

---

## 7. Figma / Canva Overlay Instructions

### Layer Stack (bottom to top)

1. **Background** — Solid #FFFFFF fill (or subtle Nano Banana white texture)
2. **Timer number** — "5:00" | Inter ExtraBold 180px | #2563EB | Dead center of canvas, vertically at ~40% from top
3. **Subhead text** — "All it takes to know everything in tech" | Inter Medium 28px | #0F172A | Center-aligned, 32px below timer
4. **Social proof** (optional) — "1.6M readers" | Inter Regular 16px | #94A3B8 | Center-aligned, 24px below subhead
5. **CTA element** — "Free — join 1.6M readers" | Pill, corner radius 24px | #2563EB background | #FFFFFF Inter SemiBold 20px | Center-aligned, 48px below subhead
6. **Logo** — TLDR wordmark (blue) | 100px wide | Bottom-center, 48px above bottom safe margin

### Figma-Specific Notes
- Use a vertical Auto Layout frame for the text stack (timer → subhead → CTA → logo)
- Center the frame both horizontally and vertically
- Create components: `5min-clock_4x5`, `5min-clock_1x1`, `5min-clock_9x16`, `5min-clock_1.91x1`
- Consider JetBrains Mono or SF Mono for the colon

### Canva-Specific Notes
- Use "Custom Size" for each variant
- "5:00" is the hero — make it as large as possible within safe zone
- Use Canva's "Resize" to adapt layouts
- Export as PNG at 2x

---

## 8. Iteration Notes

Initial brief — no prior versions.
