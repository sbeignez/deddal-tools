# Seed Data Generation Tool

**Purpose**: Export Supabase database to iOS seed JSON files using dynamic discovery.

The database is the single source of truth. This script automatically discovers all case sets from the database and generates 3 files per case set (case sets, cases, algorithms). Files are NOT hardcoded - the export adapts to database changes automatically.

---

## Quick Start

```bash
# One-time setup
cd tools/shared/seed-data
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure database credentials
cp .env.example .env
# Edit .env with your Supabase credentials

# Export all seed data (creates backup first)
python scripts/export_seed_data.py

# Preview without writing files (shows diff comparison)
python scripts/export_seed_data.py --dry-run

# Export without creating backup
python scripts/export_seed_data.py --no-archive
```

---

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd /Users/trophee-mini/code/deddal/deddal-ios/tools/shared/seed-data

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Database Connection

Create `.env` file with your Supabase credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```
SUPABASE_HOST=db.qoglsyykgrqalsemigii.supabase.co
SUPABASE_PORT=5432
SUPABASE_DATABASE=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_actual_password_here
```

**Important**: Never commit `.env` to git (it's in `.gitignore`).

---

## Usage

### Export All Files (Dynamic Discovery)

```bash
python scripts/export_seed_data.py
```

**Output**: JSON files in `DeddalInfra/Infrastructure/Persistence/SeedData/` (dynamically generated based on database):
- For each case set in `lib_casesets` table, generates 3 files:
  - `seeddata_caseset_{caseset_code}.json` - Case set metadata
  - `seeddata_cases_{caseset_code}.json` - All cases for that case set
  - `seeddata_algorithms_{caseset_code}.json` - All algorithms for those cases
- File count adapts automatically as you add/remove case sets in the database

**Example**: For case set with code "3x3-cfop-f2l", generates:
- `seeddata_caseset_3x3-cfop-f2l.json`
- `seeddata_cases_3x3-cfop-f2l.json`
- `seeddata_algorithms_3x3-cfop-f2l.json`

### Dry Run (Preview Only)

```bash
python scripts/export_seed_data.py --dry-run
```

Preview what would be exported without writing files. Useful for:
- Testing database connection
- Validating queries
- Checking record counts

### Export Single File

```bash
python scripts/export_seed_data.py --file seeddata_cases_3x3-cfop-oll.json
```

Export only the specified file. Useful for:
- Testing changes to a specific query
- Quick iteration during development

### Validate Only (No Export)

```bash
python scripts/export_seed_data.py --validate-only
```

Run all validation checks without exporting. Useful for:
- Checking data integrity in database
- Finding validation errors before export

### Enhanced Dry-Run with Diff Preview

```bash
python scripts/export_seed_data.py --dry-run
```

Dry-run mode now shows detailed comparison with existing files:
- Count changes (added/removed records)
- Added/removed record IDs
- Breaking change warnings (>10% removal, >50% count change)
- Files with warnings highlighted in summary

```bash
python scripts/export_seed_data.py --dry-run --show-field-changes
```

Verbose mode shows field-level changes for modified records.

### Backup Management

#### Automatic Backup Before Export

By default, the script creates a timestamped backup before each export:

```bash
python scripts/export_seed_data.py  # Creates backup in backups/YYYY-MM-DD_HHMMSS/
```

Backups are stored in `tools/shared/seed-data/backups/` with manifest tracking.

#### Skip Backup

```bash
python scripts/export_seed_data.py --no-archive
```

#### List All Backups

```bash
python scripts/export_seed_data.py --list-archives
```

Shows all available backups with timestamps, file counts, and record counts.

#### Restore from Backup

```bash
python scripts/export_seed_data.py --restore 2025-12-05_170000
```

Restores all files from the specified backup (prompts for confirmation).

#### Cleanup Old Backups

```bash
python scripts/export_seed_data.py --cleanup-archives
```

Removes old backups (keeps 10 most recent, deletes older than 30 days).

---

## Output Format

All files are generated in JSON format compatible with iOS DTOs:

### Case Sets (`CaseSetDTO`)

```json
[
  {
    "id": "uuid-here",
    "code": "oll",
    "name": "OLL",
    "subtitle": "Orient Last Layer",
    "pattern_from": "2 Layers",
    "pattern_to": "Top Oriented",
    "expected_count": 57,
    "category": "Last Layer",
    "created_at": "2025-10-24T11:25:09.730Z",
    "case_ids": ["uuid-1", "uuid-2", ...]
  }
]
```

### Cases (`MethodCaseDTO`)

```json
[
  {
    "id": "uuid-here",
    "code": "OLL-1",
    "case_set_id": "uuid-of-case-set",
    "title": "Dot",
    "long_name": "OLL 1 - Dot",
    "kind": "oll",
    "pattern_from": "2 Layers",
    "pattern_to": "Top Oriented",
    "scramble": null,
    "notes": null,
    "story": null,
    "description": "All edges flipped incorrectly",
    "image_url": null,
    "image_asset_name": "3x3_cfop_oll_1",
    "difficulty": 3,
    "popularity": 75,
    "groups": ["shape:dot", "level:intermediate"],
    "created_at": "2025-10-24T11:25:09.730Z",
    "updated_at": "2025-10-24T11:25:09.730Z"
  }
]
```

### Algorithms (`AlgorithmDTO`)

```json
[
  {
    "id": "uuid-here",
    "case_id": "uuid-of-case",
    "code": "OLL-1-01",
    "sequence": "R U2 R2 F R F' U2 R' F R F'",
    "name": "Algorithm 1",
    "tags": ["fast", "fingertrick-heavy"],
    "popularity": 85,
    "difficulty": 3,
    "avg_moves": 17,
    "avg_execution_time_ms": 1200,
    "story": "Right trigger into sledgehammer",
    "created_at": "2025-10-24T11:25:09.730Z"
  }
]
```

---

## Validation

The script performs comprehensive validation:

### 1. UUID Validation
- All `id` fields must be valid UUIDs
- No duplicate IDs

### 2. Required Fields
- **Case Sets**: `id`, `code`, `name`
- **Cases**: `id`, `code`, `kind`
- **Algorithms**: `id`, `case_id`, `code`, `sequence`

### 3. Foreign Key Integrity
- `case_id` in algorithms must exist in cases
- `case_ids` in case sets must exist in cases
- `case_set_id` in cases must exist in case sets (if not null)

### 4. Case Kind Validation
- `kind` field must exist in `lib_cases` table (dynamic discovery)
- Validator queries database for all distinct `kind` values at runtime
- No hardcoded enum - automatically adapts to database changes
- Add new case kinds to database and validation adapts automatically

### 5. Data Completeness
- Required files must have records
- Warns if datasets have suspiciously low counts (<3 records)

---

## CI Validation

PRs touching `DeddalInfra/Infrastructure/Persistence/SeedData/**` automatically run validation via GitHub Actions.

### What Gets Validated in CI

| Check | Description |
|-------|-------------|
| JSON Schema | Structure, types, required fields, UUID formats |
| UUID Validation | All IDs are valid UUID format, no duplicates |
| Required Fields | Case sets: id, code, name. Cases: id, code, kind. Algorithms: id, case_id, code, sequence |
| Foreign Key Integrity | Algorithms reference valid cases, case_ids reference valid cases |

### Run Locally

```bash
# Using just recipe (recommended)
just test-seed-data

# Or directly with Python
tools/shared/seed-data/venv/bin/python tools/shared/seed-data/scripts/ci_validate.py --verbose
```

### What's NOT Validated in CI

These require database connection and are validated during `01-stage.py`:

- Case kind enum validation (uses dynamic discovery from DB)
- Data completeness warnings
- Count mismatch detection

---

## Dynamic Discovery Architecture

**No hardcoded file definitions!** The export tool uses database-driven discovery:

### How It Works

1. **Discovery Phase**: Query `lib_casesets` table for all case sets
2. **Generation Phase**: For each case set, generate 3 export definitions:
   - Case sets query: `WHERE cs.id = '{caseset_id}'`
   - Cases query: `WHERE cc.caseset_id = '{caseset_id}'`
   - Algorithms query: Join through cases to caseset
3. **Export Phase**: Execute queries and write JSON files

### Adding New Case Sets

Simply add records to `lib_casesets` table - no code changes needed:

```sql
INSERT INTO lib_casesets (code, name, category, expected_count)
VALUES ('3x3-new-caseset', 'New Case Set', 'Category Name', 42);
```

Next export automatically generates 3 files:
- `seeddata_caseset_3x3-new-caseset.json`
- `seeddata_cases_3x3-new-caseset.json`
- `seeddata_algorithms_3x3-new-caseset.json`

---

## Troubleshooting

### Connection Error

```
ConnectionError: Failed to connect to database: ...
```

**Solution**:
- Check `.env` file exists and has correct credentials
- Verify Supabase host and password
- Check network connection

### Missing Environment Variables

```
ValueError: Missing required environment variables: SUPABASE_PASSWORD
```

**Solution**:
- Ensure `.env` file exists in `tools/shared/seed-data/`
- Verify all required variables are set (HOST, DATABASE, USER, PASSWORD)

### Validation Errors

```
✗ Validation failed for seeddata_cases_3x3-cfop-oll.json (required file)
  • Record 5: Missing required field 'kind'
```

**Solution**:
- Fix data in Supabase database
- Ensure required fields are not null
- Check UUIDs are valid
- Verify foreign key relationships

### Empty Dataset

```
⚠ seeddata_cases_3x3-coll.json: No records found (skipping optional file)
```

**Solution** (if unexpected):
- Check SQL query filters in `config.yaml`
- Verify data exists in database for that case type
- Check `kind` field values match query filters

### File Permission Error

```
PermissionError: [Errno 13] Permission denied: 'DeddalInfra/Infrastructure/Persistence/SeedData/...'
```

**Solution**:
- Ensure output directory is writable
- Check Xcode isn't locking the files
- Close Xcode project before running export

---

## Integration with iOS

After exporting, the files are immediately available to the iOS app:

1. **Automatic Loading**: `MethodsSeedLoader` loads files on app launch
2. **No Xcode Changes**: Files already in "Copy Bundle Resources"
3. **Validation**: Repository hydration validates relationships

To test the exported data:

```swift
// In Xcode, run the app and check logs for:
// [MethodsSeedLoader] ✅ Loaded <count> case sets and <count> cases
// [MethodsRepository] ✅ Seed data hydration complete
```

If there are warnings:

```swift
// [MethodsRepository] ⚠️ Algorithm <code> references unknown case: <uuid>
```

This indicates foreign key issues - run validator and fix database.

---

## Workflow

### Regular Workflow (After DB Changes)

```bash
# 1. Update Supabase data via admin panel or migration

# 2. Export fresh seed data
cd tools/shared/seed-data
source venv/bin/activate
python scripts/export_seed_data.py

# 3. Build and run iOS app to test
cd ../
xcodebuild -project Deddal.xcodeproj -scheme "1. DEV Scheme" build
```

### Testing Workflow (Before Committing)

```bash
# 1. Dry run to preview (shows diff comparison)
python scripts/export_seed_data.py --dry-run

# 2. Validate only
python scripts/export_seed_data.py --validate-only

# 3. Export single file to test
python scripts/export_seed_data.py --file seeddata_cases_3x3-cfop-oll.json

# 4. Full export (creates automatic backup)
python scripts/export_seed_data.py

# 5. Git diff to review changes
git diff DeddalInfra/Infrastructure/Persistence/SeedData/

# 6. If needed, restore from backup
python scripts/export_seed_data.py --list-archives
python scripts/export_seed_data.py --restore 2025-12-05_170000
```

---

## Features

**Implemented**:

- ✅ **Backup Management**: Auto-backup before export with manifest tracking
- ✅ **Diff Viewer**: Compare old vs new exports with detailed change detection
- ✅ **Restore Capability**: Rollback to previous backups
- ✅ **Breaking Change Warnings**: Alerts for significant data changes

**Future Enhancements** (ideas for future):

- **Incremental Export**: Only export files that changed
- **GitHub Actions**: Auto-export on DB migrations
- **Cross-validation**: Validate relationships across files
- **Performance**: Parallel query execution
- **Logging**: Write detailed log file

---

## Support

If you encounter issues:

1. Check this README troubleshooting section
2. Verify `config.yaml` syntax is valid
3. Test database connection with `--validate-only`
4. Review validation errors in output
5. Check Supabase database directly

For schema changes:
- Add/remove case sets in `lib_casesets` table (export adapts automatically)
- Add/remove case kinds in `lib_cases` table (validation adapts automatically)
- Update iOS DTOs to match if field names change
- No code changes needed for new case sets or case kinds

---

**Last Updated**: December 5, 2025
**Maintainer**: Deddal Development Team
