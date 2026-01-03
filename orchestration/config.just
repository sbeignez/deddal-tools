# Shared configuration and variables

# Project paths (relative to root justfile)
PROJECT_ROOT := justfile_directory()
ASSETS_DIR := PROJECT_ROOT / "tool-assets"
DATABASE_DIR := PROJECT_ROOT / "tool-database"
SEED_DIR := PROJECT_ROOT / "tool-seed-data-generation"
SCREENSHOTS_DIR := PROJECT_ROOT / "tool-screenshots"
LOCALIZATION_DIR := PROJECT_ROOT / "tool-localization"
BUILD_DIR := PROJECT_ROOT / "tool-build"
TESTING_DIR := PROJECT_ROOT / "tool-testing"
FASTLANE_DIR := PROJECT_ROOT / "tool-fastlane"

# Xcode configuration
XCODE_PROJECT := "Deddal.xcodeproj"
XCODE_SCHEME_DEV := "1. DEV Scheme"
XCODE_SCHEME_TESTFLIGHT := "2. TestFlight Scheme"
XCODE_SCHEME_APPSTORE := "3. App Store Scheme"
XCODE_SIMULATOR := "platform=iOS Simulator,name=iPhone 17 Pro"

# Python configuration
PYTHON := "python3"
VENV_ACTIVATE := "source venv/bin/activate"

# Ruby/Fastlane configuration
BUNDLE := "/opt/homebrew/opt/ruby/bin/bundle exec"

# Color codes for output
COLOR_RESET := "\\033[0m"
COLOR_GREEN := "\\033[0;32m"
COLOR_YELLOW := "\\033[0;33m"
COLOR_RED := "\\033[0;31m"
COLOR_BLUE := "\\033[0;34m"
COLOR_CYAN := "\\033[0;36m"
