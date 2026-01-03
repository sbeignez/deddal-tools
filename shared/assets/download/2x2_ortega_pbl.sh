#!/bin/bash

# Generate 2x2 Ortega PBL case images using VisualCube API
# PBL = Permute Both Layers (5 cases for 2x2 cube)
#
# RUN:
# cd Ressources/Cases-Ortega-PBL
# bash Download-Ortega-PBL-Cases.sh

# Define the base URL for downloading 2x2 PBL images
# Key differences from 3x3:
# - pzl=2 parameter for 2x2 cube
# - No view=plan (need 3D view to show both layers' permutation)
# - No stage parameter (PBL is 2x2-specific)
base_url="https://visualcube.api.cubing.net/visualcube.php?pzl=2&fmt=svg&size=300&"

# Function to URL-encode a string
urlencode() {
  local string="${1}"
  local length="${#string}"
  local encoded=""
  local pos c
  for (( pos=0 ; pos<length ; pos++ )); do
    c="${string:$pos:1}"
    case "$c" in
      [a-zA-Z0-9.~_-]) encoded+="$c" ;;
      "'") encoded+="%27" ;;  # Properly encode single quotes
      *) encoded+=$(printf '%%%02X' "'$c") ;;
    esac
  done
  echo "$encoded"
}

# Ortega PBL Cases (2x2 cube)
# Format: "filename;scramble"
# Scrambles from: Deddal/Data/Resources/SeedData/2x2_ortega_pbl_cases.json
pbl_cases=()
pbl_cases+=("2x2_ortega_pbl_1;R U F2 R' U' R")                     # Adjacent / Adj
pbl_cases+=("2x2_ortega_pbl_2;F2 U' R' U R U F2 U R U' R'")        # Opposite / Opp
pbl_cases+=("2x2_ortega_pbl_3;R2 F2 R2")                            # Diagonal / Opp Opp
pbl_cases+=("2x2_ortega_pbl_4;R2 U R2 U2 B2 U' R2")                # Adj-Adj
pbl_cases+=("2x2_ortega_pbl_5;R U F2 R' U' R")                     # Adj-Opp (same as PBL-1)

# Rotation angle for 3D view
# Testing y45x-35 to better show both layers
# May need adjustment after seeing results
rParam="y45x-35"

echo "=== Generating 2x2 Ortega PBL Case Images ==="
echo ""

# Loop through cases
for case_info in "${pbl_cases[@]}"; do
  IFS=";" read -r case_name scramble <<< "$case_info"

  # URL encode scramble
  encoded=$(urlencode "$scramble")

  # Construct URL (no stage parameter for PBL)
  image_url="${base_url}r=${rParam}&case=${encoded}"

  echo "Downloading ${case_name}.svg"
  echo "  Scramble: ${scramble}"
  echo "  URL: ${image_url}"

  # Use curl to download
  curl -L -s -o "${case_name}.svg" "$image_url"

  # Remove white background (make transparent)
  if [ -f "${case_name}.svg" ]; then
    sed -i '' "s/<rect fill='#FFFFFF'/<rect fill='none'/g" "${case_name}.svg"
    echo "  ✅ Generated ${case_name}.svg"
  else
    echo "  ❌ Failed to download ${case_name}.svg"
  fi
  echo ""
done

echo "=== Summary ==="
svg_count=$(ls -1 2x2_ortega_pbl_*.svg 2>/dev/null | wc -l | tr -d ' ')
echo "Generated ${svg_count}/5 PBL case images"
echo ""

if [ "$svg_count" -eq 5 ]; then
  echo "✅ All PBL images generated successfully!"
  echo ""
  echo "Next steps:"
  echo "1. Review images to verify they display correctly"
  echo "2. Add images to Xcode: Deddal/App/Assets.xcassets/Ortega-PBL/"
  echo "3. Build and test app to verify images appear in Library View"
else
  echo "⚠️  Some images failed to generate. Check output above for errors."
fi
echo ""
