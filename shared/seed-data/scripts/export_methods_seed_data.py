#!/usr/bin/env python3
"""
Export Methods Seed Data

Generates JSON seed files for method data (families, configurations, states, transitions, patterns).
This is standalone data not from Supabase - it's based on the legacy MethodLibrary definitions.

Output files:
- seeddata_method_states.json
- seeddata_method_families.json
- seeddata_method_configurations.json
- seeddata_method_transitions.json
- seeddata_patterns.json
- seeddata_method_path_segments.json
- seeddata_patterns.json

Usage:
    python scripts/export_methods_seed_data.py
    python scripts/export_methods_seed_data.py --dry-run
    python scripts/export_methods_seed_data.py --output-dir /custom/path
"""

import json
import uuid
import argparse
from pathlib import Path
from datetime import datetime


# Default output directory
DEFAULT_OUTPUT_DIR = Path(__file__).parent.parent.parent / "DeddalInfra" / "Infrastructure" / "Persistence" / "SeedData"


# Stable namespace for deterministic UUIDs (do not change once published)
METHODS_NAMESPACE_UUID = uuid.UUID("6b2a2e19-4e6a-4f4a-9e2b-2d1e3d2d5a6c")


def generate_uuid(key: str) -> str:
    """Generate a deterministic UUID from a stable key."""
    return str(uuid.uuid5(METHODS_NAMESPACE_UUID, key))


# =============================================================================
# Method States
# =============================================================================

METHOD_STATES = [
    # CFOP States
    {"code": "scrambled", "name": "Scrambled"},
    {"code": "cross", "name": "Cross"},
    {"code": "f2l", "name": "2 Layers"},
    {"code": "top-edges-oriented", "name": "Top Edges Oriented"},
    {"code": "top-oriented", "name": "Top Oriented"},
    {"code": "top-corners-permuted", "name": "Top Corners Permuted"},
    {"code": "solved", "name": "Solved"},

    # 2x2 Ortega/CLL States
    {"code": "2x2-first-face", "name": "First Face"},
    {"code": "2x2-corners-oriented", "name": "Corners Oriented"},
    {"code": "2x2-solved", "name": "Solved"},

    # LBL States
    {"code": "lbl-daisy", "name": "Daisy"},
    {"code": "lbl-white-cross", "name": "White Cross"},
    {"code": "lbl-first-layer", "name": "First Layer"},
    {"code": "lbl-second-layer", "name": "Second Layer"},
    {"code": "lbl-yellow-cross", "name": "Yellow Cross"},
    {"code": "lbl-yellow-face", "name": "Yellow Face"},
    {"code": "lbl-yellow-corners", "name": "Yellow Corners"},

    # Roux States
    {"code": "roux-first-block", "name": "First Block"},
    {"code": "roux-second-block", "name": "Second Block"},
    {"code": "roux-cmll", "name": "CMLL"},
    {"code": "roux-lse", "name": "Last Six Edges"},
    {"code": "roux-lse-eo", "name": "LSE EO Complete"},
    {"code": "roux-lse-ulur", "name": "LSE ULUR Complete"},
    {"code": "roux-lse-l4e", "name": "LSE L4E Complete"},
]


# =============================================================================
# Method Transitions
# =============================================================================

METHOD_TRANSITIONS = [
    # CFOP Transitions
    {
        "name": "scramble-to-cross",
        "display_name": "Scramble → Cross",
        "from_state_code": "scrambled",
        "to_state_code": "cross",
        "case_set_codes": ["cross"],
    },
    {
        "name": "cross-to-f2l-beginner",
        "display_name": "Cross → F2L (Beginner)",
        "from_state_code": "cross",
        "to_state_code": "f2l",
        "case_set_codes": ["f2l-ls-fr"],
    },
    {
        "name": "cross-to-f2l-intermediate",
        "display_name": "Cross → F2L (Intermediate)",
        "from_state_code": "cross",
        "to_state_code": "f2l",
        "case_set_codes": ["f2l-ls-fr", "f2l-ls-fl"],
    },
    {
        "name": "f2l-to-oell",
        "display_name": "F2L → OeLL",
        "from_state_code": "f2l",
        "to_state_code": "top-edges-oriented",
        "case_set_codes": ["oell"],
    },
    {
        "name": "oell-to-ocll",
        "display_name": "OeLL → OcLL",
        "from_state_code": "top-edges-oriented",
        "to_state_code": "top-oriented",
        "case_set_codes": ["ocll"],
    },
    {
        "name": "ocll-to-pcll",
        "display_name": "OcLL → PcLL",
        "from_state_code": "top-oriented",
        "to_state_code": "top-corners-permuted",
        "case_set_codes": ["pcll"],
    },
    {
        "name": "pcll-to-pell",
        "display_name": "PcLL → PeLL",
        "from_state_code": "top-corners-permuted",
        "to_state_code": "solved",
        "case_set_codes": ["pell"],
    },
    {
        "name": "f2l-to-full-oll",
        "display_name": "F2L → Full OLL",
        "from_state_code": "f2l",
        "to_state_code": "top-oriented",
        "case_set_codes": ["oll"],
    },
    {
        "name": "full-oll-to-full-pll",
        "display_name": "Full OLL → Full PLL",
        "from_state_code": "top-oriented",
        "to_state_code": "solved",
        "case_set_codes": ["pll"],
    },
    {
        "name": "oell-to-coll",
        "display_name": "OeLL → COLL",
        "from_state_code": "top-edges-oriented",
        "to_state_code": "top-corners-permuted",
        "case_set_codes": ["coll"],
    },
    {
        "name": "f2l-to-solved-1lll",
        "display_name": "F2L → Solved (1LLL)",
        "from_state_code": "f2l",
        "to_state_code": "solved",
        "case_set_codes": ["zbll"],
    },

    # 2x2 Ortega Transitions
    {
        "name": "ortega-scramble-to-first-face",
        "display_name": "Scramble → First Face",
        "from_state_code": "scrambled",
        "to_state_code": "2x2-first-face",
        "case_set_codes": [],
    },
    {
        "name": "ortega-first-face-to-oriented",
        "display_name": "First Face → Oriented",
        "from_state_code": "2x2-first-face",
        "to_state_code": "2x2-corners-oriented",
        "case_set_codes": ["ortega-oll"],
    },
    {
        "name": "ortega-oriented-to-solved",
        "display_name": "Oriented → Solved",
        "from_state_code": "2x2-corners-oriented",
        "to_state_code": "2x2-solved",
        "case_set_codes": ["ortega-pbl"],
    },

    # 2x2 CLL Transitions
    {
        "name": "cll-scramble-to-first-face",
        "display_name": "Scramble → First Face",
        "from_state_code": "scrambled",
        "to_state_code": "2x2-first-face",
        "case_set_codes": [],
    },
    {
        "name": "cll-first-face-to-solved",
        "display_name": "First Face → Solved (CLL)",
        "from_state_code": "2x2-first-face",
        "to_state_code": "2x2-solved",
        "case_set_codes": ["2x2-cll-with-algs"],
    },

    # LBL Transitions
    {
        "name": "lbl-scramble-to-daisy",
        "display_name": "Scramble → Daisy",
        "from_state_code": "scrambled",
        "to_state_code": "lbl-daisy",
        "case_set_codes": ["l1-daisy"],
    },
    {
        "name": "lbl-daisy-to-white-cross",
        "display_name": "Daisy → White Cross",
        "from_state_code": "lbl-daisy",
        "to_state_code": "lbl-white-cross",
        "case_set_codes": ["l1-daisy-to-cross"],
    },
    {
        "name": "lbl-white-cross-to-first-layer",
        "display_name": "White Cross → First Layer",
        "from_state_code": "lbl-white-cross",
        "to_state_code": "lbl-first-layer",
        "case_set_codes": ["l2-first-layer-corners"],
    },
    {
        "name": "lbl-first-layer-to-second-layer",
        "display_name": "First Layer → Second Layer",
        "from_state_code": "lbl-first-layer",
        "to_state_code": "lbl-second-layer",
        "case_set_codes": ["l2-second-layer-edges"],
    },
    {
        "name": "lbl-second-layer-to-yellow-cross",
        "display_name": "Second Layer → Yellow Cross",
        "from_state_code": "lbl-second-layer",
        "to_state_code": "lbl-yellow-cross",
        "case_set_codes": ["l3-top-cross-orient"],
    },
    {
        "name": "lbl-yellow-cross-to-yellow-face",
        "display_name": "Yellow Cross → Yellow Face",
        "from_state_code": "lbl-yellow-cross",
        "to_state_code": "lbl-yellow-face",
        "case_set_codes": ["l3-top-corners-orient"],
    },
    {
        "name": "lbl-yellow-face-to-yellow-corners",
        "display_name": "Yellow Face → Yellow Corners",
        "from_state_code": "lbl-yellow-face",
        "to_state_code": "lbl-yellow-corners",
        "case_set_codes": ["l3-top-corners-position"],
    },
    {
        "name": "lbl-yellow-corners-to-solved",
        "display_name": "Yellow Corners → Solved",
        "from_state_code": "lbl-yellow-corners",
        "to_state_code": "solved",
        "case_set_codes": ["l3-top-edges-position"],
    },

    # Roux Transitions (Standard)
    {
        "name": "roux-scramble-to-first-block",
        "display_name": "Scramble → First Block",
        "from_state_code": "scrambled",
        "to_state_code": "roux-first-block",
        "case_set_codes": [],
    },
    {
        "name": "roux-first-block-to-second-block",
        "display_name": "First Block → Second Block",
        "from_state_code": "roux-first-block",
        "to_state_code": "roux-second-block",
        "case_set_codes": [],
    },
    {
        "name": "roux-second-block-to-cmll",
        "display_name": "Second Block → CMLL",
        "from_state_code": "roux-second-block",
        "to_state_code": "roux-cmll",
        "case_set_codes": ["roux-cmll"],
    },
    {
        "name": "roux-cmll-to-lse",
        "display_name": "CMLL → LSE",
        "from_state_code": "roux-cmll",
        "to_state_code": "solved",
        "case_set_codes": [],
    },

    # Roux Advanced LSE Transitions
    {
        "name": "roux-cmll-to-eo",
        "display_name": "CMLL → EO",
        "from_state_code": "roux-cmll",
        "to_state_code": "roux-lse-eo",
        "case_set_codes": ["roux-lse-eo"],
    },
    {
        "name": "roux-eo-to-ulur",
        "display_name": "EO → ULUR",
        "from_state_code": "roux-lse-eo",
        "to_state_code": "roux-lse-ulur",
        "case_set_codes": ["roux-lse-ulur"],
    },
    {
        "name": "roux-ulur-to-l4e",
        "display_name": "ULUR → L4E",
        "from_state_code": "roux-lse-ulur",
        "to_state_code": "solved",
        "case_set_codes": ["roux-lse-l4e"],
    },
]


# =============================================================================
# Patterns
# =============================================================================

PATTERNS = [
    {"name": "Scrambled", "pattern_string": "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Cross", "pattern_string": "MMMMMMMMMMMMMLMMLMMMMMFMMFMMMMMRMMRMMMMMBMMBMMDMDDDMDM", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Cross Slot FR", "pattern_string": "MMMMMMMMMMMMLLLLLLMMMFFMFFMMMMMRRMRRMMMBBBBBBMDMDDDMDM", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Cross Slot FL", "pattern_string": "MMMMMMMMMMMMLLMLLMMMMMFFMFFMMMRRRRRRMMMBBBBBBMDMDDDMDM", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "2 Layers", "pattern_string": "MMMMMMMMMMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Top Edges Oriented", "pattern_string": "MUMUUUMUMMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Top Oriented", "pattern_string": "UUUUUUUUUMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Top Corners Permuted", "pattern_string": "UUUUUUUUULMLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Solved", "pattern_string": "UUUUUUUUULLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Daisy", "pattern_string": "MDMDUDMDMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "First Layer Complete", "pattern_string": "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Second Layer Complete", "pattern_string": "MMMMMMMMMMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Top Cross", "pattern_string": "MUMUUUMUMMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Top Corners Oriented", "pattern_string": "UUUUUUUUUMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Top Corners Positioned", "pattern_string": "UUUUUUUUULMLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "One Face Solved", "pattern_string": "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMDMMMDMMDMMMD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Opposite Face Oriented", "pattern_string": "UMMUMMUMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMDMMMDMMDMMMD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Solved (2×2)", "pattern_string": "UUUULLLLFFFFRRRRBBBBDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Roux FB+SB", "pattern_string": "MMMMMMMMMMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Roux CMLL Done", "pattern_string": "UMUMUUMUMLMLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "First Block", "pattern_string": "MMMMMMMMMMMMLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Second Block", "pattern_string": "MMMMMMMMMMMMLLLLLLMMMFFFFFFMMMMMMMMMMMMMMMMMMDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Corners Last Layer", "pattern_string": "UMUMUMUMULMLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "Last Six Edges", "pattern_string": "UUUUUUUUULLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "LSE EO Complete", "pattern_string": "UMUMUMUMULLLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "LSE ULUR Complete", "pattern_string": "UMULUMURMLLLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
    {"name": "LSE L4E Complete", "pattern_string": "UUUUUUUUULLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBBDDDDDDDDD", "allowed_auf": ["", "U", "U'", "U2"]},
]


# =============================================================================
# Path Segments
# =============================================================================

PATH_SEGMENTS = [
    {
        "code": "cfop-beginner-path",
        "name": "CFOP Beginner Core",
        "state_codes": ["scrambled", "cross", "f2l", "top-edges-oriented", "top-oriented", "top-corners-permuted", "solved"],
    },
    {
        "code": "cfop-full-path",
        "name": "CFOP Full Last Layer",
        "state_codes": ["scrambled", "cross", "f2l", "top-oriented", "solved"],
    },
    {
        "code": "cfop-coll-path",
        "name": "CFOP COLL Variant",
        "state_codes": ["scrambled", "cross", "f2l", "top-edges-oriented", "top-corners-permuted", "solved"],
    },
    {
        "code": "cfop-1lll-path",
        "name": "CFOP Advanced 1LLL",
        "state_codes": ["scrambled", "cross", "f2l", "solved"],
    },
    {
        "code": "ortega-path",
        "name": "Ortega Method",
        "state_codes": ["scrambled", "2x2-first-face", "2x2-corners-oriented", "2x2-solved"],
    },
    {
        "code": "cll-path",
        "name": "CLL Method",
        "state_codes": ["scrambled", "2x2-first-face", "2x2-solved"],
    },
    {
        "code": "lbl-path",
        "name": "Layer-by-Layer Method",
        "state_codes": ["scrambled", "lbl-daisy", "lbl-white-cross", "lbl-first-layer", "lbl-second-layer",
                        "lbl-yellow-cross", "lbl-yellow-face", "lbl-yellow-corners", "solved"],
    },
    {
        "code": "roux-standard-path",
        "name": "Roux Standard",
        "state_codes": ["scrambled", "roux-first-block", "roux-second-block", "roux-cmll", "solved"],
    },
    {
        "code": "roux-advanced-path",
        "name": "Roux Advanced",
        "state_codes": ["scrambled", "roux-first-block", "roux-second-block", "roux-cmll",
                        "roux-lse-eo", "roux-lse-ulur", "solved"],
    },
]


# =============================================================================
# Patterns
# =============================================================================
# Pattern strings use face-based notation: U,L,F,R,B,D for faces, M for mask
# Orientation: Yellow-Up, Blue-Front (CFOP solving orientation)

PATTERNS = [
    # CFOP Patterns (3x3)
    {
        "name": "Scrambled",
        "pattern_string": "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Cross",
        "pattern_string": "MMMMMMMMMMMMMLMMLMMMMMFMMFMMMMMRMMRMMMMMBMMBMMDMDDDMDM",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Cross Slot FR",
        "pattern_string": "MMMMMMMMMMMMLLLLLLMMMFFMFFMMMMMRRMRRMMMBBBBBBMDMDDDMDM",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Cross Slot FL",
        "pattern_string": "MMMMMMMMMMMMLLMLLMMMMMFFMFFMMMRRRRRRMMMBBBBBBMDMDDDMDM",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "2 Layers",
        "pattern_string": "MMMMMMMMMMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Top Edges Oriented",
        "pattern_string": "MUMUUUMUMMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Top Oriented",
        "pattern_string": "UUUUUUUUUMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Top Corners Permuted",
        "pattern_string": "UUUUUUUUULMLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Solved",
        "pattern_string": "UUUUUUUUULLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },

    # LBL (Layer-by-Layer) Patterns
    {
        "name": "Daisy",
        "pattern_string": "MDMDUDMDMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "First Layer Complete",
        "pattern_string": "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Second Layer Complete",
        "pattern_string": "MMMMMMMMMMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Top Cross",
        "pattern_string": "MUMUUUMUMMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Top Corners Oriented",
        "pattern_string": "UUUUUUUUUMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Top Corners Positioned",
        "pattern_string": "UUUUUUUUULMLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },

    # 2x2 Patterns (24 chars: 6 faces × 4 corners)
    {
        "name": "One Face Solved",
        "pattern_string": "MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMDMMMDMMDMMMD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Opposite Face Oriented",
        "pattern_string": "UMMUMMUMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMDMMMDMMDMMMD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Solved (2×2)",
        "pattern_string": "UUUULLLLFFFFRRRRBBBBDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },

    # Roux Method Patterns
    {
        "name": "Roux FB+SB",
        "pattern_string": "MMMMMMMMMMMMLLLLLLMMMFFFFFFMMMRRRRRRMMMBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Roux CMLL Done",
        "pattern_string": "UMUMUUMUMLMLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "First Block",
        "pattern_string": "MMMMMMMMMMMMLLLLLLMMMMMMMMMMMMMMMMMMMMMMMMMMBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Second Block",
        "pattern_string": "MMMMMMMMMMMMLLLLLLMMMFFFFFFMMMMMMMMMMMMMMMMMMDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Corners Last Layer",
        "pattern_string": "UMUMUMUMULMLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "Last Six Edges",
        "pattern_string": "UUUUUUUUULLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "LSE EO Complete",
        "pattern_string": "UMUMUMUMULLLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "LSE ULUR Complete",
        "pattern_string": "UMULUMURMLLLLLLLLLFMFFFFFFFRMRRRRRRRBMBBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
    {
        "name": "LSE L4E Complete",
        "pattern_string": "UUUUUUUUULLLLLLLLLFFFFFFFFFRRRRRRRRRBBBBBBBBBDDDDDDDDD",
        "allowed_auf": ["", "U", "U'", "U2"],
    },
]


# =============================================================================
# Method Configurations
# =============================================================================

METHOD_CONFIGURATIONS = [
    # CFOP Configurations
    {
        "code": "3x3-cfop-4lll",
        "name": "CFOP 4LLL",
        "description_text": "Cross, F2L, followed by 2-look OLL (OeLL→OcLL) and 2-look PLL (PcLL→PeLL)",
        "family_code": "3x3-cfop",
        "difficulty": "beginner",
        "path_segment_code": "cfop-beginner-path",
        "language_tags": ["en"],
    },
    {
        "code": "3x3-cfop-2lll",
        "name": "CFOP 2LLL",
        "description_text": "Full OLL PLL: Cross, F2L followed by full one-look OLL and PLL",
        "family_code": "3x3-cfop",
        "difficulty": "intermediate",
        "path_segment_code": "cfop-full-path",
        "language_tags": ["en"],
    },
    {
        "code": "3x3-cfop-coll",
        "name": "CFOP 3LLL COLL",
        "description_text": "Cross, F2L, advanced 3-look last layer with COLL (OeLL→COLL→PeLL)",
        "family_code": "3x3-cfop",
        "difficulty": "advanced",
        "path_segment_code": "cfop-coll-path",
        "language_tags": ["en"],
    },
    {
        "code": "3x3-cfop-1lll",
        "name": "CFOP 1LLL",
        "description_text": "Cross, F2L followed by 1-look last layer (ZBLL - requires recognition of combined OLL+PLL patterns)",
        "family_code": "3x3-cfop",
        "difficulty": "advanced",
        "path_segment_code": "cfop-1lll-path",
        "language_tags": ["en"],
    },

    # Roux Configurations
    {
        "code": "3x3-roux",
        "name": "Roux",
        "description_text": "Block building method: FB → SB → CMLL (42 cases) → LSE (intuitive)",
        "family_code": "3x3-roux",
        "difficulty": "intermediate",
        "path_segment_code": "roux-standard-path",
        "language_tags": ["en"],
    },
    {
        "code": "3x3-roux-advanced",
        "name": "Roux Advanced",
        "description_text": "Full algorithmic Roux: FB → SB → CMLL (42) → EO (10) → ULUR (4) → L4E (4)",
        "family_code": "3x3-roux",
        "difficulty": "advanced",
        "path_segment_code": "roux-advanced-path",
        "language_tags": ["en"],
    },

    # 2x2 Configurations
    {
        "code": "2x2-ortega",
        "name": "Ortega",
        "description_text": "First Face, OLL (7 cases), PBL (5 cases)",
        "family_code": "2x2-ortega",
        "difficulty": "beginner",
        "path_segment_code": "ortega-path",
        "language_tags": ["en"],
    },
    {
        "code": "2x2-cll",
        "name": "CLL",
        "description_text": "First Face, CLL one-look (42 cases)",
        "family_code": "2x2-cll",
        "difficulty": "advanced",
        "path_segment_code": "cll-path",
        "language_tags": ["en"],
    },

    # LBL Configuration
    {
        "code": "3x3-lbl",
        "name": "Layer-by-Layer",
        "description_text": "First Layer (Cross + Corners), Middle Layer, Last Layer (4 steps)",
        "family_code": "3x3-lbl",
        "difficulty": "beginner",
        "path_segment_code": "lbl-path",
        "language_tags": ["en"],
    },
]


# =============================================================================
# Method Families
# =============================================================================

METHOD_FAMILIES = [
    {
        "code": "3x3-cfop",
        "name": "CFOP",
        "puzzle_id": "3x3",
        "state_codes": ["scrambled", "cross", "f2l", "top-edges-oriented", "top-oriented", "top-corners-permuted", "solved"],
        "configuration_codes": ["3x3-cfop-4lll", "3x3-cfop-2lll", "3x3-cfop-coll", "3x3-cfop-1lll"],
    },
    {
        "code": "3x3-roux",
        "name": "Roux",
        "puzzle_id": "3x3",
        "state_codes": ["scrambled", "roux-first-block", "roux-second-block", "roux-cmll", "roux-lse",
                        "roux-lse-eo", "roux-lse-ulur", "roux-lse-l4e", "solved"],
        "configuration_codes": ["3x3-roux", "3x3-roux-advanced"],
    },
    {
        "code": "3x3-lbl",
        "name": "Layer-by-Layer",
        "puzzle_id": "3x3",
        "state_codes": ["scrambled", "lbl-daisy", "lbl-white-cross", "lbl-first-layer", "lbl-second-layer",
                        "lbl-yellow-cross", "lbl-yellow-face", "lbl-yellow-corners", "solved"],
        "configuration_codes": ["3x3-lbl"],
    },
    {
        "code": "2x2-ortega",
        "name": "Ortega",
        "puzzle_id": "2x2",
        "state_codes": ["scrambled", "2x2-first-face", "2x2-corners-oriented", "2x2-solved"],
        "configuration_codes": ["2x2-ortega"],
    },
    {
        "code": "2x2-cll",
        "name": "CLL",
        "puzzle_id": "2x2",
        "state_codes": ["scrambled", "2x2-first-face", "2x2-solved"],
        "configuration_codes": ["2x2-cll"],
    },
]


def add_ids(items: list, key_field: str, prefix: str) -> list:
    """Add deterministic UUID ids to each item based on a stable key."""
    for item in items:
        key_value = item.get(key_field)
        if not key_value:
            raise ValueError(f"Missing '{key_field}' for deterministic id generation")
        item["id"] = generate_uuid(f"{prefix}:{key_value}")
    return items


def write_json(data: list, filepath: Path, dry_run: bool = False) -> None:
    """Write data to JSON file."""
    if dry_run:
        print(f"[DRY RUN] Would write {len(data)} items to {filepath}")
        print(json.dumps(data[:2], indent=2))  # Preview first 2 items
        print("...")
        return

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Wrote {len(data)} items to {filepath}")


def validate_seed_data(output_dir: Path) -> bool:
    """
    Validate existing seed data files for:
    1. File existence
    2. Valid JSON structure
    3. Required fields present
    4. Referential integrity (state codes, family codes, etc.)

    Returns True if all validations pass.
    """
    print("=" * 60)
    print("VALIDATING METHOD SEED DATA")
    print("=" * 60)
    print()

    errors = []
    warnings = []

    # Expected files
    files = {
        "states": output_dir / "seeddata_method_states.json",
        "families": output_dir / "seeddata_method_families.json",
        "configurations": output_dir / "seeddata_method_configurations.json",
        "transitions": output_dir / "seeddata_method_transitions.json",
        "path_segments": output_dir / "seeddata_method_path_segments.json",
        "patterns": output_dir / "seeddata_patterns.json",
    }

    # Load all files
    data = {}
    for name, filepath in files.items():
        if not filepath.exists():
            errors.append(f"❌ Missing file: {filepath.name}")
            continue
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data[name] = json.load(f)
            print(f"✅ Loaded {filepath.name} ({len(data[name])} items)")
        except json.JSONDecodeError as e:
            errors.append(f"❌ Invalid JSON in {filepath.name}: {e}")

    if errors:
        print()
        print("VALIDATION FAILED - File loading errors:")
        for e in errors:
            print(f"  {e}")
        return False

    print()
    print("Checking required fields...")

    # Build lookup sets
    state_codes = {s["code"] for s in data.get("states", [])}
    family_codes = {f["code"] for f in data.get("families", [])}
    config_codes = {c["code"] for c in data.get("configurations", [])}
    path_segment_codes = {p["code"] for p in data.get("path_segments", [])}
    pattern_names = {p["name"] for p in data.get("patterns", [])}

    # Validate states
    for state in data.get("states", []):
        if not state.get("id"):
            errors.append(f"State missing 'id': {state.get('code')}")
        if not state.get("code"):
            errors.append(f"State missing 'code': {state}")
        if not state.get("name"):
            errors.append(f"State missing 'name': {state.get('code')}")

    # Validate families
    for family in data.get("families", []):
        if not family.get("id"):
            errors.append(f"Family missing 'id': {family.get('code')}")
        if not family.get("code"):
            errors.append(f"Family missing 'code': {family}")
        if not family.get("name"):
            errors.append(f"Family missing 'name': {family.get('code')}")

        # Check state_codes reference valid states
        for sc in family.get("state_codes", []):
            if sc not in state_codes:
                errors.append(f"Family '{family.get('code')}' references unknown state: {sc}")

        # Check configuration_codes reference valid configs
        for cc in family.get("configuration_codes", []):
            if cc not in config_codes:
                errors.append(f"Family '{family.get('code')}' references unknown config: {cc}")

    # Validate configurations
    for config in data.get("configurations", []):
        if not config.get("id"):
            errors.append(f"Config missing 'id': {config.get('code')}")
        if not config.get("code"):
            errors.append(f"Config missing 'code': {config}")
        if not config.get("family_code"):
            errors.append(f"Config missing 'family_code': {config.get('code')}")
        elif config["family_code"] not in family_codes:
            errors.append(f"Config '{config.get('code')}' references unknown family: {config['family_code']}")

        if not config.get("path_segment_code"):
            errors.append(f"Config missing 'path_segment_code': {config.get('code')}")
        elif config["path_segment_code"] not in path_segment_codes:
            errors.append(f"Config '{config.get('code')}' references unknown path_segment: {config['path_segment_code']}")

    # Validate transitions
    for trans in data.get("transitions", []):
        if not trans.get("id"):
            errors.append(f"Transition missing 'id': {trans.get('name')}")
        if not trans.get("name"):
            errors.append(f"Transition missing 'name': {trans}")

        from_code = trans.get("from_state_code")
        to_code = trans.get("to_state_code")

        if not from_code:
            errors.append(f"Transition missing 'from_state_code': {trans.get('name')}")
        elif from_code not in state_codes:
            errors.append(f"Transition '{trans.get('name')}' references unknown from_state: {from_code}")

        if not to_code:
            errors.append(f"Transition missing 'to_state_code': {trans.get('name')}")
        elif to_code not in state_codes:
            errors.append(f"Transition '{trans.get('name')}' references unknown to_state: {to_code}")

        # Note: case_set_codes references are checked against existing caseset files
        # This is a warning since casesets are managed separately
        for csc in trans.get("case_set_codes", []):
            caseset_file = output_dir / f"seeddata_caseset_{csc}.json"
            if not caseset_file.exists():
                warnings.append(f"Transition '{trans.get('name')}' references caseset not in SeedData: {csc}")

    # Validate path_segments
    for segment in data.get("path_segments", []):
        if not segment.get("id"):
            errors.append(f"PathSegment missing 'id': {segment.get('code')}")
        if not segment.get("code"):
            errors.append(f"PathSegment missing 'code': {segment}")
        if not segment.get("name"):
            errors.append(f"PathSegment missing 'name': {segment.get('code')}")

        for sc in segment.get("state_codes", []):
            if sc not in state_codes:
                errors.append(f"PathSegment '{segment.get('code')}' references unknown state: {sc}")

    # Validate patterns
    for pattern in data.get("patterns", []):
        if not pattern.get("id"):
            errors.append(f"Pattern missing 'id': {pattern.get('name')}")
        if not pattern.get("name"):
            errors.append(f"Pattern missing 'name': {pattern}")
        if not pattern.get("pattern_string"):
            errors.append(f"Pattern missing 'pattern_string': {pattern.get('name')}")

    # Validate transition pattern references (if definition_from/to_pattern_name are used)
    for trans in data.get("transitions", []):
        from_pattern = trans.get("definition_from_pattern_name")
        to_pattern = trans.get("definition_to_pattern_name")

        if from_pattern and from_pattern not in pattern_names:
            warnings.append(f"Transition '{trans.get('name')}' references unknown from_pattern: {from_pattern}")
        if to_pattern and to_pattern not in pattern_names:
            warnings.append(f"Transition '{trans.get('name')}' references unknown to_pattern: {to_pattern}")

    # Report results
    print()
    if warnings:
        print("⚠️  WARNINGS:")
        for w in warnings:
            print(f"  {w}")
        print()

    if errors:
        print("❌ VALIDATION FAILED:")
        for e in errors:
            print(f"  {e}")
        return False

    print("✅ ALL VALIDATIONS PASSED")
    print()
    print("Summary:")
    print(f"  - {len(data.get('states', []))} states")
    print(f"  - {len(data.get('families', []))} families")
    print(f"  - {len(data.get('configurations', []))} configurations")
    print(f"  - {len(data.get('transitions', []))} transitions")
    print(f"  - {len(data.get('path_segments', []))} path segments")
    print(f"  - {len(data.get('patterns', []))} patterns")

    return True


def main():
    parser = argparse.ArgumentParser(description="Generate method seed data JSON files")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files")
    parser.add_argument("--validate", action="store_true", help="Validate existing seed data files")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
                        help="Output directory for JSON files")
    args = parser.parse_args()

    output_dir = args.output_dir

    # Validation mode
    if args.validate:
        success = validate_seed_data(output_dir)
        exit(0 if success else 1)

    dry_run = args.dry_run

    print(f"{'[DRY RUN] ' if dry_run else ''}Generating method seed data...")
    print(f"Output directory: {output_dir}")
    print()

    # Generate with UUIDs
    states = add_ids(METHOD_STATES.copy(), key_field="code", prefix="state")
    families = add_ids([f.copy() for f in METHOD_FAMILIES], key_field="code", prefix="family")
    configurations = add_ids([c.copy() for c in METHOD_CONFIGURATIONS], key_field="code", prefix="config")
    transitions = add_ids([t.copy() for t in METHOD_TRANSITIONS], key_field="name", prefix="transition")
    path_segments = add_ids([p.copy() for p in PATH_SEGMENTS], key_field="code", prefix="path")
    patterns = add_ids([p.copy() for p in PATTERNS], key_field="name", prefix="pattern")

    # Write files
    write_json(states, output_dir / "seeddata_method_states.json", dry_run)
    write_json(families, output_dir / "seeddata_method_families.json", dry_run)
    write_json(configurations, output_dir / "seeddata_method_configurations.json", dry_run)
    write_json(transitions, output_dir / "seeddata_method_transitions.json", dry_run)
    write_json(path_segments, output_dir / "seeddata_method_path_segments.json", dry_run)
    write_json(patterns, output_dir / "seeddata_patterns.json", dry_run)

    print()
    print("Summary:")
    print(f"  - {len(states)} method states")
    print(f"  - {len(families)} method families")
    print(f"  - {len(configurations)} method configurations")
    print(f"  - {len(transitions)} method transitions")
    print(f"  - {len(path_segments)} path segments")
    print(f"  - {len(patterns)} patterns")

    if not dry_run:
        print()
        print("✅ Done! Seed data files generated successfully.")
        print("Next steps:")
        print("  1. Verify Xcode copy phase includes these files")
        print("  2. Run tests to validate JSON loading")


if __name__ == "__main__":
    main()
