#!/bin/bash

# Populate null image_asset_name values in JSON seed data

set -e

echo "🔄 Populating null image_asset_name values in JSON seed data..."
echo ""

# Helper function to convert code to image_asset_name
code_to_image_name() {
    local code="$1"
    local cube_type="$2"  # "3x3" or "2x2"
    local method="$3"     # "cfop" or "ortega"

    # Convert code to lowercase and replace underscores/hyphens
    local identifier=$(echo "$code" | sed 's/^[^-]*-//' | tr '[:upper:]' '[:lower:]')

    echo "caseimg_${cube_type}_${method}_${identifier}"
}

# Update F2L null values (FR cases)
echo "📝 Updating F2L FR null values..."
jq 'map(
    if .code | test("-FR$") and (.image_asset_name == null) then
        .image_asset_name = ("caseimg_3x3_cfop_f2l_" + (.code | sub("^F2L-"; "") | sub("-FR$"; "-fr")))
    else
        .
    end
)' Deddal/Data/Resources/SeedData/f2l_cases.json > Deddal/Data/Resources/SeedData/f2l_cases.json.tmp
mv Deddal/Data/Resources/SeedData/f2l_cases.json.tmp Deddal/Data/Resources/SeedData/f2l_cases.json
echo "  ✅ F2L FR cases populated"
echo ""

# Update OLL null values
echo "📝 Updating OLL null values..."
jq 'map(
    if .image_asset_name == null then
        .image_asset_name = ("caseimg_3x3_cfop_oll_" + (.code | sub("^OLL-"; "")))
    else
        .
    end
)' Deddal/Data/Resources/SeedData/oll_cases.json > Deddal/Data/Resources/SeedData/oll_cases.json.tmp
mv Deddal/Data/Resources/SeedData/oll_cases.json.tmp Deddal/Data/Resources/SeedData/oll_cases.json
echo "  ✅ OLL cases populated"
echo ""

# Update PLL null values
echo "📝 Updating PLL null values..."
jq 'map(
    if .image_asset_name == null then
        .image_asset_name = ("caseimg_3x3_cfop_pll_" + (.code | sub("^PLL-"; "") | ascii_downcase))
    else
        .
    end
)' Deddal/Data/Resources/SeedData/pll_cases.json > Deddal/Data/Resources/SeedData/pll_cases.json.tmp
mv Deddal/Data/Resources/SeedData/pll_cases.json.tmp Deddal/Data/Resources/SeedData/pll_cases.json
echo "  ✅ PLL cases populated"
echo ""

echo "════════════════════════════════════════"
echo "✅ All null image_asset_name values populated!"
echo "════════════════════════════════════════"

# Verify counts
echo ""
echo "Verification:"
echo "  F2L nulls: $(jq '[.[] | select(.image_asset_name == null)] | length' Deddal/Data/Resources/SeedData/f2l_cases.json)"
echo "  OLL nulls: $(jq '[.[] | select(.image_asset_name == null)] | length' Deddal/Data/Resources/SeedData/oll_cases.json)"
echo "  PLL nulls: $(jq '[.[] | select(.image_asset_name == null)] | length' Deddal/Data/Resources/SeedData/pll_cases.json)"
