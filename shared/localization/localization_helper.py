#!/usr/bin/env python3
"""
iOS Localization Helper Script

This script provides utilities for managing Xcode String Catalogs in the Deddal iOS app.
It encapsulates all the learnings from localization issues encountered during development.

Usage:
    python3 Scripts/localization_helper.py <command> [args]

Commands:
    protect-core           Set all Core strings to "manual" extraction state
    validate-core          Check if Core.xcstrings only contains universal UI strings
    move-string            Move a string between catalogs
    find-untranslated      Find strings missing translations for a language
    add-core-string        Add a new string to Core.xcstrings with proper formatting
    check-extraction       Check extraction states across all catalogs
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Set

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
CORE_PATH = PROJECT_ROOT / "Deddal/App/Localization/Core.xcstrings"
ONBOARDING_PATH = PROJECT_ROOT / "Deddal/App/Localization/Onboarding.xcstrings"
LOCALIZABLE_PATH = PROJECT_ROOT / "Deddal/App/Localization/Localizable.xcstrings"

# Valid Core strings (universal UI actions only)
VALID_CORE_STRINGS = {
    'Add', 'Back', 'Cancel', 'Close', 'Continue', 'Delete',
    'Done', 'Next', 'No', 'OK', 'Save', 'Skip'
}

# App-specific strings that should NOT be in Core
APP_SPECIFIC_STRINGS = {
    'Home', 'Library', 'Practice', 'Progress', 'Settings',
    'Today', 'Account', 'Profile', 'Statistics'
}

# Supported languages
LANGUAGES = ['ja', 'fr', 'es', 'zh-Hans']


def load_catalog(path: Path) -> Dict:
    """Load a String Catalog JSON file."""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_catalog(path: Path, catalog: Dict):
    """Save a String Catalog JSON file."""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved {path.name}")


def protect_core():
    """Set all Core strings to 'manual' extraction state to prevent Xcode removal."""
    print("Protecting Core.xcstrings from automatic removal...")

    core = load_catalog(CORE_PATH)
    updated = 0

    for key, value in core['strings'].items():
        current_state = value.get('extractionState')
        if current_state != 'manual':
            value['extractionState'] = 'manual'
            updated += 1
            print(f"  • {key}: {current_state or 'none'} → manual")

    if updated > 0:
        save_catalog(CORE_PATH, core)
        print(f"\n✓ Protected {updated} strings from automatic removal")
    else:
        print("✓ All strings already protected")


def validate_core():
    """Check if Core.xcstrings only contains universal UI strings."""
    print("Validating Core.xcstrings structure...")

    core = load_catalog(CORE_PATH)
    issues = []

    for key in core['strings'].keys():
        if key not in VALID_CORE_STRINGS:
            if key in APP_SPECIFIC_STRINGS:
                issues.append(f"⚠️  '{key}' is app-specific, should be in Localizable.xcstrings")
            else:
                issues.append(f"⚠️  '{key}' might not be universal enough for Core.xcstrings")

    for key in VALID_CORE_STRINGS:
        if key not in core['strings']:
            issues.append(f"❌ Missing expected Core string: '{key}'")

    if issues:
        print("\nIssues found:")
        for issue in issues:
            print(f"  {issue}")
        return False
    else:
        print(f"✓ Core.xcstrings is valid ({len(core['strings'])} strings)")
        return True


def find_untranslated(catalog_path: Path, language: str):
    """Find strings missing translations for a specific language."""
    catalog = load_catalog(catalog_path)
    untranslated = []

    for key, value in catalog['strings'].items():
        localizations = value.get('localizations', {})
        if language not in localizations:
            untranslated.append((key, 'missing'))
        elif localizations[language]['stringUnit']['state'] == 'new':
            untranslated.append((key, 'new'))

    print(f"\n{catalog_path.name}: Untranslated {language} strings: {len(untranslated)}\n")

    if untranslated:
        for key, state in untranslated[:20]:  # Show first 20
            print(f"  • {key} ({state})")

        if len(untranslated) > 20:
            print(f"\n  ... and {len(untranslated) - 20} more")
    else:
        print("  ✓ All strings translated!")


def check_extraction_states():
    """Check extraction states across all catalogs."""
    print("Checking extraction states across all catalogs...\n")

    catalogs = {
        'Core': CORE_PATH,
        'Onboarding': ONBOARDING_PATH,
        'Localizable': LOCALIZABLE_PATH
    }

    for name, path in catalogs.items():
        catalog = load_catalog(path)
        states = {}

        for key, value in catalog['strings'].items():
            state = value.get('extractionState', 'omitted')
            states[state] = states.get(state, 0) + 1

        print(f"{name}.xcstrings:")
        print(f"  Total strings: {len(catalog['strings'])}")
        for state, count in sorted(states.items()):
            print(f"  {state}: {count}")
        print()


def add_core_string(key: str):
    """Add a new string to Core.xcstrings with proper template."""
    if key in VALID_CORE_STRINGS:
        print(f"String '{key}' already exists in valid Core strings")
        return

    print(f"\n⚠️  WARNING: '{key}' will be added to Core.xcstrings")
    print("Make sure this is a universal UI action, not app-specific!")
    print("\nValid Core strings should be:")
    print("  • Generic action words (Back, Cancel, Done, Save, etc.)")
    print("  • Reusable across any iOS app")
    print("  • Used in 5+ different screens\n")

    response = input("Continue? (y/N): ")
    if response.lower() != 'y':
        print("Cancelled")
        return

    comment = input("Enter generic comment (e.g., 'Action button to...'): ")

    # Translations
    translations = {}
    for lang in LANGUAGES:
        value = input(f"Enter {lang} translation: ")
        translations[lang] = value

    # Load and update Core catalog
    core = load_catalog(CORE_PATH)

    core['strings'][key] = {
        'comment': comment,
        'extractionState': 'manual',  # Critical!
        'localizations': {
            lang: {
                'stringUnit': {
                    'state': 'translated',
                    'value': value
                }
            }
            for lang, value in translations.items()
        }
    }

    save_catalog(CORE_PATH, core)
    print(f"\n✓ Added '{key}' to Core.xcstrings with 'manual' extraction state")


def move_string(key: str, from_catalog: str, to_catalog: str):
    """Move a string between catalogs."""
    catalog_map = {
        'core': CORE_PATH,
        'onboarding': ONBOARDING_PATH,
        'localizable': LOCALIZABLE_PATH
    }

    from_path = catalog_map.get(from_catalog.lower())
    to_path = catalog_map.get(to_catalog.lower())

    if not from_path or not to_path:
        print("Invalid catalog names. Use: core, onboarding, or localizable")
        return

    # Load both catalogs
    from_cat = load_catalog(from_path)
    to_cat = load_catalog(to_path)

    # Check if string exists
    if key not in from_cat['strings']:
        print(f"String '{key}' not found in {from_catalog}.xcstrings")
        return

    # Move string
    string_data = from_cat['strings'][key]
    to_cat['strings'][key] = string_data
    del from_cat['strings'][key]

    # Save both catalogs
    save_catalog(from_path, from_cat)
    save_catalog(to_path, to_cat)

    print(f"\n✓ Moved '{key}' from {from_catalog} to {to_catalog}")


def print_usage():
    """Print usage information."""
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]

    try:
        if command == 'protect-core':
            protect_core()

        elif command == 'validate-core':
            validate_core()

        elif command == 'find-untranslated':
            if len(sys.argv) < 4:
                print("Usage: find-untranslated <catalog> <language>")
                print("Catalogs: core, onboarding, localizable")
                print("Languages: ja, fr, es, zh-Hans")
                sys.exit(1)

            catalog_map = {
                'core': CORE_PATH,
                'onboarding': ONBOARDING_PATH,
                'localizable': LOCALIZABLE_PATH
            }
            catalog = sys.argv[2].lower()
            language = sys.argv[3]

            if catalog not in catalog_map:
                print("Invalid catalog. Use: core, onboarding, or localizable")
                sys.exit(1)

            find_untranslated(catalog_map[catalog], language)

        elif command == 'check-extraction':
            check_extraction_states()

        elif command == 'add-core-string':
            if len(sys.argv) < 3:
                print("Usage: add-core-string <key>")
                sys.exit(1)
            add_core_string(sys.argv[2])

        elif command == 'move-string':
            if len(sys.argv) < 5:
                print("Usage: move-string <key> <from-catalog> <to-catalog>")
                print("Catalogs: core, onboarding, localizable")
                sys.exit(1)
            move_string(sys.argv[2], sys.argv[3], sys.argv[4])

        else:
            print(f"Unknown command: {command}")
            print_usage()
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Error: Could not find file: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in catalog file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
