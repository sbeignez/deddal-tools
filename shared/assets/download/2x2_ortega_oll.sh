#!/bin/bash

# Generate 2x2 Ortega OLL case images using VisualCube API
# OLL = Orient Last Layer (7 cases for 2x2 cube)
#
# RUN:
# cd Ressources/Cases-Ortega-OLL
# bash Download-Ortega-OLL-Cases.sh

# Define the base URL for downloading 2x2 OLL images
# Key difference from 3x3: pzl=2 parameter
base_url="https://visualcube.api.cubing.net/visualcube.php?pzl=2&fmt=svg&size=300&view=plan&"

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

# Ortega OLL Cases (2x2 cube)
# Format: "filename;scramble"
# Scrambles from: Deddal/Data/Resources/SeedData/2x2_ortega_oll_cases.json
oll_cases=()
oll_cases+=("2x2_ortega_oll_1;R U2 R' U' R U' R'")                 # Sune
oll_cases+=("2x2_ortega_oll_2;R U R' U R U2 R'")                   # Anti-Sune
oll_cases+=("2x2_ortega_oll_3;F R U R' U' F'")                     # U / Headlights
oll_cases+=("2x2_ortega_oll_4;F R U R' U' R U R' U' F'")           # Pi / Bruno
oll_cases+=("2x2_ortega_oll_5;F' R' F R U R U' R'")                # T / Chameleon
oll_cases+=("2x2_ortega_oll_6;R2 U2 R U2 R2")                      # H / Double Anti-Sune
oll_cases+=("2x2_ortega_oll_7;F' R' U R U R' F R")                 # L / Bowtie

# Standard rotation for 2x2 OLL (same as 3x3)
rParam="y30x-35"

echo "=== Generating 2x2 Ortega OLL Case Images ==="
echo ""

# Loop through cases
for case_info in "${oll_cases[@]}"; do
  IFS=";" read -r case_name scramble <<< "$case_info"

  # URL encode scramble
  encoded=$(urlencode "$scramble")

  # Construct URL - testing without stage parameter for 2x2
  # If images don't look right, try adding: &stage=oll
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
svg_count=$(ls -1 2x2_ortega_oll_*.svg 2>/dev/null | wc -l | tr -d ' ')
echo "Generated ${svg_count}/7 OLL case images"
echo ""

if [ "$svg_count" -eq 7 ]; then
  echo "✅ All OLL images generated successfully!"
  echo ""
  echo "Next steps:"
  echo "1. Review images to verify they display correctly"
  echo "2. Add images to Xcode: Deddal/App/Assets.xcassets/Ortega-OLL/"
  echo "3. Run PBL script: cd ../Cases-Ortega-PBL && bash Download-Ortega-PBL-Cases.sh"
else
  echo "⚠️  Some images failed to generate. Check output above for errors."
fi
echo ""
