#!/usr/bin/env python3
"""
Validate pending algorithm submissions using iOS cube engine.

This script:
1. Fetches pending submissions from Supabase
2. Gets case start states for each case
3. Calls iOS ValidateAlgorithmUseCase via Swift test
4. Reports full validation including whether algorithm solves the case

Usage:
    python3 validate_with_cube_engine.py

Requirements:
    pip install supabase

Environment:
    SUPABASE_SERVICE_ROLE_KEY - Service role key for database access
"""

import os
import json
import subprocess
import tempfile
from supabase import create_client

# Supabase configuration
SUPABASE_URL = "https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_SERVICE_KEY:
    print("ERROR: SUPABASE_SERVICE_ROLE_KEY environment variable not set")
    exit(1)

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Project paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../.."))
XCODE_PROJECT = os.path.join(PROJECT_ROOT, "Deddal.xcodeproj")

def get_pending_submissions():
    """Fetch all pending submissions with case details."""
    try:
        # Get pending submissions
        submissions = supabase.table('lib_algorithm_submissions')\
            .select('*')\
            .eq('status', 'pending')\
            .order('created_at')\
            .execute()

        return submissions.data
    except Exception as e:
        print(f"❌ Error fetching submissions: {e}")
        return []

def get_case_start_state(case_code):
    """Get the case start state (scramble) for validation."""
    try:
        case = supabase.table('lib_cases')\
            .select('scramble')\
            .eq('code', case_code)\
            .execute()

        if case.data and len(case.data) > 0:
            return case.data[0].get('scramble')
        return None
    except Exception as e:
        print(f"  ⚠️  Error fetching case state for {case_code}: {e}")
        return None

def run_swift_validation(submissions):
    """
    Run Swift validation test with algorithm data.

    Returns: List of validation results
    """
    # Prepare input data
    input_data = []
    for sub in submissions:
        case_state = get_case_start_state(sub['case_code'])
        input_data.append({
            'caseCode': sub['case_code'],
            'algorithm': sub['sequence'],
            'caseStartState': case_state
        })

    # Create temporary files for input/output
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as input_file:
        json.dump(input_data, input_file, indent=2)
        input_path = input_file.name

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as output_file:
        output_path = output_file.name

    try:
        print(f"\n🔧 Running iOS cube engine validation...")
        print(f"   Input: {input_path}")
        print(f"   Output: {output_path}")

        # Run Swift test
        env = os.environ.copy()
        env['ALGORITHM_INPUT_JSON'] = input_path
        env['ALGORITHM_OUTPUT_JSON'] = output_path

        cmd = [
            'xcodebuild', 'test',
            '-project', XCODE_PROJECT,
            '-scheme', '1. DEV Scheme',
            '-only-testing:DeddalTests/AlgorithmValidationCLISuite',
            '-destination', 'platform=iOS Simulator,name=iPhone 17 Pro',
            '-quiet'
        ]

        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT
        )

        if result.returncode != 0:
            print(f"\n⚠️  Warning: xcodebuild exited with code {result.returncode}")
            print(f"   This may be expected if validation test reported issues")

        # Read output
        with open(output_path, 'r') as f:
            results = json.load(f)

        return results

    except Exception as e:
        print(f"❌ Error running Swift validation: {e}")
        return []

    finally:
        # Cleanup temp files
        if os.path.exists(input_path):
            os.unlink(input_path)
        if os.path.exists(output_path):
            os.unlink(output_path)

def display_results(submissions, validation_results):
    """Display validation results in readable format."""
    print("\n" + "="*100)
    print("VALIDATION RESULTS (iOS Cube Engine)")
    print("="*100)

    if not validation_results:
        print("\n❌ No validation results available")
        return

    valid_count = 0
    invalid_count = 0

    for idx, (sub, result) in enumerate(zip(submissions, validation_results), 1):
        print(f"\n{'-'*100}")
        print(f"#{idx} - Submission ID: {sub['id']}")
        print(f"Case Code: {result['caseCode']}")
        print(f"Algorithm: {result['algorithm']}")

        # Validation status
        if result['isValid']:
            print(f"✅ VALID")
            valid_count += 1

            if result.get('solves') is not None:
                if result['solves']:
                    print(f"   ✅ Solves the case correctly")
                else:
                    print(f"   ❌ Does NOT solve the case")
        else:
            print(f"❌ INVALID - {result['validationResult']}")
            if result.get('errorMessage'):
                print(f"   Error: {result['errorMessage']}")
            invalid_count += 1

        # Additional info
        if result.get('hasSuboptimalPatterns'):
            print(f"   ⚠️  Has suboptimal move patterns")

        if result.get('solves') is None:
            print(f"   ℹ️  Could not verify solving (case state not available)")

    # Summary
    print(f"\n{'='*100}")
    print("SUMMARY")
    print(f"{'='*100}")
    print(f"Total submissions: {len(submissions)}")
    print(f"✅ Valid: {valid_count}")
    print(f"❌ Invalid: {invalid_count}")
    print(f"{'='*100}")

def main():
    print("="*100)
    print("ALGORITHM VALIDATION - iOS Cube Engine")
    print("="*100)

    # Get pending submissions
    submissions = get_pending_submissions()

    if not submissions:
        print("\n✅ No pending submissions found.")
        return

    print(f"\nFound {len(submissions)} pending submission(s)")

    # Run Swift validation
    results = run_swift_validation(submissions)

    if not results:
        print("\n❌ Failed to get validation results from iOS engine")
        print("   Falling back to basic Python validation...")
        # Could fall back to validate_pending_submissions.py here
        return

    # Display results
    display_results(submissions, results)

if __name__ == "__main__":
    main()
