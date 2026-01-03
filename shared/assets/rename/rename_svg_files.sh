#!/bin/bash

# Rename all SVG source files based on mapping CSV
# Uses git mv to preserve file history

set -e  # Exit on error

CSV_FILE="rename_mapping.csv"
ERRORS=0
SUCCESS=0

echo "🔄 Renaming SVG source files using git mv..."
echo ""

# Process only SVG entries from CSV (skip header)
tail -n +2 "$CSV_FILE" | grep '^svg,' | while IFS=',' read -r type category old_name new_name; do
    # Determine source directory based on category
    case "$category" in
        "f2l")
            src_dir="Ressources/Cases-F2L"
            ;;
        "oll")
            src_dir="Ressources/Cases-OLL"
            ;;
        "oell")
            src_dir="Ressources/Cases-OLL"
            ;;
        "pll")
            src_dir="Ressources/PLL-cases"
            ;;
        "pcll")
            src_dir="Ressources/PLL-cases"
            ;;
        "ortega-oll")
            src_dir="Ressources/Cases-Ortega-OLL"
            ;;
        "ortega-pbl")
            src_dir="Ressources/Cases-Ortega-PBL"
            ;;
        *)
            echo "⚠️  Unknown category: $category for $old_name"
            ((ERRORS++))
            continue
            ;;
    esac

    old_path="$src_dir/$old_name"
    new_path="$src_dir/$new_name"

    # Check if source file exists
    if [ ! -f "$old_path" ]; then
        echo "⚠️  File not found: $old_path"
        ((ERRORS++))
        continue
    fi

    # Check if destination already exists
    if [ -f "$new_path" ]; then
        echo "⚠️  Destination already exists: $new_path"
        ((ERRORS++))
        continue
    fi

    # Perform git mv
    if git mv "$old_path" "$new_path" 2>/dev/null; then
        echo "✅ $category: $old_name → $new_name"
        ((SUCCESS++))
    else
        echo "❌ Failed to rename: $old_path"
        ((ERRORS++))
    fi
done

echo ""
echo "════════════════════════════════════════"
echo "SVG Rename Summary:"
echo "  ✅ Success: $SUCCESS files"
echo "  ❌ Errors:  $ERRORS files"
echo "════════════════════════════════════════"

if [ $ERRORS -eq 0 ]; then
    echo "✅ All SVG files renamed successfully!"
    exit 0
else
    echo "⚠️  Completed with $ERRORS errors"
    exit 1
fi
