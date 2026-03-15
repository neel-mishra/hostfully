"""Shared scaffolding for platform-specific report analyzers."""

from datetime import datetime

# Common rules applied to all platform reports
SHARED_RULES = """
RULES (apply to all platforms):
- ALWAYS use pre-computed/authoritative numbers when provided. Do NOT recalculate from raw data.
- Always cite specific numbers. Never say "improved" without a %, $, or absolute number.
- If data is missing or the account has no active campaigns, state that clearly.
- Use $ formatting for costs, % for rates. Preserve decimal precision from the source data.
- Keep the tone analytical and direct — no fluff.
- Never use the word "conversions" — always say "leads" instead.
"""


def build_report_header(platform: str, since: str, until: str) -> str:
    """Standard report header."""
    return f"""# {platform} — Weekly Performance Intelligence Report
**Period:** {since} to {until}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
