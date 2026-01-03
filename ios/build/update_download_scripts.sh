#!/bin/bash

# Update download and upload scripts with new naming convention

set -e

echo "🔄 Updating download/upload scripts with new naming..."
echo ""

# F2L script - replace Case-F2L-XX-YY with 3x3_cfop_f2l_X-yy (no padding, lowercase)
echo "📝 Updating F2L download script..."
sed -i '' 's/Case-F2L-0\([1-9]\)-FR/3x3_cfop_f2l_\1-fr/g' Ressources/Cases-F2L/Download-F2L-Cases.sh
sed -i '' 's/Case-F2L-\([1-9][0-9]\)-FR/3x3_cfop_f2l_\1-fr/g' Ressources/Cases-F2L/Download-F2L-Cases.sh
sed -i '' 's/Case-F2L-0\([1-9]\)-FL/3x3_cfop_f2l_\1-fl/g' Ressources/Cases-F2L/Download-F2L-Cases.sh
sed -i '' 's/Case-F2L-\([1-9][0-9]\)-FL/3x3_cfop_f2l_\1-fl/g' Ressources/Cases-F2L/Download-F2L-Cases.sh
echo "  ✅ F2L script updated"
echo ""

# OLL script - replace Case-OLL-XX with 3x3_cfop_oll_X (no padding)
echo "📝 Updating OLL download script..."
sed -i '' 's/Case-OLL-0\([1-9]\)/3x3_cfop_oll_\1/g' Ressources/Cases-OLL/Download-OLL-Cases.sh
sed -i '' 's/Case-OLL-\([1-9][0-9]\)/3x3_cfop_oll_\1/g' Ressources/Cases-OLL/Download-OLL-Cases.sh
# Also update OeLL cases
sed -i '' 's/Case-OeLL-Dot/3x3_cfop_oell_dot/g' Ressources/Cases-OLL/Download-OLL-Cases.sh
sed -i '' 's/Case-OeLL-I/3x3_cfop_oell_i/g' Ressources/Cases-OLL/Download-OLL-Cases.sh
sed -i '' 's/Case-OeLL-L/3x3_cfop_oell_l/g' Ressources/Cases-OLL/Download-OLL-Cases.sh
echo "  ✅ OLL script updated"
echo ""

# PLL script - replace img-case-X-Perm with 3x3_cfop_pll_x-perm (lowercase)
echo "📝 Updating PLL download script..."
sed -i '' 's/img-case-Aa-Perm/3x3_cfop_pll_aa-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Ab-Perm/3x3_cfop_pll_ab-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-E-Perm/3x3_cfop_pll_e-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-F-Perm/3x3_cfop_pll_f-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Ga-Perm/3x3_cfop_pll_ga-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Gb-Perm/3x3_cfop_pll_gb-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Gc-Perm/3x3_cfop_pll_gc-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Gd-Perm/3x3_cfop_pll_gd-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-H-Perm/3x3_cfop_pll_h-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Ja-Perm/3x3_cfop_pll_ja-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Jb-Perm/3x3_cfop_pll_jb-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Na-Perm/3x3_cfop_pll_na-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Nb-Perm/3x3_cfop_pll_nb-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Ra-Perm/3x3_cfop_pll_ra-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Rb-Perm/3x3_cfop_pll_rb-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-T-Perm/3x3_cfop_pll_t-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Ua-Perm/3x3_cfop_pll_ua-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Ub-Perm/3x3_cfop_pll_ub-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-V-Perm/3x3_cfop_pll_v-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Y-Perm/3x3_cfop_pll_y-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-Z-Perm/3x3_cfop_pll_z-perm/g' Ressources/PLL-cases/Download-PLL-Cases.sh
# PcLL cases
sed -i '' 's/img-case-PcLL-Adj/3x3_cfop_pll_pcll-adj/g' Ressources/PLL-cases/Download-PLL-Cases.sh
sed -i '' 's/img-case-PcLL-Dia/3x3_cfop_pll_pcll-dia/g' Ressources/PLL-cases/Download-PLL-Cases.sh
echo "  ✅ PLL script updated"
echo ""

# Upload script - update old Ortega naming
echo "📝 Updating upload script..."
if [ -f upload_case_images.sh ]; then
    sed -i '' 's/caseimg_Ortega-OLL-/2x2_ortega_oll_/g' upload_case_images.sh
    sed -i '' 's/caseimg_Ortega-PBL-/2x2_ortega_pbl_/g' upload_case_images.sh
    echo "  ✅ Upload script updated"
else
    echo "  ⚠️  Upload script not found"
fi
echo ""

echo "════════════════════════════════════════"
echo "✅ All scripts updated successfully!"
echo "════════════════════════════════════════"
