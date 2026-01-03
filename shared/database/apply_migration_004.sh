#!/bin/bash
#
# Apply migration 004: Change knowledge_level from 0-5 to 0-100 percentage
#
# IMPORTANT: This migration converts existing data before changing constraints
#
# Usage:
#   1. Run this script to see the SQL commands
#   2. Copy the SQL and run it in Supabase SQL Editor
#   3. Run verification queries from verify_migration_004.sql
#

set -e

MIGRATION_FILE="$(dirname "$0")/migrations/004_change_knowledge_level_to_percentage.sql"

echo "========================================="
echo "Migration 004: Knowledge Level to Percentage"
echo "========================================="
echo ""
echo "⚠️  IMPORTANT: This migration will:"
echo "   1. Convert existing 0-5 values → 0-100 percentages"
echo "   2. Drop old CHECK constraint (0-5)"
echo "   3. Add new CHECK constraint (0-100)"
echo ""
echo "Example conversions:"
echo "   0 → 0%"
echo "   1 → 20%"
echo "   2 → 40%"
echo "   3 → 60%"
echo "   4 → 80%"
echo "   5 → 100%"
echo ""
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
echo "========================================="
echo ""
echo "After migration, verify with:"
echo "  cat tool-database/verify_migration_004.sql"
echo ""
