# Two-Step Workflow Implementation Status

## ✅ Completed

1. **requirements.txt** - Added jinja2>=3.1.0
2. **deployer.py** - Complete deployment manager (350 lines)
   - list_staged(), deploy(), preview_deploy()
   - Deployment manifest tracking
   - Backup integration
3. **report_generator.py** - HTML report generation (450 lines)
   - Beautiful HTML reports with CSS
   - Summary statistics, detailed diffs
   - Deployment instructions
4. **diff_viewer.py** - No changes needed (already provides all data)

## 🔄 In Progress - export_seed_data.py Refactoring

### Changes Needed:

#### 1. Add Imports (after line 38)
```python
from deployer import DeploymentManager
from report_generator import ReportGenerator
```

#### 2. Modify SeedDataExporter.__init__() (around line 49)
Add parameters:
- `staging_mode: bool = False`
- `staging_timestamp: Optional[str] = None`

Store these in self, use to determine output path.

#### 3. Modify _get_output_path() method (line 284)
```python
def _get_output_path(self, file_name: str) -> Path:
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
```

#### 4. Add generate_report() method to SeedDataExporter (after export_all)
```python
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
    print(f"To deploy: python scripts/export_seed_data.py --deploy {self.staging_timestamp}")
```

#### 5. Modify main() - Add New Arguments (after line 433)
```python
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
```

#### 6. Modify main() - Add Command Routing (before args parsing, after line 435)
```python
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

# Handle archive commands (existing code continues)
if args.list_archives or args.restore or args.cleanup_archives:
    # ... existing code ...

# Determine mode
staging_mode = args.stage or args.quick
quick_mode = args.quick

# Create exporter
exporter = SeedDataExporter(
    dry_run=args.dry_run or args.validate_only,
    enable_archive=not args.no_archive if not staging_mode else False,  # No archive in staging mode
    enable_diff=not args.no_diff,
    show_field_changes=args.show_field_changes,
    staging_mode=staging_mode  # NEW
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
```

## ⏳ Remaining Tasks

1. Create directory structure:
   - `mkdir -p staging deployments`
   - Add .gitkeep files

2. Update .gitignore:
   - Add `staging/` (or keep for review - TBD)

3. Test:
   - `python scripts/export_seed_data.py --stage`
   - `python scripts/export_seed_data.py --deploy TIMESTAMP`
   - `python scripts/export_seed_data.py --quick`

4. Documentation:
   - Update README.md with two-step workflow
   - Update CLAUDE.md

## Files Modified

- ✅ requirements.txt
- ✅ deployer.py (new)
- ✅ report_generator.py (new)
- ⏳ export_seed_data.py (in progress)
- ⏳ .gitignore
- ⏳ README.md
- ⏳ CLAUDE.md

## Estimated Remaining Work

- export_seed_data.py modifications: ~100 lines of changes
- Directory creation: 2 minutes
- Testing: 10 minutes
- Documentation: 15 minutes

**Total**: ~30 minutes to complete
