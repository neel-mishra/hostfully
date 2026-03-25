# Visual Creative Brief – `static_social-proof_mar26_v1`

## 1. Brief Header

| Field | Value |
|-------|-------|
| **Brief ID** | meta-reader-acq-social-proof-grid-v1 |
| **Version** | v1 |
| **Date Created** | 2026-03-16 |
| **Status** | Draft |
| **Platform** | Meta (Facebook / Instagram) |
| **Ad Type** | Single Image |
| **Campaign** | us-ca_meta_leads_reader-acquisition_mar26 |
| **Ad Group** | broad_advantageplus_readers_prospecting / lal_subscribers-1pct_usca_prospecting / retargeting_site-visitors30_engagers90 |
| **Ad Name** | static_social-proof_mar26_v1 |
| **Placements** | Advantage+ (Feed, Stories, Reels, Right Column, Audience Network) |
| **Network Side** | Reader acquisition |
| **Target Persona** | Builders and ambitious professionals who care what their peers read |
| **Messaging Pillar** | Professional Credibility / Peer Proof |
| **Ad Creative** | [us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md](../../us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md) |
| **Campaign Structure** | [us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md](../../us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md) |
| **Campaign Index** | [_index.md](../../_index.md) |

---

## 2. Concept Overview

**Concept Name:** Social Proof Grid

**Description:** A grid-style layout that quickly communicates “people like you already read TLDR.” Top half: a bold headline and short explanation. Bottom half: compact social-proof elements — subscriber count, small logos (if available), and 2–3 short testimonial callouts.

**Visual Hook:** Seeing that a meaningful, credible group already relies on TLDR — makes subscribing feel like the default choice.

**On-Image Copy:**
- **Headline:** “The newsletter tech people actually read.”
- **Subhead:** “Engineers, PMs, founders, and builders start their day with TLDR.”
- **Proof tiles (examples):**
  - “Trusted by thousands of builders”
  - “5‑minute daily briefing”
  - “Free, no fluff”
- **CTA badge:** “Join free”

**Emotional Tone:** Inclusive, confident, peer-driven; “you’re in good company here.”

---

## 3. Sizing Variants

| Priority | Size Name | Dimensions | Aspect Ratio | File Type | Max Size | Placement |
|----------|-----------|------------|--------------|-----------|----------|-----------|
| Hero | Feed Portrait | 1080 x 1350px | 4:5 | PNG | 30MB | Feed (mobile-optimized) |
| Adapt | Stories/Reels | 1080 x 1920px | 9:16 | PNG | 30MB | Stories, Reels |
| Adapt | Feed Square | 1080 x 1080px | 1:1 | PNG | 30MB | Feed fallback, Marketplace |

---

## 4. Layout & Safe Zones

### 4:5 Feed Portrait (Hero)

- Top 35–40%: Headline + subhead, left-aligned or center-aligned.
- Bottom 60–65%: 3–4 social-proof tiles in a simple grid:
  - Each tile: icon (simple shape), short line of text.
  - One tile can carry the subscriber count (e.g., “1.6M+ readers” if you’re comfortable; otherwise “Thousands of readers”).
- CTA badge pinned near bottom center: “Join free”.
- Keep all text in center 70% vertical safe zone; avoid top 250px / bottom 150px overlap.

### 1:1 Feed Square

- Compress the grid to 2–3 tiles.
- Scale headline text up slightly; keep subhead to max 2 lines.
- Place CTA directly under the grid.

### 9:16 Stories / Reels

- Stack elements vertically:
  - Top: Headline.
  - Middle: 3 proof tiles in a single column.
  - Bottom: CTA badge.
- Maintain 320px safe zones at top/bottom.

---

## 5. Visual Design Specs

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | White | #FFFFFF | Canvas |
| Headline text | TLDR Black | #0F172A | Hero line |
| Subhead text | Slate | #64748B | Supporting line |
| Tile background | Light Slate | #F1F5F9 | Proof tiles |
| Tile border | Slate | #E2E8F0 | Optional subtle border |
| Accent | TLDR Blue | #2563EB | Icons, CTA, key phrases |
| CTA text | White | #FFFFFF | On CTA pill |

### Typography

| Element | Font | Weight | Size (4:5) | Notes |
|---------|------|--------|------------|-------|
| Headline | Inter | 700 | 60–64px | “The newsletter tech people actually read.” |
| Subhead | Inter | 400 | 30–32px | Max 2 lines |
| Tile text | Inter | 500 | 26px | One line per tile |
| CTA text | Inter | 600 | 26–28px | “Join free” |

---

## 6. Asset Content Guidelines

- **Logos:** Only include company logos if you have explicit permission / existing relationship. Otherwise use generic “avatars” or icons.
- **Testimonials:** If you have real short quotes (“TLDR is my favorite way to catch up on tech”), they can live in 1–2 tiles. Keep them to max 8–10 words.
- **Icons:** Use simple geometric icons (circles, checkmarks, minimal line art). No clip-art style.

---

## 7. Nano Banana Prompt (Optional Crowd/Pattern Background)

If you want a subtle “many people” motif behind the tiles:

**Prompt:**
```
Minimal abstract background suggesting a crowd of people as soft circular silhouettes in TLDR blue and muted neutral tones, heavily blurred and low contrast. Modern, techy, editorial feel. No readable faces, no text, no logos.
```

**Negative prompt:**
```
sharp faces, detailed people, text, logos, clutter, busy, low quality, dark, noisy
```

Use overlay layer at low opacity; keep proof tiles and text on a solid white panel for legibility.

