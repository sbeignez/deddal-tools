#!/bin/bash

# Localization Analysis Script
# Analyzes Localizable.xcstrings to generate coverage report

CATALOG_PATH="Deddal/App/Localizable.xcstrings"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "========================================="
echo "Deddal iOS - Localization Coverage Report"
echo "========================================="
echo ""

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo -e "${RED}Error: jq is not installed. Install with: brew install jq${NC}"
    exit 1
fi

# Check if catalog exists
if [ ! -f "$CATALOG_PATH" ]; then
    echo -e "${RED}Error: $CATALOG_PATH not found${NC}"
    exit 1
fi

# Total number of strings
TOTAL_STRINGS=$(jq '.strings | length' "$CATALOG_PATH")
echo -e "${BLUE}Total Strings:${NC} $TOTAL_STRINGS"
echo ""

# Supported languages
LANGUAGES=("ja" "fr" "es" "zh-Hans")
LANGUAGE_NAMES=("Japanese" "French" "Spanish" "Chinese Simplified")

echo "========================================="
echo "Coverage by Language"
echo "========================================="
echo ""

for i in "${!LANGUAGES[@]}"; do
    LANG="${LANGUAGES[$i]}"
    LANG_NAME="${LANGUAGE_NAMES[$i]}"

    # Count translated strings for this language
    TRANSLATED=$(jq --arg lang "$LANG" '
        .strings |
        to_entries |
        map(select(.value.localizations[$lang].stringUnit.state == "translated")) |
        length
    ' "$CATALOG_PATH")

    # Count new/untranslated strings
    NEW=$(jq --arg lang "$LANG" '
        .strings |
        to_entries |
        map(select(.value.localizations[$lang] == null or .value.localizations[$lang].stringUnit.state == "new")) |
        length
    ' "$CATALOG_PATH")

    # Count stale strings
    STALE=$(jq --arg lang "$LANG" '
        .strings |
        to_entries |
        map(select(.value.localizations[$lang].stringUnit.state == "stale")) |
        length
    ' "$CATALOG_PATH")

    # Calculate percentage
    if [ "$TOTAL_STRINGS" -gt 0 ]; then
        PERCENTAGE=$(awk "BEGIN {printf \"%.1f\", ($TRANSLATED / $TOTAL_STRINGS) * 100}")
    else
        PERCENTAGE="0.0"
    fi

    # Color based on coverage
    if (( $(echo "$PERCENTAGE >= 90" | bc -l) )); then
        COLOR=$GREEN
    elif (( $(echo "$PERCENTAGE >= 70" | bc -l) )); then
        COLOR=$YELLOW
    else
        COLOR=$RED
    fi

    echo -e "${COLOR}$LANG_NAME ($LANG):${NC}"
    echo "  Translated: $TRANSLATED / $TOTAL_STRINGS ($PERCENTAGE%)"
    echo "  New/Missing: $NEW"
    echo "  Stale: $STALE"
    echo ""
done

echo "========================================="
echo "Strings by State (English)"
echo "========================================="
echo ""

# Count strings without any localization
NO_LOCALIZATION=$(jq '
    .strings |
    to_entries |
    map(select(.value.localizations == null or .value.localizations | length == 0)) |
    length
' "$CATALOG_PATH")

echo "Strings with no localizations: $NO_LOCALIZATION"
echo ""

echo "========================================="
echo "Sample Untranslated Strings (First 10)"
echo "========================================="
echo ""

for LANG in "${LANGUAGES[@]}"; do
    echo -e "${YELLOW}$LANG:${NC}"
    jq -r --arg lang "$LANG" '
        .strings |
        to_entries |
        map(select(.value.localizations[$lang] == null or .value.localizations[$lang].stringUnit.state == "new")) |
        .[0:10] |
        .[] |
        "  - " + .key
    ' "$CATALOG_PATH"
    echo ""
done

echo "========================================="
echo "Recommendations"
echo "========================================="
echo ""

# Check if any language is below 100%
ALL_100=true
for LANG in "${LANGUAGES[@]}"; do
    TRANSLATED=$(jq --arg lang "$LANG" '
        .strings |
        to_entries |
        map(select(.value.localizations[$lang].stringUnit.state == "translated")) |
        length
    ' "$CATALOG_PATH")

    if [ "$TRANSLATED" -lt "$TOTAL_STRINGS" ]; then
        ALL_100=false
        break
    fi
done

if [ "$ALL_100" = true ]; then
    echo -e "${GREEN}✓ All languages have 100% coverage!${NC}"
else
    echo -e "${YELLOW}⚠ Translation work needed:${NC}"
    echo "  1. Review untranslated strings listed above"
    echo "  2. Add translations to Localizable.xcstrings"
    echo "  3. Mark all strings as 'state: translated'"
    echo "  4. Re-run this script to verify"
fi

echo ""
echo "========================================="
echo "Analysis Complete"
echo "========================================="
