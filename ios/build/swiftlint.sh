#!/bin/bash

# SwiftLint Build Phase Script
# Runs SwiftLint on the source code

# Only run on macOS
if [[ "$(uname)" != "Darwin" ]]; then
    echo "SwiftLint is only supported on macOS"
    exit 0
fi

# Check if SwiftLint is installed
if command -v swiftlint >/dev/null 2>&1; then
    # Run SwiftLint
    swiftlint
else
    echo "warning: SwiftLint not installed. Install with: brew install swiftlint"
fi
