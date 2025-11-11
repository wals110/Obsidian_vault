

1. Introduction : La Fin d'une Ère de Mise à l'Échelle ?

Les progrès fulgurants des grands modèles de langage (LLM) au cours des dernières années ont été principalement alimentés par une stratégie simple mais puissante : la mise à l'échelle. Cette approche consiste à entraîner des modèles de plus en plus grands sur des volumes toujours plus massifs de données textuelles humaines, majoritairement issues du web public. L'importance stratégique de cette analyse est d'évaluer la durabilité de ce paradigme en répondant à une question critique : les données textuelles publiques disponibles, qui ont jusqu'ici soutenu cette croissance, seront-elles bientôt épuisées ?

La conclusion centrale de cette analyse est sans équivoque : si les tendances actuelles de développement des LLM se maintiennent, le stock de données textuelles humaines publiques de haute qualité sera entièrement utilisé pour l'entraînement des modèles entre 2026 et 2032. Cette projection place le secteur de l'intelligence artificielle face à un goulot d'étranglement potentiel qui pourrait redéfinir les stratégies de R&D pour la prochaine décennie.

Pour parvenir à cette prévision, une modélisation rigoureuse de l'offre et de la demande de données a été élaborée, une méthodologie que nous allons maintenant détailler.

2. Méthodologie : Modélisation de l'Offre et de la Demande de Données

Pour prévoir la date d'épuisement des données, il est essentiel de modéliser deux variables clés : le stock total de données disponibles (l'offre) et la taille croissante des ensembles de données utilisés pour l'entraînement des modèles de pointe (la demande). La confrontation de ces deux trajectoires permet de déterminer leur point d'intersection, qui correspond au moment où la demande dépassera l'offre disponible. La rigueur de cette modélisation est fondamentale pour la crédibilité des projections qui en découlent.

2.1. Quantification du Stock de Données : L'Offre Disponible

La méthodologie d'estimation du stock total de données textuelles publiques se concentre sur le "web indexé" comme principale source, car il constitue la base de la plupart des grands corpus d'entraînement. Pour quantifier sa taille, l'index de Google, le moteur de recherche le plus utilisé au monde, est utilisé comme un proxy fiable.

L'analyse aboutit à une estimation médiane de **250 milliards de pages web** contenues dans cet index. En traduisant ce volume en jetons (_tokens_), l'unité de base utilisée pour l'entraînement des modèles, on obtient un stock brut d'environ **510 billions (trillion) de jetons** (avec un intervalle de confiance à 95 % compris entre 130 et 2 100 billions de jetons) pour l'ensemble du web indexé. Cependant, des incertitudes demeurent quant au taux de croissance annuel de ce stock. Compte tenu des preuves contradictoires, un intervalle de confiance prudent entre 0 % et 10 % par an est utilisé dans le modèle.

2.2. Ajustement du Stock Effectif : Qualité et Répétition des Données

Le stock brut de données ne représente pas la quantité réellement utilisable pour un entraînement performant. Il est donc nécessaire d'introduire le concept de "stock effectif", qui tient compte de deux facteurs cruciaux : la qualité des données et la pratique de l'entraînement multi-époques.

L'impact de la **qualité des données** est considérable. Les techniques de filtrage modernes, qui éliminent les textes de faible qualité pour optimiser la performance des modèles, réduisent le stock total de manière significative. Les études montrent que seules les données de meilleure qualité sont conservées, ce qui représente entre **10 % et 40 %** du stock initialement dédupliqué.

Inversement, la pratique de l'**entraînement multi-époques**, qui consiste à présenter plusieurs fois les mêmes données au modèle pendant son entraînement, peut augmenter la taille _effective_ d'un ensemble de données. Cette technique permet de mieux exploiter les corpus de haute qualité, avec un gain maximal estimé entre **3x et 5x** la taille du corpus initial, une fourchette plus réaliste que l'estimation théorique de 3x à 15x, car les gains les plus élevés impliqueraient des procédures d'entraînement inefficaces qui ne correspondent pas aux pratiques courantes.

2.3. Projection de la Demande en Données : Une Croissance Exponentielle

Pour projeter la croissance future de la taille des ensembles de données d'entraînement, une double approche a été adoptée afin de capturer l'ensemble des dynamiques en jeu.

1. **Projection basée sur les tendances historiques :** L'analyse des modèles de langage publiés depuis 2010 révèle un taux de croissance médian de **0,38 ordre de grandeur par an**. Cela équivaut à une multiplication de la taille des ensembles de données par un facteur de **2,4 chaque année**.

2. **Projection basée sur la croissance de la puissance de calcul :** Cette seconde approche part du constat que la croissance exponentielle historique de la taille des ensembles de données est insoutenable à long terme. Elle propose donc un modèle plus réaliste en liant la croissance des données à celle, plus contrainte, de la puissance de calcul disponible pour l'entraînement. Cette projection est contrainte par les limites physiques et économiques (production de puces, approvisionnement énergétique) et s'appuie sur les lois de mise à l'échelle neuronale (comme la loi de Chinchilla).

La projection finale est une combinaison pondérée de ces deux modèles afin de refléter l'incertitude sur la pérennité des tendances actuelles. C'est en confrontant cette projection de la demande avec les estimations de l'offre effective que l'on peut déterminer un calendrier de la pénurie.

3. Projections Clés : Le Calendrier de la Pénurie

La convergence des modèles d'offre et de demande permet de répondre à la question centrale de cette analyse : à quel moment le développement des grands modèles de langage consommera-t-il l'intégralité du stock effectif de données textuelles publiques ? Les résultats indiquent une échéance plus proche que beaucoup ne l'imaginent.

3.1. Le Point de Croisement : Épuisement Prévu d'ici 2028

La conclusion principale de la projection est que l'année médiane où les ensembles de données d'entraînement des modèles de pointe atteindront la taille du stock de données effectif est **2028**. D'ici **2032**, cet épuisement devient "très probable" selon le modèle. Ce point de croisement correspond à des modèles nécessitant une puissance de calcul d'entraînement d'environ **5e28 FLOP** (opérations en virgule flottante au total pour l'entraînement), en supposant un entraînement optimisé du point de vue du calcul.

3.2. L'Impact Accélérateur du Sur-entraînement (Overtraining)

Le calendrier pourrait être encore plus serré en raison de la pratique du sur-entraînement (_overtraining_). Cette technique consiste à utiliser un ratio jetons/paramètre plus élevé que celui considéré comme optimal du point de vue du calcul (défini par exemple par la loi de Chinchilla à environ 20 jetons par paramètre), souvent dans le but d'améliorer l'efficacité du modèle en phase d'inférence (son utilisation pratique).

L'étude évalue qu'un sur-entraînement raisonnable de **5x** par rapport aux normes optimales avancerait la date du goulot d'étranglement des données d'environ **un an**. Cette pratique, motivée par des considérations économiques liées au coût d'utilisation des modèles, accélère donc la consommation du stock fini de données publiques. Face à ce goulot d'étranglement imminent, l'exploration de solutions alternatives devient une priorité stratégique.

4. Au-delà des Données Publiques : Analyse des Stratégies Alternatives

Bien que la projection d'un épuisement des données publiques soit préoccupante, elle ne signifie pas la fin de la progression de l'IA. Elle signale plutôt la nécessité d'un changement de paradigme. Cette section évalue de manière critique la viabilité et les implications des principales stratégies envisagées pour surmonter cette limitation.

4.1. Données Synthétiques Générées par l'IA

Les données synthétiques, générées par des modèles d'IA eux-mêmes, offrent un potentiel quasi illimité pour augmenter le volume de données d'entraînement. Cependant, cette approche présente des défis critiques. Le plus notable est le risque d'**"effondrement du modèle" (****model collapse****)**, un phénomène où les modèles entraînés sur leurs propres générations oublient progressivement la distribution originale des données humaines et produisent des résultats de plus en plus homogènes et dégradés. Si cette stratégie est prometteuse dans des domaines où les résultats sont facilement vérifiables (mathématiques, programmation), son application au langage naturel, plus subjectif et complexe, reste un défi majeur.

4.2. Apprentissage Multimodal et par Transfert

Une autre stratégie consiste à élargir le stock de données en y intégrant des modalités non textuelles (images, vidéos) ou en exploitant des domaines riches en données structurées. Bien que les stocks actuels d'images et de vidéos soient vastes, les estimations suggèrent qu'ils **ne sont pas suffisants à eux seuls** pour empêcher un goulot d'étranglement à long terme. Au-delà de ces modalités, des stocks de données potentiellement mille fois plus importants existent dans des domaines scientifiques comme la génomique ou l'astronomie. Cependant, leur utilité et leur synergie avec les tâches linguistiques restent des questions ouvertes qui nécessitent des recherches approfondies.

4.3. Exploitation des Données Non Publiques

D'immenses réservoirs de données textuelles existent en dehors du web public, principalement au sein du "deep web", des plateformes de médias sociaux et des applications de messagerie instantanée. L'utilisation de ces données pourrait théoriquement augmenter le stock total jusqu'à 3 quadrillions de jetons. Toutefois, cet apport colossal ne **retarderait le goulot d'étranglement que d'environ un an et demi**. De plus, leur exploitation se heurte à des obstacles majeurs :

• **Confidentialité :** L'entraînement sur des conversations privées ou des contenus non publics constituerait une violation grave de la vie privée des utilisateurs.

• **Légalité :** Des défis juridiques importants se poseraient concernant le consentement et les droits d'utilisation de ces données.

• **Qualité :** La qualité de ces données est probablement inférieure à celle du contenu web soigneusement sélectionné et filtré.

• **Fragmentation :** Les données sont réparties entre de multiples entreprises concurrentes, rendant un accès unifié et à grande échelle très improbable.

4.4. Amélioration de l'Efficacité Algorithmique

La force la plus prometteuse qui s'oppose à la pénurie de données est l'amélioration continue de l'efficacité algorithmique. Les progrès dans les architectures de modèles, les techniques d'entraînement et l'optimisation permettent d'obtenir de meilleures performances avec moins de données. Le taux d'amélioration de l'efficacité est estimé à **0,4 ordre de grandeur par an** (avec un intervalle de confiance à 95 % de 0,1 à 0,8). Concrètement, cela signifie que chaque année, il faut environ 2,5 fois moins de calcul (et donc potentiellement moins de données) pour atteindre le même niveau de performance qu'un modèle de l'année précédente.

5. Conclusion : Un Changement de Paradigme pour l'IA

Les conclusions de cette analyse peuvent être synthétisées en deux points principaux. Premièrement, il est clair que le paradigme actuel, basé sur la mise à l'échelle de modèles de plus en plus grands avec des données textuelles humaines publiques, atteindra ses limites physiques avant la fin de la décennie. La croissance exponentielle de la demande ne peut se poursuivre indéfiniment face à une ressource finie.

Deuxièmement, il est probable que des sources de données alternatives, telles que les données synthétiques ou l'apprentissage par transfert à partir d'autres modalités, seront adoptées à grande échelle avant que ce point de rupture ne soit atteint. Cette transition permettra à la mise à l'échelle de se poursuivre, mais elle marquera un changement de paradigme significatif pour le domaine de l'IA, passant d'une ère d'abondance de données publiques à une ère d'ingénierie des données et d'efficacité algorithmique.

Il convient de souligner l'incertitude inhérente à ces projections à long terme dans un domaine qui évolue aussi rapidement. L'importance de la recherche future sera donc cruciale pour quantifier l'efficacité des nouvelles méthodes, identifier les sources de données les plus prometteuses et développer les techniques qui permettront de "faire plus avec moins".

