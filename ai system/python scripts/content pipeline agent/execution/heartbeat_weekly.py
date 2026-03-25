
import time
import schedule
from execution_commander import ExecutionCommander
from datetime import datetime

def job():
    print(f"💓 Weekly Heartbeat Triggered at {datetime.now()}")
    commander = ExecutionCommander()
    commander.run_weekly_creation()

def main():
    print("⏳ Weekly Scheduler Started...")
    print("   Scheduled to run every Monday at 09:00 AM.")
    
    # Schedule weekly run
    schedule.every().monday.at("09:00").do(job)
    
    # Run once immediately for verification if needed (commented out for prod)
    # job()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    try:
        import schedule
        main()
    except ImportError:
        print("⚠️ 'schedule' library not found. Please run: pip install schedule")
        # Fallback for testing
        job()
