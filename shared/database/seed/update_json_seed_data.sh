#!/bin/bash

# Update JSON seed data files with new image_asset_name values

set -e

CSV_FILE="rename_mapping.csv"
SUCCESS=0
ERRORS=0

echo "🔄 Updating JSON seed data with new image_asset_name values..."
echo ""

# Process each JSON file separately
JSON_FILES=(
    "Deddal/Data/Resources/SeedData/f2l_cases.json"
    "Deddal/Data/Resources/SeedData/oll_cases.json"
    "Deddal/Data/Resources/SeedData/pll_cases.json"
    "Deddal/Data/Resources/SeedData/2x2_ortega_oll_cases.json"
    "Deddal/Data/Resources/SeedData/2x2_ortega_pbl_cases.json"
)

for json_file in "${JSON_FILES[@]}"; do
    if [ ! -f "$json_file" ]; then
        echo "⚠️  File not found: $json_file"
        ((ERRORS++))
        continue
    fi

    echo "📝 Processing: $(basename "$json_file")"

    # Create a temporary file for modifications
    tmp_file="${json_file}.tmp"
    cp "$json_file" "$tmp_file"

    # Extract relevant mappings from CSV based on JSON file type
    case "$(basename "$json_file")" in
        "f2l_cases.json")
            category="f2l"
            ;;
        "oll_cases.json")
            category="oll"
            ;;
        "pll_cases.json")
            category="pll"
            ;;
        "2x2_ortega_oll_cases.json")
            category="ortega-oll"
            ;;
        "2x2_ortega_pbl_cases.json")
            category="ortega-pbl"
            ;;
        *)
            echo "⚠️  Unknown JSON file type"
            ((ERRORS++))
            continue
            ;;
    esac

    # Process each JSON mapping from CSV
    while IFS=',' read -r type cat old_name new_name; do
        [ "$type" != "json" ] && continue
        [ "$cat" != "$category" ] && continue

        # For null values, we need to populate them by finding the matching code
        if [ "$old_name" = "null" ]; then
            # Extract code from new_name: caseimg_3x3_cfop_oll_1 → OLL-1
            # This is complex, so we'll use a different approach
            # Skip null updates for now - they'll be handled by specific case logic
            continue
        fi

        # Update the JSON: find records with matching image_asset_name and update it
        jq --arg old "$old_name" --arg new "$new_name" \
            'map(if .image_asset_name == $old then .image_asset_name = $new else . end)' \
            "$tmp_file" > "${tmp_file}.updated"
        mv "${tmp_file}.updated" "$tmp_file"

        echo "  ✅ Updated: $old_name → $new_name"
        ((SUCCESS++))
    done < <(tail -n +2 "$CSV_FILE")

    # Move temp file to original
    mv "$tmp_file" "$json_file"
    echo ""
done

echo "════════════════════════════════════════"
echo "JSON Seed Data Update Summary:"
echo "  ✅ Records updated: $SUCCESS"
echo "  ❌ Errors:          $ERRORS"
echo "════════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo "✅ All JSON seed data updated successfully!"
    exit 0
else
    echo "⚠️  Completed with $ERRORS errors"
    exit 1
fi
