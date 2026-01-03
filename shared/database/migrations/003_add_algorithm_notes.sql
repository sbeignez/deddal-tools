-- Migration: Add alg_notes column to lib_user_algorithms table
-- Purpose: Enable sync of user's algorithm notes between local and cloud
-- Created: 2025-01-18

-- Add alg_notes column to lib_user_algorithms table
ALTER TABLE lib_user_algorithms
ADD COLUMN alg_notes TEXT;

-- Update existing rows to have empty string instead of NULL
-- This ensures consistent behavior with local SwiftData model
UPDATE lib_user_algorithms
SET alg_notes = ''
WHERE alg_notes IS NULL;

-- No index needed - alg_notes is not queried for filtering/sorting
-- Notes are always fetched alongside their parent algorithm record
