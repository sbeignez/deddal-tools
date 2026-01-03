#!/usr/bin/env python3
"""
Extract individual move card diagrams from PDF-to-SVG converted pages.

Version 3: Extract content by identifying element ranges between card clipPaths.

Strategy:
- Each card consists of background clipPath groups followed by content elements
- Content elements appear BETWEEN this card's clipPath and the next card's clipPath
- Extract all sibling elements in this range
"""

import re
import os
import json
from pathlib import Path
from xml.etree import ElementTree as ET

# Input/output directories
INPUT_DIR = Path("move_diagrams_from_pdf")
OUTPUT_DIR = Path("move_cards_extracted_v3")

# Minimum dimensions to consider a valid move card
MIN_WIDTH = 150
MIN_HEIGHT = 150

# SVG namespace
SVG_NS = "http://www.w3.org/2000/svg"


def parse_clippath_bbox(svg_content):
    """Extract bounding boxes from clipPath definitions."""
    cards = []

    # Pattern for rectangle coordinates
    pattern = r'<clipPath\s+id="(clip-\d+)">\s*<path[^>]+d="[Mm]\s*([0-9.]+)[,\s]+([0-9.]+)\s+[Ll]\s*([0-9.]+)[,\s]+([0-9.]+)\s+[Ll]\s*([0-9.]+)[,\s]+([0-9.]+)\s+[Ll]\s*([0-9.]+)[,\s]+([0-9.]+)\s*[Zz]'

    for match in re.finditer(pattern, svg_content, re.IGNORECASE):
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


def find_card_content_elements(root, card, all_card_ids):
    """
    Find all elements that belong to this card.

    Strategy:
    1. Find all groups with clip-path="url(#card_id)"
    2. Find the NEXT card's clipPath group (to know where content ends)
    3. Extract all sibling elements between this card and next card
    """
    clip_ref = f"url(#{card['id']})"
    elements = []

    # Get all top-level groups (direct children of root)
    all_groups = list(root)

    # Find index of first group with this card's clipPath
    start_idx = None
    for idx, elem in enumerate(all_groups):
        if elem.get('clip-path') == clip_ref:
            start_idx = idx
            break

    if start_idx is None:
        print(f"  ⚠️  Could not find clipPath group for {card['id']}")
        return elements

    # Find index of next card's clipPath (to know where to stop)
    end_idx = len(all_groups)  # Default to end of document
    for next_card_id in all_card_ids:
        if next_card_id == card['id']:
            continue
        next_clip_ref = f"url(#{next_card_id})"
        for idx in range(start_idx + 1, len(all_groups)):
            if all_groups[idx].get('clip-path') == next_clip_ref:
                end_idx = idx
                break
        if end_idx < len(all_groups):
            break

    # Extract all elements from start_idx to end_idx
    elements = all_groups[start_idx:end_idx]

    return elements


def extract_card_content(svg_path, card, all_cards, output_path):
    """
    Extract a single card with ALL content.
    """
    # Parse SVG
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Create new SVG root
    new_svg = ET.Element('svg', {
        'version': '1.1',
        'xmlns': SVG_NS,
        'xmlns:xlink': 'http://www.w3.org/1999/xlink',
        'width': f"{card['width']:.2f}",
        'height': f"{card['height']:.2f}",
        'viewBox': f"0 0 {card['width']:.2f} {card['height']:.2f}"
    })

    # Copy entire defs section
    defs = root.find(f'.//{{{SVG_NS}}}defs')
    if defs is not None:
        new_svg.append(defs)

    # Create main group with translation
    main_group = ET.SubElement(new_svg, 'g', {
        'transform': f"translate(-{card['x']:.6f}, -{card['y']:.6f})"
    })

    # Find all elements belonging to this card
    all_card_ids = [c['id'] for c in all_cards]
    content_elements = find_card_content_elements(root, card, all_card_ids)

    # Copy elements to main group
    for elem in content_elements:
        main_group.append(elem)

    # Write to file
    output_tree = ET.ElementTree(new_svg)
    ET.indent(output_tree, space='  ')
    output_tree.write(output_path, encoding='unicode', xml_declaration=True)

    print(f"  ✓ Extracted {card['id']}: {card['width']:.0f}×{card['height']:.0f}px ({len(content_elements)} elements)")


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
            extract_card_content(page_path, card, cards_sorted, output_path)
            extracted.append({
                'page': page_name,
                'card_number': idx,
                'clip_id': card['id'],
                'bbox': card,
                'output_file': output_name
            })
        except Exception as e:
            print(f"  ❌ Error extracting {card['id']}: {e}")
            import traceback
            traceback.print_exc()

    return extracted


def main():
    """Main extraction process."""
    print("=" * 60)
    print("Move Card Extractor v3 - Sequential Element Extraction")
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
    print("1. Open extracted SVG files in browser to verify content")
    print("2. Identify which move each card represents")
    print("3. Rename files to move notation (e.g., move_U.svg)")


if __name__ == "__main__":
    main()
