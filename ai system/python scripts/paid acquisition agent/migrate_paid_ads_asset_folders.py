from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ASSETS_ROOT = REPO_ROOT / "docs" / "paid_ads_assets"


def migrate_campaign(campaign_dir: Path) -> None:
    """
    For a given campaign directory, move flat files into their
    new subfolders while keeping filenames unchanged.
    """
    # Map of substring -> subfolder name
    patterns = {
        "_campaign-structure.md": "campaign-structure",
        "_ad-creative_": "ad-creative",
        "_landing-page-and-cro_": "landing-page-and-cro",
        "_tracking-implementation-and-qa_": "tracking-implementation-and-qa",
        "-build-sheet.md": "build-sheet",
        "_ab-test-plan_": "ab-test-plan",
    }

    for entry in list(campaign_dir.iterdir()):
        if not entry.is_file() or not entry.name.endswith(".md"):
            continue
        name = entry.name
        for needle, folder in patterns.items():
            if needle in name:
                target_dir = campaign_dir / folder
                target_dir.mkdir(parents=True, exist_ok=True)
                target_path = target_dir / name
                if target_path.exists():
                    # If somehow already migrated, skip
                    break
                entry.rename(target_path)
                break


def main() -> None:
    if not ASSETS_ROOT.exists():
        print(f"No assets root at {ASSETS_ROOT}, nothing to migrate.")
        return

    for channel_dir in ASSETS_ROOT.iterdir():
        if not channel_dir.is_dir():
            continue
        for campaign_dir in channel_dir.iterdir():
            if not campaign_dir.is_dir():
                continue
            migrate_campaign(campaign_dir)

    print("Migration complete. Paid ads assets are now folderized by output type.")


if __name__ == "__main__":
    main()

