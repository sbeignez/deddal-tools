#!/usr/bin/env python3
"""
Extract individual move card diagrams from PDF-to-SVG converted pages.

CORRECT APPROACH: Use spatial filtering to include only elements whose
coordinates fall within each card's bounding box (x, y, x+width, y+height).
"""

import re
import os
import json
from pathlib import Path
from xml.etree import ElementTree as ET

# Input/output directories
INPUT_DIR = Path("move_diagrams_from_pdf")
OUTPUT_DIR = Path("move_cards_extracted_final")

# Minimum dimensions to consider a valid move card
MIN_WIDTH = 150
MIN_HEIGHT = 150

# SVG namespace
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"


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
                'height': height,
                'x_max': x_max,
                'y_max': y_max
            })

    return cards


def extract_numbers_from_string(text):
    """Extract all numeric values from a string."""
    if not text:
        return []
    # Match both integer and decimal numbers, including negative
    numbers = re.findall(r'-?[0-9]+\.?[0-9]*', text)
    return [float(n) for n in numbers]


def get_element_coordinates(elem):
    """
    Extract coordinate values from an SVG element.
    Returns a list of (x, y) tuples found in the element.
    """
    coords = []

    # Check common position attributes
    if elem.get('x') and elem.get('y'):
        try:
            coords.append((float(elem.get('x')), float(elem.get('y'))))
        except ValueError:
            pass

    if elem.get('cx') and elem.get('cy'):
        try:
            coords.append((float(elem.get('cx')), float(elem.get('cy'))))
        except ValueError:
            pass

    # Check path data
    d = elem.get('d')
    if d:
        numbers = extract_numbers_from_string(d)
        # Group numbers into (x, y) pairs
        for i in range(0, len(numbers) - 1, 2):
            coords.append((numbers[i], numbers[i + 1]))

    # Check transform attribute
    transform = elem.get('transform')
    if transform:
        # Extract translate values
        translate_match = re.search(r'translate\(\s*(-?[0-9.]+)[,\s]+(-?[0-9.]+)\s*\)', transform)
        if translate_match:
            coords.append((float(translate_match.group(1)), float(translate_match.group(2))))

        # Extract matrix translation (last two values)
        matrix_match = re.search(r'matrix\([^,]+,[^,]+,[^,]+,[^,]+,\s*(-?[0-9.]+)[,\s]+(-?[0-9.]+)\s*\)', transform)
        if matrix_match:
            coords.append((float(matrix_match.group(1)), float(matrix_match.group(2))))

    return coords


def element_in_bbox(elem, bbox):
    """
    Check if element's coordinates fall within the bounding box.
    Returns True if ANY coordinate of the element is inside the bbox.
    """
    x_min, y_min = bbox['x'], bbox['y']
    x_max, y_max = bbox['x_max'], bbox['y_max']

    # Get all coordinates from this element
    coords = get_element_coordinates(elem)

    # Check if any coordinate falls within the bbox
    for x, y in coords:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True

    return False


def collect_elements_in_bbox(root, bbox):
    """
    Recursively collect all elements whose coordinates fall within the bbox.
    """
    elements = []

    # Iterate through all elements in the SVG
    for elem in root.iter():
        # Skip the root svg element and defs
        if elem.tag.endswith('svg') or elem.tag.endswith('defs'):
            continue

        # Check if this element's coordinates are in the bbox
        if element_in_bbox(elem, bbox):
            # Check if we haven't already added a parent of this element
            is_child_of_existing = False
            for existing in elements:
                # Check if elem is a descendant of existing
                if elem in list(existing.iter()):
                    is_child_of_existing = True
                    break

            if not is_child_of_existing:
                # Check if any existing element is a child of this one
                elements_to_remove = []
                for existing in elements:
                    if existing in list(elem.iter()):
                        elements_to_remove.append(existing)

                for to_remove in elements_to_remove:
                    elements.remove(to_remove)

                elements.append(elem)

    return elements


def extract_card_content(svg_path, card, output_path):
    """
    Extract a single card by collecting all elements within its bounding box.
    """
    # Parse SVG
    tree = ET.parse(svg_path)
    root = tree.getroot()

    # Create new SVG root
    new_svg = ET.Element('svg', {
        'version': '1.1',
        'xmlns': SVG_NS,
        'xmlns:xlink': XLINK_NS,
        'width': f"{card['width']:.2f}",
        'height': f"{card['height']:.2f}",
        'viewBox': f"0 0 {card['width']:.2f} {card['height']:.2f}"
    })

    # Copy entire defs section (needed for clipPaths, gradients, glyphs)
    defs = root.find(f'.//{{{SVG_NS}}}defs')
    if defs is not None:
        new_svg.append(defs)

    # Create main group with translation to move content to origin
    main_group = ET.SubElement(new_svg, 'g', {
        'transform': f"translate(-{card['x']:.6f}, -{card['y']:.6f})"
    })

    # Collect all elements within the bounding box
    content_elements = collect_elements_in_bbox(root, card)

    print(f"  ✓ Found {len(content_elements)} elements in bbox for {card['id']}")

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
            extract_card_content(page_path, card, output_path)
            extracted.append({
                'page': page_name,
                'card_number': idx,
                'clip_id': card['id'],
                'bbox': {
                    'x': card['x'],
                    'y': card['y'],
                    'width': card['width'],
                    'height': card['height']
                },
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
    print("Move Card Extractor - Spatial Filtering")
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
