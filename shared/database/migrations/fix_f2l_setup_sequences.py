#!/usr/bin/env python3
"""
Fix F2L setupSequence (scramble) values in JSON seed data and generate SQL migration.

The scramble values were incorrectly set to be the same as algorithms.
They should be the setup moves that CREATE the case, not solve it.

Correct setup data sourced from speedcubedb.com
"""

import json
import re
from pathlib import Path

# Correct setup sequences for FR slot (from speedcubedb.com)
CORRECT_SETUPS_FR = {
    1: "F R' F' R",
    2: "R' F R F'",
    3: "F' U F",
    4: "R U' R'",
    5: "R U R' U2' R U' R' U",
    6: "F' U' F U2' F' U F U'",
    7: "R U R' U2' R U2' R' U",
    8: "r' U' R2 U' R2' U2' r",
    9: "F' U F U' R U R' U",
    10: "R U' R' U' R U' R' U",
    11: "F' U F U' R U2' R' U",
    12: "R U R' U2' R U R' U' R U R'",
    13: "r U2' R' U R U' R' U M",
    14: "R U' R' U' R U R' U",
    15: "R U R' U' R U R' U2' R U' R'",
    16: "F' U F U2' R U R'",
    17: "R U' R' U R U2' R'",
    18: "R U R' U' R U R' F R' F' R",
    19: "R U R' U' R U2' R' U'",
    20: "R U R' F R' F' R2' U R' U",
    21: "R U' R' U2' R U R'",
    22: "F' L' U2' L F",
    23: "R U' R' U R U' R' U2' R U' R'",
    24: "R U R' F R U R' U' F'",
    25: "F' R U R' U' R' F R",
    26: "F' U' F U R U R' U'",
    27: "R U R' U' R U R'",
    28: "R' F R F' U R U' R'",
    29: "F R' F' R F R' F' R",
    30: "R U' R' U R U' R'",
    31: "R U R' F R' F' R U",
    32: "R U' R' U R U' R' U R U' R'",
    33: "R U R' U2' R U R' U",
    34: "R U' R' U2' R U' R' U'",
    35: "F' U F U' R U' R' U",
    36: "R U' R' U2' F R' F' R U2'",
    37: "R U' R U2' F R2' F' U2' R2'",
    38: "R U' R' U R U2' R' U R U' R'",
    39: "R U' R' U' R U R' U2' R U' R'",
    40: "R U R' F U R U' R' F' R U R'",
    41: "R F U R U' R' F' U' R'",
}

def mirror_move(move: str) -> str:
    """
    Mirror a single move (left-right reflection).
    Rules:
    - R ↔ L' (swap face AND flip prime)
    - F, U, B, D → flip prime only
    - Wide moves follow same pattern
    - M → M' (follows L direction)
    """
    # Define the mirror mapping
    mirror_map = {
        # R ↔ L with prime swap
        "R": "L'", "R'": "L", "R2": "L2", "R2'": "L2'",
        "L": "R'", "L'": "R", "L2": "R2", "L2'": "R2'",
        # F, U, B, D - flip prime only
        "F": "F'", "F'": "F", "F2": "F2", "F2'": "F2'",
        "U": "U'", "U'": "U", "U2": "U2", "U2'": "U2'",
        "B": "B'", "B'": "B", "B2": "B2", "B2'": "B2'",
        "D": "D'", "D'": "D", "D2": "D2", "D2'": "D2'",
        # Wide moves - same pattern
        "r": "l'", "r'": "l", "r2": "l2", "r2'": "l2'",
        "l": "r'", "l'": "r", "l2": "r2", "l2'": "r2'",
        "f": "f'", "f'": "f", "f2": "f2", "f2'": "f2'",
        "u": "u'", "u'": "u", "u2": "u2", "u2'": "u2'",
        "b": "b'", "b'": "b", "b2": "b2", "b2'": "b2'",
        "d": "d'", "d'": "d", "d2": "d2", "d2'": "d2'",
        # Slice moves:
        # M is on the left-right symmetry axis, stays same
        "M": "M", "M'": "M'", "M2": "M2", "M2'": "M2'",
        # E is horizontal, stays same
        "E": "E", "E'": "E'", "E2": "E2", "E2'": "E2'",
        # S follows F direction, F→F' so S→S'
        "S": "S'", "S'": "S", "S2": "S2", "S2'": "S2'",
        # Rotations - flip prime
        "x": "x'", "x'": "x", "x2": "x2",
        "y": "y'", "y'": "y", "y2": "y2",
        "z": "z'", "z'": "z", "z2": "z2",
    }
    return mirror_map.get(move, move)


def mirror_moves(moves: str) -> str:
    """Mirror a move sequence for FL slot (left-right reflection)"""
    # Tokenize - pattern matches: R, R', R2, R2' as single tokens
    # [()'] grouping notation is ignored
    tokens = re.findall(r"[RLUDFBrludfbMSExyz]2?'?", moves)

    mirrored = [mirror_move(token) for token in tokens if token]
    return ' '.join(mirrored)

def generate_fl_setups():
    """Generate FL slot setups by mirroring FR setups"""
    fl_setups = {}
    for num, setup in CORRECT_SETUPS_FR.items():
        fl_setups[num] = mirror_moves(setup)
    return fl_setups

def update_json_file(json_path: Path):
    """Update the JSON seed file with correct scramble values"""
    with open(json_path, 'r') as f:
        cases = json.load(f)

    fl_setups = generate_fl_setups()

    updated_count = 0
    for case in cases:
        code = case.get('code', '')
        match = re.match(r'F2L-(\d+)-(F[LR])', code)
        if match:
            num = int(match.group(1))
            slot = match.group(2)

            if slot == 'FR' and num in CORRECT_SETUPS_FR:
                old_scramble = case.get('scramble', '')
                new_scramble = CORRECT_SETUPS_FR[num]
                if old_scramble != new_scramble:
                    print(f"{code}: '{old_scramble}' -> '{new_scramble}'")
                    case['scramble'] = new_scramble
                    updated_count += 1
            elif slot == 'FL' and num in fl_setups:
                old_scramble = case.get('scramble', '')
                new_scramble = fl_setups[num]
                if old_scramble != new_scramble:
                    print(f"{code}: '{old_scramble}' -> '{new_scramble}'")
                    case['scramble'] = new_scramble
                    updated_count += 1

    # Write back
    with open(json_path, 'w') as f:
        json.dump(cases, f, indent=2)

    print(f"\nUpdated {updated_count} cases in {json_path}")
    return cases

def generate_sql_migration(cases: list, output_path: Path):
    """Generate SQL UPDATE statements for Supabase"""
    sql_lines = [
        "-- Fix F2L setupSequence (scramble) values",
        "-- The scramble values were incorrectly set to algorithms instead of setup moves",
        "-- Generated by fix_f2l_setup_sequences.py",
        "",
        "BEGIN;",
        ""
    ]

    for case in cases:
        code = case.get('code', '')
        if code.startswith('F2L-'):
            scramble = case.get('scramble', '').replace("'", "''")  # Escape single quotes
            sql_lines.append(f"UPDATE lib_cases SET scramble = '{scramble}' WHERE code = '{code}';")

    sql_lines.extend([
        "",
        "COMMIT;",
        ""
    ])

    with open(output_path, 'w') as f:
        f.write('\n'.join(sql_lines))

    print(f"Generated SQL migration: {output_path}")

def main():
    script_dir = Path(__file__).parent
    json_path = script_dir.parent.parent / "Deddal/Data/Resources/SeedData/3x3_cfop_f2l_cases.json"
    sql_path = script_dir / "fix_f2l_setup_sequences.sql"

    print("=" * 60)
    print("Fixing F2L setupSequence values")
    print("=" * 60)

    # Update JSON
    print("\n--- Updating JSON ---")
    cases = update_json_file(json_path)

    # Generate SQL
    print("\n--- Generating SQL ---")
    generate_sql_migration(cases, sql_path)

    print("\n" + "=" * 60)
    print("Done! Review changes and run SQL migration on Supabase.")
    print("=" * 60)

if __name__ == "__main__":
    main()
