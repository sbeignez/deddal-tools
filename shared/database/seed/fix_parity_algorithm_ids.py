#!/usr/bin/env python3
"""
Fix parity algorithm IDs - convert string IDs to proper UUIDs.
Also fix case_id references.
"""

import json
import uuid
from pathlib import Path

# Base paths
SEED_DATA_PATH = Path("/Users/trophee-mini/code/deddal/deddal-ios/Deddal/Data/Resources/SeedData")

# UUID v5 namespace
NAMESPACE = uuid.NAMESPACE_DNS

# Parity algorithm files
ALGORITHM_FILES = [
    "4x4_parity_oll_algorithms.json",
    "4x4_parity_pll_algorithms.json",
    "5x5_parity_algorithms.json",
    "6x6_parity_oll_algorithms.json",
    "6x6_parity_pll_algorithms.json",
    "7x7_parity_algorithms.json",
]


def generate_algorithm_uuid(alg_code):
    """Generate deterministic UUID v5 for an algorithm"""
    name = f"deddal.algorithm.{alg_code.lower()}"
    return str(uuid.uuid5(NAMESPACE, name))


def generate_case_uuid(case_code):
    """Generate deterministic UUID v5 for a case"""
    name = f"deddal.case.{case_code.lower()}"
    return str(uuid.uuid5(NAMESPACE, name))


def is_uuid(value):
    """Check if a string is a valid UUID"""
    try:
        uuid.UUID(value)
        return True
    except (ValueError, AttributeError):
        return False


def fix_algorithm_file(filename):
    """Update algorithm file to use UUIDs"""
    file_path = SEED_DATA_PATH / filename

    if not file_path.exists():
        print(f"  WARNING: {filename} not found")
        return 0

    # Load algorithms
    with open(file_path, 'r') as f:
        algorithms = json.load(f)

    # Update algorithm IDs and case_ids to proper UUIDs
    for alg in algorithms:
        alg_code = alg.get("code")
        old_id = alg.get("id")
        old_case_id = alg.get("case_id")

        # Fix algorithm ID
        if old_id and not is_uuid(old_id):
            new_id = generate_algorithm_uuid(alg_code)
            alg["id"] = new_id
            print(f"    {alg_code}: {old_id} → {new_id}")

        # Fix case_id reference (extract case code from old ID)
        if old_case_id and not is_uuid(old_case_id):
            # Convert case_id like "4x4-oll-parity-001" to case code like "4x4-OLL-PARITY"
            # This is tricky - we need to know the case code format
            # For parity cases, we can infer from the case_id pattern
            case_code_map = {
                "4x4-oll-parity-001": "4x4-OLL-PARITY",
                "4x4-pll-parity-001": "4x4-PLL-PARITY-ADJ",
                "4x4-pll-parity-002": "4x4-PLL-PARITY-OPP",
                "4x4-pll-parity-003": "4x4-PLL-PARITY-DIAG",
                "4x4-pll-parity-004": "4x4-PLL-PARITY-U",
                "5x5-parity-001": "5x5-EDGE-PARITY",
                "6x6-oll-parity-001": "6x6-OLL-PARITY",
                "6x6-pll-parity-001": "6x6-PLL-PARITY-ADJ",
                "6x6-pll-parity-002": "6x6-PLL-PARITY-OPP",
                "6x6-pll-parity-003": "6x6-PLL-PARITY-DIAG",
                "6x6-pll-parity-004": "6x6-PLL-PARITY-U",
                "7x7-parity-001": "7x7-EDGE-PARITY",
            }

            case_code = case_code_map.get(old_case_id)
            if case_code:
                new_case_id = generate_case_uuid(case_code)
                alg["case_id"] = new_case_id

    # Save updated algorithms
    with open(file_path, 'w') as f:
        json.dump(algorithms, f, indent=2, ensure_ascii=False)

    return len(algorithms)


def main():
    """Main execution"""
    print("=" * 60)
    print("Fix Parity Algorithm IDs")
    print("=" * 60)
    print()

    total_fixed = 0

    for filename in ALGORITHM_FILES:
        print(f"Processing {filename}...")
        count = fix_algorithm_file(filename)
        total_fixed += count
        print()

    print("=" * 60)
    print(f"✅ Fixed {total_fixed} parity algorithms!")
    print("=" * 60)


if __name__ == "__main__":
    main()
