#!/bin/bash

# Sample script to generate 10 diverse move visualizations (static SVG + animated GIF)
# This generates a representative sample for quality review

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

  # Remove white background rectangle from SVG (make background transparent)
  sed -i '' "/<rect fill='#FFFFFF'/d" "${static_dir}/${filename}.svg"

  echo "  ✓ Static SVG saved: ${static_dir}/${filename}.svg"
}

# Function to generate animated GIF for a move
generate_animated() {
  local move="$1"
  local filename=$(sanitize_filename "$move")

  echo "Generating animated GIF for move: $move → ${filename}.gif"

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
    echo "  ✓ Animated GIF saved: ${animated_dir}/${filename}.gif"
  elif command -v convert &> /dev/null; then
    # Fallback to 'convert' for older ImageMagick versions
    convert -delay 50 -loop 0 "${temp_dir}/frame_0.svg" "${temp_dir}/frame_1.svg" "${animated_dir}/${filename}.gif"
    echo "  ✓ Animated GIF saved: ${animated_dir}/${filename}.gif"
    echo "  ⚠ Using deprecated 'convert' command. Update ImageMagick for 'magick' support."
  else
    echo "  ⚠ ImageMagick not installed. Skipping GIF generation."
    echo "  Install with: brew install imagemagick"
  fi

  # Clean up temp files
  rm -f "${temp_dir}/frame_"*.svg
}

# Sample 10 moves covering diverse move types
moves=(
  "F"      # Face turn clockwise
  "F'"     # Face turn counter-clockwise
  "R"      # Right face clockwise
  "R'"     # Right face counter-clockwise
  "U"      # Up face clockwise
  "U'"     # Up face counter-clockwise
  "F2"     # Face 180° turn
  "R2"     # Right 180° turn
  "x"      # Cube rotation (x-axis)
  "M"      # Middle slice move
)

echo "========================================="
echo "Sample Move Visualization Generator"
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
echo "✓ Sample generation complete!"
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
echo "  1. Review SVG files in a vector editor (Illustrator, Inkscape, Figma)"
echo "  2. Check that the visual style matches your reference"
echo "  3. If satisfied, proceed with generating all 109 moves"
echo ""
