-- ============================================================
-- Recognition Groups Database Population Script
-- ============================================================
-- Generated: 2025-01-14
-- Purpose: Upload recognition groups for OLL + Ortega cases to Supabase
-- Total: 69 cases (57 OLL + 7 Ortega OLL + 5 Ortega PBL)
--
-- INSTRUCTIONS:
-- 1. Go to Supabase Dashboard → SQL Editor
-- 2. Paste this entire script
-- 3. Click "Run" to execute all UPDATE statements
-- 4. Verify: SELECT COUNT(*) FROM lib_cases WHERE array_length(groups, 1) > 0;
--    Expected: 188 total cases with groups (119 existing + 69 new)
-- ============================================================

-- ============================================================
-- PART 1: OLL CASES (57 cases)
-- ============================================================

-- DOT CASES (OLL 1-4) - No edges oriented
UPDATE lib_cases
SET groups = ARRAY['shape:dot', 'edges:none_oriented', 'corners:none_oriented', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-1', 'OLL-2');

UPDATE lib_cases
SET groups = ARRAY['shape:dot', 'edges:none_oriented', 'corners:two_diagonal', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-3', 'OLL-4');

-- SQUARE CASES (OLL 5-8)
UPDATE lib_cases
SET groups = ARRAY['shape:square', 'edges:none_oriented', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-5', 'OLL-6');

UPDATE lib_cases
SET groups = ARRAY['shape:square', 'edges:none_oriented', 'corners:two_adjacent', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-7', 'OLL-8');

-- SMALL L CASES (OLL 9-12)
UPDATE lib_cases
SET groups = ARRAY['shape:l_shape', 'edges:two_adjacent', 'corners:one_oriented', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-9', 'OLL-10');

UPDATE lib_cases
SET groups = ARRAY['shape:l_shape', 'edges:two_adjacent', 'corners:two_diagonal', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-11', 'OLL-12');

-- LIGHTNING BOLT CASES (OLL 13-16)
UPDATE lib_cases
SET groups = ARRAY['shape:lightning', 'edges:two_adjacent', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-13', 'OLL-14');

UPDATE lib_cases
SET groups = ARRAY['shape:lightning', 'edges:two_adjacent', 'corners:two_diagonal', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-15', 'OLL-16');

-- FISH CASES (OLL 17-20)
UPDATE lib_cases
SET groups = ARRAY['shape:fish', 'edges:two_adjacent', 'corners:two_adjacent', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-17', 'OLL-18', 'OLL-19', 'OLL-20');

-- T-SHAPE CASES (OLL 33, 45) - Two opposite edges oriented
UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_opposite', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-33', 'OLL-45');

-- P-SHAPE CASES (OLL 31-32, 43-44)
UPDATE lib_cases
SET groups = ARRAY['shape:p_shape', 'edges:two_adjacent', 'corners:two_adjacent', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-31', 'OLL-32', 'OLL-43', 'OLL-44');

-- W-SHAPE CASES (OLL 36-38)
UPDATE lib_cases
SET groups = ARRAY['shape:w_shape', 'edges:two_opposite', 'corners:two_adjacent', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-36', 'OLL-38');

UPDATE lib_cases
SET groups = ARRAY['shape:w_shape', 'edges:two_opposite', 'corners:two_diagonal', 'pattern:mixed', 'level:intermediate']
WHERE code = 'OLL-37';

-- C-SHAPE CASES (OLL 34-35)
UPDATE lib_cases
SET groups = ARRAY['shape:c_shape', 'edges:two_opposite', 'corners:two_adjacent', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-34', 'OLL-35');

-- I-SHAPE CASES (OLL 51-54) - Two opposite edges
UPDATE lib_cases
SET groups = ARRAY['shape:i_shape', 'edges:two_opposite', 'corners:two_diagonal', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-51', 'OLL-52', 'OLL-53', 'OLL-54');

-- LINE CASE (OLL 55)
UPDATE lib_cases
SET groups = ARRAY['shape:line', 'edges:two_opposite', 'corners:three_oriented', 'pattern:mixed', 'level:beginner']
WHERE code = 'OLL-55';

-- T-SHAPE CASES (OLL 56, 46, 47, 48, 49, 50)
UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_opposite', 'corners:two_diagonal', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-56');

UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_opposite', 'corners:two_adjacent', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-46', 'OLL-48', 'OLL-50');

UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_opposite', 'corners:two_diagonal', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-47', 'OLL-49');

-- T-SHAPE CASES (OLL 39-42)
UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_adjacent', 'corners:two_adjacent', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-39', 'OLL-40', 'OLL-41', 'OLL-42');

-- OcLL CASES (OLL 21-27) - All edges oriented (Cross)
UPDATE lib_cases
SET groups = ARRAY['shape:cross', 'edges:all_oriented', 'corners:none_oriented', 'pattern:corners_only', 'level:beginner']
WHERE code = 'OLL-21';

UPDATE lib_cases
SET groups = ARRAY['shape:cross', 'edges:all_oriented', 'corners:one_oriented', 'pattern:corners_only', 'level:beginner']
WHERE code IN ('OLL-22', 'OLL-23', 'OLL-24', 'OLL-25');

UPDATE lib_cases
SET groups = ARRAY['shape:cross', 'edges:all_oriented', 'corners:two_adjacent', 'pattern:corners_only', 'level:beginner']
WHERE code IN ('OLL-26', 'OLL-27');

-- OLL 28-30: All edges oriented
UPDATE lib_cases
SET groups = ARRAY['shape:cross', 'edges:all_oriented', 'corners:two_diagonal', 'pattern:corners_only', 'level:intermediate']
WHERE code IN ('OLL-28', 'OLL-29', 'OLL-30');

-- OLL 57: All corners oriented
UPDATE lib_cases
SET groups = ARRAY['shape:cross', 'edges:all_oriented', 'corners:all_oriented', 'pattern:mixed', 'level:beginner']
WHERE code = 'OLL-57';

-- ============================================================
-- PART 2: ORTEGA OLL CASES (7 cases)
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:sune', 'corners:one_oriented', 'level:beginner']
WHERE code = 'Ortega-OLL-1';

UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:antisune', 'corners:one_oriented', 'level:beginner']
WHERE code = 'Ortega-OLL-2';

UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:u', 'corners:two_diagonal', 'level:beginner']
WHERE code = 'Ortega-OLL-3';

UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:pi', 'corners:two_adjacent', 'level:beginner']
WHERE code = 'Ortega-OLL-4';

UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:t', 'corners:two_adjacent', 'level:beginner']
WHERE code = 'Ortega-OLL-5';

UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:h', 'corners:two_diagonal', 'level:beginner']
WHERE code = 'Ortega-OLL-6';

UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:l', 'corners:two_adjacent', 'level:beginner']
WHERE code = 'Ortega-OLL-7';

-- ============================================================
-- PART 3: ORTEGA PBL CASES (5 cases)
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['type:adjacent_swap', 'layers:one_layer', 'level:beginner']
WHERE code = 'Ortega-PBL-1';

UPDATE lib_cases
SET groups = ARRAY['type:diagonal_swap', 'layers:one_layer', 'level:intermediate']
WHERE code = 'Ortega-PBL-2';

UPDATE lib_cases
SET groups = ARRAY['type:diagonal_swap', 'layers:both_layers', 'level:beginner']
WHERE code = 'Ortega-PBL-3';

UPDATE lib_cases
SET groups = ARRAY['type:adjacent_swap', 'layers:both_layers', 'level:intermediate']
WHERE code = 'Ortega-PBL-4';

UPDATE lib_cases
SET groups = ARRAY['type:mixed_swap', 'layers:both_layers', 'level:beginner']
WHERE code = 'Ortega-PBL-5';

-- ============================================================
-- VERIFICATION QUERIES
-- ============================================================

-- Check total cases with recognition groups (should be 188)
SELECT COUNT(*) as total_with_groups
FROM lib_cases
WHERE array_length(groups, 1) > 0;

-- Count by case kind
SELECT
  kind,
  COUNT(*) as total,
  COUNT(*) FILTER (WHERE array_length(groups, 1) > 0) as with_groups
FROM lib_cases
WHERE kind IN ('f2l', 'oll', 'pll', 'ocll', 'oell', 'pell', 'pcll', 'ortega_oll', 'ortega_pbl')
GROUP BY kind
ORDER BY kind;

-- Show sample OLL cases to verify
SELECT code, title, groups
FROM lib_cases
WHERE kind = 'oll'
ORDER BY code
LIMIT 10;
