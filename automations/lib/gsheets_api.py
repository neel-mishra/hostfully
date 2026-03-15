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

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

CLIENT_EMAIL = os.environ.get("GSHEETS_CLIENT_EMAIL", "")
PRIVATE_KEY = os.environ.get("GSHEETS_PRIVATE_KEY", "").replace("\\n", "\n")
FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID_SHEETS", "") or os.environ.get("DEFAULT_GOOGLE_SHEETS_FOLDER_ID", "")


def get_service():
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    if not CLIENT_EMAIL or not PRIVATE_KEY:
        print(json.dumps({"error": "GSHEETS_CLIENT_EMAIL or GSHEETS_PRIVATE_KEY not set"}))
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
    sheets, drive = get_service()
    body = {"properties": {"title": title}}
    ss = sheets.spreadsheets().create(body=body).execute()
    sheet_id = ss["spreadsheetId"]

    drive.files().update(
        fileId=sheet_id,
        addParents=FOLDER_ID,
        supportsAllDrives=True,
        fields="id, parents",
    ).execute()

    print(json.dumps({"spreadsheetId": sheet_id, "title": title, "url": ss.get("spreadsheetUrl", "")}))


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
    args = parser.parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "create":
        cmd_create(args.title)
    elif args.command == "update":
        cmd_update(args.title, args.range, args.values)
    elif args.command == "read":
        cmd_read(args.title, args.range)


if __name__ == "__main__":
    main()
