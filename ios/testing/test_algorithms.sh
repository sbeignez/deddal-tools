#!/bin/bash
# Test expensive algorithm validation tests
# These tests verify that all F2L/OLL/PLL algorithms correctly transform cube states

set -e  # Exit on error

echo "🧪 Running Algorithm Validation Tests..."
echo "⚠️  This will test ~300-500 algorithm transformations (may take several minutes)"
echo ""

# Navigate to project directory
cd "$(dirname "$0")/.."

# Run CaseAlgsTests
echo "Running CaseAlgsTests..."
xcodebuild test \
  -project Deddal.xcodeproj \
  -scheme "1. DEV Scheme" \
  -only-testing:DeddalTests/CaseAlgsTests \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro' \
  2>&1 | grep -E "(Test Suite|Test Case|passed|failed|✔|✘)" | tail -50

echo ""
echo "✅ Algorithm validation complete!"
