#!/usr/bin/env python3
"""
Extract individual move card diagrams from PDF-to-SVG converted pages.

This script identifies move cards by finding clipPath definitions in the SVG,
extracts their bounding boxes, and creates individual SVG files for each card
with content properly positioned at 0,0.
"""

import re
import os
import json
from pathlib import Path
from xml.etree import ElementTree as ET

# Input/output directories
INPUT_DIR = Path("move_diagrams_from_pdf")
OUTPUT_DIR = Path("move_cards_extracted")

# Minimum dimensions to consider a valid move card (filter out small elements)
MIN_WIDTH = 150
MIN_HEIGHT = 150


def parse_clippath_bbox(svg_content):
    """
    Extract bounding boxes from clipPath definitions.

    Pattern: <clipPath id="clip-N">
               <path d="m x1,y1 h width v height H x1 Z" />
             </clipPath>

    Returns list of dicts with id, x, y, width, height
    """
    cards = []

    # Pattern 1: Rectangle path (m x,y h w v h H x Z)
    pattern1 = r'<clipPath\s+id="(clip-\d+)">\s*<path[^>]+d="[Mm]\s*([0-9.]+)[,\s]+([0-9.]+)\s+[Hh]\s*([0-9.]+)\s+[Vv]\s*([0-9.]+)\s+[Hh]\s*([0-9.]+)\s*[Zz]'

    # Pattern 2: Explicit rectangle coordinates (M x1 y1 L x2 y2 L x3 y3 L x4 y4 Z)
    pattern2 = r'<clipPath\s+id="(clip-\d+)">\s*<path[^>]+d="[Mm]\s*([0-9.]+)[,\s]+([0-9.]+)\s+[Ll]\s*([0-9.]+)[,\s]+([0-9.]+)\s+[Ll]\s*([0-9.]+)[,\s]+([0-9.]+)\s+[Ll]\s*([0-9.]+)[,\s]+([0-9.]+)\s*[Zz]'

    # Try pattern 1 first
    for match in re.finditer(pattern1, svg_content, re.IGNORECASE):
        clip_id = match.group(1)
        x1 = float(match.group(2))
        y1 = float(match.group(3))
        x2 = float(match.group(4))
        y2 = float(match.group(5))

        width = abs(x2 - x1)
        height = abs(y2 - y1)

        if width > MIN_WIDTH and height > MIN_HEIGHT:
            cards.append({
                'id': clip_id,
                'x': min(x1, x2),
                'y': min(y1, y2),
                'width': width,
                'height': height
            })

    # Try pattern 2 if pattern 1 didn't find enough cards
    if len(cards) < 3:
        for match in re.finditer(pattern2, svg_content, re.IGNORECASE):
            clip_id = match.group(1)
            x1, y1 = float(match.group(2)), float(match.group(3))
            x2, y2 = float(match.group(4)), float(match.group(5))
            x3, y3 = float(match.group(6)), float(match.group(7))
            x4, y4 = float(match.group(8)), float(match.group(9))

            x_min = min(x1, x2, x3, x4)
            y_min = min(y1, y2, y3, y4)
            x_max = max(x1, x2, x3, x4)
            y_max = max(y1, y2, y3, y4)

            width = x_max - x_min
            height = y_max - y_min

            if width > MIN_WIDTH and height > MIN_HEIGHT:
                cards.append({
                    'id': clip_id,
                    'x': x_min,
                    'y': y_min,
                    'width': width,
                    'height': height
                })

    return cards


def extract_card_content(svg_path, card, output_path):
    """
    Extract a single card from the source SVG and save as new file.

    Creates a new SVG with:
    - ViewBox starting at 0,0 with card dimensions
    - All content translated to position at origin
    """
    # Read source SVG
    with open(svg_path, 'r') as f:
        content = f.read()

    # Parse SVG
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Get namespace
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    # Create new SVG root
    new_svg = ET.Element('svg')
    new_svg.set('version', '1.1')
    new_svg.set('xmlns', 'http://www.w3.org/2000/svg')
    new_svg.set('width', f"{card['width']:.2f}")
    new_svg.set('height', f"{card['height']:.2f}")
    new_svg.set('viewBox', f"0 0 {card['width']:.2f} {card['height']:.2f}")

    # Copy defs section (needed for clipPaths, gradients, etc.)
    defs = root.find('.//{http://www.w3.org/2000/svg}defs')
    if defs is not None:
        new_svg.append(defs)

    # Create main group with translation
    main_group = ET.SubElement(new_svg, 'g')
    main_group.set('transform', f"translate(-{card['x']:.6f}, -{card['y']:.6f})")

    # Find and copy the group that uses this clipPath
    clip_ref = f"url(#{card['id']})"
    for elem in root.iter():
        if elem.get('clip-path') == clip_ref:
            # Copy this element and all its children
            main_group.append(elem)
            break

    # Write to file
    tree = ET.ElementTree(new_svg)
    ET.indent(tree, space='  ')
    tree.write(output_path, encoding='unicode', xml_declaration=True)

    print(f"  ✓ Extracted {card['id']}: {card['width']:.0f}×{card['height']:.0f}px")


def process_page(page_path):
    """Process a single PDF page SVG and extract all move cards."""
    page_name = page_path.stem
    print(f"\n📄 Processing {page_name}...")

    # Read SVG content
    with open(page_path, 'r') as f:
        content = f.read()

    # Extract card bounding boxes
    cards = parse_clippath_bbox(content)

    if not cards:
        print(f"  ⚠️  No move cards found")
        return []

    # Sort cards by position (top-to-bottom, left-to-right)
    cards_sorted = sorted(cards, key=lambda c: (round(c['y'] / 50), c['x']))

    print(f"  Found {len(cards_sorted)} move cards")

    # Extract each card
    extracted = []
    for idx, card in enumerate(cards_sorted, 1):
        output_name = f"{page_name}_card-{idx:02d}.svg"
        output_path = OUTPUT_DIR / output_name

        try:
            extract_card_content(page_path, card, output_path)
            extracted.append({
                'page': page_name,
                'card_number': idx,
                'clip_id': card['id'],
                'bbox': card,
                'output_file': output_name
            })
        except Exception as e:
            print(f"  ❌ Error extracting {card['id']}: {e}")

    return extracted


def main():
    """Main extraction process."""
    print("=" * 60)
    print("Move Card Extractor")
    print("=" * 60)

    # Create output directory
    OUTPUT_DIR.mkdir(exist_ok=True)

    # Find all page SVG files
    page_files = sorted(INPUT_DIR.glob("page-*.svg"))

    if not page_files:
        print(f"\n❌ No page-*.svg files found in {INPUT_DIR}")
        return

    print(f"\nFound {len(page_files)} page(s) to process")

    # Process each page
    all_extracted = []
    for page_path in page_files:
        extracted = process_page(page_path)
        all_extracted.extend(extracted)

    # Save metadata
    metadata_path = OUTPUT_DIR / "extraction_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(all_extracted, f, indent=2)

    print("\n" + "=" * 60)
    print(f"✅ Extraction complete!")
    print(f"   Total cards extracted: {len(all_extracted)}")
    print(f"   Output directory: {OUTPUT_DIR}")
    print(f"   Metadata saved: {metadata_path}")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review extracted cards in a browser or vector editor")
    print("2. Identify which move each card represents")
    print("3. Rename files to move notation (e.g., move_U.svg)")


if __name__ == "__main__":
    main()
