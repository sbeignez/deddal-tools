#!/bin/bash

# Download 4x4 parity case images from VisualCube API
# Output directory: current directory (run from tools/shared/assets/download/)

# Base URL for VisualCube API (4x4 cube)
base_url="https://visualcube.api.cubing.net/visualcube.php?fmt=svg&size=512&pzl=4&"

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

# 4x4 Parity Cases
# Format: filename;view;scramble_algorithm
parity_cases=()

# OLL Parity - Yellow top with one flipped dedge (edge flip parity)
# Creates OLL parity: one dedge flipped on an otherwise oriented LL
parity_cases+=("4x4_oll_parity;plan;alg=Rw U2 x Rw U2 Rw U2 Rw' U2 Lw U2 Rw' U2 Rw U2 Rw' U2 Rw'")

# PLL Adjacent Parity - Two adjacent dedges swapped (Ua perm with parity)
# Yellow top, adjacent edges need swap
parity_cases+=("4x4_pll_parity_adj;plan;alg=r2 U2 r2 Uw2 r2 Uw2")

# PLL Opposite Parity - Two opposite dedges swapped (H perm with parity)
# Yellow top, opposite edges need swap
parity_cases+=("4x4_pll_parity_opp;plan;alg=r2 U2 r2 Uw2 r2 u2")

# PLL Diagonal Parity - Diagonal dedges swapped (Z perm with parity)
# Yellow top, diagonal edges need swap
parity_cases+=("4x4_pll_parity_diag;plan;alg=r2 U2 r2 Uw2 r2 Uw2 U2")

# PLL + U-perm - Edge parity combined with 3-cycle of corners
# Yellow top with both edge swap and corner cycle
parity_cases+=("4x4_pll_parity_uperm;plan;alg=r2 U2 r2 Uw2 r2 Uw2 M2 U M2 U2 M2 U M2")

echo "Downloading 4x4 parity case images..."
echo "=========================================="

# Loop through cases
for case_info in "${parity_cases[@]}"; do
  IFS=";" read -r filename view params <<< "$case_info"

  # Construct URL with case parameters
  image_url="${base_url}view=${view}&${params}"

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
echo "4x4 parity image download complete!"
echo "Total images: ${#parity_cases[@]}"
