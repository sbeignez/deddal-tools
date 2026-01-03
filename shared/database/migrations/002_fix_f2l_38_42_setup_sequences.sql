-- Migration: Fix F2L-38 to F2L-42 FR setup sequences (scramble field)
-- Date: 2025-11-22
-- Issue: Case 37 is skipped in F2L numbering, causing index offset for cases 38-42
--
-- The scramble field represents the setup sequence that transforms a solved cube
-- into the case state. These were incorrectly assigned due to the skipped case 37.

-- F2L-38-FR: Edge in slot, corner on top
UPDATE lib_method_cases
SET scramble = 'R U'' R U2'' F R2'' F'' U2'' R2'''
WHERE id = '7dc06020-5025-4ce7-8a3a-615178e98c81';

-- F2L-39-FR: Edge on top, corner in slot (wrong orientation)
UPDATE lib_method_cases
SET scramble = 'R U'' R'' U R U2'' R'' U R U'' R'''
WHERE id = '83666531-9176-4d1b-94fc-2cba34f65969';

-- F2L-40-FR: Edge on top, corner in slot (wrong orientation)
UPDATE lib_method_cases
SET scramble = 'R U'' R'' U'' R U R'' U2'' R U'' R'''
WHERE id = '8c06a47d-2d67-4691-b4ad-653bcb80fb26';

-- F2L-41-FR: Both pieces in slot (wrong orientation)
UPDATE lib_method_cases
SET scramble = 'R U R'' F U R U'' R'' F'' R U R'''
WHERE id = '25f3ac3a-bd1f-4d3d-8916-46b03fb59efd';

-- F2L-42-FR: Both pieces in slot (wrong orientation)
UPDATE lib_method_cases
SET scramble = 'R F U R U'' R'' F'' U'' R'''
WHERE id = '2e678e65-ae5b-4ef8-a69c-00fcbb2749a1';

-- FL slot mirrors (same offset issue)

-- F2L-38-FL: Mirror of FR
UPDATE lib_method_cases
SET scramble = 'L'' U L'' U2'' F'' L2'' F U2'' L2'''
WHERE id = 'd303323b-7b5c-47d9-a8a7-1bf1cd2e26a3';

-- F2L-39-FL: Mirror of FR
UPDATE lib_method_cases
SET scramble = 'L'' U L U'' L'' U2'' L U'' L'' U L'
WHERE id = '2d816020-9df7-4ca2-bd3c-a70f54cb8c1a';

-- F2L-40-FL: Mirror of FR
UPDATE lib_method_cases
SET scramble = 'L'' U L U L'' U'' L U2'' L'' U L'
WHERE id = '31d83476-3933-49ad-9843-0972226a54d8';

-- F2L-41-FL: Mirror of FR
UPDATE lib_method_cases
SET scramble = 'L'' U'' L F'' U'' L'' U L F L'' U'' L'
WHERE id = '423477e1-92fa-48a4-acd8-832a2cd7e013';

-- F2L-42-FL: Mirror of FR
UPDATE lib_method_cases
SET scramble = 'L'' F'' U'' L'' U L F U L'
WHERE id = 'f3368791-65b0-444a-93d5-174459090bd5';

-- Verify the updates
SELECT code, scramble
FROM lib_method_cases
WHERE code IN ('F2L-38-FR', 'F2L-39-FR', 'F2L-40-FR', 'F2L-41-FR', 'F2L-42-FR',
               'F2L-38-FL', 'F2L-39-FL', 'F2L-40-FL', 'F2L-41-FL', 'F2L-42-FL')
ORDER BY code;
