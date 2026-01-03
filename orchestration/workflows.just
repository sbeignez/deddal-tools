# High-level cross-tool workflows

# Complete release preparation workflow
workflow-release-prep:
    @just _divider
    @just _info "🚀 Starting release preparation workflow..."
    @just _divider
    @just _step "1" "6" "Checking database migrations..."
    @just db-migrate-check
    @just _step "2" "6" "Exporting seed data..."
    @just seed-export-all
    @just _step "3" "6" "Checking localization coverage..."
    @just loc-check-coverage
    @just _step "4" "6" "Generating screenshots..."
    @just screenshots-generate-all
    @just _step "5" "6" "Running all tests..."
    @just build-test-all
    @just _step "6" "6" "Uploading screenshots..."
    @just screenshots-upload
    @just _divider
    @just _success "Release preparation complete!"

# Refresh all assets from VisualCube API
workflow-asset-refresh:
    @just _divider
    @just _info "🎨 Refreshing all assets..."
    @just _divider
    @just _step "1" "4" "Downloading all case images..."
    @just assets-download-all
    @just _step "2" "4" "Populating null image metadata..."
    @just assets-populate-nulls
    @just _step "3" "4" "Renaming and organizing assets..."
    @just assets-rename-all
    @just _step "4" "4" "Uploading to Supabase..."
    @just assets-upload-all
    @just _divider
    @just _success "Asset refresh complete!"

# Full database sync workflow
workflow-db-sync:
    @just _divider
    @just _info "🗄️  Syncing database..."
    @just _divider
    @just _step "1" "4" "Generating seed data..."
    @just db-seed-generate
    @just _step "2" "4" "Syncing algorithms..."
    @just db-sync-algorithms
    @just _step "3" "4" "Syncing stories..."
    @just db-sync-stories
    @just _step "4" "4" "Exporting seed data..."
    @just seed-export-all
    @just _divider
    @just _success "Database sync complete!"

# Development environment setup
workflow-dev-setup:
    @just _divider
    @just _info "🛠️  Setting up development environment..."
    @just _divider
    @just _step "1" "5" "Installing dependencies..."
    @just setup-all
    @just _step "2" "5" "Running migrations..."
    @just db-migrate-run
    @just _step "3" "5" "Exporting seed data..."
    @just seed-export-all
    @just _step "4" "5" "Building debug configuration..."
    @just build-debug
    @just _step "5" "5" "Running tests..."
    @just build-test-unit
    @just _divider
    @just _success "Development environment ready!"

# Pre-commit validation workflow
workflow-pre-commit:
    @just _divider
    @just _info "🔍 Running pre-commit checks..."
    @just _divider
    @just _step "1" "3" "Running linter..."
    @just build-lint
    @just _step "2" "3" "Running unit tests..."
    @just build-test-unit
    @just _step "3" "3" "Checking localization..."
    @just loc-check-missing
    @just _divider
    @just _success "Pre-commit checks passed!"

# Full CI/CD simulation
workflow-ci:
    @just _divider
    @just _info "🤖 Simulating CI/CD pipeline..."
    @just _divider
    @just _step "1" "5" "Cleaning build artifacts..."
    @just build-clean
    @just _step "2" "5" "Building debug..."
    @just build-debug
    @just _step "3" "5" "Running all tests..."
    @just build-test-all
    @just _step "4" "5" "Running linter..."
    @just build-lint
    @just _step "5" "5" "Validating seed data..."
    @just seed-export-dry-run
    @just _divider
    @just _success "CI/CD simulation complete!"
