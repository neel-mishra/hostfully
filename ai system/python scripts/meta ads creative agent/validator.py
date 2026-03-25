"""
validator.py — Post-Generation Quality Checks

6 validation checks that catch terminology violations, generic SaaS tropes,
missing attributions, and copy limit overruns before output is finalized.
"""

import re
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class ValidationIssue:
    severity: str  # "error" or "warning"
    check: str
    message: str
    location: str | None = None


@dataclass
class ValidationReport:
    issues: list[ValidationIssue] = field(default_factory=list)
    passed: bool = True

    def add(
        self,
        severity: str,
        check: str,
        message: str,
        location: str | None = None,
    ) -> None:
        issue = ValidationIssue(
            severity=severity,
            check=check,
            message=message,
            location=location,
        )
        self.issues.append(issue)
        if severity == "error":
            self.passed = False

    def summary(self) -> str:
        if not self.issues:
            return "✅ All validation checks passed."

        errors = sum(1 for i in self.issues if i.severity == "error")
        warnings = sum(1 for i in self.issues if i.severity == "warning")

        parts = []
        if errors:
            parts.append(f"❌ {errors} error(s)")
        if warnings:
            parts.append(f"⚠️ {warnings} warning(s)")

        status = "FAILED" if errors else "PASSED with warnings"
        return f"Validation {status}: {', '.join(parts)}"


# ---------------------------------------------------------------------------
# Check 1 — Terminology Gate (ERROR severity)
# ---------------------------------------------------------------------------

BANNED_TERMS: dict[str, str] = {
    r"dashboard\s+tool": "Use 'AI marketing agent', 'AI teammate', or 'AI-powered workspace'",
    r"automation\s+software": "Use 'AI marketing agent' or 'autonomous marketing agent'",
    r"analytics\s+platform": "Use 'AI-powered workspace' or 'conversational marketing agent'",
    r"co[\-\s]?pilot": "NEVER use 'co-pilot' — that is Ryze's positioning. Use 'teammate' or 'agent'",
    r"just\s+another\s+ai": "Never diminish the category",
}


def check_terminology(output: str, report: ValidationReport) -> None:
    """Detect banned terms in the generated output."""
    output_lower = output.lower()
    for pattern, replacement in BANNED_TERMS.items():
        for match in re.finditer(pattern, output_lower):
            start = max(0, match.start() - 30)
            end = min(len(output), match.end() + 30)
            context = output[start:end].replace("\n", " ")
            report.add(
                severity="error",
                check="terminology_gate",
                message=f"Banned term '{match.group()}' found. {replacement}",
                location=f"...{context}...",
            )


# ---------------------------------------------------------------------------
# Check 2 — Blandness Filter (WARNING severity)
# ---------------------------------------------------------------------------

BLAND_PATTERNS: list[str] = [
    r"floating\s+laptop",
    r"person\s+smiling\s+at\s+(phone|screen|laptop)",
    r"abstract\s+gradient\s+blob",
    r"all[\-\s]in[\-\s]one\s+(platform|solution)",
    r"sav(e|ing)\s+time",
    r"streamline\s+your",
    r"unlock\s+the\s+(power|potential)",
    r"transform(ing)?\s+the\s+(way|how)",
    r"purple[\s/]+blue\s+gradient\s+background",
    r"10x\s+your\s+marketing",
    r"supercharge\s+your",
    r"\bai[\-\s]powered\b(?!\s+workspace|\s+agent|\s+marketing)",
]


def check_blandness(output: str, report: ValidationReport) -> None:
    """Detect generic SaaS creative tropes."""
    output_lower = output.lower()
    for pattern in BLAND_PATTERNS:
        for match in re.finditer(pattern, output_lower):
            start = max(0, match.start() - 20)
            end = min(len(output), match.end() + 20)
            context = output[start:end].replace("\n", " ")
            report.add(
                severity="warning",
                check="blandness_filter",
                message=f"Generic SaaS trope detected: '{match.group()}'",
                location=f"...{context}...",
            )


# ---------------------------------------------------------------------------
# Check 3 — Inspiration Attribution (ERROR severity)
# ---------------------------------------------------------------------------

def check_inspiration_attribution(output: str, report: ValidationReport) -> None:
    """Verify every concept has a valid brand inspiration."""
    concept_headers = re.findall(r"CONCEPT\s+\[?\d+\]?", output, re.IGNORECASE)
    inspired_by = re.findall(
        r"(?:Inspired\s+By|Inspired\s+by)\s*:\s*(.+?)(?:\n|$)",
        output,
    )

    num_concepts = len(concept_headers)

    if num_concepts == 0:
        report.add(
            severity="error",
            check="inspiration_attribution",
            message="No CONCEPT headers found in output",
        )
        return

    # Filter out invalid attributions
    valid_attributions = []
    for attr in inspired_by:
        attr_clean = attr.strip().lower()
        if attr_clean and attr_clean not in ("n/a", "none", "tbd", "") and len(attr_clean) >= 5:
            valid_attributions.append(attr)

    # We expect at least one Inspired By per concept (may appear in header and brand reference)
    # Check that at least num_concepts valid attributions exist
    if len(valid_attributions) < num_concepts:
        report.add(
            severity="error",
            check="inspiration_attribution",
            message=(
                f"Found {len(valid_attributions)} valid 'Inspired By' attributions "
                f"for {num_concepts} concepts. Each concept needs a brand inspiration."
            ),
        )


# ---------------------------------------------------------------------------
# Check 4 — Premium Quality Markers (WARNING severity)
# ---------------------------------------------------------------------------

QUALITY_MARKERS = ["typography", "negative space", "hierarchy", "alignment", "focal point"]


def check_premium_quality(output: str, report: ValidationReport) -> None:
    """Check that the output mentions at least 3 of 5 premium quality markers."""
    output_lower = output.lower()
    found = [m for m in QUALITY_MARKERS if m in output_lower]
    missing = [m for m in QUALITY_MARKERS if m not in output_lower]

    if len(found) < 3:
        report.add(
            severity="warning",
            check="premium_quality_markers",
            message=(
                f"Only {len(found)}/5 premium quality markers found. "
                f"Missing: {', '.join(missing)}. "
                f"Found: {', '.join(found) if found else 'none'}"
            ),
        )


# ---------------------------------------------------------------------------
# Check 5 — Copy Character Limits (WARNING severity)
# ---------------------------------------------------------------------------

def check_copy_limits(output: str, report: ValidationReport) -> None:
    """Check Primary Text, Headline, and Description character limits."""

    # Primary Text: 125 chars max
    primary_texts = re.findall(
        r"Primary\s+Text\s*:\s*(.+?)(?:\n|$)", output
    )
    for i, text in enumerate(primary_texts, 1):
        text_clean = text.strip().strip("*").strip()
        if len(text_clean) > 125:
            report.add(
                severity="warning",
                check="copy_limits",
                message=f"Primary Text #{i} is {len(text_clean)} chars (max 125): '{text_clean[:50]}...'",
            )

    # Below-image Headline: 40 chars max
    headlines = re.findall(
        r"(?:^|\n)\s*\*?\*?Headline\*?\*?\s*:\s*(.+?)(?:\n|$)", output
    )
    # Filter to below-image headlines (longer ones, not on-image 8-12 word headlines)
    # We look for headlines in the BELOW-IMAGE section
    below_image_sections = re.split(r"BELOW[\-\s]IMAGE\s+AD\s+COPY", output, flags=re.IGNORECASE)
    for idx, section in enumerate(below_image_sections[1:], 1):
        bl_headlines = re.findall(
            r"Headline\s*:\s*(.+?)(?:\n|$)", section
        )
        for j, hl in enumerate(bl_headlines[:1], 1):  # Take first headline per section
            hl_clean = hl.strip().strip("*").strip()
            if len(hl_clean) > 40:
                report.add(
                    severity="warning",
                    check="copy_limits",
                    message=f"Below-image Headline (concept {idx}) is {len(hl_clean)} chars (max 40): '{hl_clean}'",
                )

    # Description: 30 chars max
    descriptions = re.findall(
        r"Description\s*:\s*(.+?)(?:\n|$)", output
    )
    for i, desc in enumerate(descriptions, 1):
        desc_clean = desc.strip().strip("*").strip()
        if len(desc_clean) > 30:
            report.add(
                severity="warning",
                check="copy_limits",
                message=f"Description #{i} is {len(desc_clean)} chars (max 30): '{desc_clean}'",
            )


# ---------------------------------------------------------------------------
# Check 6 — Pattern Break Presence (WARNING severity)
# ---------------------------------------------------------------------------

def check_pattern_breaks(output: str, report: ValidationReport) -> None:
    """Verify a Pattern Break field exists for every concept."""
    concept_headers = re.findall(r"CONCEPT\s+\[?\d+\]?", output, re.IGNORECASE)
    pattern_breaks = re.findall(
        r"Pattern\s+Break\s*:\s*(.+?)(?:\n|$)", output, re.IGNORECASE
    )

    num_concepts = len(concept_headers)
    valid_breaks = [
        pb for pb in pattern_breaks
        if pb.strip() and pb.strip().lower() not in ("n/a", "none", "tbd", "")
    ]

    if len(valid_breaks) < num_concepts:
        report.add(
            severity="warning",
            check="pattern_break_presence",
            message=(
                f"Found {len(valid_breaks)} Pattern Break fields "
                f"for {num_concepts} concepts. Each concept needs a pattern break."
            ),
        )


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def validate_output(output: str, num_concepts: int) -> ValidationReport:
    """Run all 6 validation checks and return a ValidationReport."""
    report = ValidationReport()

    check_terminology(output, report)
    check_blandness(output, report)
    check_inspiration_attribution(output, report)
    check_premium_quality(output, report)
    check_copy_limits(output, report)
    check_pattern_breaks(output, report)

    return report


# ---------------------------------------------------------------------------
# Format for Output
# ---------------------------------------------------------------------------

def format_validation_for_output(report: ValidationReport) -> str:
    """Format the validation report as a markdown section."""
    lines = [
        "# VALIDATION REPORT",
        "",
        report.summary(),
    ]

    if report.issues:
        lines.append("")
        lines.append("## Details")
        lines.append("")
        for issue in report.issues:
            icon = "❌" if issue.severity == "error" else "⚠️"
            loc = f" | `{issue.location}`" if issue.location else ""
            lines.append(f"- {icon} **[{issue.check}]** {issue.message}{loc}")

    return "\n".join(lines)
