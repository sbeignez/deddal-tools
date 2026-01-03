#!/usr/bin/env python3
"""
Sync all seed data JSON files to Supabase.
This includes case sets, cases, and algorithms for parity and CLL.

Usage:
    python3 sync_seed_data.py

Requirements:
    pip install supabase

Environment:
    SUPABASE_URL - Your Supabase project URL
    SUPABASE_SERVICE_KEY - Your Supabase service role key (has write access)
"""

import json
import os
from pathlib import Path
from datetime import datetime
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY environment variable not set")
    print("Set it with: export SUPABASE_SERVICE_KEY='your-service-role-key'")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Base path to seed data
SEED_DATA_PATH = Path("/Users/trophee-mini/code/deddal/deddal-ios/Deddal/Data/Resources/SeedData")

# Case sets file
CASE_SETS_FILE = SEED_DATA_PATH / "all_case_sets.json"

# Case files to sync (parity + CLL)
CASE_FILES = [
    # Parity cases
    "4x4_parity_oll_cases.json",
    "4x4_parity_pll_cases.json",
    "5x5_parity_cases.json",
    "6x6_parity_oll_cases.json",
    "6x6_parity_pll_cases.json",
    "7x7_parity_cases.json",
    # CLL cases
    "2x2_cll_cases.json",
]

# Algorithm files to sync (parity + CLL - currently parity only)
ALGORITHM_FILES = [
    # Parity algorithms
    "4x4_parity_oll_algorithms.json",
    "4x4_parity_pll_algorithms.json",
    "5x5_parity_algorithms.json",
    "6x6_parity_oll_algorithms.json",
    "6x6_parity_pll_algorithms.json",
    "7x7_parity_algorithms.json",
    # Note: CLL algorithms not included yet (as per user request)
]


def load_case_sets():
    """Load case sets from JSON file."""
    print(f"Loading case sets from {CASE_SETS_FILE.name}...")

    if not CASE_SETS_FILE.exists():
        print(f"ERROR: File not found: {CASE_SETS_FILE}")
        return []

    with open(CASE_SETS_FILE, 'r') as f:
        case_sets = json.load(f)
        print(f"  Found {len(case_sets)} case sets")
        return case_sets


def load_cases():
    """Load all cases from JSON files."""
    all_cases = []

    for filename in CASE_FILES:
        file_path = SEED_DATA_PATH / filename

        if not file_path.exists():
            print(f"WARNING: File not found: {file_path}")
            continue

        print(f"Loading {filename}...")
        with open(file_path, 'r') as f:
            cases = json.load(f)
            print(f"  Found {len(cases)} cases")
            all_cases.extend(cases)

    return all_cases


def load_algorithms():
    """Load all algorithms from JSON files."""
    all_algorithms = []

    for filename in ALGORITHM_FILES:
        file_path = SEED_DATA_PATH / filename

        if not file_path.exists():
            print(f"WARNING: File not found: {file_path}")
            continue

        print(f"Loading {filename}...")
        with open(file_path, 'r') as f:
            algorithms = json.load(f)
            print(f"  Found {len(algorithms)} algorithms")
            all_algorithms.extend(algorithms)

    return all_algorithms


def sync_case_sets(case_sets):
    """Sync case sets to Supabase lib_casesets table."""
    if not case_sets:
        print("No case sets to sync")
        return True

    print(f"\nSyncing {len(case_sets)} case sets to Supabase...")

    # Map JSON fields to database columns
    db_case_sets = []
    for cs in case_sets:
        db_cs = {
            'id': cs['id'],
            'code': cs['code'],
            'name': cs['name'],
            'subtitle': cs.get('subtitle'),
            'pattern_from': cs.get('pattern_from'),
            'pattern_to': cs.get('pattern_to'),
            'expected_count': cs.get('expected_count'),
            'category': cs.get('category'),
            'created_at': cs.get('created_at'),
        }
        # Note: case_ids array and updated_at not included
        db_case_sets.append(db_cs)

    # Batch upsert (Supabase handles insert/update)
    batch_size = 50
    total_batches = (len(db_case_sets) + batch_size - 1) // batch_size

    for i in range(0, len(db_case_sets), batch_size):
        batch = db_case_sets[i:i + batch_size]
        batch_num = (i // batch_size) + 1

        print(f"  Batch {batch_num}/{total_batches}: Upserting {len(batch)} case sets...")

        try:
            response = supabase.table('lib_casesets').upsert(batch).execute()
            print(f"    ✓ Success")
        except Exception as e:
            print(f"    ERROR: {e}")
            return False

    return True


def sync_cases(cases):
    """Sync cases to Supabase lib_cases table."""
    if not cases:
        print("No cases to sync")
        return True

    print(f"\nSyncing {len(cases)} cases to Supabase...")

    # Map JSON fields to database columns
    db_cases = []
    for case in cases:
        db_case = {
            'id': case['id'],
            'code': case['code'],
            'case_set_id': case['case_set_id'],
            'title': case.get('title'),
            'long_name': case.get('long_name'),
            'kind': case.get('kind'),
            'pattern_from': case.get('pattern_from'),
            'pattern_to': case.get('pattern_to'),
            'scramble': case.get('scramble'),
            'notes': case.get('notes', ''),
            'story': case.get('story', ''),
            'description': case.get('description', ''),
            'image_asset_name': case.get('image_asset_name', ''),
            'difficulty': case.get('difficulty'),
            'popularity': case.get('popularity'),
            'groups': case.get('groups', []),
            'created_at': case.get('created_at'),
        }
        db_cases.append(db_case)

    # Batch upsert
    batch_size = 100
    total_batches = (len(db_cases) + batch_size - 1) // batch_size

    for i in range(0, len(db_cases), batch_size):
        batch = db_cases[i:i + batch_size]
        batch_num = (i // batch_size) + 1

        print(f"  Batch {batch_num}/{total_batches}: Upserting {len(batch)} cases...")

        try:
            response = supabase.table('lib_cases').upsert(batch).execute()
            print(f"    ✓ Success")
        except Exception as e:
            print(f"    ERROR: {e}")
            return False

    return True


def sync_algorithms(algorithms):
    """Sync algorithms to Supabase lib_algorithms table."""
    if not algorithms:
        print("No algorithms to sync")
        return True

    print(f"\nSyncing {len(algorithms)} algorithms to Supabase...")

    # Map JSON fields to database columns
    db_algorithms = []
    for alg in algorithms:
        db_alg = {
            'id': alg['id'],
            'case_id': alg['case_id'],
            'code': alg['code'],
            'name': alg.get('name'),
            'sequence': alg.get('sequence'),  # Algorithm moves
            'tags': alg.get('tags', []),  # Array of tags
            'popularity': alg.get('popularity'),
            'difficulty': alg.get('difficulty'),
            'created_at': alg.get('created_at'),
        }
        db_algorithms.append(db_alg)

    # Batch upsert
    batch_size = 100
    total_batches = (len(db_algorithms) + batch_size - 1) // batch_size

    for i in range(0, len(db_algorithms), batch_size):
        batch = db_algorithms[i:i + batch_size]
        batch_num = (i // batch_size) + 1

        print(f"  Batch {batch_num}/{total_batches}: Upserting {len(batch)} algorithms...")

        try:
            response = supabase.table('lib_algorithms').upsert(batch).execute()
            print(f"    ✓ Success")
        except Exception as e:
            print(f"    ERROR: {e}")
            return False

    return True


def main():
    """Main execution."""
    print("=" * 60)
    print("Sync Seed Data JSON → Supabase")
    print("=" * 60)

    # Load all data
    case_sets = load_case_sets()
    cases = load_cases()
    algorithms = load_algorithms()

    print("\n" + "=" * 60)
    print("Summary:")
    print(f"  Case Sets:  {len(case_sets)}")
    print(f"  Cases:      {len(cases)}")
    print(f"  Algorithms: {len(algorithms)}")
    print("=" * 60)

    if not case_sets and not cases and not algorithms:
        print("\nERROR: No data loaded from JSON files")
        return

    # Confirm before syncing
    response = input("\nProceed with sync to Supabase? (yes/no): ")
    if response.lower() != 'yes':
        print("Sync cancelled.")
        return

    # Sync in order: case_sets → cases → algorithms (for FK constraints)
    success = True

    if case_sets:
        success = success and sync_case_sets(case_sets)

    if cases and success:
        success = success and sync_cases(cases)

    if algorithms and success:
        success = success and sync_algorithms(algorithms)

    # Summary
    print("\n" + "=" * 60)
    if success:
        print("✅ Sync complete!")
        print("\nSynced:")
        if case_sets:
            print(f"  - {len(case_sets)} case sets")
        if cases:
            print(f"  - {len(cases)} cases")
        if algorithms:
            print(f"  - {len(algorithms)} algorithms")
    else:
        print("❌ Sync failed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
