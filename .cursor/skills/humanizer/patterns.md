# AI Writing Patterns — Detection Guide

Known patterns that make copy sound AI-generated. Each pattern includes what to look for and how to fix it. This file is a living document — new patterns are added after each humanizer feedback cycle.

---

## Structural Patterns

### 1. The Throat-Clear Opening
**What it is:** Starting with setup instead of the point. "In today's rapidly evolving landscape..." or "When it comes to X, it's important to..."
**Fix:** Delete the first sentence. Start with the second one. If the second one is also throat-clearing, start with the third.

### 2. The Triple Structure
**What it is:** Everything in threes. Three benefits, three examples, three bullet points. Consistent triplicate grouping throughout.
**Fix:** Vary the count. Two is fine. Four is fine. One strong point beats three weak ones.

### 3. Symmetrical Headers
**What it is:** Headers that follow an unnaturally parallel structure. "The Power of X," "The Promise of Y," "The Potential of Z."
**Fix:** Make headers informational, not performative. Say what the section contains.

### 4. The Perfect Sandwich
**What it is:** Every paragraph follows intro → body → wrap-up. No paragraph is allowed to just... end after making its point.
**Fix:** Let paragraphs end abruptly when the point is made. Not everything needs a concluding sentence.

### 5. Excessive Subheading Density
**What it is:** A subheading every 2-3 sentences. Real writers use subheadings when the topic genuinely shifts, not every paragraph.
**Fix:** Merge related sections. Use transitions instead of headers. Let content flow.

---

## Transition Patterns

### 6. The Bridge Phrase
**What it is:** "But here's the thing," "And that's exactly why," "What's more," "That said," "Here's where it gets interesting." These are AI crutches for connecting paragraphs.
**Fix:** Often the transition isn't needed at all. Delete it. If the paragraphs connect logically, the reader doesn't need a bridge.

### 7. The Pivot Signal
**What it is:** "However," "Nevertheless," "On the flip side," "Conversely" — used mechanically rather than when there's a genuine contrast.
**Fix:** Use "but" when you mean "but." Save formal pivot words for actual argumentative turns.

### 8. The Summary Transition
**What it is:** "This means that..." or "In other words..." used to restate what was just said in slightly different words.
**Fix:** If you said it clearly the first time, don't say it again.

---

## Word Choice Patterns

### 9. The Adverb Stack
**What it is:** "Truly," "remarkably," "significantly," "fundamentally," "incredibly," "seamlessly" — intensifiers that add emphasis without information.
**Fix:** Delete the adverb. If the sentence is weaker without it, the sentence itself is weak — rewrite it.

### 10. The Abstract Noun
**What it is:** "Leverage," "utilize," "facilitate," "optimize," "streamline" — corporate verbs that mean nothing specific.
**Fix:** Use the concrete verb. "Use" not "leverage." "Speed up" not "streamline." "Help" not "facilitate."

### 11. The Hedge Cluster
**What it is:** "It's worth noting that," "It's important to remember," "One might argue," "It could be said that" — qualifiers that drain authority.
**Fix:** Just say the thing. If it's worth noting, note it. Don't announce that you're about to note it.

### 12. The Enthusiastic Adjective
**What it is:** "Powerful," "robust," "cutting-edge," "game-changing," "transformative," "innovative" — marketing adjectives that signal AI.
**Fix:** Replace with specific evidence. Not "powerful reporting" but "reporting that shows CPC, CTR, and attributed pipeline in one dashboard."

### 13. The Colon-List Combo
**What it is:** "There are several key benefits: efficiency, scalability, and reliability." AI loves introducing lists with colons.
**Fix:** Either make it a proper list (with bullets) or weave the items into prose. The colon-list is a neither-here-nor-there format.

---

## Paragraph Patterns

### 14. The Identical Paragraph Shape
**What it is:** Every paragraph is 3-4 sentences, roughly the same length. Human writing has rhythm — some paragraphs are one sentence, some are seven.
**Fix:** Vary paragraph length deliberately. A one-sentence paragraph hits hard. Use it.

### 15. The Comprehensive Treatment
**What it is:** AI tries to cover every angle of every point. Humans are selective — they go deep on what matters and skip what doesn't.
**Fix:** Cut the weakest 30% of points. Double down on the strongest ones.

### 16. The Diplomatic Tone
**What it is:** Never taking a strong position. "There are pros and cons to both approaches." "It depends on your specific needs."
**Fix:** Have an opinion. TLDR's voice is authoritative. Pick a side when the evidence supports it.

---

## Opening/Closing Patterns

### 17. The Question Opener
**What it is:** "Have you ever wondered...?" or "What if there was a way to...?" AI defaults to rhetorical questions as openers.
**Fix:** Start with a fact, a number, or a bold claim. TLDR leads with the news, not a question.

### 18. The Call-to-Action Closing
**What it is:** Every piece ends with "Ready to get started?" or "The future of X is here — are you ready?"
**Fix:** End with the last real point. The piece should feel complete, not like a sales pitch.

### 19. The Recap Closing
**What it is:** "In conclusion," "To sum up," "At the end of the day" — restating everything that was just said.
**Fix:** If the piece is short enough to read in one sitting (and it should be), no recap needed. End on the strongest point.

---

## TLDR-Specific Patterns

### 20. Wrong Side of the Network
**What it is:** Using advertiser language in reader-facing copy or vice versa. "ROI" in a newsletter blurb. "Curated" in a sales email.
**Fix:** Check `commands/identity/brand_voice_matrix.md` Section 3 for the right voice.

### 21. The Superlative Without Proof
**What it is:** "The best newsletter" instead of "The most-read daily tech newsletter — 1.6M subscribers."
**Fix:** Replace superlatives with specifics. Numbers, case studies, proof points from `commands/identity/messaging_pillars.md`.

---

## Content Patterns

### 22. The Placeholder Link
**What it is:** `[link to internal article on X]` or `[link to resource]` scattered throughout. AI generates these as structural filler — they signal "I'm a template, not a finished piece." Real writers either include the actual link or don't reference it at all.
**Fix:** Delete the placeholder entirely. If the reference matters, add the real link. If you don't have it, rewrite the sentence to stand on its own.

### 23. The Actionable Takeaway Box
**What it is:** A bolded "**Actionable Takeaway:**" callout after every section. AI does this to seem practical, but it breaks flow and patronizes the reader. The content itself should be actionable — you shouldn't need a separate box to extract the point.
**Fix:** Delete the takeaway box. Weave the action into the last sentence of the section. If the section doesn't naturally end with something actionable, the section itself might be fluff.

### 24. The Meta-Description Voice Bleed
**What it is:** The meta title and description sound just as AI as the body copy. "Unlock the secrets to..." or "Discover proven strategies for..." in the SEO metadata.
**Fix:** Write meta descriptions in the same voice as the rewritten body. Short, specific, no "unlock/discover/proven." TLDR style: state the fact, state the benefit.

### 25. The 2x Bloat Ratio
**What it is:** AI drafts are consistently 2-3x longer than they need to be. A point that needs one sentence gets three. A section that needs three bullets gets six. The piece feels comprehensive but reads as padded.
**Fix:** After rewriting, check word count. If the rewrite isn't at least 40% shorter than the original, you haven't cut enough.

---

*To add a new pattern: append it at the end of the relevant section with the next sequential number, following the same format (name, what it is, fix).*
