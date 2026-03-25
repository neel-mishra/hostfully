#!/usr/bin/env python3
"""
Deep crawler for Figma MCP public docs and repo files.

Outputs:
- mirror/: raw fetched content
- crawl-index.json: normalized crawl metadata
- coverage-report.md: crawl summary
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from collections import deque
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen


USER_AGENT = "TLDR-Figma-MCP-Crawler/1.0 (+local)"
TIMEOUT_SECONDS = 25
MAX_URLS = 2000
MAX_DEPTH = 8
REQUEST_DELAY_SECONDS = 0.15

SEED_URLS = [
    "https://github.com/mcp/com.figma.mcp/mcp",
    "https://github.com/figma/mcp-server-guide",
    "https://developers.figma.com/docs/figma-mcp-server/",
]

ALLOWLIST_PREFIXES = [
    "https://github.com/mcp/com.figma.mcp/mcp",
    "https://github.com/figma/mcp-server-guide",
    "https://raw.githubusercontent.com/figma/mcp-server-guide/",
    "https://api.github.com/repos/figma/mcp-server-guide/",
    "https://developers.figma.com/docs/figma-mcp-server/",
]

OUT_ROOT = Path(__file__).resolve().parent
MIRROR_DIR = OUT_ROOT / "mirror"
INDEX_PATH = OUT_ROOT / "crawl-index.json"
REPORT_PATH = OUT_ROOT / "coverage-report.md"
GUIDE_PATH = OUT_ROOT / "figma-mcp-build-guide.md"
SPEC_PATH = OUT_ROOT / "figma-mcp-crawl-spec.md"


class LinkExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: Set[str] = set()

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag.lower() != "a":
            return
        for k, v in attrs:
            if k.lower() == "href" and v:
                self.links.add(v)


@dataclass
class CrawlEntry:
    url: str
    canonical_url: str
    depth: int
    status: str
    http_status: Optional[int]
    content_type: Optional[str]
    source_kind: str
    content_sha256: Optional[str]
    bytes: int
    discovered_links: List[str]
    error: Optional[str]
    mirror_path: Optional[str]
    fetched_at_unix: float


def canonicalize(url: str) -> str:
    p = urlparse(url)
    scheme = p.scheme.lower()
    netloc = p.netloc.lower()
    path = re.sub(r"/{2,}", "/", p.path or "/")
    if path != "/" and path.endswith("/"):
        path = path[:-1]
    query_pairs = [(k, v) for (k, v) in parse_qsl(p.query, keep_blank_values=True) if not k.startswith("utm_")]
    query = "&".join(f"{k}={v}" for (k, v) in sorted(query_pairs))
    return urlunparse((scheme, netloc, path, "", query, ""))


def in_scope(url: str) -> bool:
    c = canonicalize(url)
    return any(c.startswith(prefix.rstrip("/")) for prefix in ALLOWLIST_PREFIXES)


def detect_kind(url: str, content_type: str) -> str:
    if "api.github.com/repos/figma/mcp-server-guide/git/trees" in url:
        return "github_api_tree"
    if "api.github.com/repos/figma/mcp-server-guide/contents" in url:
        return "github_api_contents"
    if "json" in content_type:
        return "json"
    if "html" in content_type:
        return "html"
    if "markdown" in content_type or url.endswith(".md"):
        return "markdown"
    return "text"


def fetch(url: str) -> Tuple[int, str, bytes]:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "*/*"})
    with urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        body = resp.read()
        status = getattr(resp, "status", 200)
        ctype = resp.headers.get("Content-Type", "application/octet-stream")
        return status, ctype, body


def extract_links(url: str, content_type: str, text: str) -> Set[str]:
    out: Set[str] = set()
    if "html" in content_type:
        parser = LinkExtractor()
        parser.feed(text)
        for href in parser.links:
            out.add(urljoin(url, href))
    elif "json" in content_type:
        # GitHub API payloads include direct URL fields.
        for m in re.findall(r'"(?:html_url|url|download_url|git_url)"\s*:\s*"([^"]+)"', text):
            out.add(urljoin(url, m))
    else:
        # Markdown/plaintext links.
        for m in re.findall(r"\[[^\]]+\]\((https?://[^)]+)\)", text):
            out.add(m)
        for m in re.findall(r"\bhttps?://[^\s)>\"]+", text):
            out.add(m.rstrip(".,"))
    return out


def mirror_file_path(url: str, content_type: str) -> Path:
    c = canonicalize(url)
    p = urlparse(c)
    safe_host = p.netloc.replace(":", "_")
    safe_path = p.path.strip("/") or "root"
    safe_path = re.sub(r"[^A-Za-z0-9._/\-]", "_", safe_path)
    ext = ".txt"
    if "json" in content_type:
        ext = ".json"
    elif "html" in content_type:
        ext = ".html"
    elif "markdown" in content_type or safe_path.endswith(".md"):
        ext = ".md"
    if safe_path.endswith(ext):
        rel = Path(safe_host) / safe_path
    else:
        rel = Path(safe_host) / f"{safe_path}{ext}"
    return MIRROR_DIR / rel


def synthesize_docs(entries: List[CrawlEntry]) -> None:
    guide = """# Figma MCP Build Guide

## What is set up in this repo
- Cursor MCP server config includes `figma` pointing to `https://mcp.figma.com/mcp`.
- Crawl artifacts for Figma MCP docs are stored in `ai system/mcp/figma_mcp/mirror/`.
- Crawl metadata and link coverage are in `crawl-index.json` and `coverage-report.md`.

## Cursor setup (already configured)
1. Open Cursor settings MCP panel to verify server `figma` is enabled.
2. Ensure you are authenticated when prompted by Cursor.
3. In agent chat, run `#get_design_context` to confirm tool visibility.

## VS Code manual setup
Use `MCP:Add Server` with:
- Type: `HTTP`
- URL: `https://mcp.figma.com/mcp`
- Server ID: `figma`

## Claude Code manual setup
Run:
```bash
claude mcp add --transport http figma https://mcp.figma.com/mcp
```

## Common Figma MCP flow
1. Run `get_design_context` for selected frame/layer URL.
2. Run `get_screenshot` for fidelity checks.
3. Run `get_variable_defs` to map tokens and styles.
4. Use Code Connect tools (`get_code_connect_map`, suggestions/mappings) for component reuse.

## Rate-limit notes
- Starter / View / Collab seats may be limited to a small monthly call quota.
- Dev/Full seats on paid plans generally use per-minute API-style limits.
"""
    GUIDE_PATH.write_text(guide, encoding="utf-8")

    spec = """# Figma MCP Crawl Spec

## Objective
Continuously mirror public Figma MCP docs and related repo files to support offline reference and reproducible setup.

## Scope allowlist
- `github.com/mcp/com.figma.mcp/mcp`
- `github.com/figma/mcp-server-guide`
- `raw.githubusercontent.com/figma/mcp-server-guide/*`
- `api.github.com/repos/figma/mcp-server-guide/*`
- `developers.figma.com/docs/figma-mcp-server/*`

## Crawler behavior
- URL canonicalization, deduplication, and depth-bounded traversal.
- HTML/JSON/Markdown link extraction.
- Per-URL mirrored content under `mirror/<host>/<path>`.
- Coverage index with status, hash, type, discovered links, and errors.

## Re-run
```bash
python3 "ai system/mcp/figma_mcp/scrape_figma_mcp.py"
```
"""
    SPEC_PATH.write_text(spec, encoding="utf-8")


def main() -> None:
    MIRROR_DIR.mkdir(parents=True, exist_ok=True)
    queue: deque[Tuple[str, int]] = deque((u, 0) for u in SEED_URLS)
    visited: Set[str] = set()
    entries: List[CrawlEntry] = []
    failed = 0
    skipped = 0

    while queue and len(visited) < MAX_URLS:
        url, depth = queue.popleft()
        c = canonicalize(url)
        if c in visited:
            continue
        visited.add(c)

        if depth > MAX_DEPTH or not in_scope(c):
            skipped += 1
            entries.append(
                CrawlEntry(
                    url=url,
                    canonical_url=c,
                    depth=depth,
                    status="skipped",
                    http_status=None,
                    content_type=None,
                    source_kind="out_of_scope_or_depth",
                    content_sha256=None,
                    bytes=0,
                    discovered_links=[],
                    error=None,
                    mirror_path=None,
                    fetched_at_unix=time.time(),
                )
            )
            continue

        try:
            time.sleep(REQUEST_DELAY_SECONDS)
            http_status, ctype, body = fetch(c)
            text = body.decode("utf-8", errors="replace")
            kind = detect_kind(c, ctype)
            links = sorted({canonicalize(x) for x in extract_links(c, ctype, text)})
            for link in links:
                if link not in visited and in_scope(link):
                    queue.append((link, depth + 1))

            out_path = mirror_file_path(c, ctype)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(body)
            digest = hashlib.sha256(body).hexdigest()

            entries.append(
                CrawlEntry(
                    url=url,
                    canonical_url=c,
                    depth=depth,
                    status="ok",
                    http_status=http_status,
                    content_type=ctype,
                    source_kind=kind,
                    content_sha256=digest,
                    bytes=len(body),
                    discovered_links=links,
                    error=None,
                    mirror_path=str(out_path.relative_to(OUT_ROOT)),
                    fetched_at_unix=time.time(),
                )
            )
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            failed += 1
            entries.append(
                CrawlEntry(
                    url=url,
                    canonical_url=c,
                    depth=depth,
                    status="failed",
                    http_status=getattr(exc, "code", None),
                    content_type=None,
                    source_kind="error",
                    content_sha256=None,
                    bytes=0,
                    discovered_links=[],
                    error=str(exc),
                    mirror_path=None,
                    fetched_at_unix=time.time(),
                )
            )

    INDEX_PATH.write_text(
        json.dumps([asdict(e) for e in entries], indent=2, ensure_ascii=True),
        encoding="utf-8",
    )

    ok_count = sum(1 for e in entries if e.status == "ok")
    report = (
        "# Coverage Report\n\n"
        f"- Total visited: {len(visited)}\n"
        f"- Fetched OK: {ok_count}\n"
        f"- Skipped: {skipped}\n"
        f"- Failed: {failed}\n"
        f"- Index: `{INDEX_PATH.name}`\n"
        f"- Mirror root: `{MIRROR_DIR.name}/`\n"
    )
    REPORT_PATH.write_text(report, encoding="utf-8")
    synthesize_docs(entries)


if __name__ == "__main__":
    main()
