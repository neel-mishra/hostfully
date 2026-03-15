#!/usr/bin/env python3
"""
Landing Page Generator Agent
Synthesizes ad copy hooks and overarching strategic context to build 
high-converting landing page markdown wireframes (Hero, Trust, PAS, CTA).
"""
import os
import sys
import time
import glob
import signal
from datetime import datetime

from dotenv import load_dotenv
import google.generativeai as genai

class TimeoutException(Exception):
    pass

def _timeout_handler(signum, frame):
    raise TimeoutException("API timeout")

signal.signal(signal.SIGALRM, _timeout_handler)

def safe_generate(prompt: str, retries: int = 5, timeout: int = 150):
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

class LandingPageAgent:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        
        load_dotenv(os.path.join(self.workspace_root, ".env"))
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env.")
            sys.exit(1)
        genai.configure(api_key=api_key)
        
        self.commands_dir = os.path.join(self.workspace_root, "commands")
        self.ads_dir = os.path.join(self.workspace_root, "docs", "paid_ads_assets")
        self.output_dir = os.path.join(self.workspace_root, "docs", "landing_pages")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.context = {}

    def load_context(self):
        """Loads required Markdown files from the commands/ directory."""
        print("📥 Loading strategic context...")
        files_to_load = {
            "icp": "core/ideal_customer_profile.md",
            "messaging": "identity/messaging_pillars.md"
        }
        
        for key, rel_path in files_to_load.items():
            full_path = os.path.join(self.commands_dir, rel_path)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    self.context[key] = f.read()
            except FileNotFoundError:
                print(f"⚠️ Warning: Could not find {full_path}. Using empty context.")
                self.context[key] = f"No context provided for {key}."

    def load_latest_ad_assets(self) -> str:
        """Finds the most recent Search and Social ad outputs to maintain message scent."""
        print("📥 Loading latest ad assets for message scent...")
        ad_context = ""
        
        # Latest Search Ads CSV
        search_files = glob.glob(os.path.join(self.ads_dir, "search_ads_copy_*.csv"))
        if search_files:
            latest_search = max(search_files, key=os.path.getctime)
            with open(latest_search, "r", encoding="utf-8") as f:
                ad_context += "\n--- LATEST SEARCH ADS COPY ---\n" + f.read()[:1000] # Limit size
                
        # Latest Social Ads MD
        social_files = glob.glob(os.path.join(self.ads_dir, "social_ads_concepts_*.md"))
        if social_files:
            latest_social = max(social_files, key=os.path.getctime)
            with open(latest_social, "r", encoding="utf-8") as f:
                ad_context += "\n--- LATEST SOCIAL ADS COPY ---\n" + f.read()[:2000] # Limit size
                
        return ad_context

    def generate_landing_page(self, campaign_theme: str):
        """Uses Gemini to generate a structured markdown landing page."""
        print(f"🏗️  Drafting Landing Page for campaign: '{campaign_theme}'...")
        ad_assets = self.load_latest_ad_assets()
        
        prompt = f"""
        You are a master Conversion Rate Optimizer and direct-response Copywriter.
        
        CONTEXT:
        Ideal Customer Profile:
        {self.context.get('icp')}
        
        Messaging Pillars:
        {self.context.get('messaging')}
        
        ACTIVE AD CAMPAIGN ASSETS (Maintain strict message scent with these):
        {ad_assets}
        
        TASK:
        Generate a highly structured Markdown landing page wireframe for the '{campaign_theme}' campaign.
        Ensure seamless continuity from the ad hook to the landing page H1.
        
        STRUCTURE REQUIREMENT (Must include these sections):
        1. [Hero Section]: H1 (Value prop), H2 (Subheadline), Primary CTA button text.
        2. [Trust/Social Proof]: Logos to display or specific testimonial themes.
        3. [Problem/Agitation]: Remind them of the pain point highlighted in the ads.
        4. [Solution/Feature Map]: Use bullet points to map features to the desired outcome.
        5. [Final CTA]: A compelling closing argument and action button.
        
        Format entirely in Markdown. Do not include introductory notes or conversational filler.
        """
        
        raw_markdown = safe_generate(prompt)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_theme = campaign_theme.replace(" ", "_").lower()
        output_file = os.path.join(self.output_dir, f"landing_page_{safe_theme}_{timestamp}.md")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(raw_markdown.strip())
            
        print(f"✅ Saved Landing Page Wireframe to: {output_file}")

    def run(self):
        self.load_context()
        print("\n--- Starting Landing Page Generator Agent ---")
        self.generate_landing_page(campaign_theme="AI Marketing Hub")
        print("--- Landing Page Agent Complete ---\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))
    
    agent = LandingPageAgent(workspace_root=project_root)
    agent.run()
