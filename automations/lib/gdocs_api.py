#!/usr/bin/env python3
"""
Google Docs API wrapper for Cursor Automations.

Usage:
  python gdocs_api.py list
  python gdocs_api.py create --title "My Report"
  python gdocs_api.py update --doc-name "My Report" --text "Content here" --location start
  python gdocs_api.py update --doc-id "abc123" --text "More content" --location end
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(WORKSPACE_ROOT / ".env")

CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
REFRESH_TOKEN = os.environ.get("GOOGLE_REFRESH_TOKEN", "")
FOLDER_ID = os.environ.get("DRIVE_FOLDER_ID_DOCS", "") or os.environ.get("DEFAULT_GOOGLE_DOCS_FOLDER_ID", "")

TOKEN_URL = "https://oauth2.googleapis.com/token"
DOCS_URL = "https://docs.googleapis.com/v1/documents"
DRIVE_URL = "https://www.googleapis.com/drive/v3/files"


def get_access_token():
    if not REFRESH_TOKEN:
        print(json.dumps({"error": "GOOGLE_REFRESH_TOKEN not set"}))
        sys.exit(1)
    resp = requests.post(TOKEN_URL, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": REFRESH_TOKEN,
        "grant_type": "refresh_token",
    }, timeout=30)
    data = resp.json()
    if "access_token" not in data:
        print(json.dumps({"error": "Token refresh failed", "detail": data}))
        sys.exit(1)
    return data["access_token"]


def headers():
    return {"Authorization": f"Bearer {get_access_token()}", "Content-Type": "application/json"}


def resolve_doc_id(name):
    h = headers()
    resp = requests.get(DRIVE_URL, headers=h, params={
        "q": f"name='{name}' and mimeType='application/vnd.google-apps.document' and trashed=false",
        "fields": "files(id,name)",
        "supportsAllDrives": "true",
        "includeItemsFromAllDrives": "true",
        "orderBy": "modifiedTime desc",
    }, timeout=30)
    files = resp.json().get("files", [])
    return files[0]["id"] if files else None


def cmd_list():
    h = headers()
    resp = requests.get(DRIVE_URL, headers=h, params={
        "q": f"'{FOLDER_ID}' in parents and mimeType='application/vnd.google-apps.document' and trashed=false",
        "fields": "files(id,name,modifiedTime)",
        "supportsAllDrives": "true",
        "includeItemsFromAllDrives": "true",
    }, timeout=30)
    print(json.dumps(resp.json().get("files", []), indent=2))


def cmd_create(title):
    h = headers()

    resp = requests.post(DOCS_URL, headers=h, json={"title": title}, timeout=30)
    doc = resp.json()
    doc_id = doc.get("documentId", "")

    if FOLDER_ID and doc_id:
        requests.patch(
            f"{DRIVE_URL}/{doc_id}",
            headers=h,
            params={"addParents": FOLDER_ID, "supportsAllDrives": "true"},
            timeout=30,
        )

    print(json.dumps({"documentId": doc_id, "title": title, "url": f"https://docs.google.com/document/d/{doc_id}"}))
    return doc_id


def cmd_update(doc_id=None, doc_name=None, text="", location="end"):
    if not doc_id:
        if doc_name:
            doc_id = resolve_doc_id(doc_name)
        if not doc_id:
            print(json.dumps({"error": f"Document '{doc_name}' not found"}))
            sys.exit(1)

    h = headers()

    if location == "start":
        index = 1
    else:
        resp = requests.get(f"{DOCS_URL}/{doc_id}", headers=h, timeout=30)
        body = resp.json().get("body", {}).get("content", [])
        index = body[-1]["endIndex"] - 1 if body else 1
        index = max(1, index)

    requests.post(f"{DOCS_URL}/{doc_id}:batchUpdate", headers=h, json={
        "requests": [{"insertText": {"location": {"index": index}, "text": text}}]
    }, timeout=60)

    print(json.dumps({"status": "ok", "documentId": doc_id, "chars_inserted": len(text)}))


def main():
    parser = argparse.ArgumentParser(description="Google Docs API CLI")
    parser.add_argument("command", choices=["list", "create", "update"])
    parser.add_argument("--title", help="Doc title (for create)")
    parser.add_argument("--doc-id", help="Document ID (for update)")
    parser.add_argument("--doc-name", help="Document name (for update, alternative to --doc-id)")
    parser.add_argument("--text", help="Text to insert")
    parser.add_argument("--location", choices=["start", "end"], default="end")
    args = parser.parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "create":
        cmd_create(args.title)
    elif args.command == "update":
        cmd_update(doc_id=args.doc_id, doc_name=args.doc_name, text=args.text, location=args.location)


if __name__ == "__main__":
    main()
