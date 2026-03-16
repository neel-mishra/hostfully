#!/usr/bin/env python3
"""
Generate a video script from a blog post markdown file.

Usage:
  python run_video_script_for_blog.py --file path/to/blog.md --slug my-slug
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "python scripts" / "visual generators" / "videos"))

from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = WORKSPACE_ROOT / "docs" / "content_assets" / "video_scripts"


def main():
    parser = argparse.ArgumentParser(description="Generate video script from blog post")
    parser.add_argument("--file", type=str, required=True, help="Path to blog markdown file")
    parser.add_argument("--slug", type=str, required=True, help="Short slug for output filename")
    args = parser.parse_args()

    source = Path(args.file)
    if not source.exists():
        print(f"Error: File not found: {source}")
        sys.exit(1)

    load_dotenv(WORKSPACE_ROOT / ".env")

    blog_content = source.read_text(encoding="utf-8")

    try:
        from video_script_agent import VideoScriptAgent
        agent = VideoScriptAgent()
        script = agent.generate_script(blog_content[:3000], "TLDR blog post")
    except Exception as e:
        print(f"Video script generation failed: {e}")
        script = None

    if not script:
        print("VideoScriptAgent unavailable or failed. Skipping.")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    out_path = OUTPUT_DIR / f"{args.slug}_{today}.md"
    out_path.write_text(script, encoding="utf-8")
    print(f"Video script saved to {out_path}")


if __name__ == "__main__":
    main()
