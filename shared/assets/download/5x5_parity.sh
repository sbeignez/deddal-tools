#!/bin/bash

# Download 5x5 parity case images from VisualCube API
# Output directory: current directory (run from tool-assets/download/)

# Base URL for VisualCube API (5x5 cube)
base_url="https://visualcube.api.cubing.net/visualcube.php?fmt=svg&size=512&pzl=5&"

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
      "'") encoded+="%27" ;;
      *) encoded+=$(printf '%%%02X' "'$c") ;;
    esac
  done
  echo "$encoded"
}

# 5x5 Parity Cases (only edge parity on odd cubes)
# Format: filename;view;scramble_algorithm
parity_cases=()

# Edge Parity (single flipped edge)
parity_cases+=("5x5_edge_parity;plan;Rw U2 Rw x U2 Rw U2 3Rw' U2 Lw U2 Rw' U2 Rw U2 Rw' U2 Rw'")

echo "Downloading 5x5 parity case images..."
echo "=========================================="

# Loop through cases
for case_info in "${parity_cases[@]}"; do
  IFS=";" read -r filename view scramble <<< "$case_info"

  # URL encode the scramble
  encoded_scramble=$(urlencode "$scramble")

  # Construct URL
  image_url="${base_url}view=${view}&alg=${encoded_scramble}"

  echo "Downloading ${filename}.svg..."
  echo "  URL: $image_url"

  # Download with curl
  curl -L -s -o "${filename}.svg" "$image_url"

  # Remove white background (macOS sed syntax)
  if [ -f "${filename}.svg" ]; then
    sed -i '' "s/<rect fill='#FFFFFF'/<rect fill='none'/g" "${filename}.svg"
    echo "  ✓ Downloaded and processed ${filename}.svg"
  else
    echo "  ✗ Failed to download ${filename}.svg"
  fi
done

echo "=========================================="
echo "5x5 parity image download complete!"
echo "Total images: ${#parity_cases[@]}"
