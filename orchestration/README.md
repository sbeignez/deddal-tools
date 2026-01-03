# Justfile Orchestration System

Deddal iOS uses [Just](https://github.com/casey/just) to orchestrate 60+ tools across 9 specialized folders. This provides a unified CLI with interactive menus, dependency tracking, error handling, and workflow automation.

## Quick Start

### Installation

```bash
# Install Just (if not already installed)
brew install just

# Optional: Install fzf for enhanced interactive menus
brew install fzf

# Verify installation
just --version
```

### First-Time Setup

```bash
# From project root
cd /path/to/deddal-ios

# Install all dependencies (Python, Ruby, etc.)
just setup-all

# Verify everything works
just --list
```

## Common Usage

```bash
# Show all available recipes
just --list

# Interactive menu (choose with arrow keys)
just --choose

# Quick menu alias
just menu

# Run specific recipe
just build-debug
just screenshots-generate-all
just seed-export-all
```

## Recipe Categories

All recipes follow the naming convention: `<domain>-<action>-<target>`

### Setup (`setup-*`)
**First-time environment configuration**

```bash
just setup-all                   # Install all dependencies
just setup-check-dependencies    # Verify tools installed
just setup-python-env            # Create Python virtual environments
just setup-ruby-bundler          # Install Ruby gems (Fastlane)
```

### Workflows (`workflow-*`)
**High-level cross-tool workflows**

```bash
just workflow-release-prep       # Complete release preparation
just workflow-asset-refresh      # Download → populate → rename → upload assets
just workflow-db-sync            # Database sync workflow
just workflow-dev-setup          # Setup development environment
just workflow-pre-commit         # Pre-commit validation (lint + tests)
just workflow-ci                 # CI/CD simulation
```

### Build (`build-*`)
**Build and testing**

```bash
just build-debug                 # Build debug configuration
just build-testflight            # Build TestFlight configuration
just build-appstore              # Build App Store configuration
just build-clean                 # Clean build artifacts
just build-test-all              # Run all tests (unit + UI)
just build-test-unit             # Run unit tests only
just build-test-ui               # Run UI tests only
just build-test-class CubeTests  # Run specific test class
just build-lint                  # Run SwiftLint
```

### Seed Data (`seed-*`)
**Export seed data from database**

```bash
just seed-export-all             # Export all 41 JSON files (auto-backup)
just seed-export-dry-run         # Preview changes without writing
just seed-export-file f2l_cases.json  # Export single file
just seed-list-archives          # Show available backups
just seed-restore 2025-12-11     # Restore from backup
just seed-stage-deploy           # Stage and deploy workflow
```

### Database (`db-*`)
**Database management**

```bash
just db-migrate-run              # Run SQL migrations
just db-migrate-check            # Check migration status
just db-seed-generate            # Generate UUID seed data
just db-sync-algorithms          # Sync algorithms to Supabase
just db-sync-stories             # Sync story content to Supabase
```

### Assets (`assets-*`)
**Asset management (case images)**

```bash
just assets-download-all         # Download all case images from VisualCube API
just assets-download-f2l         # Download F2L cases only
just assets-upload-all           # Upload to Supabase storage
just assets-rename-all           # Rename and organize assets
just assets-populate-nulls       # Populate null image names
```

### Screenshots (`screenshots-*`)
**App Store screenshot generation**

```bash
just screenshots-generate-all    # Full 5-step pipeline
just screenshots-snap            # Step 1: Capture via UI tests
just screenshots-frame           # Step 2: Add device frames
just screenshots-background      # Step 3: Render gradients
just screenshots-text            # Step 4: Overlay localized text
just screenshots-upload          # Step 5: Upload to App Store Connect
just screenshots-locale fr       # Generate for specific locale
just screenshots-preview         # Open in Finder
```

### Localization (`loc-*`)
**Translation management**

```bash
just loc-extract-untranslated    # Find missing translations
just loc-auto-translate          # AI translation (costs money)
just loc-import-translations     # Import to string catalogs
just loc-check-coverage          # Analyze coverage
just loc-check-missing           # Validation
just loc-workflow-full           # Extract → translate → import
```

### Testing (`test-*`)
**Algorithm validation**

```bash
just test-algorithms             # Run ~300-500 algorithm tests
just test-algorithms-method f2l  # Test specific method (f2l/oll/pll)
```

### Fastlane (`fastlane-*`)
**App Store automation**

```bash
just fastlane-screenshots        # Generate via Fastlane
just fastlane-upload-screenshots # Upload to App Store Connect
just fastlane-upload-metadata    # Upload metadata only
just fastlane-run <lane>         # Run custom Fastlane lane
```

### Version Management (`version-*`, `release-*`)
**Automated version bumping and release workflow**

#### Display & Atomic Operations

```bash
just version-show                # Show current version and build
just v                           # Alias for version-show

just version-bump-patch          # 1.2.3 → 1.2.4 (bug fixes)
just vp                          # Alias

just version-bump-minor          # 1.2.3 → 1.3.0 (new features)
just vm                          # Alias

just version-bump-major          # 1.2.3 → 2.0.0 (breaking changes)
just vM                          # Alias

just version-set 1.2.3           # Set specific version
just version-bump-build          # Increment build number
just version-commit              # Commit version changes to git
just version-tag                 # Create and push git tag
```

#### App Store Connect Integration

```bash
just version-check-asc           # Check ASC version status
just version-create-asc 1.2.3    # Create new version in ASC
```

#### Complete Release Workflows

```bash
# Patch release (bug fixes)
just release-patch               # Bump patch → build → commit → tag → ASC
just rp                          # Alias

# Minor release (new features)
just release-minor               # Bump minor → reset build → commit → tag → ASC
just rm                          # Alias

# Major release (breaking changes)
just release-major               # Bump major → reset build → commit → tag → ASC
just rM                          # Alias

# Custom release
just release-custom 1.2.3 42     # Set version + build → commit → tag → ASC
```

#### Rollback & Verification

```bash
just version-rollback            # Undo last version commit (preserves changes)
just version-verify              # Verify Xcode project vs git tags consistency
```

**Workflow Steps:**
1. **Local version bump** - Updates Xcode project
2. **Build increment** - Increments build number
3. **Git commit** - Commits with standard message
4. **Git tag** - Creates versioned tag (e.g., `v1.2.3-42`)
5. **ASC version creation** - Creates version in App Store Connect

**Example: Patch Release**
```bash
# Before: 1.0.6 (Build 15)
just release-patch

# Runs:
# - bump_patch → 1.0.7
# - bump_build → Build 16
# - commit_version → "Bump version to 1.0.7 (16)"
# - tag_version → Creates tag v1.0.7-16
# - create_new_version → Creates 1.0.7 in ASC

# After: 1.0.7 (Build 16)
# Next: Upload build to TestFlight for version 1.0.7
```

## Interactive Menus

### Main Menu

```bash
just menu
# or
just --choose
```

Shows all 95+ recipes alphabetically, naturally grouped by prefix.

### Category Menus

```bash
just a   # Assets menu
just b   # Build menu
just d   # Database menu
just l   # Localization menu
just s   # Screenshots menu
just w   # Workflows menu
```

Shortcuts for category-specific recipe selection.

### With Fuzzy Search (fzf)

If `fzf` is installed:
```bash
just --choose
# Type "download" → filters to download recipes
# Arrow keys to select, Enter to run
```

## Common Workflows

### Daily Development

```bash
# Morning: Check dependencies
just setup-check-dependencies

# Development cycle
just build-debug
just build-test-unit

# Before committing
just workflow-pre-commit
```

### Asset Update

```bash
# Full asset pipeline
just workflow-asset-refresh

# Or step-by-step
just assets-download-all
just assets-populate-nulls
just assets-rename-all
just assets-upload-all
```

### Release Preparation

```bash
# Complete release workflow
just workflow-release-prep       # Migrations → seed → screenshots → tests

# Version management (new!)
just release-patch               # Automated patch release (1.0.6 → 1.0.7)
just release-minor               # Automated minor release (1.0.6 → 1.1.0)
just release-major               # Automated major release (1.0.6 → 2.0.0)

# Or manual steps
just version-show                # Check current version
just db-migrate-check            # Verify migrations
just seed-export-all             # Export seed data
just loc-check-coverage          # Check translations
just screenshots-generate-all    # Generate screenshots
just build-test-all              # Run tests
just version-bump-patch          # Bump version
just version-commit              # Commit version
just version-tag                 # Tag release
just version-create-asc 1.0.7    # Create ASC version
# → Upload build to TestFlight
just screenshots-upload          # Upload screenshots
```

### Seed Data Management

```bash
# 1. Update database (via Supabase admin or migrations)
just db-migrate-run

# 2. Preview changes
just seed-export-dry-run

# 3. Export seed data (creates automatic backup)
just seed-export-all

# 4. Test in app
just build-debug

# 5. If issues, restore backup
just seed-list-archives
just seed-restore 2025-12-11_143000
```

## Advanced Features

### Confirmation Prompts

Destructive operations require Y/n confirmation:

```bash
just assets-upload-all
# → Prompt: Upload all assets to Supabase? (Y/n)

just db-migrate-run
# → Prompt: Run all pending migrations? (Y/n)
```

### Error Handling

All recipes have automatic error detection:

```bash
just assets-download-all
# If any script fails:
# ❌ Failed: tool-assets/download/3x3_cfop_f2l.sh
```

### Colored Output

- ✅ Green - Success messages
- ⚠️  Yellow - Warnings
- ❌ Red - Errors
- ℹ️  Blue - Info messages
- [1/5] Cyan - Step progress

### Python Venv Auto-Activation

Recipes automatically activate Python virtual environments:

```bash
just seed-export-all
# Automatically: cd tool-seed-data-generation && source venv/bin/activate && python export_seed_data.py
```

## Troubleshooting

### Just Not Found

```bash
# Check installation
which just

# Install if missing
brew install just
```

### Python Virtual Environment Errors

```bash
# Reset Python environments
rm -rf tool-seed-data-generation/venv
rm -rf tool-database/venv
rm -rf tool-localization/venv

# Re-run setup
just setup-python-env
```

### Recipe Failed

```bash
# Check the script manually
cd tool-assets/download
./3x3_cfop_f2l.sh
```

### Xcode Build Errors

```bash
# Clean and rebuild
just build-clean
just build-debug
```

## Migration from Direct Script Usage

**Before (manual):**
```bash
cd tool-seed-data-generation
source venv/bin/activate
python export_seed_data.py
```

**After (orchestrated):**
```bash
just seed-export-all
```

**Benefits:**
- ✅ Auto venv activation
- ✅ Error handling
- ✅ Colored output
- ✅ Confirmation prompts
- ✅ Automatic backups

## File Structure

```
justfile (root)                    # Minimal orchestrator
└── tool-all/
    ├── config.just               # Shared configuration
    ├── helpers.just              # Reusable helper functions
    ├── workflows.just            # High-level workflows
    ├── recipes/
    │   ├── assets.just           # Asset recipes (15 recipes)
    │   ├── build.just            # Build recipes (11 recipes)
    │   ├── database.just         # Database recipes (11 recipes)
    │   ├── seed.just             # Seed data recipes (9 recipes)
    │   ├── screenshots.just      # Screenshot recipes (11 recipes)
    │   ├── localization.just     # Localization recipes (8 recipes)
    │   ├── testing.just          # Testing recipes (2 recipes)
    │   └── fastlane.just         # Fastlane recipes (5 recipes)
    └── README.md                 # This file
```

## Contributing

When adding new tools or scripts:

1. Add wrapper recipes to appropriate `tool-all/recipes/*.just` file
2. Follow naming convention: `<domain>-<action>-<target>`
3. Use helper recipes from `tool-all/helpers.just`
4. Add confirmation prompts for destructive operations
5. Test with `just --list` and `just <recipe-name>`
6. Update this README if adding new categories

## Tips & Best Practices

1. **Use `--list` to discover:**
   ```bash
   just --list | grep download
   ```

2. **Dry-run before destructive ops:**
   ```bash
   just seed-export-dry-run
   just seed-export-all
   ```

3. **Test locally before CI/CD:**
   ```bash
   just workflow-ci
   ```

4. **Use workflows for multi-step tasks:**
   ```bash
   just workflow-release-prep
   ```

5. **Category menus for focused work:**
   ```bash
   just a  # Assets only
   just s  # Screenshots only
   ```

## Reference

- [Just Documentation](https://just.systems/)
- [Just GitHub Repo](https://github.com/casey/just)
- Project CLAUDE.md - Architecture and development guide
- `/Users/trophee-mini/.claude/plans/snappy-cuddling-spark.md` - Implementation plan
