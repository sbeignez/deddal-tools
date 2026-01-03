# Deddal iOS - Project Tools Reference

Complete catalog of all automation tools, scripts, and utilities available in the project.

**Last Updated:** 2025-12-11

> **🎉 New: Justfile Orchestration System**
>
> All tools are now orchestrated via [Just](https://github.com/casey/just) task runner. Instead of calling scripts directly, use `just` commands for better error handling, confirmation prompts, and workflow automation.
>
> **Quick Start:**
> ```bash
> just --list              # See all 95+ recipes
> just --choose            # Interactive menu
> just setup-all           # Install dependencies
> ```
>
> **See:** [tool-all/README.md](README.md) for complete Justfile documentation.

---

## Table of Contents

- [Asset Management](#asset-management)
- [Database & Seed Data](#database--seed-data)
- [Localization](#localization)
- [Testing](#testing)
- [Build & CI](#build--ci)
- [Screenshots](#screenshots)
- [Fastlane Automation](#fastlane-automation)

---

## Asset Management

**Location:** `tool-assets/`

Tools for managing case images (SVG visualizations from VisualCube API).

### Download Scripts (`tool-assets/download/`)

Download case images from VisualCube API:

- **3x3_cfop_f2l.sh** - Download F2L case images
- **3x3_cfop_oll.sh** - Download OLL case images
- **3x3_cfop_pll.sh** - Download PLL case images
- **3x3_cfop_pcll.sh** - Download PCLL case images
- **3x3_lbl.sh** - Download LBL (Layer-by-Layer) case images
- **2x2_ortega_oll.sh** - Download 2x2 Ortega OLL images
- **2x2_ortega_pbl.sh** - Download 2x2 Ortega PBL images
- **2x2_cll.sh** - Download 2x2 CLL case images

### Upload Scripts (`tool-assets/upload/`)

Upload images to Supabase storage:

- **upload_case_images.sh** - Bash script for uploading to Supabase
- **upload_case_images.py** - Python script for uploading to Supabase

**Usage (Recommended - via Justfile):**
```bash
just assets-upload-all           # Upload all assets to Supabase
just assets-upload-bash          # Use Bash script variant
```

**Legacy Usage (Direct script):**
```bash
cd tool-assets/upload
./upload_case_images.sh
```

### Rename Scripts (`tool-assets/rename/`)

Rename and organize asset files:

- **rename_assets.sh** - Master rename script
- **rename_imagesets.sh** - Rename .imageset folders
- **rename_imageset_svgs.sh** - Rename SVG files within imagesets
- **rename_svg_files.sh** - Rename individual SVG files
- **generate_rename_mapping.sh** - Generate mapping CSV for renaming

### Export Scripts (`tool-assets/export/`)

- **export-case-images.sh** - Export case images for distribution

### Populate Scripts (`tool-assets/populate/`)

Fill in missing data:

- **populate_null_image_names.sh** - Fix null image names (Bash)
- **populate_null_images.py** - Fix null images (Python)

---

## Database & Seed Data

### Database Tools (`tool-database/`)

Scripts for managing Supabase database and migrations.

#### Seed Data (`tool-database/seed/`)

Generate and update seed data:

- **generate_uuids.py** - Generate UUIDs for database records
- **update_json_files.py** - Update JSON seed files
- **update_json_seed_data.sh** - Bash wrapper for JSON updates
- **export_algs_to_json.py** - Export algorithms to JSON format

**Usage (Recommended - via Justfile):**
```bash
just db-seed-generate            # Generate UUID seed data
just db-seed-update-json         # Update JSON seed files
just db-seed-export-algs         # Export algorithms to JSON
```

**Legacy Usage (Direct script):**
```bash
cd tool-database/seed
python3 generate_uuids.py
```

#### Sync Scripts (`tool-database/sync/`)

- **sync_algorithms_to_supabase.py** - Sync algorithm library to cloud

#### Story Management (`tool-database/stories/`)

Manage story content in database:

- **sync_story_content.py** - Sync story content to Supabase
- **generate_sync_sql.py** - Generate SQL for story sync
- **sync_via_mcp.py** - Sync via Supabase MCP
- **update_index.py** - Update story index

#### Migrations (`tool-database/migrations/`)

Database schema migrations:

- **001_add_onboarding_fields.sql** - Onboarding schema migration

---

### Seed Data Generation (`tool-seed-data-generation/`)

Complete toolset for generating and deploying seed data exports.

**Main Scripts:**

- **01-stage.py** - Stage seed data for deployment
- **02-deploy.py** - Deploy seed data to Supabase

**Subdirectories:**

- `scripts/` - Helper utilities and validators
- `schemas/` - JSON schemas for validation
- `documentation/` - Implementation guides
- `deployments/` - Deployment manifests

**Usage:**
```bash
cd tool-seed-data-generation
python3 01-stage.py
python3 02-deploy.py
```

**Features:**
- JSON schema validation
- Archive management
- Diff viewing
- Deployment tracking

---

## Localization

**Location:** `tool-localization/`

Tools for managing app localization across 5 languages (en, fr, es, ja, zh-Hans).

### Scripts

- **auto_translate.py** - Automated translation using APIs
- **extract_untranslated.py** - Extract missing translations
- **import_translations.py** - Import translated strings
- **localization_helper.py** - Helper utilities
- **split_catalog.py** - Split string catalogs
- **analyze_localization.sh** - Analyze localization coverage
- **check_localization.sh** - Check for localization issues
- **create_locale_folders.sh** - Create locale folder structure

**Usage:**
```bash
cd tool-localization

# Extract untranslated strings
python3 extract_untranslated.py

# Auto-translate missing strings
python3 auto_translate.py

# Import translations
python3 import_translations.py translations.json
```

### Translation Files

- **ComprehensiveTranslations.json** - Full translation data
- **NewStringsTranslations.json** - New strings to translate

---

## Testing

**Location:** `tool-testing/`

### Scripts

- **test_algorithms.sh** - Run algorithm validation tests (~300-500 cases)

**Usage:**
```bash
cd tool-testing
./test_algorithms.sh
```

**CI Integration:**
- Used by GitHub Actions workflow: `.github/workflows/test_algorithms.yml`
- Validates F2L, OLL, PLL algorithm transformations

---

## Build & CI

**Location:** `tool-build/`

Build utilities and code quality tools.

### Scripts

- **fastlane_run.sh** - Execute Fastlane commands
- **swiftlint.sh** - Run SwiftLint code style checks
- **update_download_scripts.sh** - Update download script configurations

**Usage:**
```bash
cd tool-build

# Run SwiftLint
./swiftlint.sh

# Execute Fastlane lane
./fastlane_run.sh screenshots
```

---

## Screenshots

**Location:** `tool-screenshots/`

Complete subsystem for App Store screenshot generation.

**See:** `tool-screenshots/CLAUDE.md` for detailed documentation

**Key Features:**
- Automated screenshot capture for 5 locales
- Device frame application
- Background gradient rendering
- Text overlay localization
- Fastlane integration for App Store Connect upload

**Important:**
- Never delete full output folders (`rm -rf output/`)
- Use file-by-file replacement to preserve structure

**Usage:**
```bash
cd tool-screenshots

# Generate screenshots
./scripts/1_capture.sh

# Add device frames
./scripts/2_frame.sh

# Add text overlays
./scripts/3_text.sh
```

---

## Fastlane Automation

**Location:** `tool-fastlane/`

Comprehensive App Store Connect automation using Fastlane.

**Configuration Files:**
- `Fastfile` - Main lane definitions
- `Deliverfile` - Metadata delivery configuration
- `Snapfile` - Screenshot capture configuration

### Screenshot Lanes

#### Production Screenshots
```bash
# Generate all production screenshots
bundle exec fastlane ios screenshots_prod
# or
bundle exec fastlane ios snap

# Generate dark mode screenshots
bundle exec fastlane ios screenshots_dark

# Generate both light and dark
bundle exec fastlane ios screenshots_both
```

#### Test Screenshots
```bash
# Quick test (1 device, 1 language)
bundle exec fastlane ios screenshots_test

# Dark mode test
bundle exec fastlane ios screenshots_dark_test
```

#### Framing
```bash
# Add frames to production screenshots
bundle exec fastlane ios frame

# Add frames to test screenshots
bundle exec fastlane ios frame_test
```

### Upload Lanes

```bash
# Update all release notes with standard text
bundle exec fastlane ios update_release_notes

# Upload screenshots only
bundle exec fastlane ios upload_screenshots

# Upload metadata only (release notes, descriptions, etc.)
bundle exec fastlane ios upload_metadata

# Upload both screenshots and metadata
bundle exec fastlane ios upload_all
```

**update_release_notes** - Updates all 39 locale release notes with standard minimal text:
- "We're constantly improving Deddal. This update includes performance enhancements and bug fixes."
- No competitive intelligence leaked
- Professional and simple
- Includes feedback email (contact@deddal.app)

### Version Management Lanes

**NEW** - Query and create App Store Connect versions:

```bash
# Check current version status
bundle exec fastlane ios check_version_status

# Create new version
bundle exec fastlane ios create_new_version version:1.0.7
```

**Features:**
- Query live and in-development versions
- Display version status with emoji indicators
- Create new versions with duplicate detection
- Show next steps after version creation

### Utility Lanes

```bash
# Clean test screenshots
bundle exec fastlane ios clean_test

# Clean production screenshots
bundle exec fastlane ios clean_prod
```

### Complete Workflow Example

```bash
# 1. Check current version status
bundle exec fastlane ios check_version_status

# 2. Create new version if needed
bundle exec fastlane ios create_new_version version:1.0.7

# 3. Update release notes with standard text
bundle exec fastlane ios update_release_notes

# 4. Generate screenshots
bundle exec fastlane ios screenshots_prod

# 5. Add device frames
bundle exec fastlane ios frame

# 6. Upload to App Store Connect
bundle exec fastlane ios upload_all

# 7. Upload a build (done separately via Xcode or CI)
```

---

## Development Commands

From `CLAUDE.md`:

### Building

```bash
# Build debug configuration
xcodebuild -project Deddal.xcodeproj -scheme "1. DEV Scheme" -configuration 1.Debug build

# Build for TestFlight
xcodebuild -project Deddal.xcodeproj -scheme "2. TestFlight Scheme" -configuration 2.TestFlight build

# Build for App Store
xcodebuild -project Deddal.xcodeproj -scheme "3. App Store Scheme" -configuration 3.Release build
```

### Testing

```bash
# Run all tests
xcodebuild test -project Deddal.xcodeproj -scheme "1. DEV Scheme" -testPlan Deddal.xctestplan -destination 'platform=iOS Simulator,name=iPhone 17 Pro'

# Run specific test class
xcodebuild test -project Deddal.xcodeproj -scheme "1. DEV Scheme" -only-testing:DeddalTests/CubeTests -destination 'platform=iOS Simulator,name=iPhone 17 Pro'
```

---

## Quick Reference

### Most Common Commands

```bash
# Check App Store version
bundle exec fastlane ios check_version_status

# Create new version
bundle exec fastlane ios create_new_version version:1.0.7

# Generate screenshots
bundle exec fastlane ios snap

# Upload metadata
bundle exec fastlane ios upload_metadata

# Run tests
xcodebuild test -project Deddal.xcodeproj -scheme "1. DEV Scheme" -testPlan Deddal.xctestplan -destination 'platform=iOS Simulator,name=iPhone 17 Pro'

# Sync algorithms to Supabase
cd tool-database/sync && python3 sync_algorithms_to_supabase.py

# Upload case images
cd tool-assets/upload && ./upload_case_images.sh

# Check localization coverage
cd tool-localization && ./analyze_localization.sh
```

---

## Getting Help

- **Fastlane:** `bundle exec fastlane lanes` - List all available lanes
- **Tool Docs:** Each tool directory may contain its own README or CLAUDE.md
- **Main Docs:** `/documentation` - Project-wide documentation
- **CLAUDE.md:** Project-specific instructions for AI assistance

---

## Contributing

When adding new tools:

1. Place in appropriate `tool-*` directory
2. Add brief description to this document
3. Include usage examples
4. Document any dependencies
5. Update table of contents if adding new category
