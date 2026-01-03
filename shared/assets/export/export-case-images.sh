#!/bin/bash
# Export case images from iOS xcassets to staging directory

ASSETS_DIR="./Deddal/App/Assets.xcassets"
EXPORT_DIR="/tmp/case-images-export"

echo "🔍 Exporting case images from iOS xcassets..."
echo ""

# Create export directory structure
mkdir -p "$EXPORT_DIR/oll"
mkdir -p "$EXPORT_DIR/pll"
mkdir -p "$EXPORT_DIR/f2l"

# Function to export images from a category
export_category() {
    local category=$1
    local target_dir=$2
    local source_dir="$ASSETS_DIR/$category"

    echo "📦 Exporting $category images..."

    if [ ! -d "$source_dir" ]; then
        echo "  ⚠ Directory not found: $source_dir"
        return
    fi

    local count=0

    # Find all .imageset directories
    while IFS= read -r imageset; do
        # Extract the base name (e.g., "Case-OLL-1" from "Case-OLL-1.imageset")
        local basename=$(basename "$imageset" .imageset)

        # Find SVG file in this imageset
        local svg_file=$(find "$imageset" -name "*.svg" -type f | head -1)

        if [ -n "$svg_file" ]; then
            # Copy with original filename
            cp "$svg_file" "$target_dir/$basename.svg"
            count=$((count + 1))
        else
            echo "  ⚠ No SVG found in $basename"
        fi
    done < <(find "$source_dir" -name "*.imageset" -type d)

    echo "  ✓ Exported $count images"
}

# Export each category
export_category "OLL" "$EXPORT_DIR/oll"
export_category "PLL" "$EXPORT_DIR/pll"
export_category "F2L" "$EXPORT_DIR/f2l"

echo ""
echo "✅ Export complete!"
echo "📁 Images exported to: $EXPORT_DIR"
echo ""
echo "Summary:"
echo "  OLL: $(ls -1 "$EXPORT_DIR/oll" 2>/dev/null | wc -l | xargs) images"
echo "  PLL: $(ls -1 "$EXPORT_DIR/pll" 2>/dev/null | wc -l | xargs) images"
echo "  F2L: $(ls -1 "$EXPORT_DIR/f2l" 2>/dev/null | wc -l | xargs) images"
echo "  Total: $(find "$EXPORT_DIR" -name "*.svg" | wc -l | xargs) images"
