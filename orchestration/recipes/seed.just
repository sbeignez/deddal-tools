# Seed Data Export Recipes
# Prefix: seed-*

# Export all seed data from database (with automatic backup)
seed-export-all:
    @just _info "📦 Exporting all seed data from database..."
    @just _python-exec {{SEED_DIR}} "scripts/export_seed_data.py"
    @just _success "Seed data exported (41 files)"

# Export with dry-run (preview changes without writing)
seed-export-dry-run:
    @just _info "🔍 Previewing seed data changes..."
    @just _python-exec {{SEED_DIR}} "scripts/export_seed_data.py" "--dry-run"

# Export single file
seed-export-file filename:
    @just _info "📦 Exporting {{filename}}..."
    @just _python-exec {{SEED_DIR}} "scripts/export_seed_data.py" "--file" "{{filename}}"
    @just _success "{{filename}} exported"

# List available backup archives
seed-list-archives:
    @just _info "📚 Available backup archives:"
    @just _python-exec {{SEED_DIR}} "scripts/export_seed_data.py" "--list-archives"

# Restore from backup archive
seed-restore timestamp:
    @just _warn "Restoring from backup: {{timestamp}}"
    @just _confirm "Restore seed data from {{timestamp}}?"
    @just _python-exec {{SEED_DIR}} "scripts/export_seed_data.py" "--restore" "{{timestamp}}"
    @just _success "Seed data restored from {{timestamp}}"

# Export without creating backup (not recommended)
seed-export-no-backup:
    @just _warn "Exporting without backup (not recommended)"
    @just _confirm "Export without backup?"
    @just _python-exec {{SEED_DIR}} "scripts/export_seed_data.py" "--no-archive"

# Stage seed data (01-stage.py)
seed-stage:
    @just _info "🎬 Staging seed data..."
    @just _python-exec {{SEED_DIR}} "scripts/01-stage.py"
    @just _success "Seed data staged"

# Deploy seed data (02-deploy.py)
seed-deploy:
    @just _warn "Deploying seed data to production"
    @just _confirm "Deploy seed data to production?"
    @just _python-exec {{SEED_DIR}} "scripts/02-deploy.py"
    @just _success "Seed data deployed"

# Stage and deploy workflow
seed-stage-deploy:
    @just seed-stage
    @just seed-deploy
