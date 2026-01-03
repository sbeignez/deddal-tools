#!/usr/bin/env python3
"""
Merge CLL data:
1. Update old 'cll' case set code to '2x2-cll'
2. Add 2 missing PBL cases from new data
3. Delete duplicate new case set
"""

import os
import json
from pathlib import Path
from supabase import create_client

# Supabase configuration
SUPABASE_URL = "https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY not set")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Load new CLL cases from JSON
SEED_DATA_PATH = Path("/Users/trophee-mini/code/deddal/deddal-ios/Deddal/Data/Resources/SeedData")
with open(SEED_DATA_PATH / "2x2_cll_cases.json", 'r') as f:
    new_cll_cases = json.load(f)


def main():
    print("=" * 60)
    print("Merge CLL Data")
    print("=" * 60)
    print()

    # Step 1: Get old and new case set IDs
    old_cll = supabase.table('lib_casesets').select('id').eq('code', 'cll').execute()
    new_cll = supabase.table('lib_casesets').select('id').eq('code', '2x2-cll').execute()

    if not old_cll.data or not new_cll.data:
        print("ERROR: Could not find both case sets")
        return

    old_cll_id = old_cll.data[0]['id']
    new_cll_id = new_cll.data[0]['id']

    print(f"Old CLL ID: {old_cll_id}")
    print(f"New CLL ID: {new_cll_id}")
    print()

    # Step 2: Update old case set code to '2x2-cll'
    print("Step 1: Update old case set code 'cll' → '2x2-cll-with-algs'...")
    supabase.table('lib_casesets').update({
        'code': '2x2-cll-with-algs',
        'name': '2×2 CLL (with algorithms)',
        'expected_count': 42
    }).eq('id', old_cll_id).execute()
    print("  ✓ Updated")
    print()

    # Step 3: Find the 2 PBL cases in new data
    print("Step 2: Find PBL cases to add...")
    pbl_cases = [c for c in new_cll_cases if 'PBL' in c.get('title', '')]
    print(f"  Found {len(pbl_cases)} PBL cases:")
    for case in pbl_cases:
        print(f"    - {case['code']}: {case['title']}")
    print()

    # Step 4: Add PBL cases to old case set (update case_set_id)
    print("Step 3: Add PBL cases to old case set...")
    for case in pbl_cases:
        case_copy = case.copy()
        case_copy['case_set_id'] = old_cll_id

        # Insert or update
        supabase.table('lib_cases').upsert(case_copy).execute()
        print(f"  ✓ Added {case['code']}")
    print()

    # Step 5: Delete new case set and its cases
    print("Step 4: Delete duplicate new case set...")

    # Delete cases first (FK constraint)
    new_cases = supabase.table('lib_cases').select('id').eq('case_set_id', new_cll_id).execute()
    if new_cases.data:
        case_ids = [c['id'] for c in new_cases.data]
        supabase.table('lib_cases').delete().in_('id', case_ids).execute()
        print(f"  ✓ Deleted {len(case_ids)} cases")

    # Delete case set
    supabase.table('lib_casesets').delete().eq('id', new_cll_id).execute()
    print(f"  ✓ Deleted case set")
    print()

    # Step 6: Verify final state
    print("Step 5: Verify final state...")
    final_caseset = supabase.table('lib_casesets').select('*').eq('id', old_cll_id).execute()
    final_cases = supabase.table('lib_cases').select('id').eq('case_set_id', old_cll_id).execute()

    case_ids = [c['id'] for c in final_cases.data]
    final_algs = supabase.table('lib_algorithms').select('id').in_('case_id', case_ids).execute()

    cs = final_caseset.data[0]
    print(f"  Case Set: {cs['code']} ({cs['name']})")
    print(f"  Cases: {len(final_cases.data)}")
    print(f"  Algorithms: {len(final_algs.data)}")
    print()

    print("=" * 60)
    print("✅ Merge complete!")
    print(f"Result: 2×2 CLL with {len(final_cases.data)} cases and {len(final_algs.data)} algorithms")
    print("=" * 60)


if __name__ == "__main__":
    main()
