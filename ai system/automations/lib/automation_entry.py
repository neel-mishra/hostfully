#!/usr/bin/env python3
"""Guardrailed launcher for automation commands.

Phase 0 guarantees:
- preflight dependency check per automation
- logical-period idempotency gate
- run ledger events
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from automation_runtime import emit_run_event, is_duplicate_success, logical_period_idempotency_key

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent

DEFAULT_GRANULARITY = {
    '1': 'day',
    '2': 'week',
    '3': 'month',
    '4': 'week',
    '5': 'week',
    '6': 'week',
    '7': 'week',
    '8': 'week',
    '9': 'month',
    '10': 'month',
}


def run_preflight(automation_id: str, strict: bool) -> tuple[bool, dict]:
    cmd = [
        sys.executable,
        str(WORKSPACE_ROOT / 'ai system/automations/lib/preflight_automations.py'),
        '--automation',
        automation_id,
        '--no-write-report',
    ]
    if strict:
        cmd.append('--strict')
    proc = subprocess.run(cmd, cwd=str(WORKSPACE_ROOT), capture_output=True, text=True)
    payload = {}
    try:
        payload = json.loads(proc.stdout.strip() or '{}')
    except Exception:
        payload = {'raw_stdout': proc.stdout, 'raw_stderr': proc.stderr}
    return proc.returncode == 0, payload


def run_entrypoint(
    automation_id: str,
    workflow_name: str,
    default_granularity: str,
    argv: list[str] | None = None,
) -> int:
    parser = argparse.ArgumentParser(description=f'Guardrailed entrypoint for {workflow_name}')
    parser.add_argument('--idempotency-key', help='Optional explicit idempotency key')
    parser.add_argument('--idempotency-granularity', choices=['day', 'week', 'month'], default=default_granularity)
    parser.add_argument('--allow-duplicate-run', action='store_true')
    parser.add_argument('--no-preflight', action='store_true')
    parser.add_argument('--strict-preflight', action='store_true', default=True)
    parser.add_argument('--dry-run', action='store_true', help='Run checks only, do not execute command')
    parser.add_argument('--', dest='dashdash', action='store_true')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Command to execute after --')
    args = parser.parse_args(argv)

    suffix = workflow_name.lower().replace(' ', '_')
    logical_key = args.idempotency_key or logical_period_idempotency_key(
        f'automation_{automation_id}',
        granularity=args.idempotency_granularity,
        suffix=suffix,
    )

    if not args.allow_duplicate_run and is_duplicate_success(logical_key):
        print(json.dumps({'status': 'skipped', 'reason': 'idempotent_success', 'idempotency_key': logical_key}))
        emit_run_event(workflow_name, 'skipped', step='entrypoint', idempotency_key=logical_key)
        return 0

    if not args.no_preflight:
        ok, payload = run_preflight(automation_id, args.strict_preflight)
        if not ok:
            emit_run_event(workflow_name, 'failed', step='preflight', idempotency_key=logical_key, details=payload)
            print(json.dumps({'status': 'failed', 'stage': 'preflight', 'details': payload}, indent=2))
            return 1

    emit_run_event(workflow_name, 'started', step='entrypoint', idempotency_key=logical_key)

    cmd = list(args.command)
    if cmd and cmd[0] == '--':
        cmd = cmd[1:]

    if args.dry_run or not cmd:
        print(json.dumps({
            'status': 'ready',
            'workflow': workflow_name,
            'automation_id': automation_id,
            'idempotency_key': logical_key,
            'command': cmd,
            'dry_run': args.dry_run,
            'ts': datetime.now(timezone.utc).isoformat(),
        }, indent=2))
        emit_run_event(workflow_name, 'success', step='entrypoint', idempotency_key=logical_key, details={'dry_run': True, 'command': cmd})
        return 0

    proc = subprocess.run(cmd, cwd=str(WORKSPACE_ROOT))
    if proc.returncode == 0:
        emit_run_event(workflow_name, 'success', step='entrypoint', idempotency_key=logical_key, details={'command': cmd})
    else:
        emit_run_event(workflow_name, 'failed', step='entrypoint', idempotency_key=logical_key, details={'command': cmd, 'returncode': proc.returncode})
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description='Generic automation launcher')
    parser.add_argument('--automation', required=True, help='Automation number (1-10)')
    parser.add_argument('--workflow-name', required=True)
    parser.add_argument('--idempotency-key')
    parser.add_argument('--idempotency-granularity', choices=['day', 'week', 'month'])
    parser.add_argument('--allow-duplicate-run', action='store_true')
    parser.add_argument('--no-preflight', action='store_true')
    parser.add_argument('--strict-preflight', action='store_true', default=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('command', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    gran = args.idempotency_granularity or DEFAULT_GRANULARITY.get(args.automation, 'day')
    forwarded = []
    if args.idempotency_key:
        forwarded += ['--idempotency-key', args.idempotency_key]
    forwarded += ['--idempotency-granularity', gran]
    if args.allow_duplicate_run:
        forwarded.append('--allow-duplicate-run')
    if args.no_preflight:
        forwarded.append('--no-preflight')
    if args.strict_preflight:
        forwarded.append('--strict-preflight')
    if args.dry_run:
        forwarded.append('--dry-run')
    forwarded += ['--'] + args.command
    return run_entrypoint(args.automation, args.workflow_name, gran, argv=forwarded)


if __name__ == '__main__':
    raise SystemExit(main())
