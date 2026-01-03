#!/bin/bash

# Upload case SVG images to Supabase Storage (Flat Structure)
# All images uploaded to bucket root with naming convention: {puzzle}_{method}_{caseset}_{case}.svg

set -e

# Supabase configuration
SUPABASE_URL="https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFvZ2xzeXlrZ3JxYWxzZW1pZ2lpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEyMzMyNTcsImV4cCI6MjA3NjgwOTI1N30.LBk9-Li5WTQsRkH4JmqMv9cnWbfnnQOdVdLl_yvJk0k"
BUCKET_NAME="case-images"
ASSETS_DIR="Deddal/App/Assets.xcassets"

# Counters
SUCCESS=0
ERRORS=0
TOTAL=0

# Function to upload single SVG from imageset
upload_imageset() {
    local imageset_dir="$1"
    local imageset_name=$(basename "$imageset_dir" .imageset)

    # Find SVG file in imageset directory
    local svg_file=$(find "$imageset_dir" -name "*.svg" -type f | head -1)

    if [[ -z "$svg_file" ]]; then
        echo "  ⚠️  No SVG found in $imageset_name"
        return 1
    fi

    # Upload directly to bucket root with imageset name
    local storage_path="${imageset_name}.svg"
    local url="${SUPABASE_URL}/storage/v1/object/${BUCKET_NAME}/${storage_path}"

    # Upload with upsert (overwrite if exists)
    local http_code=$(curl -s -w "%{http_code}" -o /dev/null \
        -X POST "$url" \
        -H "Authorization: Bearer ${SUPABASE_ANON_KEY}" \
        -H "Content-Type: image/svg+xml" \
        -H "x-upsert: true" \
        --data-binary "@${svg_file}")

    if [[ "$http_code" == "200" ]] || [[ "$http_code" == "201" ]]; then
        echo "  ✅ ${storage_path} (HTTP $http_code)"
        ((SUCCESS++))
        return 0
    else
        echo "  ❌ ${storage_path} (HTTP $http_code)"
        ((ERRORS++))
        return 1
    fi
}

echo "=== Uploading Case Images to Supabase Storage (Flat Structure) ==="
echo ""

# Find all imagesets containing SVG files
IMAGESETS=$(find "$ASSETS_DIR" -name "*.imageset" -type d | sort)
TOTAL=$(echo "$IMAGESETS" | wc -l | tr -d ' ')

echo "Found $TOTAL imagesets"
echo ""

# Upload by case set for organized output
echo "Uploading images:"
echo ""

# F2L (3x3 CFOP)
echo "3x3 CFOP F2L:"
while IFS= read -r imageset; do
    if [[ "$imageset" =~ 3x3_cfop_f2l ]]; then
        upload_imageset "$imageset"
    fi
done <<< "$IMAGESETS"

# OLL (3x3 CFOP)
echo ""
echo "3x3 CFOP OLL:"
while IFS= read -r imageset; do
    if [[ "$imageset" =~ 3x3_cfop_oll/ ]] && [[ ! "$imageset" =~ 3x3_cfop_oell ]]; then
        upload_imageset "$imageset"
    fi
done <<< "$IMAGESETS"

# PLL (3x3 CFOP)
echo ""
echo "3x3 CFOP PLL:"
while IFS= read -r imageset; do
    if [[ "$imageset" =~ 3x3_cfop_pll/ ]] && [[ ! "$imageset" =~ 3x3_cfop_pcll ]]; then
        upload_imageset "$imageset"
    fi
done <<< "$IMAGESETS"

# OeLL (3x3 CFOP Beginner)
echo ""
echo "3x3 CFOP OeLL (Beginner):"
while IFS= read -r imageset; do
    if [[ "$imageset" =~ 3x3_cfop_oell ]]; then
        upload_imageset "$imageset"
    fi
done <<< "$IMAGESETS"

# PcLL (3x3 CFOP Beginner)
echo ""
echo "3x3 CFOP PcLL (Beginner):"
while IFS= read -r imageset; do
    if [[ "$imageset" =~ 3x3_cfop_pcll ]]; then
        upload_imageset "$imageset"
    fi
done <<< "$IMAGESETS"

# Ortega OLL (2x2)
echo ""
echo "2x2 Ortega OLL:"
while IFS= read -r imageset; do
    if [[ "$imageset" =~ 2x2_ortega_oll ]]; then
        upload_imageset "$imageset"
    fi
done <<< "$IMAGESETS"

# Ortega PBL (2x2)
echo ""
echo "2x2 Ortega PBL:"
while IFS= read -r imageset; do
    if [[ "$imageset" =~ 2x2_ortega_pbl ]]; then
        upload_imageset "$imageset"
    fi
done <<< "$IMAGESETS"

# CLL (2x2)
echo ""
echo "2x2 CLL:"
while IFS= read -r imageset; do
    if [[ "$imageset" =~ 2x2_cll ]]; then
        upload_imageset "$imageset"
    fi
done <<< "$IMAGESETS"

# Error cases
echo ""
echo "Error cases:"
while IFS= read -r imageset; do
    if [[ "$imageset" =~ 3x3_error ]]; then
        upload_imageset "$imageset"
    fi
done <<< "$IMAGESETS"

echo ""
echo "=== Upload Summary ==="
echo "Total imagesets: $TOTAL"
echo "Successful uploads: $SUCCESS"
echo "Failed uploads: $ERRORS"
echo ""

if [[ $ERRORS -gt 0 ]]; then
    echo "⚠️  Some uploads failed. Check output above for details."
    exit 1
else
    echo "✅ All images uploaded successfully!"
    echo ""
    echo "Public URL format:"
    echo "  ${SUPABASE_URL}/storage/v1/object/public/${BUCKET_NAME}/{image_asset_name}.svg"
    echo ""
    echo "Example:"
    echo "  ${SUPABASE_URL}/storage/v1/object/public/${BUCKET_NAME}/3x3_cfop_f2l_1_fl.svg"
    exit 0
fi
