#!/usr/bin/env python3
"""
Align all locale description.txt files with en-US baseline (Option B: Concise & Punchy).
Updated description covers all 4 enabled tabs: Home, Library, Progress, Practice.
Uses emoji for visual hierarchy and clear outcome focus ("get faster").
"""

import os
import re
from pathlib import Path

# Target structure from en-US (Option B: Concise & Punchy)
DESCRIPTIONS = {
    "en-US": """Master CFOP algorithms and improve your solve times with Deddal—the speedcubing training app designed to help you get faster.

📊 TRACK YOUR PROGRESS
Monitor your skill level and see which algorithms you've mastered. Track improvement across F2L, OLL, and PLL cases with detailed analytics.

📚 COMPLETE ALGORITHM LIBRARY
Access all CFOP cases—F2L, 2-Look OLL/PLL, and full OLL/PLL sets. Browse multiple algorithm variations per case to find solutions that match your solving style.

🎥 VISUAL LEARNING
Watch step-by-step algorithm visualizations. Understand move sequences, learn execution flow, and build muscle memory with interactive playback.

🎯 FOCUSED PRACTICE
Train specific case sets, drill weak spots, and build pattern recognition speed with targeted practice modes.

Built by cubers, for cubers. Clean interface, fast performance, and features that actually help you improve.

---
Terms of Use (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "en-AU": """Master CFOP algorithms and improve your solve times with Deddal—the speedcubing training app designed to help you get faster.

📊 TRACK YOUR PROGRESS
Monitor your skill level and see which algorithms you've mastered. Track improvement across F2L, OLL, and PLL cases with detailed analytics.

📚 COMPLETE ALGORITHM LIBRARY
Access all CFOP cases—F2L, 2-Look OLL/PLL, and full OLL/PLL sets. Browse multiple algorithm variations per case to find solutions that match your solving style.

🎥 VISUAL LEARNING
Watch step-by-step algorithm visualisations. Understand move sequences, learn execution flow, and build muscle memory with interactive playback.

🎯 FOCUSED PRACTICE
Train specific case sets, drill weak spots, and build pattern recognition speed with targeted practice modes.

Built by cubers, for cubers. Clean interface, fast performance, and features that actually help you improve.

---
Terms of Use (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "en-CA": """Master CFOP algorithms and improve your solve times with Deddal—the speedcubing training app designed to help you get faster.

📊 TRACK YOUR PROGRESS
Monitor your skill level and see which algorithms you've mastered. Track improvement across F2L, OLL, and PLL cases with detailed analytics.

📚 COMPLETE ALGORITHM LIBRARY
Access all CFOP cases—F2L, 2-Look OLL/PLL, and full OLL/PLL sets. Browse multiple algorithm variations per case to find solutions that match your solving style.

🎥 VISUAL LEARNING
Watch step-by-step algorithm visualisations. Understand move sequences, learn execution flow, and build muscle memory with interactive playback.

🎯 FOCUSED PRACTICE
Train specific case sets, drill weak spots, and build pattern recognition speed with targeted practice modes.

Built by cubers, for cubers. Clean interface, fast performance, and features that actually help you improve.

---
Terms of Use (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "en-GB": """Master CFOP algorithms and improve your solve times with Deddal—the speedcubing training app designed to help you get faster.

📊 TRACK YOUR PROGRESS
Monitor your skill level and see which algorithms you've mastered. Track improvement across F2L, OLL, and PLL cases with detailed analytics.

📚 COMPLETE ALGORITHM LIBRARY
Access all CFOP cases—F2L, 2-Look OLL/PLL, and full OLL/PLL sets. Browse multiple algorithm variations per case to find solutions that match your solving style.

🎥 VISUAL LEARNING
Watch step-by-step algorithm visualisations. Understand move sequences, learn execution flow, and build muscle memory with interactive playback.

🎯 FOCUSED PRACTICE
Train specific case sets, drill weak spots, and build pattern recognition speed with targeted practice modes.

Built by cubers, for cubers. Clean interface, fast performance, and features that actually help you improve.

---
Terms of Use (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "fr-FR": """Maîtrisez les algorithmes CFOP et améliorez vos temps de résolution avec Deddal—l'application d'entraînement speedcubing conçue pour vous aider à progresser.

📊 SUIVEZ VOS PROGRÈS
Surveillez votre niveau de compétence et voyez quels algorithmes vous avez maîtrisés. Suivez l'amélioration sur les cas F2L, OLL et PLL avec des analyses détaillées.

📚 BIBLIOTHÈQUE COMPLÈTE D'ALGORITHMES
Accédez à tous les cas CFOP—F2L, 2-Look OLL/PLL et ensembles OLL/PLL complets. Parcourez plusieurs variations d'algorithmes par cas pour trouver des solutions qui correspondent à votre style de résolution.

🎥 APPRENTISSAGE VISUEL
Regardez des visualisations d'algorithmes étape par étape. Comprenez les séquences de mouvements, apprenez le flux d'exécution et développez la mémoire musculaire avec la lecture interactive.

🎯 PRATIQUE CIBLÉE
Entraînez des ensembles de cas spécifiques, travaillez les points faibles et développez la vitesse de reconnaissance des motifs avec des modes de pratique ciblés.

Conçu par des cubers, pour des cubers. Interface épurée, performances rapides et fonctionnalités qui vous aident vraiment à progresser.

---
Conditions d'utilisation (EULA) : https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "fr-CA": """Maîtrisez les algorithmes CFOP et améliorez vos temps de résolution avec Deddal—l'application d'entraînement speedcubing conçue pour vous aider à progresser.

📊 SUIVEZ VOS PROGRÈS
Surveillez votre niveau de compétence et voyez quels algorithmes vous avez maîtrisés. Suivez l'amélioration sur les cas F2L, OLL et PLL avec des analyses détaillées.

📚 BIBLIOTHÈQUE COMPLÈTE D'ALGORITHMES
Accédez à tous les cas CFOP—F2L, 2-Look OLL/PLL et ensembles OLL/PLL complets. Parcourez plusieurs variations d'algorithmes par cas pour trouver des solutions qui correspondent à votre style de résolution.

🎥 APPRENTISSAGE VISUEL
Regardez des visualisations d'algorithmes étape par étape. Comprenez les séquences de mouvements, apprenez le flux d'exécution et développez la mémoire musculaire avec la lecture interactive.

🎯 PRATIQUE CIBLÉE
Entraînez des ensembles de cas spécifiques, travaillez les points faibles et développez la vitesse de reconnaissance des motifs avec des modes de pratique ciblés.

Conçu par des cubers, pour des cubers. Interface épurée, performances rapides et fonctionnalités qui vous aident vraiment à progresser.

---
Conditions d'utilisation (EULA) : https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "es-ES": """Domina los algoritmos CFOP y mejora tus tiempos de resolución con Deddal—la aplicación de entrenamiento de speedcubing diseñada para ayudarte a mejorar.

📊 SIGUE TU PROGRESO
Monitorea tu nivel de habilidad y ve qué algoritmos has dominado. Rastrea la mejora en los casos F2L, OLL y PLL con análisis detallados.

📚 BIBLIOTECA COMPLETA DE ALGORITMOS
Accede a todos los casos CFOP—F2L, 2-Look OLL/PLL y conjuntos OLL/PLL completos. Explora múltiples variaciones de algoritmos por caso para encontrar soluciones que se ajusten a tu estilo de resolución.

🎥 APRENDIZAJE VISUAL
Observa visualizaciones de algoritmos paso a paso. Comprende las secuencias de movimientos, aprende el flujo de ejecución y desarrolla memoria muscular con reproducción interactiva.

🎯 PRÁCTICA ENFOCADA
Entrena conjuntos de casos específicos, trabaja puntos débiles y desarrolla velocidad de reconocimiento de patrones con modos de práctica dirigidos.

Creado por cubers, para cubers. Interfaz limpia, rendimiento rápido y funciones que realmente te ayudan a mejorar.

---
Términos de Uso (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "es-MX": """Domina los algoritmos CFOP y mejora tus tiempos de resolución con Deddal—la aplicación de entrenamiento de speedcubing diseñada para ayudarte a mejorar.

📊 SIGUE TU PROGRESO
Monitorea tu nivel de habilidad y ve qué algoritmos has dominado. Rastrea la mejora en los casos F2L, OLL y PLL con análisis detallados.

📚 BIBLIOTECA COMPLETA DE ALGORITMOS
Accede a todos los casos CFOP—F2L, 2-Look OLL/PLL y conjuntos OLL/PLL completos. Explora múltiples variaciones de algoritmos por caso para encontrar soluciones que se ajusten a tu estilo de resolución.

🎥 APRENDIZAJE VISUAL
Observa visualizaciones de algoritmos paso a paso. Comprende las secuencias de movimientos, aprende el flujo de ejecución y desarrolla memoria muscular con reproducción interactiva.

🎯 PRÁCTICA ENFOCADA
Entrena conjuntos de casos específicos, trabaja puntos débiles y desarrolla velocidad de reconocimiento de patrones con modos de práctica dirigidos.

Creado por cubers, para cubers. Interfaz limpia, rendimiento rápido y funciones que realmente te ayudan a mejorar.

---
Términos de Uso (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "ja": """CFOPアルゴリズムをマスターし、Deddalで解法タイムを改善—より速くなるために設計されたスピードキューブトレーニングアプリ。

📊 進捗を追跡
スキルレベルを監視し、習得したアルゴリズムを確認。詳細な分析でF2L、OLL、PLLケースの改善を追跡。

📚 完全なアルゴリズムライブラリ
すべてのCFOPケースにアクセス—F2L、2-Look OLL/PLL、完全なOLL/PLLセット。ケースごとに複数のアルゴリズムバリエーションを閲覧し、あなたの解法スタイルに合うソリューションを見つける。

🎥 ビジュアル学習
ステップバイステップのアルゴリズム視覚化を観察。動きのシーケンスを理解し、実行フローを学び、インタラクティブな再生で筋肉記憶を構築。

🎯 集中練習
特定のケースセットをトレーニングし、弱点を鍛え、ターゲット練習モードでパターン認識速度を向上。

キューバーによる、キューバーのための。クリーンなインターフェース、高速パフォーマンス、実際に上達に役立つ機能。

---
利用規約 (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "zh-Hans": """掌握CFOP算法并提高解魔方速度，Deddal—专为帮助你提速而设计的速度魔方训练应用。

📊 追踪进度
监控技能水平，查看已掌握的算法。通过详细分析追踪F2L、OLL和PLL案例的改进。

📚 完整算法库
访问所有CFOP案例—F2L、2-Look OLL/PLL和完整OLL/PLL集合。浏览每个案例的多种算法变体，找到适合你解法风格的方案。

🎥 可视化学习
观看分步算法可视化。理解移动序列，学习执行流程，通过互动播放建立肌肉记忆。

🎯 专注练习
训练特定案例集，攻克薄弱环节，通过针对性练习模式提升模式识别速度。

由魔方玩家打造，为魔方玩家服务。简洁界面，快速性能，真正帮助你提升的功能。

---
使用条款 (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "zh-Hant": """掌握CFOP演算法並提高解魔方速度，Deddal—專為幫助你提速而設計的速度魔方訓練應用程式。

📊 追蹤進度
監控技能水平，查看已掌握的演算法。透過詳細分析追蹤F2L、OLL和PLL案例的改進。

📚 完整演算法庫
存取所有CFOP案例—F2L、2-Look OLL/PLL和完整OLL/PLL集合。瀏覽每個案例的多種演算法變體，找到適合你解法風格的方案。

🎥 視覺化學習
觀看分步演算法視覺化。理解移動序列，學習執行流程，透過互動播放建立肌肉記憶。

🎯 專注練習
訓練特定案例集，攻克薄弱環節，透過針對性練習模式提升模式識別速度。

由魔方玩家打造，為魔方玩家服務。簡潔介面，快速效能，真正幫助你提升的功能。

---
使用條款 (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "de-DE": """Meistern Sie CFOP-Algorithmen und verbessern Sie Ihre Lösezeiten mit Deddal—der Speedcubing-Trainings-App, die Ihnen hilft, schneller zu werden.

📊 VERFOLGEN SIE IHREN FORTSCHRITT
Überwachen Sie Ihr Fähigkeitsniveau und sehen Sie, welche Algorithmen Sie gemeistert haben. Verfolgen Sie Verbesserungen bei F2L-, OLL- und PLL-Fällen mit detaillierten Analysen.

📚 VOLLSTÄNDIGE ALGORITHMUS-BIBLIOTHEK
Greifen Sie auf alle CFOP-Fälle zu—F2L, 2-Look OLL/PLL und vollständige OLL/PLL-Sets. Durchsuchen Sie mehrere Algorithmusvariationen pro Fall, um Lösungen zu finden, die zu Ihrem Lösungsstil passen.

🎥 VISUELLES LERNEN
Sehen Sie sich Schritt-für-Schritt-Algorithmus-Visualisierungen an. Verstehen Sie Bewegungsabläufe, lernen Sie den Ausführungsfluss und bauen Sie Muskelgedächtnis mit interaktiver Wiedergabe auf.

🎯 GEZIELTES ÜBEN
Trainieren Sie spezifische Fall-Sets, arbeiten Sie an Schwachstellen und bauen Sie Mustererkennung-Geschwindigkeit mit gezielten Übungsmodi auf.

Von Cubern gebaut, für Cuber. Saubere Benutzeroberfläche, schnelle Leistung und Funktionen, die Ihnen tatsächlich helfen, sich zu verbessern.

---
Nutzungsbedingungen (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "it": """Padroneggia gli algoritmi CFOP e migliora i tuoi tempi di risoluzione con Deddal—l'app di allenamento per speedcubing progettata per aiutarti a migliorare.

📊 TRACCIA I TUOI PROGRESSI
Monitora il tuo livello di abilità e vedi quali algoritmi hai padroneggiato. Traccia i miglioramenti sui casi F2L, OLL e PLL con analisi dettagliate.

📚 LIBRERIA COMPLETA DI ALGORITMI
Accedi a tutti i casi CFOP—F2L, 2-Look OLL/PLL e set OLL/PLL completi. Sfoglia più variazioni di algoritmi per caso per trovare soluzioni che corrispondono al tuo stile di risoluzione.

🎥 APPRENDIMENTO VISIVO
Guarda visualizzazioni di algoritmi passo dopo passo. Comprendi le sequenze di mosse, impara il flusso di esecuzione e costruisci memoria muscolare con riproduzione interattiva.

🎯 PRATICA MIRATA
Allenati su set di casi specifici, lavora sui punti deboli e sviluppa velocità di riconoscimento dei pattern con modalità di pratica mirate.

Costruito da cuber, per cuber. Interfaccia pulita, prestazioni veloci e funzionalità che ti aiutano davvero a migliorare.

---
Termini di utilizzo (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "pt-BR": """Domine algoritmos CFOP e melhore seus tempos de resolução com Deddal—o aplicativo de treinamento de speedcubing projetado para ajudá-lo a ficar mais rápido.

📊 ACOMPANHE SEU PROGRESSO
Monitore seu nível de habilidade e veja quais algoritmos você dominou. Acompanhe a melhoria nos casos F2L, OLL e PLL com análises detalhadas.

📚 BIBLIOTECA COMPLETA DE ALGORITMOS
Acesse todos os casos CFOP—F2L, 2-Look OLL/PLL e conjuntos OLL/PLL completos. Navegue por múltiplas variações de algoritmos por caso para encontrar soluções que correspondam ao seu estilo de resolução.

🎥 APRENDIZADO VISUAL
Assista visualizações de algoritmos passo a passo. Compreenda sequências de movimentos, aprenda o fluxo de execução e construa memória muscular com reprodução interativa.

🎯 PRÁTICA FOCADA
Treine conjuntos de casos específicos, trabalhe pontos fracos e desenvolva velocidade de reconhecimento de padrões com modos de prática direcionados.

Construído por cubers, para cubers. Interface limpa, desempenho rápido e recursos que realmente ajudam você a melhorar.

---
Termos de Uso (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "pt-PT": """Domine algoritmos CFOP e melhore os seus tempos de resolução com Deddal—a aplicação de treino de speedcubing concebida para o ajudar a ficar mais rápido.

📊 ACOMPANHE O SEU PROGRESSO
Monitorize o seu nível de habilidade e veja quais algoritmos dominou. Acompanhe a melhoria nos casos F2L, OLL e PLL com análises detalhadas.

📚 BIBLIOTECA COMPLETA DE ALGORITMOS
Aceda a todos os casos CFOP—F2L, 2-Look OLL/PLL e conjuntos OLL/PLL completos. Navegue por múltiplas variações de algoritmos por caso para encontrar soluções que correspondam ao seu estilo de resolução.

🎥 APRENDIZAGEM VISUAL
Veja visualizações de algoritmos passo a passo. Compreenda sequências de movimentos, aprenda o fluxo de execução e construa memória muscular com reprodução interativa.

🎯 PRÁTICA FOCADA
Treine conjuntos de casos específicos, trabalhe pontos fracos e desenvolva velocidade de reconhecimento de padrões com modos de prática direcionados.

Construído por cubers, para cubers. Interface limpa, desempenho rápido e recursos que realmente o ajudam a melhorar.

---
Termos de Utilização (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "ko": """CFOP 알고리즘을 마스터하고 Deddal로 해결 시간을 개선하세요—더 빨라지도록 설계된 스피드큐빙 훈련 앱입니다.

📊 진행 상황 추적
기술 수준을 모니터링하고 마스터한 알고리즘을 확인하세요. 상세한 분석으로 F2L, OLL, PLL 케이스의 개선을 추적합니다.

📚 완전한 알고리즘 라이브러리
모든 CFOP 케이스에 액세스—F2L, 2-Look OLL/PLL 및 전체 OLL/PLL 세트. 케이스당 여러 알고리즘 변형을 탐색하여 해결 스타일에 맞는 솔루션을 찾으세요.

🎥 시각적 학습
단계별 알고리즘 시각화를 시청하세요. 이동 순서를 이해하고, 실행 흐름을 배우며, 대화형 재생으로 근육 기억을 구축합니다.

🎯 집중 연습
특정 케이스 세트를 훈련하고, 약점을 연마하며, 목표 연습 모드로 패턴 인식 속도를 향상시킵니다.

큐버에 의해, 큐버를 위해 제작. 깔끔한 인터페이스, 빠른 성능, 실제로 향상에 도움이 되는 기능.

---
이용 약관 (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "ru": """Освойте алгоритмы CFOP и улучшите время сборки с Deddal—приложением для тренировок по спидкубингу, разработанным, чтобы помочь вам стать быстрее.

📊 ОТСЛЕЖИВАЙТЕ ПРОГРЕСС
Отслеживайте уровень навыков и смотрите, какие алгоритмы вы освоили. Отслеживайте улучшения по случаям F2L, OLL и PLL с подробной аналитикой.

📚 ПОЛНАЯ БИБЛИОТЕКА АЛГОРИТМОВ
Получите доступ ко всем случаям CFOP—F2L, 2-Look OLL/PLL и полным наборам OLL/PLL. Просматривайте несколько вариантов алгоритмов для каждого случая, чтобы найти решения, соответствующие вашему стилю сборки.

🎥 ВИЗУАЛЬНОЕ ОБУЧЕНИЕ
Смотрите пошаговые визуализации алгоритмов. Понимайте последовательности ходов, изучайте поток выполнения и развивайте мышечную память с интерактивным воспроизведением.

🎯 ЦЕЛЕНАПРАВЛЕННАЯ ПРАКТИКА
Тренируйте конкретные наборы случаев, работайте над слабыми местами и развивайте скорость распознавания паттернов с целевыми режимами практики.

Создано кьюберами, для кьюберов. Чистый интерфейс, быстрая производительность и функции, которые действительно помогают улучшиться.

---
Условия использования (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "ar-SA": """أتقن خوارزميات CFOP وحسّن أوقات الحل مع Deddal—تطبيق تدريب السرعة المصمم لمساعدتك على التحسن.

📊 تتبع تقدمك
راقب مستوى مهارتك وشاهد الخوارزميات التي أتقنتها. تتبع التحسن في حالات F2L و OLL و PLL بتحليلات مفصلة.

📚 مكتبة خوارزميات كاملة
الوصول إلى جميع حالات CFOP—F2L و 2-Look OLL/PLL ومجموعات OLL/PLL الكاملة. تصفح تنويعات خوارزميات متعددة لكل حالة للعثور على حلول تناسب أسلوب الحل الخاص بك.

🎥 التعلم البصري
شاهد تصورات الخوارزميات خطوة بخطوة. فهم تسلسلات الحركة، تعلم تدفق التنفيذ، وبناء الذاكرة العضلية مع التشغيل التفاعلي.

🎯 ممارسة مركزة
تدرب على مجموعات حالات محددة، اعمل على نقاط الضعف، وطور سرعة التعرف على الأنماط مع أوضاع التدريب المستهدفة.

بُني بواسطة اللاعبين، للاعبين. واجهة نظيفة، أداء سريع، وميزات تساعدك فعلاً على التحسن.

---
شروط الاستخدام (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "ca": """Domina els algoritmes CFOP i millora els teus temps de resolució amb Deddal—l'aplicació d'entrenament de speedcubing dissenyada per ajudar-te a millorar.

📊 SEGUEIX EL TEU PROGRÉS
Monitoritza el teu nivell d'habilitat i veu quins algoritmes has dominat. Segueix la millora en els casos F2L, OLL i PLL amb anàlisis detallades.

📚 BIBLIOTECA COMPLETA D'ALGORITMES
Accedeix a tots els casos CFOP—F2L, 2-Look OLL/PLL i conjunts OLL/PLL complets. Explora múltiples variacions d'algoritmes per cas per trobar solucions que s'ajustin al teu estil de resolució.

🎥 APRENENTATGE VISUAL
Observa visualitzacions d'algoritmes pas a pas. Comprèn les seqüències de moviments, aprèn el flux d'execució i desenvolupa memòria muscular amb reproducció interactiva.

🎯 PRÀCTICA ENFOCADA
Entrena conjunts de casos específics, treballa punts febles i desenvolupa velocitat de reconeixement de patrons amb modes de pràctica dirigits.

Creat per cubers, per a cubers. Interfície neta, rendiment ràpid i funcions que realment t'ajuden a millorar.

---
Condicions d'ús (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "cs": """Zvládněte algoritmy CFOP a zlepšete své časy řešení s Deddal—aplikací pro trénink speedcubingu navržené, aby vám pomohla zrychlit.

📊 SLEDUJTE SVůJ POKROK
Sledujte úroveň dovedností a zjistěte, které algoritmy jste zvládli. Sledujte zlepšení u případů F2L, OLL a PLL s podrobnou analytikou.

📚 KOMPLETNÍ KNIHOVNA ALGORITMŮ
Získejte přístup ke všem případům CFOP—F2L, 2-Look OLL/PLL a úplným sadám OLL/PLL. Procházejte více variací algoritmů na případ a najděte řešení, která odpovídají vašemu stylu řešení.

🎥 VIZUÁLNÍ UČENÍ
Sledujte vizualizace algoritmů krok za krokem. Pochopte sekvence tahů, naučte se průběh provádění a vybudujte si svalovou paměť s interaktivním přehráváním.

🎯 CÍLENÝ TRÉNINK
Trénujte konkrétní sady případů, pracujte na slabých místech a rozvíjejte rychlost rozpoznávání vzorů s cílenými tréninkovými režimy.

Vytvořeno cubery, pro cubery. Čisté rozhraní, rychlý výkon a funkce, které vám skutečně pomáhají zlepšit se.

---
Podmínky použití (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "da": """Mestre CFOP-algoritmer og forbedr dine løsningstider med Deddal—speedcubing-træningsappen designet til at hjælpe dig med at blive hurtigere.

📊 SPOR DIN FREMGANG
Overvåg dit færdighedsniveau og se, hvilke algoritmer du har mestret. Spor forbedring på tværs af F2L-, OLL- og PLL-cases med detaljeret analyse.

📚 KOMPLET ALGORITMEBIBLIOTEK
Få adgang til alle CFOP-cases—F2L, 2-Look OLL/PLL og komplette OLL/PLL-sæt. Gennemse flere algoritmevariationer pr. case for at finde løsninger, der matcher din løsningsstil.

🎥 VISUEL LÆRING
Se trin-for-trin algoritmevisualiseringer. Forstå bevægelsessekvenser, lær udførelsesflow og byg muskelhukommelse med interaktiv afspilning.

🎯 FOKUSERET TRÆNING
Træn specifikke case-sæt, arbejd på svage punkter og udvikl mønstergenkendelseshastighed med målrettede træningsmode.

Bygget af cubere, til cubere. Ren grænseflade, hurtig ydeevne og funktioner, der faktisk hjælper dig med at forbedre dig.

---
Brugsbetingelser (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "el": """Κατακτήστε τους αλγόριθμους CFOP και βελτιώστε τους χρόνους λύσης με το Deddal—την εφαρμογή προπόνησης speedcubing σχεδιασμένη να σας βοηθήσει να γίνετε ταχύτεροι.

📊 ΠΑΡΑΚΟΛΟΥΘΗΣΤΕ ΤΗΝ ΠΡΟΟΔΟ ΣΑΣ
Παρακολουθήστε το επίπεδο δεξιοτήτων σας και δείτε ποιους αλγόριθμους έχετε κατακτήσει. Παρακολουθήστε τη βελτίωση σε περιπτώσεις F2L, OLL και PLL με λεπτομερή ανάλυση.

📚 ΠΛΗΡΗΣ ΒΙΒΛΙΟΘΗΚΗ ΑΛΓΟΡΙΘΜΩΝ
Αποκτήστε πρόσβαση σε όλες τις περιπτώσεις CFOP—F2L, 2-Look OLL/PLL και πλήρη σύνολα OLL/PLL. Περιηγηθείτε σε πολλαπλές παραλλαγές αλγορίθμων ανά περίπτωση για να βρείτε λύσεις που ταιριάζουν στο στυλ επίλυσής σας.

🎥 ΟΠΤΙΚΗ ΜΑΘΗΣΗ
Παρακολουθήστε οπτικοποιήσεις αλγορίθμων βήμα προς βήμα. Κατανοήστε ακολουθίες κινήσεων, μάθετε τη ροή εκτέλεσης και χτίστε μυϊκή μνήμη με διαδραστική αναπαραγωγή.

🎯 ΣΤΟΧΕΥΜΕΝΗ ΕΞΑΣΚΗΣΗ
Εκπαιδεύστε συγκεκριμένα σύνολα περιπτώσεων, εργαστείτε σε αδύναμα σημεία και αναπτύξτε ταχύτητα αναγνώρισης μοτίβων με στοχευμένες λειτουργίες εξάσκησης.

Δημιουργήθηκε από cubers, για cubers. Καθαρή διεπαφή, γρήγορη απόδοση και λειτουργίες που πραγματικά σας βοηθούν να βελτιωθείτε.

---
Όροι χρήσης (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "fi": """Hallitse CFOP-algoritmit ja paranna ratkaisuaikojasi Deddalilla—speedcubing-harjoitussovellus, joka on suunniteltu auttamaan sinua nopeutumaan.

📊 SEURAA EDISTYMISTÄSI
Seuraa taitotasoasi ja katso, mitkä algoritmit olet hallinnut. Seuraa parannusta F2L-, OLL- ja PLL-tapauksissa yksityiskohtaisilla analyyseilla.

📚 TÄYDELLINEN ALGORITMIKIRJASTO
Pääse käsiksi kaikkiin CFOP-tapauksiin—F2L, 2-Look OLL/PLL ja täydelliset OLL/PLL-sarjat. Selaa useita algoritmivariaatioita tapausta kohden löytääksesi ratkaisut, jotka sopivat ratkaisutyylisi.

🎥 VISUAALINEN OPPIMINEN
Katso vaiheittaisia algoritmin visualisointeja. Ymmärrä siirtojen järjestykset, opi suorituksen kulku ja rakenna lihasmuisti interaktiivisella toistolla.

🎯 KOHDENNETTU HARJOITTELU
Harjoittele tiettyjä tapaussarjoja, työstä heikkoja kohtia ja kehitä kuvioiden tunnistusnopeutta kohdennetuilla harjoitustiloilla.

Cubereille cubereiden toimesta. Siisti käyttöliittymä, nopea suorituskyky ja ominaisuudet, jotka todella auttavat sinua parantumaan.

---
Käyttöehdot (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "he": """שלוט באלגוריתמי CFOP ושפר את זמני הפתרון שלך עם Deddal—אפליקציית האימון ל-speedcubing שתוכננה לעזור לך להשתפר.

📊 עקוב אחר ההתקדמות
עקוב אחר רמת המיומנות שלך וראה אילו אלגוריתמים שלטת. עקוב אחר שיפור במקרי F2L, OLL ו-PLL עם ניתוח מפורט.

📚 ספריית אלגוריתמים מלאה
גישה לכל מקרי CFOP—F2L, 2-Look OLL/PLL וסטים מלאים של OLL/PLL. עיין בווריאציות אלגוריתמים מרובות למקרה כדי למצוא פתרונות שמתאימים לסגנון הפתרון שלך.

🎥 למידה ויזואלית
צפה בהדמיות אלגוריתמים שלב אחר שלב. הבן רצפי תנועות, למד זרימת ביצוע ובנה זיכרון שרירים עם השמעה אינטראקטיבית.

🎯 תרגול ממוקד
אמן סטים ספציפיים של מקרים, עבוד על נקודות חולשה ופתח מהירות זיהוי דפוסים עם מצבי תרגול ממוקדים.

נבנה על ידי cubers, עבור cubers. ממשק נקי, ביצועים מהירים ותכונות שבאמת עוזרות לך להשתפר.

---
תנאי שימוש (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "hi": """CFOP एल्गोरिदम में महारत हासिल करें और Deddal के साथ अपने समाधान समय में सुधार करें—स्पीडक्यूबिंग प्रशिक्षण ऐप जो आपको तेज़ होने में मदद करने के लिए डिज़ाइन किया गया है।

📊 अपनी प्रगति को ट्रैक करें
अपने कौशल स्तर की निगरानी करें और देखें कि आपने कौन से एल्गोरिदम में महारत हासिल की है। विस्तृत विश्लेषण के साथ F2L, OLL और PLL मामलों में सुधार को ट्रैक करें।

📚 पूर्ण एल्गोरिदम लाइब्रेरी
सभी CFOP मामलों तक पहुंच—F2L, 2-Look OLL/PLL और पूर्ण OLL/PLL सेट। प्रति मामले कई एल्गोरिदम विविधताओं को ब्राउज़ करें ताकि आपकी समाधान शैली से मेल खाने वाले समाधान मिल सकें।

🎥 दृश्य शिक्षण
चरण-दर-चरण एल्गोरिदम विज़ुअलाइज़ेशन देखें। चाल अनुक्रमों को समझें, निष्पादन प्रवाह सीखें, और इंटरैक्टिव प्लेबैक के साथ मांसपेशी स्मृति बनाएं।

🎯 केंद्रित अभ्यास
विशिष्ट मामले सेट प्रशिक्षित करें, कमजोर बिंदुओं पर काम करें, और लक्षित अभ्यास मोड के साथ पैटर्न पहचान गति विकसित करें।

क्यूबर्स द्वारा, क्यूबर्स के लिए बनाया गया। साफ इंटरफ़ेस, तेज़ प्रदर्शन, और सुविधाएं जो वास्तव में आपको सुधारने में मदद करती हैं।

---
उपयोग की शर्तें (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "hr": """Savladajte CFOP algoritme i poboljšajte vrijeme rješavanja s Deddal—aplikacijom za speedcubing trening dizajniranom da vam pomogne da postanete brži.

📊 PRATITE SVOJ NAPREDAK
Pratite razinu vještina i vidite koje ste algoritme savladali. Pratite poboljšanje F2L, OLL i PLL slučajeva s detaljnom analitikom.

📚 POTPUNA BIBLIOTEKA ALGORITAMA
Pristupite svim CFOP slučajevima—F2L, 2-Look OLL/PLL i potpunim OLL/PLL setovima. Pregledajte više varijacija algoritama po slučaju kako biste pronašli rješenja koja odgovaraju vašem stilu rješavanja.

🎥 VIZUALNO UČENJE
Gledajte vizualizacije algoritama korak po korak. Razumite sekvence poteza, naučite tok izvršavanja i izgradite mišićnu memoriju s interaktivnom reprodukcijom.

🎯 FOKUSIRANA PRAKSA
Trenirajte određene setove slučajeva, radite na slabim točkama i razvijajte brzinu prepoznavanja uzoraka s ciljanim načinima vježbanja.

Napravljeno od strane cubera, za cubere. Čisto sučelje, brze performanse i značajke koje vam stvarno pomažu da se poboljšate.

---
Uvjeti korištenja (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "hu": """Sajátítsa el a CFOP algoritmusokat és javítsa megoldási idejét a Deddal segítségével—a speedcubing edzőalkalmazás, amely segít gyorsabbá válni.

📊 KÖVESSE NYOMON FEJLŐDÉSÉT
Figyelje készségszintjét és lássa, mely algoritmusokat sajátította el. Kövesse nyomon a javulást az F2L, OLL és PLL eseteknél részletes elemzésekkel.

📚 TELJES ALGORITMUS KÖNYVTÁR
Férjen hozzá az összes CFOP esethez—F2L, 2-Look OLL/PLL és teljes OLL/PLL készletek. Böngésszen több algoritmus variáción eseteként, hogy megtalálja a megoldási stílusának megfelelő megoldásokat.

🎥 VIZUÁLIS TANULÁS
Nézzen lépésről lépésre algoritmus vizualizációkat. Értse meg a mozdulatsor rendjét, tanulja meg a végrehajtási folyamatot, és építsen izommemóriát interaktív lejátszással.

🎯 CÉLZOTT GYAKORLÁS
Gyakoroljon konkrét eset készleteket, dolgozzon a gyenge pontokon, és fejlessze a minta felismerési sebességet célzott gyakorló módokkal.

Cuberek által, cubereknek készítve. Tiszta felület, gyors teljesítmény és olyan funkciók, amelyek tényleg segítenek fejlődni.

---
Felhasználási feltételek (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "id": """Kuasai algoritma CFOP dan tingkatkan waktu penyelesaian Anda dengan Deddal—aplikasi pelatihan speedcubing yang dirancang untuk membantu Anda menjadi lebih cepat.

📊 LACAK KEMAJUAN ANDA
Pantau tingkat keterampilan Anda dan lihat algoritma mana yang telah Anda kuasai. Lacak peningkatan di kasus F2L, OLL, dan PLL dengan analitik terperinci.

📚 PERPUSTAKAAN ALGORITMA LENGKAP
Akses semua kasus CFOP—F2L, 2-Look OLL/PLL, dan set OLL/PLL lengkap. Jelajahi berbagai variasi algoritma per kasus untuk menemukan solusi yang sesuai dengan gaya penyelesaian Anda.

🎥 PEMBELAJARAN VISUAL
Tonton visualisasi algoritma langkah demi langkah. Pahami urutan gerakan, pelajari alur eksekusi, dan bangun memori otot dengan pemutaran interaktif.

🎯 LATIHAN TERFOKUS
Latih set kasus tertentu, kerjakan titik lemah, dan kembangkan kecepatan pengenalan pola dengan mode latihan yang ditargetkan.

Dibangun oleh cubers, untuk cubers. Antarmuka bersih, kinerja cepat, dan fitur yang benar-benar membantu Anda meningkat.

---
Ketentuan Penggunaan (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "ms": """Kuasai algoritma CFOP dan tingkatkan masa penyelesaian anda dengan Deddal—aplikasi latihan speedcubing yang direka untuk membantu anda menjadi lebih pantas.

📊 JEJAKI KEMAJUAN ANDA
Pantau tahap kemahiran anda dan lihat algoritma mana yang telah anda kuasai. Jejaki peningkatan merentas kes F2L, OLL, dan PLL dengan analitik terperinci.

📚 PERPUSTAKAAN ALGORITMA LENGKAP
Akses semua kes CFOP—F2L, 2-Look OLL/PLL, dan set OLL/PLL lengkap. Layari pelbagai variasi algoritma setiap kes untuk mencari penyelesaian yang sesuai dengan gaya penyelesaian anda.

🎥 PEMBELAJARAN VISUAL
Tonton visualisasi algoritma langkah demi langkah. Fahami jujukan pergerakan, pelajari aliran pelaksanaan, dan bina ingatan otot dengan main balik interaktif.

🎯 LATIHAN FOKUS
Latih set kes tertentu, kerjakan titik lemah, dan kembangkan kelajuan pengiktirafan corak dengan mod latihan yang disasarkan.

Dibina oleh cubers, untuk cubers. Antara muka bersih, prestasi pantas, dan ciri yang benar-benar membantu anda bertambah baik.

---
Syarat Penggunaan (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "nl-NL": """Beheers CFOP-algoritmen en verbeter je oplos tijden met Deddal—de speedcubing trainingsapp ontworpen om je te helpen sneller te worden.

📊 VOLG JE VOORUITGANG
Monitor je vaardigheidsniveau en zie welke algoritmen je beheerst. Volg verbetering over F2L-, OLL- en PLL-gevallen met gedetailleerde analyses.

📚 COMPLETE ALGORITMEBIBLIOTHEEK
Toegang tot alle CFOP-gevallen—F2L, 2-Look OLL/PLL en volledige OLL/PLL-sets. Blader door meerdere algoritme variaties per geval om oplossingen te vinden die bij je oplosstijl passen.

🎥 VISUEEL LEREN
Bekijk stap-voor-stap algoritme visualisaties. Begrijp bewegingssequenties, leer uitvoeringsflow en bouw spiergeheugen op met interactief afspelen.

🎯 GERICHTE OEFENING
Train specifieke geval sets, werk aan zwakke punten en ontwikkel patroonherkenningssnelheid met gerichte oefen modi.

Gebouwd door cubers, voor cubers. Schone interface, snelle prestaties en functies die je echt helpen verbeteren.

---
Gebruiksvoorwaarden (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "no": """Mestre CFOP-algoritmer og forbedre løsningstidene dine med Deddal—speedcubing-treningsappen designet for å hjelpe deg med å bli raskere.

📊 SPOR FREMGANGEN DIN
Overvåk ferdighetsnivået ditt og se hvilke algoritmer du har mestret. Spor forbedring på tvers av F2L-, OLL- og PLL-tilfeller med detaljert analyse.

📚 KOMPLETT ALGORITMEBIBLIOTEK
Få tilgang til alle CFOP-tilfeller—F2L, 2-Look OLL/PLL og fullstendige OLL/PLL-sett. Bla gjennom flere algoritmevariasjoner per tilfelle for å finne løsninger som passer løsningsstilen din.

🎥 VISUELL LÆRING
Se trinn-for-trinn algoritmevisualiseringer. Forstå bevegelsessekvenser, lær utførelsesflyt og bygg muskelhukommelse med interaktiv avspilling.

🎯 FOKUSERT ØVELSE
Tren spesifikke tilfellessett, jobb med svake punkter og utvikle mønstergjenkjenningshastighet med målrettede øvingsmodi.

Bygget av cubere, for cubere. Rent grensesnitt, rask ytelse og funksjoner som faktisk hjelper deg med å forbedre deg.

---
Bruksvilkår (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "pl": """Opanuj algorytmy CFOP i popraw swoje czasy układania z Deddal—aplikacją treningową speedcubingu zaprojektowaną, aby pomóc ci przyspieszyć.

📊 ŚLEDŹ SWOJE POSTĘPY
Monitoruj poziom umiejętności i zobacz, które algorytmy opanowałeś. Śledź poprawę w przypadkach F2L, OLL i PLL za pomocą szczegółowej analityki.

📚 KOMPLETNA BIBLIOTEKA ALGORYTMÓW
Uzyskaj dostęp do wszystkich przypadków CFOP—F2L, 2-Look OLL/PLL i pełnych zestawów OLL/PLL. Przeglądaj wiele wariantów algorytmów na przypadek, aby znaleźć rozwiązania pasujące do twojego stylu układania.

🎥 NAUKA WIZUALNA
Oglądaj wizualizacje algorytmów krok po kroku. Zrozum sekwencje ruchów, naucz się przepływu wykonania i zbuduj pamięć mięśniową dzięki interaktywnemu odtwarzaniu.

🎯 SKONCENTROWANA PRAKTYKA
Trenuj konkretne zestawy przypadków, pracuj nad słabymi punktami i rozwijaj szybkość rozpoznawania wzorców za pomocą ukierunkowanych trybów ćwiczeń.

Stworzone przez cuberów, dla cuberów. Czysty interfejs, szybka wydajność i funkcje, które naprawdę pomagają ci się poprawiać.

---
Warunki użytkowania (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "ro": """Stăpânește algoritmii CFOP și îmbunătățește timpii de rezolvare cu Deddal—aplicația de antrenament pentru speedcubing concepută să te ajute să devii mai rapid.

📊 URMĂREȘTE-ȚI PROGRESUL
Monitorizează nivelul de abilități și vezi ce algoritmi ai stăpânit. Urmărește îmbunătățirea în cazurile F2L, OLL și PLL cu analize detaliate.

📚 BIBLIOTECĂ COMPLETĂ DE ALGORITMI
Accesează toate cazurile CFOP—F2L, 2-Look OLL/PLL și seturi complete OLL/PLL. Navighează prin multiple variații de algoritmi per caz pentru a găsi soluții care se potrivesc stilului tău de rezolvare.

🎥 ÎNVĂȚARE VIZUALĂ
Vizionează vizualizări de algoritmi pas cu pas. Înțelege secvențele de mișcări, învață fluxul de execuție și construiește memorie musculară cu redare interactivă.

🎯 PRACTICĂ FOCALIZATĂ
Antrenează seturi specifice de cazuri, lucrează la punctele slabe și dezvoltă viteza de recunoaștere a tiparelor cu moduri de practică țintite.

Construit de cuberi, pentru cuberi. Interfață curată, performanță rapidă și funcții care chiar te ajută să te îmbunătățești.

---
Termeni de utilizare (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "sk": """Ovládnite algoritmy CFOP a zlepšite časy riešenia s Deddal—aplikáciou na tréning speedcubingu navrhnutou na to, aby vám pomohla zrýchliť.

📊 SLEDUJTE SVOJ POKROK
Sledujte úroveň zručností a zistite, ktoré algoritmy ste ovládli. Sledujte zlepšenie v prípadoch F2L, OLL a PLL s podrobnou analytikou.

📚 KOMPLETNÁ KNIŽNICA ALGORITMOV
Získajte prístup ku všetkým prípadom CFOP—F2L, 2-Look OLL/PLL a úplným sadám OLL/PLL. Prechádzajte viacerými variantmi algoritmov na prípad a nájdite riešenia, ktoré zodpovedajú vášmu štýlu riešenia.

🎥 VIZUÁLNE UČENIE
Sledujte vizualizácie algoritmov krok za krokom. Pochopte postupnosti ťahov, naučte sa priebeh vykonávania a vybudujte svalovú pamäť s interaktívnym prehrávaním.

🎯 CIELENÝ TRÉNING
Trénujte konkrétne sady prípadov, pracujte na slabých miestach a rozvíjajte rýchlosť rozpoznávania vzorov s cielenými režimami tréningu.

Vytvorené cubermi, pre cuberov. Čisté rozhranie, rýchly výkon a funkcie, ktoré vám skutočne pomôžu zlepšiť sa.

---
Podmienky používania (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "sv": """Bemästra CFOP-algoritmer och förbättra dina lösningstider med Deddal—speedcubing-träningsappen designad för att hjälpa dig bli snabbare.

📊 SPÅRA DIN FRAMGÅNG
Övervaka din färdighetsnivå och se vilka algoritmer du har bemästrat. Spåra förbättring över F2L-, OLL- och PLL-fall med detaljerad analys.

📚 KOMPLETT ALGORITMBIBLIOTEK
Få tillgång till alla CFOP-fall—F2L, 2-Look OLL/PLL och kompletta OLL/PLL-uppsättningar. Bläddra igenom flera algoritmvariationer per fall för att hitta lösningar som matchar din lösningsstil.

🎥 VISUELL INLÄRNING
Titta på steg-för-steg-algoritmvisualiseringar. Förstå rörelsesekvenser, lär dig körningsflödet och bygg muskelminne med interaktiv uppspelning.

🎯 FOKUSERAD TRÄNING
Träna specifika falluppsättningar, arbeta med svaga punkter och utveckla mönsterigenkänningshastighet med riktade övningslägen.

Byggd av cubere, för cubere. Rent gränssnitt, snabb prestanda och funktioner som faktiskt hjälper dig att förbättras.

---
Användarvillkor (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "th": """ฝึกฝนอัลกอริทึม CFOP และปรับปรุงเวลาของคุณด้วย Deddal—แอปฝึกซ้อม speedcubing ที่ออกแบบมาเพื่อช่วยให้คุณเร็วขึ้น

📊 ติดตามความคืบหน้าของคุณ
ตรวจสอบระดับทักษะของคุณและดูว่าคุณเชี่ยวชาญอัลกอริทึมใดบ้าง ติดตามการปรับปรุงข้ามกรณี F2L, OLL และ PLL ด้วยการวิเคราะห์โดยละเอียด

📚 ไลบรารีอัลกอริทึมครบถ้วน
เข้าถึงกรณี CFOP ทั้งหมด—F2L, 2-Look OLL/PLL และชุด OLL/PLL ที่สมบูรณ์ เรียกดูรูปแบบอัลกอริทึมหลายรูปแบบต่อกรณีเพื่อค้นหาโซลูชันที่เหมาะกับสไตล์การแก้ของคุณ

🎥 การเรียนรู้ด้วยภาพ
ดูภาพแสดงอัลกอริทึมทีละขั้นตอน เข้าใจลำดับการเคลื่อนไหว เรียนรู้การไหลของการดำเนินการ และสร้างความจำของกล้ามเนื้อด้วยการเล่นแบบโต้ตอบ

🎯 การฝึกซ้อมแบบมุ่งเป้า
ฝึกชุดกรณีเฉพาะ แก้ไขจุดอ่อน และพัฒนาความเร็วในการจดจำรูปแบบด้วยโหมดฝึกซ้อมที่กำหนดเป้าหมาย

สร้างโดยคิวเบอร์ สำหรับคิวเบอร์ อินเทอร์เฟซที่สะอาด ประสิทธิภาพที่รวดเร็ว และคุณสมบัติที่ช่วยคุณพัฒนาจริงๆ

---
ข้อกำหนดการใช้งาน (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "tr": """CFOP algoritmalarında ustalaşın ve Deddal ile çözüm sürelerinizi geliştirin—daha hızlı olmanıza yardımcı olmak için tasarlanmış speedcubing eğitim uygulaması.

📊 İLERLEMENİZİ TAKİP EDİN
Beceri seviyenizi izleyin ve hangi algoritmalarda uzmanlaştığınızı görün. Detaylı analizlerle F2L, OLL ve PLL durumlarında gelişimi takip edin.

📚 EKSIKSIZ ALGORITMA KÜTÜPHANESI
Tüm CFOP durumlarına erişin—F2L, 2-Look OLL/PLL ve tam OLL/PLL setleri. Çözüm tarzınıza uygun çözümler bulmak için durum başına birden fazla algoritma varyasyonuna göz atın.

🎥 GÖRSEL ÖĞRENME
Adım adım algoritma görselleştirmelerini izleyin. Hareket dizilerini anlayın, yürütme akışını öğrenin ve interaktif oynatmayla kas hafızası oluşturun.

🎯 ODAKLI UYGULAMA
Belirli durum setlerini çalıştırın, zayıf noktalar üzerinde çalışın ve hedefli uygulama modlarıyla desen tanıma hızını geliştirin.

Cuber'lar tarafından, cuber'lar için yapıldı. Temiz arayüz, hızlı performans ve gerçekten gelişmenize yardımcı olan özellikler.

---
Kullanım Koşulları (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "uk": """Опануйте алгоритми CFOP і покращте час збирання з Deddal—додатком для тренувань зі спідкубінгу, розробленим, щоб допомогти вам стати швидшими.

📊 ВІДСТЕЖУЙТЕ ПРОГРЕС
Відстежуйте рівень навичок і дивіться, які алгоритми ви опанували. Відстежуйте покращення у випадках F2L, OLL і PLL з детальною аналітикою.

📚 ПОВНА БІБЛІОТЕКА АЛГОРИТМІВ
Отримайте доступ до всіх випадків CFOP—F2L, 2-Look OLL/PLL та повних наборів OLL/PLL. Переглядайте кілька варіантів алгоритмів для кожного випадку, щоб знайти рішення, що відповідають вашому стилю збирання.

🎥 ВІЗУАЛЬНЕ НАВЧАННЯ
Дивіться покрокові візуалізації алгоритмів. Розумійте послідовності ходів, вивчайте потік виконання та будуйте м'язову пам'ять з інтерактивним відтворенням.

🎯 ЦІЛЕСПРЯМОВАНА ПРАКТИКА
Тренуйте конкретні набори випадків, працюйте над слабкими місцями та розвивайте швидкість розпізнавання патернів з цільовими режимами практики.

Створено к'юберами, для к'юберів. Чистий інтерфейс, швидка продуктивність та функції, які справді допомагають покращитися.

---
Умови використання (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",

    "vi": """Làm chủ thuật toán CFOP và cải thiện thời gian giải của bạn với Deddal—ứng dụng đào tạo speedcubing được thiết kế để giúp bạn nhanh hơn.

📊 THEO DÕI TIẾN TRÌNH
Theo dõi mức độ kỹ năng và xem bạn đã thành thạo thuật toán nào. Theo dõi cải thiện qua các trường hợp F2L, OLL và PLL với phân tích chi tiết.

📚 THƯ VIỆN THUẬT TOÁN ĐẦY ĐỦ
Truy cập tất cả các trường hợp CFOP—F2L, 2-Look OLL/PLL và bộ OLL/PLL đầy đủ. Duyệt nhiều biến thể thuật toán mỗi trường hợp để tìm giải pháp phù hợp với phong cách giải của bạn.

🎥 HỌC TẬP TRỰC QUAN
Xem hình ảnh hóa thuật toán từng bước. Hiểu chuỗi di chuyển, học luồng thực thi và xây dựng trí nhớ cơ bắp với phát lại tương tác.

🎯 LUYỆN TẬP TẬP TRUNG
Luyện tập các bộ trường hợp cụ thể, khắc phục điểm yếu và phát triển tốc độ nhận dạng mẫu với các chế độ luyện tập có mục tiêu.

Được xây dựng bởi cubers, cho cubers. Giao diện sạch sẽ, hiệu suất nhanh và các tính năng thực sự giúp bạn cải thiện.

---
Điều khoản Sử dụng (EULA): https://www.apple.com/legal/internet-services/itunes/dev/stdeula/
""",
}

def main():
    metadata_dir = Path(__file__).parent

    updated_count = 0
    skipped_count = 0

    for locale, content in DESCRIPTIONS.items():
        desc_file = metadata_dir / locale / "description.txt"

        if not desc_file.parent.exists():
            print(f"⚠️  Skipping {locale}: directory not found")
            skipped_count += 1
            continue

        # Write aligned description
        with open(desc_file, 'w', encoding='utf-8') as f:
            f.write(content)

        updated_count += 1
        print(f"✅ Updated {locale}/description.txt")

    print(f"\n🎉 Complete: {updated_count} updated, {skipped_count} skipped")
    print("\nAll descriptions now aligned with Option B: Concise & Punchy")
    print("✅ Covers all 4 enabled tabs: Home, Library, Progress, Practice")
    print("✅ Clear outcome focus: 'get faster'")
    print("✅ Emoji for visual hierarchy")
    print("✅ ~900 chars (22% of 4000 char limit)")

if __name__ == "__main__":
    main()
