#!/usr/bin/env python3
"""
Validate and approve algorithm submissions.

This script:
1. Validates pending submissions (notation, duplicates, solving)
2. Shows validation results
3. Adds approved algorithms to lib_algorithms table
4. Updates submission status to 'approved'

Usage:
    # Interactive mode (prompts for each submission)
    python3 approve_submissions.py

    # Auto-approve all valid submissions (dry run first)
    python3 approve_submissions.py --auto-approve --dry-run

    # Auto-approve all valid submissions (production)
    python3 approve_submissions.py --auto-approve

    # Approve specific submission by ID
    python3 approve_submissions.py --submission-id <uuid>

Requirements:
    pip install supabase

Environment:
    SUPABASE_SERVICE_ROLE_KEY - Service role key for database access
"""

import os
import re
import uuid
import hashlib
import argparse
from datetime import datetime, timezone
from supabase import create_client

# Supabase configuration
SUPABASE_URL = "https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_ROLE_KEY environment variable not set")
    exit(1)

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Valid move notation pattern
VALID_MOVES = re.compile(r"^[RUFLDBMESxyzrufldб]['2]?$")

# =============================================================================
# LEGACY CODE RESOLUTION
# =============================================================================

def resolve_legacy_case_code(case_code: str) -> str | None:
    """
    Resolve legacy case codes to canonical format using database pattern matching.

    Examples:
        OLL-22 → 3X3-CFOP-OLL-22
        F2L-01 → 3X3-CFOP-F2L-01-FR (or similar)

    Args:
        case_code: Legacy or canonical case code

    Returns:
        Canonical code if found, None otherwise
    """
    # Try exact match first
    result = supabase.table('lib_cases')\
        .select('code')\
        .eq('code', case_code)\
        .limit(1)\
        .execute()

    if result.data:
        return result.data[0]['code']

    # Try pattern matching: %-{legacy_code}
    result = supabase.table('lib_cases')\
        .select('code')\
        .like('code', f'%-{case_code}')\
        .limit(1)\
        .execute()

    if result.data:
        return result.data[0]['code']

    return None

def generate_algorithm_code(case_code: str, sequence: str) -> str:
    """
    Generate hash-based algorithm code.

    Format: ALG-{5-char-hash}-{case_code}

    The hash is computed from the normalized sequence:
    - Remove spaces
    - Remove apostrophes
    - Convert to lowercase
    - Compute MD5 hash
    - Take first 5 hex characters (uppercase)

    Args:
        case_code: Canonical case code (e.g., "3X3-CFOP-OLL-22")
        sequence: Algorithm move sequence (e.g., "R U R' U'")

    Returns:
        Algorithm code in format ALG-{hash}-{case_code}

    Example:
        sequence = "R U R' U'"
        case_code = "3X3-CFOP-OLL-22"
        → "ALG-A1B2C-3X3-CFOP-OLL-22"
    """
    # Normalize: remove spaces and apostrophes, lowercase
    normalized = sequence.replace(" ", "").replace("'", "").lower()

    # Compute MD5 hash
    hash_input = normalized.encode('utf-8')
    hash_digest = hashlib.md5(hash_input).hexdigest()[:5].upper()

    # Format: ALG-{hash}-{case_code}
    return f"ALG-{hash_digest}-{case_code}"

# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_move_notation(sequence: str) -> tuple[bool, str]:
    """Validate algorithm move notation."""
    moves = sequence.split()
    for move in moves:
        if not VALID_MOVES.match(move):
            return False, f"Invalid move: '{move}'"
    return True, ""

def check_case_exists(case_code: str) -> tuple[bool, dict]:
    """
    Check if case exists, trying legacy code resolution if needed.

    Args:
        case_code: Case code (legacy or canonical)

    Returns:
        (exists, case_data_dict)
        case_data_dict includes 'code' with the canonical code
    """
    # Try exact match first
    result = supabase.table('lib_cases')\
        .select('id, code, title, case_set_id')\
        .eq('code', case_code)\
        .execute()

    if result.data:
        return True, result.data[0]

    # Try legacy code resolution
    canonical_code = resolve_legacy_case_code(case_code)
    if canonical_code and canonical_code != case_code:
        result = supabase.table('lib_cases')\
            .select('id, code, title, case_set_id')\
            .eq('code', canonical_code)\
            .execute()

        if result.data:
            return True, result.data[0]

    return False, {}

def check_duplicate(case_id: str, sequence: str) -> tuple[bool, dict]:
    """Check if algorithm already exists for this case."""
    # Normalize sequence
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

def validate_submission(submission: dict) -> tuple[bool, list[str]]:
    """
    Validate a submission for approval.

    Returns: (is_valid, list_of_errors)
    """
    errors = []

    # Validate move notation
    is_valid_notation, notation_error = validate_move_notation(submission['sequence'])
    if not is_valid_notation:
        errors.append(f"Invalid notation: {notation_error}")

    # Check case exists
    case_exists, case_data = check_case_exists(submission['case_code'])
    if not case_exists:
        errors.append(f"Case '{submission['case_code']}' not found in database")
    else:
        # Check for duplicates
        is_duplicate, duplicate_data = check_duplicate(case_data['id'], submission['sequence'])
        if is_duplicate:
            errors.append(f"Duplicate algorithm (ID: {duplicate_data['id']})")

    return len(errors) == 0, errors

# =============================================================================
# DATABASE OPERATIONS
# =============================================================================

def add_algorithm_to_library(submission: dict, case_data: dict, dry_run: bool = False) -> tuple[bool, str]:
    """
    Add approved algorithm to lib_algorithms table with hash-based code.

    Args:
        submission: Submission data with sequence and notes
        case_data: Case data with canonical code
        dry_run: If True, only preview changes

    Returns:
        (success, algorithm_id or error_message)
    """
    # Generate new algorithm ID
    alg_id = str(uuid.uuid4())

    # Generate hash-based algorithm code: ALG-{hash}-{case_code}
    alg_code = generate_algorithm_code(case_data['code'], submission['sequence'])

    # Check for hash collision (algorithm with same code already exists)
    existing = supabase.table('lib_algorithms')\
        .select('id, sequence')\
        .eq('code', alg_code)\
        .execute()

    if existing.data:
        return False, f"Algorithm with this code already exists (duplicate sequence): {alg_code}"

    # Prepare algorithm data
    algorithm = {
        'id': alg_id,
        'case_id': case_data['id'],
        'code': alg_code,  # ALG-{hash}-{case_code}
        'name': submission.get('notes') or 'User Algorithm',
        'sequence': submission['sequence'],
        'tags': ['user_submitted'],
        'difficulty': None,
        'popularity': 0,
        'avg_moves': len(submission['sequence'].split()),
        'avg_execution_time_ms': None,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'story': None,
    }

    if dry_run:
        print(f"      [DRY RUN] Would create algorithm: {alg_code}")
        return True, alg_id

    try:
        # Insert algorithm
        supabase.table('lib_algorithms').insert(algorithm).execute()
        return True, alg_id
    except Exception as e:
        return False, str(e)

def update_submission_status(submission_id: str, status: str, algorithm_id: str = None,
                            rejection_reason: str = None, dry_run: bool = False) -> bool:
    """
    Update submission status (approved/rejected).

    Returns: success
    """
    update_data = {
        'status': status,
        'reviewed_at': datetime.now(timezone.utc).isoformat(),
        'reviewed_by': None,  # NULL = automated review
    }

    if status == 'rejected' and rejection_reason:
        update_data['rejection_reason'] = rejection_reason

    if dry_run:
        print(f"      [DRY RUN] Would update submission status to '{status}'")
        if rejection_reason:
            print(f"      [DRY RUN] Rejection reason: {rejection_reason}")
        return True

    try:
        supabase.table('lib_algorithm_submissions')\
            .update(update_data)\
            .eq('id', submission_id)\
            .execute()
        return True
    except Exception as e:
        print(f"      ❌ Error updating submission: {e}")
        return False

def get_user_email(user_id: str) -> str:
    """Get user email from auth.users."""
    try:
        response = supabase.auth.admin.get_user_by_id(user_id)
        if response and response.user:
            return response.user.email or "Unknown"
    except:
        pass
    return "Unknown"

# =============================================================================
# APPROVAL WORKFLOWS
# =============================================================================

def approve_submission(submission: dict, case_data: dict, dry_run: bool = False) -> bool:
    """
    Approve a submission: add to library and update status.

    Returns: success
    """
    # Add to library
    success, result = add_algorithm_to_library(submission, case_data, dry_run)
    if not success:
        print(f"      ❌ Failed to add algorithm: {result}")
        return False

    alg_id = result
    print(f"      ✅ Algorithm added to library: {alg_id}")

    # Update submission status
    if update_submission_status(submission['id'], 'approved', alg_id, dry_run=dry_run):
        print(f"      ✅ Submission marked as approved")
        return True
    else:
        print(f"      ⚠️  Algorithm added but failed to update submission status")
        return False

def reject_submission(submission: dict, reason: str, dry_run: bool = False) -> bool:
    """
    Reject a submission with a reason.

    Returns: success
    """
    if update_submission_status(submission['id'], 'rejected', rejection_reason=reason, dry_run=dry_run):
        print(f"      ✅ Submission rejected: {reason}")
        return True
    else:
        return False

def process_submission(submission: dict, auto_approve: bool = False, dry_run: bool = False) -> str:
    """
    Process a single submission.

    Returns: 'approved', 'rejected', 'skipped'
    """
    print(f"\n{'-'*100}")
    print(f"Submission ID: {submission['id']}")
    print(f"Case Code: {submission['case_code']}")
    print(f"Algorithm: {submission['sequence']}")

    # Get submitter info
    user_email = get_user_email(submission['submitted_by'])
    print(f"Submitted by: {user_email}")

    if submission.get('notes'):
        print(f"Notes: {submission['notes']}")

    # Validate
    is_valid, errors = validate_submission(submission)

    if is_valid:
        print(f"\n   ✅ Validation passed")

        # Get case data for approval
        _, case_data = check_case_exists(submission['case_code'])

        if auto_approve:
            print(f"   🤖 Auto-approving...")
            if approve_submission(submission, case_data, dry_run):
                return 'approved'
            else:
                return 'rejected'
        else:
            # Interactive mode
            response = input(f"\n   Approve this submission? [y/N/s=skip]: ").strip().lower()
            if response == 'y':
                if approve_submission(submission, case_data, dry_run):
                    return 'approved'
                else:
                    return 'rejected'
            elif response == 's':
                print(f"   ⏸️  Skipped")
                return 'skipped'
            else:
                print(f"   ⏸️  Not approved")
                return 'skipped'
    else:
        print(f"\n   ❌ Validation failed:")
        for error in errors:
            print(f"      - {error}")

        if auto_approve:
            print(f"   🤖 Auto-rejecting...")
            reason = "; ".join(errors)
            if reject_submission(submission, reason, dry_run):
                return 'rejected'
            else:
                return 'skipped'
        else:
            # Interactive mode
            response = input(f"\n   Reject this submission? [y/N]: ").strip().lower()
            if response == 'y':
                reason = "; ".join(errors)
                if reject_submission(submission, reason, dry_run):
                    return 'rejected'
                else:
                    return 'skipped'
            else:
                print(f"   ⏸️  Not rejected")
                return 'skipped'

def process_all_submissions(auto_approve: bool = False, dry_run: bool = False):
    """Process all pending submissions."""
    print("="*100)
    print("ALGORITHM SUBMISSION APPROVAL")
    if dry_run:
        print("[DRY RUN MODE - No changes will be made]")
    print("="*100)

    # Get pending submissions
    try:
        submissions = supabase.table('lib_algorithm_submissions')\
            .select('*')\
            .eq('status', 'pending')\
            .order('created_at')\
            .execute()
    except Exception as e:
        print(f"❌ Error fetching submissions: {e}")
        exit(1)

    if not submissions.data:
        print("\n✅ No pending submissions found.")
        return

    print(f"\nFound {len(submissions.data)} pending submission(s)")

    approved_count = 0
    rejected_count = 0
    skipped_count = 0

    for submission in submissions.data:
        result = process_submission(submission, auto_approve, dry_run)
        if result == 'approved':
            approved_count += 1
        elif result == 'rejected':
            rejected_count += 1
        else:
            skipped_count += 1

    # Summary
    print(f"\n{'='*100}")
    print("SUMMARY")
    print(f"{'='*100}")
    print(f"Total: {len(submissions.data)}")
    print(f"✅ Approved: {approved_count}")
    print(f"❌ Rejected: {rejected_count}")
    print(f"⏸️  Skipped: {skipped_count}")

    if dry_run:
        print(f"\n⚠️  DRY RUN MODE - No changes were made to the database")

    print(f"{'='*100}")

def process_single_submission(submission_id: str, auto_approve: bool = False, dry_run: bool = False):
    """Process a single submission by ID."""
    print("="*100)
    print(f"PROCESSING SUBMISSION: {submission_id}")
    if dry_run:
        print("[DRY RUN MODE - No changes will be made]")
    print("="*100)

    try:
        result = supabase.table('lib_algorithm_submissions')\
            .select('*')\
            .eq('id', submission_id)\
            .execute()

        if not result.data:
            print(f"\n❌ Submission not found: {submission_id}")
            return

        submission = result.data[0]

        if submission['status'] != 'pending':
            print(f"\n⚠️  Submission already processed (status: {submission['status']})")
            return

        process_submission(submission, auto_approve, dry_run)

    except Exception as e:
        print(f"❌ Error: {e}")

# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Validate and approve algorithm submissions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (prompts for each)
  %(prog)s

  # Auto-approve all valid (dry run)
  %(prog)s --auto-approve --dry-run

  # Auto-approve all valid (production)
  %(prog)s --auto-approve

  # Approve specific submission
  %(prog)s --submission-id abc123...
        """
    )

    parser.add_argument('--submission-id', metavar='UUID', help='Process specific submission by ID')
    parser.add_argument('--auto-approve', action='store_true', help='Automatically approve valid submissions')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')

    args = parser.parse_args()

    if args.submission_id:
        process_single_submission(args.submission_id, args.auto_approve, args.dry_run)
    else:
        process_all_submissions(args.auto_approve, args.dry_run)

if __name__ == "__main__":
    main()
