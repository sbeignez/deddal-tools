-- Quick verification: Does alg_notes column exist?
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'lib_user_algorithms'
  AND column_name = 'alg_notes';
