#!/usr/bin/env python3
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
        self.winning_angles_dir = os.path.join(
            self.workspace_root, "docs", "context_repository", "paid_ads", "winning_angles"
        )
        self.signals_jsonl = os.path.join(
            self.workspace_root, "outputs", "training_data", "paid_ads", "signals", "signals_latest.jsonl"
        )
        self.angle_priors_json = os.path.join(
            self.winning_angles_dir, "angle_priors_mar2026_onward.json"
        )
        self.search_weight_keyword_intent = 0.40
        self.search_weight_hist_ctr = 0.25
        self.search_weight_hist_conv = 0.35
        self.search_exploration_ratio = 0.20
        
        self.context = {}

    def _read_text_if_exists(self, path: str) -> str:
        if not os.path.exists(path):
            return ""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _load_training_context(self) -> dict:
        top10 = self._read_text_if_exists(
            os.path.join(self.winning_angles_dir, "top10_reusable_angles_mar2026_onward.md")
        )
        google_winners = self._read_text_if_exists(
            os.path.join(self.winning_angles_dir, "google_mar2026_onward.md")
        )
        signal_rows = []
        if os.path.exists(self.signals_jsonl):
            with open(self.signals_jsonl, "r", encoding="utf-8") as f:
                for line in f:
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if row.get("platform") == "google":
                        signal_rows.append(row)
                    if len(signal_rows) >= 30:
                        break
        priors = {}
        if os.path.exists(self.angle_priors_json):
            try:
                with open(self.angle_priors_json, "r", encoding="utf-8") as f:
                    priors = json.load(f)
            except json.JSONDecodeError:
                priors = {}
        return {
            "top10": top10,
            "google_winners": google_winners,
            "signals": signal_rows,
            "angle_priors": priors,
        }

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
        training = self._load_training_context()
        signal_preview = "\n".join(
            [
                f"- blended={r.get('blended_score')} conv={r.get('results_or_conversions')} ctr={r.get('ctr')} text={str(r.get('entity_text',''))[:90]}"
                for r in training["signals"][:10]
            ]
        )
        priors_preview = json.dumps(training.get("angle_priors") or {}, indent=2)[:3500]

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

        HISTORICAL WINNERS CONTEXT:
        {training['top10']}

        GOOGLE WINNERS DETAIL:
        {training['google_winners']}

        STRUCTURED SIGNAL PREVIEW:
        {signal_preview}

        ANGLE PRIORS (JSON from creative_mapping / winners — use for Angle Tag selection):
        {priors_preview}
        
        TASK:
        1. Cluster these keywords logically into Ad Groups.
        2. Write 3 Headlines and 2 Descriptions per Ad Group.
        3. Assign one **Angle Tag** per ad group from this closed set (pick the best fit):
           ops_relief, roi_proof, scale_story, integration_power, social_proof, offer_urgency, general_value.
        4. Use weighted strategy:
           - {self.search_weight_keyword_intent*100:.0f}% keyword intent
           - {self.search_weight_hist_ctr*100:.0f}% historical CTR signal
           - {self.search_weight_hist_conv*100:.0f}% historical conversion signal
           - Reserve ~{self.search_exploration_ratio*100:.0f}% of rows as explicit exploration (tag general_value or note in Keywords).
        5. At least 80% of ad groups should use angle tags that appear in the ANGLE PRIORS ranked_families top half when priors exist; otherwise lean on top10/google winners text.
        6. STRICT CONSTRAINTS:
           - Headlines MUST be 30 characters or less.
           - Descriptions MUST be 90 characters or less.
           - Do not use exclamation points in the headline.
           
        OUTPUT FORMAT:
        Return ONLY a properly formatted CSV. No markdown code blocks, no intro text.
        Headers exactly: Campaign,Ad Group,Angle Tag,Headline 1,Headline 2,Headline 3,Description 1,Description 2,Keywords
        """
        print("✍️  Generating AI Ad Copy based on strategic constraints...")
        raw_csv = safe_generate(prompt)
        
        # Strip potential markdown fences
        if raw_csv.startswith("```"):
            raw_csv = "\n".join(raw_csv.split("\n")[1:-1])
            
        output_file = os.path.join(self.output_dir, f"search_ads_copy_{int(time.time())}.csv")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(raw_csv.strip())
        # Basic constraints sanity check for downstream QA.
        try:
            import io
            r = csv.DictReader(io.StringIO(raw_csv.strip()))
            for row in r:
                if not (row.get("Angle Tag") or "").strip():
                    print(f"   ⚠️ Missing Angle Tag for ad group {row.get('Ad Group')}")
                for h in ("Headline 1", "Headline 2", "Headline 3"):
                    if len((row.get(h) or "").strip()) > 30:
                        print(f"   ⚠️ Constraint warning: {h} exceeds 30 chars in ad group {row.get('Ad Group')}")
                for d in ("Description 1", "Description 2"):
                    if len((row.get(d) or "").strip()) > 90:
                        print(f"   ⚠️ Constraint warning: {d} exceeds 90 chars in ad group {row.get('Ad Group')}")
        except Exception:
            pass
            
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
