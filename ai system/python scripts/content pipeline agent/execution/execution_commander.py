
import os
import sys
from datetime import datetime
from blog_writer_agent import BlogWriterAgent

class ExecutionCommander:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.script_dir, "execution.log")

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        print(entry)
        with open(self.log_file, "a") as f:
            f.write(entry + "\n")

    def run_weekly_creation(self):
        self.log("=== WEEKLY EXECUTION START ===")
        self.log("🚀 Starting Blog Writer Agent...")
        try:
            agent = BlogWriterAgent()
            # Inherit paths from agent logic
            self.log(f"   Pipeline CSV: {agent.pipeline_path}")
            self.log(f"   Blogs Dir: {agent.blogs_dir}")
            
            # Execute
            # Note: We need to adapt BlogWriterAgent to run in this context
            # Since I imported the class, I can just instantiate and run.
            
            # To capture print output from agent to log, I would ideally redirect stdout
            # For MVP, I will just let it print to console (which launchd captures) 
            # and log the high level start/stop here.
            
            agent.run() 
            
            self.log("✅ Blog Writer Agent run complete.")
            
            self.log("🚀 Starting Social Media Agent (Aggregator)...")
            sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../social media agent")))
            from social_media_agent import SocialMediaAgent
            social_agent = SocialMediaAgent()
            social_agent.run()
            self.log("✅ Social Media Agent run complete.")
            
        except Exception as e:
            self.log(f"❌ Execution Workflow failed: {e}")
            
        self.log("=== WEEKLY EXECUTION END ===")

if __name__ == "__main__":
    commander = ExecutionCommander()
    commander.run_weekly_creation()
