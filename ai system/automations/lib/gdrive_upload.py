#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def _load_env(root: Path) -> None:
    load_dotenv(root / ".env")
    load_dotenv(root / "miscellaneous" / ".env", override=True)


def _build_drive_client() -> object:
    client_id = os.getenv("GOOGLE_CLIENT_ID", "").strip()
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "").strip()
    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN", "").strip()
    if not (client_id and client_secret and refresh_token):
        raise RuntimeError("Missing GOOGLE_CLIENT_ID/GOOGLE_CLIENT_SECRET/GOOGLE_REFRESH_TOKEN")
    creds = Credentials(
        None,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=["https://www.googleapis.com/auth/drive.file"],
    )
    creds.refresh(Request())
    return build("drive", "v3", credentials=creds)


def upload_file(file_path: Path, folder_id: str) -> dict:
    drive = _build_drive_client()
    name = file_path.name
    escaped_name = name.replace("'", "\\'")
    q = f"'{folder_id}' in parents and name='{escaped_name}' and trashed=false"
    existing = (
        drive.files()
        .list(
            q=q,
            fields="files(id,name)",
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        )
        .execute()
        .get("files", [])
    )

    media = MediaFileUpload(str(file_path), mimetype="text/markdown", resumable=False)
    if existing:
        return (
            drive.files()
            .update(
                fileId=existing[0]["id"],
                media_body=media,
                fields="id,name,webViewLink",
                supportsAllDrives=True,
            )
            .execute()
        )
    body = {"name": name, "parents": [folder_id], "mimeType": "text/markdown"}
    return (
        drive.files()
        .create(body=body, media_body=media, fields="id,name,webViewLink", supportsAllDrives=True)
        .execute()
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload or update a file in Google Drive folder.")
    parser.add_argument("--file", required=True, help="Path to local file")
    parser.add_argument("--folder-id", required=True, help="Google Drive folder ID")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent.parent.parent
    _load_env(root)
    file_path = Path(args.file).expanduser().resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    out = upload_file(file_path, args.folder_id)
    print(out.get("id", ""))
    print(out.get("name", ""))
    print(out.get("webViewLink", ""))


if __name__ == "__main__":
    main()
