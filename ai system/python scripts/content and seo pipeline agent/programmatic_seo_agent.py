#!/usr/bin/env python3
"""
Programmatic SEO Page Generator Agent
A generic engine for automating the creation of highly structured,
bottom-of-funnel SEO pages at scale based on dynamic templates.
"""
import os
import sys
import csv
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


class ProgrammaticSEOAgent:
    """
    Reads a CSV of target entities (competitors, integrations, features)
    and a Markdown template to mass-produce SEO-optimized pages.
    """

    DEFAULT_TEMPLATE = """
# {entity_name} — {page_type}

## Overview
[Provide a detailed, factual overview of {entity_name} as it relates to our product.]

## Key Comparison Points
| Feature | Our Product | {entity_name} |
|---------|-------------|----------------|
| [Feature 1] | ✅ | ❌ |
| [Feature 2] | ✅ | ⚠️ |

## Why Choose Us Over {entity_name}
[3 compelling, data-backed reasons.]

## Migration Guide
[Step-by-step instructions for switching from {entity_name}.]

## FAQ
[3-5 frequently asked questions about {entity_name} vs our product.]
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
        self.output_dir = os.path.join(self.workspace_root, "docs", "seo_pages")
        os.makedirs(self.output_dir, exist_ok=True)

        self.context = {}

    def load_context(self):
        """Loads the business context and product DNA for grounding."""
        print("📥 Loading strategic context...")
        files_to_load = {
            "business": "core/business_context.md",
            "product": "core/product_dna.md",
            "competitors": "core/competitor_landscape.md",
        }
        for key, rel_path in files_to_load.items():
            full_path = os.path.join(self.commands_dir, rel_path)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    self.context[key] = f.read()
            except FileNotFoundError:
                print(f"⚠️ Warning: Could not find {full_path}.")
                self.context[key] = ""

    def load_entities(self, csv_path: str) -> list:
        """Reads the CSV of target entities."""
        entities = []
        try:
            with open(csv_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    entities.append(row)
        except FileNotFoundError:
            print(f"❌ Entity CSV not found: {csv_path}")
        return entities

    def generate_page(self, entity: dict, template: str = None):
        """Generates a single SEO page for the given entity."""
        entity_name = entity.get("name", "Unknown")
        page_type = entity.get("type", "Comparison")

        if template is None:
            template = self.DEFAULT_TEMPLATE

        prompt = f"""
You are an expert SEO Copywriter and content strategist.

BUSINESS CONTEXT:
{self.context.get('business', '')}

PRODUCT CONTEXT:
{self.context.get('product', '')}

COMPETITOR LANDSCAPE:
{self.context.get('competitors', '')}

TARGET ENTITY: {entity_name}
PAGE TYPE: {page_type}

TEMPLATE TO FOLLOW:
{template}

TASK:
Fill in the template above for the entity "{entity_name}".
- Write factual, authoritative content. Do not hallucinate product features.
- Add a compelling meta title (under 60 chars) and meta description (under 155 chars) at the top.
- Ensure every heading uses proper H2/H3 hierarchy.
- Write for a marketing professional audience.
- Format: clean Markdown only. No intro fluff.
"""
        print(f"   ✍️ Generating SEO page: {entity_name} ({page_type})...")
        raw_md = safe_generate(prompt)

        safe_name = entity_name.replace(" ", "_").replace("/", "_").lower()
        output_file = os.path.join(self.output_dir, f"seo_{page_type.lower()}_{safe_name}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(raw_md.strip())
        print(f"   ✅ Saved: {output_file}")

    def run(self, csv_path: str = None):
        self.load_context()
        print("\n--- Starting Programmatic SEO Agent ---")

        if csv_path and os.path.exists(csv_path):
            entities = self.load_entities(csv_path)
        else:
            # Default demo entities when no CSV is provided
            entities = [
                {"name": "HubSpot Marketing Hub", "type": "comparison"},
                {"name": "Shopify", "type": "integration"},
            ]
            print("   ℹ️ No entity CSV provided. Using demo entities.")

        for entity in entities:
            self.generate_page(entity)
            time.sleep(2)

        print("--- Programmatic SEO Agent Complete ---\n")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))

    csv_arg = sys.argv[1] if len(sys.argv) > 1 else None
    agent = ProgrammaticSEOAgent(workspace_root=project_root)
    agent.run(csv_path=csv_arg)
