#!/usr/bin/env python3
"""
Creative Direction Agent (Visuals & Design)
Translates written content or strategic concepts into explicit
art direction prompts for design teams or AI image generators.
"""
import os
import sys
import glob
import time
import signal
from datetime import datetime

from dotenv import load_dotenv
import google.generativeai as genai

class TimeoutException(Exception):
    pass

def _timeout_handler(signum, frame):
    raise TimeoutException("API timeout")

signal.signal(signal.SIGALRM, _timeout_handler)

def safe_generate(prompt: str, retries: int = 5, timeout: int = 120):
    model = genai.GenerativeModel('gemini-2.5-flash')
    for attempt in range(retries):
        try:
            time.sleep(4)
            signal.alarm(timeout)
            response = model.generate_content(prompt)
            signal.alarm(0)
            return response.text
        except TimeoutException:
            signal.alarm(0)
            print(f"      ⚠️ API timeout on attempt {attempt+1}/{retries}")
            time.sleep(10)
        except Exception as e:
            signal.alarm(0)
            print(f"      ⚠️ API error on attempt {attempt+1}/{retries}: {e}")
            time.sleep(65)
    raise Exception("Max retries reached for Gemini API")


class CreativeDirectionAgent:
    """
    Reads finalized content drafts and a brand visual identity file,
    then appends detailed image generation prompts to each asset.
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root

        load_dotenv(os.path.join(self.workspace_root, ".env"))
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env.")
            sys.exit(1)
        genai.configure(api_key=api_key)

        self.commands_dir = os.path.join(self.workspace_root, "commands")
        self.content_dirs = [
            os.path.join(self.workspace_root, "docs", "seo_pages"),
            os.path.join(self.workspace_root, "docs", "content_briefs"),
            os.path.join(self.workspace_root, "docs", "landing_pages"),
        ]
        self.output_dir = os.path.join(self.workspace_root, "docs", "creative_assets")
        os.makedirs(self.output_dir, exist_ok=True)

        self.context = {}

    def load_context(self):
        """Loads the brand visual identity and creative direction."""
        print("📥 Loading brand visual identity...")
        files_to_load = {
            "creative_direction": "identity/creative_direction.md",
            "style_guide": "identity/style_guides.md",
            "brand_voice": "identity/brand_voice_matrix.md",
        }
        for key, rel_path in files_to_load.items():
            full_path = os.path.join(self.commands_dir, rel_path)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    self.context[key] = f.read()
            except FileNotFoundError:
                print(f"⚠️ Warning: Could not find {full_path}.")
                self.context[key] = ""

    def find_content_files(self) -> list:
        """Discover recent .md content files to process."""
        files = []
        for d in self.content_dirs:
            if os.path.isdir(d):
                for md_file in glob.glob(os.path.join(d, "*.md")):
                    files.append(md_file)
        return sorted(files, key=os.path.getmtime, reverse=True)[:5]  # Process latest 5

    def generate_visual_prompts(self, content_path: str):
        """Analyzes a Markdown file and generates visual design prompts."""
        with open(content_path, "r", encoding="utf-8") as f:
            content_text = f.read()

        # Truncate very large files
        if len(content_text) > 4000:
            content_text = content_text[:4000] + "\n[...truncated...]"

        filename = os.path.basename(content_path)
        print(f"   🎨 Generating visual prompts for: {filename}")

        prompt = f"""
You are an elite Creative Director specializing in B2B SaaS marketing visuals.

BRAND VISUAL IDENTITY:
{self.context.get('creative_direction', '')}

STYLE GUIDE:
{self.context.get('style_guide', '')}

CONTENT TO VISUALIZE:
Filename: {filename}
---
{content_text}
---

TASK:
Analyze this content and generate 2-3 detailed image generation prompts (suitable for Midjourney or DALL-E).
Each prompt must:
1. Align with the brand visual identity above (colors, mood, style).
2. Be spatially descriptive (describe foreground, background, lighting, composition).
3. Include exact hex color codes from the style guide.
4. Specify the intended use (hero image, social thumbnail, inline illustration).

FORMAT:
### Visual Asset 1: [Intended Use]
**Prompt:** [Detailed generation prompt]
**Dimensions:** [Recommended aspect ratio]
**Notes:** [Any design constraints]

### Visual Asset 2: [Intended Use]
...
"""

        raw_md = safe_generate(prompt)

        # Save to creative assets directory
        safe_name = os.path.splitext(filename)[0]
        output_file = os.path.join(self.output_dir, f"visuals_{safe_name}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# Creative Direction: {filename}\n\n")
            f.write(f"**Source:** `{content_path}`\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(raw_md.strip())

        print(f"   ✅ Saved: {output_file}")

    def run(self):
        self.load_context()
        print("\n--- Starting Creative Direction Agent ---")

        content_files = self.find_content_files()
        if not content_files:
            print("   ⚠️ No content files found to process.")
            print("   Tip: Run the SEO, Ideation, or Landing Page agents first.")
        else:
            print(f"   📂 Found {len(content_files)} content files to process.")
            for f in content_files:
                self.generate_visual_prompts(f)
                time.sleep(2)

        print("--- Creative Direction Agent Complete ---\n")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))

    agent = CreativeDirectionAgent(workspace_root=project_root)
    agent.run()
