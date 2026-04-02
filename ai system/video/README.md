## VibeHypeVideoPipeline (`ai system/video/`)

This workspace hosts a Remotion-based hype video pipeline that reuses your real product UI components and renders a 20s 9:16 trailer.

### Install

```bash
cd "ai system/video"
npm install
```

### Preview

```bash
cd "ai system/video"
npm start
```

Open the Remotion preview UI, select `HypeVertical-9x16`, and scrub through the 20s storyboard.

### Render via CLI

Vertical 9:16:

```bash
cd "ai system/video"
COMP=HypeVertical-9x16 OUT=out/hype-9x16.mp4 node scripts/render.ts
```

Horizontal 16:9:

```bash
cd "ai system/video"
COMP=HypeHorizontal-16x9 OUT=out/hype-16x9.mp4 node scripts/render.ts
```

### Storyboard workflow

- Edit `src/storyboard/default20s.ts` to change beats, copy, and UI states.
- Wire beats to UI wrappers/compositions as you build out `src/ui` and `src/comps`.
- Use `UiParityHarness` to chase pixel-perfect matches against real app screenshots.

### Audio and post-production

- Use the `sfx` and `musicCue` fields in `src/storyboard/default20s.ts` as guidance for **where** audio events should land.
- Primary audio (music + detailed sound design) is added in CapCut or a similar NLE; the Remotion render is visual-first.
- Treat storyboard audio cues as a checklist when doing the CapCut pass: line them up on the waveform, then export platform presets.

### Music (Suno) and CapCut handoff

- Generate 2–3 20–25s tracks in Suno that match the video’s energy.
- Export high-quality audio (WAV/MP3).
- In CapCut, import the Remotion MP4 and Suno track.
- Make final micro-edits: beat-synced cuts, motion accents, captions, and safe framing.
- Export platform-specific presets (Reels, TikTok, Shorts) from CapCut.

