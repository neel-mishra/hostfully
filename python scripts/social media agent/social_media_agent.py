import os
import glob
import json
import time
from datetime import datetime
from typing import List, Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
load_dotenv(dotenv_path=os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../.env")))

# Configure Gemini
API_KEY = os.getenv('GEMINI_API_KEY')
if not API_KEY:
    # Fallback: check persistent context or user env? 
    # For now assume it's in .env or raises error
    print("⚠️ GEMINI_API_KEY not found in .env. Attempting to use default from env var.")
    API_KEY = os.environ.get('GEMINI_API_KEY')

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment")

genai.configure(api_key=API_KEY)

# Constants
MODEL_NAME = "gemini-flash-latest" 
DOCS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../docs"))
BLOGS_DIR = os.path.join(DOCS_DIR, "blogs")
SOCIAL_DIR = os.path.join(DOCS_DIR, "social media")
AGENTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../agents"))
IDENTITY_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../commands/identity"))

import sys
# Add visual generators (images and videos) to path
VISUAL_GEN_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../visual generators"))
sys.path.append(os.path.join(VISUAL_GEN_DIR, "images"))
sys.path.append(os.path.join(VISUAL_GEN_DIR, "videos"))

try:
    from generate_image import generate_image # type: ignore
except ImportError:
    generate_image = None
    print("⚠️ Could not import generate_image. Visuals will be skipped.")

try:
    from video_script_agent import VideoScriptAgent # type: ignore
except ImportError:
    VideoScriptAgent = None
    print("⚠️ Could not import VideoScriptAgent.")

# Verify Keys (Masked)
def check_keys():
    gemini_key = os.environ.get("GEMINI_API_KEY")
    router_key = os.environ.get("OPENROUTER_API_KEY")
    print(f"🔑 Keys Loaded: Gemini={'Yes' if gemini_key else 'No'}, OpenRouter={'Yes' if router_key else 'No'}")

class SocialMediaAgent:
    def __init__(self):
        check_keys()
        self.model = genai.GenerativeModel(MODEL_NAME)
        if VideoScriptAgent:
            self.video_agent = VideoScriptAgent()
        else:
            self.video_agent = None

    def load_context(self) -> str:
        """Loads agent personas and identity."""
        context = []
        
        # Load Social Media Agent & Content Creator Agent
        for agent_file in ["social-media-agent.md", "content-creator-agent.md"]:
            path = os.path.join(AGENTS_DIR, agent_file)
            if os.path.exists(path):
                with open(path, "r") as f:
                    context.append(f"=== {agent_file} ===\n{f.read()}\n")
        
        # Load Creative Direction for Visuals
        creative_path = os.path.join(IDENTITY_DIR, "creative_direction.md")
        if os.path.exists(creative_path):
             with open(creative_path, "r") as f:
                    context.append(f"=== creative_direction.md ===\n{f.read()}\n")

        return "\n".join(context)

    def get_week_number(self, date: datetime) -> int:
        """
        Returns week number (1-4) based on the first Monday of the month.
        Constraint: Week number maxes out at 4.
        """
        # Find the first day of the month
        first_day = date.replace(day=1)
        
        # Find first Monday (0=Monday, 6=Sunday)
        while first_day.weekday() != 0:
            first_day = first_day.replace(day=first_day.day + 1)
            
        # If current date is before first Monday, it's week 1 (technically week 0 but we map to 1)
        if date < first_day:
            return 1

        # Calculate weeks elapsed since first Monday
        delta = date - first_day
        week_num = (delta.days // 7) + 1
        
        # Clamp to max 4 as requested
        return min(week_num, 4)

    def get_day_prefix(self, day: str) -> str:
        """prefix day with number for sorting: 1. Monday..."""
        mapping = {
            "Monday": "1. Monday",
            "Tuesday": "2. Tuesday",
            "Wednesday": "3. Wednesday",
            "Thursday": "4. Thursday",
            "Friday": "5. Friday"
        }
        return mapping.get(day, day)

    def load_weekly_blogs(self) -> List[Dict[str, str]]:
        """Loads the 3 most recently created blog posts."""
        if not os.path.exists(BLOGS_DIR):
            print(f"⚠️ Blogs directory not found: {BLOGS_DIR}")
            return []
            
        all_blogs = glob.glob(os.path.join(BLOGS_DIR, "**", "*.md"), recursive=True)
        
        if not all_blogs:
            print("⚠️ No blog files found.")
            return []
            
        # Sort by creation time (newest first)
        all_blogs.sort(key=os.path.getctime, reverse=True)
        
        # Take top 3
        recent_blogs = all_blogs[:3] # type: ignore
        
        loaded_blogs = []
        for blog_path in recent_blogs:
            with open(blog_path, "r") as f:
                content = f.read()
                filename = str(os.path.basename(blog_path))
                loaded_blogs.append({"title": filename, "content": content})
                
        return loaded_blogs

    def audit_visual(self, image_path: str, creative_guidelines: str) -> str | None:
        """
        Audits the generated image against brand guidelines using Gemini Vision.
        Returns: None if passed, or a feedback string if failed.
        """
        print(f"   🔍 Auditing visual: {os.path.basename(image_path)}")
        
        try:
            # Load image for Gemini
            image_file = genai.upload_file(image_path)
            
            prompt = f"""
            Act as the Brand Director. Review this image against our Creative Direction:
            
            {creative_guidelines}
            
            Does this image ALIGN with the guidelines? (Colors, Mood, Minimalism)
            If YES, output only "PASS".
            If NO, output "FAIL: [Specific feedback to fix the image]".
            """
            
            audit_model = genai.GenerativeModel("gemini-1.5-flash-latest")
            response = audit_model.generate_content([prompt, image_file])
            result = response.text.strip()
            
            if "PASS" in result:
                print("      ✅ Image passed audit.")
                return None # type: ignore
            else:
                feedback = result.replace("FAIL:", "").strip()
                print(f"      ❌ Image failed audit: {feedback}")
                return feedback
                
        except Exception as e:
            print(f"      ⚠️  Audit failed (error): {e}")
            return None # Assume pass if audit breaks to avoid loops

    def generate_visual_for_post(self, prompt: str, output_path: str, context: str):
        """Generates visual, audits it, and retries once if needed."""
        if not generate_image:
            print("   ⚠️ Nano Banana (generate_image) not available.")
            return

        # extract creative direction from context for audit
        creative_direction = ""
        if "=== creative_direction.md ===" in context:
             creative_direction = context.split("=== creative_direction.md ===")[1].split("===")[0]

        print(f"   🎨 Generating visual...")
        try:
            # Attempt 1
            generate_image(prompt=prompt, output_path=output_path)
            
            # Audit
            if os.path.exists(output_path) and creative_direction:
                feedback = self.audit_visual(output_path, creative_direction)
                
                # Retry if failed
                if feedback:
                    print(f"   🔄 Retrying visual with feedback...")
                    new_prompt = f"{prompt}. IMPORTANT CORRECTION: {feedback}"
                    generate_image(prompt=new_prompt, output_path=output_path)
                    print(f"      ✅ Retry complete.")
                    
        except ValueError as e:
            print(f"   ⚠️ Visual generation skipped: {e}")
        except Exception as e:
            print(f"   ❌ Visual generation error: {e}")

    def generate_plan(self, blogs: List[Dict[str, str]], context: str) -> List[Dict[str, Any]]:
        """
        Analyzes 3 blogs and generates a 5-day social media plan (JSON).
        Aggregator Strategy: Maps blogs to Mon-Fri slots based on 5-Day Omni strategy.
        """
        if not blogs:
            print("❌ No blogs found to process.")
            return []

        blog_summaries = ""
        for i, blog in enumerate(blogs):
             # Truncate content to avoid token limits, prioritizing the beginning
             content_snippet = blog['content'][:5000] 
             blog_summaries += f"--- BLOG {i+1}: {blog['title']} ---\n{content_snippet}\n...\n\n"

        prompt = f"""
        {context}

        # TASK: Create a 5-Day Social Media Pack (LinkedIn) based on the following 3 Blogs.
        
        ## INPUT BLOGS (The Source Material)
        {blog_summaries}

        ## STRATEGY: The 5-Day Omni-Content (Aggregator Mode)
        You are the Strategic Editor. Your goal is to weave these 3 blogs into a cohesive week of content.
        Do NOT just post links. Extract the core value. 
        You must decide how to distribute the insights from the 3 blogs across the 5 days.
        You can dedicate a day to one blog, or synthesize multiple blogs into one post.
        
        **The Schedule Archetypes:**
        1. **Monday (The Breakdown)**: Educational framework. Explain a core concept.
        2. **Tuesday (The Contrarian)**: Engagement hook. Use a strong opinion or counter-narrative.
        3. **Wednesday (The Story)**: Social proof. Share a case study or story.
        4. **Thursday (The List)**: Saves/Utility. Aggregate tools/tips/mistakes.
        5. **Friday (The Insight)**: Thought Leadership. Future trends/predictions.

        ## OUTPUT FORMAT (JSON ONLY)
        Return a valid JSON array of 5 objects. Each object must have:
        - "day": "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
        - "archetype": "The Breakdown", etc.
        - "reasoning": Why you chose this source content for this day.
        - "copy": The full LinkedIn post text (hooks, body, call to action). Use formatted text with line breaks.
        - "visual_prompt": A detailed prompt for an AI image generator to create a minimal, premium, on-brand visual.
        """
        
        print("🧠 Generating 5-day social strategy...")
        response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        
        try:
            return json.loads(response.text)
        except Exception as e:
            print(f"❌ Error parsing JSON response: {e}")
            # print(response.text) # Debug only
            return []

    def save_pack(self, plan: List[Dict[str, Any]], context: str): # Context needed for audit
        """Saves the planned posts to the folder structure."""
        if not plan: return

        # 1. Determine Folder Name: [Month] Week [N] (1-4)
        now = datetime.now()
        month_name = now.strftime("%B")
        week_num = self.get_week_number(now)
        folder_name = f"{month_name} Week {week_num}"
        
        week_dir = os.path.join(SOCIAL_DIR, folder_name)
        if not os.path.exists(week_dir):
            os.makedirs(week_dir)
            
        print(f"📂 Saving social pack to: {week_dir}")

        # 2. Save each day
        for post in plan:
            day = post.get("day", "Unknown")
            day_folder_name = self.get_day_prefix(day)
            
            day_dir = os.path.join(week_dir, day_folder_name)
            if not os.path.exists(day_dir):
                os.makedirs(day_dir)
            
            # Save Copy
            copy_path = os.path.join(day_dir, "copy.md")

            with open(copy_path, "w") as f:
                content = f"""# {day} - {post.get('archetype')}

## Strategy & Reasoning
{post.get('reasoning')}

## Visual Prompt
{post.get('visual_prompt')}

---

## LinkedIn Post Copy

{post.get('copy')}
"""
                f.write(content)
            
            # 3. Generate Visual
            visual_path = os.path.join(day_dir, "visual.png")
            if post.get('visual_prompt'):
                self.generate_visual_for_post(post['visual_prompt'], visual_path, context)
            
            # 4. Generate Video Script (Fault Tolerant)
            script_path = os.path.join(day_dir, "script.md")
            if post.get('copy') and self.video_agent:
                script = self.video_agent.generate_script(post['copy'], context)
                if script:
                     with open(script_path, "w") as f:
                         f.write(script)
                     print(f"      🎬 Saved video script.")
            
            print(f"   ✅ Saved {day} post.")

    def run(self):
        print("🚀 Starting Social Media Agent (Aggregator Mode)...")
        
        # 1. Load Context
        context_str = self.load_context()
        
        # 2. Load Top 3 Blogs
        blogs = self.load_weekly_blogs()
        print(f"   Loaded {len(blogs)} recent blogs.")
        
        # 3. Plan & Write
        if blogs:
            plan = self.generate_plan(blogs, context_str)
            # 4. Save
            self.save_pack(plan, context_str)
            print("✨ Social Media Pack generation complete.")
        else:
            print("⚠️ No blogs to process. Exiting.")

if __name__ == "__main__":
    agent = SocialMediaAgent()
    agent.run()
