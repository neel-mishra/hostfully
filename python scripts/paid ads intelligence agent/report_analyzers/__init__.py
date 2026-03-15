"""Platform-specific report analyzers for paid ads intelligence."""

from .meta_ads_analyzer import generate_meta_report
from .google_ads_analyzer import generate_google_report

__all__ = ["generate_meta_report", "generate_google_report"]
