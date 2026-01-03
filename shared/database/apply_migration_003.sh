#!/bin/bash
#
# Apply migration 003: Add alg_notes column to lib_user_algorithms
#
# Usage:
#   1. Run this script to see the SQL commands
#   2. Copy the SQL and run it in Supabase SQL Editor
#   3. Or use Supabase CLI: supabase db execute -f tool-database/migrations/003_add_algorithm_notes.sql
#

set -e

MIGRATION_FILE="$(dirname "$0")/migrations/003_add_algorithm_notes.sql"

echo "========================================="
echo "Migration 003: Add Algorithm Notes Column"
echo "========================================="
echo ""
echo "SQL to execute in Supabase:"
echo ""
cat "$MIGRATION_FILE"
echo ""
echo "========================================="
echo ""
echo "To apply this migration:"
echo ""
echo "Option 1 - Supabase Dashboard:"
echo "  1. Go to https://supabase.com/dashboard"
echo "  2. Select your project"
echo "  3. Navigate to SQL Editor"
echo "  4. Copy/paste the SQL above"
echo "  5. Click 'Run'"
echo ""
echo "Option 2 - Supabase CLI:"
echo "  supabase db execute -f $MIGRATION_FILE"
echo ""
echo "Option 3 - Direct psql:"
echo "  psql \$DATABASE_URL -f $MIGRATION_FILE"
echo ""
echo "========================================="
