# Architecture Validation

This folder contains tooling to enforce Clean Architecture boundaries in the Deddal codebase.

## Goals

- Protect DeddalCore from UI and infrastructure dependencies.
- Keep infrastructure free from UI frameworks.
- Prevent UI from reaching into concrete infra implementations.
- Catch violations early in CI and in local development.

## Layers

- `DeddalCore/Sources/DeddalDomain`
  Pure domain logic. Entities, value objects, domain services.

- `DeddalCore/Sources/DeddalApplication`
  Use cases. Orchestrates domain objects through ports. No knowledge of UI or persistence details.

- `DeddalCore/Sources/DeddalAdapters`
  Port and adapter interfaces shared across platforms.

- `Deddal/Layer-Domain`, `Deddal/Layer-Application`, `Deddal/Layer-Adapters`
  App level domain, use cases, and adapters.

- `DeddalInfra/Infrastructure`
  Infrastructure implementation layer (SwiftData, Supabase, analytics, timers, etc.).

- `Deddal/Layer-UI`
  SwiftUI views and view models. Talks to use cases, not concrete infra.

- `Deddal/AppShell`
  Composition root. Wires everything together.

## Script: check_dependencies.sh

Run all architecture checks:

```bash
./tool-arch/check_dependencies.sh
```

What it currently enforces:
1. **DeddalDomain** must not import:
   - SwiftUI, UIKit
   - SwiftData, StoreKit
   - AVKit, RealityKit, SceneKit
   - CoreBluetooth, AppKit

2. **DeddalApplication** must not import the same frameworks.

3. **DeddalInfra/Infrastructure** must not import SwiftUI.

4. **Deddal/Layer-UI** must not reference infra implementation details:
   - DataController
   - SwiftDataTimerProfileRepository
   - SwiftDataUserRepository
   - SwiftDataUserAlgorithmProgressRepository
   - SupabaseClient
   - SupabaseAuth
   - RealtimeManager
   - SwiftData
   - CoreBluetooth

Legacy code under `Deddal/Legacy` is excluded for now so we can migrate it gradually.

If a violation is found the script prints the offending locations and exits with status 1.

## SwiftLint integration

Architecture rules are also exposed as SwiftLint custom_rules so violations appear in Xcode as errors.

See `.swiftlint.yml` for:
- `no_swiftui_in_core`
- `no_swiftdata_in_domain`
- `no_swiftui_in_infra`
- `no_infra_types_in_ui`

These rules mirror the shell script checks.

## How to fix violations

1. **If a Core file imports a forbidden framework:**
   - Move that logic into an adapter or infra service.
   - Inject a port into the use case instead.

2. **If a UI file references an infra implementation:**
   - Introduce a port (protocol) and a use case.
   - Inject the use case from DependencyContainer into the view model.
   - Replace direct infra usage with calls to the use case.

3. **If a rule is too strict or false positive:**
   - Adjust the regex in `.swiftlint.yml` or `check_dependencies.sh`.
   - Keep the intent: Core has no framework dependencies, UI has no infra details.

## Future extensions

Add rules to:
- Forbid SwiftData imports in `DeddalCore/Sources/DeddalApplication`.
- Forbid Supabase in Core layers.
- Forbid StoreKit and CoreBluetooth in Core.
- Add graph based dependency checks if needed.

For now this setup gives a strict but pragmatic guardrail that matches the current architecture without blocking migration work in `Deddal/Legacy`.

## Architectural Baseline (v0.6.0)

From version 0.6.0 onward, the following invariants are treated as hard rules and enforced by this tooling:

- `DeddalDomain`:
  - No framework imports (SwiftUI, SwiftData, UIKit, AppKit, CoreBluetooth, StoreKit, AVKit, RealityKit, SceneKit)
  - Pure domain entities and value objects only

- `DeddalApplication`:
  - No persistence or UI framework imports (SwiftData, SwiftUI, UIKit)
  - Use cases depend only on domain types and ports

- `DeddalInfra/Infrastructure`:
  - No SwiftUI imports

- `Deddal/Layer-UI`:
  - No direct references to infrastructure singletons or SwiftData types

In addition, mapper tests in `DeddalCore/Tests/AdaptersTests/Persistence/SwiftData` verify that
domain entities and SwiftData models stay in sync.

Before merging to main:

1. Run `just arch-check`
2. Run `swift test --package-path DeddalCore`

Both must pass.
