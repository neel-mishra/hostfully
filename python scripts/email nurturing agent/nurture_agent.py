#!/usr/bin/env python3
"""
Nurture Agent — Generates email nurturing sequences using Gemini REST API.
Scrapes a landing page for facts, loads strategic context from agent files,
and drafts A/B variant emails for a Free -> Paid upsell campaign.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ---------------------------------------------------------------------------
# 1. Environment Setup
# ---------------------------------------------------------------------------

# Resolve the project root (two levels up from this script)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))

# Load .env from the project root (where .env actually lives)
from dotenv import load_dotenv
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("❌ GEMINI_API_KEY not found. Set it in your .env file at the project root.")
    sys.exit(1)

# Correct model name for the Gemini REST endpoint (2026 context)
# gemini-1.5 is gone. gemini-2.0 hit limits. Using 2.5-flash.
MODEL_NAME = "gemini-2.5-flash"

# Import the scraper (same directory)
sys.path.append(SCRIPT_DIR)
from landing_page_scraper import scrape_landing_page

# ---------------------------------------------------------------------------
# 2. Reusable HTTP Session (created once, used for all API calls)
# ---------------------------------------------------------------------------

def create_api_session():
    """Create a requests session with retry logic for Gemini API."""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=3,           # waits: 3s, 6s, 12s
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session

API_SESSION = create_api_session()

# ---------------------------------------------------------------------------
# 3. NurtureAgent Class
# ---------------------------------------------------------------------------

class NurtureAgent:
    def __init__(self, target_url):
        self.target_url = target_url
        self.context = {}
        self.strategy = {}

    # ---- Context Loading ---------------------------------------------------

    def load_context(self):
        """Scrape the landing page and load all strategic agent files."""
        # 1. Scrape Landing Page (Source of Truth)
        print(f"🕷️  Scraping {self.target_url}...")
        self.context["product_data"] = scrape_landing_page(self.target_url)

        if "error" in self.context["product_data"]:
            print(f"⚠️  Scraper warning: {self.context['product_data']['error']}")

        # 2. Load Strategic Agent Files
        agents_dir = os.path.join(BASE_DIR, "agents")
        identity_dir = os.path.join(BASE_DIR, "commands", "identity")

        self._load_file(os.path.join(agents_dir, "product", "product-strategy-agent.md"), "product_strategy")
        self._load_file(os.path.join(agents_dir, "product", "pricing-packaging-agent.md"), "pricing_strategy")
        self._load_file(os.path.join(identity_dir, "brand_voice_matrix.md"), "brand_voice",
                        fallback="Tone: Professional yet conversational.")
        self._load_file(os.path.join(agents_dir, "content", "email-sequence-agent.md"), "email_persona",
                        fallback="You are an expert email copywriter.")

        print(f"✅  Context loaded ({len(self.context)} sources)")

    def _load_file(self, path, key, fallback=None):
        """Safely read a file into self.context[key]."""
        try:
            with open(path, "r") as f:
                self.context[key] = f.read()
        except FileNotFoundError:
            if fallback:
                self.context[key] = fallback
                print(f"⚠️  {os.path.basename(path)} not found — using fallback.")
            else:
                print(f"❌  Missing required file: {path}")
                raise

    # ---- Sequence Strategy -------------------------------------------------

    def generate_sequence_strategy(self, source, goal):
        """Define the 6-email nurturing sequence structure."""
        self.strategy = {
            "source": source,
            "goal": goal,
            "emails": [
                {"day": 0, "type": "Welcome + Quick Win",  "focus": "Immediate Value"},
                {"day": 1, "type": "Getting Started",       "focus": "Core Feature Activation"},
                {"day": 3, "type": "Social Proof",          "focus": "Case Study / Success Story"},
                {"day": 5, "type": "Logic / Problem",       "focus": "Why Upgrade? (Pain Point)"},
                {"day": 7, "type": "Hard Offer",            "focus": "Incentivized Upgrade"},
                {"day": 10, "type": "Last Chance",          "focus": "Downsell / Urgency"},
            ],
        }

    # ---- Email Drafting (Gemini REST API) ----------------------------------

    def draft_email(self, email_meta, variant):
        """Call Gemini REST API to generate one email variant."""
        product_strat = self.context.get("product_strategy", "")[:1000]
        pricing_strat = self.context.get("pricing_strategy", "")[:1000]

        prompt = f"""
You are the Email Sequence Agent.

PERSONA:
{self.context.get('email_persona', '')}

BRAND VOICE:
{self.context.get('brand_voice', '')}

STRATEGIC FRAMEWORK (Style Only — Do NOT use specific data from here):
Product Strategy: {product_strat}
Pricing Strategy: {pricing_strat}

SOURCE OF TRUTH (Facts / Prices / Features — USE THIS DATA):
{json.dumps(self.context.get('product_data', {}), indent=2)}

TASK:
Draft Email #{email_meta['day']} for a '{self.strategy['source']} -> {self.strategy['goal']}' sequence.
Type: {email_meta['type']}
Focus: {email_meta['focus']}

VARIANT: {variant}
(Variant A = Standard approach. Variant B = Significantly different hook / subject line for A/B testing.)

CONSTRAINTS:
- Do NOT hallucinate features or prices absent from SOURCE OF TRUTH.
- Use the exact pricing from SOURCE OF TRUTH when mentioning price.
- Output strictly in Markdown format.
- Include a Subject Line at the top.
"""

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{MODEL_NAME}:generateContent?key={API_KEY}"
        )
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        try:
            # Rate-limit guard: ~5s between calls keeps us under 15 RPM free tier
            time.sleep(5)

            response = API_SESSION.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=90,
            )

            if response.status_code == 200:
                data = response.json()
                try:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
                except (KeyError, IndexError):
                    print(f"⚠️  Unexpected response shape: {json.dumps(data)[:200]}")
                    return "Error: unexpected API response structure."
            else:
                print(f"⚠️  API returned {response.status_code}")
                return f"API Error {response.status_code}: {response.text[:300]}"

        except requests.exceptions.Timeout:
            return "Error: API request timed out after 90s."
        except requests.exceptions.ConnectionError as e:
            return f"Error: Connection failed — {e}"
        except Exception as e:
            return f"Error generating email: {e}"

    # ---- Orchestration ------------------------------------------------------

    def run(self):
        """Main entry point: load context, generate all emails, save."""
        self.load_context()
        self.generate_sequence_strategy("Free User", "Paid Upgrade")

        docs_dir = os.path.join(BASE_DIR, "docs", "email", "free_user_upsell")
        os.makedirs(docs_dir, exist_ok=True)

        total = len(self.strategy["emails"])
        print(f"\n🚀 Starting Generation — {total} emails × 2 variants")
        print(f"   Target: {self.target_url}")
        print(f"   Output: {docs_dir}\n")

        for i, email in enumerate(self.strategy["emails"]):
            email_dir = os.path.join(docs_dir, f"email_{i + 1:02d}")
            os.makedirs(email_dir, exist_ok=True)

            # Variant A
            print(f"   [{i + 1}/{total}] Email {i + 1} ({email['type']}) — Variant A...", end=" ", flush=True)
            body_a = self.draft_email(email, "A")
            with open(os.path.join(email_dir, "variant_a.md"), "w") as f:
                f.write(body_a)
            print("✓")

            # Variant B
            print(f"   [{i + 1}/{total}] Email {i + 1} ({email['type']}) — Variant B...", end=" ", flush=True)
            body_b = self.draft_email(email, "B")
            with open(os.path.join(email_dir, "variant_b.md"), "w") as f:
                f.write(body_b)
            print("✓")

        print(f"\n✅ Sequence generated → {docs_dir}")


# ---------------------------------------------------------------------------
# 4. CLI Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python nurture_agent.py <landing_page_url>")
        sys.exit(1)

    agent = NurtureAgent(sys.argv[1])
    agent.run()
