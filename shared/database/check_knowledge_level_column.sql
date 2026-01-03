-- Check the data type of the knowledge_level column in lib_user_algorithms
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default,
    character_maximum_length,
    numeric_precision
FROM information_schema.columns
WHERE table_name = 'lib_user_algorithms'
  AND column_name = 'knowledge_level';
