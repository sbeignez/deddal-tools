-- Verification queries for migration 003: Algorithm Notes Column
-- Run these in Supabase SQL Editor to verify the migration was applied successfully

-- 1. Check if alg_notes column exists in lib_user_algorithms table
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'lib_user_algorithms'
  AND column_name = 'alg_notes';

-- Expected output:
-- column_name | data_type | is_nullable | column_default
-- alg_notes   | text      | YES         | NULL

-- 2. Count total rows and rows with notes
SELECT
    COUNT(*) as total_rows,
    COUNT(alg_notes) as rows_with_notes,
    COUNT(CASE WHEN alg_notes = '' THEN 1 END) as rows_with_empty_string,
    COUNT(CASE WHEN alg_notes IS NULL THEN 1 END) as rows_with_null,
    COUNT(CASE WHEN alg_notes != '' AND alg_notes IS NOT NULL THEN 1 END) as rows_with_actual_notes
FROM lib_user_algorithms;

-- Expected output after migration:
-- total_rows | rows_with_notes | rows_with_empty_string | rows_with_null | rows_with_actual_notes
-- N          | N               | N                      | 0              | 0

-- 3. Sample a few rows to verify structure
SELECT
    id,
    algorithm_id,
    knowledge_level,
    alg_notes,
    LENGTH(alg_notes) as note_length,
    updated_at
FROM lib_user_algorithms
LIMIT 5;

-- 4. Verify table schema (all columns)
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'lib_user_algorithms'
ORDER BY ordinal_position;
