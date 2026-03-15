
import time
import schedule
from commander import CommanderAgent
from datetime import datetime

def job():
    print(f"💓 Heartbeat Triggered at {datetime.now()}")
    commander = CommanderAgent()
    commander.execute_daily_workflow()

def main():
    print("⏳ Heartbeat Scheduler Started...")
    print("   Scheduled to run daily at 08:00 AM.")
    
    # Schedule daily run
    schedule.every().day.at("08:00").do(job)
    
    # Also run once immediately on startup for verification/demo purposes
    # job() 
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    # Ensure schedule library is installed, else fail gracefully or install
    try:
        import schedule
        main()
    except ImportError:
        print("⚠️ 'schedule' library not found. Please run: pip install schedule")
        # Fallback: Just run once and exit for now (Simulated Cron)
        job()
