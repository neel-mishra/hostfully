#!/usr/bin/env python3
"""
Google Sheets API wrapper for Cursor Automations.

Usage:
  python gsheets_api.py list
  python gsheets_api.py create --title "My Sheet"
  python gsheets_api.py update --title "My Sheet" --range "Sheet1" --values '[["a","b"],["c","d"]]'
  python gsheets_api.py read --title "My Sheet" --range "Sheet1!A:Z"
"""

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from automation_runtime import (
    emit_run_event,
    is_duplicate_success,
    logical_period_idempotency_key,
    preflight_env,
)

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

def _normalize_private_key(raw: str) -> str:
    """Handle key from .env: literal \\n or actual newlines, and strip."""
    if not raw:
        return ""
    key = raw.strip()
    # If stored as single line with literal \n, expand to real newlines
    if "\\n" in key and "\n" not in key:
        key = key.replace("\\n", "\n")
    return key


def _check_pem_line_lengths(key: str) -> None:
    """PEM base64 lines should be 64 chars (except the last). One short line = corrupt key."""
    lines = [l for l in key.split("\n") if l and not l.startswith("-----")]
    bad = [i for i, l in enumerate(lines) if len(l) != 64 and i < len(lines) - 1]
    if bad:
        raise ValueError(
            "GSHEETS_PRIVATE_KEY is corrupt: base64 line(s) %s have length != 64 (got %s). "
            "Re-copy the full private_key from your service account JSON into .env as one line with \\n for newlines."
            % (bad, [len(lines[i]) for i in bad])
        )


CLIENT_EMAIL = os.environ.get("GSHEETS_CLIENT_EMAIL", "")
PRIVATE_KEY = _normalize_private_key(os.environ.get("GSHEETS_PRIVATE_KEY", ""))
FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID_SHEETS", "") or os.environ.get("DEFAULT_GOOGLE_SHEETS_FOLDER_ID", "")


def get_service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    if not CLIENT_EMAIL or not PRIVATE_KEY:
        print(json.dumps({"error": "GSHEETS_CLIENT_EMAIL or GSHEETS_PRIVATE_KEY not set"}))
        sys.exit(1)

    try:
        _check_pem_line_lengths(PRIVATE_KEY)
    except ValueError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    creds = service_account.Credentials.from_service_account_info(
        {
            "type": "service_account",
            "client_email": CLIENT_EMAIL,
            "private_key": PRIVATE_KEY,
            "token_uri": "https://oauth2.googleapis.com/token",
        },
        scopes=[
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ],
    )
    sheets = build("sheets", "v4", credentials=creds)
    drive = build("drive", "v3", credentials=creds)
    return sheets, drive


def resolve_sheet_id(drive, title):
    res = drive.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.spreadsheet' and name='{title}' and trashed=false",
        fields="files(id, name)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
    files = res.get("files", [])
    if not files:
        return None
    return files[0]["id"]


def cmd_list():
    _, drive = get_service()
    res = drive.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.spreadsheet' and trashed=false",
        fields="files(id, name, modifiedTime)",
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
    ).execute()
    print(json.dumps(res.get("files", []), indent=2))


def cmd_create(title):
    _, drive = get_service()
    # Create sheet directly in the shared folder via Drive API so SA's Editor on folder is used
    body = {
        "name": title,
        "mimeType": "application/vnd.google-apps.spreadsheet",
        "parents": [FOLDER_ID],
    }
    file = (
        drive.files()
        .create(
            body=body,
            supportsAllDrives=True,
            fields="id, name, webViewLink",
        )
        .execute()
    )
    sheet_id = file["id"]
    url = file.get("webViewLink") or f"https://docs.google.com/spreadsheets/d/{sheet_id}/edit"
    print(json.dumps({"spreadsheetId": sheet_id, "title": title, "url": url}))


def cmd_update(title, range_, values_json):
    sheets, drive = get_service()
    sheet_id = resolve_sheet_id(drive, title)
    if not sheet_id:
        print(json.dumps({"error": f"Sheet '{title}' not found. Create it first."}))
        sys.exit(1)

    values = json.loads(values_json)
    sheets.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range=range_,
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": values},
    ).execute()
    print(json.dumps({"status": "ok", "title": title, "rows_appended": len(values)}))


def cmd_read(title, range_):
    sheets, drive = get_service()
    sheet_id = resolve_sheet_id(drive, title)
    if not sheet_id:
        print(json.dumps({"error": f"Sheet '{title}' not found."}))
        sys.exit(1)

    res = sheets.spreadsheets().values().get(
        spreadsheetId=sheet_id, range=range_
    ).execute()
    print(json.dumps(res.get("values", []), indent=2))


def main():
    parser = argparse.ArgumentParser(description="Google Sheets API CLI")
    parser.add_argument("command", choices=["list", "create", "update", "read"])
    parser.add_argument("--title", help="Sheet title")
    parser.add_argument("--range", help="Cell range (e.g. Sheet1, Sheet1!A:Z)")
    parser.add_argument("--values", help='JSON array of arrays: \'[["a","b"],["c","d"]]\'')
    parser.add_argument("--idempotency-key", help="Optional idempotency key")
    parser.add_argument("--idempotency-granularity", choices=["day", "week", "month"], default="day")
    parser.add_argument("--allow-duplicate-run", action="store_true")
    args = parser.parse_args()

    idempotency_key = args.idempotency_key or logical_period_idempotency_key(
        "gsheets_api",
        granularity=args.idempotency_granularity,
        suffix=f"{args.command}:{args.title or ''}:{args.range or ''}",
    )
    if (not args.allow_duplicate_run) and is_duplicate_success(idempotency_key):
        print(json.dumps({"status": "skipped", "reason": "idempotent_success", "idempotency_key": idempotency_key}))
        emit_run_event("gsheets_api", "skipped", step=args.command, idempotency_key=idempotency_key)
        return

    missing = preflight_env(["GSHEETS_CLIENT_EMAIL", "GSHEETS_PRIVATE_KEY"])
    if missing:
        print(json.dumps({"error": "missing_env", "missing": missing}))
        emit_run_event("gsheets_api", "failed", step=args.command, idempotency_key=idempotency_key, details={"missing_env": missing})
        sys.exit(1)

    emit_run_event("gsheets_api", "started", step=args.command, idempotency_key=idempotency_key)

    if args.command == "list":
        cmd_list()
    elif args.command == "create":
        cmd_create(args.title)
    elif args.command == "update":
        cmd_update(args.title, args.range, args.values)
    elif args.command == "read":
        cmd_read(args.title, args.range)
    emit_run_event("gsheets_api", "success", step=args.command, idempotency_key=idempotency_key)


if __name__ == "__main__":
    main()
