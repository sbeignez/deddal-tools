-- Migration: add_cll_algorithms_part1 + add_cll_algorithms_part2
-- Applied: 2025-11-23
-- Description: Add algorithms for all 40 CLL cases (2x2 method)
--
-- This migration was applied via Supabase MCP.
-- CLL cases had 0 algorithms, causing "Loading algorithm..." bug in Lib_CaseView.
--
-- Groups: AS (6), H (4), L (6), PI (6), SUNE (6), T (6), U (6) = 40 cases
-- Each case has 4 algorithm variants with popularity scores.

-- Example structure (full data applied via MCP):
-- INSERT INTO lib_algorithms (case_id, code, sequence, name, popularity) VALUES
-- ('uuid', 'CLL-AS-01-01', 'y R U2 R'' U'' R U'' R''', 'Algorithm 1', 90),
-- ...

-- Status: APPLIED via Supabase MCP
-- Supabase migration versions: 20251123211154, 20251123211637
