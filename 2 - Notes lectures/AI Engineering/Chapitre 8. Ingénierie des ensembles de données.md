

La qualité d'un modèle dépend de la qualité de ses données d'entraînement. Même la meilleure équipe d'apprentissage automatique au monde, dotée d'une puissance de calcul illimitée, ne pourra pas optimiser un bon modèle si vous ne disposez pas de données. L'objectif de l'ingénierie des données est de créer un jeu de données permettant d'entraîner le meilleur modèle possible, idéalement dans les limites du budget alloué.

Comme de moins en moins d'entreprises peuvent se permettre de développer des modèles à partir de zéro, elles sont de plus en plus nombreuses à se tourner vers les données pour différencier leurs performances en IA. À mesure que les modèles exigent davantage de données, la gestion de ces données devient plus complexe et nécessite des investissements accrus dans les talents et [les](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1508) infrastructures.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1508)

Les opérations de données, autrefois tâches annexes effectuées à la demande, sont devenues des rôles à part entière. De nombreuses entreprises spécialisées en IA emploient désormais des étiqueteurs de données, des créateurs de jeux de données et des ingénieurs en qualité des données, intégrés à leurs équipes d'ingénierie principales ou travaillant en étroite collaboration avec elles.

Si le paysage des modèles est déjà complexe avec ses nombreuses offres, celui des données l'est encore plus, avec un nombre croissant d'ensembles de données et de techniques. Ce chapitre vous offre une vue d'ensemble de ce paysage et des éléments à prendre en compte lors de la création de votre propre ensemble de données.

Le processus commence par la curation des données, en répondant à des questions telles que : De quelles données avez-vous besoin ? En quelle quantité ? Qu’entend-on par données de haute qualité ? Il aborde ensuite les techniques de synthèse et de traitement des données. La curation, la génération et le traitement des données ne suivent pas un cheminement linéaire. Il vous faudra probablement faire des allers-retours entre les différentes étapes.

Pour un même modèle, les différentes phases d'entraînement visent à lui enseigner différentes capacités et nécessitent donc des jeux de données aux attributs différents. Par exemple, la quantité de données pour le pré-entraînement est souvent mesurée en nombre de jetons, tandis que celle pour l'ajustement supervisé est souvent mesurée en nombre d'exemples. Cependant, dans les grandes lignes, leurs processus de curation suivent le même principe. Ce chapitre se concentre sur les données post-entraînement, car elles sont plus pertinentes pour les développeurs d'applications. J'inclurai néanmoins des enseignements tirés des données de pré-entraînement lorsque ceux-ci s'avèrent utiles pour le post-entraînement.

Il existe des bonnes pratiques à suivre et des outils pour automatiser certaines étapes du processus. Cependant, les données resteront principalement le fruit d'efforts, de sacrifices et de sueur.

# Une vision de l'IA centrée sur les données

L'importance croissante accordée aux données dans le développement de l'IA a donné naissance à _une IA centrée sur les données_ , par opposition à _une IA centrée sur les modèles :_

- L'IA centrée sur les modèles vise à améliorer les performances de l'IA en perfectionnant les modèles eux-mêmes. Cela implique de concevoir de nouvelles architectures, d'augmenter la taille des modèles ou de développer de nouvelles techniques d'entraînement.
    
- L'IA centrée sur les données vise à améliorer les performances de l'IA en enrichissant les données. Cela implique le développement de nouvelles techniques de traitement des données et la création d'ensembles de données de haute qualité permettant d'entraîner de meilleurs modèles avec moins de ressources.
    

Aux débuts de l'apprentissage profond, de nombreux benchmarks d'IA étaient axés sur le modèle. À partir d'un jeu de données comme ImageNet, on cherchait à entraîner le meilleur modèle possible avec ce même jeu de données. Ces dernières années, les benchmarks se sont davantage orientés vers les données. Pour un même modèle, on cherche à développer un jeu de données permettant d'obtenir les meilleures performances possibles pour ce modèle.

En 2021, Andrew Ng a lancé un [concours d'IA axé sur les données](https://oreil.ly/2JlmX) où les participants devaient améliorer le même ensemble de données de base en appliquant des techniques telles que la correction d'étiquettes incorrectes, l'ajout d'exemples de cas limites, l'augmentation des données, etc.

En 2023, DataComp ( [Gadre et al., 2023](https://arxiv.org/abs/2304.14108) ) a organisé un [concours](https://oreil.ly/Xe50R) visant à créer le meilleur jeu de données pour l'entraînement d'un modèle CLIP ( [Radford et al., 2021](https://arxiv.org/abs/2103.00020) ). Un script standardisé entraîne un modèle CLIP sur chaque jeu de données soumis. La qualité d'un jeu de données est évaluée en fonction des performances du modèle résultant sur 38 tâches en aval. En 2024, un concours similaire a été organisé pour évaluer des jeux de données destinés aux modèles de langage comportant de 412 millions à 7 milliards de paramètres ( [Li et al., 2024](https://arxiv.org/abs/2406.11794) ). Parmi les autres benchmarks similaires axés sur les données, on peut citer DataPerf ( [MLCommons, 2023](https://oreil.ly/IK-1c) ) et dcbench ( [Eyuboglu et Karlaš, 2022](https://oreil.ly/BHEh1) ).

La distinction entre modèles et données permet d'orienter la recherche. En réalité, cependant, un progrès technologique significatif nécessite souvent d'investir à la fois dans l'amélioration des modèles et des données.

# Conservation des données

Bien que les données ne puissent pas résoudre tous les problèmes des modèles d'IA, elles constituent souvent un élément clé de la solution. Des données pertinentes peuvent rendre le modèle plus performant, plus sûr et capable de traiter des contextes plus longs. À l'inverse, des données de mauvaise qualité peuvent engendrer des biais et des erreurs d'interprétation. Des données erronées peuvent nuire au modèle et gaspiller des ressources.

La curation des données est une science qui exige de comprendre comment le modèle apprend et quelles ressources sont disponibles pour l'aider dans cet apprentissage. Les créateurs d'ensembles de données doivent travailler en étroite collaboration avec les développeurs d'applications et de modèles. Dans une petite équipe, il peut s'agir d'une seule et même [personne](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1512) : celle qui est responsable de l'entraînement d'un modèle est également responsable de l'acquisition des données nécessaires. Cependant, les organisations ayant d'importants besoins en données font souvent appel à des profils spécialisés.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1512)

Les données nécessaires dépendent de votre tâche et des connaissances que vous souhaitez transmettre au modèle. Pour l'apprentissage auto-supervisé, vous avez besoin de séquences de données. Pour l'apprentissage par instructions, les données doivent être au format (instruction, réponse). Pour l'apprentissage par préférences, les données doivent être au format (instruction, réponse gagnante, réponse perdante). Pour entraîner un modèle de récompense, vous pouvez utiliser le même format de données que pour l'apprentissage par préférences ou des données avec des scores annotés pour chaque exemple, au format ((instruction, réponse), score).

Les données d'entraînement doivent présenter les comportements que vous souhaitez que votre modèle apprenne. Obtenir des annotations de données de haute qualité est toujours un défi, mais c'est encore plus complexe lorsqu'il s'agit d'enseigner aux modèles des comportements complexes tels que le raisonnement par chaîne de pensée et l'utilisation d'outils. Prenons deux exemples pour comprendre pourquoi :

Chaîne de pensée

Comme expliqué au [chapitre 5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) , l'incitation CoT encourage le modèle à résoudre un problème étape par étape avant de fournir la réponse finale. Pour apprendre à un modèle à générer des réponses étape par étape, ses données d'entraînement doivent inclure des réponses CoT. L'article « Scaling Instruction-Finetuned Language Models » ( [Chun et al., 2024](https://oreil.ly/imdhy) ) montre que l'intégration de réponses étape par étape dans les données d'ajustement améliore considérablement les performances des modèles de différentes tailles sur les tâches CoT, la précision doublant presque pour certaines tâches.

Générer des réponses en plusieurs étapes peut s'avérer fastidieux et chronophage : expliquer la résolution d'un problème mathématique étape par étape est bien plus complexe que de simplement donner la réponse finale. Pour illustrer ce point, voici deux exemples : l'un ne contient que la réponse finale, l'autre inclut la méthode CoT. Ces deux exemples sont tirés de Chun et al. (2024).

```
**Consigne** : Veuillez répondre à la question suivante. Quel est le point d'ébullition ?
d'azote ?
**Réponse (sans CoT)** : -320,4 °F
**Consigne CoT** : Répondez à la question suivante en raisonnant étape par étape.
La cafétéria avait 23 pommes. S'ils en ont utilisé 20 pour le déjeuner et en ont acheté 6 autres,
Combien de pommes ont-ils ?
**Réponse (avec CoT)** : La cafétéria avait initialement 23 pommes. Ils en ont utilisé 20.
pour préparer le déjeuner. Ils avaient donc 23 - 20 = 3 pommes. Ils ont acheté 6 pommes supplémentaires, donc ils
ont 3 + 6 = 9.
```        

De ce fait, les jeux de données CoT sont moins courants que les autres jeux de données d'instructions.

Utilisation des outils

Compte tenu de la grande quantité de connaissances acquises par un modèle lors du pré-entraînement, de nombreux modèles peuvent savoir intuitivement utiliser certains outils. Cependant, la capacité d'un modèle à utiliser des outils peut être améliorée en lui présentant des exemples d'utilisation. Il est courant de faire appel à des experts du domaine pour créer des données d'utilisation d'outils : chaque requête correspond à une tâche nécessitant l'utilisation d'un outil, et sa réponse aux actions nécessaires pour accomplir cette tâche. Par exemple, si vous souhaitez obtenir des données pour affiner un modèle afin qu'il agisse comme un assistant personnel, vous pouvez interroger des assistants personnels professionnels sur les types de tâches qu'ils effectuent habituellement, comment ils les effectuent et quels outils ils utilisent. Si vous demandez à des experts humains d'expliquer leur méthode de travail, ils risquent d'omettre certaines étapes, soit par oubli, soit parce qu'ils les jugent non essentielles. Il est souvent nécessaire d'observer comment les humains effectuent ces tâches pour garantir l'exactitude des explications.

Cependant, ce qui est efficace pour les humains ne l'est pas forcément pour l'IA, et inversement. Par conséquent, les annotations humaines ne sont pas toujours optimales pour les agents d'IA. Par exemple, un humain privilégiera une interface web, tandis qu'il est plus simple pour un modèle d'utiliser une API. Pour effectuer une recherche, un humain ouvrira d'abord un navigateur, copiera et collera sa requête dans la barre de recherche, puis cliquera sur chaque résultat. Un modèle, quant à lui, peut simplement envoyer une requête à l'API de recherche et traiter tous les résultats simultanément. C'est pourquoi de nombreux modèles s'appuient sur des simulations et d'autres techniques de synthèse pour générer des données d'utilisation d'outils, comme nous le verrons plus loin dans ce chapitre.

Les données d'utilisation d'outils peuvent également nécessiter des formats spécifiques. Dans les données de conversation classiques, l'utilisateur et l'IA échangent à tour de rôle, chaque échange contenant un seul message. Cependant, pour l'utilisation d'outils, l'IA peut avoir besoin de générer plusieurs messages à chaque échange, chaque message étant envoyé à une destination différente. Par exemple, elle peut envoyer un message à l'interpréteur de code et un autre à l'utilisateur (par exemple, pour l'informer de son fonctionnement). Pour répondre à ce besoin, les auteurs de Llama 3 ( [Dubey et al., 2024](https://arxiv.org/abs/2407.21783) ) ont conçu un format de conversation multi-messages composé d'en-têtes spécifiant la source et la destination de chaque message, et de jetons de terminaison spécifiques indiquant le début des échanges entre l'utilisateur et l'IA.

Lors de la sélection de données pour des applications dotées d'interfaces conversationnelles, il est important de déterminer si vous avez besoin de données à échange unique, à échanges multiples, ou des deux. Les données à échange unique permettent d'entraîner un modèle à répondre à des instructions individuelles. Les données à échanges multiples, quant à elles, apprennent au modèle à résoudre des tâches ; or, de nombreuses tâches du monde réel impliquent des allers-retours. Par exemple, face à une requête, un modèle peut avoir besoin de clarifier l'intention de l'utilisateur avant de traiter la tâche. Après la réponse du modèle, l'utilisateur peut apporter des corrections ou des informations complémentaires pour la suite.

Les données à un seul tour sont plus simples et, par conséquent, plus faciles à obtenir. Les données à plusieurs tours nécessitent souvent des scénarios spécifiques ou des interactions plus complexes pour être recueillies.

La curation des données ne se limite pas à la création de nouvelles données pour aider un modèle à apprendre de nouveaux comportements ; elle consiste également à supprimer les données existantes pour l'aider à corriger les mauvaises habitudes. Imaginez que vous travaillez sur un chatbot comme ChatGPT et que vous entendiez des utilisateurs se plaindre de son arrogance, de son caractère agaçant et du gaspillage de leurs jetons. Par exemple, lorsqu'un utilisateur lui demande de vérifier l'exactitude factuelle d'une affirmation, le chatbot répond : « L'affirmation est correcte, mais sa formulation pourrait être améliorée. » Il continue ensuite à reformuler l'affirmation sans qu'on le lui ait demandé.

Vous constatez, après analyse, que les données d'entraînement contiennent plusieurs exemples d'annotations avec des suggestions non sollicitées. Vous demandez alors la suppression de ces exemples et sollicitez de nouveaux exemples illustrant la vérification des faits sans réécriture non sollicitée.

Chaque application peut nécessiter des données aux caractéristiques différentes. De même, les différentes phases d'entraînement requièrent des combinaisons de données différentes. Toutefois, de manière générale, la curation des données suit trois critères : la qualité, la couverture et la quantité des données.

Pour mieux comprendre ces termes, imaginez l'entraînement d'un modèle comme une préparation culinaire : les données qui lui sont fournies en sont les ingrédients. La qualité des données est comparable à la qualité des ingrédients ; impossible de préparer un bon plat avec des ingrédients avariés. La couverture des données équivaut à un dosage précis des ingrédients (par exemple, il ne faut pas trop ni pas assez de sucre). La quantité de données correspond au nombre d'ingrédients nécessaires. Examinons ces termes plus en détail.

## Qualité des données

Un petit volume de données de haute qualité peut surpasser un grand volume de données bruitées, c'est-à-dire des données non pertinentes ou incohérentes. Les créateurs de la famille de modèles Yi ont constaté que 10 000 instructions soigneusement conçues sont supérieures à des centaines de milliers d'instructions bruitées ( [Young et al., 2024](https://arxiv.org/abs/2403.04652) ).

De même, l’étude « LIMA : Less Is More for Alignment » ( [Zhou et al., 2023](https://arxiv.org/abs/2305.11206) ) montre qu’un modèle Llama à 65 milliards de paramètres, affiné à l’aide de 1 000 invites et réponses soigneusement sélectionnées, peut produire des réponses équivalentes ou nettement supérieures à celles de GPT-4 dans 43 % des cas, selon l’évaluation d’annotateurs humains. Cependant, le faible nombre d’exemples de données rend LIMA moins robuste que les modèles professionnels.

L' [équipe de Llama 3](https://arxiv.org/abs/2407.21783) est également parvenue à la même conclusion. Elle a notamment constaté que les données générées par l'humain sont plus sujettes aux erreurs et aux incohérences, en particulier pour les politiques de sécurité nuancées. Cela l'a amenée à développer des outils d'annotation assistés par l'IA afin de garantir une qualité de données optimale.

La plupart des gens comprennent l'importance de la qualité des données, mais qu'entend-on par données de haute qualité ? En résumé, des données sont considérées comme de haute qualité si elles vous permettent de travailler efficacement et de manière fiable. Cependant, la définition précise varie selon les personnes. [De](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1515) manière générale, des données peuvent être considérées comme de haute qualité si elles présentent les six caractéristiques suivantes : pertinence, adéquation aux exigences de la tâche, cohérence, formatage correct, unicité et conformité. Certains cas d'utilisation spécifiques peuvent avoir d'autres exigences.

**Pertinent**

Les exemples d'entraînement doivent être pertinents pour la tâche à accomplir. Par exemple, si la tâche consiste à répondre à des questions juridiques actuelles, un jeu de données juridiques du XIXe siècle pourrait ne pas être pertinent. En revanche, si la tâche porte sur le système juridique du XIXe siècle, ce jeu de données est tout à fait pertinent.

**Conforme aux exigences de la tâche**

Les annotations doivent être conformes aux exigences de la tâche. Par exemple, si la tâche exige une cohérence factuelle, les annotations doivent être factuellement correctes. Si la tâche exige de la créativité, les annotations doivent être créatives. Si la tâche exige non seulement une note, mais aussi une justification de cette note, les annotations doivent inclure les deux. En revanche, si la tâche exige des réponses concises, les annotations doivent être concises.

J'ai utilisé « aligné » au lieu de « précis » ou « correct » car, selon la tâche, une réponse précise ou correcte peut ne pas être ce que souhaite l'utilisateur.

**Cohérent**

Les annotations doivent être cohérentes entre les exemples et les annotateurs. Si deux annotateurs sont chargés d'annoter le même exemple, leurs annotations ne doivent pas différer sensiblement. Dans le cas d'une évaluation de dissertations de 1 à 5, deux dissertations ayant la même note sont-elles considérées comme étant de qualité équivalente ? Des annotations incohérentes peuvent perturber le modèle et entraver son apprentissage.

Disposer de bonnes directives d'annotation est essentiel pour obtenir des annotations à la fois conformes aux exigences de la tâche et cohérentes.

**Formaté correctement**

Tous les exemples doivent respecter le format attendu par le modèle. Les éléments de formatage redondants peuvent perturber l'apprentissage du modèle et doivent donc être supprimés. Par exemple, si vous extrayez des avis clients d'un site web, vous devez supprimer les balises HTML. Attention aux espaces blancs de fin de ligne, aux sauts de ligne, aux incohérences de casse et aux formats numériques [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1516)

**Suffisamment unique**

Cela fait référence aux exemples uniques dans vos données. Dans le contexte de l'entraînement [de](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1517) modèles, les doublons peuvent introduire des biais et contaminer les données. J'utilise l'expression « suffisamment uniques » car certains cas d'utilisation peuvent tolérer différents niveaux de doublons.

**Conforme**

Les données doivent être conformes à toutes les politiques internes et externes applicables (y compris les lois et réglementations). Par exemple, si l'utilisation de données personnelles est interdite pour l'entraînement des modèles, les données ne doivent contenir aucune donnée personnelle.

Avant de commencer à créer des données, il est important de réfléchir à la signification de chacune de ces caractéristiques. Les techniques présentées dans cette section visent à produire des données possédant ces caractéristiques.

## Couverture des données

Les données d'entraînement d'un modèle doivent couvrir l'ensemble des problèmes qu'il est censé résoudre. Dans le monde réel, les utilisateurs rencontrent souvent une grande variété de problèmes, et la manière dont ils les expriment peut varier considérablement. Disposer de données reflétant la diversité des usages de votre application est essentiel pour que le modèle soit performant. Cette couverture nécessite _une diversité de données_ suffisante , d'où l'appellation courante de « diversité des données ».

Par exemple, si certains utilisateurs rédigent des instructions détaillées avec de nombreuses références tandis que d'autres préfèrent des instructions concises, vos données d'entraînement doivent inclure les deux types d'instructions. Si les requêtes des utilisateurs contiennent fréquemment des fautes de frappe, vous devez inclure des exemples avec ces fautes. Si votre application est compatible avec plusieurs langages de programmation, vos données d'entraînement doivent inclure les langages utilisés par vos utilisateurs.

Les applications présentent différentes dimensions de la diversité. Par exemple, un outil de traduction du français vers l'anglais n'a pas nécessairement besoin de diversité linguistique, mais pourrait tirer profit d'une diversité de sujets, de longueurs et de styles d'expression. En revanche, un chatbot qui recommande des produits à des clients du monde entier n'a pas forcément besoin de diversité de domaine, mais la diversité linguistique et culturelle sera importante.

Pour les applications généralistes comme les chatbots, les données d'ajustement fin doivent être diversifiées et couvrir un large éventail de sujets et de schémas d'élocution. [Ding et al. (2023)](https://arxiv.org/abs/2305.14233) estiment que la méthode la plus simple pour améliorer les performances des modèles de langage conversationnel consiste à accroître la qualité et la diversité des données utilisées lors de l'entraînement. Pour développer Nemotron ( [Adler et al., 2024](https://arxiv.org/abs/2406.11704) ), les chercheurs de NVIDIA se sont concentrés sur la création d'un ensemble de données diversifié en termes de tâches, de sujets et d'instructions. Cet ensemble comprend des instructions pour différents formats de sortie, des instructions de longueurs variables et des instructions pour des réponses ouvertes ou fermées (oui/non). L'article « Le dilemme de l'ajout de données » ( [Shen et al., 2024](https://www.arxiv.org/abs/2408.04154) ) a démontré que, dans certains cas, l'ajout de données hétérogènes supplémentaires peut dégrader les performances.

Meta a indiqué que [Llama 3](https://arxiv.org/abs/2407.21783) ne diffère pas significativement des versions précédentes de Llama en termes d'architecture du modèle. Les gains de performance de Llama 3 sont « principalement dus à l'amélioration de la qualité et de la diversité des données, ainsi qu'à l'augmentation de la taille de l'ensemble d'entraînement ». L'article sur Llama 3 fournit des informations détaillées sur la couverture des données pour chacune des trois phases d'entraînement : pré-entraînement, ajustement supervisé et ajustement des préférences. Bien que ce chapitre se concentre sur les données post-entraînement, il est utile d'examiner la _répartition des données_ pour un même modèle à travers les différentes phases d'entraînement afin de comparer et de mettre en évidence les points à prendre en compte pour chaque phase.

Un axe de diversité constant dans les trois phases est la diversité de domaine, bien que sa définition précise _varie_ , comme le montre le [tableau 8-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_table_1_1730130931981135) . Ce tableau ne présente que les domaines généraux et n'inclut pas les sujets plus spécifiques, tels que la « géométrie », une sous-catégorie des mathématiques. Les données post-entraînement présentent également d'autres axes de diversité non représentés dans le tableau, comme le nombre de jetons (pour le contexte et la réponse) et le nombre de tours de parole. Llama 3 utilise des données synthétiques pour le post-entraînement ; une autre dimension est donc le ratio entre les données générées par l'humain et celles générées par l'IA.

Tableau 8-1. Pour Llama 3, différentes phases d'entraînement ont des mélanges de domaines optimaux différents.

|                                   |Pré-formation|réglage fin supervisé|Réglage fin des préférences|
|---|---|---|---|
| Connaissances générales (anglais) |50%|52,66%|81,99%|
| Mathématiques et raisonnement     |25%|21,19%|5,89%|
| Codage                            |17%|14,89%|6,93%|
| Multilingue                       |8%|3,01%|5,19%|
| Comme un examen                   |X|8,14%|X|
| Contexte long                     |X|0,11%|X|

Il est intéressant de noter que, lors du pré-entraînement et de l'ajustement supervisé, le nombre de jetons combinant mathématiques, raisonnement et code représente près de la moitié des données d'entraînement. Bien que je ne connaisse pas le pourcentage exact de données internet constituées de mathématiques et de code, je pense qu'il est bien inférieur à 50 %. Les auteurs de Llama 3 ont montré que l' _entraînement_ du modèle sur de petits volumes de données de code et de mathématiques de haute qualité (avec un taux d'apprentissage progressivement plus faible et des volumes croissants de données de code et de mathématiques) permet d'améliorer ses performances sur des benchmarks clés. Ceci confirme l'idée largement répandue que des données de code et de mathématiques de haute qualité sont plus efficaces que du texte en langage naturel pour améliorer les capacités de raisonnement du modèle.

Le pourcentage de données de code et de mathématiques lors du réglage fin des préférences est beaucoup plus faible (12,82 % combinés), probablement parce que l'objectif est de refléter la distribution réelle des préférences des utilisateurs.

Cela soulève une question : comment choisir la combinaison de données la plus appropriée ? Une approche simple consiste à sélectionner une combinaison de données reflétant fidèlement l’utilisation réelle de l’application. Il est également possible de mener des expériences pour identifier les combinaisons de données optimales. Par exemple, Meta a réalisé des expériences sur les lois d’échelle, similaires à celles décrites dans la section [« Extrapolation d’échelle »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_scaling_extrapolation_1730147895572029) . Pour chaque combinaison de données candidate, plusieurs petits modèles ont été entraînés, puis utilisés pour prédire les performances d’un grand modèle sur cette même combinaison. La combinaison finale retenue est la combinaison la plus performante, obtenue à partir des résultats expérimentaux.

Pour évaluer l'impact de la diversité et de la qualité des données, [Zhou et al. (2023)](https://arxiv.org/abs/2305.11206) ont mené une expérience intéressante : ils ont entraîné un modèle de langage à 7 milliards de paramètres sur trois ensembles de données de même taille (2 000 exemples), mais présentant des caractéristiques différentes. Le premier est de haute qualité mais peu diversifié. Le deuxième est diversifié mais de faible qualité. Le troisième est à la fois diversifié et de haute qualité. [La figure 8-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_figure_1_1730130931958804) illustre la qualité de génération des trois modèles obtenus.

![Graphique à barres bleues et rouges de tailles différentes. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0801.png)

###### Figure 8-1. Un modèle à 7B paramètres, affiné sur un jeu de données à la fois de haute qualité et diversifié, surpasse le même modèle affiné sur un jeu de données soit diversifié, soit de haute qualité. Image tirée de Zhou et al. (2023). L’image est sous licence CC BY 4.0.

## Quantité de données

Demander de combien de données on a besoin revient à demander de combien d'argent on a besoin. La réponse varie énormément d'une situation à l'autre. À un extrême, [Jeremy Howard et Jonathan Whitaker](https://oreil.ly/mUEJO) ont mené une expérience intéressante pour démontrer que les modèles d'apprentissage automatique (LLM) peuvent apprendre à partir d'un seul exemple. À l'autre extrême, certaines équipes ont affiné leurs modèles grâce à des millions d'exemples.

Bien que des millions d'exemples puissent paraître considérables, ce nombre reste faible comparé aux données généralement nécessaires pour entraîner un modèle de base à partir de zéro. À titre de comparaison, Llama 2 et Llama 3 ont été entraînés respectivement avec 2 000 milliards et 16 000 milliards de jetons. Si chaque exemple représente 2 000 jetons, cela équivaut à 1 milliard et 15 milliards d'exemples.

---
###### Note

Vous vous demandez peut-être : si je dispose de millions d’exemples, ne devrais-je pas simplement entraîner un modèle à partir de zéro ? Il est important d’évaluer si l’entraînement d’un modèle à partir de zéro améliorerait vos performances. Bien que l’ajustement fin d’un modèle pré-entraîné soit généralement plus efficace que l’entraînement à partir de zéro, il existe des situations où il peut s’avérer contre-productif, notamment lorsque vous disposez d’un grand nombre de données d’entraînement. Ceci est dû à un phénomène appelé _ossification_ , où le pré-entraînement peut _figer_ les poids du modèle, les empêchant ainsi de s’adapter aussi bien aux données d’ajustement fin ( [Hernandez et al., 2021](https://arxiv.org/abs/2102.01293) ). Les modèles plus petits sont plus sensibles à l’ossification que les modèles plus grands.

---
Outre la qualité et la diversité des données, trois autres facteurs influencent la quantité de données dont vous avez besoin :

**Techniques de réglage fin**

L'optimisation complète promet des performances optimales, mais elle exige une quantité de données considérablement supérieure aux méthodes PEFT comme LoRa. Si vous disposez de dizaines de milliers, voire de millions de paires (instruction, réponse), l'optimisation complète peut s'avérer pertinente. En revanche, si vous ne possédez que quelques centaines ou quelques milliers d'exemples, la méthode PEFT sera probablement la plus adaptée.

**Complexité de la tâche**

Une tâche simple, comme celle de déterminer si un avis sur un produit est positif ou négatif, nécessitera beaucoup moins de données qu'une tâche complexe, comme celle de répondre à une question concernant des documents financiers.

**Performances du modèle de base**

Plus le modèle de base se rapproche des performances souhaitées, moins il faut d'exemples pour y parvenir. En supposant que les modèles de base plus grands soient meilleurs, il est possible que vous ayez besoin de moins d'exemples pour affiner les grands modèles. C'est l'inverse du pré-entraînement, où les grands modèles nécessitent davantage de données d'entraînement.

[Le guide d'ajustement fin d'OpenAI](https://oreil.ly/-R3Wd) indique que, avec un nombre réduit d'exemples (100), les modèles plus avancés offrent de meilleures performances d'ajustement fin. Ceci s'explique probablement par le fait que ces modèles sont déjà plus performants par défaut. Cependant, après un ajustement fin sur un grand nombre d'exemples (550 000), les cinq modèles de l'expérience ont présenté des performances similaires, comme illustré dans [la figure 8-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_figure_2_1730130931958852) .

![Graphique à barres de couleurs différentes. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0802.png)

###### Figure 8-2. Avec 100 exemples, les modèles les plus avancés offrent des performances nettement supérieures après ajustement. Avec 550 000 exemples, tous les modèles présentent des performances similaires après ajustement. Expériences réalisées avec le corpus Stanford Natural Language Inference (SNLI).

En résumé, si vous disposez de peu de données, vous pouvez utiliser les méthodes PEFT sur des modèles plus avancés. Si vous disposez d'un grand nombre de données, utilisez un ajustement fin complet sur des modèles plus petits.

Avant d'investir dans la constitution d'un vaste ensemble de données, il peut être judicieux de commencer par un petit ensemble bien conçu (par exemple, 50 exemples) afin de vérifier si un réglage fin peut améliorer le modèle. Si ce petit ensemble suffit à atteindre les performances souhaitées, c'est parfait. Des améliorations significatives indiquent qu'un plus grand nombre de données permettra d'améliorer encore les performances. En revanche, si aucune amélioration n'est observée avec un petit ensemble de données, un ensemble plus important ne sera que rarement efficace.

Toutefois, il convient d'être prudent avant de conclure que le réglage fin sur un petit ensemble de données n'améliore pas un modèle. De nombreux facteurs, outre les données elles-mêmes, peuvent influencer les résultats du réglage fin, tels que le choix des hyperparamètres (par exemple, un taux d'apprentissage trop élevé ou trop faible), la qualité des données, des énoncés mal conçus, etc. _Dans la grande majorité des cas, vous devriez constater des améliorations après un réglage fin sur 50 à 100 exemples._

---
###### Conseil

Il est possible de réduire la quantité de données de haute qualité nécessaires en affinant d'abord votre modèle à l'aide de données de moindre qualité ou moins pertinentes. Voici trois exemples de cette approche :

Auto-supervisé → supervisé

Vous souhaitez affiner un modèle pour répondre à des questions juridiques. Votre ensemble (question, réponse) est restreint, mais vous disposez de nombreux documents juridiques. Vous pouvez commencer par affiner votre modèle sur des documents juridiques de manière auto-supervisée, puis l'affiner davantage sur des paires (question, réponse).

Données moins pertinentes → données pertinentes

Vous souhaitez affiner un modèle pour classifier les sentiments exprimés dans les avis clients, mais vous disposez de peu de données sur les sentiments exprimés dans les produits et de beaucoup plus de données sur les sentiments exprimés dans les tweets. Vous pouvez commencer par affiner votre modèle pour classifier les sentiments exprimés dans les tweets, puis l'affiner davantage pour classifier les sentiments exprimés dans les produits.

Données synthétiques → données réelles

Vous souhaitez affiner un modèle de prédiction des pathologies à partir de rapports médicaux. Compte tenu de la nature sensible de cette tâche, vos données sont limitées. Vous pouvez utiliser des modèles d'IA pour synthétiser une grande quantité de données afin d'affiner d'abord votre modèle, puis l'affiner davantage sur vos données réelles. Cette approche est plus complexe à maîtriser, car elle nécessite deux opérations d'affinage distinctes et une transition coordonnée entre elles. Sans une bonne maîtrise du processus, vous risquez de consommer davantage de ressources de calcul pour obtenir un modèle moins performant que celui obtenu par un simple affinage avec des données de haute qualité [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1523)

---
Expérimenter avec un petit jeu de données permet d'estimer la quantité de données supplémentaires nécessaires. Vous pouvez affiner un modèle sur des sous-ensembles de votre jeu de données actuel (par exemple, 25 %, 50 %, 100 %) et visualiser l'évolution des performances en fonction de la taille du jeu de données. Une forte augmentation des performances avec la taille du jeu de données signifie qu'un doublement des données apportera une amélioration significative. À l'inverse, une faible augmentation des performances signifie qu'un doublement des données n'entraînera qu'une légère amélioration. [La figure 8-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_figure_3_1730130931958912) illustre ce type de graphique.

![Un graphique avec une description de ligne générée automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0803.png)

###### Figure 8-3. La courbe de gain de performance avec différentes tailles d'ensemble de données peut vous aider à estimer l'impact des exemples d'entraînement supplémentaires sur les performances de votre modèle.

La courbe de gain de performance illustrée à [la figure 8-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_figure_3_1730130931958912) est assez typique. Dans la plupart des cas, l'ajout d'exemples d'entraînement supplémentaires n'apporte qu'un gain de performance décroissant : à nombre d'exemples égal, l'amélioration des performances diminue généralement à mesure que la taille de l'ensemble de données augmente. Par exemple, les 1 000 premiers exemples peuvent améliorer la précision d'un modèle de dix points de pourcentage, tandis que les 1 000 suivants ne l'amélioreront que de cinq points.

Bien qu'un plus grand nombre d'exemples d'ajustement fin améliore généralement les performances d'un modèle, la diversité de ces exemples est également importante. L'article « Scaling Instruction-Finetuned Language Models » ( [Chung et al., 2022](https://arxiv.org/abs/2210.11416) ) montre que les performances du modèle augmentent significativement lorsque le nombre de tâches d'ajustement fin passe de 9 à 282. Au-delà de 282 tâches, les gains de performance se stabilisent, même si des améliorations positives, quoique progressives, persistent jusqu'à 1 836 tâches, comme illustré dans [la figure 8-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_figure_4_1730130931958939) . Cela suggère que le modèle bénéficie grandement d'une exposition à un ensemble diversifié de tâches lors de l'ajustement fin.

La diversité des données peut se refléter dans les types de tâches (comme la synthèse et la réponse aux questions), la diversité des sujets (comme la mode, la finance et la technologie) et les formats de sortie attendus (comme les sorties JSON ou les réponses par oui ou par non).

![Un graphique de nombres et un certain nombre de tâches de réglage fin. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0804.png)

###### Figure 8-4. La diversité du nombre de tâches d'ajustement fin peut influencer les performances du modèle. Image extraite de « Scaling Instruction-Finetuned Language Models » (Chung et al., 2022). Cette image est sous licence CC BY 4.0.

La quantité de données nécessaires au réglage fin dépend non seulement de vos besoins, mais aussi de votre budget. Si vous prévoyez un budget de 10 000 $ pour l'annotation des données et que chaque exemple coûte 2 $ à annoter, vous ne pourrez utiliser que 5 000 exemples au maximum. Il vous faudra peut-être aussi trouver un équilibre entre le budget alloué aux données et celui consacré au calcul. Investir davantage dans les données réduit le budget disponible pour le calcul, et inversement.

## Acquisition et annotation des données

L'objectif de l'acquisition de données est de constituer un ensemble de données suffisamment volumineux, de qualité et de diversité adaptées à vos besoins, tout en garantissant le respect de la vie privée des utilisateurs et la conformité aux réglementations. L'acquisition de données comprend la collecte de données par diverses méthodes, telles que l'extraction de données publiques, l'achat de données propriétaires, l'annotation et la synthèse de données. _La stratégie d'acquisition de données_ constitue un domaine de recherche de niche en pleine expansion : comment acquérir au mieux un ensemble de données répondant à des exigences spécifiques, compte tenu d'un budget donné ?

La source de données la plus importante est cependant généralement celle provenant de votre propre application. Si vous parvenez à créer un[Un système](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1526) _d'échange de données_ exploitant les données générées par vos utilisateurs pour améliorer continuellement votre produit vous offrira un avantage considérable. Les données applicatives sont idéales car elles sont parfaitement pertinentes et alignées sur votre objectif. Autrement dit, elles correspondent à la distribution des données qui vous intéressent, ce qui est extrêmement difficile à obtenir avec d'autres sources de données. Les données générées par les utilisateurs peuvent être du contenu utilisateur, des données système issues de l'utilisation ou des retours d'expérience. La conception de votre système de retour d'expérience est abordée au [chapitre 10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_ai_engineering_architecture_and_user_feedback_1730130985311851) .[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1526)[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_ai_engineering_architecture_and_user_feedback_1730130985311851)

Avant d'investir dans la création de vos propres données, consultez d'abord les jeux de données disponibles. Les plateformes de données sont vastes et proposent des données open source et propriétaires. Avec un peu de chance, certaines d'entre elles correspondront exactement à vos besoins. Cependant, il s'agit souvent d'une approche hybride. Un jeu de données peut être constitué à partir de plusieurs sources et via différents canaux d'acquisition. Par exemple, le processus de création d'un jeu de données (instruction, réponse) pourrait se dérouler comme suit :

1. Recherchez les jeux de données disponibles présentant les caractéristiques souhaitées. Vous pourriez trouver un jeu de données prometteur contenant 10 000 exemples.
    
2. Supprimez les instructions de mauvaise qualité. Supposons qu'il vous reste alors 9 000 exemples.
    
3. Mettez de côté les consignes ayant reçu des réponses de faible qualité. Supposons que vous trouviez 3 000 exemples de ce type. Il vous reste alors 6 000 exemples de consignes et de réponses de haute qualité.
    
4. Saisissez manuellement les réponses aux 3 000 instructions de haute qualité. Votre ensemble de données compte désormais 9 000 exemples de haute qualité.
    
5. Constatant l'insuffisance de données sur le sujet X, créez manuellement un ensemble de 100 modèles d'instructions concernant X. Utilisez ensuite un modèle d'IA pour synthétiser 2 000 instructions à partir de ces 10 modèles.
    
6. Annotez manuellement ces 2 000 instructions synthétiques. Votre ensemble de données compte désormais 11 000 exemples.
    

Il s'agit bien sûr d'une simplification excessive du processus réel de curation des jeux de données, la grande majorité des étapes étant occultées pour économiser du papier et épargner aux lecteurs la monotonie de la lecture. Par exemple, il peut arriver, à plusieurs reprises, que vous vous rendiez compte que de nombreuses annotations sont inutiles ; vous devez alors mettre à jour les consignes d'annotation et réannoter vos données. Pire encore, vous pourriez découvrir que certaines annotations sont factuellement incorrectes, et vous devrez donc faire appel à une autre équipe d'annotateurs pour vérifier les annotations initiales. Ou encore, vous pourriez constater que 100 instructions synthétiques par modèle nuisent à la diversité de vos données ; vous devez alors créer davantage de modèles et générer moins d'instructions par modèle. Et ainsi de suite.

---
# Ressources pour les ensembles de données accessibles au public

Voici quelques ressources où vous pouvez trouver des jeux de données accessibles au public. Bien qu'il soit conseillé d'exploiter les données disponibles, il ne faut jamais leur accorder une confiance aveugle. Les données doivent être minutieusement examinées et validées.

Vérifiez toujours la licence d'un jeu de données avant de l'utiliser. Efforcez-vous de comprendre d'où proviennent les données. Même si un jeu de données possède une licence autorisant une utilisation commerciale, il est possible qu'une partie provienne d'une source qui ne l'autorise pas.

1. [Hugging Face](https://oreil.ly/tlt5h) et [Kaggle](https://oreil.ly/g8A4a) hébergent chacun des centaines de milliers d'ensembles de données.
    
2. Google propose une fonction [de recherche de jeux de données](https://oreil.ly/TgOaR) formidable et sous-estimée .
    
3. Les gouvernements sont souvent d'excellents fournisseurs de données ouvertes. [Data.gov](https://data.gov/) héberge des centaines de milliers d'ensembles de données, et [data.gov.in](https://data.gov.in/) en héberge des dizaines de milliers.
    
4. [L'Institut de recherche sociale](https://oreil.ly/VhVzp) (ICPSR) de l'Université du Michigan possède des données provenant de dizaines de milliers d'études sociales.
    
5. [Le dépôt d'apprentissage automatique de l'UC Irvine](https://oreil.ly/jAR9e) et [OpenML](https://oreil.ly/d-Yty) sont deux anciens dépôts de jeux de données, hébergeant chacun plusieurs milliers de jeux de données.
    
6. Le [réseau Open Data Network](https://oreil.ly/_tW6P) vous permet d'effectuer des recherches parmi des dizaines de milliers d'ensembles de données.
    
7. Les fournisseurs de services cloud hébergent souvent une petite collection d'ensembles de données ouverts ; le plus notable est [Open Data d'AWS](https://oreil.ly/DZ5uV) .
    
8. Les frameworks ML disposent souvent de petits ensembles de données pré-construits que vous pouvez charger lors de l'utilisation du framework, tels que [les ensembles de données TensorFlow](https://oreil.ly/HMJX_) .
    
9. Certains outils d'évaluation proposent des jeux de données de référence suffisamment volumineux pour l'optimisation de PEFT. Par exemple, l'outil [lm-evaluation-harness d'Eleuther AI](https://github.com/EleutherAI/lm-evaluation-harness) héberge plus de 400 jeux de données de référence, contenant en moyenne plus de 2 000 exemples par jeu.
    
10. La [collection de données de grands réseaux de Stanford](https://oreil.ly/eb_Bn) est un excellent dépôt pour les ensembles de données graphiques.

---

Il est souvent nécessaire d'annoter ses propres données pour un ajustement précis. L'annotation est complexe, non seulement en raison du processus lui-même, mais aussi à cause de la difficulté à élaborer des directives d'annotation claires. Par exemple, il faut définir précisément ce qu'est une bonne réponse et en expliquer les caractéristiques. Une réponse peut-elle être correcte sans être utile ? Quelle est la différence entre les réponses méritant une note de 3 et celles méritant une note de 4 ? Des directives d'annotation sont indispensables, que ce soit pour les annotations manuelles ou automatisées par l'IA.

Certaines équipes, dont [LinkedIn](https://www.linkedin.com/blog/engineering/generative-ai/musings-on-building-a-generative-ai-product?_l=en_US) , ont indiqué que les règles d'annotation figuraient parmi les aspects les plus complexes de leur processus de développement en IA. Il est alarmant de constater combien de personnes abandonnent une annotation rigoureuse en cours de route, faute de temps et d'efforts, en espérant que leurs modèles trouveront d'eux-mêmes les réponses adéquates. Si de nombreux modèles sont suffisamment performants pour y parvenir occasionnellement, compter sur eux pour y parvenir peut s'avérer trop risqué pour de nombreuses applications.

La bonne nouvelle est que ces lignes directrices sont identiques à celles relatives aux données d'évaluation, comme expliqué au [chapitre 4.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) C'est un argument supplémentaire pour consacrer plus de temps à l'élaboration de lignes directrices et de données d'évaluation pertinentes. Avec un peu de chance, vos exemples d'évaluation pourront être enrichis ou servir de base à la synthèse de nouvelles données. La section suivante abordera la question suivante..

# Augmentation et synthèse des données

Avec la puissance de calcul et les talents, les données représentent le plus grand défi de l'IA. Générer des données par programmation est un objectif à long terme pour l'ensemble du secteur. _L'augmentation_ et _la synthèse des données sont deux processus couramment utilisés._

- [L'augmentation des données permet de créer de nouvelles données à partir de données existantes (qui sont](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1535) réelles). Par exemple, à partir d'une image réelle d'un chat, on peut la retourner pour créer une nouvelle image du même chat.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1535)
    
- La synthèse de données génère des données imitant les propriétés de données réelles. Par exemple, on peut simuler le déplacement d'une souris sur une page web pour générer des données sur les mouvements d'un bot.
    

Autrement dit, les données augmentées sont issues de données réelles, tandis que les données synthétiques ne sont pas réelles. Cependant, comme l'augmentation et la synthèse visent toutes deux à automatiser la création de données, les deux termes sont parfois utilisés indifféremment. Dans ce chapitre, j'utiliserai souvent le terme « synthèse de données » pour désigner les deux.

Les données générées artificiellement sont utilisées depuis longtemps en génie logiciel. À l'origine, elles servaient à générer des données factices à des fins de test. Par exemple, des bibliothèques comme [_Faker_](https://github.com/joke2k/faker) et [_Chance_](https://chancejs.com/) permettent de générer des données dans des formats simples tels que des noms, des adresses, des numéros de téléphone et des adresses e-mail pour les tests. Imaginons que vous ayez développé un programme pour analyser des adresses de livraison. Vous pouvez utiliser des générateurs de données factices pour générer des adresses dans différents pays et régions, avec des formats variés, afin de vous assurer que votre programme peut toutes les analyser.

L'IA étant capable de générer des données indiscernables de celles produites par les humains, il est possible de synthétiser des données beaucoup plus sophistiquées, telles que des notes médicales, des contrats, des états financiers, des descriptions de produits, des images, des publicités vidéo, etc. Cela facilite la génération de données et permet davantage de cas d'utilisation de données synthétiques.

Bien que les données synthétiques promettent de réduire considérablement la pression sur les données générées par l'humain, elles ne les remplacent pas complètement. Dans de nombreux cas d'utilisation, comme l'explique l'article [« Limites des données générées par l'IA »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_limitations_to_ai_generated_data_1730130932021346) , la combinaison de données humaines et de données générées par l'IA offre souvent les meilleurs résultats.

## Pourquoi la synthèse des données

Les données synthétiques présentent de nombreux avantages. Elles permettent d'améliorer les trois piliers essentiels des données : quantité, couverture et qualité. Elles permettent également d'atténuer les problèmes de confidentialité et d'affiner les modèles.

**Pour augmenter la quantité de données**

La principale raison d'être de la synthèse de données est qu'elle permet de produire des données à grande échelle, garantissant ainsi un approvisionnement abondant pour l'entraînement et le test des modèles d'IA. En théorie, davantage de données permettent aux modèles de généraliser à un plus large éventail de tâches. Ceci est particulièrement utile lorsque les données réelles sont rares ou difficiles à obtenir, comme les données relatives à des conditions météorologiques exceptionnelles, à l'exploration des grands fonds marins ou aux accidents pour les véhicules autonomes.

**Pour augmenter la couverture des données**

Vous pouvez générer des données aux caractéristiques ciblées afin d'améliorer les performances d'un modèle ou de l'amener à exprimer des comportements spécifiques. Par exemple, vous pouvez générer des textes très courts ou très longs. Vous pouvez créer des conversations contenant des expressions toxiques pour un modèle de détection de contenus toxiques. Inversement, si des données réelles sont toxiques, vous pouvez synthétiser des données sûres. L'utilisation de l'IA pour synthétiser des exemples adverses est particulièrement courante. Il est également possible de générer des données pour les classes rares afin de pallier les problèmes de déséquilibre des classes. Comme décrit dans « TrueTeacher », [Gekhman et al. (2022)](https://arxiv.org/abs/2305.11171) ont utilisé des modèles linéaires à long terme (LLM) pour générer des résumés factuellement incohérents, qu'ils ont ensuite utilisés pour entraîner des modèles à détecter ces incohérences.

Dans leur article intitulé « Découverte des comportements des modèles de langage grâce à des évaluations rédigées par les modèles » ( [Perez et al., 2022](https://arxiv.org/abs/2212.09251) ), Anthropic a examiné diverses techniques de synthèse de données permettant de générer des ensembles de données spécifiques capables de tester 154 comportements différents de l'IA, notamment des traits de personnalité, des opinions politiques, des positions éthiques et des biais sociaux. Les auteurs ont constaté que, lors de comparaisons directes entre des ensembles de données générés par des modèles de langage et des ensembles de données rédigés par des humains, « les ensembles de données rédigés par des modèles de langage atteignent une qualité comparable à celle des ensembles rédigés par des humains, voire la surpassent parfois ».

Autrement dit, vous pouvez utiliser des données synthétiques pour accroître la couverture des données : générer des données ciblées pour couvrir les domaines où les données existantes sont insuffisantes.

**Pour améliorer la qualité des données**

Bien que l'on considère généralement que les données synthétiques sont souvent de moindre qualité que les données générées par l'humain, il arrive que ce soit l'inverse. _Parfois, les humains peuvent avoir des limitations fondamentales qui font que les données qu'ils produisent sont de moindre qualité que celles générées par l'IA. Un exemple est celui des données d'utilisation d'outils évoquées précédemment : les humains et l'IA ont des modes de fonctionnement et des préférences d'outils fondamentalement différents. Un autre exemple concerne la génération de problèmes mathématiques complexes : l'IA peut générer des_ [questions](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1536) bien plus complexes que ce qu'un expert humain moyen pourrait concevoir.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1536)

Certaines équipes privilégient également l'utilisation de l'IA pour générer des données de préférences. Si les préférences de chaque individu sont relativement constantes, les performances varient considérablement d'une personne à l'autre, influencées non seulement par les préférences individuelles, mais aussi par l'humeur et les motivations. Les évaluations de préférences générées par l'IA, en revanche, peuvent être bien plus cohérentes et fiables.

**Pour atténuer les préoccupations relatives à la vie privée**

Les données synthétiques sont souvent la seule option lorsque l'utilisation de données générées par l'humain est impossible pour des raisons de confidentialité. Par exemple, dans le secteur de la santé, où la législation rend difficile, voire impossible, l'utilisation de dossiers patients réels pour entraîner un modèle, il est possible de générer des dossiers patients synthétiques ne contenant aucune information sensible. Dans le secteur des assurances, on peut utiliser des demandes de remboursement synthétiques à la place des demandes réelles, qui incluent des informations personnelles et financières sensibles.

**Pour distiller les modèles**

Il peut arriver que l'on souhaite entraîner un modèle à imiter le comportement d'un autre. L'objectif est souvent de créer un modèle plus économique et/ou plus rapide (le modèle distillé) dont les performances soient comparables à celles du modèle original. Pour ce faire, on entraîne le modèle distillé à l'aide de données générées par le modèle original.

Ce ne sont là que cinq des nombreuses raisons qui poussent les chercheurs à recourir à la synthèse de données. Compte tenu de son attrait indéniable, de plus en plus de modèles sont entraînés avec des données synthétiques et de nouvelles techniques de synthèse de données sont mises au point.

## Techniques traditionnelles de synthèse de données

La synthèse de données n'est pas propre à l'IA. Elle est utilisée depuis longtemps dans les tests logiciels, les jeux vidéo et la robotique. L'utilisation d'algorithmes pour générer des données est également appelée _génération procédurale_ , par opposition à _la génération manuelle_ . La génération procédurale est couramment utilisée dans les jeux vidéo pour générer à la volée du contenu tel que des niveaux, des cartes, des objets et des personnages. [La](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1539) plupart des techniques de génération de données utilisées dans ces secteurs peuvent être appliquées à l'IA.

Traditionnellement, deux approches de synthèse et d'augmentation des données sont utilisées : les méthodes basées sur des règles et la simulation. Une méthode plus récente, rendue possible par les modèles d'IA avancés, consiste à utiliser l'IA elle-même pour synthétiser les données. Cette section présente un aperçu de ces deux techniques traditionnelles avant d'aborder la synthèse de données assistée par l'IA dans la section suivante.

### Synthèse de données basée sur des règles

La méthode la plus simple pour générer des données consiste à utiliser des règles et des modèles prédéfinis. Par exemple, pour créer une transaction par carte bancaire, commencez par un modèle de transaction et utilisez un générateur aléatoire comme Faker pour remplir chaque champ de ce modèle :

```
An example of a transaction template. 
Transaction ID: [Unique Identifier]
Date: [MM/DD/YYYY]
Time: [HH:MM:SS]
Amount: [Transaction Amount]
Merchant Name: [Merchant/Store Name]
Merchant Category: [Category Code]
Location: [City, State, Country]
Payment Method: [Credit Card/Debit Card/Cash/Online Payment]
Transaction Status: [Completed/Pending/Failed]
Description: [Transaction Description]
```

En raison de la sensibilité des données transactionnelles, de nombreux modèles de détection de fraude sont d'abord entraînés sur des données transactionnelles synthétiques générées à partir de modèles comme celui-ci afin de prouver leur faisabilité avant d'avoir accès à des données réelles.

Il est courant d'utiliser des modèles pour générer des documents suivant une structure spécifique, tels que des factures, des CV, des formulaires fiscaux, des relevés bancaires, des programmes d'événements, des catalogues de produits, des contrats, des fichiers de configuration, etc. Les modèles peuvent également servir à générer des données respectant une grammaire et une syntaxe particulières, comme les expressions régulières et les équations mathématiques. On peut ainsi générer des équations mathématiques que les modèles d'IA doivent résoudre. DeepMind a entraîné AlphaGeometry, un modèle de géométrie de niveau olympique, à l'aide de 100 millions d'exemples synthétiques ( [Trinh et al., 2024](https://oreil.ly/skn8z) ).

Il est possible de générer de nouvelles données à partir de données existantes en appliquant des transformations simples. Pour les images, on peut effectuer une rotation, un recadrage, une mise à l'échelle ou effacer une partie de l'image de manière aléatoire. Une image de chat retournée restera un chat. Une image d'un match de football légèrement recadrée restera un match de football. [Krizhevsky et al. (2012)](https://oreil.ly/ez6Iw) ont démontré, dans leur article de référence sur AlexNet, l'utilité de cette technique en l'utilisant pour enrichir le jeu de données ImageNet ( [Deng et al., 2009](https://oreil.ly/i7hpS) ).

Dans un texte, vous pouvez remplacer aléatoirement un mot par un mot similaire, à condition que ce remplacement ne modifie ni le sens ni la tonalité de la phrase. Par exemple, la phrase originale « C'est une infirmière _fantastique_ » peut donner : « C'est une _excellente_ infirmière ».

Cette approche permet d'atténuer les biais potentiels dans vos données. Si vous craignez un biais sexiste dans vos données, par exemple si le mot « infirmière » est associé aux femmes et le mot « médecin » aux hommes, vous pouvez remplacer les mots généralement genrés par leur contraire, comme « elle » par « il », comme illustré dans [le tableau 8-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_table_2_1730130931981173) .

Tableau 8-2. L'augmentation des données peut contribuer à atténuer certains biais dans vos données.

|Données originales|Données augmentées|
|---|---|
|C'est une infirmière fantastique.|_C'est_ un infirmier fantastique.  <br>C'est une _médecin_ fantastique .|
|Le PDG de l'entreprise, M. Alex Wang, …|La PDG de l'entreprise, _Mme Alexa Wang_ , …|
|Aujourd'hui, ma mère a préparé un gratin pour le dîner.|Aujourd'hui, mon _père_ a préparé un gratin pour le dîner.|
|Emily a toujours adoré le violon.|_Mohammed_ a toujours adoré le violon.|

On peut trouver des mots similaires soit à l'aide d'un dictionnaire de synonymes, soit en repérant les mots dont les représentations vectorielles sont proches dans un espace de représentation vectorielle des mots. Il est possible d'aller au-delà du simple remplacement de mots en demandant à l'IA de reformuler ou de traduire un exemple, comme nous le verrons plus loin.

Une transformation intéressante est la perturbation : l’ajout de bruit à des données existantes pour générer de nouvelles données. Initialement, les chercheurs ont découvert qu’une légère perturbation d’un échantillon de données pouvait induire les modèles en erreur et les amener à le classer incorrectement. Par exemple, l’ajout de bruit blanc à l’image d’un bateau peut conduire le modèle à le confondre avec une voiture. L’article « One Pixel Attack for Fooling Deep Neural Networks » ( [Su et al., 2017](https://arxiv.org/abs/1710.08864) ) a montré que 67,97 % des images naturelles du jeu de données de test Kaggle CIFAR-10 et 16,04 % des images de test ImageNet pouvaient être mal classées en modifiant un seul pixel. Cette vulnérabilité représente un risque sérieux si elle est exploitée. Un attaquant pourrait tromper un modèle d’IA et se faire passer pour un employé autorisé, ou amener une voiture autonome à confondre un séparateur de voie avec une voie de circulation, provoquant ainsi des accidents.

Vous pouvez entraîner votre modèle sur des données perturbées. La perturbation peut à la fois améliorer les performances du modèle et le rendre plus robuste face aux attaques (voir [Goodfellow et al., 2013](https://arxiv.org/abs/1302.4389) et [Moosavi-Dezfooli et al., 2015](https://arxiv.org/abs/1511.04599) ). En 2019, Hendrycks et Dietterich ont créé [ImageNet-C et ImageNet-P](https://arxiv.org/abs/1903.12261) en appliquant 15 altérations visuelles courantes, telles que la modification de la luminosité, l'ajout de neige, la modification du contraste et l'ajout de bruit aux images d'ImageNet.

La perturbation peut également être utilisée pour les textes. Par exemple, pour entraîner BERT, les auteurs ont remplacé 1,5 % des jetons par des mots aléatoires ( [Devlin et al., 2018](https://arxiv.org/abs/1810.04805) ). Ils ont constaté que cette perturbation entraînait une légère amélioration des performances.

Les données visuelles peuvent être enrichies grâce à des algorithmes plus sophistiqués. [Snap (2022)](https://oreil.ly/1YFbA) propose une excellente étude de cas sur la manière dont l'entreprise enrichit ses ressources pour créer des cas limites non représentés et atténuer les biais implicites dans ses données. À partir d'un personnage, elle synthétise des personnages similaires, mais avec des couleurs de peau, des morphologies, des coiffures, des vêtements et même des expressions faciales différents. Ces ressources enrichies servent ensuite à entraîner des modèles d'IA.

### Simulation

Au lieu de mener des expériences pour collecter des données dans le monde réel, ce qui peut s'avérer coûteux et dangereux, il est possible de simuler ces expériences virtuellement. Par exemple, pour tester la réaction d'une voiture autonome face à un cheval sur l'autoroute, il serait dangereux de lâcher un véritable cheval. On simule donc cette situation dans un environnement virtuel. Parmi les moteurs de simulation de conduite autonome, on peut citer CARLA ( [Dosovitskiy et al., 2017](https://arxiv.org/abs/1711.03938) ), [SimulationCity de Waymo](https://oreil.ly/xbyXd) et [la simulation de San Francisco de Tesla](https://oreil.ly/YnbiK) .

De même, il est très courant de simuler des données d'entraînement pour la robotique dans un environnement virtuel. Imaginons que vous souhaitiez entraîner un robot à verser du café, mais que vous ne sachiez pas précisément comment chaque articulation doit se mouvoir pour que l'action réussisse. Vous pouvez simuler plusieurs scénarios avec différents mouvements articulaires et n'utiliser que ceux où le café est versé avec succès pour entraîner le robot.

Les simulations permettent de réaliser de multiples expériences à moindre coût, tout en évitant les accidents et les dommages matériels. Un robot performant en simulation peut ne pas fonctionner dans le monde réel, mais s'il échoue en simulation, il échouera probablement aussi dans le monde réel. Cependant, aussi sophistiquées soient-elles, les simulations restent des simplifications du monde réel. Le domaine Sim2Real vise à adapter au monde réel les algorithmes entraînés en simulation.

Les simulations sont couramment utilisées pour générer des données permettant d'apprendre aux modèles à utiliser des outils. Comme mentionné précédemment, les actions humaines ne sont pas toujours les plus efficaces pour les agents d'IA. Les simulations peuvent aider à identifier des actions que les humains négligent. À partir d'une requête, il est possible de simuler différentes séquences d'actions, de les exécuter et d'en valider les résultats. La séquence d'actions la plus efficace est ensuite utilisée comme réponse annotée à la requête.

Les simulations sont particulièrement précieuses pour générer des données relatives à des événements rares. Par exemple, en finance, les chercheurs peuvent simuler des scénarios tels que l'entrée en bourse réussie d'une entreprise ou une faillite importante afin d'en comprendre les impacts sur le marché. Les fabricants peuvent simuler des défauts de matériaux ou d'assemblages pour générer des données permettant d'entraîner des modèles de détection d'anomalies et de contrôle qualité. De même, en simulant les systèmes terrestres, les climatologues peuvent créer des variations de température, des régimes de précipitations et des scénarios météorologiques extrêmes. Ces données synthétiques sont ensuite intégrées à des modèles d'IA, leur permettant ainsi d'apprendre d'un éventail plus large de futurs possibles.

Les techniques basées sur des règles et sur la simulation se sont avérées utiles dans de nombreux cas d'utilisation, mais ce n'est qu'avec l'avènement de l'IA capable de générer des données réalistes et de haute qualité que la synthèse de données a véritablement pris son essor. Examinons ces méthodes plus en détail.

## Synthèse de données basée sur l'IA

Tout comme les humains disposent d'une infinité de façons de générer des données, l'IA peut également le faire de multiples manières. Les techniques présentées ici ne sont pas exhaustives, mais elles vous en donneront un bon aperçu.

_Les puissants modèles d'IA ouvrent de nombreuses perspectives pour la simulation_ . L'IA peut simuler les résultats de programmes quelconques. Par exemple, « StableToolBench » ( [Guo et al., 2024](https://arxiv.org/abs/2403.07714) ) illustre comment utiliser l'IA pour simuler des API sans avoir à les appeler. Imaginez que vous souhaitiez entraîner un modèle à interagir avec un ensemble d'API. Au lieu d'effectuer de véritables appels d'API — potentiellement coûteux ou lents —, vous pouvez utiliser un modèle d'IA pour simuler les résultats attendus de ces appels.

L'IA peut simuler le comportement humain. Par exemple, imaginez que vous vouliez entraîner un bot à jouer aux échecs. Une partie jouée par des humains serait trop longue. Les parties contre des IA seraient beaucoup plus rapides. Pour entraîner son bot Dota 2, OpenAI a utilisé un simulateur qui lui permettait de jouer quotidiennement l'équivalent de 180 ans de parties. Le bot a appris en jouant contre lui-même, une approche appelée _auto-apprentissage_ , qui lui a permis de développer et d'affiner ses stratégies au fil du temps ( [OpenAI, 2019](https://oreil.ly/rX6oc) ). De même, DeepMind a utilisé l'auto-apprentissage pour collecter des données issues de millions de parties de go afin d'entraîner AlphaGo ( [Silver et al., 2016](https://oreil.ly/prIw9) ).

L'auto-apprentissage est utile non seulement pour les bots de jeux vidéo, mais aussi pour les agents en général. On peut faire négocier des IA entre elles en utilisant différentes stratégies afin de déterminer laquelle est la plus efficace. On peut par exemple faire jouer à une version du modèle le rôle d'un client rencontrant des problèmes, et à une autre celui d'un agent du service client.

_Les capacités de reformulation et de traduction de l'IA peuvent être utilisées pour enrichir les ensembles de données existants._ Par exemple, face à la requête « Comment réinitialiser mon mot de passe ? », l'IA peut la reformuler pour créer trois nouvelles requêtes :

1. « J’ai oublié mon mot de passe. »
    
2. « Comment puis-je changer mon mot de passe ? »
    
3. « Étapes pour réinitialiser les mots de passe. »
    

[Yu et al. (2023)](https://arxiv.org/abs/2309.12284) ont réécrit les 15 000 exemples des bases de données MATH et GSM-8K de différentes manières afin de créer MetaMath, un nouveau jeu de données de près de 400 000 exemples. Ils ont démontré que leurs modèles, entraînés sur ce nouveau jeu de données, surpassaient des modèles plus importants sur des jeux de données mathématiques de référence similaires.

Il est courant d'utiliser l'IA pour traduire des données rédigées dans des langues à ressources abondantes (plus facilement disponibles en ligne) vers des langues à faibles ressources, afin de faciliter l'entraînement de modèles dans ces dernières. Cela s'avère utile pour entraîner un petit modèle spécialisé dans une langue à faibles ressources comme le quechua ou le lao.

On peut vérifier la qualité des traductions par _rétrotraduction_ . Supposons que la phrase anglaise originale soit _X_ et la phrase laotienne traduite _Y._ On peut utiliser un autre modèle pour retraduire la traduction en langue originale, _Xʹ_ , puis comparer _Xʹ_ avec la phrase originale X. Si les différences sont importantes, la traduction _Y_ est probablement de mauvaise qualité.

L'IA peut traduire non seulement les langues naturelles, mais aussi les langages de programmation. On peut l'utiliser pour traduire du code écrit dans un langage vers un autre.Les [auteurs de Llama 3](https://arxiv.org/abs/2407.21783) ont utilisé la traduction automatique de leur jeu de données SFT avec un large éventail de langages de programmation. En effet, l'entraînement de Llama 3 repose en grande partie sur des données synthétiques, et les auteurs ont eu recours à de nombreuses techniques originales pour générer des données utiles.

Par exemple, ils ont utilisé la rétro-traduction pour générer des explications et une documentation sur le code. À partir d'extraits de code, ils ont utilisé l'IA pour générer ces explications et cette documentation. Ils ont ensuite de nouveau utilisé l'IA pour générer des extraits de code à partir de ces explications et de cette documentation. Ce n'est que si le code généré est jugé fidèle à l'original que les explications et la documentation seront utilisées pour affiner le modèle.

L'IA peut générer des données pour le pré-entraînement et le post-entraînement, mais les données synthétiques sont intentionnellement beaucoup plus souvent utilisées dans le post-entraînement que dans le pré-entraînement. Cela s'explique peut-être par le fait que le pré-entraînement vise à enrichir les connaissances du modèle ; or, si l'IA peut synthétiser des connaissances existantes sous différents formats, la synthèse de nouvelles connaissances s'avère plus complexe.

Cependant, face à l'afflux de contenus générés par l'IA sur Internet, les modèles exploitant les données en ligne sont probablement déjà pré-entraînés sur des données synthétiques. On trouve également des ensembles de données synthétiques comme [Cosmopedia](https://oreil.ly/0ymnI) (Allal et al., 2024), une collection de 25 milliards de jetons composée de manuels scolaires, d'articles de blog, de récits, de publications et d'articles WikiHow synthétiques générés par [Mixtral-8x7B-Instruct-v0.1](https://oreil.ly/FyHwn) (Jiang et al., 2024).

La synthèse des données post-entraînement est également plus courante car la production de ces données, incluant les données d'instructions et de préférences, est généralement plus complexe. Utiliser l'IA pour sélectionner la meilleure réponse parmi plusieurs est plus simple ; une grande partie de ce sujet a déjà été abordée au [chapitre 3.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) La principale difficulté consiste à prendre en compte les biais du modèle, comme le biais de première position, où le modèle est plus susceptible de privilégier la première option. Pour éviter ce biais, les chercheurs de NVIDIA ont interrogé l'IA à deux reprises, une fois en inversant l'ordre des réponses. Ils n'ont retenu un triplet (réponse pertinente, réponse gagnante, réponse perdante) valide que lorsque l'IA a désigné le même gagnant lors des deux interrogations ( [NVIDIA, 2024](https://oreil.ly/f8LPj) ).

La section suivante portera sur la manière d'utiliser l'IA pour synthétiser des données d'instructions en vue d'un réglage fin supervisé.

### Synthèse des données d'instructions

Lors de la mise au point des instructions, chaque exemple comprend une instruction et une réponse. L'IA peut être utilisée pour synthétiser les instructions, les réponses, ou les deux. Par exemple, on peut utiliser l'IA pour générer les instructions et des humains pour rédiger les réponses. On peut également utiliser des humains pour rédiger les instructions et l'IA pour générer les réponses.

- Pour la génération d'instructions, afin de garantir un nombre suffisant d'instructions pour votre cas d'utilisation, vous pouvez commencer par une liste de sujets, de mots-clés et/ou des types d'instructions souhaités dans votre ensemble de données. Ensuite, pour chaque élément de cette liste, générez un certain nombre d'instructions. Vous pouvez également partir d'un ensemble de modèles et générer un certain nombre d'exemples pour chaque modèle. Notez que la liste de sujets et les modèles peuvent être générés par une IA.
    
- Pour la génération de réponses, vous pouvez générer une ou plusieurs réponses par instruction.
    

Par exemple, pour créer UltraChat ( [Ding et al., 2023](https://arxiv.org/abs/2305.14233) ), un ensemble de données de dialogues à plusieurs tours de parole, les auteurs ont d'abord demandé à ChatGPT de générer 30 thèmes portant sur divers aspects de notre vie quotidienne, tels que la technologie, l'alimentation, la mode, la nature, l'éducation, la finance, les voyages, etc. Pour chaque thème, ils ont demandé à ChatGPT de générer entre 30 et 50 sous-thèmes. Les auteurs ont ensuite utilisé le même modèle pour générer les instructions et les réponses correspondantes à ces sous-thèmes.

De même, pour entraîner Alpaca ( [Taori et al., 2023](https://oreil.ly/u9ghd) ), les chercheurs de Stanford ont commencé avec 175 exemples (instruction, réponse) issus du jeu de données initial Self-Instruct ( [Wang et al., 2022](https://arxiv.org/abs/2212.10560) ). Ces exemples avaient été initialement conçus pour couvrir un large éventail d'utilisations. Les auteurs d'Alpaca ont ensuite utilisé un modèle GPT-3, _text-davinci-003_ , pour générer 52 000 paires (instruction, réponse) similaires à ces exemples initiaux, comme illustré dans [la figure 8-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_figure_6_1730130931958982) .

![Gros plan d'un panneau. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0805.png)

###### Figure 8-5. Une tâche initiale et une tâche générée utilisées pour entraîner Alpaca.

Il existe de nombreuses manières créatives de synthétiser des données d'instructions présentant certaines caractéristiques. Par exemple, tout comme il est plus difficile pour les humains de rédiger des textes longs que des textes courts, il est plus difficile pour l'IA de générer des réponses longues et de qualité que des instructions courtes. Plus la réponse est longue, plus le risque d'hallucinations de l'IA est élevé. Que se passerait-il si nous utilisions des réponses générées par des humains avec des instructions générées par l'IA ? Certains chercheurs, tels que [Köksal et al. (2023)](https://arxiv.org/abs/2304.08460) , [Li et al. (2023)](https://arxiv.org/abs/2308.06259) et [Chen et al. (2023)](https://arxiv.org/abs/2309.05447) , adoptent l' approche _inverse_ : ils partent de contenus longs et de qualité existants, comme des histoires, des livres et des articles Wikipédia, et utilisent l'IA pour générer des amorces susceptibles de susciter ce type de contenu. Cette méthode permet d'obtenir des données d'instructions de meilleure qualité, en évitant les hallucinations générées par l'IA dans les réponses.

Il est possible d'utiliser l'instruction inverse pour développer des modèles de plus en plus performants sans ajouter de données annotées manuellement. [11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1549) Li et al. (2023) montrent comment cela fonctionne :

1. Commencez par un petit nombre d'exemples initiaux pour entraîner un modèle faible.
    
2. Utilisez ce modèle faible pour générer des instructions à partir de contenu existant de haute qualité afin de créer des données d'instructions de haute qualité.
    
3. Affinez le modèle faible grâce à ces nouvelles données d'instructions de haute qualité.
    
4. Répéter jusqu'à obtention des résultats souhaités.
    

Une approche créative consiste à utiliser des données synthétiques pour affiner un modèle afin de comprendre des contextes plus longs. Par exemple, si votre modèle actuel traite un maximum de 8 000 jetons, mais que vous souhaitez qu'il en traite 128 000, le processus d'affinage pour les contextes longs pourrait ressembler à ceci :

- Divisez les documents longs en morceaux plus courts (par exemple, moins de 8 000 jetons).
    
- Pour chaque court segment, générez plusieurs paires (question, réponse).
    
- Pour chaque paire (question, réponse), utilisez le document long original, qui peut contenir plus de 8 000 mots mais être plus court que la longueur cible, comme contexte. Cela permet au modèle d’apprendre à utiliser ce contexte étendu pour répondre aux questions.
    

Le niveau de détail de l'article sur Llama 3 ( [Dubey et al., 2024](https://arxiv.org/abs/2407.21783) ) en fait une excellente étude de cas pour la synthèse de données d'instructions. J'ai déjà mentionné deux méthodes de synthèse de données utilisées par Llama 3 : la traduction et la rétro-traduction de code. Ces deux méthodes génèrent davantage de données à partir d'extraits de code existants. Cependant, les auteurs ont également utilisé l'IA pour synthétiser des données d'instructions de codage à partir de zéro, selon le flux de travail suivant :

1. Utiliser l'IA pour générer une vaste collection de descriptions de problèmes de programmation couvrant un large éventail de sujets.
    
2. Étant donné un énoncé de problème et un langage de programmation, générez une solution. Dubey et al. ont constaté que l'intégration de règles générales de bonne programmation et d'un raisonnement de type CoT contribuait à améliorer la qualité des réponses.
    

Pour garantir la qualité des données générées, ils ont utilisé un processus rigoureux d'analyse de la justesse et de correction des erreurs :

1. Analysez le code généré à l'aide d'analyseurs syntaxiques et de linters afin de détecter les erreurs de syntaxe telles que les importations manquantes et les variables non initialisées.
    
2. Utilisez des tests unitaires pour détecter les erreurs d'exécution. Fait intéressant, ces tests unitaires ont été générés à l'aide de l'IA.
    
3. Lorsqu'une solution échoue à une étape quelconque, invitez le modèle à réviser le code. Cette invite comprend la description initiale du problème, la solution erronée et les retours de l'analyseur syntaxique, du linter et des tests unitaires. Seuls les exemples qui réussissent tous les contrôles sont inclus dans l'ensemble de données final d'ajustement supervisé [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1551)
    

En combinant les trois méthodes (traduction, rétro-traduction et génération de code), le flux de travail de synthèse de données de Llama 3 est particulièrement impressionnant. Voici, en résumé, comment ces trois méthodes interagissent :

1. Utiliser l'IA pour générer des descriptions de problèmes.
    
2. Utiliser l'IA pour générer des solutions à chaque problème dans différents langages de programmation.
    
3. Utiliser l'IA pour générer des tests unitaires afin de tester le code généré.
    
4. Demander à l'IA de corriger les erreurs dans le code synthétisé.
    
5. Utiliser l'IA pour traduire le code généré dans différents langages de programmation. Éliminer le code traduit qui ne réussit pas les tests.
    
6. Utilisez l'IA pour générer des conversations sur le code, incluant des explications et de la documentation. Filtrez les explications et la documentation générées qui ne passent pas la vérification de traduction inverse.
    

En utilisant ce pipeline, Dubey et al. ont pu générer plus de 2,7 millions d'exemples de codage synthétiques pour le réglage fin supervisé de Llama 3.1.

### Vérification des données

Étant donné l'importance de la qualité des données pour les performances du modèle, il est crucial de disposer d'un moyen de la vérifier. La qualité des données générées par l'IA peut être mesurée de la même manière que celle des autres résultats d'IA : par l'évaluation de leur exactitude fonctionnelle et par des experts en IA.

Bien que cette section soit axée sur les données synthétiques, la plupart des techniques peuvent être utilisées pour évaluer la qualité des données d'entraînement en général.

Rappelons le concept de développement piloté par l'évaluation présenté au [chapitre 4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) , selon lequel les entreprises sont plus enclines à créer des applications qu'elles peuvent évaluer. De même, on a tendance à synthétiser des données vérifiables. Le codage est l'un des cas d'utilisation les plus courants du modèle de base, car il peut être évalué fonctionnellement. C'est pourquoi les exemples liés au codage figurent parmi les données les plus fréquemment synthétisées. La plupart des données synthétiques utilisées pour entraîner Llama 3 sont liées au codage. Les trois méthodes de synthèse de données employées par les auteurs produisent des données vérifiables par programmation, x, grâce à l'exécution de code et à la rétro-traduction.

Pour les données synthétiques dont la correction fonctionnelle est impossible à vérifier, on utilise généralement des vérificateurs IA. Un vérificateur IA peut être un juge IA généraliste ou un évaluateur spécialisé. Il existe de nombreuses façons de formuler le problème de vérification. Dans sa forme la plus simple, le vérificateur IA peut attribuer à chaque exemple généré une note de 1 à 5 ou le classer comme bon ou mauvais. On peut également décrire les exigences de qualité à un modèle de base et lui demander de déterminer si un exemple de données les satisfait.

Si vous tenez à la cohérence factuelle des données, vous pouvez utiliser les techniques de détection des incohérences factuelles abordées au [chapitre 4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) pour filtrer les exemples susceptibles de contenir des hallucinations.

Selon le cas d'utilisation et les données générées, vous pouvez aussi faire preuve de créativité. Par exemple, si vous souhaitez que des données synthétiques imitent des données réelles, leur qualité peut être évaluée en fonction de la difficulté à les distinguer. Vous pourriez entraîner un détecteur de contenu IA à identifier les données générées par l'IA : s'il est facile de différencier les données réelles des données synthétiques, ces dernières sont de mauvaise qualité. Ou encore, si vous souhaitez que les données synthétiques ressemblent à des travaux universitaires de haut niveau, vous pourriez entraîner un classificateur à prédire si un article généré serait accepté à une conférence prestigieuse comme NeurIPS (Conférence et Atelier sur les Systèmes de Traitement de l'Information Neurale) et à rejeter tout article dont l'acceptation est clairement prédite.

Vous pouvez utiliser un modèle pour détecter le thème de chaque exemple généré, puis supprimer ceux dont le thème est hors sujet. Si vous prévoyez que toutes les données suivent un schéma similaire, vous pouvez également recourir à la détection d'anomalies pour identifier les valeurs aberrantes ; ces exemples aberrants peuvent être de faible qualité.

Tout comme les données réelles, les données synthétiques peuvent être filtrées à l'aide d'heuristiques. En général, il est conseillé de supprimer les exemples vides ou trop courts pour votre application. Si un exemple est trop long, vous pouvez le tronquer ou le supprimer. Vous pouvez filtrer les données par mots-clés, par utilisateur/auteur, par date de création, par métadonnées ou par source. Par exemple, les auteurs de Self-Instruct ( [Wang et al., 2022](https://arxiv.org/abs/2212.10560) ) ont filtré les exemples générés à l'aide des heuristiques suivantes :

- Exemples répétitifs
    
- Instructions trop longues ou trop courtes
    
- Exemples avec la même consigne mais des réponses différentes
    
- Exemples où la sortie est une répétition de l'entrée
    

Malgré la multitude de techniques d'évaluation des données synthétiques, cette évaluation demeure complexe. Comme pour toute application d'IA, le critère de qualité ultime pour les données générées par l'IA réside dans leurs performances réelles – leur capacité à améliorer les performances du modèle – et les données synthétiques ont passé ce test avec succès pour de nombreux modèles.

### Limites des données générées par l'IA

Face à l'utilité croissante des données synthétiques, il est séduisant d'imaginer la possibilité de ne plus jamais avoir à se soucier des données annotées par des humains. Cependant, si le rôle des données synthétiques est assurément voué à prendre de l'importance, les données générées par l'IA ne remplaceront peut-être jamais entièrement les données produites par des humains. Plusieurs raisons expliquent cela, mais les quatre principales sont la différence de qualité, les limites de l'imitation, le risque d'effondrement des modèles et la manière dont la génération de données par l'IA masque leur origine.

#### Contrôle de qualité

Les données générées par l'IA peuvent être de faible qualité et, comme on le répète souvent, « si les données d'entrée sont mauvaises, les résultats le seront aussi ». Comme mentionné précédemment, on hésitera à utiliser des données synthétiques si leur qualité n'est pas vérifiable. Développer des méthodes et des indicateurs fiables pour évaluer ces données sera essentiel pour les rendre plus utiles.

#### Imitation superficielle

Comme le souligne l’article « La fausse promesse de l’imitation des LLM propriétaires » ( [Gudibande et al., 2023](https://arxiv.org/abs/2305.15717) ), les performances perçues grâce à l’imitation peuvent être superficielles. Cette recherche montre que les modèles d’imitation reproduisent bien le style des modèles enseignants, mais peuvent avoir des difficultés avec l’exactitude des faits et la généralisation à des tâches extérieures aux données d’entraînement.

Pire encore, l'imitation peut conduire le modèle élève à des hallucinations. Imaginons que le modèle enseignant soit capable de répondre à des problèmes mathématiques complexes, et que ses réponses à ces problèmes soient alors des solutions. Entraîner un modèle élève sur ces solutions lui apprend à produire des réponses qui ressemblent à des solutions, même s'il est incapable de résoudre ces problèmes. [Gudibande](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1561) et al. (2023) suggèrent que, pour améliorer les capacités de raisonnement, il est nécessaire de se concentrer sur l'amélioration de la qualité des modèles de base.

#### Effondrement potentiel du modèle

On ignore également la quantité de données générées par l'IA sur laquelle un modèle peut être entraîné. Certaines études ont montré que l'utilisation _récursive de ces données lors de l'entraînement engendre des défauts irréversibles dans les modèles obtenus, dégradant ainsi leurs performances au fil du temps. Dans « The Curse of Recursion: Training on Generated Data Makes Models Forget »,_ [Shumailov et al. (2023)](https://arxiv.org/abs/2305.17493) ont nommé ce phénomène _« effondrement du modèle_ » et ont démontré son occurrence dans des modèles tels que les auto-encodeurs variationnels , les [modèles](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1564) de mélange gaussien et les LLM. L'effondrement du modèle peut se produire aussi bien avant qu'après l'entraînement.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1564)

Une explication possible est que les modèles d'IA sont plus enclins à générer des événements probables (par exemple, ne pas avoir de cancer) et moins enclins à générer des événements improbables (par exemple, avoir un cancer). Au fil des itérations, les événements probables sont surreprésentés, tandis que les événements improbables sont sous-représentés dans les données générées. Cela conduit les modèles à produire davantage d'événements fréquents au fil du temps, tout en oubliant les événements rares.

Dans leur article intitulé « L’effondrement du modèle est-il inévitable ? », [Gerstgrasser et al. (2024)](https://arxiv.org/abs/2404.01413) affirment que si l’effondrement du modèle est inévitable lorsque l’ensemble des données d’entraînement est entièrement synthétique, il peut être évité en mélangeant données synthétiques et données réelles. [Bertrand et al. (2023)](https://arxiv.org/abs/2310.00429) et [Dohmatob et al. (2024)](https://arxiv.org/abs/2402.07043) présentent des résultats similaires. Cependant, aucun de ces articles ne formule de recommandation définitive quant à la proportion de données synthétiques par rapport aux données réelles.

Certains chercheurs ont réussi à améliorer les performances de modèles en utilisant une grande quantité de données synthétiques. Par exemple, l'article « Common 7B Language Models Already Possess Strong Math Capabilities » ( [Li et al., 2024](https://arxiv.org/abs/2403.04706) ) démontre que les données synthétiques sont presque aussi efficaces que les données réelles pour l'optimisation des modèles Llama 2-7B sur des problèmes mathématiques. Dans leurs expériences, les données synthétiques ne présentent aucune saturation manifeste, même lorsqu'elles sont portées à environ un million d'échantillons. De même, [Nemotron-4 340B-Instruct](https://oreil.ly/IUA3j) (NVIDIA, 2024) a utilisé 98 % de données synthétiques lors de ses phases d'optimisation des instructions et des préférences. Cependant, ces expériences n'ont été réalisées que pour une seule itération du modèle.

Les données générées par l'IA peuvent également perpétuer les biais. L'article « Boucles de rétroaction des données : amplification des biais des ensembles de données par le modèle » ( [Taori et Hashimoto, 2023](https://oreil.ly/OZxiz) ) démontre que lorsque des modèles sont entraînés sur des ensembles de données incluant des sorties de modèles antérieurs, tout biais existant dans le modèle peut être amplifié. Les auteurs constatent que plus les sorties du modèle sont fidèles aux caractéristiques de la distribution d'entraînement initiale, plus la boucle de rétroaction est stable, minimisant ainsi le risque d' amplification des biais.

#### Traçabilité obscure des données

Cette limitation des données générées par l'IA est plus subtile. La génération par l'IA masque la provenance des données. Les modèles d'IA sont influencés par leurs données d'entraînement et peuvent parfois les reproduire à l'insu de l'utilisateur. Cela engendre des risques. Imaginons que vous utilisiez le modèle X pour générer des données d'entraînement. Si le modèle X a été entraîné sur des données comportant des violations de droits d'auteur, votre modèle pourrait lui aussi enfreindre ces droits.

Imaginez ensuite que vous utilisiez le jeu de données de référence B pour évaluer votre modèle, et que celui-ci affiche d'excellentes performances. Cependant, si le modèle X a également été entraîné sur le jeu de données de référence B, votre résultat sur B est faussé. Sans traçabilité claire des données, il est difficile d'évaluer la viabilité commerciale d'un modèle ou de se fier à ses performances.

Nous avons abordé l'utilisation de l'IA pour générer des données, leur évaluation et ses limites. Dans la section suivante, nous allons examiner un cas d'utilisation particulier de la synthèse de données où les données générées par l'IA ne sont pas seulement complémentaires, mais indispensables : la distillation de modèles..

## Distillation modèle

_La distillation de modèles_ (ou _distillation des connaissances_ ) est une méthode qui consiste à entraîner un petit modèle (l'élève) à imiter un modèle plus grand (le professeur) ( [Hinton et al., 2015](https://arxiv.org/abs/1503.02531) ). Les connaissances du grand modèle sont ainsi distillées dans le petit modèle, d'où le terme de distillation.

Traditionnellement, l'objectif de la distillation de modèles est de produire des modèles plus petits pour leur déploiement. Le déploiement d'un modèle volumineux peut s'avérer gourmand en ressources. La distillation permet de produire un modèle élève plus petit et plus rapide, dont les performances restent comparables à celles du modèle enseignant. Par exemple, DistilBERT, un modèle distillé à partir de BERT, réduit la taille d'un modèle BERT de 40 % tout en conservant 97 % de ses capacités de compréhension du langage et en étant 60 % plus rapide ( [Sanh et al., 2019](https://arxiv.org/abs/1910.01108) ).

Le modèle étudiant peut être entraîné à partir de zéro comme DistilBERT ou affiné à partir d'un modèle pré-entraîné comme [Alpaca](https://github.com/tatsu-lab/stanford_alpaca) .En 2023, Taori et al. ont affiné Llama-7B, la version à 7 milliards de paramètres de Llama, sur des exemples générés par _text-davinci-003_ , un modèle à 175 milliards de paramètres. Le modèle résultant, Alpaca, se comporte de manière similaire à _text-davinci-003_ , tout en étant 4 % plus petit que le modèle initial.

---
###### Note

Tous les modèles ne peuvent pas être distillés. De nombreuses licences de modèles interdisent l'utilisation de leurs résultats pour entraîner d'autres modèles, notamment des modèles concurrents.

---


Les données d'instructions synthétiques sont couramment utilisées conjointement avec des techniques d'adaptation, telles que LoRA. Par exemple, [BuzzFeed](https://oreil.ly/U7gfm) a affiné un modèle Flan-T5 à l'aide de LoRA et d'exemples générés par _text-davinci-003_ d'OpenAI . Le modèle obtenu a permis de réduire le coût d'inférence de 80 %, mais ses performances réelles restent à évaluer (2023).

Il est important de noter que l'entraînement avec des données synthétiques ne constitue pas systématiquement une distillation de modèle. La distillation de modèle suppose que les performances du modèle enseignant servent de référence absolue pour le modèle élève. Cependant, il est possible d'utiliser des données synthétiques pour entraîner un modèle élève plus grand et plus performant que le modèle enseignant.

L’amorçage de modèles avec instruction inversée ( [Li et al., 2023](https://arxiv.org/abs/2308.06259) ), abordé dans la section précédente, en est un exemple. Un autre exemple est Nemotron-4 de NVIDIA. Une équipe de chercheurs de NVIDIA a d’abord pré-entraîné un modèle de base de 340 milliards de paramètres. Ce modèle a ensuite été affiné à l’aide de données d’instructions et de préférences générées par [Mixtral-8x7B-Instruct-v0.1 (Jiang et al., 2024), un modèle de mélange d’experts à](https://oreil.ly/-Vd_q) [56](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1573) milliards de paramètres. Le modèle élève ainsi obtenu, Nemotron-4-340B-Instruct, a surpassé le modèle enseignant sur diverses tâches ( [NVIDIA, 2024](https://oreil.ly/iGToR) ).

L'article Llama 3 souligne que si l'entraînement sur des données générées par un modèle plus performant peut améliorer significativement les performances d'un modèle, l'entraînement sans discernement sur des données auto-générées n'améliore pas ses performances et peut même les dégrader. Cependant, en introduisant des mécanismes de vérification de la qualité des données synthétiques et en utilisant uniquement des données synthétiques vérifiées, les chercheurs ont pu améliorer continuellement un modèle grâce à ses propres données générées.

# Data Processing

Les données doivent être traitées conformément aux exigences de chaque cas d'utilisation. Cette section présente quelques étapes de traitement des données à titre de référence.

Je trouve utile de lire des articles modèles qui divulguent les détails de leurs ensembles de données, car ils contiennent souvent d'excellents conseils sur la façon dont les chercheurs ont organisé, généré et traité les données.

---
###### Conseil

Avec un grand volume de données, chacune de ces étapes de traitement peut prendre des heures, voire des jours. Voici quelques conseils pour optimiser l'efficacité du processus :

- Vous pouvez effectuer ces étapes de traitement des données dans l'ordre qui vous permet d'économiser du temps et de la puissance de calcul. Par exemple, si le nettoyage de chaque exemple prend plus de temps que la déduplication des données, il est préférable de supprimer les doublons avant de procéder au nettoyage. En revanche, si la déduplication est plus longue que le filtrage des données de faible qualité, il est conseillé de filtrer ces dernières en premier.
    
- Effectuez toujours des essais préliminaires pour vérifier que vos scripts de traitement fonctionnent comme prévu avant de les appliquer à toutes vos données.
    
- Évitez de modifier les données sur place. Il est conseillé de conserver une copie des données originales pour deux raisons :
    
    - Vous ou une autre équipe pourriez avoir besoin de traiter les données différemment pour d'autres applications.
        
    - Des bugs dans vos scripts peuvent potentiellement corrompre vos données.
        

---
## Inspecter les données

Supposons qu'après avoir analysé des données publiques et internes, vous ayez constitué un ensemble de données brutes. La première étape consiste à examiner ces données afin d'en évaluer la qualité. Il faut recueillir des informations et des statistiques les concernant. D'où proviennent ces données ? Comment ont-elles été traitées ? À quelles autres fins ont-elles été utilisées ?

Représentez graphiquement la distribution des jetons (pour identifier les jetons fréquents), la longueur des entrées, la longueur des réponses, etc. Les données utilisent-elles des jetons spécifiques ? Pouvez-vous obtenir une distribution des thèmes et des langues présents dans les données ? Dans quelle mesure ces thèmes et langues sont-ils pertinents pour votre tâche ?

Vous pouvez faire preuve de créativité dans l'utilisation des statistiques pour comprendre vos données. Par exemple, [une équipe de chercheurs de Microsoft (2023)](https://arxiv.org/abs/2304.03277) a utilisé la distribution des paires (verbe, complément d'objet direct, nom) et la longueur des réponses pour comparer les performances des générations GPT-3 et GPT-4 pour un même ensemble d'instructions, comme illustré dans [les figures 8-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_figure_7_1730130931959005) et [8-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_figure_8_1730130931959026) . Ce type d'analyse est utile non seulement pour évaluer les données, mais aussi les modèles.

![Un graphique avec des chiffres et un diagramme à barres. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0806.png)

###### Figure 8-6. Une statistique utile est la distribution de (verbe, nom complément d'objet direct) dans vos données. Image tirée de « Instruction Tuning with GPT-4 » (Peng et al., 2023).

![Graphique illustrant une séquence de sortie. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0807.png)

###### Figure 8-7. La distribution de la longueur de réponse pour GPT-4 et GPT-3. Image tirée de « Instruction Tuning with GPT-4 » (Peng et al., 2023).

GPT-4 semble posséder une gamme plus large et plus diversifiée de paires verbe-nom et tend à générer des réponses plus longues.

Représentez graphiquement ces distributions par source de données, période, annotateur, etc. Observez-vous des tendances dans les questions, avec des réponses plus longues/courtes ou des scores plus élevés/plus faibles ? Y a-t-il des valeurs aberrantes ? Quelle pourrait en être la cause ? Que faire ?

Si les scores sont censés suivre une distribution normale, est-ce le cas pour tous les annotateurs ? Vous remarquerez peut-être que certains annotateurs ont tendance à donner des réponses beaucoup plus courtes ou à surévaluer les scores ; il vous appartient alors de décider de l’interprétation de leurs annotations.

Si chaque exemple comporte plusieurs annotations, calculez le désaccord entre les annotateurs. Examinez les exemples présentant des annotations contradictoires et résolvez les conflits.

Il existe de nombreux outils d'exploration de données utiles, mais ils ne remplaceront jamais l'inspection manuelle des données. Dans tous les projets auxquels j'ai participé, un simple _examen des données_ _pendant_ _15 minutes m'a généralement permis d'obtenir des informations précieuses qui m'ont épargné des heures de travail fastidieux_ . [Greg Brockman, cofondateur d'OpenAI](https://x.com/gdb/status/1622683988736479232) , a tweeté : « L'inspection manuelle des données présente probablement le meilleur rapport valeur/prestige de toutes les activités d'apprentissage automatique. »

Examinez vos données pour vérifier la pertinence des exemples. S'il s'agit de données annotées, sélectionnez quelques requêtes et essayez de les annoter vous-même afin de comparer vos annotations à celles fournies. Cela vous permettra d'évaluer la fiabilité des annotations. Vérifiez ensuite les réponses. Les exemples sont-ils suffisamment uniques ? Existe-t-il des exemples avec la même requête mais des réponses différentes ? Ou inversement ?

## Données dédupliquées

Les données dupliquées peuvent fausser la distribution des données et introduire des biais dans votre modèle. Prenons l'exemple d'un jeu de données semblable au [Tableau 8-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_table_3_1730130931981189) . Les entrées dupliquées pourraient amener le modèle à conclure, à tort, que tous les éléments rouges sont chers. Les doublons peuvent également contaminer l'ensemble de test. Lors de la répartition des données dupliquées entre les ensembles d'entraînement et de test, on pourrait par exemple trouver une entrée dans l'ensemble d'entraînement et sa copie dans l'ensemble de test.

Tableau 8-3. Un jeu de données factice avec des exemples dupliqués dans les cellules grises.

|     |Entrée (Description du produit)|Sortie (Prix)|
|---|---|---|
| 1   |`{item: pencil, color: red}`|`$20`|
| 2   |`{item: compass, color: green}`|`$2`|
| 3   |`{item: pencil, color: red}`|`$20`|
| 4   |`{item: pencil, color: red}`|`$20`|
| 5   |`{item: pencil, color: green}`|`$1`|

Plusieurs études ont démontré l'impact négatif des duplications de données d'entraînement sur les performances des modèles ; voir [Lee et al. (2021)](https://arxiv.org/abs/2107.06499) et [Tirumala et al. (2023)](https://arxiv.org/abs/2308.12284) . Une étude menée par Anthropic a montré que la répétition de 0,1 % des données 100 fois peut entraîner une dégradation des performances d'un modèle à 800 millions de paramètres, les ramenant à celles d'un modèle à 400 millions de paramètres, alors même que 90 % des données d'entraînement restent uniques ( [Hernandez et al., 2022](https://arxiv.org/abs/2205.10487) ). Même lorsque les duplications n'affectent pas directement les performances du modèle, elles peuvent engendrer une perte de temps et de ressources de calcul.

Selon les données, il existe de nombreuses formes de duplication, dont certaines sont plus difficiles à détecter. Voici par exemple quelques types de duplications dans un ensemble de documents :

- Duplication de documents entiers : un même document apparaissant plus d’une fois.
    
- Duplications au sein d'un même document : par exemple, le même paragraphe apparaît deux fois dans un même document.
    
- Duplications entre documents : par exemple, une même citation populaire apparaît dans plusieurs documents.
    

La définition des doublons dépend également de votre approche. Par exemple, souhaitez-vous les considérer au niveau du document, du paragraphe, de la phrase ou du mot ? Deux textes doivent-ils être identiques pour être considérés comme des doublons, ou un chevauchement de 80 % est-il suffisant ? Deux listes sont-elles considérées comme des doublons si elles contiennent les mêmes éléments, mais dans un ordre différent ?

La déduplication peut s'appuyer sur les mêmes techniques que celles utilisées pour les mesures de similarité (présentées au [chapitre 3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) ). Elle sert également à la résolution d'identité, permettant de déterminer si deux identités (par exemple, deux profils sur les réseaux sociaux) sont identiques. Voici quelques méthodes concrètes pour dédupliquer des données :

comparaison par paires

Calculez le score de similarité de chaque exemple avec tous les autres exemples de l'ensemble de données, en utilisant la correspondance exacte, la correspondance n-gramme, la correspondance floue ou le score de similarité sémantique, comme expliqué au [chapitre 3.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) Cette approche peut toutefois s'avérer coûteuse avec de grands ensembles de données.

Hachage

Répartissez les exemples par hachage dans différents compartiments et effectuez la vérification uniquement parmi les exemples appartenant au même compartiment. Les méthodes de déduplication basées sur le hachage incluent [MinHash](https://en.wikipedia.org/wiki/MinHash) et [le filtre de Bloom](https://en.wikipedia.org/wiki/Bloom_filter) .

Réduction de dimensionnalité

Utilisez une technique de réduction de dimensionnalité pour commencer par réduire la dimensionnalité de vos données, puis effectuez une comparaison par paires. De nombreuses techniques de recherche vectorielle, présentées au [chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) , peuvent être utilisées à cette fin.

Une recherche rapide permettra de trouver de nombreuses bibliothèques facilitant la déduplication. Parmi elles, citons [dupeGuru](https://github.com/arsenetar/dupeguru) , [Dedupe](https://github.com/dedupeio/dedupe) , [datasketch](https://github.com/ekzhu/datasketch) , [TextDistance](https://github.com/life4/textdistance) , [TheFuzz](https://github.com/seatgeek/thefuzz) et [deduplicate-text-datasets](https://github.com/google-research/deduplicate-text-datasets) . <sup> [16 </sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1584)

## Nettoyer et filtrer les données

Les données doivent être nettoyées pour que votre modèle soit performant et sûr.

Il est conseillé de commencer par supprimer les balises de formatage superflues. Étant donné que de nombreux jeux de données publics sont extraits d'Internet, les balises HTML superflues sont fréquentes. À moins de vouloir entraîner votre modèle sur des balises HTML, supprimez-les. [Databricks](https://oreil.ly/Gbu2T) a constaté que la suppression des jetons Markdown et HTML superflus améliorait la précision de son modèle de 20 % tout en réduisant la longueur des jetons d'entrée de 60 %.

Vous devez nettoyer vos données de tout élément non conforme à vos politiques, comme les données personnelles, les données sensibles, les données protégées par le droit d'auteur ou les données considérées comme toxiques. Les techniques présentées au [chapitre 4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) peuvent vous aider. Supprimez tous les champs dont l'utilisation est interdite, tels que le code postal, le nom et le sexe.

Vous pouvez également supprimer les données de faible qualité, en utilisant les techniques décrites dans la section [« Vérification des données »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_data_verification_1730130932021284) pour détecter ces données.

L'inspection manuelle des données est particulièrement importante à cette étape. Un examen attentif des données peut vous aider à repérer des schémas pouvant servir d'heuristiques pour détecter les données de faible qualité. Ces heuristiques peuvent ne pas être évidentes. Par exemple, [Kern et al. (2024)](https://arxiv.org/html/2311.14212v2) ont constaté que les annotations réalisées durant la seconde moitié d'une session d'annotation sont de moindre qualité, probablement en raison de l'ennui ou de la fatigue de l'annotateur.

Si vous disposez de plus de données que nécessaire ou que vous ne pouvez en utiliser (par exemple, en raison de votre budget de calcul), vous pouvez affiner le filtrage. Par exemple, vous pouvez utiliser des techniques _d'apprentissage actif_ pour sélectionner les exemples les plus pertinents pour l'apprentissage de votre modèle. Vous pouvez également recourir à [l'échantillonnage d'importance](https://oreil.ly/Tb4-W) pour identifier les exemples les plus importants pour votre tâche. L'efficacité de ces méthodes dépend de votre capacité à évaluer correctement l'importance de chaque exemple d'entraînement. Dans leur article sur l'élagage des données ( [Sorscher et al., 2022](https://arxiv.org/abs/2206.14486) ), des chercheurs ont conclu que la découverte de métriques d'élagage efficaces peut réduire considérablement les coûts en ressources de l'apprentissage profond moderne.

## Données de format

Une fois vos données dédupliquées et nettoyées, vous devez les convertir au format requis par le modèle que vous affinez. Chaque modèle utilise un tokenizer spécifique et attend des données dans un format de chat particulier, comme expliqué au [chapitre 5.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) Utiliser un format de chat incorrect peut engendrer des dysfonctionnements inattendus.

Si vous effectuez un finetuning supervisé, vos données sont très probablement au format (instruction, réponse). Les instructions peuvent être décomposées en (invite système, invite utilisateur). Si vous êtes passé du développement des invites au finetuning, les instructions utilisées pour le finetuning peuvent différer de celles utilisées lors du développement des invites. Pendant le finetuning, les instructions ne nécessitent généralement ni description de la tâche ni exemples. Si vous disposez de suffisamment d'exemples d'entraînement, le modèle peut apprendre directement le comportement attendu de la tâche à partir de ces exemples.

À titre d'exemple, imaginez que vous utilisiez cette instruction en trois étapes pour votre tâche de classification des aliments avec un modèle de base :

```
Label the following item as either edible or inedible.
    
Item: burger
Label: edible

Item: car
Label: inedible
   
Item: mushroom
Label: edible
   
Item: {INPUT}
Label:
```          

Pour le réglage fin, tous les exemples inclus dans l'invite à 3 coups peuvent être convertis en exemples d'entraînement. Les données d'entraînement pour le réglage fin ressembleront au [tableau 8-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_table_4_1730130931981212) .

Tableau 8-4. Exemple de données d'entraînement utilisées pour une tâche de classification alimentaire.

| Exemple d'identifiant | Saisir         | Sortir     |
| --------------------- | -------------- | ---------- |
| 1                     | `burger -->`   | `edible`   |
| 2                     | `car -->`      | `inedible` |
| 3                     | `mushroom -->` | `edible`   |
| …                     | …              | …          |

Une fois le modèle affiné, vous pouvez utiliser une invite aussi simple que :

  `{``INPUT``}` `-->`

Cette invite est beaucoup plus courte que celle utilisée avec le modèle de base. Par conséquent, si vous vous souciez des jetons d'entrée de vos instructions, un réglage fin peut permettre d'en réduire le coût.

Les différents formats de données utilisés pour l'ajustement fin peuvent influencer les performances de votre modèle. Il peut être utile de réaliser des essais pour déterminer le format le plus adapté à vos besoins.

Lorsque vous utilisez le modèle affiné, assurez-vous que les invites utilisées correspondent au format des données d'affinage. Par exemple, si les données d'entraînement utilisent l'invite au format « burger --> », les invites suivantes peuvent poser problème :

- « burger » : flèche finale manquante
    
- « Article : burger --> » : préfixe supplémentaire
    
- « burger --> » : espace supplémentaireajouté
    

# Résumé

Bien que la création de données d'entraînement soit un processus complexe, les principes de la création d'un jeu de données sont étonnamment simples. Pour constituer un jeu de données permettant d'entraîner un modèle, il faut commencer par définir les comportements que le modèle doit apprendre, puis concevoir un jeu de données illustrant ces comportements. Compte tenu de l'importance des données, les équipes mettent en place des postes dédiés, chargés d'acquérir les jeux de données appropriés tout en garantissant la confidentialité et la conformité.

Les données nécessaires dépendent non seulement de votre cas d'utilisation, mais aussi de la phase d'entraînement. Le pré-entraînement requiert des données différentes de celles nécessaires pour le réglage fin des instructions et le réglage fin des préférences. Cependant, la conception des jeux de données, quelle que soit la phase d'entraînement, repose sur les trois mêmes critères fondamentaux : la qualité, la couverture et la quantité.

Si la quantité de données utilisées pour entraîner un modèle fait souvent la une, disposer de données de haute qualité et suffisamment complètes est tout aussi important. Un petit volume de données de haute qualité peut surpasser un grand volume de données bruitées. De même, de nombreuses équipes ont constaté qu'accroître la diversité de leurs ensembles de données est essentiel pour améliorer les performances de leurs modèles.

Face à la difficulté d'acquérir des données de haute qualité, de nombreuses équipes se sont tournées vers les données synthétiques. Si la génération de données par programmation a longtemps été un objectif, ce n'est qu'avec l'avènement de l'IA et sa capacité à créer des données réalistes et complexes que les données synthétiques sont devenues une solution pratique pour de nombreux cas d'utilisation. Ce chapitre présente différentes techniques de synthèse de données, et plus particulièrement la synthèse de données d'instructions pour le réglage fin.

À l'instar des données réelles, les données synthétiques doivent être évaluées afin de garantir leur qualité avant d'être utilisées pour l'entraînement des modèles. L'évaluation des données générées par l'IA est tout aussi complexe que celle des autres résultats de l'IA, et les utilisateurs privilégient les données générées qu'ils peuvent évaluer avec fiabilité.

Les données représentent un défi car de nombreuses étapes de leur création sont difficilement automatisables. Annoter des données est complexe, mais élaborer des consignes d'annotation l'est encore plus. Automatiser la génération de données est difficile, mais automatiser leur vérification l'est encore plus. Si la synthèse de données permet d'en générer davantage, il est impossible d'automatiser la réflexion sur les données souhaitées. L'automatisation des consignes d'annotation est complexe. Enfin, l'attention portée aux détails ne peut être automatisée.

Cependant, les problèmes complexes engendrent des solutions créatives. Lors de mes recherches pour ce chapitre, j'ai été particulièrement frappée par l'importance de la créativité dans la conception des jeux de données. Il existe une multitude de façons de construire et d'évaluer des données. J'espère que la diversité des techniques de synthèse et de vérification des données présentées dans ce chapitre vous inspirera pour la conception de vos propres jeux de données.

Supposons que vous ayez constitué un excellent jeu de données vous permettant d'entraîner un modèle performant. Comment déployer ce modèle ? Le chapitre suivant abordera l'optimisation de l'inférence en termes de latence et de coût.

[1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1508-marker)L'importance croissante des données se reflète dans l'évolution des efforts de traitement entre GPT-3 et GPT-4. Dans la liste des contributeurs à GPT-3 ( [OpenAI, 2020](https://oreil.ly/R4-VI) ), seules deux personnes étaient créditées pour la collecte, le filtrage et la déduplication des données, ainsi que pour l'analyse des chevauchements sur les données d'entraînement. La situation a radicalement changé trois ans plus tard. Pour GPT-4 ( [OpenAI, 2023](https://oreil.ly/F9Fyc) ), quatre-vingts personnes ont été créditées pour leur participation à différents processus de traitement des données. Cette liste n'inclut pas encore les annotateurs de données recrutés par OpenAI auprès de fournisseurs de données. Pour un format en apparence aussi simple que ChatML, onze personnes ont été impliquées, dont de nombreux chercheurs confirmés. En [2016, lors d'une session de questions-réponses (AMA)](https://oreil.ly/h-lAl) , Wojciech Zaremba, cofondateur d'OpenAI, avait déclaré que l'équipe prévoyait de mener la majeure partie de ses recherches à partir d'ensembles de données publics.

[2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1512-marker)Si vous utilisez beaucoup de données, assurer leur conformité peut à elle seule constituer un travail à temps plein.

[3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1515-marker)J'adore écrire, mais je déteste tenter de résumer les opinions de chacun en une seule définition. [IBM](https://oreil.ly/3d_EG) définit la qualité des données selon sept dimensions : exhaustivité, unicité, validité, actualité, exactitude, cohérence et adéquation à l'usage. [Wikipédia](https://en.wikipedia.org/wiki/Data_quality) y ajoute l'accessibilité, la comparabilité, la crédibilité, la flexibilité et la plausibilité. Nombre de ces définitions abordent la qualité des données dans un large éventail de cas d'utilisation. Ici, je souhaite me concentrer sur la qualité des données pour l'optimisation fine.

[4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1516-marker)Un bug particulièrement gênant dont je me souviens encore est celui d'une colonne de données de type float qui a été mal enregistrée comme un entier, ce qui a arrondi ces valeurs et entraîné des comportements déconcertants.

[5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1517-marker)Bien que cela ne concerne pas le caractère unique de vos données, posséder des données que personne d'autre ne possède peut s'avérer extrêmement précieux.

[6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1523-marker)Dans [_l'ouvrage « Conception de systèmes d'apprentissage automatique »_](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) , j'ai également abordé d'autres techniques permettant de réduire la demande en données annotées, notamment la supervision faible, la semi-supervision et l'apprentissage actif.

[7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1526-marker)J'ai entendu tellement d'entreprises parler de « cercle vertueux des données » dans leurs présentations que je suis convaincu qu'il est illégal de lancer une startup d'IA sans mentionner ce concept.

[8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1535-marker)Mon livre, [_Designing Machine Learning Systems_](https://learning.oreilly.com/library/view/designing-machine-learning/9781098107956/ch04.html#perturbation) , aborde l'augmentation des données au chapitre 4.

[9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1536-marker)Un exemple évident que je n'ai pas inclus dans le texte principal est celui de l'entraînement d'un modèle pour détecter du contenu généré par l'IA. Il vous faut du contenu généré par l'IA comme exemples d'entraînement.

[10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1539-marker)De nombreux jeux exceptionnels sont possibles grâce à la génération procédurale. Des jeux comme _Minecraft_ et _No Man's Sky_ utilisent des fonctions de bruit et des algorithmes fractals pour créer de vastes mondes immersifs. Dans _Donjons et Dragons_ , la génération procédurale permet de créer des donjons, des quêtes et des rencontres aléatoires, ce qui rend le jeu plus attrayant en y ajoutant une part d'imprévisibilité et en offrant des possibilités infinies.

[11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1549-marker)Cela signifie qu'en théorie, il est possible d'entraîner un modèle capable de s'améliorer continuellement. Cependant, sa faisabilité en pratique est une autre affaire.

[12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1551-marker)Ils « ont observé qu’environ 20 % des solutions étaient initialement incorrectes mais se corrigeaient d’elles-mêmes, ce qui indique que le modèle a appris des retours d’exécution et a amélioré ses performances. »

[13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1561-marker)Le même problème peut survenir avec les annotations humaines. Si l'annotateur humain utilise ses connaissances, contrairement au modèle, pour répondre à une question, il induit en réalité le modèle en erreur.

[14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1564-marker)Ce concept a également été expliqué plus tard par les mêmes auteurs dans [« AI Models Collapse When Trained on Recursively Generated Data »](https://oreil.ly/hJhTF) ( _Nature_ , juillet 2024).

[15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1573-marker)Comparer le nombre de paramètres d'un modèle de mélange d'experts comme Mixtral à celui d'un modèle dense comme Nemotron-4 n'est pas juste, mais le fait que le modèle enseignant (Mixtral) soit plus petit que le modèle étudiant (Nemotron-4) reste valable.

[16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#id1584-marker)L'une de mes bibliothèques open source, [lazyNLP](https://github.com/chiphuyen/lazynlp) , prend également en charge l'estimation du chevauchement et la déduplication à l'aide du filtre de Bloom.