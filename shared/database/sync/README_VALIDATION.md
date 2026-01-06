# Algorithm Submission Validation Tools

## Overview

Three validation scripts for user-submitted algorithms, each with different capabilities:

| Script | Notation | Duplicates | Solves Case | Speed |
|--------|----------|------------|-------------|-------|
| `validate_pending_submissions.py` | ✅ | ✅ | ❌ | Fast |
| `validate_submissions_complete.py` | ✅ | ✅ | ⚠️ (pycuber) | Fast |
| `validate_with_cube_engine.py` | ✅ | ✅ | ✅ (iOS engine) | Slow |

## 1. Basic Validation (Python Only)

**Script**: `validate_pending_submissions.py`

**What it checks**:
- ✅ Move notation validity (R, U, F, L, D, B, M, E, S, x, y, z, wide moves)
- ✅ Case exists in database
- ✅ Exact duplicate detection
- ❌ Does NOT verify if algorithm solves the case

**Usage**:
```bash
python3 validate_pending_submissions.py
```

**Output Example**:
```
====================================================================================================
VALIDATION SUMMARY
====================================================================================================
Total submissions: 5
🟢 Valid (new): 4
🟡 Valid (duplicate): 0
🔴 Invalid: 1
====================================================================================================
```

**Best for**: Quick validation of notation and duplicates

---

## 2. Complete Validation (Python + pycuber)

**Script**: `validate_submissions_complete.py`

**What it checks**:
- ✅ Everything from basic validation
- ✅ **Algorithm solving verification** (if pycuber installed)

**Setup**:
```bash
pip install pycuber
```

**Usage**:
```bash
python3 validate_submissions_complete.py
```

**Limitations**:
- ⚠️ pycuber uses different cube representation than iOS
- ⚠️ Wide moves (r, f, u) may not work exactly the same
- ⚠️ Not 100% accurate for edge cases

**Best for**: Quick validation with solving check (90% accuracy)

---

## 3. Full iOS Cube Engine Validation (Swift)

**Script**: `validate_with_cube_engine.py`

**What it checks**:
- ✅ Everything from basic validation
- ✅ **Exact iOS cube engine validation** (same code as app)
- ✅ Suboptimal move pattern detection
- ✅ 100% accurate solving verification

**Setup**:

1. Add `DeddalTests/CLI/AlgorithmValidationCLI.swift` to Xcode project:
   - Open `Deddal.xcodeproj` in Xcode
   - Right-click `DeddalTests` folder → Add Files
   - Select `DeddalTests/CLI/AlgorithmValidationCLI.swift`
   - Ensure "DeddalTests" target is checked

2. Build to verify:
   ```bash
   xcodebuild -project Deddal.xcodeproj -scheme "1. DEV Scheme" -destination 'platform=iOS Simulator,name=iPhone 17 Pro' clean build
   ```

**Usage**:
```bash
python3 validate_with_cube_engine.py
```

**How it works**:
1. Python fetches pending submissions from Supabase
2. Writes algorithm data to temp JSON file
3. Runs Swift test via xcodebuild
4. Swift test uses `ValidateAlgorithmUseCase` (same as iOS app)
5. Python reads validation results from output JSON
6. Displays results

**Best for**: Production validation before approving submissions

---

## Complete Approval Workflow

### Recommended Production Workflow:

**Step 1: Query Pending Submissions**
```bash
python3 query_pending_submissions.py
```
Shows who submitted what, with user emails.

**Step 2: Validate Submissions**
```bash
# Quick validation (notation + duplicates)
python3 validate_pending_submissions.py

# OR Full validation (notation + duplicates + solving)
python3 validate_with_cube_engine.py
```

**Step 3: Approve Valid Submissions**
```bash
# Interactive mode (prompts for each submission)
python3 approve_submissions.py

# Auto-approve with dry-run (preview changes)
python3 approve_submissions.py --auto-approve --dry-run

# Auto-approve (production - adds to database)
python3 approve_submissions.py --auto-approve
```

**What `approve_submissions.py` does**:
1. ✅ Validates each submission (notation, case exists, duplicates)
2. ✅ Adds valid algorithms to `lib_algorithms` table
3. ✅ Generates unique algorithm codes (e.g., `3X3-OCLL-L-USR-001`)
4. ✅ Updates submission status to 'approved' or 'rejected'
5. ✅ Tracks reviewer and timestamp

---

### Quick Approval (all-in-one):

```bash
# Dry run (preview only)
python3 approve_submissions.py --auto-approve --dry-run

# Production (approve and add to database)
python3 approve_submissions.py --auto-approve
```

---

## Other Scripts

### Query Pending Submissions
**Script**: `query_pending_submissions.py`

Shows pending submissions with user details (email):
```bash
python3 query_pending_submissions.py
```

### Review and Approve
**Script**: `review_algorithm_submissions.py`

Approve or reject submissions:
```bash
# Dry run (preview)
python3 review_algorithm_submissions.py --all --dry-run

# Auto-approve all valid
python3 review_algorithm_submissions.py --all --auto-approve

# Reject specific submission
python3 review_algorithm_submissions.py --reject <uuid> --reason "Invalid notation"
```

---

## Environment Setup

All scripts require:
```bash
export SUPABASE_SERVICE_ROLE_KEY="your-service-role-key"
pip install supabase
```

For `validate_submissions_complete.py` (optional):
```bash
pip install pycuber
```

---

## Validation Results Explained

### Status Codes:
- 🟢 **VALID** - Ready for review/approval
- 🟡 **VALID BUT DUPLICATE** - Already exists in database
- 🔴 **INVALID** - Has errors, cannot be approved

### Common Issues:

1. **Case NOT found**: Incorrect case code format
   - Example: "OLL-22" should be "3X3-CFOP-OLL-22"
   - Fix: Update submission case_code in database

2. **Invalid move notation**: Unsupported move
   - Valid: R, U, F, L, D, B, M, E, S, x, y, z (with ', 2)
   - Valid: r, u, f, l, d, b (wide moves)
   - Invalid: T, W, custom notation

3. **Algorithm doesn't solve case**: Wrong algorithm or scramble
   - Verify scramble in lib_cases table is correct
   - Test algorithm manually in app

4. **Duplicate**: Exact same algorithm already exists
   - Check if user wants to mark as alternative
   - Or reject with "Duplicate submission" reason

---

## File Locations

```
tools/shared/database/sync/
├── query_pending_submissions.py          # Query with user details
├── validate_pending_submissions.py       # Basic validation (notation + duplicates)
├── validate_submissions_complete.py      # Complete validation (+ solving via pycuber)
├── validate_with_cube_engine.py         # iOS engine validation (Swift wrapper)
├── approve_submissions.py               # ⭐ Validate + approve/reject (recommended)
├── review_algorithm_submissions.py       # Legacy approval script
└── README_VALIDATION.md                  # This file

DeddalTests/CLI/
└── AlgorithmValidationCLI.swift         # Swift test for cube engine validation
```

**Main Scripts**:
- **approve_submissions.py** - All-in-one validation and approval (recommended)
- **review_algorithm_submissions.py** - Legacy script (more features, more complex)

---

## Architecture

### iOS Validation Flow:
```
Python → Temp JSON → xcodebuild → Swift Test → ValidateAlgorithmUseCase
                                                       ↓
                                                   FacesCube
                                                   MoveSequence
                                                       ↓
                                              Validation Result
                                                       ↓
                                         Output JSON ← Python
```

### Why Three Scripts?

1. **validate_pending_submissions.py**: Fast, no dependencies, good for quick checks
2. **validate_submissions_complete.py**: Medium accuracy, uses Python cube library
3. **validate_with_cube_engine.py**: 100% accurate, uses exact iOS code

---

## Troubleshooting

### "SUPABASE_SERVICE_ROLE_KEY not set"
```bash
export SUPABASE_SERVICE_ROLE_KEY="your-key-here"
```

### "pycuber not available"
```bash
pip install pycuber
# Or use validate_pending_submissions.py instead
```

### "xcodebuild exited with code 65"
- Swift test file not added to Xcode project
- Follow setup instructions in section 3 above

### "Failed to get validation results"
- Check that DeddalTests/CLI/AlgorithmValidationCLI.swift is in Xcode
- Verify test target includes the file
- Run xcodebuild manually to see detailed errors

---

## Future Improvements

- [ ] Add batch processing for large submission queues
- [ ] Email notifications to users on approval/rejection
- [ ] Automatic duplicate merging
- [ ] Performance benchmarking (avg moves, execution time)
- [ ] Integration with GitHub Actions for CI/CD
