#!/bin/bash

# Rename SVG files inside imageset folders to match Contents.json references

set -e

SUCCESS=0
ERRORS=0

echo "🔄 Renaming SVG files inside imageset folders..."
echo ""

# Find all imageset folders with new naming
find Deddal/App/Assets.xcassets -name "caseimg_*.imageset" -type d | while read -r imageset_dir; do
    contents_json="$imageset_dir/Contents.json"

    # Check if Contents.json exists
    if [ ! -f "$contents_json" ]; then
        echo "⚠️  No Contents.json in $imageset_dir"
        ((ERRORS++))
        continue
    fi

    # Get the expected SVG filename from Contents.json
    expected_svg=$(jq -r '.images[0].filename' "$contents_json")

    # Skip if no filename in Contents.json
    if [ "$expected_svg" = "null" ] || [ -z "$expected_svg" ]; then
        continue
    fi

    # Find the actual SVG file in the directory
    actual_svg=$(ls "$imageset_dir"/*.svg 2>/dev/null | head -1 | xargs -n 1 basename 2>/dev/null || echo "")

    if [ -z "$actual_svg" ]; then
        echo "⚠️  No SVG found in $imageset_dir"
        ((ERRORS++))
        continue
    fi

    # If names don't match, rename the file
    if [ "$actual_svg" != "$expected_svg" ]; then
        old_path="$imageset_dir/$actual_svg"
        new_path="$imageset_dir/$expected_svg"

        if git mv "$old_path" "$new_path" 2>/dev/null; then
            echo "✅ $(basename "$imageset_dir"): $actual_svg → $expected_svg"
            ((SUCCESS++))
        else
            echo "❌ Failed to rename: $old_path"
            ((ERRORS++))
        fi
    fi
done

echo ""
echo "════════════════════════════════════════"
echo "Imageset SVG Rename Summary:"
echo "  ✅ Success: $SUCCESS files"
echo "  ❌ Errors:  $ERRORS files"
echo "════════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo "✅ All imageset SVGs renamed successfully!"
    exit 0
else
    echo "⚠️  Completed with $ERRORS errors"
    exit 1
fi
