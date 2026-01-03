#!/bin/bash

# Generate White Cross SVG assets using VisualCube API
# Based on scrambles from 3x3_cross_cases.json

set -e

OUTPUT_DIR="cross_svgs"
BASE_URL="https://visualcube.api.cubing.net/visualcube.php"

# VisualCube parameters
SIZE=300
FORMAT="svg"
VIEW="plan"  # Top-down view to see cross clearly
STAGE="cross"  # Highlights cross edges

echo "==========================================="
echo "White Cross SVG Generator"
echo "==========================================="
echo ""

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Case 1: U Layer Oriented
echo "Generating: 3x3_cross_u-oriented-01.svg"
curl -s "${BASE_URL}?fmt=${FORMAT}&size=${SIZE}&view=${VIEW}&stage=${STAGE}&alg=F2+D+F2" \
  -o "${OUTPUT_DIR}/3x3_cross_u-oriented-01.svg"

# Case 2: U Layer Flipped
echo "Generating: 3x3_cross_u-flipped-01.svg"
curl -s "${BASE_URL}?fmt=${FORMAT}&size=${SIZE}&view=${VIEW}&stage=${STAGE}&alg=R+U+R'" \
  -o "${OUTPUT_DIR}/3x3_cross_u-flipped-01.svg"

# Case 3: U Layer Adjacent
echo "Generating: 3x3_cross_u-adjacent-01.svg"
curl -s "${BASE_URL}?fmt=${FORMAT}&size=${SIZE}&view=${VIEW}&stage=${STAGE}&alg=U+F2" \
  -o "${OUTPUT_DIR}/3x3_cross_u-adjacent-01.svg"

# Case 4: U Layer Opposite
echo "Generating: 3x3_cross_u-opposite-01.svg"
curl -s "${BASE_URL}?fmt=${FORMAT}&size=${SIZE}&view=${VIEW}&stage=${STAGE}&alg=U2+F2" \
  -o "${OUTPUT_DIR}/3x3_cross_u-opposite-01.svg"

# Case 5: D Layer Misaligned
echo "Generating: 3x3_cross_d-misaligned-01.svg"
curl -s "${BASE_URL}?fmt=${FORMAT}&size=${SIZE}&view=${VIEW}&stage=${STAGE}&alg=F2+U2+F2" \
  -o "${OUTPUT_DIR}/3x3_cross_d-misaligned-01.svg"

# Case 6: D Layer Flipped
echo "Generating: 3x3_cross_d-flipped-01.svg"
curl -s "${BASE_URL}?fmt=${FORMAT}&size=${SIZE}&view=${VIEW}&stage=${STAGE}&alg=F'+U'+R+U+F2" \
  -o "${OUTPUT_DIR}/3x3_cross_d-flipped-01.svg"

# Case 7: Middle Layer Edge
echo "Generating: 3x3_cross_middle-01.svg"
curl -s "${BASE_URL}?fmt=${FORMAT}&size=${SIZE}&view=${VIEW}&stage=${STAGE}&alg=R+U'+R'" \
  -o "${OUTPUT_DIR}/3x3_cross_middle-01.svg"

# Case 8: Middle Layer Flipped
echo "Generating: 3x3_cross_middle-flipped-01.svg"
curl -s "${BASE_URL}?fmt=${FORMAT}&size=${SIZE}&view=${VIEW}&stage=${STAGE}&alg=R'+F+R" \
  -o "${OUTPUT_DIR}/3x3_cross_middle-flipped-01.svg"

echo ""
echo "==========================================="
echo "✅ Generation complete!"
echo "   Output directory: ${OUTPUT_DIR}"
echo "   Files generated: 8 SVG files"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Review SVGs: open ${OUTPUT_DIR}/*.svg"
echo "2. Copy to Assets.xcassets:"
echo "   cp ${OUTPUT_DIR}/*.svg ../../Deddal/App/Assets.xcassets/Cross/"
