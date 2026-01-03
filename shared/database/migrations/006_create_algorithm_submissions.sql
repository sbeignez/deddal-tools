-- Migration: create_algorithm_submissions_table
-- Applied: 2025-11-23
-- Description: Create table for user-submitted algorithm suggestions
--
-- This migration was applied via Supabase MCP.

CREATE TABLE lib_algorithm_submissions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  case_id UUID REFERENCES lib_cases(id),
  case_code TEXT NOT NULL,
  sequence TEXT NOT NULL,
  notes TEXT,
  submitted_by UUID REFERENCES auth.users(id),
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
  created_at TIMESTAMPTZ DEFAULT now(),
  reviewed_at TIMESTAMPTZ,
  reviewed_by UUID REFERENCES auth.users(id),
  rejection_reason TEXT
);

-- Indexes
CREATE INDEX idx_algorithm_submissions_status ON lib_algorithm_submissions(status);
CREATE INDEX idx_algorithm_submissions_submitted_by ON lib_algorithm_submissions(submitted_by);
CREATE INDEX idx_algorithm_submissions_case_id ON lib_algorithm_submissions(case_id);

-- Enable RLS
ALTER TABLE lib_algorithm_submissions ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can submit algorithms"
  ON lib_algorithm_submissions FOR INSERT TO authenticated
  WITH CHECK (auth.uid() = submitted_by);

CREATE POLICY "Users can view own submissions"
  ON lib_algorithm_submissions FOR SELECT TO authenticated
  USING (auth.uid() = submitted_by);

CREATE POLICY "Admins can view all submissions"
  ON lib_algorithm_submissions FOR SELECT TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = auth.uid()
      AND (auth.users.email LIKE '%@trophee.co' OR auth.users.email = 'sbeignez@gmail.com')
    )
  );

CREATE POLICY "Admins can update submissions"
  ON lib_algorithm_submissions FOR UPDATE TO authenticated
  USING (
    EXISTS (
      SELECT 1 FROM auth.users
      WHERE auth.users.id = auth.uid()
      AND (auth.users.email LIKE '%@trophee.co' OR auth.users.email = 'sbeignez@gmail.com')
    )
  );

-- Edge Function: submit-algorithm (deployed separately)
-- - Validates user, inserts submission, sends email to deddal@trophee.com.hk
-- - Rate limit: 5 submissions/day per user

-- Status: APPLIED via Supabase MCP
-- Supabase migration version: 20251123220308
