#!/usr/bin/env python3
"""
Remove emojis from description.txt and release_notes.txt files.
App Store Connect doesn't allow emojis in these fields.
"""

import re
from pathlib import Path

def remove_emojis(text):
    """Remove all emojis from text using regex patterns."""
    # Pattern to match emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub('', text)

def main():
    metadata_dir = Path(__file__).parent
    updated_count = 0

    # Find all description.txt and release_notes.txt files
    for locale_dir in metadata_dir.iterdir():
        if not locale_dir.is_dir():
            continue

        for filename in ['description.txt', 'release_notes.txt']:
            file_path = locale_dir / filename

            if not file_path.exists():
                continue

            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                original = f.read()

            # Remove emojis
            cleaned = remove_emojis(original)

            # Skip if no changes
            if original == cleaned:
                continue

            # Write cleaned version
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned)

            updated_count += 1
            print(f"✅ Removed emojis from {locale_dir.name}/{filename}")

    print(f"\n🎉 Complete: {updated_count} files updated")
    print("✅ All emojis removed from descriptions and release notes")
    print("✅ Files are now App Store Connect compatible")

if __name__ == "__main__":
    main()
