# Screenshot Automation - Architecture

This document provides a technical deep dive into the screenshot automation architecture, focusing on the story-driven visual storytelling system.

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Story-Driven Architecture](#story-driven-architecture)
3. [Filename Format Evolution](#filename-format-evolution)
4. [Configuration Files](#configuration-files)
5. [Pipeline Stages (Detailed)](#pipeline-stages-detailed)
6. [Per-Screenshot Theming](#per-screenshot-theming)
7. [Error Handling](#error-handling)
8. [Testing Strategy](#testing-strategy)
9. [Automation Conventions](#automation-conventions)
10. [Future Enhancements](#future-enhancements)

---

## System Overview

The screenshot automation system is a **5-stage pipeline**:

```
┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐
│   SNAP     │──▶│   FRAME    │──▶│ BACKGROUND │──▶│    TEXT    │──▶│   UPLOAD   │
│(xcodebuild)│   │(ImageMagick)│   │  (Story)   │   │(39 langs)  │   │ (Fastlane) │
└────────────┘   └────────────┘   └────────────┘   └────────────┘   └────────────┘
  ~2min/device    ~10sec          ~20sec          ~30sec           ~1-2min
```

### Key Innovations

1. **Story-Driven Backgrounds**: Per-screenshot visual styling with rainbow gradient progressions
2. **Multi-Language Generation**: 39 App Store languages from 5 captured screenshots
3. **Error Resilience**: `_ERROR` suffix fallback for failed captures
4. **Per-Screenshot Theming**: Dynamic light/dark theme switching during capture
5. **Natural Ordering**: Position-based filenames (01-10) for App Store sequence

---

## Story-Driven Architecture

### Problem Statement

The original pipeline generated all screenshots with uniform backgrounds. There was no way to:
1. Define canonical sequence of 10 App Store screenshots
2. Create visual progressions (e.g., rainbow colors)
3. Apply per-screenshot background styles
4. Ensure natural ordering for uploads

### Solution: Story Metadata

**`story_metadata.json` is the SOURCE OF TRUTH** for the entire visual pipeline. It defines:
- Which 10 screenshots appear in the App Store
- Their sequence (positions 1-10)
- Visual styling per screenshot (background style, theme, colors)

### Key Design Decisions

1. **Single Canonical Story**: One universal story across all devices
2. **Late Filtering**: Steps 1-2 generate all screenshots, Step 3 filters to story
3. **Position in Filename**: Position (01-10) added at Step 3 for natural sorting
4. **Visual Storytelling**: Support gradient (2-color) and mesh (4-corner) backgrounds
5. **Per-Screenshot Control**: Each position has independent style, theme, colors

---

## Filename Format Evolution

### Steps 1-2 (Before Story Filtering)

```
Format: {TIMESTAMP}.{DEVICE}.{ORIENTATION}.{SCREENSHOT_ID}.{LANGUAGE}.png
Example: 20251104.1942.iPhone17PM.V.AppLaunch.en-US.png
Fields: 6 (timestamp.timestamp.device.orientation.screenshot_id.language)
```

### Steps 3-5 (After Story Filtering)

```
Format: {TIMESTAMP}.{DEVICE}.{ORIENTATION}.{POSITION}.{SCREENSHOT_ID}.{LANGUAGE}.png
Example: 20251104.1942.iPhone17PM.V.01.AppLaunch.en-US.png
Fields: 7 (timestamp.timestamp.device.orientation.position.screenshot_id.language)
```

**Position Field:**
- Format: Two-digit zero-padded (01-10)
- Purpose: Natural sorting for App Store
- Location: Between orientation and screenshot_id
- When Added: Step 3 (background generation)
- Function: `printf "%02d" ${position}`

### Step 4 Output (With Text Languages)

```
Format: {TIMESTAMP}.{DEVICE}.{ORIENTATION}.{POSITION}.{SCREENSHOT_ID}.{LANG_SNAP}.{LANG_TEXT}.png
Example: 20251104.1942.iPhone17PM.V.01.AppLaunch.en-US.fr-FR.png
Fields: 8 (adds lang_text for generated text language)
```

This allows Portuguese text on Spanish screenshots: `...es-ES.pt-BR.png`

---

## Automatic File Replacement

### File-by-File Cleanup Strategy

Each script (1-4) implements automatic file replacement to maintain **exactly one version** of each screenshot. Before saving a new file, the script deletes old versions with different timestamps.

### Implementation

**Pattern Matching Logic:**
```bash
# Extract pattern by removing timestamp (first 2 fields)
local pattern=$(echo "${filename}" | cut -d'.' -f3-)

# Find and delete old versions matching pattern (excluding current file)
find "${output_dir}" -name "*.${pattern}" ! -name "${filename}" -delete 2>/dev/null || true
```

**Example:**
```bash
# New file: 20251105.1442.iPhone17PM.V.01.Home.en-US.png
# Pattern:  iPhone17PM.V.01.Home.en-US.png (timestamp removed)

# Finds:    20251105.1338.iPhone17PM.V.01.Home.en-US.png (old timestamp)
# Excludes: 20251105.1442.iPhone17PM.V.01.Home.en-US.png (current file)
# Deletes:  Old version
# Saves:    New version
```

### Safety Features

1. **File-by-file processing**: Each file is handled individually
   - If script crashes, only current file is affected
   - Unprocessed files retain old versions

2. **Atomic replacement**: Old version deleted only before new save
   - Prevents loss if new save fails
   - Always have at least one version available

3. **Silent failures**: `2>/dev/null || true` prevents errors
   - No error if old file doesn't exist (first run)
   - Pipeline continues regardless

4. **Timestamp preservation**: Each run gets unique timestamp
   - Can identify when screenshots were captured
   - Useful for debugging and version tracking

### Script Locations

**1_snap.sh** (Lines 310-312):
```bash
# Delete old versions of this screenshot (keep only latest timestamp)
local pattern=$(echo "${filename}" | cut -d'.' -f3-)
find "${output_dir}" -name "*.${pattern}" ! -name "${filename}" -delete 2>/dev/null || true
```

**2_frame.sh** (Lines 100-102):
```bash
# Delete old versions of this screenshot (keep only latest timestamp)
local pattern=$(echo "${filename}" | cut -d'.' -f3-)
find "${output_dir}" -name "*.${pattern}" ! -name "${filename}" -delete 2>/dev/null || true
```

**3_background.sh** (Lines 190-192):
```bash
# Delete old versions of this screenshot (keep only latest timestamp)
local pattern=$(echo "${output_filename}" | cut -d'.' -f3-)
find "${output_dir}" -name "*.${pattern}" ! -name "${output_filename}" -delete 2>/dev/null || true
```

**4_text.sh** (Lines 290-292):
```bash
# Delete old versions of this screenshot (keep only latest timestamp)
local pattern=$(echo "${output_filename}" | cut -d'.' -f3-)
find "${output_dir}" -name "*.${pattern}" ! -name "${output_filename}" -delete 2>/dev/null || true
```

### Benefits

✅ **No accumulation**: Only latest version exists
✅ **No manual cleanup**: Automatic on every run
✅ **Safe partial runs**: Failed runs don't corrupt existing files
✅ **Version tracking**: Timestamps identify when captured
✅ **Disk space efficient**: No old versions consuming space

### Important: Never Delete Full Folders

⚠️ **NEVER** use `rm -rf output/` or delete entire step folders. This breaks the pipeline and loses all screenshots. The automatic file-by-file replacement handles cleanup correctly.

**Correct approach:**
- Let automatic replacement handle cleanup (default)
- Use `0_cleanup.sh` for manual archival
- Delete individual files if needed (not recommended)

**Incorrect approach:**
- `rm -rf output/1-snap/` ❌ Breaks pipeline
- `rm -rf output/` ❌ Destroys all output
- Deleting folders before completion ❌ Loses partial progress

---

## Configuration Files

### story_metadata.json

**SOURCE OF TRUTH for visual storytelling**

```json
{
  "version": "1.0",
  "story": [
    {
      "position": 1,
      "screenshot_id": "Practice",
      "description": "Practice mode - Red-purple (rainbow start)",
      "style": "mesh",
      "theme": "light",
      "colors": {
        "color_top_left": "#C71585",
        "color_top_right": "#8B5CF6",
        "color_bottom_left": "#F0ABFC",
        "color_bottom_right": "#DDD6FE"
      }
    }
  ]
}
```

**Fields:**
| Field | Required | Values | Description |
|-------|----------|--------|-------------|
| `position` | Yes | 1-10 | Story sequence (determines filename ordering) |
| `screenshot_id` | Yes | String | Must match screenshot_metadata.json entry |
| `description` | No | String | Human-readable note (not used by scripts) |
| `style` | Yes | `gradient` \| `mesh` | Background rendering style |
| `theme` | Yes | `light` \| `dark` | Affects text color in Step 4 |
| `colors` | Yes | Object | Color specifications (format depends on style) |

**Color Specifications:**

**Gradient (2-color linear):**
```json
"colors": {
  "color1": "#0B3D91",
  "color2": "#1976D2"
}
```

**Mesh (4-corner blend):**
```json
"colors": {
  "color_top_left": "#0B3D91",
  "color_top_right": "#1976D2",
  "color_bottom_left": "#2196F3",
  "color_bottom_right": "#64B5F6"
}
```

### screenshot_metadata.json

**Text content for all languages**

```json
{
  "Home": {
    "en-US": {
      "title": "Master CFOP Algorithms",
      "subtitle": "Learn F2L, OLL, and PLL efficiently",
      "title_size": 95,
      "title_color": "#1A1A1A"
    },
    "fr-FR": {
      "title": "Maîtrisez les Algorithmes CFOP",
      "subtitle": "Apprenez F2L, OLL et PLL efficacement"
    }
  }
}
```

### language_mappings.json

**Fallback chain for 39 App Store languages**

```json
{
  "source_languages": ["en-US", "fr-FR", "es-ES", "ja", "zh-Hans"],
  "mappings": {
    "pt-BR": {
      "primary": "es-ES",
      "secondary": "en-US"
    },
    "ko": {
      "primary": "ja",
      "secondary": "en-US"
    }
  }
}
```

**How it works:**
1. Capture screenshots in 1-5 source languages
2. Step 4 reads mappings for all 39 target languages
3. Finds source screenshots using fallback chain (primary → secondary)
4. Applies text overlays using target language metadata
5. Result: 39 complete language sets from ~5 captures!

---

## Pipeline Stages (Detailed)

### Step 1: Capture (1_snap.sh)

**Input:**
- `config/devices.txt` - Device list
- `config/languages.txt` - Source languages
- `config/screenshot_metadata.json` - Metadata path

**Process:**
1. For each device × language:
   - Set simulator language
   - Create config JSON with `metadataPath`
   - Run `xcodebuild test` with UI Tests
   - Extract screenshots from xcresult bundle
2. Saves to `output/1-snap/{language}/{device}/`

**Output:** Raw screenshots (6-field filename format)

**Key Code:**
```bash
# Write config for UI test
cat > /tmp/screenshot_config.json <<EOF
{
  "timestamp": "${SCREENSHOT_TIMESTAMP}",
  "deviceShort": "${device_short}",
  "language": "${language}",
  "orientation": "${orientation}",
  "metadataPath": "${CONFIG_DIR}/screenshot_metadata.json"
}
EOF

# Run UI test
xcodebuild test \
  -project ../Deddal.xcodeproj \
  -scheme "Screenshots Scheme" \
  -destination "platform=iOS Simulator,name=${device}"
```

---

### Step 2: Frame (2_frame.sh)

**Input:** Raw screenshots from Step 1

**Process:**
1. Load device configuration (corner radius, screen dimensions)
2. For each screenshot:
   - Detect landscape orientation
   - Resize to fit device screen area
   - Apply rounded corners
   - Composite onto bezel overlay
3. Saves to `output/2-frame/`

**Output:** Bezeled screenshots (6-field filename format)

**Modular Design:** Uses `lib/bezel_module.sh` for reusable logic

---

### Step 3: Background (3_background.sh)

**⭐ TRANSFORMATION POINT - Story Filtering Happens Here**

**Input:**
- Bezeled screenshots from Step 2
- `config/story_metadata.json` (SOURCE OF TRUTH)

**Process:**
1. Read story_metadata.json for canonical 10-screenshot sequence
2. **Loop through positions 1-10 (not files!)**
3. For each position:
   - Get story config (screenshot_id, style, theme, colors)
   - Find matching screenshot from Step 2 output
   - **Add POSITION to filename** (01-10)
   - Apply story-specific colors (gradient or mesh)
4. Saves to `output/3-background/`

**Output:** Story screenshots with backgrounds (7-field filename format)

**Key Implementation:**

```bash
# Loop through story positions (1-10)
for position in {1..10}; do
    # Get story config for this position
    local story_config=$(get_story_background_config "${position}")

    # Parse: screenshot_id|style|theme|colors
    local screenshot_id=$(echo "${story_config}" | cut -d'|' -f1)
    local style=$(echo "${story_config}" | cut -d'|' -f2)
    local theme=$(echo "${story_config}" | cut -d'|' -f3)

    # Find matching screenshots from step 2 output
    local input_screenshot=$(find "${device_dir}" -name "*${screenshot_id}.${language}.png")

    # Add position to filename
    local position_padded=$(printf "%02d" ${position})
    local output_filename="${timestamp}.${device}.${orientation}.${position_padded}.${screenshot_id}.${language}.png"

    # Apply story-specific colors
    if [ "${style}" = "gradient" ]; then
        add_background ... "${c1}" "${c2}" ...
    else  # mesh
        add_mesh_background ... "${ctl}" "${ctr}" "${cbl}" "${cbr}" ...
    fi
done
```

**Python Helper:**
```python
def get_story_background_config(position):
    with open('story_metadata.json') as f:
        config = json.load(f)
    for item in config['story']:
        if item['position'] == position:
            return f"{screenshot_id}|{style}|{theme}|{colors}"
```

---

### Step 4: Text (4_text.sh)

**Multi-Language Generation**

**Input:**
- Story screenshots from Step 3
- `config/screenshot_metadata.json` (text content)
- `config/language_mappings.json` (fallback mappings)

**Process:**
1. Read language_mappings.json for all 39 target languages
2. For each target language:
   - **Find source screenshots using fallback chain** (primary → secondary)
   - Load text from screenshot_metadata.json
   - Select language-specific font
   - Render title + subtitle with wrapping
   - Composite text onto canvas
3. Saves to `output/4-text/`

**Output:** 39 complete language sets (8-field filename format)

**Font Support:**
- Latin: Ubuntu
- Japanese: Hiragino Sans GB
- Chinese: PingFang SC/TC
- Arabic: Geeza Pro
- Korean: Apple SD Gothic Neo
- Thai: Thonburi
- (See `assets/fonts/README.md` for complete list)

**Key Code:**
```bash
# Get source language using fallback
get_source_language() {
    local target_lang="$1"
    python3 -c "
import json
with open('${LANGUAGE_MAPPINGS_FILE}') as f:
    config = json.load(f)
mapping = config['mappings']['${target_lang}']
# Try primary, then secondary
if os.path.isdir('${INPUT_DIR}/' + mapping['primary']):
    print(mapping['primary'])
elif mapping['secondary']:
    print(mapping['secondary'])
"
}
```

---

### Step 5: Upload (5_upload.sh)

**Input:**
- Final screenshots from Step 4
- `config/story_metadata.json` (screenshot selection)

**Process:**
1. Read story_metadata.json to get screenshot IDs
2. Copy screenshots to Fastlane directory structure
3. Run `fastlane deliver` in screenshot-only mode

**Output:** Uploaded to App Store Connect

**Key Code:**
```bash
# Get screenshot IDs from story
selected_screenshots=$(python3 -c "
import json
with open('${story_config}') as f:
    data = json.load(f)
    ids = [item['screenshot_id'] for item in data['story']]
    print(' '.join(ids))
")

# Copy only story screenshots
for screenshot_id in ${selected_screenshots}; do
    for png_file in "${device_dir}"/*"${screenshot_id}"*.png; do
        cp -f "${png_file}" "${fastlane_dir}/"
    done
done
```

---

## Per-Screenshot Theming

### Dynamic Theme Switching

Each screenshot can specify `"theme": "light"` or `"theme": "dark"` independently.

**Benefits:**
- ✅ Single test run captures all screenshots
- ✅ App restarts with different theme as needed
- ✅ Supports mixed themes (e.g., screenshots 1-9 light, 10 dark)
- ✅ No need to run entire pipeline twice

### Theme System Architecture

```
story_metadata.json
  ↓ (theme: "light" or "dark")
1_snap.sh
  ↓ (passes metadataPath)
ScreenshotUITests.swift
  ├─ loadMetadata()
  ├─ getTheme(for: screenshotId)
  ├─ ensureTheme(required)
  └─ restartAppWithTheme(theme)
      ↓ (sets -ScreenshotTheme launch arg)
Deddal App
  └─ Reads ProcessInfo, applies theme
```

### UI Test Methods

**loadMetadata()** - Reads screenshot_metadata.json:
```swift
private func loadMetadata() -> [String: [String: Any]]? {
    let configPath = "/tmp/screenshot_config.json"
    guard let config = loadJSON(configPath),
          let metadataPath = config["metadataPath"] as? String else {
        return nil
    }
    return loadJSON(metadataPath)
}
```

**restartAppWithTheme()** - Restarts app with theme:
```swift
@MainActor
private func restartAppWithTheme(_ theme: String) {
    app.terminate()
    app.launchArguments = [
        "-UITesting",
        "-ScreenshotTheme", theme  // ⭐ Key line
    ]
    app.launch()
    usleep(1_000_000)  // 1 second stabilize
}
```

**ensureTheme()** - Checks and switches if needed:
```swift
private func ensureTheme(_ required: String) {
    if currentTheme != required {
        restartAppWithTheme(required)
        currentTheme = required
    }
}
```

---

## Error Handling

### _ERROR Suffix Fallback

The pipeline supports graceful handling of failed screenshots using `_ERROR` suffix.

#### How Step 1 Generates ERROR Screenshots

When XCTest navigation fails:
- ScreenshotUITests.swift calls `snapshot(ScreenshotName.libraryF2L.error)`
- ScreenshotConstants.swift `.error` property appends "_ERROR"
- Example: `Library_F2L` → `Library_F2L_ERROR`

#### Step 3 Fallback Mechanism

```bash
# Try regular screenshot first
local input_screenshot=$(find "${device_dir}" -name "*${screenshot_id}.${language}.png")
local screenshot_suffix=""

if [ ! -f "${input_screenshot}" ]; then
    # Try _ERROR fallback
    input_screenshot=$(find "${device_dir}" -name "*${screenshot_id}_ERROR.${language}.png")
    if [ -f "${input_screenshot}" ]; then
        screenshot_suffix="_ERROR"
        log_warning "Using ERROR fallback: ${screenshot_id}"
    fi
fi

# Preserve _ERROR in output filename
output_filename="${timestamp}.${device}.${orientation}.${position}.${screenshot_id}${screenshot_suffix}.${language}.png"
```

#### Pipeline Propagation

The `_ERROR` suffix automatically propagates:
- **Step 3 → 4**: Filename parsing preserves `_ERROR` in screenshot_id field
- **Step 4 → 5**: Wildcard matching includes `_ERROR` screenshots
- **Statistics**: Step 3 tracks and reports ERROR fallback count

**Benefits:**
1. Pipeline completes despite partial failures
2. Error visibility through `_ERROR` suffix
3. Failed screenshots still captured for review
4. No data loss
5. Clean implementation (~20 lines in Step 3)

---

## Testing Strategy

### Unit Testing (per component)

**Test metadata loading:**
```bash
echo '{"01_Test": {"theme": "dark"}}' > /tmp/test_metadata.json
# Run testMinimalScreenshot, verify theme applied
```

**Test theme application:**
```bash
xcodebuild test -only-testing:...:testMinimalScreenshot
# Check logs for "✅ Restarted app with theme: dark"
```

**Test scrolling:**
```bash
# Look for logs: "✓ Found and tapped 'library_caseSet_OLL' after 2 scrolls"
```

### Integration Testing

**Single screenshot test:**
```bash
# Modify metadata to only include Home
# Verify 1 screenshot per device
```

**Theme switching test:**
```bash
# Metadata: 01 = light, 02 = dark, 03 = light
# Verify 3 app restarts in logs
```

**Multi-device test:**
```bash
# 2 devices, 1 language, 10 screenshots
# Expected: 20 screenshots total
```

### End-to-End Testing

```bash
cd tools/shared/screenshots
# No cleanup needed - automatic file replacement handles old versions
./generate.sh

# Verify:
# - Story screenshots exist with positions 01-10
# - Themes applied correctly
# - Text overlays for 39 languages
# - Natural ordering
```

---

## Automation Conventions

To keep screenshots stable as the app evolves, every change touching the pipeline must follow these rules:

1. **Accessibility Identifier Source of Truth**
   - Declare identifiers exclusively in `Deddal/App/AccessibilityID.swift` using the dotted `Namespace.Component.Detail` format.
   - Use the provided helpers (`AccessibilityID.Library.caseSetCell(id:)`, etc.) so SwiftUI views expose stable IDs regardless of localization.
   - Pass canonical codes/slugs (e.g., `CaseSet.code`) for dynamic items instead of localized display names.

2. **UITest Selectors**
   - Mirror identifiers in `DeddalScreenshotsUITests/ScreenshotConstants.swift` and update both files in the same PR when naming changes.
   - UITests may only query through these constants; never rely on button labels or hierarchy order.

3. **Step 1 Configuration Profiles**
   - All device/language combinations live in `tools/shared/screenshots/config/1-snap.json` under `configurations`.
   - Wrapper scripts (`1a`, `1b`, etc.) simply export `CONFIG=<profile>` and call `1_snap.sh`. Do not duplicate the `xcodebuild` invocation or hardcode simulator names.
   - When adding or removing a profile, keep the wrapper list in sync so `CONFIG` always points to a valid entry.

4. **Error Screenshots**
   - `_ERROR` files are diagnostic only. Fix the failing selector/identifier before passing assets downstream—Steps 3-5 should not rely on `_ERROR` outputs for production uploads.

Document these conventions in PR descriptions any time you touch identifiers, Step 1 profiles, or wrapper scripts so the next contributor can trace the intent quickly.

---

## Future Enhancements

### Potential Features

1. **Multiple Stories**: Different stories per market/device
2. **Position Ranges**: Define sub-sequences ("tutorial" = positions 1-3)
3. **Story Templates**: Pre-defined color progressions (rainbow, sunset, etc.)
4. **Dynamic Colors**: Generate progressions from base color + algorithm
5. **Animation**: Export story as video for promotional materials
6. **Screenshot Comparison**: Detect visual regressions using ImageMagick
7. **A/B Testing**: Generate multiple story variations

### Architecture Extensions

1. **Story Validation**: Pre-flight checks for story_metadata.json
2. **Story Preview**: Generate thumbnail grid showing color progression
3. **Story Editor**: GUI tool for building/editing stories
4. **Incremental Captures**: Skip already captured screenshots
5. **Parallel Device Testing**: Multiple simulators in parallel

---

## Performance Considerations

### Bottlenecks

1. **App Restart Overhead**: ~1-2s per restart
   - Optimization: Group screenshots by theme
2. **Simulator Performance**: Slow on older Macs
   - Mitigation: Use `-parallel-testing-enabled NO`
3. **xcodebuild Startup**: ~2min first build, ~10s cached

### Optimization Strategies

1. **Minimize Restarts**: Group light screenshots together, then dark
2. **Parallel Devices**: Future - run multiple simulators
3. **Incremental Captures**: Check for existing files, skip if timestamp matches

---

## Architecture Decision Records

### ADR-001: Use JSON for metadata instead of plist
- **Decision**: JSON
- **Rationale**: Human-readable, easy to edit, standard format, better git diffs

### ADR-002: Pass metadata path instead of parsing in bash
- **Decision**: Pass path to UI test
- **Rationale**: Swift has better JSON parsing, single source of truth

### ADR-003: App restart for theme instead of in-app toggle
- **Decision**: Restart with launch argument
- **Rationale**: Clean state, matches real UX, avoids animation artifacts

### ADR-004: Use XCUIElement scrolling instead of accessibility
- **Decision**: `swipeUp()` on table
- **Rationale**: More reliable, matches user interaction

### ADR-005: Story filtering at Step 3 instead of Step 1
- **Decision**: Late filtering at background stage
- **Rationale**: Flexibility to change story without re-capturing

---

## File References

**Modified for Story Architecture:**
- `config/story_metadata.json` (created)
- `scripts/3_background.sh` (major refactor)
- `scripts/4_text.sh` (filename parsing updated)
- `scripts/5_upload.sh` (uses story_metadata.json)

**Unchanged:**
- `scripts/1_snap.sh` (passes metadataPath)
- `scripts/2_frame.sh` (no story awareness)

---

## See Also

- **[README.md](README.md)** - User documentation and quick start guide
- **[CLAUDE.md](CLAUDE.md)** - AI assistant instructions and critical rules
- **[assets/fonts/README.md](assets/fonts/README.md)** - Font management and licensing
- **[AI_LOGS.md](AI_LOGS.md)** - Historical implementation log

---

Generated by Trophee Ltd
