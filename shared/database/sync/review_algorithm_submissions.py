#!/usr/bin/env python3
"""
Review and approve/reject user-submitted algorithms.

This script provides a secure workflow for reviewing algorithm submissions:
- Validates move notation and security
- Detects duplicates
- Approves/rejects submissions
- Updates database atomically

Usage:
    # Review all pending submissions (dry-run)
    python3 review_algorithm_submissions.py --all --dry-run

    # Auto-approve all valid submissions
    python3 review_algorithm_submissions.py --all --auto-approve

    # Review specific submission
    python3 review_algorithm_submissions.py --submission-id <uuid>

    # Reject submission
    python3 review_algorithm_submissions.py --reject <uuid> --reason "Invalid notation"

Requirements:
    pip install supabase

Environment:
    SUPABASE_SERVICE_ROLE_KEY - Service role key for database access
"""

import os
import re
import sys
import uuid
import argparse
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
from supabase import create_client, Client

# Supabase configuration
SUPABASE_URL = "https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_ROLE_KEY environment variable not set")
    exit(1)

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# System reviewer ID (for automated approvals)
SYSTEM_REVIEWER_ID = "00000000-0000-0000-0000-000000000000"

# Valid cube move notation pattern
MOVE_PATTERN = re.compile(r"^[RUFLDBMESxyz]['2]?\s*$")
MAX_SEQUENCE_LENGTH = 500  # characters


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================

def validate_move_notation(sequence: str) -> Tuple[bool, Optional[str]]:
    """
    Validate cube algorithm move notation.

    Returns: (is_valid, error_message)
    """
    if not sequence or not sequence.strip():
        return False, "Empty sequence"

    if len(sequence) > MAX_SEQUENCE_LENGTH:
        return False, f"Sequence too long (max {MAX_SEQUENCE_LENGTH} chars)"

    # Split by whitespace and validate each move
    moves = sequence.strip().split()

    for move in moves:
        if not MOVE_PATTERN.match(move):
            return False, f"Invalid move notation: '{move}'"

    return True, None


def check_case_exists(case_id: str) -> bool:
    """Check if case_id exists in lib_cases table."""
    try:
        response = supabase.table('lib_cases').select('id').eq('id', case_id).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"  ⚠️  Error checking case: {e}")
        return False


def check_user_exists(user_id: str) -> bool:
    """Check if user exists in users table."""
    if not user_id:
        return False

    try:
        response = supabase.table('users').select('id').eq('id', user_id).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"  ⚠️  Error checking user: {e}")
        return False


def check_algorithm_exists(case_id: str, sequence: str) -> bool:
    """Check if this exact algorithm already exists for the case."""
    try:
        response = supabase.table('lib_algorithms').select('id').eq('case_id', case_id).eq('sequence', sequence).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"  ⚠️  Error checking existing algorithms: {e}")
        return False


# =============================================================================
# SUBMISSION PROCESSING
# =============================================================================

def get_pending_submissions() -> List[Dict]:
    """Fetch all pending submissions."""
    try:
        response = supabase.table('lib_algorithm_submissions').select('*').eq('status', 'pending').order('created_at').execute()
        return response.data
    except Exception as e:
        print(f"❌ Error fetching submissions: {e}")
        return []


def get_submission_by_id(submission_id: str) -> Optional[Dict]:
    """Fetch a specific submission by ID."""
    try:
        response = supabase.table('lib_algorithm_submissions').select('*').eq('id', submission_id).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"❌ Error fetching submission: {e}")
        return None


def find_duplicate_submissions(submissions: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Group submissions by (case_id, sequence) to find duplicates.

    Returns: Dict mapping (case_id, sequence) to list of submissions
    """
    groups = {}

    for sub in submissions:
        key = (sub['case_id'], sub['sequence'])
        if key not in groups:
            groups[key] = []
        groups[key].append(sub)

    return groups


def validate_submission(submission: Dict) -> Tuple[bool, Optional[str]]:
    """
    Validate a submission for approval.

    Returns: (is_valid, error_message)
    """
    # Validate move notation
    is_valid, error = validate_move_notation(submission['sequence'])
    if not is_valid:
        return False, f"Invalid notation: {error}"

    # Check case exists
    if not check_case_exists(submission['case_id']):
        return False, f"Case ID not found: {submission['case_id']}"

    # Check if algorithm already exists
    if check_algorithm_exists(submission['case_id'], submission['sequence']):
        return False, "Algorithm already exists for this case"

    return True, None


def approve_submission(submission: Dict, dry_run: bool = False) -> bool:
    """
    Approve a submission and insert algorithm into lib_algorithms.

    Returns: True if successful, False otherwise
    """
    # Generate new algorithm ID
    alg_id = str(uuid.uuid4())

    # Prepare algorithm data
    algorithm = {
        'id': alg_id,
        'case_id': submission['case_id'],
        'code': f"{submission['case_code']}-USR",  # User-submitted tag
        'name': f"User Algorithm",
        'sequence': submission['sequence'],
        'tags': ['user_submitted'],
        'difficulty': None,
        'popularity': 0,
        'avg_moves': None,
        'avg_execution_time_ms': None,
        'created_at': datetime.now(timezone.utc).isoformat(),
        'story': None,
    }

    # Prepare submission update
    submission_update = {
        'status': 'approved',
        'reviewed_at': datetime.now(timezone.utc).isoformat(),
        'reviewed_by': None,  # NULL - automated system review
    }

    if dry_run:
        print(f"  [DRY RUN] Would insert algorithm: {alg_id}")
        print(f"  [DRY RUN] Would update submission status to 'approved'")
        return True

    try:
        # Insert algorithm
        supabase.table('lib_algorithms').insert(algorithm).execute()

        # Update submission
        supabase.table('lib_algorithm_submissions').update(submission_update).eq('id', submission['id']).execute()

        return True
    except Exception as e:
        print(f"  ❌ Error approving submission: {e}")
        return False


def reject_submission(submission: Dict, reason: str, dry_run: bool = False) -> bool:
    """
    Reject a submission with a reason.

    Returns: True if successful, False otherwise
    """
    submission_update = {
        'status': 'rejected',
        'reviewed_at': datetime.now(timezone.utc).isoformat(),
        'reviewed_by': None,  # NULL - automated system review
        'rejection_reason': reason,
    }

    if dry_run:
        print(f"  [DRY RUN] Would update submission status to 'rejected'")
        print(f"  [DRY RUN] Reason: {reason}")
        return True

    try:
        supabase.table('lib_algorithm_submissions').update(submission_update).eq('id', submission['id']).execute()
        return True
    except Exception as e:
        print(f"  ❌ Error rejecting submission: {e}")
        return False


def mark_as_duplicate(submission: Dict, dry_run: bool = False) -> bool:
    """
    Mark a submission as duplicate (special rejection reason).

    Returns: True if successful, False otherwise
    """
    return reject_submission(submission, "Duplicate submission", dry_run)


# =============================================================================
# MAIN WORKFLOWS
# =============================================================================

def review_all_submissions(auto_approve: bool = False, dry_run: bool = False):
    """Review all pending submissions."""
    print("="*80)
    print("REVIEWING ALL PENDING SUBMISSIONS")
    print("="*80)

    submissions = get_pending_submissions()

    if not submissions:
        print("\n✅ No pending submissions found.")
        return

    print(f"\nFound {len(submissions)} pending submission(s)\n")

    # Group by case + sequence to detect duplicates
    groups = find_duplicate_submissions(submissions)

    approved_count = 0
    rejected_count = 0
    duplicate_count = 0

    for (case_id, sequence), group in groups.items():
        # Take the oldest submission as primary
        primary = group[0]
        duplicates = group[1:]

        print("-"*80)
        print(f"Case: {primary['case_code']}")
        print(f"Algorithm: {sequence[:70]}{'...' if len(sequence) > 70 else ''}")
        print(f"Submissions: {len(group)} (1 primary + {len(duplicates)} duplicate(s))")

        # Validate primary submission
        is_valid, error = validate_submission(primary)

        if is_valid:
            print(f"✅ Validation passed")

            if auto_approve:
                if approve_submission(primary, dry_run):
                    print(f"✅ Approved submission {primary['id'][:8]}...")
                    approved_count += 1
                else:
                    print(f"❌ Failed to approve")
                    rejected_count += 1
            else:
                print(f"⏸️  Awaiting manual approval (use --auto-approve)")
        else:
            print(f"❌ Validation failed: {error}")
            if auto_approve:
                if reject_submission(primary, error, dry_run):
                    print(f"❌ Rejected submission {primary['id'][:8]}...")
                    rejected_count += 1

        # Handle duplicates
        for dup in duplicates:
            print(f"  📋 Duplicate: {dup['id'][:8]}... (created {dup['created_at']})")
            if auto_approve:
                if mark_as_duplicate(dup, dry_run):
                    print(f"  ❌ Marked as duplicate")
                    duplicate_count += 1

    # Summary
    print("\n" + "="*80)
    print("REVIEW SUMMARY")
    print("="*80)
    print(f"Approved: {approved_count}")
    print(f"Rejected: {rejected_count}")
    print(f"Duplicates: {duplicate_count}")

    if dry_run:
        print("\n⚠️  DRY RUN MODE - No changes were made to the database")


def review_single_submission(submission_id: str, auto_approve: bool = False, dry_run: bool = False):
    """Review a single submission by ID."""
    print("="*80)
    print(f"REVIEWING SUBMISSION: {submission_id}")
    print("="*80)

    submission = get_submission_by_id(submission_id)

    if not submission:
        print(f"\n❌ Submission not found: {submission_id}")
        return

    print(f"\nCase: {submission['case_code']}")
    print(f"Algorithm: {submission['sequence']}")
    print(f"Status: {submission['status']}")
    print(f"Submitted: {submission['created_at']}")
    print(f"Submitted by: {submission['submitted_by']}")

    # Validate
    is_valid, error = validate_submission(submission)

    if is_valid:
        print(f"\n✅ Validation passed")

        if auto_approve:
            if approve_submission(submission, dry_run):
                print(f"✅ Approved!")
            else:
                print(f"❌ Failed to approve")
        else:
            print(f"\n⏸️  Use --auto-approve to approve this submission")
    else:
        print(f"\n❌ Validation failed: {error}")


def reject_submission_by_id(submission_id: str, reason: str, dry_run: bool = False):
    """Reject a specific submission."""
    print("="*80)
    print(f"REJECTING SUBMISSION: {submission_id}")
    print("="*80)

    submission = get_submission_by_id(submission_id)

    if not submission:
        print(f"\n❌ Submission not found: {submission_id}")
        return

    print(f"\nCase: {submission['case_code']}")
    print(f"Algorithm: {submission['sequence']}")
    print(f"Reason: {reason}")

    if reject_submission(submission, reason, dry_run):
        print(f"\n✅ Rejected!")
    else:
        print(f"\n❌ Failed to reject")


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Review and approve/reject user-submitted algorithms",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Review all pending submissions (dry-run)
  %(prog)s --all --dry-run

  # Auto-approve all valid submissions
  %(prog)s --all --auto-approve

  # Review specific submission
  %(prog)s --submission-id abc123...

  # Reject submission
  %(prog)s --reject abc123... --reason "Invalid notation"
        """
    )

    parser.add_argument('--all', action='store_true', help='Review all pending submissions')
    parser.add_argument('--submission-id', metavar='UUID', help='Review specific submission by ID')
    parser.add_argument('--reject', metavar='UUID', help='Reject submission by ID')
    parser.add_argument('--reason', metavar='TEXT', help='Rejection reason (required with --reject)')
    parser.add_argument('--auto-approve', action='store_true', help='Automatically approve valid submissions')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')

    args = parser.parse_args()

    # Validate arguments
    if not any([args.all, args.submission_id, args.reject]):
        parser.error("Must specify one of: --all, --submission-id, --reject")

    if args.reject and not args.reason:
        parser.error("--reject requires --reason")

    # Execute
    if args.all:
        review_all_submissions(auto_approve=args.auto_approve, dry_run=args.dry_run)
    elif args.submission_id:
        review_single_submission(args.submission_id, auto_approve=args.auto_approve, dry_run=args.dry_run)
    elif args.reject:
        reject_submission_by_id(args.reject, args.reason, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
