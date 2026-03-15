#!/usr/bin/env python3
"""
Content Repurposing Agent

Takes a single long-form content piece and generates a full multi-channel
distribution kit: LinkedIn posts, Twitter/X threads, email subject lines,
newsletter blurbs, executive summaries, and SEO meta descriptions.

Usage:
  python repurpose_agent.py --file path/to/content.md                    # repurpose one piece
  python repurpose_agent.py --file path/to/content.md --side advertiser  # advertiser-facing
  python repurpose_agent.py --dry-run --file path/to/content.md          # preview
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
COMMANDS_DIR = WORKSPACE_ROOT / "commands"
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "content_assets" / "repurposed"


def _resolve_env_key(name: str) -> str | None:
    val = os.environ.get(name)
    if val:
        return val
    current = Path(__file__).resolve().parent
    while current != current.parent:
        env_file = current / ".env"
        if env_file.exists():
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith(f"{name}="):
                        return line.split("=", 1)[1].strip().strip("'\"")
        current = current.parent
    return None


CLAUDE_API_BASE = "https://api.anthropic.com/v1/messages"


def claude_generate(prompt: str, api_key: str, max_tokens: int = 8192, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            resp = requests.post(
                CLAUDE_API_BASE,
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-20250514",
                    "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=180,
            )
            if resp.status_code == 200:
                return resp.json()["content"][0]["text"]
            if resp.status_code == 429:
                time.sleep(min(60, 2 ** (attempt + 2)))
                continue
            time.sleep(5)
        except Exception as e:
            print(f"  ⚠ Claude exception: {e}")
            time.sleep(10)
    raise Exception("Max retries reached")


def load_voice_context() -> str:
    parts = []
    for path in [
        "identity/brand_voice_matrix.md",
        "identity/style_guides.md",
        "identity/messaging_pillars.md",
    ]:
        try:
            parts.append((COMMANDS_DIR / path).read_text()[:1500])
        except FileNotFoundError:
            pass
    return "\n\n".join(parts)


def repurpose(source_path: Path, side: str, api_key: str) -> str:
    source_content = source_path.read_text(encoding="utf-8")
    voice_context = load_voice_context()
    source_title = source_path.stem.replace("-", " ").replace("_", " ").title()

    side_instruction = ""
    if side == "reader":
        side_instruction = """
TARGET SIDE: Reader-facing
- Tone: informed peer, not corporate
- Focus: time savings, curation quality, tech insight
- Pillars: Time Reclaimed, Curated Signal, Professional Credibility
- Use "you" language directed at tech professionals"""
    else:
        side_instruction = """
TARGET SIDE: Advertiser-facing
- Tone: data-driven, ROI-focused, consultative
- Focus: performance metrics, audience quality, case studies
- Pillars: Outperform Paid Social, Audience Concentration, Low Noise
- Reference proof points: Delve (52x ROI), Plaid (20x ROI), Redact (50% lower CPC)"""

    prompt = f"""You are a content distribution specialist for TLDR, the largest daily tech newsletter (7M+ subscribers).

Take this source content and generate a full multi-channel repurposing kit.

SOURCE CONTENT:
{source_content[:12000]}

VOICE & STYLE:
{voice_context[:3000]}

{side_instruction}

Generate the complete kit in this format:

# Content Repurposing Kit: {source_title}

**Source:** {source_path.name}
**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Target Side:** {side}

---

## LinkedIn Posts

### Angle A: Insight Lead
[Open with the most surprising insight. 150-250 words. Hook first line. 2-3 hashtags. CTA at end.]

### Angle B: Data Lead
[Open with a compelling stat. 150-250 words. Different angle than A.]

### Angle C: Story Lead
[Open with narrative hook. 150-250 words. Different angle than A and B.]

---

## Twitter/X Thread

1/ [Hook — single most compelling takeaway, under 280 chars]
2/ [Key point 1]
3/ [Key point 2]
4/ [Key point 3]
5/ [Key point 4]
6/ [Key point 5]
7/ [So-what / implication]
8/ [CTA + link placeholder]

---

## Email Subject Lines

1. [question format]
2. [stat-led format]
3. [curiosity gap format]
4. [direct/declarative format]
5. [contrarian format]

---

## Newsletter Blurb

[50-75 words. TLDR editorial style: concise, informative. Natural link placement.]

---

## Executive Summary

[250-400 words. Key findings, supporting data, implications. Suitable for leadership.]

---

## SEO Meta Description

[150-160 characters. Primary keyword included. Click-worthy.]

RULES:
- Every LinkedIn post must have a different opening hook and angle
- Twitter thread tweets must be under 280 characters each
- Email subject lines: 2-6 words, lowercase, internal-feeling
- Newsletter blurb must match TLDR editorial voice exactly
- No emoji overload, no hashtag spam"""

    return claude_generate(prompt, api_key)


def main():
    parser = argparse.ArgumentParser(description="Content Repurposing Agent")
    parser.add_argument("--file", type=str, required=True, help="Path to source content file")
    parser.add_argument("--side", type=str, default="reader", choices=["reader", "advertiser"],
                        help="Target side: reader or advertiser")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()

    source = Path(args.file)
    if not source.exists():
        print(f"❌ File not found: {source}")
        sys.exit(1)

    load_dotenv(WORKSPACE_ROOT / ".env")
    api_key = _resolve_env_key("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ ANTHROPIC_API_KEY not found.")
        sys.exit(1)

    print(f"  📄 Source: {source.name}")
    print(f"  🎯 Side: {args.side}")

    if args.dry_run:
        print(f"  🧪 DRY RUN: would generate repurposing kit")
        return

    kit = repurpose(source, args.side, api_key)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    slug = source.stem.lower().replace(" ", "_")[:40]
    today = datetime.now().strftime("%Y-%m-%d")
    out_path = OUTPUT_DIR / f"{slug}_{today}_kit.md"
    out_path.write_text(kit, encoding="utf-8")

    print(f"  ✅ Kit saved to {out_path}")


if __name__ == "__main__":
    main()
