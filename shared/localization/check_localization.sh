#!/bin/bash

# Localization Checker for Deddal
# Finds hardcoded strings that should be localized

echo "🔍 Checking for hardcoded strings in Deddal..."
echo ""

# Find Text() with hardcoded strings (excluding variables and interpolation)
echo "📝 Text() with hardcoded strings:"
echo "=================================="
grep -rn --include="*.swift" 'Text("\([^$%@]\|[^"]*[a-zA-Z][^"]*\)")' Deddal/Views | \
  grep -v 'String(localized:' | \
  grep -v '//.*Text' | \
  grep -v 'Text("")' | \
  head -30
echo ""

# Count total occurrences
TOTAL_HARDCODED=$(grep -r --include="*.swift" 'Text("\([^$%@]\|[^"]*[a-zA-Z][^"]*\)")' Deddal/Views | \
  grep -v 'String(localized:' | \
  grep -v '//.*Text' | \
  grep -v 'Text("")' | \
  wc -l)

echo "📊 Statistics:"
echo "=============="
echo "Total hardcoded Text() strings: $TOTAL_HARDCODED"
echo ""

# Check for Button labels with hardcoded strings
echo "🔘 Button labels with hardcoded strings:"
echo "========================================="
grep -rn --include="*.swift" 'Button.*{' -A 2 Deddal/Views | \
  grep -E 'Text\("' | \
  grep -v 'String(localized:' | \
  head -15
echo ""

# Check for navigationTitle with hardcoded strings
echo "🧭 Navigation titles with hardcoded strings:"
echo "============================================="
grep -rn --include="*.swift" 'navigationTitle.*"' Deddal/Views | \
  grep -v 'String(localized:' | \
  head -10
echo ""

# Check translation state in Localizable.xcstrings
echo "🌍 Translation Status:"
echo "======================"
NEW_STRINGS=$(grep -c '"state" : "new"' Deddal/App/Localizable.xcstrings)
TOTAL_KEYS=$(grep -cE '^\s{4}"[^"]+"\s*:\s*\{$' Deddal/App/Localizable.xcstrings)

echo "Total string keys: $TOTAL_KEYS"
echo "Strings marked 'new': $NEW_STRINGS"
echo "Percentage untranslated: $(echo "scale=1; $NEW_STRINGS * 100 / ($TOTAL_KEYS * 5)" | bc)%"
echo ""

echo "✅ Check complete!"
echo ""
echo "💡 Recommendations:"
echo "  1. Wrap hardcoded strings with String(localized:)"
echo "  2. Add contextual comments for translators"
echo "  3. Review and mark translations as 'translated' in Xcode"
echo ""
