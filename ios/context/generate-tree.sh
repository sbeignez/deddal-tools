#!/bin/bash

# Deddal iOS Tree Structure Generator
# Usage: ./tools/ios/context/generate-tree.sh [target_directory] [output_file]
# Example: ./tools/ios/context/generate-tree.sh Deddal documentation/Deddal-Tree-Structure.md
#
# When called with no arguments, generates trees for both Deddal and DeddalCore

# Get the deddal-ios root directory (parent of tools/ios/context)
DEDDAL_IOS_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Function to generate tree for a single directory
generate_tree() {
  local TARGET_DIR="$1"
  local OUTPUT_FILE="$2"

  # Full paths
  local FULL_TARGET_DIR="$DEDDAL_IOS_ROOT/$TARGET_DIR"
  local FULL_OUTPUT_FILE="$DEDDAL_IOS_ROOT/$OUTPUT_FILE"

  # Check if target directory exists
  if [ ! -d "$FULL_TARGET_DIR" ]; then
    echo "Error: Target directory does not exist: $FULL_TARGET_DIR"
    return 1
  fi

  # Create output directory if it doesn't exist
  local OUTPUT_DIR=$(dirname "$FULL_OUTPUT_FILE")
  mkdir -p "$OUTPUT_DIR"

  echo "Generating tree structure..."
  echo "  Source: $FULL_TARGET_DIR"
  echo "  Output: $FULL_OUTPUT_FILE"

  # Generate the tree structure
  cd "$FULL_TARGET_DIR"

  # Create temporary file
  local TEMP_FILE=$(mktemp)

  # Write header
  echo "# $(basename "$TARGET_DIR") Folder Structure" > "$TEMP_FILE"
  echo "" >> "$TEMP_FILE"
  echo "Generated: $(date)" >> "$TEMP_FILE"
  echo "" >> "$TEMP_FILE"
  echo '```' >> "$TEMP_FILE"

  # Generate tree with formatting
  find . -name ".DS_Store" -prune -o -print | \
    grep -v ".DS_Store" | \
    sed 's|^\./||' | \
    grep -v '^$' | \
    sort | \
    awk '
    BEGIN {
      FS = "/"
    }
    {
      depth = NF - 1
      name = $NF
      if (name == ".") next

      # Print indentation
      for (i = 0; i < depth; i++) {
        printf "   "
      }

      # Print the item
      if (depth > 0) {
        printf "|   "
      }
      print name
    }
    ' >> "$TEMP_FILE"

  # Close code block
  echo '```' >> "$TEMP_FILE"

  # Move to final location
  mv "$TEMP_FILE" "$FULL_OUTPUT_FILE"

  echo "✓ Tree structure saved to: $OUTPUT_FILE"
  echo "  Total lines: $(wc -l < "$FULL_OUTPUT_FILE")"
  echo ""
}

# Main logic
if [ $# -eq 0 ]; then
  # No arguments - generate for Deddal, DeddalCore, and DeddalTests
  echo "Generating tree structures for Deddal, DeddalCore, and DeddalTests..."
  echo ""
  generate_tree "Deddal" "documentation/Deddal-Tree-Structure.md"
  generate_tree "DeddalCore" "documentation/DeddalCore-Tree-Structure.md"
  generate_tree "DeddalTests" "documentation/DeddalTests-Tree-Structure.md"
  echo "✅ All tree structures generated successfully!"
else
  # Arguments provided - use existing single-directory behavior
  TARGET_DIR="${1:-Deddal}"
  OUTPUT_FILE="${2:-documentation/Deddal-Tree-Structure.md}"
  generate_tree "$TARGET_DIR" "$OUTPUT_FILE"
fi
