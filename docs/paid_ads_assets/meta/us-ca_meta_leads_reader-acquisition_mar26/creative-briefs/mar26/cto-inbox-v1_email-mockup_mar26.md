# Visual Creative Brief

## 1. Brief Header

| Field | Value |
|-------|-------|
| **Brief ID** | meta-reader-acq-cto-inbox-v1 |
| **Version** | v1 |
| **Date Created** | 2026-03-09 |
| **Status** | Draft |
| **Platform** | Meta (Facebook / Instagram) |
| **Ad Type** | Single Image |
| **Campaign** | us-ca_meta_leads_reader-acquisition_mar26 |
| **Ad Group** | lal_subscribers-3pct_us-ca |
| **Ad Name** | single-img_cto-inbox-v1 |
| **Placements** | Advantage+ (Feed, Stories, Reels, Right Column, Audience Network) |
| **Network Side** | Reader acquisition |
| **Target Persona** | R3: The Ambitious Builder |
| **Messaging Pillar** | Pillar 3: Professional Credibility |
| **Ad Creative** | [us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md](../../us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md) |
| **Campaign Structure** | [us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md](../../us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md) |
| **Campaign Index** | [_index.md](../../_index.md) |

---

## 2. Concept Overview

**Concept Name:** The CTO's Inbox

**Description:** A realistic but stylized inbox mockup on a dark background. One unread email highlighted — "TLDR Tech" as the sender, subject line: "AI funding hits $100B, GitHub ships Copilot X, and the layoffs nobody's talking about." The rest of the inbox is grayed out. The message: this is the one email that matters.

**Visual Hook:** The single highlighted unread email in a sea of grayed-out messages — the eye is drawn to the bright blue highlight row immediately.

**On-Image Copy:**
- **Headline:** "The one email your CTO never skips"
- **Subhead/Body:** None — the inbox mockup IS the supporting content
- **Stat/Number:** None
- **CTA:** "FREE" (badge overlay, top-right corner)

**Emotional Tone:** Peer credibility, curiosity

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
- [ ] File names follow convention: `meta-reader-acq-cto-inbox-v1_{size-name}.png`
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
│  │  "The one email your CTO" │  │  ← Headline at top of
│  │   (center, 36px)          │  │    safe zone
│  │                           │  │
│  │  ┌─────────────────────┐  │  │
│  │  │ grayed email row    │  │  │
│  │  │▓▓ TLDR (highlighted)│  │  │  ← Inbox mockup centered
│  │  │ grayed email row    │  │  │    in safe zone (5 rows)
│  │  │ grayed email row    │  │  │
│  │  │ grayed email row    │  │  │
│  │  └─────────────────────┘  │  │
│  │                 TLDR logo─►│  │
│  └───────────────────────────┘  │
│  [FREE badge top-right corner]  │
│  ▓ BOTTOM 150px ▓▓▓▓▓▓▓▓▓▓▓▓  │
└─────────────────────────────────┘
```

**Stories / Reels — 9:16 (1080 x 1920px):**

```
┌─────────────────────────────────┐
│  ▓ TOP 320px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │  ← Profile, "Sponsored"
│                                 │
│  ┌───────────────────────┐     │
│  │ "The one email your   │     │  ← Headline at 40px
│  │  CTO never skips"     │  ♡  │
│  │                       │  💬 │
│  │ ┌───────────────────┐ │  ↗  │
│  │ │ grayed row        │ │     │  ← Expand to 6-7 rows
│  │ │▓▓ TLDR highlight ▓│ │     │    in taller canvas
│  │ │ grayed row        │ │     │    780px wide (safe width)
│  │ │ grayed row        │ │     │
│  │ │ grayed row        │ │     │
│  │ │ grayed row        │ │     │
│  │ └───────────────────┘ │     │
│  │      TLDR logo ──────►│     │
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
│ ▓ │ "The one email..."    │  ▓ │  ← Reduce to 4 inbox rows
│ ▓ │ ┌─────────────────┐  │  ▓ │    to fit 864x864 safe zone
│ ▓ │ │ grayed row      │  │  ▓ │
│ ▓ │ │▓▓ TLDR highlight│  │  ▓ │
│ ▓ │ │ grayed row      │  │  ▓ │
│ ▓ │ │ grayed row      │  │  ▓ │
│ ▓ │ └─────────────────┘  │  ▓ │
│ ▓ │        TLDR logo ───►│  ▓ │
│ ▓ └───────────────────────┘  ▓ │
│  ▓ BOTTOM 108px ▓▓▓▓▓▓▓▓▓▓▓▓  │
└─────────────────────────────────┘
```

**Right Column — 1.91:1 (1200 x 628px):**

```
┌─────────────────────────────────────────┐
│ ▓60px ┌───────────────────────┐  60px ▓ │
│ ▓     │ "The one email your   │       ▓ │  ← Reduce inbox to 2-3
│ ▓     │  CTO never skips"     │       ▓ │    rows. Headline at 40px.
│ ▓     │ ▓▓ TLDR highlight ▓▓  │       ▓ │    Logo right side.
│ ▓     │ grayed row    TLDR ──►│       ▓ │
│ ▓     └───────────────────────┘       ▓ │
│ ▓60px ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  60px ▓ │
└─────────────────────────────────────────┘
```

### Recommended Layout (per size)

**4:5 (Hero):**
- **Headline:** Center-aligned, 280px from top, 36px
- **Inbox mockup:** Centered, 900px wide x 500px tall, 48px below headline
- **TLDR highlight row:** Second row (eye naturally tracks to highlighted item)
- **FREE badge:** Top-right corner, 48px from edges (outside safe zone — intentional accent)
- **Logo:** Bottom-right of safe zone, 40px from edges

**9:16 (Stories/Reels):**
- Scale headline to 40px for full-screen
- Expand inbox to 6-7 rows using taller safe zone
- Inbox 780px wide (safe width minus right margin for icons)
- Logo bottom-center (avoid right-edge Reels icons)

**1:1 (Feed Square):**
- Reduce inbox to 4 rows to fit 864x864
- Scale headline to 32px
- Inbox width: 780px centered in safe zone

**1.91:1 (Right Column):**
- Reduce inbox to 2-3 rows max
- Headline at 40px — must be legible at small size
- Remove FREE badge — too small
- Simplified: headline + abbreviated inbox + logo

### Designer Notes

- **DO:** Verify the highlighted TLDR email row is inside the safe zone and visually prominent at every size
- **DO:** Scale inbox mockup proportionally — more rows on taller formats (9:16), fewer on shorter (1.91:1)
- **DO:** Keep inbox container within safe zone margins at every size
- **DO:** Use minimum 18px for inbox text on 4:5, scale up for 9:16, simplify for 1.91:1
- **DON'T:** Place headline in top 250px (4:5) or top 320px (9:16) — profile overlay
- **DON'T:** Place inbox rows in bottom 150px (4:5) or bottom 320px (9:16) — crop/CTA zones
- **DON'T:** Make inbox too realistic on 1.91:1 — at small size, fine detail is noise. Abstract it
- **NOTE:** FREE badge is intentionally placed outside safe zone (top-right corner) as a visual accent — not critical content
- **NOTE:** Meta may auto-crop 4:5 to 1:1 — verify center 1080x1080 still shows headline + highlighted row
- **NOTE:** Inbox content is illustrative — use realistic but fictional sender names and subject lines

---

## 5. Visual Design Specs

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | TLDR Black | #0F172A | Full canvas background behind inbox |
| Inbox Background | Dark Slate | #1E293B | Inbox container background |
| Highlighted Row | TLDR Blue | #2563EB (15% opacity) | Background tint of the TLDR email row |
| Unread Indicator | TLDR Blue | #2563EB | Blue dot next to unread TLDR email |
| Grayed Rows | Muted Gray | #334155 | Other emails — muted, not in focus |
| Grayed Text | Dark Gray | #64748B | Sender names, subject lines of other emails |
| Highlighted Text | White | #FFFFFF | TLDR email sender name and subject line |
| Headline Text | White | #FFFFFF | "The one email your CTO never skips" |
| FREE Badge BG | Signal Green | #10B981 | Badge background |
| FREE Badge Text | White | #FFFFFF | "FREE" text |

### Typography

| Element | Font | Weight | Size | Color | Notes |
|---------|------|--------|------|-------|-------|
| Headline | Inter | 700 (Bold) | 36px | #FFFFFF | Center-aligned, top of safe zone, max 2 lines |
| Inbox sender (TLDR) | Inter | 600 (SemiBold) | 18px | #FFFFFF | Left-aligned within highlighted row |
| Inbox subject (TLDR) | Inter | 400 (Regular) | 16px | #E2E8F0 | Below sender, left-aligned |
| Inbox sender (others) | Inter | 400 (Regular) | 18px | #64748B | Left-aligned, muted |
| Inbox subject (others) | Inter | 400 (Regular) | 16px | #475569 | Below sender, muted |
| FREE badge | Inter | 700 (Bold) | 14px | #FFFFFF | All caps, inside green badge |

### Logo

- **File:** TLDR logo icon (blue circle with "T") as sender avatar + TLDR wordmark bottom-right
- **Placement:** Sender avatar (36x36px, left of highlight row) + wordmark (100px, bottom-right)
- **Clear space:** 16px around avatar, 24px around wordmark

### Background Treatment

- **Type:** Solid dark + inbox UI overlay
- **Colors:** #0F172A canvas, #1E293B inbox container
- **Image treatment:** No Nano Banana base — UI mockup built in Figma/Canva

---

## 6. Nano Banana Prompt

UI mockup concept — no AI-generated image required. Build inbox in Figma/Canva.

**Alternative — atmospheric background behind inbox:**

**Prompt:**
```
Dark, moody workspace background with soft blue ambient lighting. A desk surface barely visible in the shadows, with subtle bokeh light spots suggesting a monitor glow. Deep navy (#0F172A) overall tone with hints of blue (#2563EB) reflected light. Cinematic, professional, tech workspace atmosphere. No screens, no devices, no people, no objects in focus — just ambient mood lighting on a dark surface.
```

**Negative prompt:**
```
text, words, letters, logos, screens, monitors, keyboards, phones, devices, people, faces, bright, daylight, cluttered, busy, cartoonish, low quality, blurry
```

**Settings:**
- **Aspect ratio:** 4:5
- **Style:** Photographic / cinematic

**Post-generation notes:**
- Ambient background is optional — solid #0F172A works well
- If used, must be very dark so inbox mockup overlay stands out
- All inbox UI elements built in Figma/Canva, not generated

---

## 7. Figma / Canva Overlay Instructions

### Layer Stack (bottom to top)

1. **Background** — Solid #0F172A fill (or Nano Banana ambient workspace)
2. **Headline text** — "The one email your CTO never skips" | Inter Bold 36px | #FFFFFF | Center-aligned, 280px from top
3. **Inbox container** — Rounded rectangle (16px radius), #1E293B fill, 900px x 500px | Centered, 48px below headline
4. **Email row 1 (grayed)** — 80px tall | Sender: "Newsletter Weekly" #64748B | Subject: "This week in product design..." #475569
5. **Email row 2 (HIGHLIGHTED)** — 80px tall | #2563EB at 15% opacity | Blue dot (8px) | TLDR avatar (36x36) | Sender: "TLDR Tech" #FFFFFF | Subject: "AI funding hits $100B, GitHub ships Copilot X, and the layoffs nobody's talking about" #E2E8F0
6. **Email row 3 (grayed)** — Sender: "Dev Updates" | Subject: "v4.2 release notes..."
7. **Email row 4 (grayed)** — Sender: "TechCrunch" | Subject: "Startups to watch in..."
8. **Email row 5 (grayed)** — Sender: "Marketing Weekly" | Subject: "Campaign performance..."
9. **FREE badge** — Pill 60x28px | #10B981 fill | "FREE" Inter Bold 14px #FFFFFF | Top-right, 48px from edges
10. **Logo** — TLDR wordmark (white) | 100px wide | Bottom-right, 40px from edges

### Figma-Specific Notes
- Build inbox as a frame with Auto Layout (vertical stack of row components)
- Highlighted row is a variant with #2563EB/15% background
- Create components: `cto-inbox_4x5`, `cto-inbox_1x1`, `cto-inbox_9x16`
- For 1:1: reduce to 4 rows, headline to 40px. For 9:16: add rows, increase spacing

### Canva-Specific Notes
- Build inbox using rectangles + text elements + circle for avatar
- Use "Group" to keep inbox elements together
- Highlighted row: blue rectangle at reduced opacity behind text
- Export as PNG at 2x

---

## 8. Iteration Notes

Initial brief — no prior versions.
