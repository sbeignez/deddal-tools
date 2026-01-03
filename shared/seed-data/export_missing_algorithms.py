#!/usr/bin/env python3
"""
Quick script to export missing algorithm files that the main export script got stuck on.
Exports OLL, PLL, PCLL, PELL, and Ortega-PBL algorithm files directly from Supabase.
"""

import json
import os
from supabase import create_client

# Supabase credentials from environment
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://qoglsyykgrqalsemigii.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_KEY:
    print("ERROR: SUPABASE_SERVICE_KEY environment variable not set")
    exit(1)

# Initialize Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Output directory
OUTPUT_DIR = "staging/2025-12-08_193714/ios"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Algorithm file exports (code prefix -> filename)
EXPORTS = {
    "3X3-CFOP-OLL-": "seeddata_algorithms_oll.json",
    "3X3-CFOP-PLL-": "seeddata_algorithms_pll.json",
    "3X3-PCLL-": "seeddata_algorithms_pcll.json",
    "3X3-PELL-": "seeddata_algorithms_pell.json",
    "2X2-ORTEGA-PBL-": "seeddata_algorithms_ortega-pbl.json",
}

for code_prefix, filename in EXPORTS.items():
    print(f"Exporting {filename}...")

    # Query algorithms with this prefix
    response = supabase.table("lib_algorithms") \
        .select("id, case_id, code, sequence, name, tags, popularity, difficulty, avg_moves, avg_execution_time_ms, story, created_at") \
        .like("code", f"{code_prefix}%") \
        .order("code") \
        .execute()

    algorithms = response.data
    count = len(algorithms)

    if count == 0:
        print(f"  ⚠ No records found for {code_prefix}")
        continue

    # Write to file
    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, 'w') as f:
        json.dump(algorithms, f, indent=2)

    print(f"  ✓ Exported {count} records to {filename}")

print("\n✓ All missing algorithm files exported successfully!")
