# Screenshot Automation Recipes
# Prefix: screenshots-*

# Generate all screenshots (full 5-step pipeline)
screenshots-generate-all:
    @just _info "📸 Generating all screenshots..."
    @just _exec {{SCREENSHOTS_DIR}}/generate.sh
    @just _success "Screenshots generated for all locales"

# Step 1: Capture raw screenshots using UI tests
screenshots-snap:
    @just _info "📸 Step 1: Capturing raw screenshots..."
    @just _exec {{SCREENSHOTS_DIR}}/scripts/1_snap.sh
    @just _success "Raw screenshots captured"

# Step 2: Add device frames
screenshots-frame:
    @just _info "🖼️  Step 2: Adding device frames..."
    @just _exec {{SCREENSHOTS_DIR}}/scripts/2_frame.sh
    @just _success "Device frames added"

# Step 3: Render background gradients
screenshots-background:
    @just _info "🎨 Step 3: Rendering backgrounds..."
    @just _exec {{SCREENSHOTS_DIR}}/scripts/3_background.sh
    @just _success "Backgrounds rendered"

# Step 4: Overlay localized text
screenshots-text:
    @just _info "✍️  Step 4: Overlaying text..."
    @just _exec {{SCREENSHOTS_DIR}}/scripts/4_text.sh
    @just _success "Text overlays added"

# Step 5: Upload to App Store Connect via Fastlane
screenshots-upload:
    @just _warn "Uploading screenshots to App Store Connect"
    @just _confirm "Upload screenshots to App Store Connect?"
    @just _exec {{SCREENSHOTS_DIR}}/scripts/5_upload.sh
    @just _success "Screenshots uploaded"

# Run steps 1-4 (full local generation, no upload)
screenshots-generate-local:
    @just screenshots-snap
    @just screenshots-frame
    @just screenshots-background
    @just screenshots-text
    @just _success "Screenshots ready for preview (not uploaded)"

# Generate screenshots for specific locale
screenshots-locale locale:
    @just _info "📸 Generating screenshots for {{locale}}..."
    #!/usr/bin/env bash
    set -euo pipefail
    cd {{SCREENSHOTS_DIR}}
    LOCALE={{locale}} ./generate.sh
    just _success "Screenshots for {{locale}} ready"

# Clean screenshot output folders (use with caution)
screenshots-clean:
    @just _warn "This will delete screenshot output files"
    @just _confirm "Clean all screenshot outputs?"
    rm -rf {{SCREENSHOTS_DIR}}/output/*/
    @just _success "Screenshot outputs cleaned"

# Preview screenshots in Finder
screenshots-preview:
    @just _info "👀 Opening screenshots in Finder..."
    open {{SCREENSHOTS_DIR}}/output/
