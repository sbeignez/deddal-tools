#!/bin/bash

# Generate 2x2 CLL case images using VisualCube API
# CLL = Corner Last Layer (40 cases for 2x2 cube)
#
# RUN:
# cd Ressources/assets_2x2_cll
# bash Download-CLL-Cases.sh

# Define the base URL for downloading 2x2 CLL images
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

# CLL Cases (2x2 cube)
# Format: "filename;scramble"
# Scrambles from: claude/02-features/methods-sync/cll_seed_generator.py (first algorithm)
cll_cases=()

# AS (Anti-Sune) cases (6 cases)
cll_cases+=("2x2_cll_cll_as1;y R U2 R' U' R U' R'")
cll_cases+=("2x2_cll_cll_as2;R U2 R' F R' F' R U' R U' R'")
cll_cases+=("2x2_cll_cll_as3;y2 F' L F L' U2 L' U2 L")
cll_cases+=("2x2_cll_cll_as4;y2 R' F R F' R U R'")
cll_cases+=("2x2_cll_cll_as5;y2 R U2 R' U2 R' F R F'")
cll_cases+=("2x2_cll_cll_as6;y' R U2 R' U' R U' R' F R' F' R U R U' R' U'")

# H cases (4 cases)
cll_cases+=("2x2_cll_cll_h1;F R2 U' R2 U' R2 U R2 F'")
cll_cases+=("2x2_cll_cll_h2;R U R' U R U R' F R' F' R")
cll_cases+=("2x2_cll_cll_h3;y F R U R' U' R U R' U' R U R' U' F'")
cll_cases+=("2x2_cll_cll_h4;y R2 U2 R' U2 R2")

# L cases (6 cases)
cll_cases+=("2x2_cll_cll_l1;y R U2 R' F' R U2 R' U R' F2 R")
cll_cases+=("2x2_cll_cll_l2;y2 R U2 R2 F2 R U R' F2 R F'")
cll_cases+=("2x2_cll_cll_l3;y2 R' U R' U2 R U' R' U R U' R2")
cll_cases+=("2x2_cll_cll_l4;y R U2 R2 F R F' R U2 R'")
cll_cases+=("2x2_cll_cll_l5;y F R' F' R U R U' R'")
cll_cases+=("2x2_cll_cll_l6;y2 F' R U R' U' R' F R")

# Pi cases (6 cases)
cll_cases+=("2x2_cll_cll_pi1;y F R' F' R U2 R U' R' U R U2 R'")
cll_cases+=("2x2_cll_cll_pi2;R U2 R' U' R U R' U2 R' F R F'")
cll_cases+=("2x2_cll_cll_pi3;y F R2 U' R2 U R2 U R2 F'")
cll_cases+=("2x2_cll_cll_pi4;y2 R' F R F' R U' R' U' R U' R'")
cll_cases+=("2x2_cll_cll_pi5;y' R' U' R' F R F' R U' R' U2 R")
cll_cases+=("2x2_cll_cll_pi6;R U' R2 U R2 U R2 U' R")

# Sune cases (6 cases)
cll_cases+=("2x2_cll_cll_sune1;L' U2 L U2 L F' L' F")
cll_cases+=("2x2_cll_cll_sune2;R U R' U' R' F R F' R U R' U R U2 R'")
cll_cases+=("2x2_cll_cll_sune3;R U' R' F R' F' R")
cll_cases+=("2x2_cll_cll_sune4;F R' F' R U2 R U2 R'")
cll_cases+=("2x2_cll_cll_sune5;y2 R U R' U R' F R F' R U2 R'")
cll_cases+=("2x2_cll_cll_sune6;R U R' U R U2 R'")

# T cases (6 cases)
cll_cases+=("2x2_cll_cll_t1;y' R U R' U' R' F R F'")
cll_cases+=("2x2_cll_cll_t2;y L' U' L U L F' L' F")
cll_cases+=("2x2_cll_cll_t3;F U' R U2 R' U' F2 R U R'")
cll_cases+=("2x2_cll_cll_t4;R' U R U2 R2 F' R U' R' F2 R2")
cll_cases+=("2x2_cll_cll_t5;y2 F R U R' U' R U' R' U' R U R' F'")
cll_cases+=("2x2_cll_cll_t6;R' U R U2 R2 F R F' R")

# U cases (6 cases)
cll_cases+=("2x2_cll_cll_u1;y' F R U R' U' F'")
cll_cases+=("2x2_cll_cll_u2;R' U' R2 U R' U2 R U2 R' U R'")
cll_cases+=("2x2_cll_cll_u3;y2 F R U R' U2 F' R U' R' F")
cll_cases+=("2x2_cll_cll_u4;y' F R' F' R U' R U' R' U2 R U' R'")
cll_cases+=("2x2_cll_cll_u5;R U' R2 F R F' R U R' U' R U R'")
cll_cases+=("2x2_cll_cll_u6;R' U R' F R F' R U2 R' U R")

# Standard rotation for 2x2 CLL
rParam="y30x-35"

echo "=== Generating 2x2 CLL Case Images ==="
echo ""

# Loop through cases
for case_info in "${cll_cases[@]}"; do
  IFS=";" read -r case_name scramble <<< "$case_info"

  # URL encode scramble
  encoded=$(urlencode "$scramble")

  # Construct URL
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
svg_count=$(ls -1 2x2_cll_cll_*.svg 2>/dev/null | wc -l | tr -d ' ')
echo "Generated ${svg_count}/40 CLL case images"
echo ""

if [ "$svg_count" -eq 40 ]; then
  echo "✅ All CLL images generated successfully!"
  echo ""
  echo "Next steps:"
  echo "1. Review images to verify they display correctly"
  echo "2. Create Xcode imagesets: Deddal/App/Assets.xcassets/2x2_cll/"
  echo "3. Update seed data JSON with image_asset_name fields"
  echo "4. Upload to Supabase Storage using upload_case_images.sh"
else
  echo "⚠️  Some images failed to generate. Check output above for errors."
fi
echo ""
