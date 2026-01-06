#!/usr/bin/env python3
"""
Validate pending algorithm submissions (READ-ONLY analysis).

Checks:
1. Duplicate detection - algorithm already exists for the case
2. Move notation validation - uses valid cube notation
3. Case existence - case_code exists in lib_cases

Usage:
    python3 validate_pending_submissions.py

Requirements:
    pip install supabase

Environment:
    SUPABASE_SERVICE_ROLE_KEY - Service role key for database access
"""

import os
import re
from supabase import create_client

# Supabase configuration
SUPABASE_URL = "https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_ROLE_KEY environment variable not set")
    exit(1)

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Valid move notation pattern (includes lowercase for wide moves)
VALID_MOVES = re.compile(r"^[RUFLDBMESxyzrufldб]['2]?$")

def validate_move_notation(sequence: str) -> tuple[bool, str]:
    """
    Validate algorithm move notation.

    Returns:
        (is_valid, error_message)
    """
    moves = sequence.split()

    for move in moves:
        if not VALID_MOVES.match(move):
            return False, f"Invalid move: '{move}'"

    return True, ""

def check_duplicate(case_code: str, sequence: str) -> tuple[bool, dict]:
    """
    Check if algorithm already exists for this case.

    Returns:
        (is_duplicate, existing_algorithm_data)
    """
    # First get the case to find its case_id
    case_result = supabase.table('lib_cases')\
        .select('id, code, title')\
        .eq('code', case_code)\
        .execute()

    if not case_result.data:
        return False, {"error": f"Case '{case_code}' not found in database"}

    case_id = case_result.data[0]['id']

    # Normalize sequences for comparison (remove extra spaces)
    normalized_sequence = ' '.join(sequence.split())

    # Check if this exact algorithm exists
    existing = supabase.table('lib_algorithms')\
        .select('id, sequence, name, tags')\
        .eq('case_id', case_id)\
        .execute()

    if not existing.data:
        return False, {}

    # Check for exact match
    for alg in existing.data:
        existing_normalized = ' '.join(alg['sequence'].split())
        if existing_normalized == normalized_sequence:
            return True, alg

    return False, {"similar_count": len(existing.data)}

def check_case_exists(case_code: str) -> tuple[bool, dict]:
    """
    Check if case exists in lib_cases.

    Returns:
        (exists, case_data)
    """
    result = supabase.table('lib_cases')\
        .select('id, code, title, case_set_id')\
        .eq('code', case_code)\
        .execute()

    if result.data:
        return True, result.data[0]
    else:
        return False, {}

print("=" * 100)
print("ALGORITHM SUBMISSION VALIDATION")
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

    print(f"\nValidating {len(submissions.data)} pending submission(s)\n")

    valid_count = 0
    duplicate_count = 0
    invalid_count = 0

    # Validate each submission
    for idx, sub in enumerate(submissions.data, 1):
        print("-" * 100)
        print(f"#{idx} - Submission ID: {sub['id']}")
        print(f"Case Code: {sub['case_code']}")
        print(f"Algorithm: {sub['sequence']}")

        issues = []
        warnings = []

        # Check 1: Case exists
        case_exists, case_data = check_case_exists(sub['case_code'])
        if case_exists:
            print(f"✅ Case exists: {case_data.get('title', 'N/A')}")
        else:
            print(f"❌ Case NOT found: {sub['case_code']}")
            issues.append("Case does not exist in database")

        # Check 2: Move notation validation
        is_valid_notation, notation_error = validate_move_notation(sub['sequence'])
        if is_valid_notation:
            print(f"✅ Move notation valid")
        else:
            print(f"❌ Invalid move notation: {notation_error}")
            issues.append(f"Invalid notation: {notation_error}")

        # Check 3: Duplicate detection
        is_duplicate, duplicate_data = check_duplicate(sub['case_code'], sub['sequence'])
        if is_duplicate:
            print(f"⚠️  DUPLICATE found:")
            print(f"   Algorithm ID: {duplicate_data['id']}")
            if duplicate_data.get('name'):
                print(f"   Name: {duplicate_data['name']}")
            if duplicate_data.get('tags'):
                print(f"   Tags: {duplicate_data['tags']}")
            warnings.append("Exact duplicate exists")
            duplicate_count += 1
        elif 'error' in duplicate_data:
            print(f"❌ {duplicate_data['error']}")
            issues.append(duplicate_data['error'])
        elif duplicate_data.get('similar_count', 0) > 0:
            print(f"ℹ️  {duplicate_data['similar_count']} other algorithm(s) exist for this case (not duplicates)")
        else:
            print(f"✅ No duplicates found")

        # Summary for this submission
        print()
        if issues:
            print(f"🔴 INVALID - Issues: {', '.join(issues)}")
            invalid_count += 1
        elif warnings:
            print(f"🟡 VALID BUT DUPLICATE - Warnings: {', '.join(warnings)}")
        else:
            print(f"🟢 VALID - Ready for review")
            valid_count += 1

        print()

    # Final summary
    print("=" * 100)
    print("VALIDATION SUMMARY")
    print("=" * 100)
    print(f"Total submissions: {len(submissions.data)}")
    print(f"🟢 Valid (new): {valid_count}")
    print(f"🟡 Valid (duplicate): {duplicate_count}")
    print(f"🔴 Invalid: {invalid_count}")
    print("=" * 100)

except Exception as e:
    print(f"❌ Error validating submissions: {e}")
    exit(1)
