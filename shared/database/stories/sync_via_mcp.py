#!/usr/bin/env python3
"""
Sync story content to Supabase using UPDATE statements in batches.
This script generates SQL for Supabase MCP tool execution.
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
        print(f"WARNING: Story file not found: {rel_path}")
        return None
    return path.read_text(encoding='utf-8').strip()

def main():
    # Load index
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    print("=== Generating Supabase UPDATE statements ===\n")

    # Collect case story updates
    case_updates = []
    missing_case_files = []

    for entry in index_data.get("case_stories", []):
        case_code = entry["case_code"]
        content = read_story(entry["file_path"])

        if content:
            case_updates.append((case_code, content))
        else:
            missing_case_files.append(entry["file_path"])

    # Collect algorithm story updates
    alg_updates = []
    missing_alg_files = []

    for entry in index_data.get("algorithm_stories", []):
        alg_code = entry["algorithm_code"]
        content = read_story(entry["file_path"])

        if content:
            alg_updates.append((alg_code, content))
        else:
            missing_alg_files.append(entry["file_path"])

    # Report
    print(f"✓ Found {len(case_updates)} case stories to sync")
    print(f"✓ Found {len(alg_updates)} algorithm stories to sync")

    if missing_case_files:
        print(f"\n⚠️  WARNING: {len(missing_case_files)} case story files not found")
    if missing_alg_files:
        print(f"⚠️  WARNING: {len(missing_alg_files)} algorithm story files not found")

    # Generate batch SQL files (split into chunks)
    batch_size = 10  # Update 10 cases per batch
    total_case_batches = (len(case_updates) + batch_size - 1) // batch_size
    total_alg_batches = (len(alg_updates) + batch_size - 1) // batch_size

    print(f"\nGenerating SQL batches:")
    print(f"  - Case stories: {total_case_batches} batches")
    print(f"  - Algorithm stories: {total_alg_batches} batches")

    # Generate case story batches
    for batch_num in range(total_case_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(case_updates))
        batch = case_updates[start_idx:end_idx]

        output_file = STORIES_ROOT / f"sync_cases_batch_{batch_num + 1:02d}.sql"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"-- Batch {batch_num + 1}/{total_case_batches}: Cases {start_idx + 1}-{end_idx}\n\n")

            for code, content in batch:
                escaped_content = escape_sql_string(content)
                f.write(f"UPDATE lib_cases SET story = '{escaped_content}' WHERE code = '{code}';\n\n")

        print(f"  ✓ Generated: {output_file.name}")

    # Generate algorithm story batches
    for batch_num in range(total_alg_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(alg_updates))
        batch = alg_updates[start_idx:end_idx]

        output_file = STORIES_ROOT / f"sync_algorithms_batch_{batch_num + 1:02d}.sql"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"-- Batch {batch_num + 1}/{total_alg_batches}: Algorithms {start_idx + 1}-{end_idx}\n\n")

            for code, content in batch:
                escaped_content = escape_sql_string(content)
                f.write(f"UPDATE lib_algorithms SET story = '{escaped_content}' WHERE code = '{code}';\n\n")

        print(f"  ✓ Generated: {output_file.name}")

    print(f"\n✅ Generated {total_case_batches + total_alg_batches} batch SQL files")

if __name__ == "__main__":
    main()
