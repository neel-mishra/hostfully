import os
import requests
import json
from dotenv import load_dotenv

class VideoScriptAgent:
    def __init__(self):
        # Expectation: environment loaded by parent agent
        self.api_key = os.environ.get("OPENROUTER_API_KEY")

    def generate_script(self, copy_text: str, context: str) -> str | None:
        """
        Generates a 30-60s video script from the LinkedIn copy.
        Uses OpenRouter API. Handles 402/Credits errors gracefully by skipping.
        """
        if not self.api_key:
            print("   ⚠️ Video Script Skipped: OPENROUTER_API_KEY missing.")
            return None

        print("   🎬 Generating Video Script (via OpenRouter)...")

        prompt = f"""
        TASK: Convert the following LinkedIn post into a high-energy 60-second vertical video script (TikTok/Reels).
        
        SOURCE COPY:
        {copy_text}
        
        OUTPUT FORMAT (Markdown):
        # Video Script
        
        ## Hook (0-5s)
        - **Visual**: [Describe visual hook]
        - **Audio**: [Spoken hook]
        
        ## Body (Main Content)
        - [Scene 1]: [Visual / B-roll] | [Narration]
        - [Scene 2]: [Visual] | [Narration]
        
        ## Call to Action
        - **Visual**: [Text overlay]
        - **Audio**: [CTA]
        """

        try:
            # Using a reliable model via OpenRouter
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://antigravity.dev", # Optional
                    "X-Title": "Antigravity Content Agent"
                },
                data=json.dumps({
                    "model": "google/gemini-2.0-flash-001",
                    "messages": [{"role": "user", "content": prompt}]
                }),
                timeout=30
            )
            
            # 1. Handle Credits Error (The expected state for now)
            if response.status_code == 402:
                 print("      ⚠️ Video Script Skipped: Insufficient OpenRouter Credits (402).")
                 return None
            
            # 2. Handle Other API Errors
            if response.status_code != 200:
                print(f"      ⚠️ Video Script Skipped: API Error {response.status_code} - {response.text[:100]}...")
                return None
                
            # 3. Success
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                script = result['choices'][0]['message']['content']
                print("      ✅ Video Script Generated.")
                return script
            else:
                 print("      ⚠️ Video Script Skipped: Empty response.")
                 return None

        except Exception as e:
            print(f"      ⚠️ Video Script Skipped: Error {e}")
            return None
