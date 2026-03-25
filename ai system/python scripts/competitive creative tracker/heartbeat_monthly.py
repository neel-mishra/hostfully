"""
heartbeat_monthly.py — Monthly Competitive Creative Tracker Scheduler

Runs the competitive tracker audit on the last day of every month.
Scrapes all five platforms: Meta, Google, LinkedIn, TikTok, X.

Two scheduling mechanisms:
  1. Python `schedule` library (runs as a long-lived process)
  2. macOS LaunchAgent plist (see com.tldr.tech.competitivetracker.monthly.plist)

Usage:
  python heartbeat_monthly.py          # start the scheduler daemon
  python heartbeat_monthly.py --now    # run immediately then exit
"""

import argparse
import calendar
import time
from datetime import datetime

import schedule

from competitive_tracker import run_audit


def is_last_day_of_month() -> bool:
    today = datetime.now()
    last_day = calendar.monthrange(today.year, today.month)[1]
    return today.day == last_day


def job():
    print(f"💓 Monthly Heartbeat Check at {datetime.now()}")
    if is_last_day_of_month():
        print("📅 Last day of the month — running competitive audit (all platforms)...")
        run_audit(platforms=None, dry_run=False)
    else:
        print(f"📅 Not the last day (today is day {datetime.now().day}) — skipping.")


def main():
    parser = argparse.ArgumentParser(description="Monthly Competitive Tracker Heartbeat")
    parser.add_argument("--now", action="store_true", help="Run audit immediately then exit")
    args = parser.parse_args()

    if args.now:
        print("🚀 Running audit immediately (all platforms)...")
        run_audit(platforms=None, dry_run=False)
        return

    print("⏳ Monthly Scheduler Started...")
    print("   Checks daily at 08:00. Runs audit on the last day of each month.")
    print("   Platforms: Meta, Google, LinkedIn, TikTok, X")

    schedule.every().day.at("08:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    try:
        import schedule
        main()
    except ImportError:
        print("⚠️ 'schedule' library not found. Install: pip install schedule")
        print("   Running audit once as fallback...")
        run_audit(platforms=None, dry_run=False)
