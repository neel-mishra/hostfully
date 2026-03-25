#!/usr/bin/env python3
"""
Search Term Ranking Analytics Agent
Tracks organic search positioning for designated keyword clusters
via the Google Search Console API. Identifies "Striking Distance"
keywords and generates optimization action reports.

Uses the same credentials as all GSC consumers: set GSC_SITE_URL and
GOOGLE_APPLICATION_CREDENTIALS in the workspace .env (see docs/GSC_GA4_SETUP.md).
When unset, runs in mock mode. See also ai system/automations/lib/gsc_api.py for CLI usage.
"""
import os
import sys
import csv
import time
from datetime import datetime, timedelta

from dotenv import load_dotenv

# NOTE: Requires `google-api-python-client` and `google-auth` packages
# pip install google-api-python-client google-auth-oauthlib
try:
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    GSC_AVAILABLE = True
except ImportError:
    GSC_AVAILABLE = False


class SearchRankingAgent:
    """
    Queries Google Search Console for keyword performance data,
    identifies striking-distance keywords (positions 11-20),
    and outputs an optimization hit-list.
    """

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        load_dotenv(os.path.join(self.workspace_root, ".env"))

        self.site_url = os.getenv("GSC_SITE_URL", "")
        self.credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
        self.output_dir = os.path.join(self.workspace_root, "docs", "analytics_reports")
        os.makedirs(self.output_dir, exist_ok=True)

        self.service = None

    def _init_client(self) -> bool:
        """Initialize the Search Console API client."""
        if not GSC_AVAILABLE:
            print("⚠️ google-api-python-client not installed. Running in mock mode.")
            return False
        if not self.site_url:
            print("⚠️ GSC_SITE_URL not set in .env. Running in mock mode.")
            return False
        try:
            scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
            creds = service_account.Credentials.from_service_account_file(
                self.credentials_path, scopes=scopes
            )
            self.service = build("searchconsole", "v1", credentials=creds)
            return True
        except Exception as e:
            print(f"⚠️ Could not init Search Console client: {e}. Running in mock mode.")
            return False

    def fetch_search_data(self, start_date: str, end_date: str) -> list:
        """Fetch search analytics data from GSC or return mock data."""
        if self.service:
            try:
                request = {
                    "startDate": start_date,
                    "endDate": end_date,
                    "dimensions": ["query", "page"],
                    "rowLimit": 500,
                }
                response = self.service.searchanalytics().query(
                    siteUrl=self.site_url, body=request
                ).execute()
                rows = []
                for row in response.get("rows", []):
                    rows.append({
                        "query": row["keys"][0],
                        "page": row["keys"][1],
                        "clicks": row.get("clicks", 0),
                        "impressions": row.get("impressions", 0),
                        "ctr": row.get("ctr", 0),
                        "position": row.get("position", 0),
                    })
                return rows
            except Exception as e:
                print(f"   ⚠️ GSC API error: {e}")

        # Mock data fallback
        print("   📊 Using mock search ranking data...")
        return [
            {"query": "ai marketing automation tool", "page": "/features", "clicks": 120, "impressions": 3400, "ctr": 0.035, "position": 8.2},
            {"query": "cross channel ad management", "page": "/product", "clicks": 45, "impressions": 2100, "ctr": 0.021, "position": 14.5},
            {"query": "meta ads reporting software", "page": "/integrations/meta", "clicks": 30, "impressions": 1800, "ctr": 0.017, "position": 18.1},
            {"query": "google ads automation ai", "page": "/integrations/google", "clicks": 85, "impressions": 2800, "ctr": 0.030, "position": 11.3},
            {"query": "tiktok ads manager alternative", "page": "/integrations/tiktok", "clicks": 15, "impressions": 900, "ctr": 0.017, "position": 22.7},
            {"query": "unified marketing dashboard", "page": "/", "clicks": 200, "impressions": 5200, "ctr": 0.038, "position": 5.1},
            {"query": "ai campaign optimizer", "page": "/features", "clicks": 60, "impressions": 2000, "ctr": 0.030, "position": 12.8},
            {"query": "marketing automation saas", "page": "/pricing", "clicks": 95, "impressions": 3100, "ctr": 0.031, "position": 9.4},
            {"query": "reduce cpa with ai", "page": "/blog/cpa-optimization", "clicks": 10, "impressions": 600, "ctr": 0.017, "position": 19.5},
            {"query": "multi channel attribution", "page": "/features", "clicks": 55, "impressions": 1700, "ctr": 0.032, "position": 15.2},
        ]

    def classify_keywords(self, rows: list) -> dict:
        """Classify keywords into buckets based on position."""
        buckets = {
            "top_10": [],        # Positions 1-10: Defend
            "striking_distance": [],  # Positions 11-20: Push to page 1
            "opportunity": [],    # Positions 21-50: Long-term plays
        }
        for row in rows:
            pos = row.get("position", 100)
            if pos <= 10:
                buckets["top_10"].append(row)
            elif pos <= 20:
                buckets["striking_distance"].append(row)
            else:
                buckets["opportunity"].append(row)

        # Sort striking distance by impressions (highest potential first)
        buckets["striking_distance"].sort(key=lambda x: x["impressions"], reverse=True)
        return buckets

    def generate_report(self, buckets: dict) -> str:
        """Builds the Keyword Action Report as Markdown."""
        lines = [
            "# Search Term Ranking Report",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 🎯 Striking Distance Keywords (Positions 11-20)",
            "*These terms need on-page optimization to break into page 1.*",
            "",
            "| Query | Page | Position | Impressions | CTR | Action |",
            "|-------|------|----------|-------------|-----|--------|",
        ]
        for kw in buckets["striking_distance"]:
            action = "Refresh H1 + add FAQ" if kw["position"] < 15 else "Deepen content + internal links"
            lines.append(
                f"| {kw['query']} | {kw['page']} | {kw['position']:.1f} "
                f"| {kw['impressions']} | {kw['ctr']:.1%} | {action} |"
            )

        lines.extend([
            "",
            "## ✅ Top 10 Keywords (Defend)",
            "",
            "| Query | Page | Position | Clicks |",
            "|-------|------|----------|--------|",
        ])
        for kw in buckets["top_10"]:
            lines.append(f"| {kw['query']} | {kw['page']} | {kw['position']:.1f} | {kw['clicks']} |")

        lines.extend([
            "",
            "## 🌱 Opportunity Keywords (Positions 21+)",
            "",
            "| Query | Page | Position | Impressions |",
            "|-------|------|----------|-------------|",
        ])
        for kw in buckets["opportunity"]:
            lines.append(f"| {kw['query']} | {kw['page']} | {kw['position']:.1f} | {kw['impressions']} |")

        return "\n".join(lines)

    def export_csv(self, buckets: dict):
        """Export striking-distance keywords as a CSV action list."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = os.path.join(self.output_dir, f"striking_distance_keywords_{timestamp}.csv")
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["query", "page", "position", "clicks", "impressions", "ctr", "action"])
            writer.writeheader()
            for kw in buckets["striking_distance"]:
                action = "Refresh H1 + add FAQ" if kw["position"] < 15 else "Deepen content + internal links"
                writer.writerow({**kw, "action": action})
        print(f"   📄 Exported CSV: {csv_path}")

    def run(self):
        print("\n--- Starting Search Ranking Agent ---")
        self._init_client()

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=28)).strftime("%Y-%m-%d")

        rows = self.fetch_search_data(start_date, end_date)
        buckets = self.classify_keywords(rows)

        report = self.generate_report(buckets)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"search_ranking_report_{timestamp}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)

        self.export_csv(buckets)

        print(f"✅ Saved Ranking Report to: {output_file}")
        print(f"   🎯 Found {len(buckets['striking_distance'])} striking-distance keywords")
        print("--- Search Ranking Agent Complete ---\n")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))

    agent = SearchRankingAgent(workspace_root=project_root)
    agent.run()
