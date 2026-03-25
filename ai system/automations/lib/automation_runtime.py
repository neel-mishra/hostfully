#!/usr/bin/env python3
"""
Shared runtime primitives for automation safety:
- preflight env checks
- canonical path resolution
- run ledger events
- optional idempotency checks
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent


def _ledger_path() -> Path:
    out = WORKSPACE_ROOT / "outputs" / "automation_runs"
    out.mkdir(parents=True, exist_ok=True)
    return out / "run_ledger.jsonl"


def emit_run_event(
    workflow: str,
    status: str,
    *,
    step: str = "main",
    idempotency_key: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    event = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "workflow": workflow,
        "step": step,
        "status": status,
        "idempotency_key": idempotency_key,
        "details": details or {},
    }
    with _ledger_path().open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=True) + "\n")


def is_duplicate_success(idempotency_key: str | None) -> bool:
    if not idempotency_key:
        return False
    path = _ledger_path()
    if not path.exists():
        return False
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            try:
                event = json.loads(line)
            except Exception:
                continue
            if event.get("idempotency_key") == idempotency_key and event.get("status") == "success":
                return True
    return False


def preflight_env(required_vars: list[str]) -> list[str]:
    import os

    missing = [name for name in required_vars if not os.environ.get(name, "").strip()]
    return missing


def resolve_docs_path(path_str: str) -> Path:
    """
    Canonical resolver for docs path drift:
    1) docs/*
    2) outputs/docs/*
    """
    raw = Path(path_str)
    if raw.is_absolute():
        return raw

    primary = WORKSPACE_ROOT / raw
    if primary.exists():
        return primary

    path_parts = raw.parts
    if path_parts and path_parts[0] == "docs":
        alt = WORKSPACE_ROOT / "outputs" / raw
        if alt.exists():
            return alt

    return primary


def logical_period_idempotency_key(
    workflow: str,
    *,
    granularity: str = "day",
    dt: datetime | None = None,
    suffix: str | None = None,
) -> str:
    """
    Build consistent idempotency keys by logical period.
    granularity: day | week | month
    """
    current = dt or datetime.now(timezone.utc)
    if granularity == "month":
        period = current.strftime("%Y-%m")
    elif granularity == "week":
        iso_year, iso_week, _ = current.isocalendar()
        period = f"{iso_year}-W{iso_week:02d}"
    else:
        period = current.strftime("%Y-%m-%d")
    if suffix:
        return f"{workflow}:{period}:{suffix}"
    return f"{workflow}:{period}"
