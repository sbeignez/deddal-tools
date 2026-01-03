-- Migration: add_oll_algorithms_missing
-- Applied: 2025-11-23
-- Description: Add algorithms for 22 OLL cases that were missing from seed data
--
-- This migration was applied via Supabase MCP.
-- These OLL cases had 0 algorithms, causing "Loading algorithm..." bug.
--
-- Missing cases: OLL 1-10, 15, 17, 21, 24, 25, 27, 29, 30, 34, 36, 39, 41
-- Each case has 2-3 algorithm variants with popularity scores.

-- Example structure (full data applied via MCP):
-- INSERT INTO lib_algorithms (case_id, code, sequence, name, popularity) VALUES
-- ('uuid', 'OLL-1-01', 'R U2 R2 F R F'' U2 R'' F R F''', 'Main Algorithm', 95),
-- ('uuid', 'OLL-27-01', 'R U R'' U R U2 R''', 'Sune', 98),
-- ...

-- Status: APPLIED via Supabase MCP
-- Supabase migration version: 20251123211748
