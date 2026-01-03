#!/usr/bin/env python3

import json
import sys

def populate_null_images():
    """Populate null image_asset_name values in JSON seed data"""

    # F2L FR cases
    print("📝 Updating F2L FR null values...")
    with open('Deddal/Data/Resources/SeedData/f2l_cases.json', 'r') as f:
        f2l_cases = json.load(f)

    updated = 0
    for case in f2l_cases:
        if case['code'].endswith('-FR') and case['image_asset_name'] is None:
            # Extract number: F2L-10-FR → 10
            num = case['code'].replace('F2L-', '').replace('-FR', '')
            case['image_asset_name'] = f"caseimg_3x3_cfop_f2l_{num}-fr"
            updated += 1

    with open('Deddal/Data/Resources/SeedData/f2l_cases.json', 'w') as f:
        json.dump(f2l_cases, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Updated {updated} F2L FR cases")
    print()

    # OLL cases
    print("📝 Updating OLL null values...")
    with open('Deddal/Data/Resources/SeedData/oll_cases.json', 'r') as f:
        oll_cases = json.load(f)

    updated = 0
    for case in oll_cases:
        if case['image_asset_name'] is None:
            # Extract number: OLL-1 → 1
            num = case['code'].replace('OLL-', '')
            case['image_asset_name'] = f"caseimg_3x3_cfop_oll_{num}"
            updated += 1

    with open('Deddal/Data/Resources/SeedData/oll_cases.json', 'w') as f:
        json.dump(oll_cases, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Updated {updated} OLL cases")
    print()

    # PLL cases
    print("📝 Updating PLL null values...")
    with open('Deddal/Data/Resources/SeedData/pll_cases.json', 'r') as f:
        pll_cases = json.load(f)

    updated = 0
    for case in pll_cases:
        if case['image_asset_name'] is None:
            # Extract perm name: PLL-Aa-Perm → aa-perm (lowercase)
            perm = case['code'].replace('PLL-', '').lower()
            case['image_asset_name'] = f"caseimg_3x3_cfop_pll_{perm}"
            updated += 1

    with open('Deddal/Data/Resources/SeedData/pll_cases.json', 'w') as f:
        json.dump(pll_cases, f, indent=2, ensure_ascii=False)
    print(f"  ✅ Updated {updated} PLL cases")
    print()

    print("════════════════════════════════════════")
    print("✅ All null image_asset_name values populated!")
    print("════════════════════════════════════════")

    # Verify
    print()
    print("Verification:")
    with open('Deddal/Data/Resources/SeedData/f2l_cases.json', 'r') as f:
        f2l = json.load(f)
        f2l_nulls = sum(1 for c in f2l if c['image_asset_name'] is None)
        print(f"  F2L nulls: {f2l_nulls}")

    with open('Deddal/Data/Resources/SeedData/oll_cases.json', 'r') as f:
        oll = json.load(f)
        oll_nulls = sum(1 for c in oll if c['image_asset_name'] is None)
        print(f"  OLL nulls: {oll_nulls}")

    with open('Deddal/Data/Resources/SeedData/pll_cases.json', 'r') as f:
        pll = json.load(f)
        pll_nulls = sum(1 for c in pll if c['image_asset_name'] is None)
        print(f"  PLL nulls: {pll_nulls}")

if __name__ == '__main__':
    populate_null_images()
