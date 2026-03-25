# Visual Creative Brief – `static_noise-vs-signal_mar26_v1`

## 1. Brief Header

| Field | Value |
|-------|-------|
| **Brief ID** | meta-reader-acq-noise-vs-signal-split-v1 |
| **Version** | v1 |
| **Date Created** | 2026-03-16 |
| **Status** | Draft |
| **Platform** | Meta (Facebook / Instagram) |
| **Ad Type** | Single Image |
| **Campaign** | us-ca_meta_leads_reader-acquisition_mar26 |
| **Ad Group** | broad_advantageplus_readers_prospecting / retargeting_site-visitors30_engagers90 |
| **Ad Name** | static_noise-vs-signal_mar26_v1 |
| **Placements** | Advantage+ (Feed, Stories, Reels, Right Column, Audience Network) |
| **Network Side** | Reader acquisition |
| **Target Persona** | Tech readers overwhelmed by feeds and news volume |
| **Messaging Pillar** | Curated Signal / Time Reclaimed |
| **Ad Creative** | [us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md](../../us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md) |
| **Campaign Structure** | [us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md](../../us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md) |
| **Campaign Index** | [_index.md](../../_index.md) |

---

## 2. Concept Overview

**Concept Name:** Split Screen – “Less Noise. More Signal.”

**Description:** A clean left/right split visual. Left side: chaotic, blurred, noisy “feed” suggesting endless posts and notifications. Right side: calm TLDR email preview with minimal, structured content. Center line (or subtle divider) visually separates chaos from clarity.

**Visual Hook:** Contrast. Instantly communicates that TLDR is the clean alternative to doom‑scrolling.

**On-Image Copy:**
- **Left label (optional):** “Endless scroll”
- **Right label (optional):** “One email”
- **Headline (across or on right):** “Escape the scroll. Keep the signal.”
- **CTA badge (right side):** “Get TLDR free”

Tone: Relieved, calm, slightly playful — never scolding.

---

## 3. Layout & Safe Zones

### 4:5 Feed Portrait (Hero)

- Canvas divided vertically:
  - Left 50%: noisy feed.
  - Right 50%: TLDR email preview.
- Keep center division crisp (straight line or subtle gradient).
- Place headline either:
  - Across the top safe zone (spanning both halves), or
  - On the right half above the email preview.
- Place CTA badge on the right half near bottom safe zone.

### 1:1 Feed Square

- Same split, with slight bias:
  - 45% left (noise), 55% right (TLDR).
- Keep type larger to accommodate smaller canvas.

### 9:16 Stories / Reels

- Use horizontal split instead:
  - Top half: blurred feed chaos.
  - Bottom half: clean TLDR email preview + headline + CTA.
- Ensure overlays at top/bottom don’t cover headline or CTA.

---

## 4. Visual Design Specs

### “Noise” Side

- Abstract feed look:
  - Blocks / rectangles suggesting posts, comments, notifications.
  - Heavy blur and low opacity so nothing is readable.
  - Use muted greys and a few bright accent colors to suggest clutter.
- Never show real text, logos, or real social media UIs.

### “Signal” Side

- Clean TLDR email mockup:
  - White background, structured headlines, bullets.
  - Use TLDR Blue accents.
- Background behind email: plain white or very light slate (#F8FAFC).

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Noise background | Darker slate | #020617–#111827 | Left/top chaos |
| Noise blocks | Grey + accent | #4B5563, #6B7280, #EF4444, #F59E0B | Feed rectangles |
| Signal background | Soft white | #F8FAFC | Right/bottom TLDR area |
| Email content | White | #FFFFFF | Inside email card |
| Headline text | TLDR Black | #0F172A | “Escape the scroll. Keep the signal.” |
| CTA background | TLDR Blue | #2563EB | CTA pill |
| CTA text | White | #FFFFFF | On CTA |

---

## 5. Typography

| Element | Font | Weight | Size (4:5) | Notes |
|---------|------|--------|------------|-------|
| Headline | Inter | 700 | 60px | “Escape the scroll. Keep the signal.” |
| Labels | Inter | 500 | 26–28px | “Endless scroll” / “One email” |
| CTA text | Inter | 600 | 26–28px | “Get TLDR free” |

Keep all on-image text minimal; details live in primary text field.

---

## 6. Nano Banana Prompt (Base for Noise Half)

If you want AI base for the noisy half:

**Prompt:**
```
Chaotic abstract social media feed background, lots of overlapping rectangles and notification-style shapes, bright accent colors on dark grey, heavily blurred and defocused, no readable text or logos, sense of infinite scroll and information overload.
```

**Negative prompt:**
```
readable text, specific app UIs, logos, faces, people, sharp details, low quality
```

Use only on the “noise” side; overlay the TLDR email mockup on a clean solid background on the “signal” side.

