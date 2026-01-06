#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/arch_validators.sh"

ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"

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
