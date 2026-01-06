#!/usr/bin/env bash
# Infrastructure Guard
# Validates DeddalInfra architecture rules

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/arch_validators.sh"

ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

echo "[infra-guard] Checking DeddalInfra architecture rules..."

# Rule 1: DeddalInfra must not import App/UI frameworks
check_imports_forbidden \
  "$ROOT/DeddalInfra" \
  "DeddalInfra" \
  "Deddal" \
  "SwiftUI" \
  "SceneKit"

# Rule 2: DeddalInfra must not reference App singletons
check_symbol_forbidden \
  "$ROOT/DeddalInfra" \
  "DeddalInfra" \
  "Logger\\.app" \
  "DataController" \
  "MethodLibrary"

# Rule 3: DeddalInfra must not reference App models
check_symbol_forbidden \
  "$ROOT/DeddalInfra" \
  "DeddalInfra" \
  "LibCase" \
  "Solve" \
  "BLEDevice" \
  "TutorialProgressData" \
  "Achievement"

echo "[infra-guard] ✅ All DeddalInfra architecture checks passed"
