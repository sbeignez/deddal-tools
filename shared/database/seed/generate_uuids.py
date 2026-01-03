#!/usr/bin/env python3
"""
Generate deterministic UUIDs for beginner cases and algorithms.
Uses UUID v5 with DNS namespace for reproducibility.
"""

import json
import uuid

# UUID v5 namespace (DNS namespace standard)
NAMESPACE = uuid.NAMESPACE_DNS

def generate_case_uuid(mnemonic_id):
    """Generate UUID v5 for a case using format: deddal.case.{mnemonic_id}"""
    name = f"deddal.case.{mnemonic_id}"
    return str(uuid.uuid5(NAMESPACE, name))

def generate_algorithm_uuid(mnemonic_id):
    """Generate UUID v5 for an algorithm using format: deddal.algorithm.{mnemonic_id}"""
    name = f"deddal.algorithm.{mnemonic_id}"
    return str(uuid.uuid5(NAMESPACE, name))

def main():
    # Generate case UUID mapping
    case_ids = [
        "oell-01-line",
        "oell-02-lshape",
        "oell-03-dot",
        "ocll-01-sune",
        "ocll-02-antisune",
        "ocll-03-h",
        "ocll-04-pi",
        "ocll-05-u",
        "ocll-06-t",
        "ocll-07-l",
        "pcll-01-adjacent",
        "pcll-02-diagonal",
        "pell-01-ua",
        "pell-02-ub",
        "pell-03-z",
        "pell-04-h"
    ]

    case_mapping = {}
    for mnemonic_id in case_ids:
        new_uuid = generate_case_uuid(mnemonic_id)
        case_mapping[mnemonic_id] = new_uuid
        print(f"Case: {mnemonic_id:20} -> {new_uuid}")

    print("\n" + "="*60 + "\n")

    # Generate algorithm UUID mapping
    algorithm_ids = [
        "oell-line-01",
        "oell-lshape-01",
        "oell-dot-01",
        "ocll-sune-01",
        "ocll-antisune-01",
        "ocll-h-01",
        "ocll-pi-01",
        "ocll-u-01",
        "ocll-t-01",
        "ocll-l-01",
        "pcll-adjacent-01",
        "pcll-adjacent-02",
        "pcll-diagonal-01",
        "pell-ua-01",
        "pell-ua-02",
        "pell-ub-01",
        "pell-ub-02",
        "pell-z-01",
        "pell-z-02",
        "pell-h-01",
        "pell-h-02"
    ]

    algorithm_mapping = {}
    for mnemonic_id in algorithm_ids:
        new_uuid = generate_algorithm_uuid(mnemonic_id)
        algorithm_mapping[mnemonic_id] = new_uuid
        print(f"Algorithm: {mnemonic_id:20} -> {new_uuid}")

    # Save mappings to JSON file
    mappings = {
        "case_mapping": case_mapping,
        "algorithm_mapping": algorithm_mapping
    }

    with open("/Users/trophee-mini/code/deddal/deddal-ios/uuid_mapping.json", "w") as f:
        json.dump(mappings, f, indent=2)

    print("\n" + "="*60)
    print(f"Saved mappings to uuid_mapping.json")
    print(f"Total cases: {len(case_mapping)}")
    print(f"Total algorithms: {len(algorithm_mapping)}")

if __name__ == "__main__":
    main()
