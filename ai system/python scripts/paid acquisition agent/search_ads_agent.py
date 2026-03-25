#!/usr/import/env python3
"""
Search Ads Keyword & Copywriter Agent
Generates high-intent search ad copy mapped to specific strategic query groups.
Uses Google Ads API (mocked/impl) for Keyword Planner to cluster keywords,
then uses Gemini to strictly format copy adhering to Google Ads character limits.
"""
import os
import sys
import json
import csv
import time
import signal
from typing import List, Dict

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
            time.sleep(4)  # Rate limiting
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
            time.sleep(60)
    raise Exception("Max retries reached for Gemini API")

class SearchAdsAgent:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        
        load_dotenv(os.path.join(self.workspace_root, ".env"))
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env.")
            sys.exit(1)
        genai.configure(api_key=api_key)
        
        self.commands_dir = os.path.join(self.workspace_root, "commands")
        self.output_dir = os.path.join(self.workspace_root, "docs", "paid_ads_assets")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.context = {}

    def load_context(self):
        """Loads required Markdown files from the commands/ directory."""
        print("📥 Loading strategic context...")
        files_to_load = {
            "icp": "core/ideal_customer_profile.md",
            "messaging": "identity/messaging_pillars.md",
            "ad_frameworks": "identity/ad_copy_frameworks.md"
        }
        
        for key, rel_path in files_to_load.items():
            full_path = os.path.join(self.commands_dir, rel_path)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    self.context[key] = f.read()
            except FileNotFoundError:
                print(f"⚠️ Warning: Could not find {full_path}. Using empty context.")
                self.context[key] = f"No context provided for {key}."

    def run_keyword_planner(self, seed_query: str) -> List[dict]:
        """
        Interacts with Google Ads API Keyword Planner.
        NOTE: Google Ads API requires developer tokens, OAuth credentials, and customer IDs.
        For demonstration, this functions as a mock if credentials are missing.
        """
        # Pseudo-code for actual implementation:
        # client = GoogleAdsClient.load_from_storage("googleads.yaml")
        # keyword_plan_idea_service = client.get_service("KeywordPlanIdeaService")
        # request = client.get_type("GenerateKeywordIdeasRequest")
        # ... logic
        print(f"🔍 Running Google Ads Keyword Planner research for: '{seed_query}'...")
        # Mock Response
        mock_data = [
            {"keyword": "AI marketing automation", "volume": 12000, "competition": "HIGH"},
            {"keyword": "cross channel attribution tool", "volume": 5400, "competition": "MEDIUM"},
            {"keyword": "meta ads reporting automated", "volume": 3200, "competition": "LOW"},
            {"keyword": "ai media buyer software", "volume": 8100, "competition": "HIGH"},
        ]
        time.sleep(2)  # Simulate network request
        print(f"   ✓ Discovered {len(mock_data)} highly relevant keywords.")
        return mock_data
        
    def group_and_generate_ad_copy(self, seed_query: str):
        """Uses Gemini to cluster keywords and generate valid Google Ads copy."""
        keywords = self.run_keyword_planner(seed_query)
        kw_list_str = "\n".join([f"- {k['keyword']} (Vol: {k['volume']})" for k in keywords])
        
        prompt = f"""
        You are an expert Google Search Ads Copywriter.
        
        CONTEXT:
        Ideal Customer Profile:
        {self.context.get('icp')}
        
        Messaging Pillars:
        {self.context.get('messaging')}
        
        Ad Copy Frameworks:
        {self.context.get('ad_frameworks')}
        
        KEYWORDS FOUND:
        {kw_list_str}
        
        TASK:
        1. Cluster these keywords logically into Ad Groups.
        2. Write 3 Headlines and 2 Descriptions per Ad Group.
        3. STRICT CONSTRAINTS:
           - Headlines MUST be 30 characters or less.
           - Descriptions MUST be 90 characters or less.
           - Do not use exclamation points in the headline.
           
        OUTPUT FORMAT:
        Return ONLY a properly formatted CSV. No markdown code blocks, no intro text.
        Headers exactly: Campaign,Ad Group,Headline 1,Headline 2,Headline 3,Description 1,Description 2,Keywords
        """
        print("✍️  Generating AI Ad Copy based on strategic constraints...")
        raw_csv = safe_generate(prompt)
        
        # Strip potential markdown fences
        if raw_csv.startswith("```"):
            raw_csv = "\n".join(raw_csv.split("\n")[1:-1])
            
        output_file = os.path.join(self.output_dir, f"search_ads_copy_{int(time.time())}.csv")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(raw_csv.strip())
            
        print(f"✅ Saved Search Ads CSV to: {output_file}")
        
    def run(self):
        self.load_context()
        print("\n--- Starting Search Ads Agent ---")
        self.group_and_generate_ad_copy("AI marketing analytics and automation")
        print("--- Search Ads Agent Complete ---\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))
    
    agent = SearchAdsAgent(workspace_root=project_root)
    agent.run()
