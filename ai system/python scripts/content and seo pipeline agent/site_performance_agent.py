#!/usr/bin/env python3
"""
Site Performance Analytics Agent
Ensures the website maintains Core Web Vitals excellence
using the Google PageSpeed Insights API. Runs audits on core URLs
and triggers alerts if metrics fall below configurable thresholds.
"""
import os
import sys
import json
import time
from datetime import datetime

import requests
from dotenv import load_dotenv


class SitePerformanceAgent:
    """
    Hits the PageSpeed Insights API for a list of URLs,
    checks LCP, INP, CLS, and overall performance scores,
    and generates a Markdown health report.
    """

    # Configurable thresholds (seconds / scores)
    THRESHOLDS = {
        "lcp_ms": 2500,        # Largest Contentful Paint (ms) — good: <2500
        "inp_ms": 200,         # Interaction to Next Paint (ms) — good: <200
        "cls": 0.1,            # Cumulative Layout Shift — good: <0.1
        "perf_score": 0.90,    # Lighthouse performance score — good: >0.90
    }

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root
        load_dotenv(os.path.join(self.workspace_root, ".env"))

        self.api_key = os.getenv("PAGESPEED_API_KEY", "")
        self.output_dir = os.path.join(self.workspace_root, "docs", "analytics_reports")
        os.makedirs(self.output_dir, exist_ok=True)

    def audit_url(self, url: str, strategy: str = "mobile") -> dict:
        """Run a PageSpeed Insights audit on a single URL."""
        if self.api_key:
            api_url = (
                f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
                f"?url={url}&strategy={strategy}&key={self.api_key}"
                f"&category=performance"
            )
            try:
                resp = requests.get(api_url, timeout=60)
                resp.raise_for_status()
                data = resp.json()

                lh = data.get("lighthouseResult", {})
                audits = lh.get("audits", {})
                categories = lh.get("categories", {})

                return {
                    "url": url,
                    "strategy": strategy,
                    "source": "PageSpeed API",
                    "perf_score": categories.get("performance", {}).get("score", 0),
                    "lcp_ms": audits.get("largest-contentful-paint", {}).get("numericValue", 0),
                    "inp_ms": audits.get("interaction-to-next-paint", {}).get("numericValue", 0),
                    "cls": audits.get("cumulative-layout-shift", {}).get("numericValue", 0),
                    "fcp_ms": audits.get("first-contentful-paint", {}).get("numericValue", 0),
                    "ttfb_ms": audits.get("server-response-time", {}).get("numericValue", 0),
                }
            except Exception as e:
                print(f"   ⚠️ PageSpeed API error for {url}: {e}")

        # Mock fallback
        print(f"   📊 Using mock performance data for: {url}")
        return {
            "url": url,
            "strategy": strategy,
            "source": "Mock Data",
            "perf_score": 0.87,
            "lcp_ms": 2200,
            "inp_ms": 150,
            "cls": 0.05,
            "fcp_ms": 1100,
            "ttfb_ms": 320,
        }

    def check_thresholds(self, result: dict) -> list:
        """Check a URL's metrics against configurable thresholds."""
        alerts = []
        if result["lcp_ms"] > self.THRESHOLDS["lcp_ms"]:
            alerts.append(f"🔴 LCP too slow: {result['lcp_ms']:.0f}ms (threshold: {self.THRESHOLDS['lcp_ms']}ms)")
        if result["inp_ms"] > self.THRESHOLDS["inp_ms"]:
            alerts.append(f"🔴 INP too slow: {result['inp_ms']:.0f}ms (threshold: {self.THRESHOLDS['inp_ms']}ms)")
        if result["cls"] > self.THRESHOLDS["cls"]:
            alerts.append(f"🔴 CLS too high: {result['cls']:.3f} (threshold: {self.THRESHOLDS['cls']})")
        if result["perf_score"] < self.THRESHOLDS["perf_score"]:
            alerts.append(f"🟡 Performance score low: {result['perf_score']:.0%} (threshold: {self.THRESHOLDS['perf_score']:.0%})")
        return alerts

    def generate_report(self, results: list) -> str:
        """Builds a Markdown performance report."""
        lines = [
            "# Site Performance Report (Core Web Vitals)",
            f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Metrics Overview",
            "| URL | Strategy | Perf Score | LCP (ms) | INP (ms) | CLS | Status |",
            "|-----|----------|-----------|----------|----------|-----|--------|",
        ]

        all_alerts = []
        for r in results:
            alerts = self.check_thresholds(r)
            status = "✅ Pass" if not alerts else "⚠️ Fail"
            lines.append(
                f"| {r['url']} | {r['strategy']} | {r['perf_score']:.0%} "
                f"| {r['lcp_ms']:.0f} | {r['inp_ms']:.0f} | {r['cls']:.3f} | {status} |"
            )
            if alerts:
                all_alerts.append({"url": r["url"], "alerts": alerts})

        if all_alerts:
            lines.extend(["", "## ⚠️ Threshold Violations"])
            for entry in all_alerts:
                lines.append(f"\n**{entry['url']}**")
                for a in entry["alerts"]:
                    lines.append(f"- {a}")

        lines.extend([
            "",
            "## Thresholds Used",
            f"- LCP: < {self.THRESHOLDS['lcp_ms']}ms",
            f"- INP: < {self.THRESHOLDS['inp_ms']}ms",
            f"- CLS: < {self.THRESHOLDS['cls']}",
            f"- Performance Score: > {self.THRESHOLDS['perf_score']:.0%}",
        ])

        return "\n".join(lines)

    def run(self, urls: list = None):
        print("\n--- Starting Site Performance Agent ---")

        if not urls:
            urls = [
                "https://hostfully.tech",
                "https://hostfully.tech/tech",
                "https://hostfully.tech/ai",
            ]
            print("   ℹ️ No URLs provided. Using defaults.")

        results = []
        for url in urls:
            print(f"   🔍 Auditing: {url}")
            result = self.audit_url(url, strategy="mobile")
            results.append(result)
            time.sleep(1)

        report = self.generate_report(results)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"site_performance_{timestamp}.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"✅ Saved Performance Report to: {output_file}")

        # Print any alerts to console
        for r in results:
            alerts = self.check_thresholds(r)
            if alerts:
                print(f"   🚨 ALERTS for {r['url']}:")
                for a in alerts:
                    print(f"      {a}")

        print("--- Site Performance Agent Complete ---\n")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, "../../"))

    agent = SitePerformanceAgent(workspace_root=project_root)
    agent.run()
