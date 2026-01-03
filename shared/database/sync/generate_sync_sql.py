#!/usr/bin/env python3
"""
Generate SQL INSERT statements for syncing seed data to Supabase.
Generates upsert SQL that can be executed via Supabase MCP.

Usage:
    python3 generate_sync_sql.py > sync_seed_data.sql
"""

import json
from pathlib import Path
from datetime import datetime

# Base path to seed data
SEED_DATA_PATH = Path("/Users/trophee-mini/code/deddal/deddal-ios/Deddal/Data/Resources/SeedData")

# Case sets file
CASE_SETS_FILE = SEED_DATA_PATH / "all_case_sets.json"

# Case files to sync (parity + CLL)
CASE_FILES = [
    # Parity cases
    "4x4_parity_oll_cases.json",
    "4x4_parity_pll_cases.json",
    "5x5_parity_cases.json",
    "6x6_parity_oll_cases.json",
    "6x6_parity_pll_cases.json",
    "7x7_parity_cases.json",
    # CLL cases
    "2x2_cll_cases.json",
]

# Algorithm files to sync (parity only - CLL algorithms not yet)
ALGORITHM_FILES = [
    "4x4_parity_oll_algorithms.json",
    "4x4_parity_pll_algorithms.json",
    "5x5_parity_algorithms.json",
    "6x6_parity_oll_algorithms.json",
    "6x6_parity_pll_algorithms.json",
    "7x7_parity_algorithms.json",
]


def escape_sql_string(s):
    """Escape single quotes in SQL strings."""
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"


def load_case_sets():
    """Load case sets from JSON file."""
    if not CASE_SETS_FILE.exists():
        return []

    with open(CASE_SETS_FILE, 'r') as f:
        return json.load(f)


def load_cases():
    """Load all cases from JSON files."""
    all_cases = []

    for filename in CASE_FILES:
        file_path = SEED_DATA_PATH / filename

        if not file_path.exists():
            continue

        with open(file_path, 'r') as f:
            cases = json.load(f)
            all_cases.extend(cases)

    return all_cases


def load_algorithms():
    """Load all algorithms from JSON files."""
    all_algorithms = []

    for filename in ALGORITHM_FILES:
        file_path = SEED_DATA_PATH / filename

        if not file_path.exists():
            continue

        with open(file_path, 'r') as f:
            algorithms = json.load(f)
            all_algorithms.extend(algorithms)

    return all_algorithms


def generate_case_set_sql(case_sets):
    """Generate SQL for case sets."""
    if not case_sets:
        return ""

    sql = "-- Sync case sets\n"

    for cs in case_sets:
        sql += f"""
INSERT INTO lib_case_sets (
    id, code, name, subtitle, pattern_from, pattern_to,
    expected_count, category, created_at, updated_at
) VALUES (
    {escape_sql_string(cs['id'])},
    {escape_sql_string(cs['code'])},
    {escape_sql_string(cs['name'])},
    {escape_sql_string(cs.get('subtitle'))},
    {escape_sql_string(cs.get('pattern_from'))},
    {escape_sql_string(cs.get('pattern_to'))},
    {cs.get('expected_count', 0)},
    {escape_sql_string(cs.get('category'))},
    {escape_sql_string(cs.get('created_at'))},
    {escape_sql_string(datetime.utcnow().isoformat() + 'Z')}
)
ON CONFLICT (id) DO UPDATE SET
    code = EXCLUDED.code,
    name = EXCLUDED.name,
    subtitle = EXCLUDED.subtitle,
    pattern_from = EXCLUDED.pattern_from,
    pattern_to = EXCLUDED.pattern_to,
    expected_count = EXCLUDED.expected_count,
    category = EXCLUDED.category,
    updated_at = EXCLUDED.updated_at;
"""

    return sql


def generate_case_sql(cases):
    """Generate SQL for cases."""
    if not cases:
        return ""

    sql = "-- Sync cases\n"

    for case in cases:
        # Convert groups array to PostgreSQL array format
        groups = case.get('groups', [])
        groups_sql = "ARRAY[" + ", ".join([escape_sql_string(g) for g in groups]) + "]::text[]"

        sql += f"""
INSERT INTO lib_cases (
    id, code, case_set_id, title, long_name, kind,
    pattern_from, pattern_to, scramble, notes, story,
    description, image_asset_name, difficulty, popularity,
    groups, created_at, updated_at
) VALUES (
    {escape_sql_string(case['id'])},
    {escape_sql_string(case['code'])},
    {escape_sql_string(case['case_set_id'])},
    {escape_sql_string(case.get('title'))},
    {escape_sql_string(case.get('long_name'))},
    {escape_sql_string(case.get('kind'))},
    {escape_sql_string(case.get('pattern_from'))},
    {escape_sql_string(case.get('pattern_to'))},
    {escape_sql_string(case.get('scramble'))},
    {escape_sql_string(case.get('notes', ''))},
    {escape_sql_string(case.get('story', ''))},
    {escape_sql_string(case.get('description', ''))},
    {escape_sql_string(case.get('image_asset_name', ''))},
    {case.get('difficulty')},
    {case.get('popularity')},
    {groups_sql},
    {escape_sql_string(case.get('created_at'))},
    {escape_sql_string(datetime.utcnow().isoformat() + 'Z')}
)
ON CONFLICT (id) DO UPDATE SET
    code = EXCLUDED.code,
    case_set_id = EXCLUDED.case_set_id,
    title = EXCLUDED.title,
    long_name = EXCLUDED.long_name,
    kind = EXCLUDED.kind,
    pattern_from = EXCLUDED.pattern_from,
    pattern_to = EXCLUDED.pattern_to,
    scramble = EXCLUDED.scramble,
    notes = EXCLUDED.notes,
    story = EXCLUDED.story,
    description = EXCLUDED.description,
    image_asset_name = EXCLUDED.image_asset_name,
    difficulty = EXCLUDED.difficulty,
    popularity = EXCLUDED.popularity,
    groups = EXCLUDED.groups,
    updated_at = EXCLUDED.updated_at;
"""

    return sql


def generate_algorithm_sql(algorithms):
    """Generate SQL for algorithms."""
    if not algorithms:
        return ""

    sql = "-- Sync algorithms\n"

    for alg in algorithms:
        sql += f"""
INSERT INTO lib_algorithms (
    id, case_id, code, name, moves, tag,
    complexity, popularity, created_at, updated_at
) VALUES (
    {escape_sql_string(alg['id'])},
    {escape_sql_string(alg['case_id'])},
    {escape_sql_string(alg['code'])},
    {escape_sql_string(alg.get('name'))},
    {escape_sql_string(alg.get('moves'))},
    {escape_sql_string(alg.get('tag'))},
    {alg.get('complexity')},
    {alg.get('popularity')},
    {escape_sql_string(alg.get('created_at'))},
    {escape_sql_string(datetime.utcnow().isoformat() + 'Z')}
)
ON CONFLICT (id) DO UPDATE SET
    case_id = EXCLUDED.case_id,
    code = EXCLUDED.code,
    name = EXCLUDED.name,
    moves = EXCLUDED.moves,
    tag = EXCLUDED.tag,
    complexity = EXCLUDED.complexity,
    popularity = EXCLUDED.popularity,
    updated_at = EXCLUDED.updated_at;
"""

    return sql


def main():
    """Main execution."""
    # Load all data
    case_sets = load_case_sets()
    cases = load_cases()
    algorithms = load_algorithms()

    print("-- ============================================================")
    print("-- Seed Data Sync SQL")
    print("-- Generated:", datetime.utcnow().isoformat() + 'Z')
    print("-- ============================================================")
    print()
    print("-- Summary:")
    print(f"--   Case Sets:  {len(case_sets)}")
    print(f"--   Cases:      {len(cases)}")
    print(f"--   Algorithms: {len(algorithms)}")
    print("-- ============================================================")
    print()

    # Generate SQL in order (case_sets → cases → algorithms)
    sql = ""

    if case_sets:
        sql += generate_case_set_sql(case_sets)
        sql += "\n"

    if cases:
        sql += generate_case_sql(cases)
        sql += "\n"

    if algorithms:
        sql += generate_algorithm_sql(algorithms)
        sql += "\n"

    print(sql)

    print("-- ============================================================")
    print("-- End of sync SQL")
    print("-- ============================================================")


if __name__ == "__main__":
    main()
