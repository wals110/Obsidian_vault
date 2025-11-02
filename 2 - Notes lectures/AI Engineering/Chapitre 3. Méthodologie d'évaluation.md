

Plus l'IA est utilisée, plus le risque d'échecs catastrophiques augmente. Nous avons déjà constaté de nombreux échecs depuis l'apparition des modèles de base. Un homme s'est suicidé après avoir été [incité par un chatbot à le faire](https://oreil.ly/tMH21) . Des avocats ont présenté [de faux témoignages, prétendument hallucinés par une IA](https://oreil.ly/-0Iq1) . Air Canada a été condamnée à verser des dommages et intérêts lorsque son chatbot [a fourni de fausses informations à un passager](https://oreil.ly/kKWnZ) . Sans moyen de contrôler la qualité des résultats de l'IA, les risques qu'elle comporte pourraient, dans de nombreuses applications, surpasser ses avantages.

Alors que les équipes s'empressent d'adopter l'IA, beaucoup réalisent rapidement que le principal obstacle à la concrétisation des applications d'IA est l'évaluation. Pour certaines applications, la mise au point de cette évaluation peut représenter la majeure partie des efforts de développement [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id871)

Compte tenu de l'importance et de la complexité de l'évaluation, cet ouvrage lui consacre deux chapitres. Le premier chapitre présente différentes méthodes d'évaluation des modèles ouverts, leur fonctionnement et leurs limites. Le chapitre suivant explique comment utiliser ces méthodes pour sélectionner les modèles adaptés à votre application et construire un pipeline d'évaluation.

Bien que l'évaluation soit abordée dans des chapitres dédiés, elle doit être envisagée dans le contexte d'un système global, et non isolément. L'évaluation vise à atténuer les risques et à révéler les opportunités. Pour atténuer les risques, il est essentiel d'identifier les points faibles du système et d'adapter l'évaluation en conséquence. Souvent, cela peut nécessiter une refonte du système afin d'améliorer la visibilité de ses défaillances. Sans une compréhension claire de ces défaillances, aucun outil ni indicateur d'évaluation ne pourra garantir la robustesse du système.

Avant d'aborder les méthodes d'évaluation, il est important de reconnaître les difficultés liées à l'évaluation des modèles de base. Face à cette complexité, beaucoup se fient au _bouche-à_ [-](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id872) oreille (par exemple, quelqu'un affirme que le modèle X est bon) ou à une appréciation visuelle des résultats. [Cela](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id873) accroît les risques et ralentit l'itération des applications. Il est donc nécessaire d'investir dans une évaluation systématique afin d'obtenir des résultats plus fiables.

Étant donné que de nombreux modèles de base comportent un module de langage, ce chapitre propose un aperçu des métriques utilisées pour évaluer ces modèles, notamment l'entropie croisée et la perplexité. Ces métriques sont essentielles pour guider l'entraînement et l'ajustement des modèles de langage et sont fréquemment utilisées dans de nombreuses méthodes d'évaluation.

L'évaluation des modèles de base est particulièrement complexe en raison de leur nature ouverte, et je présenterai les meilleures pratiques pour y parvenir. Le recours à des évaluateurs humains demeure une option nécessaire pour de nombreuses applications. Cependant, compte tenu de la lenteur et du coût des annotations humaines, l'objectif est d'automatiser le processus. Cet ouvrage se concentre sur l'évaluation automatique, qui comprend à la fois l'évaluation exacte et l'évaluation subjective.

L'intelligence artificielle (IA) en tant que juge, ou évaluation subjective, est une approche émergente. Elle consiste à utiliser l'IA pour évaluer les réponses d'autres IA. Le caractère subjectif de cette évaluation tient au fait que le score dépend du modèle et des consignes utilisés par l'IA. Bien que cette approche gagne rapidement du terrain dans le secteur, elle suscite également une vive opposition de la part de ceux qui estiment que l'IA n'est pas suffisamment fiable pour cette tâche importante. Je suis particulièrement enthousiaste à l'idée d'approfondir ce sujet, et j'espère que vous le serez aussi.

# Les défis de l'évaluation des modèles de fondation

L'évaluation des modèles d'apprentissage automatique a toujours été complexe. Avec l'introduction des modèles de base, elle l'est devenue encore davantage. Plusieurs raisons expliquent pourquoi l'évaluation des modèles de base est plus difficile que celle des modèles d'apprentissage automatique traditionnels.

Premièrement, plus les modèles d'IA deviennent intelligents, plus il est difficile de les évaluer. La plupart des gens peuvent déceler une erreur dans la résolution d'un problème mathématique d'un élève de primaire. Rares sont ceux qui peuvent en faire autant pour un problème mathématique de niveau doctoral. [Il](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id874) est facile de repérer un mauvais résumé de livre s'il est incompréhensible, mais beaucoup plus difficile s'il est cohérent. Pour valider la qualité d'un résumé, il est parfois nécessaire de lire le livre au préalable. Ceci nous amène à une conséquence : l'évaluation peut s'avérer beaucoup plus chronophage pour les tâches complexes. On ne peut plus se contenter d'évaluer une réponse sur sa seule sonorité. Il faut également vérifier les faits, raisonner et même faire appel à une expertise du domaine.

Deuxièmement, la nature ouverte des modèles de base remet en cause l'approche traditionnelle d'évaluation d'un modèle par rapport à des données de référence. En apprentissage automatique traditionnel, la plupart des tâches sont fermées. Par exemple, un modèle de classification ne peut produire que des résultats appartenant aux catégories attendues. Pour évaluer un tel modèle, on compare ses résultats aux résultats attendus. Si le résultat attendu est de la catégorie X, mais que le résultat du modèle est de la catégorie Y, le modèle est erroné. En revanche, pour une tâche ouverte, à une entrée donnée, il existe un nombre considérable de réponses correctes possibles. Il est donc impossible de constituer une liste exhaustive de résultats corrects à utiliser comme référence.

Troisièmement, la plupart des modèles de base sont considérés comme des boîtes noires, soit parce que leurs fournisseurs choisissent de ne pas divulguer leurs détails, soit parce que les développeurs d'applications n'ont pas l'expertise nécessaire pour les comprendre. Des détails tels que l'architecture du modèle, les données d'entraînement et le processus d'entraînement peuvent révéler beaucoup de choses sur ses forces et ses faiblesses. Sans ces détails, on ne peut évaluer un modèle qu'en observant ses résultats.

Dans le même temps, les bancs d'essai d'évaluation disponibles publiquement se sont révélés inadéquats pour évaluer les modèles de base. Idéalement, ces bancs d'essai devraient couvrir l'ensemble des capacités des modèles. À mesure que l'IA progresse, les bancs d'essai doivent évoluer. Un banc d'essai est considéré comme saturé pour un modèle dès que celui-ci atteint le score parfait. Or, avec les modèles de base, la saturation des bancs d'essai est rapide. Le banc d'essai [GLUE](https://arxiv.org/abs/1804.07461) (General Language Understanding Evaluation), publié en 2018, a atteint la saturation en seulement un an, ce qui a nécessité l'introduction de [SuperGLUE](https://arxiv.org/abs/1905.00537) en 2019. De même, [NaturalInstructions](https://arxiv.org/abs/2104.08773) (2021) a été remplacé par [Super-NaturalInstructions](https://arxiv.org/abs/2204.07705) (2022). [MMLU](https://arxiv.org/abs/2009.03300) (2020), un banc d'essai performant sur lequel s'appuyaient de nombreux modèles de base initiaux, a été largement remplacé par [MMLU-Pro](https://arxiv.org/abs/2406.01574) (2024).

Enfin, et surtout, le champ d'application de l'évaluation s'est élargi pour les modèles à usage général. Pour les modèles dédiés à une tâche spécifique, l'évaluation consiste à mesurer leurs performances sur la tâche pour laquelle ils ont été entraînés. En revanche, pour les modèles à usage général, l'évaluation ne se limite pas à l'évaluation de leurs performances sur des tâches connues, mais vise également à découvrir de nouvelles tâches qu'ils peuvent accomplir, y compris celles qui dépassent les capacités humaines. L'évaluation se voit ainsi confier la responsabilité supplémentaire d'explorer le potentiel et les limites de l'IA.

La bonne nouvelle est que les nouveaux défis de l'évaluation ont suscité de nombreuses nouvelles méthodes et de nouveaux référentiels. [La figure 3-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_1_1730150757025034) montre que le nombre d'articles publiés sur l'évaluation des LLM a connu une croissance exponentielle chaque mois au cours du premier semestre 2023, passant de 2 articles par mois à près de 35 articles par mois.

![Un graphique avec une ligne ascendante. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0301.png)

###### Figure 3-1. L'évolution des articles d'évaluation des LLM au fil du temps. Image tirée de [Chang et al. (2023)](https://arxiv.org/abs/2307.03109) .

Dans ma propre analyse des [1 000 principaux dépôts liés à l’IA sur GitHub](https://huyenchip.com/llama-police) , classés par nombre d’étoiles, j’ai trouvé plus de 50 dépôts dédiés à l’évaluation (en mai 2024). [5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id875) Lorsque l’on représente graphiquement le nombre de dépôts d’évaluation en fonction de leur date de création, la courbe de croissance semble exponentielle, comme le montre [la figure 3-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_2_1730150757025049) .

La mauvaise nouvelle est que, malgré l'intérêt croissant porté à l'évaluation, celle-ci reste à la traîne par rapport au reste du processus d'ingénierie de l'IA. [Balduzzi et al. de DeepMind](https://arxiv.org/abs/1806.02643) ont constaté dans leur article que « le développement des évaluations a bénéficié de peu d'attention systématique comparé au développement des algorithmes ». Selon cet article, les résultats expérimentaux sont presque exclusivement utilisés pour améliorer les algorithmes et rarement pour améliorer l'évaluation. Face à ce manque d'investissements dans l'évaluation, [Anthropic](https://oreil.ly/gPbjS) a appelé les décideurs politiques à augmenter les financements et les subventions publiques, tant pour le développement de nouvelles méthodologies d'évaluation que pour l'analyse de la robustesse des évaluations existantes .

![Graphique illustrant la croissance d'un certain nombre de personnes. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0302.png)

###### Figure 3-2. Nombre de dépôts d'évaluation open source parmi les 1 000 dépôts d'IA les plus populaires sur GitHub.

Pour démontrer davantage à quel point l'investissement dans l'évaluation est en retard par rapport à d'autres domaines de l'IA, le nombre d'outils d'évaluation est faible par rapport au nombre d'outils de modélisation, d'entraînement et d'orchestration de l'IA, comme le montre la [figure 3-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_3_1730150757025061) .

Un investissement insuffisant engendre des infrastructures inadéquates, ce qui complique la réalisation d'évaluations systématiques. Interrogés sur leur méthode d'évaluation des applications d'IA, nombreux sont ceux qui m'ont confié se fier à leur intuition. Beaucoup utilisent un petit nombre de critères d'évaluation pour leurs modèles. Le choix de ces critères est souvent empirique, reposant généralement sur l'expérience personnelle de l'évaluateur plutôt que sur les besoins de l'application. Cette approche empirique peut suffire au démarrage d'un projet, mais elle s'avère insuffisante pour l'amélioration continue de l'application. Cet ouvrage propose une approche systématique de l'évaluation.

![Un graphique à barres avec description textuelle généré automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0303.png)

###### Figure 3-3. Selon les données issues de ma liste des 1 000 dépôts d'IA les plus populaires sur GitHub, l'évaluation est en retard par rapport à d'autres aspects de l'ingénierie de l'IA en termes d'outils open source.

# Comprendre les métriques de modélisation du langage

Les modèles de base ont évolué à partir des modèles de langage. Nombre d'entre eux conservent des modèles de langage comme composants principaux. Pour ces modèles, les performances du modèle de langage sont généralement bien corrélées aux performances du modèle de base sur les applications en aval ( [Liu et al., 2023](https://oreil.ly/vX-My) ). Par conséquent, une compréhension générale des métriques de modélisation du langage peut s'avérer très utile pour appréhender les performances en aval [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id878)

Comme indiqué au [chapitre 1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_introduction_to_building_ai_applications_with_foun_1730130814984319) , la modélisation du langage existe depuis des décennies, popularisée par Claude Shannon dans son article de 1951 intitulé « Prediction and Entropy of Printed English ». Les métriques utilisées pour guider le développement des modèles de langage ont peu évolué depuis. La plupart des modèles de langage autorégressifs sont entraînés à l'aide de l'entropie croisée ou de son dérivé, la perplexité. Lors de la lecture d'articles et de rapports de modélisation, vous rencontrerez peut-être également les termes « bits par caractère » (BPC) et « bits par octet » (BPB) ; il s'agit de variantes de l'entropie croisée.

Les quatre métriques (entropie croisée, perplexité, BPC et BPB) sont étroitement liées. Connaître la valeur de l'une permet de calculer les trois autres, à condition de disposer des informations nécessaires. Bien que je les désigne comme des métriques de modélisation du langage, elles peuvent être utilisées pour tout modèle générant des séquences de jetons, y compris des jetons non textuels.

Rappelons qu'un modèle de langage encode des informations statistiques (la probabilité d'apparition d'un jeton dans un contexte donné) sur les langues. Statistiquement, dans le contexte « J'aime boire __ », le mot suivant a plus de chances d'être « thé » que « charbon ». Plus un modèle capture d'informations statistiques, plus il est performant pour prédire le jeton suivant.

En langage d'apprentissage automatique, un modèle de langage apprend la distribution de ses données d'entraînement. Plus cet apprentissage est précis, plus il est performant pour prédire les données suivantes et plus son entropie croisée d'entraînement est faible. Comme pour tout modèle d'apprentissage automatique, il est important d'évaluer ses performances non seulement sur les données d'entraînement, mais aussi sur les données de production. En général, plus vos données sont proches des données d'entraînement du modèle, meilleures seront ses performances sur vos données.

Comparée au reste de l'ouvrage, cette section est riche en mathématiques. Si vous la trouvez complexe, n'hésitez pas à la sauter et à vous concentrer sur l'explication de l'interprétation de ces métriques. Même si vous n'entraînez ni n'affinez de modèles de langage, la compréhension de ces métriques peut vous aider à choisir les modèles les plus adaptés à votre application. Ces métriques peuvent également servir, dans certains cas, pour des techniques d'évaluation et de déduplication des données, comme nous l'expliquons tout au long de ce livre.

## Entropie

_L'entropie_ mesure la quantité d'information, en moyenne, qu'un jeton véhicule. Plus l'entropie est élevée, plus chaque jeton véhicule d'information et plus il faut de bits pour le représenter. [7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id881)

Prenons un exemple simple pour illustrer cela. Imaginons que vous souhaitiez créer un langage pour décrire les positions à l'intérieur d'un carré, comme illustré sur [la figure 3-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_4_1730150757025074) . Si votre langage ne comporte que deux jetons, représentés par (a) sur [la figure 3-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_4_1730150757025074) , chaque jeton indique si la position est supérieure ou inférieure. Puisqu'il n'y a que deux jetons, un bit suffit pour les représenter. L'entropie de ce langage est donc de 1.

![Deux carrés avec des chiffres. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0304.png)

###### Figure 3-4. Deux langages décrivent des positions à l'intérieur d'un carré. Comparés au langage de gauche (a), les jetons de droite (b) véhiculent plus d'informations, mais nécessitent plus de bits pour être représentés.

Si votre langage comporte quatre jetons, comme illustré en (b) dans [la figure 3-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_4_1730150757025074) , chaque jeton peut indiquer une position plus précise : en haut à gauche, en haut à droite, en bas à gauche ou en bas à droite. Cependant, comme il y a maintenant quatre jetons, il faut deux bits pour les représenter. L’entropie de ce langage est de 2. Ce langage a une entropie plus élevée, car chaque jeton véhicule plus d’informations, mais sa représentation nécessite également plus de bits.

Intuitivement, l'entropie mesure la difficulté à prédire la suite d'un mot dans une langue. Plus l'entropie d'une langue est faible (moins chaque mot contient d'information), plus cette langue est prévisible. Dans notre exemple précédent, la langue à deux mots seulement est plus facile à prédire que celle à quatre mots (il suffit de choisir parmi deux mots possibles au lieu de quatre). C'est comparable au fait que, si vous pouvez parfaitement prédire ce que je vais dire ensuite, mes paroles n'apportent aucune information nouvelle.

## Entropie croisée

Lorsqu'on entraîne un modèle de langage sur un jeu de données, l'objectif est de lui faire apprendre la distribution de ces données d'entraînement. Autrement dit, il s'agit de lui permettre de prédire la prochaine donnée. L'entropie croisée d'un modèle de langage sur un jeu de données mesure la difficulté qu'il rencontre pour prédire la prochaine donnée.

L'entropie croisée d'un modèle sur les données d'entraînement dépend de deux qualités :

1. La prédictibilité des données d'entraînement, mesurée par l'entropie des données d'entraînement
    
2. Comment la distribution capturée par le modèle de langage diverge de la distribution réelle des données d'entraînement
    

L'entropie et l'entropie croisée partagent la même notation mathématique, $H$ Soit $P$ la distribution réelle des données d'entraînement et _Q_ la distribution apprise par le modèle de langage. Par conséquent, ce qui suit est vrai :

- L'entropie des données d'entraînement est donc $H(P)$.
- La divergence de $Q$ par rapport à $P$ peut être mesurée à l'aide de la divergence de Kullback-Leibler (KL), qui est mathématiquement représentée comme $D_{KL}(P||Q)$
- L'entropie croisée du modèle par rapport aux données d'entraînement est donc : $H(P,Q) - H(P) + D_{KL}(P||Q)$
    

L'entropie croisée n'est pas symétrique. L'entropie croisée de _Q_ par rapport à $P — H ( P , Q ) —$ est différente de l'entropie croisée de _P_ par rapport à $Q — H ( Q , P )$.

Un modèle de langage est entraîné à minimiser son entropie croisée par rapport aux données d'entraînement. Si le modèle apprend parfaitement à partir de ces données, son entropie croisée sera exactement égale à l'entropie des données d'entraînement. La divergence de Kullback-Leibler de Q par rapport à P sera alors nulle. On peut considérer l'entropie croisée d'un modèle comme une approximation de l'entropie de ses données d'entraînement.

## Bits par caractère et bits par octet

L'unité d'entropie et d'entropie croisée est le bit. Si l'entropie croisée d'un modèle de langage est de 6 bits, ce modèle nécessite 6 bits pour représenter chaque jeton.

Comme les méthodes de tokenisation varient selon les modèles (par exemple, certains utilisent des mots et d'autres des caractères), le nombre de bits par jeton n'est pas comparable d'un modèle à l'autre. Certains modèles utilisent plutôt le nombre de _bits par caractère_ (BPC). Si le nombre de bits par jeton est de 6 et que chaque jeton est composé en moyenne de 2 caractères, le BPC est de 6/2 = 3.

Une difficulté liée au BPC provient des différents schémas d'encodage des caractères. Par exemple, en ASCII, chaque caractère est encodé sur 7 bits, tandis qu'en UTF-8, un caractère peut être encodé sur 8 à 32 bits. Une mesure plus standardisée serait le nombre _de bits par octet_ (BPB), soit le nombre de bits nécessaires à un modèle de langage pour représenter un octet des données d'entraînement initiales. Si le BPC est de 3 et que chaque caractère est codé sur 7 bits (soit ⅞ d'octet), alors le BPB est de 3 / (⅞) = 3,43.

L'entropie croisée indique l'efficacité d'un modèle de langage pour la compression de texte. Si le BPB d'un modèle de langage est de 3,43, ce qui signifie qu'il peut représenter chaque octet original (8 bits) avec 3,43 bits, ce modèle peut compresser le texte d'entraînement original à moins de la moitié de sa taille initiale.

## Perplexité

_La perplexité_ est l'exponentielle de l'entropie et de l'entropie croisée. On l'abrège souvent en PPL. Étant donné un ensemble de données suivant la distribution réelle _P_ , sa perplexité est définie comme suit :

$PPL(P) = 2^{H(P)}$

La perplexité d'un modèle de langage (avec la distribution apprise _Q_ ) sur cet ensemble de données est définie comme suit :

$PPL(P) = 2^{H(P,Q)}$

Si l'entropie croisée mesure la difficulté pour un modèle de prédire le jeton suivant, la perplexité mesure le degré d'incertitude lié à cette prédiction. Plus l'incertitude est élevée, plus le nombre de jetons possibles est important.

Considérons un modèle de langage entraîné à encoder parfaitement les 4 jetons de position, comme dans [la figure 3-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_4_1730150757025074) (b). L'entropie croisée de ce modèle est de 2 bits. Si ce modèle tente de prédire une position dans le carré, il doit choisir parmi 2Il y a donc 4 options possibles. Par conséquent, ce modèle de langage a une perplexité de 4.

Jusqu'à présent, j'ai utilisé _le bit_ comme unité d'entropie et d'entropie croisée. Chaque bit peut représenter 2<sup>2</sup> valeurs uniques, d'où la base 2 dans l'équation de perplexité précédente.

Les frameworks d'apprentissage automatique populaires, tels que TensorFlow et PyTorch, utilisent le logarithme népérien ( _nat_ ) comme unité pour l'entropie et l'entropie croisée. Nat utilise la [base de _e_](https://en.wikipedia.org/wiki/E_\(mathematical_constant\)) , la base du logarithme népérien. [Si](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id892) vous utilisez _nat_ comme unité, la perplexité est l'exponentielle de _e_ :

$PPL(P) = e^{H(P,Q)}$

En raison de la confusion autour des termes _bit_ et _nat_ , de nombreuses personnes rapportent la perplexité, au lieu de l'entropie croisée, lorsqu'elles rendent compte des performances de leurs modèles de langage.

## Interprétation et cas d'utilisation de la perplexité

Comme nous l'avons vu, l'entropie croisée, la perplexité, le BPC et le BPB sont des variantes des mesures de précision prédictive des modèles de langage. Plus un modèle prédit un texte avec précision, plus ces métriques sont faibles. Dans cet ouvrage, j'utiliserai la perplexité comme métrique par défaut pour la modélisation du langage . Il est important de noter que plus l'incertitude du modèle quant à la prédiction de la suite d'un texte dans un ensemble de données donné est grande, plus la perplexité est élevée.

La valeur considérée comme acceptable pour la perplexité dépend des données elles-mêmes et de la méthode de calcul précise, notamment du nombre de jetons précédents auxquels le modèle a accès. Voici quelques règles générales :

Des données plus structurées entraînent une perplexité attendue plus faible.

Des données plus structurées sont plus prévisibles. Par exemple, le code HTML est plus prévisible que le texte courant. Si vous voyez une balise HTML ouvrante, `<head>,`vous pouvez prédire la présence d'une balise fermante `</head>,`à proximité. Par conséquent, la perplexité attendue d'un modèle appliqué au code HTML devrait être inférieure à celle d'un modèle appliqué au texte courant.

Plus le vocabulaire est étendu, plus la perplexité est grande.

Intuitivement, plus le nombre de jetons possibles est élevé, plus il est difficile pour le modèle de prédire le jeton suivant. Par exemple, la perplexité d'un modèle sur un livre pour enfants sera probablement inférieure à sa perplexité sur _Guerre et Paix_ . Pour un même ensemble de données, par exemple en anglais, la perplexité basée sur les caractères (prédiction du caractère suivant) sera inférieure à la perplexité basée sur les mots (prédiction du mot suivant), car le nombre de caractères possibles est inférieur au nombre de mots possibles.

Plus le contexte est long, plus la perplexité est faible.

Plus un modèle dispose de contexte, moins il sera incertain dans la prédiction du jeton suivant. En 1951, Claude Shannon a évalué l'entropie croisée de son modèle en l'utilisant pour prédire le jeton suivant à partir des dix jetons précédents. À l'heure actuelle, la perplexité d'un modèle peut généralement être calculée et conditionnée par un nombre de jetons précédents compris entre 500 et 10 000, voire davantage, ce nombre étant limité par la longueur maximale du contexte du modèle.

À titre indicatif, il n'est pas rare d'observer des valeurs de perplexité aussi basses que 3, voire inférieures. Si tous les jetons d'une langue hypothétique ont une probabilité d'apparition égale, une perplexité de 3 signifie que ce modèle a une chance sur trois de prédire correctement le jeton suivant. Sachant que le vocabulaire d'un modèle compte entre plusieurs dizaines de milliers et centaines de milliers de jetons, ces probabilités sont extrêmement faibles.

Outre son utilité pour guider l'entraînement des modèles de langage, la perplexité est précieuse à de nombreuses étapes du processus d'ingénierie en IA. Tout d'abord, elle constitue un bon indicateur des capacités d'un modèle. Si un modèle peine à prédire le jeton suivant, ses performances sur les tâches en aval seront probablement également médiocres. Le rapport GPT-2 d'OpenAI montre que les modèles plus grands, et donc plus puissants, affichent systématiquement une perplexité plus faible sur divers jeux de données, comme l'illustre le [tableau 3-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_table_1_1730150757038068) . Malheureusement, suivant la tendance croissante des entreprises à dissimuler leurs modèles, beaucoup ont cessé de communiquer leur perplexité.

Tableau 3-1. Les modèles GPT-2 de plus grande taille présentent systématiquement une perplexité plus faible sur différents ensembles de données. Source : [OpenAI, 2018](https://oreil.ly/Loidb)

| LAMBADA  <br>(PPL) | LAMBADA  <br>(ACC) | CBT-CN  <br>(ACC) | TCC-NE  <br>(ACC) | WikiText2  <br>(PPL) | PTB  <br>(PPL) | enwiki8  <br>(BPB) | texte8  <br>(BPC) | WikiText103  <br>(PBL) | IBW  <br>(PPL) |        |
| ------------------ | ------------------ | ----------------- | ----------------- | -------------------- | -------------- | ------------------ | ----------------- | ---------------------- | -------------- | ------ |
| SOTA               | 99,8               | 59,23             | 85,7              | 82,3                 | 39.14          | 46,54              | 0,99              | 1.08                   | 18.3           | 21.8   |
| 117M               | 35.13              | 45,99             | 87,65             | 83,4                 | 29.41          | 65,85              | 1.16              | 1.17                   | 37,50          | 75,20  |
| 345M               | 15,60              | 55,48             | 92,35             | 87.1                 | 22,76          | 47,33              | 1.01              | 1.06                   | 26,37          | 55,72  |
| 762M               | 10,87              | 60,12             | 93,45             | 88.0                 | 19,93          | 40,31              | 0,97              | 1.02                   | 22.05          | 44,575 |
| 1542M              | 8,63               | 63,24             | 93,30             | 89,05                | 18.34          | 35,76              | 0,93              | 0,98                   | 17.48          | 42.16  |

###### Avertissement

La perplexité n'est peut-être pas un indicateur fiable pour évaluer les modèles ayant subi un post-entraînement à l'aide de techniques telles que SFT et RLHF. [Le](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id895) post-entraînement consiste à apprendre aux modèles à accomplir des tâches. Plus un modèle excelle dans l'exécution des tâches, moins il est performant pour prédire les jetons suivants. La perplexité d'un modèle de langage augmente généralement après un post-entraînement. Certains affirment que le post-entraînement _réduit_ l'entropie. De même, la quantification – une technique qui réduit la précision numérique d'un modèle et, par conséquent, son empreinte mémoire – peut également modifier la perplexité d'un modèle de manière inattendue [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id896)

Rappelons que la perplexité d'un modèle par rapport à un texte mesure la difficulté qu'il lui faut pour prédire ce texte. Pour un modèle donné, la perplexité est minimale pour les textes qu'il a vus et mémorisés lors de son entraînement. Par conséquent, la perplexité permet de déterminer si un texte figurait dans les données d'entraînement du modèle.Ceci est utile pour détecter la contamination des données : si la perplexité d'un modèle sur les données de référence est faible, il est probable que ces données aient été incluses dans ses données d'entraînement, ce qui rend ses performances moins fiables. Cette méthode peut également servir à la déduplication des données d'entraînement : par exemple, n'ajouter de nouvelles données à l'ensemble d'entraînement existant que si leur perplexité est élevée.

La perplexité est maximale pour les textes imprévisibles, comme ceux exprimant des idées inhabituelles (par exemple « mon chien enseigne la physique quantique pendant son temps libre ») ou du charabia (par exemple « chat à la maison va œil »). La perplexité peut donc servir à détecter les textes anormaux.

La perplexité et les métriques associées nous aident à comprendre les performances du modèle de langage sous-jacent, ce qui permet d'appréhender indirectement ses performances sur les tâches en aval. La suite de ce chapitre explique comment mesurer directement les performances d'un modèle sur ces tâches.

# Comment utiliser un modèle de langage pour calculer la perplexité d'un texte

La perplexité d'un modèle par rapport à un texte mesure la difficulté qu'il lui faut pour prédire ce texte. Étant donné un modèle de langage _X_ et une séquence de jeton
![[CleanShot 2025-11-01 at 20.51.38.png]]
La perplexité de $X$ pour cette séquence est :

![[CleanShot 2025-11-01 at 20.52.29.png]]

où $P(x_i|x_1,...,x_{i-1})$  désigne la probabilité que $X$ soit attribué au jeton $x_i$ compte tenu des jetons précédents $x_1,...,x_{i-1}$.

[Pour calculer la perplexité, il faut accéder aux probabilités (ou logprobs) que le modèle de langage attribue à chaque jeton suivant. Malheureusement, comme indiqué au chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) , tous les modèles commerciaux ne rendent pas accessibles leurs logprobs.

# Évaluation exacte

Lors de l'évaluation des performances des modèles, il est important de distinguer l'évaluation exacte de l'évaluation subjective. L'évaluation exacte produit un jugement sans ambiguïté. Par exemple, si la réponse à une question à choix multiple est A et que vous choisissez B, votre réponse est fausse. Il n'y a aucune ambiguïté à ce sujet. En revanche, la notation des dissertations est subjective. La note d'une dissertation dépend de la personne qui l'évalue. Une même personne, interrogée à deux reprises à un intervalle de temps, peut attribuer des notes différentes à une même dissertation. La notation des dissertations peut gagner en précision grâce à des critères d'évaluation clairs. Comme vous le verrez dans la section suivante, l'IA, en tant que juge, est subjective. Le résultat de l'évaluation peut varier en fonction du modèle de juge et du sujet.

J'aborderai deux approches d'évaluation permettant d'obtenir des scores précis : la correction fonctionnelle et les mesures de similarité par rapport à des données de référence. Cette section se concentre sur l'évaluation des réponses ouvertes (génération de texte arbitraire) plutôt que sur celle des réponses fermées (comme la classification). Ce choix n'est pas dû au fait que les modèles de base ne sont pas utilisés pour les tâches fermées. En réalité, de nombreux systèmes de modèles de base comportent au moins un module de classification, généralement pour la classification des intentions ou la notation. Cette section privilégie l'évaluation des réponses ouvertes car l'évaluation des réponses fermées est déjà bien maîtrisée.

## Correction fonctionnelle

L'évaluation de la correction fonctionnelle consiste à évaluer un système en fonction de sa capacité à remplir les fonctionnalités attendues. Par exemple, si vous demandez à un modèle de créer un site web, le site généré répond-il à vos exigences ? Si vous demandez à un modèle d'effectuer une réservation dans un restaurant, le modèle y parvient-il ?

La correction fonctionnelle est le critère ultime d'évaluation des performances d'une application, car elle mesure si celle-ci remplit sa fonction. Cependant, la correction fonctionnelle n'est pas toujours simple à mesurer, et son automatisation est difficile.

La génération de code est un exemple de tâche où la mesure de la correction fonctionnelle peut être automatisée. La correction fonctionnelle d'un code correspond parfois à _sa précision d'exécution_ . Supposons que vous demandiez au modèle d'écrire une fonction Python, `num1` `gcd(num1, num2)`, qui calcule le plus grand commun dénominateur (PGCD) de deux nombres, `num2` et `num1`. Le code généré peut ensuite être entré dans un interpréteur Python pour vérifier sa validité et, le cas échéant, s'il produit le résultat attendu pour une paire donnée `(num1, num2)`. Par exemple, étant donné la paire `num1`, `num2` et `num2` `(num1=15, num2=20)`, si la fonction `gcd(15, 20)`ne renvoie pas 5, la réponse correcte, vous savez qu'elle est incorrecte.

Bien avant que l'IA ne soit utilisée pour écrire du code, la vérification automatique de la correction fonctionnelle du code était une pratique courante en génie logiciel. Le code est généralement validé par [des tests unitaires](https://en.wikipedia.org/wiki/Unit_testing) , qui l'exécutent dans différents scénarios afin de s'assurer qu'il produit les résultats attendus. L'évaluation de la correction fonctionnelle est la méthode utilisée par les plateformes de programmation comme LeetCode et HackerRank pour valider les solutions soumises.

Les benchmarks populaires pour évaluer les capacités de génération de code de l'IA, tels que [HumanEval d'OpenAI](https://oreil.ly/CjYs9) et [MBPP (Mostly Basic Python Problems Dataset) de Google](https://github.com/google-research/google-research/tree/master/mbpp) , utilisent la correction fonctionnelle comme critère.Les benchmarks pour la conversion de texte en SQL (génération de requêtes SQL à partir de langages naturels) comme Spider ( [Yu et al., 2018](https://oreil.ly/ijU20) ), BIRD-SQL (Big Bench for Large-scale Database Grounded Text-to-SQL Evaluation) ( [Li et al., 2023](https://oreil.ly/rrSS9) ) et WikiSQL ( [Zhong, et al., 2017](https://arxiv.org/abs/1709.00103) ) s'appuient également sur la correction fonctionnelle.

Un problème de référence est accompagné d'un ensemble de cas de test. Chaque cas de test comprend un scénario d'exécution du code et le résultat attendu pour ce scénario. Voici un exemple de problème et de ses cas de test dans HumanEval :

```python
#Problème
from typing import List
def has_close_elements(numbers: List[float], threshold: float) -> bool:
      Vérifiez si, dans la liste de nombres donnée, deux nombres quelconques sont plus proches l'un de l'autre.
      autre que le seuil donné.
      >>> has_close_elements([1.0, 2.0, 3.0], 0.5) False
      >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3) True
      ""
      
#Cas de test (chaque instruction assert représente un cas de test)
def check(candidat):
      assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.3) == True
      assert candidate([1.0, 2.0, 3.9, 4.0, 5.0, 2.2], 0.05) == False
      assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.95) == True
      assert candidate([1.0, 2.0, 5.9, 4.0, 5.0], 0.8) == False
      assert candidate([1.0, 2.0, 3.0, 4.0, 5.0, 2.0], 0.1) == True
      assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 1.0) == True
      assert candidate([1.1, 2.2, 3.1, 4.1, 5.1], 0.5) == False   
      
      
```



Lors de l'évaluation d'un modèle, pour chaque problème, un certain nombre d'exemples de code, notés _k_ , sont générés. Un modèle résout un problème si au moins un des _k_ exemples de code générés réussit tous les tests de ce problème. Le score final, appelé _pass@k_ , correspond à la proportion de problèmes résolus parmi l'ensemble des problèmes. S'il y a 10 problèmes et qu'un modèle en résout 5 avec _k_ = 3, alors son score pass@3 est de 50 %. Plus un modèle génère d'exemples de code, plus il a de chances de résoudre chaque problème, et donc plus son score final est élevé. En conséquence, le score pass@1 devrait être inférieur au score pass@3, qui lui-même devrait être inférieur au score pass@10.

Une autre catégorie de tâches dont la correction fonctionnelle peut être évaluée automatiquement est celle des bots de jeu. Si vous créez un bot pour jouer _à Tetris , vous pouvez évaluer sa performance grâce au score qu'il obtient. Les tâches ayant des objectifs mesurables peuvent généralement être évaluées à l'aide de la correction fonctionnelle. Par_ [exemple](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id906) , si vous demandez à une IA de planifier vos charges de travail afin d'optimiser la consommation d'énergie, la performance de l'IA peut être mesurée par la quantité d'énergie économisée.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id906)

## Mesures de similarité par rapport aux données de référence

Si la tâche qui vous intéresse ne peut être évaluée automatiquement par correction fonctionnelle, une approche courante consiste à comparer les résultats de l'IA à des données de référence. Par exemple, si vous demandez à un modèle de traduire une phrase du français vers l'anglais, vous pouvez comparer la traduction anglaise générée à la traduction anglaise correcte.

Chaque exemple des données de référence suit le format (entrée, réponses de référence). Une entrée peut avoir plusieurs réponses de référence, comme plusieurs traductions anglaises possibles d'une phrase française. Les réponses de référence sont également appelées_Les données de référence_ ou _les réponses canoniques_ sont utilisées pour les métriques qui nécessitent des références , tandis que celles qui n'en nécessitent pas sont dites _sans_ _référence_ .

Cette méthode d'évaluation, qui nécessite des données de référence, est limitée par la quantité et la rapidité de leur production. Ces données sont généralement générées par des humains, et de plus en plus par des IA. Utiliser des données humaines comme référence revient à considérer la performance humaine comme l'étalon-or, et à évaluer la performance de l'IA par rapport à celle-ci. La production de données humaines peut s'avérer coûteuse et chronophage, ce qui incite de nombreux chercheurs à privilégier l'IA. Si les données générées par l'IA peuvent encore nécessiter une vérification humaine, le travail requis est bien moindre que celui nécessaire à la production de données de référence à partir de zéro.

Les réponses générées qui ressemblent le plus aux réponses de référence sont considérées comme meilleures. Il existe quatre façons de mesurer la similarité entre deux textes ouverts :

1. Demander à un évaluateur de déterminer si deux textes sont identiques
    
2. Correspondance exacte : indique si la réponse générée correspond exactement à l’une des réponses de référence.
    
3. Similarité lexicale : degré de similarité entre la réponse générée et les réponses de référence
    
4. Similarité sémantique : degré de proximité (sémantique) entre la réponse générée et les réponses de référence
    

Deux réponses peuvent être comparées par des évaluateurs humains ou par des évaluateurs IA. Ces derniers sont de plus en plus courants et feront l'objet de la section suivante.

Cette section se concentre sur les métriques conçues manuellement : la correspondance exacte, la similarité lexicale et la similarité sémantique. Les scores de correspondance exacte sont binaires (correspondance ou non), tandis que les deux autres scores sont sur une échelle continue (par exemple, entre 0 et 1 ou entre -1 et 1). Malgré la simplicité d'utilisation et la flexibilité de l'IA comme outil d'évaluation, les mesures de similarité conçues manuellement restent largement utilisées dans l'industrie pour leur précision.

###### Note

Cette section explique comment utiliser les mesures de similarité pour évaluer la qualité d'un résultat généré. Toutefois, ces mesures peuvent également servir dans de nombreux autres cas d'utilisation, notamment :

Récupération et recherche

trouver des articles similaires à une requête

Classement

classer les éléments en fonction de leur similarité avec une requête

Clustering

Regrouper les éléments en fonction de leur degré de similarité.

Détection d'anomalies

détecter les éléments les moins similaires aux autres

Déduplication des données

supprimer les éléments trop similaires à d'autres éléments

Les techniques abordées dans cette section seront réutilisées tout au long du livre.

### Correspondance exacte

On parle de correspondance exacte si la réponse générée correspond exactement à l'une des réponses de référence. La correspondance exacte convient aux tâches qui attendent des réponses courtes et précises, comme les problèmes de mathématiques simples, les questions de culture générale et les questions de type quiz. Voici des exemples de questions qui appellent des réponses courtes et précises :

- « Combien font 2 + 3 ? »
    
- « Qui a été la première femme à remporter un prix Nobel ? »
    
- « Quel est le solde actuel de mon compte ? »
    
- « Complétez la phrase : Paris est à la France ce que ___ est à l'Angleterre. »
    

Il existe des variantes de correspondance qui tiennent compte des problèmes de formatage. L'une d'elles consiste à accepter comme correspondance toute sortie contenant la réponse de référence. Prenons l'exemple de la question « Combien font 2 + 3 ? » La réponse de référence est « 5 ». Cette variante accepte toutes les sorties contenant « 5 », y compris « La réponse est 5 » et « 2 + 3 font 5 ».

Cependant, cette variation peut parfois conduire à l'acceptation d'une réponse erronée. Prenons l'exemple de la question « En quelle année Anne Frank est-elle née ? » Anne Frank est née le 12 juin 1929, la réponse correcte est donc 1929. Si le modèle affiche « 12 septembre 1929 », l'année correcte figure bien dans le résultat, mais ce dernier est factuellement incorrect.

Au-delà des tâches simples, la correspondance exacte est rarement efficace. Prenons l'exemple de la phrase française « Comment ça va ? ». Il existe plusieurs traductions anglaises possibles, telles que « How are you ? », « How is everything ? » et « How are you doing ? ». Si les données de référence ne contiennent que ces trois traductions et qu'un modèle génère « How is it going ? », sa réponse sera considérée comme incorrecte. Plus le texte original est long et complexe, plus le nombre de traductions possibles est élevé. Il est impossible de créer un ensemble exhaustif de réponses possibles pour une entrée donnée. Pour les tâches complexes, la similarité lexicale et la similarité sémantique sont plus performantes.

### Similarité lexicale

La similarité lexicale mesure le degré de chevauchement entre deux textes. Pour ce faire, il faut d'abord décomposer chaque texte en unités lexicales plus petites.

Dans sa forme la plus simple, la similarité lexicale peut être mesurée en comptant le nombre de mots communs à deux textes. Prenons par exemple la réponse de référence _« Mes chats font peur aux souris »_ et deux réponses générées :

- « Mes chats mangent les souris »
    
- « Les chats et les souris se battent tout le temps. »
    

Supposons que chaque jeton soit un mot. Si l'on ne tient compte que du chevauchement des mots individuels, la réponse A contient 4 mots sur 5 de la réponse de référence (le score de similarité est de 80 %), tandis que la réponse B n'en contient que 3 sur 5 (le score de similarité est de 60 %). La réponse A est donc considérée comme plus similaire à la réponse de référence.

Une méthode pour mesurer la similarité lexicale est _la correspondance approximative de chaînes de caractères_ , aussi appelée _correspondance floue_ . Elle mesure la similarité entre deux textes en comptant le nombre de modifications nécessaires pour passer de l'un à l'autre, un nombre appelé _distance d'édition_ . Les trois opérations d'édition habituelles sont :

1. Suppression : « b _r_ ad » -> « bad »
    
2. Insertion : « bad » -> « _bar_ »
    
3. Substitution : « bad _»_ -> « _bed_ »
    

Certains algorithmes de correspondance floue considèrent également la transposition, c'est-à-dire l'échange de deux lettres (par exemple, « ma _ts_ » → « ma _st_ »), comme une modification. Cependant, d'autres algorithmes de correspondance floue traitent chaque transposition comme deux opérations de modification : une suppression et une insertion.

Par exemple, « bad » est une modification de « barde » et trois modifications de « cash », donc « bad » est considéré comme plus similaire à « barde » qu’à « cash ».

Une autre façon de mesurer la similarité lexicale est _la similarité n-gramme_ , calculée à partir du chevauchement de séquences de jetons ( _n-grammes_ ) plutôt que de jetons individuels. Un unigramme est un jeton. Un bigramme est un ensemble de deux jetons. « Mes chats font peur aux souris » est composé de quatre bigrammes : « mes chats », « chats font peur », « faire peur aux » et « les souris ». On mesure le pourcentage de n-grammes présents dans les réponses de référence et également présents dans la réponse générée [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id922)

Les métriques courantes de similarité lexicale sont BLEU, ROUGE, METEOR++, TER et CIDEr. Elles diffèrent par leur méthode de calcul du chevauchement. Avant l'avènement des modèles de base, BLEU, ROUGE et leurs équivalents étaient largement utilisés, notamment pour la traduction automatique. Depuis, moins de benchmarks utilisent la similarité lexicale. Parmi ceux qui l'utilisent, on peut citer [WMT](https://oreil.ly/92yRh) , [COCO Captions](https://oreil.ly/BO3-0) et [GEMv2](https://arxiv.org/abs/2206.11249) .

L'un des inconvénients de cette méthode est qu'elle nécessite la constitution d'un ensemble complet de réponses de référence. Une bonne réponse peut obtenir un faible score de similarité si l'ensemble de référence ne contient aucune réponse qui lui ressemble. Sur certains exemples de test, [Adept](https://oreil.ly/OWD2v) a constaté que les faibles performances de son modèle Fuyu n'étaient pas dues à des erreurs dans ses résultats, mais à l'absence de certaines réponses correctes dans les données de référence. [La figure 3-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_5_1730150757025084) illustre un exemple de tâche de légende d'image où Fuyu a généré une légende correcte, mais a obtenu un faible score.

De plus, les références peuvent être erronées. Par exemple, les organisateurs de la tâche partagée WMT 2023 Metrics, qui vise à examiner les métriques d'évaluation de la traduction automatique, ont signalé avoir trouvé de nombreuses traductions de référence de mauvaise qualité dans leurs données. La faible qualité des données de référence est l'une des raisons pour lesquelles les métriques sans référence étaient de sérieuses alternatives aux métriques basées sur des références en termes de corrélation avec le jugement humain ( [Freitag et al., 2023](https://oreil.ly/tmWqk) ).

Un autre inconvénient de cette mesure est que des scores de similarité lexicale élevés ne signifient pas toujours de meilleures réponses. Par exemple, sur HumanEval, un banc d'essai de génération de code, OpenAI a constaté que les scores BLEU des solutions incorrectes et correctes étaient similaires. Cela indique qu'optimiser les scores BLEU ne revient pas à optimiser la correction fonctionnelle ( [Chen et al., 2021](https://arxiv.org/abs/2107.03374) ).

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0305.png)

###### Figure 3-5. Un exemple où Fuyu a généré une option correcte mais a reçu un score faible en raison de la limitation des légendes de référence.

### Similarité sémantique

La similarité lexicale mesure la ressemblance visuelle de deux textes, et non leur sens. Prenons les phrases « Quoi de neuf ? » et « Comment vas-tu ? ». Lexicalement, elles diffèrent : elles partagent peu de mots et de lettres. Cependant, sémantiquement, elles sont proches. Inversement, des textes d'apparence similaire peuvent avoir des significations très différentes. « Mangeons, grand-mère » et « Mangeons grand-mère » signifient deux choses totalement différentes.

_La similarité sémantique_ vise à calculer la similarité sémantique. Cela nécessite d'abord de transformer un texte en une représentation numérique, appelée _plongement_ . Par exemple, la phrase « le chat est assis sur un tapis » pourrait être représentée par un plongement de ce type : `[0.11, 0.02, 0.54]`. La similarité sémantique est donc également appelée _similarité de plongement_ .

[Le chapitre « Introduction aux plongements lexicaux »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_introduction_to_embedding_1730150757064669) explique le fonctionnement de ces plongements. Supposons pour l'instant que vous disposiez d'un moyen de transformer des textes en plongements lexicaux. La similarité entre deux plongements peut être calculée à l'aide de métriques telles que la similarité cosinus. Deux plongements identiques ont un score de similarité de 1. Deux plongements opposés ont un score de similarité de -1.

_J'utilise des exemples textuels, mais la similarité sémantique peut être calculée pour des représentations vectorielles de n'importe quelle modalité de données, y compris les images et l'audio._ La similarité sémantique pour le texte est parfois appelée similarité textuelle sémantique.

###### Avertissement

Bien que je classe la similarité sémantique dans la catégorie des évaluations exactes, elle peut être considérée comme subjective, car différents algorithmes d'intégration peuvent produire des intégrations différentes. Cependant, étant donné deux intégrations, le score de similarité entre elles est calculé de manière exacte.

Mathématiquement, soit A un plongement de la réponse générée et B un plongement d'une réponse de référence. La similarité cosinus entre A et B est calculée comme suit :, avec:

- $A.B$ étant le produit scalaire de A et B
- $||A||$ étant la norme euclidienne (également connue sous le nom denorme) de A. Si A est [0,11, 0,02, 0,54],$||A|| = \sqrt{0,11^2+0,02^2+0,54^2}$

Les métriques de similarité textuelle sémantique incluent [BERTScore](https://arxiv.org/abs/1904.09675) (les embeddings sont générés par BERT) et [MoverScore](https://oreil.ly/v2ENK) (les embeddings sont générés par un mélange d' algorithmes).

La similarité sémantique textuelle ne requiert pas un ensemble de réponses de référence aussi exhaustif que la similarité lexicale. Toutefois, sa fiabilité dépend de la qualité de l'algorithme d'intégration sous-jacent. Deux textes de même sens peuvent présenter un faible score de similarité sémantique si leurs intégrations sont de mauvaise qualité. Un autre inconvénient de cette mesure réside dans le fait que l'algorithme d'intégration sous-jacent peut nécessiter une puissance de calcul et un temps d'exécution non négligeables.

Avant d'aborder le rôle de l'IA dans le système de jugement, faisons un bref rappel sur la notion d'embedding. L'embedding est au cœur de la similarité sémantique et constitue la base de nombreux sujets que nous explorerons dans cet ouvrage, notamment la recherche vectorielle au [chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) et la déduplication des données au [chapitre 8.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888).

## Introduction à l'intégration

Puisque les ordinateurs fonctionnent avec des nombres, un modèle doit convertir ses données d'entrée en représentations numériques exploitables par les ordinateurs. _Un plongement lexical est une représentation numérique qui vise à saisir le sens des données originales._

Un vecteur d'embedding est un vecteur. Par exemple, la phrase _« le chat est assis sur un tapis »_ pourrait être représentée par un vecteur d'embedding comme celui-ci : . Ici, j'utilise un petit vecteur à titre d'exemple. En réalité, la taille d'un vecteur d'embedding (le nombre d'éléments dans le vecteur d'embedding) est généralement comprise entre 100 et [10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id927)`[0.11, 0.02, 0.54]` 000.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id927)

Les modèles spécialement entraînés pour produire des plongements lexicaux incluent les modèles open source BERT, CLIP (Contrastive Language–Image Pre-training) et [Sentence Transformers](https://github.com/UKPLab/sentence-transformers) . Il existe également des modèles de plongement lexicaux propriétaires disponibles sous forme d'API. [Le](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id929) [tableau 3-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_table_2_1730150757038080) présente la taille des plongements lexicaux de certains modèles populaires.

Tableau 3-2. Tailles d'intégration utilisées par les modèles courants.

|Modèle|Taille d'intégration|
|---|---|
|[BERT de Google](https://arxiv.org/abs/1810.04805)|Base BERT : 768  <br>BERT large : 1024|
|[CLIP d'OpenAI](https://oreil.ly/0Cfcw)|Image : 512  <br>Texte : 512|
|[API d'intégration OpenAI](https://oreil.ly/SBUiU)|text-embedding-3-small : 1536  <br>text-embedding-3-large : 3072|
|[Cohere's Embed v3](https://oreil.ly/BNNNm)|embed-english-v3.0 : 1024  <br>embed-english-light-3.0 : 384|

Comme les modèles nécessitent généralement une transformation préalable de leurs entrées en représentations vectorielles, de nombreux modèles d'apprentissage automatique, tels que les GPT et Llamas, intègrent une étape de génération d'embeddings. [L'architecture des transformeurs](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_transformer_architecture_1730147895571820) permet de visualiser la couche d'embeddings dans un modèle de type transformeur. Si vous avez accès aux couches intermédiaires de ces modèles, vous pouvez les utiliser pour extraire des embeddings. Toutefois, la qualité de ces embeddings peut être inférieure à celle des embeddings générés par des modèles d'embeddings spécialisés.

L'objectif de l'algorithme d'intégration est de produire des représentations vectorielles qui capturent l'essence des données originales. Comment le vérifier ? Le vecteur d'intégration `[0.11, 0.02, 0.54]`ne ressemble en rien au texte original « le chat est assis sur un tapis ».

De manière générale, un algorithme d'intégration est considéré comme performant si les représentations vectorielles de textes plus similaires sont plus proches, selon la similarité cosinus ou des métriques similaires. La représentation vectorielle de la phrase « le chat est assis sur un tapis » devrait être plus proche de celle de « le chien joue sur l'herbe » que de celle de « la recherche en IA est super amusante ».

Vous pouvez également évaluer la qualité des plongements lexicaux en fonction de leur utilité pour votre tâche. Les plongements lexicaux sont utilisés dans de nombreuses applications, notamment la classification, la modélisation thématique, les systèmes de recommandation et RAG. MTEB (Massive Text Embedding Benchmark, [Muennighoff et al., 2023](https://arxiv.org/abs/2210.07316) ) est un exemple de benchmark mesurant la qualité des plongements lexicaux sur plusieurs tâches.

J'utilise des textes comme exemples, mais toute donnée peut être représentée par des vecteurs. Par exemple, les solutions e-commerce comme [Criteo](https://arxiv.org/abs/1607.07326) et [Coveo](https://oreil.ly/a6jbV) proposent des vecteurs pour les produits. [Pinterest](https://oreil.ly/uJNFH) propose des vecteurs pour les images, les graphiques, les requêtes et même les utilisateurs.

Une nouvelle voie de recherche consiste à créer des représentations vectorielles conjointes pour des données de modalités différentes. CLIP ( [Radford et al., 2021](https://arxiv.org/abs/2103.00020) ) a été l'un des premiers modèles majeurs capables de projeter des données de modalités différentes, texte et images, dans un espace vectoriel conjoint. ULIP (représentation unifiée du langage, des images et des nuages ​​de points) ( [Xue et al., 2022](https://arxiv.org/abs/2212.05171) ) vise à créer des représentations unifiées du texte, des images et des nuages ​​de points 3D. ImageBind ( [Girdhar et al., 2023](https://arxiv.org/abs/2305.05665) ) apprend une représentation vectorielle conjointe à travers six modalités différentes, incluant le texte, les images et l'audio.

[La figure 3-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_6_1730150757025090) illustre l'architecture de CLIP. CLIP est entraîné à l'aide de paires (image, texte). Le texte associé à une image peut être sa légende ou un commentaire. Pour chaque paire (image, texte), CLIP utilise un encodeur de texte pour convertir le texte en un vecteur de texte, et un encodeur d'image pour convertir l'image en un vecteur d'image. Il projette ensuite ces deux vecteurs dans un espace commun. L'objectif de l'entraînement est d'obtenir un vecteur d'image aussi proche que possible de celui du texte correspondant dans cet espace commun.

![Schéma d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0306.png)

###### Figure 3-6. Architecture de CLIP (Radford et al., 2021).

Un espace d'intégration conjoint capable de représenter des données de modalités différentes est un _espace d'intégration multimodal_ . Dans un espace d'intégration conjoint texte-image, l'intégration d'une image d'un homme pêchant sera plus proche de l'intégration du texte « un pêcheur » que de celle du texte « défilé de mode ». Cet espace d'intégration conjoint permet de comparer et de combiner les intégrations de modalités différentes. Par exemple, il permet la recherche d'images à partir d'un texte. Étant donné un texte, il aide à trouver les images les plus proches de ce texte..

# L'IA comme juge

Les difficultés liées à l'évaluation des réponses ouvertes ont conduit de nombreuses équipes à recourir à l'évaluation humaine. L'IA ayant déjà permis d'automatiser avec succès de nombreuses tâches complexes, peut-elle également automatiser l'évaluation ?L'approche consistant à utiliser l'IA pour évaluer l'IA est appelée « IA comme juge » ou « LLM comme juge ».Un modèle d'IA utilisé pour évaluer d'autres modèles d'IA est appelé _juge d'IA_ . [15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id937)

L'idée d'utiliser l'IA pour automatiser l'évaluation existe depuis longtemps, [¹⁶](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id938) mais elle n'est devenue concrète que lorsque les modèles d'IA ont acquis cette capacité, vers 2020 avec la sortie de GPT-3. À l'heure actuelle, l'IA comme juge est devenue l'une des méthodes les plus courantes, sinon la plus courante, pour évaluer les modèles d'IA en production. La plupart des démonstrations de startups spécialisées dans l'évaluation par IA que j'ai vues en 2023 et 2024 utilisaient l'IA comme juge, d'une manière ou d'une autre. Le rapport [_« State of AI »_](https://oreil.ly/7Fkh-) [de LangChain](https://oreil.ly/7Fkh-) en 2023 indiquait que 58 % des évaluations sur leur plateforme étaient réalisées par des juges IA. L'IA comme juge est également un domaine de recherche actif.

## Pourquoi l'IA comme juge ?

Les systèmes d'évaluation par IA sont rapides, faciles à utiliser et relativement peu coûteux comparés aux évaluateurs humains. Ils peuvent également fonctionner sans données de référence, ce qui permet de les utiliser dans des environnements de production où ces données sont inexistantes.

Vous pouvez demander à des modèles d'IA d'évaluer un résultat selon divers critères : exactitude, répétitivité, toxicité, pertinence, hallucinations, etc. C'est comparable à la manière dont vous pouvez demander à une personne son avis sur n'importe quel sujet. Vous pourriez penser : « Mais on ne peut pas toujours se fier à l'opinion des gens. » C'est vrai, et on ne peut pas non plus toujours se fier aux jugements de l'IA. Cependant, comme chaque modèle d'IA est une agrégation de l'opinion collective, il est possible qu'ils émettent des jugements représentatifs de cette opinion. Avec la bonne consigne et le bon modèle, vous pouvez obtenir des évaluations relativement pertinentes sur un large éventail de sujets.

Des études ont démontré que certains systèmes d'évaluation par intelligence artificielle (IA) présentent une forte corrélation avec les évaluateurs humains. En 2023, [Zheng et al.](https://arxiv.org/abs/2306.05685) ont constaté que sur leur banc d'essai, MT-Bench, le taux de concordance entre GPT-4 et les humains atteignait 85 %, soit un taux supérieur à celui observé entre humains (81 %). Les auteurs d'AlpacaEval ( [Dubois et al., 2023](https://arxiv.org/abs/2404.04475) ) ont également observé que leurs IA présentaient une corrélation quasi parfaite (0,98) avec le classement de Chat Arena de LMSYS, évalué par des humains.

L'IA peut non seulement évaluer une réponse, mais aussi expliquer sa décision, ce qui s'avère particulièrement utile pour vérifier les résultats d'une évaluation. [La figure 3-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_7_1730150757025099) illustre un exemple d'explication du jugement par GPT-4.

Sa flexibilité rend l'IA utile comme outil d'évaluation dans de nombreuses applications, et pour certaines d'entre elles, elle constitue la seule option d'évaluation automatique. Même si ses jugements ne sont pas toujours aussi pertinents que ceux des humains, ils peuvent néanmoins suffire à orienter le développement d'une application et à fournir la confiance nécessaire pour lancer un projet.

![Capture d'écran d'un document. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0307.png)

###### Figure 3-7. Non seulement les juges IA peuvent noter, mais ils peuvent également expliquer leurs décisions.

## Comment utiliser l'IA comme juge

Il existe de nombreuses façons d'utiliser l'IA pour porter des jugements. Par exemple, vous pouvez l'utiliser pour évaluer la qualité d'une réponse individuellement, la comparer à des données de référence ou la comparer à une autre réponse. Voici des exemples simples de requêtes pour ces trois approches :

1. Évaluer la qualité d'une réponse en elle-même, compte tenu de la question initiale :
    
    « Compte tenu de la question et de la réponse suivantes, évaluez la qualité de la réponse. »
    Pour répondre à cette question, utilisez une échelle de 1 à 5.
    - 1 signifie très mauvais.
    - 5 signifie très bien.
    Question : [QUESTION]
    Réponse : [RÉPONSE]
    Score:"
    

2. Comparer une réponse générée à une réponse de référence permet d'évaluer si elle est identique à la réponse de référence. Cette approche peut constituer une alternative aux mesures de similarité conçues par l'humain.
    
    « Compte tenu de la question suivante, de la réponse de référence et de la réponse générée,
    Évaluer si la réponse générée est identique à la réponse de référence.
    Afficher Vrai ou Faux.
    Question : [QUESTION]
    Réponse de référence : [RÉPONSE DE RÉFÉRENCE]
    Réponse générée : [RÉPONSE GÉNÉRÉE]
    
3. Comparez deux réponses générées et déterminez laquelle est la meilleure ou prédisez celle que les utilisateurs sont susceptibles de préférer. Ceci est utile pour générer des données de préférence en vue de l'alignement post-entraînement (abordé au [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) ), du calcul lors des tests (abordé au [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) ) et du classement des modèles par évaluation comparative (abordé dans la section suivante).
    
    « Compte tenu de la question suivante et des deux réponses possibles, déterminez laquelle est la bonne réponse. »
    Mieux. Sortie A ou B.
    Question : [QUESTION]
    A : [PREMIÈRE RÉPONSE]
    B : [DEUXIÈME RÉPONSE]
    La meilleure réponse est :
    

Un système d'évaluation IA généraliste peut être sollicité pour analyser une réponse selon divers critères. Si vous développez un chatbot de jeu de rôle, vous pourriez vérifier si sa réponse correspond au rôle que les utilisateurs souhaitent lui attribuer, par exemple : « Cette réponse évoque-t-elle Gandalf ? » Si vous créez une application de génération de photos promotionnelles de produits, vous pourriez demander : « Sur une échelle de 1 à 5, comment évalueriez-vous la fiabilité du produit présenté sur cette image ? » [Le tableau 3-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_table_3_1730150757038092) présente les critères d'évaluation intégrés les plus courants proposés par certains outils d'IA.

Tableau 3-3. Exemples de critères de jugement intégrés proposés par certains outils d'IA, en septembre 2024. Notez que ces critères intégrés évolueront à mesure que ces outils évolueront.
|Outils d'IA|Critères intégrés|
|---|---|
|[Azure AI Studio](https://oreil.ly/57jOL)|Fondements, pertinence, cohérence, fluidité, similarité|
|[MLflow.metrics](https://oreil.ly/2oEO1)|Fidélité, pertinence|
|[Évaluation des critères de LangChain](https://oreil.ly/R1sCz)|Concision, pertinence, exactitude, cohérence, nocivité, malice, utilité, controverse, misogynie, insensibilité, criminalité|
|[Ragas](https://oreil.ly/5T3ey)|Fidélité, pertinence de la réponse|

Il est essentiel de se rappeler que les critères d'évaluation de l'IA ne sont pas standardisés. Les scores de pertinence d'Azure AI Studio peuvent être très différents de ceux de MLflow. Ces scores dépendent du modèle et de l'instruction sous-jacents de l'évaluateur.

La manière de configurer les instructions pour un juge IA est similaire à celle utilisée pour toute application d'IA. En général, les instructions du juge doivent clairement expliquer les points suivants :

1. La tâche que le modèle doit accomplir consiste par exemple à évaluer la pertinence entre une réponse générée et la question.
    
2. Les critères d'évaluation du modèle doivent être les suivants : « Votre objectif principal doit être de déterminer si la réponse générée contient suffisamment d'informations pour répondre à la question posée, conformément à la réponse de référence. » Plus les instructions sont détaillées, mieux c'est.
    
3. Le système de notation peut être l'un des suivants :
    
    - Classification, par exemple bon/mauvais ou pertinent/non pertinent/neutre.
        
    - Les valeurs numériques discrètes, telles que de 1 à 5, peuvent être considérées comme un cas particulier de classification, où chaque classe a une interprétation numérique au lieu d'une interprétation sémantique.
        
    - Des valeurs numériques continues, par exemple entre 0 et 1, lorsque vous souhaitez évaluer le degré de similarité.
        

###### Conseil

Les modèles de langage sont généralement plus performants avec le texte qu'avec les nombres. Il a été constaté que les systèmes de jugement par IA sont plus efficaces en matière de classification qu'avec les systèmes de notation numérique.

Pour les systèmes de notation numérique, la notation discrète semble plus performante que la notation continue. Empiriquement, plus l'intervalle de notation discrète est large, moins le modèle est précis. Les systèmes de notation discrète classiques se situent entre 1 et 5.

Il a été démontré que les consignes accompagnées d'exemples donnent de meilleurs résultats. Si vous utilisez un système de notation de 1 à 5, incluez des exemples de réponses correspondant à chaque note (1, 2, 3, 4 ou 5) et, si possible, expliquez la justification de chaque note. Les bonnes pratiques en matière de consignes sont abordées au [chapitre 5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) .

Voici un extrait de l'invite utilisée par Azure AI Studio pour évaluer la [_pertinence_](https://oreil.ly/Hlkax) des critères . Elle explique la tâche, les critères, le système de notation, un exemple d'entrée ayant obtenu un score faible et la justification de ce score. Une partie de l'invite a été supprimée par souci de concision.

Votre tâche consiste à évaluer la pertinence entre une réponse générée et la question.
d'après la réponse réelle comprise entre 1 et 5, et veuillez également
Indiquez la raison de la notation.
Votre objectif principal devrait être de déterminer si la réponse générée
contient suffisamment d'informations pour répondre à la question posée selon les
Réponse basée sur la vérité terrain. …
Si la réponse générée contredit la réponse de référence, elle recevra un
faible score de 1 à 2.
Par exemple, à la question « Le ciel est-il bleu ? », la réponse de référence est « Oui,
« Le ciel est bleu. » et la réponse générée est « Non, le ciel n'est pas bleu. »
Dans cet exemple, la réponse générée contredit la réponse de référence.
affirmer que le ciel n'est pas bleu, alors qu'en réalité il l'est.
Cette incohérence se traduirait par une faible note de 1 à 2, et la raison de cette incohérence serait…
Un score faible refléterait la contradiction entre la réponse générée et la
Réponse basée sur la vérité terrain.
          

[La figure 3-8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_8_1730150757025107) montre un exemple de juge IA qui évalue la qualité d'une réponse lorsqu'on lui donne la question.

![Diagramme d'une question. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0308.png)

###### Figure 3-8. Un exemple de juge IA qui évalue la qualité d'une réponse à une question.

Un juge IA n'est pas qu'un simple modèle ; c'est un système qui combine un modèle et une consigne. Modifier le modèle, la consigne ou les paramètres d'échantillonnage du modèle produit un juge différent.

## Les limites de l'IA en tant que juge

Malgré les nombreux avantages de l'IA comme outil d'évaluation, de nombreuses équipes hésitent à adopter cette approche. Utiliser l'IA pour évaluer l'IA semble paradoxal. La nature probabiliste de l'IA la rend apparemment trop peu fiable pour jouer ce rôle. Les systèmes d'évaluation par IA peuvent potentiellement engendrer des coûts et une latence non négligeables pour une application. Compte tenu de ces limitations, certaines équipes considèrent l'IA comme une solution de repli, lorsqu'elles ne disposent d'aucune autre méthode d'évaluation de leurs systèmes, notamment en production.

### Incohérence

Pour qu'une méthode d'évaluation soit fiable, ses résultats doivent être cohérents. Or, les systèmes d'évaluation par IA, comme toutes les applications d'IA, fonctionnent selon des principes probabilistes. Un même système, face à une même entrée, peut attribuer des scores différents selon la manière dont il est interrogé. Même un même système, interrogé avec la même instruction, peut produire des scores différents s'il est exécuté deux fois. Cette incohérence rend difficile la reproduction et la fiabilité des résultats d'évaluation.

Il est possible d'améliorer la cohérence d'un juge IA. [Le chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) explique comment y parvenir grâce à des variables d'échantillonnage. [Zheng et al. (2023)](https://arxiv.org/abs/2306.05685) ont démontré que l'intégration d'exemples d'évaluation dans les consignes permet d'accroître la cohérence de GPT-4 de 65 % à 77,5 %. Ils ont toutefois reconnu qu'une forte cohérence n'implique pas nécessairement une grande précision : le juge peut commettre systématiquement les mêmes erreurs. De plus, l'ajout d'exemples allonge les consignes, ce qui augmente le coût d'inférence. Dans l'expérience de Zheng et al., l'intégration d'exemples supplémentaires dans les consignes a quadruplé le temps de calcul de GPT-4.

### ambiguïté des critères

Contrairement à de nombreuses métriques conçues par l'humain, les métriques utilisées par l'IA pour évaluer les performances ne sont pas standardisées, ce qui peut entraîner des erreurs d'interprétation et des utilisations inappropriées. À l'heure actuelle, les outils open source MLflow, Ragas et LlamaIndex intègrent tous le critère _de fidélité_ permettant de mesurer la pertinence d'une sortie générée par rapport au contexte donné, mais leurs instructions et leurs systèmes de notation diffèrent. Comme le montre le [tableau 3-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_table_4_1730150757038100) , MLflow utilise un système de notation de 1 à 5, Ragas utilise 0 et 1, tandis que LlamaIndex demande à l'utilisateur de répondre par OUI ou NON.

Tableau 3-4. Différents outils peuvent avoir des invites par défaut très difficiles pour les mêmes critères.

|Outil|Invite  <br>[partiellement omise par souci de concision]|Système de notation|
|---|---|---|
|[Flux ML](https://github.com/mlflow/mlflow/blob/5cdae7c4321015620032d02a3b84fb6127247392/mlflow/metrics/genai/prompts/v1.py)|`Faithfulness is only evaluated with the provided output and provided context, please ignore the provided input entirely when scoring faithfulness.` `Faithfulness` `assesses how much of the` `provided` `output is factually consistent with the provided context.…`  <br>  <br><br>`Faithfulness: Below are the details for different scores:`<br><br>`- Score 1: None of the claims in the output can be inferred from the provided` `context.`<br><br>`- Score 2: …`|1–5|
|[Ragas](https://github.com/explodinggradients/ragas/blob/b276f59c0d4eb4795dc28966bfbce14d5aacd140/src/ragas/metrics/_faithfulness.py#L93C1-L94C1)|`Your task is to judge the faithfulness of a series of statements based on a given context. For each statement you must return verdict as 1 if the` `statement` `can be verified based on the context or 0 if the statement can not be verified based on the context.`|0 et 1|
|[Index des lamas](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/evaluation/faithfulness.py)|`Please tell if a given piece of information is supported by the context.`<br><br>`You need to answer with either YES or NO.`<br><br>`Answer YES if any of the context` `supports` `the information, even if most of the context is unrelated. Some examples are` `provided` `below.`<br><br>  <br><br>`Information: Apple pie is generally double-crusted.`<br><br>`Context: An apple pie is a fruit pie… It is generally double-crusted, with` `pastry` `both above and below the filling ...`<br><br>`Answer: YES`|Oui et non|

Les scores de fidélité fournis par ces trois outils ne seront pas comparables. Si, pour une paire (contexte, réponse) donnée, MLflow attribue un score de fidélité de 3, Ragas de 1 et LlamaIndex de NON, quel score utiliseriez-vous ?

Une application évolue avec le temps, mais son évaluation devrait idéalement rester fixe. Ainsi, les indicateurs d'évaluation permettent de suivre les changements de l'application. Cependant, les systèmes d'évaluation par IA sont eux aussi des applications d'IA, ce qui signifie qu'ils peuvent également évoluer.

Imaginez que le mois dernier, le score de cohérence de votre application était de 90 %, et que ce mois-ci, il est de 92 %. Cela signifie-t-il que la cohérence de votre application s'est améliorée ? Il est difficile de répondre à cette question à moins d'être absolument certain que les évaluateurs IA utilisés dans les deux cas sont exactement les mêmes. Que se passe-t-il si le sujet traité par l'évaluateur ce mois-ci est différent de celui du mois dernier ? Peut-être avez-vous opté pour un sujet légèrement plus performant, ou un collègue a corrigé une faute de frappe dans le sujet du mois dernier, et l'évaluateur de ce mois-ci est plus indulgent.

Cela peut s'avérer particulièrement source de confusion si l'application et le système d'évaluation par IA sont gérés par des équipes différentes. L'équipe en charge de l'IA peut modifier la composition des évaluateurs sans en informer l'équipe en charge de l'application. Par conséquent, cette dernière pourrait attribuer à tort les modifications des résultats d'évaluation à des changements au sein de l'application, plutôt qu'à des changements de membres des évaluateurs.

###### Conseil

Ne faites confiance à aucun juge IA si vous ne pouvez pas voir le modèle et l'invite utilisés pour le jugement.

La standardisation des méthodes d'évaluation prend du temps. À mesure que le domaine évolue et que des garde-fous sont mis en place, j'espère que les futurs systèmes d'évaluation par IA deviendront beaucoup plus standardisés et fiables.

### Augmentation des coûts et de la latence

Vous pouvez utiliser des juges IA pour évaluer les applications, aussi bien en phase d'expérimentation qu'en production. De nombreuses équipes les utilisent comme garde-fous en production afin de réduire les risques, en ne présentant aux utilisateurs que les réponses validées par l'IA.

L'utilisation de modèles puissants pour évaluer les réponses peut s'avérer coûteuse. Si vous utilisez GPT-4 pour générer et évaluer les réponses, vous effectuerez deux fois plus d'appels à GPT-4, ce qui doublera approximativement vos coûts d'API. Si vous avez trois questions d'évaluation parce que vous souhaitez évaluer trois critères (par exemple, la qualité globale de la réponse, la cohérence factuelle et la toxicité), vous multiplierez par quatre le nombre d'appels d'API.<sup> [17</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id948)

Vous pouvez réduire les coûts en utilisant des modèles moins performants comme évaluateurs (voir [« Quels modèles peuvent servir d’évaluateurs ? »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_what_models_can_act_as_judges_1730150757064924) ). Vous pouvez également réduire les coûts en effectuant _des vérifications ponctuelles_ : n’évaluer qu’un sous-ensemble de réponses. [Cependant,](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id949) ce type de vérification peut vous amener à ne pas détecter certaines erreurs. Plus le pourcentage d’échantillons évalués est élevé, plus vous aurez confiance dans vos résultats d’évaluation, mais plus les coûts seront importants. Trouver le juste équilibre entre coût et fiabilité peut nécessiter plusieurs essais. Ce processus est abordé plus en détail au [chapitre 4.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) En définitive, les évaluateurs IA sont beaucoup moins coûteux que les évaluateurs humains.

L'intégration de juges IA dans votre pipeline de production peut engendrer de la latence. Si vous évaluez les réponses avant de les renvoyer aux utilisateurs, vous devez faire un compromis : un risque réduit, mais une latence accrue. Cette latence supplémentaire peut rendre cette option inenvisageable pour les applications aux exigences de latence strictes.

### Les biais de l'IA en tant que juge

Les évaluateurs humains ont des biais, tout comme les systèmes d'évaluation par IA. Ces biais varient d'une IA à l'autre. Cette section abordera certains des plus courants. Comprendre les biais de vos systèmes d'évaluation par IA vous permettra d'interpréter correctement leurs scores et même de les atténuer.

Les systèmes d'évaluation par intelligence artificielle ont tendance à présenter _un biais d'auto-évaluation_ : un modèle privilégie ses propres réponses par rapport à celles générées par d'autres modèles. Le même mécanisme qui permet à un modèle de calculer la réponse la plus probable lui attribue également un score élevé. Dans [l'expérience de Zheng et al. (2023)](https://arxiv.org/abs/2306.05685) , GPT-4 se favorise avec un taux de victoire supérieur de 10 %, tandis que Claude-v1 se favorise avec un taux de victoire supérieur de 25 %.

De nombreux modèles d'IA présentent un biais de première position. Un système d'évaluation par IA peut privilégier la première réponse lors d'une comparaison par paires ou la première dans une liste d'options. Ce biais peut être atténué en répétant le même test plusieurs fois avec des ordres différents ou en utilisant des consignes soigneusement conçues. Le biais de position de l'IA est l'inverse de celui des humains. Ces derniers ont tendance à privilégier [la dernière réponse vue](https://oreil.ly/2XDI0) _,_ un phénomène appelé _biais de récence_ .

Certains systèmes d'évaluation par intelligence artificielle présentent _un biais de verbosité_ , privilégiant les réponses les plus longues, indépendamment de leur qualité. [Wu et Aji (2023)](https://arxiv.org/abs/2307.03025) ont constaté que GPT-4 et Claude-1 préfèrent les réponses longues (environ 100 mots) comportant des erreurs factuelles aux réponses courtes et correctes (environ 50 mots). [Saito et al. (2023)](https://oreil.ly/IOp9H) ont étudié ce biais dans le cadre de tâches créatives et ont observé que lorsque la différence de longueur est suffisamment importante (par exemple, une réponse deux fois plus longue que l'autre), le système privilégie presque systématiquement la plus longue. [Cependant](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id952) , Zheng et al. (2023) et Saito et al. (2023) ont tous deux constaté que GPT-4 est moins sujet à ce biais que GPT-3.5, ce qui suggère que ce biais pourrait disparaître à mesure que les modèles gagnent en puissance.

Outre ces biais, les systèmes d'évaluation par IA présentent les mêmes limitations que toutes les applications d'IA, notamment en matière de confidentialité et de propriété intellectuelle. Si vous utilisez un modèle propriétaire, vous devrez lui transmettre vos données. Or, si le fournisseur du modèle ne divulgue pas ses données d'entraînement, vous ne pourrez pas être certain que son utilisation commerciale est sans risque.

Malgré les limites de l'IA comme système de jugement, ses nombreux avantages me laissent penser que son adoption continuera de croître. Toutefois, les systèmes de jugement par IA devraient être complétés par des méthodes d'évaluation précises et/ou une évaluation humaine.

## Quels mannequins peuvent faire office de juges ?

Le juge peut être plus fort, plus faible ou de même niveau que le modèle évalué. Chaque scénario présente des avantages et des inconvénients.

À première vue, l'idée d'un correcteur plus compétent semble logique. Le correcteur ne devrait-il pas être plus compétent que le candidat ? Non seulement les modèles plus performants peuvent formuler de meilleurs jugements, mais ils peuvent aussi contribuer à l'amélioration des modèles moins performants en les guidant vers des réponses plus pertinentes.

Vous vous demandez peut-être : si vous avez déjà accès à un modèle plus performant, pourquoi utiliser un modèle moins puissant pour générer les réponses ? La réponse tient au coût et à la latence. Votre budget ne vous permet peut-être pas d’utiliser le modèle le plus performant pour générer toutes les réponses ; vous l’utilisez donc pour évaluer un sous-ensemble de celles-ci. Par exemple, vous pouvez utiliser un modèle interne peu coûteux pour générer les réponses et GPT-4 pour évaluer 1 % d’entre elles.

Le modèle le plus performant peut également être trop lent pour votre application. Vous pouvez utiliser un modèle rapide pour générer les réponses, tandis que le modèle plus performant, mais plus lent, effectue l'évaluation en arrière-plan. Si le modèle performant juge la réponse du modèle moins performante incorrecte, des mesures correctives peuvent être prises, comme la mise à jour de la réponse avec celle du modèle performant. Notez que le schéma inverse est également courant : vous utilisez un modèle performant pour générer les réponses, tandis qu'un modèle moins performant s'exécute en arrière-plan pour effectuer l'évaluation.

Utiliser le modèle le plus performant comme juge pose deux problèmes. Premièrement, ce modèle se retrouvera sans juge approprié. Deuxièmement, il nous faut une autre méthode d'évaluation pour déterminer quel modèle est le plus performant.

Utiliser un modèle pour s'auto _-évaluer_ , ou _autocritique_ , peut sembler trompeur, notamment en raison du risque de biais d'auto-évaluation. Cependant, l'auto-évaluation peut s'avérer très utile pour vérifier la cohérence des résultats. Si un modèle estime que sa propre réponse est incorrecte, sa fiabilité est probablement compromise. Au-delà de cette vérification, demander à un modèle de s'auto-évaluer peut l'inciter à réviser et à améliorer ses réponses ( [Press et al., 2022](https://arxiv.org/abs/2210.03350) ; [Gou et al., 2023](https://arxiv.org/abs/2305.11738) ; [Valmeekamet et al., 2023](https://arxiv.org/abs/2310.08118) ). L'exemple [suivant](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id955) illustre ce à quoi pourrait ressembler une auto-évaluation :

**Question [de l'utilisateur]** : Combien font 10 + 3 ?
 **Première réponse [de l'IA]** : 30.
 **Auto-évaluation [de l'IA]** : Cette réponse est-elle correcte ?
 **Réponse finale [de l'IA]** : Non. La bonne réponse est 13.
          

Une question demeure : le modèle d’évaluation peut-il être moins performant que le modèle évalué ? Certains affirment qu’évaluer est plus aisé que générer. N’importe qui peut avoir un avis sur la qualité d’une chanson, mais tout le monde ne sait pas composer. Des modèles moins performants devraient pouvoir évaluer les résultats de modèles plus performants.

[Zheng et al. (2023)](https://arxiv.org/abs/2306.05685) ont constaté que les modèles plus performants correspondent mieux aux préférences humaines, ce qui incite les individus à choisir les modèles les plus performants qu'ils peuvent se permettre. Cependant, cette expérience se limitait à des juges généralistes. Une piste de recherche qui me passionne est celle des juges spécialisés, de petite taille. Ces juges spécialisés sont formés pour formuler des jugements spécifiques, selon des critères et des systèmes de notation précis. Un juge spécialisé, de petite taille, peut se révéler plus fiable qu'un juge généraliste plus important pour des jugements spécifiques.

Du fait des nombreuses possibilités d'utilisation des juges IA, il existe de nombreux juges IA spécialisés. Je vais ici présenter trois exemples de juges spécialisés : les modèles de récompense, les juges basés sur des références et les modèles de préférence.

Modèle de récompense

Un modèle de récompense prend en entrée une paire (invite, réponse) et évalue la pertinence de la réponse en fonction de l'invite. Les modèles de récompense sont utilisés avec succès dans l'apprentissage par renforcement à long terme (RLHF) depuis de nombreuses années. [Cappy,](https://arxiv.org/abs/2311.06720) développé par Google en 2023, est un exemple de modèle de récompense. À partir d'une paire (invite, réponse), Cappy attribue un score entre 0 et 1, indiquant la justesse de la réponse. Cappy est un système d'évaluation léger, doté de 360 ​​millions de paramètres, bien plus petit que les modèles de base à usage général.

juge fondé sur des références

Un système d'évaluation par référence compare la réponse générée à une ou plusieurs réponses de référence. Ce système peut attribuer un score de similarité ou un score de qualité (évaluant la pertinence de la réponse générée par rapport aux réponses de référence). Par exemple, BLEURT ( [Sellam et al., 2020](https://arxiv.org/abs/2004.04696) ) prend en entrée une paire (réponse candidate, réponse de référence) et calcule un score de similarité entre la réponse candidate et la réponse de référence. [Prometheus](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id959) ( [Kim et al., 2023](https://arxiv.org/abs/2310.08491) ) prend en entrée (consigne, réponse générée, réponse de référence, grille d'évaluation) et attribue un score de qualité compris entre 1 et 5, en supposant que la réponse de référence obtienne la note maximale de 5.

Modèle de préférence

Un modèle de préférence prend en entrée (invite, réponse 1, réponse 2) et détermine laquelle des deux réponses est la meilleure (préférée par les utilisateurs) pour l'invite donnée. Il s'agit là d'une des pistes les plus prometteuses pour les évaluateurs spécialisés. La capacité à prédire les préférences humaines ouvre de nombreuses perspectives. Comme indiqué au [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) , les données de préférence sont essentielles pour aligner les modèles d'IA sur les préférences humaines, mais leur obtention est complexe et coûteuse. Disposer d'un bon prédicteur des préférences humaines facilite généralement l'évaluation et rend les modèles plus sûrs à utiliser. De nombreuses initiatives ont été menées pour développer des modèles de préférence, notamment PandaLM ( [Wang et al., 2023](https://arxiv.org/abs/2306.05087) ) et JudgeLM ( [Zhu et al., 2023](https://arxiv.org/abs/2310.17631) ). [La figure 3-9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_9_1730150757025114) illustre le fonctionnement de PandaLM. Ce modèle indique non seulement la meilleure réponse, mais en explique également le raisonnement.

![Diagramme d'un diagramme. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0309.png)

###### Figure 3-9. Exemple de résultat de PandaLM, à partir d'une requête humaine et de deux réponses générées. Image tirée de Wang et al. (2023), légèrement modifiée pour plus de clarté. L'image originale est disponible sous licence Apache 2.0.

Malgré ses limites, l'approche de l'IA comme juge est polyvalente et performante. L'utilisation de modèles moins coûteux comme juges la rend encore plus utile. Nombre de mes collègues, initialement sceptiques, ont commencé à s'y fier davantage en production.

L'idée d'une IA comme juge est passionnante, et la prochaine approche que nous allons aborder est tout aussi fascinante. Elle s'inspire de la conception de jeux vidéo, un domaine captivant..

# Modèles de classement avec évaluation comparative

Souvent, on évalue des modèles non pas pour leurs scores, mais pour savoir lequel est le plus adapté à nos besoins. On souhaite alors obtenir un classement de ces modèles. Ce classement peut se faire par une évaluation ponctuelle ou par une évaluation comparative.

L'évaluation par points consiste à évaluer chaque modèle indépendamment, [puis](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id965) à les classer selon leurs scores. Par exemple, pour déterminer le meilleur danseur, on évalue chaque danseur individuellement, on lui attribue un score, puis on choisit celui qui a obtenu le score le plus élevé.

L'évaluation comparative permet de comparer différents modèles et d'établir un classement à partir des résultats. Pour un même concours de danse, on peut demander à tous les candidats de danser côte à côte, puis interroger les juges sur leur préférence et désigner le danseur ayant recueilli le plus de votes.

Pour les réponses dont la qualité est subjective, l'évaluation comparative est généralement plus aisée que l'évaluation par points. Par exemple, il est plus facile de déterminer laquelle des deux chansons est la meilleure que d'attribuer à chacune une note précise.

En intelligence artificielle, l'évaluation comparative a été utilisée pour la première fois en 2021 par [Anthropic](https://arxiv.org/abs/2112.00861) pour classer différents modèles. Elle est également au cœur du classement [Chatbot Arena](https://oreil.ly/MHt5H) de LMSYS , qui classe les modèles à l'aide de scores calculés à partir de comparaisons par paires effectuées par la communauté.

De nombreux fournisseurs de modèles utilisent l'évaluation comparative pour évaluer leurs modèles en production. [La figure 3-10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_figure_10_1730150757025123) illustre un exemple où ChatGPT invite ses utilisateurs à comparer deux résultats côte à côte. Ces résultats peuvent être générés par des modèles différents, ou par le même modèle avec des variables d'échantillonnage différentes.

![Capture d'écran d'un dictionnaire. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0310.png)

###### Figure 3-10. ChatGPT demande parfois aux utilisateurs de comparer deux résultats côte à côte.

Pour chaque requête, au moins deux modèles sont sélectionnés. Un évaluateur, humain ou IA, désigne le modèle gagnant. De nombreux développeurs autorisent les égalités afin d'éviter un choix aléatoire lorsque les versions sont d'égale qualité.

Il est essentiel de garder à l'esprit que _toutes les questions ne doivent pas être traitées par préférence_ . Il est souvent préférable de privilégier la justesse des réponses. Imaginez que vous demandiez au modèle : « Existe-t-il un lien entre les radiations des téléphones portables et les tumeurs cérébrales ? » et que le modèle vous propose deux options : « Oui » et « Non ». Un vote basé sur les préférences peut induire des signaux erronés qui, s'ils sont utilisés pour entraîner votre modèle, peuvent engendrer des comportements inadaptés.

Demander aux utilisateurs de choisir peut aussi engendrer de la frustration. Imaginez que vous posiez une question de maths au modèle parce que vous ne connaissez pas la réponse, et que le modèle vous donne deux réponses différentes en vous demandant de choisir celle que vous préférez. Si vous aviez connu la bonne réponse, vous n'auriez même pas posé la question au modèle.

Lorsqu'on recueille des avis comparatifs d'utilisateurs, l'une des difficultés consiste à déterminer quelles questions peuvent être résolues par un vote de préférence et lesquelles ne devraient pas l'être. Le vote de préférence n'est pertinent que si les votants maîtrisent le sujet. Cette approche fonctionne généralement dans les applications où l'IA joue un rôle d'assistant, aidant les utilisateurs à accélérer les tâches qu'ils savent effectuer, et non lorsque les utilisateurs demandent à l'IA d'effectuer des tâches qu'ils ne savent pas réaliser eux-mêmes.

Il ne faut pas confondre l'évaluation comparative avec les tests A/B. Lors d'un test A/B, l'utilisateur visualise les résultats d'un seul modèle candidat à la fois. En revanche, lors d'une évaluation comparative, l'utilisateur visualise simultanément les résultats de plusieurs modèles.

Chaque comparaison est appelée une_match_ . Ce processus aboutit à une série de comparaisons, comme indiqué dans [le tableau 3-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_table_5_1730150757038107) .

Tableau 3-5. Exemples d'historique de comparaisons de modèles par paires.
|Correspondre #|Modèle A|Modèle B|Gagnant|
|---|---|---|---|
|1|Modèle 1|Modèle 2|Modèle 1|
|2|Modèle 3|Modèle 10|Modèle 10|
|3|Modèle 7|Modèle 4|Modèle 4|
|…||||

La probabilité que le modèle A soit préféré au modèle B correspond au _taux de victoire_ de A par rapport à B. On peut calculer ce taux de victoire en examinant tous les matchs entre A et B et en calculant le pourcentage de victoires de A.

S'il n'y a que deux modèles, les classer est simple : le modèle le plus souvent gagnant est mieux classé. Plus il y a de modèles, plus le classement devient complexe. Prenons l'exemple de cinq modèles, avec les taux de victoire empiriques entre paires de modèles présentés dans [le tableau 3-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_table_6_1730150757038117) . À première vue, il n'est pas évident de classer ces cinq modèles.

Tableau 3-6. Exemples de taux de victoire de cinq modèles. La colonne A >> B indique l'événement où A est préféré à B.
|Modèle paire #|Modèle A|Modèle B|# correspondances|A >> B|
|---|---|---|---|---|
|1|Modèle 1|Modèle 2|1000|90%|
|2|Modèle 1|Modèle 3|1000|40%|
|3|Modèle 1|Modèle 4|1000|15%|
|4|Modèle 1|Modèle 5|1000|10%|
|5|Modèle 2|Modèle 3|1000|60%|
|6|Modèle 2|Modèle 4|1000|80%|
|7|Modèle 2|Modèle 5|1000|80%|
|8|Modèle 3|Modèle 4|1000|70%|
|9|Modèle 3|Modèle 5|1000|10%|
|10|Modèle 4|Modèle 5|1000|20%|

À partir de signaux comparatifs, un _algorithme d'évaluation_ est utilisé pour établir un classement des modèles. Généralement, cet algorithme calcule d'abord un score pour chaque modèle à partir des signaux comparatifs, puis classe les modèles en fonction de leurs scores.

L'évaluation comparative est un concept récent en intelligence artificielle, mais elle est utilisée depuis près d'un siècle dans d'autres secteurs. Elle est particulièrement répandue dans le sport et les jeux vidéo. De nombreux algorithmes de notation développés pour ces autres domaines peuvent être adaptés à l'évaluation des modèles d'IA, tels que Elo, Bradley-Terry et TrueSkill.LMSYS Chatbot Arena utilisait initialement le système Elo pour calculer le classement des modèles, mais est ensuite passé à l'algorithme de Bradley-Terry, car il s'est avéré que le système Elo était sensible à l'ordre des évaluateurs et des invites. [23](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id970)

_Un classement est correct si, pour toute paire de modèles, le modèle le mieux classé a plus de chances de l'emporter face au modèle le moins bien classé_ . Si le modèle A est mieux classé que le modèle B, les utilisateurs devraient préférer le modèle A au modèle B plus de la moitié du temps.

Dans cette optique, le classement des modèles est un problème de prédiction. On calcule un classement à partir des résultats des matchs historiques et on l'utilise pour prédire les résultats futurs. Différents algorithmes de classement peuvent produire des résultats différents, et il n'existe pas de classement de référence. La qualité d'un classement est déterminée par sa capacité à prédire les résultats futurs. Mon analyse du classement de Chatbot Arena montre que le classement produit est bon, du moins pour les paires de modèles ayant un nombre suffisant de matchs. L'analyse est disponible sur le [dépôt GitHub du livre.](https://github.com/chiphuyen/aie-book)

## Les défis de l'évaluation comparative

Dans le cadre d'une évaluation ponctuelle, la partie la plus complexe consiste à concevoir le référentiel et les indicateurs permettant de recueillir les signaux pertinents. Le calcul des scores pour classer les modèles est aisé. En revanche, avec une évaluation comparative, la collecte des signaux et le classement des modèles s'avèrent plus difficiles. Cette section aborde les trois principaux défis de l'évaluation comparative.

### Goulots d'étranglement liés à l'évolutivité

L'évaluation comparative est gourmande en données. Le nombre de paires de modèles à comparer croît de façon quadratique avec le nombre de modèles. En janvier 2024, LMSYS a évalué 57 modèles à l'aide de 244 000 comparaisons. Bien que cela puisse paraître beaucoup, cela ne représente en moyenne que 153 comparaisons par paire de modèles (57 modèles correspondent à 1 596 paires de modèles). Ce nombre est faible, compte tenu de la grande variété de tâches qu'un modèle de base est censé accomplir.

Heureusement, il n'est pas toujours nécessaire de comparer directement deux modèles pour déterminer lequel est le meilleur. Les algorithmes de classement supposent généralement _la transitivité_ . Si le modèle A est mieux classé que le modèle B, et que le modèle B est mieux classé que le modèle C, alors, par transitivité, on peut déduire que le modèle A est mieux classé que le modèle C. Autrement dit, si l'algorithme est certain que le modèle A est meilleur que le modèle B et que le modèle B est meilleur que le modèle C, il n'a pas besoin de comparer le modèle A au modèle C pour le savoir.

Cependant, il n'est pas clair si cette hypothèse de transitivité s'applique aux modèles d'IA.De nombreux articles analysant le système Elo pour l'évaluation de l'IA pointent du doigt l'hypothèse de transitivité comme une limite ( [Boubdir et al.](https://arxiv.org/abs/2311.17295) ; [Balduzzi et al.](https://arxiv.org/abs/1806.02643) ; et [Munos et al.](https://arxiv.org/abs/2312.00886) ). Ils soutiennent que la préférence humaine n'est pas nécessairement transitive. De plus, la non-transitivité peut s'expliquer par le fait que différentes paires de modèles sont évaluées par différents évaluateurs et à partir de consignes différentes.

Il y a aussi la difficulté d'évaluer les nouveaux modèles. L'évaluation indépendante consiste à évaluer uniquement le nouveau modèle. L'évaluation comparative, quant à elle, implique de comparer le nouveau modèle aux modèles existants, ce qui peut modifier le classement de ces derniers.

Cela complique également l'évaluation des modèles privés. Imaginez que vous ayez créé un modèle pour votre entreprise, à partir de données internes. Vous souhaitez comparer ce modèle avec des modèles publics afin de déterminer s'il serait plus avantageux d'utiliser un modèle public.Si vous souhaitez utiliser une évaluation comparative pour votre modèle, vous devrez probablement collecter vos propres signaux comparatifs et créer votre propre classement, ou payer l'un de ces classements publics pour qu'il effectue une évaluation privée pour vous.

Le problème de passage à l'échelle peut être atténué grâce à de meilleurs algorithmes d'appariement. Jusqu'à présent, nous avons supposé que les modèles étaient sélectionnés aléatoirement pour chaque appariement, de sorte que toutes les paires de modèles apparaissent dans un nombre approximativement égal d'appariements. Cependant, il n'est pas nécessaire de comparer toutes les paires de modèles de manière égale. Dès que nous sommes confiants quant au résultat d'une paire de modèles, nous pouvons cesser de les apparier. Un algorithme d'appariement efficace devrait privilégier les appariements qui réduisent le plus l'incertitude dans le classement général.

### Manque de normalisation et de contrôle de la qualité

Une méthode pour recueillir des données comparatives consiste à solliciter l'avis de la communauté, à l'instar de LMSYS Chatbot Arena. N'importe qui peut se rendre sur [le site web](https://oreil.ly/td_MY) , saisir une question, recevoir deux réponses de deux modèles anonymes et voter pour le meilleur. Les noms des modèles ne sont révélés qu'après la clôture du vote.

Cette approche présente l'avantage de capter un large éventail de signaux et se révèle relativement difficile à manipuler.<sup> [24</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id976) Toutefois, son inconvénient réside dans la difficulté à imposer une standardisation et un contrôle qualité.

Premièrement, toute personne ayant accès à Internet peut utiliser n'importe quelle question pour évaluer ces modèles, et il n'existe aucune norme définissant ce qui constitue une meilleure réponse. Il serait peut-être excessif d'attendre des volontaires qu'ils vérifient l'exactitude des réponses ; ils pourraient donc, sans le savoir, privilégier des réponses qui paraissent meilleures, mais qui sont factuellement incorrectes.

Certaines personnes préfèrent des réponses polies et modérées, tandis que d'autres privilégient les réponses sans filtre. C'est à la fois un avantage et un inconvénient. Un avantage, car cela permet de refléter les préférences humaines en situation réelle. Un inconvénient, car ces préférences ne sont pas toujours adaptées. Par exemple, si un utilisateur demande à un modèle de raconter une blague déplacée et que celui-ci refuse, l'utilisateur pourrait voter contre. Or, en tant que développeur d'application, vous préféreriez peut-être que le modèle refuse. Certains utilisateurs pourraient même, par malveillance, sélectionner les réponses toxiques comme leurs préférées, faussant ainsi le classement.

Deuxièmement, les comparaisons participatives exigent que les utilisateurs évaluent les modèles en dehors de leur environnement de travail. Sans ancrage dans la réalité, les questions posées lors des tests risquent de ne pas refléter l'utilisation concrète de ces modèles. Les participants pourraient se contenter des premières questions qui leur viennent à l'esprit, sans recourir à des techniques de questionnement sophistiquées.

Parmi [les 33 000 requêtes](https://oreil.ly/eI9Vq) publiées par LMSYS Chatbot Arena en 2023, 180 sont « bonjour » et « salut », soit 0,55 % des données, sans compter les variantes comme « bonjour ! », « bonjour. », « hola », « hey », etc. On y trouve de nombreuses énigmes. La question « X a 3 sœurs, chacune a un frère. Combien de frères X a-t-il ? » a été posée 44 fois.

Les questions simples sont faciles à répondre, ce qui rend difficile la différenciation des performances des modèles. L'évaluation des modèles à l'aide d'un trop grand nombre de questions simples peut fausser le classement.

Si un classement public ne prend pas en charge la construction de contexte sophistiquée, comme l'enrichissement du contexte avec des documents pertinents extraits de vos bases de données internes, son classement ne reflétera pas la performance potentielle d'un modèle pour votre système RAG. La capacité à générer de bonnes réponses est différente de la capacité à extraire les documents les plus pertinents.

Une solution possible pour imposer une standardisation consiste à limiter les utilisateurs à un ensemble de requêtes prédéfinies. Cependant, cela pourrait nuire à la capacité du classement à refléter la diversité des cas d'utilisation. LMSYS, quant à lui, permet aux utilisateurs d'utiliser n'importe quelle requête, mais filtre ensuite [les requêtes strictes](https://x.com/lmarena_ai/status/1792625968865026427) à l'aide de son modèle interne et classe les modèles en ne retenant que ces dernières.

Une autre solution consiste à faire appel uniquement à des évaluateurs de confiance. On peut les former aux critères de comparaison de deux réponses ou à l'utilisation de questions pratiques et de techniques d'incitation sophistiquées. C'est l'approche employée par Scale pour [son classement comparatif privé](https://oreil.ly/kIJ9F) . Le principal inconvénient de cette méthode est son coût élevé et la réduction importante du nombre de comparaisons possibles.

Une autre option consiste à intégrer une évaluation comparative à vos produits et à permettre aux utilisateurs d'évaluer les modèles lors de leurs tâches. Par exemple, pour la génération de code, vous pouvez suggérer deux extraits de code dans l'éditeur de code de l'utilisateur et le laisser choisir le meilleur. De nombreuses applications de messagerie instantanée le font déjà. Cependant, comme mentionné précédemment, l'utilisateur peut ne pas savoir quel extrait de code est le plus pertinent, car il n'est pas expert.

De plus, les utilisateurs peuvent ne pas lire les deux options et cliquer au hasard sur l'une d'elles. Cela peut fausser considérablement les résultats. Cependant, les indications provenant du faible pourcentage d'utilisateurs qui votent correctement peuvent parfois suffire à déterminer quel modèle est le meilleur.

_Certaines équipes privilégient l'IA aux évaluateurs humains. Si l'IA n'égale peut-être pas les experts humains qualifiés, elle peut néanmoins se révéler plus fiable que les internautes lambda_ .

### De la performance comparative à la performance absolue

Pour de nombreuses applications, nous n'avons pas forcément besoin des meilleurs modèles possibles. Un modèle suffisamment performant suffit. L'évaluation comparative nous indique quel modèle est le meilleur, mais elle ne nous renseigne ni sur la qualité intrinsèque d'un modèle, ni sur son adéquation à notre cas d'utilisation. Supposons que le classement indique que le modèle B est meilleur que le modèle A. Plusieurs scénarios peuvent alors se présenter :

1. Le modèle B est bon, mais le modèle A est mauvais.
    
2. Les deux modèles, A et B, sont mauvais.
    
3. Les deux modèles, A et B, sont bons.
    

Vous avez besoin d'autres formes d'évaluation pour déterminer quel scénario est vrai.

Imaginons que nous utilisions le modèle A pour le support client, et que ce modèle résolve 70 % des tickets. Considérons maintenant le modèle B, qui l'emporte sur le modèle A dans 51 % des cas. Il est difficile de déterminer comment ce taux de réussite de 51 % se traduit en nombre de requêtes que le modèle B peut résoudre. Plusieurs personnes m'ont indiqué que, d'après leur expérience, une variation de 1 % du taux de réussite peut entraîner un gain de performance considérable dans certaines applications, mais un gain minime dans d'autres.

Lorsqu'il s'agit de choisir entre A et B, les préférences personnelles ne font pas tout. Le coût est également un facteur important. Ignorer le gain de performance attendu complique l'analyse coûts-avantages. Si le modèle B coûte deux fois plus cher que le modèle A, une simple comparaison ne suffit pas à déterminer si le gain de performance justifie le surcoût.

## L'avenir de l'évaluation comparative

Compte tenu des nombreuses limites de l'évaluation comparative, on peut se demander si elle a un avenir. Pourtant, elle présente de nombreux avantages. Tout d'abord, comme évoqué dans la section [« Post-entraînement »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_post_training_1730147895572108) , il s'avère plus simple de comparer deux résultats que d'attribuer à chacun une note précise. À mesure que les modèles deviennent plus performants et surpassent les performances humaines, il pourrait devenir impossible pour les évaluateurs humains d'attribuer des notes précises aux réponses des modèles. Cependant, ils pourraient toujours être capables de déceler la différence, et l'évaluation comparative pourrait alors demeurer la seule option. Par exemple, l'article sur Llama 2 a montré que même lorsque le modèle s'aventure dans un type d'écriture dépassant les capacités des meilleurs annotateurs humains, ces derniers peuvent encore fournir un retour d'information précieux en comparant deux réponses ( [Touvron et al., 2023](https://arxiv.org/abs/2307.09288) ).

Deuxièmement, l'évaluation comparative vise à saisir la qualité qui nous importe le plus : la préférence humaine. Elle réduit la nécessité de créer constamment de nouveaux référentiels pour suivre le rythme des progrès fulgurants de l'IA. Contrairement aux référentiels qui deviennent obsolètes lorsque les performances des modèles atteignent la perfection, les évaluations comparatives ne seront jamais saturées tant que de nouveaux modèles plus performants seront mis au point.

L'évaluation comparative est relativement difficile à manipuler, car il n'existe pas de moyen simple de tricher, comme entraîner son modèle sur des données de référence. C'est pourquoi beaucoup font davantage confiance aux résultats des classements comparatifs publics qu'à ceux de tout autre classement public.

L'évaluation comparative peut nous fournir des informations précieuses sur les modèles, informations qu'il serait impossible d'obtenir autrement. Pour une évaluation hors ligne, elle constitue un excellent complément aux référentiels d'évaluation. Pour une évaluation en ligne, elle peut être complémentaire aux tests A/B.

# Résumé

Plus les modèles d'IA sont performants, plus le risque de défaillances catastrophiques est élevé, ce qui rend l'évaluation d'autant plus cruciale. Or, évaluer des modèles puissants et ouverts représente un véritable défi. Face à ces difficultés, de nombreuses équipes se tournent vers l'évaluation humaine. L'intervention humaine pour vérifier la cohérence des données est toujours utile, et dans bien des cas, elle est indispensable. Ce chapitre s'est toutefois concentré sur différentes approches de l'évaluation automatique.

Ce chapitre s'ouvre sur une analyse des raisons pour lesquelles les modèles de base sont plus difficiles à évaluer que les modèles d'apprentissage automatique traditionnels. Malgré le développement de nombreuses nouvelles techniques d'évaluation, les investissements dans ce domaine restent inférieurs à ceux consacrés au développement des modèles et des applications.

Comme de nombreux modèles de base comportent un module de modélisation du langage, nous avons examiné de plus près les métriques de modélisation du langage, notamment la perplexité et l'entropie croisée. Beaucoup de personnes à qui j'ai parlé trouvent ces métriques complexes ; j'ai donc inclus une section expliquant comment les interpréter et les exploiter pour l'évaluation et le traitement des données.

Ce chapitre s'est ensuite intéressé aux différentes méthodes d'évaluation des réponses ouvertes, notamment la correction fonctionnelle, les scores de similarité et l'intelligence artificielle comme juge. Les deux premières méthodes sont exactes, tandis que l'évaluation par l'IA est subjective.

Contrairement à l'évaluation objective, les mesures subjectives dépendent fortement de l'évaluateur. Leurs scores doivent être interprétés en fonction des évaluateurs utilisés. Des scores visant à mesurer une même qualité par différents évaluateurs IA peuvent ne pas être comparables. Les évaluateurs IA, comme toutes les applications d'IA, doivent être améliorés par itération, ce qui signifie que leurs jugements évoluent. De ce fait, ils ne constituent pas des points de référence fiables pour suivre les changements d'une application au fil du temps. Bien que prometteurs, les évaluateurs IA devraient être complétés par une évaluation objective, une évaluation humaine, ou les deux.

Lors de l'évaluation de modèles, il est possible d'évaluer chaque modèle indépendamment, puis de les classer selon leurs scores. On peut également les classer à l'aide de signaux comparatifs : lequel des deux modèles est le meilleur ? L'évaluation comparative est courante dans le domaine sportif, notamment aux échecs, et gagne en popularité dans l'évaluation de l'IA. Tant l'évaluation comparative que le processus d'alignement post-entraînement nécessitent des signaux de préférence, dont la collecte est coûteuse. Ceci a motivé le développement de modèles de préférence : des juges d'IA spécialisés qui prédisent la réponse préférée des utilisateurs.

Bien que les métriques de modélisation du langage et les mesures de similarité conçues manuellement existent depuis un certain temps, l'IA en tant qu'outil d'évaluation et d'analyse comparative ne s'est généralisée qu'avec l'émergence des modèles de base. De nombreuses équipes cherchent à les intégrer à leurs processus d'évaluation. Le chapitre suivant abordera la conception d'un processus d'évaluation fiable pour les applications ouvertes.

[1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id871-marker)En décembre 2023, Greg Brockman, cofondateur d'OpenAI, [a tweeté](https://x.com/gdb/status/1733553161884127435) que « les évaluations sont étonnamment souvent tout ce dont vous avez besoin ».

[2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id872-marker)Une étude réalisée en 2023 par [a16z](https://oreil.ly/fti6d) a montré que 6 décideurs sur 70 évaluaient les modèles par le bouche-à-oreille.

[3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id873-marker)Également connu sous le nom de _test d'ambiance_ .

[4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id874-marker)Lors de la sortie de GPT-O1 d'OpenAI en septembre 2024, [Terrence Tao, lauréat de la médaille Fields,](https://oreil.ly/4KJQM) a comparé l'expérience de travail avec ce modèle à celle avec « un étudiant de troisième cycle moyen, mais pas totalement incompétent ». Il a émis l'hypothèse qu'une ou deux itérations supplémentaires suffiraient peut-être pour que l'IA atteigne le niveau d'un « étudiant de troisième cycle compétent ». En réaction à cette analyse, beaucoup ont ironisé sur le fait que si nous en sommes déjà au point où nous avons besoin des esprits les plus brillants pour évaluer les modèles d'IA, nous n'aurons bientôt plus personne de qualifié pour évaluer les modèles futurs.

[5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id875-marker)J'ai recherché tous les dépôts ayant au moins 500 étoiles en utilisant les mots-clés « LLM », « GPT », « génératif » et « transformateur ». J'ai également fait appel à la communauté pour trouver les dépôts manquants via mon site web [_https://huyenchip.com_](https://huyenchip.com/llama-police) .

[6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id878-marker)Bien qu'il existe une forte corrélation, les performances de la modélisation du langage n'expliquent pas entièrement les performances en aval. Ce domaine fait l'objet de recherches actives.

[7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id881-marker)Comme expliqué au [chapitre 1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_introduction_to_building_ai_applications_with_foun_1730130814984319) , un jeton peut être un caractère, un mot ou une partie de mot. Lorsque Claude Shannon a introduit la notion d'entropie en 1951, il travaillait avec des caractères. Voici [sa définition de](https://oreil.ly/HjUlH) l'entropie : _«_ L'entropie est un paramètre statistique qui mesure, en quelque sorte, la quantité d'information produite en moyenne pour chaque lettre d'un texte dans la langue. Si la langue est traduite en chiffres binaires (0 ou 1) de la manière la plus efficace, l'entropie correspond au nombre moyen de chiffres binaires nécessaires par lettre de la langue originale. »

[8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id892-marker)L'une des raisons pour lesquelles de nombreuses personnes préfèrent le logarithme népérien au logarithme en base 2 est que le logarithme népérien possède certaines propriétés qui simplifient ses calculs. Par exemple, la dérivée du logarithme népérien ln( _x_ ) est 1/ _x_ .

[9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id895-marker)Si vous n'êtes pas sûr de ce que signifient SFT (supervised finetuning) et RLHF (reinforcement learning from human feedback), consultez [le chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) .

[10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id896-marker)La quantification est abordée au [chapitre 7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) .

[11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id906-marker)Le problème est que, si de nombreuses tâches complexes ont des objectifs mesurables, l'IA n'est pas encore suffisamment performante pour les réaliser de bout en bout. Elle peut donc être utilisée pour une partie de la solution. Parfois, évaluer une partie d'une solution est plus difficile qu'évaluer le résultat final. Imaginez que vous vouliez évaluer les compétences d'un joueur d'échecs. Il est plus facile d'évaluer le résultat de la partie (victoire, défaite ou nulle) que d'évaluer un seul coup.

[12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id922-marker)Vous pourriez également vouloir effectuer un traitement selon que vous souhaitiez que « cats » et « cat » ou « will not » et « won't » soient considérés comme deux jetons distincts.

[13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id927-marker)Bien qu'un espace vectoriel à 10 000 éléments puisse paraître de grande dimension, sa dimensionnalité est bien inférieure à celle des données brutes. Un plongement est donc considéré comme une représentation de données complexes dans un espace de dimension inférieure.

[14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id929-marker)Il existe également des modèles qui génèrent des plongements lexicaux, par opposition aux plongements lexicaux de documentation, tels que word2vec (Mikolov et al., [« Efficient Estimation of Word Representations in Vector Space »](https://arxiv.org/abs/1301.3781) , _arXiv_ , v3, 7 septembre 2013) et GloVe (Pennington et al., [« GloVe: Global Vectors for Word Representation »](https://oreil.ly/O5QTX) , Stanford University Natural Language Processing Group (blog), 2014).

[15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id937-marker)Il ne faut pas confondre le terme _« juge IA »_ avec le cas d'utilisation où l'IA est employée comme juge au tribunal.

[16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id938-marker)En 2017, j'ai présenté [MEWR](https://x.com/chipro/status/937384141791698944) (Machine translation Evaluation metric Without Reference text) lors d'un atelier NeurIPS. Cette méthode d'évaluation exploite des modèles de langage plus performants pour évaluer automatiquement les traductions automatiques. Malheureusement, je n'ai jamais pu poursuivre ces recherches, la vie m'en ayant empêché.

[17](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id948-marker)Dans certains cas, l'évaluation peut absorber la majeure partie du budget, voire plus que la génération de réponses.

[18](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id949-marker)Le contrôle ponctuel est identique à l'échantillonnage.

[19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id952-marker)Saito et al. (2023) ont constaté que les humains ont également tendance à privilégier les réponses plus longues, mais dans une bien moindre mesure.

[20](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id955-marker)Cette technique est parfois appelée _autocritique_ ou _auto-interrogation_ .

[21](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id959-marker)L'échelle de notation BLEURT est déroutante. Elle se situe approximativement [entre -2,5 et 1,0](https://github.com/google-research/bleurt/issues/1) . Ceci met en évidence le problème de l'ambiguïté des critères chez les juges IA : l'échelle de notation peut être arbitraire.

[22](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id965-marker)Par exemple, en utilisant une [échelle de Likert](https://en.wikipedia.org/wiki/Likert_scale) .

[23](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id970-marker)Bien que Chatbot Arena ait abandonné l'algorithme de classement Elo, ses développeurs ont continué, pendant un certain temps, à désigner les évaluations de leurs modèles par l'expression « scores Elo ». Ils ont ajusté les scores Bradley-Terry obtenus pour les faire ressembler à des scores Elo. Ce processus est assez complexe : chaque score est multiplié par 400 (l'échelle utilisée par Elo) et ajouté à 1 000 (le score Elo initial). Le score ainsi obtenu est ensuite recalculé afin que le modèle Llama-13b obtienne un score de 800.

[24](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#id976-marker)Avec la popularité croissante de Chatbot Arena, les tentatives de manipulation du classement se multiplient. Si personne ne m'a avoué avoir essayé de le truquer, plusieurs développeurs de modèles m'ont confié être convaincus que leurs concurrents tentent de le faire.