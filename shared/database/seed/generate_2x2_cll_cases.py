#!/usr/bin/env python3
"""
Generate 2x2 CLL cases JSON from scraped SpeedSolving.com HTML data.
Parses the index page to extract all 42 cases with their scrambles.
"""

import json
import uuid
import re
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser
import urllib.parse

# UUID v5 namespace for deterministic UUIDs
NAMESPACE = uuid.NAMESPACE_DNS

# CLL family mapping (based on existing 2x2_cll.sh structure)
# Family assignments from visual inspection and standard CLL organization
CLL_FAMILIES = {
    # AS (Anti-Sune) - 6 cases
    1: "AS", 2: "AS", 3: "AS", 4: "AS", 5: "AS", 6: "AS",
    # H - 4 cases
    7: "H", 8: "H", 9: "H", 10: "H",
    # L - 6 cases
    11: "L", 12: "L", 13: "L", 14: "L", 15: "L", 16: "L",
    # Pi - 6 cases
    17: "Pi", 18: "Pi", 19: "Pi", 20: "Pi", 21: "Pi", 22: "Pi",
    # Sune - 6 cases
    23: "Sune", 24: "Sune", 25: "Sune", 26: "Sune", 27: "Sune", 28: "Sune",
    # T - 6 cases
    29: "T", 30: "T", 31: "T", 32: "T", 33: "T", 34: "T",
    # U - 6 cases
    35: "U", 36: "U", 37: "U", 38: "U", 39: "U", 40: "U",
    # Pure permutation cases (corners oriented, need permutation only)
    # These are PBL-equivalent cases sometimes excluded from "true COLL"
    41: "PBL-Adj", 42: "PBL-Diag"
}

def generate_case_uuid(case_code):
    """Generate deterministic UUID v5 for a case"""
    name = f"deddal.case.{case_code.lower()}"
    return str(uuid.uuid5(NAMESPACE, name))

def generate_caseset_uuid(code):
    """Generate deterministic UUID v5 for a case set"""
    name = f"deddal.caseset.{code.lower()}"
    return str(uuid.uuid5(NAMESPACE, name))

def parse_cll_index_html(html_path):
    """
    Parse 2x2-CLL.html index page to extract all 42 cases.
    Returns list of dicts with case_number and scramble.
    """
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    cases = []

    # Find all case links with cid parameter
    # Pattern: href='...&amp;cid=1' or &cid=1
    cid_pattern = re.compile(r'cid=(\d+)')

    # Extract scrambles from HTML comments (most reliable)
    # Pattern: <!--R U R' U R U2 R'-->
    comment_pattern = re.compile(r'<!--(.+?)-->')

    # Find all table cell sections containing case data
    td_blocks = re.findall(r'<td>.*?</td>', html_content, re.DOTALL)

    for td_block in td_blocks:
        # Extract case ID from link
        cid_match = cid_pattern.search(td_block)
        if not cid_match:
            continue

        case_number = int(cid_match.group(1))

        # Extract scramble from HTML comment (most reliable source)
        comment_match = comment_pattern.search(td_block)
        if comment_match:
            scramble = comment_match.group(1).strip()
        else:
            # Fallback: try to extract from img alt attribute
            alt_match = re.search(r'alt="([^"]+)"', td_block)
            if alt_match:
                scramble = alt_match.group(1).strip()
            else:
                print(f"Warning: No scramble found for case #{case_number}")
                scramble = ""

        cases.append({
            'case_number': case_number,
            'scramble': scramble
        })

    return sorted(cases, key=lambda x: x['case_number'])

def create_case_json(case_data, case_set_id):
    """Convert parsed case data to JSON format"""
    case_number = case_data['case_number']
    family = CLL_FAMILIES.get(case_number, "Unknown")

    # Determine family index (e.g., AS-1, AS-2, ...)
    family_cases = [k for k, v in CLL_FAMILIES.items() if v == family]
    family_index = family_cases.index(case_number) + 1 if case_number in family_cases else case_number

    code = f"CLL-{family}-{family_index}"
    case_id = generate_case_uuid(code)

    # Family descriptions
    family_descriptions = {
        "AS": "Anti-Sune pattern on last layer",
        "H": "H pattern on last layer",
        "L": "L pattern on last layer",
        "Pi": "Pi pattern on last layer",
        "Sune": "Sune pattern on last layer",
        "T": "T pattern on last layer",
        "U": "U pattern on last layer",
        "PBL-Adj": "Adjacent corner swap (pure permutation, PBL equivalent)",
        "PBL-Diag": "Diagonal corner swap (pure permutation, PBL equivalent)"
    }

    # Family difficulty (rough estimate)
    family_difficulty = {
        "AS": 2, "Sune": 2, "U": 2, "T": 3, "H": 3, "L": 3, "Pi": 3,
        "PBL-Adj": 1, "PBL-Diag": 1  # Easier since they're just PBL
    }

    # Popularity estimate (higher for common families)
    family_popularity = {
        "AS": 80, "Sune": 80, "U": 70, "T": 70, "H": 65, "L": 65, "Pi": 60,
        "PBL-Adj": 40, "PBL-Diag": 40  # Less common in CLL practice
    }

    # Special handling for PBL-equivalent cases
    is_pbl_case = family.startswith("PBL")

    groups = [
        "puzzle:2x2",
        f"family:{family.lower()}",
        "level:advanced",
        "method:cll"
    ]

    # Add appropriate tags based on case type
    if is_pbl_case:
        groups.append("corners:pure_permutation")
        groups.append("pbl_equivalent")
        groups.append("often_excluded")
    else:
        groups.append("corners:permutation_and_orientation")

    return {
        "id": case_id,
        "code": code,
        "case_set_id": case_set_id,
        "title": f"{family} {family_index}",
        "long_name": f"2×2 CLL {family} {family_index}",
        "kind": "cll",
        "pattern_from": "First Layer Complete",
        "pattern_to": "Cube Solved",
        "scramble": case_data['scramble'],
        "notes": "Pure permutation case (PBL equivalent)" if is_pbl_case else "",
        "story": "",
        "description": family_descriptions.get(family, ""),
        "image_asset_name": "",  # No images for now
        "difficulty": family_difficulty.get(family, 3),
        "popularity": family_popularity.get(family, 50),
        "created_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "groups": groups
    }

def main():
    """Main execution"""
    # Paths
    html_path = Path("/Users/trophee-mini/code/deddal/deddal-explore/data/01-raw/site_speedsolving.com/2025-12-01_alt/html/2x2-CLL.html")
    output_dir = Path("/Users/trophee-mini/code/deddal/deddal-ios/Deddal/Data/Resources/SeedData")

    print("="*60)
    print("2×2 CLL Cases JSON Generator")
    print("="*60)

    # Generate case set UUID
    case_set_id = generate_caseset_uuid("2x2-cll")
    print(f"\nCase Set ID: {case_set_id}")

    # Parse HTML
    print(f"\nParsing HTML from: {html_path}")
    if not html_path.exists():
        print(f"ERROR: HTML file not found at {html_path}")
        return

    cases_raw = parse_cll_index_html(html_path)
    print(f"Found {len(cases_raw)} cases")

    # Convert to JSON format
    cases_json = []
    for case_data in cases_raw:
        case_json = create_case_json(case_data, case_set_id)
        cases_json.append(case_json)
        print(f"  Case #{case_data['case_number']:2d}: {case_json['code']:12s} - {case_json['scramble'][:30]}")

    # Write cases JSON
    cases_output_path = output_dir / "2x2_cll_cases.json"
    with open(cases_output_path, 'w', encoding='utf-8') as f:
        json.dump(cases_json, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Written {len(cases_json)} cases to: {cases_output_path}")

    # Family distribution
    print("\nFamily Distribution:")
    families = {}
    for case in cases_json:
        family = case['title'].split()[0]
        families[family] = families.get(family, 0) + 1

    for family, count in sorted(families.items()):
        print(f"  {family:10s}: {count} cases")

    print("\n" + "="*60)
    print(f"Total: {len(cases_json)} CLL cases generated")
    print(f"Case Set ID: {case_set_id}")
    print("="*60)

if __name__ == "__main__":
    main()
