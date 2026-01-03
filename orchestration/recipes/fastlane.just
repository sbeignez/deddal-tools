# Fastlane & App Store Recipes
# Prefix: fastlane-*, version-*, release-*

# === Screenshots & Metadata ===

# Generate localized screenshots via Fastlane
fastlane-screenshots:
    @just _info "📸 Generating screenshots via Fastlane..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios screenshots
    just _success "Fastlane screenshots complete"

# Add device frames to screenshots
fastlane-add-frames:
    @just _info "🖼️  Adding device frames..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios add_frames
    just _success "Frames added"

# Upload screenshots to App Store Connect
fastlane-upload-screenshots:
    @just _warn "Uploading screenshots to App Store Connect"
    @just _confirm "Upload screenshots to App Store Connect?"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios upload_screenshots
    just _success "Screenshots uploaded"

# Upload metadata only (no screenshots)
fastlane-upload-metadata:
    @just _warn "Uploading metadata to App Store Connect"
    @just _confirm "Upload metadata to App Store Connect?"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios upload_metadata
    just _success "Metadata uploaded"

# Upload release notes only (no screenshots/binary)
fastlane-upload-release-notes:
    @just _warn "Uploading release notes to App Store Connect (metadata only)"
    @just _confirm "Upload release notes to App Store Connect?"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios upload_release_notes
    just _success "Release notes uploaded"

# Version bump + ASC + release notes workflow
release-with-notes version:
    @just _divider
    @just _info "📱 Preparing release {{version}} (local + ASC + release notes)"
    @just _divider
    @just _step "1" "4" "Show current version/build"
    @just version-show
    @just _step "2" "4" "Set local version to {{version}}"
    @just version-set {{version}}
    @just _step "3" "4" "Create version {{version}} in App Store Connect"
    @just version-create-asc {{version}}
    @just _step "4" "4" "Upload release notes"
    @just fastlane-upload-release-notes
    @just _divider
    @just _success "Release {{version}} prepared locally and in ASC (notes uploaded)"

# Run custom Fastlane lane
fastlane-run lane:
    @just _info "🚀 Running Fastlane lane: {{lane}}..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios {{lane}}
    just _success "Fastlane lane {{lane}} complete"

# === Version Management ===

# Show current version and build number
version-show:
    @just _info "📱 Showing current version..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios show_version

# Bump patch version (1.2.3 → 1.2.4)
version-bump-patch:
    @just _info "⬆️  Bumping patch version..."
    @just _confirm "Bump patch version (1.2.3 → 1.2.4)?"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios bump_patch
    just _success "Patch version bumped"

# Bump minor version (1.2.3 → 1.3.0)
version-bump-minor:
    @just _info "⬆️  Bumping minor version..."
    @just _confirm "Bump minor version (1.2.3 → 1.3.0)?"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios bump_minor
    just _success "Minor version bumped"

# Bump major version (1.2.3 → 2.0.0)
version-bump-major:
    @just _info "⬆️  Bumping major version..."
    @just _confirm "Bump major version (1.2.3 → 2.0.0)?"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios bump_major
    just _success "Major version bumped"

# Set specific version
version-set version:
    @just _info "📝 Setting version to {{version}}..."
    @just _confirm "Set version to {{version}}?"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios set_version version:{{version}}
    just _success "Version set to {{version}}"

# Bump build number
version-bump-build:
    @just _info "⬆️  Bumping build number..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios bump_build
    just _success "Build number bumped"

# Commit version changes to git
version-commit:
    @just _info "💾 Committing version changes..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios commit_version
    just _success "Version changes committed"

# Create and push git tag for current version
version-tag:
    @just _info "🏷️  Creating version tag..."
    @just _confirm "Create and push git tag?"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios tag_version
    just _success "Version tag created and pushed"

# Check App Store Connect version status
version-check-asc:
    @just _info "🔍 Checking App Store Connect version status..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios check_version_status

# Create new version in App Store Connect
version-create-asc version:
    @just _info "📦 Creating version {{version}} in App Store Connect..."
    @just _confirm "Create version {{version}} in App Store Connect?"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios create_new_version version:{{version}}
    just _success "Version {{version}} created in ASC"

# === Complete Release Workflows ===

# Patch release: bump patch → build → commit → tag → ASC
release-patch:
    @just _step "1" "5" "Starting patch release workflow"
    @just _confirm "Start patch release? (bump patch → build → commit → tag → ASC)"
    @just _step "2" "5" "Bumping version and build"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios release_patch
    @just _success "✅ Patch release complete!"
    @just _info "📝 Next: Upload build to TestFlight"

# Minor release: bump minor → reset build → commit → tag → ASC
release-minor:
    @just _step "1" "5" "Starting minor release workflow"
    @just _confirm "Start minor release? (bump minor → reset build to 1 → commit → tag → ASC)"
    @just _step "2" "5" "Bumping version and resetting build"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios release_minor
    @just _success "✅ Minor release complete!"
    @just _info "📝 Next: Upload build to TestFlight"

# Major release: bump major → reset build → commit → tag → ASC
release-major:
    @just _step "1" "5" "Starting major release workflow"
    @just _confirm "Start major release? (bump major → reset build to 1 → commit → tag → ASC)"
    @just _step "2" "5" "Bumping version and resetting build"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios release_major
    @just _success "✅ Major release complete!"
    @just _info "📝 Next: Upload build to TestFlight"

# Custom release: set version & build → commit → tag → ASC
release-custom version build="1":
    @just _step "1" "5" "Starting custom release workflow"
    @just _confirm "Create release {{version}} (Build {{build}})?"
    @just _step "2" "5" "Setting version and build"
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    {{BUNDLE}} fastlane ios release_custom version:{{version}} build:{{build}}
    @just _success "✅ Custom release complete: {{version}} ({{build}})"
    @just _info "📝 Next: Upload build to TestFlight"

# === Version Rollback & Verification ===

# Rollback last version commit (uncommitted changes preserved)
version-rollback:
    @just _warn "⚠️  Rolling back last version commit"
    @just _confirm "Rollback last version commit? (git reset HEAD~1)"
    @just _info "Rolling back..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{PROJECT_ROOT}}
    git reset HEAD~1
    just _success "Version commit rolled back (files still modified)"
    @just _info "💡 Changes preserved in working directory. Run 'git checkout .' to discard"

# Verify version consistency (Xcode project vs git tags)
version-verify:
    @just _info "🔍 Verifying version consistency..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{FASTLANE_DIR}}
    VERSION=$({{BUNDLE}} fastlane run get_version_number xcodeproj:../Deddal.xcodeproj target:Deddal | grep "Result:" | awk '{print $2}')
    BUILD=$({{BUNDLE}} fastlane run get_build_number xcodeproj:../Deddal.xcodeproj | grep "Result:" | awk '{print $2}')
    TAG="v${VERSION}-${BUILD}"
    echo ""
    echo "📱 Local Xcode Project:"
    echo "   Version: $VERSION"
    echo "   Build: $BUILD"
    echo ""
    cd ..
    if git rev-parse "$TAG" >/dev/null 2>&1; then
    echo "✅ Git tag exists: $TAG"
    else
    echo "⚠️  Git tag missing: $TAG"
    echo "💡 Run 'just version-tag' to create it"
    fi
    LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "none")
    echo ""
    echo "🏷️  Latest Git Tag: $LATEST_TAG"
