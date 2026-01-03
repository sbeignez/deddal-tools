#!/bin/bash

# Generate 3x3 PcLL (Permute Corners of Last Layer) case images using VisualCube API
# PcLL = 2-Look LL Step 3 (Beginner Method)
# Only 2 cases: Adjacent corner swap and Diagonal corner swap
#
# RUN:
# cd Ressources/assets_3x3_cfop_pcll
# bash Download-PcLL-Cases.sh

# Define the base URL for downloading images
base_url="https://visualcube.api.cubing.net/visualcube.php?fmt=svg&size=200&view=plan&"

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

# PcLL Cases (simplified for beginners - only corner permutation)
# Format: "filename;stage;rotation;formula;arrows"
# Using "coll" stage (Corner Orientation Last Layer) with edge arrows in black
pcll_cases=()
pcll_cases+=("3x3_cfop_pcll_adj;coll;Good;R U' L' U R' U' L;U2U8-black,U8U2-black")
pcll_cases+=("3x3_cfop_pcll_dia;coll;Good;F R (U' R' U') (R U R' F') (R U R' U') (R' F R F');U0U8-black,U8U0-black")

# Standard rotation for 3x3 PLL view
rParam="y30x-35"

echo "=== Generating PcLL Case Images ==="
echo ""

# Loop through cases
for case_info in "${pcll_cases[@]}"; do
  IFS=";" read -r case_name stage rotation formula arrows <<< "$case_info"

  # Encode formula properly
  encoded=$(urlencode "$formula")

  # Construct final URL
  image_url="${base_url}stage=${stage}&r=${rParam}&case=${encoded}&arw=${arrows}"

  echo "Downloading ${case_name}.svg"
  echo "  Formula: ${formula}"
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
svg_count=$(ls -1 3x3_cfop_pcll_*.svg 2>/dev/null | wc -l | tr -d ' ')
echo "Generated ${svg_count}/2 PcLL case images"
echo ""

if [ "$svg_count" -eq 2 ]; then
  echo "✅ All PcLL images generated successfully!"
  echo ""
  echo "Next steps:"
  echo "1. Review images to verify they display correctly"
  echo "2. These are beginner-friendly simplified PLL cases showing only corner permutation"
  echo "3. Add images to Xcode: Deddal/App/Assets.xcassets/PLL/"
else
  echo "⚠️  Some images failed to generate. Check output above for errors."
fi
echo ""
