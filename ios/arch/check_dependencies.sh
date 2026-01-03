#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RG="${RG:-rg}"

if ! command -v "$RG" >/dev/null 2>&1; then
  echo "Error: '$RG' command not found. Install ripgrep or set RG=grep (and adjust options)."
  exit 1
fi

# Exclude Legacy for now so you can migrate gradually
EXCLUDE="--glob=!Deddal/Legacy/**"

fail() {
  echo
  echo "ARCHITECTURE VIOLATION:"
  echo "  $1"
  echo
  echo "See tools/ios/arch/README.md for rules and how to fix."
  exit 1
}

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

echo "[arch] Checking architecture dependencies..."

# 1) DeddalDomain: no UI or infra frameworks
check_imports_forbidden \
  "$ROOT/DeddalCore/Sources/DeddalDomain" \
  "DeddalDomain" \
  "SwiftUI" \
  "UIKit" \
  "SwiftData" \
  "StoreKit" \
  "AVKit" \
  "RealityKit" \
  "SceneKit" \
  "CoreBluetooth" \
  "AppKit"

# 2) DeddalApplication: no UI or persistence frameworks
check_imports_forbidden \
  "$ROOT/DeddalCore/Sources/DeddalApplication" \
  "DeddalApplication" \
  "SwiftUI" \
  "UIKit" \
  "SwiftData" \
  "StoreKit" \
  "AVKit" \
  "RealityKit" \
  "SceneKit" \
  "CoreBluetooth" \
  "AppKit"

# 3) DeddalInfra: no SwiftUI
check_imports_forbidden \
  "$ROOT/DeddalInfra/Infrastructure" \
  "DeddalInfra" \
  "SwiftUI"

# 4) Layer-UI: do not reference infra implementations directly
check_symbol_forbidden \
  "$ROOT/Deddal/Layer-UI" \
  "Layer-UI" \
  "DataController" \
  "SwiftDataTimerProfileRepository" \
  "SwiftDataUserRepository" \
  "SwiftDataUserAlgorithmProgressRepository" \
  "SupabaseClient" \
  "SupabaseAuth" \
  "RealtimeManager" \
  "SwiftData" \
  "CoreBluetooth"

echo "[arch] Architecture dependency checks passed."
