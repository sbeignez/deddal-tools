#!/usr/bin/env python3
"""
Generate SQL for syncing just the CLL case set and cases.
This outputs smaller SQL batches suitable for MCP execution.

Usage:
    python3 sync_cll_via_mcp.py
"""

import json
from pathlib import Path
from datetime import datetime

# Base path to seed data
SEED_DATA_PATH = Path("/Users/trophee-mini/code/deddal/deddal-ios/Deddal/Data/Resources/SeedData")


def escape_sql_string(s):
    """Escape single quotes in SQL strings."""
    if s is None:
        return 'NULL'
    return "'" + str(s).replace("'", "''") + "'"


def load_cll_case_set():
    """Load the CLL case set entry."""
    case_sets_file = SEED_DATA_PATH / "all_case_sets.json"

    with open(case_sets_file, 'r') as f:
        case_sets = json.load(f)

    # Find CLL case set
    for cs in case_sets:
        if cs['code'] == '2x2-cll':
            return cs

    return None


def load_cll_cases():
    """Load CLL cases."""
    cll_file = SEED_DATA_PATH / "2x2_cll_cases.json"

    with open(cll_file, 'r') as f:
        return json.load(f)


def generate_case_set_sql(cs):
    """Generate SQL for CLL case set."""
    sql = f"""-- Sync CLL case set
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


def generate_cases_batch_sql(cases, batch_num, batch_size=10):
    """Generate SQL for a batch of cases."""
    start = batch_num * batch_size
    end = start + batch_size
    batch = cases[start:end]

    if not batch:
        return None

    sql = f"-- Sync CLL cases batch {batch_num + 1} (cases {start + 1}-{start + len(batch)})\n"

    for case in batch:
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


def main():
    """Main execution."""
    # Load CLL data
    case_set = load_cll_case_set()
    cases = load_cll_cases()

    print("=" * 60)
    print("CLL Data Sync via Supabase MCP")
    print("=" * 60)
    print()
    print(f"Case Set: {case_set['code']} ({case_set['name']})")
    print(f"Cases:    {len(cases)}")
    print()

    # Step 1: Sync case set
    print("STEP 1: Sync case set")
    print("-" * 60)
    case_set_sql = generate_case_set_sql(case_set)
    print(case_set_sql)
    print()

    # Step 2: Generate batches for cases (10 per batch to keep SQL size manageable)
    print("STEP 2: Sync cases in batches")
    print("-" * 60)

    batch_size = 10
    total_batches = (len(cases) + batch_size - 1) // batch_size

    for batch_num in range(total_batches):
        batch_sql = generate_cases_batch_sql(cases, batch_num, batch_size)
        if batch_sql:
            print(batch_sql)
            print()

    print("=" * 60)
    print(f"Total: 1 case set + {len(cases)} cases in {total_batches} batches")
    print("=" * 60)


if __name__ == "__main__":
    main()
