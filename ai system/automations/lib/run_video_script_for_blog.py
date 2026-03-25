#!/usr/bin/env python3
"""
Generate a video script for one blog post. Used by Automation 02 (Weekly Content Execution).
Usage:
  python3 ai system/automations/lib/run_video_script_for_blog.py --file path/to/blog.md --slug my-post-slug
"""
import argparse
import sys
from pathlib import Path
from automation_runtime import emit_run_event, resolve_docs_path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def main():
    parser = argparse.ArgumentParser(description="Generate video script for a blog post")
    parser.add_argument("--file", required=True, help="Path to blog markdown file")
    parser.add_argument("--slug", required=True, help="Slug for output filename (e.g. my-post-slug)")
    parser.add_argument("--idempotency-key", help="Optional idempotency key")
    args = parser.parse_args()
    idempotency_key = args.idempotency_key or f"video_script:{args.slug}:{args.file}"
    emit_run_event("run_video_script_for_blog", "started", step="generate", idempotency_key=idempotency_key)

    from dotenv import load_dotenv
    load_dotenv(WORKSPACE_ROOT / ".env")

    sys.path.insert(0, str(WORKSPACE_ROOT / "ai system/python scripts/visual generators/videos"))
    from video_script_agent import VideoScriptAgent

    blog_path = Path(args.file)
    if not blog_path.is_absolute():
        blog_path = WORKSPACE_ROOT / blog_path
    if not blog_path.exists():
        print(f"Error: file not found: {blog_path}")
        sys.exit(1)

    blog_content = blog_path.read_text()
    agent = VideoScriptAgent()
    script = agent.generate_script(blog_content[:3000], "TLDR tech newsletter content")
    if not script:
        sys.exit(0)

    out_dir = resolve_docs_path("docs/content_assets/repurposed")
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"video_script_{args.slug}.md"
    out.write_text(script)
    print(f"Saved: {out}")
    emit_run_event("run_video_script_for_blog", "success", step="generate", idempotency_key=idempotency_key, details={"output": str(out)})


if __name__ == "__main__":
    main()
