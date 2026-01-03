#!/usr/bin/env python3
"""
CI-friendly seed data validation (no database required).

Validates all seeddata_*.json files using existing validators:
- JSON schema validation (schema_validator.py)
- UUID format validation (validators.py)
- Required field validation (validators.py)
- Foreign key integrity across files (validators.py)

Usage:
    python ci_validate.py              # Validate all seed data files
    python ci_validate.py --verbose    # Show detailed output
"""

import argparse
import json
import sys
from pathlib import Path

# Add scripts/ to path for imports
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

from schema_validator import SchemaValidator
import validators

# Seed data location relative to this script
SEED_DATA_DIR = SCRIPTS_DIR.parent.parent / "DeddalInfra/Infrastructure/Persistence/SeedData"
SCHEMAS_DIR = SCRIPTS_DIR.parent / "schemas"


def determine_file_type(filename: str) -> str:
    """Determine file type from filename pattern."""
    if "caseset" in filename:
        return "case_sets"
    elif "cases" in filename:
        return "cases"
    elif "algorithms" in filename:
        return "algorithms"
    return "unknown"


def main():
    parser = argparse.ArgumentParser(description="Validate seed data JSON files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    args = parser.parse_args()

    if not SEED_DATA_DIR.exists():
        print(f"❌ Seed data directory not found: {SEED_DATA_DIR}")
        sys.exit(1)

    if not SCHEMAS_DIR.exists():
        print(f"❌ Schemas directory not found: {SCHEMAS_DIR}")
        sys.exit(1)

    # Initialize schema validator
    schema_validator = SchemaValidator(SCHEMAS_DIR)

    all_errors = []
    all_case_sets = []
    all_cases = []
    all_algorithms = []

    # Load and validate all files
    json_files = sorted(SEED_DATA_DIR.glob("seeddata_*.json"))
    print(f"Found {len(json_files)} seed data files")

    for json_file in json_files:
        file_type = determine_file_type(json_file.name)
        if file_type == "unknown":
            print(f"  ⚠️  Skipping unknown file type: {json_file.name}")
            continue

        try:
            with open(json_file, 'r') as f:
                records = json.load(f)
        except json.JSONDecodeError as e:
            all_errors.append(f"{json_file.name}: Invalid JSON - {e}")
            continue

        # Schema validation
        errors = schema_validator.validate(records, file_type, json_file.name)
        all_errors.extend(errors)

        # UUID validation
        errors = validators.validate_uuids(records)
        all_errors.extend([f"{json_file.name}: {e}" for e in errors])

        # Required fields
        errors = validators.validate_required_fields(records, file_type)
        all_errors.extend([f"{json_file.name}: {e}" for e in errors])

        # Collect for cross-file validation
        if file_type == "case_sets":
            all_case_sets.extend(records)
        elif file_type == "cases":
            all_cases.extend(records)
        elif file_type == "algorithms":
            all_algorithms.extend(records)

        if args.verbose:
            print(f"  ✓ {json_file.name} ({len(records)} records)")

    # Cross-file FK validation
    if args.verbose:
        print("\nCross-file validation...")

    errors = validators.validate_foreign_keys(all_algorithms, all_cases)
    all_errors.extend([f"FK: {e}" for e in errors])

    errors = validators.validate_case_set_relationships(all_case_sets, all_cases)
    all_errors.extend([f"FK: {e}" for e in errors])

    # Report results
    if all_errors:
        print(f"\n❌ Validation failed with {len(all_errors)} errors:")
        for error in all_errors[:20]:  # Limit output
            print(f"  - {error}")
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors) - 20} more")
        sys.exit(1)

    print(f"\n✅ All {len(json_files)} seed data files pass validation")
    print(f"   {len(all_case_sets)} case sets, {len(all_cases)} cases, {len(all_algorithms)} algorithms")
    sys.exit(0)


if __name__ == "__main__":
    main()
