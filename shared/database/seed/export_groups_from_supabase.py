#!/usr/bin/env python3
"""
Export recognition groups from Supabase to JSON seed files.
This syncs the source of truth (Supabase database) to local JSON seed files.

Usage:
    python3 export_groups_from_supabase.py

Requirements:
    pip install supabase

Environment:
    SUPABASE_SERVICE_KEY - Your Supabase service role key (has read access)
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

# Path to seed data directory
SEED_DATA_PATH = Path(__file__).parent.parent.parent / "Deddal" / "Data" / "Resources" / "SeedData"

# Case files to update (only case files, not algorithm files)
CASE_FILES = [
    "3x3_cfop_f2l_cases.json",
    "3x3_cfop_oll_cases.json",
    "3x3_cfop_pll_cases.json",
    "3x3_cfop_pcll_cases.json",
    "3x3_cfop_oell_cases.json",
    "2x2_ortega_oll_cases.json",
    "2x2_ortega_pbl_cases.json",
    "3x3_lbl_cases.json",
]

def fetch_groups_from_supabase():
    """Fetch all cases with their code and groups from Supabase."""
    print("Fetching recognition groups from Supabase...")

    try:
        # Query all cases with code and groups
        response = supabase.table('lib_cases') \
            .select('code, groups') \
            .execute()

        cases = response.data

        # Filter out cases with null or empty groups array
        cases_with_groups = [c for c in cases if c.get('groups') and len(c['groups']) > 0]

        print(f"  Found {len(cases_with_groups)} cases with recognition groups")

        # Create a dict for quick lookup by code
        groups_by_code = {case['code']: case['groups'] for case in cases_with_groups}

        return groups_by_code

    except Exception as e:
        print(f"  ERROR: Failed to fetch from Supabase: {e}")
        return None

def update_json_file(file_path, groups_by_code):
    """Update a single JSON file with recognition groups."""
    if not file_path.exists():
        print(f"  ⚠️  File not found: {file_path.name}")
        return 0, 0

    print(f"\nProcessing {file_path.name}...")

    # Load JSON
    with open(file_path, 'r') as f:
        cases = json.load(f)

    updated_count = 0
    skipped_count = 0

    # Update each case with groups from database
    for case in cases:
        case_code = case.get('code')

        if not case_code:
            continue

        if case_code in groups_by_code:
            case['groups'] = groups_by_code[case_code]
            updated_count += 1
        else:
            # No groups in database for this case
            skipped_count += 1

    # Write back to file with pretty formatting
    with open(file_path, 'w') as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)

    print(f"  ✓ Updated {updated_count} cases")
    if skipped_count > 0:
        print(f"  ⚠️  Skipped {skipped_count} cases (no groups in database)")

    return updated_count, skipped_count

def main():
    """Main execution."""
    print("=" * 70)
    print("Export Recognition Groups: Supabase → JSON Seed Files")
    print("=" * 70)

    # Fetch groups from Supabase
    groups_by_code = fetch_groups_from_supabase()

    if groups_by_code is None:
        print("\n❌ Failed to fetch groups from Supabase")
        return

    if not groups_by_code:
        print("\n⚠️  No recognition groups found in database")
        return

    print(f"\nTotal unique case codes with groups: {len(groups_by_code)}")

    # Show sample of groups
    print("\nSample recognition groups:")
    sample_codes = list(groups_by_code.keys())[:3]
    for code in sample_codes:
        print(f"  {code}: {groups_by_code[code]}")

    # Confirm before updating
    print("\n" + "-" * 70)
    response = input("Proceed with updating JSON files? (yes/no): ")
    if response.lower() != 'yes':
        print("Update cancelled.")
        return

    # Update each JSON file
    total_updated = 0
    total_skipped = 0
    files_updated = 0

    for filename in CASE_FILES:
        file_path = SEED_DATA_PATH / filename
        updated, skipped = update_json_file(file_path, groups_by_code)

        if updated > 0:
            files_updated += 1

        total_updated += updated
        total_skipped += skipped

    # Summary
    print("\n" + "=" * 70)
    print("📊 Summary")
    print("=" * 70)
    print(f"Files updated: {files_updated}/{len(CASE_FILES)}")
    print(f"Total cases updated: {total_updated}")
    print(f"Total cases skipped: {total_skipped}")
    print(f"Groups synced from database: {len(groups_by_code)}")
    print("\n✅ Export complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
