#!/usr/bin/env python3
"""
Content Ideation Agent (The "Pulse" Sensor)
Scrapes industry sources to identify trending topics, extract themes,
and generate content briefs (blog concepts + social hooks).
"""
import os
import sys
import csv
import time
import signal
from datetime import datetime

import requests
from bs4 import BeautifulSoup
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


class ContentIdeationAgent:
    """
    Monitors competitor/industry URLs to discover trending topics,
    then uses an LLM to transform those into actionable content briefs.
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
        self.output_dir = os.path.join(self.workspace_root, "docs", "content_briefs")
        self.tracker_path = os.path.join(self.output_dir, "ideation_tracker.csv")
        os.makedirs(self.output_dir, exist_ok=True)

        self.context = {}

    def load_context(self):
        """Loads strategic context files."""
        print("📥 Loading strategic context...")
        files_to_load = {
            "icp": "core/ideal_customer_profile.md",
            "messaging": "identity/messaging_pillars.md",
            "business": "core/business_context.md",
        }
        for key, rel_path in files_to_load.items():
            full_path = os.path.join(self.commands_dir, rel_path)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    self.context[key] = f.read()
            except FileNotFoundError:
                print(f"⚠️ Warning: Could not find {full_path}.")
                self.context[key] = ""

    def scrape_url(self, url: str) -> str:
        """Scrapes text content from a URL."""
        try:
            headers = {"User-Agent": "Mozilla/5.0 ContentIdeationBot/1.0"}
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")

            # Remove scripts/styles
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator="\n", strip=True)
            return text[:3000]  # Limit to avoid prompt bloat
        except Exception as e:
            print(f"   ⚠️ Failed to scrape {url}: {e}")
            return ""

    def scrape_sources(self, urls: list) -> str:
        """Scrape multiple URLs and concatenate their content."""
        all_content = []
        for url in urls:
            print(f"   🌐 Scraping: {url}")
            content = self.scrape_url(url)
            if content:
                all_content.append(f"--- SOURCE: {url} ---\n{content}\n")
        return "\n".join(all_content)

    def load_existing_ideas(self) -> set:
        """Load existing idea titles from tracker to prevent duplicates."""
        existing = set()
        if os.path.exists(self.tracker_path):
            with open(self.tracker_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing.add(row.get("title", "").strip().lower())
        return existing

    def generate_briefs(self, scraped_content: str):
        """Uses Gemini to produce blog concepts and social hooks from scraped content."""
        existing_ideas = self.load_existing_ideas()
        existing_str = ", ".join(list(existing_ideas)[:20]) if existing_ideas else "None yet."

        prompt = f"""
You are an expert Content Strategist for a B2B SaaS brand.

BUSINESS CONTEXT:
{self.context.get('business', '')}

IDEAL CUSTOMER PROFILE:
{self.context.get('icp', '')}

MESSAGING PILLARS:
{self.context.get('messaging', '')}

SCRAPED INDUSTRY/COMPETITOR CONTENT:
{scraped_content}

EXISTING IDEAS ALREADY GENERATED (avoid duplicates):
{existing_str}

TASK:
Based on the scraped content, generate:
1. **3 Blog Concepts** — each with a Title, Target Keyword, Brief (2-3 sentences), and Content Type (Listicle/How-To/Opinion/Case Study).
2. **5 Social Media Hooks** — each a single punchy sentence or question suitable for LinkedIn/Twitter, with a suggested visual concept.

FORMAT STRICTLY AS CSV (no markdown fences, no intro text):
Type,Title,Target Keyword,Brief,Visual Concept
blog,Title Here,keyword here,Brief description here,N/A
social,Hook text here,N/A,N/A,Visual idea here
"""

        print("✍️  Generating content briefs...")
        raw_csv = safe_generate(prompt)

        # Strip markdown fences if present
        if raw_csv.startswith("```"):
            raw_csv = "\n".join(raw_csv.split("\n")[1:-1])

        # Append to tracker
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        lines = raw_csv.strip().split("\n")

        file_exists = os.path.exists(self.tracker_path)
        with open(self.tracker_path, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write("date,type,title,target_keyword,brief,visual_concept\n")
            for line in lines:
                if line.startswith("Type,") or line.startswith("type,"):
                    continue  # skip header
                f.write(f"{timestamp},{line}\n")

        print(f"✅ Appended {len(lines)-1} briefs to: {self.tracker_path}")

    def run(self, source_urls: list = None):
        self.load_context()
        print("\n--- Starting Content Ideation Agent ---")

        if not source_urls:
            source_urls = [
                "https://blog.hubspot.com/marketing",
                "https://neilpatel.com/blog/",
            ]
            print("   ℹ️ No source URLs provided. Using defaults.")

        scraped = self.scrape_sources(source_urls)
        if scraped:
            self.generate_briefs(scraped)
        else:
            print("   ❌ No content scraped. Cannot generate briefs.")

        print("--- Content Ideation Agent Complete ---\n")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))

    agent = ContentIdeationAgent(workspace_root=project_root)
    agent.run()
