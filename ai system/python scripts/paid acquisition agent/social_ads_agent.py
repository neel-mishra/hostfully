#!/usr/bin/env python3
"""
Social Ads Visual Concept & Copy Agent
Ideates scroll-stopping ad creatives, generating primary text, headlines, 
and specific visual design prompts for social platforms based on core brand documents.
"""
import os
import sys
import time
import signal
import json
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

class SocialAdsAgent:
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
        self.market_saturation_json = os.path.join(
            self.workspace_root,
            "docs",
            "context_repository",
            "paid_ads",
            "winning_angles",
            "market_saturation_summary_mar2026_onward.json",
        )
        
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
        strict = self._read_text_if_exists(
            os.path.join(self.winning_angles_dir, "strict_winners_mar2026_onward.md")
        )
        signal_rows = []
        if os.path.exists(self.signals_jsonl):
            with open(self.signals_jsonl, "r", encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if i >= 30:
                        break
                    try:
                        signal_rows.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        saturation = {}
        if os.path.exists(self.market_saturation_json):
            try:
                with open(self.market_saturation_json, "r", encoding="utf-8") as f:
                    saturation = json.load(f)
            except json.JSONDecodeError:
                saturation = {}
        return {"top10": top10, "strict": strict, "signals": signal_rows, "saturation": saturation}

    def _saturation_training_notes(self, training: dict) -> str:
        sat = training.get("saturation") or {}
        idx = sat.get("angle_saturation_index") or {}
        thr = float(sat.get("saturation_threshold_high") or 0.7)
        pen = float(sat.get("saturation_penalty_weight") or 0.25)
        lines = [
            "",
            "## Hostfully training notes (competitor saturation)",
            "",
            f"High-saturation threshold reference: **{thr:.2f}** (index ≥ 1.0 means at/above normalized crowding). "
            f"Saturation penalty weight in system config: **{pen:.2f}**.",
            "",
        ]
        hot = [(k, float(v)) for k, v in idx.items() if float(v) >= 1.0]
        hot.sort(key=lambda x: -x[1])
        if not hot:
            lines.append(
                "_No angle families flagged at or above saturation index 1.0 in the latest market summary._"
            )
        else:
            lines.append("**Deprioritize or label as exploration** when leaning into these crowded competitor angles "
                         "(unless strict winners show Hostfully outperformance):**")
            lines.append("")
            for fam, score in hot[:12]:
                lines.append(f"- `{fam}` — saturation index **{score:.3f}**")
        lines.append("")
        return "\n".join(lines)

    def load_context(self):
        """Loads required Markdown files from the commands/ directory."""
        print("📥 Loading strategic context...")
        files_to_load = {
            "icp": "core/ideal_customer_profile.md",
            "messaging": "identity/messaging_pillars.md",
            "creative_direction": "identity/creative_direction.md"
        }
        
        for key, rel_path in files_to_load.items():
            full_path = os.path.join(self.commands_dir, rel_path)
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    self.context[key] = f.read()
            except FileNotFoundError:
                print(f"⚠️ Warning: Could not find {full_path}. Using empty context.")
                self.context[key] = f"No context provided for {key}."

    def generate_ad_concepts(self, platform: str = "Meta", angles: int = 3):
        """Uses Gemini to generate social ad concepts combining copy and visual prompts."""
        print(f"✍️  Generating AI Ad Concepts for {platform}...")
        training = self._load_training_context()
        signal_preview = "\n".join(
            [
                f"- {r.get('platform')} | {r.get('entity_type')} | blended={r.get('blended_score')} | text={str(r.get('entity_text',''))[:120]}"
                for r in training["signals"][:10]
            ]
        )
        saturation_preview = json.dumps(training.get("saturation", {}), indent=2)[:2000]
        
        prompt = f"""
        You are an elite Performance Creative Strategist and Copywriter for Meta/LinkedIn Ads.
        
        CONTEXT:
        Ideal Customer Profile:
        {self.context.get('icp')}
        
        Messaging Pillars:
        {self.context.get('messaging')}
        
        Creative Direction & Brand Visuals:
        {self.context.get('creative_direction')}

        HISTORICAL WINNING CONTEXT (Hostfully, Mar 2026 onward):
        Top reusable angles:
        {training['top10']}

        Strict winners:
        {training['strict']}

        Structured signal preview:
        {signal_preview}

        Market saturation constraint:
        {saturation_preview}
        
        TASK:
        Generate {angles} distinct Ad Concepts for {platform}.
        Each concept should target a different angle (e.g., FOMO, Ops Relief, ROI Focus) based on the ICP.
        Use this policy:
        - 80% of concepts should be built from proven winner primitives in the context above.
        - 20% can be controlled exploration variants.
        - Deprioritize heavily saturated competitor angles unless strict winners indicate clear Hostfully outperformance.
        
        For each concept, provide:
        ### Concept [Number]: [Angle Name]
        **Target Audience:** [Specific segment of the ICP]
        **Saturation note:** [One line: either "Clear lane" or "Exploration — angle is crowded in competitor data" with angle name]
        **Visual Generation Prompt (for Midjourney/Designer):** [Highly detailed, spatial description incorporating the brand colors and creative direction.]
        **Primary Text (Body Copy):** [Persuasive, engaging, hook-driven. Use emojis if platform appropriate.]
        **Headline:** [Short, punchy, below 40 chars]
        **CTA:** [Specific Call to Action]
        
        Format the entire response in clean Markdown. Avoid using introductory or concluding fluff text.
        """
        
        raw_markdown = safe_generate(prompt)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"social_ads_concepts_{platform.lower()}_{timestamp}.md")
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(raw_markdown.strip())
            f.write(self._saturation_training_notes(training))
            
        print(f"✅ Saved Social Ads Concepts to: {output_file}")

    def run(self):
        self.load_context()
        print("\n--- Starting Social Ads Agent ---")
        self.generate_ad_concepts(platform="Meta", angles=3)
        print("--- Social Ads Agent Complete ---\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))
    
    agent = SocialAdsAgent(workspace_root=project_root)
    agent.run()
