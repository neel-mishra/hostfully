
import os
import subprocess
import sys
from datetime import datetime

# Ensure current directory is in sys.path for local imports
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

from pipeline_agent import PipelineAgent # type: ignore

# Configuration
SCRAPER_SCRIPT_PATH = "../../../python scripts/competitor scrapers/competitor-blog-scraper.py"

class CommanderAgent:
    def __init__(self):
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.log_file = os.path.join(self.script_dir, "commander.log")

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}"
        print(entry)
        with open(self.log_file, "a") as f:
            f.write(entry + "\n")

    def run_scraper(self):
        self.log("🚀 Starting Competitor Blog Scraper...")
        
        # Determine absolute path to scraper
        base_dir = os.path.dirname(os.path.abspath(__file__))
        scraper_abs_path = os.path.abspath(os.path.join(base_dir, SCRAPER_SCRIPT_PATH))
        scraper_dir = os.path.dirname(scraper_abs_path)
        
        if not os.path.exists(scraper_abs_path):
            self.log(f"❌ Scraper script not found at {scraper_abs_path}")
            return False

        try:
            # Run scraper in its own directory context
            result = subprocess.run(
                [sys.executable, scraper_abs_path],
                cwd=scraper_dir,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.log("✅ Scraper completed successfully.")
                output_summary = result.stdout[-200:] if result.stdout else "No output." # type: ignore
                self.log(f"   Output Summary:\n{output_summary}")
                return True
            else:
                self.log(f"❌ Scraper failed with code {result.returncode}")
                self.log(f"   Error: {result.stderr}")
                return False

        except Exception as e:
            self.log(f"❌ Critical Error running scraper: {e}")
            return False

    def run_pipeline(self):
        self.log("🚀 Starting Pipeline Agent...")
        try:
            agent = PipelineAgent()
            # We need to adapt PipelineAgent to run within this context or import it.
            # Since we imported class, let's instantiate and run.
            
            # The PipelineAgent code I wrote uses `__file__` to find paths. 
            # This works if imported too, as __file__ belongs to the module.
            agent.run() 
            self.log("✅ Pipeline Agent completed.")
            return True
        except Exception as e:
            self.log(f"❌ Pipeline Agent failed: {e}")
            return False

    def execute_daily_workflow(self):
        self.log("=== DAILY WORKFLOW START ===")
        
        # Step 1: Run Scraper
        if self.run_scraper():
            # Step 2: Run Pipeline (only if scraper succeeds/runs)
            self.run_pipeline()
        else:
            self.log("⚠️ Skipping Pipeline run due to Scraper failure.")
            
        self.log("=== DAILY WORKFLOW END ===")

if __name__ == "__main__":
    commander = CommanderAgent()
    commander.execute_daily_workflow()
