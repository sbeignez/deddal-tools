#!/bin/bash
# inventory_tests.sh
# Analyze each test file and categorize it based on imports

set -e

echo "🔍 Analyzing test files in DeddalTests..."
echo ""
echo "File,Imports,Category,Suggested Target"
echo "---"

total=0
domain=0
application=0
adapter=0
ui=0
legacy=0
unknown=0

for file in $(find DeddalTests -name "*Tests.swift" -o -name "*Test.swift"); do
  # Skip hidden files
  if [[ $(basename "$file") == .* ]]; then
    continue
  fi

  total=$((total + 1))

  # Get all imports on single line
  imports=$(grep "^import " "$file" 2>/dev/null | awk '{print $2}' | tr '\n' ';' | sed 's/;$//')

  # Categorize based on imports and patterns
  category="Unknown"
  target="TBD"

  # Check for UI frameworks
  if echo "$imports" | grep -q "SwiftUI\|UIKit"; then
    category="UI"
    target="DeddalTests (keep)"
    ui=$((ui + 1))

  # Check for adapter frameworks (SwiftData, StoreKit, etc.)
  elif echo "$imports" | grep -q "SwiftData\|StoreKit"; then
    category="Adapter"
    target="DeddalInfraTests"
    adapter=$((adapter + 1))

  # Check if it imports DeddalInfra (likely adapter test)
  elif echo "$imports" | grep -q "DeddalInfra"; then
    category="Adapter"
    target="DeddalInfraTests"
    adapter=$((adapter + 1))

  # Check if it imports DeddalApplication (use case tests)
  elif echo "$imports" | grep -q "DeddalApplication"; then
    category="Application"
    target="DeddalCore/ApplicationTests"
    application=$((application + 1))

  # Check if it imports only DeddalDomain (pure domain)
  elif echo "$imports" | grep -q "DeddalDomain" && ! echo "$imports" | grep -q "DeddalApplication\|@testable.*Deddal"; then
    category="Domain"
    target="DeddalCore/DomainTests"
    domain=$((domain + 1))

  # Check if it's a legacy test (imports main Deddal without modern layers)
  elif echo "$imports" | grep -q "@testable.*Deddal" && ! echo "$imports" | grep -q "DeddalDomain\|DeddalApplication\|DeddalInfra"; then
    # Could be UI or Legacy - check for E2E or Game patterns
    if echo "$file" | grep -q "E2E\|Game\|ViewModel\|Coordinator"; then
      category="UI"
      target="DeddalTests (keep)"
      ui=$((ui + 1))
    else
      category="Legacy"
      target="DeddalTests/Legacy or refactor"
      legacy=$((legacy + 1))
    fi

  else
    category="Unknown"
    target="Manual review needed"
    unknown=$((unknown + 1))
  fi

  # Clean file path
  clean_file=$(echo "$file" | sed 's|^DeddalTests/||')

  echo "$clean_file,$imports,$category,$target"
done

echo ""
echo "---"
echo "📊 Summary:"
echo "  Total files: $total"
echo "  Domain: $domain"
echo "  Application: $application"
echo "  Adapter: $adapter"
echo "  UI: $ui"
echo "  Legacy: $legacy"
echo "  Unknown: $unknown"
echo ""
echo "✅ Inventory complete. Review and update TEST_MIGRATION_INVENTORY.md"
