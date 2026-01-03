#!/bin/bash

# Script to rename case image assets to standardized caseimg_{code} format
# Usage: ./rename_assets.sh [--dry-run]

ASSETS_DIR="Deddal/App/Assets.xcassets"
DRY_RUN=false

if [[ "$1" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "=== DRY RUN MODE (no changes will be made) ==="
    echo ""
fi

# Counters
RENAMED=0
SKIPPED=0
ERRORS=0

# Function to rename an imageset
rename_imageset() {
    local old_path="$1"
    local old_name=$(basename "$old_path")
    local dir_path=$(dirname "$old_path")

    # Extract code from old name
    local code=""

    if [[ "$old_name" =~ ^Case-(.+)\.imageset$ ]]; then
        # Pattern: Case-{code}.imageset
        code="${BASH_REMATCH[1]}"
    elif [[ "$old_name" =~ ^img-case-(.+)\.imageset$ ]]; then
        # Pattern: img-case-{code}.imageset
        code="${BASH_REMATCH[1]}"
    else
        echo "  ⚠️  Skipped (unknown pattern): $old_name"
        ((SKIPPED++))
        return
    fi

    # Build new name
    local new_name="caseimg_${code}.imageset"
    local new_path="${dir_path}/${new_name}"

    # Check if already renamed
    if [[ "$old_name" == "$new_name" ]]; then
        echo "  ✓  Already correct: $old_name"
        ((SKIPPED++))
        return
    fi

    # Check if target already exists
    if [[ -e "$new_path" ]]; then
        echo "  ❌ Conflict: $new_name already exists"
        ((ERRORS++))
        return
    fi

    # Perform rename
    if [[ "$DRY_RUN" == true ]]; then
        echo "  [DRY RUN] Would rename: $old_name → $new_name"
    else
        git mv "$old_path" "$new_path"
        echo "  ✅ Renamed: $old_name → $new_name"
    fi

    ((RENAMED++))
}

echo "=== Renaming Case Image Assets ==="
echo "Assets directory: $ASSETS_DIR"
echo ""

# Find and process all matching imagesets
echo "Processing F2L imagesets..."
while IFS= read -r -d '' imageset; do
    rename_imageset "$imageset"
done < <(find "$ASSETS_DIR/F2L" -name "Case-*.imageset" -type d -print0 2>/dev/null || true)

echo ""
echo "Processing OLL imagesets..."
while IFS= read -r -d '' imageset; do
    rename_imageset "$imageset"
done < <(find "$ASSETS_DIR/OLL" -name "Case-*.imageset" -type d -print0 2>/dev/null || true)

echo ""
echo "Processing PLL imagesets..."
while IFS= read -r -d '' imageset; do
    rename_imageset "$imageset"
done < <(find "$ASSETS_DIR/PLL" -name "img-case-*.imageset" -type d -print0 2>/dev/null || true)

echo ""
echo "Processing OeLL (Beginner) imagesets..."
if [[ -d "$ASSETS_DIR/OeLL" ]]; then
    while IFS= read -r -d '' imageset; do
        rename_imageset "$imageset"
    done < <(find "$ASSETS_DIR/OeLL" -name "Case-*.imageset" -type d -print0 2>/dev/null || true)
    while IFS= read -r -d '' imageset; do
        rename_imageset "$imageset"
    done < <(find "$ASSETS_DIR/OeLL" -name "img-case-*.imageset" -type d -print0 2>/dev/null || true)
else
    echo "  ⚠️  OeLL directory not found, skipping"
fi

echo ""
echo "Processing top-level error case..."
if [[ -e "$ASSETS_DIR/Case-ERROR.imageset" ]]; then
    rename_imageset "$ASSETS_DIR/Case-ERROR.imageset"
fi

echo ""
echo "=== Summary ==="
echo "Renamed: $RENAMED"
echo "Skipped: $SKIPPED"
echo "Errors:  $ERRORS"
echo ""

if [[ "$DRY_RUN" == true ]]; then
    echo "This was a dry run. To apply changes, run:"
    echo "  ./rename_assets.sh"
else
    echo "Asset renaming complete!"
    echo ""
    echo "Next steps:"
    echo "1. Verify renamed assets in Xcode"
    echo "2. Build project to check for any issues"
    echo "3. Commit changes: git add . && git commit -m 'Standardize asset naming to caseimg_{code} format'"
fi
