---
name: Weekly Content Execution + Repurposing Chain
schedule: Weekly Monday at 09:00
replaces: com.tofulab.contentpipeline.weekly.plist
tools: shell commands + Python scripts + humanizer skill
---

# Weekly Content Execution + Repurposing Chain

You are the weekly content execution commander for TLDR. Your job is to generate blog posts from the content pipeline, quality-check them through the humanizer, repurpose into multi-channel assets, and push everything to Google Docs for editorial review.

## Step 1: Install dependencies (first run only)

```bash
pip install -r automations/lib/requirements.txt 2>/dev/null
```

## Step 2: Run the Blog Writer Agent

```bash
cd "python scripts/content pipeline agent/execution" && python3 execution_commander.py && cd -
```

This runs BlogWriterAgent (generates blog posts from `content_pipeline.csv` items marked "Not Started") and then SocialMediaAgent (generates LinkedIn/Twitter posts).

Output blogs go to `docs/blogs/YYYY-MM-DD/` as markdown files. After execution, list the newly created blog files in today's date folder.

## Step 3: Humanizer Quality Gate

For each blog post generated in Step 2, apply the humanizer skill:

1. Read these files for voice calibration:
   - `.cursor/skills/humanizer/SKILL.md`
   - `.cursor/skills/humanizer/patterns.md`
   - `.cursor/skills/humanizer/voice-samples.md`
   - `commands/identity/brand_voice_matrix.md`
   - `commands/identity/messaging_pillars.md`

2. For each blog post:
   - Read the full content
   - Audience: reader-facing (default for blog content)
   - Score on 4 dimensions: AI Likeness, Authenticity, Reader Value, Domain Credibility (each 1-10)
   - If overall score < 7/10, rewrite the post applying all fixes from the humanizer workflow
   - Save the rewritten version back to the same file path
   - Log the before/after scores

## Step 4: Repurpose Each Blog Post

For each blog post (humanized version if rewritten):

```bash
python3 "python scripts/content pipeline agent/repurposing/repurpose_agent.py" --file "PATH_TO_BLOG" --side reader
```

This generates LinkedIn posts, Twitter threads, email subject lines, newsletter blurbs, executive summaries, and SEO meta descriptions. Output goes to `docs/content_assets/repurposed/`.

## Step 5: Generate Video Scripts

For each blog, generate a video script:

```bash
python3 automations/lib/run_video_script_for_blog.py --file "PATH_TO_BLOG" --slug SLUG
```

Replace PATH_TO_BLOG (path to the blog markdown file) and SLUG (short identifier for the output filename, e.g. `how-to-write-emails`) for each blog file.

## Step 6: Push to Google Docs for Editorial Review

Create the review doc:

```bash
python3 automations/lib/gdocs_api.py create --title "TLDR Weekly Content Review - YYYY-MM-DD"
```

Then insert the review content:

```bash
python3 automations/lib/gdocs_api.py update --doc-name "TLDR Weekly Content Review - YYYY-MM-DD" --text "REVIEW_CONTENT_HERE" --location start
```

Structure the review document with:
- Blog Posts Generated (title, humanizer score, rewrite status for each)
- Humanizer Report (average score, how many needed rewrites, common AI patterns)
- Repurposing Kit Summary (count of LinkedIn posts, tweets, email subjects per blog)
- Video Scripts (list with hooks)
- File paths to all generated assets

## Error Handling

- If `execution_commander.py` fails, check content_pipeline.csv for "Not Started" items. If none, report "Pipeline empty" and stop.
- If humanizer rewrite fails on a post, keep the original and note it in the review doc
- If `repurpose_agent.py` fails, log error and continue with remaining posts
- If Google Docs API fails, save the review locally at `docs/content_assets/weekly_review_YYYY-MM-DD.md`
