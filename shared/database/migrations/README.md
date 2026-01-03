# Database Migrations

This folder contains SQL migrations for the Supabase database backend.

## Migration Files

### 001_add_onboarding_fields.sql
- **Purpose**: Add onboarding-related fields to user_settings table
- **Date**: 2024-11-01
- **Status**: ✅ Applied
- **Fields Added**:
  - skill_level
  - primary_goal
  - learning_preference
  - onboarding_completed_at
  - onboarding_version
  - first_launch_date

### 002_avatar_storage_rls_policies.sql
- **Purpose**: Enable Row-Level Security (RLS) policies for avatar uploads
- **Date**: 2025-11-17
- **Status**: ⚠️ **PENDING - NEEDS TO BE APPLIED**
- **Policies Created**:
  - Users can upload their own avatar (INSERT)
  - Users can update their own avatar (UPDATE)
  - Users can delete their own avatar (DELETE)
  - Authenticated users can view any avatar (SELECT)

## How to Apply Migrations

### Option 1: Supabase Dashboard (Recommended)

1. Open [Supabase Dashboard](https://supabase.com/dashboard)
2. Navigate to your project → SQL Editor
3. Copy the SQL from the migration file
4. Paste into SQL Editor
5. Click "Run" to execute

### Option 2: Supabase MCP Tool (via Claude)

If you have the Supabase MCP server configured:

```
Use the mcp__supabase__apply_migration tool with:
- project_id: your-project-id
- name: 002_avatar_storage_rls_policies
- query: <contents of SQL file>
```

### Option 3: Supabase CLI

```bash
# Install Supabase CLI if not already installed
brew install supabase/tap/supabase

# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref your-project-ref

# Run migration
supabase db push --db-url <your-database-url>
```

## Verification

After applying a migration, verify it was successful:

### For 002_avatar_storage_rls_policies.sql

Run this query in Supabase SQL Editor:

```sql
-- Check that policies exist
SELECT policyname, cmd, roles
FROM pg_policies
WHERE tablename = 'objects'
AND policyname LIKE '%avatar%';
```

You should see 4 policies:
1. Users can upload their own avatar (INSERT)
2. Users can update their own avatar (UPDATE)
3. Users can delete their own avatar (DELETE)
4. Authenticated users can view any avatar (SELECT)

### Test Avatar Upload

After applying the migration:

1. Run the iOS app
2. Navigate to Settings → Account
3. Tap on profile photo to upload avatar
4. Check the logs for successful upload:
   ```
   [Storage] Avatar uploaded successfully: https://...
   [Queue] Successfully uploaded avatar for: <user-id>
   ```

## Current Issue (2025-11-17)

**Problem**: Avatar uploads are failing with:
```
[Storage] Avatar upload failed: new row violates row-level security policy
```

**Root Cause**: The `avatars` storage bucket exists but has no RLS policies allowing authenticated users to upload files.

**Solution**: Apply migration `002_avatar_storage_rls_policies.sql` to create the required policies.

## Storage Bucket Prerequisites

Before applying `002_avatar_storage_rls_policies.sql`, ensure the `avatars` storage bucket exists:

**Bucket Configuration** (create in Supabase Dashboard → Storage):
- **Name**: `avatars`
- **Public**: ✅ Yes (enables CDN caching and public profile viewing)
- **File size limit**: 5 MB
- **Allowed MIME types**: `image/jpeg`, `image/png`

If the bucket doesn't exist, create it first before running the migration.

## Related iOS Code

After applying RLS policies, the following iOS components will work correctly:

- **SupabaseManager+Storage.swift**: `uploadAvatar()`, `deleteAvatar()`
- **AvatarUploadQueue.swift**: Background upload queue with retry logic
- **ImageProcessor.swift**: `processAvatarImage()` - resize/compress to 500x500 JPEG
- **UserRepository**: `updateProfilePhotoURL()` - sync URL to user_settings table
- **AccountSettingsView**: Profile photo picker UI

## Migration Best Practices

1. **Test in Development First**: Always test migrations in a dev/staging environment before production
2. **Backup Before Applying**: Supabase automatically backs up, but manual snapshots are recommended
3. **Review Policies**: Check that RLS policies don't inadvertently block legitimate access
4. **Monitor Logs**: After applying, monitor Supabase logs for RLS policy violations
5. **Document Changes**: Update this README when adding new migrations

## Troubleshooting

### "Policy already exists" error
If you see `ERROR: policy "..." already exists`, the migration was previously applied. Check:
```sql
SELECT * FROM pg_policies WHERE tablename = 'objects';
```

### RLS still blocking uploads after migration
1. Verify policies were created (see Verification section above)
2. Check that user is authenticated (`auth.uid()` returns valid UUID)
3. Verify file path matches policy: `avatars/{user_id}/avatar_*.jpg`
4. Check Supabase logs for detailed error messages

### Rolling back a migration
Each migration file includes rollback instructions in comments. For `002_avatar_storage_rls_policies.sql`:
```sql
DROP POLICY IF EXISTS "Users can upload their own avatar" ON storage.objects;
DROP POLICY IF EXISTS "Users can update their own avatar" ON storage.objects;
DROP POLICY IF EXISTS "Users can delete their own avatar" ON storage.objects;
DROP POLICY IF EXISTS "Authenticated users can view any avatar" ON storage.objects;
```

## Future Migrations

When creating new migrations:
1. Use sequential numbering: `003_description.sql`, `004_description.sql`, etc.
2. Include date and purpose in file header
3. Add rollback instructions
4. Update this README with migration details
5. Test thoroughly before committing
