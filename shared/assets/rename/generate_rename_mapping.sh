#!/bin/bash

# Generate comprehensive rename mapping CSV file
# Documents all transformations: old_name → new_name

OUTPUT_FILE="rename_mapping.csv"

echo "Generating rename mapping CSV..."
echo "type,category,old_name,new_name" > "$OUTPUT_FILE"

# Helper function to convert to lowercase and clean
to_lowercase() {
    echo "$1" | tr '[:upper:]' '[:lower:]'
}

# 1. F2L SVG Files (84 files: 42 FL + 42 FR)
# Current pattern: Case-F2L-{1-42}-{FL|FR}.svg
# Target: 3x3_cfop_f2l_{1-42}-{fl|fr}.svg
echo "Processing F2L SVG files..."
for side in FL FR; do
    side_lower=$(to_lowercase "$side")
    for i in {1..42}; do
        old="Case-F2L-${i}-${side}.svg"
        new="3x3_cfop_f2l_${i}-${side_lower}.svg"
        echo "svg,f2l,$old,$new" >> "$OUTPUT_FILE"
    done
done

# 2. OLL SVG Files (57 standard + 3 OeLL = 60 files)
# Current pattern: Case-OLL-{1-57}.svg + Case-OeLL-{Dot|I|L}.svg
# Target: 3x3_cfop_oll_{1-57}.svg + 3x3_cfop_oell_{dot|i|l}.svg
echo "Processing OLL SVG files..."
for i in {1..57}; do
    old="Case-OLL-${i}.svg"
    new="3x3_cfop_oll_${i}.svg"
    echo "svg,oll,$old,$new" >> "$OUTPUT_FILE"
done

# OeLL edge cases (not in JSON, but have SVG/imageset files)
for case in "Dot:dot" "I:i" "L:l"; do
    old_case="${case%%:*}"
    new_case="${case##*:}"
    old="Case-OeLL-${old_case}.svg"
    new="3x3_cfop_oell_${new_case}.svg"
    echo "svg,oell,$old,$new" >> "$OUTPUT_FILE"
done

# 3. PLL SVG Files (21 perms + 2 PcLL = 23 files)
# Current pattern: img-case-{PermName}.svg + img-case-PcLL-{Adj|Dia}.svg
# Target: 3x3_cfop_pll_{permname}.svg + 3x3_cfop_pll_pcll-{adj|dia}.svg
echo "Processing PLL SVG files..."
pll_perms=(
    "Aa-Perm:aa-perm"
    "Ab-Perm:ab-perm"
    "E-Perm:e-perm"
    "F-Perm:f-perm"
    "Ga-Perm:ga-perm"
    "Gb-Perm:gb-perm"
    "Gc-Perm:gc-perm"
    "Gd-Perm:gd-perm"
    "H-Perm:h-perm"
    "Ja-Perm:ja-perm"
    "Jb-Perm:jb-perm"
    "Na-Perm:na-perm"
    "Nb-Perm:nb-perm"
    "Ra-Perm:ra-perm"
    "Rb-Perm:rb-perm"
    "T-Perm:t-perm"
    "Ua-Perm:ua-perm"
    "Ub-Perm:ub-perm"
    "V-Perm:v-perm"
    "Y-Perm:y-perm"
    "Z-Perm:z-perm"
)

for perm_mapping in "${pll_perms[@]}"; do
    old_perm="${perm_mapping%%:*}"
    new_perm="${perm_mapping##*:}"
    old="img-case-${old_perm}.svg"
    new="3x3_cfop_pll_${new_perm}.svg"
    echo "svg,pll,$old,$new" >> "$OUTPUT_FILE"
done

# PcLL corner permutation cases
for case in "Adj:adj" "Dia:dia"; do
    old_case="${case%%:*}"
    new_case="${case##*:}"
    old="img-case-PcLL-${old_case}.svg"
    new="3x3_cfop_pll_pcll-${new_case}.svg"
    echo "svg,pcll,$old,$new" >> "$OUTPUT_FILE"
done

# 4. Ortega OLL SVG Files (7 files)
# Current: caseimg_Ortega-OLL-{1-7}.svg
# Target: 2x2_ortega_oll_{1-7}.svg
echo "Processing Ortega OLL SVG files..."
for i in {1..7}; do
    old="caseimg_Ortega-OLL-${i}.svg"
    new="2x2_ortega_oll_${i}.svg"
    echo "svg,ortega-oll,$old,$new" >> "$OUTPUT_FILE"
done

# 5. Ortega PBL SVG Files (5 files)
# Current: caseimg_Ortega-PBL-{1-5}.svg
# Target: 2x2_ortega_pbl_{1-5}.svg
echo "Processing Ortega PBL SVG files..."
for i in {1..5}; do
    old="caseimg_Ortega-PBL-${i}.svg"
    new="2x2_ortega_pbl_${i}.svg"
    echo "svg,ortega-pbl,$old,$new" >> "$OUTPUT_FILE"
done

# 6. F2L Imageset Folders (84 folders)
# Current: caseimg_F2L-{1-42}-{FL|FR}.imageset
# Target: caseimg_3x3_cfop_f2l_{1-42}-{fl|fr}.imageset
echo "Processing F2L imageset folders..."
for side in FL FR; do
    side_lower=$(to_lowercase "$side")
    for i in {1..42}; do
        old="caseimg_F2L-${i}-${side}.imageset"
        new="caseimg_3x3_cfop_f2l_${i}-${side_lower}.imageset"
        echo "imageset,f2l,$old,$new" >> "$OUTPUT_FILE"
    done
done

# 7. OLL Imageset Folders (57 standard + 3 OeLL = 60 folders)
# Current: caseimg_OLL-{1-57}.imageset + caseimg_OeLL-{Dot|I|L}.imageset
# Target: caseimg_3x3_cfop_oll_{1-57}.imageset + caseimg_3x3_cfop_oell_{dot|i|l}.imageset
echo "Processing OLL imageset folders..."
for i in {1..57}; do
    old="caseimg_OLL-${i}.imageset"
    new="caseimg_3x3_cfop_oll_${i}.imageset"
    echo "imageset,oll,$old,$new" >> "$OUTPUT_FILE"
done

# OeLL edge cases imagesets
for case in "Dot:dot" "I:i" "L:l"; do
    old_case="${case%%:*}"
    new_case="${case##*:}"
    old="caseimg_OeLL-${old_case}.imageset"
    new="caseimg_3x3_cfop_oell_${new_case}.imageset"
    echo "imageset,oell,$old,$new" >> "$OUTPUT_FILE"
done

# 8. PLL Imageset Folders (21 perms + 2 PcLL = 23 folders)
# Current: caseimg_{PermName}.imageset (mixed case, WITHOUT "PLL-" prefix!) + caseimg_PcLL-{Adj|Dia}.imageset
# Target: caseimg_3x3_cfop_pll_{permname}.imageset + caseimg_3x3_cfop_pll_pcll-{adj|dia}.imageset
echo "Processing PLL imageset folders..."

# Standard PLL cases (note: imagesets use caseimg_Aa-Perm NOT caseimg_PLL-Aa-Perm)
pll_imageset_perms=(
    "Aa-Perm:aa-perm"
    "Ab-Perm:ab-perm"
    "E-Perm:e-perm"
    "F-Perm:f-perm"
    "Ga-Perm:ga-perm"
    "Gb-Perm:gb-perm"
    "Gc-Perm:gc-perm"
    "Gd-Perm:gd-perm"
    "H-Perm:h-perm"
    "Ja-Perm:ja-perm"
    "Jb-Perm:jb-perm"
    "Na-Perm:na-perm"
    "Nb-Perm:nb-perm"
    "Ra-Perm:ra-perm"
    "Rb-Perm:rb-perm"
    "T-Perm:t-perm"
    "Ua-Perm:ua-perm"
    "Ub-Perm:ub-perm"
    "V-Perm:v-perm"
    "Y-Perm:y-perm"
    "Z-Perm:z-perm"
)

for perm_mapping in "${pll_imageset_perms[@]}"; do
    old_perm="${perm_mapping%%:*}"
    new_perm="${perm_mapping##*:}"
    old="caseimg_${old_perm}.imageset"
    new="caseimg_3x3_cfop_pll_${new_perm}.imageset"
    echo "imageset,pll,$old,$new" >> "$OUTPUT_FILE"
done

# PcLL corner permutation cases
for case in "Adj:adj" "Dia:dia"; do
    old_case="${case%%:*}"
    new_case="${case##*:}"
    old="caseimg_PcLL-${old_case}.imageset"
    new="caseimg_3x3_cfop_pll_pcll-${new_case}.imageset"
    echo "imageset,pcll,$old,$new" >> "$OUTPUT_FILE"
done

# 9. Ortega OLL Imageset Folders (7 folders)
# Current: caseimg_Ortega-OLL-{1-7}.imageset
# Target: caseimg_2x2_ortega_oll_{1-7}.imageset
echo "Processing Ortega OLL imageset folders..."
for i in {1..7}; do
    old="caseimg_Ortega-OLL-${i}.imageset"
    new="caseimg_2x2_ortega_oll_${i}.imageset"
    echo "imageset,ortega-oll,$old,$new" >> "$OUTPUT_FILE"
done

# 10. Ortega PBL Imageset Folders (5 folders)
# Current: caseimg_Ortega-PBL-{1-5}.imageset
# Target: caseimg_2x2_ortega_pbl_{1-5}.imageset
echo "Processing Ortega PBL imageset folders..."
for i in {1..5}; do
    old="caseimg_Ortega-PBL-${i}.imageset"
    new="caseimg_2x2_ortega_pbl_${i}.imageset"
    echo "imageset,ortega-pbl,$old,$new" >> "$OUTPUT_FILE"
done

# 11. JSON Records - F2L (82 records: 42 FL with values, 40 FR with null)
# Current FL: "Case-F2L-1-FL" (42 records)
# Current FR: null (40 records - need to populate)
# Target: "caseimg_3x3_cfop_f2l_1-fl"
echo "Processing F2L JSON records..."
for side in FL FR; do
    side_lower=$(to_lowercase "$side")
    for i in {1..42}; do
        if [ "$side" = "FL" ]; then
            old="Case-F2L-${i}-${side}"
        else
            old="null"
        fi
        new="caseimg_3x3_cfop_f2l_${i}-${side_lower}"
        echo "json,f2l,$old,$new" >> "$OUTPUT_FILE"
    done
done

# 12. JSON Records - OLL (57 records, all currently null)
# Target: "caseimg_3x3_cfop_oll_1" through "caseimg_3x3_cfop_oll_57"
echo "Processing OLL JSON records..."
for i in {1..57}; do
    old="null"
    new="caseimg_3x3_cfop_oll_${i}"
    echo "json,oll,$old,$new" >> "$OUTPUT_FILE"
done

# 13. JSON Records - PLL (21 records, all currently null)
# Target: "caseimg_3x3_cfop_pll_{permname}"
echo "Processing PLL JSON records..."
for perm_mapping in "${pll_perms[@]}"; do
    new_perm="${perm_mapping##*:}"
    old="null"
    new="caseimg_3x3_cfop_pll_${new_perm}"
    echo "json,pll,$old,$new" >> "$OUTPUT_FILE"
done

# 14. JSON Records - Ortega OLL (7 records)
# Current: "caseimg_Ortega-OLL-1"
# Target: "caseimg_2x2_ortega_oll_1"
echo "Processing Ortega OLL JSON records..."
for i in {1..7}; do
    old="caseimg_Ortega-OLL-${i}"
    new="caseimg_2x2_ortega_oll_${i}"
    echo "json,ortega-oll,$old,$new" >> "$OUTPUT_FILE"
done

# 15. JSON Records - Ortega PBL (5 records)
# Current: "caseimg_Ortega-PBL-1"
# Target: "caseimg_2x2_ortega_pbl_1"
echo "Processing Ortega PBL JSON records..."
for i in {1..5}; do
    old="caseimg_Ortega-PBL-${i}"
    new="caseimg_2x2_ortega_pbl_${i}"
    echo "json,ortega-pbl,$old,$new" >> "$OUTPUT_FILE"
done

echo ""
echo "✅ Rename mapping generated: $OUTPUT_FILE"
echo ""
echo "Summary:"
echo "- SVG files: 179 mappings"
echo "- Imageset folders: 180 mappings"
echo "- JSON records: 172 mappings"
echo ""
wc -l "$OUTPUT_FILE"
