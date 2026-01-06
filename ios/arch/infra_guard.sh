#!/usr/bin/env bash
set -euo pipefail

# Fast guard: fail if DeddalInfra references App/UI-only symbols.
# Keep patterns tight and update as the refactor progresses.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

TARGET_DIR="DeddalInfra"

patterns=(
  "import Deddal"          # App target
  "import SwiftUI"         # UI framework
  "import SceneKit"        # UI/3D framework
  "Logger\\.app"           # App logger singleton
  "DataController"         # App persistence singleton
  "MethodLibrary"          # App library singleton
  "LibCase"                # App models
  "Solve"                  # App models
  "BLEDevice"              # App models
  "TutorialProgressData"   # App models
  "Achievement"            # App models
)

found_any=0

search_cmd() {
  local pattern="$1"
  if command -v rg >/dev/null 2>&1; then
    rg --fixed-strings --iglob '*.swift' --files-with-matches "$pattern" "$TARGET_DIR"
  else
    # Fallback to grep if ripgrep is unavailable
    grep -RIl --include='*.swift' -e "$pattern" "$TARGET_DIR"
  fi
}

for pattern in "${patterns[@]}"; do
  matches=$(search_cmd "$pattern" || true)
  if [[ -n "$matches" ]]; then
    echo "Forbidden pattern found: '$pattern'" >&2
    echo "$matches" >&2
    found_any=1
  fi
done

if [[ $found_any -ne 0 ]]; then
  exit 1
fi

echo "infra_guard: OK (no forbidden symbols in $TARGET_DIR)"
