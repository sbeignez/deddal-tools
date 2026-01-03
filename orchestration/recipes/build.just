# Build & Testing Recipes
# Prefix: build-*

# Build debug configuration
build-debug:
    @just _info "🔨 Building debug configuration..."
    @just _xcodebuild-run "{{XCODE_SCHEME_DEV}}" "1.Debug" "build"
    @just _success "Debug build complete"

# Build TestFlight configuration
build-testflight:
    @just _info "🔨 Building TestFlight configuration..."
    @just _xcodebuild-run "{{XCODE_SCHEME_TESTFLIGHT}}" "2.TestFlight" "build"
    @just _success "TestFlight build complete"

# Build App Store configuration
build-appstore:
    @just _info "🔨 Building App Store configuration..."
    @just _xcodebuild-run "{{XCODE_SCHEME_APPSTORE}}" "3.Release" "build"
    @just _success "App Store build complete"

# Clean build artifacts
build-clean:
    @just _info "🧹 Cleaning build artifacts..."
    xcodebuild clean -project {{XCODE_PROJECT}} -scheme "{{XCODE_SCHEME_DEV}}"
    @just _success "Build artifacts cleaned"

# Run all tests (unit + UI)
build-test-all:
    @just _info "🧪 Running all tests..."
    @just _xcodebuild-test "{{XCODE_SCHEME_DEV}}" "Deddal.xctestplan" "{{XCODE_SIMULATOR}}"
    @just _success "All tests passed"

# Run unit tests only
build-test-unit:
    @just _info "🧪 Running unit tests..."
    xcodebuild test \
        -project {{XCODE_PROJECT}} \
        -scheme "{{XCODE_SCHEME_DEV}}" \
        -only-testing:DeddalTests \
        -destination "{{XCODE_SIMULATOR}}"
    @just _success "Unit tests passed"

# Run UI tests only
build-test-ui:
    @just _info "🧪 Running UI tests..."
    xcodebuild test \
        -project {{XCODE_PROJECT}} \
        -scheme "{{XCODE_SCHEME_DEV}}" \
        -only-testing:DeddalUITests \
        -destination "{{XCODE_SIMULATOR}}"
    @just _success "UI tests passed"

# Run specific test class
build-test-class class:
    @just _info "🧪 Running {{class}} tests..."
    xcodebuild test \
        -project {{XCODE_PROJECT}} \
        -scheme "{{XCODE_SCHEME_DEV}}" \
        -only-testing:DeddalTests/{{class}} \
        -destination "{{XCODE_SIMULATOR}}"
    @just _success "{{class}} tests passed"

# Run SwiftLint
build-lint:
    @just _info "🔍 Running SwiftLint..."
    @just _exec {{BUILD_DIR}}/swiftlint.sh
    @just _success "SwiftLint passed"

# Run Fastlane command
build-fastlane *args:
    @just _info "🚀 Running Fastlane: {{args}}..."
    @just _exec {{BUILD_DIR}}/fastlane_run.sh {{args}}

# Update download scripts configuration
build-update-scripts:
    @just _info "📝 Updating download scripts..."
    @just _exec {{BUILD_DIR}}/update_download_scripts.sh
    @just _success "Download scripts updated"
