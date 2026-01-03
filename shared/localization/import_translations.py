#!/usr/bin/env python3
"""
Import translations into Localizable.xcstrings.
Takes a JSON file with translations and updates the xcstrings file.
"""

import json
import sys
from pathlib import Path

def import_translations(xcstrings_path, translations_json_path):
    """Import translations from JSON into xcstrings file."""

    # Load the xcstrings file
    with open(xcstrings_path, 'r', encoding='utf-8') as f:
        xcstrings = json.load(f)

    # Load translations
    with open(translations_json_path, 'r', encoding='utf-8') as f:
        translations = json.load(f)

    updates = 0
    additions = 0

    # Process each translation
    for item in translations:
        key = item['key']

        # Ensure the key exists in xcstrings
        if key not in xcstrings['strings']:
            xcstrings['strings'][key] = {}

        string_entry = xcstrings['strings'][key]

        # Ensure localizations object exists
        if 'localizations' not in string_entry:
            string_entry['localizations'] = {}

        # Add translations for each language
        for lang_code in ['ja', 'fr', 'es', 'zh-Hans']:
            if lang_code in item:
                translation = item[lang_code]

                if translation:  # Only add non-empty translations
                    string_entry['localizations'][lang_code] = {
                        'stringUnit': {
                            'state': 'translated',
                            'value': translation
                        }
                    }
                    updates += 1

    # Write back to file
    with open(xcstrings_path, 'w', encoding='utf-8') as f:
        json.dump(xcstrings, f, ensure_ascii=False, indent=2)

    print(f"✅ Updated {updates} translations in {xcstrings_path}")
    return updates

def main():
    if len(sys.argv) != 3:
        print("Usage: import_translations.py <xcstrings_file> <translations_json>")
        print("Example: import_translations.py Localizable.xcstrings translations.json")
        sys.exit(1)

    xcstrings_path = sys.argv[1]
    translations_json = sys.argv[2]

    if not Path(xcstrings_path).exists():
        print(f"Error: {xcstrings_path} not found")
        sys.exit(1)

    if not Path(translations_json).exists():
        print(f"Error: {translations_json} not found")
        sys.exit(1)

    import_translations(xcstrings_path, translations_json)

if __name__ == '__main__':
    main()
