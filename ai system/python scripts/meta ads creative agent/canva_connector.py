"""
canva_connector.py

Canva MCP connector for the Meta creative pipeline.

Design goals:
- Fail clearly when Canva MCP is unavailable.
- Keep zero-breakage behavior when Canva sync is disabled.
- Discover tool names from MCP descriptor files instead of hardcoding.
- Emit a deterministic sync plan JSON artifact for auditability.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


def _default_mcps_root() -> Path:
    """Cursor stores MCP descriptor JSON under ~/.cursor/projects/<slug>/mcps. Override with CURSOR_MCP_DESCRIPTORS_ROOT."""
    env = os.environ.get("CURSOR_MCP_DESCRIPTORS_ROOT")
    if env:
        return Path(env)
    return (
        Path.home()
        / ".cursor/projects/Users-neelmishra-antigravity-GTM-multi-agent-system-Hostfully/mcps"
    )


DEFAULT_MCPS_ROOT = _default_mcps_root()


class CanvaConnectorError(RuntimeError):
    """Raised when Canva MCP cannot be resolved or used."""


@dataclass
class ConceptPayload:
    concept_index: int
    concept_title: str
    visual_type: str = ""
    visual_description: str = ""
    headline: str = ""
    subtext: str = ""
    cta: str = ""
    image_prompt: str = ""


@dataclass
class CanvaSyncPlan:
    campaign_goal: str
    funnel_stage: str
    target_audience: str
    placement_tags: list[str]
    concepts: list[ConceptPayload] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_json(self) -> str:
        return json.dumps(
            {
                "campaign_goal": self.campaign_goal,
                "funnel_stage": self.funnel_stage,
                "target_audience": self.target_audience,
                "placement_tags": self.placement_tags,
                "created_at": self.created_at,
                "concepts": [c.__dict__ for c in self.concepts],
            },
            indent=2,
        )


@dataclass
class CanvaMcpDescriptor:
    server_name: str
    tools: list[str]
    has_auth_tool: bool
    path: Path


def _normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def discover_canva_server(mcps_root: Path = DEFAULT_MCPS_ROOT) -> CanvaMcpDescriptor:
    """Discover a Canva-related MCP server by scanning descriptor directories."""
    if not mcps_root.exists():
        raise CanvaConnectorError(f"MCP descriptors directory not found: {mcps_root}")

    candidates: list[CanvaMcpDescriptor] = []
    for server_dir in mcps_root.iterdir():
        if not server_dir.is_dir():
            continue
        tools_dir = server_dir / "tools"
        if not tools_dir.exists():
            continue
        tool_files = sorted(tools_dir.glob("*.json"))
        tool_names = [f.stem for f in tool_files]
        joined = _normalize(server_dir.name + " " + " ".join(tool_names))
        if "canva" not in joined:
            continue
        candidates.append(
            CanvaMcpDescriptor(
                server_name=server_dir.name,
                tools=tool_names,
                has_auth_tool="mcp_auth" in tool_names,
                path=server_dir,
            )
        )

    if not candidates:
        raise CanvaConnectorError(
            "No Canva MCP server descriptors found. Add/enable a Canva MCP server in your MCP config."
        )
    return candidates[0]


def parse_creative_output_to_plan(
    creative_output: str,
    *,
    campaign_goal: str,
    funnel_stage: str,
    target_audience: str,
    placement_tags: list[str],
) -> CanvaSyncPlan:
    """
    Parse LLM creative markdown into a structured plan for Canva MCP execution.
    The parser is tolerant and intentionally only extracts fields needed by design tooling.
    """
    chunks = re.split(r"(?:^|\n)##\s+CONCEPT\s+\[(\d+)\]:\s*", creative_output)
    concepts: list[ConceptPayload] = []
    if len(chunks) < 3:
        # Fallback: single concept if format drifted
        concepts.append(
            ConceptPayload(
                concept_index=1,
                concept_title="Concept 1",
                visual_description="Format did not match concept template; use manual import.",
            )
        )
    else:
        # chunks format: [prefix, idx1, body1, idx2, body2, ...]
        for i in range(1, len(chunks), 2):
            idx_raw = chunks[i].strip()
            body = chunks[i + 1] if i + 1 < len(chunks) else ""
            # title is up to first newline
            title_line, _, rest = body.partition("\n")
            concept_idx = int(idx_raw) if idx_raw.isdigit() else (len(concepts) + 1)
            concept_title = title_line.strip() or f"Concept {concept_idx}"

            visual_type = _extract_inline_field(rest, "Visual Type")
            visual_description = _extract_bullet_field(rest, "Scene and Composition")
            headline = _extract_after_header(rest, "### ON-IMAGE COPY VARIATIONS", r"- Headline:\s*(.+)")
            subtext = _extract_after_header(rest, "### ON-IMAGE COPY VARIATIONS", r"- Subtext:\s*(.+)")
            cta = _extract_after_header(rest, "### ON-IMAGE COPY VARIATIONS", r"- CTA:\s*(.+)")
            image_prompt = _extract_block(rest, "### AI IMAGE GENERATION PROMPT")

            concepts.append(
                ConceptPayload(
                    concept_index=concept_idx,
                    concept_title=concept_title,
                    visual_type=visual_type,
                    visual_description=visual_description,
                    headline=headline,
                    subtext=subtext,
                    cta=cta,
                    image_prompt=image_prompt,
                )
            )

    return CanvaSyncPlan(
        campaign_goal=campaign_goal,
        funnel_stage=funnel_stage,
        target_audience=target_audience,
        placement_tags=placement_tags,
        concepts=concepts,
    )


def _extract_inline_field(block: str, name: str) -> str:
    m = re.search(rf"\*\*{re.escape(name)}:\*\*\s*(.+)", block)
    return m.group(1).strip() if m else ""


def _extract_bullet_field(block: str, label: str) -> str:
    m = re.search(rf"-\s+\*\*{re.escape(label)}:\*\*\s*(.+)", block)
    return m.group(1).strip() if m else ""


def _extract_after_header(block: str, header: str, pattern: str) -> str:
    idx = block.find(header)
    if idx == -1:
        return ""
    sub = block[idx:]
    m = re.search(pattern, sub, flags=re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # Line-by-line fallback for minor format drift.
    label = pattern.split(":")[0].replace(r"\s*", "").replace("- ", "").lower()
    for line in sub.splitlines():
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        left = stripped.split(":", 1)[0].lower()
        if label and label in left:
            parts = stripped.split(":", 1)
            if len(parts) == 2:
                return parts[1].strip()
    return ""


def _extract_block(block: str, header: str) -> str:
    idx = block.find(header)
    if idx == -1:
        return ""
    sub = block[idx + len(header):]
    # until next section header
    parts = re.split(r"\n###\s+", sub, maxsplit=1)
    return parts[0].strip()


def persist_sync_plan(plan: CanvaSyncPlan, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(plan.to_json(), encoding="utf-8")


def validate_canva_tooling(descriptor: CanvaMcpDescriptor) -> dict[str, Any]:
    """
    Validate the discovered server has likely-usable design lifecycle tools.
    This is name-based to stay resilient across server implementations.
    """
    names = [_normalize(n) for n in descriptor.tools]
    checks = {
        "has_create_or_template": any(("create" in n and "design" in n) or ("template" in n) for n in names),
        "has_text_or_element_tool": any(("text" in n) or ("element" in n) or ("edit" in n) for n in names),
        "has_export_or_publish": any(("export" in n) or ("publish" in n) or ("download" in n) for n in names),
    }
    checks["ready"] = all(checks.values())
    return checks
