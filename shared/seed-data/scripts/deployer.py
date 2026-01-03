#!/usr/bin/env python3
"""
Deployment Manager

Handles deployment of staged exports to iOS SeedData directory.
Manages deployment history and provides rollback capabilities.
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from colorama import Fore, Style, init

from archive_manager import ArchiveManager

init(autoreset=True)


class DeploymentManager:
    """Manages deployment of staged exports to iOS."""

    def __init__(
        self,
        staging_root: str = "staging",
        ios_seed_data_dir: str = "../DeddalInfra/Infrastructure/Persistence/SeedData",
        deployments_dir: str = "deployments"
    ):
        """
        Initialize deployment manager.

        Args:
            staging_root: Root directory for staged exports
            ios_seed_data_dir: Path to iOS SeedData directory
            deployments_dir: Directory for deployment manifests
        """
        self.staging_root = Path(__file__).parent / staging_root
        self.ios_seed_data_dir = Path(__file__).parent / ios_seed_data_dir
        self.deployments_dir = Path(__file__).parent / deployments_dir
        self.manifest_file = self.deployments_dir / "manifest.json"

        # Initialize deployment tracking
        self._ensure_deployment_tracking()

        # Initialize archive manager for pre-deployment backups
        self.archive_manager = ArchiveManager()

    def _ensure_deployment_tracking(self):
        """Ensure deployments directory and manifest exist."""
        self.deployments_dir.mkdir(parents=True, exist_ok=True)
        if not self.manifest_file.exists():
            self._write_manifest({"deployments": []})

    def _read_manifest(self) -> Dict:
        """Read deployment manifest."""
        with open(self.manifest_file, 'r') as f:
            return json.load(f)

    def _write_manifest(self, data: Dict):
        """Write deployment manifest."""
        with open(self.manifest_file, 'w') as f:
            json.dump(data, f, indent=2)

    def list_staged(self) -> List[Dict]:
        """
        List all available staged exports.

        Returns:
            List of staged export info dicts
        """
        if not self.staging_root.exists():
            return []

        staged = []
        for timestamp_dir in sorted(self.staging_root.iterdir(), reverse=True):
            if not timestamp_dir.is_dir() or timestamp_dir.name.startswith('.'):
                continue

            ios_dir = timestamp_dir / "ios"
            reports_dir = timestamp_dir / "reports"

            if not ios_dir.exists():
                continue

            # Count files
            json_files = list(ios_dir.glob("*.json"))
            file_count = len(json_files)

            # Get metadata if available
            metadata_file = reports_dir / "export_metadata.json"
            metadata = {}
            if metadata_file.exists():
                try:
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                except Exception:
                    pass

            staged.append({
                'timestamp': timestamp_dir.name,
                'path': str(timestamp_dir),
                'file_count': file_count,
                'metadata': metadata
            })

        return staged

    def print_staged(self):
        """Print list of staged exports."""
        staged = self.list_staged()

        if not staged:
            print(f"{Fore.YELLOW}No staged exports found{Style.RESET_ALL}")
            print(f"\nRun: python export_seed_data.py --stage")
            return

        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}STAGED EXPORTS{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

        for export in staged:
            timestamp = export['timestamp']
            file_count = export['file_count']
            metadata = export['metadata']

            print(f"{Fore.GREEN}{timestamp}{Style.RESET_ALL}")
            print(f"  Files: {file_count}")
            if metadata:
                if 'total_records' in metadata:
                    print(f"  Records: {metadata['total_records']}")
                if 'database' in metadata:
                    print(f"  Database: {metadata['database']}")
            print()

        print(f"To deploy: python export_seed_data.py --deploy {staged[0]['timestamp']}")

    def get_staged_export(self, timestamp: str) -> Optional[Path]:
        """
        Get path to staged export.

        Args:
            timestamp: Export timestamp

        Returns:
            Path to staged export directory, or None if not found
        """
        if timestamp == "latest":
            staged = self.list_staged()
            if not staged:
                return None
            timestamp = staged[0]['timestamp']

        staged_path = self.staging_root / timestamp
        ios_dir = staged_path / "ios"

        if not staged_path.exists() or not ios_dir.exists():
            return None

        return staged_path

    def deploy(
        self,
        timestamp: str,
        confirm: bool = False,
        create_backup: bool = True
    ) -> bool:
        """
        Deploy staged export to iOS SeedData directory.

        Args:
            timestamp: Staged export timestamp (or "latest")
            confirm: If True, skip confirmation prompt
            create_backup: If True, create backup before deployment

        Returns:
            True if deployment successful
        """
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}DEPLOYMENT{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

        # Get staged export
        staged_path = self.get_staged_export(timestamp)
        if not staged_path:
            print(f"{Fore.RED}✗ Staged export not found: {timestamp}{Style.RESET_ALL}")
            print(f"\nAvailable staged exports:")
            self.print_staged()
            return False

        actual_timestamp = staged_path.name
        ios_src = staged_path / "ios"

        # Show deployment details
        json_files = list(ios_src.glob("*.json"))
        print(f"Staged export: {Fore.GREEN}{actual_timestamp}{Style.RESET_ALL}")
        print(f"Files to deploy: {Fore.GREEN}{len(json_files)}{Style.RESET_ALL}")
        print(f"Destination: {Fore.YELLOW}{self.ios_seed_data_dir}{Style.RESET_ALL}")

        # Load metadata
        metadata_file = staged_path / "reports" / "export_metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            print(f"Total records: {Fore.GREEN}{metadata.get('total_records', 'unknown')}{Style.RESET_ALL}")

        # Confirmation
        if not confirm:
            print(f"\n{Fore.YELLOW}This will:")
            if create_backup:
                print(f"  1. Create backup of current iOS SeedData")
            print(f"  {'2' if create_backup else '1'}. Copy {len(json_files)} files to iOS SeedData directory")
            print(f"  {'3' if create_backup else '2'}. Record deployment in manifest{Style.RESET_ALL}")

            response = input(f"\n{Fore.CYAN}Proceed with deployment? [y/N]: {Style.RESET_ALL}")
            if response.lower() != 'y':
                print(f"{Fore.YELLOW}Deployment cancelled{Style.RESET_ALL}")
                return False

        # Create backup
        backup_timestamp = None
        if create_backup:
            print(f"\n{Fore.YELLOW}Creating backup...{Style.RESET_ALL}")
            archive_path = self.archive_manager.create_archive(
                source_dir=self.ios_seed_data_dir,
                notes=f"Pre-deployment backup (staging: {actual_timestamp})"
            )
            if archive_path:
                backup_timestamp = archive_path.name
                print(f"{Fore.GREEN}✓ Backup created: {backup_timestamp}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}✗ Failed to create backup{Style.RESET_ALL}")
                return False

        # Ensure iOS directory exists
        self.ios_seed_data_dir.mkdir(parents=True, exist_ok=True)

        # Deploy files
        print(f"\n{Fore.YELLOW}Deploying files...{Style.RESET_ALL}")
        deployed_count = 0
        errors = []

        for json_file in json_files:
            try:
                dest_file = self.ios_seed_data_dir / json_file.name
                shutil.copy2(json_file, dest_file)
                deployed_count += 1
            except Exception as e:
                errors.append(f"{json_file.name}: {str(e)}")

        if errors:
            print(f"{Fore.RED}✗ Errors during deployment:{Style.RESET_ALL}")
            for error in errors[:10]:
                print(f"  {Fore.RED}• {error}{Style.RESET_ALL}")
            if len(errors) > 10:
                print(f"  {Fore.RED}... and {len(errors) - 10} more errors{Style.RESET_ALL}")
            return False

        print(f"{Fore.GREEN}✓ Deployed {deployed_count} files{Style.RESET_ALL}")

        # Record deployment
        deployment_record = {
            'staged_timestamp': actual_timestamp,
            'deployed_at': datetime.now().isoformat() + 'Z',
            'file_count': deployed_count,
            'backup_timestamp': backup_timestamp
        }

        manifest = self._read_manifest()
        manifest['deployments'].append(deployment_record)
        self._write_manifest(manifest)

        print(f"{Fore.GREEN}✓ Deployment recorded in manifest{Style.RESET_ALL}")

        # Success summary
        print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}✓ DEPLOYMENT SUCCESSFUL{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
        print(f"\nDeployed: {Fore.GREEN}{deployed_count} files{Style.RESET_ALL}")
        if backup_timestamp:
            print(f"Backup: {Fore.YELLOW}{backup_timestamp}{Style.RESET_ALL}")
        print(f"\nNext steps:")
        print(f"  1. Run iOS app to verify seed data loads correctly")
        print(f"  2. Review git diff: git diff {self.ios_seed_data_dir}")
        print(f"  3. Commit changes if tests pass")

        return True

    def preview_deploy(self, timestamp: str):
        """
        Preview what would be deployed without actually deploying.

        Args:
            timestamp: Staged export timestamp
        """
        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}DEPLOYMENT PREVIEW{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

        staged_path = self.get_staged_export(timestamp)
        if not staged_path:
            print(f"{Fore.RED}✗ Staged export not found: {timestamp}{Style.RESET_ALL}")
            return

        ios_src = staged_path / "ios"
        json_files = sorted(ios_src.glob("*.json"))

        print(f"Staged export: {Fore.GREEN}{staged_path.name}{Style.RESET_ALL}")
        print(f"Destination: {Fore.YELLOW}{self.ios_seed_data_dir}{Style.RESET_ALL}")
        print(f"\nFiles to deploy ({len(json_files)}):")

        for json_file in json_files:
            dest_file = self.ios_seed_data_dir / json_file.name
            status = "exists" if dest_file.exists() else "new"
            color = Fore.YELLOW if status == "exists" else Fore.GREEN
            print(f"  {color}{json_file.name:50s} [{status}]{Style.RESET_ALL}")

        print(f"\nTo deploy: python export_seed_data.py --deploy {staged_path.name}")

    def list_deployments(self, limit: int = 10):
        """
        List recent deployments.

        Args:
            limit: Maximum number of deployments to show
        """
        manifest = self._read_manifest()
        deployments = manifest.get('deployments', [])

        if not deployments:
            print(f"{Fore.YELLOW}No deployments recorded{Style.RESET_ALL}")
            return

        print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}DEPLOYMENT HISTORY{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")

        for deployment in reversed(deployments[-limit:]):
            staged = deployment.get('staged_timestamp', 'unknown')
            deployed_at = deployment.get('deployed_at', 'unknown')
            file_count = deployment.get('file_count', 0)
            backup = deployment.get('backup_timestamp')

            print(f"{Fore.GREEN}{deployed_at}{Style.RESET_ALL}")
            print(f"  Staged export: {staged}")
            print(f"  Files deployed: {file_count}")
            if backup:
                print(f"  Backup: {backup}")
            print()

        if len(deployments) > limit:
            print(f"Showing {limit} of {len(deployments)} total deployments")


def main():
    """Demo/testing entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Deployment manager for staged exports")
    parser.add_argument('--list-staged', action='store_true', help="List staged exports")
    parser.add_argument('--list-deployments', action='store_true', help="List deployment history")
    parser.add_argument('--deploy', type=str, metavar='TIMESTAMP', help="Deploy staged export")
    parser.add_argument('--preview', type=str, metavar='TIMESTAMP', help="Preview deployment")
    parser.add_argument('--confirm', action='store_true', help="Skip confirmation prompts")

    args = parser.parse_args()

    manager = DeploymentManager()

    if args.list_staged:
        manager.print_staged()
    elif args.list_deployments:
        manager.list_deployments()
    elif args.deploy:
        manager.deploy(args.deploy, confirm=args.confirm)
    elif args.preview:
        manager.preview_deploy(args.preview)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
