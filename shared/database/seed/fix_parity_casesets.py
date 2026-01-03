#!/usr/bin/env python3
"""
Fix parity case set IDs - add proper UUIDs to all_case_sets.json
and update parity case files to reference them.
"""

import json
import uuid
from pathlib import Path

# Base paths
SEED_DATA_PATH = Path("/Users/trophee-mini/code/deddal/deddal-ios/Deddal/Data/Resources/SeedData")
CASE_SETS_FILE = SEED_DATA_PATH / "all_case_sets.json"

# UUID v5 namespace
NAMESPACE = uuid.NAMESPACE_DNS

# Parity case set definitions
PARITY_CASE_SETS = [
    {
        "code": "4x4-oll-parity",
        "name": "4×4 OLL Parity",
        "subtitle": "Single Edge Flip Parity",
        "pattern_from": "Pre-OLL with Edge Flip",
        "pattern_to": "OLL Ready State",
        "expected_count": 1,
        "category": "4x4x4 - Parity",
    },
    {
        "code": "4x4-pll-parity",
        "name": "4×4 PLL Parity",
        "subtitle": "Edge Swap Parity",
        "pattern_from": "OLL Complete with Edge Swap",
        "pattern_to": "PLL Ready State",
        "expected_count": 4,
        "category": "4x4x4 - Parity",
    },
    {
        "code": "5x5-parity",
        "name": "5×5 Edge Parity",
        "subtitle": "Last Two Edges Parity",
        "pattern_from": "Final Two Edges",
        "pattern_to": "All Edges Paired",
        "expected_count": 1,
        "category": "5x5x5 - Parity",
    },
    {
        "code": "6x6-oll-parity",
        "name": "6×6 OLL Parity",
        "subtitle": "Single Edge Flip Parity",
        "pattern_from": "Pre-OLL with Edge Flip",
        "pattern_to": "OLL Ready State",
        "expected_count": 1,
        "category": "6x6x6 - Parity",
    },
    {
        "code": "6x6-pll-parity",
        "name": "6×6 PLL Parity",
        "subtitle": "Edge Swap Parity",
        "pattern_from": "OLL Complete with Edge Swap",
        "pattern_to": "PLL Ready State",
        "expected_count": 4,
        "category": "6x6x6 - Parity",
    },
    {
        "code": "7x7-parity",
        "name": "7×7 Edge Parity",
        "subtitle": "Last Two Edges Parity",
        "pattern_from": "Final Two Edges",
        "pattern_to": "All Edges Paired",
        "expected_count": 1,
        "category": "7x7x7 - Parity",
    },
]

# Mapping from old string IDs to codes
OLD_TO_CODE = {
    "4x4-oll-parity-set": "4x4-oll-parity",
    "4x4-pll-parity-set": "4x4-pll-parity",
    "5x5-parity-set": "5x5-parity",
    "6x6-oll-parity-set": "6x6-oll-parity",
    "6x6-pll-parity-set": "6x6-pll-parity",
    "7x7-parity-set": "7x7-parity",
}


def generate_caseset_uuid(code):
    """Generate deterministic UUID v5 for a case set"""
    name = f"deddal.caseset.{code.lower()}"
    return str(uuid.uuid5(NAMESPACE, name))


def add_parity_casesets():
    """Add parity case sets to all_case_sets.json"""
    # Load existing case sets
    with open(CASE_SETS_FILE, 'r') as f:
        case_sets = json.load(f)

    # Generate parity case set entries
    new_case_sets = []
    for cs_def in PARITY_CASE_SETS:
        case_set = {
            "id": generate_caseset_uuid(cs_def["code"]),
            "code": cs_def["code"],
            "name": cs_def["name"],
            "subtitle": cs_def["subtitle"],
            "pattern_from": cs_def["pattern_from"],
            "pattern_to": cs_def["pattern_to"],
            "expected_count": cs_def["expected_count"],
            "category": cs_def["category"],
            "created_at": "2025-12-02T00:00:00Z",
            "case_ids": []
        }
        new_case_sets.append(case_set)
        print(f"  + {case_set['code']}: {case_set['id']}")

    # Insert before the 2x2-cll entry (which is last)
    case_sets = case_sets[:-1] + new_case_sets + case_sets[-1:]

    # Save updated case sets
    with open(CASE_SETS_FILE, 'w') as f:
        json.dump(case_sets, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Added {len(new_case_sets)} parity case sets to all_case_sets.json")

    return new_case_sets


def fix_parity_case_files(case_sets):
    """Update parity case files to use proper case_set_id UUIDs"""
    # Build mapping from code to UUID
    code_to_uuid = {cs["code"]: cs["id"] for cs in case_sets}

    # Parity case files
    case_files = [
        ("4x4_parity_oll_cases.json", "4x4-oll-parity"),
        ("4x4_parity_pll_cases.json", "4x4-pll-parity"),
        ("5x5_parity_cases.json", "5x5-parity"),
        ("6x6_parity_oll_cases.json", "6x6-oll-parity"),
        ("6x6_parity_pll_cases.json", "6x6-pll-parity"),
        ("7x7_parity_cases.json", "7x7-parity"),
    ]

    for filename, case_set_code in case_files:
        file_path = SEED_DATA_PATH / filename

        if not file_path.exists():
            print(f"  WARNING: {filename} not found")
            continue

        # Load cases
        with open(file_path, 'r') as f:
            cases = json.load(f)

        # Update case_set_id to proper UUID
        correct_uuid = code_to_uuid[case_set_code]
        for case in cases:
            old_id = case.get("case_set_id")
            case["case_set_id"] = correct_uuid

        # Save updated cases
        with open(file_path, 'w') as f:
            json.dump(cases, f, indent=2, ensure_ascii=False)

        print(f"  ✓ Fixed {filename}: {len(cases)} cases updated")

    print(f"\n✓ Fixed {len(case_files)} parity case files")


def main():
    """Main execution"""
    print("=" * 60)
    print("Fix Parity Case Set IDs")
    print("=" * 60)
    print()

    # Step 1: Add parity case sets to all_case_sets.json
    print("STEP 1: Add parity case sets to all_case_sets.json")
    print("-" * 60)
    new_case_sets = add_parity_casesets()
    print()

    # Step 2: Fix parity case files
    print("STEP 2: Fix parity case files")
    print("-" * 60)
    fix_parity_case_files(new_case_sets)
    print()

    print("=" * 60)
    print("✅ All parity case sets fixed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
