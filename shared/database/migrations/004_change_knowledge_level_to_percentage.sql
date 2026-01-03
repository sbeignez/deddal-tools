-- Migration 004: Change knowledge_level from 0-5 scale to 0-100 percentage
-- Date: 2025-01-18
--
-- IMPORTANT: This migration converts existing 0-5 values to 0-100 percentages
-- before changing the constraint. Data is preserved by multiplying by 20.
--
-- Example conversions:
--   0 → 0
--   1 → 20
--   2 → 40
--   3 → 60
--   4 → 80
--   5 → 100

-- Step 1: Drop old constraint FIRST (before updating data)
-- This allows the UPDATE to succeed with values > 5
ALTER TABLE lib_user_algorithms
DROP CONSTRAINT IF EXISTS user_algorithm_progress_knowledge_level_check;

-- Step 1b: Also drop if named differently (defensive)
ALTER TABLE lib_user_algorithms
DROP CONSTRAINT IF EXISTS lib_user_algorithms_knowledge_level_check;

-- Step 2: Convert existing data (0-5 → 0-100)
-- Now safe to update without constraint violations
UPDATE lib_user_algorithms
SET knowledge_level = knowledge_level * 20
WHERE knowledge_level <= 5;

-- Step 3: Add new constraint for 0-100 range
ALTER TABLE lib_user_algorithms
ADD CONSTRAINT user_algorithm_progress_knowledge_level_check
CHECK (knowledge_level >= 0 AND knowledge_level <= 100);

-- Verification query (run after migration to verify):
-- SELECT
--     MIN(knowledge_level) as min_level,
--     MAX(knowledge_level) as max_level,
--     COUNT(*) as total_rows,
--     COUNT(CASE WHEN knowledge_level > 5 THEN 1 END) as converted_rows
-- FROM lib_user_algorithms;
