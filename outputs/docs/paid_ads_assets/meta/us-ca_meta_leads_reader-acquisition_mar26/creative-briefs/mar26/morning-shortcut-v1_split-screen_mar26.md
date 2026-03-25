# Visual Creative Brief

## 1. Brief Header

| Field | Value |
|-------|-------|
| **Brief ID** | meta-reader-acq-morning-shortcut-v1 |
| **Version** | v1 |
| **Date Created** | 2026-03-09 |
| **Status** | Draft |
| **Platform** | Meta (Facebook / Instagram) |
| **Ad Type** | Single Image |
| **Campaign** | us-ca_meta_leads_reader-acquisition_mar26 |
| **Ad Group** | lal_subscribers-3pct_us-ca / interest_tech-professionals_us-ca |
| **Ad Name** | single-img_morning-shortcut-v1 |
| **Placements** | Advantage+ (Feed, Stories, Reels, Right Column, Audience Network) |
| **Network Side** | Reader acquisition |
| **Target Persona** | R3: The Ambitious Builder |
| **Messaging Pillar** | Pillar 3: Professional Credibility (with Pillar 1: Time Reclaimed undertone) |
| **Ad Creative** | [us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md](../../us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md) |
| **Campaign Structure** | [us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md](../../us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md) |
| **Campaign Index** | [_index.md](../../_index.md) |

---

## 2. Concept Overview

**Concept Name:** The Morning Shortcut

**Description:** Split composition — left side shows a cluttered, overwhelming social feed (blurred/chaotic colors, news overload). Right side shows a clean, calm phone screen with the TLDR email open — clear, organized, brief. A dividing line with "5 min" in bold. Background: soft gray (#F1F5F9) on the TLDR side, noisy warm tones on the chaos side.

**Visual Hook:** The stark visual contrast between chaos (left) and calm (right) — the eye immediately notices the split and reads the divider text.

**On-Image Copy:**
- **Headline:** "This vs. This. 5 minutes."
- **Subhead/Body:** "Tech news without the noise"
- **Stat/Number:** "5 min" (centered on dividing line)
- **CTA:** "Subscribe free" (bottom-center, TLDR side)

**Emotional Tone:** Calm efficiency, relief

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
- [ ] File names follow convention: `meta-reader-acq-morning-shortcut-v1_{size-name}.png`
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
│  ▓ TOP 250px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Profile pic, page name,
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │    "Sponsored" label
│                                 │
│  ┌──────────┬──────────────┐   │
│  │          │              │   │
│  │  CHAOS   │  TLDR CLEAN  │   │  ← Split at center (540px
│  │  (LEFT)  │   (RIGHT)    │   │    per side). Divider + "5 min"
│  │  540px   │   540px      │   │    badge at center seam
│  │          │              │   │
│  └──────────┴──────────────┘   │
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
│  ┌─────────┬─────────┐    │
│  │         │         │ ♡  │  ← Split adapts to vertical:
│  │ CHAOS   │ TLDR    │ 💬 │    each side 390px wide (880px
│  │ (LEFT)  │ (RIGHT) │ ↗  │    safe width minus 100px
│  │ 390px   │ 390px   │    │    right margin)
│  │         │         │    │
│  └─────────┴─────────┘    │
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
│ ▓ ┌───────────┬───────────┐  ▓ │
│ ▓ │           │           │  ▓ │  ← Split at center of
│ ▓ │  CHAOS    │   TLDR    │  ▓ │    safe zone (432px/side)
│ ▓ │  (LEFT)   │  (RIGHT)  │  ▓ │    108px margins all sides
│ ▓ │           │           │  ▓ │
│ ▓ └───────────┴───────────┘  ▓ │
│ ▓                             ▓ │
│  ▓ BOTTOM 108px ▓▓▓▓▓▓▓▓▓▓▓▓  │  Alternative: stack vertically
└─────────────────────────────────┘  (chaos top, TLDR bottom)
```

**Right Column — 1.91:1 (1200 x 628px):**

```
┌─────────────────────────────────────────┐
│ ▓60px ┌──────────┬──────────┐    60px ▓ │
│ ▓     │  CHAOS   │  TLDR    │         ▓ │  ← Split works well at
│ ▓     │  (LEFT)  │  (RIGHT) │         ▓ │    this wide ratio.
│ ▓     │          │          │         ▓ │    Simplify text to
│ ▓     └──────────┴──────────┘         ▓ │    "5 min" badge only
│ ▓60px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  60px ▓ │
└─────────────────────────────────────────┘
```

### Recommended Layout (per size)

**4:5 (Hero):**
- **Headline ("This vs. This. 5 minutes."):** Full-width, top of safe zone, centered at 280px from top
- **Divider line:** 4px vertical, TLDR Blue (#2563EB), center of canvas, full height of safe zone
- **"5 min" badge:** Circle (80px), centered on divider at vertical center of safe zone
- **Subhead:** Right half, center-aligned, 64px below badge
- **CTA ("Subscribe free"):** Right half, bottom of safe zone
- **Logo:** Bottom-right of TLDR (right) side, 40px from edges

**9:16 (Stories/Reels):**
- Scale headline to 48px for full-screen
- Each side 390px wide within 880px safe width
- Move "5 min" badge higher to avoid bottom 320px CTA zone
- Logo bottom-center (not bottom-right — avoid Reels icons)

**1:1 (Feed Square):**
- Side-by-side split at 432px/side, or top/bottom stack (chaos top, TLDR bottom with horizontal divider)
- Reduce headline to 32px, badge to 60px
- Tighten all spacing — 864x864 is compact

**1.91:1 (Right Column):**
- Split works naturally at this wide ratio — landscape suits side-by-side
- Simplify text to just the "5 min" badge + "TLDR" logo
- Remove subhead, CTA, and detail text — too small

### Designer Notes

- **DO:** Verify the divider line + "5 min" badge stays centered in the safe zone on every size variant
- **DO:** Check that the split-screen concept reads clearly at every size — chaos vs. calm contrast must be instant
- **DO:** Adapt the 1:1 carefully — consider top/bottom vertical stack instead of left/right if too cramped
- **DO:** Use minimum 24px font on 4:5, 28px on 9:16, 32px on 1:1, 40px on 1.91:1
- **DON'T:** Place the headline in the top 250px on 4:5 or top 320px on 9:16 — profile overlay
- **DON'T:** Let chaos side bleed into right 100px on 9:16 — Reels engagement icons render there
- **DON'T:** Crowd the 1.91:1 — only the core concept (split + "5 min") should remain
- **NOTE:** Meta may auto-crop 4:5 to 1:1 — verify center 1080x1080 preserves the split concept
- **NOTE:** Chaos (left) side should use blurred, desaturated imagery so it doesn't overpower the clean TLDR (right) side

---

## 5. Visual Design Specs

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Clean Side Background | Soft Gray | #F1F5F9 | Right half background (the TLDR side) |
| Chaos Side | Warm Orange/Red tones | #F97316 / #EF4444 | Left half — blurred, chaotic social feed colors |
| Divider Line | TLDR Blue | #2563EB | Vertical center line |
| Divider Badge BG | TLDR Blue | #2563EB | Circle/pill behind "5 min" |
| Text Primary | TLDR Black | #0F172A | Headline text |
| Text on Badge | White | #FFFFFF | "5 min" text |
| CTA Background | TLDR Blue | #2563EB | "Subscribe free" pill |
| CTA Text | White | #FFFFFF | Button text |

### Typography

| Element | Font | Weight | Size | Color | Notes |
|---------|------|--------|------|-------|-------|
| Headline | Inter | 700 (Bold) | 40px | #0F172A | Center-aligned across full width, top of safe zone |
| Divider stat | Inter | 800 (ExtraBold) | 48px | #FFFFFF | Centered on divider line, inside blue badge |
| Subhead | Inter | 500 (Medium) | 24px | #475569 | Right side, below phone mockup |
| CTA text | Inter | 600 (SemiBold) | 20px | #FFFFFF | Inside pill button |

### Logo

- **File:** TLDR wordmark, TLDR Blue (#2563EB) on transparent
- **Placement:** Bottom-right of clean (right) side
- **Minimum size:** 100 x 28px
- **Clear space:** 20px margin

### Background Treatment

- **Type:** Split image (composite)
- **Left half:** Nano Banana-generated chaotic social feed, blurred at 40%, warm color tint
- **Right half:** Solid #F1F5F9 with a clean phone mockup showing TLDR email
- **Divider:** 4px vertical line in #2563EB with a circular badge at center

---

## 6. Nano Banana Prompt

**Prompt:**
```
A split-screen composition. Left half: a chaotic, overwhelming social media feed with overlapping headlines, notifications, breaking news banners, trending hashtags, and bright clashing colors — representing information overload, slightly blurred and desaturated with warm orange and red tones. Right half: a clean, minimal smartphone screen displaying a simple, organized email newsletter with a blue header — calm, spacious, white background, easy to read. The two halves are divided by a sharp vertical line. The overall mood contrasts stress and chaos (left) with calm clarity (right). Professional, modern, advertising photography quality. No text, no logos, no readable words on either screen.
```

**Negative prompt:**
```
text, words, letters, readable text on screens, watermarks, logos, brand names, low quality, blurry overall, distorted, cartoonish, clip art, stock photo feel, faces, people
```

**Settings:**
- **Aspect ratio:** 4:5
- **Style:** Photographic / digital composite

**Post-generation notes:**
- The base image should NOT contain any readable text — all text is added in Figma/Canva
- The left side should feel visually "loud" and the right side should feel visually "quiet"
- Generate 3-4 variations; select the one with the sharpest contrast between sides
- Crop or adjust if the phone screen on the right is too detailed — it should be suggestive, not literal

---

## 7. Figma / Canva Overlay Instructions

### Layer Stack (bottom to top)

1. **Base image** (from Nano Banana — split screen chaos vs calm)
2. **Overlay/tint** — 15% white overlay on the right half if not bright enough for text contrast
3. **Headline text** — "This vs. This. 5 minutes." | Inter Bold 40px | #0F172A | Center horizontally, 280px from top
4. **Divider line** — 4px vertical line | #2563EB | Center horizontally, full height of safe zone
5. **Divider badge** — Circle, 80px diameter | #2563EB fill | Centered on divider line at vertical center
6. **Divider stat** — "5 min" | Inter ExtraBold 48px | #FFFFFF | Centered inside divider badge
7. **Subhead text** — "Tech news without the noise" | Inter Medium 24px | #475569 | Right half, center-aligned, 64px below badge
8. **CTA element** — "Subscribe free" | Pill, corner radius 24px | #2563EB background | #FFFFFF Inter SemiBold 20px | Right half, bottom of safe zone
9. **Logo** — TLDR wordmark (blue) | 100px wide | Bottom-right of right half, 40px from edges
10. **Labels** (optional) — Small "Scrolling" on left, "TLDR" on right | Inter Medium 14px | #94A3B8

### Figma-Specific Notes
- Build the split as two frames side by side within a parent auto-layout frame
- The divider badge is an absolutely positioned element on the center seam
- Create components: `morning-shortcut_4x5`, `morning-shortcut_1x1`, `morning-shortcut_9x16`
- For 1:1 adaptation: stack vertically (chaos on top, TLDR on bottom) with horizontal divider

### Canva-Specific Notes
- Use "Custom Size" for each variant
- Split effect: two image frames side by side, masked to half-width
- Group divider line + badge + text as one element for easy centering
- Export as PNG at 2x

---

## 8. Iteration Notes

Initial brief — no prior versions.
