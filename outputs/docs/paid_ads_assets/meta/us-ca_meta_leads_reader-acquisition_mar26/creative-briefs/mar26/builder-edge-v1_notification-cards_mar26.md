# Visual Creative Brief

## 1. Brief Header

| Field | Value |
|-------|-------|
| **Brief ID** | meta-reader-acq-builder-edge-v1 |
| **Version** | v1 |
| **Date Created** | 2026-03-09 |
| **Status** | Draft |
| **Platform** | Meta (Facebook / Instagram) |
| **Ad Type** | Single Image |
| **Campaign** | us-ca_meta_leads_reader-acquisition_mar26 |
| **Ad Group** | lal_subscribers-1pct_us-ca / interest_tech-professionals_us-ca |
| **Ad Name** | single-img_builder-edge-v1 |
| **Placements** | Advantage+ (Feed, Stories, Reels, Right Column, Audience Network) |
| **Network Side** | Reader acquisition |
| **Target Persona** | R3: The Ambitious Builder |
| **Messaging Pillar** | Pillar 3: Professional Credibility |
| **Ad Creative** | [us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md](../../us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md) |
| **Campaign Structure** | [us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md](../../us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md) |
| **Campaign Index** | [_index.md](../../_index.md) |

---

## 2. Concept Overview

**Concept Name:** The Builder's Edge

**Description:** Dark gradient background (TLDR Black to TLDR Blue). Three stacked notification-style cards showing TLDR headlines — one about AI, one about a startup funding round, one about a new dev tool. Feels like an insider briefing. Accent green (#10B981) highlights on key words. TLDR logo top-left.

**Visual Hook:** The stacked notification cards — they look like push notifications or a news feed, triggering the instinct to read them. The format is instantly recognizable and curiosity-inducing.

**On-Image Copy:**
- **Headline:** "Your daily edge in tech"
- **Subhead/Body:** (Embedded in notification cards as sample headlines)
- **Stat/Number:** "1.6M+ readers"
- **CTA:** "Subscribe free"

**Notification Card Headlines (sample — not real news):**
- Card 1: "OpenAI closes $6B round at $150B valuation"
- Card 2: "Rust overtakes Go in backend adoption survey"
- Card 3: "Stripe launches AI billing engine for SaaS"

**Emotional Tone:** Ambitious, insider access

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
- [ ] File names follow convention: `meta-reader-acq-builder-edge-v1_{size-name}.png`
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
│  ▓ TOP 250px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Profile overlay
│                                 │
│  ┌───────────────────────────┐  │
│  │ TLDR logo  "Your daily    │  │  ← Logo + headline at
│  │            edge in tech"  │  │    top of safe zone
│  │                           │  │
│  │  ┌─────────────────────┐  │  │
│  │  │ AI  ▪ Card 1        │  │  │
│  │  └─────────────────────┘  │  │  ← Cards stacked: 16px
│  │    ┌─────────────────────┐│  │    gaps, 8px right offset
│  │    │ STARTUPS ▪ Card 2   ││  │    per card for depth
│  │    └─────────────────────┘│  │
│  │      ┌─────────────────────┐ │
│  │      │ DEV TOOLS ▪ Card 3  │ │
│  │      └─────────────────────┘ │
│  │  "1.6M+ readers"            │  │
│  │  [Subscribe free]            │  │  ← Stat + CTA at bottom
│  └───────────────────────────┘  │    of safe zone
│                                 │
│  ▓ BOTTOM 150px ▓▓▓▓▓▓▓▓▓▓▓▓  │
└─────────────────────────────────┘
```

**Stories / Reels — 9:16 (1080 x 1920px):**

```
┌─────────────────────────────────┐
│  ▓ TOP 320px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Profile, "Sponsored"
│                                 │
│  ┌───────────────────────┐     │
│  │ TLDR  "Your daily     │     │
│  │       edge in tech"   │  ♡  │  ← Logo + headline
│  │                       │  💬 │
│  │ ┌───────────────────┐ │  ↗  │
│  │ │ AI ▪ Card 1       │ │     │
│  │ └───────────────────┘ │     │  ← Cards max 780px wide
│  │  ┌───────────────────┐│     │    24px gaps for more
│  │  │ STARTUPS ▪ Card 2 ││     │    vertical breathing room
│  │  └───────────────────┘│     │
│  │   ┌───────────────────┐     │
│  │   │ DEV TOOLS ▪ Card 3│     │
│  │   └───────────────────┘     │
│  │                       │     │
│  │  "1.6M+ readers"     │     │
│  │  [Subscribe free]     │     │
│  └───────────────────────┘     │
│                                 │
│  ▓ BOTTOM 320px ▓▓▓▓▓▓▓▓▓▓▓▓  │  ← CTA button, reply bar
└─────────────────────────────────┘
```

**Feed Square — 1:1 (1080 x 1080px):**

```
┌─────────────────────────────────┐
│  ▓ TOP 108px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │
│ ▓                             ▓ │
│ ▓ ┌───────────────────────┐  ▓ │
│ ▓ │ TLDR "Your daily edge"│  ▓ │  ← Reduce to 2 cards
│ ▓ │                       │  ▓ │    in 864x864 safe zone
│ ▓ │ ┌─────────────────┐  │  ▓ │
│ ▓ │ │ AI ▪ Card 1     │  │  ▓ │
│ ▓ │ └─────────────────┘  │  ▓ │
│ ▓ │  ┌─────────────────┐ │  ▓ │
│ ▓ │  │ STARTUPS ▪ Card 2│ │  ▓ │
│ ▓ │  └─────────────────┘ │  ▓ │
│ ▓ │ "1.6M+"  [Subscribe] │  ▓ │
│ ▓ └───────────────────────┘  ▓ │
│  ▓ BOTTOM 108px ▓▓▓▓▓▓▓▓▓▓▓▓  │
└─────────────────────────────────┘
```

**Right Column — 1.91:1 (1200 x 628px):**

```
┌─────────────────────────────────────────┐
│ ▓60px ┌───────────────────────┐  60px ▓ │
│ ▓     │ TLDR  "Your daily     │       ▓ │  ← Single card only
│ ▓     │       edge in tech"   │       ▓ │    + headline + logo
│ ▓     │ ┌─────────────────┐  │       ▓ │    Remove stat/CTA
│ ▓     │ │ AI ▪ Card 1     │  │       ▓ │
│ ▓     │ └─────────────────┘  │       ▓ │
│ ▓     └───────────────────────┘       ▓ │
│ ▓60px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  60px ▓ │
└─────────────────────────────────────────┘
```

### Recommended Layout (per size)

**4:5 (Hero):**
- **Logo:** Top-left of safe zone, 48px from left edge
- **Headline:** Top-right of safe zone, beside logo, 32px
- **Card stack:** Center of safe zone. Cards 900px wide, 100px tall, 16px gaps, 8px right-offset per card
- **Stat ("1.6M+ readers"):** Center-aligned below cards, 40px gap
- **CTA ("Subscribe free"):** Center pill below stat, 24px gap
- **Gradient:** Darkest top-left, lightest (most blue) bottom-right

**9:16 (Stories/Reels):**
- All 3 cards fit — increase spacing to 24px between cards
- Card width: 780px (safe width after 100px right margin)
- Scale headline to 36px, stat to 28px
- Logo top-left of safe zone (below 320px top margin)

**1:1 (Feed Square):**
- Reduce to 2 cards — 3 won't fit in 864x864 with headline + stat + CTA
- Card width: 780px centered
- Tighten spacing: 12px between cards, 24px to stat
- Scale headline to 28px

**1.91:1 (Right Column):**
- Reduce to 1 card — concept as a "peek" at the briefing format
- Headline at 40px, single card at 80px
- Remove stat and CTA — too small. Logo top-left at 80x22px

### Designer Notes

- **DO:** Verify all notification cards are fully inside the safe zone — cards clipped by margins look broken
- **DO:** Scale down card count as canvas shrinks: 3 cards (4:5, 9:16) → 2 cards (1:1) → 1 card (1.91:1)
- **DO:** Maintain the 8px right-offset cascade for depth — adjust proportionally per size
- **DO:** Keep card content (category + headline + timestamp) within card bounds at every size
- **DON'T:** Place cards or headline in top 250px (4:5) or top 320px (9:16) — profile overlay
- **DON'T:** Extend cards into right 100px on 9:16 — Reels engagement icons stack there
- **DON'T:** Try to fit all 3 cards on 1:1 or 1.91:1 — too small to read, feels cramped
- **NOTE:** Meta may auto-crop 4:5 to 1:1 — verify center 1080x1080 shows headline + at least 2 cards
- **NOTE:** The staggered offset is subtle (8px/card) — don't overdo it or it looks misaligned
- **NOTE:** Gradient (#0F172A → #1E3A5F) should remain consistent across all sizes

---

## 5. Visual Design Specs

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background (top) | TLDR Black | #0F172A | Top of gradient |
| Background (bottom) | TLDR Blue Dark | #1E3A5F | Bottom of gradient, subtle blue shift |
| Card Background | Dark Slate | #1E293B | Notification card fill, 90% opacity |
| Card Border | Slate Border | #334155 | 1px border on cards |
| Card Text (headline) | White | #FFFFFF | Notification headline text |
| Card Text (category) | Signal Green | #10B981 | Category labels: "AI", "STARTUPS", "DEV TOOLS" |
| Card Timestamp | Muted Gray | #94A3B8 | "Just now" or "5 min ago" labels |
| Headline Text | White | #FFFFFF | "Your daily edge in tech" |
| Stat Text | Signal Green | #10B981 | "1.6M+ readers" |
| CTA Background | TLDR Blue | #2563EB | Pill button |
| CTA Text | White | #FFFFFF | "Subscribe free" |

### Typography

| Element | Font | Weight | Size | Color | Notes |
|---------|------|--------|------|-------|-------|
| Headline | Inter | 700 (Bold) | 32px | #FFFFFF | Top of safe zone, left or center-aligned |
| Card category | Inter | 600 (SemiBold) | 12px | #10B981 | All caps, top of each card |
| Card headline | Inter | 500 (Medium) | 18px | #FFFFFF | Below category, left-aligned, max 2 lines |
| Card timestamp | Inter | 400 (Regular) | 12px | #94A3B8 | Right-aligned, "Just now" |
| Stat number | Inter | 700 (Bold) | 24px | #10B981 | Center-aligned below card stack |
| CTA text | Inter | 600 (SemiBold) | 20px | #FFFFFF | Inside pill button |

### Logo

- **File:** TLDR wordmark, white on transparent
- **Placement:** Top-left of safe zone
- **Minimum size:** 100 x 28px
- **Clear space:** 16px margin

### Background Treatment

- **Type:** Gradient
- **Direction:** Top-left to bottom-right (135°)
- **Colors:** #0F172A (start) → #1E3A5F (end)
- **Image treatment:** No Nano Banana base needed — pure graphic concept

---

## 6. Nano Banana Prompt

Graphic/UI concept — no AI-generated base required. Build in Figma/Canva.

**Alternative — atmospheric gradient background with texture:**

**Prompt:**
```
Abstract dark gradient background flowing from deep navy (#0F172A) at the top-left to a rich dark blue (#1E3A5F) at the bottom-right. Subtle digital mesh or network lines barely visible, like a neural network visualization at 5% opacity. Faint bokeh light spots scattered at the bottom-right corner, blue-tinted. Clean, modern, tech-forward atmosphere. Premium advertising quality. No objects, no devices, no people.
```

**Negative prompt:**
```
text, words, letters, numbers, logos, faces, people, devices, screens, bright colors, busy, cluttered, cartoonish, clip art, stock photo, low quality, blurry, distorted
```

**Settings:**
- **Aspect ratio:** 4:5
- **Style:** Digital abstract / 3D render

**Post-generation notes:**
- Gradient background is optional — CSS-style gradient in Figma works perfectly
- If using Nano Banana, texture should be extremely subtle — notification cards must be the focus
- All card UI, text, and logo are built in Figma/Canva

---

## 7. Figma / Canva Overlay Instructions

### Layer Stack (bottom to top)

1. **Background** — Linear gradient: #0F172A → #1E3A5F, 135° (or Nano Banana textured gradient)
2. **Logo** — TLDR wordmark (white) | 100px wide | Top-left, 48px from left, 270px from top
3. **Headline** — "Your daily edge in tech" | Inter Bold 32px | #FFFFFF | Top area, 16px right of logo or centered below
4. **Card 1** — Rounded rect (12px radius), 900px x 100px | #1E293B 90%, 1px #334155 border | Centered, 420px from top
   - Category: "AI" | Inter SemiBold 12px | #10B981 | 24px from left, 16px from top
   - Headline: "OpenAI closes $6B round at $150B valuation" | Inter Medium 18px | #FFFFFF | 24px from left, 36px from top
   - Timestamp: "Just now" | Inter Regular 12px | #94A3B8 | Right-aligned, 24px from right
5. **Card 2** — Same specs, offset 8px right | 16px below Card 1
   - Category: "STARTUPS" | Headline: "Rust overtakes Go in backend adoption survey" | Timestamp: "2 min ago"
6. **Card 3** — Same specs, offset another 8px right | 16px below Card 2
   - Category: "DEV TOOLS" | Headline: "Stripe launches AI billing engine for SaaS" | Timestamp: "5 min ago"
7. **Stat** — "1.6M+ readers" | Inter Bold 24px | #10B981 | Center-aligned, 40px below Card 3
8. **CTA** — "Subscribe free" | Pill, 24px radius | #2563EB bg | #FFFFFF Inter SemiBold 20px | Center, 24px below stat
9. **Subtle glow** (optional) — Soft #2563EB radial glow at 8% opacity behind card stack

### Figma-Specific Notes
- Build each card as a reusable component with category color variants
- Use Auto Layout on card stack for consistent 16px spacing
- Staggered offset (8px/card) applied with manual positioning
- Create components: `builder-edge_4x5`, `builder-edge_1x1`, `builder-edge_9x16`
- For 1:1: 2 cards, tighter spacing, headline to 36px. For 9:16: add spacing, optionally add cards

### Canva-Specific Notes
- Build cards as grouped elements (rectangle + text)
- Use transparency slider for card background opacity
- Duplicate and reposition for stagger effect
- Group all cards for easy repositioning
- Export as PNG at 2x

---

## 8. Iteration Notes

Initial brief — no prior versions.
