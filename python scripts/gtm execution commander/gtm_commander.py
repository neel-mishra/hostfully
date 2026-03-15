#!/usr/bin/env python3
"""
GTM Execution Commander
Master script that reads a sprint plan JSON and sequentially orchestrates 
the execution of the individual automation agents, logging their output.
"""
import os
import sys
import json
import time
import subprocess
from datetime import datetime

class GTMCommander:
    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        self.commander_dir = os.path.join(self.workspace_root, "python scripts", "gtm execution commander")
        self.scripts_dir = os.path.join(self.workspace_root, "python scripts")
        self.config_path = os.path.join(self.commander_dir, "sprint_plan_template.json")
        self.log_file = os.path.join(self.commander_dir, "gtm_execution.log")

    def load_sprint_plan(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Failed to load sprint plan from {self.config_path}: {e}")
            sys.exit(1)

    def log(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        print(message)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def find_agent_script(self, agent_name: str) -> str:
        """Searches the python scripts directory to find the specified agent."""
        for root, dirs, files in os.walk(self.scripts_dir):
            if agent_name in files:
                return os.path.join(root, agent_name)
        return ""

    def run_agent(self, agent_path: str):
        """Executes a single python agent script via subprocess."""
        self.log(f"▶️ Executing: {os.path.basename(agent_path)}")
        try:
            # Setting stdout to PIPE allows us to capture the output, but printing it continuously
            process = subprocess.Popen(
                ["python3", agent_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                cwd=self.workspace_root
            )
            
            for line in process.stdout:
                # We log the sub-agent output cleanly
                clean_line = line.strip()
                if clean_line:
                    with open(self.log_file, "a", encoding="utf-8") as f:
                        f.write(f"    | {clean_line}\n")
                        
            process.wait()
            
            if process.returncode == 0:
                self.log(f"✅ Success: {os.path.basename(agent_path)}")
            else:
                self.log(f"⚠️ Warning: {os.path.basename(agent_path)} exited with code {process.returncode}")
                
        except Exception as e:
            self.log(f"❌ Error executing {os.path.basename(agent_path)}: {e}")

    def run(self):
        plan = self.load_sprint_plan()
        self.log("\n==================================================")
        self.log(f"🚀 GTM COMMANDER STARTING: Sprint '{plan.get('sprint_name')}'")
        self.log(f"🎯 Target Persona: {plan.get('target_persona')}")
        self.log("==================================================")
        
        for vertical in plan.get("verticals_to_run", []):
            if not vertical.get("enabled", False):
                self.log(f"\n⏩ Skipping Vertical: {vertical.get('name')} (Disabled in config)")
                continue
                
            self.log(f"\n⚙️ Starting Vertical: {vertical.get('name')}")
            for agent_name in vertical.get("agents", []):
                agent_path = self.find_agent_script(agent_name)
                if agent_path:
                    self.run_agent(agent_path)
                    time.sleep(2) # Brief pause between scripts
                else:
                    self.log(f"❌ Error: Could not locate script '{agent_name}'")
                    
        self.log("\n🏁 GTM COMMANDER EXECUTION COMPLETE.")
        self.log("==================================================\n")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))
    
    commander = GTMCommander(workspace_root=project_root)
    commander.run()
