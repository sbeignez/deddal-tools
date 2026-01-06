#!/usr/bin/env python3
"""
Complete validation of pending algorithm submissions.

Validates:
1. Move notation (Python regex)
2. Case existence (Supabase)
3. Duplicate detection (Supabase)
4. Algorithm solving (Python cube engine - if available)

For full iOS cube engine validation, use validate_with_cube_engine.py
(requires manual Xcode project setup)

Usage:
    python3 validate_submissions_complete.py

Requirements:
    pip install supabase
    pip install pycuber  # Optional, for cube solving validation

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

# Check if pycuber is available for solving validation
try:
    import pycuber as pc
    HAS_CUBE_SOLVER = True
    print("✅ pycuber available - will validate if algorithm solves case")
except ImportError:
    HAS_CUBE_SOLVER = False
    print("⚠️  pycuber not available - install with: pip install pycuber")
    print("   Validation will skip solving verification\n")

# Valid move notation pattern (includes lowercase for wide moves)
VALID_MOVES = re.compile(r"^[RUFLDBMESxyzrufldб]['2]?$")

def validate_move_notation(sequence: str) -> tuple[bool, str]:
    """Validate algorithm move notation."""
    moves = sequence.split()

    for move in moves:
        if not VALID_MOVES.match(move):
            return False, f"Invalid move: '{move}'"

    return True, ""

def check_case_exists(case_code: str) -> tuple[bool, dict]:
    """Check if case exists in lib_cases."""
    result = supabase.table('lib_cases')\
        .select('id, code, title, case_set_id, scramble')\
        .eq('code', case_code)\
        .execute()

    if result.data:
        return True, result.data[0]
    else:
        return False, {}

def check_duplicate(case_code: str, sequence: str) -> tuple[bool, dict]:
    """Check if algorithm already exists for this case."""
    # Get case
    case_result = supabase.table('lib_cases')\
        .select('id, code, title')\
        .eq('code', case_code)\
        .execute()

    if not case_result.data:
        return False, {"error": f"Case '{case_code}' not found in database"}

    case_id = case_result.data[0]['id']

    # Normalize sequences for comparison
    normalized_sequence = ' '.join(sequence.split())

    # Check existing algorithms
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

def validate_solving_pycuber(scramble: str, algorithm: str) -> tuple[bool, str]:
    """
    Validate if scramble + algorithm results in solved cube using pycuber.

    Note: This is a simplified validation. Full validation should use iOS cube engine
    which has the exact same move notation and cube representation.
    """
    if not HAS_CUBE_SOLVER:
        return None, "Cube solver not available"

    try:
        # Create solved cube
        cube = pc.Cube()

        # Apply scramble
        scramble_formula = pc.Formula(scramble)
        cube(scramble_formula)

        # Apply algorithm
        alg_formula = pc.Formula(algorithm)
        cube(alg_formula)

        # Check if solved
        is_solved = str(cube) == str(pc.Cube())

        if is_solved:
            return True, "Algorithm solves the case"
        else:
            return False, "Algorithm does NOT solve the case"

    except Exception as e:
        return None, f"Error validating: {str(e)}"

print("=" * 100)
print("COMPLETE ALGORITHM SUBMISSION VALIDATION")
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
    solves_verified = 0
    solves_failed = 0

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

        # Check 3: Solving validation (if case found and pycuber available)
        if case_exists and is_valid_notation and case_data.get('scramble'):
            solves, solve_msg = validate_solving_pycuber(case_data['scramble'], sub['sequence'])
            if solves is True:
                print(f"✅ Algorithm solves the case")
                solves_verified += 1
            elif solves is False:
                print(f"❌ {solve_msg}")
                issues.append(solve_msg)
                solves_failed += 1
            elif solves is None:
                print(f"⚠️  {solve_msg}")
        elif case_exists and is_valid_notation:
            print(f"ℹ️  No scramble available - cannot verify solving")

        # Check 4: Duplicate detection
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
    if HAS_CUBE_SOLVER:
        print(f"\nSolving verification:")
        print(f"  ✅ Verified solving: {solves_verified}")
        print(f"  ❌ Does NOT solve: {solves_failed}")
    print("=" * 100)

except Exception as e:
    print(f"❌ Error validating submissions: {e}")
    exit(1)
