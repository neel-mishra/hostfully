---
name: humanizer
description: Score and rewrite AI-generated copy to sound human. Use when the user says "humanize," "sounds like AI," "make this sound human," "rewrite in my voice," "AI score," "humanizer," or when reviewing any near-final draft for AI patterns. Scores on four dimensions, diagnoses specific AI tells, and rewrites in TLDR's brand voice.
---

# Humanizer

Score drafts for AI-ness, diagnose what makes them feel machine-generated, and rewrite them to sound like a human wrote them — specifically a human who writes for TLDR.

## Workflow

### Step 1: Load Context

Before scoring or rewriting, read these files for voice calibration:

1. `commands/identity/brand_voice_matrix.md` — TLDR's voice rules
2. `commands/identity/messaging_pillars.md` — what TLDR sounds like when it's on
3. `.cursor/skills/humanizer/voice-samples.md` — real human-written samples (the ground truth)
4. `.cursor/skills/humanizer/patterns.md` — known AI patterns to detect

Determine the audience: **reader-facing** or **advertiser-facing** — the voice differs.

### Step 2: Score the Draft

Rate the draft on four dimensions, each 1–10:

| Dimension | 1 (Bad) | 5 (Passable) | 10 (Nailed It) |
|---|---|---|---|
| **AI Likeness** | Obviously machine-generated. Hits 5+ patterns from `patterns.md` | Some AI tells but could pass casual reading | Indistinguishable from human writing. Zero detected patterns |
| **Authenticity** | Generic voice. Could be any brand | Has some brand markers but inconsistent | Sounds exactly like TLDR — matches voice samples, follows brand matrix |
| **Reader Value** | Fluff and filler. No takeaway | Useful but padded with unnecessary setup | Every sentence earns its place. High density of insight per word |
| **Domain Credibility** | Surface-level, Wikipedia-grade understanding | Shows awareness of the space but uses safe/obvious takes | Demonstrates insider knowledge. Specific, opinionated, references real signals |

**Output format:**

```
## Humanizer Score

| Dimension | Score | Key Issue |
|---|---|---|
| AI Likeness | X/10 | [one-line diagnosis] |
| Authenticity | X/10 | [one-line diagnosis] |
| Reader Value | X/10 | [one-line diagnosis] |
| Domain Credibility | X/10 | [one-line diagnosis] |

**Overall: X/10**
```

### Step 3: Diagnose AI Patterns

Flag every specific instance where the draft feels AI-generated. Reference patterns from `patterns.md` by name. For each flag:

```
**[Pattern Name]** — Line/section where it appears
> "[exact quote from draft]"
Fix: [specific fix — not "make it more natural" but "replace with X" or "cut entirely"]
```

Aim for 5–15 flags per draft. If you find fewer than 3, the draft might already be clean — say so.

### Step 4: Rewrite

Rewrite the entire draft applying all fixes. Rules:

1. **Match the voice samples** in `.cursor/skills/humanizer/voice-samples.md` — sentence length, rhythm, how they open paragraphs, how they transition
2. **Apply brand voice matrix** — concise, trustworthy, sharp. Not terse, not preachy, not edgy
3. **Kill the patterns** — every item from Step 3 must be fixed in the rewrite
4. **Preserve the substance** — don't lose facts, data points, or arguments. Rewrite the packaging, not the payload
5. **Shorter is better** — if you can cut a sentence and lose nothing, cut it
6. **Lead with the interesting thing** — not "In today's landscape..." but the actual point
7. **One idea per sentence** — compound sentences are an AI tell

### Step 5: Show the Delta

After rewriting, show the before/after score:

```
## Score Delta

| Dimension | Before | After | Change |
|---|---|---|---|
| AI Likeness | X | Y | +Z |
| Authenticity | X | Y | +Z |
| Reader Value | X | Y | +Z |
| Domain Credibility | X | Y | +Z |
```

---

## Self-Improvement Protocol

After the user gives feedback on a rewrite, ask:

> "Should I update the humanizer skill based on this feedback? I can add new patterns, adjust scoring criteria, or update the voice samples."

If yes:

1. **New pattern detected?** → Append to `.cursor/skills/humanizer/patterns.md` with name, description, example, and fix
2. **Scoring calibration off?** → Note the recalibration in this file under "Scoring Adjustments"
3. **Voice sample needed?** → Ask the user for a paragraph of their own writing and append to `.cursor/skills/humanizer/voice-samples.md`
4. **Rewrite rule learned?** → Add to the "Rewrite Rules Learned" section below

---

## Rewrite Rules Learned

*This section grows over time as the skill learns from feedback.*

### Rule 1: Use the company's own data as proof points
TLDR has 48% open rates, 7M+ subscribers, 12 newsletters, specific case studies (Delve 52x ROI, Redact 50% lower CPC). When writing reader-facing content about newsletters, reference TLDR's actual numbers. First-party data instantly kills the generic Wikipedia feel and adds domain credibility. Check `commands/identity/messaging_pillars.md` for proof points.

### Rule 2: Target 40-60% word count reduction
Unedited AI blog posts are consistently 2-3x longer than they should be. The first humanizer run cut from ~1,800 words to ~750 (58% reduction). If your rewrite isn't at least 40% shorter, you haven't cut enough filler.

### Rule 3: "Have an opinion" is the highest-impact single fix
Replacing hedge language ("there are pros and cons," "it depends on your needs") with a clear position ("Habits drive open rates more than subject lines do") is the single change that most improves both AI Likeness and Domain Credibility scores. TLDR's brand voice is authoritative — lean into it.

### Rule 4: Delete every "Actionable Takeaway" box
AI loves bolded callout boxes. They break flow and patronize readers. The content itself should be the takeaway.

### Rule 5: Humanize the metadata too
Meta titles and descriptions get overlooked. They need the same treatment as body copy — no "unlock the secrets" or "discover proven strategies."

---

## Scoring Adjustments

*Calibration notes from user feedback on scoring accuracy.*

### Baseline: Unedited AI blog posts score 2-3/10
First calibration run confirmed that raw Claude/GPT output on a generic blog topic (no voice samples, no brand context) lands at 2/10 overall. This is the floor. Anything scoring below 4 needs a full rewrite, not edits.
