#!/bin/bash

# RUN
# Open terminal
# cd /Users/trophee-mini/code/deddal/deddal-ios/Ressources/assets_3x3_lbl
# bash Download-LBL-Cases.sh

# Define the base URL for downloading images.
base_url="https://visualcube.api.cubing.net/visualcube.php?fmt=svg&"

# Function to URL-encode a string.
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

# LBL Cases stored in a flat array
# Format: filename;size;view;stage;formula;rotation
lbl_cases=()

# First Layer Cases (3D view, 300px)
lbl_cases+=("3x3_lbl_first-layer-corners_01;300;;;fl;R U R' U';")
lbl_cases+=("3x3_lbl_first-layer-corners-helper_01;300;;;fl;R' D' R D;")

# Second Layer Cases (3D view, 300px)
lbl_cases+=("3x3_lbl_second-layer-edges-left_01;300;;;f2l;U' L' U L U F U' F';")
lbl_cases+=("3x3_lbl_second-layer-edges-right_01;300;;;f2l;U R U' R' U' F' U F;")

# Last Layer Cases (top-down view, 200px)
lbl_cases+=("3x3_lbl_top-cross_01;200;plan;ll;F U R U' R' F';")
lbl_cases+=("3x3_lbl_top-corners-orient_01;200;plan;ll;R U R' U R U2 R';")
lbl_cases+=("3x3_lbl_top-corners-position_01;200;plan;ll;R' F R' B2 R F' R' B2 R2 U';")
lbl_cases+=("3x3_lbl_top-edges-position_01;200;plan;ll;F2 U L R' F2 L' R U F2;")

# Loop through cases
for case_info in "${lbl_cases[@]}"; do
  IFS=";" read -r case_name size view stage formula rotation <<< "$case_info"

  # Build URL parameters
  params="size=${size}"

  # Add view parameter if specified (for top-down last layer cases)
  if [ -n "$view" ]; then
    params="${params}&view=${view}"
  fi

  # Add stage parameter if specified
  if [ -n "$stage" ]; then
    params="${params}&stage=${stage}"
  fi

  # Encode formula properly
  encoded=$(urlencode "$formula")
  params="${params}&case=${encoded}"

  # Add rotation if specified (otherwise uses default 3D angle)
  if [ -n "$rotation" ]; then
    params="${params}&r=${rotation}"
  fi

  # Construct final URL
  image_url="${base_url}${params}"

  echo "Downloading ${case_name} from: $image_url"

  # Use curl to download
  curl -L -s -o "${case_name}.svg" "$image_url"

  # Remove white background fill
  if [ -f "${case_name}.svg" ]; then
    sed -i '' "s/<rect fill='#FFFFFF'/<rect fill='none'/g" "${case_name}.svg"
    echo "✓ Downloaded and processed ${case_name}.svg"
  else
    echo "✗ Failed to download ${case_name}.svg"
  fi
done

echo ""
echo "Download complete! Generated 8 LBL case images."
