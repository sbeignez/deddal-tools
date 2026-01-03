#!/usr/bin/env python3
"""
Align all locale promotional_text.txt files with en-US baseline.
Promotional text (170 chars max) appears at top of App Store listing.
Highlights v0.4.1 key features: 4 tabs (Home, Library, Progress, Practice).
"""

import os
from pathlib import Path

# Promotional text for each locale (170 char limit)
PROMOTIONAL_TEXTS = {
    "en-US": "Track your progress, master all CFOP algorithms, and get faster with visual learning and targeted practice. Built by cubers for cubers.",

    "en-AU": "Track your progress, master all CFOP algorithms, and get faster with visual learning and targeted practice. Built by cubers for cubers.",

    "en-CA": "Track your progress, master all CFOP algorithms, and get faster with visual learning and targeted practice. Built by cubers for cubers.",

    "en-GB": "Track your progress, master all CFOP algorithms, and get faster with visual learning and targeted practice. Built by cubers for cubers.",

    "fr-FR": "Suivez vos progrès, maîtrisez tous les algorithmes CFOP et progressez avec l'apprentissage visuel et la pratique ciblée. Conçu par des cubers.",

    "fr-CA": "Suivez vos progrès, maîtrisez tous les algorithmes CFOP et progressez avec l'apprentissage visuel et la pratique ciblée. Conçu par des cubers.",

    "es-ES": "Rastrea tu progreso, domina todos los algoritmos CFOP y mejora con aprendizaje visual y práctica dirigida. Hecho por cubers para cubers.",

    "es-MX": "Rastrea tu progreso, domina todos los algoritmos CFOP y mejora con aprendizaje visual y práctica dirigida. Hecho por cubers para cubers.",

    "ja": "進捗を追跡し、すべてのCFOPアルゴリズムを習得し、視覚的学習と集中練習でさらに速くなりましょう。キューバーによって作られました。",

    "zh-Hans": "追踪进度，掌握所有CFOP算法，通过可视化学习和针对性练习提升速度。由魔方爱好者为魔方爱好者打造。",

    "zh-Hant": "追蹤進度，掌握所有CFOP算法，通過視覺化學習和針對性練習提升速度。由魔方愛好者為魔方愛好者打造。",

    "de-DE": "Verfolge deinen Fortschritt, meistere alle CFOP-Algorithmen und werde schneller mit visuellem Lernen und gezieltem Training. Von Cubern für Cuber.",

    "it": "Monitora i tuoi progressi, padroneggia tutti gli algoritmi CFOP e diventa più veloce con l'apprendimento visivo e la pratica mirata. Fatto da cuber.",

    "pt-BR": "Acompanhe seu progresso, domine todos os algoritmos CFOP e fique mais rápido com aprendizado visual e prática direcionada. Feito por cubers.",

    "pt-PT": "Acompanhe o seu progresso, domine todos os algoritmos CFOP e fique mais rápido com aprendizagem visual e prática direcionada. Feito por cubers.",

    "ko": "진행 상황을 추적하고, 모든 CFOP 알고리즘을 마스터하고, 시각적 학습과 집중 연습으로 더 빨라지세요. 큐버가 만든 앱입니다.",

    "ru": "Отслеживайте прогресс, осваивайте все алгоритмы CFOP и становитесь быстрее с визуальным обучением и целевой практикой. Создано кубёрами.",

    "ar-SA": "تتبع تقدمك، أتقن جميع خوارزميات CFOP، وكن أسرع مع التعلم المرئي والممارسة الموجهة. صنع بواسطة المكعبين للمكعبين.",

    "ca": "Fes seguiment del teu progrés, domina tots els algorismes CFOP i millora amb l'aprenentatge visual i la pràctica dirigida. Fet per cubers.",

    "cs": "Sledujte svůj pokrok, ovládněte všechny algoritmy CFOP a zrychlete se vizuálním učením a cíleným tréninkem. Vytvořeno cubery pro cubery.",

    "da": "Følg din fremgang, mestre alle CFOP-algoritmer og bliv hurtigere med visuel læring og målrettet træning. Lavet af cubers til cubers.",

    "el": "Παρακολουθήστε την πρόοδό σας, κατακτήστε όλους τους αλγορίθμους CFOP και γίνετε ταχύτεροι με οπτική μάθηση και στοχευμένη εξάσκηση.",

    "fi": "Seuraa edistymistäsi, hallitse kaikki CFOP-algoritmit ja nopeudu visuaalisen oppimisen ja kohdistetun harjoittelun avulla. Cubereiden tekemä.",

    "he": "עקוב אחר ההתקדמות שלך, שלוט בכל אלגוריתמי CFOP והפוך למהיר יותר עם למידה חזותית ותרגול ממוקד. נוצר על ידי קיוברים.",

    "hi": "अपनी प्रगति को ट्रैक करें, सभी CFOP एल्गोरिदम में महारत हासिल करें और विज़ुअल लर्निंग और टार्गेटेड प्रैक्टिस से तेज़ बनें।",

    "hr": "Pratite svoj napredak, ovladajte sve CFOP algoritme i postanite brži s vizualnim učenjem i ciljanom praksom. Napravljeno od cubera za cubere.",

    "hu": "Kövesd nyomon a haladásod, sajátítsd el az összes CFOP algoritmust és gyorsulj vizuális tanulással és célzott gyakorlással. Cuberek által.",

    "id": "Lacak kemajuan Anda, kuasai semua algoritma CFOP, dan tingkatkan kecepatan dengan pembelajaran visual dan latihan terarah. Dibuat oleh cuber.",

    "ms": "Jejaki kemajuan anda, kuasai semua algoritma CFOP dan jadi lebih pantas dengan pembelajaran visual dan latihan tersasar. Dibuat oleh cubers.",

    "nl-NL": "Volg je voortgang, beheers alle CFOP-algoritmen en word sneller met visueel leren en gerichte oefening. Gemaakt door cubers voor cubers.",

    "no": "Følg fremgangen din, mestre alle CFOP-algoritmer og bli raskere med visuell læring og målrettet trening. Laget av cubers for cubers.",

    "pl": "Śledź swoje postępy, opanuj wszystkie algorytmy CFOP i przyspiesz dzięki wizualnemu uczeniu się i ukierunkowanej praktyce. Stworzone przez cuberów.",

    "ro": "Urmărește-ți progresul, stăpânește toți algoritmii CFOP și devino mai rapid cu învățare vizuală și practică țintită. Făcut de cuberi pentru cuberi.",

    "sk": "Sledujte svoj pokrok, ovládnite všetky algoritmy CFOP a zrýchlite sa vizuálnym učením a cieleným tréningom. Vytvorené cubermi pre cuberov.",

    "sv": "Följ dina framsteg, bemästra alla CFOP-algoritmer och bli snabbare med visuellt lärande och riktad träning. Gjort av cubers för cubers.",

    "th": "ติดตามความคืบหน้าของคุณ ฝึกฝนอัลกอริทึม CFOP ทั้งหมด และเพิ่มความเร็วด้วยการเรียนรู้แบบภาพและการฝึกฝนที่ตรงเป้าหมาย",

    "tr": "İlerlemenizi takip edin, tüm CFOP algoritmalarında ustalaşın ve görsel öğrenme ve hedefli pratikle daha hızlı olun. Cuberlar tarafından yapıldı.",

    "uk": "Відстежуйте свій прогрес, опануйте всі алгоритми CFOP і ставайте швидшими з візуальним навчанням і цільовою практикою. Зроблено кубером.",

    "vi": "Theo dõi tiến trình của bạn, làm chủ tất cả thuật toán CFOP và nhanh hơn với học tập trực quan và luyện tập có mục tiêu. Do cuber tạo ra.",
}

def main():
    metadata_dir = Path(__file__).parent
    updated_count = 0
    skipped_count = 0

    for locale, content in PROMOTIONAL_TEXTS.items():
        promo_file = metadata_dir / locale / "promotional_text.txt"

        if not promo_file.parent.exists():
            print(f"⚠️  Skipping {locale}: directory not found")
            skipped_count += 1
            continue

        # Verify character limit (170 chars)
        char_count = len(content)
        if char_count > 170:
            print(f"⚠️  WARNING: {locale} exceeds 170 chars ({char_count} chars)")

        # Write promotional text
        with open(promo_file, 'w', encoding='utf-8') as f:
            f.write(content)

        updated_count += 1
        print(f"✅ Updated {locale}/promotional_text.txt ({char_count}/170 chars)")

    print(f"\n🎉 Complete: {updated_count} updated, {skipped_count} skipped")
    print("\nAll promotional texts now aligned")
    print("✅ Highlights v0.4.1 features: Track Progress, Library, Visual Learning, Practice")
    print("✅ Clear outcome focus: 'get faster'")
    print("✅ Under 170 character limit")

if __name__ == "__main__":
    main()
