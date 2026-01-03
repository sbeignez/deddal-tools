#!/bin/bash

# Define the base URL for downloading images.
base_url="https://visualcube.api.cubing.net/visualcube.php?fmt=svg&size=200&view=plan&"

# Function to URL-encode a string.
urlencode() {
  local string="${1}"
  local length="${#string}"
  local encoded=""
  local pos c
  for (( pos=0 ; pos<length ; pos++ )); do
    c="${string:$pos:1}"
    case "$c" in
      [a-zA-Z0-9.~_-]) encoded+="$c" ;;
      "'") encoded+="%27" ;;  # Properly encode single quotes
      *) encoded+=$(printf '%%%02X' "'$c") ;;
    esac
  done
  echo "$encoded"
}

# PLL Cases stored in a flat array (no associative arrays)
pll_cases=()
pll_cases+=("3x3_cfop_pll_ua-perm;pll;Good;U2 (R U' R U) R U (R U' R' U') R2;U1U3-s7,U3U5-s7,U5U1-s7")
pll_cases+=("3x3_cfop_pll_ub-perm;pll;Good;U2 R2 U (R U R' U') R' U' (R' U R');U1U5-s7,U5U3-s7,U3U1-s7")
pll_cases+=("3x3_cfop_pll_h-perm;pll;Good;(M2 U' M2) U2 (M2 U' M2);U1U7,U7U1,U3U5,U5U3")
pll_cases+=("3x3_cfop_pll_z-perm;pll;Good;(M2 U) (M2 U) (M' U2) M2 (U2 M');U1U3,U3U1,U5U7,U7U5")

pll_cases+=("3x3_cfop_pll_e-perm;pll;Good;y x' (R U' R' D) (R U R' D') (R U R' D) (R U' R' D') x;U0U2,U2U0,U6U8,U8U6")
pll_cases+=("3x3_cfop_pll_na-perm;pll;Good;(R U R' U) (R U R' F') (R U R' U') R' F R2 U' R' U2 (R U' R');U2U6,U6U2,U3U5,U5U3")
pll_cases+=("3x3_cfop_pll_nb-perm;pll;Good;(R' U R U' R') (F' U' F) (R U R') (F R' F') (R U' R);U0U8,U8U0,U3U5,U5U3")
pll_cases+=("3x3_cfop_pll_v-perm;pll;Good;(R' U R' U') (R D' R' D) (R' U D') (R2 U' R2) D R2;U0U8,U8U0,U1U5,U5U1")
pll_cases+=("3x3_cfop_pll_y-perm;pll;Good;F R (U' R' U') (R U R' F') (R U R' U') (R' F R F');U0U8,U8U0,U3U1,U1U3")

pll_cases+=("3x3_cfop_pll_aa-perm;pll;Good;x (R' U R') D2 (R U' R') D2 R2 x';U0U2-s7,U2U8-s7,U8U0-s8")
pll_cases+=("3x3_cfop_pll_ab-perm;pll;Good;x R2 D2 (R U R') D2 (R U' R) x';U2U6-s8,U6U8-s7,U8U2-s7")
pll_cases+=("3x3_cfop_pll_f-perm;pll;Good;y (R' U' F') (R U R' U') R' F R2 (U' R' U') (R U R' U) R;U0U2,U2U0,U3U5,U5U3")
pll_cases+=("3x3_cfop_pll_ga-perm;pll;Good;R2 (U R' U R' U' R U') R2 D (U' R' U R) D';U0U8-s8,U8U6-s8,U6U0-s8,U1U3-s8-black,U3U7-s8-black,U7U1-s8-black")
pll_cases+=("3x3_cfop_pll_gb-perm;pll;Good;(R' U' R U) D' R2 (U R' U R U' R U') R2 D;U8U0-s8,U0U6-s8,U6U8-s8,U1U7-s8-black,U7U3-s8-black,U3U1-s8-black")
pll_cases+=("3x3_cfop_pll_gc-perm;pll;Good;R2 (U' R U' R U R' U) R2 D' (U R U' R') D;U2U6-s8,U6U8-s8,U8U2-s8,U1U5-s8-black,U5U7-s8-black,U7U1-s8-black")
pll_cases+=("3x3_cfop_pll_gd-perm;pll;Good;(R U R' U') D R2 (U' R U' R' U R' U) R2 D';U6U2-s8,U2U8-s8,U8U6-s8,U1U7-s8-black,U7U5-s8-black,U5U1-s8-black")
pll_cases+=("3x3_cfop_pll_ja-perm;pll;Good;y (R' U L') U2 (R U' R') U2 R L;U0U6,U6U0,U3U7-s6,U7U3-s6")
pll_cases+=("3x3_cfop_pll_jb-perm;pll;Good;(R U R' F') (R U R' U') R' F R2 U' R';U2U8,U8U2,U5U7-s6,U7U5-s6")
pll_cases+=("3x3_cfop_pll_ra-perm;pll;Good;y (R U' R' U') (R U R D) (R' U' R D') (R' U2 R');U1U5,U5U1,U6U8,U8U6")
pll_cases+=("3x3_cfop_pll_rb-perm;pll;Good;(R' U2) (R U2) (R' F R) (U R' U' R') F' R2;U0U2,U2U0,U5U7,U7U5")
pll_cases+=("3x3_cfop_pll_t-perm;pll;Good;(R U R' U') (R' F R2) (U' R' U') (R U R' F');U2U8,U8U2,U3U5-s8,U5U3-s8")

pll_cases+=("3x3_cfop_pll_pcll-adj;coll;Good;(R U R' U') (R' F R2) (U' R' U') (R U R' F');U2U8-black,U8U2-black")
pll_cases+=("3x3_cfop_pll_pcll-dia;coll;Good;F R (U' R' U') (R U R' F') (R U R' U') (R' F R F');U0U8-black,U8U0-black")





# Loop through cases
for case_info in "${pll_cases[@]}"; do
  IFS=";" read -r case_name stage rotation formula arrows <<< "$case_info"

  # Determine rotation parameter (always "Good" for PLL)
  rParam="y30x-35"

  # Encode formula properly
  encoded=$(urlencode "$formula")

  # Construct final URL with the new parameters
  image_url="${base_url}stage=${stage}&r=${rParam}&case=${encoded}&arw=${arrows}"

  echo "Downloading ${case_name} from: $image_url"

  # Use curl to download
  curl -L -s -o "${case_name}.svg" "$image_url"

  if [ -f "${case_name}.svg" ]; then
    sed -i '' "s/<rect fill='#FFFFFF'/<rect fill='none'/g" "${case_name}.svg" # ✅ macOS version (uses `-i ''`)
    echo "Updated ${case_name}.svg to remove background fill."
  else
    echo "Failed to download ${case_name}.svg"
  fi
done
