

Résumé Exécutif

Une analyse approfondie des tendances actuelles dans le développement des grands modèles de langage (LLM) révèle une contrainte imminente et critique : l'épuisement potentiel du stock de données textuelles publiques générées par l'homme. Selon les projections basées sur les tendances de croissance actuelles, la demande en données d'entraînement dépassera l'offre disponible entre 2026 et 2032, avec une date médiane en 2028. Ce goulot d'étranglement est dû à la croissance exponentielle de la taille des jeux de données, qui augmente d'environ 2,4 fois par an (0,38 ordres de grandeur), tandis que le stock effectif de données textuelles de haute qualité est estimé à environ 4x10¹⁴ tokens.

Le phénomène de "surentraînement" (overtraining), une pratique visant à améliorer l'efficacité des modèles en inférence, pourrait accélérer cette échéance d'un an ou deux en augmentant la consommation de données.

Face à cette limitation, la progression future de l'IA dépendra de l'adoption de nouvelles stratégies. Les pistes les plus prometteuses incluent :

1. **La génération de données synthétiques** : Utiliser les modèles d'IA eux-mêmes pour créer de nouvelles données d'entraînement à grande échelle.

2. **L'apprentissage par transfert et multimodal** : Exploiter des domaines riches en données non textuelles (images, vidéos, données génomiques) pour entraîner les modèles de langage.

3. **L'amélioration de l'efficacité des données** : Les progrès algorithmiques continus permettent d'obtenir de meilleures performances avec moins de données, compensant potentiellement la stagnation du stock.

Bien que l'utilisation de données non publiques (issues des réseaux sociaux et de la messagerie instantanée) puisse temporairement augmenter le stock disponible, elle soulève des préoccupations majeures en matière de confidentialité et de légalité, qui pourraient l'emporter sur ses avantages. En conclusion, si le paradigme actuel basé sur le texte public humain atteint ses limites au cours de cette décennie, il est probable que des sources de données alternatives permettront à la mise à l'échelle des systèmes d'IA de se poursuivre.

--------------------------------------------------------------------------------

1. Le Goulot d'Étranglement des Données : Projections et Échéances

L'analyse centrale du document porte sur la confrontation entre la demande croissante en données pour l'entraînement des LLM et le stock fini de données textuelles humaines publiques disponibles. Le point d'intersection de ces deux tendances marque le début d'un goulot d'étranglement majeur pour le développement de l'IA.

1.1. Projection de la Demande en Données d'Entraînement

La taille des jeux de données utilisés pour entraîner les LLM de pointe a connu une croissance rapide et constante.

• **Croissance Historique** : Une régression linéaire sur les données des LLM publiés entre 2010 et 2024 montre une croissance médiane de **0,38 ordres de grandeur par an** (OOM/an), soit une multiplication par 2,4 chaque année.

• **Modèles Récents** : Des modèles récents comme Llama 3 et DBRX ont été entraînés sur des jeux de données de 15T et 12T tokens respectivement, confirmant cette tendance à la hausse.

• **Projection Basée sur la Puissance de Calcul** : Pour tenir compte des limites physiques et économiques, un second modèle de projection est utilisé. Il lie la taille des données à la croissance future de la puissance de calcul disponible pour l'entraînement, en supposant une mise à l'échelle optimale (environ 20 tokens par paramètre de modèle). Cette projection suit la tendance historique jusqu'en 2030 environ, puis ralentit.

• **Projection Finale** : Le modèle final est un mélange à parts égales des projections historiques et de celles basées sur la puissance de calcul, afin de représenter l'incertitude.

1.2. Estimation du Stock de Données Textuelles Humaines

Le "stock de données" représente la quantité totale de données textuelles publiques générées par l'homme et disponibles pour l'entraînement.

• **Source Principale** : Le web indexé, dont la taille est estimée en utilisant l'index de Google comme proxy. L'analyse suggère que l'index de Google contient environ **250 milliards de pages web**.

• **Taille Brute** : En se basant sur la quantité moyenne de texte par page web (environ 7000 octets de texte brut) extraite de Common Crawl, le stock brut de tokens sur le web indexé est estimé à **510 billions (trillions) de tokens** (510T).

• **Taux de Croissance du Stock** : La croissance du stock est difficile à estimer, mais elle est modélisée avec un intervalle de confiance de 0 % à 10 % par an, tenant compte de facteurs contradictoires comme la croissance du nombre d'utilisateurs d'Internet et le phénomène de "link rot" (liens morts).

1.3. Ajustements pour la Qualité et la Répétition des Données

Le stock brut de 510T tokens n'est pas directement utilisable. Des ajustements sont nécessaires pour refléter la réalité de l'entraînement des LLM.

• **Ajustement de Qualité** : Les données de faible qualité sont filtrées, car elles ne contribuent pas à la performance du modèle. Des études empiriques montrent que seulement **10 % à 40 % des données web dédupliquées** peuvent être utilisées sans compromettre significativement les performances.

• **Ajustement pour la Répétition (Multi-Epoch)** : L'entraînement sur plusieurs "époques" (répétitions des mêmes données) peut augmenter la "taille effective" du jeu de données. Cet effet est estimé comme pouvant multiplier la taille du jeu de données par un facteur de **3 à 5x** de manière efficace.

• **Stock Effectif Final** : En combinant ces ajustements, la projection finale du stock de données effectif utilisé pour la modélisation est d'environ **4x10¹⁴ tokens (400T tokens)**.

1.4. Date Prévue de l'Épuisement du Stock

En superposant les projections de la demande et du stock effectif, une date d'épuisement peut être estimée.

• **Scénario de Base (Optimal en Calcul)** : La date médiane à laquelle la taille des jeux de données atteindra le stock total effectif est **2028**. L'intervalle de confiance à 95 % se situe entre 2026 et 2032. À ce stade, l'entraînement des modèles de pointe nécessitera environ 5x10²⁸ FLOP.

• **Scénario avec Surentraînement (Overtraining)** : De nombreux développeurs choisissent de "surentraîner" leurs modèles (utiliser plus de données par rapport à la taille du modèle que ce qui est optimal en termes de calcul d'entraînement) pour améliorer l'efficacité en inférence. Un scénario de surentraînement de 5x est jugé plausible. Dans ce cas, le goulot d'étranglement des données serait atteint **environ un an plus tôt**, à un niveau de calcul d'entraînement de ~6x10²⁷ FLOP.


![[CleanShot 2025-11-03 at 08.46.24.png]]
_Figure : Projections du stock effectif de texte public et de la taille des jeux de données utilisés pour les LLM. L'intersection indique l'année médiane (2028) où le stock devrait être entièrement utilisé. La ligne pointillée montre comment un surentraînement de 5x accélère cette échéance._

--------------------------------------------------------------------------------

2. Analyse Détaillée des Stocks de Données

L'étude quantifie plusieurs sources de données potentielles, exprimées en équivalents de tokens textuels. Les estimations sont présentées avec des intervalles de confiance à 95 % pour refléter l'incertitude.

|   |   |   |
|---|---|---|
|Source de Données|Estimation Médiane (Tokens)|Intervalle de Confiance à 95%|
|**Common Crawl**|130T|[100T, 260T]|
|**Web Indexé**|510T|[130T, 2100T]|
|**Web Entier (incl. Deep Web)**|3100T|[1900T, 5200T]|
|**Images**|300T|N/A|
|**Vidéo**|1350T|N/A|

**Méthodologies d'Estimation :**

• **Web Indexé** : L'estimation est dérivée de la taille de l'index de Google (~250 milliards de pages) et de la quantité moyenne de texte par page web, telle qu'analysée dans les archives de Common Crawl.

• **Population Internet** : Un modèle alternatif estime la production de données en fonction de la croissance historique et projetée du nombre d'utilisateurs d'Internet dans le monde, en supposant un taux de production de données par utilisateur constant. Cette méthode aboutit à une estimation plus élevée (3100T tokens), car elle inclut le "deep web" (contenu non indexé par les moteurs de recherche) et sert donc de borne supérieure.

--------------------------------------------------------------------------------

3. Stratégies pour Dépasser le Goulot d'Étranglement

Bien que l'épuisement du texte public humain semble inévitable, plusieurs stratégies pourraient permettre de poursuivre la mise à l'échelle des modèles d'IA.

3.1. Données Générées par l'IA (Données Synthétiques)

Cette approche est considérée comme l'une des plus prometteuses en raison de son potentiel d'échelle quasi illimité.

• **Potentiel** : OpenAI générerait à lui seul 100 milliards de mots par jour, ce qui équivaut en un an à une quantité de données proche du stock de haute qualité de Common Crawl.

• **Succès Actuels** : Les données synthétiques ont démontré leur efficacité dans des domaines où les résultats sont facilement vérifiables, comme les mathématiques, la programmation et les jeux (ex: AlphaZero, AlphaGeometry).

• **Défis** : L'entraînement itératif sur des données générées peut conduire à un "effondrement du modèle" (_model collapse_), où les modèles oublient la distribution originale des données humaines et produisent des résultats de plus en plus homogènes et irréalistes. La recherche se concentre sur l'atténuation de ce risque, notamment en mélangeant données synthétiques et humaines.

3.2. Apprentissage Multimodal et par Transfert

Cette stratégie consiste à exploiter des données provenant d'autres modalités ou domaines.

• **Images et Vidéos** : Bien que les stocks d'images (300T tokens-équivalents) et de vidéos (1350T tokens-équivalents) sur le web soient importants, ils ne sont pas assez vastes pour empêcher à eux seuls un goulot d'étranglement à long terme.

• **Domaines Riches en Données** : D'autres sources, comme les bases de données scientifiques (génomique, astronomie), pourraient fournir des ordres de grandeur de données supplémentaires. Par exemple, la production de données génomiques est estimée entre 2 et 40 millions de téraoctets par an d'ici 2025.

• **Incertitude** : La faisabilité et l'efficacité du transfert de connaissances de ces domaines vers les modèles de langage restent un domaine de recherche actif. Il n'est pas clair dans quelle mesure ces données présentent une synergie avec le texte.

3.3. Utilisation de Données Non Publiques

Le "deep web" et les plateformes de communication privées représentent un vaste réservoir de données textuelles.

• **Volume** : Les plateformes de contenu fermées (Facebook, Instagram, etc.) et les applications de messagerie instantanée (WhatsApp, Messenger) contiennent chacune environ un quadrillion de tokens. L'utilisation combinée de ces sources pourrait augmenter le stock total de données à 3 quadrillions de tokens, retardant le goulot d'étranglement d'environ **un an et demi**.

• **Obstacles Majeurs** :

   1. **Confidentialité** : L'utilisation de ces données constituerait une violation grave de la vie privée des utilisateurs.

   2. **Légalité** : Elle ferait probablement face à des contestations juridiques importantes.

   3. **Qualité** : La qualité du contenu des réseaux sociaux est probablement inférieure à celle du contenu web.

   4. **Fragmentation** : Les données sont réparties entre des acteurs concurrents, rendant leur agrégation peu probable.

3.4. Techniques d'Efficacité des Données

Les progrès algorithmiques permettent aux modèles d'atteindre des performances équivalentes avec moins de calcul et, par extension, moins de données.

• **Taux de Progrès** : L'efficacité des algorithmes pour les LLM s'améliore à un rythme de **0,4 OOM/an**. Cela signifie que chaque année, il faut environ 0,4 ordres de grandeur de calcul en moins pour atteindre un niveau de performance donné.

• **Impact** : Il est possible que ces gains d'efficacité se poursuivent à un rythme suffisant pour compenser la stagnation des stocks de données.

--------------------------------------------------------------------------------

4. Conclusion et Implications

L'analyse mène à une double conclusion :

1. **Une Fin de Paradigme** : Le paradigme actuel, qui repose sur la mise à l'échelle de LLM en utilisant des quantités toujours plus grandes de texte public humain, n'est pas durable et devrait atteindre une limite critique au cours de la prochaine décennie.

2. **L'Émergence d'Alternatives** : Il est très probable que des sources de données alternatives (synthétiques, multimodales) et des améliorations continues de l'efficacité des données soient adoptées avant que ce goulot d'étranglement ne stoppe complètement les progrès, permettant ainsi à la mise à l'échelle des systèmes d'IA de se poursuivre.

Le document souligne également les implications éthiques et sociétales. La pratique de l'extraction de données à grande échelle soulève des questions de justice et de compensation pour les créateurs de contenu. De plus, l'utilisation potentielle de données non publiques issues de plateformes sociales et de messageries présente des risques de confidentialité et de sécurité si importants qu'ils pourraient l'emporter sur les avantages potentiels en matière de performance des modèles.