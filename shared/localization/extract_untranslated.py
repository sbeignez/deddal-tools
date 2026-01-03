#!/usr/bin/env python3
"""
Extract untranslated strings from Localizable.xcstrings for AI translation.
Outputs JSON format with string keys, English source, and comments for context.
"""

import json
import sys

def extract_untranslated(xcstrings_path, target_language):
    """Extract strings missing translations for a specific language."""

    with open(xcstrings_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    untranslated = []

    for key, value in data['strings'].items():
        # Check if translation is missing or marked as "new"
        localizations = value.get('localizations', {})
        target_loc = localizations.get(target_language)

        needs_translation = (
            target_loc is None or
            target_loc.get('stringUnit', {}).get('state') == 'new'
        )

        if needs_translation:
            # Extract comment for context
            comment = value.get('comment', '')

            untranslated.append({
                'key': key,
                'source': key,  # English source text
                'comment': comment,
                'hasComment': bool(comment)
            })

    return untranslated

def main():
    if len(sys.argv) != 3:
        print("Usage: extract_untranslated.py <xcstrings_file> <language_code>")
        print("Example: extract_untranslated.py Localizable.xcstrings ja")
        sys.exit(1)

    xcstrings_path = sys.argv[1]
    language = sys.argv[2]

    untranslated = extract_untranslated(xcstrings_path, language)

    print(f"# Untranslated strings for {language}: {len(untranslated)}")
    print(f"# Strings with comments: {sum(1 for s in untranslated if s['hasComment'])}")
    print(f"# Strings without comments: {sum(1 for s in untranslated if not s['hasComment'])}")
    print()

    # Output as JSON
    print(json.dumps(untranslated, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
