# Visual Creative Brief

## 1. Brief Header

| Field | Value |
|-------|-------|
| **Brief ID** | meta-reader-acq-peer-signal-v1 |
| **Version** | v1 |
| **Date Created** | 2026-03-09 |
| **Status** | Draft |
| **Platform** | Meta (Facebook / Instagram) |
| **Ad Type** | Single Image |
| **Campaign** | us-ca_meta_leads_reader-acquisition_mar26 |
| **Ad Group** | lal_subscribers-1pct_us-ca / interest_tech-professionals_us-ca |
| **Ad Name** | single-img_peer-signal-v1 |
| **Placements** | Advantage+ (Feed, Stories, Reels, Right Column, Audience Network) |
| **Network Side** | Reader acquisition |
| **Target Persona** | R3: The Ambitious Builder |
| **Messaging Pillar** | Pillar 3: Professional Credibility |
| **Ad Creative** | [us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md](../../us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md) |
| **Campaign Structure** | [us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md](../../us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md) |
| **Campaign Index** | [_index.md](../../_index.md) |

---

## 2. Concept Overview

**Concept Name:** The Peer Signal

**Description:** A clean, dark blue (#0F172A) background with oversized white text: "1,600,000+ tech professionals start here." Below, a subtle grid of tiny, anonymous avatar circles suggesting a massive community. TLDR logo in bottom-right. Minimalist, authoritative.

**Visual Hook:** The oversized "1,600,000+" number — it's the first element the eye lands on, creating immediate social proof scale.

**On-Image Copy:**
- **Headline:** "1,600,000+ tech professionals start here"
- **Subhead/Body:** None — single-statement impact
- **Stat/Number:** 1,600,000+
- **CTA:** "Join for free" (on-image, small pill button)

**Emotional Tone:** Peer belonging, FOMO

---

## 3. Sizing Variants

Design the **Hero** size first, then adapt to all other sizes.

| Priority | Size Name | Dimensions | Aspect Ratio | File Type | Max Size | Placement |
|----------|-----------|------------|--------------|-----------|----------|-----------|
| Hero | Feed Portrait | 1080 x 1350px | 4:5 | PNG | 30MB | Feed (mobile-optimized) |
| Adapt | Stories/Reels | 1080 x 1920px | 9:16 | PNG | 30MB | Stories, Reels |
| Adapt | Feed Square | 1080 x 1080px | 1:1 | PNG | 30MB | Feed fallback, Marketplace |
| Optional | Right Column | 1200 x 628px | 1.91:1 | PNG | 30MB | Right column (desktop only) |

**Export checklist:**
- [ ] All sizes exported at 2x resolution for retina displays
- [ ] File names follow convention: `meta-reader-acq-peer-signal-v1_{size-name}.png`
- [ ] File sizes within 30MB per placement

---

## 4. Safe Zones & Layout Grid

### Safe Zone Measurements (all sizes)

| Size | Dimensions | Safe Content Zone | Top Margin | Bottom Margin | Left/Right | Overlay Elements |
|------|------------|-------------------|------------|---------------|------------|------------------|
| 4:5 (Hero) | 1080 x 1350px | 1080 x 950px (center 70%) | 250px | 150px | 0px (full bleed) | Profile picture + page name (top-left), 3-dot menu (top-right) |
| 9:16 (Stories/Reels) | 1080 x 1920px | 880 x 1280px (center) | 320px | 320px | 100px | Profile/username (top), CTA button + reply bar (bottom), engagement icons (right edge on Reels) |
| 1:1 (Feed Square) | 1080 x 1080px | 864 x 864px (center 80%) | 108px (10%) | 108px (10%) | 108px (10%) | Minimal — headline/CTA render below image in feed |
| 1.91:1 (Right Column) | 1200 x 628px | 1080 x 508px (center 81%) | 60px | 60px | 60px | Renders small on desktop — keep text 40px+ minimum. No platform overlay but size limits readability |

### Safe Zone Diagrams

**Feed Portrait — 4:5 (1080 x 1350px) — HERO:**

```
┌─────────────────────────────────┐
│  ▓ TOP 250px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Profile pic, page name,
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │    "Sponsored" label
│                                 │
│  ┌───────────────────────────┐  │
│  │                           │  │
│  │     SAFE CONTENT ZONE     │  │  ← "1,600,000+" stat,
│  │     1080 x 950px          │  │    headline, CTA, logo
│  │                           │  │    ALL within this zone
│  └───────────────────────────┘  │
│                                 │
│  ▓ BOTTOM 150px ▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Crop zone on some placements
└─────────────────────────────────┘
```

**Stories / Reels — 9:16 (1080 x 1920px):**

```
┌─────────────────────────────────┐
│  ▓ TOP 320px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Profile pic, username,
│  ▓ (Stories: progress bars at  ▓│    "Sponsored", close button
│  ▓  very top of screen)       ▓│
│                                 │
│  ┌───────────────────────┐     │
│  │                       │  ♡  │  ← Right edge: like, share,
│  │   SAFE CONTENT ZONE   │  💬 │    reply icons (Reels)
│  │   880 x 1280px        │  ↗  │    Keep 100px right margin
│  │                       │     │
│  └───────────────────────┘     │
│                                 │
│  ▓ BOTTOM 320px ▓▓▓▓▓▓▓▓▓▓▓▓  │  ← CTA button, reply bar,
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │    swipe-up zone
└─────────────────────────────────┘
```

**Feed Square — 1:1 (1080 x 1080px):**

```
┌─────────────────────────────────┐
│  ▓ TOP 108px (10%) ▓▓▓▓▓▓▓▓▓  │  ← May be cropped on
│ ▓                             ▓ │    some placements
│ ▓ ┌───────────────────────┐  ▓ │
│ ▓ │                       │  ▓ │
│ ▓ │   SAFE CONTENT ZONE   │  ▓ │  ← 108px margins
│ ▓ │   864 x 864px         │  ▓ │    on all sides
│ ▓ │                       │  ▓ │
│ ▓ └───────────────────────┘  ▓ │
│ ▓                             ▓ │
│  ▓ BOTTOM 108px (10%) ▓▓▓▓▓▓  │
└─────────────────────────────────┘
```

**Right Column — 1.91:1 (1200 x 628px):**

```
┌─────────────────────────────────────────┐
│ ▓60px ┌───────────────────────┐  60px ▓ │
│ ▓     │                       │       ▓ │
│ ▓     │   SAFE CONTENT ZONE   │       ▓ │  ← Renders small on desktop
│ ▓     │   1080 x 508px        │       ▓ │    Use 40px+ text minimum
│ ▓     │                       │       ▓ │    Keep composition SIMPLE
│ ▓     └───────────────────────┘       ▓ │
│ ▓60px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  60px ▓ │
└─────────────────────────────────────────┘
```

### Recommended Layout (per size)

**4:5 (Hero):**
- **Logo zone:** Bottom-right corner, 48px from edges of safe zone
- **"1,600,000+" stat:** Center, upper-middle third of safe zone — dominates the visual
- **Headline ("tech professionals start here"):** Center, 24px below stat
- **CTA ("Join for free"):** Center, 64px below headline
- **Background focus:** Even dark field — no focal point competing with the number

**9:16 (Stories/Reels):**
- Scale stat to 120px, headline to 42px — full-screen viewing
- Shift entire content stack into the center 880x1280 safe zone
- Move logo from bottom-right to bottom-center (away from right-edge engagement icons)
- Add more vertical spacing between elements

**1:1 (Feed Square):**
- Reduce stat to 72px — tighter canvas
- Tighten spacing between stat → headline → CTA
- Logo stays bottom-right, 48px from edges of 864x864 safe zone
- Remove or simplify the avatar grid to avoid clutter at smaller size

**1.91:1 (Right Column):**
- Simplify dramatically — stat "1.6M+" at 48px + "Free tech newsletter" at 28px only
- Logo bottom-right at 80x22px
- No CTA button, no avatar grid — too small to render. Let platform CTA handle conversion

### Designer Notes

- **DO:** Verify the "1,600,000+" number is fully inside the safe zone for every size — it's the single most important element
- **DO:** Design the hero (4:5) first, then adapt each size and verify content stays within its specific safe zone
- **DO:** Simplify aggressively for 1.91:1 — this renders ~300px wide on desktop. Only the stat and logo should remain
- **DO:** Use minimum 24px font on 4:5/1:1, minimum 28px on 9:16, minimum 40px on 1.91:1
- **DON'T:** Place text or logos in the top 250px on 4:5 or top 320px on 9:16 — profile overlay covers this area
- **DON'T:** Place the logo or CTA in the right 100px on 9:16 — Reels engagement icons (♡ 💬 ↗) stack here
- **DON'T:** Copy the 4:5 layout directly to 1:1 — the tighter safe zone (864x864) requires tighter spacing
- **NOTE:** Meta may auto-crop 4:5 to 1:1 on some placements. Verify the center 1080x1080 of your 4:5 works as a standalone composition
- **NOTE:** The avatar grid element should fade or be removed on smaller sizes (1:1, 1.91:1) where it becomes visual noise

---

## 5. Visual Design Specs

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary / Background | TLDR Black | #0F172A | Full background fill |
| Text / Headline | White | #FFFFFF | "1,600,000+" and headline text |
| Accent | Signal Green | #10B981 | Subtle glow or underline on "1,600,000+" |
| CTA Background | TLDR Blue | #2563EB | "Join for free" pill button background |
| CTA Text | White | #FFFFFF | "Join for free" button text |
| Avatar Grid | Soft Gray | #334155 | Tiny avatar circles (subtle, not distracting) |

### Typography

| Element | Font | Weight | Size | Color | Notes |
|---------|------|--------|------|-------|-------|
| Stat number | Inter | 800 (ExtraBold) | 96px | #FFFFFF | Center-aligned, 1 line. Scale down to 72px for 1:1, up to 120px for 9:16 |
| Headline text | Inter | 600 (SemiBold) | 36px | #FFFFFF | Center-aligned, below the stat. "tech professionals start here" |
| CTA text | Inter | 600 (SemiBold) | 20px | #FFFFFF | Inside pill button, center-aligned |

### Logo

- **File:** TLDR wordmark, white on transparent
- **Placement:** Bottom-right corner of safe zone
- **Minimum size:** 120 x 32px
- **Clear space:** 24px minimum margin around logo on all sides

### Background Treatment

- **Type:** Solid color with subtle texture
- **Colors:** #0F172A (TLDR Black) as primary fill
- **Texture:** Very subtle noise grain (2-3% opacity) to avoid flat digital feel
- **Image treatment:** No Nano Banana base image needed — this is a graphic/type-driven concept

---

## 6. Nano Banana Prompt

This concept is primarily typographic/graphic — the base image is a textured dark background with a crowd element.

**Prompt:**
```
Abstract dark navy blue background with a subtle grid pattern of hundreds of tiny circular avatars fading into the distance, suggesting a massive professional community. The circles are soft gray (#334155) on a deep navy (#0F172A) background, arranged in a gentle curved grid that recedes toward the center-bottom, creating depth. The top 60% of the image is clear dark space for text overlay. Minimal, corporate, clean. No text, no logos. Photographic quality lighting with soft ambient glow from center.
```

**Negative prompt:**
```
text, words, letters, numbers, watermarks, logos, faces, identifiable people, bright colors, gradients, cluttered, busy, cartoonish, clip art, stock photo feel, low quality, blurry, distorted
```

**Settings:**
- **Aspect ratio:** 4:5 (matching hero size)
- **Style:** 3D render / digital abstract

**Post-generation notes:**
- The base image should NOT contain any text — all text is added in Figma/Canva
- Generate 3-4 variations and select the one with the cleanest open space in the upper 60% for headline placement
- If avatars are too prominent or distracting, reduce their visibility — they should be atmospheric, not the focus

---

## 7. Figma / Canva Overlay Instructions

Everything below is layered ON TOP of the Nano Banana base image.

### Layer Stack (bottom to top)

1. **Base image** (from Nano Banana — dark background with avatar grid)
2. **Overlay/tint** — 20% #0F172A overlay if base image is too bright in the text area
3. **Stat number** — "1,600,000+" | Inter ExtraBold 96px | #FFFFFF | Center horizontally, positioned at 35% from top of canvas
4. **Headline text** — "tech professionals start here" | Inter SemiBold 36px | #FFFFFF | Center horizontally, 24px below stat number
5. **CTA element** — "Join for free" | Pill shape, corner radius 24px | Background #2563EB | Text #FFFFFF Inter SemiBold 20px | Center horizontally, 64px below headline
6. **Logo** — TLDR wordmark (white) | 120px wide | Bottom-right corner, 48px from edges of safe zone
7. **Accent line** (optional) — 2px line, #10B981, 200px wide, centered below "1,600,000+" to separate stat from headline

### Figma-Specific Notes
- Use Auto Layout for the stat + headline + CTA stack so spacing adjusts cleanly across sizes
- Create a component for each size variant: `peer-signal_4x5`, `peer-signal_1x1`, `peer-signal_9x16`, `peer-signal_1.91x1`
- Name layers: `stat_4x5`, `headline_4x5`, `cta_4x5`, `logo_4x5`
- For 9:16 Stories adaptation: scale stat to 120px, headline to 42px, add more vertical spacing

### Canva-Specific Notes
- Use "Custom Size" for each variant: 1080x1350, 1080x1080, 1080x1920, 1200x628
- Apply brand kit: Inter font, TLDR Blue (#2563EB), TLDR Black (#0F172A)
- Group stat + headline + CTA as a single element for easy repositioning across sizes
- Export as PNG (static) at 2x resolution

---

## 8. Iteration Notes

Initial brief — no prior versions.
