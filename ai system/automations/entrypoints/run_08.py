#!/usr/bin/env python3
"""Automation 08 entrypoint: Weekly CRO + Landing Page Audit."""

from __future__ import annotations

from pathlib import Path
import sys

LIB_DIR = Path(__file__).resolve().parent.parent / 'lib'
sys.path.insert(0, str(LIB_DIR))

from automation_entry import run_entrypoint

if __name__ == '__main__':
    raise SystemExit(run_entrypoint('8', 'Weekly CRO + Landing Page Audit', 'week'))
