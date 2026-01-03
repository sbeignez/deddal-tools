#!/usr/bin/env python3
"""
Import ZBLL cases and algorithms from CSV file and generate SQL migration.

This script parses a CSV file containing ZBLL algorithm data and generates
SQL INSERT statements for the lib_cases and lib_algorithms tables.

Usage:
    python import_zbll_from_csv.py --csv PATH --output PATH [--dry-run]

Example:
    python import_zbll_from_csv.py \
        --csv /path/to/zbll_speedsolving_algorithms.csv \
        --output ../migrations/insert_zbll_data.sql
"""

import argparse
import csv
import re
import uuid
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


def parse_csv(filepath: str) -> Dict[str, List[str]]:
    """Parse CSV and group algorithms by case code.

    Args:
        filepath: Path to CSV file

    Returns:
        Dictionary mapping case codes to list of algorithm sequences
        Example: {"3X3-ZBLL-AS01": ["L U2 L2 U' L'...", "R U R' U..."], ...}

    Raises:
        ValueError: If CSV format is invalid
    """
    case_algorithms = defaultdict(list)

    with open(filepath, 'r', encoding='utf-8') as f:
        # Handle potential carriage returns (^M) by using universal newlines
        reader = csv.DictReader(f)

        # Validate header
        if 'case_code' not in reader.fieldnames or 'algorithm' not in reader.fieldnames:
            raise ValueError(f"CSV must have 'case_code' and 'algorithm' columns. Found: {reader.fieldnames}")

        line_num = 1  # Header is line 1
        for row in reader:
            line_num += 1

            case_code = row['case_code'].strip()
            algorithm = row['algorithm'].strip()

            if not case_code or not algorithm:
                print(f"⚠️  Warning: Empty field at line {line_num}, skipping")
                continue

            # Validate case code format
            if not re.match(r'^3X3-ZBLL-[A-Z0-9]+$', case_code):
                print(f"⚠️  Warning: Invalid case code format '{case_code}' at line {line_num}")

            # Validate algorithm sequence (basic check for cube notation)
            if not validate_move_notation(algorithm):
                print(f"⚠️  Warning: Invalid move notation in '{case_code}' at line {line_num}: {algorithm[:50]}...")

            case_algorithms[case_code].append(algorithm)

    return dict(case_algorithms)


def validate_move_notation(sequence: str) -> bool:
    """Validate that sequence uses valid Rubik's cube notation.

    Args:
        sequence: Algorithm sequence string

    Returns:
        True if valid, False otherwise
    """
    # Basic pattern: moves are R/L/U/D/F/B/M/E/S followed by optional ' or 2
    # Also allows lowercase for wide moves and x/y/z rotations
    pattern = r"^[RLUDFBMESxyzrludfb][2']?(\s+[RLUDFBMESxyzrludfb][2']?)*$"
    return bool(re.match(pattern, sequence))


def calculate_difficulty(sequence: str) -> int:
    """Estimate difficulty rating from move count.

    Move count thresholds:
    - ≤12 moves: difficulty 2 (easy)
    - ≤18 moves: difficulty 3 (medium)
    - ≤24 moves: difficulty 4 (hard)
    - >24 moves: difficulty 5 (expert)

    Args:
        sequence: Algorithm sequence string

    Returns:
        Difficulty rating (2-5)
    """
    # Count moves (split by space, ignore rotations x/y/z)
    moves = [m for m in sequence.split() if m and m[0] in 'RLUDFBMESrludfb']
    move_count = len(moves)

    if move_count <= 12:
        return 2  # Easy (comparable to beginner F2L)
    elif move_count <= 18:
        return 3  # Medium (comparable to OLL)
    elif move_count <= 24:
        return 4  # Hard (long PLL)
    else:
        return 5  # Expert (very complex)


def calculate_popularity(index: int, total: int) -> int:
    """Calculate popularity score for algorithm variant.

    First algorithm (index 0) = 100 (most popular)
    Second algorithm = 80
    Third = 60
    Fourth+ = 40

    Args:
        index: Algorithm index (0-based)
        total: Total algorithms for this case

    Returns:
        Popularity score (0-100)
    """
    if index == 0:
        return 100  # First algorithm (most common/fastest)
    elif index == 1:
        return 80   # Second alternative
    elif index == 2:
        return 60   # Third alternative
    else:
        return 40   # Additional alternatives


def generate_case_insert(case_code: str, case_uuid: str, algorithms: List[str]) -> str:
    """Generate SQL INSERT statement for a single case.

    Args:
        case_code: Case code (e.g., '3X3-ZBLL-AS01')
        case_uuid: UUID for the case
        algorithms: List of algorithm sequences for this case

    Returns:
        SQL INSERT statement
    """
    # Calculate average difficulty from all algorithms for this case
    difficulties = [calculate_difficulty(alg) for alg in algorithms]
    avg_difficulty = round(sum(difficulties) / len(difficulties))

    # Use first algorithm's popularity as case popularity
    case_popularity = calculate_popularity(0, len(algorithms))

    return (
        f"  ('{case_uuid}', '{case_code}', 'zbll', {avg_difficulty}, "
        f"{case_popularity}, NOW())"
    )


def generate_algorithm_inserts(
    case_code: str,
    case_uuid: str,
    algorithms: List[str]
) -> List[str]:
    """Generate SQL INSERT statements for all algorithms of a case.

    Args:
        case_code: Case code (e.g., '3X3-ZBLL-AS01')
        case_uuid: UUID of the parent case
        algorithms: List of algorithm sequences

    Returns:
        List of SQL INSERT statements (one per algorithm)
    """
    inserts = []

    for idx, sequence in enumerate(algorithms):
        alg_uuid = str(uuid.uuid4())
        difficulty = calculate_difficulty(sequence)
        popularity = calculate_popularity(idx, len(algorithms))

        # Escape single quotes in sequence
        escaped_sequence = sequence.replace("'", "''")

        # Algorithm code will be generated by PostgreSQL function generate_unique_alg_code()
        # Format: ALG-{5-char-hash}-{case_code}
        insert = (
            f"  ('{alg_uuid}', '{case_uuid}', "
            f"generate_unique_alg_code('{case_code}'), "
            f"'{escaped_sequence}', {popularity}, {difficulty}, NOW())"
        )
        inserts.append(insert)

    return inserts


def generate_migration_sql(case_algorithms: Dict[str, List[str]]) -> str:
    """Generate complete SQL migration file content.

    Args:
        case_algorithms: Dictionary mapping case codes to algorithm lists

    Returns:
        Complete SQL migration as string
    """
    # Sort case codes for consistent output
    sorted_cases = sorted(case_algorithms.keys())

    # Track statistics
    total_cases = len(sorted_cases)
    total_algorithms = sum(len(algs) for algs in case_algorithms.values())

    # Generate UUIDs for all cases
    case_uuids = {case_code: str(uuid.uuid4()) for case_code in sorted_cases}

    # Build SQL content
    sql_lines = []

    # Header
    sql_lines.append("-- ZBLL Cases and Algorithms Import")
    sql_lines.append("-- Generated by import_zbll_from_csv.py")
    sql_lines.append(f"-- Total cases: {total_cases}")
    sql_lines.append(f"-- Total algorithms: {total_algorithms}")
    sql_lines.append("")

    # Update caseset expected count
    sql_lines.append("-- Update ZBLL caseset expected count")
    sql_lines.append("UPDATE lib_casesets")
    sql_lines.append(f"SET expected_count = {total_cases}")
    sql_lines.append("WHERE code = 'zbll';")
    sql_lines.append("")

    # Insert cases
    sql_lines.append(f"-- Insert {total_cases} ZBLL cases")
    sql_lines.append("INSERT INTO lib_cases (id, code, kind, difficulty, popularity, created_at)")
    sql_lines.append("VALUES")

    case_inserts = []
    for case_code in sorted_cases:
        case_uuid = case_uuids[case_code]
        algorithms = case_algorithms[case_code]
        case_inserts.append(generate_case_insert(case_code, case_uuid, algorithms))

    sql_lines.append(",\n".join(case_inserts) + ";")
    sql_lines.append("")

    # Insert algorithms
    sql_lines.append(f"-- Insert {total_algorithms} ZBLL algorithms")
    sql_lines.append("INSERT INTO lib_algorithms (id, case_id, code, sequence, popularity, difficulty, created_at)")
    sql_lines.append("VALUES")

    all_algorithm_inserts = []
    for case_code in sorted_cases:
        case_uuid = case_uuids[case_code]
        algorithms = case_algorithms[case_code]
        all_algorithm_inserts.extend(
            generate_algorithm_inserts(case_code, case_uuid, algorithms)
        )

    sql_lines.append(",\n".join(all_algorithm_inserts) + ";")
    sql_lines.append("")

    # Insert junction table entries
    sql_lines.append(f"-- Populate M:N junction table ({total_cases} relationships)")
    sql_lines.append("INSERT INTO lib_caseset_cases (caseset_id, case_id, case_index)")
    sql_lines.append("SELECT")
    sql_lines.append("  cs.id,")
    sql_lines.append("  c.id,")
    sql_lines.append("  ROW_NUMBER() OVER (PARTITION BY cs.id ORDER BY c.code)")
    sql_lines.append("FROM lib_casesets cs")
    sql_lines.append("CROSS JOIN lib_cases c")
    sql_lines.append("WHERE cs.code = 'zbll' AND c.kind = 'zbll';")
    sql_lines.append("")

    # Verification queries
    sql_lines.append("-- Verification queries")
    sql_lines.append("-- Run these after migration to verify correctness")
    sql_lines.append("")
    sql_lines.append("-- Check case count")
    sql_lines.append("-- SELECT COUNT(*) FROM lib_cases WHERE kind = 'zbll';")
    sql_lines.append(f"-- Expected: {total_cases}")
    sql_lines.append("")
    sql_lines.append("-- Check algorithm count")
    sql_lines.append("-- SELECT COUNT(*) FROM lib_algorithms a")
    sql_lines.append("-- JOIN lib_cases c ON a.case_id = c.id")
    sql_lines.append("-- WHERE c.kind = 'zbll';")
    sql_lines.append(f"-- Expected: {total_algorithms}")
    sql_lines.append("")
    sql_lines.append("-- Check junction table")
    sql_lines.append("-- SELECT COUNT(*) FROM lib_caseset_cases")
    sql_lines.append("-- WHERE caseset_id = (SELECT id FROM lib_casesets WHERE code = 'zbll');")
    sql_lines.append(f"-- Expected: {total_cases}")

    return "\n".join(sql_lines)


def print_statistics(case_algorithms: Dict[str, List[str]]) -> None:
    """Print statistics about the parsed data.

    Args:
        case_algorithms: Dictionary mapping case codes to algorithm lists
    """
    total_cases = len(case_algorithms)
    total_algorithms = sum(len(algs) for algs in case_algorithms.values())
    avg_algorithms = total_algorithms / total_cases if total_cases > 0 else 0

    # Count by subtype
    subtypes = defaultdict(lambda: {'cases': 0, 'algorithms': 0})
    for case_code, algs in case_algorithms.items():
        # Extract subtype (e.g., 'AS' from '3X3-ZBLL-AS01')
        match = re.match(r'3X3-ZBLL-([A-Z]+)\d+', case_code)
        if match:
            subtype = match.group(1)
            subtypes[subtype]['cases'] += 1
            subtypes[subtype]['algorithms'] += len(algs)

    # Check for edge cases
    cases_with_many_algs = [(code, len(algs)) for code, algs in case_algorithms.items() if len(algs) > 10]
    cases_with_no_algs = [code for code, algs in case_algorithms.items() if len(algs) == 0]

    print("\n📊 Statistics:")
    print(f"  Total unique cases: {total_cases}")
    print(f"  Total algorithms: {total_algorithms}")
    print(f"  Average algorithms per case: {avg_algorithms:.1f}")
    print()

    print("  Distribution by subtype:")
    for subtype in sorted(subtypes.keys()):
        stats = subtypes[subtype]
        print(f"    {subtype:3s}: {stats['cases']:3d} cases, {stats['algorithms']:4d} algorithms")
    print()

    # Warnings
    if cases_with_many_algs:
        print("  ⚠️  Cases with >10 algorithms:")
        for code, count in cases_with_many_algs[:5]:  # Show first 5
            print(f"      {code}: {count} algorithms")
        if len(cases_with_many_algs) > 5:
            print(f"      ... and {len(cases_with_many_algs) - 5} more")
        print()

    if cases_with_no_algs:
        print(f"  ❌ ERROR: {len(cases_with_no_algs)} cases have 0 algorithms")
        for code in cases_with_no_algs[:5]:
            print(f"      {code}")
        print()


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Import ZBLL cases and algorithms from CSV to SQL migration'
    )
    parser.add_argument(
        '--csv',
        required=True,
        help='Path to CSV file containing ZBLL algorithms'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Path to output SQL migration file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Parse and validate without writing output file'
    )

    args = parser.parse_args()

    # Validate input file exists
    csv_path = Path(args.csv)
    if not csv_path.exists():
        print(f"❌ Error: CSV file not found: {csv_path}")
        return 1

    print(f"📖 Reading CSV file: {csv_path}")

    try:
        # Parse CSV
        case_algorithms = parse_csv(str(csv_path))

        # Print statistics
        print_statistics(case_algorithms)

        # Generate SQL
        print("🔨 Generating SQL migration...")
        sql_content = generate_migration_sql(case_algorithms)

        if args.dry_run:
            print("\n✅ Dry-run complete. SQL preview (first 50 lines):")
            print("\n".join(sql_content.split("\n")[:50]))
            print("\n... (truncated)")
        else:
            # Write output file
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(sql_content)
            print(f"\n✅ SQL migration written to: {output_path}")
            print(f"   File size: {output_path.stat().st_size:,} bytes")

        return 0

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    exit(main())
