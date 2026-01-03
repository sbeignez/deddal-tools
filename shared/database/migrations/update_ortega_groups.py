#!/usr/bin/env python3
"""
Update 2x2 Ortega cases JSON with recognition groups
Generated: November 14, 2025
"""

import json
from pathlib import Path

# Ortega OLL recognition groups (7 cases - corner orientation only)
ORTEGA_OLL_GROUPS = {
    "Ortega-OLL-1": ["pattern:corners_only", "shape:sune", "corners:one_oriented", "level:beginner"],
    "Ortega-OLL-2": ["pattern:corners_only", "shape:antisune", "corners:one_oriented", "level:beginner"],
    "Ortega-OLL-3": ["pattern:corners_only", "shape:u", "corners:two_diagonal", "level:beginner"],
    "Ortega-OLL-4": ["pattern:corners_only", "shape:pi", "corners:two_adjacent", "level:beginner"],
    "Ortega-OLL-5": ["pattern:corners_only", "shape:t", "corners:two_adjacent", "level:beginner"],
    "Ortega-OLL-6": ["pattern:corners_only", "shape:h", "corners:two_diagonal", "level:beginner"],
    "Ortega-OLL-7": ["pattern:corners_only", "shape:l", "corners:two_adjacent", "level:beginner"],
}

# Ortega PBL recognition groups (5 cases - permute both layers)
ORTEGA_PBL_GROUPS = {
    "Ortega-PBL-1": ["type:adjacent_swap", "layers:one_layer", "level:beginner"],
    "Ortega-PBL-2": ["type:diagonal_swap", "layers:one_layer", "level:intermediate"],
    "Ortega-PBL-3": ["type:diagonal_swap", "layers:both_layers", "level:beginner"],
    "Ortega-PBL-4": ["type:adjacent_swap", "layers:both_layers", "level:intermediate"],
    "Ortega-PBL-5": ["type:mixed_swap", "layers:both_layers", "level:beginner"],
}

def update_json_file(file_path, groups_mapping, case_type):
    """Update a JSON file with recognition groups"""
    print(f"\nProcessing {case_type} cases from: {file_path}")

    # Read JSON file
    with open(file_path, 'r', encoding='utf-8') as f:
        cases = json.load(f)

    print(f"Found {len(cases)} {case_type} cases")

    # Update each case with groups
    updated_count = 0
    for case in cases:
        code = case.get("code")
        if code in groups_mapping:
            case["groups"] = groups_mapping[code]
            updated_count += 1
            print(f"✓ Updated {code}: {len(groups_mapping[code])} groups")
        else:
            print(f"⚠ No groups defined for {code}")

    # Write back to JSON file
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)

    print(f"✅ Successfully updated {updated_count}/{len(cases)} {case_type} cases")
    return updated_count

def main():
    # Paths to Ortega cases JSON files
    base_path = Path(__file__).parent.parent.parent / "Deddal/Data/Resources/SeedData"
    oll_path = base_path / "2x2_ortega_oll_cases.json"
    pbl_path = base_path / "2x2_ortega_pbl_cases.json"

    # Update OLL cases
    oll_count = update_json_file(oll_path, ORTEGA_OLL_GROUPS, "Ortega OLL")

    # Update PBL cases
    pbl_count = update_json_file(pbl_path, ORTEGA_PBL_GROUPS, "Ortega PBL")

    # Print final summary
    print(f"\n{'='*60}")
    print(f"📊 FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"Ortega OLL: {oll_count}/7 cases updated")
    print(f"Ortega PBL: {pbl_count}/5 cases updated")
    print(f"Total: {oll_count + pbl_count}/12 2x2 Ortega cases updated")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
