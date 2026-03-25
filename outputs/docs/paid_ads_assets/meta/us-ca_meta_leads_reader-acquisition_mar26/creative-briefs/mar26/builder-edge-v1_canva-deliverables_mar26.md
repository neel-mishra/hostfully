# Builder's Edge v1 — Canva deliverables (Mar 2026)

**Revision:** `v3` — Built per [`builder-edge-v1_notification-cards_mar26.md`](builder-edge-v1_notification-cards_mar26.md): **placement-specific layouts** (not one master blindly resized). Reference texture: `builder-edge_card_texture` (`MAHEjTm-P2A`) inside notification cards; **canvas** = gradient `#0F172A` → `#1E3A5F` (135°).

| Placement | Brief rules applied |
|-----------|---------------------|
| **4:5 Hero** | 3 cards, ~900×100, 16px gaps, 8px stagger, 32px headline, stat + CTA |
| **9:16** | 3 cards, max ~780px wide, **24px** gaps, headline **36px**, stat **28px** |
| **1:1** | **2 cards** (AI + STARTUPS), headline **28px**, 12px card gap, stat + CTA |
| **1.91:1** | **1 card** (AI only), **no stat / no CTA**, compact logo + ~40px headline |

Reference file (repo): `../assets/builder-edge_reference_bg.png`

---

## Canva — edit links (exact pixel sizes)

| Size name | Canvas | Edit |
|-----------|--------|------|
| feed-portrait | 1080 × 1350 | [Edit](https://www.canva.com/d/eNNZxWST0venqlF) |
| stories-reels | 1080 × 1920 | [Edit](https://www.canva.com/d/NiL6i6YJhS4KGqR) |
| feed-square | 1080 × 1080 | [Edit](https://www.canva.com/d/qd2_wryqFDa_jUV) |
| right-column | 1200 × 628 | [Edit](https://www.canva.com/d/ev3Y_e-8CVWLON2) |

---

## Design IDs

| Placement | ID |
|-----------|-----|
| Feed Portrait | `DAHEjeh1kBU` |
| Stories / Reels | `DAHEjaqtiL0` |
| Feed Square | `DAHEjfDAKUc` |
| Right Column | `DAHEje9Qvyo` |

---

## Exports (2× PNG)

Save as: `meta-reader-acq-builder-edge-v1_{size-name}.png`

| size-name | Pixels | Download |
|-----------|--------|----------|
| feed-portrait | 2160 × 2700 | [PNG](https://export-download.canva.com/h1kBU/DAHEjeh1kBU/-1/0/0001-8165523713192230819.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260320%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260320T235035Z&X-Amz-Expires=23717&X-Amz-Signature=7f0c53887c20541cef8346319c04574b3a97221fc96731c650b36d68638a4fd2&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sat%2C%2021%20Mar%202026%2006%3A25%3A52%20GMT) |
| stories-reels | 2160 × 3840 | [PNG](https://export-download.canva.com/qtiL0/DAHEjaqtiL0/-1/0/0001-490264045422746797.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260320%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260320T205239Z&X-Amz-Expires=34143&X-Amz-Signature=fe1848c06ef6fc587d1b3a2884abaae381e354c71a0dc01e2d1200cf85738359&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sat%2C%2021%20Mar%202026%2006%3A21%3A42%20GMT) |
| feed-square | 2160 × 2160 | [PNG](https://export-download.canva.com/DAKUc/DAHEjfDAKUc/-1/0/0001-2951481244010652883.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260320%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260320T112427Z&X-Amz-Expires=70021&X-Amz-Signature=8dfcf7a4cab80c45b4e881de91f6dfd331afd3cc0ad9ba5399f5b7f0cb3ff4ef&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sat%2C%2021%20Mar%202026%2006%3A51%3A28%20GMT) |
| right-column | 2400 × 1256 | [PNG](https://export-download.canva.com/9Qvyo/DAHEje9Qvyo/-1/0/0001-423835952678250464.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAQYCGKMUH5AO7UJ26%2F20260321%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20260321T021630Z&X-Amz-Expires=16397&X-Amz-Signature=50932f081b2a606449a0431b81e7309faf6fd1e6fa1d445c288e021ff05a370b&X-Amz-SignedHeaders=host%3Bx-amz-expected-bucket-owner&response-expires=Sat%2C%2021%20Mar%202026%2006%3A49%3A47%20GMT) |

> Export URLs expire — re-export from **Edit** links when needed.

---

## QA checklist (in Canva)

- [ ] Headline reads exactly: **Your daily edge in tech**
- [ ] Card copy matches: OpenAI / Rust / Stripe lines (or 2 lines on 1:1; 1 card on right column)
- [ ] **1:1** shows only **two** cards; **right column** has **no** stat or CTA
- [ ] Texture visible inside cards; canvas is **gradient only** (no full-bleed photo)
- [ ] Rename design titles to campaign naming if desired (Canva auto-titles may differ)

---

## Import note

Asset imported via temporary HTTPS (`tmpfiles.org`) because Canva requires `https://` URLs.
