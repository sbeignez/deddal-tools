#!/usr/bin/env python3
"""
Align all locale release_notes.txt files with en-US baseline for v0.4.1.
Release notes (4000 chars max) highlight new features in this version.
v0.4.1 introduces 4 main sections: Home, Library, Progress, Practice.
"""

import os
from pathlib import Path

# Release notes for v0.4.1 - each locale
RELEASE_NOTES = {
    "en-US": """What's New in v0.4.1

🏠 NEW: Home Dashboard
• See your current skill level at a glance
• Track mastery across F2L, OLL, and PLL
• Get personalized insights on your progress

📚 ENHANCED: Algorithm Library
• Browse all CFOP cases (F2L, OLL, PLL)
• View multiple algorithm variations per case
• Quick access to visual demonstrations

📊 NEW: Progress Tracking
• Detailed analytics on your improvement
• Case-by-case mastery overview
• Track your learning journey over time

🎯 NEW: Practice Modes
• Targeted drilling for specific case sets
• Build pattern recognition speed
• Multiple training modes to match your goals

Built by cubers, for cubers. Got feedback? Let us know at contact@deddal.app

Keep Cubing! 🎲""",

    "en-AU": """What's New in v0.4.1

🏠 NEW: Home Dashboard
• See your current skill level at a glance
• Track mastery across F2L, OLL, and PLL
• Get personalised insights on your progress

📚 ENHANCED: Algorithm Library
• Browse all CFOP cases (F2L, OLL, PLL)
• View multiple algorithm variations per case
• Quick access to visual demonstrations

📊 NEW: Progress Tracking
• Detailed analytics on your improvement
• Case-by-case mastery overview
• Track your learning journey over time

🎯 NEW: Practice Modes
• Targeted drilling for specific case sets
• Build pattern recognition speed
• Multiple training modes to match your goals

Built by cubers, for cubers. Got feedback? Let us know at contact@deddal.app

Keep Cubing! 🎲""",

    "en-CA": """What's New in v0.4.1

🏠 NEW: Home Dashboard
• See your current skill level at a glance
• Track mastery across F2L, OLL, and PLL
• Get personalized insights on your progress

📚 ENHANCED: Algorithm Library
• Browse all CFOP cases (F2L, OLL, PLL)
• View multiple algorithm variations per case
• Quick access to visual demonstrations

📊 NEW: Progress Tracking
• Detailed analytics on your improvement
• Case-by-case mastery overview
• Track your learning journey over time

🎯 NEW: Practice Modes
• Targeted drilling for specific case sets
• Build pattern recognition speed
• Multiple training modes to match your goals

Built by cubers, for cubers. Got feedback? Let us know at contact@deddal.app

Keep Cubing! 🎲""",

    "en-GB": """What's New in v0.4.1

🏠 NEW: Home Dashboard
• See your current skill level at a glance
• Track mastery across F2L, OLL, and PLL
• Get personalised insights on your progress

📚 ENHANCED: Algorithm Library
• Browse all CFOP cases (F2L, OLL, PLL)
• View multiple algorithm variations per case
• Quick access to visual demonstrations

📊 NEW: Progress Tracking
• Detailed analytics on your improvement
• Case-by-case mastery overview
• Track your learning journey over time

🎯 NEW: Practice Modes
• Targeted drilling for specific case sets
• Build pattern recognition speed
• Multiple training modes to match your goals

Built by cubers, for cubers. Got feedback? Let us know at contact@deddal.app

Keep Cubing! 🎲""",

    "fr-FR": """Nouveautés de la v0.4.1

🏠 NOUVEAU : Tableau de bord d'accueil
• Voyez votre niveau de compétence actuel en un coup d'œil
• Suivez la maîtrise F2L, OLL et PLL
• Obtenez des informations personnalisées sur vos progrès

📚 AMÉLIORÉ : Bibliothèque d'algorithmes
• Parcourez tous les cas CFOP (F2L, OLL, PLL)
• Consultez plusieurs variations d'algorithmes par cas
• Accès rapide aux démonstrations visuelles

📊 NOUVEAU : Suivi des progrès
• Analyses détaillées de votre amélioration
• Vue d'ensemble de la maîtrise cas par cas
• Suivez votre parcours d'apprentissage au fil du temps

🎯 NOUVEAU : Modes de pratique
• Exercices ciblés pour des ensembles de cas spécifiques
• Développez la vitesse de reconnaissance des motifs
• Plusieurs modes d'entraînement adaptés à vos objectifs

Conçu par des cubers, pour des cubers. Des retours ? Contactez-nous à contact@deddal.app

Continuez à Cuber ! 🎲""",

    "fr-CA": """Nouveautés de la v0.4.1

🏠 NOUVEAU : Tableau de bord d'accueil
• Voyez votre niveau de compétence actuel en un coup d'œil
• Suivez la maîtrise F2L, OLL et PLL
• Obtenez des informations personnalisées sur vos progrès

📚 AMÉLIORÉ : Bibliothèque d'algorithmes
• Parcourez tous les cas CFOP (F2L, OLL, PLL)
• Consultez plusieurs variations d'algorithmes par cas
• Accès rapide aux démonstrations visuelles

📊 NOUVEAU : Suivi des progrès
• Analyses détaillées de votre amélioration
• Vue d'ensemble de la maîtrise cas par cas
• Suivez votre parcours d'apprentissage au fil du temps

🎯 NOUVEAU : Modes de pratique
• Exercices ciblés pour des ensembles de cas spécifiques
• Développez la vitesse de reconnaissance des motifs
• Plusieurs modes d'entraînement adaptés à vos objectifs

Conçu par des cubers, pour des cubers. Des retours ? Contactez-nous à contact@deddal.app

Continuez à Cuber ! 🎲""",

    "es-ES": """Novedades de v0.4.1

🏠 NUEVO: Panel de inicio
• Ve tu nivel de habilidad actual de un vistazo
• Rastrea el dominio en F2L, OLL y PLL
• Obtén información personalizada sobre tu progreso

📚 MEJORADO: Biblioteca de algoritmos
• Navega por todos los casos CFOP (F2L, OLL, PLL)
• Consulta múltiples variaciones de algoritmos por caso
• Acceso rápido a demostraciones visuales

📊 NUEVO: Seguimiento del progreso
• Análisis detallado de tu mejora
• Resumen del dominio caso por caso
• Sigue tu viaje de aprendizaje a lo largo del tiempo

🎯 NUEVO: Modos de práctica
• Ejercicios específicos para conjuntos de casos concretos
• Desarrolla velocidad de reconocimiento de patrones
• Múltiples modos de entrenamiento según tus objetivos

Hecho por cubers, para cubers. ¿Comentarios? Escríbenos a contact@deddal.app

¡Sigue Cubeando! 🎲""",

    "es-MX": """Novedades de v0.4.1

🏠 NUEVO: Panel de inicio
• Ve tu nivel de habilidad actual de un vistazo
• Rastrea el dominio en F2L, OLL y PLL
• Obtén información personalizada sobre tu progreso

📚 MEJORADO: Biblioteca de algoritmos
• Navega por todos los casos CFOP (F2L, OLL, PLL)
• Consulta múltiples variaciones de algoritmos por caso
• Acceso rápido a demostraciones visuales

📊 NUEVO: Seguimiento del progreso
• Análisis detallado de tu mejora
• Resumen del dominio caso por caso
• Sigue tu viaje de aprendizaje a lo largo del tiempo

🎯 NUEVO: Modos de práctica
• Ejercicios específicos para conjuntos de casos concretos
• Desarrolla velocidad de reconocimiento de patrones
• Múltiples modos de entrenamiento según tus objetivos

Hecho por cubers, para cubers. ¿Comentarios? Escríbenos a contact@deddal.app

¡Sigue Cubeando! 🎲""",

    "ja": """v0.4.1の新機能

🏠 新機能：ホームダッシュボード
• 現在のスキルレベルを一目で確認
• F2L、OLL、PLLの習得状況を追跡
• 進捗に関するパーソナライズされた洞察を取得

📚 強化：アルゴリズムライブラリ
• すべてのCFOPケース（F2L、OLL、PLL）を閲覧
• ケースごとに複数のアルゴリズムバリエーションを表示
• ビジュアルデモンストレーションへの素早いアクセス

📊 新機能：進捗追跡
• 改善に関する詳細な分析
• ケースごとの習得概要
• 時間経過に伴う学習の軌跡を追跡

🎯 新機能：練習モード
• 特定のケースセットのターゲット練習
• パターン認識速度の向上
• 目標に合わせた複数のトレーニングモード

キューバーによって、キューバーのために作られました。フィードバックは contact@deddal.app までお知らせください

Keep Cubing! 🎲""",

    "zh-Hans": """v0.4.1 新功能

🏠 新增：主页仪表板
• 一目了然地查看当前技能水平
• 跨F2L、OLL和PLL追踪掌握情况
• 获取关于进度的个性化见解

📚 增强：算法库
• 浏览所有CFOP案例（F2L、OLL、PLL）
• 查看每个案例的多种算法变体
• 快速访问可视化演示

📊 新增：进度追踪
• 关于您改进的详细分析
• 逐案例掌握概览
• 跟踪您随时间的学习旅程

🎯 新增：练习模式
• 针对特定案例集的定向训练
• 培养模式识别速度
• 多种训练模式匹配您的目标

由魔方爱好者为魔方爱好者打造。有反馈吗？请通过 contact@deddal.app 告诉我们

Keep Cubing! 🎲""",

    "zh-Hant": """v0.4.1 新功能

🏠 新增：主頁儀表板
• 一目了然地查看當前技能水平
• 跨F2L、OLL和PLL追蹤掌握情況
• 獲取關於進度的個性化見解

📚 增強：算法庫
• 瀏覽所有CFOP案例（F2L、OLL、PLL）
• 查看每個案例的多種算法變體
• 快速訪問可視化演示

📊 新增：進度追蹤
• 關於您改進的詳細分析
• 逐案例掌握概覽
• 跟踪您隨時間的學習旅程

🎯 新增：練習模式
• 針對特定案例集的定向訓練
• 培養模式識別速度
• 多種訓練模式匹配您的目標

由魔方愛好者為魔方愛好者打造。有反饋嗎？請通過 contact@deddal.app 告訴我們

Keep Cubing! 🎲""",

    "de-DE": """Neu in v0.4.1

🏠 NEU: Startseiten-Dashboard
• Sehen Sie Ihr aktuelles Fähigkeitsniveau auf einen Blick
• Verfolgen Sie die Beherrschung über F2L, OLL und PLL
• Erhalten Sie personalisierte Einblicke in Ihren Fortschritt

📚 VERBESSERT: Algorithmusbibliothek
• Durchsuchen Sie alle CFOP-Fälle (F2L, OLL, PLL)
• Sehen Sie mehrere Algorithmusvariationen pro Fall
• Schneller Zugriff auf visuelle Demonstrationen

📊 NEU: Fortschrittsverfolgung
• Detaillierte Analyse Ihrer Verbesserung
• Überblick über die Beherrschung von Fall zu Fall
• Verfolgen Sie Ihre Lernreise im Laufe der Zeit

🎯 NEU: Übungsmodi
• Gezieltes Training für bestimmte Fallsets
• Steigern Sie die Geschwindigkeit der Mustererkennung
• Mehrere Trainingsmodi passend zu Ihren Zielen

Von Cubern für Cuber gemacht. Feedback? Schreiben Sie uns an contact@deddal.app

Keep Cubing! 🎲""",

    "it": """Novità nella v0.4.1

🏠 NUOVO: Dashboard Home
• Vedi il tuo livello di abilità attuale a colpo d'occhio
• Monitora la padronanza su F2L, OLL e PLL
• Ottieni approfondimenti personalizzati sui tuoi progressi

📚 MIGLIORATO: Libreria di algoritmi
• Sfoglia tutti i casi CFOP (F2L, OLL, PLL)
• Visualizza più variazioni di algoritmi per caso
• Accesso rapido alle dimostrazioni visive

📊 NUOVO: Monitoraggio progressi
• Analisi dettagliate sul tuo miglioramento
• Panoramica della padronanza caso per caso
• Traccia il tuo percorso di apprendimento nel tempo

🎯 NUOVO: Modalità di pratica
• Allenamento mirato per set di casi specifici
• Sviluppa la velocità di riconoscimento dei pattern
• Diverse modalità di allenamento per i tuoi obiettivi

Fatto da cuber per cuber. Feedback? Contattaci a contact@deddal.app

Keep Cubing! 🎲""",

    "pt-BR": """Novidades na v0.4.1

🏠 NOVO: Painel Inicial
• Veja seu nível de habilidade atual de relance
• Acompanhe o domínio em F2L, OLL e PLL
• Obtenha insights personalizados sobre seu progresso

📚 MELHORADO: Biblioteca de Algoritmos
• Navegue por todos os casos CFOP (F2L, OLL, PLL)
• Visualize múltiplas variações de algoritmos por caso
• Acesso rápido a demonstrações visuais

📊 NOVO: Acompanhamento de Progresso
• Análises detalhadas da sua melhora
• Visão geral do domínio caso a caso
• Acompanhe sua jornada de aprendizado ao longo do tempo

🎯 NOVO: Modos de Prática
• Exercícios direcionados para conjuntos de casos específicos
• Desenvolva velocidade de reconhecimento de padrões
• Múltiplos modos de treinamento para seus objetivos

Feito por cubers, para cubers. Tem feedback? Entre em contato em contact@deddal.app

Keep Cubing! 🎲""",

    "pt-PT": """Novidades na v0.4.1

🏠 NOVO: Painel Inicial
• Veja o seu nível de habilidade atual de relance
• Acompanhe o domínio em F2L, OLL e PLL
• Obtenha insights personalizados sobre o seu progresso

📚 MELHORADO: Biblioteca de Algoritmos
• Navegue por todos os casos CFOP (F2L, OLL, PLL)
• Visualize múltiplas variações de algoritmos por caso
• Acesso rápido a demonstrações visuais

📊 NOVO: Acompanhamento de Progresso
• Análises detalhadas da sua melhoria
• Visão geral do domínio caso a caso
• Acompanhe a sua jornada de aprendizagem ao longo do tempo

🎯 NOVO: Modos de Prática
• Exercícios direcionados para conjuntos de casos específicos
• Desenvolva velocidade de reconhecimento de padrões
• Múltiplos modos de treino para os seus objetivos

Feito por cubers, para cubers. Tem feedback? Entre em contacto em contact@deddal.app

Keep Cubing! 🎲""",

    "ko": """v0.4.1의 새로운 기능

🏠 새로운 기능: 홈 대시보드
• 현재 기술 수준을 한눈에 확인
• F2L, OLL, PLL 전체의 숙련도 추적
• 진행 상황에 대한 맞춤형 인사이트 얻기

📚 개선됨: 알고리즘 라이브러리
• 모든 CFOP 케이스 탐색 (F2L, OLL, PLL)
• 케이스당 여러 알고리즘 변형 보기
• 시각적 데모에 빠르게 액세스

📊 새로운 기능: 진행 상황 추적
• 개선 사항에 대한 상세한 분석
• 케이스별 숙련도 개요
• 시간 경과에 따른 학습 여정 추적

🎯 새로운 기능: 연습 모드
• 특정 케이스 세트에 대한 집중 훈련
• 패턴 인식 속도 향상
• 목표에 맞는 여러 훈련 모드

큐버가 만든 큐버를 위한 앱. 피드백이 있으신가요? contact@deddal.app로 알려주세요

Keep Cubing! 🎲""",

    "ru": """Что нового в v0.4.1

🏠 НОВОЕ: Панель главной страницы
• Смотрите свой текущий уровень навыков с первого взгляда
• Отслеживайте мастерство в F2L, OLL и PLL
• Получайте персонализированную информацию о прогрессе

📚 УЛУЧШЕНО: Библиотека алгоритмов
• Просматривайте все случаи CFOP (F2L, OLL, PLL)
• Смотрите несколько вариантов алгоритмов для каждого случая
• Быстрый доступ к визуальным демонстрациям

📊 НОВОЕ: Отслеживание прогресса
• Детальная аналитика вашего улучшения
• Обзор мастерства по каждому случаю
• Отслеживайте ваш путь обучения со временем

🎯 НОВОЕ: Режимы практики
• Целевая тренировка для конкретных наборов случаев
• Развивайте скорость распознавания паттернов
• Несколько режимов тренировки под ваши цели

Создано кубёрами для кубёров. Есть отзывы? Напишите нам на contact@deddal.app

Keep Cubing! 🎲""",

    "ar-SA": """الجديد في الإصدار 0.4.1

🏠 جديد: لوحة معلومات الصفحة الرئيسية
• شاهد مستوى مهاراتك الحالي في لمحة
• تتبع الإتقان عبر F2L و OLL و PLL
• احصل على رؤى شخصية حول تقدمك

📚 محسّن: مكتبة الخوارزميات
• تصفح جميع حالات CFOP (F2L، OLL، PLL)
• عرض أشكال متعددة من الخوارزميات لكل حالة
• وصول سريع إلى العروض التوضيحية المرئية

📊 جديد: تتبع التقدم
• تحليلات تفصيلية لتحسنك
• نظرة عامة على الإتقان حالة بحالة
• تتبع رحلة التعلم الخاصة بك بمرور الوقت

🎯 جديد: أوضاع التمرين
• تدريب موجه لمجموعات حالات محددة
• بناء سرعة التعرف على الأنماط
• أوضاع تدريب متعددة لتتناسب مع أهدافك

صُنع بواسطة المكعبين للمكعبين. لديك ملاحظات؟ اتصل بنا على contact@deddal.app

استمر في التكعيب! 🎲""",

    "ca": """Novetats de la v0.4.1

🏠 NOU: Tauler d'inici
• Veu el teu nivell d'habilitat actual d'una ullada
• Segueix el domini a F2L, OLL i PLL
• Obté informació personalitzada sobre el teu progrés

📚 MILLORAT: Biblioteca d'algorismes
• Navega per tots els casos CFOP (F2L, OLL, PLL)
• Consulta múltiples variacions d'algorismes per cas
• Accés ràpid a demostracions visuals

📊 NOU: Seguiment del progrés
• Anàlisi detallada de la teva millora
• Resum del domini cas per cas
• Segueix el teu viatge d'aprenentatge al llarg del temps

🎯 NOU: Modes de pràctica
• Exercicis específics per a conjunts de casos concrets
• Desenvolupa velocitat de reconeixement de patrons
• Múltiples modes d'entrenament segons els teus objectius

Fet per cubers, per a cubers. Comentaris? Escriu-nos a contact@deddal.app

Continua Cubejant! 🎲""",

    "cs": """Co je nového ve v0.4.1

🏠 NOVÉ: Domovský dashboard
• Sledujte svou aktuální úroveň dovedností na první pohled
• Sledujte zvládnutí F2L, OLL a PLL
• Získejte personalizované poznatky o svém pokroku

📚 VYLEPŠENO: Knihovna algoritmů
• Procházejte všechny případy CFOP (F2L, OLL, PLL)
• Zobrazujte více variací algoritmů na případ
• Rychlý přístup k vizuálním ukázkám

📊 NOVÉ: Sledování pokroku
• Podrobné analýzy vašeho zlepšení
• Přehled zvládnutí případ od případu
• Sledujte svou cestu učení v čase

🎯 NOVÉ: Režimy cvičení
• Cílené cvičení pro konkrétní sady případů
• Vytvářejte rychlost rozpoznávání vzorů
• Více tréningových režimů podle vašich cílů

Vytvořeno cubery pro cubery. Máte zpětnou vazbu? Dejte nám vědět na contact@deddal.app

Keep Cubing! 🎲""",

    "da": """Nyt i v0.4.1

🏠 NYT: Hjem-dashboard
• Se dit aktuelle færdighedsniveau med et blik
• Følg beherskelse på tværs af F2L, OLL og PLL
• Få personlige indsigter i din fremgang

📚 FORBEDRET: Algoritmebibliotek
• Gennemse alle CFOP-tilfælde (F2L, OLL, PLL)
• Se flere algoritme-variationer per tilfælde
• Hurtig adgang til visuelle demonstrationer

📊 NYT: Fremgangssporing
• Detaljerede analyser af din forbedring
• Oversigt over beherskelse tilfælde for tilfælde
• Følg din læringsrejse over tid

🎯 NYT: Øvelsestilstande
• Målrettet træning for specifikke tilfældessæt
• Byg mønstergenkendelseshastighed
• Flere træningstilstande til dine mål

Lavet af cubers til cubers. Har du feedback? Lad os vide det på contact@deddal.app

Keep Cubing! 🎲""",

    "el": """Τι νέο υπάρχει στην έκδοση v0.4.1

🏠 ΝΕΟ: Πίνακας αρχικής σελίδας
• Δείτε το τρέχον επίπεδο δεξιοτήτων σας με μια ματιά
• Παρακολουθήστε την κατάκτηση σε F2L, OLL και PLL
• Λάβετε εξατομικευμένες πληροφορίες για την πρόοδό σας

📚 ΒΕΛΤΙΩΜΕΝΟ: Βιβλιοθήκη αλγορίθμων
• Περιηγηθείτε σε όλες τις περιπτώσεις CFOP (F2L, OLL, PLL)
• Δείτε πολλαπλές παραλλαγές αλγορίθμων ανά περίπτωση
• Γρήγορη πρόσβαση σε οπτικές επιδείξεις

📊 ΝΕΟ: Παρακολούθηση προόδου
• Λεπτομερείς αναλύσεις της βελτίωσής σας
• Επισκόπηση κατάκτησης ανά περίπτωση
• Παρακολουθήστε το ταξίδι εκμάθησής σας με την πάροδο του χρόνου

🎯 ΝΕΟ: Λειτουργίες εξάσκησης
• Στοχευμένη εξάσκηση για συγκεκριμένα σύνολα περιπτώσεων
• Αναπτύξτε ταχύτητα αναγνώρισης μοτίβων
• Πολλαπλοί τρόποι εκπαίδευσης για τους στόχους σας

Φτιαγμένο από cubers για cubers. Έχετε σχόλια; Ενημερώστε μας στο contact@deddal.app

Keep Cubing! 🎲""",

    "fi": """Uutta versiossa v0.4.1

🏠 UUSI: Kotinäyttö
• Näe nykyinen taitotasosi yhdellä silmäyksellä
• Seuraa hallintaa F2L:n, OLL:n ja PLL:n osalta
• Saa henkilökohtaisia näkemyksiä edistymisestäsi

📚 PARANNETTU: Algoritmikirjasto
• Selaa kaikkia CFOP-tapauksia (F2L, OLL, PLL)
• Katso useita algoritmivariaatioita tapausta kohti
• Nopea pääsy visuaalisiin esittelyihin

📊 UUSI: Edistymisen seuranta
• Yksityiskohtaiset analyysit parantumisestasi
• Hallinta-yleiskatsaus tapaus tapaukselta
• Seuraa oppimismatkaasi ajan myötä

🎯 UUSI: Harjoittelutilat
• Kohdistettu harjoittelu tietyille tapauskokoonpanoille
• Rakenna kuvionhavaitsemisnopeutta
• Useita harjoittelutiloja tavoitteisiisi

Cubereiden tekemä cuberille. Palautetta? Kerro meille osoitteessa contact@deddal.app

Keep Cubing! 🎲""",

    "he": """מה חדש ב-v0.4.1

🏠 חדש: לוח בית
• ראה את רמת המיומנות הנוכחית שלך במבט אחד
• עקוב אחר שליטה ב-F2L, OLL ו-PLL
• קבל תובנות מותאמות אישית על ההתקדמות שלך

📚 משופר: ספריית אלגוריתמים
• עיין בכל המקרים של CFOP (F2L, OLL, PLL)
• צפה במספר וריאציות אלגוריתם למקרה
• גישה מהירה להדגמות ויזואליות

📊 חדש: מעקב התקדמות
• ניתוחים מפורטים של השיפור שלך
• סקירת שליטה ממקרה למקרה
• עקוב אחר מסע הלמידה שלך לאורך זמן

🎯 חדש: מצבי תרגול
• תרגול ממוקד עבור ערכות מקרים ספציפיות
• בנה מהירות זיהוי דפוסים
• מספר מצבי אימון בהתאם למטרות שלך

נוצר על ידי קיוברים עבור קיוברים. יש משוב? הודע לנו ב-contact@deddal.app

המשך לקובב! 🎲""",

    "hi": """v0.4.1 में नया क्या है

🏠 नया: होम डैशबोर्ड
• अपने वर्तमान कौशल स्तर को एक नज़र में देखें
• F2L, OLL, और PLL में महारत को ट्रैक करें
• अपनी प्रगति पर व्यक्तिगत अंतर्दृष्टि प्राप्त करें

📚 बेहतर: एल्गोरिदम लाइब्रेरी
• सभी CFOP केस ब्राउज़ करें (F2L, OLL, PLL)
• प्रति केस कई एल्गोरिदम विविधताएं देखें
• विज़ुअल प्रदर्शनों तक त्वरित पहुंच

📊 नया: प्रगति ट्रैकिंग
• आपके सुधार पर विस्तृत विश्लेषण
• केस-बाय-केस महारत का अवलोकन
• समय के साथ अपनी सीखने की यात्रा को ट्रैक करें

🎯 नया: प्रैक्टिस मोड
• विशिष्ट केस सेट के लिए लक्षित ड्रिलिंग
• पैटर्न पहचान की गति बढ़ाएं
• अपने लक्ष्यों से मेल खाने के लिए कई प्रशिक्षण मोड

क्यूबर्स द्वारा, क्यूबर्स के लिए बनाया गया। फीडबैक? हमें contact@deddal.app पर बताएं

Keep Cubing! 🎲""",

    "hr": """Što je novo u v0.4.1

🏠 NOVO: Početna nadzorna ploča
• Pogledajte svoju trenutnu razinu vještina na prvi pogled
• Pratite ovladavanje F2L, OLL i PLL
• Dobijte personalizirane uvide o svom napretku

📚 POBOLJŠANO: Biblioteka algoritama
• Pregledajte sve CFOP slučajeve (F2L, OLL, PLL)
• Pogledajte više varijacija algoritama po slučaju
• Brzi pristup vizualnim demonstracijama

📊 NOVO: Praćenje napretka
• Detaljne analize vašeg poboljšanja
• Pregled ovladavanja slučaj po slučaj
• Pratite svoje putovanje učenja tijekom vremena

🎯 NOVO: Načini vježbanja
• Ciljana vježba za specifične skupove slučajeva
• Izgradite brzinu prepoznavanja uzoraka
• Više načina treniranja koji odgovaraju vašim ciljevima

Napravljeno od cubera za cubere. Imate povratne informacije? Javite nam se na contact@deddal.app

Keep Cubing! 🎲""",

    "hu": """Újdonságok a v0.4.1-ben

🏠 ÚJ: Kezdőlap műszerfal
• Lásd a jelenlegi képességszintedet egy pillantásra
• Kövesd a F2L, OLL és PLL elsajátítását
• Szerezz személyre szabott betekintést a haladásodról

📚 TOVÁBBFEJLESZTETT: Algoritmuskönyvtár
• Böngéssz az összes CFOP esetet (F2L, OLL, PLL)
• Nézd meg egy eset több algoritmusvariációját
• Gyors hozzáférés a vizuális bemutatókhoz

📊 ÚJ: Haladáskövetés
• Részletes elemzések a fejlődésedről
• Eset-eseti elsajátítási áttekintés
• Kövesd a tanulási utadat az idő múlásával

🎯 ÚJ: Gyakorlási módok
• Célzott edzés specifikus esetkészletekhez
• Építsd a mintafelismerési sebességet
• Több edzésmód a céljaidhoz

Cuberek által cubereknek készítve. Van visszajelzésed? Írj nekünk a contact@deddal.app címre

Keep Cubing! 🎲""",

    "id": """Yang Baru di v0.4.1

🏠 BARU: Dasbor Beranda
• Lihat tingkat keterampilan Anda saat ini sekilas
• Lacak penguasaan di F2L, OLL, dan PLL
• Dapatkan wawasan yang dipersonalisasi tentang kemajuan Anda

📚 DITINGKATKAN: Perpustakaan Algoritma
• Jelajahi semua kasus CFOP (F2L, OLL, PLL)
• Lihat beberapa variasi algoritma per kasus
• Akses cepat ke demonstrasi visual

📊 BARU: Pelacakan Kemajuan
• Analitik terperinci tentang peningkatan Anda
• Ringkasan penguasaan kasus per kasus
• Lacak perjalanan pembelajaran Anda dari waktu ke waktu

🎯 BARU: Mode Latihan
• Latihan yang ditargetkan untuk set kasus tertentu
• Bangun kecepatan pengenalan pola
• Beberapa mode pelatihan untuk tujuan Anda

Dibuat oleh cuber untuk cuber. Punya masukan? Beri tahu kami di contact@deddal.app

Keep Cubing! 🎲""",

    "ms": """Apa yang Baharu dalam v0.4.1

🏠 BAHARU: Papan Pemuka Utama
• Lihat tahap kemahiran semasa anda sepintas lalu
• Jejaki penguasaan merentas F2L, OLL, dan PLL
• Dapatkan pandangan peribadi tentang kemajuan anda

📚 DIPERTINGKAT: Perpustakaan Algoritma
• Layari semua kes CFOP (F2L, OLL, PLL)
• Lihat pelbagai variasi algoritma setiap kes
• Akses pantas kepada demonstrasi visual

📊 BAHARU: Penjejakan Kemajuan
• Analitik terperinci tentang peningkatan anda
• Ringkasan penguasaan kes demi kes
• Jejaki perjalanan pembelajaran anda dari masa ke masa

🎯 BAHARU: Mod Latihan
• Latihan yang disasarkan untuk set kes tertentu
• Bina kelajuan pengecaman corak
• Beberapa mod latihan untuk matlamat anda

Dibuat oleh cubers untuk cubers. Ada maklum balas? Beritahu kami di contact@deddal.app

Keep Cubing! 🎲""",

    "nl-NL": """Nieuw in v0.4.1

🏠 NIEUW: Thuisdashboard
• Zie je huidige vaardigheidsniveau in één oogopslag
• Volg beheersing over F2L, OLL en PLL
• Krijg gepersonaliseerde inzichten over je voortgang

📚 VERBETERD: Algoritmebibliotheek
• Blader door alle CFOP-gevallen (F2L, OLL, PLL)
• Bekijk meerdere algoritmevariaties per geval
• Snelle toegang tot visuele demonstraties

📊 NIEUW: Voortgangsregistratie
• Gedetailleerde analyses van je verbetering
• Overzicht van beheersing per geval
• Volg je leerreis in de loop van de tijd

🎯 NIEUW: Oefenmodi
• Gerichte oefening voor specifieke gevallensets
• Bouw patroonherkenningssnelheid op
• Meerdere trainingsmodi passend bij je doelen

Gemaakt door cubers voor cubers. Feedback? Laat het ons weten op contact@deddal.app

Keep Cubing! 🎲""",

    "no": """Hva er nytt i v0.4.1

🏠 NYTT: Hjemmesidedashboard
• Se ditt nåværende ferdighetsnivå med ett blikk
• Følg mestring på tvers av F2L, OLL og PLL
• Få personlige innsikter i fremgangen din

📚 FORBEDRET: Algoritmebibliotek
• Bla gjennom alle CFOP-tilfeller (F2L, OLL, PLL)
• Se flere algoritmevarianter per tilfelle
• Rask tilgang til visuelle demonstrasjoner

📊 NYTT: Fremgangssporing
• Detaljerte analyser av forbedringen din
• Oversikt over mestring tilfelle for tilfelle
• Følg læringsreisen din over tid

🎯 NYTT: Øvelsesmoduser
• Målrettet øving for spesifikke tilfellesett
• Bygg mønstergjenkjenningshastighet
• Flere treningsmodus for målene dine

Laget av cubers for cubers. Har du tilbakemelding? Gi oss beskjed på contact@deddal.app

Keep Cubing! 🎲""",

    "pl": """Co nowego w v0.4.1

🏠 NOWE: Panel główny
• Zobacz swój obecny poziom umiejętności na pierwszy rzut oka
• Śledź opanowanie F2L, OLL i PLL
• Uzyskaj spersonalizowane informacje o swoich postępach

📚 ULEPSZONE: Biblioteka algorytmów
• Przeglądaj wszystkie przypadki CFOP (F2L, OLL, PLL)
• Wyświetl wiele wariantów algorytmu na przypadek
• Szybki dostęp do wizualnych demonstracji

📊 NOWE: Śledzenie postępów
• Szczegółowe analizy twoich ulepszeń
• Przegląd opanowania przypadek po przypadku
• Śledź swoją podróż edukacyjną w czasie

🎯 NOWE: Tryby ćwiczeń
• Ukierunkowane ćwiczenia dla określonych zestawów przypadków
• Buduj szybkość rozpoznawania wzorców
• Wiele trybów treningowych dopasowanych do twoich celów

Stworzone przez cuberów dla cuberów. Masz opinię? Daj nam znać na contact@deddal.app

Keep Cubing! 🎲""",

    "ro": """Ce e nou în v0.4.1

🏠 NOU: Tablou de bord principal
• Vezi nivelul tău actual de abilități dintr-o privire
• Urmărește stăpânirea pe F2L, OLL și PLL
• Obține informații personalizate despre progresul tău

📚 ÎMBUNĂTĂȚIT: Biblioteca de algoritmi
• Răsfoiește toate cazurile CFOP (F2L, OLL, PLL)
• Vezi mai multe variante de algoritmi pe caz
• Acces rapid la demonstrații vizuale

📊 NOU: Urmărire progres
• Analize detaliate ale îmbunătățirii tale
• Prezentare generală a stăpânirii caz cu caz
• Urmărește călătoria ta de învățare în timp

🎯 NOU: Moduri de practică
• Antrenament țintit pentru seturi specifice de cazuri
• Construiește viteza de recunoaștere a tiparelor
• Mai multe moduri de antrenament pentru obiectivele tale

Făcut de cuberi pentru cuberi. Ai feedback? Anunță-ne la contact@deddal.app

Keep Cubing! 🎲""",

    "sk": """Čo je nové vo v0.4.1

🏠 NOVÉ: Hlavný panel
• Pozrite si svoju aktuálnu úroveň zručností na prvý pohľad
• Sledujte zvládnutie F2L, OLL a PLL
• Získajte personalizované poznatky o svojom pokroku

📚 VYLEPŠENÉ: Knižnica algoritmov
• Prechádzajte všetky prípady CFOP (F2L, OLL, PLL)
• Zobrazte viac variácií algoritmov na prípad
• Rýchly prístup k vizuálnym ukážkam

📊 NOVÉ: Sledovanie pokroku
• Podrobné analýzy vášho zlepšenia
• Prehľad zvládnutia prípad od prípadu
• Sledujte svoju cestu učenia v čase

🎯 NOVÉ: Režimy cvičenia
• Cielené cvičenie pre konkrétne sady prípadov
• Vytvárajte rýchlosť rozpoznávania vzorov
• Viac tréningových režimov podľa vašich cieľov

Vytvorené cubermi pre cuberov. Máte spätnú väzbu? Dajte nám vedieť na contact@deddal.app

Keep Cubing! 🎲""",

    "sv": """Nytt i v0.4.1

🏠 NYTT: Hem-instrumentpanel
• Se din nuvarande färdighetsnivå med en blick
• Följ behärskning över F2L, OLL och PLL
• Få personliga insikter om dina framsteg

📚 FÖRBÄTTRAT: Algoritmbibliotek
• Bläddra bland alla CFOP-fall (F2L, OLL, PLL)
• Visa flera algoritmvariationer per fall
• Snabb åtkomst till visuella demonstrationer

📊 NYTT: Framstegsspårning
• Detaljerade analyser av din förbättring
• Översikt över behärskning fall för fall
• Följ din inlärningsresa över tid

🎯 NYTT: Övningslägen
• Riktad övning för specifika falluppsättningar
• Bygg mönsterigenkänningshastighet
• Flera träningslägen för dina mål

Gjort av cubers för cubers. Har du feedback? Meddela oss på contact@deddal.app

Keep Cubing! 🎲""",

    "th": """มีอะไรใหม่ใน v0.4.1

🏠 ใหม่: แดชบอร์ดหน้าแรก
• ดูระดับทักษะปัจจุบันของคุณได้อย่างรวดเร็ว
• ติดตามความเชี่ยวชาญใน F2L, OLL และ PLL
• รับข้อมูลเชิงลึกส่วนบุคคลเกี่ยวกับความคืบหน้าของคุณ

📚 ปรับปรุง: ห้องสมุดอัลกอริทึม
• เรียกดูเคส CFOP ทั้งหมด (F2L, OLL, PLL)
• ดูรูปแบบอัลกอริทึมหลายรูปแบบต่อเคส
• เข้าถึงการสาธิตภาพได้อย่างรวดเร็ว

📊 ใหม่: การติดตามความคืบหน้า
• การวิเคราะห์โดยละเอียดเกี่ยวกับการพัฒนาของคุณ
• ภาพรวมความเชี่ยวชาญแบบเคสต่อเคส
• ติดตามเส้นทางการเรียนรู้ของคุณตามกาลเวลา

🎯 ใหม่: โหมดฝึกซ้อม
• การฝึกฝนที่ตรงเป้าหมายสำหรับชุดเคสเฉพาะ
• พัฒนาความเร็วในการรับรู้รูปแบบ
• หลายโหมดการฝึกฝนที่ตรงกับเป้าหมายของคุณ

สร้างโดยนักเล่นรูบิคสำหรับนักเล่นรูบิค มีข้อเสนอแนะไหม? แจ้งให้เราทราบที่ contact@deddal.app

Keep Cubing! 🎲""",

    "tr": """v0.4.1'deki Yenilikler

🏠 YENİ: Ana Sayfa Panosu
• Mevcut beceri seviyenizi bir bakışta görün
• F2L, OLL ve PLL genelinde ustalığı takip edin
• İlerlemeniz hakkında kişiselleştirilmiş bilgiler edinin

📚 GELİŞTİRİLDİ: Algoritma Kütüphanesi
• Tüm CFOP durumlarına göz atın (F2L, OLL, PLL)
• Durum başına birden fazla algoritma varyasyonu görüntüleyin
• Görsel gösterimlere hızlı erişim

📊 YENİ: İlerleme Takibi
• İyileşmeniz hakkında ayrıntılı analizler
• Durum durum ustalık genel bakışı
• Zaman içindeki öğrenme yolculuğunuzu takip edin

🎯 YENİ: Pratik Modları
• Belirli durum setleri için hedeflenmiş pratik
• Desen tanıma hızı oluşturun
• Hedeflerinize uygun birden fazla eğitim modu

Cuberlar tarafından cuberlar için yapıldı. Geri bildiriminiz var mı? Bize contact@deddal.app adresinden bildirin

Keep Cubing! 🎲""",

    "uk": """Що нового у v0.4.1

🏠 НОВЕ: Головна панель
• Переглядайте свій поточний рівень навичок з першого погляду
• Відстежуйте майстерність у F2L, OLL і PLL
• Отримуйте персоналізовану інформацію про свій прогрес

📚 ПОКРАЩЕНО: Бібліотека алгоритмів
• Переглядайте всі випадки CFOP (F2L, OLL, PLL)
• Переглядайте кілька варіацій алгоритмів для кожного випадку
• Швидкий доступ до візуальних демонстрацій

📊 НОВЕ: Відстеження прогресу
• Детальна аналітика вашого покращення
• Огляд майстерності випадок за випадком
• Відстежуйте свій шлях навчання з часом

🎯 НОВЕ: Режими практики
• Цільова тренування для конкретних наборів випадків
• Розвивайте швидкість розпізнавання патернів
• Кілька режимів тренування під ваші цілі

Створено кубером для кубера. Є відгуки? Напишіть нам на contact@deddal.app

Keep Cubing! 🎲""",

    "vi": """Có gì mới trong v0.4.1

🏠 MỚI: Bảng điều khiển Trang chủ
• Xem mức độ kỹ năng hiện tại của bạn trong nháy mắt
• Theo dõi sự thành thạo qua F2L, OLL và PLL
• Nhận thông tin chi tiết được cá nhân hóa về tiến trình của bạn

📚 CẢI THIỆN: Thư viện Thuật toán
• Duyệt qua tất cả các trường hợp CFOP (F2L, OLL, PLL)
• Xem nhiều biến thể thuật toán cho mỗi trường hợp
• Truy cập nhanh vào các bản demo trực quan

📊 MỚI: Theo dõi Tiến trình
• Phân tích chi tiết về sự cải thiện của bạn
• Tổng quan thành thạo từng trường hợp
• Theo dõi hành trình học tập của bạn theo thời gian

🎯 MỚI: Chế độ Luyện tập
• Luyện tập có mục tiêu cho các bộ trường hợp cụ thể
• Xây dựng tốc độ nhận dạng mẫu
• Nhiều chế độ đào tạo phù hợp với mục tiêu của bạn

Được tạo bởi cuber cho cuber. Có phản hồi? Cho chúng tôi biết tại contact@deddal.app

Keep Cubing! 🎲""",
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

        # Verify character limit (4000 chars)
        char_count = len(content)
        if char_count > 4000:
            print(f"⚠️  WARNING: {locale} exceeds 4000 chars ({char_count} chars)")

        # Write release notes
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(content)

        updated_count += 1
        print(f"✅ Updated {locale}/release_notes.txt ({char_count}/4000 chars)")

    print(f"\n🎉 Complete: {updated_count} updated, {skipped_count} skipped")
    print("\nAll release notes now aligned for v0.4.1")
    print("✅ Highlights 4 new sections: Home, Library, Progress, Practice")
    print("✅ Emoji for visual hierarchy")
    print("✅ Clear version-specific content")

if __name__ == "__main__":
    main()
