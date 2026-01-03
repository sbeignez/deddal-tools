-- Migration: Avatar Storage RLS Policies
-- Purpose: Enable Row-Level Security policies for the 'avatars' storage bucket
-- Date: 2025-11-17
--
-- This migration creates RLS policies to allow authenticated users to:
-- 1. Upload their own avatar (INSERT)
-- 2. Update their own avatar (UPDATE)
-- 3. Delete their own avatar (DELETE)
-- 4. Read any avatar (SELECT) for public profile viewing
--
-- Security Model:
-- - Users can only modify avatars in folders matching their auth.uid()
-- - Folder structure: avatars/{user_id}/avatar_{timestamp}.jpg
-- - All authenticated users can view any avatar (for profile display)

-- ============================================================================
-- STORAGE BUCKET CONFIGURATION
-- ============================================================================

-- Enable RLS on the avatars bucket (if not already enabled)
-- Note: This assumes the 'avatars' bucket exists. If not, create it first in Supabase dashboard:
-- Bucket name: avatars
-- Public: true (for CDN caching and public profile viewing)
-- File size limit: 5MB
-- Allowed MIME types: image/jpeg, image/png

-- ============================================================================
-- RLS POLICIES
-- ============================================================================

-- Policy 1: Allow users to upload their own avatar
-- Grants INSERT permission for files in user's own folder
CREATE POLICY "Users can upload their own avatar"
ON storage.objects
FOR INSERT
TO authenticated
WITH CHECK (
    bucket_id = 'avatars'
    AND (storage.foldername(name))[1] = auth.uid()::text
);

-- Policy 2: Allow users to update their own avatar
-- Grants UPDATE permission for files in user's own folder
CREATE POLICY "Users can update their own avatar"
ON storage.objects
FOR UPDATE
TO authenticated
USING (
    bucket_id = 'avatars'
    AND (storage.foldername(name))[1] = auth.uid()::text
)
WITH CHECK (
    bucket_id = 'avatars'
    AND (storage.foldername(name))[1] = auth.uid()::text
);

-- Policy 3: Allow users to delete their own avatar
-- Grants DELETE permission for files in user's own folder
CREATE POLICY "Users can delete their own avatar"
ON storage.objects
FOR DELETE
TO authenticated
USING (
    bucket_id = 'avatars'
    AND (storage.foldername(name))[1] = auth.uid()::text
);

-- Policy 4: Allow all authenticated users to view any avatar
-- Grants SELECT permission for public profile viewing
-- This enables users to see other users' profile pictures
CREATE POLICY "Authenticated users can view any avatar"
ON storage.objects
FOR SELECT
TO authenticated
USING (bucket_id = 'avatars');

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Run these queries to verify the policies were created successfully:

-- 1. List all policies on storage.objects for the avatars bucket
-- SELECT policyname, cmd, roles, qual, with_check
-- FROM pg_policies
-- WHERE tablename = 'objects'
-- AND policyname LIKE '%avatar%';

-- 2. Test policy with simulated user (replace with actual user ID)
-- SET LOCAL role TO authenticated;
-- SET LOCAL "request.jwt.claim.sub" TO 'your-user-uuid-here';
-- SELECT * FROM storage.objects WHERE bucket_id = 'avatars';

-- ============================================================================
-- ROLLBACK INSTRUCTIONS
-- ============================================================================

-- To remove these policies (for testing or rollback):
-- DROP POLICY IF EXISTS "Users can upload their own avatar" ON storage.objects;
-- DROP POLICY IF EXISTS "Users can update their own avatar" ON storage.objects;
-- DROP POLICY IF EXISTS "Users can delete their own avatar" ON storage.objects;
-- DROP POLICY IF EXISTS "Authenticated users can view any avatar" ON storage.objects;

-- ============================================================================
-- ADDITIONAL NOTES
-- ============================================================================

-- Storage folder structure:
-- avatars/
--   ├── {user_id_1}/
--   │   └── avatar_1700000000.jpg
--   ├── {user_id_2}/
--   │   └── avatar_1700000001.jpg
--   └── ...

-- Image specifications (enforced by iOS ImageProcessor):
-- - Format: JPEG
-- - Dimensions: 500x500px (square, cropped from center)
-- - Quality: 80%
-- - Max size: ~200KB (after compression)
-- - Cache-Control: public, max-age=31536000 (1 year CDN cache)

-- Related iOS code:
-- - SupabaseManager+Storage.swift: uploadAvatar(), deleteAvatar()
-- - AvatarUploadQueue.swift: Background upload queue with retry logic
-- - ImageProcessor.swift: processAvatarImage() - resize and compress
-- - UserRepository: updateProfilePhotoURL() - sync URL to user_settings table
