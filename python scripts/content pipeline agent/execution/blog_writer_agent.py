import os
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import signal
import time
import google.generativeai as genai
from dotenv import load_dotenv
from pathlib import Path

class TimeoutException(Exception):
    pass

def _timeout_handler(signum, frame):
    raise TimeoutException("API timeout")

signal.signal(signal.SIGALRM, _timeout_handler)

def safe_generate(prompt, retries=5, timeout=120):
    """Wrapper to safely call Gemini with strict timeout and retries."""
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    for attempt in range(retries):
        try:
            # Prevent hitting the 15 RPM free tier limit consistently
            time.sleep(4)
            signal.alarm(timeout)
            response = model.generate_content(prompt)
            signal.alarm(0)
            return response
        except TimeoutException:
            signal.alarm(0)
            print(f"      ⚠️ API timeout on attempt {attempt+1}/{retries}")
            time.sleep(10)
        except Exception as e:
            signal.alarm(0)
            print(f"      ⚠️ API error on attempt {attempt+1}/{retries}: {e}")
            # If rate limit 429 is hit, wait longer than the 1-minute free tier window
            time.sleep(65)
    raise Exception("Max retries reached for Gemini API")

# Load environment variables from .env file in the Workspace Root
script_dir = os.path.dirname(os.path.abspath(__file__))
workspace_root = os.path.abspath(os.path.join(script_dir, "../../../"))
env_path = os.path.join(workspace_root, ".env")
if not os.path.exists(env_path):
    env_path = os.path.join(workspace_root, "../.env")
load_dotenv(env_path)

# Configuration
PIPELINE_CSV = "../../../docs/competitor content tracker/blogs/content_pipeline.csv"
BLOGS_DIR = "../../../docs/blogs/"
AGENTS_DIR = "../../../agents/"
CORE_CONTEXT_DIR = "../../../commands/core/"
IDENTITY_CONTEXT_DIR = "../../../commands/identity/"

# Max SEO audit iterations before publishing anyway
MAX_AUDIT_ITERATIONS = 3

# Files to EXCLUDE from context injection (brand-heavy, promotional)
CONTEXT_EXCLUSIONS = {
    "product_dna.md",
    "brand_voice_matrix.md",
    "messaging_pillars.md",
    "ad_copy_frameworks.md",
    "competitor_landscape.md",
    "creative_direction.md",
    "style_guide_internal.md",
    "style_guides.md",
}

# Initialize Gemini Client (Expects GEMINI_API_KEY in env)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize Anthropic (Claude) for Humanizer phase
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
CLAUDE_API_BASE = "https://api.anthropic.com/v1/messages"

# Humanizer skill file paths (relative to workspace root)
HUMANIZER_SKILL_DIR = os.path.join(workspace_root, ".cursor", "skills", "humanizer")
HUMANIZER_VOICE_SAMPLES = os.path.join(HUMANIZER_SKILL_DIR, "voice-samples.md")
HUMANIZER_PATTERNS = os.path.join(HUMANIZER_SKILL_DIR, "patterns.md")
BRAND_VOICE_MATRIX = os.path.join(workspace_root, "commands", "identity", "brand_voice_matrix.md")
MESSAGING_PILLARS = os.path.join(workspace_root, "commands", "identity", "messaging_pillars.md")


def claude_generate(prompt, max_tokens=8192, retries=3, timeout=180):
    """Call Claude API for humanizer rewriting."""
    if not ANTHROPIC_API_KEY:
        return None

    for attempt in range(retries):
        try:
            resp = requests.post(
                CLAUDE_API_BASE,
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=timeout,
            )
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
            if resp.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            print(f"      ⚠️ Claude API error {resp.status_code}: {resp.text[:200]}")
            time.sleep(5)
        except Exception as e:
            print(f"      ⚠️ Claude exception: {e}")
            time.sleep(10)
    return None


class BlogWriterAgent:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.pipeline_path = os.path.abspath(os.path.join(self.script_dir, PIPELINE_CSV))
        self.blogs_dir = os.path.abspath(os.path.join(self.script_dir, BLOGS_DIR))
        self.agents_dir = os.path.abspath(os.path.join(self.script_dir, AGENTS_DIR))

        # Ensure blogs dir exists
        if not os.path.exists(self.blogs_dir):
            os.makedirs(self.blogs_dir)

    def fetch_article_content(self, url):
        """Fetches the main content from the competitor's blog URL."""
        if not url or not url.startswith('http'):
            return "No valid URL provided."

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                article_body = soup.find('article') or soup.find('main') or soup.find('div', class_='content')
                if article_body:
                    text_content = article_body.get_text(separator='\n', strip=True)
                    return text_content[:5000]
                else:
                    return soup.get_text(separator='\n', strip=True)[:3000]
            else:
                return f"Failed to fetch content. Status code: {response.status_code}"
        except Exception as e:
            return f"Error fetching content: {e}"

    def load_agent_prompt(self, agent_filename):
        """Loads an agent markdown file and returns its content."""
        agent_path = os.path.join(self.agents_dir, agent_filename)
        if os.path.exists(agent_path):
            with open(agent_path, 'r') as f:
                return f.read()
        return ""

    def load_context(self):
        """Loads filtered context files — excludes brand-heavy promotional content."""
        context = ""

        # Load content-creator-agent persona (writing frameworks only)
        persona_path = os.path.join(self.agents_dir, "content-creator-agent.md")
        if os.path.exists(persona_path):
            with open(persona_path, 'r') as f:
                context += f"\n\n=== WRITING FRAMEWORKS ===\n{f.read()}"

        # Load Core Strategy (filtered)
        core_path = os.path.abspath(os.path.join(self.script_dir, CORE_CONTEXT_DIR))
        if os.path.exists(core_path):
            for file in os.listdir(core_path):
                if file.endswith(".md") and file not in CONTEXT_EXCLUSIONS:
                    with open(os.path.join(core_path, file), 'r') as f:
                        context += f"\n\n=== AUDIENCE CONTEXT: {file} ===\n{f.read()}"

        # Load Identity (filtered — most are excluded)
        identity_path = os.path.abspath(os.path.join(self.script_dir, IDENTITY_CONTEXT_DIR))
        if os.path.exists(identity_path):
            for file in os.listdir(identity_path):
                if file.endswith(".md") and file not in CONTEXT_EXCLUSIONS:
                    with open(os.path.join(identity_path, file), 'r') as f:
                        context += f"\n\n=== CONTEXT: {file} ===\n{f.read()}"

        return context

    # ------------------------------------------------------------------ #
    #  PHASE 1: SEO-Optimized Draft (seo-agent + copywriting-agent)
    # ------------------------------------------------------------------ #

    def generate_seo_draft(self, concept, title, context, reference_content=""):
        """
        Phase 1: Generate an SEO-optimized, brand-neutral blog draft.
        Uses prompts derived from seo-agent.md and copywriting-agent.md.
        """
        if not GEMINI_API_KEY:
            print("⚠️ GEMINI_API_KEY not found in environment variables.")
            return f"# {title}\n\n**Error**: GEMINI_API_KEY not found."

        system_prompt = """You are an expert SEO content strategist and performance marketing journalist.
You write authoritative, value-dense blog content as a NEUTRAL industry expert — similar to
publications like Search Engine Journal, MarketingProfs, or HubSpot Blog.

Your writing principles:
- Clarity over cleverness — simple language, no buzzwords
- Benefits over features — focus on reader outcomes and actionable takeaways
- Specificity over vagueness — use concrete data, real frameworks, specific numbers
- Active voice, confident tone — no hedging with "almost," "very," "really"
- One idea per section — each H2 should advance a single clear argument
- Show, don't tell — describe outcomes instead of using adverbs"""

        user_prompt = f"""**Task**: Write a complete, SEO-optimized blog post as a neutral industry publication.

**Title**: {title}
**Concept/Angle**: {concept}
**Date**: {datetime.now().strftime('%Y-%m-%d')}

**Audience Context** (use to understand WHO you're writing for, not to promote anything):
{context[:4000]}

**Competitor Reference** (use for structure and topic coverage only — do NOT copy):
{reference_content[:5000]}

**SEO Requirements**:
1. **H1**: Use the title as the single H1. Include the primary keyword.
2. **Heading Hierarchy**: Use H2 for major sections, H3 for subsections. No skipped levels.
3. **Keyword Placement**: Primary keyword must appear in the first 100 words and in at least 2 subheadings.
4. **Content Depth**: Write at least 1,200 words. Cover the topic comprehensively.
5. **Meta Tags**: End the article with an SEO metadata block:
   - Meta Title (50-60 characters, keyword near beginning)
   - Meta Description (150-160 characters, includes keyword, compelling reason to click)
   - Primary Keyword
6. **Internal Links**: Include at least 2 placeholder internal links like [Related: Topic Name](/blog/topic-slug)

**Writing Rules**:
1. Write as a neutral industry expert. Do NOT mention, promote, or reference any specific company, product, or brand as the author or publisher.
2. Do NOT include sales CTAs, product pitches, "get started" links, or self-promotional comparison tables.
3. Do NOT use phrases like "At [Company], we..." or "Our product..." or "Deploy your..."
4. The reader should extract pure value — actionable insights, data, frameworks — without feeling marketed to.
5. Use short paragraphs (2-3 sentences max), bullet points, and scannable formatting.
6. Include actionable takeaways the reader can implement immediately.

**Format**: Return strict Markdown. Start with the H1 heading."""

        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        try:
            response = safe_generate(full_prompt, retries=3, timeout=60)
            return response.text
        except Exception as e:
            return f"Error generating content via Gemini: {e}"

    # ------------------------------------------------------------------ #
    #  PHASE 2: SEO Audit (seo-audit-agent)
    # ------------------------------------------------------------------ #

    def audit_blog(self, draft, title):
        """
        Phase 2: Run an SEO audit on the generated blog draft.
        Returns a dict with 'pass' (bool), 'score' (int), and 'issues' (list).
        Uses criteria from seo-audit-agent.md.
        """
        if not GEMINI_API_KEY:
            return {"pass": True, "score": 0, "issues": []}

        audit_prompt = f"""You are an expert SEO auditor. Analyze the following blog post and evaluate it 
against these ON-PAGE SEO criteria. Return your evaluation as a JSON object.

**Blog Title**: {title}

**Blog Content**:
{draft}

**Evaluation Checklist** — For each check, mark as PASS or FAIL with a brief explanation:

1. **h1_tag**: Exactly one H1 heading that contains the primary keyword
2. **heading_hierarchy**: Logical H1 → H2 → H3 structure with no skipped levels
3. **keyword_first_100**: Primary keyword appears within the first 100 words
4. **content_depth**: Article is at least 1,200 words with comprehensive topic coverage
5. **meta_title**: SEO metadata section includes a meta title of 50-60 characters with keyword near beginning
6. **meta_description**: SEO metadata section includes a meta description of 150-160 characters with keyword
7. **internal_links**: At least 2 internal link placeholders present
8. **no_brand_promotion**: Zero mentions of any specific company or product as the author/publisher. No sales CTAs or product pitches.
9. **readability**: Short paragraphs, scannable subheadings, no jargon. Professional but accessible.
10. **actionable_value**: Contains actionable takeaways the reader can implement

**Response Format**: Return ONLY valid JSON, no markdown fencing, no explanation outside the JSON:
{{
  "pass": true/false,
  "score": <number 1-10>,
  "issues": [
    {{"check": "check_name", "status": "PASS|FAIL", "detail": "brief explanation"}}
  ]
}}

Set "pass" to true ONLY if ALL checks are PASS. The "score" should reflect overall SEO quality (10 = perfect)."""

        try:
            response = safe_generate(audit_prompt, retries=2, timeout=45)
            raw_text = response.text.strip()

            # Strip markdown code fences if present
            if raw_text.startswith("```"):
                raw_text = raw_text.split("\n", 1)[1] if "\n" in raw_text else raw_text[3:]
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3]
            raw_text = raw_text.strip()

            result = json.loads(raw_text)
            return result
        except (json.JSONDecodeError, Exception) as e:
            print(f"   ⚠️ Audit parse error: {e}. Treating as pass.")
            return {"pass": True, "score": 5, "issues": []}

    # ------------------------------------------------------------------ #
    #  PHASE 3: Refinement Loop
    # ------------------------------------------------------------------ #

    def refine_blog(self, draft, audit_result):
        """
        Phase 3: Refine the blog draft based on SEO audit findings.
        Takes the original draft + audit issues and returns a corrected version.
        """
        if not GEMINI_API_KEY:
            return draft

        issues_text = "\n".join(
            [f"- **{issue['check']}** [{issue['status']}]: {issue['detail']}"
             for issue in audit_result.get("issues", [])
             if issue.get("status") == "FAIL"]
        )

        refine_prompt = f"""You are an expert SEO content editor. A blog post has been audited and issues were found.
Your job is to fix EVERY issue listed below while preserving the quality and substance of the content.

**SEO Audit Issues to Fix**:
{issues_text}

**Original Blog Draft**:
{draft}

**Instructions**:
1. Fix every FAIL issue listed above.
2. Do NOT change sections that already pass the audit.
3. Do NOT add any company names, product names, brand mentions, or sales CTAs.
4. Maintain the neutral, expert journalist tone throughout.
5. Return the COMPLETE corrected blog in Markdown format.
6. Ensure the final article has proper SEO metadata at the end (Meta Title, Meta Description, Primary Keyword).

Return ONLY the corrected blog content in Markdown. No explanations or commentary."""

        try:
            response = safe_generate(refine_prompt, retries=2, timeout=60)
            return response.text
        except Exception as e:
            print(f"   ⚠️ Refinement error: {e}. Keeping original draft.")
            return draft

    # ------------------------------------------------------------------ #
    #  PHASE 4: Humanizer (Claude — score, diagnose, rewrite)
    # ------------------------------------------------------------------ #

    def _load_file_safe(self, path, max_chars=None):
        """Read a file if it exists, return empty string otherwise."""
        try:
            text = Path(path).read_text(encoding="utf-8")
            return text[:max_chars] if max_chars else text
        except (FileNotFoundError, OSError):
            return ""

    def humanize_draft(self, draft, title):
        """
        Phase 4: Run the humanizer skill against the draft.
        Scores on 4 dimensions, diagnoses AI patterns, rewrites.
        Uses Claude API with full humanizer skill context.
        """
        if not ANTHROPIC_API_KEY:
            print("      ⚠️ ANTHROPIC_API_KEY not set — skipping humanizer.")
            return draft, None

        voice_samples = self._load_file_safe(HUMANIZER_VOICE_SAMPLES, 3000)
        patterns = self._load_file_safe(HUMANIZER_PATTERNS, 5000)
        brand_voice = self._load_file_safe(BRAND_VOICE_MATRIX, 3000)
        pillars = self._load_file_safe(MESSAGING_PILLARS, 2000)

        if not patterns:
            print("      ⚠️ Humanizer patterns file not found — skipping humanizer.")
            return draft, None

        prompt = f"""You are the TLDR Humanizer — a copy editor that catches and fixes AI-sounding writing.

VOICE SAMPLES (match this rhythm, tone, and density):
{voice_samples}

AI PATTERNS TO DETECT AND KILL:
{patterns}

BRAND VOICE RULES:
{brand_voice}

MESSAGING CONTEXT:
{pillars}

DRAFT TO HUMANIZE:
{draft}

INSTRUCTIONS — follow this exact workflow:

STEP 1: SCORE the draft on four dimensions (1-10 each):
- AI Likeness: 1=obviously AI, 10=indistinguishable from human
- Authenticity: 1=generic voice, 10=sounds exactly like TLDR
- Reader Value: 1=fluff and filler, 10=every sentence earns its place
- Domain Credibility: 1=surface-level, 10=insider knowledge with specific data

STEP 2: DIAGNOSE — flag specific AI patterns from the patterns list. For each, cite the exact quote and state the fix.

STEP 3: REWRITE the entire draft applying all fixes:
- Match the voice samples — sentence length, rhythm, how paragraphs open
- Apply brand voice: concise, trustworthy, sharp. Not terse, not preachy
- Kill every flagged pattern
- Preserve all facts, data, and arguments — rewrite packaging, not payload
- Shorter is better — cut sentences that add nothing
- Lead with the interesting thing, not setup
- One idea per sentence
- Use TLDR's own data where relevant (48% open rates, 7M+ subscribers, 12 newsletters)
- Target 40-60% word count reduction from the original
- Humanize the meta title and description too

STEP 4: SHOW SCORES — output before and after scores.

OUTPUT FORMAT — return EXACTLY this structure:

===SCORES_BEFORE===
AI_LIKENESS: X
AUTHENTICITY: X
READER_VALUE: X
DOMAIN_CREDIBILITY: X
===END_SCORES_BEFORE===

===DIAGNOSIS===
[pattern flags — keep brief, 1-2 lines each]
===END_DIAGNOSIS===

===REWRITTEN_DRAFT===
[the full rewritten blog post in markdown, including meta tags]
===END_REWRITTEN_DRAFT===

===SCORES_AFTER===
AI_LIKENESS: X
AUTHENTICITY: X
READER_VALUE: X
DOMAIN_CREDIBILITY: X
===END_SCORES_AFTER==="""

        result = claude_generate(prompt, max_tokens=8192)
        if not result:
            print("      ⚠️ Humanizer call failed — keeping audit-refined draft.")
            return draft, None

        rewritten = self._extract_section(result, "===REWRITTEN_DRAFT===", "===END_REWRITTEN_DRAFT===")
        if not rewritten or len(rewritten.strip()) < 200:
            print("      ⚠️ Humanizer returned empty/short rewrite — keeping audit-refined draft.")
            return draft, result

        scores_before = self._extract_section(result, "===SCORES_BEFORE===", "===END_SCORES_BEFORE===")
        scores_after = self._extract_section(result, "===SCORES_AFTER===", "===END_SCORES_AFTER===")
        diagnosis = self._extract_section(result, "===DIAGNOSIS===", "===END_DIAGNOSIS===")

        if scores_before and scores_after:
            print(f"      📊 Before: {self._format_scores(scores_before)}")
            print(f"      📊 After:  {self._format_scores(scores_after)}")

        if diagnosis:
            diag_lines = [l.strip() for l in diagnosis.strip().split("\n") if l.strip()]
            print(f"      🔍 Diagnosed {len(diag_lines)} AI pattern(s)")

        original_words = len(draft.split())
        rewritten_words = len(rewritten.split())
        reduction = round((1 - rewritten_words / original_words) * 100) if original_words > 0 else 0
        print(f"      ✂️  {original_words} → {rewritten_words} words ({reduction}% reduction)")

        return rewritten.strip(), result

    @staticmethod
    def _extract_section(text, start_marker, end_marker):
        """Extract content between two markers."""
        try:
            start = text.index(start_marker) + len(start_marker)
            end = text.index(end_marker)
            return text[start:end].strip()
        except ValueError:
            return ""

    @staticmethod
    def _format_scores(scores_text):
        """Format score block into a compact one-liner."""
        parts = []
        for line in scores_text.strip().split("\n"):
            line = line.strip()
            if ":" in line:
                key, val = line.split(":", 1)
                short_key = key.strip().replace("_", " ").title()
                parts.append(f"{short_key}={val.strip()}")
        return " | ".join(parts) if parts else scores_text.strip()

    # ------------------------------------------------------------------ #
    #  Orchestration: Draft → Audit → Refine → Humanize → Publish
    # ------------------------------------------------------------------ #

    def run(self):
        print("🚀 Blog Writer Agent Starting (SEO Multi-Agent Pipeline)...")

        if not os.path.exists(self.pipeline_path):
            print(f"⚠️ Pipeline CSV not found at {self.pipeline_path}")
            return

        try:
            df = pd.read_csv(self.pipeline_path)

            # Filter: Status == 'Not Started', Sort: Weighted_Score DESC
            candidates = df[df['Status'] == 'Not Started'].sort_values(by='Weighted_Score', ascending=False)

            if candidates.empty:
                print("✨ No pending articles to write.")
                return

            # Take top 3
            to_process = candidates.head(3)
            print(f"📝 Found {len(to_process)} articles to draft.")

            # Load filtered context (brand-heavy files excluded)
            full_context = self.load_context()

            # Create date-based subfolder
            run_date = datetime.now().strftime('%Y-%m-%d')
            date_dir = os.path.join(self.blogs_dir, run_date)
            if not os.path.exists(date_dir):
                os.makedirs(date_dir)

            # Process each article through the 3-phase pipeline
            for index, row in to_process.iterrows():
                title = str(row['Article Title'])
                concept = row['Concept']
                url = row['Competitor URL']

                # Create safe filename
                safe_title = "".join([c if c.isalnum() or c in (' ', '-') else "" for c in title]).strip().replace(' ', '-')
                safe_title = safe_title[:60].strip('-')
                filename = f"{safe_title}.md"
                filepath = os.path.join(date_dir, filename)

                print(f"\n{'='*60}")
                print(f"📄 Processing: {title}")
                print(f"{'='*60}")

                # --- PHASE 1: SEO Draft ---
                print(f"   ✍️  Phase 1: Generating SEO-optimized draft...")
                print(f"   Fetching reference content from: {url}")
                reference_content = self.fetch_article_content(url)
                draft = self.generate_seo_draft(concept, title, full_context, reference_content)

                if draft.startswith("Error") or draft.startswith("# " + title[:10] + "\n\n**Error**"):
                    print(f"   ❌ Draft generation failed. Skipping.")
                    continue

                # --- PHASE 2 & 3: Audit → Refine Loop ---
                for attempt in range(1, MAX_AUDIT_ITERATIONS + 1):
                    print(f"   🔍 Phase 2: SEO Audit (attempt {attempt}/{MAX_AUDIT_ITERATIONS})...")
                    audit_result = self.audit_blog(draft, title)

                    score = audit_result.get("score", "?")
                    passed = audit_result.get("pass", False)
                    issues = [i for i in audit_result.get("issues", []) if i.get("status") == "FAIL"]

                    print(f"      Score: {score}/10 | Issues: {len(issues)}")

                    if passed:
                        print(f"   ✅ Passed SEO audit on attempt {attempt}!")
                        break

                    # Print failing checks
                    for issue in issues:
                        print(f"      ❌ {issue['check']}: {issue.get('detail', '')}")

                    if attempt < MAX_AUDIT_ITERATIONS:
                        print(f"   🔄 Phase 3: Refining draft to fix {len(issues)} issues...")
                        draft = self.refine_blog(draft, audit_result)
                    else:
                        print(f"   ⚠️  Max iterations reached. Publishing best version.")

                # --- PHASE 4: Humanizer ---
                print(f"   🧠 Phase 4: Humanizing draft (Claude)...")
                draft, humanizer_raw = self.humanize_draft(draft, title)
                if humanizer_raw:
                    print(f"   ✅ Humanizer pass complete.")
                else:
                    print(f"   ⏭️  Humanizer skipped (no API key or skill files).")

                # --- Publish ---
                with open(filepath, 'w') as f:
                    f.write(draft)

                df.at[index, 'Status'] = 'Completed'
                print(f"   📁 Published to {filename}")

            # Save CSV
            df.to_csv(self.pipeline_path, index=False)
            print(f"\n💾 Pipeline CSV updated.")
            print("🏁 Blog Writer Agent Complete.")

        except Exception as e:
            print(f"❌ Blog Writer Agent Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    agent = BlogWriterAgent()
    agent.run()
