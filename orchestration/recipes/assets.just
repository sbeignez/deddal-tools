# Asset Management Recipes
# Prefix: assets-*

# Download all case images from VisualCube API
assets-download-all:
    @just _info "📥 Downloading all case images..."
    @just assets-download-f2l
    @just assets-download-oll
    @just assets-download-pll
    @just assets-download-pcll
    @just assets-download-lbl
    @just assets-download-2x2-ortega
    @just assets-download-2x2-cll
    @just _success "All assets downloaded"

# Download F2L case images
assets-download-f2l:
    @just _exec {{ASSETS_DIR}}/download/3x3_cfop_f2l.sh

# Download OLL case images
assets-download-oll:
    @just _exec {{ASSETS_DIR}}/download/3x3_cfop_oll.sh

# Download PLL case images
assets-download-pll:
    @just _exec {{ASSETS_DIR}}/download/3x3_cfop_pll.sh

# Download PCLL case images
assets-download-pcll:
    @just _exec {{ASSETS_DIR}}/download/3x3_cfop_pcll.sh

# Download LBL case images
assets-download-lbl:
    @just _exec {{ASSETS_DIR}}/download/3x3_lbl.sh

# Download 2x2 Ortega case images
assets-download-2x2-ortega:
    @just _exec {{ASSETS_DIR}}/download/2x2_ortega_oll.sh
    @just _exec {{ASSETS_DIR}}/download/2x2_ortega_pbl.sh

# Download 2x2 CLL case images
assets-download-2x2-cll:
    @just _exec {{ASSETS_DIR}}/download/2x2_cll.sh

# Upload all assets to Supabase storage
assets-upload-all:
    @just _warn "Uploading assets to Supabase"
    @just _confirm "Upload all assets to Supabase?"
    @just _python-exec {{ASSETS_DIR}} "upload/upload_case_images.py"
    @just _success "Assets uploaded"

# Upload assets using Bash script
assets-upload-bash:
    @just _exec {{ASSETS_DIR}}/upload/upload_case_images.sh

# Rename all asset files (imagesets, SVGs)
assets-rename-all:
    @just _info "✏️  Renaming asset files..."
    @just _exec {{ASSETS_DIR}}/rename/rename_assets.sh
    @just _success "Assets renamed"

# Rename .imageset folders
assets-rename-imagesets:
    @just _exec {{ASSETS_DIR}}/rename/rename_imagesets.sh

# Rename SVG files within imagesets
assets-rename-svgs:
    @just _exec {{ASSETS_DIR}}/rename/rename_imageset_svgs.sh

# Generate rename mapping CSV
assets-rename-mapping:
    @just _exec {{ASSETS_DIR}}/rename/generate_rename_mapping.sh

# Export case images
assets-export:
    @just _exec {{ASSETS_DIR}}/export/export-case-images.sh

# Populate null image names in database
assets-populate-nulls:
    @just _info "🔧 Populating null image names..."
    @just _exec {{ASSETS_DIR}}/populate/populate_null_image_names.sh
    @just _success "Null image names populated"

# Populate null images using Python
assets-populate-nulls-py:
    @just _python-exec {{ASSETS_DIR}} "populate/populate_null_images.py"
