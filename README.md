# Deddal Tools

Automation tools for Deddal multi-platform project.

## Structure

- `shared/` - Cross-platform tools (screenshots, assets, database, etc.)
- `ios/` - iOS-specific tools (fastlane, build, testing, architecture validation)
- `android/` - Android-specific tools (future)
- `web/` - Web-specific tools (future)
- `orchestration/` - Cross-platform Just recipes and workflows

## Usage

This repository is used as a git submodule in platform repos:
- `deddal-ios/tools/` → this repo
- `deddal-android/tools/` → this repo (future)
- `deddal-web/tools/` → this repo (future)

See individual platform repos for setup instructions.
