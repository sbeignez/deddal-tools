#!/usr/bin/env python3
"""
Update OLL cases JSON with recognition groups
Generated: November 14, 2025
"""

import json
from pathlib import Path

# OLL case recognition groups mapping
OLL_GROUPS = {
    # DOT CASES (1-4)
    "OLL-1": ["shape:dot", "edges:none_oriented", "corners:none_oriented", "pattern:mixed", "level:intermediate"],
    "OLL-2": ["shape:dot", "edges:none_oriented", "corners:none_oriented", "pattern:mixed", "level:intermediate"],
    "OLL-3": ["shape:dot", "edges:none_oriented", "corners:two_diagonal", "pattern:mixed", "level:intermediate"],
    "OLL-4": ["shape:dot", "edges:none_oriented", "corners:two_diagonal", "pattern:mixed", "level:intermediate"],

    # SQUARE CASES (5-8)
    "OLL-5": ["shape:square", "edges:none_oriented", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-6": ["shape:square", "edges:none_oriented", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-7": ["shape:square", "edges:none_oriented", "corners:two_adjacent", "pattern:mixed", "level:beginner"],
    "OLL-8": ["shape:square", "edges:none_oriented", "corners:two_adjacent", "pattern:mixed", "level:beginner"],

    # SMALL L CASES (9-12)
    "OLL-9": ["shape:l_shape", "edges:two_adjacent", "corners:one_oriented", "pattern:mixed", "level:intermediate"],
    "OLL-10": ["shape:l_shape", "edges:two_adjacent", "corners:one_oriented", "pattern:mixed", "level:intermediate"],
    "OLL-11": ["shape:l_shape", "edges:two_adjacent", "corners:two_diagonal", "pattern:mixed", "level:intermediate"],
    "OLL-12": ["shape:l_shape", "edges:two_adjacent", "corners:two_diagonal", "pattern:mixed", "level:intermediate"],

    # LIGHTNING BOLT CASES (13-16)
    "OLL-13": ["shape:lightning", "edges:two_adjacent", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-14": ["shape:lightning", "edges:two_adjacent", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-15": ["shape:lightning", "edges:two_adjacent", "corners:two_adjacent", "pattern:mixed", "level:intermediate"],
    "OLL-16": ["shape:lightning", "edges:two_adjacent", "corners:two_adjacent", "pattern:mixed", "level:intermediate"],

    # DOT CASES (17-20) - Advanced
    "OLL-17": ["shape:dot", "edges:none_oriented", "corners:two_adjacent", "pattern:mixed", "level:intermediate"],
    "OLL-18": ["shape:dot", "edges:none_oriented", "corners:two_adjacent", "pattern:mixed", "level:intermediate"],
    "OLL-19": ["shape:dot", "edges:none_oriented", "corners:three_oriented", "pattern:mixed", "level:intermediate"],
    "OLL-20": ["shape:dot", "edges:none_oriented", "corners:three_oriented", "pattern:mixed", "level:intermediate"],

    # OcLL CASES (21-27) - All edges oriented
    "OLL-21": ["pattern:corners_only", "shape:cross", "corners:two_diagonal", "edges:all_oriented", "level:beginner"],
    "OLL-22": ["pattern:corners_only", "shape:cross", "corners:two_adjacent", "edges:all_oriented", "level:beginner"],
    "OLL-23": ["pattern:corners_only", "shape:cross", "corners:two_diagonal", "edges:all_oriented", "level:beginner"],
    "OLL-24": ["pattern:corners_only", "shape:cross", "corners:two_adjacent", "edges:all_oriented", "level:beginner"],
    "OLL-25": ["pattern:corners_only", "shape:cross", "corners:two_adjacent", "edges:all_oriented", "level:beginner"],
    "OLL-26": ["pattern:corners_only", "shape:cross", "corners:one_oriented", "edges:all_oriented", "level:beginner"],
    "OLL-27": ["pattern:corners_only", "shape:cross", "corners:one_oriented", "edges:all_oriented", "level:beginner"],

    # P-SHAPE CASES (28-32)
    "OLL-28": ["shape:p_shape", "edges:two_adjacent", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-29": ["shape:p_shape", "edges:two_adjacent", "corners:two_adjacent", "pattern:mixed", "level:intermediate"],
    "OLL-30": ["shape:p_shape", "edges:two_adjacent", "corners:two_adjacent", "pattern:mixed", "level:intermediate"],
    "OLL-31": ["shape:p_shape", "edges:two_adjacent", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-32": ["shape:p_shape", "edges:two_adjacent", "corners:one_oriented", "pattern:mixed", "level:beginner"],

    # T-SHAPE CASES (33-40)
    "OLL-33": ["shape:t_shape", "edges:two_opposite", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-34": ["shape:t_shape", "edges:two_opposite", "corners:two_adjacent", "pattern:mixed", "level:intermediate"],
    "OLL-35": ["shape:t_shape", "edges:two_opposite", "corners:two_adjacent", "pattern:mixed", "level:intermediate"],
    "OLL-36": ["shape:t_shape", "edges:two_opposite", "corners:two_adjacent", "pattern:mixed", "level:intermediate"],
    "OLL-37": ["shape:t_shape", "edges:two_opposite", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-38": ["shape:t_shape", "edges:two_opposite", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-39": ["shape:t_shape", "edges:two_opposite", "corners:two_adjacent", "pattern:mixed", "level:beginner"],
    "OLL-40": ["shape:t_shape", "edges:two_opposite", "corners:two_adjacent", "pattern:mixed", "level:beginner"],

    # C-SHAPE / W-SHAPE CASES (41-48)
    "OLL-41": ["shape:c_shape", "edges:two_adjacent", "corners:two_diagonal", "pattern:mixed", "level:intermediate"],
    "OLL-42": ["shape:c_shape", "edges:two_adjacent", "corners:two_diagonal", "pattern:mixed", "level:intermediate"],
    "OLL-43": ["shape:t_shape", "edges:two_opposite", "corners:none_oriented", "pattern:mixed", "level:beginner"],
    "OLL-44": ["shape:t_shape", "edges:two_opposite", "corners:none_oriented", "pattern:mixed", "level:beginner"],
    "OLL-45": ["shape:t_shape", "edges:two_opposite", "corners:none_oriented", "pattern:mixed", "level:beginner"],
    "OLL-46": ["shape:w_shape", "edges:two_adjacent", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-47": ["shape:w_shape", "edges:two_adjacent", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-48": ["shape:w_shape", "edges:two_adjacent", "corners:two_adjacent", "pattern:mixed", "level:intermediate"],

    # I-SHAPE / FISH CASES (49-56)
    "OLL-49": ["shape:i_shape", "edges:two_opposite", "corners:two_diagonal", "pattern:mixed", "level:intermediate"],
    "OLL-50": ["shape:i_shape", "edges:two_opposite", "corners:two_diagonal", "pattern:mixed", "level:intermediate"],
    "OLL-51": ["shape:i_shape", "edges:two_opposite", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-52": ["shape:i_shape", "edges:two_opposite", "corners:one_oriented", "pattern:mixed", "level:beginner"],
    "OLL-53": ["shape:fish", "edges:two_adjacent", "corners:two_diagonal", "pattern:mixed", "level:intermediate"],
    "OLL-54": ["shape:fish", "edges:two_adjacent", "corners:two_diagonal", "pattern:mixed", "level:intermediate"],
    "OLL-55": ["shape:fish", "edges:two_adjacent", "corners:two_adjacent", "pattern:mixed", "level:advanced"],
    "OLL-56": ["shape:fish", "edges:two_adjacent", "corners:two_adjacent", "pattern:mixed", "level:advanced"],

    # LINE CASE (57)
    "OLL-57": ["shape:line", "edges:two_opposite", "corners:one_oriented", "pattern:mixed", "level:beginner"],
}

def main():
    # Path to OLL cases JSON file
    json_path = Path(__file__).parent.parent.parent / "Deddal/Data/Resources/SeedData/3x3_cfop_oll_cases.json"

    print(f"Reading OLL cases from: {json_path}")

    # Read JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        cases = json.load(f)

    print(f"Found {len(cases)} OLL cases")

    # Update each case with groups
    updated_count = 0
    for case in cases:
        code = case.get("code")
        if code in OLL_GROUPS:
            case["groups"] = OLL_GROUPS[code]
            updated_count += 1
            print(f"✓ Updated {code}: {len(OLL_GROUPS[code])} groups")
        else:
            print(f"⚠ No groups defined for {code}")

    # Write back to JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Successfully updated {updated_count}/{len(cases)} OLL cases")
    print(f"📝 Written to: {json_path}")

    # Print summary by shape
    shape_counts = {}
    for groups in OLL_GROUPS.values():
        shape = next((g.split(':')[1] for g in groups if g.startswith('shape:')), 'unknown')
        shape_counts[shape] = shape_counts.get(shape, 0) + 1

    print("\n📊 Distribution by shape:")
    for shape, count in sorted(shape_counts.items()):
        print(f"  {shape}: {count} cases")

if __name__ == "__main__":
    main()
