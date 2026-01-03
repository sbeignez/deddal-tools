"""
Archive Manager

Handles backup and restore of seed data files.
Creates timestamped archives before exports and manages cleanup.
"""

import json
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

from colorama import Fore, Style


class ArchiveManager:
    """Manages backups of seed data files."""

    def __init__(self, backup_dir: str = "backups"):
        """
        Initialize archive manager.

        Args:
            backup_dir: Directory name for backups (relative to script)
        """
        self.backup_root = Path(__file__).parent / backup_dir
        self.manifest_file = self.backup_root / "manifest.json"

    def create_archive(
        self,
        source_dir: Path,
        notes: str = ""
    ) -> Optional[Path]:
        """
        Create timestamped backup of all JSON files in source directory.

        Args:
            source_dir: Directory containing files to backup
            notes: Optional notes about this backup

        Returns:
            Path to created backup directory, or None if no files to backup
        """
        # Check if source directory exists and has files
        if not source_dir.exists():
            print(f"{Fore.YELLOW}⚠ Source directory doesn't exist yet: {source_dir}{Style.RESET_ALL}")
            return None

        json_files = list(source_dir.glob("*.json"))
        if not json_files:
            print(f"{Fore.YELLOW}⚠ No JSON files to backup in {source_dir}{Style.RESET_ALL}")
            return None

        # Create backup directory with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        archive_dir = self.backup_root / timestamp
        archive_dir.mkdir(parents=True, exist_ok=True)

        # Copy all JSON files
        copied_count = 0
        total_records = 0

        for json_file in json_files:
            dest = archive_dir / json_file.name
            shutil.copy2(json_file, dest)
            copied_count += 1

            # Count records for manifest
            try:
                with open(json_file) as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        total_records += len(data)
            except:
                pass

        # Update manifest
        self._update_manifest(
            timestamp=timestamp,
            file_count=copied_count,
            total_records=total_records,
            notes=notes
        )

        print(f"{Fore.GREEN}✓ Archived {copied_count} files to {archive_dir.name}{Style.RESET_ALL}")
        return archive_dir

    def _update_manifest(
        self,
        timestamp: str,
        file_count: int,
        total_records: int,
        notes: str
    ):
        """Update manifest file with new archive entry."""
        # Load existing manifest
        manifest = {"archives": []}
        if self.manifest_file.exists():
            with open(self.manifest_file) as f:
                manifest = json.load(f)

        # Add new archive entry
        manifest["archives"].append({
            "timestamp": timestamp,
            "created_at": datetime.now().isoformat() + "Z",
            "file_count": file_count,
            "total_records": total_records,
            "notes": notes
        })

        # Save manifest
        self.backup_root.mkdir(parents=True, exist_ok=True)
        with open(self.manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)

    def list_archives(self) -> List[Dict]:
        """
        List all available archives.

        Returns:
            List of archive metadata dicts, newest first
        """
        if not self.manifest_file.exists():
            return []

        with open(self.manifest_file) as f:
            manifest = json.load(f)

        # Sort by timestamp descending (newest first)
        archives = sorted(
            manifest.get("archives", []),
            key=lambda x: x["timestamp"],
            reverse=True
        )

        return archives

    def print_archives(self):
        """Print formatted list of all archives."""
        archives = self.list_archives()

        if not archives:
            print(f"{Fore.YELLOW}No archives found{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}Available Archives:{Style.RESET_ALL}\n")
        print(f"{'Timestamp':<20} {'Files':<8} {'Records':<10} {'Notes'}")
        print("=" * 70)

        for archive in archives:
            timestamp = archive['timestamp']
            file_count = archive.get('file_count', '?')
            record_count = archive.get('total_records', '?')
            notes = archive.get('notes', '')

            # Highlight most recent
            if archive == archives[0]:
                print(f"{Fore.GREEN}{timestamp:<20} {file_count:<8} {record_count:<10} {notes}{Style.RESET_ALL}")
            else:
                print(f"{timestamp:<20} {file_count:<8} {record_count:<10} {notes}")

        print()

    def restore_archive(
        self,
        timestamp: str,
        dest_dir: Path,
        confirm: bool = True
    ) -> bool:
        """
        Restore files from a specific archive.

        Args:
            timestamp: Archive timestamp to restore (e.g., "2025-12-05_170000")
            dest_dir: Destination directory to restore files to
            confirm: If True, prompt for confirmation before overwriting

        Returns:
            True if restore succeeded, False otherwise
        """
        archive_dir = self.backup_root / timestamp

        if not archive_dir.exists():
            print(f"{Fore.RED}✗ Archive not found: {timestamp}{Style.RESET_ALL}")
            return False

        json_files = list(archive_dir.glob("*.json"))
        if not json_files:
            print(f"{Fore.RED}✗ No files in archive: {timestamp}{Style.RESET_ALL}")
            return False

        # Confirm overwrite
        if confirm:
            print(f"\n{Fore.YELLOW}WARNING: This will overwrite {len(json_files)} files in:{Style.RESET_ALL}")
            print(f"  {dest_dir}")
            response = input(f"\n{Fore.YELLOW}Continue? [y/N]: {Style.RESET_ALL}").lower()
            if response != 'y':
                print(f"{Fore.YELLOW}Restore cancelled{Style.RESET_ALL}")
                return False

        # Copy files
        dest_dir.mkdir(parents=True, exist_ok=True)
        copied_count = 0

        for json_file in json_files:
            dest = dest_dir / json_file.name
            shutil.copy2(json_file, dest)
            copied_count += 1

        print(f"{Fore.GREEN}✓ Restored {copied_count} files from {timestamp}{Style.RESET_ALL}")
        return True

    def cleanup_old_archives(
        self,
        keep_count: int = 10,
        max_age_days: int = 30
    ):
        """
        Remove old archives based on count and age limits.

        Args:
            keep_count: Keep at most this many recent archives (0 = unlimited)
            max_age_days: Delete archives older than this (0 = never delete by age)
        """
        archives = self.list_archives()

        if not archives:
            return

        deleted_count = 0

        # Delete by count (keep newest N)
        if keep_count > 0 and len(archives) > keep_count:
            to_delete = archives[keep_count:]
            for archive in to_delete:
                archive_dir = self.backup_root / archive['timestamp']
                if archive_dir.exists():
                    shutil.rmtree(archive_dir)
                    deleted_count += 1
                    print(f"{Fore.YELLOW}Deleted old archive: {archive['timestamp']}{Style.RESET_ALL}")

        # Delete by age
        if max_age_days > 0:
            cutoff_date = datetime.now() - timedelta(days=max_age_days)

            for archive in archives:
                created_at = datetime.fromisoformat(archive['created_at'].replace('Z', '+00:00'))
                if created_at < cutoff_date:
                    archive_dir = self.backup_root / archive['timestamp']
                    if archive_dir.exists():
                        shutil.rmtree(archive_dir)
                        deleted_count += 1
                        print(f"{Fore.YELLOW}Deleted expired archive: {archive['timestamp']}{Style.RESET_ALL}")

        if deleted_count > 0:
            # Update manifest to remove deleted archives
            remaining_archives = [
                a for a in archives
                if (self.backup_root / a['timestamp']).exists()
            ]
            manifest = {"archives": remaining_archives}
            with open(self.manifest_file, 'w') as f:
                json.dump(manifest, f, indent=2)

            print(f"{Fore.GREEN}✓ Cleaned up {deleted_count} old archives{Style.RESET_ALL}")

    def get_latest_archive(self) -> Optional[str]:
        """Get timestamp of most recent archive."""
        archives = self.list_archives()
        return archives[0]['timestamp'] if archives else None
