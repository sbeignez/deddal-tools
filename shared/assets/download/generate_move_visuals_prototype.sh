#!/bin/bash

# Prototype script to generate move visualizations (static SVG + animated GIF)
# This prototype generates 6 sample moves: F, R, U, F', R', U'

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

  echo "Downloading static SVG for move: $move → ${filename}.svg"
  curl -s "$url" -o "${static_dir}/${filename}.svg"

  # Remove white fill from SVG (make background transparent)
  sed -i '' 's/fill="white"//g' "${static_dir}/${filename}.svg"

  echo "  ✓ Static SVG saved: ${static_dir}/${filename}.svg"
}

# Function to generate animated GIF for a move
# Strategy: Generate 8 intermediate frames showing rotation progress
generate_animated() {
  local move="$1"
  local filename=$(sanitize_filename "$move")

  echo "Generating animated GIF for move: $move → ${filename}.gif"

  # For prototype, we'll create a simple 2-frame animation (before/after)
  # Full implementation would generate 8-10 intermediate frames

  # Frame 1: Solved cube
  local frame1_url="${base_url}?fmt=svg&size=200&view=plan&stage=full&r=y30x-35"
  curl -s "$frame1_url" -o "${temp_dir}/frame_0.svg"
  sed -i '' 's/fill="white"//g' "${temp_dir}/frame_0.svg"

  # Frame 2: After move
  local encoded_move=$(urlencode "$move")
  local frame2_url="${base_url}?fmt=svg&size=200&view=plan&stage=full&r=y30x-35&case=${encoded_move}"
  curl -s "$frame2_url" -o "${temp_dir}/frame_1.svg"
  sed -i '' 's/fill="white"//g' "${temp_dir}/frame_1.svg"

  # Check if ImageMagick is installed
  if command -v convert &> /dev/null; then
    # Convert SVGs to GIF with animation
    convert -delay 50 -loop 0 "${temp_dir}/frame_0.svg" "${temp_dir}/frame_1.svg" "${animated_dir}/${filename}.gif"
    echo "  ✓ Animated GIF saved: ${animated_dir}/${filename}.gif"
  else
    echo "  ⚠ ImageMagick not installed. Skipping GIF generation."
    echo "  Install with: brew install imagemagick"
  fi

  # Clean up temp files
  rm -f "${temp_dir}/frame_"*.svg
}

# Prototype moves to generate
moves=(
  "F"
  "R"
  "U"
  "F'"
  "R'"
  "U'"
)

echo "========================================="
echo "Move Visualization Prototype Generator"
echo "========================================="
echo ""
echo "Generating ${#moves[@]} sample moves..."
echo ""

# Generate visualizations for each move
for move in "${moves[@]}"; do
  echo "---"
  download_static "$move"
  generate_animated "$move"
  echo ""
done

echo "========================================="
echo "✓ Prototype generation complete!"
echo "========================================="
echo ""
echo "Generated files:"
echo "  Static SVGs: ${static_dir}/"
ls -lh "$static_dir"
echo ""
echo "  Animated GIFs: ${animated_dir}/"
ls -lh "$animated_dir"
echo ""
echo "Next steps:"
echo "  1. Review visual quality of generated assets"
echo "  2. Check file sizes (should be ~5KB for SVG, ~50KB for GIF)"
echo "  3. If satisfied, run full generation for all 109 moves"
echo ""
