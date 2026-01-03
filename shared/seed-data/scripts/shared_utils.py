"""
Shared Utilities for Seed Data Export Scripts

Common configuration and utilities used by both stage and deploy scripts.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Path configuration
SCRIPT_DIR = Path(__file__).parent.parent
STAGING_ROOT = SCRIPT_DIR / "staging"
IOS_SEED_DATA_DIR = SCRIPT_DIR / "../DeddalInfra/Infrastructure/Persistence/SeedData"
DEPLOYMENTS_DIR = SCRIPT_DIR / "deployments"
BACKUPS_DIR = SCRIPT_DIR / "backups"
CONFIG_FILE = SCRIPT_DIR / "scripts" / "config.yaml"


def print_header(title: str):
    """Print formatted section header."""
    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{title}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")


def print_banner():
    """Print main banner."""
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}SEED DATA EXPORT{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")


def format_json(data: List[Dict[str, Any]]) -> str:
    """
    Format JSON with custom array formatting for better readability.

    Arrays of objects are formatted with one object per line (compact objects).
    Makes case_ids and other arrays more human-readable.
    """
    # Use standard pretty-printing; avoid regex compaction (which can backtrack
    # catastrophically on markdown-heavy fields).
    return json.dumps(data, indent=2, ensure_ascii=False)


def get_latest_staged_export() -> Path | None:
    """Get the most recent staged export directory."""
    if not STAGING_ROOT.exists():
        return None

    staged_dirs = sorted([d for d in STAGING_ROOT.iterdir() if d.is_dir()], reverse=True)
    return staged_dirs[0] if staged_dirs else None


def list_staged_exports() -> List[Path]:
    """List all staged export directories."""
    if not STAGING_ROOT.exists():
        return []

    return sorted([d for d in STAGING_ROOT.iterdir() if d.is_dir()], reverse=True)
