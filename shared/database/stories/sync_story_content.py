#!/usr/bin/env python3
"""
Sync case and algorithm story content to Supabase.

The script reads Resources/Stories/index.json, loads each referenced Markdown
file, and updates the `story` columns in lib_cases / lib_algorithms so the app's
database is always aligned with the validated source files. It also refreshes
word counts and the root `last_updated` timestamp in index.json.

Usage:
    python3 sync_story_content.py [--dry-run] [--verbose]

Options:
    --dry-run     Preview changes without uploading to database
    --verbose     Show detailed output

Environment:
    SUPABASE_URL          - Supabase project URL (required).
    SUPABASE_SERVICE_KEY  - service role key with write access (required).

Dependencies:
    pip install supabase
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

try:
    from supabase import Client, create_client
except ImportError:
    sys.stderr.write("ERROR: supabase package not installed.\n")
    sys.stderr.write("Install it with: pip install supabase\n")
    sys.exit(1)

STORIES_ROOT = Path(__file__).parent
INDEX_PATH = STORIES_ROOT / "index.json"

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL:
    sys.stderr.write("ERROR: SUPABASE_URL environment variable not set.\n")
    sys.stderr.write("Set it with: export SUPABASE_URL='https://your-project.supabase.co'\n")
    sys.exit(1)

if not SUPABASE_SERVICE_KEY:
    sys.stderr.write("ERROR: SUPABASE_SERVICE_KEY environment variable not set.\n")
    sys.stderr.write("Set it with: export SUPABASE_SERVICE_KEY='your-service-role-key'\n")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_index() -> Dict:
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"index.json not found at {INDEX_PATH}")

    with INDEX_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_story(rel_path: str) -> str:
    path = STORIES_ROOT / rel_path
    if not path.exists():
        raise FileNotFoundError(f"Story file missing: {rel_path}")
    try:
        content = path.read_text(encoding="utf-8").strip()
        if not content:
            raise ValueError(f"Empty story content in {rel_path}")
        if len(content) > 100000:  # 100KB limit
            raise ValueError(f"Story too large ({len(content)} chars) in {rel_path}")
        return content
    except UnicodeDecodeError as e:
        raise ValueError(f"Invalid UTF-8 encoding in {rel_path}: {e}")
    except Exception as e:
        raise RuntimeError(f"Failed to read {rel_path}: {e}")


def collect_case_payloads(index_data: Dict) -> List[Tuple[Dict, str, int]]:
    payloads = []
    for entry in index_data.get("case_stories", []):
        content = read_story(entry["file_path"])
        words = len([w for w in content.split() if w])
        payloads.append((entry, content, words))
    return payloads


def collect_algorithm_payloads(index_data: Dict) -> List[Tuple[Dict, str, int]]:
    payloads = []
    for entry in index_data.get("algorithm_stories", []):
        content = read_story(entry["file_path"])
        words = len([w for w in content.split() if w])
        payloads.append((entry, content, words))
    return payloads


def fetch_ids(table: str, codes: List[str]) -> Dict[str, str]:
    if not codes:
        return {}

    response = (
        supabase.table(table)
        .select("id, code")
        .in_("code", codes)
        .execute()
    )

    if getattr(response, "error", None):
        raise RuntimeError(f"Supabase error fetching {table}: {response.error}")

    data = getattr(response, "data", response)
    return {row["code"]: row["id"] for row in data}


def update_rows(table: str, rows: List[Dict], dry_run: bool = False) -> None:
    if not rows:
        return

    batch_size = 10  # Smaller batches for UPDATE operations
    total = len(rows)
    total_batches = (total + batch_size - 1) // batch_size

    if dry_run:
        print(f"[DRY RUN] Would update {total} rows in {table}")
        for i, row in enumerate(rows[:3], 1):
            story_len = len(row.get('story', ''))
            print(f"  Sample {i}: ID={row.get('id')} Story={story_len} chars")
        if total > 3:
            print(f"  ... and {total - 3} more rows")
        return

    for i in range(0, total, batch_size):
        batch = rows[i : i + batch_size]
        batch_num = (i // batch_size) + 1
        print(f"[{table}] Batch {batch_num}/{total_batches}: updating {len(batch)} rows...")

        # Update each row individually to only update the story column
        for row in batch:
            response = supabase.table(table).update({"story": row["story"]}).eq("id", row["id"]).execute()
            if getattr(response, "error", None):
                raise RuntimeError(f"Supabase update error for {table}: {response.error}")


def sync_cases(case_payloads: List[Tuple[Dict, str, int]], timestamp: str, dry_run: bool = False) -> None:
    codes = [entry["case_code"] for entry, _, _ in case_payloads]
    ids = fetch_ids("lib_cases", codes)

    missing = sorted(set(codes) - set(ids.keys()))
    if missing:
        raise RuntimeError(f"Missing lib_cases rows for codes: {', '.join(missing)}")

    rows = []
    for entry, content, _ in case_payloads:
        rows.append(
            {
                "id": ids[entry["case_code"]],
                "story": content,
            }
        )

    if rows:
        update_rows("lib_cases", rows, dry_run=dry_run)
        if not dry_run:
            print(f"✓ Updated {len(rows)} case stories")


def sync_algorithms(alg_payloads: List[Tuple[Dict, str, int]], timestamp: str, dry_run: bool = False) -> None:
    codes = [entry["algorithm_code"] for entry, _, _ in alg_payloads]
    ids = fetch_ids("lib_algorithms", codes)

    missing = sorted(set(codes) - set(ids.keys()))
    if missing:
        raise RuntimeError(f"Missing lib_algorithms rows for codes: {', '.join(missing)}")

    rows = []
    for entry, content, _ in alg_payloads:
        rows.append(
            {
                "id": ids[entry["algorithm_code"]],
                "story": content,
            }
        )

    if rows:
        update_rows("lib_algorithms", rows, dry_run=dry_run)
        if not dry_run:
            print(f"✓ Updated {len(rows)} algorithm stories")


def update_index_file(index_data: Dict, case_payloads, alg_payloads, timestamp: str) -> None:
    for entry, _, words in case_payloads:
        entry["word_count"] = words
        entry.setdefault("tags", entry.get("tags", []))
        entry["last_modified"] = timestamp

    for entry, _, words in alg_payloads:
        entry["word_count"] = words
        entry.setdefault("tags", entry.get("tags", []))
        entry["last_modified"] = timestamp

    index_data["last_updated"] = timestamp

    with INDEX_PATH.open("w", encoding="utf-8") as f:
        json.dump(index_data, f, indent=2)
        f.write("\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sync story content from markdown files to Supabase database"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without uploading to database or modifying index.json"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    timestamp = iso_now()

    print("=== Sync Stories → Supabase ===")
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")

    index_data = load_index()
    print(f"✓ Loaded index.json from {INDEX_PATH}")

    case_payloads = collect_case_payloads(index_data)
    alg_payloads = collect_algorithm_payloads(index_data)

    if not case_payloads and not alg_payloads:
        print("No stories found to sync.")
        return

    total_words = sum(words for _, _, words in case_payloads + alg_payloads)
    print(f"\n📚 Found:")
    print(f"   {len(case_payloads)} case stories")
    print(f"   {len(alg_payloads)} algorithm stories")
    print(f"   {total_words} total words")

    if args.verbose:
        print("\nCase stories:")
        for entry, _, words in case_payloads[:5]:
            print(f"  - {entry['case_code']}: {words} words")
        if len(case_payloads) > 5:
            print(f"  ... and {len(case_payloads) - 5} more")

        print("\nAlgorithm stories:")
        for entry, _, words in alg_payloads[:5]:
            print(f"  - {entry['algorithm_code']}: {words} words")
        if len(alg_payloads) > 5:
            print(f"  ... and {len(alg_payloads) - 5} more")

    print(f"\n📤 Syncing to Supabase...")
    sync_cases(case_payloads, timestamp, dry_run=args.dry_run)
    sync_algorithms(alg_payloads, timestamp, dry_run=args.dry_run)

    if not args.dry_run:
        print(f"\n💾 Updating index.json...")
        update_index_file(index_data, case_payloads, alg_payloads, timestamp)
        print(f"   Timestamp: {timestamp}")
        print("\n✅ Story sync complete.")
    else:
        print(f"\n✅ Dry run complete. Run without --dry-run to apply changes.")


if __name__ == "__main__":
    main()
