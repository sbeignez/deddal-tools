#!/usr/bin/env python3
"""
Fix parity case IDs - convert string IDs to proper UUIDs.
"""

import json
import uuid
from pathlib import Path

# Base paths
SEED_DATA_PATH = Path("/Users/trophee-mini/code/deddal/deddal-ios/Deddal/Data/Resources/SeedData")

# UUID v5 namespace
NAMESPACE = uuid.NAMESPACE_DNS

# Parity case files
CASE_FILES = [
    "4x4_parity_oll_cases.json",
    "4x4_parity_pll_cases.json",
    "5x5_parity_cases.json",
    "6x6_parity_oll_cases.json",
    "6x6_parity_pll_cases.json",
    "7x7_parity_cases.json",
]


def generate_case_uuid(case_code):
    """Generate deterministic UUID v5 for a case"""
    name = f"deddal.case.{case_code.lower()}"
    return str(uuid.uuid5(NAMESPACE, name))


def fix_case_file(filename):
    """Update case file to use UUID for case IDs"""
    file_path = SEED_DATA_PATH / filename

    if not file_path.exists():
        print(f"  WARNING: {filename} not found")
        return 0

    # Load cases
    with open(file_path, 'r') as f:
        cases = json.load(f)

    # Update case IDs to proper UUIDs
    for case in cases:
        old_id = case.get("id")
        case_code = case.get("code")

        if old_id and not is_uuid(old_id):
            # Generate UUID from case code
            new_id = generate_case_uuid(case_code)
            case["id"] = new_id
            print(f"    {case_code}: {old_id} → {new_id}")

        # Remove updated_at field if present
        if "updated_at" in case:
            del case["updated_at"]

    # Save updated cases
    with open(file_path, 'w') as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)

    return len(cases)


def is_uuid(value):
    """Check if a string is a valid UUID"""
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def main():
    """Main execution"""
    print("=" * 60)
    print("Fix Parity Case IDs")
    print("=" * 60)
    print()

    total_fixed = 0

    for filename in CASE_FILES:
        print(f"Processing {filename}...")
        count = fix_case_file(filename)
        total_fixed += count
        print()

    print("=" * 60)
    print(f"✅ Fixed {total_fixed} parity cases!")
    print("=" * 60)


if __name__ == "__main__":
    main()
