#!/usr/bin/env python3
"""
Update all locale release_notes.txt files with minimal generic content.
Strategy: Don't give competitive intelligence, users don't read them anyway.
"""

from pathlib import Path

# Minimal release notes for each locale
RELEASE_NOTES = {
    "en-US": """We're constantly improving Deddal. This update includes performance enhancements and bug fixes.

Got feedback? contact@deddal.app""",

    "en-AU": """We're constantly improving Deddal. This update includes performance enhancements and bug fixes.

Got feedback? contact@deddal.app""",

    "en-CA": """We're constantly improving Deddal. This update includes performance enhancements and bug fixes.

Got feedback? contact@deddal.app""",

    "en-GB": """We're constantly improving Deddal. This update includes performance enhancements and bug fixes.

Got feedback? contact@deddal.app""",

    "fr-FR": """Nous améliorons constamment Deddal. Cette mise à jour inclut des améliorations de performance et des corrections de bugs.

Des retours ? contact@deddal.app""",

    "fr-CA": """Nous améliorons constamment Deddal. Cette mise à jour inclut des améliorations de performance et des corrections de bugs.

Des retours ? contact@deddal.app""",

    "es-ES": """Estamos mejorando constantemente Deddal. Esta actualización incluye mejoras de rendimiento y correcciones de errores.

¿Comentarios? contact@deddal.app""",

    "es-MX": """Estamos mejorando constantemente Deddal. Esta actualización incluye mejoras de rendimiento y correcciones de errores.

¿Comentarios? contact@deddal.app""",

    "ja": """Deddal を継続的に改善しています。このアップデートにはパフォーマンスの向上とバグ修正が含まれています。

フィードバックは contact@deddal.app まで""",

    "zh-Hans": """我们不断改进 Deddal。此更新包括性能增强和错误修复。

有反馈吗？contact@deddal.app""",

    "zh-Hant": """我們不斷改進 Deddal。此更新包括性能增強和錯誤修復。

有反饋嗎？contact@deddal.app""",

    "de-DE": """Wir verbessern Deddal ständig. Dieses Update enthält Leistungsverbesserungen und Fehlerbehebungen.

Feedback? contact@deddal.app""",

    "it": """Stiamo costantemente migliorando Deddal. Questo aggiornamento include miglioramenti delle prestazioni e correzioni di bug.

Feedback? contact@deddal.app""",

    "pt-BR": """Estamos constantemente melhorando o Deddal. Esta atualização inclui melhorias de desempenho e correções de bugs.

Tem feedback? contact@deddal.app""",

    "pt-PT": """Estamos constantemente a melhorar o Deddal. Esta atualização inclui melhorias de desempenho e correções de erros.

Tem feedback? contact@deddal.app""",

    "ko": """Deddal을 지속적으로 개선하고 있습니다. 이 업데이트에는 성능 향상 및 버그 수정이 포함되어 있습니다.

피드백이 있으신가요? contact@deddal.app""",

    "ru": """Мы постоянно улучшаем Deddal. Это обновление включает улучшения производительности и исправления ошибок.

Есть отзывы? contact@deddal.app""",

    "ar-SA": """نحن نعمل باستمرار على تحسين Deddal. يتضمن هذا التحديث تحسينات في الأداء وإصلاحات للأخطاء.

لديك ملاحظات؟ contact@deddal.app""",

    "ca": """Estem millorant constantment Deddal. Aquesta actualització inclou millores de rendiment i correccions d'errors.

Comentaris? contact@deddal.app""",

    "cs": """Neustále vylepšujeme Deddal. Tato aktualizace zahrnuje vylepšení výkonu a opravy chyb.

Máte zpětnou vazbu? contact@deddal.app""",

    "da": """Vi forbedrer konstant Deddal. Denne opdatering inkluderer ydeevneforbedringer og fejlrettelser.

Har du feedback? contact@deddal.app""",

    "el": """Βελτιώνουμε συνεχώς το Deddal. Αυτή η ενημέρωση περιλαμβάνει βελτιώσεις απόδοσης και διορθώσεις σφαλμάτων.

Έχετε σχόλια; contact@deddal.app""",

    "fi": """Parannamme jatkuvasti Deddalia. Tämä päivitys sisältää suorituskyvyn parannuksia ja virheiden korjauksia.

Palautetta? contact@deddal.app""",

    "he": """אנחנו משפרים את Deddal באופן מתמיד. עדכון זה כולל שיפורי ביצועים ותיקוני באגים.

יש משוב? contact@deddal.app""",

    "hi": """हम Deddal में लगातार सुधार कर रहे हैं। इस अपडेट में प्रदर्शन में सुधार और बग फिक्स शामिल हैं।

फीडबैक? contact@deddal.app""",

    "hr": """Neprestano poboljšavamo Deddal. Ovo ažuriranje uključuje poboljšanja performansi i ispravke grešaka.

Imate povratne informacije? contact@deddal.app""",

    "hu": """Folyamatosan fejlesztjük a Deddalt. Ez a frissítés teljesítménybeli fejlesztéseket és hibajavításokat tartalmaz.

Van visszajelzésed? contact@deddal.app""",

    "id": """Kami terus meningkatkan Deddal. Pembaruan ini mencakup peningkatan kinerja dan perbaikan bug.

Punya masukan? contact@deddal.app""",

    "ms": """Kami sentiasa menambah baik Deddal. Kemas kini ini termasuk peningkatan prestasi dan pembetulan pepijat.

Ada maklum balas? contact@deddal.app""",

    "nl-NL": """We verbeteren Deddal voortdurend. Deze update bevat prestatieverbeteringen en bugfixes.

Feedback? contact@deddal.app""",

    "no": """Vi forbedrer Deddal kontinuerlig. Denne oppdateringen inkluderer ytelsesforbedringer og feilrettinger.

Har du tilbakemelding? contact@deddal.app""",

    "pl": """Nieustannie ulepszamy Deddal. Ta aktualizacja obejmuje usprawnienia wydajności i poprawki błędów.

Masz opinię? contact@deddal.app""",

    "ro": """Îmbunătățim constant Deddal. Această actualizare include îmbunătățiri de performanță și remedieri de erori.

Ai feedback? contact@deddal.app""",

    "sk": """Neustále vylepšujeme Deddal. Táto aktualizácia zahŕňa vylepšenia výkonu a opravy chýb.

Máte spätnú väzbu? contact@deddal.app""",

    "sv": """Vi förbättrar ständigt Deddal. Den här uppdateringen inkluderar prestandaförbättringar och buggfixar.

Har du feedback? contact@deddal.app""",

    "th": """เรากำลังปรับปรุง Deddal อย่างต่อเนื่อง การอัปเดตนี้รวมถึงการปรับปรุงประสิทธิภาพและการแก้ไขบั๊ก

มีข้อเสนอแนะไหม? contact@deddal.app""",

    "tr": """Deddal'ı sürekli geliştiriyoruz. Bu güncelleme performans iyileştirmeleri ve hata düzeltmeleri içerir.

Geri bildiriminiz var mı? contact@deddal.app""",

    "uk": """Ми постійно покращуємо Deddal. Це оновлення включає покращення продуктивності та виправлення помилок.

Є відгуки? contact@deddal.app""",

    "vi": """Chúng tôi liên tục cải thiện Deddal. Bản cập nhật này bao gồm các cải tiến hiệu suất và sửa lỗi.

Có phản hồi? contact@deddal.app""",
}

def main():
    metadata_dir = Path(__file__).parent
    updated_count = 0
    skipped_count = 0

    for locale, content in RELEASE_NOTES.items():
        notes_file = metadata_dir / locale / "release_notes.txt"

        if not notes_file.parent.exists():
            print(f"⚠️  Skipping {locale}: directory not found")
            skipped_count += 1
            continue

        # Write minimal release notes
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(content)

        updated_count += 1
        char_count = len(content)
        print(f"✅ Updated {locale}/release_notes.txt ({char_count} chars)")

    print(f"\n🎉 Complete: {updated_count} updated, {skipped_count} skipped")
    print("\nAll release notes now minimal and generic")
    print("✅ No competitive intelligence leaked")
    print("✅ Professional and simple")
    print("✅ Includes feedback email")

if __name__ == "__main__":
    main()
