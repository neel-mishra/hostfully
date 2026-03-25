# Visual Creative Brief – `static_time-saved_mar26_v1`

## 1. Brief Header

| Field | Value |
|-------|-------|
| **Brief ID** | meta-reader-acq-time-saved-email-preview-v1 |
| **Version** | v1 |
| **Date Created** | 2026-03-16 |
| **Status** | Draft |
| **Platform** | Meta (Facebook / Instagram) |
| **Ad Type** | Single Image |
| **Campaign** | us-ca_meta_leads_reader-acquisition_mar26 |
| **Ad Group** | broad_advantageplus_readers_prospecting / interests_tech-biz-news_prospecting |
| **Ad Name** | static_time-saved_mar26_v1 |
| **Placements** | Advantage+ (Feed, Stories, Reels, Right Column, Audience Network) |
| **Network Side** | Reader acquisition |
| **Target Persona** | Tech-curious professionals (engineers, PMs, founders, growth, data) |
| **Messaging Pillar** | Time Reclaimed |
| **Ad Creative** | [us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md](../../us-ca_meta_leads_reader-acquisition_mar26_ad-creative_mar26.md) |
| **Campaign Structure** | [us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md](../../us-ca_meta_leads_reader-acquisition_mar26_campaign-structure.md) |
| **Campaign Index** | [_index.md](../../_index.md) |

---

## 2. Concept Overview

**Concept Name:** Email Preview – “5‑Minute Briefing”

**Description:** A clean, realistic preview of the TLDR email on a phone screen, centered on a white or very light background. Above the device: a short line anchoring the 5‑minute promise. Below: a simple CTA to “Get the 5‑minute briefing.” The hero is the newsletter UI itself.

**Visual Hook:** Seeing the actual email — it looks skimmable, structured, and approachable. The viewer immediately understands “this is what I’ll get.”

**On-Image Copy:**
- **Top kicker (optional):** “Takes ~5 minutes”
- **Headline:** “Your daily tech briefing.”
- **Subhead:** “One email. All the important stories, tools, and ideas.”
- **CTA badge/button:** “Get TLDR free”

**Emotional Tone:** Calm, competent, low‑friction; “this will make my mornings easier.”

---

## 3. Sizing Variants

| Priority | Size Name | Dimensions | Aspect Ratio | File Type | Max Size | Placement |
|----------|-----------|------------|--------------|-----------|----------|-----------|
| Hero | Feed Portrait | 1080 x 1350px | 4:5 | PNG | 30MB | Feed (mobile-optimized) |
| Adapt | Stories/Reels | 1080 x 1920px | 9:16 | PNG | 30MB | Stories, Reels |
| Adapt | Feed Square | 1080 x 1080px | 1:1 | PNG | 30MB | Feed fallback, Marketplace |

**Export checklist:**
- [ ] Export all sizes at 2x resolution.
- [ ] Filenames: `meta-reader-acq-time-saved-email-preview-v1_{size-name}.png`.
- [ ] Phone screen content readable on a small mobile feed (no tiny text).

---

## 4. Layout & Safe Zones

### Shared Layout Principles

- TLDR email preview sits in the **vertical center**, slightly above exact center to leave room for CTA/subhead below.
- On-asset text should be minimal and large; detailed copy lives in the ad text field, not on the image.
- No critical content in the very top (profile overlay) or bottom (CTA/on-screen buttons) zones.

### 4:5 Feed Portrait (Hero – 1080 x 1350px)

- **Safe content zone:** Center 1080 x 950px (same pattern as existing briefs).
- **Layout:**
  - Top 15–20%: “Takes ~5 minutes” in small uppercase type.
  - Middle 50%: Phone mockup showing TLDR email. Screen should show:
    - Header with TLDR logo.
    - A few story headlines and bullets to convey skimmable structure.
  - Below phone: “Your daily tech briefing.” then “One email. All the important stories, tools, and ideas.”
  - Bottom safe zone: pill CTA “Get TLDR free”.

### 9:16 Stories / Reels

- **Safe content zone:** 880 x 1280px center.
- **Layout changes:**
  - Phone mockup slightly larger; vertically centered between overlays.
  - Move headline/subhead above the phone; CTA text below.
  - Keep enough right-hand margin (~100px) for engagement icons.

### 1:1 Feed Square

- **Safe content zone:** 864 x 864px center.
- **Layout changes:**
  - Crop in tighter on the phone screen and simplify on-image text:
    - Headline: “Your daily tech briefing.”
    - CTA: “Get TLDR free”.
  - Consider removing kicker “Takes ~5 minutes” if space is tight.

---

## 5. Visual Design Specs

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Background | Soft white | #F8FAFC | Canvas background |
| Device bezel | Near-black | #020617 | Phone frame |
| Email chrome | White | #FFFFFF | Inside device |
| Primary accent | TLDR Blue | #2563EB | Buttons, links, logo |
| Text (headline) | TLDR Black | #0F172A | On-image copy |
| CTA text | White | #FFFFFF | On CTA pill |

### Typography

| Element | Font | Weight | Size (4:5) | Color | Notes |
|---------|------|--------|------------|-------|-------|
| Headline | Inter | 700 | 64px | #0F172A | “Your daily tech briefing.” |
| Subhead | Inter | 400 | 32px | #0F172A | Max 2 lines |
| Kicker | Inter | 500 | 24px | #64748B | “Takes ~5 minutes” |
| CTA | Inter | 600 | 28px | #FFFFFF | Inside pill button |

### Logo

- Use TLDR wordmark in TLDR Blue (#2563EB) on transparent.
- Include within the email preview header **and** optionally as a small mark near the CTA.

---

## 6. Nano Banana Prompt (Optional Background)

If you want a subtle, photo-real background behind the phone:

**Prompt:**
```
Minimal desk scene with soft neutral background, subtle blur, and a clean modern feel. Focus is on empty space in the center for a phone mockup overlay. No visible logos, no text, no people. High-key lighting, tech-savvy aesthetic, advertising-quality.
```

**Negative prompt:**
```
text, letters, numbers, logos, clutter, busy, dark, low quality, noisy, messy, hands, people, faces
```

Keep all important content in the overlay; background is just texture.

