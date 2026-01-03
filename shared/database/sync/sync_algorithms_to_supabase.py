#!/usr/bin/env python3
"""
Sync algorithm JSON files to Supabase lib_algorithms table.
This pushes the source of truth (hard-coded algorithms extracted to JSON) to the database.

Usage:
    python3 sync_algorithms_to_supabase.py

Requirements:
    pip install supabase

Environment:
    SUPABASE_URL - Your Supabase project URL
    SUPABASE_SERVICE_KEY - Your Supabase service role key (has write access)
"""

import json
import os
from pathlib import Path
from datetime import datetime
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY environment variable not set")
    print("Set it with: export SUPABASE_SERVICE_KEY='your-service-role-key'")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Paths to algorithm JSON files
BASE_PATH = Path(__file__).parent / "Deddal" / "Data" / "Resources" / "SeedData"
ALGORITHM_FILES = [
    BASE_PATH / "f2l_algorithms.json",
    BASE_PATH / "oll_algorithms.json",
    BASE_PATH / "pll_algorithms.json",
]

def load_algorithms():
    """Load all algorithms from JSON files."""
    all_algorithms = []

    for file_path in ALGORITHM_FILES:
        if not file_path.exists():
            print(f"WARNING: File not found: {file_path}")
            continue

        print(f"Loading {file_path.name}...")
        with open(file_path, 'r') as f:
            algorithms = json.load(f)
            print(f"  Found {len(algorithms)} algorithms")
            all_algorithms.extend(algorithms)

    return all_algorithms

def sync_to_supabase(algorithms):
    """Sync algorithms to Supabase lib_algorithms table."""
    print(f"\nSyncing {len(algorithms)} algorithms to Supabase...")

    # Map JSON fields to database columns
    db_algorithms = []
    for alg in algorithms:
        db_alg = {
            'id': alg['id'],
            'case_id': alg['case_id'],
            'code': alg['code'],
            'name': alg.get('name'),
            'moves': alg.get('moves'),
            'tag': alg.get('tag'),
            'complexity': alg.get('complexity'),
            'popularity': alg.get('popularity'),
            'created_at': alg.get('created_at'),
            'updated_at': datetime.utcnow().isoformat() + 'Z',
        }
        db_algorithms.append(db_alg)

    # Batch upsert algorithms (Supabase upsert handles insert/update)
    # Process in batches of 100 to avoid hitting limits
    batch_size = 100
    total_batches = (len(db_algorithms) + batch_size - 1) // batch_size

    for i in range(0, len(db_algorithms), batch_size):
        batch = db_algorithms[i:i + batch_size]
        batch_num = (i // batch_size) + 1

        print(f"  Batch {batch_num}/{total_batches}: Upserting {len(batch)} algorithms...")

        response = supabase.table('lib_algorithms').upsert(batch).execute()

        if hasattr(response, 'error') and response.error:
            print(f"    ERROR: {response.error}")
            return False

        print(f"    ✓ Success")

    return True

def main():
    """Main execution."""
    print("=" * 60)
    print("Sync Algorithms JSON → Supabase")
    print("=" * 60)

    # Load algorithms from JSON files
    algorithms = load_algorithms()

    if not algorithms:
        print("\nERROR: No algorithms loaded from JSON files")
        return

    print(f"\nTotal algorithms loaded: {len(algorithms)}")

    # Confirm before syncing
    response = input("\nProceed with sync to Supabase? (yes/no): ")
    if response.lower() != 'yes':
        print("Sync cancelled.")
        return

    # Sync to Supabase
    success = sync_to_supabase(algorithms)

    if success:
        print("\n" + "=" * 60)
        print("✅ Sync complete!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ Sync failed!")
        print("=" * 60)

if __name__ == "__main__":
    main()
