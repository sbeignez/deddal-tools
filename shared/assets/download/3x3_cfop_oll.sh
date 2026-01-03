#!/bin/bash

# RUN
# Open terminal
# cd Code, cd LookAhead.. Case OLL
# bash Dowonload-OLL-Cases

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

# OLL Cases stored in a flat array (no associative arrays)
oll_cases=()
oll_cases+=("3x3_cfop_oll_1;oll;;(R U2 R') (R' F R F') U2 (R' F R F');")
oll_cases+=("3x3_cfop_oll_2;oll;;F (R U R' U') F' f (R U R' U') f';")
oll_cases+=("3x3_cfop_oll_3;oll;;y' f (R U R' U') f' (U') F (R U R' U') F';")
oll_cases+=("3x3_cfop_oll_4;oll;;y' f (R U R' U') f' (U) F (R U R' U') F';")
oll_cases+=("3x3_cfop_oll_5;oll;;r' U2 (R U R' U) r;")
oll_cases+=("3x3_cfop_oll_6;oll;;r U2 (R' U' R U') r';")
oll_cases+=("3x3_cfop_oll_7;oll;;r (U R' U R) U2 r';")
oll_cases+=("3x3_cfop_oll_8;oll;;y2 r' (U' R U' R') U2 r;")
oll_cases+=("3x3_cfop_oll_9;oll;;y (R U R' U') (R' F R) (R U R' U') F';")
oll_cases+=("3x3_cfop_oll_10;oll;;(R U R' U) (R' F R F') (R U2 R');")
oll_cases+=("3x3_cfop_oll_11;oll;;M (R U R' U R U2 R') U M';")
oll_cases+=("3x3_cfop_oll_12;oll;;y' M' (R' U' R U' R' U2 R) U' M;")
oll_cases+=("3x3_cfop_oll_13;oll;;(r U' r') U' (r U r') (F' U F);")
oll_cases+=("3x3_cfop_oll_14;oll;;R' F (R U R') F' R (F U' F');")
oll_cases+=("3x3_cfop_oll_15;oll;;(r' U' r) (R' U' R U) (r' U r);")
oll_cases+=("3x3_cfop_oll_16;oll;;(r U r') (R U R' U') (r U' r');")
oll_cases+=("3x3_cfop_oll_17;oll;;(R U R' U) (R' F R F') U2 (R' F R F');")
oll_cases+=("3x3_cfop_oll_18;oll;;r U R' U R U2 r2 U' R U' R' U2 r;")
oll_cases+=("3x3_cfop_oll_19;oll;;M U (R U R' U') M' (R' F R F');")
oll_cases+=("3x3_cfop_oll_20;oll;;(r U R' U' M2) U (R U' R') U' M';")
oll_cases+=("3x3_cfop_oll_21;oll;;(R U R' U) (R U' R' U) (R U2 R');")
oll_cases+=("3x3_cfop_oll_22;oll;;R U2 (R2' U') (R2 U') (R2' U') U' R;")
oll_cases+=("3x3_cfop_oll_23;oll;;R2 D (R' U2 R) D' (R' U2 R');")
oll_cases+=("3x3_cfop_oll_24;oll;;(r U R' U') (r' F R F');")
oll_cases+=("3x3_cfop_oll_25;oll;;F' r U R' U' r' F R;")
oll_cases+=("3x3_cfop_oll_26;oll;;R U2 (R' U' R U') R';")
oll_cases+=("3x3_cfop_oll_27;oll;;(R U R' U) (R U2 R');")
oll_cases+=("3x3_cfop_oll_28;oll;;(r U R' U') M (U R U' R');")
oll_cases+=("3x3_cfop_oll_29;oll;;y2 R2 U' R F R' U R2 U' R' F' R;")
oll_cases+=("3x3_cfop_oll_30;oll;;y2 F U (R U2 R') U' (R U2 R') U' F';")
oll_cases+=("3x3_cfop_oll_31;oll;;(R' U' F) (U R U' R') F' R;")
oll_cases+=("3x3_cfop_oll_32;oll;;y2 L U F' U' L' U L F L';")
oll_cases+=("3x3_cfop_oll_33;oll;;(R U R' U') (R' F R F');")
oll_cases+=("3x3_cfop_oll_34;oll;;R U R2 U' R' F (R U R U') F';")
oll_cases+=("3x3_cfop_oll_35;oll;;(R U2 R') (R' F R F') (R U2 R');")
oll_cases+=("3x3_cfop_oll_36;oll;;(L' U' L U') (L' U L U) (L F' L' F);")
oll_cases+=("3x3_cfop_oll_37;oll;;F R (U' R' U') (R U R') F';")
oll_cases+=("3x3_cfop_oll_38;oll;;(R U R' U) (R U' R' U') (R' F R F');")
oll_cases+=("3x3_cfop_oll_39;oll;;y L F' (L' U' L U) F U' L';")
oll_cases+=("3x3_cfop_oll_40;oll;;y R' F R U R' U' F' U R;")
oll_cases+=("3x3_cfop_oll_41;oll;;(R U R' U) (R U2 R') F (R U R' U') F';")
oll_cases+=("3x3_cfop_oll_42;oll;;(R' U' R U') (R' U2 R) F (R U R' U') F';")
oll_cases+=("3x3_cfop_oll_43;oll;;R' U' (F' U F) R;")
oll_cases+=("3x3_cfop_oll_44;oll;;f (R U R' U') f';")
oll_cases+=("3x3_cfop_oll_45;oll;;F (R U R' U') F';")
oll_cases+=("3x3_cfop_oll_46;oll;;(R' U' R' F R F') U R;")
oll_cases+=("3x3_cfop_oll_47;oll;;F' (L' U' L U) (L' U' L U) F;")
oll_cases+=("3x3_cfop_oll_48;oll;;F (R U R' U') (R U R' U') F';")
oll_cases+=("3x3_cfop_oll_49;oll;;r U' (r2 U) (r2 U) (r2) U' r;")
oll_cases+=("3x3_cfop_oll_50;oll;;r' U (r2 U') (r2 U') (r2) U r';")
oll_cases+=("3x3_cfop_oll_51;oll;;f (R U R' U') (R U R' U') f';")
oll_cases+=("3x3_cfop_oll_52;oll;;R' (F' U' F U') (R U R' U) R;")
oll_cases+=("3x3_cfop_oll_53;oll;;(r' U2 R U R' U' R U R' U r);")
oll_cases+=("3x3_cfop_oll_54;oll;;(r U2 R' U' R U R' U' R U' r');")
oll_cases+=("3x3_cfop_oll_55;oll;;(R U2 R2 U' R U' R') U2 F R F';")
oll_cases+=("3x3_cfop_oll_56;oll;;(r U r') (U R U' R') (U R U' R') (r U' r');")
oll_cases+=("3x3_cfop_oll_57;oll;;(R U R' U') M' (U R U' r');")


oll_cases+=("3x3_cfop_oell_l;oell;;f ( R U R' U' ) f';")
oll_cases+=("3x3_cfop_oell_i;oell;;F ( R U R' U' ) F';")
oll_cases+=("3x3_cfop_oell_dot;oell;;F ( R U R' U' ) F' f ( R U R' U' ) f';")



# Loop through cases
for case_info in "${oll_cases[@]}"; do
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
