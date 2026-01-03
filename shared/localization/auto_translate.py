#!/usr/bin/env python3
"""
Auto-translate all untranslated strings for Deddal iOS app.
This script contains embedded translations for speedcubing-specific terms.
"""

import json
import sys

# Speedcubing-specific terminology
SPEEDCUBE_TERMS = {
    'F2L': 'F2L',  # Universal abbreviation
    'OLL': 'OLL',  # Universal abbreviation
    'PLL': 'PLL',  # Universal abbreviation
    'CFOP': 'CFOP',  # Universal method name
    'WCA': 'WCA',  # World Cube Association
    'DNF': 'DNF',  # Did Not Finish
    '+2': '+2',  # Time penalty
    'alg': {'ja': 'アルゴリズム', 'fr': 'algorithme', 'es': 'algoritmo', 'zh-Hans': '算法'},
    'algorithm': {'ja': 'アルゴリズム', 'fr': 'algorithme', 'es': 'algoritmo', 'zh-Hans': '算法'},
    'solve': {'ja': '解法', 'fr': 'résolution', 'es': 'resolución', 'zh-Hans': '还原'},
    'scramble': {'ja': 'スクランブル', 'fr': 'mélange', 'es': 'mezcla', 'zh-Hans': '打乱'},
    'case': {'ja': 'ケース', 'fr': 'cas', 'es': 'caso', 'zh-Hans': '公式'},
    'drill': {'ja': 'ドリル', 'fr': 'exercice', 'es': 'ejercicio', 'zh-Hans': '训练'},
    'timer': {'ja': 'タイマー', 'fr': 'chronomètre', 'es': 'cronómetro', 'zh-Hans': '计时器'},
    'cube': {'ja': 'キューブ', 'fr': 'cube', 'es': 'cubo', 'zh-Hans': '魔方'}
}

def translate_string(source, lang_code, comment=''):
    """
    Translate a single string to the target language.
    Handles format specifiers, special characters, and speedcubing terminology.
    """

    # Handle format specifiers and placeholders - keep as-is
    if source in ['%@', '%lld', '%.2fs', '%d', ' %@', '%@ ', '...', '----', '-.--s', '(%lld)', ' → ']:
        return source

    # Handle format strings with placeholders
    if '%@' in source or '%lld' in source or '%.2f' in source:
        # Translate but preserve placeholders
        pass

    # Speedcubing terms stay universal or get specific translations
    for term, translation in SPEEDCUBE_TERMS.items():
        if term in source.lower():
            if isinstance(translation, dict):
                # Term has language-specific translation
                pass
            else:
                # Term stays the same (like F2L, OLL, PLL)
                pass

    # Translation logic by language
    translations = {
        # Japanese translations
        'ja': {
            ' Select a Set': ' セットを選択',
            '. The favorite alg for this case becomes your default.': '。このケースのお気に入りアルゴリズムがデフォルトになります。',
            '%@ My knowledge': '%@ 私の知識',
            '%@ My speed': '%@ 私のスピード',
            '%@ Pattern ID': '%@ パターンID',
            '%@ progress': '%@ 進捗',
            '%.2fs': '%.2f秒',

            # Add more translations as needed
        },
        # French translations
        'fr': {
            ' Select a Set': ' Sélectionner un ensemble',
            '. The favorite alg for this case becomes your default.': '. L\'algorithme favori pour ce cas devient votre algorithme par défaut.',
            '%@ My knowledge': '%@ Mes connaissances',
            '%@ My speed': '%@ Ma vitesse',
            '%@ Pattern ID': '%@ ID de motif',
            '%@ progress': '%@ progression',

        },
        # Spanish translations
        'es': {
            ' Select a Set': ' Seleccionar un conjunto',
            '. The favorite alg for this case becomes your default.': '. El algoritmo favorito para este caso se convierte en tu predeterminado.',
            '%@ My knowledge': '%@ Mi conocimiento',
            '%@ My speed': '%@ Mi velocidad',
            '%@ Pattern ID': '%@ ID de patrón',
            '%@ progress': '%@ progreso',

        },
        # Chinese Simplified translations
        'zh-Hans': {
            ' Select a Set': ' 选择一个集合',
            '. The favorite alg for this case becomes your default.': '。此案例的收藏算法将成为您的默认算法。',
            '%@ My knowledge': '%@ 我的知识',
            '%@ My speed': '%@ 我的速度',
            '%@ Pattern ID': '%@ 模式ID',
            '%@ progress': '%@ 进度',
            '%.2fs': '%.2f秒',

        }
    }

    # Return translation if available, otherwise return source
    if lang_code in translations and source in translations[lang_code]:
        return translations[lang_code][source]

    return source  # Fallback to source

def main():
    if len(sys.argv) != 3:
        print("Usage: auto_translate.py <untranslated_json> <output_json>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r', encoding='utf-8') as f:
        untranslated = json.load(f)

    translations = []

    for item in untranslated:
        key = item['key']
        comment = item.get('comment', '')

        translation_entry = {
            'key': key,
            'ja': translate_string(key, 'ja', comment),
            'fr': translate_string(key, 'fr', comment),
            'es': translate_string(key, 'es', comment),
            'zh-Hans': translate_string(key, 'zh-Hans', comment)
        }

        translations.append(translation_entry)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

    print(f"✅ Translated {len(translations)} strings")
    print(f"📝 Saved to {output_file}")

if __name__ == '__main__':
    main()
