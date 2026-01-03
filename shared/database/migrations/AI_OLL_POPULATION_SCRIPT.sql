-- OLL Recognition Groups Population Script
-- Generated: November 14, 2025
-- Total: 57 cases with shape, edges, corners, pattern, level groups

-- ============================================================
-- DOT CASES (OLL 1-4) - No edges oriented
-- ============================================================

-- OLL 1-2: Line pattern, no edges oriented
UPDATE lib_cases
SET groups = ARRAY['shape:dot', 'edges:none_oriented', 'corners:none_oriented', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-1', 'OLL-2');

-- OLL 3-4: Dot pattern variations
UPDATE lib_cases
SET groups = ARRAY['shape:dot', 'edges:none_oriented', 'corners:two_diagonal', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-3', 'OLL-4');

-- ============================================================
-- SQUARE CASES (OLL 5-8) - Square edge pattern
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['shape:square', 'edges:none_oriented', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-5', 'OLL-6');

UPDATE lib_cases
SET groups = ARRAY['shape:square', 'edges:none_oriented', 'corners:two_adjacent', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-7', 'OLL-8');

-- ============================================================
-- SMALL L CASES (OLL 9-12) - L-shaped edge patterns
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['shape:l_shape', 'edges:two_adjacent', 'corners:one_oriented', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-9', 'OLL-10');

UPDATE lib_cases
SET groups = ARRAY['shape:l_shape', 'edges:two_adjacent', 'corners:two_diagonal', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-11', 'OLL-12');

-- ============================================================
-- LIGHTNING BOLT CASES (OLL 13-16)
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['shape:lightning', 'edges:two_adjacent', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-13', 'OLL-14');

UPDATE lib_cases
SET groups = ARRAY['shape:lightning', 'edges:two_adjacent', 'corners:two_adjacent', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-15', 'OLL-16');

-- ============================================================
-- DOT CASES (OLL 17-20) - Advanced dot patterns
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['shape:dot', 'edges:none_oriented', 'corners:two_adjacent', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-17', 'OLL-18');

UPDATE lib_cases
SET groups = ARRAY['shape:dot', 'edges:none_oriented', 'corners:three_oriented', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-19', 'OLL-20');

-- ============================================================
-- OcLL CASES (OLL 21-27) - All edges oriented, corners only
-- ============================================================
-- These were populated earlier, but confirming here for completeness

-- OLL 21: H-Shape (Double Sune)
UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:cross', 'corners:two_diagonal', 'edges:all_oriented', 'level:beginner']
WHERE code = 'OLL-21';

-- OLL 22: Pi-Shape
UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:cross', 'corners:two_adjacent', 'edges:all_oriented', 'level:beginner']
WHERE code = 'OLL-22';

-- OLL 23: U-Shape / Headlights
UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:cross', 'corners:two_diagonal', 'edges:all_oriented', 'level:beginner']
WHERE code = 'OLL-23';

-- OLL 24: T-Shape / Chameleon
UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:cross', 'corners:two_adjacent', 'edges:all_oriented', 'level:beginner']
WHERE code = 'OLL-24';

-- OLL 25: L-Shape / Bowtie
UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:cross', 'corners:two_adjacent', 'edges:all_oriented', 'level:beginner']
WHERE code = 'OLL-25';

-- OLL 26: Anti-Sune
UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:cross', 'corners:one_oriented', 'edges:all_oriented', 'level:beginner']
WHERE code = 'OLL-26';

-- OLL 27: Sune (Most common OLL)
UPDATE lib_cases
SET groups = ARRAY['pattern:corners_only', 'shape:cross', 'corners:one_oriented', 'edges:all_oriented', 'level:beginner']
WHERE code = 'OLL-27';

-- ============================================================
-- P-SHAPE CASES (OLL 28-32)
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['shape:p_shape', 'edges:two_adjacent', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code = 'OLL-28';

UPDATE lib_cases
SET groups = ARRAY['shape:p_shape', 'edges:two_adjacent', 'corners:two_adjacent', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-29', 'OLL-30');

UPDATE lib_cases
SET groups = ARRAY['shape:p_shape', 'edges:two_adjacent', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-31', 'OLL-32');

-- ============================================================
-- T-SHAPE CASES (OLL 33-40)
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_opposite', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code = 'OLL-33';

UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_opposite', 'corners:two_adjacent', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-34', 'OLL-35', 'OLL-36');

UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_opposite', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-37', 'OLL-38');

UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_opposite', 'corners:two_adjacent', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-39', 'OLL-40');

-- ============================================================
-- C-SHAPE / W-SHAPE CASES (OLL 41-48)
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['shape:c_shape', 'edges:two_adjacent', 'corners:two_diagonal', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-41', 'OLL-42');

UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_opposite', 'corners:none_oriented', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-43', 'OLL-44');

UPDATE lib_cases
SET groups = ARRAY['shape:t_shape', 'edges:two_opposite', 'corners:none_oriented', 'pattern:mixed', 'level:beginner']
WHERE code = 'OLL-45';

UPDATE lib_cases
SET groups = ARRAY['shape:w_shape', 'edges:two_adjacent', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-46', 'OLL-47');

UPDATE lib_cases
SET groups = ARRAY['shape:w_shape', 'edges:two_adjacent', 'corners:two_adjacent', 'pattern:mixed', 'level:intermediate']
WHERE code = 'OLL-48';

-- ============================================================
-- I-SHAPE / FISH CASES (OLL 49-56)
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['shape:i_shape', 'edges:two_opposite', 'corners:two_diagonal', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-49', 'OLL-50');

UPDATE lib_cases
SET groups = ARRAY['shape:i_shape', 'edges:two_opposite', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code IN ('OLL-51', 'OLL-52');

UPDATE lib_cases
SET groups = ARRAY['shape:fish', 'edges:two_adjacent', 'corners:two_diagonal', 'pattern:mixed', 'level:intermediate']
WHERE code IN ('OLL-53', 'OLL-54');

UPDATE lib_cases
SET groups = ARRAY['shape:fish', 'edges:two_adjacent', 'corners:two_adjacent', 'pattern:mixed', 'level:advanced']
WHERE code IN ('OLL-55', 'OLL-56');

-- ============================================================
-- LINE / CROSS CASE (OLL 57)
-- ============================================================

UPDATE lib_cases
SET groups = ARRAY['shape:line', 'edges:two_opposite', 'corners:one_oriented', 'pattern:mixed', 'level:beginner']
WHERE code = 'OLL-57';

-- ============================================================
-- VALIDATION QUERY
-- ============================================================

-- Check population count by shape
SELECT
  CASE
    WHEN 'shape:dot' = ANY(groups) THEN 'Dot'
    WHEN 'shape:square' = ANY(groups) THEN 'Square'
    WHEN 'shape:l_shape' = ANY(groups) THEN 'L-Shape'
    WHEN 'shape:lightning' = ANY(groups) THEN 'Lightning'
    WHEN 'shape:cross' = ANY(groups) THEN 'Cross (OcLL)'
    WHEN 'shape:p_shape' = ANY(groups) THEN 'P-Shape'
    WHEN 'shape:t_shape' = ANY(groups) THEN 'T-Shape'
    WHEN 'shape:c_shape' = ANY(groups) THEN 'C-Shape'
    WHEN 'shape:w_shape' = ANY(groups) THEN 'W-Shape'
    WHEN 'shape:i_shape' = ANY(groups) THEN 'I-Shape'
    WHEN 'shape:fish' = ANY(groups) THEN 'Fish'
    WHEN 'shape:line' = ANY(groups) THEN 'Line'
    ELSE 'Other'
  END as shape_category,
  COUNT(*) as case_count
FROM lib_cases
WHERE kind = 'oll'
GROUP BY shape_category
ORDER BY shape_category;

-- Check total population
SELECT
  COUNT(*) as total_oll_cases,
  COUNT(*) FILTER (WHERE groups IS NOT NULL AND array_length(groups, 1) > 0) as populated_cases,
  COUNT(*) FILTER (WHERE groups IS NULL OR array_length(groups, 1) = 0) as empty_cases
FROM lib_cases
WHERE kind = 'oll';

-- Sample cases by difficulty
SELECT
  CASE
    WHEN 'level:beginner' = ANY(groups) THEN 'Beginner'
    WHEN 'level:intermediate' = ANY(groups) THEN 'Intermediate'
    WHEN 'level:advanced' = ANY(groups) THEN 'Advanced'
    ELSE 'Unassigned'
  END as difficulty_level,
  COUNT(*) as case_count
FROM lib_cases
WHERE kind = 'oll'
GROUP BY difficulty_level
ORDER BY difficulty_level;
