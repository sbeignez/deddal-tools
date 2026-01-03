-- Fix OcLL setupSequence (scramble) values
-- The scramble values were incorrectly set to algorithms instead of proper setup moves
-- Generated for 4 OcLL cases

BEGIN;

UPDATE lib_cases SET scramble = 'F R'' F'' r U R U'' r''' WHERE code = '3X3-OCLL-T';
UPDATE lib_cases SET scramble = 'R'' F'' r U R U'' r'' F' WHERE code = '3X3-OCLL-L';
UPDATE lib_cases SET scramble = 'R U R'' U R U2'' R''' WHERE code = '3X3-OCLL-ANTISUNE';
UPDATE lib_cases SET scramble = 'R U2'' R'' U'' R U'' R''' WHERE code = '3X3-OCLL-SUNE';

COMMIT;
