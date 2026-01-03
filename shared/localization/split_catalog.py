#!/usr/bin/env python3
"""
Split Localizable.xcstrings into modular catalogs.
Creates Core.xcstrings and Onboarding.xcstrings.
"""

import json
import sys
from pathlib import Path

def create_catalog_structure(source_language="en"):
    """Create base structure for a string catalog."""
    return {
        "sourceLanguage": source_language,
        "strings": {},
        "version": "1.0"
    }

def split_catalog(input_path, output_dir):
    """Split catalog into Core, Onboarding, and main."""

    # Read source catalog
    with open(input_path, 'r', encoding='utf-8') as f:
        source = json.load(f)

    # Initialize new catalogs
    core_catalog = create_catalog_structure()
    onboarding_catalog = create_catalog_structure()
    main_catalog = create_catalog_structure()
    main_catalog['strings'] = source['strings'].copy()

    # Core string keys (common UI elements used everywhere)
    core_keys = [
        "Add", "Back", "Cancel", "Close", "Continue", "Delete", "Done",
        "Edit", "Home", "Library", "Next", "OK", "Practice", "Progress",
        "Remove", "Retry", "Save", "Settings", "Skip", "Yes", "No"
    ]

    # Onboarding keywords (identify by comment or key)
    onboarding_keywords = [
        "onboarding", "welcome", "profiling", "firstaction",
        "accountcreation", "getting started", "choose what you'd like"
    ]

    # Extract Core strings
    for key in core_keys:
        if key in source['strings']:
            core_catalog['strings'][key] = source['strings'][key]
            del main_catalog['strings'][key]

    # Extract Onboarding strings
    keys_to_remove = []
    for key, value in source['strings'].items():
        comment = value.get('comment', '').lower()
        key_lower = key.lower()

        # Check if it's onboarding-related
        if any(keyword in comment or keyword in key_lower for keyword in onboarding_keywords):
            onboarding_catalog['strings'][key] = value
            keys_to_remove.append(key)

    for key in keys_to_remove:
        if key in main_catalog['strings']:
            del main_catalog['strings'][key]

    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Write catalogs
    core_path = output_dir / "Core.xcstrings"
    onboarding_path = output_dir / "Onboarding.xcstrings"
    main_path = output_dir / "Localizable.xcstrings"

    with open(core_path, 'w', encoding='utf-8') as f:
        json.dump(core_catalog, f, ensure_ascii=False, indent=2)

    with open(onboarding_path, 'w', encoding='utf-8') as f:
        json.dump(onboarding_catalog, f, ensure_ascii=False, indent=2)

    with open(main_path, 'w', encoding='utf-8') as f:
        json.dump(main_catalog, f, ensure_ascii=False, indent=2)

    print(f"✅ Created Core.xcstrings: {len(core_catalog['strings'])} strings")
    print(f"✅ Created Onboarding.xcstrings: {len(onboarding_catalog['strings'])} strings")
    print(f"✅ Updated Localizable.xcstrings: {len(main_catalog['strings'])} strings")
    print(f"\nTotal: {len(core_catalog['strings']) + len(onboarding_catalog['strings']) + len(main_catalog['strings'])}")
    print(f"Original: {len(source['strings'])}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: split_catalog.py <input_xcstrings> <output_dir>")
        sys.exit(1)

    split_catalog(sys.argv[1], sys.argv[2])
