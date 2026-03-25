#!/usr/bin/env python3
"""
CRO Hypothesis Agent
Acts as an automated landing page auditor.
Takes an HTML structure (scraped or provided) and evaluates it against
the GTM context to generate a structured "CRO Sprint Report" with testing ideas.
"""
import os
import sys
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

def safe_generate(prompt: str, retries: int = 5, timeout: int = 150):
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
            time.sleep(60)
            # Switch to flash if pro is consistently rate limited
            if attempt == 1:
                 print("      🔄 Switching to gemini-2.5-flash to bypass quota issues...")
                 model = genai.GenerativeModel('gemini-2.5-flash')

    raise Exception("Max retries reached for Gemini API")

class CROHypothesisAgent:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        
        load_dotenv(os.path.join(self.workspace_root, ".env"))
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env.")
            sys.exit(1)
        genai.configure(api_key=api_key)
        
        self.commands_dir = os.path.join(self.workspace_root, "commands")
        self.output_dir = os.path.join(self.workspace_root, "docs", "cro_reports")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.context = {}

    def load_context(self):
        """Loads required Markdown files from the commands/ directory."""
        print("📥 Loading strategic context...")
        files_to_load = {
            "icp": "core/ideal_customer_profile.md",
            "messaging": "identity/messaging_pillars.md",
            "gtm_goals": "ops/gtm_launch_playbook.md"
        }
        
        for key, rel_path in files_to_load.items():
            full_path = os.path.join(self.commands_dir, rel_path)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    self.context[key] = f.read()
            except FileNotFoundError:
                print(f"⚠️ Warning: Could not find {full_path}. Using empty context.")
                self.context[key] = f"No context provided for {key}."

    def generate_hypothesis(self, target_url: str, html_content_mock: str):
        """Uses Gemini to audit the page and generate a CRO report."""
        print(f"🕵️  Generating CRO Hypothesis Report for: {target_url}...")
        
        prompt = f"""
        You are an elite Conversion Rate Optimization (CRO) Specialist.
        
        CONTEXT:
        Ideal Customer Profile:
        {self.context.get('icp')}
        
        Messaging Pillars:
        {self.context.get('messaging')}
        
        GTM Launch Goals (Friction Removal):
        {self.context.get('gtm_goals')}
        
        PAGE TO AUDIT:
        URL: {target_url}
        Page Content / HTML Structure:
        ---
        {html_content_mock}
        ---
        
        TASK:
        Generate a "CRO Sprint Report" suggesting specific structural, copy, or design A/B tests to improve the 7-day free trial conversion rate on this page.
        
        FORMAT YOUR RESPONSE AS STRICT MARKDOWN:
        ### CRO Audit: {target_url}
        
        #### 1. Friction Analysis
        [Identify 2-3 specific areas where the page messaging, layout, or CTA creates friction based on the GTM context.]
        
        #### 2. Optimization Hypotheses (A/B Tests)
        [Provide 3 structured hypotheses looking like this:
        - **If we change...** (the specific variable)
        - **Then...** (the expected outcome in user behavior)
        - **Because...** (the strategic rationale tied to the ICP/Messaging)]
        
        #### 3. Recommended Copy Rewrites
        [Provide specific "Change X to Y" copy recommendations for the H1 or primary CTA.]
        """
        
        raw_markdown = safe_generate(prompt)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_url = target_url.replace("https://", "").replace("http://", "").replace("/", "_").replace(".", "_")
        output_file = os.path.join(self.output_dir, f"cro_sprint_report_{safe_url}_{timestamp}.md")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(raw_markdown.strip())
            
        print(f"✅ Saved CRO Sprint Report to: {output_file}")

    def run(self):
        self.load_context()
        print("\n--- Starting CRO Hypothesis Agent ---")
        
        # Mock HTML Content for testing the implementation
        mock_html = '''
        <header>
            <h1>Marketing Automation Software</h1>
            <h2>Do more with your ads. Start free today.</h2>
            <button>Sign Up</button>
        </header>
        <section class="features">
            <ul>
                <li>Google Ads integration</li>
                <li>Meta reports</li>
            </ul>
        </section>
        '''
        
        self.generate_hypothesis(target_url="https://tldr.tech/signup", html_content_mock=mock_html)
        print("--- CRO Hypothesis Agent Complete ---\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))
    
    agent = CROHypothesisAgent(workspace_root=project_root)
    agent.run()
