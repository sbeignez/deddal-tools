#!/usr/bin/env python3
"""
Update Case Codes In-Place

Updates existing iOS seed data JSON files to use new PUZZLE-METHOD-CASESET prefixed codes.
Applies the same transformation logic as the SQL migration 20251208140000.

This is faster than re-exporting entire datasets.
"""

import json
import os
from pathlib import Path
from typing import Dict, List

# Seed data directory
SEED_DATA_DIR = Path(__file__).parent.parent / "DeddalInfra/Infrastructure/Persistence/SeedData"

def transform_case_code(code: str) -> str:
    """
    Transform case code to include PUZZLE-METHOD-CASESET prefix.

    Mirrors the logic from SQL migration 20251208140000_add_puzzle_method_case_prefixes.sql
    """
    # Already has prefix (from previous run or already migrated)
    if code.startswith(('2X2-', '3X3-', '4X4-', '5X5-', '6X6-', '7X7-')):
        return code

    # NxN Parity Codes (normalize lowercase to uppercase)
    if code.startswith('4x4-'):
        return code[:3].upper() + code[3:]
    if code.startswith('5x5-'):
        return code[:3].upper() + code[3:]
    if code.startswith('6x6-'):
        return code[:3].upper() + code[3:]
    if code.startswith('7x7-'):
        return code[:3].upper() + code[3:]

    # 3x3 CFOP - F2L
    if code.startswith('F2L-'):
        return f'3X3-CFOP-{code}'

    # 3x3 CFOP - OLL
    if code.startswith('OLL-'):
        return f'3X3-CFOP-{code}'

    # 3x3 CFOP - PLL (pattern: {CASE}-Perm)
    if '-Perm' in code and not code.startswith(('4X4-', '6X6-', '4x4-', '6x6-')):
        # Normalize to uppercase PERM
        return f'3X3-CFOP-PLL-{code.replace("-Perm", "-PERM").upper()}'

    # 2x2 - CLL Method
    if code.startswith('CLL-'):
        return f'2X2-{code}'

    # 2x2 - Ortega Method
    if code.startswith('ORTEGA-'):
        return f'2X2-{code}'

    # 2x2 - Ortega Method (mixed case - normalize)
    if code.startswith('Ortega-'):
        # Extract part after first hyphen and uppercase it
        suffix = code.split('-', 1)[1].upper()
        return f'2X2-ORTEGA-{suffix}'

    # 3x3 - Layer-by-Layer Method
    if code.startswith('3x3_cross_'):
        suffix = code[len('3x3_cross_'):].upper()
        return f'3X3-LBL-CROSS-{suffix}'

    if code.startswith('3x3_lbl_'):
        suffix = code[len('3x3_lbl_'):].upper()
        return f'3X3-LBL-{suffix}'

    # 3x3 - Advanced Last Layer Subsets (hyphen-separated)
    advanced_prefixes = ['OCLL-', 'PCLL-', 'COLL-', 'ZBLL-', 'PELL-', 'OELL-']
    for prefix in advanced_prefixes:
        # Check case-insensitively
        if code.upper().startswith(prefix):
            # Normalize to uppercase prefix
            normalized_code = code.upper()[:len(prefix)] + code[len(prefix):]
            return f'3X3-{normalized_code}'

    # 3x3 - Advanced Last Layer Subsets (space-separated)
    # OcLL Sune → 3X3-OCLL-SUNE
    # PeLL Ua → 3X3-PELL-UA
    for prefix in ['OcLL ', 'OCLL ', 'OeLL ', 'OELL ', 'PcLL ', 'PCLL ', 'PeLL ', 'PELL ', 'COLL ']:
        if code.startswith(prefix):
            # Extract prefix (first 4 chars) and normalize
            case_prefix = prefix.strip().upper()
            # Extract suffix after space and replace spaces with hyphens, uppercase
            suffix = code.split(' ', 1)[1].replace(' ', '-').upper()
            return f'3X3-{case_prefix}-{suffix}'

    # Fallback - code couldn't be transformed
    print(f"  ⚠️  WARNING: Could not transform code: {code}")
    return code


def update_case_file(filepath: Path) -> Dict[str, int]:
    """
    Update case codes in a single JSON file.

    Returns:
        Statistics: {'total': int, 'updated': int, 'unchanged': int, 'warnings': int}
    """
    print(f"\nProcessing {filepath.name}...")

    with open(filepath, 'r') as f:
        cases = json.load(f)

    stats = {'total': len(cases), 'updated': 0, 'unchanged': 0, 'warnings': 0}

    for case in cases:
        old_code = case['code']
        new_code = transform_case_code(old_code)

        if new_code != old_code:
            case['code'] = new_code
            stats['updated'] += 1
            print(f"  ✓ {old_code} → {new_code}")
        else:
            stats['unchanged'] += 1

        if 'WARNING' in new_code or new_code == old_code and not new_code.startswith(('2X2-', '3X3-', '4X4-', '5X5-', '6X6-', '7X7-')):
            stats['warnings'] += 1

    # Write updated file
    with open(filepath, 'w') as f:
        json.dump(cases, f, indent=2, ensure_ascii=False)

    print(f"  Total: {stats['total']} | Updated: {stats['updated']} | Unchanged: {stats['unchanged']}")

    if stats['warnings'] > 0:
        print(f"  ⚠️  {stats['warnings']} codes could not be transformed")

    return stats


def main():
    """Update all case seed data files."""
    print("=" * 70)
    print("Update Case Codes In-Place")
    print("=" * 70)
    print(f"Seed data directory: {SEED_DATA_DIR}")

    if not SEED_DATA_DIR.exists():
        print(f"\n❌ ERROR: Seed data directory not found: {SEED_DATA_DIR}")
        return 1

    # Find all case JSON files (not algorithm files)
    case_files = sorted([
        f for f in SEED_DATA_DIR.glob("seeddata_cases_*.json")
        if not f.name.startswith("seeddata_algorithms_")
    ])

    if not case_files:
        print("\n❌ No case seed data files found")
        return 1

    print(f"\nFound {len(case_files)} case files to update:")
    for f in case_files:
        print(f"  - {f.name}")

    # Process each file
    total_stats = {'total': 0, 'updated': 0, 'unchanged': 0, 'warnings': 0}

    for filepath in case_files:
        stats = update_case_file(filepath)
        total_stats['total'] += stats['total']
        total_stats['updated'] += stats['updated']
        total_stats['unchanged'] += stats['unchanged']
        total_stats['warnings'] += stats['warnings']

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Files processed: {len(case_files)}")
    print(f"Total cases: {total_stats['total']}")
    print(f"Codes updated: {total_stats['updated']}")
    print(f"Codes unchanged: {total_stats['unchanged']}")
    print(f"Warnings: {total_stats['warnings']}")

    if total_stats['warnings'] == 0:
        print("\n✅ All case codes successfully updated!")
        return 0
    else:
        print(f"\n⚠️  {total_stats['warnings']} codes could not be transformed - manual review needed")
        return 1


if __name__ == '__main__':
    exit(main())
