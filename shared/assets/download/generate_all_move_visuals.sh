#!/bin/bash

# Full script to generate all 109 move visualizations (static SVG + animated GIF)
# Based on Move enum from Deddal/Models/Cube/Move.swift

# Base URL for VisualCube API
base_url="https://visualcube.api.cubing.net/visualcube.php"

# Output directories
static_dir="../../Ressources/move_visuals/static"
animated_dir="../../Ressources/move_visuals/animated"
temp_dir="../../Ressources/move_visuals/temp"

# Create directories
mkdir -p "$static_dir"
mkdir -p "$animated_dir"
mkdir -p "$temp_dir"

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

# Function to sanitize move notation for filename
# F  → F
# F' → F_prime
# F2 → F2
# F2' → F2_prime
sanitize_filename() {
  local move="$1"
  echo "$move" | sed "s/'/_prime/g"
}

# Function to download static SVG for a move
download_static() {
  local move="$1"
  local filename=$(sanitize_filename "$move")
  local encoded_move=$(urlencode "$move")

  local url="${base_url}?fmt=svg&size=200&view=plan&stage=full&r=y30x-35&case=${encoded_move}"

  curl -s "$url" -o "${static_dir}/${filename}.svg"

  # Remove white background rectangle from SVG (make background transparent)
  sed -i '' "/<rect fill='#FFFFFF'/d" "${static_dir}/${filename}.svg"
}

# Function to generate animated GIF for a move
generate_animated() {
  local move="$1"
  local filename=$(sanitize_filename "$move")

  # Frame 1: Solved cube
  local frame1_url="${base_url}?fmt=svg&size=200&view=plan&stage=full&r=y30x-35"
  curl -s "$frame1_url" -o "${temp_dir}/frame_0.svg"
  sed -i '' "/<rect fill='#FFFFFF'/d" "${temp_dir}/frame_0.svg"

  # Frame 2: After move
  local encoded_move=$(urlencode "$move")
  local frame2_url="${base_url}?fmt=svg&size=200&view=plan&stage=full&r=y30x-35&case=${encoded_move}"
  curl -s "$frame2_url" -o "${temp_dir}/frame_1.svg"
  sed -i '' "/<rect fill='#FFFFFF'/d" "${temp_dir}/frame_1.svg"

  # Check if ImageMagick is installed
  if command -v magick &> /dev/null; then
    # Convert SVGs to GIF with animation (using 'magick' instead of deprecated 'convert')
    magick -delay 50 -loop 0 "${temp_dir}/frame_0.svg" "${temp_dir}/frame_1.svg" "${animated_dir}/${filename}.gif"
  elif command -v convert &> /dev/null; then
    # Fallback to 'convert' for older ImageMagick versions
    convert -delay 50 -loop 0 "${temp_dir}/frame_0.svg" "${temp_dir}/frame_1.svg" "${animated_dir}/${filename}.gif"
  else
    echo "  ⚠ ImageMagick not installed. Skipping GIF generation."
    echo "  Install with: brew install imagemagick"
    return 1
  fi

  # Clean up temp files
  rm -f "${temp_dir}/frame_"*.svg
}

# All 109 moves from Move enum
# Face Turns: F, B, L, R, U, D (+ ', 2, 2', 3, 3' variants) = 36 moves
# Cube Rotations: x, y, z (+ ', 2, 2', 3, 3' variants) = 18 moves
# Wide Moves: f, b, l, r, u, d (+ ', 2, 2', 3, 3' variants) = 36 moves
# Slice Moves: M, E, S (+ ', 2, 2', 3, 3' variants) = 18 moves
# Special: ERROR (#) = 1 move
moves=(
  # Face Turns (36)
  "F" "B" "L" "R" "U" "D"
  "F'" "B'" "L'" "R'" "U'" "D'"
  "F2" "B2" "L2" "R2" "U2" "D2"
  "F2'" "B2'" "L2'" "R2'" "U2'" "D2'"
  "F3" "B3" "L3" "R3" "U3" "D3"
  "F3'" "B3'" "L3'" "R3'" "U3'" "D3'"

  # Cube Rotations (18)
  "x" "y" "z"
  "x'" "y'" "z'"
  "x2" "y2" "z2"
  "x2'" "y2'" "z2'"
  "x3" "y3" "z3"
  "x3'" "y3'" "z3'"

  # Wide Moves (36)
  "f" "b" "l" "r" "u" "d"
  "f'" "b'" "l'" "r'" "u'" "d'"
  "f2" "b2" "l2" "r2" "u2" "d2"
  "f2'" "b2'" "l2'" "r2'" "u2'" "d2'"
  "f3" "b3" "l3" "r3" "u3" "d3"
  "f3'" "b3'" "l3'" "r3'" "u3'" "d3'"

  # Slice Moves (18)
  "M" "E" "S"
  "M'" "E'" "S'"
  "M2" "E2" "S2"
  "M2'" "E2'" "S2'"
  "M3" "E3" "S3"
  "M3'" "E3'" "S3'"

  # Special (1)
  "#"
)

total=${#moves[@]}
current=0

echo "========================================="
echo "Move Visualization Generator"
echo "========================================="
echo ""
echo "Generating ${total} move visualizations..."
echo ""

# Generate visualizations for each move
for move in "${moves[@]}"; do
  ((current++))
  filename=$(sanitize_filename "$move")

  echo "[$current/$total] Processing move: $move → ${filename}"

  download_static "$move"
  generate_animated "$move"

  # Show progress every 10 moves
  if (( current % 10 == 0 )); then
    echo "  Progress: $current/$total moves complete"
  fi
done

echo ""
echo "========================================="
echo "✓ Generation complete!"
echo "========================================="
echo ""
echo "Summary:"
echo "  Total moves: ${total}"
echo "  Static SVGs: ${static_dir}/"
echo "  Animated GIFs: ${animated_dir}/"
echo ""

# Calculate total size
static_size=$(du -sh "$static_dir" | cut -f1)
animated_size=$(du -sh "$animated_dir" | cut -f1)

echo "Disk usage:"
echo "  Static SVGs: ${static_size}"
echo "  Animated GIFs: ${animated_size}"
echo ""
echo "Next steps:"
echo "  1. Import assets into Assets.xcassets"
echo "  2. Create MoveVisualizationService for move-to-asset mapping"
echo "  3. Build AlgorithmVisualSequence SwiftUI component"
echo ""
