-- Migration: 007_add_roux_lse_case_sets
-- Description: Add LSE (Last Six Edges) case sets, cases, and algorithms for Roux Advanced method
-- Applied: 2025-12-18
--
-- This migration adds 3 case sets for the algorithmic LSE path:
-- 1. LSE-EO (Edge Orientation) - 10 cases
-- 2. LSE-ULUR (UL/UR Positioning) - 4 cases (intuitive recognition)
-- 3. LSE-L4E (Last 4 Edges Permutation) - 4 cases
--
-- Also tags 8 CMLL cases with level:beginner for two-look CMLL filtering

-- ============================================================================
-- PART 1: CREATE CASE SETS
-- ============================================================================

-- LSE-EO Case Set (Edge Orientation)
INSERT INTO lib_casesets (id, code, name, subtitle, category, expected_count, pattern_from, pattern_to)
VALUES (
  'c1a2b3d4-e5f6-7890-abcd-ef1234567890',
  'roux-lse-eo',
  'LSE-EO',
  'Edge Orientation (Roux 4a)',
  'Roux Method - Last Six Edges',
  10,
  NULL,
  NULL
);

-- LSE-ULUR Case Set (UL/UR edges)
INSERT INTO lib_casesets (id, code, name, subtitle, category, expected_count, pattern_from, pattern_to)
VALUES (
  'd2b3c4e5-f6a7-8901-bcde-f23456789012',
  'roux-lse-ulur',
  'LSE-ULUR',
  'UL/UR Edge Positioning (Roux 4b)',
  'Roux Method - Last Six Edges',
  4,
  NULL,
  NULL
);

-- LSE-L4E Case Set (Last 4 Edges)
INSERT INTO lib_casesets (id, code, name, subtitle, category, expected_count, pattern_from, pattern_to)
VALUES (
  'e3c4d5f6-a7b8-9012-cdef-345678901234',
  'roux-lse-l4e',
  'LSE-L4E',
  'Last 4 Edges Permutation (Roux 4c)',
  'Roux Method - Last Six Edges',
  4,
  NULL,
  NULL
);

-- ============================================================================
-- PART 2: CREATE LSE-EO CASES (10 cases)
-- ============================================================================

-- EO Case 1: All Oriented (Skip)
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  'e0111111-1111-1111-1111-111111111111',
  '3X3-LSE-EO01',
  'All Oriented',
  'roux_lse_eo',
  '',
  1,
  100,
  ARRAY['group:skip'],
  'Edge Orientation'
);

-- EO Case 2: Front Arrow
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  'e0222222-2222-2222-2222-222222222222',
  '3X3-LSE-EO02',
  'Front Arrow',
  'roux_lse_eo',
  'M U M''',
  2,
  95,
  ARRAY['group:arrow'],
  'Edge Orientation'
);

-- EO Case 3: Back Arrow
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  'e0333333-3333-3333-3333-333333333333',
  '3X3-LSE-EO03',
  'Back Arrow',
  'roux_lse_eo',
  'M'' U'' M',
  2,
  95,
  ARRAY['group:arrow'],
  'Edge Orientation'
);

-- EO Case 4: 2 Adjacent / 2 (5-mover)
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  'e0444444-4444-4444-4444-444444444444',
  '3X3-LSE-EO04',
  '2 Adjacent / 2',
  'roux_lse_eo',
  'M U'' M U2 M'' U M''',
  3,
  80,
  ARRAY['group:2adj'],
  'Edge Orientation'
);

-- EO Case 5: Front 1 / 1
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  'e0555555-5555-5555-5555-555555555555',
  '3X3-LSE-EO05',
  'Front 1 / 1',
  'roux_lse_eo',
  'M'' U M U M'' U M''',
  3,
  75,
  ARRAY['group:1-1'],
  'Edge Orientation'
);

-- EO Case 6: Back 1 / 1
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  'e0666666-6666-6666-6666-666666666666',
  '3X3-LSE-EO06',
  'Back 1 / 1',
  'roux_lse_eo',
  'M U'' M'' U'' M U'' M''',
  3,
  75,
  ARRAY['group:1-1'],
  'Edge Orientation'
);

-- EO Case 7: 2 Adjacent / 0
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  'e0777777-7777-7777-7777-777777777777',
  '3X3-LSE-EO07',
  '2 Adjacent / 0',
  'roux_lse_eo',
  'M U M U2 M U M''',
  3,
  70,
  ARRAY['group:2adj'],
  'Edge Orientation'
);

-- EO Case 8: 2 Opposite / 2
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  'e0888888-8888-8888-8888-888888888888',
  '3X3-LSE-EO08',
  '2 Opposite / 2',
  'roux_lse_eo',
  'M U'' M'' U'' M'' U M''',
  3,
  70,
  ARRAY['group:2opp'],
  'Edge Orientation'
);

-- EO Case 9: 2 Opposite / 0
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  'e0999999-9999-9999-9999-999999999999',
  '3X3-LSE-EO09',
  '2 Opposite / 0',
  'roux_lse_eo',
  'M U M'' U M U'' M''',
  3,
  65,
  ARRAY['group:2opp'],
  'Edge Orientation'
);

-- EO Case 10: All 6 Misoriented
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  'e0aaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
  '3X3-LSE-EO10',
  'All 6 Misoriented',
  'roux_lse_eo',
  'M U M U M U M'' U'' M'' U'' M''',
  4,
  50,
  ARRAY['group:all6'],
  'Edge Orientation'
);

-- ============================================================================
-- PART 3: CREATE LSE-ULUR CASES (4 cases for recognition)
-- ============================================================================

-- ULUR Case 1: Both on D layer
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  '01010101-1111-1111-1111-111111111111',
  '3X3-LSE-ULUR01',
  'Both on D Layer',
  'roux_lse_ulur',
  '',
  2,
  100,
  ARRAY['group:d-layer'],
  'UL/UR Positioned'
);

-- ULUR Case 2: Both on U layer (opposite)
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  '01020202-2222-2222-2222-222222222222',
  '3X3-LSE-ULUR02',
  'Both on U Layer (Opposite)',
  'roux_lse_ulur',
  'M'' U2 M''',
  2,
  90,
  ARRAY['group:u-layer'],
  'UL/UR Positioned'
);

-- ULUR Case 3: Diagonal (UF/DB or UB/DF)
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  '01030303-3333-3333-3333-333333333333',
  '3X3-LSE-ULUR03',
  'Diagonal Position',
  'roux_lse_ulur',
  'M'' U2 M'' U M2',
  2,
  85,
  ARRAY['group:diagonal'],
  'UL/UR Positioned'
);

-- ULUR Case 4: Both on same layer (adjacent)
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  '01040404-4444-4444-4444-444444444444',
  '3X3-LSE-ULUR04',
  'Adjacent Position',
  'roux_lse_ulur',
  'M2 U M'' U2 M'' U M2',
  3,
  80,
  ARRAY['group:adjacent'],
  'UL/UR Positioned'
);

-- ============================================================================
-- PART 4: CREATE LSE-L4E CASES (4 permutation cases)
-- ============================================================================

-- L4E Case 1: Ua Perm
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  '14e11111-1111-1111-1111-111111111111',
  '3X3-LSE-L4E01',
  'Ua Perm',
  'roux_lse_l4e',
  'M2 U'' M U2 M'' U'' M2',
  2,
  100,
  ARRAY['group:u-perm'],
  'Solved'
);

-- L4E Case 2: Ub Perm
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  '14e22222-2222-2222-2222-222222222222',
  '3X3-LSE-L4E02',
  'Ub Perm',
  'roux_lse_l4e',
  'M2 U M U2 M'' U M2',
  2,
  100,
  ARRAY['group:u-perm'],
  'Solved'
);

-- L4E Case 3: Z Perm
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  '14e33333-3333-3333-3333-333333333333',
  '3X3-LSE-L4E03',
  'Z Perm',
  'roux_lse_l4e',
  'M2 U'' M2 U2 M2 U'' M2',
  3,
  85,
  ARRAY['group:z-perm'],
  'Solved'
);

-- L4E Case 4: H Perm
INSERT INTO lib_cases (id, code, title, kind, scramble, difficulty, popularity, groups, pattern_to)
VALUES (
  '14e44444-4444-4444-4444-444444444444',
  '3X3-LSE-L4E04',
  'H Perm',
  'roux_lse_l4e',
  'M2 U M2 U2 M2 U M2',
  2,
  90,
  ARRAY['group:h-perm'],
  'Solved'
);

-- ============================================================================
-- PART 5: LINK CASES TO CASE SETS (lib_caseset_cases)
-- ============================================================================

-- LSE-EO case links
INSERT INTO lib_caseset_cases (caseset_id, case_id, case_index) VALUES
('c1a2b3d4-e5f6-7890-abcd-ef1234567890', 'e0111111-1111-1111-1111-111111111111', 0),
('c1a2b3d4-e5f6-7890-abcd-ef1234567890', 'e0222222-2222-2222-2222-222222222222', 1),
('c1a2b3d4-e5f6-7890-abcd-ef1234567890', 'e0333333-3333-3333-3333-333333333333', 2),
('c1a2b3d4-e5f6-7890-abcd-ef1234567890', 'e0444444-4444-4444-4444-444444444444', 3),
('c1a2b3d4-e5f6-7890-abcd-ef1234567890', 'e0555555-5555-5555-5555-555555555555', 4),
('c1a2b3d4-e5f6-7890-abcd-ef1234567890', 'e0666666-6666-6666-6666-666666666666', 5),
('c1a2b3d4-e5f6-7890-abcd-ef1234567890', 'e0777777-7777-7777-7777-777777777777', 6),
('c1a2b3d4-e5f6-7890-abcd-ef1234567890', 'e0888888-8888-8888-8888-888888888888', 7),
('c1a2b3d4-e5f6-7890-abcd-ef1234567890', 'e0999999-9999-9999-9999-999999999999', 8),
('c1a2b3d4-e5f6-7890-abcd-ef1234567890', 'e0aaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 9);

-- LSE-ULUR case links
INSERT INTO lib_caseset_cases (caseset_id, case_id, case_index) VALUES
('d2b3c4e5-f6a7-8901-bcde-f23456789012', '01010101-1111-1111-1111-111111111111', 0),
('d2b3c4e5-f6a7-8901-bcde-f23456789012', '01020202-2222-2222-2222-222222222222', 1),
('d2b3c4e5-f6a7-8901-bcde-f23456789012', '01030303-3333-3333-3333-333333333333', 2),
('d2b3c4e5-f6a7-8901-bcde-f23456789012', '01040404-4444-4444-4444-444444444444', 3);

-- LSE-L4E case links
INSERT INTO lib_caseset_cases (caseset_id, case_id, case_index) VALUES
('e3c4d5f6-a7b8-9012-cdef-345678901234', '14e11111-1111-1111-1111-111111111111', 0),
('e3c4d5f6-a7b8-9012-cdef-345678901234', '14e22222-2222-2222-2222-222222222222', 1),
('e3c4d5f6-a7b8-9012-cdef-345678901234', '14e33333-3333-3333-3333-333333333333', 2),
('e3c4d5f6-a7b8-9012-cdef-345678901234', '14e44444-4444-4444-4444-444444444444', 3);

-- ============================================================================
-- PART 6: ADD ALGORITHMS FOR LSE CASES
-- ============================================================================

-- LSE-EO Algorithms
INSERT INTO lib_algorithms (id, case_id, code, sequence, name, popularity) VALUES
-- Skip (no algorithm needed)
(gen_random_uuid(), 'e0111111-1111-1111-1111-111111111111', 'LSE-EO01-01', '', 'Skip', 100),
-- Front Arrow
(gen_random_uuid(), 'e0222222-2222-2222-2222-222222222222', 'LSE-EO02-01', 'M'' U M', 'Standard', 95),
-- Back Arrow
(gen_random_uuid(), 'e0333333-3333-3333-3333-333333333333', 'LSE-EO03-01', 'M U M''', 'Standard', 95),
-- 2 Adjacent / 2
(gen_random_uuid(), 'e0444444-4444-4444-4444-444444444444', 'LSE-EO04-01', 'M2 U'' M'' U'' M''', 'Standard', 80),
-- Front 1 / 1
(gen_random_uuid(), 'e0555555-5555-5555-5555-555555555555', 'LSE-EO05-01', 'M U'' M'' U'' M U'' M''', 'Standard', 75),
(gen_random_uuid(), 'e0555555-5555-5555-5555-555555555555', 'LSE-EO05-02', 'M U M'' U M U M''', 'Alternative', 65),
-- Back 1 / 1
(gen_random_uuid(), 'e0666666-6666-6666-6666-666666666666', 'LSE-EO06-01', 'M'' U'' M U'' M'' U'' M''', 'Standard', 75),
(gen_random_uuid(), 'e0666666-6666-6666-6666-666666666666', 'LSE-EO06-02', 'M'' U M U M'' U M', 'Alternative', 65),
-- 2 Adjacent / 0
(gen_random_uuid(), 'e0777777-7777-7777-7777-777777777777', 'LSE-EO07-01', 'M'' U'' M'' U2 M'' U'' M''', 'Standard', 70),
-- 2 Opposite / 2
(gen_random_uuid(), 'e0888888-8888-8888-8888-888888888888', 'LSE-EO08-01', 'M'' U2 M'' U2 M U'' M''', 'Standard', 70),
-- 2 Opposite / 0
(gen_random_uuid(), 'e0999999-9999-9999-9999-999999999999', 'LSE-EO09-01', 'M'' U'' M U M'' U'' M''', 'Standard', 65),
-- All 6 Misoriented
(gen_random_uuid(), 'e0aaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'LSE-EO10-01', 'M'' U'' M'' U2 M'' U'' M U'' M'' U'' M''', 'Standard', 50);

-- LSE-ULUR Algorithms (mostly intuitive, but key sequences)
INSERT INTO lib_algorithms (id, case_id, code, sequence, name, popularity) VALUES
(gen_random_uuid(), '01010101-1111-1111-1111-111111111111', 'LSE-ULUR01-01', 'M2', 'Insert to UL/UR slots', 100),
(gen_random_uuid(), '01020202-2222-2222-2222-222222222222', 'LSE-ULUR02-01', 'U M2 U''', 'Align then insert', 90),
(gen_random_uuid(), '01030303-3333-3333-3333-333333333333', 'LSE-ULUR03-01', 'M'' U2 M''', 'Bring to same layer', 85),
(gen_random_uuid(), '01040404-4444-4444-4444-444444444444', 'LSE-ULUR04-01', 'U M'' U2 M'' U M2', 'Realign and insert', 80);

-- LSE-L4E Algorithms
INSERT INTO lib_algorithms (id, case_id, code, sequence, name, popularity) VALUES
-- Ua Perm
(gen_random_uuid(), '14e11111-1111-1111-1111-111111111111', 'LSE-L4E01-01', 'M2 U M U2 M'' U M2', 'Standard Ua', 100),
(gen_random_uuid(), '14e11111-1111-1111-1111-111111111111', 'LSE-L4E01-02', 'M2 U M'' U2 M U M2', 'Alternative Ua', 70),
-- Ub Perm
(gen_random_uuid(), '14e22222-2222-2222-2222-222222222222', 'LSE-L4E02-01', 'M2 U'' M U2 M'' U'' M2', 'Standard Ub', 100),
(gen_random_uuid(), '14e22222-2222-2222-2222-222222222222', 'LSE-L4E02-02', 'M2 U'' M'' U2 M U'' M2', 'Alternative Ub', 70),
-- Z Perm
(gen_random_uuid(), '14e33333-3333-3333-3333-333333333333', 'LSE-L4E03-01', 'M2 U M2 U M'' U2 M2 U2 M''', 'Standard Z', 85),
(gen_random_uuid(), '14e33333-3333-3333-3333-333333333333', 'LSE-L4E03-02', 'E2 M'' E2 M', 'Slice Z', 60),
-- H Perm
(gen_random_uuid(), '14e44444-4444-4444-4444-444444444444', 'LSE-L4E04-01', 'M2 U'' M2 U2 M2 U'' M2', 'Standard H', 90),
(gen_random_uuid(), '14e44444-4444-4444-4444-444444444444', 'LSE-L4E04-02', 'M2 U M2 U2 M2 U M2', 'Inverse H', 85);

-- ============================================================================
-- PART 7: TAG CMLL BEGINNER CASES (for two-look CMLL filtering)
-- ============================================================================

-- Update 8 CMLL cases to add level:beginner group for two-look approach
-- These are the most common/easiest cases that form a beginner subset

-- Sune cases (basic)
UPDATE lib_cases
SET groups = array_append(groups, 'level:beginner')
WHERE code IN (
  '3X3-CMLL-S01',   -- Sune Pure
  '3X3-CMLL-AS01'   -- Anti Sune Pure
);

-- H cases (easy recognition)
UPDATE lib_cases
SET groups = array_append(groups, 'level:beginner')
WHERE code IN (
  '3X3-CMLL-H01',   -- H Columns
  '3X3-CMLL-H02'    -- H Rows
);

-- Pi cases (distinct pattern)
UPDATE lib_cases
SET groups = array_append(groups, 'level:beginner')
WHERE code IN (
  '3X3-CMLL-PI01',  -- Pi Right Bar
  '3X3-CMLL-PI02'   -- Pi Left Bar
);

-- U cases (common)
UPDATE lib_cases
SET groups = array_append(groups, 'level:beginner')
WHERE code IN (
  '3X3-CMLL-U01',   -- U Forward
  '3X3-CMLL-U02'    -- U Backward
);

-- ============================================================================
-- VERIFICATION QUERIES (run after migration to verify)
-- ============================================================================

-- Verify case set counts
-- SELECT code, name, expected_count FROM lib_casesets WHERE code LIKE 'roux-lse%';

-- Verify case counts per set
-- SELECT cs.code, COUNT(cc.case_id) as actual_count
-- FROM lib_casesets cs
-- LEFT JOIN lib_caseset_cases cc ON cs.id = cc.caseset_id
-- WHERE cs.code LIKE 'roux-lse%'
-- GROUP BY cs.code;

-- Verify beginner CMLL tags
-- SELECT code, title, groups FROM lib_cases WHERE 'level:beginner' = ANY(groups);
