import csv
import os
from datetime import datetime
from typing import List, Dict


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUDIENCE_ROOT = os.path.join(REPO_ROOT, "docs", "paid_acquisition", "audiences")


def _today_folder() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def _input_dir() -> str:
    return os.path.join(AUDIENCE_ROOT, _today_folder())


def _load_contacts_buyer_only() -> List[Dict[str, str]]:
    path = os.path.join(_input_dir(), "contacts_buyer_only.csv")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)  # type: ignore[return-value]


def _ensure_export_dir() -> str:
    path = os.path.join(_input_dir(), "exports")
    os.makedirs(path, exist_ok=True)
    return path


def _write_linkedin_export(contacts: List[Dict[str, str]], out_dir: str) -> str:
    """
    Minimal schema for LinkedIn Matched Audiences.
    Typically supports email, company, and job title.
    """
    path = os.path.join(out_dir, "linkedin_matched_audience.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "company", "job_title"])
        for c in contacts:
            email = (c.get("email") or "").strip()
            if not email:
                continue
            writer.writerow(
                [
                    email,
                    (c.get("company_name") or "").strip(),
                    (c.get("title") or "").strip(),
                ]
            )
    return path


def _write_meta_export(contacts: List[Dict[str, str]], out_dir: str) -> str:
    """
    Minimal schema for Meta Custom Audiences based on email.
    """
    path = os.path.join(out_dir, "meta_custom_audience.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "phone"])
        for c in contacts:
            email = (c.get("email") or "").strip()
            phone = (c.get("phone") or "").strip()
            if not email and not phone:
                continue
            writer.writerow([email, phone])
    return path


def _write_youtube_export(contacts: List[Dict[str, str]], out_dir: str) -> str:
    """
    Minimal schema for Google/YouTube Customer Match.
    Here we use email-only for simplicity.
    """
    path = os.path.join(out_dir, "google_youtube_customer_match.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["email"])
        for c in contacts:
            email = (c.get("email") or "").strip()
            if not email:
                continue
            writer.writerow([email])
    return path


def _write_readme(out_dir: str, total_contacts: int) -> None:
    path = os.path.join(out_dir, "README.md")
    today = _today_folder()
    lines = [
        "# Audience Export Pack",
        "",
        f"- Date folder: {today}",
        f"- Total buyer contacts in source: {total_contacts}",
        "",
        "This folder contains manual-upload-ready CSVs for:",
        "",
        "- LinkedIn Matched Audiences (`linkedin_matched_audience.csv`)",
        "- Meta Custom Audiences (`meta_custom_audience.csv`)",
        "- Google/YouTube Customer Match (`google_youtube_customer_match.csv`)",
        "",
        "Upload steps (high level):",
        "",
        "1. LinkedIn Campaign Manager → Account Assets → Matched Audiences → Create list → Upload list.",
        "2. Meta Ads Manager → Audiences → Create Audience → Custom Audience → Customer List.",
        "3. Google Ads → Tools & Settings → Audience Manager → Segments → Upload Customer list.",
        "",
        "Ensure you follow each platform's latest requirements for hashing and field mapping.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def _write_manifest(
    linkedin_path: str,
    meta_path: str,
    yt_path: str,
    total_contacts: int,
    out_dir: str,
) -> None:
    path = os.path.join(out_dir, "audience_manifest.md")
    lines = [
        "# Audience Export Manifest",
        "",
        f"- Generated at (UTC): {datetime.utcnow().isoformat()}",
        f"- Source buyer contacts: {total_contacts}",
        "",
        "Files:",
        f"- LinkedIn: `{os.path.basename(linkedin_path)}`",
        f"- Meta: `{os.path.basename(meta_path)}`",
        f"- Google/YouTube: `{os.path.basename(yt_path)}`",
        "",
        "Note: Hashing and final formatting should be applied according to",
        "each platform's latest specs before upload.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def run_audience_exporter() -> None:
    contacts = _load_contacts_buyer_only()
    if not contacts:
        return

    out_dir = _ensure_export_dir()
    linkedin_path = _write_linkedin_export(contacts, out_dir)
    meta_path = _write_meta_export(contacts, out_dir)
    yt_path = _write_youtube_export(contacts, out_dir)
    _write_readme(out_dir, len(contacts))
    _write_manifest(linkedin_path, meta_path, yt_path, len(contacts), out_dir)


if __name__ == "__main__":
    run_audience_exporter()

