#!/usr/bin/env python3
"""
Seed Data Export Script

Exports Supabase database tables to iOS seed JSON files.
The database is the single source of truth - this script can be re-run anytime.

Features:
- Automatic backup before export (with --no-archive to skip)
- Enhanced dry-run with diff preview
- Restore from backup capability
- Breaking change warnings

Usage:
    python export_seed_data.py                    # Export all files (creates backup)
    python export_seed_data.py --dry-run          # Preview with diff comparison
    python export_seed_data.py --file oll_cases.json  # Export single file
    python export_seed_data.py --validate-only    # Validate only, no export
    python export_seed_data.py --no-archive       # Skip backup creation
    python export_seed_data.py --list-archives    # List all backups
    python export_seed_data.py --restore TIMESTAMP  # Restore from backup
    python export_seed_data.py --cleanup-archives # Remove old backups
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import psycopg2
import requests
import yaml
from colorama import Fore, Style, init
from dotenv import load_dotenv

import validators
from archive_manager import ArchiveManager
from diff_viewer import DiffViewer
from deployer import DeploymentManager
from report_generator import ReportGenerator

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)


class SeedDataExporter:
    """Exports Supabase data to iOS seed JSON files."""

    def __init__(
        self,
        config_path: str = "config.yaml",
        dry_run: bool = False,
        enable_archive: bool = True,
        enable_diff: bool = True,
        show_field_changes: bool = False,
        staging_mode: bool = False
    ):
        """
        Initialize exporter.

        Args:
            config_path: Path to YAML config file
            dry_run: If True, don't write files (preview only)
            enable_archive: If True, create backup before export
            enable_diff: If True, show diff preview in dry-run
            show_field_changes: If True, show field-level changes in diff
            staging_mode: If True, export to staging area instead of iOS directory
        """
        self.dry_run = dry_run
        self.enable_archive = enable_archive
        self.enable_diff = enable_diff
        self.staging_mode = staging_mode
        self.staging_timestamp = None  # Set during export if staging_mode
        self.config = self._load_config(config_path)
        self.conn = None
        self._use_rest_api = False
        self._rest_url = None
        self._rest_key = None
        self.stats = {
            'files_exported': 0,
            'files_skipped': 0,
            'total_records': 0,
            'errors': [],
            'warnings': []
        }

        # Initialize archive and diff managers
        self.archive_manager = ArchiveManager() if enable_archive else None
        self.diff_viewer = DiffViewer(show_field_changes=show_field_changes) if enable_diff else None
        self.comparisons = []  # Store diff results for summary

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        config_file = Path(__file__).parent / config_path
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)

    def connect_db(self):
        """Establish database connection using environment variables.

        Tries PostgreSQL connection first, falls back to REST API if it fails.
        """
        load_dotenv()

        # Try PostgreSQL connection first
        pg_vars = ['SUPABASE_HOST', 'SUPABASE_DATABASE', 'SUPABASE_USER', 'SUPABASE_PASSWORD']
        pg_available = all(os.getenv(var) for var in pg_vars)

        if pg_available:
            try:
                self.conn = psycopg2.connect(
                    host=os.getenv('SUPABASE_HOST'),
                    port=int(os.getenv('SUPABASE_PORT', 5432)),
                    database=os.getenv('SUPABASE_DATABASE'),
                    user=os.getenv('SUPABASE_USER'),
                    password=os.getenv('SUPABASE_PASSWORD'),
                    sslmode='require'
                )
                self._use_rest_api = False
                print(f"{Fore.GREEN}✓ Connected to Supabase database (PostgreSQL){Style.RESET_ALL}")
                return
            except Exception as e:
                print(f"{Fore.YELLOW}⚠ PostgreSQL connection failed: {e}{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  Falling back to REST API...{Style.RESET_ALL}")

        # Fall back to REST API
        rest_vars = ['SUPABASE_URL', 'SUPABASE_SERVICE_ROLE_KEY']
        missing = [var for var in rest_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required environment variables for REST API: {', '.join(missing)}")

        self._use_rest_api = True
        self._rest_url = os.getenv('SUPABASE_URL')
        self._rest_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
        print(f"{Fore.GREEN}✓ Connected to Supabase (REST API){Style.RESET_ALL}")

    def close_db(self):
        """Close database connection."""
        if self.conn and not self._use_rest_api:
            self.conn.close()
            print(f"{Fore.GREEN}✓ Database connection closed{Style.RESET_ALL}")
        elif self._use_rest_api:
            print(f"{Fore.GREEN}✓ REST API session closed{Style.RESET_ALL}")

    def _rest_query(self, table: str, select: str = "*", filters: Dict[str, Any] = None, order: str = None) -> List[Dict[str, Any]]:
        """Execute a REST API query against Supabase.

        Args:
            table: Table name to query
            select: Select clause (PostgREST syntax)
            filters: Dict of column=value filters
            order: Order clause (e.g., "code.asc")

        Returns:
            List of records as dictionaries
        """
        url = f"{self._rest_url}/rest/v1/{table}"
        params = {"select": select}
        if filters:
            for key, value in filters.items():
                params[key] = f"eq.{value}"
        if order:
            params["order"] = order

        headers = {
            "apikey": self._rest_key,
            "Authorization": f"Bearer {self._rest_key}"
        }

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def _discover_case_sets(self) -> List[Dict[str, Any]]:
        """
        Query database to discover all case sets.

        Returns:
            List of case set records with id, code, category
        """
        if self._use_rest_api:
            records = self._rest_query("lib_casesets", "id,code,category", order="code")
            return [{'id': str(r['id']), 'code': r['code'], 'category': r['category']} for r in records]

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

    def _execute_rest_query_for_type(self, export_type: str, caseset_id: str) -> List[Dict[str, Any]]:
        """Execute REST API query for a specific export type.

        Args:
            export_type: One of 'case_sets', 'cases', 'algorithms'
            caseset_id: UUID of the case set

        Returns:
            List of records as dictionaries
        """
        if export_type == 'case_sets':
            # Get case set
            url = f"{self._rest_url}/rest/v1/lib_casesets"
            headers = {"apikey": self._rest_key, "Authorization": f"Bearer {self._rest_key}"}
            params = {"id": f"eq.{caseset_id}"}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            casesets = response.json()
            if not casesets:
                return []
            cs = casesets[0]

            # Get case IDs in order
            url = f"{self._rest_url}/rest/v1/lib_caseset_cases"
            params = {"caseset_id": f"eq.{caseset_id}", "select": "case_id,case_index", "order": "case_index"}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            caseset_cases = response.json()

            # Get case codes
            case_ids_list = []
            for cc in caseset_cases:
                url = f"{self._rest_url}/rest/v1/lib_cases"
                params = {"id": f"eq.{cc['case_id']}", "select": "id,code"}
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                cases = response.json()
                if cases:
                    case_ids_list.append({'id': str(cases[0]['id']), 'code': cases[0]['code']})

            return [{
                'id': cs['id'],
                'code': cs['code'],
                'name': cs['name'],
                'subtitle': cs.get('subtitle'),
                'pattern_from': cs.get('pattern_from'),
                'pattern_to': cs.get('pattern_to'),
                'expected_count': cs.get('expected_count'),
                'category': cs.get('category'),
                'case_ids': case_ids_list if case_ids_list else None,
                'created_at': cs.get('created_at')
            }]

        elif export_type == 'cases':
            headers = {"apikey": self._rest_key, "Authorization": f"Bearer {self._rest_key}"}

            # Get case IDs in order from junction table
            url = f"{self._rest_url}/rest/v1/lib_caseset_cases"
            params = {"caseset_id": f"eq.{caseset_id}", "select": "case_id,case_index", "order": "case_index"}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            caseset_cases = response.json()

            # Get full case data for each case
            results = []
            for cc in caseset_cases:
                url = f"{self._rest_url}/rest/v1/lib_cases"
                params = {"id": f"eq.{cc['case_id']}"}
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                cases = response.json()
                if cases:
                    c = cases[0]
                    results.append({
                        'id': c['id'],
                        'code': c['code'],
                        'case_set_id': caseset_id,
                        'title': c.get('title'),
                        'long_name': c.get('long_name'),
                        'kind': c.get('kind'),
                        'pattern_from': c.get('pattern_from'),
                        'pattern_to': c.get('pattern_to'),
                        'scramble': c.get('scramble'),
                        'notes': c.get('notes'),
                        'story': c.get('story'),
                        'description': c.get('description'),
                        'image_url': c.get('image_url'),
                        'image_asset_name': c.get('image_asset_name'),
                        'difficulty': c.get('difficulty'),
                        'popularity': c.get('popularity'),
                        'groups': c.get('groups'),
                        'created_at': c.get('created_at'),
                        'updated_at': c.get('updated_at')
                    })
            return results

        elif export_type == 'algorithms':
            headers = {"apikey": self._rest_key, "Authorization": f"Bearer {self._rest_key}"}

            # Get case IDs from junction table
            url = f"{self._rest_url}/rest/v1/lib_caseset_cases"
            params = {"caseset_id": f"eq.{caseset_id}", "select": "case_id"}
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            caseset_cases = response.json()
            case_ids = [cc['case_id'] for cc in caseset_cases]

            if not case_ids:
                return []

            # Get algorithms for these cases
            results = []
            for case_id in case_ids:
                url = f"{self._rest_url}/rest/v1/lib_algorithms"
                params = {"case_id": f"eq.{case_id}", "order": "popularity.desc.nullslast"}
                response = requests.get(url, params=params, headers=headers)
                response.raise_for_status()
                algs = response.json()
                for a in algs:
                    results.append({
                        'id': a['id'],
                        'case_id': a['case_id'],
                        'code': a.get('code'),
                        'sequence': a.get('sequence'),
                        'name': a.get('name'),
                        'tags': a.get('tags'),
                        'popularity': a.get('popularity'),
                        'difficulty': a.get('difficulty'),
                        'avg_moves': a.get('avg_moves'),
                        'avg_execution_time_ms': a.get('avg_execution_time_ms'),
                        'story': a.get('story'),
                        'created_at': a.get('created_at')
                    })
            return results

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

    def _format_json(self, data: List[Dict[str, Any]]) -> str:
        """
        Format JSON with custom array formatting for better readability.

        Arrays of objects are formatted with one object per line (compact objects).
        Makes case_ids and other arrays more human-readable.
        """
        import re

        # First, serialize with standard formatting
        json_str = json.dumps(data, indent=2, ensure_ascii=False)

        # Post-process to compact array objects onto single lines
        # Match array of objects pattern: "[\n    {...},\n    {...}\n  ]"
        # Replace with: "[{...}, {...}]" (one object per line)

        def compact_array_objects(match):
            """Compact objects within arrays to single lines."""
            array_content = match.group(0)

            # Find all objects within this array
            objects = re.findall(r'\{\s*([^}]+?)\s*\}', array_content)
            if not objects:
                return array_content

            # Check if these are simple objects (not nested arrays/objects)
            # Simple heuristic: no nested brackets
            is_simple = all('[' not in obj and '{' not in obj for obj in objects)

            if is_simple and len(objects) > 0:
                # Get indentation level
                indent_match = re.search(r'\n(\s+)\{', array_content)
                if not indent_match:
                    return array_content

                indent = indent_match.group(1)
                base_indent = indent[:-2]  # Parent array indent

                # Compact each object to single line
                compact_objects = []
                for obj in objects:
                    # Clean up whitespace within object
                    compact_obj = re.sub(r'\s+', ' ', obj.strip())
                    compact_objects.append(f"{{{compact_obj}}}")

                # Rebuild array with one object per line
                result = "[\n"
                for i, obj in enumerate(compact_objects):
                    comma = "," if i < len(compact_objects) - 1 else ""
                    result += f"{indent}{obj}{comma}\n"
                result += f"{base_indent}]"
                return result

            return array_content

        # Apply compacting to arrays of objects
        # Match pattern: array with objects that span multiple lines
        pattern = r'\[\s*\n\s*\{[^[]*?\}\s*(?:,\s*\n\s*\{[^[]*?\}\s*)*\n\s*\]'
        json_str = re.sub(pattern, compact_array_objects, json_str, flags=re.MULTILINE)

        return json_str

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
        caseset_id = file_config.get('caseset_id')

        print(f"\n{Fore.CYAN}Exporting {file_name}...{Style.RESET_ALL}")

        try:
            # Execute query (REST API or PostgreSQL)
            if self._use_rest_api and caseset_id:
                records = self._execute_rest_query_for_type(file_type, caseset_id)
            else:
                records = self.execute_query(sql)
            record_count = len(records)

            # Validate data
            validation_errors = self._validate_records(records, file_type, file_name)

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
                json_content = self._format_json(records)
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
        file_name: str
    ) -> List[str]:
        """
        Validate records using validators module.

        Args:
            records: List of records to validate
            file_type: Type of file for context
            file_name: Name of file for completeness checks

        Returns:
            List of error messages (empty if valid)
        """
        all_errors = []

        # UUID validation
        all_errors.extend(validators.validate_uuids(records, 'id'))

        # Required field validation
        all_errors.extend(validators.validate_required_fields(records, file_type))

        # File-type specific validations
        if file_type == 'cases':
            all_errors.extend(validators.validate_case_kind_enum(records))

        # Data completeness check
        all_errors.extend(validators.validate_data_completeness(records, file_name))

        return all_errors

    def _get_output_path(self, file_name: str) -> Path:
        """Get full output path for a file."""
        if self.staging_mode:
            # Export to staging/TIMESTAMP/ios/
            if not self.staging_timestamp:
                self.staging_timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
            staging_dir = Path(__file__).parent / "staging" / self.staging_timestamp / "ios"
            staging_dir.mkdir(parents=True, exist_ok=True)
            return staging_dir / file_name
        else:
            # Export to iOS SeedData (current behavior)
            output_dir = Path(__file__).parent / self.config['output_dir']
            output_dir.mkdir(parents=True, exist_ok=True)
            return output_dir / file_name

    def export_all(self, file_filter: Optional[str] = None):
        """
        Export all configured files.

        Args:
            file_filter: If provided, only export files matching this name
        """
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}SEED DATA EXPORT{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

        if self.dry_run:
            print(f"{Fore.BLUE}[DRY RUN MODE - No files will be written]{Style.RESET_ALL}\n")

        # Create archive before export (if enabled and not dry-run)
        if self.archive_manager and not self.dry_run and self.enable_archive:
            print(f"\n{Fore.YELLOW}=== CREATING BACKUP ==={Style.RESET_ALL}")
            output_dir = Path(__file__).parent / self.config['output_dir']
            archive_path = self.archive_manager.create_archive(
                source_dir=output_dir,
                notes="Pre-export backup"
            )
            if archive_path:
                print(f"{Fore.GREEN}✓ Backup created: {archive_path.name}{Style.RESET_ALL}")

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
            print(f"\n{Fore.RED}✗ Export completed with errors{Style.RESET_ALL}")
            if not self.staging_mode:
                sys.exit(1)
            # In staging mode, continue to generate report with errors visible
        elif self.stats['warnings']:
            print(f"\n{Fore.YELLOW}⚠ Export completed with warnings{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.GREEN}✓ Export completed successfully{Style.RESET_ALL}")

    def generate_report(self):
        """Generate HTML report after staging export."""
        if not self.staging_mode or not self.staging_timestamp:
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
        staging_root = Path(__file__).parent / "staging" / self.staging_timestamp
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
        print(f"To deploy: python export_seed_data.py --deploy {self.staging_timestamp}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Export Supabase data to iOS seed JSON files"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Preview export without writing files"
    )
    parser.add_argument(
        '--file',
        type=str,
        help="Export only this specific file (e.g., 3x3_cfop_oll_cases.json)"
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help="Validate data only, don't export"
    )
    parser.add_argument(
        '--no-archive',
        action='store_true',
        help="Skip creating backup before export"
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
        '--list-archives',
        action='store_true',
        help="List all available backups and exit"
    )
    parser.add_argument(
        '--restore',
        type=str,
        metavar='TIMESTAMP',
        help="Restore files from backup (e.g., 2025-12-05_170000)"
    )
    parser.add_argument(
        '--cleanup-archives',
        action='store_true',
        help="Clean up old backups (keep 10 most recent, delete older than 30 days)"
    )

    # Staging & Deployment
    parser.add_argument(
        '--stage',
        action='store_true',
        help='Export to staging area with report generation'
    )
    parser.add_argument(
        '--deploy',
        type=str,
        metavar='TIMESTAMP',
        help='Deploy staged export to iOS (e.g., 2025-12-05_180000)'
    )
    parser.add_argument(
        '--deploy-latest',
        action='store_true',
        help='Deploy most recent staged export'
    )
    parser.add_argument(
        '--list-staged',
        action='store_true',
        help='List all staged exports'
    )
    parser.add_argument(
        '--list-deployments',
        action='store_true',
        help='Show deployment history'
    )
    parser.add_argument(
        '--preview-deploy',
        type=str,
        metavar='TIMESTAMP',
        help='Preview what would be deployed'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='One-step export (stage + deploy immediately, legacy behavior)'
    )

    args = parser.parse_args()

    # Handle deployment commands
    if args.list_staged or args.deploy or args.deploy_latest or args.list_deployments or args.preview_deploy:
        deployment_manager = DeploymentManager()

        if args.list_staged:
            deployment_manager.print_staged()
            return

        if args.list_deployments:
            deployment_manager.list_deployments()
            return

        if args.preview_deploy:
            deployment_manager.preview_deploy(args.preview_deploy)
            return

        if args.deploy or args.deploy_latest:
            timestamp = "latest" if args.deploy_latest else args.deploy
            success = deployment_manager.deploy(timestamp, confirm=False)
            sys.exit(0 if success else 1)

        return

    # Handle archive-only commands
    if args.list_archives or args.restore or args.cleanup_archives:
        archive_manager = ArchiveManager()

        if args.list_archives:
            archive_manager.print_archives()
            return

        if args.restore:
            output_dir = Path(__file__).parent / "../DeddalInfra/Infrastructure/Persistence/SeedData"
            success = archive_manager.restore_archive(
                timestamp=args.restore,
                dest_dir=output_dir,
                confirm=True
            )
            sys.exit(0 if success else 1)

        if args.cleanup_archives:
            archive_manager.cleanup_old_archives(keep_count=10, max_age_days=30)
            return

    # Determine mode
    staging_mode = args.stage or args.quick
    quick_mode = args.quick

    # Create exporter
    exporter = SeedDataExporter(
        dry_run=args.dry_run or args.validate_only,
        enable_archive=not args.no_archive if not staging_mode else False,  # No archive in staging mode
        enable_diff=not args.no_diff,
        show_field_changes=args.show_field_changes,
        staging_mode=staging_mode
    )

    # Run export
    exporter.export_all(file_filter=args.file)

    # Generate report if staging
    if staging_mode and not args.dry_run:
        exporter.generate_report()

    # Quick mode - auto-deploy
    if quick_mode and not args.dry_run:
        print(f"\n{Fore.CYAN}[QUICK MODE] Auto-deploying...{Style.RESET_ALL}")
        deployment_manager = DeploymentManager()
        success = deployment_manager.deploy(exporter.staging_timestamp, confirm=True, create_backup=True)
        if not success:
            sys.exit(1)


if __name__ == "__main__":
    main()
