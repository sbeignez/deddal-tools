#!/bin/bash

# Define the base URL for downloading images.
base_url="https://visualcube.api.cubing.net/visualcube.php?fmt=svg&size=300&"

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

# F2L Cases stored in a flat array (no associative arrays)
f2l_cases=()
f2l_cases+=("3x3_cfop_f2l_1-fr;f2l;Good;U (R U' R')") ##
f2l_cases+=("3x3_cfop_f2l_2-fr;f2l;Good;F R' F' R")
f2l_cases+=("3x3_cfop_f2l_3-fr;f2l;Good;F' U' F")
f2l_cases+=("3x3_cfop_f2l_4-fr;f2l;Good;(R U R')") ##
f2l_cases+=("3x3_cfop_f2l_5-fr;f2l;Good;U' (R U R') U2 (R U' R')") ##
f2l_cases+=("3x3_cfop_f2l_6-fr;f2l;Good;y U (L' U' L) U2 (L' U L) y'")
f2l_cases+=("3x3_cfop_f2l_7-fr;f2l;Good;U' (R U2' R') U2 (R U' R')")
f2l_cases+=("3x3_cfop_f2l_8-fr;f2l;Good;y U (L' U2 L) U2 (L' U L) y'")
f2l_cases+=("3x3_cfop_f2l_9-fr;f2l;Good;F (R U R' U') F' (R U' R')")
f2l_cases+=("3x3_cfop_f2l_10-fr;f2l;Good;U' (R U R') U (R U R')")
f2l_cases+=("3x3_cfop_f2l_11-fr;f2l;Good;U' (R U2' R') U (F' U' F)")
f2l_cases+=("3x3_cfop_f2l_12-fr;f2l;Good;R U' R' U R U' R' U2 (R U' R')")
f2l_cases+=("3x3_cfop_f2l_13-fr;f2l;Good;y' U (R' U R) U' (R' U' R) y")
f2l_cases+=("3x3_cfop_f2l_14-fr;f2l;Good;U' (R U' R') U (R U R')")
f2l_cases+=("3x3_cfop_f2l_15-fr;f2l;Good;(R U R') U2 (R U' R') U (R U' R')")
f2l_cases+=("3x3_cfop_f2l_16-fr;f2l;Good;U F (R U R' U') F' U (R U' R')")
f2l_cases+=("3x3_cfop_f2l_17-fr;f2l;Good;(R U2' R') U' (R U R')")
f2l_cases+=("3x3_cfop_f2l_18-fr;f2l;Good;y' (R' U2 R) U (R' U' R) y")
f2l_cases+=("3x3_cfop_f2l_19-fr;f2l;Good;U (R U2' R') U (R U' R')")
f2l_cases+=("3x3_cfop_f2l_20-fr;f2l;Good;y' U' (R' U2 R) U' (R' U R) y")
f2l_cases+=("3x3_cfop_f2l_21-fr;f2l;Good;U2 (R U R') U (R U' R')")
f2l_cases+=("3x3_cfop_f2l_22-fr;f2l;Good;y' U2 (R' U' R) U' (R' U R) y")
f2l_cases+=("3x3_cfop_f2l_23-fr;f2l;Good;U (R U' R') U' (R U' R') U (R U' R')")
f2l_cases+=("3x3_cfop_f2l_24-fr;f2l;Good;F (U R U' R') F' (R U' R')")
f2l_cases+=("3x3_cfop_f2l_25-fr;f2l;Good;U' (R U' R') U' (R U R') U (R U R')")
f2l_cases+=("3x3_cfop_f2l_26-fr;f2l;Good;U (R U' R') (F R' F' R)")
f2l_cases+=("3x3_cfop_f2l_27-fr;f2l;Good;(R U' R') U (R U' R')")
f2l_cases+=("3x3_cfop_f2l_28-fr;f2l;Good;(R U R') U' (F R' F' R)")
f2l_cases+=("3x3_cfop_f2l_29-fr;f2l;Good;(R' F R F') U (R U' R')")
f2l_cases+=("3x3_cfop_f2l_30-fr;f2l;Good;(R U R') U' (R U R')")
f2l_cases+=("3x3_cfop_f2l_31-fr;f2l;Good;U' (R' F R F') (R U' R')") #
f2l_cases+=("3x3_cfop_f2l_32-fr;f2l;Good;(R U R' U') (R U R' U') (R U R' U')")
f2l_cases+=("3x3_cfop_f2l_33-fr;f2l;Good;U' (R U' R') U2 (R U' R')")
f2l_cases+=("3x3_cfop_f2l_34-fr;f2l;Good;U (R U R') U2 (R U R')")
f2l_cases+=("3x3_cfop_f2l_35-fr;f2l;Good;U2 (R U R') (F R' F' R)") ##
f2l_cases+=("3x3_cfop_f2l_36-fr;f2l;Good;U2 (R' F R F') U2 (R U R')")
f2l_cases+=("3x3_cfop_f2l_37-fr;f2l;Good;y y'")
f2l_cases+=("3x3_cfop_f2l_38-fr;f2l;Good;(R' F R F') (R U' R') U (R U' R') U2 (R U' R')")
f2l_cases+=("3x3_cfop_f2l_39-fr;f2l;Good;(R U' R') U' (R U R') U2 (R U' R')")
f2l_cases+=("3x3_cfop_f2l_40-fr;f2l;Good;(R U' R') U (R U2' R') U (R U' R')")
f2l_cases+=("3x3_cfop_f2l_41-fr;f2l;Good;R F (U R U' R') F' U' R'") #
f2l_cases+=("3x3_cfop_f2l_42-fr;f2l;Good;R U F (R U R' U') F' R'") #

f2l_cases+=("3x3_cfop_f2l_1-fl;f2l;Bad;U' L' U L") # ok
f2l_cases+=("3x3_cfop_f2l_2-fl;f2l;Bad;F' L F L'")
f2l_cases+=("3x3_cfop_f2l_3-fl;f2l;Bad;F U F'")
f2l_cases+=("3x3_cfop_f2l_4-fl;f2l;Bad;(L' U' L)")
f2l_cases+=("3x3_cfop_f2l_5-fl;f2l;Bad;U L' U' L U2 (L' U L)")
f2l_cases+=("3x3_cfop_f2l_6-fl;f2l;Bad;y U' (L U L') U2 (L U' L') y'")
f2l_cases+=("3x3_cfop_f2l_7-fl;f2l;Bad;U L' U2 L U2 (L' U L)")
f2l_cases+=("3x3_cfop_f2l_8-fl;f2l;Bad;y' U' (R U2' R') U2 (R U' R') y")
f2l_cases+=("3x3_cfop_f2l_9-fl;f2l;Bad;F' (L' U' L U) F' (L' U L)")
f2l_cases+=("3x3_cfop_f2l_10-fl;f2l;Bad;U L' U' L U' (L' U' L)")
f2l_cases+=("3x3_cfop_f2l_11-fl;f2l;Bad;U (L' U2 L) U' (F U F')")
f2l_cases+=("3x3_cfop_f2l_12-fl;f2l;Bad;L U2 L2' U' L2 U' L'")
f2l_cases+=("3x3_cfop_f2l_13-fl;f2l;Bad;y U' (L U' L') U (L U L') y'")
f2l_cases+=("3x3_cfop_f2l_14-fl;f2l;Bad;U (L' U L) U' (L' U' L)")
f2l_cases+=("3x3_cfop_f2l_15-fl;f2l;Bad;(L' U' L) U2 (L' U L) U' (L' U L)")
f2l_cases+=("3x3_cfop_f2l_16-fl;f2l;Bad;U' F' (L' U' L U) F U' (L' U L)")
f2l_cases+=("3x3_cfop_f2l_17-fl;f2l;Bad;(L' U2 L) U (L' U' L)")
f2l_cases+=("3x3_cfop_f2l_18-fl;f2l;Bad;y (L U2 L') U' (L U L') y'")
f2l_cases+=("3x3_cfop_f2l_19-fl;f2l;Bad;U' (L' U2 L) U' (L' U L)")
f2l_cases+=("3x3_cfop_f2l_20-fl;f2l;Bad;y U (L U2' L') U (L U' L') y'")
f2l_cases+=("3x3_cfop_f2l_21-fl;f2l;Bad;U2 (L' U' L) U' (L' U L)")
f2l_cases+=("3x3_cfop_f2l_22-fl;f2l;Bad;y U2 (L U L') U (L U' L') y'") ##
f2l_cases+=("3x3_cfop_f2l_23-fl;f2l;Bad;U' (L' U L) U (L' U L) U' (L' U L)")
f2l_cases+=("3x3_cfop_f2l_24-fl;f2l;Bad;F' (U' L' U L) F (L' U L)")
f2l_cases+=("3x3_cfop_f2l_25-fl;f2l;Bad;L F L' (U' L' U L) F'") ##
f2l_cases+=("3x3_cfop_f2l_26-fl;f2l;Bad;U' (L' U L) (F' L F L')")
f2l_cases+=("3x3_cfop_f2l_27-fl;f2l;Bad;(L' U L) U' (L' U L)")
f2l_cases+=("3x3_cfop_f2l_28-fl;f2l;Bad;(L' U' L) U (F' L F L')")
f2l_cases+=("3x3_cfop_f2l_29-fl;f2l;Bad;(L F' L' F) U' (L' U L)")
f2l_cases+=("3x3_cfop_f2l_30-fl;f2l;Bad;(L' U' L) U (L' U' L)")
f2l_cases+=("3x3_cfop_f2l_31-fl;f2l;Bad;U (L F' L' F) (L' U L)")
f2l_cases+=("3x3_cfop_f2l_32-fl;f2l;Bad;(L' U' L U) (L' U' L U) (L' U' L U)")
f2l_cases+=("3x3_cfop_f2l_33-fl;f2l;Bad;U (L' U L) U2 (L' U L)")
f2l_cases+=("3x3_cfop_f2l_34-fl;f2l;Bad;U' (L' U' L) U2 (L' U' L)")
f2l_cases+=("3x3_cfop_f2l_35-fl;f2l;Bad;U2 (L' U' L) (F' L F L')")
f2l_cases+=("3x3_cfop_f2l_36-fl;f2l;Bad;U2 (L F' L' F) U2 (L' U' L)")
f2l_cases+=("3x3_cfop_f2l_37-fl;f2l;Bad;y y'")
f2l_cases+=("3x3_cfop_f2l_38-fl;f2l;Bad;(L F' L' F) (L' U L) U' (L' U L) U2 (L' U L)")
f2l_cases+=("3x3_cfop_f2l_39-fl;f2l;Bad;(L' U L) U (L' U' L) U2 (L' U L)")
f2l_cases+=("3x3_cfop_f2l_40-fl;f2l;Bad;(L' U L) U' (L' U2 L) U' (L' U L)")
f2l_cases+=("3x3_cfop_f2l_41-fl;f2l;Bad;L' F' (U' L' U L) F U L")
f2l_cases+=("3x3_cfop_f2l_42-fl;f2l;Bad;L' U' F' (L' U' L U) F L")


# Loop through cases
for case_info in "${f2l_cases[@]}"; do
  IFS=";" read -r case_name stage rotation formula <<< "$case_info"

  # Determine rotation parameter
  if [[ "$rotation" == "Good" ]]; then
    rParam="y30x-35"
  else
    rParam="y-30x-35"
  fi

  # Encode formula properly
  encoded=$(urlencode "$formula")

  # Construct final URL
  image_url="${base_url}stage=${stage}&r=${rParam}&case=${encoded}"

  echo "Downloading ${case_name} from: $image_url"

  # Use curl to download
  curl -L -s -o "${case_name}.svg" "$image_url"

  # ✅ Replace fill='#FFFFFF' with fill="none" in the downloaded SVG
  if [ -f "${case_name}.svg" ]; then
    sed -i '' "s/<rect fill='#FFFFFF'/<rect fill='none'/g" "${case_name}.svg" # ✅ macOS version (uses `-i ''`)
    echo "Updated ${case_name}.svg to remove background fill."
  else
    echo "Failed to download ${case_name}.svg"
  fi
#  if [ $? -eq 0 ]; then
#    echo "Saved ${case_name}.svg"
#  else
#    echo "Failed to download ${case_name}.svg"
#  fi
done

