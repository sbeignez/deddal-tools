#!/bin/bash

# Deddal iOS - Create All App Store Locale Folders
# Creates metadata folder structure for 25+ App Store languages
# Date: 2025-11-03

set -e

METADATA_DIR="/Users/trophee-mini/Code/deddal/deddal-ios/tool-fastlane/metadata"
cd "$METADATA_DIR"

echo "🌍 Creating App Store Locale Folders for Deddal iOS"
echo "=================================================="
echo ""

# Required files for each locale
FILES=(
    "name.txt"
    "subtitle.txt"
    "description.txt"
    "keywords.txt"
    "promotional_text.txt"
    "release_notes.txt"
    "privacy_url.txt"
    "marketing_url.txt"
    "support_url.txt"
)

# PRIORITY 1: Top 10 Languages (MUST HAVE)
PRIORITY1=(
    "en-GB:English (UK):172 countries"
    "es-MX:Spanish (Mexico):19 countries (LATAM)"
    "pt-BR:Portuguese (Brazil):Brazil + diaspora"
    "de-DE:German (Germany):Germany, Austria, Switzerland"
    "zh-Hant:Chinese (Traditional):Taiwan, Hong Kong, Macau"
    "ko:Korean:South Korea"
)

# PRIORITY 2: Next 10 Languages (SHOULD HAVE)
PRIORITY2=(
    "it:Italian:Italy, Switzerland, San Marino"
    "nl-NL:Dutch:Netherlands, Belgium"
    "ru:Russian:Russia, CIS countries"
    "pl:Polish:Poland"
    "tr:Turkish:Turkey"
    "id:Indonesian:Indonesia"
    "th:Thai:Thailand"
    "vi:Vietnamese:Vietnam"
    "ar:Arabic:17 countries"
)

# PRIORITY 3: Regional & Niche (NICE TO HAVE)
PRIORITY3=(
    "sv:Swedish:Sweden"
    "no:Norwegian:Norway"
    "da:Danish:Denmark"
    "fi:Finnish:Finland"
    "cs:Czech:Czech Republic"
    "ro:Romanian:Romania"
    "uk:Ukrainian:Ukraine"
    "el:Greek:Greece, Cyprus"
    "he:Hebrew:Israel"
    "ms:Malay:Malaysia, Singapore"
    "ca:Catalan:Catalonia"
    "hr:Croatian:Croatia"
    "hu:Hungarian:Hungary"
    "sk:Slovak:Slovakia"
    "en-AU:English (Australia):Australia, NZ"
    "en-CA:English (Canada):Canada"
    "fr-CA:French (Canada):Quebec"
    "pt-PT:Portuguese (Portugal):Portugal"
)

# Function to create locale folder
create_locale() {
    local locale_code=$1
    local locale_name=$2
    local locale_reach=$3

    if [ -d "$locale_code" ]; then
        echo "⏭️  $locale_code ($locale_name) - Already exists, skipping"
        return
    fi

    echo "📁 Creating $locale_code ($locale_name) - $locale_reach"
    mkdir -p "$locale_code"

    # Create all required files
    for file in "${FILES[@]}"; do
        touch "$locale_code/$file"
    done

    # Add placeholder content to help translators
    echo "Deddal" > "$locale_code/name.txt"
    echo "CFOP Training" > "$locale_code/subtitle.txt"
    echo "[TODO: Translate description for $locale_name]" > "$locale_code/description.txt"
    echo "[TODO: Research keywords for $locale_name]" > "$locale_code/keywords.txt"
    echo "[TODO: Translate promotional text for $locale_name]" > "$locale_code/promotional_text.txt"
    echo "[TODO: Translate release notes for $locale_name]" > "$locale_code/release_notes.txt"
    echo "https://deddal.app/privacy" > "$locale_code/privacy_url.txt"
    echo "https://deddal.app" > "$locale_code/marketing_url.txt"
    echo "https://deddal.app/support" > "$locale_code/support_url.txt"

    echo "   ✅ Created $locale_code with placeholder content"
    echo ""
}

# PHASE 1A: Priority 1 Languages
echo "🔴 PHASE 1A: Creating Priority 1 Languages (Top 10)"
echo "===================================================="
echo ""

for locale in "${PRIORITY1[@]}"; do
    IFS=: read -r code name reach <<< "$locale"
    create_locale "$code" "$name" "$reach"
done

# PHASE 1B: Priority 2 Languages
echo ""
echo "🟡 PHASE 1B: Creating Priority 2 Languages (Next 10)"
echo "====================================================="
echo ""

for locale in "${PRIORITY2[@]}"; do
    IFS=: read -r code name reach <<< "$locale"
    create_locale "$code" "$name" "$reach"
done

# PHASE 2: Priority 3 Languages
echo ""
echo "🟢 PHASE 2: Creating Priority 3 Languages (Nice to Have)"
echo "=========================================================="
echo ""

for locale in "${PRIORITY3[@]}"; do
    IFS=: read -r code name reach <<< "$locale"
    create_locale "$code" "$name" "$reach"
done

# Summary
echo ""
echo "✅ Locale Folder Creation Complete!"
echo "===================================="
echo ""
echo "📊 Summary:"
echo "   - Priority 1: 6 new languages (en-GB, es-MX, pt-BR, de-DE, zh-Hant, ko)"
echo "   - Priority 2: 9 languages (it, nl-NL, ru, pl, tr, id, th, vi, ar)"
echo "   - Priority 3: 18 languages (Scandinavian, Eastern Europe, regional variants)"
echo "   - Existing: 5 languages (en-US, fr-FR, es-ES, ja, zh-Hans)"
echo ""
echo "📁 Total: 38 locale folders"
echo ""
echo "🔍 Existing locales:"
ls -1 "$METADATA_DIR" | grep -E '^[a-z]{2}(-[A-Z]{2})?$' || true
echo ""
echo "📋 Next Steps:"
echo "   1. Review AI_LOCALIZATION_STRATEGY.md for prioritization"
echo "   2. Adapt en-GB, es-MX from existing (free, 2-4 hours)"
echo "   3. Hire professional translators for pt-BR, de-DE, zh-Hant, ko (\$2,000)"
echo "   4. Generate screenshots: bundle exec fastlane screenshots_prod"
echo "   5. Upload: bundle exec fastlane upload_all"
echo ""
echo "💡 Translation Status: All folders created with [TODO] placeholders"
echo "   Replace placeholders with actual translations before uploading!"
echo ""
