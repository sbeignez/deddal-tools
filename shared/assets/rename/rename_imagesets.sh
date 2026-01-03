#!/bin/bash

# Rename all imageset folders and update Contents.json files
# Uses git mv to preserve file history

set -e  # Exit on error

CSV_FILE="rename_mapping.csv"
IMAGESET_SUCCESS=0
IMAGESET_ERRORS=0
JSON_SUCCESS=0
JSON_ERRORS=0

echo "🔄 Renaming imageset folders and updating Contents.json files..."
echo ""

# Process only imageset entries from CSV (skip header)
while IFS=',' read -r type category old_name new_name; do
    [ "$type" != "imageset" ] && continue

    # Determine asset catalog directory based on category
    case "$category" in
        "f2l")
            asset_dir="Deddal/App/Assets.xcassets/F2L"
            ;;
        "oll")
            asset_dir="Deddal/App/Assets.xcassets/OLL"
            ;;
        "oell")
            asset_dir="Deddal/App/Assets.xcassets/OeLL"
            ;;
        "pll")
            asset_dir="Deddal/App/Assets.xcassets/PLL"
            ;;
        "pcll")
            asset_dir="Deddal/App/Assets.xcassets/PLL"
            ;;
        "ortega-oll")
            asset_dir="Deddal/App/Assets.xcassets/Ortega-OLL"
            ;;
        "ortega-pbl")
            asset_dir="Deddal/App/Assets.xcassets/Ortega-PBL"
            ;;
        *)
            echo "⚠️  Unknown category: $category for $old_name"
            ((IMAGESET_ERRORS++))
            continue
            ;;
    esac

    old_path="$asset_dir/$old_name"
    new_path="$asset_dir/$new_name"

    # Check if source folder exists
    if [ ! -d "$old_path" ]; then
        echo "⚠️  Folder not found: $old_path"
        ((IMAGESET_ERRORS++))
        continue
    fi

    # Update Contents.json before renaming folder
    contents_json="$old_path/Contents.json"
    if [ -f "$contents_json" ]; then
        # Extract old SVG filename from current Contents.json
        old_svg=$(jq -r '.images[0].filename' "$contents_json")

        if [ "$old_svg" != "null" ] && [ -n "$old_svg" ]; then
            # Calculate new SVG filename (remove caseimg_ prefix, add path suffix)
            # Old imageset: caseimg_F2L-1-FL.imageset → new SVG should be 3x3_cfop_f2l_1-fl.svg
            new_svg=$(echo "$new_name" | sed 's/^caseimg_//' | sed 's/\.imageset$/\.svg/')

            # Update Contents.json with new filename
            jq ".images[0].filename = \"$new_svg\"" "$contents_json" > "${contents_json}.tmp"
            mv "${contents_json}.tmp" "$contents_json"
            echo "  📝 Updated Contents.json: $old_svg → $new_svg"
            ((JSON_SUCCESS++))
        else
            echo "  ⚠️  No filename found in Contents.json for $old_name"
            ((JSON_ERRORS++))
        fi
    else
        echo "  ⚠️  Contents.json not found in $old_path"
        ((JSON_ERRORS++))
    fi

    # Rename the imageset folder using git mv
    if git mv "$old_path" "$new_path" 2>/dev/null; then
        echo "✅ $category: $old_name → $new_name"
        ((IMAGESET_SUCCESS++))
    else
        echo "❌ Failed to rename: $old_path"
        ((IMAGESET_ERRORS++))
    fi

    echo ""
done < <(tail -n +2 "$CSV_FILE")

echo "════════════════════════════════════════"
echo "Imageset Rename Summary:"
echo "  ✅ Folders renamed:  $IMAGESET_SUCCESS"
echo "  📝 Contents.json updated: $JSON_SUCCESS"
echo "  ❌ Folder errors:   $IMAGESET_ERRORS"
echo "  ⚠️  JSON errors:     $JSON_ERRORS"
echo "════════════════════════════════════════"

total_errors=$((IMAGESET_ERRORS + JSON_ERRORS))

if [ $total_errors -eq 0 ]; then
    echo "✅ All imagesets renamed and Contents.json updated successfully!"
    exit 0
else
    echo "⚠️  Completed with $total_errors total errors"
    exit 1
fi
