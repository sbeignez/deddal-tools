# tool-assets - Asset Management

Scripts for managing Rubik's Cube case visualization assets (SVG images from VisualCube API).

> **✨ Recommended Usage:** Use the Justfile orchestration system instead of calling scripts directly:
> ```bash
> just assets-download-all    # Download all case images
> just assets-upload-all      # Upload to Supabase
> just assets-rename-all      # Organize assets
> just workflow-asset-refresh # Complete asset pipeline
> ```
>
> See [../tool-all/README.md](../tool-all/README.md) for complete documentation.

## Overview

This folder contains 18 scripts organized into 5 categories for the complete lifecycle of case image assets:
1. Downloading from VisualCube API
2. Uploading to Supabase storage
3. Renaming and organizing files
4. Exporting assets
5. Populating missing data

## Folder Structure

```
tool-assets/
├── download/     # Download case images from VisualCube API (8 scripts)
├── upload/       # Upload images to Supabase storage (2 scripts)
├── rename/       # Rename and organize asset files (5 scripts)
├── export/       # Export assets (1 script)
└── populate/     # Populate missing data (2 scripts)
```

## Download Scripts (8 files)

Download case visualization images from VisualCube API for different cube methods:

### 3x3 CFOP Method
- `3x3_cfop_f2l.sh` - Download F2L (First Two Layers) case images
- `3x3_cfop_oll.sh` - Download OLL (Orientation of Last Layer) case images
- `3x3_cfop_pll.sh` - Download PLL (Permutation of Last Layer) case images
- `3x3_cfop_pcll.sh` - Download PCLL case images

### Other Methods
- `3x3_lbl.sh` - Download Layer-by-Layer method images
- `2x2_ortega_oll.sh` - Download 2x2 Ortega OLL case images
- `2x2_ortega_pbl.sh` - Download 2x2 Ortega PBL case images
- `2x2_cll.sh` - Download 2x2 CLL case images

**Usage:**
```bash
cd tool-assets/download
./3x3_cfop_f2l.sh   # Downloads F2L case images
```

## Upload Scripts (2 files)

Upload case images to Supabase cloud storage:

- `upload_case_images.sh` - Bash implementation for uploading images
- `upload_case_images.py` - Python implementation for uploading images

**Usage:**
```bash
cd tool-assets/upload
./upload_case_images.sh     # Bash version
# or
python3 upload_case_images.py  # Python version
```

**Requirements:**
- Supabase credentials configured
- Images must exist locally before upload

## Rename Scripts (5 files)

Rename and organize asset files to match naming conventions:

- `rename_assets.sh` - Master script for renaming assets
- `rename_imagesets.sh` - Rename .imageset folders (Xcode asset catalogs)
- `rename_imageset_svgs.sh` - Rename SVG files within imagesets
- `rename_svg_files.sh` - Rename individual SVG files
- `generate_rename_mapping.sh` - Generate CSV mapping of old→new names

**Usage:**
```bash
cd tool-assets/rename
./generate_rename_mapping.sh  # First, generate mapping
./rename_assets.sh             # Then, execute rename
```

**Workflow:**
1. Generate mapping CSV showing old→new filenames
2. Review mapping for correctness
3. Execute rename script to apply changes
4. Verify renames completed successfully

## Export Scripts (1 file)

Export case images for external use:

- `export-case-images.sh` - Export case images to specified format/location

**Usage:**
```bash
cd tool-assets/export
./export-case-images.sh
```

## Populate Scripts (2 files)

Populate missing or null image data:

- `populate_null_image_names.sh` - Bash script to populate null image names
- `populate_null_images.py` - Python script to populate null images

**Usage:**
```bash
cd tool-assets/populate
./populate_null_image_names.sh  # Bash version
# or
python3 populate_null_images.py # Python version
```

**When to use:**
- After downloading new case images
- When image metadata is incomplete
- When image names need to be generated from case codes

## Common Workflows

### Adding New Case Images

1. **Download** images from VisualCube API:
   ```bash
   cd download
   ./3x3_cfop_f2l.sh  # Or relevant method script
   ```

2. **Populate** missing data if needed:
   ```bash
   cd ../populate
   python3 populate_null_images.py
   ```

3. **Rename** to match conventions:
   ```bash
   cd ../rename
   ./generate_rename_mapping.sh
   ./rename_assets.sh
   ```

4. **Upload** to Supabase:
   ```bash
   cd ../upload
   ./upload_case_images.sh
   ```

### Updating Existing Assets

1. Generate rename mapping to see what needs updating
2. Execute rename scripts
3. Re-upload changed images to Supabase

## Dependencies

**Bash scripts require:**
- curl (for VisualCube API downloads)
- jq (for JSON processing)
- Standard Unix tools (sed, awk, grep)

**Python scripts require:**
- Python 3.8+
- Supabase Python SDK (for upload scripts)
- Requests library (for API calls)

Install Python dependencies:
```bash
pip3 install supabase requests
```

## Related Documentation

- Main project: `/CLAUDE.md`
- Supabase setup: `/documentation/01-architecture/`
- Asset naming conventions: Check rename scripts for patterns

## Troubleshooting

**Download failures:**
- Check internet connection
- Verify VisualCube API is accessible
- Review case code formatting in scripts

**Upload failures:**
- Verify Supabase credentials in environment
- Check Supabase storage bucket exists
- Ensure images exist locally before upload

**Rename issues:**
- Always generate mapping first and review
- Back up assets before running rename scripts
- Check for file naming conflicts

Generated by Trophee Ltd
