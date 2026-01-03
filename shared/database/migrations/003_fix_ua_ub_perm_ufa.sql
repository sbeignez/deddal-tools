-- Fix Ua-Perm and Ub-Perm scrambles with [U2] UFA prefix
-- The U2 adjustment aligns the rendered case image with the VisualCube assets
-- Generated 2025-11-23

BEGIN;

UPDATE lib_cases SET scramble = '[U2] M2'' U'' M'' U2'' M U'' M2''' WHERE code = 'Ua-Perm';
UPDATE lib_cases SET scramble = '[U2] M2'' U M'' U2'' M U M2''' WHERE code = 'Ub-Perm';

COMMIT;
