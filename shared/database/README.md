# tool-database - Database & Seed Data Management

Scripts for managing Supabase database content, seed data generation, and migrations.

## Overview

This folder contains 11 files organized into 4 categories:
1. Seed data generation and updates
2. Algorithm synchronization to Supabase
3. Story content management
4. Database migrations

## Folder Structure

```
tool-database/
├── seed/         # Generate and update seed data (4 scripts)
├── sync/         # Sync data to Supabase (1 script)
├── stories/      # Manage story content (4 scripts)
└── migrations/   # Database migrations (SQL files)
```

## Seed Scripts (4 files)

Generate and update JSON seed data for local development and testing:

- `generate_uuids.py` - Generate UUIDs for database records
- `update_json_files.py` - Update JSON seed files with new data
- `update_json_seed_data.sh` - Bash wrapper for JSON update workflow
- `export_algs_to_json.py` - Export algorithm library to JSON format

**Usage:**

Generate UUIDs for new records:
```bash
cd tool-database/seed
python3 generate_uuids.py
```

Export algorithms to JSON:
```bash
python3 export_algs_to_json.py > algorithms.json
```

Update seed data files:
```bash
./update_json_seed_data.sh
```

**When to use:**
- Adding new algorithm cases to the library
- Updating case metadata (recognition hints, difficulty)
- Preparing seed data for database migrations
- Generating test data for development

## Sync Scripts (1 file)

Synchronize local algorithm data to Supabase cloud database:

- `sync_algorithms_to_supabase.py` - Sync algorithm library to cloud

**Usage:**
```bash
cd tool-database/sync
python3 sync_algorithms_to_supabase.py
```

**What it syncs:**
- Algorithm cases (F2L, OLL, PLL)
- Algorithm move sequences
- Case recognition hints
- Difficulty levels
- Image references

**Requirements:**
- Supabase credentials configured
- Supabase MCP server running (recommended)
- Local algorithm library up to date

## Story Scripts (4 files)

Manage story content in the Supabase database:

- `sync_story_content.py` - Sync story content to Supabase
- `generate_sync_sql.py` - Generate SQL for story synchronization
- `sync_via_mcp.py` - Sync stories using Supabase MCP
- `update_index.py` - Update story index/ordering

**Usage:**

Sync story content via MCP (recommended):
```bash
cd tool-database/stories
python3 sync_via_mcp.py
```

Generate SQL for manual review:
```bash
python3 generate_sync_sql.py > story_sync.sql
```

Update story index:
```bash
python3 update_index.py
```

**Story content includes:**
- Learning journey stories
- Tutorial content
- Recognition training materials
- User-facing educational content

## Migrations (1 folder)

SQL migration files for database schema changes:

```
migrations/
└── 001_add_onboarding_fields.sql  # Initial onboarding schema
```

**Migration naming convention:**
- `###_description.sql` (e.g., `001_add_onboarding_fields.sql`)
- Incrementing numbers for ordering
- Descriptive names for clarity

**Applying migrations:**

Via Supabase MCP:
```bash
# Use Supabase MCP tool: mcp__supabase__apply_migration
```

Manually via Supabase Dashboard:
1. Open Supabase project dashboard
2. Navigate to SQL Editor
3. Paste migration content
4. Execute SQL

**Best practices:**
- Always test migrations locally first
- Use transactions for multi-step migrations
- Include rollback instructions in comments
- Track applied migrations in database

## Common Workflows

### Updating Algorithm Library

1. **Export** algorithms from app to JSON:
   ```bash
   cd seed
   python3 export_algs_to_json.py > algorithms.json
   ```

2. **Generate** UUIDs for new cases:
   ```bash
   python3 generate_uuids.py
   ```

3. **Sync** to Supabase:
   ```bash
   cd ../sync
   python3 sync_algorithms_to_supabase.py
   ```

### Adding Story Content

1. **Prepare** story content in JSON format

2. **Sync** via MCP (recommended):
   ```bash
   cd stories
   python3 sync_via_mcp.py
   ```

3. **Update** story index:
   ```bash
   python3 update_index.py
   ```

### Database Schema Changes

1. **Create** migration file:
   ```bash
   cd migrations
   nano 002_add_new_feature.sql
   ```

2. **Test** migration locally (via Supabase local dev or staging)

3. **Apply** to production via Supabase MCP or Dashboard

## Dependencies

**Python scripts require:**
- Python 3.8+
- Supabase Python SDK
- JSON processing libraries

Install dependencies:
```bash
pip3 install supabase python-dotenv
```

**Environment variables:**
```bash
export SUPABASE_URL="your-project-url"
export SUPABASE_KEY="your-service-key"
```

**Supabase MCP:**
- Configured in Claude Code settings
- Enables direct database operations from CLI
- See main `CLAUDE.md` for MCP setup

## Related Documentation

- Main project: `/CLAUDE.md`
- Supabase architecture: `/documentation/01-architecture/`
- Algorithm library: `Deddal/Models/Methods/`

## Troubleshooting

**Sync failures:**
- Verify Supabase credentials in environment
- Check network connectivity
- Review Supabase project quotas/limits
- Check for UUID conflicts

**Migration errors:**
- Test migrations on staging/local first
- Review SQL syntax
- Check for table/column conflicts
- Ensure migrations run in order

**UUID generation:**
- Ensure no duplicate UUIDs across runs
- Verify UUID format (v4 standard)
- Check UUID uniqueness in database

**Story sync issues:**
- Validate JSON story content format
- Check for missing required fields
- Verify story IDs are unique
- Review story index integrity

Generated by Trophee Ltd
