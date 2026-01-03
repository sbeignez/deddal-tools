#!/bin/bash
# Download all Noto fonts for screenshot text overlays
# License: SIL Open Font License 1.1

set -euo pipefail

FONTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📥 Downloading Noto fonts for 39 languages (Bold + Regular)..."

# Latin (supports all Latin-script languages)
echo "  → Latin (Noto Sans) - Bold + Regular"
curl -L "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Bold.ttf" \
  -o "$FONTS_DIR/latin/NotoSans-Bold.ttf"
curl -L "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSans/NotoSans-Regular.ttf" \
  -o "$FONTS_DIR/latin/NotoSans-Regular.ttf"

# Cyrillic (Russian, Ukrainian)
echo "  → Cyrillic (Noto Sans) - symlinks to Latin"
# Noto Sans already includes Cyrillic, just symlink both weights
ln -sf "../latin/NotoSans-Bold.ttf" "$FONTS_DIR/cyrillic/NotoSans-Bold.ttf"
ln -sf "../latin/NotoSans-Regular.ttf" "$FONTS_DIR/cyrillic/NotoSans-Regular.ttf"

# Arabic (ar-SA)
echo "  → Arabic (Noto Sans Arabic) - Bold + Regular"
curl -L "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Bold.ttf" \
  -o "$FONTS_DIR/arabic/NotoSansArabic-Bold.ttf"
curl -L "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSansArabic/NotoSansArabic-Regular.ttf" \
  -o "$FONTS_DIR/arabic/NotoSansArabic-Regular.ttf"

# Hebrew (he)
echo "  → Hebrew (Noto Sans Hebrew) - Bold + Regular"
curl -L "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSansHebrew/NotoSansHebrew-Bold.ttf" \
  -o "$FONTS_DIR/hebrew/NotoSansHebrew-Bold.ttf"
curl -L "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSansHebrew/NotoSansHebrew-Regular.ttf" \
  -o "$FONTS_DIR/hebrew/NotoSansHebrew-Regular.ttf"

# Greek (el)
echo "  → Greek (Noto Sans) - symlinks to Latin"
# Noto Sans already includes Greek, just symlink both weights
ln -sf "../latin/NotoSans-Bold.ttf" "$FONTS_DIR/greek/NotoSans-Bold.ttf"
ln -sf "../latin/NotoSans-Regular.ttf" "$FONTS_DIR/greek/NotoSans-Regular.ttf"

# Chinese Simplified (zh-Hans)
echo "  → Chinese Simplified (Noto Sans SC) - Bold + Regular"
curl -L "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Bold.otf" \
  -o "$FONTS_DIR/chinese/NotoSansSC-Bold.otf"
curl -L "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/SimplifiedChinese/NotoSansCJKsc-Regular.otf" \
  -o "$FONTS_DIR/chinese/NotoSansSC-Regular.otf"

# Chinese Traditional (zh-Hant)
echo "  → Chinese Traditional (Noto Sans TC) - Bold + Regular"
curl -L "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/TraditionalChinese/NotoSansCJKtc-Bold.otf" \
  -o "$FONTS_DIR/chinese/NotoSansTC-Bold.otf"
curl -L "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/TraditionalChinese/NotoSansCJKtc-Regular.otf" \
  -o "$FONTS_DIR/chinese/NotoSansTC-Regular.otf"

# Japanese (ja)
echo "  → Japanese (Noto Sans JP) - Bold + Regular"
curl -L "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Bold.otf" \
  -o "$FONTS_DIR/japanese/NotoSansJP-Bold.otf"
curl -L "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Japanese/NotoSansCJKjp-Regular.otf" \
  -o "$FONTS_DIR/japanese/NotoSansJP-Regular.otf"

# Korean (ko)
echo "  → Korean (Noto Sans KR) - Bold + Regular"
curl -L "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Korean/NotoSansCJKkr-Bold.otf" \
  -o "$FONTS_DIR/korean/NotoSansKR-Bold.otf"
curl -L "https://github.com/notofonts/noto-cjk/raw/main/Sans/OTF/Korean/NotoSansCJKkr-Regular.otf" \
  -o "$FONTS_DIR/korean/NotoSansKR-Regular.otf"

# Thai (th)
echo "  → Thai (Noto Sans Thai) - Bold + Regular"
curl -L "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSansThai/NotoSansThai-Bold.ttf" \
  -o "$FONTS_DIR/thai/NotoSansThai-Bold.ttf"
curl -L "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSansThai/NotoSansThai-Regular.ttf" \
  -o "$FONTS_DIR/thai/NotoSansThai-Regular.ttf"

# Devanagari - Hindi (hi)
echo "  → Devanagari/Hindi (Noto Sans Devanagari) - Bold + Regular"
curl -L "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Bold.ttf" \
  -o "$FONTS_DIR/devanagari/NotoSansDevanagari-Bold.ttf"
curl -L "https://github.com/notofonts/noto-fonts/raw/main/hinted/ttf/NotoSansDevanagari/NotoSansDevanagari-Regular.ttf" \
  -o "$FONTS_DIR/devanagari/NotoSansDevanagari-Regular.ttf"

echo "✅ All fonts downloaded successfully!"
echo ""
echo "Font sizes:"
du -sh "$FONTS_DIR"/*/*.{ttf,otf} 2>/dev/null | sort -h

echo ""
echo "Total: $(find "$FONTS_DIR" -name '*.ttf' -o -name '*.otf' | wc -l | tr -d ' ') font files"
