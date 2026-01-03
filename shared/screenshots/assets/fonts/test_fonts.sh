#!/bin/bash
# Test all Noto fonts for 39 languages
# Generates sample images to verify fonts are working

set -euo pipefail

FONTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEST_OUTPUT="${FONTS_DIR}/test_output"

mkdir -p "${TEST_OUTPUT}"

echo "🎨 Testing all 39 language fonts..."

# Test each language with sample text
declare -A TEST_TEXTS
TEST_TEXTS["ar-SA"]="مرحبا بك"
TEST_TEXTS["he"]="שלום"
TEST_TEXTS["el"]="Καλώς ήρθες"
TEST_TEXTS["ru"]="Привет"
TEST_TEXTS["uk"]="Привіт"
TEST_TEXTS["zh-Hans"]="你好"
TEST_TEXTS["zh-Hant"]="你好"
TEST_TEXTS["ja"]="こんにちは"
TEST_TEXTS["ko"]="안녕하세요"
TEST_TEXTS["th"]="สวัสดี"
TEST_TEXTS["hi"]="नमस्ते"
TEST_TEXTS["en-US"]="Hello World"
TEST_TEXTS["fr-FR"]="Bonjour"
TEST_TEXTS["es-ES"]="Hola"
TEST_TEXTS["de-DE"]="Guten Tag"
TEST_TEXTS["it"]="Ciao"
TEST_TEXTS["pt-BR"]="Olá"
TEST_TEXTS["nl-NL"]="Hallo"
TEST_TEXTS["da"]="Hej"
TEST_TEXTS["no"]="Hei"
TEST_TEXTS["sv"]="Hej"
TEST_TEXTS["fi"]="Hei"
TEST_TEXTS["pl"]="Cześć"
TEST_TEXTS["cs"]="Ahoj"
TEST_TEXTS["sk"]="Ahoj"
TEST_TEXTS["hr"]="Bok"
TEST_TEXTS["hu"]="Helló"
TEST_TEXTS["ro"]="Salut"
TEST_TEXTS["ca"]="Hola"
TEST_TEXTS["id"]="Halo"
TEST_TEXTS["ms"]="Hai"
TEST_TEXTS["vi"]="Xin chào"
TEST_TEXTS["tr"]="Merhaba"

# Font mapping (same as in imagemagick_utils.sh)
get_font_for_lang() {
    local lang="$1"
    case "${lang}" in
        ar-SA) echo "${FONTS_DIR}/arabic/NotoSansArabic-Bold.ttf" ;;
        he) echo "${FONTS_DIR}/hebrew/NotoSansHebrew-Bold.ttf" ;;
        el) echo "${FONTS_DIR}/greek/NotoSans-Bold.ttf" ;;
        ru|uk) echo "${FONTS_DIR}/cyrillic/NotoSans-Bold.ttf" ;;
        zh-Hans) echo "${FONTS_DIR}/chinese/NotoSansSC-Bold.otf" ;;
        zh-Hant) echo "${FONTS_DIR}/chinese/NotoSansTC-Bold.otf" ;;
        ja) echo "${FONTS_DIR}/japanese/NotoSansJP-Bold.otf" ;;
        ko) echo "${FONTS_DIR}/korean/NotoSansKR-Bold.otf" ;;
        th) echo "${FONTS_DIR}/thai/NotoSansThai-Bold.ttf" ;;
        hi) echo "${FONTS_DIR}/devanagari/NotoSansDevanagari-Bold.ttf" ;;
        *) echo "${FONTS_DIR}/latin/NotoSans-Bold.ttf" ;;
    esac
}

# Generate test image for each language
for lang in "${!TEST_TEXTS[@]}"; do
    text="${TEST_TEXTS[$lang]}"
    font=$(get_font_for_lang "$lang")
    output="${TEST_OUTPUT}/${lang}.png"

    if [ ! -f "${font}" ]; then
        echo "  ❌ ${lang}: Font missing: ${font}"
        continue
    fi

    # Generate test image with ImageMagick
    if magick -size 600x200 \
        -background white \
        -fill black \
        -font "${font}" \
        -pointsize 48 \
        -gravity center \
        label:"${text}" \
        "${output}" 2>/dev/null; then
        echo "  ✅ ${lang}: ${text}"
    else
        echo "  ❌ ${lang}: Failed to render"
    fi
done

echo ""
echo "✅ Font test complete!"
echo "📂 Test images: ${TEST_OUTPUT}"
echo ""
echo "Total fonts: $(find "${FONTS_DIR}" -name '*.ttf' -o -name '*.otf' | wc -l | tr -d ' ')"
echo "Total size: $(du -sh "${FONTS_DIR}" | cut -f1)"
