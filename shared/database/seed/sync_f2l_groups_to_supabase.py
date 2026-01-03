#!/usr/bin/env python3
"""
Sync F2L recognition groups from local JSON to Supabase database.

After auto-categorizing F2L cases with 7 new recognition categories,
this script updates the Supabase database to keep it as source of truth.
"""

import json
import os
import sys
from pathlib import Path
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

# Path to F2L cases JSON
F2L_JSON_PATH = Path(__file__).parent.parent.parent / "Deddal/Data/Resources/SeedData/3x3_cfop_f2l_cases.json"

def sync_f2l_groups_to_supabase():
    """Sync F2L groups from JSON to Supabase lib_cases table."""

    # Check for service key
    if not SUPABASE_SERVICE_KEY:
        print("❌ Error: SUPABASE_SERVICE_KEY environment variable not set")
        print("\nSet it with:")
        print("export SUPABASE_SERVICE_KEY='your-service-key-here'")
        return

    # Initialize Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

    print("=" * 80)
    print("Sync F2L Recognition Groups: JSON → Supabase Database")
    print("=" * 80)

    # Load F2L JSON
    print(f"\nLoading F2L cases from: {F2L_JSON_PATH}")
    with open(F2L_JSON_PATH, 'r') as f:
        f2l_cases = json.load(f)

    print(f"  Loaded {len(f2l_cases)} F2L cases")

    # Show sample of what will be updated
    sample_case = f2l_cases[0]
    print(f"\nSample case to sync:")
    print(f"  Code: {sample_case['code']}")
    print(f"  Groups ({len(sample_case.get('groups', []))}): {sample_case.get('groups', [])}")

    # Confirm before proceeding (unless --yes flag)
    auto_confirm = '--yes' in sys.argv or '-y' in sys.argv

    if not auto_confirm:
        print("\n" + "-" * 80)
        confirm = input(f"Proceed with updating {len(f2l_cases)} F2L cases in Supabase? (yes/no): ")
        if confirm.lower() != 'yes':
            print("\n❌ Sync cancelled")
            return
    else:
        print("\n" + "-" * 80)
        print(f"Auto-confirming: Proceeding with update of {len(f2l_cases)} F2L cases")

    print("\n" + "=" * 80)
    print("Syncing to Supabase...")
    print("=" * 80)

    updated_count = 0
    error_count = 0

    for case in f2l_cases:
        code = case['code']
        groups = case.get('groups', [])

        try:
            # Update the case in Supabase
            response = supabase.table('lib_cases') \
                .update({'groups': groups}) \
                .eq('code', code) \
                .execute()

            # Check if update was successful
            if response.data:
                updated_count += 1
                print(f"  ✓ {code}: Updated with {len(groups)} groups")
            else:
                print(f"  ⚠️  {code}: No matching record found in database")
                error_count += 1

        except Exception as e:
            print(f"  ❌ {code}: Error - {str(e)}")
            error_count += 1

    # Summary
    print("\n" + "=" * 80)
    print("📊 Summary")
    print("=" * 80)
    print(f"Cases updated: {updated_count}/{len(f2l_cases)}")
    print(f"Errors/Warnings: {error_count}")

    if error_count == 0:
        print("\n✅ All F2L cases synced successfully to Supabase!")
    else:
        print(f"\n⚠️  Sync completed with {error_count} errors/warnings")

    print("=" * 80)

if __name__ == "__main__":
    sync_f2l_groups_to_supabase()
