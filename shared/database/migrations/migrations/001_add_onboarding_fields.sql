-- ================================================
-- Migration: Add Onboarding Fields to user_settings
-- ================================================
--
-- PURPOSE: Add onboarding-related columns to user_settings table
--          to support cross-device onboarding state synchronization
--
-- DATE: 2025-11-01
-- RELATED: feature/supabase-live-testing, OnboardingManager.swift
--
-- TESTING: After running this migration, verify with:
--   SELECT column_name, data_type
--   FROM information_schema.columns
--   WHERE table_name = 'user_settings'
--   ORDER BY ordinal_position;
--
-- ================================================

-- Add onboarding fields to user_settings table
ALTER TABLE user_settings
  ADD COLUMN IF NOT EXISTS skill_level TEXT,
  ADD COLUMN IF NOT EXISTS primary_goal TEXT,
  ADD COLUMN IF NOT EXISTS learning_preference TEXT,
  ADD COLUMN IF NOT EXISTS onboarding_completed_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS onboarding_version TEXT DEFAULT '1.0',
  ADD COLUMN IF NOT EXISTS first_launch_date TIMESTAMPTZ;

-- Add helpful comments for documentation
COMMENT ON COLUMN user_settings.skill_level IS
  'User skill level: beginner, intermediate, or advanced';

COMMENT ON COLUMN user_settings.primary_goal IS
  'Primary learning goal: learn_new, improve_speed, find_better, or track_progress';

COMMENT ON COLUMN user_settings.learning_preference IS
  'Learning preference: videos, text, practice, or mix';

COMMENT ON COLUMN user_settings.onboarding_completed_at IS
  'Timestamp when user completed onboarding flow';

COMMENT ON COLUMN user_settings.onboarding_version IS
  'Version of onboarding flow completed (for tracking changes)';

COMMENT ON COLUMN user_settings.first_launch_date IS
  'First time user launched the app (for analytics and lapsed user detection)';

-- ================================================
-- Verification Query
-- ================================================
--
-- Run this to verify migration succeeded:
--
-- SELECT
--   column_name,
--   data_type,
--   is_nullable,
--   column_default
-- FROM information_schema.columns
-- WHERE table_name = 'user_settings'
--   AND column_name IN (
--     'skill_level',
--     'primary_goal',
--     'learning_preference',
--     'onboarding_completed_at',
--     'onboarding_version',
--     'first_launch_date'
--   )
-- ORDER BY column_name;
--
-- Expected result: 6 rows showing the new columns
--
-- ================================================
