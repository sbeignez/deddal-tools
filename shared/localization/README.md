# tools/shared/localization - Translation Management

Scripts for managing app localization across 5 languages: English (source), French, Spanish, Japanese, and Chinese (Simplified).

## Overview

This folder contains 11 files for the complete localization workflow:
- 8 Python/Bash scripts for translation automation
- 2 JSON files with translation data

## Folder Structure

```
tools/shared/localization/
├── translations/              # Translation JSON data
│   ├── ComprehensiveTranslations.json
│   └── NewStringsTranslations.json
└── (8 scripts)                # Automation scripts
```

## Scripts

### auto_translate.py

Automatically translate strings using translation APIs.

**Usage:**
```bash
python3 auto_translate.py --source en --target fr
```

**Features:**
- Batch translation processing
- API integration (Google Translate, DeepL)
- Context-aware translation
- Quality validation

**When to use:**
- Adding new language support
- Bulk translation of new strings
- Initial translation pass (always review manually)

### extract_untranslated.py

Extract strings that are missing translations in target languages.

**Usage:**
```bash
python3 extract_untranslated.py --locale fr
```

**Output:**
- JSON file with missing translations
- Report of translation coverage percentage
- List of keys needing translation

**When to use:**
- Before starting translation work
- Checking translation completeness
- Preparing work for translators

### import_translations.py

Import translated strings into String Catalogs (.xcstrings files).

**Usage:**
```bash
python3 import_translations.py --input translations.json --catalog Localizable.xcstrings
```

**Features:**
- Validates translation format
- Updates String Catalogs
- Preserves existing translations
- Reports conflicts

**When to use:**
- After receiving translations from translators
- Importing bulk translation updates
- Syncing translation JSON to String Catalogs

### localization_helper.py

Helper utilities for localization tasks.

**Usage:**
```bash
python3 localization_helper.py --command validate --catalog Core.xcstrings
```

**Functions:**
- Validate String Catalog format
- Count strings per locale
- Find duplicate keys
- Check for missing comments

**When to use:**
- Quality checking String Catalogs
- Debugging localization issues
- Preparing translation reports

### split_catalog.py

Split a large String Catalog into modular catalogs (Core, Onboarding, Localizable).

**Usage:**
```bash
python3 split_catalog.py --input Localizable.xcstrings --output-dir ./split
```

**Features:**
- Modular catalog organization
- Preserves translation state
- Maintains metadata

**When to use:**
- Reorganizing localization structure
- Creating new modular catalogs
- Refactoring large catalogs

**Note:** Deddal iOS already uses 3 modular catalogs:
- `Core.xcstrings` (12 strings) - Universal UI actions
- `Onboarding.xcstrings` (45 strings) - First-time user experience
- `Localizable.xcstrings` (535 strings) - Main application

### analyze_localization.sh

Analyze localization coverage and completeness across all languages.

**Usage:**
```bash
./analyze_localization.sh
```

**Output:**
- Translation coverage percentages per language
- List of missing translations
- Catalog size statistics
- Quality metrics

**When to use:**
- Before releases to check completeness
- Monitoring translation progress
- Identifying localization gaps

### check_localization.sh

Check for common localization issues and errors.

**Usage:**
```bash
./check_localization.sh
```

**Checks:**
- Missing translation keys
- Invalid String Catalog format
- Placeholder mismatches (%d, %s, etc.)
- Untranslated strings in code

**When to use:**
- Before committing localization changes
- CI/CD pipeline validation
- Pre-release quality checks

### create_locale_folders.sh

Create locale folder structure for Fastlane metadata.

**Usage:**
```bash
./create_locale_folders.sh
```

**Creates:**
```
tools/ios/fastlane/metadata/
├── en-US/
├── fr-FR/
├── es-ES/
├── ja/
└── zh-Hans/
```

**When to use:**
- Setting up App Store localization
- Adding new language support
- Organizing Fastlane metadata

## Translation Data Files

### translations/ComprehensiveTranslations.json

Complete translation dataset for all supported languages.

**Structure:**
```json
{
  "string_key": {
    "en": "English text",
    "fr": "French text",
    "es": "Spanish text",
    "ja": "Japanese text",
    "zh-Hans": "Chinese text"
  }
}
```

**When to use:**
- Source of truth for translations
- Bulk import to String Catalogs
- Translation memory reference

### translations/NewStringsTranslations.json

New strings pending translation.

**Structure:**
```json
{
  "new_string_key": {
    "en": "English text",
    "fr": "",  // Needs translation
    "es": "",
    "ja": "",
    "zh-Hans": ""
  }
}
```

**When to use:**
- Tracking new strings added to app
- Preparing work for translators
- Incremental translation updates

## Common Workflows

### Adding New Strings

1. **Extract** untranslated strings:
   ```bash
   python3 extract_untranslated.py --all-locales
   ```

2. **Auto-translate** (initial pass):
   ```bash
   python3 auto_translate.py --batch
   ```

3. **Review** translations manually

4. **Import** to String Catalogs:
   ```bash
   python3 import_translations.py --input NewStringsTranslations.json
   ```

### Adding New Language

1. **Create** locale folders:
   ```bash
   ./create_locale_folders.sh
   ```

2. **Extract** all strings:
   ```bash
   python3 extract_untranslated.py --locale NEW_LOCALE
   ```

3. **Translate** strings (manual or API)

4. **Import** translations:
   ```bash
   python3 import_translations.py --locale NEW_LOCALE
   ```

5. **Validate**:
   ```bash
   ./check_localization.sh
   ```

### Pre-Release Checks

1. **Analyze** coverage:
   ```bash
   ./analyze_localization.sh
   ```

2. **Check** for issues:
   ```bash
   ./check_localization.sh
   ```

3. **Validate** String Catalogs:
   ```bash
   python3 localization_helper.py --command validate --all
   ```

## Supported Languages

| Language | Locale Code | String Catalog Support |
|----------|-------------|------------------------|
| English | en | ✅ Source language |
| French | fr | ✅ Full support |
| Spanish | es | ✅ Full support |
| Japanese | ja | ✅ Full support |
| Chinese (Simplified) | zh-Hans | ✅ Full support |

## String Catalog Files

Located in `Deddal/App/Localization/`:
- **Core.xcstrings** (12 strings) - Universal UI actions (Back, Cancel, Done, Save, etc.)
- **Onboarding.xcstrings** (45 strings) - First-time user experience
- **Localizable.xcstrings** (535 strings) - Main application strings

**Important:** String Catalogs are auto-discovered by Xcode. Don't add them to targets manually.

## Dependencies

**Python scripts require:**
- Python 3.8+
- Translation API SDKs (optional, for auto_translate.py)
  - Google Cloud Translate
  - DeepL API

Install dependencies:
```bash
pip3 install google-cloud-translate deepl
```

**Environment variables:**
```bash
export GOOGLE_TRANSLATE_API_KEY="your-key"
export DEEPL_API_KEY="your-key"
```

## Related Documentation

- Main localization guide: `/LOCALIZATION.md`
- String Catalogs: `Deddal/App/Localization/`
- Fastlane metadata: `tools/ios/fastlane/metadata/`
- Project documentation: `/CLAUDE.md`

## Best Practices

### Translation Quality

1. **Always review** automated translations
2. **Provide context** in String Catalog comments
3. **Use placeholders** correctly (%d, %s, %@)
4. **Test UI** in all languages (layout, truncation)
5. **Respect cultural norms** (dates, numbers, currency)

### String Catalog Usage

1. **Use string literals** in SwiftUI for automatic localization:
   ```swift
   Text("Key")  // ✅ Updates when language changes
   ```

2. **Avoid String(localized:)** in SwiftUI views:
   ```swift
   Text(String(localized: "Key"))  // ❌ Won't update dynamically
   ```

3. **Return LocalizedStringKey** from enums:
   ```swift
   enum SkillLevel {
       case beginner
       var displayName: LocalizedStringKey { "Beginner" }
   }
   ```

### Translation Workflow

1. **Extract** → 2. **Translate** → 3. **Review** → 4. **Import** → 5. **Test**

Always run quality checks before committing localization changes.

## Troubleshooting

**Missing translations:**
- Run `extract_untranslated.py` to identify gaps
- Check String Catalog state in Xcode
- Verify locale codes are correct

**Import failures:**
- Validate JSON format
- Check for duplicate keys
- Ensure String Catalog is not corrupted
- Review import script logs

**Language not showing in app:**
- Check Xcode project localization settings
- Verify String Catalog includes locale
- Rebuild app after adding translations
- Check device/simulator language settings

**Auto-translation issues:**
- Verify API keys are set
- Check API quotas/limits
- Review API error messages
- Fall back to manual translation if needed

Generated by Trophee Ltd
