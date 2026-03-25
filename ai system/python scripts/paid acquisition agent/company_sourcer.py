import csv
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUDIENCE_ROOT = os.path.join(REPO_ROOT, "docs", "paid_acquisition", "audiences")


@dataclass
class CompanyRecord:
    domain: str
    name: str
    tech_signal: str
    source: str
    note: str = ""


def _today_folder() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def _ensure_output_dir() -> str:
    subdir = _today_folder()
    path = os.path.join(AUDIENCE_ROOT, subdir)
    os.makedirs(path, exist_ok=True)
    return path


def _read_builtwith_csv(path: str, tech_signal: str) -> List[CompanyRecord]:
    """
    Minimal parser for a BuiltWith-style export.
    We assume there is at least a `Domain` column and optionally `Company Name`.
    """
    records: List[CompanyRecord] = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain = (row.get("Domain") or row.get("domain") or "").strip()
            if not domain:
                continue
            name = (row.get("Company Name") or row.get("company") or "").strip()
            records.append(
                CompanyRecord(
                    domain=domain,
                    name=name or domain,
                    tech_signal=tech_signal,
                    source="builtwith",
                )
            )
    return records


def _read_manual_seed_csv(path: str, label: str) -> List[CompanyRecord]:
    """
    Manual seed CSVs must contain at least a `domain` column.
    Optional columns: `name`, `note`.
    """
    records: List[CompanyRecord] = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            domain = (row.get("domain") or "").strip()
            if not domain:
                continue
            name = (row.get("name") or "").strip() or domain
            note = (row.get("note") or "").strip()
            records.append(
                CompanyRecord(
                    domain=domain,
                    name=name,
                    tech_signal=label,
                    source="manual_seed",
                    note=note,
                )
            )
    return records


def _dedupe(records: List[CompanyRecord]) -> List[CompanyRecord]:
    seen = set()
    deduped: List[CompanyRecord] = []
    for rec in records:
        key = rec.domain.lower()
        if key in seen:
            continue
        seen.add(key)
        deduped.append(rec)
    return deduped


def _write_companies_raw(records: List[CompanyRecord], out_dir: str) -> str:
    path = os.path.join(out_dir, "companies_raw.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "domain",
                "company_name",
                "tech_signal",
                "source",
                "note",
                "ingested_at_utc",
            ]
        )
        now = datetime.utcnow().isoformat()
        for r in records:
            writer.writerow(
                [r.domain, r.name, r.tech_signal, r.source, r.note, now]
            )
    return path


def _write_manifest(records: List[CompanyRecord], out_dir: str) -> None:
    path = os.path.join(out_dir, "companies_raw_manifest.md")
    lines = [
        "# Company Sourcing Manifest",
        "",
        f"- Generated at (UTC): {datetime.utcnow().isoformat()}",
        f"- Total unique companies: {len(records)}",
        "",
        "## Sources",
        "",
        "- This pack aggregates one or more BuiltWith exports and manual seed CSVs.",
        "",
        "Fields:",
        "- `domain` – canonical web domain",
        "- `company_name` – best-guess company name",
        "- `tech_signal` – short label such as `drift_installed` or `sponsors_newsletters`",
        "- `source` – `builtwith` or `manual_seed`",
        "- `note` – optional freeform note from seed files",
        "- `ingested_at_utc` – ISO timestamp when this file was created.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def run_company_sourcer(
    builtwith_paths: list[str] | None = None,
    builtwith_label: str = "",
    manual_seed_paths: list[str] | None = None,
    manual_label: str = "",
) -> None:
    builtwith_paths = builtwith_paths or []
    manual_seed_paths = manual_seed_paths or []

    records: List[CompanyRecord] = []
    for p in builtwith_paths:
        if os.path.exists(p):
            records.extend(_read_builtwith_csv(p, tech_signal=builtwith_label))

    for p in manual_seed_paths:
        if os.path.exists(p):
            records.extend(_read_manual_seed_csv(p, label=manual_label))

    if not records:
        return

    deduped = _dedupe(records)
    out_dir = _ensure_output_dir()
    _write_companies_raw(deduped, out_dir)
    _write_manifest(deduped, out_dir)


if __name__ == "__main__":
    # Example usage: run with environment-specific paths, or call from a higher-level orchestrator.
    run_company_sourcer()

