#!/usr/bin/env python3
"""
Website Traffic Analytics Agent
Monitors overall website traffic health via the Google Analytics Data API (GA4).
Pulls sessions, bounce rates, and funnel drop-off metrics, then generates
automated alerts or summary reports.
"""
import os
import sys
import json
import time
from datetime import datetime, timedelta

from dotenv import load_dotenv

# NOTE: Requires `google-analytics-data` pip package and a GCP Service Account
# pip install google-analytics-data
try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient
    from google.analytics.data_v1beta.types import (
        RunReportRequest, DateRange, Metric, Dimension
    )
    GA4_AVAILABLE = True
except ImportError:
    GA4_AVAILABLE = False


class TrafficAnalyticsAgent:
    """
    Connects to GA4, pulls key metrics, detects anomalies
    against simple historical baselines, and writes a report.
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        load_dotenv(os.path.join(self.workspace_root, ".env"))

        self.property_id = os.getenv("GA4_PROPERTY_ID", "")
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
        self.output_dir = os.path.join(self.workspace_root, "docs", "analytics_reports")
        os.makedirs(self.output_dir, exist_ok=True)

        self.client = None

    def _init_client(self):
        """Initialize the GA4 API client."""
        if not GA4_AVAILABLE:
            print("⚠️ google-analytics-data package not installed. Running in mock mode.")
            return False
        if not self.property_id:
            print("⚠️ GA4_PROPERTY_ID not set in .env. Running in mock mode.")
            return False
        if self.credentials_path and os.path.exists(self.credentials_path):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.credentials_path
        try:
            self.client = BetaAnalyticsDataClient()
            return True
        except Exception as e:
            print(f"⚠️ Could not create GA4 client: {e}. Running in mock mode.")
            return False

    def fetch_report(self, start_date: str, end_date: str) -> dict:
        """Fetch a GA4 report for the given date range."""
        if self.client:
            request = RunReportRequest(
                property=f"properties/{self.property_id}",
                date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
                metrics=[
                    Metric(name="sessions"),
                    Metric(name="bounceRate"),
                    Metric(name="averageSessionDuration"),
                    Metric(name="conversions"),
                ],
                dimensions=[Dimension(name="date")],
            )
            try:
                response = self.client.run_report(request)
                rows = []
                for row in response.rows:
                    rows.append({
                        "date": row.dimension_values[0].value,
                        "sessions": int(row.metric_values[0].value),
                        "bounce_rate": float(row.metric_values[1].value),
                        "avg_duration": float(row.metric_values[2].value),
                        "conversions": int(row.metric_values[3].value),
                    })
                return {"source": "GA4 API", "rows": rows}
            except Exception as e:
                print(f"   ⚠️ GA4 API error: {e}")

        # Mock data fallback
        print("   📊 Using mock traffic data...")
        today = datetime.now()
        mock_rows = []
        for i in range(7):
            d = today - timedelta(days=i)
            mock_rows.append({
                "date": d.strftime("%Y%m%d"),
                "sessions": 1200 - (i * 50) + (i % 3 * 80),
                "bounce_rate": 0.42 + (i * 0.02),
                "avg_duration": 185.0 - (i * 5),
                "conversions": 45 - (i * 3),
            })
        return {"source": "Mock Data", "rows": mock_rows}

    def detect_anomalies(self, data: dict) -> list:
        """Simple anomaly detection: flag days with >20% deviation from 7-day mean."""
        rows = data.get("rows", [])
        if len(rows) < 3:
            return []

        avg_sessions = sum(r["sessions"] for r in rows) / len(rows)
        avg_bounce = sum(r["bounce_rate"] for r in rows) / len(rows)

        alerts = []
        latest = rows[0]
        if abs(latest["sessions"] - avg_sessions) / avg_sessions > 0.20:
            direction = "spike" if latest["sessions"] > avg_sessions else "drop"
            alerts.append(
                f"🚨 Session {direction}: {latest['sessions']} vs 7-day avg {avg_sessions:.0f} "
                f"({((latest['sessions']-avg_sessions)/avg_sessions)*100:+.1f}%)"
            )
        if latest["bounce_rate"] > avg_bounce * 1.15:
            alerts.append(
                f"🚨 Bounce rate elevated: {latest['bounce_rate']:.1%} vs avg {avg_bounce:.1%}"
            )
        return alerts

    def generate_report(self, data: dict, anomalies: list) -> str:
        """Builds a Markdown report."""
        rows = data.get("rows", [])
        lines = [
            f"# Website Traffic Report",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"**Data Source:** {data.get('source', 'Unknown')}",
            "",
        ]

        if anomalies:
            lines.append("## ⚠️ Anomalies Detected")
            for a in anomalies:
                lines.append(f"- {a}")
            lines.append("")

        lines.append("## Daily Metrics (Last 7 Days)")
        lines.append("| Date | Sessions | Bounce Rate | Avg Duration (s) | Conversions |")
        lines.append("|------|----------|-------------|-------------------|-------------|")
        for r in rows:
            lines.append(
                f"| {r['date']} | {r['sessions']} | {r['bounce_rate']:.1%} "
                f"| {r['avg_duration']:.0f} | {r['conversions']} |"
            )
        lines.append("")

        if rows:
            total_sessions = sum(r["sessions"] for r in rows)
            total_conv = sum(r["conversions"] for r in rows)
            lines.append("## Summary")
            lines.append(f"- **Total Sessions:** {total_sessions}")
            lines.append(f"- **Total Conversions:** {total_conv}")
            lines.append(f"- **Overall Conversion Rate:** {total_conv/total_sessions:.2%}" if total_sessions else "")

        return "\n".join(lines)

    def run(self):
        print("\n--- Starting Traffic Analytics Agent ---")
        live = self._init_client()

        today = datetime.now().strftime("%Y-%m-%d")
        week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        data = self.fetch_report(start_date=week_ago, end_date=today)
        anomalies = self.detect_anomalies(data)

        report = self.generate_report(data, anomalies)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"traffic_report_{timestamp}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"✅ Saved Traffic Report to: {output_file}")
        if anomalies:
            print("   🚨 ANOMALIES FOUND:")
            for a in anomalies:
                print(f"      {a}")
        print("--- Traffic Analytics Agent Complete ---\n")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))

    agent = TrafficAnalyticsAgent(workspace_root=project_root)
    agent.run()
