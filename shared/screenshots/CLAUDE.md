# Screenshot Automation - Claude Instructions

This file contains instructions for AI assistants (Claude) working on the screenshot automation system.

---

## Critical Rules

### ⚠️ NEVER Delete Full Output Folders

**NEVER** execute or suggest commands like:
- `rm -rf output/`
- `rm -rf output/1-snap/`
- `rm -rf output/2-frame/`
- `rm -rf output/3-background/`
- `rm -rf output/4-text/`
- Any variation that deletes entire step folders

**Why this is critical:**
- Breaks the pipeline by removing directory structure
- Loses all screenshots (no recovery possible)
- The automatic file-by-file replacement already handles cleanup correctly
- Partial runs would lose all progress

### ✅ Correct Cleanup Approaches

**1. Automatic file-by-file replacement (default):**
- Scripts 1-4 automatically delete old versions before saving new ones
- No manual intervention needed
- Safe for partial runs

**2. Manual cleanup script (when needed):**
```bash
# Archive raw screenshots and clean all
./scripts/0_cleanup.sh --archive

# Keep raw screenshots, delete processed outputs
./scripts/0_cleanup.sh --keep-snap
```

**3. Individual file deletion (rare):**
```bash
# Delete specific old files by pattern (if absolutely necessary)
find output/1-snap/en-US/iPhone17PM -name "20251104.*.png" -delete
```

---

## File Replacement Strategy

### How It Works

Each script implements file-by-file replacement:
1. Extract pattern from filename (without timestamp)
2. Find old files matching pattern
3. Delete old versions
4. Save new file

**Example:**
```bash
# Pattern: iPhone17PM.V.01.Home.en-US.png (no timestamp)
# Deletes: 20251105.1338.iPhone17PM.V.01.Home.en-US.png (old)
# Saves:   20251105.1442.iPhone17PM.V.01.Home.en-US.png (new)
```

### Safety Features

- **One file at a time**: Crash-safe, unprocessed files keep old versions
- **Atomic operation**: Old deleted only before new save
- **Timestamp preserved**: Each run has unique timestamp for tracking
- **Silent failures**: No errors if old file doesn't exist

---

## System Architecture

### Pipeline Overview

```
1_snap.sh → 2_frame.sh → 3_background.sh → 4_text.sh → 5_upload.sh
```

Each step:
1. Reads input from previous step (or generates new)
2. Deletes old version of each file being processed
3. Processes and saves new version
4. Continues to next file

### Filename Format

**Steps 1-2:** `{TIMESTAMP}.{DEVICE}.{ORIENTATION}.{SCREENSHOT_ID}.{LANGUAGE}.png`
**Steps 3-4:** `{TIMESTAMP}.{DEVICE}.{ORIENTATION}.{POSITION}.{SCREENSHOT_ID}.{LANGUAGE}.png`
**Step 4 final:** `{TIMESTAMP}.{DEVICE}.{ORIENTATION}.{POSITION}.{SCREENSHOT_ID}.{LANG_SNAP}.{LANG_TEXT}.png`

**Timestamp format:** `YYYYMMDD.HHMM` (minute precision)

---

## Code Modification Guidelines

### When Modifying Scripts 1-4

If you need to modify the file saving logic:

1. **Always preserve the cleanup pattern:**
   ```bash
   # Delete old versions first
   local pattern=$(echo "${filename}" | cut -d'.' -f3-)
   find "${output_dir}" -name "*.${pattern}" ! -name "${filename}" -delete 2>/dev/null || true

   # Then save new file
   [save operation]
   ```

2. **Never remove the cleanup logic** - it prevents file accumulation

3. **Test partial runs** - ensure crashed scripts don't corrupt output

### When Adding New Steps

If creating a new processing step (e.g., 6_watermark.sh):

1. **Implement file-by-file cleanup** using the same pattern as scripts 1-4
2. **Document in README.md and ARCHITECTURE.md**
3. **Update this CLAUDE.md** with new step information

---

## Common Tasks

### Debugging Failed Runs

```bash
# Check output directories for file counts
find output/1-snap -name "*.png" | wc -l
find output/2-frame -name "*.png" | wc -l
find output/3-background -name "*.png" | wc -l
find output/4-text -name "*.png" | wc -l

# Check for mixed timestamps (indicates partial run)
find output/1-snap -name "*.png" | cut -d'.' -f1-2 | sort -u

# Check logs
tail -100 /tmp/screenshot_*.log
```

### Re-running Failed Steps

```bash
# Re-run specific step (automatic cleanup happens)
./scripts/2_frame.sh   # Replaces old framed versions
./scripts/3_background.sh  # Replaces old background versions
./scripts/4_text.sh    # Replaces old text versions
```

### Updating Configuration

```bash
# story_metadata.json - Visual storytelling (SOURCE OF TRUTH)
# screenshot_metadata.json - Text content per language
# language_mappings.json - 39-language fallback chain

# After config changes, re-run affected steps
./scripts/3_background.sh  # If story colors changed
./scripts/4_text.sh        # If text content changed
```

---

## Testing Changes

### Test File-by-File Replacement

```bash
# Run once
./scripts/1_snap.sh
ls -la output/1-snap/en-US/iPhone17PM/*.png  # Note timestamp

# Wait 1 minute, run again
./scripts/1_snap.sh
ls -la output/1-snap/en-US/iPhone17PM/*.png  # New timestamp, same file count
```

### Test Crash Recovery

```bash
# Start a run
./scripts/2_frame.sh &
PID=$!

# Kill mid-run
sleep 5
kill $PID

# Check output - should have mix of old and new timestamps
find output/2-frame -name "*.png" | cut -d'.' -f1-2 | sort -u

# Re-run - completes missing files, replaces old ones
./scripts/2_frame.sh
```

---

## Version Control

### Files to Commit

- ✅ Scripts (scripts/*.sh)
- ✅ Config (config/*.json)
- ✅ Documentation (*.md)
- ✅ Assets (assets/frames/, assets/fonts/)
- ❌ Output (output/**/*.png) - git ignored
- ❌ Archive (archive/**) - git ignored

### Commit Guidelines

Follow parent repository's commit message format:
```
Brief description of changes

Generated by Trophee Ltd
```

---

## References

- **README.md** - User-facing documentation
- **ARCHITECTURE.md** - Technical deep dive
- **AI_LOGS.md** - Historical implementation log

---

Generated by Trophee Ltd
