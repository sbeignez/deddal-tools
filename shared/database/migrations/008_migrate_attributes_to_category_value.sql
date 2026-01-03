-- Migration: Convert groups and tags to category:value format
--
-- This migration updates the attribute tokens in lib_cases.groups and
-- lib_algorithms.tags columns to use the standardized category:value format.
--
-- IMPORTANT: Run this migration on production database, then re-export seed data.
--
-- Created: 2025-12-18
-- Related: Unified Attribute System implementation

-- ============================================================================
-- PHASE 1: lib_cases - groups column
-- ============================================================================
-- Current state: 121 tokens already in category:value format, 2 legacy tokens

-- Convert legacy tokens in lib_cases.groups
UPDATE lib_cases
SET groups = array_replace(groups, 'often_excluded', 'flag:often_excluded')
WHERE 'often_excluded' = ANY(groups);

UPDATE lib_cases
SET groups = array_replace(groups, 'pbl_equivalent', 'flag:pbl_equivalent')
WHERE 'pbl_equivalent' = ANY(groups);

-- ============================================================================
-- PHASE 2: lib_algorithms - tags column
-- ============================================================================
-- Current state: 2834 algorithms with null tags, 26 unique legacy tokens

-- Puzzle tags
UPDATE lib_algorithms
SET tags = array_replace(tags, '4x4', 'puzzle:4x4')
WHERE '4x4' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, '5x5', 'puzzle:5x5')
WHERE '5x5' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, '6x6', 'puzzle:6x6')
WHERE '6x6' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, '7x7', 'puzzle:7x7')
WHERE '7x7' = ANY(tags);

-- Type tags
UPDATE lib_algorithms
SET tags = array_replace(tags, 'standard', 'type:standard')
WHERE 'standard' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'alternative', 'type:alternative')
WHERE 'alternative' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'parity', 'type:parity')
WHERE 'parity' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'combined', 'type:combined')
WHERE 'combined' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'user_submitted', 'source:user_submitted')
WHERE 'user_submitted' = ANY(tags);

-- Stage tags
UPDATE lib_algorithms
SET tags = array_replace(tags, 'oll', 'stage:oll')
WHERE 'oll' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'pll', 'stage:pll')
WHERE 'pll' = ANY(tags);

-- Speed tags
UPDATE lib_algorithms
SET tags = array_replace(tags, 'fast', 'speed:fast')
WHERE 'fast' = ANY(tags);

-- Swap type tags
UPDATE lib_algorithms
SET tags = array_replace(tags, 'adjacent', 'swap_type:adjacent')
WHERE 'adjacent' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'diagonal', 'swap_type:diagonal')
WHERE 'diagonal' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'opposite', 'swap_type:opposite')
WHERE 'opposite' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'edge', 'piece:edge')
WHERE 'edge' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'uperm', 'family:uperm')
WHERE 'uperm' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'back', 'direction:back')
WHERE 'back' = ANY(tags);

-- Slot position tags (complex - need careful mapping)
UPDATE lib_algorithms
SET tags = array_replace(tags, 'In Back Right Slot', 'slot_position:back_right')
WHERE 'In Back Right Slot' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'In Back Right Slot, Advanced', 'slot_position:back_right,level:advanced')
WHERE 'In Back Right Slot, Advanced' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'In Front Left Slot', 'slot_position:front_left')
WHERE 'In Front Left Slot' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'In Front Left Slot, Beginner', 'slot_position:front_left,level:beginner')
WHERE 'In Front Left Slot, Beginner' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'To Back Right Slot', 'target_slot:back_right')
WHERE 'To Back Right Slot' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'To FL', 'target_slot:front_left')
WHERE 'To FL' = ANY(tags);

UPDATE lib_algorithms
SET tags = array_replace(tags, 'Solve to back', 'solve_direction:back')
WHERE 'Solve to back' = ANY(tags);

-- Technique notation tag
UPDATE lib_algorithms
SET tags = array_replace(tags, 'F''<UL>F', 'technique:sledgehammer_variant')
WHERE 'F''<UL>F' = ANY(tags);

-- ============================================================================
-- VERIFICATION QUERIES (run after migration)
-- ============================================================================

-- Check for any remaining legacy tokens in groups (tokens without colon)
-- SELECT DISTINCT token FROM (
--   SELECT unnest(groups) as token FROM lib_cases WHERE groups IS NOT NULL
-- ) t WHERE token NOT LIKE '%:%';

-- Check for any remaining legacy tokens in tags (tokens without colon)
-- SELECT DISTINCT token FROM (
--   SELECT unnest(tags) as token FROM lib_algorithms WHERE tags IS NOT NULL
-- ) t WHERE token NOT LIKE '%:%';

-- Count tokens by category for groups
-- SELECT split_part(token, ':', 1) as category, COUNT(*) FROM (
--   SELECT unnest(groups) as token FROM lib_cases WHERE groups IS NOT NULL
-- ) t GROUP BY category ORDER BY COUNT(*) DESC;

-- Count tokens by category for tags
-- SELECT split_part(token, ':', 1) as category, COUNT(*) FROM (
--   SELECT unnest(tags) as token FROM lib_algorithms WHERE tags IS NOT NULL
-- ) t GROUP BY category ORDER BY COUNT(*) DESC;
