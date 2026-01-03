# Screenshot Automation System

A self-contained, Fastlane-free screenshot automation system for iOS App Store submissions with visual storytelling capabilities.

## Why This System?

**Problems with Fastlane snapshot:**
- Ruby dependency hell
- Slow execution (10+ minutes)
- Complex debugging
- Over-engineered for simple tasks

**This Solution:**
- ✅ Fast native xcodebuild (no Ruby overhead)
- ✅ Simple bash scripts (easy to debug)
- ✅ ImageMagick for framing (free, powerful)
- ✅ Story-driven visual progression (rainbow gradients)
- ✅ Multi-language generation (39 languages from 5 captures)
- ✅ Keeps Fastlane only for App Store upload
- ✅ Self-contained in one folder

---

> **✨ Recommended Usage:** Use the Justfile orchestration system for easier screenshot generation:
> ```bash
> just screenshots-generate-all    # Full 5-step pipeline
> just screenshots-snap            # Step 1: Capture
> just screenshots-frame           # Step 2: Add frames
> just screenshots-background      # Step 3: Backgrounds
> just screenshots-text            # Step 4: Text overlays
> just screenshots-upload          # Step 5: Upload to App Store
> just screenshots-generate-local  # Steps 1-4 only (no upload)
> ```
>
> See [../tool-all/README.md](../tool-all/README.md) for complete documentation.

---

## Quick Start

### Prerequisites

1. **ImageMagick** (for framing):
   ```bash
   brew install imagemagick
   ```

2. **Xcode and iOS Simulator** (already installed)

3. **Fastlane** (only for upload, already configured):
   ```bash
   cd ..
   bundle install
   ```

### Generate All Screenshots

```bash
cd tool-screenshots
./generate.sh
```

This will:
1. ✅ Capture screenshots for all configured devices/languages
2. ✅ Add device bezels and story-driven backgrounds
3. ✅ Generate text overlays for all 39 App Store languages
4. ✅ Ask if you want to upload to App Store

### Run Individual Steps

```bash
# Capture only
./generate.sh --capture-only

# Frame existing screenshots (Steps 2-4)
./generate.sh --frame-only

# Upload existing screenshots
./generate.sh --upload-only

# Debug mode
DEBUG=1 ./generate.sh
```

### Output

- `output/1-snap/` - Raw screenshots from UI tests
- `output/2-frame/` - Screenshots with device bezels
- `output/3-background/` - With story-driven gradient backgrounds
- `output/4-text/` - Final App Store ready (39 languages)

### Automatic File Management

**No cleanup needed!** The system automatically maintains one version of each screenshot:

- **File-by-file replacement**: Before saving each new screenshot, the script deletes old versions with different timestamps
- **Safety first**: One file at a time - if the script crashes, unprocessed files keep their old versions
- **Timestamp preservation**: Each run gets a unique timestamp (YYYYMMDD.HHMM) for identification
- **Always current**: Output folders contain only the latest version of each screenshot

**Example:**
```bash
# Run 1 at 13:38 creates: 20251105.1338.iPhone17PM.V.01.Home.en-US.png
# Run 2 at 14:42 deletes old, creates: 20251105.1442.iPhone17PM.V.01.Home.en-US.png
# Result: Only one file remains (latest timestamp)
```

**Manual Cleanup (Optional):**

If you want to archive or clean output folders manually:
```bash
# Archive raw screenshots, delete all
./scripts/0_cleanup.sh --archive

# Keep raw screenshots, delete processed outputs
./scripts/0_cleanup.sh --keep-snap
```

⚠️ **Important**: Never delete entire output folders (`rm -rf output/`) as this breaks the pipeline. Use the cleanup script or let automatic replacement handle it.

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                          generate.sh                              │
│                   (Main orchestration script)                     │
└──────────────────────────────────────────────────────────────────┘
                                 │
        ┌────────────┬───────────┼────────────┬────────────┐
        │            │           │            │            │
        ▼            ▼           ▼            ▼            ▼
   ┌────────┐   ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
   │ Step 1 │   │ Step 2 │  │ Step 3 │  │ Step 4 │  │ Step 5 │
   │ Snap   │──▶│ Frame  │─▶│ Backgr │─▶│  Text  │─▶│ Upload │
   │        │   │        │  │        │  │        │  │        │
   └────────┘   └────────┘  └────────┘  └────────┘  └────────┘
   xcodebuild   ImageMagick ImageMagick ImageMagick Fastlane
   UI Tests     Device PNG  Story Colors Text Render  deliver
```

### Pipeline Stages

1. **Step 1 (1_snap.sh)**: Capture screenshots via xcodebuild + UI Tests
2. **Step 2 (2_frame.sh)**: Add device bezels (iPhone/iPad frames)
3. **Step 3 (3_background.sh)**: Add story-driven gradient backgrounds
4. **Step 4 (4_text.sh)**: Generate text overlays for 39 languages
5. **Step 5 (5_upload.sh)**: Upload to App Store Connect via Fastlane

**For detailed architecture:** See [ARCHITECTURE.md](ARCHITECTURE.md)

---

## Folder Structure

```
tool-screenshots/
├── README.md                          # This file
├── ARCHITECTURE.md                    # Technical deep dive
├── generate.sh                        # Main entry point
├── config/
│   ├── story_metadata.json            # Story sequence + visual styling
│   ├── screenshot_metadata.json       # Text content per language
│   ├── language_mappings.json         # 39-language fallback mappings
│   ├── devices.txt                    # Device list
│   └── languages.txt                  # Source language codes
├── scripts/
│   ├── 1_snap.sh                      # Screenshot capture
│   ├── 2_frame.sh                     # Device bezel overlay
│   ├── 3_background.sh                # Story backgrounds
│   ├── 4_text.sh                      # Text overlays
│   ├── 5_upload.sh                    # App Store upload
│   └── lib/                           # Modular libraries
│       ├── bezel_module.sh
│       ├── background_module.sh
│       ├── text_module.sh
│       └── imagemagick_utils.sh
├── assets/
│   ├── frames/                        # Device frame templates
│   └── fonts/                         # Multi-language fonts
│       └── README.md                  # Font inventory
└── output/
    ├── 1-snap/                        # Raw screenshots
    ├── 2-frame/                       # With bezels
    ├── 3-background/                  # With backgrounds
    └── 4-text/                        # Final (39 languages)
```

---

## Configuration

### Story-Driven Screenshots

**story_metadata.json** - SOURCE OF TRUTH for visual storytelling:

```json
{
  "story": [
    {
      "position": 1,
      "screenshot_id": "Practice",
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

**Key Features:**
- Defines canonical sequence of 10 App Store screenshots
- Per-screenshot positioning (01-10)
- Per-screenshot backgrounds (gradient or mesh)
- Per-screenshot themes (light/dark)
- Creates visual progressions (e.g., rainbow colors)

### Text Content

**screenshot_metadata.json** - Titles and descriptions per language:

```json
{
  "Home": {
    "en-US": {
      "title": "Master CFOP Algorithms",
      "subtitle": "Learn F2L, OLL, and PLL efficiently"
    },
    "fr-FR": {
      "title": "Maîtrisez les Algorithmes CFOP",
      "subtitle": "Apprenez F2L, OLL et PLL efficacement"
    }
  }
}
```

### Multi-Language Generation

**language_mappings.json** - Fallback chain for 39 App Store languages:

```json
{
  "source_languages": ["en-US", "fr-FR", "es-ES", "ja", "zh-Hans"],
  "mappings": {
    "pt-BR": {
      "primary": "es-ES",
      "secondary": "en-US"
    },
    "de-DE": {
      "primary": "en-US",
      "secondary": null
    }
  }
}
```

**How it works:**
1. Capture screenshots in 1-5 source languages
2. Step 4 generates all 39 App Store languages using fallback mappings
3. Example: Portuguese (pt-BR) uses Spanish screenshots + Portuguese text
4. Result: 39 complete language sets from ~5 captures!

### Device & Language Lists

**devices.txt** - iOS simulator names (one per line):
```
iPhone 15 Pro Max
iPad Pro 13-inch (M4)
```

**languages.txt** - Source language codes (one per line):
```
en-US
fr-FR
es-ES
ja
zh-Hans
```

---

## How It Works

### Step 1: Capture Screenshots (1_snap.sh)

1. Reads devices from `config/devices.txt`
2. Reads source languages from `config/languages.txt`
3. For each device × language combination:
   - Sets simulator language
   - Runs `xcodebuild test` with UI Tests
   - Extracts screenshots from xcresult bundle
4. Saves raw screenshots to `output/1-snap/{language}/{device}/`

**Example:**
```bash
xcodebuild test \
  -project ../Deddal.xcodeproj \
  -scheme "Screenshots Scheme" \
  -destination 'platform=iOS Simulator,name=iPhone 15 Pro Max' \
  -resultBundlePath ./results.xcresult
```

### Step 2: Add Device Bezels (2_frame.sh)

1. Loads device frame templates from `assets/frames/`
2. For each raw screenshot:
   - Detects landscape orientation
   - Resizes screenshot to fit device screen area
   - Applies rounded corners matching device
   - Composites onto bezel overlay
3. Saves bezeled screenshots to `output/2-frame/`

**Modular Design:** Uses `lib/bezel_module.sh` for reusable compositing logic.

### Step 3: Add Story Backgrounds (3_background.sh)

**Story-Driven Processing:**

1. Reads `story_metadata.json` for canonical 10-screenshot sequence
2. Loops through positions 1-10 (not files!)
3. For each position:
   - Finds matching screenshot from Step 2 output
   - Applies story-specific colors (gradient or mesh)
   - Adds position to filename (01-10)
4. Saves to `output/3-background/`

**Features:**
- Gradient style (2-color linear)
- Mesh style (4-corner blend)
- Per-screenshot themes
- Error fallback (`_ERROR` suffix support)
- Natural ordering for App Store

### Step 4: Add Text Overlays (4_text.sh)

**Multi-Language Generation:**

1. Reads `language_mappings.json` for all 39 target languages
2. For each target language:
   - Finds source screenshots using fallback chain
   - Loads text from `screenshot_metadata.json`
   - Renders title + subtitle with language-specific fonts
3. Generates 39 complete language sets

**Font Support:**
- Latin: Ubuntu
- Japanese: Hiragino
- Chinese: PingFang
- Arabic: Geeza Pro
- (See `assets/fonts/README.md` for complete list)

### Step 5: Upload to App Store (5_upload.sh)

1. Copies screenshots to Fastlane directory structure
2. Runs `fastlane deliver` in screenshot-only mode
3. Uploads to App Store Connect

**Example:**
```bash
fastlane deliver \
  --skip_metadata \
  --skip_binary_upload \
  --overwrite_screenshots
```

---

## Customization

### Change Story Colors

Edit `config/story_metadata.json`:

```json
{
  "story": [
    {
      "position": 1,
      "screenshot_id": "Home",
      "style": "gradient",
      "theme": "light",
      "colors": {
        "color1": "#0B3D91",
        "color2": "#1976D2"
      }
    }
  ]
}
```

### Add Custom Device Frames

1. Create PNG with transparent background showing device bezel
2. Save to `assets/frames/{device_name}.png`
3. Update `scripts/lib/frame_templates.sh` with dimensions

### Customize Processing Steps

**Modular library functions allow editing individual steps:**

- Edit `lib/bezel_module.sh` - Modify corner radius, scaling, shadows
- Edit `lib/background_module.sh` - Change gradient angles, patterns
- Edit `lib/text_module.sh` - Adjust wrapping, spacing, effects

**Run custom pipeline:**
```bash
# Run only Steps 2-3 (skip text)
./scripts/2_frame.sh
./scripts/3_background.sh
cp -r output/3-background/* output/4-text/
```

### Advanced ImageMagick

```bash
# Create custom gradient
convert screenshot.png \
  -background gradient:blue-purple \
  -flatten output.png

# Combine multiple screenshots
convert screenshot1.png screenshot2.png \
  +append output.png

# Add custom rounded corners
convert screenshot.png \
  -alpha set -virtual-pixel transparent \
  -channel A -blur 0x8 -level 50,100% +channel \
  output.png
```

---

## Troubleshooting

### Quick Diagnostics

```bash
# Check dependencies
brew list imagemagick && echo "✅ ImageMagick" || echo "❌ Missing"
xcodebuild -version
xcrun simctl list devices | grep Booted

# Test minimal capture
DEBUG=1 ./generate.sh --capture-only 2>&1 | tee /tmp/diag.log

# Check results
find output/1-snap -name "*.png" | wc -l
```

### Common Issues

#### "No screenshots extracted"

**Causes:**
- UI test didn't run
- Screenshots not saved as attachments
- Wrong test method name

**Solutions:**
```bash
# Check if test started
grep "Testing started" /tmp/screenshot_xcodebuild_error.log

# Verify scheme exists
open Deddal.xcodeproj

# Check test method
grep "func testMinimalScreenshot" DeddalScreenshotsUITests/ScreenshotUITests.swift
```

#### "ImageMagick not installed"

```bash
brew install imagemagick
convert --version  # Should show ImageMagick 7.x.x
```

#### "OLL/PLL Navigation Fails"

**Cause:** OLL/PLL cells below the fold

**Solution:** Increase scroll attempts in UI test:
```swift
scrollToAndTapCell(identifier: "library_caseSet_OLL", maxScrolls: 10)
```

#### Theme Not Applied

**Diagnosis:**
```bash
# Check metadata
cat config/story_metadata.json | jq '.story[] | select(.screenshot_id=="Settings_Dark") | .theme'

# Check app launch args
grep "ScreenshotTheme" /tmp/screenshot_xcodebuild_error.log
```

#### Test Timeout

**Solutions:**
- Reduce wait times in UI test (500ms instead of 1s)
- Group screenshots by theme to minimize app restarts
- Remove unnecessary waits after navigation

### Debug Mode

```bash
# Enable verbose output
DEBUG=1 ./generate.sh

# Run individual steps
./scripts/1_snap.sh
./scripts/2_frame.sh
./scripts/3_background.sh
./scripts/4_text.sh

# Monitor simulator logs
xcrun simctl spawn booted log stream --predicate 'processImagePath contains "Deddal"'

# Inspect xcresult
xcrun xcresulttool get attachments --path /tmp/test_results.xcresult
```

### Reset Environment

```bash
# Clean everything and start fresh
xcrun simctl shutdown all
xcrun simctl erase "iPhone 15 Pro Max"
rm -rf ~/Library/Developer/Xcode/DerivedData
cd tool-screenshots && rm -rf output/*
./generate.sh --capture-only
```

---

## CI/CD Integration

### GitHub Actions

```yaml
- name: Generate Screenshots
  run: |
    cd tool-screenshots
    brew install imagemagick
    ./generate.sh --capture-only
```

### GitLab CI

```yaml
screenshots:
  script:
    - cd tool-screenshots
    - ./generate.sh
  artifacts:
    paths:
      - tool-screenshots/output/4-text/
```

---

## Benefits Over Fastlane Snapshot

| Feature | Fastlane | This System |
|---------|----------|-------------|
| Speed | 10+ min | 2-3 min |
| Dependencies | Ruby + gems | Native tools |
| Debugging | Complex | Simple bash |
| Customization | Limited | Unlimited |
| Visual Storytelling | No | Yes (rainbow gradients) |
| Multi-Language | Manual | Automatic (39 from 5) |
| CI Cost | High | Low |
| Maintenance | Hard | Easy |

### Modular Architecture Benefits

**Separation of Concerns:**
- Each step (bezel, background, text) is independent
- Modify one step without affecting others
- Easier debugging and testing

**Incremental Processing:**
- Re-run only the steps that changed
- Update text without regenerating screenshots
- Change story colors without re-capturing

**Transparent Pipeline:**
- Inspect output at each step
- Catch errors early
- Understand exactly what each step does

---

## Requirements

- macOS with Xcode
- iOS Simulator
- ImageMagick 7: `brew install imagemagick`
- Fastlane (for upload only): `bundle install`

---

## See Also

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Technical deep dive into story-driven architecture
- **[CLAUDE.md](CLAUDE.md)** - AI assistant instructions and critical rules
- **[assets/fonts/README.md](assets/fonts/README.md)** - Font management and licensing
- **[AI_LOGS.md](AI_LOGS.md)** - Historical implementation log

---

## Credits

Created to solve Fastlane Ruby dependency issues while maintaining automation quality.

Generated by Trophee Ltd
