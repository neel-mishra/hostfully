# TLDR Weekly Content Review — 2026-05-11

**Generated:** Monday, May 11, 2026
**Pipeline source:** `outputs/docs/competitor content tracker/blogs/content_pipeline.csv`
**Blog output directory:** `outputs/docs/blogs/2026-05-11/`
**Google Docs:** Unavailable (GOOGLE_CLIENT_ID not configured). Review saved locally.

---

## Blog Posts Generated

| # | Title | Humanizer Score (Before → After) | Rewrite Status | Word Count |
|---|-------|----------------------------------|----------------|------------|
| 1 | Why Your Emails Are Going to Gmail's Promotions Tab | 2/10 → 8/10 | Full rewrite | 853 |
| 2 | How To Build a Fanbase: From Followers to True Fans | 2/10 → 8/10 | Full rewrite | 745 |
| 3 | Milk Road: From 0 to Acquisition in 10 Months | 2/10 → 8/10 | Full rewrite | 824 |

**Source articles (from pipeline, sorted by Weighted_Score):**
1. "Why Your Emails Are Going to Gmail's Promotions" (Score: 2.6) — competitor ref: beehiiv.com
2. "How To Build a Fanbase: From Followers to True Fans" (Score: 2.2) — competitor ref: beehiiv.com
3. "Milk Road: From 0 to Acquisition in 10 months" (Score: 2.2) — competitor ref: beehiiv.com

---

## Humanizer Report

**Average score after rewrite:** 8/10 across all dimensions
**Posts needing full rewrite:** 3 of 3 (100%)
**Posts passing threshold (7+):** 3 of 3 after rewrite

### Score Breakdown by Dimension

| Dimension | Avg Before | Avg After | Change |
|-----------|-----------|-----------|--------|
| AI Likeness | 2.0 | 8.0 | +6.0 |
| Authenticity | 1.3 | 8.0 | +6.7 |
| Reader Value | 3.0 | 8.0 | +5.0 |
| Domain Credibility | 2.0 | 8.0 | +6.0 |

### Common AI Patterns Detected and Fixed

- **Throat-Clear Openings** — "In today's crowded digital landscape..." / "The journey from a nascent idea..." / "When your carefully crafted emails land..."
- **Hedge Clusters** — "It is crucial to reiterate," "It is important to recognize," "It is essential to understand"
- **Adverb Stacks** — "meticulously," "significantly," "fundamentally," "remarkably," "exceedingly"
- **Enthusiastic Adjectives** — "sophisticated," "robust," "comprehensive," "powerful"
- **Actionable Takeaway Boxes** — Present in all 3 posts; all deleted
- **Identical Paragraph Shapes** — Uniform 3-4 sentence paragraphs throughout
- **Diplomatic Tone** — No opinions taken in any original draft
- **Bloat** — Average 60% word count reduction across all 3 posts
- **Meta Description Voice Bleed** — "Discover why..." / "Discover actionable strategies..."
- **Excessive keyword repetition** — Milk Road post had "acquisition" 25+ times

### Note on Humanizer Execution

The Anthropic (Claude) API returned `400: credit balance too low` during the blog writer's built-in Phase 4 humanizer. All 3 posts were humanized via the Cursor agent humanizer skill instead. The Gemini-based repurpose_agent.py was also bypassed for the same reason.

---

## Repurposing Kit Summary

| Blog Post | LinkedIn Posts | Twitter Threads | Email Subjects | Newsletter Blurbs | Exec Summaries | SEO Meta |
|-----------|---------------|-----------------|----------------|-------------------|----------------|----------|
| Gmail Promotions | 3 (Insight, Data, Story) | 1 (8 tweets) | 5 | 1 | 1 | 1 |
| Build a Fanbase | 3 (Insight, Data, Story) | 1 (8 tweets) | 5 | 1 | 1 | 1 |
| Milk Road | 3 (Insight, Data, Story) | 1 (8 tweets) | 5 | 1 | 1 | 1 |
| **Totals** | **9** | **3 (24 tweets)** | **15** | **3** | **3** | **3** |

---

## Video Scripts

| Blog Post | Script Title | Hook |
|-----------|-------------|------|
| Gmail Promotions | Why Your Emails Land in Gmail Promotions | "Your emails aren't going to spam. They're going to Promotions. There's a massive difference." |
| Build a Fanbase | How To Build a Fanbase (Not Just a Following) | "You don't need a million followers. You need a thousand fans." |
| Milk Road | How Milk Road Sold for 7 Figures in 10 Months | "Zero subscribers to a seven-figure acquisition. Ten months. Here's the actual playbook." |

Each video script includes: 60s format, visual + audio direction for every scene, and 3 alternative hooks for A/B testing.

---

## File Paths to All Generated Assets

### Blog Posts (humanized)
- `outputs/docs/blogs/2026-05-11/Why-Your-Emails-Are-Going-to-Gmails-Promotions.md`
- `outputs/docs/blogs/2026-05-11/How-To-Build-a-Fanbase-From-Followers-to-True-Fans.md`
- `outputs/docs/blogs/2026-05-11/Milk-Road-From-0-to-Acquisition-in-10-months.md`

### Repurposing Kits
- `outputs/docs/content_assets/repurposed/why-your-emails-are-going-to-gmails-promoti_2026-05-11_kit.md`
- `outputs/docs/content_assets/repurposed/how-to-build-a-fanbase-from-followers-to-t_2026-05-11_kit.md`
- `outputs/docs/content_assets/repurposed/milk-road-from-0-to-acquisition-in-10-mon_2026-05-11_kit.md`

### Video Scripts
- `outputs/docs/content_assets/repurposed/video_script_gmail-promotions.md`
- `outputs/docs/content_assets/repurposed/video_script_build-a-fanbase.md`
- `outputs/docs/content_assets/repurposed/video_script_milk-road.md`

### Pipeline CSV (updated)
- `outputs/docs/competitor content tracker/blogs/content_pipeline.csv`

### This Review
- `outputs/docs/content_assets/weekly_review_2026-05-11.md`

---

## Execution Notes

- **Execution time:** Blog Writer Agent ran from 01:04 to 01:08 UTC (3.5 minutes for 3 posts)
- **SEO audit:** All 3 posts went through Gemini-based SEO audit/refine loops (2-3 iterations each)
- **Social Media Agent:** Skipped (path mismatch for blog directory in social_media_agent.py)
- **API issues:** Anthropic API out of credits; OpenRouter API key not available; Gemini API functional; Google Docs OAuth missing CLIENT_ID
- **Pipeline status:** 3 items moved from "Not Started" to "Completed" in content_pipeline.csv
- **Remaining pipeline items:** 8 "Not Started" items remaining for future runs
