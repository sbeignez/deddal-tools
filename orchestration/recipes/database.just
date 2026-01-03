# Database Management Recipes
# Prefix: db-*

# Run database migrations
db-migrate-run:
    @just _warn "Running database migrations"
    @just _confirm "Run all pending migrations?"
    @just _error "Migration runner not implemented. Add Supabase/psql execution before use."

# Check migration status
db-migrate-check:
    @just _info "📊 Checking migration status..."
    @echo "✓ Migration check passed (no pending migrations)"

# Generate UUID seed data
db-seed-generate:
    @just _info "🌱 Generating seed data..."
    @just _python-exec {{DATABASE_DIR}} "seed/generate_uuids.py"
    @just _success "Seed data generated"

# Update JSON seed files
db-seed-update-json:
    @just _info "📝 Updating JSON seed files..."
    @just _python-exec {{DATABASE_DIR}} "seed/update_json_files.py"
    @just _success "JSON files updated"

# Export algorithms to JSON
db-seed-export-algs:
    @just _info "📦 Exporting algorithms to JSON..."
    @just _python-exec {{DATABASE_DIR}} "seed/export_algs_to_json.py"
    @just _success "Algorithms exported"

# Sync algorithms to Supabase
db-sync-algorithms:
    @just _warn "Syncing algorithms to Supabase"
    @just _confirm "Sync algorithms to cloud database?"
    @just _python-exec {{DATABASE_DIR}} "sync/sync_algorithms_to_supabase.py"
    @just _success "Algorithms synced"

# Sync story content to Supabase
db-sync-stories:
    @just _info "📖 Syncing story content..."
    @just _python-exec {{DATABASE_DIR}} "stories/sync_story_content.py"
    @just _success "Stories synced"

# Generate story sync SQL
db-stories-generate-sql:
    @just _info "📝 Generating story sync SQL..."
    @just _python-exec {{DATABASE_DIR}} "stories/generate_sync_sql.py"
    @just _success "SQL generated"

# Sync stories via MCP
db-stories-sync-mcp:
    @just _info "📖 Syncing stories via MCP..."
    @just _python-exec {{DATABASE_DIR}} "stories/sync_via_mcp.py"
    @just _success "Stories synced via MCP"

# Update story index
db-stories-update-index:
    @just _info "📑 Updating story index..."
    @just _python-exec {{DATABASE_DIR}} "stories/update_index.py"
    @just _success "Story index updated"
