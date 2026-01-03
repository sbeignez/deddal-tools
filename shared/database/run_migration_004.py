#!/usr/bin/env python3
"""
Execute Migration 004: Change knowledge_level from 0-5 to 0-100 percentage

This script runs the migration directly against the Supabase database.
"""

import os
import sys
from supabase import create_client

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

def run_migration():
    """Execute migration 004."""

    # Check for required environment variables
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("❌ Error: Required environment variables not set")
        print("\nRequired:")
        print("  - SUPABASE_URL")
        print("  - SUPABASE_SERVICE_ROLE_KEY")
        print("\nPlease run this migration manually in Supabase SQL Editor:")
        print("  cat tool-database/migrations/004_change_knowledge_level_to_percentage.sql")
        sys.exit(1)

    # Create Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

    print("=" * 60)
    print("Migration 004: Knowledge Level to Percentage")
    print("=" * 60)

    try:
        # Step 1: Get current data statistics
        print("\n📊 Current data statistics:")
        response = supabase.table('lib_user_algorithms').select('knowledge_level').execute()
        if response.data:
            levels = [row['knowledge_level'] for row in response.data]
            print(f"  Total rows: {len(levels)}")
            print(f"  Min level: {min(levels) if levels else 'N/A'}")
            print(f"  Max level: {max(levels) if levels else 'N/A'}")

            # Count rows that need conversion (0-5 scale)
            old_scale_count = sum(1 for level in levels if level <= 5)
            print(f"  Rows with old scale (0-5): {old_scale_count}")
        else:
            print("  No data found")

        print("\n⚠️  WARNING: This migration will:")
        print("  1. Convert existing 0-5 values → 0-100 percentages")
        print("  2. Drop old CHECK constraint (0-5)")
        print("  3. Add new CHECK constraint (0-100)")
        print("\nThis migration cannot be executed via the Supabase Python client.")
        print("The Python client (PostgREST) does not support DDL operations like ALTER TABLE.")
        print("\n✅ Please run the migration in Supabase SQL Editor instead:")
        print(f"\n1. Go to: {SUPABASE_URL.replace('https://', 'https://supabase.com/dashboard/project/')}/sql")
        print("2. Copy the SQL from: tool-database/migrations/004_change_knowledge_level_to_percentage.sql")
        print("3. Paste and execute in SQL Editor")
        print("\n📝 After running the migration, verify with:")
        print("   cat tool-database/verify_migration_004.sql")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_migration()
