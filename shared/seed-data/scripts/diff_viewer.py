"""
Diff Viewer

Compares new data with existing files and shows detailed changes.
Used for enhanced dry-run mode.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from colorama import Fore, Style


class DiffViewer:
    """Compares and displays differences between old and new seed data."""

    def __init__(self, show_field_changes: bool = False):
        """
        Initialize diff viewer.

        Args:
            show_field_changes: If True, show field-level changes (verbose)
        """
        self.show_field_changes = show_field_changes

    def compare_with_existing(
        self,
        new_records: List[Dict[str, Any]],
        file_path: Path,
        file_name: str
    ) -> Dict[str, Any]:
        """
        Compare new records with existing file.

        Args:
            new_records: New data from database
            file_path: Path to existing file
            file_name: Name of file for display

        Returns:
            Dict with comparison results
        """
        # Check if file exists
        if not file_path.exists():
            return {
                'status': 'new',
                'new_count': len(new_records),
                'message': f"[NEW FILE] Would create {file_name}",
                'file_name': file_name
            }

        # Load existing data
        try:
            with open(file_path) as f:
                existing_records = json.load(f)
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error reading existing file: {e}",
                'file_name': file_name
            }

        # Perform comparison
        return self._compare_records(existing_records, new_records, file_name)

    def _compare_records(
        self,
        old_records: List[Dict[str, Any]],
        new_records: List[Dict[str, Any]],
        file_name: str
    ) -> Dict[str, Any]:
        """
        Compare two sets of records and return diff details.

        Args:
            old_records: Existing records
            new_records: New records from database
            file_name: Name of file for context

        Returns:
            Dict with detailed comparison results
        """
        old_count = len(old_records)
        new_count = len(new_records)

        # Build ID sets for comparison
        old_ids = {str(r.get('id', '')) for r in old_records if r.get('id')}
        new_ids = {str(r.get('id', '')) for r in new_records if r.get('id')}

        # Find differences
        added_ids = new_ids - old_ids
        removed_ids = old_ids - new_ids
        common_ids = old_ids & new_ids

        # Check for modified records
        modified = []
        if self.show_field_changes and common_ids:
            old_by_id = {str(r['id']): r for r in old_records if r.get('id')}
            new_by_id = {str(r['id']): r for r in new_records if r.get('id')}

            for record_id in common_ids:
                old_rec = old_by_id.get(record_id)
                new_rec = new_by_id.get(record_id)

                if old_rec and new_rec:
                    changed_fields = self._find_changed_fields(old_rec, new_rec)
                    if changed_fields:
                        modified.append({
                            'id': record_id,
                            'code': new_rec.get('code', 'unknown'),
                            'fields': changed_fields
                        })

        # Check for breaking changes
        warnings = self._check_breaking_changes(removed_ids, old_count, new_count)

        return {
            'status': 'changed' if (added_ids or removed_ids or modified) else 'unchanged',
            'old_count': old_count,
            'new_count': new_count,
            'diff': new_count - old_count,
            'added_ids': added_ids,
            'removed_ids': removed_ids,
            'modified': modified,
            'warnings': warnings,
            'file_name': file_name
        }

    def _find_changed_fields(
        self,
        old_record: Dict[str, Any],
        new_record: Dict[str, Any]
    ) -> List[str]:
        """
        Find which fields changed between two records.

        Args:
            old_record: Existing record
            new_record: New record

        Returns:
            List of changed field names
        """
        changed = []

        # Skip timestamp fields
        skip_fields = {'created_at', 'updated_at'}

        # Check all fields in both records
        all_keys = set(old_record.keys()) | set(new_record.keys())

        for key in all_keys:
            if key in skip_fields:
                continue

            old_val = old_record.get(key)
            new_val = new_record.get(key)

            # Compare values (handle None, arrays, etc.)
            if old_val != new_val:
                changed.append(key)

        return changed

    def _check_breaking_changes(
        self,
        removed_ids: Set[str],
        old_count: int,
        new_count: int
    ) -> List[str]:
        """
        Check for potentially breaking changes.

        Args:
            removed_ids: Set of removed record IDs
            old_count: Original record count
            new_count: New record count

        Returns:
            List of warning messages
        """
        warnings = []

        # Warn if removing records
        if removed_ids:
            warnings.append(
                f"{len(removed_ids)} records will be removed - "
                "may break iOS app references"
            )

        # Warn if removing >10% of records
        if old_count > 0:
            removal_pct = (len(removed_ids) / old_count) * 100
            if removal_pct > 10:
                warnings.append(
                    f"Removing {removal_pct:.1f}% of records - "
                    "verify this is intentional"
                )

        # Warn if drastic count change
        if old_count > 0:
            change_pct = abs((new_count - old_count) / old_count) * 100
            if change_pct > 50:
                warnings.append(
                    f"Record count changed by {change_pct:.1f}% - "
                    "verify database query is correct"
                )

        return warnings

    def print_diff(self, comparison: Dict[str, Any]):
        """
        Print formatted diff output.

        Args:
            comparison: Comparison results from compare_with_existing()
        """
        status = comparison['status']
        file_name = comparison.get('file_name', 'unknown')

        # New file
        if status == 'new':
            print(f"  {Fore.GREEN}[NEW FILE] {comparison['message']}{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}{comparison['new_count']} records{Style.RESET_ALL}")
            return

        # Error
        if status == 'error':
            print(f"  {Fore.RED}[ERROR] {comparison['message']}{Style.RESET_ALL}")
            return

        # Unchanged
        if status == 'unchanged':
            print(f"  {Fore.BLUE}[UNCHANGED] {comparison['new_count']} records{Style.RESET_ALL}")
            return

        # Changed - show details
        old_count = comparison['old_count']
        new_count = comparison['new_count']
        diff = comparison['diff']
        added = comparison['added_ids']
        removed = comparison['removed_ids']
        modified = comparison.get('modified', [])

        # Count summary
        if diff != 0:
            color = Fore.GREEN if diff > 0 else Fore.YELLOW
            print(f"  {color}Count: {old_count} → {new_count} ({diff:+d}){Style.RESET_ALL}")
        else:
            print(f"  Count: {new_count} (no change)")

        # Added records
        if added:
            print(f"  {Fore.GREEN}+ {len(added)} new records{Style.RESET_ALL}")
            if len(added) <= 5:
                for record_id in list(added)[:5]:
                    print(f"    • {record_id[:8]}...")

        # Removed records
        if removed:
            print(f"  {Fore.RED}- {len(removed)} removed records{Style.RESET_ALL}")
            if len(removed) <= 5:
                for record_id in list(removed)[:5]:
                    print(f"    • {record_id[:8]}...")

        # Modified records (field-level changes)
        if modified:
            print(f"  {Fore.YELLOW}~ {len(modified)} modified records{Style.RESET_ALL}")
            for mod in modified[:3]:  # Show first 3
                fields = ', '.join(mod['fields'][:3])  # Show first 3 fields
                if len(mod['fields']) > 3:
                    fields += f" (+{len(mod['fields']) - 3} more)"
                print(f"    • {mod['code']}: {fields}")

        # Warnings
        for warning in comparison.get('warnings', []):
            print(f"  {Fore.YELLOW}⚠️  {warning}{Style.RESET_ALL}")

    def print_summary(self, all_comparisons: List[Dict[str, Any]]):
        """
        Print summary of all file comparisons.

        Args:
            all_comparisons: List of comparison results
        """
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}DIFF SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")

        new_files = [c for c in all_comparisons if c['status'] == 'new']
        unchanged = [c for c in all_comparisons if c['status'] == 'unchanged']
        changed = [c for c in all_comparisons if c['status'] == 'changed']
        errors = [c for c in all_comparisons if c['status'] == 'error']

        print(f"New files: {Fore.GREEN}{len(new_files)}{Style.RESET_ALL}")
        print(f"Unchanged files: {Fore.BLUE}{len(unchanged)}{Style.RESET_ALL}")
        print(f"Changed files: {Fore.YELLOW}{len(changed)}{Style.RESET_ALL}")
        if errors:
            print(f"Errors: {Fore.RED}{len(errors)}{Style.RESET_ALL}")

        # Total record changes
        total_added = sum(len(c.get('added_ids', [])) for c in changed)
        total_removed = sum(len(c.get('removed_ids', [])) for c in changed)

        if total_added or total_removed:
            print(f"\nTotal changes:")
            if total_added:
                print(f"  {Fore.GREEN}+ {total_added} records added{Style.RESET_ALL}")
            if total_removed:
                print(f"  {Fore.RED}- {total_removed} records removed{Style.RESET_ALL}")

        # Highlight files with warnings
        files_with_warnings = [c for c in all_comparisons if c.get('warnings')]
        if files_with_warnings:
            print(f"\n{Fore.YELLOW}Files with warnings:{Style.RESET_ALL}")
            for comp in files_with_warnings:
                print(f"  • {comp['file_name']}")
                for warning in comp['warnings'][:2]:
                    print(f"    ⚠️  {warning}")
