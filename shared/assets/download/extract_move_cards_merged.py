#!/usr/bin/env python3
"""
Extract individual move card diagrams from PDF-to-SVG converted pages.

FINAL VERSION: Merges overlapping clipPaths before extraction.
Each move card may have multiple clipPaths (main card + arrow clipping regions).
We merge these into a single bounding box per card.
"""

import re
import os
import json
from pathlib import Path
from xml.etree import ElementTree as ET

# Input/output directories
INPUT_DIR = Path("move_diagrams_from_pdf")
OUTPUT_DIR = Path("move_cards_final")

# Minimum dimensions to consider a valid move card
MIN_WIDTH = 150
MIN_HEIGHT = 150

# Position tolerance for grouping overlapping clipPaths (in pixels)
POSITION_TOLERANCE = 10

# SVG namespace
SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"


def parse_all_clippaths(svg_content):
    """
    Extract ALL clipPath bounding boxes from SVG (including small ones).
    We'll merge them later.
    """
    clippaths = []

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

        clippaths.append({
            'id': clip_id,
            'x': x_min,
            'y': y_min,
            'width': width,
            'height': height,
            'x_max': x_max,
            'y_max': y_max
        })

    return clippaths


def is_valid_move_card(width, height):
    """
    Check if dimensions match a valid move card.

    Valid move cards are portrait orientation with specific aspect ratio:
    - Width: 170-180px
    - Height: 255-265px
    - Aspect ratio: ~0.67 (portrait)
    """
    if height == 0:
        return False

    aspect = width / height

    return (
        width < height and           # Portrait orientation
        0.63 < aspect < 0.72 and     # Correct aspect ratio
        170 < width < 180 and        # Valid width range
        255 < height < 265           # Valid height range
    )


def merge_overlapping_bboxes(clippaths):
    """
    Merge overlapping clipPaths into single card bounding boxes.

    Strategy:
    1. Group clipPaths by approximate position (within POSITION_TOLERANCE)
    2. For each group, create merged bbox = union of all boxes
    3. Filter by dimensional criteria to keep only valid move cards
    """
    if not clippaths:
        return []

    # Sort by position for easier grouping
    sorted_clips = sorted(clippaths, key=lambda c: (c['y'], c['x']))

    # Group overlapping clipPaths
    groups = []
    current_group = [sorted_clips[0]]

    for clip in sorted_clips[1:]:
        # Check if this clip overlaps with current group
        # (within tolerance of any clip in the group)
        overlaps = False
        for group_clip in current_group:
            if (abs(clip['x'] - group_clip['x']) <= POSITION_TOLERANCE and
                abs(clip['y'] - group_clip['y']) <= POSITION_TOLERANCE):
                overlaps = True
                break

        if overlaps:
            current_group.append(clip)
        else:
            groups.append(current_group)
            current_group = [clip]

    # Add last group
    groups.append(current_group)

    # Merge each group into a single bounding box
    merged_cards = []
    for group in groups:
        # Find union of all boxes in group
        x_min = min(c['x'] for c in group)
        y_min = min(c['y'] for c in group)
        x_max = max(c['x_max'] for c in group)
        y_max = max(c['y_max'] for c in group)

        width = x_max - x_min
        height = y_max - y_min

        # Filter by dimensional criteria for valid move cards
        if is_valid_move_card(width, height):
            # Use first clipPath ID as reference
            merged_cards.append({
                'id': group[0]['id'],
                'clip_ids': [c['id'] for c in group],  # Track all merged IDs
                'x': x_min,
                'y': y_min,
                'width': width,
                'height': height,
                'x_max': x_max,
                'y_max': y_max
            })

    return merged_cards


def extract_numbers_from_string(text):
    """Extract all numeric values from a string."""
    if not text:
        return []
    numbers = re.findall(r'-?[0-9]+\.?[0-9]*', text)
    return [float(n) for n in numbers]


def get_element_coordinates(elem):
    """Extract coordinate values from an SVG element."""
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
        for i in range(0, len(numbers) - 1, 2):
            coords.append((numbers[i], numbers[i + 1]))

    # Check transform attribute
    transform = elem.get('transform')
    if transform:
        # Extract translate values
        translate_match = re.search(r'translate\(\s*(-?[0-9.]+)[,\s]+(-?[0-9.]+)\s*\)', transform)
        if translate_match:
            coords.append((float(translate_match.group(1)), float(translate_match.group(2))))

        # Extract matrix translation
        matrix_match = re.search(r'matrix\([^,]+,[^,]+,[^,]+,[^,]+,\s*(-?[0-9.]+)[,\s]+(-?[0-9.]+)\s*\)', transform)
        if matrix_match:
            coords.append((float(matrix_match.group(1)), float(matrix_match.group(2))))

    return coords


def element_in_bbox(elem, bbox):
    """Check if element's coordinates fall within the bounding box."""
    x_min, y_min = bbox['x'], bbox['y']
    x_max, y_max = bbox['x_max'], bbox['y_max']

    coords = get_element_coordinates(elem)

    for x, y in coords:
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True

    return False


def collect_elements_in_bbox(root, bbox):
    """Recursively collect all elements whose coordinates fall within the bbox."""
    elements = []

    for elem in root.iter():
        # Skip root svg element and defs
        if elem.tag.endswith('svg') or elem.tag.endswith('defs'):
            continue

        if element_in_bbox(elem, bbox):
            # Avoid adding both parent and child
            is_child_of_existing = False
            for existing in elements:
                if elem in list(existing.iter()):
                    is_child_of_existing = True
                    break

            if not is_child_of_existing:
                # Remove children if we're adding a parent
                elements_to_remove = []
                for existing in elements:
                    if existing in list(elem.iter()):
                        elements_to_remove.append(existing)

                for to_remove in elements_to_remove:
                    elements.remove(to_remove)

                elements.append(elem)

    return elements


def extract_card_content(svg_path, card, output_path):
    """Extract a single card using merged bounding box."""
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

    # Copy entire defs section
    defs = root.find(f'.//{{{SVG_NS}}}defs')
    if defs is not None:
        new_svg.append(defs)

    # Create main group with translation
    main_group = ET.SubElement(new_svg, 'g', {
        'transform': f"translate(-{card['x']:.6f}, -{card['y']:.6f})"
    })

    # Collect all elements within the bounding box
    content_elements = collect_elements_in_bbox(root, card)

    # Copy elements to main group
    for elem in content_elements:
        main_group.append(elem)

    # Write to file
    output_tree = ET.ElementTree(new_svg)
    ET.indent(output_tree, space='  ')
    output_tree.write(output_path, encoding='unicode', xml_declaration=True)

    clip_ids_str = ', '.join(card['clip_ids'])
    print(f"  ✓ Extracted {card['width']:.0f}×{card['height']:.0f}px ({len(content_elements)} elements) - merged from: {clip_ids_str}")


def process_page(page_path):
    """Process a single PDF page SVG and extract all move cards."""
    page_name = page_path.stem
    print(f"\n📄 Processing {page_name}...")

    # Read SVG content
    with open(page_path, 'r') as f:
        content = f.read()

    # Extract ALL clipPaths
    all_clippaths = parse_all_clippaths(content)
    print(f"  Found {len(all_clippaths)} clipPaths total")

    # Merge overlapping clipPaths
    merged_cards = merge_overlapping_bboxes(all_clippaths)
    print(f"  Merged into {len(merged_cards)} unique cards")

    if not merged_cards:
        print(f"  ⚠️  No move cards found after merging")
        return []

    # Sort cards by position
    cards_sorted = sorted(merged_cards, key=lambda c: (round(c['y'] / 50), c['x']))

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
                'clip_ids': card['clip_ids'],
                'bbox': {
                    'x': card['x'],
                    'y': card['y'],
                    'width': card['width'],
                    'height': card['height']
                },
                'output_file': output_name
            })
        except Exception as e:
            print(f"  ❌ Error extracting card {idx}: {e}")
            import traceback
            traceback.print_exc()

    return extracted


def main():
    """Main extraction process."""
    print("=" * 70)
    print("Move Card Extractor - Final Version (Merged ClipPaths)")
    print("=" * 70)

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

    print("\n" + "=" * 70)
    print(f"✅ Extraction complete!")
    print(f"   Total cards extracted: {len(all_extracted)}")
    print(f"   Output directory: {OUTPUT_DIR}")
    print(f"   Metadata saved: {metadata_path}")
    print("=" * 70)
    print("\nNext steps:")
    print("1. Open extracted SVG files in browser to verify complete content")
    print("2. Identify which move each card represents")
    print("3. Rename files to move notation (e.g., move_U.svg)")


if __name__ == "__main__":
    main()
