#!/usr/bin/env python3
"""
Auto-categorize F2L cases with new 7-category recognition system.

Analyzes existing descriptions and generates new category tags:
1. corner_position
2. edge_position
3. edge_orientation
4. piece_location
5. top_color_pattern
6. pair_u_relationship
7. solve_approach
"""

import json
from pathlib import Path

# Path to F2L cases JSON
F2L_JSON_PATH = Path(__file__).parent.parent.parent / "Deddal/Data/Resources/SeedData/3x3_cfop_f2l_cases.json"

def parse_description(desc):
    """Parse existing description into category values."""
    if not desc or desc == "No description":
        return None

    # Description format: "{Connection} - {Color} - {EO}"
    # Examples:
    # "Connected - Same Colour on Top - Good EO"
    # "Slotted - Corner in Slot - Bad EO"

    parts = [p.strip() for p in desc.split(' - ')]
    if len(parts) != 3:
        return None

    connection, color, eo = parts

    result = {}

    # Parse piece_location and piece positions
    if connection == "Connected":
        result['piece_location'] = "both_in_u"
        result['corner_position'] = "u_layer"
        result['edge_position'] = "u_layer"
        result['pair_u_relationship'] = "connected"

    elif connection == "Disconnected":
        result['piece_location'] = "both_in_u"
        result['corner_position'] = "u_layer"
        result['edge_position'] = "u_layer"
        result['pair_u_relationship'] = "separated"

    elif "Slotted" in connection:
        if "Both Pieces in Slot" in color:
            result['piece_location'] = "both_slotted_together"
            result['corner_position'] = "in_slot"
            result['edge_position'] = "in_slot"
            result['pair_u_relationship'] = "n/a"
            result['top_color_pattern'] = "n/a"

        elif "Corner in Slot" in color:
            result['piece_location'] = "corner_slotted"
            result['corner_position'] = "in_slot"
            result['edge_position'] = "u_layer"  # Edge must be in U if corner is slotted
            result['pair_u_relationship'] = "n/a"
            result['top_color_pattern'] = "n/a"

        elif "Edge in Slot" in color:
            result['piece_location'] = "edge_slotted"
            result['corner_position'] = "u_layer"  # Corner must be in U if edge is slotted
            result['edge_position'] = "in_slot"
            result['pair_u_relationship'] = "n/a"
            result['top_color_pattern'] = "n/a"

    # Parse top_color_pattern (only for both_in_u cases)
    if result.get('piece_location') == "both_in_u":
        if "Same Colour on Top" in color:
            result['top_color_pattern'] = "same_colors"
        elif "Different Colours on Top" in color:
            result['top_color_pattern'] = "different_colors"
        elif "Cross Colour on Top" in color:
            result['top_color_pattern'] = "cross_color_up"

    # Parse edge_orientation
    if "Good EO" in eo:
        result['edge_orientation'] = "oriented"
    elif "Bad EO" in eo:
        result['edge_orientation'] = "flipped"

    return result

def infer_solve_approach(categories):
    """Infer solve approach from other categories."""
    piece_loc = categories.get('piece_location')
    pair_rel = categories.get('pair_u_relationship')
    color_pat = categories.get('top_color_pattern')

    # Simple heuristics (can be refined later)
    if piece_loc == "both_in_u":
        if pair_rel == "connected":
            if color_pat == "cross_color_up":
                return "complex"  # Weird cases
            else:
                return "direct_insert"  # Basic insertions or split
        elif pair_rel == "separated":
            return "hide_reposition"  # Hide corner, position edge

    elif piece_loc in ["corner_slotted", "edge_slotted", "both_slotted_together"]:
        return "extract_rebuild"  # Extract from slot

    return "complex"  # Default to complex for unknown

def categorize_all_cases():
    """Categorize all 82 F2L cases."""
    # Load JSON
    with open(F2L_JSON_PATH, 'r') as f:
        cases = json.load(f)

    print(f"Loaded {len(cases)} F2L cases")
    print("\n" + "="*80)
    print("Pass 1: Categorizing FR cases...")
    print("="*80)

    categorized_count = 0
    missing_desc_count = 0

    # Pass 1: Categorize all FR cases first
    for case in cases:
        code = case['code']
        desc = case.get('description')
        slot = case.get('groups', [])[0].split(':')[1] if case.get('groups') else 'unknown'

        # Skip FL cases in pass 1
        if slot == 'FL':
            continue

        # Parse existing description
        parsed = parse_description(desc)

        if parsed:
            # Add solve_approach
            parsed['solve_approach'] = infer_solve_approach(parsed)

            # Build new groups array
            new_groups = []

            # Keep only existing basic groups (slot, level) - remove old categories
            old_categories = ['technique', 'piece_location', 'corner_position', 'edge_position',
                            'pair_u_relationship', 'top_color_pattern', 'edge_orientation', 'solve_approach']
            for g in case.get('groups', []):
                category = g.split(':')[0]
                if category not in old_categories:  # Keep only slot and level
                    new_groups.append(g)

            # Add new categories
            for category, value in parsed.items():
                new_groups.append(f"{category}:{value}")

            case['groups'] = new_groups
            categorized_count += 1

            print(f"✓ {code}: {len(new_groups)} groups")

        else:
            print(f"⚠️  {code}: No description")
            missing_desc_count += 1

    # Pass 2: Mirror FR → FL
    print("\n" + "="*80)
    print("Pass 2: Mirroring FR → FL cases...")
    print("="*80)

    for case in cases:
        code = case['code']
        slot = code.split('-')[-1]  # Get FL or FR from code

        if slot == 'FL':
            # Find corresponding FR case
            fr_code = code.replace('-FL', '-FR')
            fr_case = next((c for c in cases if c['code'] == fr_code), None)

            if fr_case and fr_case.get('groups'):
                # Copy groups from FR, but change slot
                new_groups = []
                for g in fr_case.get('groups', []):
                    if g.startswith('slot:'):
                        new_groups.append('slot:FL')
                    else:
                        new_groups.append(g)

                case['groups'] = new_groups
                categorized_count += 1
                print(f"✓ {code}: Mirrored from {fr_code} ({len(new_groups)} groups)")
            else:
                print(f"⚠️  {code}: No FR mirror found for {fr_code}")
                missing_desc_count += 1

    print("\n" + "="*80)
    print("Summary:")
    print("="*80)
    print(f"Categorized: {categorized_count}/{len(cases)}")
    print(f"Missing: {missing_desc_count}/{len(cases)}")

    # Save updated JSON
    with open(F2L_JSON_PATH, 'w') as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Updated JSON saved to: {F2L_JSON_PATH}")

    # Show sample case
    if cases:
        print("\n" + "="*80)
        print("Sample categorized case:")
        print("="*80)
        sample = next((c for c in cases if c['code'] == 'F2L-01-FR'), cases[0])
        print(f"Code: {sample['code']}")
        print(f"Description: {sample.get('description', 'N/A')}")
        print(f"Groups ({len(sample.get('groups', []))}):")
        for g in sample.get('groups', []):
            print(f"  - {g}")

if __name__ == "__main__":
    categorize_all_cases()
