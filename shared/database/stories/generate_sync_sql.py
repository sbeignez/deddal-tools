#!/usr/bin/env python3
"""
Generate SQL statements to sync story content to Supabase.
Outputs SQL UPDATE statements that can be executed via Supabase MCP tool.
"""

import json
from pathlib import Path

STORIES_ROOT = Path(__file__).parent
INDEX_PATH = STORIES_ROOT / "index.json"

def escape_sql_string(s):
    """Escape single quotes for SQL."""
    return s.replace("'", "''")

def read_story(rel_path):
    """Read story content from markdown file."""
    path = STORIES_ROOT / rel_path
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8").strip()

def main():
    # Load index
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    # Generate SQL for case stories
    case_updates = []
    for entry in index_data.get("case_stories", []):
        case_code = entry["case_code"]
        content = read_story(entry["file_path"])

        if content:
            escaped_content = escape_sql_string(content)
            sql = f"UPDATE lib_cases SET story = '{escaped_content}' WHERE code = '{case_code}';"
            case_updates.append(sql)

    # Generate SQL for algorithm stories
    alg_updates = []
    for entry in index_data.get("algorithm_stories", []):
        alg_code = entry["algorithm_code"]
        content = read_story(entry["file_path"])

        if content:
            escaped_content = escape_sql_string(content)
            sql = f"UPDATE lib_algorithms SET story = '{escaped_content}' WHERE code = '{alg_code}';"
            alg_updates.append(sql)

    # Output counts
    print(f"Generated {len(case_updates)} case story updates")
    print(f"Generated {len(alg_updates)} algorithm story updates")
    print(f"\nTotal SQL statements: {len(case_updates) + len(alg_updates)}")

    # Write to file
    output_file = STORIES_ROOT / "sync_stories.sql"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("-- Sync case stories to Supabase\n")
        f.write(f"-- Generated: {len(case_updates)} case updates, {len(alg_updates)} algorithm updates\n\n")

        f.write("-- Case stories\n")
        for sql in case_updates:
            f.write(sql + "\n")

        f.write("\n-- Algorithm stories\n")
        for sql in alg_updates:
            f.write(sql + "\n")

    print(f"\nSQL written to: {output_file}")
    print(f"File size: {output_file.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()
