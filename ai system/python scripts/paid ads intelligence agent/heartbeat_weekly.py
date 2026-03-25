#!/usr/bin/env python3
"""
Weekly Heartbeat for Paid Ads Intelligence Agent.
Runs every Friday at 18:00 (end of business week) and generates
performance reports for all live paid ads channels.

Usage:
  # Run the scheduler (stays alive, fires every Friday):
  python heartbeat_weekly.py

  # Run once immediately (for testing or manual trigger):
  python heartbeat_weekly.py --now
"""

import sys
import time
import argparse
from datetime import datetime

try:
    import schedule
except ImportError:
    schedule = None

from paid_ads_intelligence_agent import PaidAdsIntelligenceAgent, WORKSPACE_ROOT


def job():
    now = datetime.now()
    print(f"\n💓 Paid Ads Intelligence Heartbeat — {now.strftime('%A %B %d, %Y %H:%M')}")
    agent = PaidAdsIntelligenceAgent(workspace_root=str(WORKSPACE_ROOT))
    output = agent.run(dt=now)
    print(f"💓 Heartbeat complete. Output: {output}\n")


def main():
    parser = argparse.ArgumentParser(description="Paid Ads Intelligence Weekly Scheduler")
    parser.add_argument("--now", action="store_true", help="Run immediately instead of scheduling")
    args = parser.parse_args()

    if args.now:
        print("🚀 Running paid ads intelligence agent immediately...")
        job()
        return

    if schedule is None:
        print("⚠️ 'schedule' library not installed. Install with: pip install schedule")
        print("   Falling back to immediate run.")
        job()
        return

    print("⏳ Paid Ads Intelligence Weekly Scheduler Started")
    print("   Scheduled: Every Friday at 18:00")
    print("   Press Ctrl+C to stop.\n")

    schedule.every().friday.at("18:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹ Scheduler stopped.")
