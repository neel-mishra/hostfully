#!/usr/bin/env python3
"""
Outbound Sequence Strategist Agent
Builds multi-step cold email sequences tailored to specific outbound hypotheses.
Outputs plain-text sequences and explicit prompt templates for Clay enrichment.
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

class OutboundSequenceAgent:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        
        load_dotenv(os.path.join(self.workspace_root, ".env"))
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("❌ GEMINI_API_KEY not found in .env.")
            sys.exit(1)
        genai.configure(api_key=api_key)
        
        self.commands_dir = os.path.join(self.workspace_root, "commands")
        self.output_dir = os.path.join(self.workspace_root, "docs", "outbound_assets")
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.context = {}

    def load_context(self):
        """Loads required Markdown files from the commands/ directory."""
        print("📥 Loading strategic context...")
        files_to_load = {
            "icp": "core/ideal_customer_profile.md",
            "messaging": "identity/messaging_pillars.md",
            "voice": "identity/brand_voice_matrix.md"
        }
        
        for key, rel_path in files_to_load.items():
            full_path = os.path.join(self.commands_dir, rel_path)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    self.context[key] = f.read()
            except FileNotFoundError:
                print(f"⚠️ Warning: Could not find {full_path}. Using empty context.")
                self.context[key] = f"No context provided for {key}."

    def generate_sequence(self, campaign_hypothesis: str, target_persona: str):
        """Uses Gemini to generate a 3-step sequence and Clay enrichment prompts."""
        print(f"📧 Drafting sequence for: '{campaign_hypothesis}' -> Persona: {target_persona}")
        
        prompt = f"""
        You are an elite B2B Outbound Strategist and Cold Email Copywriter.
        
        CONTEXT:
        Ideal Customer Profile:
        {self.context.get('icp')}
        
        Messaging Pillars:
        {self.context.get('messaging')}
        
        Brand Voice:
        {self.context.get('voice')}
        
        CAMPAIGN TARGET:
        Persona: {target_persona}
        Hypothesis: {campaign_hypothesis}
        
        TASK:
        Generate a 3-step cold email sequence optimized for reply rate. 
        Email 1: The Hook & Agitation (Value led)
        Email 2: The Bump/Case Study (Social proof)
        Email 3: The Breakup/Hail Mary (Low friction CTA)
        
        RULES:
        - Write in plain-text. NO HTML formatting. Low capitalization. 
        - Keep emails extremely short (under 75 words).
        - Use conversational, non-salesy language.
        
        CRUCIAL - IN ADDITION TO THE EMAILS:
        You must write a "Clay AI Prompt" for Email 1. This prompt must instruct an AI enrichment tool 
        (like Clay) exactly how to research the prospect's LinkedIn or Company website to generate a hyper-personalized 
        opening line that transitions naturally into your Email 1 hook.
        
        FORMAT THE RESPONSE STRICTLY AS MARKDOWN:
        ### Campaign Overview
        [Brief summary]
        
        ### Clay AI Enrichment Prompt (For First Line Generation)
        ```prompt
        [Your detailed prompt here]
        ```
        
        ### Email 1
        Subject: [subject]
        [Body]
        
        ### Email 2
        Subject: [subject]
        [Body]
        
        ### Email 3
        Subject: [subject]
        [Body]
        """
        
        raw_markdown = safe_generate(prompt)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = campaign_hypothesis.replace(" ", "_").replace("/", "_").lower()
        output_file = os.path.join(self.output_dir, f"outbound_seq_{safe_name}_{timestamp}.md")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(raw_markdown.strip())
            
        print(f"✅ Saved Outbound Sequence to: {output_file}")

    def run(self):
        self.load_context()
        print("\n--- Starting Outbound Sequence Agent ---")
        self.generate_sequence(
            campaign_hypothesis="Recent hiring spree indicates growth chaos/ops debt",
            target_persona="VP of Marketing at B2B SaaS"
        )
        print("--- Outbound Agent Complete ---\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))
    
    agent = OutboundSequenceAgent(workspace_root=project_root)
    agent.run()
