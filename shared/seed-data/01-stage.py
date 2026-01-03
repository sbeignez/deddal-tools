#!/usr/bin/env python3
"""
Seed Data Staging Script (Step 1 of 2)

Exports Supabase database tables to a staging directory with review report.
This is the first step in the 2-step export workflow.

Workflow:
  1. Stage (this script):  Database → staging/TIMESTAMP/ + HTML report
  2. Deploy (02-deploy.py): Review → Deploy to iOS directory

Features:
- Exports to staging/TIMESTAMP/ios/ for review
- Generates HTML report with diff comparison
- No automatic deployment - review before deploying
- Validates data integrity

Usage:
    python 01-stage.py                    # Export to staging with report
    python 01-stage.py --dry-run          # Preview without writing files
    python 01-stage.py --file oll_cases.json  # Stage single file
    python 01-stage.py --validate-only    # Validate only, no export
    python 01-stage.py --show-field-changes  # Show detailed diff
    python 01-stage.py --skip-schema-validation  # Skip JSON Schema validation

Next Step:
    python 02-deploy.py TIMESTAMP         # Deploy staged export to iOS
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
import yaml
from colorama import Fore, Style, init
from dotenv import load_dotenv

# Import from scripts/ package
ROOT_DIR = Path(__file__).parent
SCRIPTS_DIR = ROOT_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import validators
from diff_viewer import DiffViewer
from report_generator import ReportGenerator
from schema_validator import SchemaValidator

# Import from shared utilities
from shared_utils import format_json, print_header, STAGING_ROOT

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)


class SeedDataExporter:
    """Exports Supabase data to iOS seed JSON files."""

    def __init__(
        self,
        config_path: str = "scripts/config.yaml",
        dry_run: bool = False,
        enable_diff: bool = True,
        show_field_changes: bool = False,
        skip_schema_validation: bool = False
    ):
        """
        Initialize staging exporter.

        Args:
            config_path: Path to YAML config file
            dry_run: If True, don't write files (preview only)
            enable_diff: If True, show diff preview
            show_field_changes: If True, show field-level changes in diff
            skip_schema_validation: If True, skip JSON Schema validation
        """
        self.dry_run = dry_run
        self.enable_diff = enable_diff
        self.skip_schema_validation = skip_schema_validation
        self.staging_timestamp = None  # Set during export
        self.config = self._load_config(config_path)
        self.conn = None
        self.stats = {
            'files_exported': 0,
            'files_skipped': 0,
            'total_records': 0,
            'errors': [],
            'warnings': []
        }

        # Initialize diff manager
        self.diff_viewer = DiffViewer(show_field_changes=show_field_changes) if enable_diff else None
        self.comparisons = []  # Store diff results for summary

        # Initialize schema validator
        schemas_dir = ROOT_DIR / "schemas"
        self.schema_validator = SchemaValidator(schemas_dir=schemas_dir)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        config_file = Path(__file__).parent / config_path
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def connect_db(self):
        """Establish database connection using environment variables."""
        load_dotenv(SCRIPTS_DIR / '.env')

        required_vars = ['SUPABASE_HOST', 'SUPABASE_DATABASE', 'SUPABASE_USER', 'SUPABASE_PASSWORD']
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        try:
            self.conn = psycopg2.connect(
                host=os.getenv('SUPABASE_HOST'),
                port=int(os.getenv('SUPABASE_PORT', 5432)),
                database=os.getenv('SUPABASE_DATABASE'),
                user=os.getenv('SUPABASE_USER'),
                password=os.getenv('SUPABASE_PASSWORD')
            )
            print(f"{Fore.GREEN}✓ Connected to Supabase database{Style.RESET_ALL}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

    def close_db(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            print(f"{Fore.GREEN}✓ Database connection closed{Style.RESET_ALL}")

    def _discover_case_sets(self) -> List[Dict[str, Any]]:
        """
        Query database to discover all case sets.

        Returns:
            List of case set records with id, code, category
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, code, category
            FROM lib_casesets
            ORDER BY code
        """)

        case_sets = []
        for row in cursor.fetchall():
            case_sets.append({
                'id': str(row[0]),  # Convert UUID to string
                'code': row[1],
                'category': row[2]
            })

        cursor.close()
        return case_sets

    def _build_query_for_type(self, export_type: str, caseset_id: str) -> str:
        """
        Build SQL query for a specific export type and case set.

        Args:
            export_type: One of 'case_sets', 'cases', 'algorithms'
            caseset_id: UUID of the case set

        Returns:
            SQL query string
        """
        if export_type == 'case_sets':
            return f"""
                SELECT
                    cs.id,
                    cs.code,
                    cs.name,
                    cs.subtitle,
                    cs.pattern_from,
                    cs.pattern_to,
                    cs.expected_count,
                    cs.category,
                    COALESCE(
                        (
                            SELECT json_agg(
                                json_build_object(
                                    'id', c.id::text,
                                    'code', c.code
                                ) ORDER BY cc.case_index
                            )
                            FROM lib_caseset_cases cc
                            JOIN lib_cases c ON cc.case_id = c.id
                            WHERE cc.caseset_id = cs.id
                        ),
                        '[]'::json
                    ) as case_ids,
                    cs.created_at
                FROM lib_casesets cs
                WHERE cs.id = '{caseset_id}'
            """

        elif export_type == 'cases':
            return f"""
                SELECT
                    c.id,
                    c.code,
                    cc.caseset_id as case_set_id,
                    c.title,
                    c.long_name,
                    c.kind,
                    c.pattern_from,
                    c.pattern_to,
                    c.scramble,
                    c.notes,
                    c.story,
                    c.description,
                    c.image_url,
                    c.image_asset_name,
                    c.difficulty,
                    c.popularity,
                    c.groups,
                    c.created_at,
                    c.updated_at
                FROM lib_cases c
                JOIN lib_caseset_cases cc ON c.id = cc.case_id
                WHERE cc.caseset_id = '{caseset_id}'
                ORDER BY cc.case_index
            """

        elif export_type == 'algorithms':
            return f"""
                SELECT
                    a.id,
                    a.case_id,
                    a.code,
                    a.sequence,
                    a.name,
                    a.tags,
                    a.popularity,
                    a.difficulty,
                    a.avg_moves,
                    a.avg_execution_time_ms,
                    a.story,
                    a.created_at
                FROM lib_algorithms a
                JOIN lib_cases c ON a.case_id = c.id
                JOIN lib_caseset_cases cc ON c.id = cc.case_id
                WHERE cc.caseset_id = '{caseset_id}'
                ORDER BY a.popularity DESC NULLS LAST
            """

        else:
            raise ValueError(f"Unknown export type: {export_type}")

    def _generate_filename(self, caseset_code: str, export_type: str) -> str:
        """
        Generate filename in format: seeddata_{type}_{code}.json

        Args:
            caseset_code: Case set code from database
            export_type: One of 'case_sets', 'cases', 'algorithms'

        Returns:
            Formatted filename string

        Examples:
            - ('3x3-cfop-f2l', 'case_sets') → 'seeddata_caseset_3x3-cfop-f2l.json'
            - ('3x3-cfop-f2l', 'cases') → 'seeddata_cases_3x3-cfop-f2l.json'
            - ('3x3-cfop-f2l', 'algorithms') → 'seeddata_algorithms_3x3-cfop-f2l.json'
        """
        # Map export type to filename component
        type_map = {
            'case_sets': 'caseset',
            'cases': 'cases',
            'algorithms': 'algorithms'
        }

        if export_type not in type_map:
            raise ValueError(f"Unknown export type: {export_type}")

        # Build filename
        type_str = type_map[export_type]
        return f"seeddata_{type_str}_{caseset_code}.json"

    def _generate_export_definitions(self, case_sets: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, str]]]:
        """
        Generate export file definitions from discovered case sets.

        Args:
            case_sets: List of case set records from database

        Returns:
            Dict with keys 'case_sets', 'cases', 'algorithms', each containing list of file configs
        """
        definitions = {
            'case_sets': [],
            'cases': [],
            'algorithms': []
        }

        for cs in case_sets:
            code = cs['code']
            caseset_id = cs['id']

            # Generate 3 file definitions per case set
            for export_type in ['case_sets', 'cases', 'algorithms']:
                definitions[export_type].append({
                    'file': self._generate_filename(code, export_type),
                    'sql': self._build_query_for_type(export_type, caseset_id),
                    'required': False,  # All files optional by default (allow empty case sets)
                    'caseset_code': code,
                    'caseset_id': caseset_id
                })

        return definitions

    def execute_query(self, sql: str) -> List[Dict[str, Any]]:
        """
        Execute SQL query and return results as list of dicts.

        Args:
            sql: SQL query to execute

        Returns:
            List of records as dictionaries
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            columns = [desc[0] for desc in cursor.description]
            results = []
            for row in cursor.fetchall():
                record = dict(zip(columns, row))
                # Convert UUIDs and other types to strings for JSON serialization
                record = self._serialize_record(record)
                results.append(record)
            return results
        finally:
            cursor.close()

    def _serialize_record(self, record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert record to JSON-serializable format.

        Handles:
        - UUID objects → strings
        - datetime objects → ISO8601 strings with fractional seconds
        - None → null
        - Dictionaries → recursively serialize nested objects
        - Arrays → recursively serialize items
        """
        return {key: self._serialize_value(value) for key, value in record.items()}

    def _serialize_value(self, value: Any) -> Any:
        """
        Recursively serialize a value to JSON-compatible format.

        Handles nested structures from PostgreSQL json_agg() and other sources.
        """
        if value is None:
            return None
        elif isinstance(value, datetime):
            # Format with fractional seconds (Supabase format)
            return value.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        elif hasattr(value, 'hex'):  # UUID object
            return str(value)
        elif isinstance(value, dict):
            # Recursively serialize dictionary
            return {k: self._serialize_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            # Recursively serialize list items
            return [self._serialize_value(item) for item in value]
        else:
            return value


    def export_file(
        self,
        file_config: Dict[str, Any],
        file_type: str
    ) -> Tuple[bool, int]:
        """
        Export single file.

        Args:
            file_config: File configuration from YAML
            file_type: Type of file ('case_sets', 'cases', 'algorithms')

        Returns:
            Tuple of (success: bool, record_count: int)
        """
        file_name = file_config['file']
        required = file_config.get('required', False)
        sql = file_config['sql']

        print(f"\n{Fore.CYAN}Exporting {file_name}...{Style.RESET_ALL}")

        try:
            # Execute query
            records = self.execute_query(sql)
            record_count = len(records)

            # Validate data
            validation_errors = self._validate_records(records, file_type, file_name, db_conn=self.conn)

            if validation_errors:
                if required:
                    print(f"{Fore.RED}✗ Validation failed for {file_name} (required file){Style.RESET_ALL}")
                    for error in validation_errors[:5]:  # Show first 5 errors
                        print(f"  {Fore.RED}• {error}{Style.RESET_ALL}")
                    if len(validation_errors) > 5:
                        print(f"  {Fore.YELLOW}... and {len(validation_errors) - 5} more errors{Style.RESET_ALL}")
                    self.stats['errors'].extend(validation_errors)
                    return False, 0
                else:
                    print(f"{Fore.YELLOW}⚠ Validation warnings for {file_name} (optional file){Style.RESET_ALL}")
                    for error in validation_errors[:3]:
                        print(f"  {Fore.YELLOW}• {error}{Style.RESET_ALL}")
                    self.stats['warnings'].extend(validation_errors)

            # Check for empty datasets
            if record_count == 0:
                if required:
                    error = f"{file_name}: Required file has no records"
                    print(f"{Fore.RED}✗ {error}{Style.RESET_ALL}")
                    self.stats['errors'].append(error)
                    return False, 0
                else:
                    print(f"{Fore.YELLOW}⚠ {file_name}: No records found (skipping optional file){Style.RESET_ALL}")
                    self.stats['files_skipped'] += 1
                    return True, 0

            # Show diff preview if enabled (dry-run or always)
            if self.diff_viewer and (self.dry_run or self.enable_diff):
                output_path = self._get_output_path(file_name)
                comparison = self.diff_viewer.compare_with_existing(records, output_path, file_name)
                self.comparisons.append(comparison)
                self.diff_viewer.print_diff(comparison)

            # Write JSON file
            if not self.dry_run:
                output_path = self._get_output_path(file_name)
                # Use custom formatter for better array readability
                json_content = format_json(records)
                with open(output_path, 'w') as f:
                    f.write(json_content)
                print(f"{Fore.GREEN}✓ Exported {record_count} records to {file_name}{Style.RESET_ALL}")
            else:
                print(f"{Fore.BLUE}[DRY RUN] Would export {record_count} records to {file_name}{Style.RESET_ALL}")

            self.stats['files_exported'] += 1
            self.stats['total_records'] += record_count
            return True, record_count

        except Exception as e:
            error = f"{file_name}: {str(e)}"
            print(f"{Fore.RED}✗ Export failed: {error}{Style.RESET_ALL}")
            self.stats['errors'].append(error)
            return False, 0

    def _validate_records(
        self,
        records: List[Dict[str, Any]],
        file_type: str,
        file_name: str,
        db_conn=None
    ) -> List[str]:
        """
        Validate records using schema validation and validators module.

        Args:
            records: List of records to validate
            file_type: Type of file for context
            file_name: Name of file for completeness checks

        Returns:
            List of error messages (empty if valid)
        """
        all_errors = []

        # Step 1: JSON Schema validation (structural validation)
        # Schema errors are CRITICAL and block export
        if not self.skip_schema_validation:
            schema_errors = self.schema_validator.validate(records, file_type, file_name)
            if schema_errors:
                # Schema validation failures are critical
                all_errors.extend(schema_errors)
                # Return immediately - don't proceed with other validations if schema is invalid
                return all_errors

        # Step 2: Domain-specific validation (data completeness, foreign keys)
        # These are warnings that don't block export

        # UUID validation
        all_errors.extend(validators.validate_uuids(records, 'id'))

        # Required field validation
        all_errors.extend(validators.validate_required_fields(records, file_type))

        # File-type specific validations
        if file_type == 'cases':
            all_errors.extend(validators.validate_case_kind_enum(records, db_conn=db_conn))

        # Data completeness check
        all_errors.extend(validators.validate_data_completeness(records, file_name))

        return all_errors

    def _get_output_path(self, file_name: str) -> Path:
        """Get full output path for a file (always staging)."""
        # Always export to staging/TIMESTAMP/ios/
        if not self.staging_timestamp:
            self.staging_timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        staging_dir = STAGING_ROOT / self.staging_timestamp / "ios"
        staging_dir.mkdir(parents=True, exist_ok=True)
        return staging_dir / file_name

    def export_all(self, file_filter: Optional[str] = None):
        """
        Export all configured files to staging.

        Args:
            file_filter: If provided, only export files matching this name
        """
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}SEED DATA STAGING - Step 1 of 2{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

        if self.dry_run:
            print(f"{Fore.BLUE}[DRY RUN MODE - No files will be written]{Style.RESET_ALL}\n")

        # Connect to database
        self.connect_db()

        try:
            # Discover case sets from database
            print(f"\n{Fore.CYAN}Discovering case sets from database...{Style.RESET_ALL}")
            case_sets = self._discover_case_sets()
            print(f"{Fore.GREEN}✓ Found {len(case_sets)} case sets{Style.RESET_ALL}")

            # Generate export definitions dynamically
            export_defs = self._generate_export_definitions(case_sets)

            # Export case sets
            case_set_files = export_defs['case_sets']
            print(f"\n{Fore.YELLOW}=== CASE SETS ({len(case_set_files)} files) ==={Style.RESET_ALL}")
            for file_config in case_set_files:
                if file_filter and file_config['file'] != file_filter:
                    continue
                self.export_file(file_config, 'case_sets')

            # Export cases
            case_files = export_defs['cases']
            print(f"\n{Fore.YELLOW}=== CASES ({len(case_files)} files) ==={Style.RESET_ALL}")
            for file_config in case_files:
                if file_filter and file_config['file'] != file_filter:
                    continue
                self.export_file(file_config, 'cases')

            # Export algorithms
            algorithm_files = export_defs['algorithms']
            print(f"\n{Fore.YELLOW}=== ALGORITHMS ({len(algorithm_files)} files) ==={Style.RESET_ALL}")
            for file_config in algorithm_files:
                if file_filter and file_config['file'] != file_filter:
                    continue
                self.export_file(file_config, 'algorithms')

        finally:
            self.close_db()

        # Print summary
        self._print_summary()

    def _print_summary(self):
        """Print export summary statistics."""
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}EXPORT SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

        print(f"Files exported: {Fore.GREEN}{self.stats['files_exported']}{Style.RESET_ALL}")
        print(f"Files skipped: {Fore.YELLOW}{self.stats['files_skipped']}{Style.RESET_ALL}")
        print(f"Total records: {Fore.GREEN}{self.stats['total_records']}{Style.RESET_ALL}")

        # Print diff summary if available
        if self.diff_viewer and self.comparisons:
            self.diff_viewer.print_summary(self.comparisons)

        if self.stats['errors']:
            print(f"\n{Fore.RED}ERRORS ({len(self.stats['errors'])}):{Style.RESET_ALL}")
            for error in self.stats['errors'][:10]:
                print(f"  {Fore.RED}• {error}{Style.RESET_ALL}")
            if len(self.stats['errors']) > 10:
                print(f"  {Fore.RED}... and {len(self.stats['errors']) - 10} more errors{Style.RESET_ALL}")

        if self.stats['warnings']:
            print(f"\n{Fore.YELLOW}WARNINGS ({len(self.stats['warnings'])}):{Style.RESET_ALL}")
            for warning in self.stats['warnings'][:10]:
                print(f"  {Fore.YELLOW}• {warning}{Style.RESET_ALL}")
            if len(self.stats['warnings']) > 10:
                print(f"  {Fore.YELLOW}... and {len(self.stats['warnings']) - 10} more warnings{Style.RESET_ALL}")

        if self.stats['errors']:
            print(f"\n{Fore.RED}✗ Staging completed with errors{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Note: Errors visible in report - review before deployment{Style.RESET_ALL}")
        elif self.stats['warnings']:
            print(f"\n{Fore.YELLOW}⚠ Staging completed with warnings{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}✓ Staging completed successfully{Style.RESET_ALL}")

    def generate_report(self):
        """Generate HTML report after staging export."""
        if not self.staging_timestamp:
            return

        # Generate report
        report_gen = ReportGenerator()

        # Prepare export data
        export_data = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'database': os.getenv('SUPABASE_HOST', 'unknown'),
            'staged_timestamp': self.staging_timestamp
        }

        # Output paths
        staging_root = STAGING_ROOT / self.staging_timestamp
        reports_dir = staging_root / "reports"

        # Generate HTML report
        html_path = reports_dir / "export_report.html"
        report_gen.generate_html_report(export_data, self.comparisons, self.stats, html_path)

        # Generate metadata
        metadata_path = reports_dir / "export_metadata.json"
        report_gen.generate_metadata(export_data, self.stats, metadata_path)

        # Generate summary
        summary_path = reports_dir / "export_summary.json"
        report_gen.generate_summary(self.comparisons, summary_path)

        print(f"\n{Fore.GREEN}✓ Report generated: {html_path}{Style.RESET_ALL}")
        print(f"\nTo review: open {html_path}")
        print(f"To deploy: python scripts/02-deploy.py {self.staging_timestamp}")


def main():
    """Main entry point for staging script."""
    parser = argparse.ArgumentParser(
        description="Stage Supabase data export for review (Step 1 of 2)"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Preview export without writing files"
    )
    parser.add_argument(
        '--file',
        type=str,
        help="Stage only this specific file (e.g., seeddata_caseset_3x3-cfop-oll.json)"
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help="Validate data only, don't export"
    )
    parser.add_argument(
        '--no-diff',
        action='store_true',
        help="Skip showing diff preview"
    )
    parser.add_argument(
        '--show-field-changes',
        action='store_true',
        help="Show field-level changes in diff (verbose)"
    )
    parser.add_argument(
        '--skip-schema-validation',
        action='store_true',
        help="Skip JSON Schema validation (use only for emergency exports)"
    )

    args = parser.parse_args()

    # Create exporter (always in staging mode)
    exporter = SeedDataExporter(
        dry_run=args.dry_run or args.validate_only,
        enable_diff=not args.no_diff,
        show_field_changes=args.show_field_changes,
        skip_schema_validation=args.skip_schema_validation
    )

    # Run export to staging
    exporter.export_all(file_filter=args.file)

    # Generate report (unless dry-run)
    if not args.dry_run:
        exporter.generate_report()


if __name__ == "__main__":
    main()
