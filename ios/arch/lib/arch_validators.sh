#!/usr/bin/env bash
# Architecture validation library
# Shared functions for enforcing Clean Architecture boundaries

set -euo pipefail

# Validate ripgrep is available
if ! command -v rg &> /dev/null; then
    echo "Error: ripgrep (rg) is not installed"
    echo "Install with: brew install ripgrep (macOS) or apt-get install ripgrep (Ubuntu)"
    exit 1
fi

# Configuration
RG="${RG:-rg}"
# Exclude Legacy for now so you can migrate gradually
EXCLUDE="--glob=!Deddal/Legacy/**"

# Error reporting function
fail() {
  echo
  echo "ARCHITECTURE VIOLATION:"
  echo "  $1"
  echo
  echo "See tools/ios/arch/README.md for rules and how to fix."
  exit 1
}

# check_imports_forbidden <path> <label> <forbidden_framework1> [<forbidden_framework2> ...]
#
# Validates that no Swift files in the given path import any of the forbidden frameworks.
# Exits with status 1 if violations are found.
#
# Arguments:
#   path  - Directory to check for imports
#   label - Human-readable label for error messages
#   ...   - List of forbidden framework names
#
# Example:
#   check_imports_forbidden DeddalInfra/Infrastructure "DeddalInfra" SwiftUI UIKit
check_imports_forbidden() {
  local path="$1"
  local label="$2"
  shift 2
  local forbidden=("$@")

  # Skip if directory does not exist (keeps script safe while you refactor)
  if [ ! -d "$path" ]; then
    return 0
  fi

  for imp in "${forbidden[@]}"; do
    if $RG $EXCLUDE --no-heading --line-number --fixed-strings "import $imp" "$path" > /tmp/arch_check.txt 2>/dev/null; then
      echo "Forbidden import '$imp' found in $label:"
      cat /tmp/arch_check.txt
      fail "$label must not import $imp"
    fi
  done
}

# check_symbol_forbidden <path> <label> <forbidden_symbol1> [<forbidden_symbol2> ...]
#
# Validates that no Swift files in the given path reference any of the forbidden symbols.
# Exits with status 1 if violations are found.
#
# Arguments:
#   path  - Directory to check for symbol references
#   label - Human-readable label for error messages
#   ...   - List of forbidden symbol names
#
# Example:
#   check_symbol_forbidden Deddal/Layer-UI "Layer-UI" DataController SupabaseClient
check_symbol_forbidden() {
  local path="$1"
  local label="$2"
  shift 2
  local symbols=("$@")

  if [ ! -d "$path" ]; then
    return 0
  fi

  for sym in "${symbols[@]}"; do
    if $RG $EXCLUDE --no-heading --line-number --fixed-strings "$sym" "$path" > /tmp/arch_check.txt 2>/dev/null; then
      echo "Forbidden symbol '$sym' referenced in $label:"
      cat /tmp/arch_check.txt
      fail "$label must not reference $sym directly"
    fi
  done
}
