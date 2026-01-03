"""
Data validation functions for seed data export.

Validates exported data against iOS DTO requirements:
- UUID format validation
- Foreign key integrity
- Required field validation
- Case count validation
"""

import uuid
from typing import List, Dict, Any, Set


def validate_uuids(records: List[Dict[str, Any]], field_name: str = 'id') -> List[str]:
    """
    Validate that all IDs are valid UUIDs.

    Args:
        records: List of records to validate
        field_name: Name of the UUID field to check

    Returns:
        List of error messages (empty if all valid)
    """
    errors = []
    for idx, record in enumerate(records):
        if field_name not in record:
            errors.append(f"Record {idx}: Missing '{field_name}' field")
            continue

        try:
            uuid.UUID(str(record[field_name]))
        except (ValueError, AttributeError):
            errors.append(f"Record {idx}: Invalid UUID '{record[field_name]}'")

    return errors


def validate_required_fields(records: List[Dict[str, Any]], file_type: str) -> List[str]:
    """
    Validate required fields based on file type.

    Args:
        records: List of records to validate
        file_type: Type of file ('case_sets', 'cases', 'algorithms')

    Returns:
        List of error messages (empty if all valid)
    """
    required_fields = {
        'case_sets': ['id', 'code', 'name'],
        'cases': ['id', 'code', 'kind'],
        'algorithms': ['id', 'case_id', 'code', 'sequence']
    }

    if file_type not in required_fields:
        return [f"Unknown file type: {file_type}"]

    errors = []
    fields = required_fields[file_type]

    for idx, record in enumerate(records):
        for field in fields:
            value = record.get(field)
            is_missing = value is None or (field not in record)

            # Special case: Allow empty sequence for "Skip" algorithms (no moves needed)
            if file_type == 'algorithms' and field == 'sequence':
                name = (record.get('name') or '').lower()
                is_skip = name in ('skip', 'solved', 'none', '')
                if is_skip and value == '':
                    continue  # Empty sequence is valid for skip cases
                if value == '':
                    is_missing = True

            if is_missing:
                errors.append(f"Record {idx} (code={record.get('code', 'unknown')}): Missing required field '{field}'")

    return errors


def validate_foreign_keys(
    algorithms: List[Dict[str, Any]],
    cases: List[Dict[str, Any]]
) -> List[str]:
    """
    Validate foreign key relationships between algorithms and cases.

    Args:
        algorithms: List of algorithm records
        cases: List of case records

    Returns:
        List of error messages (empty if all valid)
    """
    errors = []

    # Build set of valid case IDs
    case_ids: Set[str] = {str(case['id']) for case in cases if 'id' in case}

    # Check each algorithm's case_id
    for algo in algorithms:
        if 'case_id' not in algo:
            errors.append(f"Algorithm {algo.get('code', 'unknown')}: Missing case_id")
            continue

        case_id = str(algo['case_id'])
        if case_id not in case_ids:
            errors.append(
                f"Algorithm {algo.get('code', 'unknown')}: "
                f"References non-existent case_id {case_id}"
            )

    return errors


def validate_case_set_relationships(
    case_sets: List[Dict[str, Any]],
    cases: List[Dict[str, Any]]
) -> List[str]:
    """
    Validate case_ids in case sets reference existing cases.

    Args:
        case_sets: List of case set records
        cases: List of case records

    Returns:
        List of error messages (empty if all valid)
    """
    errors = []

    # Build set of valid case IDs
    case_ids: Set[str] = {str(case['id']) for case in cases if 'id' in case}

    # Check each case set's case_ids array
    for case_set in case_sets:
        if 'case_ids' not in case_set or case_set['case_ids'] is None:
            continue  # case_ids is optional

        for case_id_ref in case_set['case_ids']:
            # case_id_ref can be a string UUID or an object {"id": "...", "code": "..."}
            if isinstance(case_id_ref, dict):
                case_id = str(case_id_ref.get('id', ''))
            else:
                case_id = str(case_id_ref)

            if case_id not in case_ids:
                errors.append(
                    f"Case set {case_set.get('code', 'unknown')}: "
                    f"References non-existent case_id {case_id} in case_ids array"
                )

    return errors


def validate_case_kind_enum(
    records: List[Dict[str, Any]],
    valid_kinds: Set[str] = None,
    db_conn = None
) -> List[str]:
    """
    Validate that case 'kind' field matches valid case kinds from database.

    NOTE: This function now uses DYNAMIC DISCOVERY from the database.
    Case kinds are NOT hardcoded - they are discovered at runtime by querying
    the lib_cases table for all distinct 'kind' values.

    Args:
        records: List of case records
        valid_kinds: Optional set of valid kinds (if None, will query database)
        db_conn: Optional database connection (if None and valid_kinds is None, will create connection)

    Returns:
        List of error messages (empty if all valid)
    """
    # If valid_kinds not provided, discover from database
    if valid_kinds is None:
        if db_conn is None:
            return ["validate_case_kind_enum: db_conn is required when valid_kinds not provided"]
        should_close_conn = False

        # Query database for all distinct case kinds
        cursor = db_conn.cursor()
        cursor.execute("SELECT DISTINCT kind FROM lib_cases WHERE kind IS NOT NULL ORDER BY kind")
        valid_kinds = {row[0] for row in cursor.fetchall()}
        cursor.close()

    errors = []
    for record in records:
        if 'kind' not in record:
            continue  # Will be caught by required field validation

        kind = record['kind']
        if kind not in valid_kinds:
            errors.append(
                f"Case {record.get('code', 'unknown')}: "
                f"Invalid kind '{kind}' (not in database)"
            )

    return errors


def validate_case_count(
    case_set: Dict[str, Any],
    actual_count: int
) -> List[str]:
    """
    Validate actual case count matches expected_count in case set.

    Args:
        case_set: Case set record with expected_count
        actual_count: Actual number of cases found

    Returns:
        List of warning messages (empty if counts match)
    """
    warnings = []

    if 'expected_count' not in case_set or case_set['expected_count'] is None:
        return warnings  # No expected count defined

    expected = case_set['expected_count']
    if actual_count != expected:
        warnings.append(
            f"Case set {case_set.get('code', 'unknown')}: "
            f"Expected {expected} cases, found {actual_count}"
        )

    return warnings


def validate_data_completeness(records: List[Dict[str, Any]], file_name: str) -> List[str]:
    """
    Check for empty or suspiciously small datasets.

    Args:
        records: List of records
        file_name: Name of the file being validated

    Returns:
        List of warning messages
    """
    warnings = []

    # Files that legitimately have low record counts
    low_count_ok = (
        'caseset_' in file_name or  # Caseset files always have exactly 1 record
        'parity' in file_name or     # Parity files can have 1-5 cases
        '-l1-' in file_name or       # Layer 1 beginner methods
        '-l2-' in file_name or       # Layer 2 beginner methods
        '-l3-' in file_name          # Layer 3 beginner methods
    )

    if len(records) == 0:
        warnings.append(f"{file_name}: No records found (empty dataset)")
    elif len(records) < 3 and not low_count_ok:
        warnings.append(
            f"{file_name}: Only {len(records)} records found (suspiciously low count)"
        )

    return warnings
