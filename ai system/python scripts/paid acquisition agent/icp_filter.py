import csv
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple


REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
AUDIENCE_ROOT = os.path.join(REPO_ROOT, "docs", "paid_acquisition", "audiences")
COMMANDS_DIR = os.path.join(REPO_ROOT, "commands")


@dataclass
class EnrichedCompany:
    domain: str
    company_name: str
    employee_range: str
    industry: str
    geography: str
    funding_stage: str
    icp_score: float
    icp_reason: str


def _today_folder() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d")


def _input_dir() -> str:
    return os.path.join(AUDIENCE_ROOT, _today_folder())


def _load_companies_raw() -> List[dict]:
    path = os.path.join(_input_dir(), "companies_raw.csv")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)  # type: ignore[return-value]


def _load_icp_text() -> str:
    path = os.path.join(COMMANDS_DIR, "core", "ideal_customer_profile.md")
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _simple_enrich_and_score(row: dict, icp_text: str) -> EnrichedCompany:
    """
    Placeholder enrichment + scoring function.
    In a full implementation, this would call external enrichment APIs.
    Here we apply simple heuristics so the pipeline is wired.
    """
    domain = (row.get("domain") or "").strip()
    name = (row.get("company_name") or domain).strip()

    # Very rough heuristics; replace with real enrichment later.
    employee_range = "51-200"
    industry = "B2B SaaS"
    geography = "US"
    funding_stage = "Series B+"

    score = 0.0
    reasons: List[str] = []

    if "SaaS" in icp_text or "SaaS" in name:
        score += 0.3
        reasons.append("Matches SaaS pattern from ICP.")
    if "US" in icp_text or ".us" in domain:
        score += 0.2
        reasons.append("US-focused ICP.")
    if "marketing" in icp_text.lower():
        score += 0.2
        reasons.append("ICP mentions marketing; assuming fit with Hostfully GTM product.")

    if score == 0.0:
        reasons.append("Fallback: insufficient data; treating as low-fit.")

    return EnrichedCompany(
        domain=domain,
        company_name=name,
        employee_range=employee_range,
        industry=industry,
        geography=geography,
        funding_stage=funding_stage,
        icp_score=round(score, 2),
        icp_reason=" ".join(reasons),
    )


def _score_all(companies_raw: List[dict], icp_text: str) -> List[EnrichedCompany]:
    return [_simple_enrich_and_score(row, icp_text) for row in companies_raw]


def _write_scored(companies: List[EnrichedCompany], out_dir: str) -> str:
    path = os.path.join(out_dir, "companies_scored.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "domain",
                "company_name",
                "employee_range",
                "industry",
                "geography",
                "funding_stage",
                "icp_score",
                "icp_reason",
            ]
        )
        for c in companies:
            writer.writerow(
                [
                    c.domain,
                    c.company_name,
                    c.employee_range,
                    c.industry,
                    c.geography,
                    c.funding_stage,
                    c.icp_score,
                    c.icp_reason,
                ]
            )
    return path


def _write_icp_subset(companies: List[EnrichedCompany], out_dir: str, threshold: float) -> Tuple[str, int]:
    path = os.path.join(out_dir, "companies_icp.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "domain",
                "company_name",
                "employee_range",
                "industry",
                "geography",
                "funding_stage",
                "icp_score",
                "icp_reason",
            ]
        )
        kept = 0
        for c in companies:
            if c.icp_score >= threshold:
                kept += 1
                writer.writerow(
                    [
                        c.domain,
                        c.company_name,
                        c.employee_range,
                        c.industry,
                        c.geography,
                        c.funding_stage,
                        c.icp_score,
                        c.icp_reason,
                    ]
                )
    return path, kept


def _write_manifest(total: int, kept: int, threshold: float, out_dir: str) -> None:
    path = os.path.join(out_dir, "companies_icp_manifest.md")
    lines = [
        "# ICP Filtering Manifest",
        "",
        f"- Generated at (UTC): {datetime.utcnow().isoformat()}",
        f"- Total companies scored: {total}",
        f"- Companies above threshold ({threshold}): {kept}",
        "",
        "Scoring is currently heuristic and should be treated as a wiring placeholder.",
        "Replace `_simple_enrich_and_score` with real enrichment + scoring when ready.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def run_icp_filter(threshold: float = 0.5) -> None:
    out_dir = _input_dir()
    os.makedirs(out_dir, exist_ok=True)
    companies_raw = _load_companies_raw()
    if not companies_raw:
        return

    icp_text = _load_icp_text()
    scored = _score_all(companies_raw, icp_text)
    _write_scored(scored, out_dir)
    _, kept = _write_icp_subset(scored, out_dir, threshold=threshold)
    _write_manifest(len(scored), kept, threshold, out_dir)


if __name__ == "__main__":
    run_icp_filter()

