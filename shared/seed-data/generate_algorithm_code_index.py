#!/usr/bin/env python3
"""
Generate algorithm code normalization index from seed data JSON files.

This script reads all algorithm JSON files and creates a pre-computed index
mapping normalized algorithm sequences to their canonical codes.

Output: DeddalInfra/Infrastructure/Persistence/SeedData/seeddata_algorithm_code_index.json
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


# Algorithm JSON files to process
ALGORITHM_FILES = [
    "seeddata_algorithms_f2l-ls-fr.json",
    "seeddata_algorithms_f2l-ls-fl.json",
    "seeddata_algorithms_oll.json",
    "seeddata_algorithms_pll.json",
    "seeddata_algorithms_coll.json",
    "seeddata_algorithms_oell.json",
    "seeddata_algorithms_ocll.json",
    "seeddata_algorithms_pcll.json",
    "seeddata_algorithms_pell.json",
    "seeddata_algorithms_zbll.json",
    "seeddata_algorithms_roux-cmll.json",
    "seeddata_algorithms_roux-lse-eo.json",
    "seeddata_algorithms_roux-lse-ulur.json",
    "seeddata_algorithms_roux-lse-l4e.json",
    "seeddata_algorithms_ortega-oll.json",
    "seeddata_algorithms_ortega-pbl.json",
    "seeddata_algorithms_2x2-cll-with-algs.json",
    "seeddata_algorithms_4x4-oll-parity.json",
    "seeddata_algorithms_4x4-pll-parity.json",
    "seeddata_algorithms_5x5-parity.json",
    "seeddata_algorithms_6x6-oll-parity.json",
    "seeddata_algorithms_6x6-pll-parity.json",
    "seeddata_algorithms_7x7-parity.json",
]


def normalize_sequence(raw: str) -> str:
    """
    Normalize algorithm sequence to canonical form.

    Replicates normalization logic from LegacyAlgorithmCodeResolver.normalizeSequence().

    Rules:
    - Remove spaces, parentheses, brackets
    - Uppercase all moves (R, U, F, L, D, B, M, S, E, r, l, u, d, f, b)
    - Preserve modifiers (', 2)
    - Preserve wide moves (w)
    - Strip leading/trailing cube rotations (X, Y, Z with modifiers)

    Args:
        raw: Raw algorithm sequence string

    Returns:
        Normalized sequence string with spaces between moves
    """
    # Remove spaces, parentheses, brackets
    filtered = raw.replace(" ", "").replace("(", "").replace(")", "")
    filtered = filtered.replace("[", "").replace("]", "")

    # Parse tokens
    tokens = []
    chars = list(filtered)
    index = 0

    while index < len(chars):
        # Start with current character (uppercase)
        token = chars[index].upper()

        # Check for wide move indicator (w)
        if index + 1 < len(chars):
            potential_wide = chars[index + 1]
            if potential_wide in ('w', 'W'):
                token += 'w'
                index += 1

        # Check for modifier (' or 2)
        if index + 1 < len(chars):
            next_char = chars[index + 1]
            if next_char in ("'", "2"):
                token += next_char
                index += 1

        tokens.append(token)
        index += 1

    # Strip leading/trailing cube rotations
    rotation_set = {"X", "X'", "X2", "Y", "Y'", "Y2", "Z", "Z'", "Z2"}

    while tokens and tokens[0] in rotation_set:
        tokens.pop(0)

    while tokens and tokens[-1] in rotation_set:
        tokens.pop()

    return " ".join(tokens)


def load_algorithms_from_json(file_path: Path) -> List[Dict]:
    """Load algorithm list from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  Warning: File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"⚠️  Warning: Invalid JSON in {file_path}: {e}")
        return []


def build_index(seed_data_dir: Path) -> Tuple[Dict[str, str], List[str]]:
    """
    Build algorithm code normalization index.

    Args:
        seed_data_dir: Path to DeddalInfra/Infrastructure/Persistence/SeedData/

    Returns:
        Tuple of (index dict, list of conflict warnings)
    """
    index: Dict[str, str] = {}
    conflicts: List[str] = []
    total_algorithms = 0

    for filename in ALGORITHM_FILES:
        file_path = seed_data_dir / filename
        algorithms = load_algorithms_from_json(file_path)

        if not algorithms:
            continue

        print(f"Processing {filename}: {len(algorithms)} algorithms")
        total_algorithms += len(algorithms)

        for algo in algorithms:
            code = algo.get("code")
            sequence = algo.get("sequence")

            if not code or not sequence:
                print(f"  ⚠️  Skipping algorithm with missing code or sequence: {algo.get('id')}")
                continue

            # Normalize sequence
            normalized = normalize_sequence(sequence)

            # Check for conflicts
            if normalized in index:
                existing_code = index[normalized]
                if existing_code != code:
                    conflict_msg = f"Conflict: '{normalized}' → [{existing_code}, {code}]"
                    conflicts.append(conflict_msg)
            else:
                index[normalized] = code

    print(f"\n✅ Processed {total_algorithms} algorithms from {len(ALGORITHM_FILES)} files")
    print(f"✅ Generated {len(index)} unique normalized sequence mappings")

    return index, conflicts


def main():
    """Generate algorithm code normalization index."""
    # Determine paths
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    seed_data_dir = project_root / "DeddalInfra" / "Infrastructure" / "Persistence" / "SeedData"
    output_file = seed_data_dir / "seeddata_algorithm_code_index.json"

    print("=" * 60)
    print("Algorithm Code Index Generator")
    print("=" * 60)
    print(f"Seed data directory: {seed_data_dir}")
    print(f"Output file: {output_file}")
    print()

    # Verify seed data directory exists
    if not seed_data_dir.exists():
        print(f"❌ Error: Seed data directory not found: {seed_data_dir}")
        return 1

    # Build index
    index, conflicts = build_index(seed_data_dir)

    # Log conflicts (if any)
    if conflicts:
        print(f"\n⚠️  Found {len(conflicts)} conflicting sequences:")
        for i, conflict in enumerate(conflicts[:10], 1):  # Show first 10
            print(f"  {i}. {conflict}")
        if len(conflicts) > 10:
            print(f"  ... and {len(conflicts) - 10} more")

    # Create output JSON
    output = {
        "index": index,
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_mappings": len(index),
        "conflicts": len(conflicts),
        "algorithm_files": ALGORITHM_FILES
    }

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False, sort_keys=True)

    print(f"\n✅ Successfully generated algorithm code index")
    print(f"   Output: {output_file}")
    print(f"   Mappings: {len(index)}")
    print(f"   Conflicts: {len(conflicts)}")

    return 0


if __name__ == "__main__":
    exit(main())
