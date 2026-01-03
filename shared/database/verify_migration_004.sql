-- Verification queries for migration 004: Knowledge Level to Percentage
-- Run these in Supabase SQL Editor after applying the migration

-- 1. Check constraint was updated
SELECT
    conname as constraint_name,
    pg_get_constraintdef(oid) as constraint_definition
FROM pg_constraint
WHERE conrelid = 'lib_user_algorithms'::regclass
  AND conname LIKE '%knowledge_level%';

-- Expected output:
-- constraint_name                              | constraint_definition
-- user_algorithm_progress_knowledge_level_check | CHECK ((knowledge_level >= 0) AND (knowledge_level <= 100))

-- 2. Verify data ranges
SELECT
    MIN(knowledge_level) as min_level,
    MAX(knowledge_level) as max_level,
    AVG(knowledge_level) as avg_level,
    COUNT(*) as total_rows,
    COUNT(CASE WHEN knowledge_level > 5 THEN 1 END) as converted_rows,
    COUNT(CASE WHEN knowledge_level <= 5 THEN 1 END) as old_scale_rows
FROM lib_user_algorithms;

-- Expected output after migration:
-- min_level | max_level | avg_level | total_rows | converted_rows | old_scale_rows
-- 0         | 100       | ~40-60    | N          | N              | 0

-- 3. Sample converted data
SELECT
    id,
    algorithm_id,
    knowledge_level,
    updated_at
FROM lib_user_algorithms
ORDER BY knowledge_level DESC
LIMIT 10;

-- 4. Check for any invalid values (should return 0 rows)
SELECT COUNT(*) as invalid_rows
FROM lib_user_algorithms
WHERE knowledge_level < 0 OR knowledge_level > 100;

-- Expected: 0 invalid rows
