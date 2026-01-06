#!/usr/bin/env python3
"""
Query pending algorithm submissions with user details (READ-ONLY).

Usage:
    python3 query_pending_submissions.py

Requirements:
    pip install supabase

Environment:
    SUPABASE_SERVICE_ROLE_KEY - Service role key for database access
"""

import os
from supabase import create_client

# Supabase configuration
SUPABASE_URL = "https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_ROLE_KEY environment variable not set")
    exit(1)

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Query pending submissions with user details
print("=" * 100)
print("PENDING ALGORITHM SUBMISSIONS")
print("=" * 100)

try:
    # Get pending submissions
    submissions = supabase.table('lib_algorithm_submissions')\
        .select('*')\
        .eq('status', 'pending')\
        .order('created_at')\
        .execute()

    if not submissions.data:
        print("\n✅ No pending submissions found.")
        exit(0)

    print(f"\nFound {len(submissions.data)} pending submission(s)\n")

    # For each submission, fetch user details
    for idx, sub in enumerate(submissions.data, 1):
        print("-" * 100)
        print(f"#{idx} - Submission ID: {sub['id']}")
        print(f"Created: {sub['created_at']}")
        print(f"Case Code: {sub['case_code']}")
        print(f"Algorithm: {sub['sequence']}")
        if sub.get('notes'):
            print(f"Notes: {sub['notes']}")

        # Fetch user details from auth.users
        user_id = sub['submitted_by']
        if user_id:
            try:
                # Query auth.users table directly
                response = supabase.auth.admin.get_user_by_id(user_id)

                if response:
                    user = response.user
                    print(f"\nSubmitted by:")
                    print(f"  User ID: {user.id}")
                    if user.email:
                        print(f"  Email: {user.email}")
                    # Check user_metadata for display name or full name
                    metadata = user.user_metadata or {}
                    if metadata.get('display_name'):
                        print(f"  Display Name: {metadata['display_name']}")
                    if metadata.get('full_name'):
                        print(f"  Full Name: {metadata['full_name']}")
                    if metadata.get('name'):
                        print(f"  Name: {metadata['name']}")
                else:
                    print(f"\nSubmitted by: {user_id}")
                    print("  (User not found)")

            except Exception as e:
                print(f"\nSubmitted by: {user_id}")
                print(f"  (Error fetching user details: {e})")
        else:
            print("\nSubmitted by: (Unknown)")

        print()

    print("=" * 100)
    print(f"TOTAL PENDING: {len(submissions.data)}")
    print("=" * 100)

except Exception as e:
    print(f"❌ Error querying submissions: {e}")
    exit(1)
