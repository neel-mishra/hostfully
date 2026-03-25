import csv
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUDIENCE_ROOT = os.path.join(REPO_ROOT, "docs", "paid_acquisition", "audiences")


BUYER_ALLOWLIST = [
    "cmo",
    "chief marketing officer",
    "cro",
    "chief revenue officer",
    "vp marketing",
    "head of marketing",
    "demand generation",
    "demand gen",
    "growth marketing",
    "revops",
    "revenue operations",
    "vp growth",
    "paid media",
]

EXCLUDE_KEYWORDS = [
    "intern",
    "junior",
    "student",
    "engineer",
    "developer",
    "product manager",
    "advisor",
    "former",
    "ex-",
]


@dataclass
class Contact:
    domain: str
    company_name: str
    full_name: str
    title: str
    email: str
    linkedin_url: str
    phone: str
    reason: str = ""


def _today_folder() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def _input_dir() -> str:
    return os.path.join(AUDIENCE_ROOT, _today_folder())


def _load_companies_icp() -> List[dict]:
    path = os.path.join(_input_dir(), "companies_icp.csv")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)  # type: ignore[return-value]


def _fake_contacts_for_company(row: dict) -> List[Contact]:
    """
    Placeholder contact enrichment that fabricates a small buying committee.
    Replace with real enrichment (Clearbit, Apollo, etc.) when available.
    """
    domain = row.get("domain") or ""
    name = row.get("company_name") or domain
    domain = domain.strip()
    name = name.strip()
    email_domain = domain if "@" not in domain else domain.split("@")[-1]

    contacts: List[Contact] = []
    # CMO
    contacts.append(
        Contact(
            domain=domain,
            company_name=name,
            full_name="CMO Placeholder",
            title="Chief Marketing Officer",
            email=f"cmo@{email_domain}",
            linkedin_url="",
            phone="",
            reason="placeholder_cmo",
        )
    )
    # Head of Demand Gen
    contacts.append(
        Contact(
            domain=domain,
            company_name=name,
            full_name="Demand Gen Lead Placeholder",
            title="Head of Demand Generation",
            email=f"demandgen@{email_domain}",
            linkedin_url="",
            phone="",
            reason="placeholder_demand_gen",
        )
    )
    return contacts


def _is_buyer(title: str) -> Tuple[bool, str]:
    t = title.lower()
    for bad in EXCLUDE_KEYWORDS:
        if bad in t:
            return False, f"exclude_keyword:{bad}"
    for good in BUYER_ALLOWLIST:
        if good in t:
            return True, f"buyer_match:{good}"
    return False, "no_buyer_keyword_match"


def _write_contacts_raw(contacts: List[Contact], out_dir: str) -> str:
    path = os.path.join(out_dir, "contacts_raw.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "domain",
                "company_name",
                "full_name",
                "title",
                "email",
                "linkedin_url",
                "phone",
                "reason",
            ]
        )
        for c in contacts:
            writer.writerow(
                [
                    c.domain,
                    c.company_name,
                    c.full_name,
                    c.title,
                    c.email,
                    c.linkedin_url,
                    c.phone,
                    c.reason,
                ]
            )
    return path


def _write_buyer_only(
    contacts: List[Contact],
    out_dir: str,
) -> Tuple[str, List[Contact], List[Contact]]:
    buyers: List[Contact] = []
    suppressed: List[Contact] = []
    for c in contacts:
        is_buyer, why = _is_buyer(c.title)
        if is_buyer:
            buyers.append(Contact(**{**c.__dict__, "reason": why}))
        else:
            suppressed.append(Contact(**{**c.__dict__, "reason": why}))

    buyers_path = os.path.join(out_dir, "contacts_buyer_only.csv")
    with open(buyers_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "domain",
                "company_name",
                "full_name",
                "title",
                "email",
                "linkedin_url",
                "phone",
                "reason",
            ]
        )
        for c in buyers:
            writer.writerow(
                [
                    c.domain,
                    c.company_name,
                    c.full_name,
                    c.title,
                    c.email,
                    c.linkedin_url,
                    c.phone,
                    c.reason,
                ]
            )

    return buyers_path, buyers, suppressed


def _write_suppression(suppressed: List[Contact], out_dir: str) -> str:
    path = os.path.join(out_dir, "suppression_lists.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "domain",
                "company_name",
                "full_name",
                "title",
                "email",
                "linkedin_url",
                "phone",
                "reason",
            ]
        )
        for c in suppressed:
            writer.writerow(
                [
                    c.domain,
                    c.company_name,
                    c.full_name,
                    c.title,
                    c.email,
                    c.linkedin_url,
                    c.phone,
                    c.reason,
                ]
            )
    return path


def _write_manifest(
    total_contacts: int,
    buyer_count: int,
    suppressed_count: int,
    out_dir: str,
) -> None:
    path = os.path.join(out_dir, "buying_committee_manifest.md")
    lines = [
        "# Buying Committee Manifest",
        "",
        f"- Generated at (UTC): {datetime.utcnow().isoformat()}",
        f"- Total contacts (raw): {total_contacts}",
        f"- Buyer-only contacts: {buyer_count}",
        f"- Suppressed contacts: {suppressed_count}",
        "",
        "Filtering rules:",
        "- Allowlist titles (buyers): " + ", ".join(BUYER_ALLOWLIST),
        "- Exclusion keywords: " + ", ".join(EXCLUDE_KEYWORDS),
        "",
        "Current contacts are placeholders; replace `_fake_contacts_for_company` with",
        "real enrichment when ready.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def run_buying_committee_enricher() -> None:
    out_dir = _input_dir()
    os.makedirs(out_dir, exist_ok=True)
    companies = _load_companies_icp()
    if not companies:
        return

    contacts: List[Contact] = []
    for row in companies:
        contacts.extend(_fake_contacts_for_company(row))

    if not contacts:
        return

    _write_contacts_raw(contacts, out_dir)
    _, buyers, suppressed = _write_buyer_only(contacts, out_dir)
    _write_suppression(suppressed, out_dir)
    _write_manifest(len(contacts), len(buyers), len(suppressed), out_dir)


if __name__ == "__main__":
    run_buying_committee_enricher()

