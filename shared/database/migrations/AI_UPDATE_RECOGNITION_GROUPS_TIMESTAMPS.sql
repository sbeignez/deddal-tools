-- ============================================================
-- Update Timestamps for Recognition Groups
-- ============================================================
-- Generated: 2025-01-15
-- Purpose: Update updated_at timestamps for all cases with recognition groups
--          This enables the app's sync mechanism to detect and fetch the new groups
--
-- BACKGROUND:
-- The app uses timestamp comparison (updated_at > lastSyncDate) to determine
-- if it should sync from the database. When we added recognition groups to
-- existing cases without updating timestamps, the app didn't detect changes.
--
-- INSTRUCTIONS:
-- 1. Go to Supabase Dashboard → SQL Editor
-- 2. Paste this script
-- 3. Click "Run" to update all timestamps
-- 4. Verify: SELECT COUNT(*), MAX(updated_at), MIN(updated_at)
--            FROM lib_cases WHERE array_length(groups, 1) > 0;
--    Expected: 188 cases with recent timestamps
-- ============================================================

-- Update timestamps for all cases that have recognition groups
UPDATE lib_cases
SET updated_at = NOW()
WHERE array_length(groups, 1) > 0;

-- ============================================================
-- VERIFICATION QUERY
-- ============================================================

-- Verify timestamps were updated
SELECT
  COUNT(*) as total_with_groups,
  MAX(updated_at) as most_recent_update,
  MIN(updated_at) as oldest_update,
  COUNT(*) FILTER (WHERE updated_at > NOW() - INTERVAL '1 minute') as just_updated
FROM lib_cases
WHERE array_length(groups, 1) > 0;

-- Expected results:
-- total_with_groups: 188
-- most_recent_update: ~current timestamp
-- oldest_update: ~current timestamp (or slightly earlier if some were already recent)
-- just_updated: 188 (all should be updated within last minute)

-- ============================================================
-- BREAKDOWN BY CASE KIND
-- ============================================================

SELECT
  kind,
  COUNT(*) as total,
  COUNT(*) FILTER (WHERE array_length(groups, 1) > 0) as with_groups,
  MAX(updated_at) FILTER (WHERE array_length(groups, 1) > 0) as latest_update
FROM lib_cases
WHERE kind IN ('f2l', 'oll', 'pll', 'ocll', 'oell', 'pell', 'pcll', 'ortega_oll', 'ortega_pbl')
GROUP BY kind
ORDER BY kind;

-- Expected breakdown:
-- f2l:         41 total, 41 with groups
-- oll:         57 total, 57 with groups
-- pll:         21 total, 21 with groups
-- ocll:        7 total, 7 with groups
-- oell:        4 total, 4 with groups
-- pell:        5 total, 5 with groups
-- pcll:        4 total, 4 with groups
-- ortega_oll:  7 total, 7 with groups
-- ortega_pbl:  5 total, 5 with groups
-- Total:       151 total, 188 with groups (note: some cases appear in multiple kinds)
