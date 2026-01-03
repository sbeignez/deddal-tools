#!/usr/bin/env python3
"""
Update index.json with new story metadata for F2L-FR, PLL, OLL, OeLL, and PcLL stories.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

# Base path for stories
STORIES_BASE = Path("/Users/trophee-mini/code/deddal/deddal-ios/Resources/Stories")
INDEX_FILE = STORIES_BASE / "index.json"

# Timestamp for new entries
TIMESTAMP = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

def count_words(file_path):
    """Count words in a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return len(content.split())

def create_f2l_entries():
    """Create entries for new F2L-FR stories."""
    entries = []

    # F2L-04, 05, 06, 07, 08
    f2l_codes = [
        ("F2L-04-FR", "separated", "good-eo"),
        ("F2L-05-FR", "separated", "same-color"),
        ("F2L-06-FR", "separated", "bad-eo"),
        ("F2L-07-FR", "separated", "setup-pair"),
        ("F2L-08-FR", "separated", "same-top"),
        ("F2L-11-FR", "separated", "different-color"),
        ("F2L-12-FR", "separated", "corner-first"),
        ("F2L-13-FR", "separated", "edge-first"),
        ("F2L-14-FR", "separated", "bad-setup"),
        ("F2L-15-FR", "connected", "ready-insert"),
        ("F2L-16-FR", "connected", "extract-pair"),
        ("F2L-17-FR", "connected", "hide-corner"),
        ("F2L-18-FR", "connected", "bad-eo"),
        ("F2L-19-FR", "connected", "split-pair"),
        ("F2L-21-FR", "separated", "opposite-colors"),
        ("F2L-22-FR", "separated", "hide-edge"),
        ("F2L-23-FR", "separated", "sexy-setup"),
        ("F2L-24-FR", "separated", "double-sexy"),
        ("F2L-25-FR", "corner-in", "edge-above"),
        ("F2L-26-FR", "corner-in", "bad-eo"),
        ("F2L-27-FR", "corner-in", "good-eo"),
        ("F2L-28-FR", "corner-in", "split-insert"),
        ("F2L-29-FR", "corner-in", "sledge"),
        ("F2L-30-FR", "corner-in", "hedge"),
        ("F2L-31-FR", "edge-in", "corner-above"),
        ("F2L-32-FR", "edge-in", "split"),
        ("F2L-33-FR", "edge-in", "insert"),
        ("F2L-34-FR", "both-in", "wrong-slot"),
        ("F2L-35-FR", "both-in", "extract"),
        ("F2L-36-FR", "both-in", "rotate"),
        ("F2L-38-FR", "separated", "advanced"),
        ("F2L-39-FR", "separated", "multi-step"),
        ("F2L-40-FR", "separated", "fast-setup"),
        ("F2L-41-FR", "both-in", "complex"),
        ("F2L-42-FR", "both-in", "reinsert")
    ]

    for code, tag1, tag2 in f2l_codes:
        # Keep the hyphen before slot (e.g., f2l_04-fr.md not f2l_04_fr.md)
        file_name = f"3x3_cfop_f2l_{code.lower().replace('f2l-', '')}.md"
        file_path_str = f"3x3/cfop/f2l/{file_name}"
        full_path = STORIES_BASE / file_path_str

        word_count = count_words(full_path) if full_path.exists() else 220

        entries.append({
            "puzzle": "3x3",
            "method": "cfop",
            "case_set": "f2l",
            "case_code": code,
            "file_name": file_name,
            "file_path": file_path_str,
            "author": "Trophee Ltd",
            "last_modified": TIMESTAMP,
            "tags": [tag1, tag2],
            "word_count": word_count
        })

    return entries

def create_pll_entries():
    """Create entries for new PLL stories."""
    entries = []

    pll_codes = [
        ("Na-Perm", "edges-corners", "cycle"),
        ("Nb-Perm", "edges-corners", "cycle"),
        ("Ra-Perm", "edges-corners", "adjacent"),
        ("Rb-Perm", "edges-corners", "adjacent"),
        ("Ua-Perm", "edges", "anti-clockwise"),
        ("Ub-Perm", "edges", "clockwise"),
        ("V-Perm", "edges-corners", "diagonal"),
        ("Y-Perm", "corners", "diagonal"),
        ("Z-Perm", "edges", "adjacent-swap")
    ]

    for code, tag1, tag2 in pll_codes:
        # Keep the hyphen (e.g., pll_na-perm.md not pll_na_perm.md)
        file_name = f"3x3_cfop_pll_{code.lower()}.md"
        file_path_str = f"3x3/cfop/pll/{file_name}"
        full_path = STORIES_BASE / file_path_str

        word_count = count_words(full_path) if full_path.exists() else 180

        entries.append({
            "puzzle": "3x3",
            "method": "cfop",
            "case_set": "pll",
            "case_code": code,
            "file_name": file_name,
            "file_path": file_path_str,
            "author": "Trophee Ltd",
            "last_modified": TIMESTAMP,
            "tags": ["pll", tag1, tag2],
            "word_count": word_count
        })

    return entries

def create_oll_entries():
    """Create entries for new OLL stories (OLL-04 through OLL-57)."""
    entries = []

    # OLL shape and pattern tags
    oll_tags = {
        4: ("square", "right"), 5: ("square", "left"), 6: ("square", "W"), 7: ("square", "W"),
        8: ("square", "W"), 9: ("fish", "right"), 10: ("fish", "left"),
        11: ("lightning", "right"), 12: ("lightning", "left"),
        13: ("c-shape", "right"), 14: ("c-shape", "left"), 15: ("c-shape", "right"), 16: ("c-shape", "left"),
        17: ("dot", "corners"), 18: ("dot", "corners"), 19: ("dot", "corners"), 20: ("dot", "corners"),
        21: ("cross", "h-shape"), 22: ("cross", "pi-shape"), 23: ("cross", "headlights"), 24: ("cross", "t-shape"),
        25: ("cross", "l-shape"), 26: ("cross", "antisune"), 27: ("cross", "sune"),
        28: ("line", "corners"), 29: ("line", "w-shape"), 30: ("line", "c-shape"), 31: ("line", "p-shape"),
        32: ("line", "w-shape"), 33: ("line", "t-shape"), 34: ("line", "c-shape"), 35: ("line", "fish"),
        36: ("line", "w-shape"), 37: ("fish", "front"), 38: ("fish", "back"),
        39: ("lightning", "big"), 40: ("lightning", "big"),
        41: ("dot", "awkward"), 42: ("dot", "awkward"), 43: ("p-shape", "right"), 44: ("p-shape", "left"),
        45: ("line", "vertical"), 46: ("line", "horizontal"),
        47: ("square", "right"), 48: ("square", "left"),
        49: ("square", "W"), 50: ("square", "W"),
        51: ("i-shape", "vertical"), 52: ("i-shape", "horizontal"),
        53: ("square", "small"), 54: ("square", "small"),
        55: ("i-shape", "front"), 56: ("i-shape", "back"), 57: ("line", "gun")
    }

    for num in range(4, 58):
        code = f"OLL-{num}"
        tag1, tag2 = oll_tags.get(num, ("oll", "pattern"))

        file_name = f"3x3_cfop_oll_{num:02d}.md"
        file_path_str = f"3x3/cfop/oll/{file_name}"
        full_path = STORIES_BASE / file_path_str

        word_count = count_words(full_path) if full_path.exists() else 190

        entries.append({
            "puzzle": "3x3",
            "method": "cfop",
            "case_set": "oll",
            "case_code": code,
            "file_name": file_name,
            "file_path": file_path_str,
            "author": "Trophee Ltd",
            "last_modified": TIMESTAMP,
            "tags": [tag1, tag2],
            "word_count": word_count
        })

    return entries

def create_oell_entries():
    """Create entries for OeLL stories."""
    entries = []

    oell_cases = [
        ("OeLL Dot", "oell_dot.md", "dot", "no-edges"),
        ("OeLL Line", "oell_line.md", "line", "opposite-edges"),
        ("OeLL L", "oell_l.md", "l-shape", "adjacent-edges")
    ]

    for code, file_name, tag1, tag2 in oell_cases:
        file_name_full = f"3x3_cfop_{file_name}"
        file_path_str = f"3x3/cfop/oell/{file_name_full}"
        full_path = STORIES_BASE / file_path_str

        word_count = count_words(full_path) if full_path.exists() else 200

        entries.append({
            "puzzle": "3x3",
            "method": "cfop",
            "case_set": "oell",
            "case_code": code,
            "file_name": file_name_full,
            "file_path": file_path_str,
            "author": "Trophee Ltd",
            "last_modified": TIMESTAMP,
            "tags": ["2-look", tag1, tag2],
            "word_count": word_count
        })

    return entries

def create_pcll_entries():
    """Create entries for PcLL stories."""
    entries = []

    pcll_cases = [
        ("PcLL Adjacent", "pcll_adjacent.md", "adjacent", "headlights"),
        ("PcLL Diagonal", "pcll_diagonal.md", "diagonal", "no-headlights")
    ]

    for code, file_name, tag1, tag2 in pcll_cases:
        file_name_full = f"3x3_cfop_{file_name}"
        file_path_str = f"3x3/cfop/pcll/{file_name_full}"
        full_path = STORIES_BASE / file_path_str

        word_count = count_words(full_path) if full_path.exists() else 180

        entries.append({
            "puzzle": "3x3",
            "method": "cfop",
            "case_set": "pcll",
            "case_code": code,
            "file_name": file_name_full,
            "file_path": file_path_str,
            "author": "Trophee Ltd",
            "last_modified": TIMESTAMP,
            "tags": ["2-look", tag1, tag2],
            "word_count": word_count
        })

    return entries

def main():
    """Main function to update index.json."""
    # Read current index
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_data = json.load(f)

    # Collect all new entries
    new_entries = []
    new_entries.extend(create_f2l_entries())
    new_entries.extend(create_pll_entries())
    new_entries.extend(create_oll_entries())
    new_entries.extend(create_oell_entries())
    new_entries.extend(create_pcll_entries())

    # Add new entries to case_stories array
    index_data["case_stories"].extend(new_entries)

    # Update metadata
    index_data["last_updated"] = TIMESTAMP

    # Write updated index
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Updated index.json with {len(new_entries)} new story entries")
    print(f"   - F2L-FR: 34 stories")
    print(f"   - PLL: 9 stories")
    print(f"   - OLL: 54 stories")
    print(f"   - OeLL: 3 stories")
    print(f"   - PcLL: 2 stories")
    print(f"   Total case stories: {len(index_data['case_stories'])}")

if __name__ == "__main__":
    main()
