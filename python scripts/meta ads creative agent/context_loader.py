"""
context_loader.py — Brand Context File Loader

Reads all 8 brand markdown files from the project root, parses them into
heading-to-content sections, and assembles a single BRAND CONTEXT block
for injection into the system prompt.
"""

import os
import re
from pathlib import Path


# Relative paths from project root to each brand context file
CONTEXT_FILES = {
    "creative_direction": "commands/identity/creative_direction.md",
    "messaging_pillars": "commands/identity/messaging_pillars.md",
    "ideal_customer_profile": "commands/core/ideal_customer_profile.md",
    "business_context": "commands/core/business_context.md",
    "ad_copy_frameworks": "commands/identity/ad_copy_frameworks.md",
    "competitor_landscape": "commands/core/competitor_landscape.md",
    "brand_voice_matrix": "commands/identity/brand_voice_matrix.md",
    "style_guides": "commands/identity/style_guides.md",
}


def _extract_sections(markdown: str) -> dict[str, str]:
    """Split a markdown file by headings (h1 through h4) into a dict of heading → content."""
    sections: dict[str, str] = {}
    current_heading = ""
    current_content: list[str] = []

    for line in markdown.split("\n"):
        heading_match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading_match:
            # Save previous section
            if current_heading:
                sections[current_heading] = "\n".join(current_content).strip()
            current_heading = heading_match.group(2).strip()
            current_content = []
        else:
            current_content.append(line)

    # Save last section
    if current_heading:
        sections[current_heading] = "\n".join(current_content).strip()

    return sections


def load_all_context(project_root: str | None = None) -> dict[str, dict]:
    """
    Load every brand context file. Returns a dict where each key is a context
    file name (like 'creative_direction', 'messaging_pillars', etc.) and each
    value is a dict with 'raw' (full markdown text or None) and 'sections'
    (dict mapping each heading to its content).
    """
    if project_root is None:
        # Walk up from this file to find the project root (where 'commands/' exists)
        current = Path(__file__).resolve().parent
        while current != current.parent:
            if (current / "commands").is_dir():
                project_root = str(current)
                break
            current = current.parent
        if project_root is None:
            project_root = os.getcwd()

    context: dict[str, dict] = {}

    for name, rel_path in CONTEXT_FILES.items():
        full_path = os.path.join(project_root, rel_path)
        if os.path.exists(full_path):
            with open(full_path, "r", encoding="utf-8") as f:
                raw = f.read()
            context[name] = {
                "raw": raw,
                "sections": _extract_sections(raw),
            }
        else:
            print(f"  ⚠ Context file not found: {rel_path}")
            context[name] = {
                "raw": None,
                "sections": {},
            }

    return context


# ---------------------------------------------------------------------------
# Section extractors
# ---------------------------------------------------------------------------

def get_visual_identity(context: dict[str, dict]) -> str:
    """Extract visual identity, imagery style, AI prompting, brand symbols,
    creative adjustments sections from creative_direction."""
    cd = context.get("creative_direction", {})
    sections = cd.get("sections", {})
    if not sections and cd.get("raw"):
        return cd["raw"]

    target_keys = [
        "visual identity", "imagery style", "ai prompting",
        "brand symbols", "creative adjustments", "color palette",
        "typography", "logo", "imagery",
    ]

    parts: list[str] = []
    for heading, content in sections.items():
        if any(k in heading.lower() for k in target_keys):
            parts.append(f"### {heading}\n{content}")

    return "\n\n".join(parts) if parts else cd.get("raw", "")


def get_messaging_pillars(context: dict[str, dict]) -> str:
    """Return full messaging pillars document."""
    mp = context.get("messaging_pillars", {})
    return mp.get("raw", "") or ""


def get_terminology_rules(context: dict[str, dict]) -> str:
    """Extract the terminology and positioning section specifically."""
    mp = context.get("messaging_pillars", {})
    sections = mp.get("sections", {})

    target_keys = ["terminology", "positioning", "rules"]
    parts: list[str] = []
    for heading, content in sections.items():
        if any(k in heading.lower() for k in target_keys):
            parts.append(f"### {heading}\n{content}")

    return "\n\n".join(parts) if parts else ""


def get_icp_summary(context: dict[str, dict]) -> str:
    """Return full ICP document."""
    icp = context.get("ideal_customer_profile", {})
    return icp.get("raw", "") or ""


def get_competitor_summary(context: dict[str, dict]) -> str:
    """Return full competitor landscape document."""
    cl = context.get("competitor_landscape", {})
    return cl.get("raw", "") or ""


def get_ad_copy_rules(context: dict[str, dict]) -> str:
    """Extract Meta-specific ad copy section from ad_copy_frameworks."""
    acf = context.get("ad_copy_frameworks", {})
    sections = acf.get("sections", {})

    target_keys = ["meta", "facebook", "instagram"]
    parts: list[str] = []
    for heading, content in sections.items():
        if any(k in heading.lower() for k in target_keys):
            parts.append(f"### {heading}\n{content}")

    # If no Meta-specific section found, return the whole file
    return "\n\n".join(parts) if parts else (acf.get("raw", "") or "")


def build_brand_context_block(context: dict[str, dict]) -> str:
    """Assemble the full prompt block from all extractors."""
    sections = [
        "# BRAND CONTEXT",
        "",
        "## Visual Identity and Creative Direction",
        get_visual_identity(context),
        "",
        "## Messaging Pillars",
        get_messaging_pillars(context),
        "",
        "## Terminology and Positioning Rules",
        get_terminology_rules(context),
        "",
        "## Ideal Customer Profile",
        get_icp_summary(context),
        "",
        "## Competitor Landscape",
        get_competitor_summary(context),
        "",
        "## Meta Ad Copy Frameworks",
        get_ad_copy_rules(context),
    ]

    return "\n".join(sections)
