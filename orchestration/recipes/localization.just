# Localization Recipes
# Prefix: loc-*

# Extract untranslated strings from string catalogs
loc-extract-untranslated:
    @just _info "🔍 Extracting untranslated strings..."
    @just _python-exec {{LOCALIZATION_DIR}} "extract_untranslated.py"
    @just _success "Untranslated strings extracted"

# Auto-translate missing strings
loc-auto-translate:
    @just _warn "Auto-translating missing strings (uses AI translation APIs)"
    @just _confirm "Proceed with auto-translation? This may incur costs."
    @just _python-exec {{LOCALIZATION_DIR}} "auto_translate.py"
    @just _success "Translation complete"

# Import translated strings back to catalogs
loc-import-translations:
    @just _info "📥 Importing translations..."
    @just _python-exec {{LOCALIZATION_DIR}} "import_translations.py"
    @just _success "Translations imported"

# Split string catalog into separate files
loc-split-catalog:
    @just _info "📂 Splitting string catalog..."
    @just _python-exec {{LOCALIZATION_DIR}} "split_catalog.py"
    @just _success "Catalog split"

# Analyze localization coverage
loc-check-coverage:
    @just _info "📊 Analyzing localization coverage..."
    @just _exec {{LOCALIZATION_DIR}}/analyze_localization.sh

# Check for localization issues
loc-check-missing:
    @just _info "🔍 Checking for missing translations..."
    @just _exec {{LOCALIZATION_DIR}}/check_localization.sh

# Create locale folder structure
loc-create-folders:
    @just _info "📁 Creating locale folder structure..."
    @just _exec {{LOCALIZATION_DIR}}/create_locale_folders.sh
    @just _success "Locale folders created"

# Full localization workflow (extract → translate → import)
loc-workflow-full:
    @just _divider
    @just _info "🌐 Running full localization workflow..."
    @just _divider
    @just _step "1" "3" "Extracting untranslated strings..."
    @just loc-extract-untranslated
    @just _step "2" "3" "Auto-translating..."
    @just loc-auto-translate
    @just _step "3" "3" "Importing translations..."
    @just loc-import-translations
    @just _divider
    @just _success "Localization workflow complete"
