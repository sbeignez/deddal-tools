#!/usr/bin/env python3
"""
Upload case SVG images to Supabase Storage
Organizes images by category: f2l/, oll/, pll/, oell/
"""

import os
import re
import requests
from pathlib import Path
from typing import Dict, List

# Supabase configuration
SUPABASE_URL = "https://qoglsyykgrqalsemigii.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFvZ2xzeXlrZ3JxYWxzZW1pZ2lpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjEyMzMyNTcsImV4cCI6MjA3NjgwOTI1N30.LBk9-Li5WTQsRkH4JmqMv9cnWbfnnQOdVdLl_yvJk0k"
BUCKET_NAME = "case-images"

# Base directory for assets
ASSETS_DIR = "Deddal/App/Assets.xcassets"

# Category mapping based on code patterns
def get_category(code: str) -> str:
    """Determine category folder from case code"""
    if code.startswith("F2L-"):
        return "f2l"
    elif code.startswith("OLL-"):
        return "oll"
    elif code.endswith("-Perm") or code.startswith("PcLL-"):
        return "pll"
    elif code.startswith("OeLL-"):
        return "oell"
    elif code == "ERROR":
        return "other"
    else:
        return "other"

def extract_code_from_filename(filename: str) -> str:
    """Extract case code from SVG filename"""
    # Remove "Case-" or "img-case-" prefix and ".svg" suffix
    code = filename.replace("Case-", "").replace("img-case-", "").replace(".svg", "")
    return code

def find_all_svg_files() -> List[tuple]:
    """Find all SVG files in asset catalog and return (svg_path, code, category)"""
    svg_files = []

    for root, dirs, files in os.walk(ASSETS_DIR):
        for file in files:
            if file.endswith(".svg"):
                svg_path = os.path.join(root, file)
                code = extract_code_from_filename(file)
                category = get_category(code)
                svg_files.append((svg_path, code, category))

    return sorted(svg_files, key=lambda x: (x[2], x[1]))

def upload_to_supabase(svg_path: str, code: str, category: str) -> Dict:
    """Upload single SVG to Supabase Storage"""
    # Storage path: {category}/{code}.svg
    storage_path = f"{category}/{code}.svg"

    # Read SVG file
    with open(svg_path, 'rb') as f:
        svg_data = f.read()

    # Upload to Supabase Storage
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{storage_path}"
    headers = {
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "image/svg+xml",
        "x-upsert": "true"  # Overwrite if exists
    }

    response = requests.post(url, data=svg_data, headers=headers)

    return {
        "code": code,
        "category": category,
        "storage_path": storage_path,
        "status": response.status_code,
        "success": response.status_code in [200, 201],
        "public_url": f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET_NAME}/{storage_path}"
    }

def main():
    print("=== Uploading Case Images to Supabase Storage ===\n")

    # Find all SVG files
    svg_files = find_all_svg_files()
    print(f"Found {len(svg_files)} SVG files\n")

    # Count by category
    category_counts = {}
    for _, _, category in svg_files:
        category_counts[category] = category_counts.get(category, 0) + 1

    print("Distribution by category:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count} images")
    print()

    # Upload all files
    results = []
    success_count = 0
    error_count = 0

    for i, (svg_path, code, category) in enumerate(svg_files, 1):
        print(f"[{i}/{len(svg_files)}] Uploading {category}/{code}.svg... ", end="", flush=True)

        result = upload_to_supabase(svg_path, code, category)
        results.append(result)

        if result["success"]:
            print("✅")
            success_count += 1
        else:
            print(f"❌ (HTTP {result['status']})")
            error_count += 1

    # Summary
    print("\n=== Upload Summary ===")
    print(f"Total: {len(results)}")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")

    # Show sample URLs
    if success_count > 0:
        print("\nSample URLs (first 3 by category):")
        for category in sorted(set(r["category"] for r in results if r["success"])):
            cat_results = [r for r in results if r["category"] == category and r["success"]][:3]
            print(f"\n  {category}:")
            for r in cat_results:
                print(f"    {r['code']}: {r['public_url']}")

    # Show errors if any
    if error_count > 0:
        print("\nFailed uploads:")
        for r in results:
            if not r["success"]:
                print(f"  {r['code']} (HTTP {r['status']})")

    return 0 if error_count == 0 else 1

if __name__ == "__main__":
    exit(main())
