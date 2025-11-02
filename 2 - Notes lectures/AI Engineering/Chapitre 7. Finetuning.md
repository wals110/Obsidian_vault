

Le finetuning est le processus d'adaptation d'un modèle à une tâche spécifique par un entraînement supplémentaire, que ce soit sur l'ensemble du modèle ou sur une partie de celui-ci. Les chapitres [5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) et [6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) abordent les méthodes basées sur des incitations, qui adaptent un modèle en lui fournissant des instructions, un contexte et des outils. Le finetuning, quant à lui, adapte un modèle en ajustant ses pondérations.

Le réglage fin permet d'améliorer divers aspects d'un modèle. Il peut optimiser ses capacités spécifiques à un domaine, comme le codage ou la réponse à des questions médicales, et renforcer sa sécurité. Cependant, il est le plus souvent utilisé pour améliorer sa capacité à suivre des instructions, notamment pour garantir le respect de styles et de formats de sortie spécifiques.

Bien que le réglage fin permette de créer des modèles mieux adaptés à vos besoins, il exige un investissement initial plus important. On me demande souvent quand privilégier le réglage fin et quand utiliser la méthode RAG (Relative Auto-Global Index). Après une présentation du réglage fin, ce chapitre abordera les raisons de l'utiliser et celles de ne pas l'utiliser, ainsi qu'un cadre de réflexion simple pour choisir entre le réglage fin et les méthodes alternatives.

Comparativement aux méthodes basées sur les invites, le réglage fin consomme beaucoup plus de mémoire. À l'échelle des modèles de base actuels, un réglage fin naïf requiert souvent plus de mémoire que celle disponible sur un seul GPU. Cela rend le réglage fin coûteux et complexe. Comme nous l'avons vu tout au long de ce chapitre, la réduction des besoins en mémoire est une motivation essentielle pour de nombreuses techniques de réglage fin. Une section de ce chapitre est consacrée à la description des facteurs contribuant à l'empreinte mémoire d'un modèle, ce qui est important pour la compréhension de ces techniques.

L'approche PEFT (parameter-efficient finetuning), qui optimise l'utilisation de la mémoire, s'est imposée comme la méthode dominante en matière de réglage fin. Ce chapitre explore la méthode PEFT et ses différences avec le réglage fin traditionnel ; il présente également un aperçu de ses techniques en constante évolution. Je me concentrerai plus particulièrement sur une catégorie prometteuse : les techniques basées sur les adaptateurs.

Avec les méthodes basées sur des invites, une connaissance du fonctionnement interne des modèles d'apprentissage automatique est recommandée, mais pas indispensable. Cependant, le réglage fin vous amène au domaine de l'entraînement des modèles, où des connaissances en apprentissage automatique sont nécessaires. Les bases de l'apprentissage automatique dépassent le cadre de cet ouvrage. Si vous souhaitez une révision rapide, le [dépôt GitHub](https://github.com/chiphuyen/aie-book) du livre contient des liens vers des ressources utiles. Dans ce chapitre, j'aborderai quelques concepts fondamentaux directement pertinents pour notre discussion.

Ce chapitre est celui qui m'a posé le plus de difficultés techniques à rédiger, non pas en raison de la complexité des concepts abordés, mais plutôt de leur vaste portée. Je soupçonne qu'il sera également difficile à lire. Si, à un moment donné, vous avez l'impression de vous attarder trop sur des détails qui ne sont pas pertinents pour votre travail, n'hésitez pas à passer au suivant.

Il y a beaucoup à dire. Entrons dans le vif du sujet !

# Aperçu du réglage fin

Pour affiner le modèle, on part d'un modèle de base qui possède certaines, mais pas toutes, les fonctionnalités nécessaires. L'objectif de l'affinage est d'obtenir un modèle suffisamment performant pour votre tâche spécifique.

Le réglage fin est une méthode d' _apprentissage par transfert_ , un concept introduit par [Bozinovski et Fulgosi](https://oreil.ly/Udw0Z) en 1976. L'apprentissage par transfert vise à transposer les connaissances acquises lors d'une tâche afin d'accélérer l'apprentissage d'une nouvelle tâche connexe. Ce processus est conceptuellement similaire à la manière dont les humains transfèrent leurs compétences : par exemple, savoir jouer du piano facilite l'apprentissage d'un autre instrument de musique.

L'un des premiers succès à grande échelle en matière d'apprentissage par transfert fut le système de traduction multilingue de Google ( [Johnson et al., 2016](https://arxiv.org/abs/1611.04558) ). Le modèle a transféré ses connaissances en matière de traduction portugais-anglais et anglais-espagnol pour traduire directement du portugais vers l'espagnol, même en l'absence d'exemples portugais-espagnol dans les données d'entraînement.

Depuis les débuts de l'apprentissage profond, l'apprentissage par transfert offre une solution aux tâches pour lesquelles les données d'entraînement sont limitées ou coûteuses. En entraînant un modèle de base sur des tâches disposant de nombreuses données, il est possible de transférer ces connaissances à une tâche cible.

Pour les LLM, les connaissances acquises lors du pré-entraînement à la complétion de texte (une tâche pour laquelle les données sont abondantes) sont transférées à des tâches plus spécialisées, comme la réponse aux questions juridiques ou la conversion de texte en SQL, pour lesquelles les données disponibles sont souvent plus rares. Cette capacité d'apprentissage par transfert confère une valeur particulière aux modèles de base.

L'apprentissage par transfert améliore _l'efficacité de l'échantillonnage_ , permettant à un modèle d'apprendre le même comportement avec moins d'exemples. Un modèle _économe en exemples_ apprend efficacement à partir d'un nombre réduit d'échantillons. Par exemple, alors que l'entraînement d'un modèle de réponse à des questions juridiques à partir de zéro peut nécessiter des millions d'exemples, l'ajustement fin d'un bon modèle de base peut n'en nécessiter que quelques centaines.

Idéalement, la majeure partie des connaissances que le modèle doit acquérir est déjà présente dans le modèle de base, et le fine-tuning ne fait qu'affiner son comportement. [L'article d'OpenAI sur InstructGPT](https://oreil.ly/5-5lw) (2022) suggère de considérer le fine-tuning comme un moyen de libérer les capacités intrinsèques du modèle, mais difficiles d'accès pour l'utilisateur par la seule force des instructions.

###### Note

Le réglage fin n'est pas la seule méthode d'apprentissage par transfert. Une autre approche consiste à utiliser _le transfert basé sur les caractéristiques_ . Dans cette approche, un modèle est entraîné à extraire des caractéristiques des données, généralement sous forme de vecteurs d'intégration, qui sont ensuite utilisés par un autre modèle. J'évoque brièvement le transfert basé sur les caractéristiques au [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) , lorsque j'explique comment une partie d'un modèle de base peut être réutilisée pour une tâche de classification en _ajoutant une tête de classifieur_ .

Le transfert basé sur les caractéristiques est très courant en vision par ordinateur. Par exemple, dans la seconde moitié des années 2010, de nombreux chercheurs ont utilisé des modèles entraînés sur l'ensemble de données ImageNet pour extraire des caractéristiques d'images et les utiliser dans d'autres tâches de vision par ordinateur telles que la détection d'objets ou la segmentation d'images.

Le finetuning fait partie du processus d'entraînement d'un modèle. Il prolonge le pré-entraînement. Puisque tout entraînement effectué après le pré-entraînement est du finetuning, ce dernier peut prendre de nombreuses formes. [Le chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) a déjà abordé deux types de finetuning :Réglage fin supervisé et réglage fin des préférences. Passons rapidement en revue ces méthodes et comment vous pouvez les utiliser en tant que développeur d'applications.

Rappelons que l'entraînement d'un modèle commence par _un pré-entraînement_ , généralement réalisé par auto-supervision. L'auto-supervision permet au modèle d'apprendre à partir d'une grande quantité de données non étiquetées. Pour les modèles de langage, les données d'auto-supervision sont généralement des _séquences de texte_ ne nécessitant aucune annotation.

Avant d'affiner ce modèle pré-entraîné avec des données spécifiques à la tâche, coûteuses, vous pouvez l'affiner par auto-apprentissage en utilisant des données connexes peu onéreuses. Par exemple, pour affiner un modèle de réponse aux questions juridiques, avant de l'affiner sur des données annotées (questions, réponses) coûteuses, vous pouvez l'affiner sur des documents juridiques bruts. De même, pour affiner un modèle de résumé de livres en vietnamien, vous pouvez d'abord l'affiner sur un vaste corpus de textes vietnamiens. _L'affinage par auto-apprentissage_ est également appelé _pré-entraînement continu_ .

Comme expliqué au [chapitre 1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_introduction_to_building_ai_applications_with_foun_1730130814984319) , les modèles de langage peuvent être autorégressifs ou masqués. Un modèle autorégressif prédit le jeton suivant d'une séquence en utilisant les jetons précédents comme contexte. Un modèle masqué, quant à lui, complète le jeton manquant en utilisant les jetons qui le précèdent et le suivent. De même, grâce à l'apprentissage supervisé, il est possible d'affiner un modèle pour prédire le jeton suivant ou compléter le jeton manquant. Cette dernière technique, également appelée _affinage par remplissage_ , est particulièrement utile pour des tâches telles que l'édition de texte et le débogage de code. Il est possible d'affiner un modèle pour le remplissage même s'il a été pré-entraîné de manière autorégressive.

L'immense quantité de données dont un modèle peut tirer des enseignements lors de l'apprentissage auto-supervisé lui confère une compréhension approfondie du monde. Cependant, il peut s'avérer difficile pour les utilisateurs d'exploiter ces connaissances pour leurs tâches, ou le comportement du modèle peut être en décalage avec les préférences humaines. Le réglage fin supervisé utilise des données annotées de haute qualité pour affiner le modèle et l'adapter aux usages et aux préférences des utilisateurs.

Lors de _l'ajustement supervisé_ , le modèle est entraîné à l'aide de paires (entrée, sortie) : l'entrée peut être une consigne et la sortie une réponse. Une réponse peut être ouverte, comme pour la tâche de résumé de livre, ou fermée, comme pour une tâche de classification. La création de données de consignes de haute qualité peut s'avérer complexe et coûteuse, notamment pour les consignes exigeant une cohérence factuelle, une expertise du domaine ou le respect des normes politiques. [Le chapitre 8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) explique comment acquérir ces données.

Un modèle peut également être affiné grâce à l'apprentissage par renforcement afin de générer des réponses qui maximisent les préférences humaines. Cet affinement nécessite des données comparatives qui suivent généralement le format suivant : (instruction, réponse gagnante, réponse perdante).

Il est possible d'affiner un modèle pour étendre la longueur de son contexte. _L'affinage pour contexte long_ nécessite généralement de modifier l'architecture du modèle, notamment en ajustant les plongements positionnels. Une longue séquence implique davantage de positions possibles pour les jetons, et les plongements positionnels doivent pouvoir les gérer. Comparé à d'autres techniques d'affinage, l'affinage pour contexte long est plus complexe. Le modèle résultant peut également présenter des performances dégradées sur des séquences plus courtes.

[Figure 7-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07a_figure_1_1730160615799658) Cette figure illustre la création de différents modèles Code Llama ( [Rozière et al., 2024](https://arxiv.org/abs/2308.12950) ), à partir du modèle de base Llama 2, en utilisant différentes techniques d'ajustement fin. Grâce à un ajustement fin basé sur un contexte long, les auteurs ont pu augmenter la longueur maximale du contexte du modèle de 4 096 à 16 384 jetons afin de prendre en charge des fichiers de code plus longs. Sur l'image, l'ajustement fin des instructions fait référence à un ajustement fin supervisé.

L'ajustement fin peut être effectué aussi bien par les développeurs de modèles que par les développeurs d'applications. Les développeurs de modèles effectuent généralement un post-entraînement avec différentes techniques d'ajustement fin avant la publication du modèle. Ils peuvent également publier différentes versions du modèle, chacune affinée à un degré différent, afin que les développeurs d'applications puissent choisir la version la plus adaptée à leurs besoins.

![Diagramme d'un programme. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0701.png)

###### Figure 7-1. Différentes techniques de réglage fin utilisées pour créer différents modèles Code Llama. Image tirée de Rozière et al. (2024). Adaptée d'une image originale sous licence CC BY 4.0.

En tant que développeur d'applications, vous pourriez affiner un modèle pré-entraîné, mais le plus souvent, vous affinerez un modèle post-entraîné. Plus un modèle est précis et plus ses connaissances sont pertinentes pour votre tâche, moins vous aurez de travail à fournir pour l'adapter.

# Quand effectuer les derniers réglages

Avant d'explorer différentes techniques de réglage fin, il est essentiel de déterminer si cette approche est adaptée à votre situation. Comparé aux méthodes basées sur des incitations, le réglage fin exige des ressources nettement plus importantes, non seulement en termes de données et de matériel, mais aussi en compétences en apprentissage automatique. C'est pourquoi on y recourt généralement _après_ de nombreuses expérimentations avec des méthodes basées sur des incitations. Toutefois, réglage fin et incitations ne sont pas incompatibles. Les problèmes concrets nécessitent souvent les deux approches.

## Raisons d'affiner

Le principal objectif du réglage fin est d'améliorer la qualité d'un modèle, tant au niveau de ses capacités générales que de ses capacités spécifiques à une tâche. Le réglage fin est couramment utilisé pour améliorer la capacité d'un modèle à générer des sorties conformes à des structures spécifiques, telles que les formats JSON ou YAML.

Un modèle généraliste performant sur de nombreux tests de performance peut ne pas l'être pour votre tâche spécifique. Si le modèle que vous souhaitez utiliser n'a pas été suffisamment entraîné pour votre tâche, un ajustement fin avec vos données peut s'avérer particulièrement utile.

Par exemple, un modèle standard peut être performant pour la conversion de texte vers le dialecte SQL standard, mais échouer avec un dialecte SQL moins courant. Dans ce cas, un paramétrage précis du modèle sur des données contenant ce dialecte SQL s'avérera utile. De même, si le modèle fonctionne correctement avec le SQL standard pour les requêtes courantes, mais rencontre souvent des difficultés avec les requêtes spécifiques aux clients, un paramétrage précis sur ces dernières pourrait être bénéfique.

L'un des cas d'utilisation particulièrement intéressants du finetuning est la correction des biais. L'idée est que si le modèle de base perpétue certains biais issus de ses données d'entraînement, l'exposition à des données soigneusement sélectionnées lors du finetuning peut contrer ces biais ( [Wang et Russakovsky, 2023](https://oreil.ly/iPwB_) ). Par exemple, si un modèle attribue systématiquement aux PDG des noms à consonance masculine, son finetuning sur un ensemble de données comportant de nombreuses femmes PDG peut atténuer ce biais. [Garimella et al. (2022)](https://oreil.ly/RoPL4) ont constaté que le finetuning de modèles de langage de type BERT sur des textes rédigés par des femmes peut réduire les biais de genre de ces modèles, tandis que leur finetuning sur des textes d'auteurs africains peut réduire les biais raciaux.

Il est possible d'optimiser un modèle complexe pour l'améliorer, mais l'optimisation de modèles plus petits est beaucoup plus courante. Ces derniers nécessitent moins de mémoire et sont donc plus faciles à optimiser. Ils sont également moins coûteux et plus rapides à mettre en œuvre en production.

Une approche courante consiste à affiner un petit modèle pour qu'il imite le comportement d'un modèle plus vaste à l'aide des données générées par ce dernier. Cette approche, qui consiste à condenser les connaissances du modèle vaste en un petit modèle, est appelée _distillation_ . Elle est abordée au [chapitre 8,](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) ainsi que d'autres techniques de synthèse de données.

Un petit modèle, optimisé pour une tâche spécifique, peut surpasser un modèle standard beaucoup plus volumineux pour cette même tâche. Par exemple, Grammarly a constaté que ses modèles Flan-T5 optimisés ( [Chung et al., 2022](https://arxiv.org/abs/2210.11416) ) étaient plus performants qu'une variante de GPT-3 spécialisée dans la correction de texte pour un large éventail de tâches d'aide à la rédaction, malgré une taille 60 fois inférieure. Le processus d'optimisation n'a utilisé que 82 000 paires (instruction, sortie), soit moins que les données généralement nécessaires pour entraîner un modèle de correction de texte à partir de zéro.

Aux débuts des modèles de base, lorsque les modèles les plus performants étaient commerciaux et que l'accès au réglage fin était limité, peu de modèles compétitifs étaient disponibles pour ce réglage. Cependant, avec la prolifération de modèles de haute qualité de toutes tailles, adaptés à une grande variété de domaines, au sein de la communauté open source, le réglage fin est devenu beaucoup plus viable et attractif.

## Raisons de ne pas procéder à un réglage fin

Bien que le réglage fin puisse améliorer un modèle de multiples façons, bon nombre de ces améliorations peuvent également être obtenues, dans une certaine mesure, sans réglage fin. Le réglage fin peut améliorer les performances d'un modèle, tout comme des invites et un contexte soigneusement conçus. Le réglage fin peut faciliter la structuration des résultats, mais de nombreuses autres techniques, présentées au [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) , permettent également d'atteindre cet objectif.

Premièrement, bien que l'optimisation d'un modèle pour une tâche spécifique puisse améliorer ses performances pour cette tâche, elle peut les dégrader pour d'autres tâches. [Cela](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1369) peut s'avérer frustrant lorsque ce modèle est destiné à une application qui attend des requêtes variées.

Imaginez que vous ayez besoin d'un modèle pour trois types de requêtes : recommandations de produits, modifications de commandes et avis généraux. Initialement, le modèle fonctionne bien pour les recommandations de produits et les avis généraux, mais mal pour les modifications de commandes. Pour y remédier, vous affinez le modèle sur un ensemble de données de paires (requête, réponse) concernant les modifications de commandes. Le modèle affiné pourrait effectivement être plus performant pour ce type de requête, mais moins performant pour les deux autres.

Que faire dans ce cas ? Vous pouvez affiner le modèle pour toutes les requêtes qui vous intéressent, et pas seulement en modifiant leur ordre. Si vous n’arrivez pas à obtenir un modèle performant pour toutes vos tâches, envisagez d’utiliser des modèles distincts pour chaque tâche. Si vous souhaitez combiner ces modèles distincts en un seul pour simplifier leur utilisation, vous pouvez également envisager de les fusionner, comme expliqué plus loin dans ce chapitre.

Si vous débutez un projet, le réglage fin est rarement la première étape à entreprendre. Il exige des investissements initiaux importants et une maintenance continue. Tout d'abord, il vous faut des données. L'acquisition manuelle de données annotées peut s'avérer longue et coûteuse, notamment pour les tâches nécessitant un esprit critique et une expertise du domaine. Les données open source et les données générées par l'IA peuvent réduire les coûts, mais leur efficacité est très variable.

Deuxièmement, le finetuning requiert la maîtrise de l'entraînement des modèles. Il est nécessaire d'évaluer des modèles de base afin d'en choisir un à affiner. Selon vos besoins et vos ressources, les options peuvent être limitées. Bien que les frameworks et API de finetuning puissent automatiser de nombreuses étapes du processus, il est indispensable de comprendre les différents paramètres d'entraînement à ajuster, de suivre l'apprentissage et de déboguer en cas de problème. Par exemple, il faut comprendre le fonctionnement d'un optimiseur, le taux d'apprentissage approprié, la quantité de données d'entraînement nécessaire, comment gérer le surapprentissage et le sous-apprentissage, et comment évaluer les modèles tout au long du processus.

Troisièmement, une fois votre modèle affiné, il vous faudra déterminer comment le déployer. Allez-vous l'héberger vous-même ou utiliser un service API ? Comme expliqué au [chapitre 9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301) , l'optimisation de l'inférence pour les grands modèles, notamment les LLM, est complexe. L'affinage est plus aisé techniquement si vous hébergez déjà vos modèles en interne et que vous savez comment les gérer.

Plus important encore, vous devez définir une politique et un budget pour le suivi, la maintenance et la mise à jour de votre modèle. À mesure que vous affinez votre modèle, de nouveaux modèles de base sont développés rapidement. Ces modèles de base peuvent progresser plus vite que votre modèle affiné. Si un nouveau modèle de base surpasse votre modèle affiné pour votre tâche spécifique, quel niveau d'amélioration des performances doit atteindre pour que vous adoptiez ce nouveau modèle ? Et si un nouveau modèle de base ne surpasse pas immédiatement votre modèle actuel, mais a le potentiel de le faire après affinage, seriez-vous prêt à l'expérimenter ?

Dans de nombreux cas, le passage à un meilleur modèle n'apporterait qu'une petite amélioration marginale, et votre tâche pourrait se voir attribuer une priorité moindre que des projets plus rentables, comme l'activation de nouveaux cas d'utilisation. [2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1370)

Les expérimentations en ingénierie de l'IA doivent commencer par la génération d'invites, en suivant les bonnes pratiques décrites au [chapitre 6.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) N'explorez des solutions plus avancées que si la génération d'invites seule s'avère insuffisante. Assurez-vous d'avoir testé minutieusement différentes invites, car les performances d'un modèle peuvent varier considérablement selon les invites utilisées.

De nombreux praticiens avec lesquels j'ai discuté partagent une histoire similaire : quelqu'un se plaint de l'inefficacité des invites et insiste sur leur optimisation. Après enquête, il s'avère que les expérimentations sur les invites étaient minimales et non systématiques. Les instructions étaient imprécises, les exemples ne représentaient pas des données réelles et les indicateurs étaient mal définis. Après avoir affiné le processus d'expérimentation des invites, leur qualité s'est suffisamment améliorée pour convenir à leur application [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1371)

# Réglage fin des tâches spécifiques au domaine

Attention à l'argument selon lequel les modèles généralistes ne sont pas performants pour les tâches spécifiques à un domaine et qu'il est donc nécessaire de les affiner ou de les entraîner pour vos tâches spécifiques. À mesure que les modèles généralistes gagnent en puissance, ils deviennent également plus performants pour les tâches spécifiques à un domaine et peuvent surpasser les modèles dédiés.

BloombergGPT, lancé par Bloomberg en mars 2023, est un modèle spécialisé intéressant parmi les premiers à avoir été développé. À l'époque, les modèles les plus performants du marché étaient tous propriétaires, et Bloomberg recherchait un modèle de taille moyenne, efficace pour les tâches financières et pouvant être hébergé en interne pour les cas d'utilisation impliquant des données sensibles. Ce modèle, doté de 50 milliards de paramètres, a nécessité 1,3 million d'heures de calcul sur GPU A100 pour son entraînement. Le coût estimé de ce calcul se situait entre 1,3 et 2,6 millions de dollars, hors coûts liés aux données ( [Wu et al., 2023](https://arxiv.org/abs/2303.17564) ).

Le même mois, OpenAI a publié GPT-4-0314. [Une](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1374) étude de [Li et al. (2023)](https://arxiv.org/abs/2305.05862) a démontré que GPT-4-0314 surpassait largement BloombergGPT sur divers indicateurs financiers. [Le tableau 7-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07a_table_1_1730160615803945) présente le détail de deux de ces indicateurs.

Tableau 7-1. Les modèles à usage général comme GPT-4 peuvent surpasser les modèles financiers dans les domaines financiers .

|Modèle|Analyse des sentiments FiQA  <br>(F1 pondéré)|ConvFinQA  <br>(précision)|
|---|---|---|
|GPT-4-0314 (zéro-shot)|87,15|76,48|
|BloombergGPT|75,07|43.41|

Depuis, plusieurs modèles de taille moyenne aux performances comparables à celles de GPT-4 ont été publiés, notamment [Claude 3.5 Sonnet](https://oreil.ly/J-soV) (70 milliards de paramètres), [Llama 3-70B-Instruct](https://oreil.ly/6lt6-) et [Qwen2-72B-Instruct](https://oreil.ly/HZnfa) . Ces deux derniers sont à poids libre et peuvent être hébergés sur un serveur dédié.

Les benchmarks étant insuffisants pour refléter les performances réelles, il est possible que BloombergGPT soit performant pour Bloomberg dans ses cas d'utilisation spécifiques. L'équipe Bloomberg a certainement acquis une expérience précieuse grâce à l'entraînement de ce modèle, ce qui pourrait lui permettre de mieux développer et exploiter les modèles futurs.

L'optimisation fine et les expériences préliminaires nécessitent toutes deux des processus systématiques. La réalisation d'expériences préliminaires permet aux développeurs de mettre en place un processus d'évaluation, des directives d'annotation des données et des pratiques de suivi des expériences qui serviront d'étapes essentielles à l' optimisation fine.

Avant l'introduction de la mise en cache des invites, l'un des avantages du réglage fin était l'optimisation de l'utilisation des jetons. Plus on ajoute d'exemples à une invite, plus le modèle utilise de jetons d'entrée, ce qui augmente la latence et le coût. Au lieu d'inclure les exemples dans chaque invite, on peut régler finement un modèle sur ces exemples. Cela permet d'utiliser des invites plus courtes avec le modèle réglé finement, comme illustré dans [la figure 7-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07a_figure_2_1730160615799676) .

Grâce à la mise en cache des invites, qui permet de conserver les segments d'invites répétitifs pour les réutiliser, cet avantage est moins significatif. La mise en cache des invites est abordée plus en détail au [chapitre 9.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301) Toutefois, le nombre d'exemples utilisables avec une invite reste limité par la longueur maximale du contexte. Avec le réglage fin, ce nombre est illimité.

![Diagramme d'un modèle. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0702.png)

###### Figure 7-2. Au lieu d'inclure des exemples dans chaque invite, ce qui augmente le coût et la latence, vous affinez un modèle sur ces exemples.

## Réglage fin et RAG

Une fois les gains de performance obtenus grâce aux invites optimisés, vous vous demanderez peut-être s'il convient ensuite de procéder à une analyse RAG ou à un réglage fin. La réponse dépend de la nature des défaillances de votre modèle : sont-elles liées à des problèmes d'information ou de comportement ?

_Si le modèle échoue par manque d'informations, un système RAG (Réponse, Agilité, Importance) lui donnant accès aux sources d'information pertinentes peut s'avérer utile_ . Les défaillances liées à un manque d'informations surviennent lorsque les résultats sont factuellement erronés ou obsolètes. Voici deux exemples de scénarios où ce type de défaillance se produit :

Le modèle ne dispose pas de ces informations.

Les modèles publics ne possèdent généralement pas d'informations vous concernant ou concernant votre organisation. Lorsqu'un modèle ne dispose pas de l'information, il vous le signale ou fournit une réponse fictive.

Le modèle contient des informations obsolètes.

Si vous demandez : « Combien d'albums studio Taylor Swift a-t-elle sortis ? » et que la réponse correcte est 11, mais que le modèle répond 10, cela peut être dû au fait que la date limite de référence du modèle était antérieure à la sortie du dernier album.

L'article [« Fine-Tuning or Retrieval? »](https://oreil.ly/t9HTH) d'Ovadia et al. (2024) a démontré que pour les tâches nécessitant des informations actualisées, comme les questions sur l'actualité, le modèle RAG était plus performant que les modèles affinés. De plus, le modèle RAG de base était plus performant que les modèles affinés, comme le montre le [tableau 7-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07a_table_2_1730160615803962) . Ce résultat indique que _si l'affinage peut améliorer les performances d'un modèle pour une tâche spécifique, il peut aussi entraîner une baisse de performance dans d'autres domaines._

Tableau 7-2. RAG surpasse le finetuning sur une tâche de questions-réponses sur des événements d'actualité, sélectionnée par Ovadia et al. (2024). FT-reg et FT-par font référence à deux approches de finetuning différentes utilisées par l'auteur.


|            | Modèle de base | Modèle de base + RAG | FT-reg | FT-par | FT-reg + RAG | FT-par + RAG |
| ---------- | -------------- | -------------------- | ------ | ------ | ------------ | ------------ |
| Mistral-7B | 0,481          | 0,875                | 0,504  | 0,588  | 0,810        | 0,830        |
| Lama 2-7B  | 0,353          | 0,585                | 0,219  | 0,392  | 0,326        | 0,520        |
| Orque 2-7B | 0,456          | 0,876                | 0,511  | 0,566  | 0,820        | 0,826        |

En revanche, _si le modèle présente des problèmes de comportement, un réglage fin peut s'avérer utile_ . Un de ces problèmes survient lorsque les résultats du modèle sont factuellement corrects, mais non pertinents pour la tâche. Par exemple, vous demandez au modèle de générer des spécifications techniques pour un projet logiciel à destination de vos équipes d'ingénierie. Bien que précises, ces spécifications manquent de détails. Un réglage fin du modèle à l'aide de spécifications techniques bien définies peut rendre les résultats plus pertinents.

Un autre problème survient lorsque le format de sortie attendu n'est pas respecté. Par exemple, si vous avez demandé au modèle de générer du code HTML, mais que ce code ne compile pas, cela peut être dû à une exposition insuffisante du modèle au HTML dans ses données d'entraînement. Vous pouvez corriger ce problème en exposant davantage le modèle au code HTML lors de la phase d'ajustement.

L'analyse sémantique est une catégorie de tâches dont le succès repose sur la capacité du modèle à générer des sorties au format attendu et qui, par conséquent, nécessite souvent un paramétrage précis. L'analyse sémantique est brièvement abordée dans les chapitres [2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) et [6.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) Pour rappel, l'analyse sémantique consiste à convertir le langage naturel en un format structuré tel que JSON. Les modèles prêts à l'emploi performants conviennent généralement aux syntaxes courantes et relativement simples comme JSON, YAML et les expressions régulières. Cependant, ils peuvent s'avérer moins performants pour les syntaxes disposant de moins d'exemples sur Internet, comme un langage spécifique à un domaine pour un outil moins répandu ou une syntaxe complexe.

_En résumé, le réglage fin concerne la forme, tandis que le système RAG s'applique aux faits_ . Un système RAG intègre à votre modèle des connaissances externes pour construire des réponses plus précises et informatives.Un système RAG peut contribuer à atténuer les hallucinations de votre modèle. Le réglage fin, quant à lui, aide votre modèle à comprendre et à respecter les syntaxes et les styles.⁵ [Bien](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1377) que le réglage fin puisse potentiellement réduire les hallucinations s'il est effectué avec suffisamment de données de haute qualité, il peut également les aggraver si la qualité des données est faible.

Si votre modèle présente des problèmes d'information et de comportement, commencez par RAG. RAG est généralement plus simple car vous n'aurez pas à vous soucier de la curation des données d'entraînement ni de l'hébergement des modèles affinés. Avec RAG, privilégiez les solutions simples basées sur les termes, comme BM25, plutôt que de vous lancer directement dans une solution nécessitant des bases de données vectorielles.

RAG peut également apporter un gain de performance plus significatif que le finetuning. Ovadia et al. (2024) ont montré que pour presque toutes les catégories de questions du [benchmark MMLU](https://arxiv.org/abs/2009.03300) , RAG surpasse le finetuning pour trois modèles différents : Mistral 7B, Llama 2-7B et Orca 2-7B.

Cependant, RAG et le finetuning ne sont pas incompatibles. Ils peuvent parfois être utilisés conjointement pour optimiser les performances de votre application. Dans la même expérience, [Ovadia et al. (2024)](https://oreil.ly/t9HTH) ont montré que l'intégration de RAG à un modèle finement ajusté pouvait améliorer ses performances sur le benchmark MMLU dans 43 % des cas. Il est important de noter que, dans cette expérience, l'utilisation de RAG avec des modèles finement ajustés n'améliore pas les performances dans 57 % des cas, comparativement à l'utilisation de RAG seul.

Il n'existe pas de flux de travail universel pour toutes les applications. [La figure 7-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07a_figure_3_1730160615799691) illustre différents parcours possibles lors du développement d'une application. La flèche indique l'étape suivante à envisager. Cette figure s'inspire d'un exemple de flux de travail présenté par [OpenAI](https://oreil.ly/Ny1WI) (2023).

![Diagramme d'un processus. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0703.png)

###### Figure 7-3. Exemples de flux de développement d'applications. Après une recherche simple (telle qu'une recherche par terme), le choix d'expérimenter une recherche plus complexe (telle qu'une recherche hybride) ou un réglage fin dépend de chaque application et de ses modes de défaillance.

Le processus d'adaptation d'un modèle à une tâche pourrait donc se dérouler comme suit. Notez qu'avant toute étape d'adaptation, vous devez définir vos critères d'évaluation et concevoir votre pipeline d'évaluation, comme expliqué au [chapitre 4.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) Ce pipeline vous permettra de mesurer votre progression lors du développement de votre application. L'évaluation n'intervient pas uniquement au début ; elle doit être présente à chaque étape du processus.

1. Essayez de faire en sorte qu'un modèle exécute votre tâche uniquement à l'aide d'invites. Appliquez les bonnes pratiques d'ingénierie des invites présentées au [chapitre 5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) , notamment le versionnage systématique de vos invites.
    
2. Ajoutez davantage d'exemples à l'invite. Selon le cas d'utilisation, le nombre d'exemples nécessaires peut varier entre 1 et 50.
    
3. Si votre modèle échoue fréquemment par manque d'informations, connectez-le à des sources de données capables de fournir les informations pertinentes. Lorsque vous débutez avec RAG, commencez par utiliser des méthodes de recherche basiques comme la recherche par termes. Même avec une recherche simple, l'ajout de connaissances pertinentes et précises devrait améliorer les performances de votre modèle.
    
4. En fonction des modes de défaillance de votre modèle, vous pourriez envisager l'une des étapes suivantes :
    
    1. Si le modèle continue à présenter des échecs liés à l'information, vous pourriez essayer des méthodes RAG encore plus avancées, telles que la récupération basée sur l'intégration.
        
    2. Si le modèle présente toujours des problèmes de comportement, comme la génération de réponses non pertinentes, mal formatées ou non sécurisées, vous pouvez procéder à un réglage fin. La recherche basée sur l'intégration accroît la complexité de l'inférence en ajoutant des composants au processus, tandis que le réglage fin augmente la complexité du développement du modèle sans modifier l'inférence.
        
5. Combinez RAG et réglage fin pour obtenir des performances encore meilleures.
    

Si, après avoir pesé le pour et le contre du réglage fin et d'autres techniques alternatives, vous décidez de régler votre modèle avec précision, la suite de ce chapitre vous est destinée. Commençons par examiner le principal défi du réglage fin : sa limitation en termes de mémoire..

# Goulots d'étranglement de la mémoire

Le réglage fin étant gourmand en mémoire, de nombreuses techniques visent à minimiser leur empreinte mémoire. Comprendre les causes de cette limitation est essentiel pour saisir le fonctionnement de ces techniques. Cette compréhension vous permettra ensuite de choisir la méthode de réglage fin la plus adaptée à vos besoins.

Outre l'explication du goulot d'étranglement lié à la mémoire lors du réglage fin, cette section présente également des formules permettant d'estimer rapidement l'utilisation de la mémoire pour chaque modèle. Ce calcul est utile pour évaluer le matériel nécessaire au déploiement ou au réglage fin d'un modèle.

Le calcul de la mémoire nécessitant une explication détaillée des concepts de bas niveau en apprentissage automatique et en informatique, cette section est techniquement complexe. Si vous maîtrisez déjà ces concepts, vous pouvez la passer.

# Points clés pour comprendre les goulots d'étranglement de la mémoire

Si vous décidez de passer cette section, voici quelques points essentiels. Si certains de ces points vous sont inconnus, les concepts présentés dans cette section devraient vous éclairer.

1. En raison de la taille des modèles de base, la mémoire constitue un facteur limitant pour leur utilisation, tant pour l'inférence que pour l'ajustement fin. La mémoire nécessaire à l'ajustement fin est généralement bien supérieure à celle requise pour l'inférence, du fait du mode d'entraînement des réseaux de neurones.
    
2. Les principaux facteurs contribuant à l'empreinte mémoire d'un modèle lors de la mise au point sont son nombre de paramètres, son nombre de paramètres entraînables et ses représentations numériques.
    
3. Plus le nombre de paramètres entraînables est élevé, plus l'empreinte mémoire est importante. On peut réduire les besoins en mémoire pour le réglage fin en diminuant le nombre de paramètres entraînables. C'est précisément le principe du PEFT (parameter-efficient finetuning).
    
4. La quantification consiste à convertir un modèle d'un format à haute résolution (plus de bits) vers un format à basse résolution (moins de bits). C'est une méthode simple et efficace pour réduire l'empreinte mémoire d'un modèle. Pour un modèle de 13 milliards de paramètres, l'utilisation du format FP32 implique 4 octets par poids, soit 52 Go pour l'ensemble des poids. En réduisant chaque valeur à seulement 2 octets, la mémoire nécessaire pour les poids du modèle diminue à 26 Go.
    
5. L'inférence est généralement effectuée en utilisant le moins de bits possible, tels que 16 bits, 8 bits et même 4 bits.
    
6. L'entraînement est plus sensible à la précision numérique ; il est donc plus difficile d'entraîner un modèle avec une précision faible. L'entraînement se fait généralement en précision mixte, certaines opérations étant effectuées en haute précision (par exemple, 32 bits) et d'autres en basse précision (par exemple, 16 bits ou 8 bits).
    

## Rétropropagation et paramètres entraînables

Un facteur déterminant de l'empreinte mémoire d'un modèle lors de l'ajustement fin est le nombre de ses _paramètres entraînables_ . Un paramètre entraînable est un paramètre pouvant être mis à jour pendant l'ajustement fin. Lors du pré-entraînement, tous les paramètres du modèle sont mis à jour. Lors de l'inférence, aucun paramètre n'est mis à jour. Lors de l'ajustement fin, certains ou tous les paramètres peuvent être mis à jour. Les paramètres qui restent inchangés sont appelés _paramètres gelés_ .

[La mémoire nécessaire pour chaque paramètre entraînable dépend de](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1382) la méthode d'entraînement du modèle. À l'heure actuelle, les réseaux de neurones sont généralement entraînés à l'aide d'un mécanisme appelé rétropropagation.⁶ _Avec_ la rétropropagation, chaque étape d'entraînement se compose de deux phases :[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1382)

1. Passage avant : le processus de calcul de la sortie à partir de l'entrée.
    
2. Passage en sens inverse : processus de mise à jour des poids du modèle à l’aide des signaux agrégés du passage en sens direct.
    

Lors de l'inférence, seule la passe avant est exécutée. Lors de l'entraînement, les deux passes sont exécutées. De manière générale, la passe arrière fonctionne comme suit :

1. Comparez la sortie calculée lors de la propagation avant à la sortie attendue (vérité terrain). Si elles diffèrent, le modèle a commis une erreur et les paramètres doivent être ajustés. La différence entre la sortie calculée et la sortie attendue est appelée la _perte_ .
    
2. Calculez la contribution de chaque paramètre entraînable à l'erreur. Cette valeur est appelée _gradient . Mathématiquement, les gradients sont calculés_ [en](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1383) dérivant la fonction de perte par rapport à chaque paramètre entraînable. Il existe une valeur de gradient par paramètre entraînable. Si un paramètre présente un gradient élevé, il contribue significativement à la perte et doit être ajusté davantage.
    
3. Ajustez les valeurs des paramètres entraînables en fonction de leur gradient. L'ampleur de ce réajustement, compte tenu de la valeur du gradient, est déterminée par l' _optimiseur_ . Parmi les optimiseurs courants, on trouve la descente de gradient stochastique (SGD) et Adam. Pour les modèles basés sur les transformeurs, Adam est de loin l'optimiseur le plus utilisé.
    

La propagation avant et arrière d'un réseau neuronal hypothétique à trois paramètres et une fonction d'activation non linéaire est visualisée dans [la figure 7-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_1_1730159634220258) . J'utilise ce réseau neuronal fictif pour simplifier la visualisation.

![Diagramme de flux : description générée automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0704.png)

###### Figure 7-4. Le passage avant et arrière d'un réseau neuronal simple.

Lors de la rétropropagation, chaque paramètre entraînable est associé à des valeurs supplémentaires, son gradient et les états de son optimiseur. Par conséquent, plus le nombre de paramètres entraînables est élevé, plus la mémoire nécessaire pour stocker ces valeurs supplémentaires est importante.

## Mathématiques de la mémoire

Il est utile de connaître la quantité de mémoire requise par un modèle afin d'utiliser le matériel adéquat. Souvent, vous possédez déjà le matériel et devez calculer si vous pouvez vous permettre d'exécuter un modèle donné. Si un modèle nécessite 30 Go de mémoire pour effectuer l'inférence, une puce dotée de 24 Go de mémoire sera insuffisante.

L'empreinte mémoire d'un modèle dépend du modèle lui-même, de la charge de travail et des différentes techniques d'optimisation utilisées pour réduire sa consommation de mémoire. Comme il est impossible de prendre en compte toutes les techniques d'optimisation et toutes les charges de travail, cette section ne présentera que les formules de calcul approximatives, qui vous donneront une idée générale de la quantité de mémoire nécessaire au fonctionnement d'un modèle, aussi bien pendant l'inférence que pendant l'entraînement.

###### Note

L'inférence et l'entraînement ayant des profils de mémoire distincts est l'une des raisons de la divergence des puces pour l'entraînement et l'inférence, comme discuté au [chapitre 9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301) .

### Mémoire nécessaire à l'inférence

Lors de l'inférence, seule la propagation avant est exécutée. Cette propagation nécessite de la mémoire pour les poids du modèle. Soit N le nombre de paramètres du modèle et M la mémoire nécessaire pour chaque paramètre ; la mémoire nécessaire pour charger les paramètres du modèle est :

N × M

La transmission avant nécessite également de la mémoire pour les valeurs d'activation.Les modèles Transformer nécessitent de la mémoire pour stocker les vecteurs clé-valeur nécessaires au mécanisme d'attention. La mémoire requise, tant pour les valeurs d'activation que pour les vecteurs clé-valeur, croît linéairement avec la longueur de la séquence et la taille du lot.

Pour de nombreuses applications, on peut considérer que la mémoire allouée aux vecteurs d'activation et de paires clé-valeur représente 20 % de la mémoire utilisée pour les poids du modèle. Si votre application utilise un contexte plus long ou une taille de lot plus importante, la mémoire réellement nécessaire sera supérieure. Cette hypothèse ramène l'empreinte mémoire du modèle à :

N × M × 1,2

Considérons un modèle à 13 milliards de paramètres. Si chaque paramètre nécessite 2 octets, les poids du modèle nécessiteront 13 milliards × 2 octets = 26 Go. La mémoire totale requise pour l'inférence sera donc de 26 Go × 1,2 = 31,2 Go.

L'empreinte mémoire d'un modèle augmente rapidement avec sa taille. Plus les modèles sont volumineux, plus la mémoire devient un facteur limitant pour leur fonctionnement. [Un modèle de 70](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1389) [milliards](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1390) de paramètres, avec 2 octets par paramètre, nécessitera la somme colossale de 140 Go de mémoire rien que pour ses poids.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1390)

### Mémoire nécessaire à l'entraînement

Pour entraîner un modèle, il faut de la mémoire pour ses poids et ses activations, comme nous l'avons déjà évoqué. De plus, il faut de la mémoire pour les gradients et les états de l'optimiseur, dont la taille augmente avec le nombre de paramètres entraînables.

Globalement, la mémoire nécessaire à l'entraînement est calculée comme suit :

- Mémoire d'entraînement = poids du modèle + activations + gradients + états de l'optimiseur
    

###### Conseil

Lors de la rétropropagation, chaque paramètre entraînable nécessite une valeur pour le gradient plus zéro à deux valeurs pour les états de l'optimiseur, selon l'optimiseur :

- Un optimiseur SGD de base n'a pas d'état.
    
- Un optimiseur de momentum stocke une valeur par paramètre entraînable.
    
- Un optimiseur Adam stocke deux valeurs par paramètre entraînable.
    

Imaginez que vous mettez à jour tous les paramètres d'un modèle à 13 milliards de paramètres à l'aide de l'optimiseur Adam. Chaque paramètre entraînable possédant trois valeurs pour son gradient et l'état de l'optimiseur, et si chaque valeur occupe deux octets, la mémoire nécessaire pour les gradients et l'état de l'optimiseur sera de :

13 milliards × 3 × 2 octets = 78 Go

Cependant, si vous ne disposez que de 1 milliard de paramètres entraînables, la mémoire nécessaire pour les gradients et les états de l'optimiseur ne sera que de :

1 milliard × 3 × 2 octets = 6 Go

Il est important de noter que, dans la formule précédente, j'ai supposé que la mémoire nécessaire aux activations était inférieure à celle requise pour les poids du modèle. Or, en réalité, la mémoire requise pour les activations peut être bien plus importante. Si les activations sont stockées pour le calcul du gradient, la mémoire nécessaire peut largement dépasser celle requise pour les poids du modèle. [La figure 7-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_2_1730159634220278) illustre la mémoire requise pour les activations comparée à celle requise pour les poids du modèle pour différents modèles Megatron à différentes échelles, d'après l'article [« Reducing Activation Recomputation in Large Transformer Models »](https://arxiv.org/abs/2205.05198) de Korthikanti et al. (2022).

Une façon de réduire la mémoire nécessaire aux activations consiste à ne pas les stocker. Au lieu de les conserver pour une réutilisation ultérieure, on les recalcule lorsque cela est nécessaire. Cette technique est appelée _point de contrôle du gradient_ ou _recalcul des activations_ . Bien que cela réduise les besoins en mémoire, le temps d'entraînement augmente en raison du recalcul..[10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1395)

![Graphique d'un graphique. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0705.png)

###### Figure 7-5. La mémoire nécessaire aux activations peut largement dépasser celle requise pour les poids du modèle. Image tirée de Korthikanti et al., 2022.

## Représentations numériques

Dans les calculs de mémoire effectués jusqu'à présent, j'ai supposé que chaque valeur occupait deux octets. La mémoire nécessaire pour représenter chaque valeur d'un modèle contribue directement à l'empreinte mémoire totale de ce modèle. Si l'on réduit de moitié la mémoire requise pour chaque valeur, la mémoire nécessaire aux poids du modèle est également réduite de moitié.

Avant d'aborder la question de la réduction de la mémoire nécessaire pour chaque valeur, il est utile de comprendre les représentations numériques. Dans les réseaux de neurones, les valeurs numériques sont traditionnellement représentées par [des nombres à virgule flottante](https://en.wikipedia.org/wiki/Floating-point_arithmetic) . La famille de formats à virgule flottante la plus courante est la famille FP, qui respecte la norme IEEE [754](https://en.wikipedia.org/wiki/IEEE_754) (Institute of Electrical and Electronics Engineers) relative à l'arithmétique à virgule flottante .

- Le format FP32 utilise 32 bits (4 octets) pour représenter un nombre à virgule flottante. Ce format est appelé simple précision.
    
- FP64 utilise 64 bits (8 octets) et est appelé double précision.
    
- FP16 utilise 16 bits (2 octets) et est appelé demi-précision.
    

Bien que le format FP64 soit encore utilisé dans de nombreux calculs (à l'heure actuelle, il s'agit du format par défaut pour NumPy et pandas), il est rarement employé dans les réseaux de neurones en raison de son empreinte mémoire. Les formats FP32 et FP16 sont plus courants. Parmi les autres formats à virgule flottante populaires dans les charges de travail d'IA, on trouve _BF16_ (BFloat16) et _TF32_ (TensorFloat-32). BF16 a été conçu par Google pour optimiser les performances d'IA sur [les](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1396) [TPU](https://oreil.ly/BGXtn) , tandis que TF32 a été conçu par NVIDIA pour [les GPU](https://oreil.ly/0pZgw) .[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1396)

Les nombres peuvent également être représentés sous forme d'entiers. Bien que moins courants que les formats à virgule flottante, les formats entiers gagnent en popularité. Les formats entiers courants sont INT8 (entiers 8 bits) et INT4 (entiers 4 bits) [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1397)

Chaque format de nombre à virgule flottante utilise généralement 1 bit pour représenter le signe du nombre, c'est-à-dire négatif ou positif. Les bits restants sont répartis entre _la plage_ et _la précision_ : [13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1398)

Gamme

Le nombre de bits de plage détermine l'étendue des valeurs que le format peut représenter. Plus il y a de bits, plus la plage est étendue. C'est comparable au fait d'avoir plus de chiffres, ce qui permet de représenter une plus grande variété de nombres.

Précision

Le nombre de bits de précision détermine la précision avec laquelle un nombre peut être représenté. Réduire le nombre de bits de précision diminue la précision du nombre. Par exemple, si vous convertissez 10,1234 dans un format ne prenant en charge que deux chiffres décimaux, cette valeur devient 10,12, ce qui est moins précis que la valeur d'origine.

[La figure 7-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_3_1730159634220288) présente différents formats de nombres à virgule flottante, ainsi que leur plage et leur précision en bits. [14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1401)

![Graphique avec chiffres et description textuelle généré automatiquement avec un niveau de confiance moyen](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0706.png)

###### Figure 7-6. Différents formats numériques avec leur plage et leur précision.

Les formats comportant plus de bits sont considérés comme _plus précis_ . Convertir un nombre d'un format haute précision vers un format basse précision (par exemple, de FP32 à FP16) revient à _réduire sa précision_ . Une réduction de la précision peut entraîner une modification de la valeur ou des erreurs. [Le tableau 7-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_table_1_1730159634233580) illustre la conversion des valeurs FP32 vers FP16, BF16 et TF32.

Tableau 7-3. Conversion des valeurs FP32 en formats de précision inférieure. Les imprécisions résultantes sont indiquées en italique.

|FP32|FP16|BF16|TF32|
|---|---|---|---|
|0,0123456789|0,01234 _43603515625_|0,0123 _291_|0,01234 _43603515625_|
|0,123456789|0,1234 _7412109375_|0,123 _535_|0,1234 _130859375_|
|1,23456789|1 234 _375_|1.234 _38_|1 234 _375_|
|12,3456789|12,34 _375_|12,3 _75_|12,34 _375_|
|123,456789|123,4 _375_|123. _5_|123,4 _375_|
|1234,56789|123 _5.0_|123 _2.0_|1234. _0_|
|12345,6789|1234 _4.0_|123 _52.0_|1234 _4.0_|
|123456.789|_INF_ [a](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1402)|123 _392,0_|123456. _0_|
|1234567,89|_INF_|123 _6990.0_|123 _3920.0_|
|[un](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1402-marker)Les valeurs hors limites en FP16 sont arrondies à l'infini.|   |   |   |

Notez dans [le tableau 7-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_table_1_1730159634233580) que, bien que les formats BF16 et FP16 possèdent le même nombre de bits, BF16 dispose de plus de bits pour la plage et de moins de bits pour la précision. Cela permet à BF16 de représenter des valeurs élevées qui ne sont pas prises en compte par FP16. Cependant, cela rend également BF16 moins précis que FP16. Par exemple, 1234,56789 correspond à 1235,0 en FP16 (variation de 0,035 %) mais à 1232,0 en BF16 (variation de 0,208 %).

###### Avertissement

Lors de l'utilisation d'un modèle, assurez-vous de le charger dans le format prévu à cet effet. Charger un modèle dans un format numérique incorrect peut entraîner des modifications importantes. Par exemple, les poids de Llama 2 étaient initialement définis sur BF16. Cependant, de nombreuses équipes ont chargé le modèle au format FP16 et ont ensuite constaté avec déception que sa qualité était bien inférieure à celle annoncée.. [15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1404) Bien que ce malentendu ait fait perdre du temps à beaucoup de gens, le point positif est qu'il a forcé beaucoup de gens à apprendre les représentations numériques.

Le format le plus adapté à vos besoins dépend de la distribution des valeurs numériques de votre charge de travail (notamment la plage de valeurs requise), de la sensibilité de votre charge de travail aux petites variations numériques et du matériel sous-jacent. [16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1405)

## Quantification

Moins il faut de bits pour représenter les valeurs d'un modèle, plus son empreinte mémoire est réduite. Un modèle à 10 milliards de paramètres au format 32 bits nécessite 40 Go pour ses poids, tandis que le même modèle au format 16 bits n'en nécessite que 20 Go. La réduction de la précision, également appelée quantification, est une méthode économique et extrêmement efficace pour réduire l'empreinte mémoire d'un modèle. Elle est simple à mettre en œuvre et s'applique à différentes tâches et architectures. En apprentissage automatique, la faible précision désigne généralement tout format utilisant moins de bits que la norme FP32.

# Quantification versus précision réduite

À proprement parler, on parle de quantification uniquement si le format cible est un entier. Cependant, en pratique, le terme « quantification » désigne toutes les techniques de conversion de valeurs vers un format de précision inférieure. Dans cet ouvrage, j’utilise le terme « quantification » pour désigner la réduction de précision, par souci de cohérence avec la littérature existante.

Pour effectuer une quantification, il faut décider quoi quantifier et quand :

Que quantifier

Idéalement, il faudrait quantifier ce qui consomme le plus de mémoire, mais cela dépend aussi de ce qui peut être quantifié sans trop impacter les performances. Comme expliqué dans [« Calculs de la mémoire »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_memory_math_1730159634259402) , les principaux contributeurs à l'empreinte mémoire d'un modèle lors de l'inférence sont ses poids et ses activations. La quantification des [poids](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1406) est plus courante que celle des activations, car l'activation des poids a généralement un impact plus stable sur les performances, avec une perte de précision moindre.

Quand quantifier

La quantification peut intervenir pendant ou après l'entraînement. La quantification post-entraînement (QPE) consiste à quantifier un modèle une fois son entraînement terminé. La QPE est de loin la plus courante. Elle est également plus pertinente pour les développeurs d'applications d'IA qui, généralement, n'entraînent pas les modèles.

### quantification de l'inférence

Aux débuts de l'apprentissage profond, il était courant d'entraîner et de déployer des modèles en utilisant 32 bits avec FP32. Depuis la fin des années 2010, le déploiement de modèles en 16 bits, voire avec une précision moindre, s'est largement répandu. Par exemple, [Dettmers et al. (2022)](https://arxiv.org/abs/2208.07339) ont réalisé un excellent travail en quantifiant les LLM sur 8 bits avec LLM.int8() et sur 4 bits avec QLoRA ( [Dettmers et al., 2023](https://arxiv.org/abs/2305.14314) ).

Un modèle peut également être servi en _précision mixte_ , où la précision des valeurs est réduite lorsque cela est possible et maintenue à une précision plus élevée lorsque nécessaire. Pour servir des modèles sur ses appareils, [Apple](https://oreil.ly/lqLfv) (2024) a utilisé un système de quantification combinant les formats 2 bits et 4 bits, avec une moyenne de 3,5 bits par poids. Toujours en 2024, en prévision des réseaux neuronaux 4 bits, NVIDIA a annoncé sa nouvelle architecture GPU, [Blackwell](https://oreil.ly/FIP9V) , qui prend en charge l'inférence de modèles en virgule flottante 4 bits.

Dès que l'on descend en dessous de 8 bits, la représentation numérique devient plus complexe. On peut conserver les valeurs des paramètres sous forme de nombres à virgule flottante en utilisant l'un des formats [minifloat](https://en.wikipedia.org/wiki/Minifloat) , tels que FP8 (8 bits) et FP4 (4 bits). [Le](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1407) plus souvent, cependant, les valeurs des paramètres sont converties en un format entier, tel que INT8 ou INT4.

La quantification est efficace, mais elle a ses limites. On ne peut pas avoir moins d'un bit par valeur, et certains ont tenté une représentation sur un bit, par exemple BinaryConnect ( [Courbariaux et al., 2015](https://arxiv.org/abs/1511.00363) ), Xnor-Net ( [Rastegari et al., 2016](https://arxiv.org/abs/1603.05279) ) et BitNet ( [Wang et al., 2023](https://arxiv.org/abs/2310.11453) ). [19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1408)

En 2024, des chercheurs de Microsoft ( [Ma et al.](https://arxiv.org/abs/2402.17764) ) ont annoncé l'entrée dans l'ère des modèles de langage à 1 bit avec l'introduction de BitNet b1.58, un modèle de langage basé sur les transformeurs qui ne nécessite que 1,58 bit par paramètre et dont les performances sont comparables à celles des modèles à 16 bits.Llama 2 ( [Touvron et al., 2023](https://arxiv.org/abs/2307.09288) ) jusqu'à 3,9 milliards de paramètres, comme indiqué dans [le tableau 7-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_table_2_1730159634233604) .

Tableau 7-4. Performances de BitNet b1.58 comparées à celles de Llama 2 16 bits sur différents benchmarks et pour différentes tailles de modèle, jusqu'à 3,9 milliards de paramètres. Résultats de Ma et al. (2024).

|Modèle|Taille|ARCe|ARCc|HS|BQ|OQ|PQ|WGe|Moyenne|
|---|---|---|---|---|---|---|---|---|---|
|Llama LLM|700 m|54,7|23.0|37.0|60,0|20.2|68,9|54,8|45,5|
|BitNet b1.58|700 m|51,8|21.4|35.1|58.2|20.0|68.1|55.2|44,3|
|Llama LLM|1,3B|56,9|23,5|38,5|59.1|21.6|70,0|53,9|46.2|
|BitNet b1.58|1,3B|54,9|24.2|37,7|56,7|19.6|68,8|55,8|45.4|
|Llama LLM|3B|62.1|25.6|43,3|61,8|24.6|72.1|58.2|49,7|
|BitNet b1.58|3B|61,4|28.3|42,9|61,5|26.6|71,5|59,3|50,2|
|BitNet b1.58|3,9B|64.2|28.7|44.2|63,5|24.2|73,2|60,5|51.2|

Une précision réduite diminue non seulement l'empreinte mémoire, mais améliore souvent aussi la vitesse de calcul. Premièrement, elle autorise une taille de lot plus importante, permettant au modèle de traiter davantage d'entrées en parallèle. Deuxièmement, une précision réduite accélère le calcul, ce qui réduit encore la latence d'inférence et le temps d'entraînement. Pour illustrer cela, prenons l'exemple de l'addition de deux nombres. Si nous effectuons l'addition bit à bit, chaque bit prenant _t_ nanosecondes, il faudra _32t_ nanosecondes pour 32 bits, mais seulement _16t_ nanosecondes pour 16 bits. Cependant, réduire la précision ne réduit pas toujours la latence en raison du calcul supplémentaire nécessaire à la conversion de format.

La réduction de la précision présente des inconvénients. Chaque conversion entraîne souvent une légère modification de la valeur, et de nombreuses petites modifications peuvent engendrer une baisse significative des performances. Si une valeur se situe en dehors de la plage de valeurs que le format de précision réduite peut représenter, elle risque d'être convertie en l'infini ou en une valeur arbitraire, ce qui dégrade davantage la qualité du modèle. La réduction de la précision avec un impact minimal sur les performances du modèle fait l'objet de recherches actives, menées aussi bien par les développeurs de modèles que par les fabricants de matériel et les développeurs d'applications.

L'inférence en faible précision est devenue la norme. Un modèle est entraîné avec un format de haute précision pour optimiser ses performances, puis sa précision est réduite pour l'inférence. Les principaux frameworks d'apprentissage automatique, tels que PyTorch, TensorFlow et les transformateurs de Hugging Face, proposent l'inférence en faible précision (PTQ) gratuitement, en quelques lignes de code.

Certains périphériques ne prennent en charge que l'inférence quantifiée. Par conséquent, les frameworks d'inférence embarqués, tels que TensorFlow Lite et PyTorch Mobile, proposent également PTQ.

### quantification de l'entraînement

La quantification pendant l'entraînement n'est pas encore aussi courante que la quantification pendant l'entraînement (PTQ), mais elle gagne du terrain. La quantification pendant l'entraînement poursuit deux objectifs distincts :

1. L'objectif est de produire un modèle performant même avec une faible précision lors de l'inférence. Il s'agit de pallier le problème de la dégradation potentielle de la qualité d'un modèle lors de la quantification post-entraînement.
    
2. Pour réduire le temps et le coût d'entraînement, la quantification diminue l'empreinte mémoire d'un modèle, permettant ainsi son entraînement sur du matériel moins coûteux ou l'entraînement d'un modèle plus complexe sur le même matériel. La quantification accélère également les calculs, ce qui réduit encore les coûts.
    

Une technique de quantification pourrait permettre d'atteindre l'un ou l'autre de ces objectifs, voire les deux.

L'entraînement prenant en compte la quantification (QAT) vise à créer un modèle performant en faible précision pour l'inférence. Grâce au QAT, le modèle simule un comportement en faible précision (par exemple, 8 bits) pendant l'entraînement, ce qui lui permet d'apprendre à produire des résultats de haute qualité malgré une faible précision. Cependant, le QAT ne réduit pas le temps d'entraînement du modèle, car ses calculs sont toujours effectués en haute précision. Le QAT peut même l'augmenter en raison du travail supplémentaire que représente la simulation d'un comportement en faible précision.

En revanche, entraîner un modèle directement avec une précision réduite peut contribuer à atteindre les deux objectifs. Des tentatives d'entraînement de modèles avec une précision réduite ont été menées dès 2016 ; voir [Hubara et al. (2016)](https://oreil.ly/D-wIG) et [Jacob et al. (2017)](https://arxiv.org/abs/1712.05877) . [Character.AI (2024)](https://oreil.ly/J7kVB) a indiqué avoir réussi à entraîner ses modèles entièrement en INT8, ce qui a permis d'éliminer le décalage entre la précision d'entraînement et la précision de rendu, tout en améliorant considérablement l'efficacité de l'entraînement [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1415) Cependant , l'entraînement avec une précision réduite est plus complexe, car la rétropropagation est plus sensible à ce type de précision.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1415)

L'entraînement à faible précision est souvent réalisé en [_précision mixte_](https://oreil.ly/pBaQM) , où une copie des poids est conservée en haute précision tandis que d'autres valeurs, comme les gradients et les activations, sont conservées en basse précision. [<sup>21</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1416) Il est également possible de calculer les valeurs de poids les moins sensibles en basse précision et les plus sensibles en haute précision. Par exemple, LLM-QAT ( [Liu et al., 2023](https://arxiv.org/abs/2305.17888) ) quantifie les poids et les activations sur 4 bits, mais conserve les plongements sur 16 bits.

Les parties du modèle qui doivent être moins précises peuvent être définies automatiquement grâce à la [_précision mixte automatique._](https://oreil.ly/JZRsd)(AMP) fonctionnalité offerte par de nombreux frameworks ML.

Il est également possible d'avoir différentes phases d'entraînement à différents niveaux de précision. Par exemple, un modèle peut être entraîné avec une précision élevée, puis affiné avec une précision moindre. C'est particulièrement courant pour les modèles de base, où l'équipe qui entraîne un modèle à partir de zéro peut être une organisation disposant de la puissance de calcul nécessaire pour un entraînement en haute précision. Une fois le modèle publié, les développeurs disposant de moins de ressources de calcul peuvent l'affiner avec une précision moindre.précision.

# Techniques de réglage fin

J'espère que la section précédente a clairement démontré pourquoi l'ajustement fin des modèles à grande échelle est si gourmand en mémoire. Plus cet ajustement est gourmand en mémoire, moins il est accessible. Les techniques permettant de réduire l'empreinte mémoire d'un modèle rendent l'ajustement fin plus accessible, permettant ainsi à un plus grand nombre de personnes d'adapter les modèles à leurs applications. Cette section se concentre sur les techniques d'ajustement fin économes en mémoire, et plus particulièrement sur l'ajustement fin optimisé des paramètres.

J'aborderai également la fusion de modèles, une approche intéressante mais plus expérimentale pour la création de modèles personnalisés. Bien que la fusion de modèles ne soit généralement pas considérée comme du réglage fin, je l'inclus dans cette section car elle est complémentaire. Le réglage fin adapte un modèle à des besoins spécifiques. La fusion de modèles combine plusieurs modèles, souvent des modèles réglés finement, dans le même but.

Bien que la combinaison de plusieurs modèles ne soit pas un concept nouveau, de nouveaux types de modèles et des techniques de réglage fin ont inspiré de nombreuses techniques créatives de fusion de modèles, ce qui rend cette section particulièrement intéressante à aborder.

## Réglage fin efficace des paramètres

Aux débuts du finetuning, les modèles étaient suffisamment petits pour permettre un finetuning complet. Cette approche est appelée _finetuning intégral_ . Dans le finetuning intégral, le nombre de paramètres entraînables est exactement égal au nombre de paramètres.

Le réglage fin complet peut ressembler à l'entraînement. La principale différence réside dans le fait que l'entraînement commence avec des poids de modèle aléatoires, tandis que le réglage fin commence avec des poids de modèle préalablement entraînés.

Comme expliqué dans [« Mathématiques de la mémoire »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_memory_math_1730159634259402) , plus le nombre de paramètres entraînables est élevé, plus la mémoire nécessaire est importante. Prenons l’exemple d’un modèle à 7 milliards de paramètres :

- Si vous utilisez un format 16 bits comme FP16, le chargement des poids du modèle à lui seul nécessite 14 Go de mémoire.
    
- L'optimisation complète de ce modèle avec l'optimiseur Adam, également au format 16 bits, nécessite 7B × 3 × 2 octets supplémentaires = 42 Go de mémoire.
    
- La mémoire totale nécessaire pour les poids, les gradients et les états de l'optimiseur du modèle est alors de 14 Go + 42 Go = 56 Go.
    

56 Go dépassent la capacité mémoire de la plupart des cartes graphiques grand public, qui sont généralement équipées de 12 à 24 Go de mémoire, les cartes graphiques haut de gamme offrant jusqu'à 48 Go. Et cette estimation de mémoire ne tient pas encore compte de la mémoire requise pour les activations.

###### Note

Pour adapter un modèle à un matériel donné, il est possible soit de réduire son empreinte mémoire, soit d'optimiser l'utilisation de la mémoire du matériel. Des techniques comme la quantification et PEFT contribuent à minimiser l'empreinte mémoire totale. Parmi les techniques visant à mieux exploiter la mémoire matérielle, on trouve _le déchargement du processeur_ . Au lieu de tenter d'adapter l'intégralité du modèle aux GPU, il est possible de décharger la mémoire excédentaire sur les CPU, comme l'a démontré DeepSpeed ​​( [Rasley et al., 2020](https://oreil.ly/Np1Hn) ).

Nous n'avons pas non plus abordé le fait que le finetuning complet, notamment le finetuning supervisé et le finetuning par préférences, nécessite généralement une grande quantité de données annotées de haute qualité, inaccessibles à la plupart des utilisateurs. En raison des exigences élevées en mémoire et en données du finetuning complet, _le finetuning partiel_ a émergé. Dans le finetuning partiel, seuls certains paramètres du modèle sont mis à jour. Par exemple, pour un modèle à dix couches, on peut figer les neuf premières et affiner uniquement la dernière, réduisant [ainsi](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1429) le nombre de paramètres entraînables à 10 % de celui du finetuning complet.

Bien que le réglage partiel permette de réduire l'empreinte mémoire, il est _gourmand en paramètres_ . En effet, il nécessite un grand nombre de paramètres entraînables pour atteindre des performances proches de celles du réglage complet. Une étude de [Houlsby et al. (2019)](https://arxiv.org/abs/1902.00751) montre qu'avec un modèle BERT de grande taille ( [Devlin et al., 2018](https://arxiv.org/abs/1810.04805) ), il faudrait mettre à jour environ 25 % des paramètres pour obtenir des performances comparables à celles du réglage complet sur le benchmark GLUE ( [Wang et al., 2018](https://arxiv.org/abs/1804.07461) ). [La figure 7-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_4_1730159634220299) illustre la courbe de performance du réglage partiel en fonction du nombre de paramètres entraînables.

![Graphique représentant plusieurs objets. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0707.png)

###### Figure 7-7. La courbe bleue montre qu'un réglage fin partiel nécessite de nombreux paramètres entraînables pour atteindre des performances comparables à celles d'un réglage fin complet. Image tirée de Houlsby et al. (2019).

Ceci soulève la question suivante : comment obtenir des performances proches de celles d'un réglage fin complet tout en utilisant un nombre considérablement réduit de paramètres entraînables ? Les techniques de réglage fin issues de cette recherche sont dites « efficaces en termes de paramètres ». Il n'existe pas de seuil précis qu'une méthode de réglage fin doit atteindre pour être considérée comme telle. Toutefois, de manière générale, une technique est considérée comme efficiente en termes de paramètres si elle permet d'obtenir des performances proches de celles d'un réglage fin complet tout en utilisant un nombre de paramètres entraînables plusieurs ordres de grandeur inférieur.

Le concept de PEFT (parameter-efficient finetuning) a été introduit par Houlsby et al. (2019). Ces auteurs ont démontré qu'en insérant judicieusement des paramètres supplémentaires dans le modèle, il est possible d'obtenir d'excellentes performances de finetuning avec un nombre réduit de paramètres entraînables. Ils ont inséré deux modules d'adaptation dans chaque bloc transformateur d'un modèle BERT, comme illustré dans [la figure 7-8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_5_1730159634220312) .

![Diagramme d'une couche - Description générée automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0708.png)

###### Figure 7-8. En insérant deux modules d'adaptation dans chaque couche transformeur d'un modèle BERT et en mettant à jour uniquement les adaptateurs, Houlsby et al. (2019) ont pu obtenir de fortes performances de réglage fin en utilisant un petit nombre de paramètres entraînables.

Lors de l'ajustement fin, les paramètres originaux du modèle sont restés inchangés ; seuls les adaptateurs ont été mis à jour. Le nombre de paramètres entraînables correspond au nombre de paramètres des adaptateurs. Sur le benchmark GLUE, les performances obtenues sont inférieures de 0,4 % à celles d'un ajustement fin complet, avec seulement 3 % du nombre de paramètres entraînables. La courbe orange de [la figure 7-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_4_1730159634220299) illustre l'écart de performance entre un ajustement fin complet et un ajustement fin réalisé avec différentes tailles d'adaptateurs.

Cependant, cette approche présente l'inconvénient d'accroître la latence d'inférence du modèle affiné. Les adaptateurs introduisent des couches supplémentaires, ce qui ajoute des étapes de calcul à la propagation avant et ralentit l'inférence.

PEFT permet un réglage fin sur du matériel plus abordable, le rendant accessible à un plus grand nombre de développeurs. Les méthodes PEFT sont généralement économes en paramètres et en échantillons. Alors qu'un réglage fin complet peut nécessiter des dizaines de milliers, voire des millions d'exemples pour obtenir des améliorations de qualité notables, certaines méthodes PEFT offrent d'excellentes performances avec seulement quelques milliers d'exemples.

Compte tenu de l'attrait évident de la PEFT, les techniques PEFT se développent rapidement. La section suivante présentera un aperçu de ces techniques avant d'aborder plus en détail la technique PEFT la plus courante : la LoRA.

### Techniques PEFT

Le vaste univers actuel du PEFT se divise généralement en deux catégories : _les méthodes basées sur des adaptateurs_ et _les méthodes basées sur des invites souples_ . Toutefois, il est probable que de nouvelles catégories apparaissent à l’avenir.

_Les méthodes basées sur des adaptateurs_ désignent toutes les méthodes qui ajoutent des modules aux poids du modèle, comme celle développée par [Houlsby et al. (2019)](https://arxiv.org/abs/1902.00751) . Du fait de l'ajout de paramètres, elles sont également appelées _méthodes additives_ .

À l'heure actuelle, LoRA ( [Hu et al., 2021](https://arxiv.org/abs/2106.09685) ) est de loin la méthode basée sur des adaptateurs la plus populaire et fera l'objet de la section suivante. Parmi les autres méthodes basées sur des adaptateurs, on peut citer BitFit ( [Zaken et al., 2021](https://arxiv.org/abs/2106.10199) ), apparue à peu près en même temps que LoRA. Plus récemment, IA3 ( [Liu et al., 2022](https://oreil.ly/avDPk) ) se distingue par sa stratégie de traitement par lots efficace pour les tâches mixtes, ce qui la rend particulièrement intéressante pour l'ajustement fin multitâche. Elle a démontré sa supériorité par rapport à LoRA, voire même à l'ajustement fin complet dans certains cas. LongLoRA ( [Chen et al., 2023](https://arxiv.org/abs/2309.12307) ) est une variante de LoRA qui intègre des techniques de modification de l'attention afin d'étendre la longueur du contexte.

Si les méthodes basées sur des adaptateurs ajoutent des paramètres entraînables à l'architecture du modèle, les méthodes basées sur des incitations souples modifient la façon dont le modèle traite les entrées en introduisant des jetons entraînables spécifiques. Ces jetons supplémentaires sont fournis au modèle en même temps que les jetons d'entrée. On les appelle _incitations souples_ car, à l'instar des entrées (incitations strictes), elles guident également le comportement du modèle. Cependant, les incitations souples diffèrent des incitations strictes sur deux points :

- Les invites strictes sont lisibles par l'humain. Elles contiennent généralement des jetons _discrets_ tels que « je », « écrire », « un » et « beaucoup ». En revanche, les invites souples sont des vecteurs continus, semblables à des vecteurs d'intégration, et ne sont pas lisibles par l'humain.
    
- Les invites rigides sont statiques et non paramétrables, tandis que les invites souples peuvent être optimisées par rétropropagation lors du processus de réglage, ce qui permet de les adapter à des tâches spécifiques.
    

Certains décrivent l'incitation souple comme un compromis entre l'ingénierie des incitations et le réglage fin. [La figure 7-9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_6_1730159634220324) illustre comment utiliser conjointement des incitations souples et des incitations strictes pour orienter le comportement d'un modèle.

![Diagramme d'un modèle. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0709.png)

###### Figure 7-9. Les incitations dures et les incitations douces peuvent être combinées pour modifier les comportements d'un modèle.

Le réglage des invites souples, en tant que sous-domaine, se caractérise par une série de techniques aux noms similaires pouvant prêter à confusion, telles que le réglage préfixe ( [Li et Liang, 2021](https://arxiv.org/abs/2101.00190) ), le réglage P ( [Liu et al., 2021](https://arxiv.org/abs/2103.10385) ) et le réglage des invites ( [Lester et al., 2021](https://arxiv.org/abs/2104.08691) ) [.²³](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1431) Elles diffèrent principalement par l'emplacement d'insertion des invites souples. Par exemple, le réglage préfixe ajoute des invites souples au début de l'entrée à chaque couche du transformateur, tandis que le réglage des invites les ajoute uniquement à l'entrée intégrée. Si vous souhaitez utiliser l'une de ces techniques, de nombreux frameworks PEFT les implémentent nativement.

Pour mieux comprendre les méthodes PEFT utilisées, j'ai analysé plus de 1 000 problèmes ouverts sur le [dépôt GitHub huggingface/peft](https://github.com/huggingface/peft) en octobre 2024. Je pars du principe que les utilisateurs d'une technique donnée sont plus susceptibles de signaler des problèmes ou de poser des questions à son sujet. [La figure 7-10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_7_1730159634220334) présente les résultats. Concernant le « P-Tuning », j'ai recherché les mots-clés « p_tuning » et « p tuning » afin de tenir compte des différentes orthographes.

![Graphique d'un graphique avec des barres de différentes couleurs. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0710.png)

###### Figure 7-10. Nombre de problèmes associés aux différentes techniques de réglage fin du dépôt GitHub huggingface/peft. Ce nombre permet d'estimer la popularité de chaque technique.

Cette analyse montre clairement la domination de LoRA. Les invites souples sont moins courantes, mais on observe un intérêt croissant de la part de ceux qui souhaitent une personnalisation plus poussée que celle offerte par l'ingénierie des invites, sans pour autant vouloir investir dans un paramétrage fin.

Compte tenu de la popularité de LoRA, la section suivante explique son fonctionnement et comment il résout le problème posé par les méthodes basées sur les adaptateurs précoces. Même si vous n'utilisez pas LoRA, cette analyse approfondie vous permettra d'explorer d'autres méthodes de réglage fin.

### LoRA

Contrairement à la méthode d'adaptation originale de [Houlsby et al. (2019)](https://arxiv.org/abs/1902.00751) , LoRA (Low-Rank Adaptation) ( [Hu et al., 2021](https://arxiv.org/abs/2106.09685) ) intègre des paramètres supplémentaires sans augmenter la latence d'inférence. Au lieu d'ajouter des couches au modèle de base, LoRA utilise des modules qui peuvent être réintégrés aux couches d'origine.

Vous pouvez appliquer LoRA à des matrices de poids individuelles. Étant donné une matrice de poids, LoRA la décompose en le produit de deux matrices plus petites, puis met à jour ces deux matrices avant de les fusionner à nouveau avec la matrice d'origine.

Considérons la matrice de poids _W_ de dimension _n_ × _m_ . LoRA fonctionne comme suit :

1. Tout d'abord, choisissez la dimension des matrices les plus petites. Soit _r_ la valeur choisie. Construisez deux matrices : _A_ (dimension _n_ × _r_ ) et _B_ (dimension _r_ × _m_ ). Leur produit est _W =_ AB _,_ qui est de même dimension que _W._ _r_ est le _rang_ LoRA .
    
2. Ajoutez _W_ _<sub>AB</sub>_ à la matrice de poids initiale _W_ pour créer une nouvelle matrice de poids _W_ '. Utilisez _W_ ' à la place de _W_ dans le modèle. Vous pouvez utiliser un hyperparamètre α pour déterminer la contribution _de W<sub>_ _AB</sub>_ à la nouvelle matrice.â
    
3. Lors du réglage fin, mettez à jour uniquement les paramètres de _A_ et _B._ _W_ reste inchangé.
    

[La figure 7-11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_8_1730159634220345) visualise ce processus.

![Diagramme d'un diagramme. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0711.png)

###### Figure 7-11. Pour appliquer LoRA à une matrice de poids W, décomposez-la en le produit de deux matrices A et B. Lors de l'ajustement fin, seules A et B sont mises à jour. W reste inchangée.

###### Note

LoRA (Low-Rank Adaptation) repose sur le concept de _factorisation de faible rang_ , une technique de réduction de dimensionnalité éprouvée. L'idée principale est de factoriser une grande matrice en le produit de deux matrices plus petites afin de réduire le nombre de paramètres, et par conséquent les besoins en calcul et en mémoire. Par exemple, une `9 × 9`matrice peut être factorisée en le produit de deux matrices de dimensions `9 × 1`et `1 × 9`. La matrice originale possède 81 paramètres, tandis que les deux matrices produits n'en possèdent que 18 au total.

Le nombre de colonnes de la première matrice factorisée et celui de la seconde correspondent au rang de la factorisation. La matrice originale est _de rang maximal_ , tandis que les deux matrices plus petites représentent une approximation de rang inférieur.

Bien que la factorisation puisse réduire considérablement le nombre de paramètres, elle entraîne une perte d'information car elle n'approxime que la matrice originale. Plus le rang est élevé, plus la factorisation préserve d'informations de la matrice originale.

À l'instar de la méthode d'adaptation originale, LoRA est économe en paramètres et en échantillons. La factorisation permet à LoRA d'utiliser encore moins de paramètres entraînables. L'article sur LoRA a démontré que, pour GPT-3, LoRA atteint des performances comparables, voire supérieures, à celles obtenues avec un réglage fin complet sur plusieurs tâches, en utilisant seulement ~4,7 millions de paramètres entraînables, soit 0,0027 % du réglage fin complet.

#### Pourquoi LoRA fonctionne-t-il ?

Les méthodes à faible consommation de paramètres comme LoRa sont devenues si populaires que beaucoup les considèrent comme allant de soi. _Mais à quoi sert une telle efficacité paramétrique ?_ Si un modèle nécessite de nombreux paramètres pour apprendre certains comportements lors du pré-entraînement, ne devrait-il pas en nécessiter également beaucoup pour modifier ces comportements lors du fine-tuning ?

On peut se poser la même question concernant les données. Si un modèle nécessite une grande quantité de données pour apprendre un comportement, ne devrait-il pas en nécessiter également une grande quantité pour modifier significativement ce comportement ? Comment est-il possible d'avoir besoin de millions, voire de milliards d'exemples pour pré-entraîner un modèle, mais seulement de quelques centaines ou milliers pour l'affiner ?

De nombreux articles ont montré que, malgré leurs nombreux paramètres, les modèles linéaires à longue portée (LLM) présentent une dimension intrinsèque très faible ; voir [Li et al. (2018)](https://arxiv.org/abs/1804.08838) , [Aghajanyan et al. (2020)](https://arxiv.org/abs/2012.13255) et [Hu et al. (2021)](https://arxiv.org/abs/2106.09685) . Ils ont démontré que _le pré-entraînement minimise implicitement la dimension intrinsèque du modèle_ . De façon surprenante, les modèles plus grands tendent à avoir une dimension intrinsèque plus faible après pré-entraînement. Ceci suggère que le pré-entraînement agit comme un cadre de compression pour les tâches en aval. Autrement dit, plus un LLM est bien entraîné, plus il est facile de l'affiner à l'aide d'un petit nombre de paramètres entraînables et d'une petite quantité de données.

On pourrait se demander si, puisque la factorisation de faible rang est si performante, _on ne l'utilise pas également pour le pré-entraînement._ Au lieu de pré-entraîner un modèle complexe et d'appliquer la factorisation de faible rang uniquement lors de l'ajustement fin, ne pourrait-on pas factoriser le modèle dès le départ pour le pré-entraînement ? Le pré-entraînement par factorisation de faible rang permet de réduire considérablement le nombre de paramètres du modèle, et donc son temps et son coût.

Tout au long des années 2010, de nombreuses personnes ont essayé d'entraîner des réseaux neuronaux de faible rang, comme en témoignent des études telles que « Low-Rank Matrix Factorization for Deep Neural Network Training with High-Dimensional Output Targets » ( [Sainath et al., 2013](https://oreil.ly/xzdiG) ), « Semi-Orthogonal Low-Rank Matrix Factorization for Deep Neural Networks » ( [Povey et al., 2018](https://oreil.ly/LHLNz) ) et « Speeding up Convolutional Neural Networks with Low Rank Expansions » ( [Jaderberg et al., 2014](https://oreil.ly/BR63I) ).

La factorisation de faible rang s'est avérée efficace à petite échelle. Par exemple, en appliquant diverses stratégies de factorisation, notamment le remplacement de la convolution 3 × 3 par une convolution 1 × 1, SqueezeNet ( [Iandola et al., 2016](https://arxiv.org/abs/1602.07360) ) atteint une précision équivalente à celle d'AlexNet sur ImageNet avec 50 fois moins de paramètres.

Des tentatives plus récentes d'entraînement de modèles linéaires à faible rang incluent ReLoRA ( [Lialin et al., 2023](https://arxiv.org/abs/2307.05695) ) et GaLore ( [Zhao et al., 2024](https://arxiv.org/abs/2403.03507) ). ReLoRA fonctionne avec des modèles de type Transformer comportant jusqu'à 1,3 milliard de paramètres. GaLore atteint des performances comparables à celles d'un modèle de rang complet pour 1 milliard de paramètres et des performances prometteuses pour 7 milliards de paramètres.

Il est possible que, dans un avenir proche, les chercheurs parviennent à développer une méthode permettant d'étendre le pré-entraînement de faible rang à des centaines de milliards de paramètres. Cependant, si [l'argument d'Aghajanyan et al.](https://arxiv.org/abs/2012.13255) est correct — à savoir que le pré-entraînement compresse implicitement la dimension intrinsèque d'un modèle —, un pré-entraînement de rang complet reste nécessaire pour réduire suffisamment cette dimension intrinsèque et permettre ainsi l'utilisation d'une factorisation de faible rang. Il serait intéressant d'étudier précisément la quantité d'entraînement de rang complet requise avant de pouvoir passer à un entraînement de faible rang.

#### Configurations LoRA

Pour appliquer LoRA, il est nécessaire de déterminer les matrices de pondération auxquelles l'appliquer ainsi que le rang de chaque factorisation. Cette section détaille les éléments à prendre en compte pour chacune de ces décisions.

LoRA peut être appliqué à chaque matrice de poids individuelle. Son efficacité dépend donc non seulement des matrices auxquelles il est appliqué, mais aussi de l'architecture du modèle, car différentes architectures utilisent différentes matrices de poids.

Bien que l'algorithme LoRA ait été utilisé avec d'autres architectures, comme les réseaux de neurones convolutifs ( [Dutt et al., 2023](https://arxiv.org/abs/2305.08252) ; [Zhong et al., 2024](https://arxiv.org/abs/2401.17868) ; [Aleem et al., 2024](https://arxiv.org/abs/2402.04964) ), il a principalement été employé pour les modèles de type Transformer. <sup> [24](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1439) </sup> LoRA est généralement appliqué aux quatre matrices de poids des modules d'attention : les matrices de requête ( _W<sub>_ _q</sub>_ ), de clé ( _W<sub>_ _k</sub>_ ), de valeur ( _W<sub>_ _v_ </sub>) et de projection de sortie ( _W_ _<sub>o</sub>_ ).

En règle générale, l'algorithme LoRA est appliqué uniformément à toutes les matrices de même type au sein d'un modèle. Par exemple, appliquer LoRA à la matrice de requête revient à l'appliquer à toutes les matrices de requête du modèle.

En théorie, on pourrait appliquer LoRA à toutes ces matrices d'attention. Cependant, on est souvent limité par la mémoire du matériel et on ne peut gérer qu'un nombre fixe de paramètres entraînables. Avec un nombre limité de paramètres entraînables, à quelles matrices faut-il appliquer LoRA pour optimiser les performances ?

Lors de l'ajustement fin de GPT-3 175B, Hu et al. (2021) ont fixé leur budget de paramètres entraînables à 18 millions, soit 0,01 % du nombre total de paramètres du modèle. Ce budget leur permet d'appliquer LoRA aux éléments suivants :

1. Une matrice de rang 8
    
2. Deux matrices de rang 4
    
3. Les quatre matrices de rang 2
    

###### Note

GPT-3 175B possède 96 couches transformeuses avec une dimension de modèle de 12 288. L'application de LoRA avec rang = 2 aux quatre matrices donnerait (12 288 × 2 × 2) × 4 = 196 608 paramètres entraînables par couche, soit 18 874 368 paramètres entraînables pour l'ensemble du modèle.

Ils ont constaté que l'application de LoRA aux quatre matrices, avec un rang de 2, offre les meilleures performances sur les benchmarks WikiSQL ( [Zhong et al., 2017 ) et MultiNLI (Multi-Genre Natural Language Inference) (](https://arxiv.org/abs/1709.00103) [Williams et al., 2017](https://oreil.ly/mqHMU) ). [Le tableau 7-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_table_3_1730159634233616) présente leurs résultats. Cependant, les auteurs suggèrent que, si l'on ne peut choisir que deux matrices d'attention, les matrices de requête et de valeur donnent généralement les meilleurs résultats.

Tableau 7-5. Performances de LoRA avec un budget de 18 millions de paramètres entraînables. Résultats de LoRA (Hu et al., 2021).

|                   |Nombre de paramètres entraînables = 18M|   |   |   |   |   |   |
|---|---|---|---|---|---|---|---|
| Type de poids     |W q|W k|W v|W o|W q , W k|W q , W v|W q , W k , W v , W o|
| Rang r            |8|8|8|8|4|4|2|
| WikiSQL (± 0,5%)  |70,4|70,0|73,0|73,2|71,4|**73,7**|**73,7**|
| MultiNLI (± 0,1%) |91,0|90,8|91,0|91,3|91,3|91,3|**91,7**|

Les observations empiriques suggèrent que l'application de LoRA à un plus grand nombre de matrices de poids, y compris les matrices de propagation directe, donne de meilleurs résultats. Par exemple, Databricks a démontré que le gain de performance le plus important obtenu provenait de l'application de LoRA à toutes les couches de propagation directe ( [Sooriyarachchi, 2023](https://oreil.ly/zzREV) ). [Fomenko et al. (2024)](https://arxiv.org/html/2404.05086v1) ont noté que LoRA basé sur la propagation directe peut être complémentaire à LoRA basé sur l'attention, bien que ce dernier offre généralement une plus grande efficacité compte tenu des contraintes de mémoire.

L'avantage de LoRA est que, bien que ses performances dépendent de son rang, des études ont montré qu'un _petit rang (r), par exemple entre 4 et 64, est généralement suffisant pour de nombreux cas d'utilisation_ . Un _rang_ plus petit signifie moins de paramètres LoRA, ce qui se traduit par une empreinte mémoire réduite.

Les auteurs de LoRA ont constaté, à leur grande surprise, que l'augmentation de la valeur de _r_ n'améliore pas les performances du finetuning. Cette observation concorde avec le rapport de Databricks indiquant qu'« augmenter _r_ au-delà d'une certaine valeur peut ne pas entraîner d'amélioration perceptible de la qualité des résultats du modèle » (Sooriyarachchi, 2023).²⁵ [Certains](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1441) affirment qu'une valeur de _r_ trop élevée peut même être préjudiciable, car elle peut conduire à un surapprentissage. Cependant, dans certains cas, un rang plus élevé peut s'avérer nécessaire. [Raschka (2023)](https://oreil.ly/A-d5f) a constaté que _r_ = 256 offrait les meilleures performances pour ses tâches.

Un autre hyperparamètre LoRA que vous pouvez configurer est la valeurqui détermine la contribution du produit _W_ _AB_ à la nouvelle matrice lors de la fusion :âEn pratique, j'ai souvent vu ɑ choisi de sorte que le ratioLe rapport se situe généralement entre 1:8 et 8:1, mais le rapport optimal varie. Par exemple, si _r_ est petit, vous pourriez vouloirêtre plus grand, et si _r_ est grand, vous pourriez vouloirêtre plus petite. Des essais sont nécessaires pour déterminer la meilleure solution.combinaison adaptée à votre cas d'utilisation.

#### Adaptateurs LoRa de service

LoRa permet non seulement d'affiner les modèles en consommant moins de mémoire et de données, mais aussi de simplifier le déploiement de plusieurs modèles grâce à sa modularité. Pour comprendre cet avantage, examinons comment déployer un modèle affiné avec LoRa.

En général, il existe deux manières de servir un modèle LoRA affiné :

1. Fusionnez les poids LoRA _A_ et _B_ avec le modèle original pour créer la nouvelle matrice Wʹ avant de déployer le modèle affiné. Comme aucun calcul supplémentaire n'est effectué lors de l'inférence, aucune latence supplémentaire n'est ajoutée.
    
2. Pendant la diffusion, conservez _W_ , _A_ et _B_ séparés. La fusion de _A_ et _B_ en _W_ a lieu pendant l'inférence, ce qui engendre une latence supplémentaire.
    

La première option est généralement préférable si vous n'avez qu'un seul modèle LoRA à gérer, tandis que la seconde est généralement plus adaptée à _la gestion_ de plusieurs modèles LoRA partageant le même modèle de base. [La figure 7-12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_9_1730159634220354) illustre la gestion de plusieurs modèles LoRA lorsque les adaptateurs LoRA sont séparés.

![Diagramme de flux : description générée automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0712.png)

###### Figure 7-12. Le fait de garder les adaptateurs LoRA séparés permet la réutilisation de la même matrice de rang complet _W_ dans le service multi-LoRA.

Pour le déploiement multi-LoRa, bien que l'option 2 induise une latence supplémentaire, elle réduit considérablement l'espace de stockage nécessaire. Prenons l'exemple d'un modèle affiné pour chacun de vos clients utilisant LoRa. Avec 100 clients, vous obtenez 100 modèles affinés, partageant tous le même modèle de base. Avec l'option 1, vous devez stocker 100 matrices de rang maximal _W_ '. Avec l'option 2, vous n'avez besoin de stocker qu'une seule matrice de rang maximal _W_ et 100 ensembles de matrices plus petites ( _A_ , _B_ ).

Pour mettre cela en perspective, supposons que la matrice originale _W_ soit de dimension `4096 × 4096` (16,8 millions de paramètres). Si le rang de LoRA est 8, le nombre de paramètres dans _A_ et _B_ est`4096 × 8 × 2 = 65,536` :

- Dans l'option 1, 100 matrices de rang complet _W_ ʹ totalisent `16.8M × 100 = 1.68B`les paramètres.
    
- Dans l'option 2, une matrice de rang complet _W_ et 100 ensembles de petites matrices ( _A_ , _B_ ) totalisent : `16.8M + 65,536 × 100 = 23.3M`paramètres.
    

L'option 2 permet également de passer plus rapidement d'une tâche à l'autre. Supposons que vous utilisiez actuellement le modèle du client _X. Pour passer au client_ _Y_ , au lieu de charger la matrice de poids complète de X, il vous suffit de charger l'adaptateur LoRa de Y, ce qui réduit considérablement le temps de chargement. Bien que la séparation des modèles _A_ et _B_ engendre une latence supplémentaire, des techniques d'optimisation permettent de la minimiser. Le [dépôt GitHub du livre](https://github.com/chiphuyen/aie-book) contient une description détaillée de la procédure à suivre.

Le déploiement multi-LoRA facilite la combinaison de plusieurs modèles spécialisés. Au lieu d'un seul modèle puissant pour de multiples tâches, un adaptateur LoRA est dédié à chaque tâche. Par exemple, Apple a utilisé plusieurs [adaptateurs LoRA](https://oreil.ly/vfXqE) pour adapter le même modèle de base à 3 milliards de paramètres aux différentes fonctionnalités de l'iPhone (2024). L'entreprise a eu recours à des techniques de quantification pour réduire davantage l'empreinte mémoire de ce modèle de base et des adaptateurs, permettant ainsi leur déploiement sur l'appareil.

La modularité des adaptateurs LoRa permet leur partage et leur réutilisation. Des adaptateurs LoRa optimisés sont disponibles publiquement et peuvent être utilisés comme des modèles pré-entraînés. Vous les trouverez sur [Hugging Face](https://oreil.ly/T08JJ) [26](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1444) ou via des initiatives telles [qu'AdapterHub](https://adapterhub.ml/) .

Vous vous demandez peut-être : « LoRA semble prometteur, mais quel est le piège ? » Le principal inconvénient de LoRA est qu’il n’offre pas des performances aussi élevées qu’un réglage fin complet. Sa mise en œuvre est également plus complexe, car elle implique de modifier l’implémentation du modèle, ce qui requiert une bonne compréhension de son architecture et des compétences en programmation. Toutefois, ce problème ne se pose généralement que pour les modèles de base moins répandus. Les frameworks PEFT, tels que [PEFT de Hugging Face](https://github.com/huggingface/peft) , [Axolotl](https://github.com/axolotl-ai-cloud/axolotl) , [unsloth](https://github.com/unslothai/unsloth) et [LitGPT](https://github.com/Lightning-AI/litgpt) , prennent généralement en charge LoRA nativement pour les modèles de base populaires.

#### LoRA quantifié

L'essor rapide de LoRA a engendré le développement de nombreuses variantes. Certaines visent à réduire encore davantage le nombre de paramètres entraînables. Cependant, comme l'illustre le [tableau 7-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_table_4_1730159634233626) , la mémoire occupée par un adaptateur LoRA est minime comparée à celle des poids du modèle. Réduire le nombre de paramètres LoRA ne diminue donc que très légèrement l'empreinte mémoire globale.

Tableau 7-6. La mémoire nécessaire aux poids LoRA comparée à celle nécessaire aux poids du modèle.

|              |Mémoire des poids du modèle  <br>(16 bits)|Paramètres entraînables LoRA  <br>(r=2, matrices de requête et de clé)|mémoire de l'adaptateur LoRA  <br>(16 bits)|
|---|---|---|---|
| Lama 2 (13B) |26 Go|3,28 m|6,55 Mo|
| GPT-3 (175B) |350 Go|18,87 M|37,7 Mo|

Plutôt que de chercher à réduire le nombre de paramètres de LoRA, il est plus efficace de réduire l'utilisation de la mémoire en quantifiant les poids, les activations et/ou les gradients du modèle lors de l'ajustement fin. Une version quantifiée prometteuse de LoRA est QLoRA ( [Dettmers](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1447) [et al., 2023](https://arxiv.org/abs/2305.14314) ). Dans l'article original sur LoRA, les poids du modèle sont stockés sur 16 bits lors de l'ajustement fin. QLoRA les stocke sur 4 bits, mais les déquantifie (les reconvertit) en BF16 lors des calculs de propagation avant et arrière.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1447)

Le format 4 bits utilisé par QLoRA est NF4 (NormalFloat-4), qui quantifie les valeurs en se basant sur le fait que les poids pré-entraînés suivent généralement une distribution normale de médiane nulle. Outre cette quantification 4 bits, QLoRA utilise également des optimiseurs paginés pour transférer automatiquement les données entre le CPU et le GPU lorsque ce dernier manque de mémoire, notamment pour les séquences longues. Ces techniques permettent d'affiner un modèle à 65 milliards de paramètres sur un seul GPU de 48 Go.

Les auteurs ont optimisé divers modèles, dont Llama 7B à 65B, en mode 4 bits. La famille de modèles ainsi obtenue, appelée Guanaco, a démontré des performances compétitives sur les bancs d'essai publics et lors d'évaluations comparatives.[Le tableau 7-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_table_5_1730159634233637) présente les classements Elo des modèles Guanaco, GPT-4 et ChatGPT en mai 2023, selon GPT-4. Bien que Guanaco 65B n'ait pas surpassé GPT-4, il était souvent préféré à ChatGPT.

Tableau 7-7. Classements Elo des modèles Guanaco comparés à ceux des modèles populaires en mai 2023, avec GPT-4 comme juge. L'expérience provient de QLoRA (Dettmers et al., 2023).

|Modèle|Taille|Elo|
|---|---|---|
|GPT-4|-|1348 ± 1|
|Guanaco 65B|41 Go|1022 ± 1|
|Guanaco 33B|21 Go|992 ± 1|
|Vicuna 13B|26 Go|974 ± 1|
|ChatGPT|-|966 ± 1|
|Guanaco 13B|10 Go|916 ± 1|
|Barde|-|902 ± 1|
|Guanaco 7B|6 Go|879 ± 1|

La principale limitation de QLoRA réside dans le coût élevé de la quantification NF4. Bien que QLoRA permette de réduire l'empreinte mémoire, le temps d'entraînement peut s'en trouver allongé en raison du temps supplémentaire requis par les étapes de quantification et de déquantification.

Grâce à son potentiel d'économie de mémoire, le LoRA quantifié est un domaine de recherche actif. Outre le QLoRA, les travaux sur le LoRA quantifié incluent le QA-LoRA ( [Xu et al., 2023](https://arxiv.org/abs/2309.14717) ), le ModuLoRA ( [Yin et al., 2023](https://arxiv.org/abs/2309.16119) ) et l'IR-QLoRA ( [Qin et al., 2024](https://arxiv.org/abs/2402.05445) )..

## Fusion de modèles et réglage fin multitâche

Si le réglage fin permet de créer un modèle personnalisé en modifiant un seul modèle, la fusion de modèles permet d'en créer un en combinant plusieurs. La fusion de modèles offre une plus grande flexibilité que le simple réglage fin. Vous pouvez fusionner deux modèles existants pour créer un nouveau modèle, potentiellement plus utile. Vous pouvez également régler finement chacun des modèles constitutifs, ou tous, avant de les fusionner.

Bien qu'il ne soit pas nécessaire d'affiner davantage le modèle fusionné, ses performances peuvent souvent être améliorées par un réglage fin. Sans réglage fin, la fusion de modèles peut être effectuée sans GPU, ce qui la rend particulièrement intéressante pour les développeurs de modèles indépendants disposant de ressources de calcul limitées.

L'objectif de la fusion de modèles est de créer un modèle unique offrant une valeur ajoutée supérieure à celle de ses composants pris séparément. Cette valeur ajoutée peut provenir d'une amélioration des performances. Par exemple, si deux modèles excellent dans des domaines différents pour une même tâche, leur fusion en un seul modèle sera plus performant que chacun pris individuellement. Imaginons un modèle capable de répondre aux 60 % premières questions et un autre aux 60 % dernières. Combinés, ils pourraient répondre à 80 % des questions.

La valeur ajoutée peut également provenir d'une empreinte mémoire réduite, ce qui engendre des coûts moindres. Par exemple, si vous disposez de deux modèles capables d'effectuer des tâches différentes, vous pouvez les fusionner en un seul modèle capable de réaliser les deux tâches avec moins de paramètres. Cette approche est particulièrement intéressante pour les modèles basés sur des adaptateurs. À partir de deux modèles affinés sur un même modèle de base, vous pouvez combiner leurs adaptateurs en un seul.

L'un des cas d'utilisation importants de la fusion de modèles est l'optimisation multitâche. Sans fusion de modèles, si vous souhaitez optimiser un modèle pour plusieurs tâches, vous devez généralement suivre l'une de ces approches :

Réglage fin simultané

Vous créez un ensemble de données contenant des exemples pour toutes les tâches et vous affinez le modèle sur cet ensemble afin qu'il apprenne toutes les tâches simultanément. Cependant, comme il est généralement plus difficile d'acquérir plusieurs compétences en même temps, cette approche nécessite généralement davantage de données et un entraînement plus long.

Réglage fin séquentiel

Il est possible d'affiner le modèle pour chaque tâche séparément, mais de manière séquentielle. Après avoir entraîné un modèle sur la tâche A, entraînez-le sur la tâche B, et ainsi de suite. L'hypothèse sous-jacente est qu'il est plus facile pour les modèles d'apprendre une tâche à la fois. Malheureusement, les réseaux de neurones sont sujets à l'oubli catastrophique ( [Kirkpatrick et al., 2016](https://arxiv.org/abs/1612.00796) ). Un modèle peut oublier comment effectuer une tâche apprise précédemment lorsqu'il est entraîné sur une nouvelle tâche, ce qui entraîne une baisse significative de ses performances sur les tâches précédentes.

La fusion de modèles offre une autre méthode d'ajustement fin multitâche. Elle permet d'ajuster le modèle sur différentes tâches séparément, mais en parallèle. Une fois cette étape terminée, les différents modèles sont fusionnés. L'ajustement fin sur chaque tâche séparément permet au modèle d'apprendre plus efficacement cette tâche. L'absence d'apprentissage séquentiel réduit considérablement le risque d'oubli catastrophique.

La fusion de modèles est également intéressante lorsqu'il s'agit de déployer des modèles sur des appareils tels que des téléphones, des ordinateurs portables, des voitures, des montres connectées et des robots d'entrepôt. Le déploiement embarqué est souvent complexe en raison de la capacité de mémoire limitée des appareils. Au lieu de surcharger un appareil avec plusieurs modèles pour différentes tâches, il est possible de les fusionner en un seul modèle capable d'effectuer plusieurs tâches tout en nécessitant beaucoup moins de mémoire.

Le déploiement sur l'appareil est nécessaire dans les cas d'utilisation où les données ne peuvent pas quitter l'appareil (souvent pour des raisons de confidentialité), ou lorsque l'accès à Internet est limité ou peu fiable. Le déploiement sur l'appareil peut également réduire considérablement les coûts d'inférence. Plus vous déchargez de calculs sur les appareils des utilisateurs, moins vous payez les centres de données. [28](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1463)

La fusion de modèles est une méthode d' _apprentissage fédéré_ ( [McMahan et al., 2016](https://arxiv.org/abs/1602.05629) ) où plusieurs appareils entraînent le même modèle à l'aide de données distinctes. Par exemple, si vous déployez le modèle X sur plusieurs appareils, chaque instance de X peut continuer à apprendre indépendamment à partir des données de son propre appareil. Au bout d'un certain temps, vous disposez de plusieurs instances de X, chacune entraînée sur des données différentes. Vous pouvez alors fusionner ces instances en un nouveau modèle de base intégrant l'apprentissage de tous les modèles constitutifs.

L'idée de combiner des modèles pour obtenir de meilleures performances a émergé avec _les méthodes d'ensemble de modèles_ . Selon [Wikipédia](https://en.wikipedia.org/wiki/Ensemble_learning) , l'ensemble de modèles combine « plusieurs algorithmes d'apprentissage afin d'obtenir de meilleures performances prédictives que celles obtenues avec chacun des algorithmes pris individuellement ». Alors que la fusion de modèles implique généralement le mélange des paramètres des modèles constitutifs, l'ensemble de modèles combine généralement uniquement les sorties des modèles, en conservant l'intégrité de chaque modèle constitutif.

[Par exemple, dans le cadre d'un ensemble de modèles](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1465) , face à une requête donnée, trois modèles peuvent générer trois réponses différentes. Une réponse finale est ensuite générée à partir de ces trois réponses, soit par un vote majoritaire simple, soit par un autre module d'apprentissage automatique entraînable. Bien que l'ensemble de modèles puisse généralement améliorer les performances, son coût d'inférence est plus élevé car il nécessite plusieurs appels d'inférence par requête.

[La figure 7-13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_10_1730159634220361) compare l'assemblage et la fusion de modèles. À l'instar des ensembles de modèles qui dominaient autrefois les classements, de nombreux modèles en tête du [classement Open LLM de Hugging Face](https://oreil.ly/hRV9P) sont des modèles fusionnés.

![Diagramme d'un modèle. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0713.png)

###### Figure 7-13. Comment fonctionnent l'assemblage et la fusion de modèles.

De nombreuses techniques de fusion de modèles sont expérimentales et risquent de devenir obsolètes à mesure que la communauté approfondit sa compréhension de la théorie sous-jacente. C'est pourquoi je me concentrerai sur les approches de fusion de haut niveau plutôt que sur une technique particulière.

Les méthodes de fusion de modèles diffèrent par la manière dont les paramètres constitutifs sont combinés. Trois méthodes sont présentées ici : la sommation, l’empilement de couches et la concaténation. [La figure 7-14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_11_1730159634220368) illustre leurs principales différences.

![Schéma de briques de différentes couleurs. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0714.png)

###### Figure 7-14. Trois approches principales de fusion de modèles : sommation, empilement de couches et concaténation.

Il est possible de combiner ces approches lors de la fusion de modèles, par exemple en additionnant certaines couches et en empilant d'autres. Examinons chacune de ces approches.

### Somme

Cette approche consiste à additionner les pondérations des modèles constitutifs. J'aborderai deux méthodes de sommation : la combinaison linéaire et l'interpolation linéaire sphérique. Si les paramètres de deux modèles sont d'échelles différentes (par exemple, si les valeurs des paramètres d'un modèle sont beaucoup plus élevées que celles de l'autre), il est possible de les redimensionner avant la sommation afin que leurs valeurs de paramètres soient du même ordre de grandeur.

#### Combinaison linéaire

La combinaison linéaire comprend à la fois une moyenne et une moyenne pondérée. Étant donné deux modèles, A et B, leur moyenne pondérée est :

[La figure 7-15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_12_1730159634220376) montre comment combiner linéairement deux couches lorsque _w_ _A_ = _w_ _B_ = 1.

![Diagramme de cercles jaunes numérotés. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0715.png)

###### Figure 7-15. Fusion des paramètres par moyennage.

La combinaison linéaire fonctionne étonnamment bien, compte tenu de sa simplicité. [L'](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1466) idée que plusieurs modèles puissent être combinés linéairement pour en créer un meilleur a été étudiée dès le début des années 1990 ( [Perrone, 1993](https://oreil.ly/eXC02) ). La combinaison linéaire est fréquemment utilisée dans l'apprentissage fédéré ( [Wang et al., 2020](https://oreil.ly/ZKRPR) ).

Il est possible de combiner linéairement des modèles entiers ou des parties de modèles. Les « soupes de modèles » ( [Wortsman et al., 2022](https://arxiv.org/abs/2203.05482) ) ont démontré comment la moyenne des poids de plusieurs modèles affinés peut améliorer la précision sans augmenter le temps d'inférence. Toutefois, il est plus courant de fusionner des modèles en combinant linéairement des composants spécifiques, tels que leurs adaptateurs.

Bien qu'il soit possible de combiner linéairement n'importe quel ensemble de modèles, _la combinaison linéaire est particulièrement efficace pour les modèles affinés à partir d'un même modèle de base._ Dans ce cas, la combinaison linéaire peut être appréhendée à travers le concept de _vecteurs de tâches_ . L'idée est que, une fois un modèle affiné pour une tâche spécifique, sa soustraction du modèle de base permet d'obtenir un vecteur qui capture l'essence de la tâche. Les vecteurs de tâches sont également appelés _paramètres delta_ . Si vous effectuez un affinage avec LoRA, vous pouvez construire le vecteur de tâches à partir des poids LoRA.

Les vecteurs de tâches permettent d'effectuer _des opérations arithmétiques_ ( [Ilharco et al., 2022](https://arxiv.org/abs/2212.04089) ), comme l'addition de deux vecteurs pour combiner leurs capacités ou la soustraction d'un vecteur pour réduire certaines capacités. La soustraction de tâches peut s'avérer utile pour éliminer les comportements indésirables du modèle, tels que les capacités intrusives comme la reconnaissance faciale ou les biais acquis lors du pré-entraînement.

La combinaison linéaire est simple lorsque les composants à fusionner ont la même architecture et la même taille. Cependant, elle peut également fonctionner pour des modèles qui n'ont ni la même architecture ni la même taille. Par exemple, si la couche d'un modèle est plus grande que celle de l'autre, vous pouvez projeter une ou les deux couches dans la même dimension.

Certains auteurs ont proposé d'aligner les modèles avant de les moyenner afin de garantir que les paramètres fonctionnellement liés soient moyennés ensemble, comme dans « Model Fusion via Optimal Transport » ( [Singh et Jaggi, 2020](https://arxiv.org/abs/1910.05653) ), « Git Re-Basin: Merging Models Modulo Permutation Symmetries » ( [Ainsworth et al., 2022](https://arxiv.org/abs/2209.04836) ) et « Merging by Matching Models in Task Parameter Subspaces » ( [Tam et al., 2023](https://arxiv.org/abs/2312.04339) ). Bien qu'il soit logique de combiner des paramètres alignés, l'alignement peut s'avérer complexe ; par conséquent, cette approche est moins courante pour les combinaisons linéaires simples.

#### Interpolation linéaire sphérique (SLERP)

Une autre méthode courante de sommation de modèles est SLERP, qui est basée sur l'opérateur mathématique du même nom, l'interpolation linéaire sphérique.

###### Note

L'interpolation consiste à estimer des valeurs inconnues à partir de valeurs connues. Dans le cas de la fusion de modèles, la valeur inconnue correspond au modèle fusionné, et les valeurs connues aux modèles constitutifs. La combinaison linéaire est une technique d'interpolation. La méthode SLERP en est une autre.

La formule de SLERP étant complexe et les outils de fusion de modèles l'implémentant généralement automatiquement, je n'entrerai pas dans les détails ici. Intuitivement, on peut se représenter chaque composante (vecteur) à fusionner comme un point sur une sphère. Pour fusionner deux vecteurs, on trace d'abord le chemin le plus court entre ces deux points à la surface de la sphère. Cela revient à tracer le chemin le plus court entre deux villes sur la surface de la Terre. Le vecteur résultant de la fusion de ces deux vecteurs est un point situé sur ce chemin. La position exacte de ce point dépend du facteur d'interpolation, que l'on peut définir entre 0 et 1. Les valeurs inférieures à 0,5 rapprochent le vecteur fusionné du premier vecteur, ce qui signifie que le premier vecteur contribuera davantage au résultat. Un facteur de 0,5 signifie que l'on choisit un point exactement à mi-chemin. Ce point médian est le point bleu de [la figure 7-16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_13_1730159634220389) .

L'opération mathématique SLERP est définie avec seulement deux vecteurs, ce qui signifie qu'on ne peut fusionner que deux vecteurs à la fois. Si vous souhaitez fusionner plus de deux vecteurs, vous pouvez potentiellement effectuer SLERP séquentiellement, c'est-à-dire fusionner A avec B, puis le résultat obtenu avec C.

![Un cercle avec des flèches et un cercle rouge. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0716.png)

###### Figure 7-16. Fonctionnement de SLERP pour deux vecteurs t1 et t2. La ligne rouge représente leur chemin le plus court sur la surface sphérique. Selon l'interpolation, le vecteur résultant peut être n'importe quel point de ce chemin. Le vecteur bleu représente le vecteur résultant lorsque le facteur d'interpolation est de 0,5.

#### Élimination des paramètres redondants spécifiques à la tâche

Lors de la phase d'ajustement fin, de nombreux paramètres du modèle sont modifiés. Cependant, la plupart de ces modifications sont mineures et n'ont pas d'incidence significative sur les performances du modèle. [Les](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1473) modifications qui n'améliorent pas les performances du modèle sont considérées _comme redondantes_ .

Dans l'article « TIES-Merging : Résolution des interférences lors de la fusion de modèles », [Yadav et al. (2023)](https://arxiv.org/abs/2306.01708) ont démontré qu'il est possible de réinitialiser une grande partie des paramètres du vecteur de tâches avec une dégradation minimale des performances, comme illustré dans [la figure 7-17](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_14_1730159634220402) . La réinitialisation consiste à rétablir la valeur d'origine du paramètre affiné dans le modèle de base, ce qui revient à annuler le paramètre correspondant du vecteur de tâches. (Rappelons que le vecteur de tâches s'obtient en soustrayant le modèle de base du modèle affiné.)

![Graphique avec une ligne droite et une ligne pointillée. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0717.png)

###### Figure 7-17. Dans les expériences de Yadav et al., conserver les 20 % supérieurs des paramètres du vecteur de tâche donne des performances comparables à celles obtenues en conservant 100 % des paramètres.

Ces paramètres redondants, bien qu'inoffensifs pour un modèle pris individuellement, peuvent nuire au modèle fusionné. Les techniques de fusion telles que TIES (Yadav et al., 2023) et DARE ( [Yu et al., 2023](https://arxiv.org/abs/2311.03099) ) éliminent d'abord les paramètres redondants des vecteurs de tâches avant de les fusionner. [Ces](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1474) deux études ont démontré que cette pratique améliore significativement la qualité des modèles fusionnés finaux. Plus le nombre de modèles à fusionner est élevé, plus l'élagage est important, car les risques d'interférence entre les paramètres redondants d'une tâche et d'autres tâches sont accrus.[33](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1477)

### Empilement de couches

Cette approche consiste à superposer différentes couches issues d'un ou plusieurs modèles. Par exemple, on peut utiliser la première couche du modèle 1 et la seconde du modèle 2. Également appelée _fusion_ par couches ou _fusion hybride_ , elle permet de créer des modèles aux architectures et aux nombres de paramètres uniques. Contrairement à la fusion par sommation, les modèles résultant de cette superposition nécessitent généralement un réglage fin supplémentaire pour optimiser leurs performances.

L'un des premiers succès de la fusion de modèles est [Goliath-120B](https://oreil.ly/IM0Jc) (Alpindale, 2023), issu de la fusion de deux modèles Llama 2-70B finement optimisés, [Xwin](https://oreil.ly/URfbk) et [Euryale](https://oreil.ly/Ftnxd) . 72 des 80 couches de chaque modèle ont été combinées.

L'empilement de couches peut être utilisé pour entraîner des modèles de type « mixte d'experts » (MoE), comme présenté dans « Sparse Upcycling : Training Mixture-of-Experts from Dense Checkpoints » ( [Komatsuzaki et al., 2022](https://arxiv.org/abs/2212.05055) ). Plutôt que d'entraîner un modèle MoE à partir de zéro, on utilise un modèle pré-entraîné et on en crée plusieurs copies de certaines couches ou modules. Un routeur est ensuite ajouté pour acheminer chaque entrée vers la copie la plus appropriée. On entraîne ensuite le modèle fusionné, associé au routeur, afin d'optimiser ses performances. [La figure 7-18](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_15_1730159634220410) illustre ce processus.

Komatsuzaki et al. ont démontré que l'empilement de couches permet de produire des modèles plus performants que les modèles MoE entraînés à partir de zéro. En utilisant cette approche, Together AI a combiné six modèles open source moins performants pour créer Mixture-of-Agents, qui a atteint des performances comparables à celles de GPT-4o d'OpenAI sur certains benchmarks ( [Wang et al., 2024](https://arxiv.org/abs/2406.04692) ).

![Schéma d'une machine. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0718.png)

###### Figure 7-18. Vous pouvez créer un modèle MoE à partir d'un modèle pré-entraîné. Image adaptée de Komatsuzaki et al. (2022).

Un cas d'utilisation intéressant de l'empilement de couches est _la mise à l'échelle de modèles_ . La mise à l'échelle de modèles consiste à étudier comment créer des modèles plus grands en utilisant moins de ressources. Parfois, on peut souhaiter un modèle plus volumineux que celui dont on dispose déjà, probablement parce que des modèles plus grands offrent de meilleures performances. Par exemple, votre équipe a peut-être initialement entraîné un modèle pour qu'il tienne sur votre GPU de 40 Go. Cependant, vous avez obtenu une nouvelle machine avec 80 Go, ce qui vous permet de déployer un modèle plus grand. Au lieu d'entraîner un nouveau modèle à partir de zéro, vous pouvez utiliser l'empilement de couches pour créer un modèle plus grand à partir du modèle existant.

Une méthode de mise à l'échelle par couches consiste à utiliser _la mise à l'échelle en profondeur_ . [Kim et al. (2023)](https://arxiv.org/abs/2312.15166) ont utilisé cette technique pour créer SOLAR 10.7B à partir d'un modèle à 7 milliards de paramètres comportant 32 couches. La procédure est la suivante :

1. Faites une copie du modèle pré-entraîné original.
    
2. Fusionnez ces deux copies en additionnant certaines couches (deux couches sont additionnées pour n'en former qu'une seule) et en empilant les autres. Les couches à additionner sont soigneusement sélectionnées pour correspondre à la taille du modèle cible. Pour SOLAR 10.7B, 16 couches sont additionnées, ce qui donne un modèle final comportant 32 × 2 - 16 = 48 couches.
    
3. Poursuivre l'entraînement de ce modèle amélioré afin d'atteindre les performances cibles.
    

[La figure 7-19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_16_1730159634220419) illustre ce processus.

![Capture d'écran d'un programme informatique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0719.png)

###### Figure 7-19. Utilisation de la mise à l'échelle en profondeur pour créer un modèle à 48 couches à partir d'un modèle à 32 couches. L'image est sous licence CC BY 4.0 et a été légèrement modifiée pour une meilleure lisibilité.

### Enchaînement

Au lieu d'additionner les paramètres des modèles constitutifs de différentes manières, vous pouvez également les concaténer. Le nombre de paramètres du composant fusionné sera la somme du nombre de paramètres de tous les composants constitutifs.Si vous fusionnez deux adaptateurs LoRA de rangs _r_ 1 et _r_ 2 , le rang de l'adaptateur fusionné sera _r_ 1 + _r_ 2 , comme indiqué dans [la figure 7-20](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_figure_17_1730159634220429) .

![Diagramme d'un algorithme. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0720.png)

###### Figure 7-20. Si vous fusionnez deux adaptateurs LoRA en utilisant la concaténation, le rang de l'adaptateur fusionné sera la somme des rangs des deux adaptateurs.

La concaténation est déconseillée car elle ne réduit pas l'empreinte mémoire par rapport à l'exécution séparée des différents modèles. Bien qu'elle puisse améliorer les performances, le gain obtenu ne justifie pas nécessairement le nombre de paramètres supplémentaires.[34](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1487)

## Tactiques de réglage fin

Ce chapitre a présenté différentes approches de réglage fin, les problèmes qu'elles résolvent et leur fonctionnement. Dans cette dernière partie, je me concentrerai sur des tactiques de réglage fin plus pratiques.

### Cadres de réglage fin et modèles de base

Bien que de nombreux aspects du réglage fin — décider de procéder au réglage fin, acquérir des données et maintenir les modèles réglés — soient complexes, le processus de réglage fin en lui-même est relativement simple. Il vous suffit de choisir trois éléments : un modèle de base, une méthode de réglage fin et un cadre de travail pour ce réglage.

#### Modèles de base

[Le chapitre 4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) a déjà abordé les critères de sélection de modèles applicables aux méthodes basées sur des invites et à l'ajustement fin. Parmi ces critères figurent la taille du modèle, les licences et les performances de référence. Au début d'un projet d'IA, lorsque vous évaluez encore la faisabilité de votre tâche, il est judicieux de commencer par le modèle le plus performant que votre budget vous permette. Si ce modèle peine à produire de bons résultats, les modèles moins puissants risquent d'être encore moins performants. Si le modèle le plus performant répond à vos besoins, vous pouvez alors explorer des modèles moins puissants, en utilisant le modèle initial comme référence.

Pour le réglage fin, les modèles de départ varient selon les projets. [Le document de bonnes pratiques d'OpenAI sur le réglage fin](https://oreil.ly/7I6Ch) donne des exemples de deux approches de développement : l'approche progressive et l'approche par distillation.

Le parcours de progression ressemble à ceci :

1. Testez votre code de réglage fin en utilisant le modèle le moins cher et le plus rapide pour vous assurer qu'il fonctionne comme prévu. [35](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1489)
    
2. Testez vos données en affinant un modèle intermédiaire. Si la perte d'entraînement ne diminue pas avec davantage de données, il y a peut-être un problème.
    
3. Effectuez quelques expériences supplémentaires avec le meilleur modèle pour voir jusqu'où vous pouvez pousser les performances.
    
4. Une fois que vous avez obtenu de bons résultats, effectuez un entraînement avec tous les modèles afin de définir la frontière prix/performance et de sélectionner le modèle le plus adapté à votre cas d'utilisation.
    

Le processus de distillation pourrait ressembler à ceci :

1. Commencez avec un petit ensemble de données et le modèle le plus performant que vous puissiez vous permettre. Entraînez le meilleur modèle possible avec cet ensemble réduit. Le modèle de base étant déjà performant, il nécessite moins de données pour obtenir de bons résultats.
    
2. Utilisez ce modèle affiné pour générer davantage de données d'entraînement.
    
3. Utilisez ce nouvel ensemble de données pour entraîner un modèle moins coûteux.
    

Le réglage fin intervenant généralement après des expérimentations et une ingénierie rapide, il est idéal de posséder une bonne compréhension du comportement des différents modèles avant de commencer cette étape. Votre démarche de réglage fin doit être planifiée en fonction de cette compréhension.

#### Méthodes de réglage fin

Rappelons que les techniques d'adaptation comme LoRa sont économiques, mais n'offrent généralement pas les mêmes performances qu'un réglage fin complet. Si vous débutez avec le réglage fin, essayez une solution comme LoRa, et tentez le réglage fin complet plus tard.

Les méthodes d'ajustement fin à utiliser dépendent également du volume de vos données. Selon le modèle de base et la tâche, un ajustement fin complet nécessite généralement au moins plusieurs milliers d'exemples, et souvent bien plus. Les méthodes PEFT, en revanche, peuvent offrir de bonnes performances avec un ensemble de données beaucoup plus petit. Si vous disposez d'un petit ensemble de données, par exemple quelques centaines d'exemples, un ajustement fin complet pourrait ne pas surpasser LoRA.

Tenez compte du nombre de modèles affinés nécessaires et de la manière dont vous souhaitez les diffuser lors du choix d'une méthode d'affinage. Les méthodes basées sur des adaptateurs, comme LoRa, permettent de diffuser plus efficacement plusieurs modèles partageant le même modèle de base. Avec LoRa, un seul modèle complet suffit, tandis qu'un affinage complet requiert la diffusion de plusieurs modèles complets.

#### Cadres de réglage fin

La méthode la plus simple pour affiner un modèle consiste à utiliser une API d'affinage. Vous pouvez y importer des données, sélectionner un modèle de base et obtenir en retour un modèle affiné. À l'instar des API d'inférence de modèles, les API d'affinage peuvent être fournies par des fournisseurs de modèles, des fournisseurs de services cloud et des prestataires tiers. Cette approche présente toutefois une limite : vous êtes limité aux modèles de base pris en charge par l'API. De plus, celle-ci peut ne pas exposer toutes les options permettant d'optimiser les performances d'affinage. Les API d'affinage conviennent aux utilisateurs recherchant une solution rapide et simple, mais peuvent s'avérer frustrantes pour ceux qui souhaitent une personnalisation plus poussée.

Vous pouvez également affiner votre modèle à l'aide de l'un des nombreux frameworks d'affinage disponibles, tels que [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) , [unsloth](https://github.com/unslothai/unsloth) , [PEFT](https://github.com/huggingface/peft) , [Axolotl](https://github.com/axolotl-ai-cloud/axolotl) et [LitGPT](https://github.com/Lightning-AI/litgpt) . Ces frameworks prennent en charge un large éventail de méthodes d'affinage, notamment les techniques basées sur les adaptateurs. Pour un affinage complet, de nombreux modèles de base proposent leur code source d'entraînement sur GitHub ; vous pouvez le cloner et l'exécuter avec vos propres données. [Llama Police](https://huyenchip.com/llama-police) propose une liste plus exhaustive et à jour des frameworks d'affinage et des dépôts de modèles.

Le réglage fin personnalisé offre une plus grande flexibilité, mais nécessite l'allocation de la puissance de calcul nécessaire. Pour la plupart des modèles, un GPU de milieu de gamme peut suffire si vous utilisez uniquement des techniques basées sur des adaptateurs. Au besoin, une puissance de calcul supérieure peut être envisagée avec un framework s'intégrant parfaitement à votre fournisseur de cloud.

Pour affiner un modèle en utilisant plusieurs machines, vous aurez besoin d'un framework qui vous aide à effectuer un entraînement distribué, tel que [DeepSpeed](https://github.com/microsoft/DeepSpeed) , [PyTorch Distributed](https://oreil.ly/hxUAk) et [ColossalAI](https://github.com/microsoft/DeepSpeed) .

### Réglage fin des hyperparamètres

Selon le modèle de base et la méthode d'ajustement fin, de nombreux hyperparamètres peuvent être optimisés pour améliorer l'efficacité de l'ajustement. Pour connaître les hyperparamètres spécifiques à votre cas d'utilisation, consultez la documentation du modèle de base ou du framework d'ajustement fin que vous utilisez. Je vais ici aborder quelques hyperparamètres importants qui reviennent fréquemment.

#### taux d'apprentissage

Le taux d'apprentissage détermine la vitesse à laquelle les paramètres du modèle évoluent à chaque étape d'apprentissage. Si l'on compare l'apprentissage à la recherche d'un chemin vers un objectif, le taux d'apprentissage correspond à la taille du pas. Si ce pas est trop petit, atteindre l'objectif risque d'être trop long. À l'inverse, s'il est trop grand, l'objectif risque d'être dépassé et, par conséquent, le modèle risque de ne jamais converger.

Il n'existe pas de taux d'apprentissage optimal universel. Il est nécessaire d'expérimenter avec différents taux, généralement compris entre 1e-7 et 1e-3, afin de déterminer celui qui convient le mieux. Une pratique courante consiste à multiplier le taux d'apprentissage obtenu à la fin de la phase de pré-entraînement par une constante comprise entre 0,1 et 1.

La courbe de perte peut vous donner des indications sur le taux d'apprentissage. Si elle fluctue beaucoup, le taux d'apprentissage est probablement trop élevé. Si elle est stable mais met du temps à diminuer, l'apprentissage est probablement trop faible. Augmentez le taux d'apprentissage jusqu'à ce que la courbe de perte reste stable.

Vous pouvez faire varier les taux d'apprentissage pendant l'entraînement. Vous pouvez utiliser des taux d'apprentissage plus élevés au début et plus faibles vers la fin. Les algorithmes qui déterminent comment les taux d'apprentissage doivent évoluer au cours de l'entraînement sont appelés des programmes de variation des taux d'apprentissage.

#### Taille du lot

La taille du lot détermine le nombre d'exemples dont un modèle tire des enseignements à chaque étape pour mettre à jour ses poids. Une taille de lot trop petite, par exemple inférieure à huit, peut entraîner une instabilité de l'entraînement. Une taille de lot plus [importante](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1497) permet d'agréger les signaux provenant de différents exemples, ce qui se traduit par des mises à jour plus stables et fiables.

En général, plus la taille des lots est importante, plus le modèle peut traiter rapidement les exemples d'entraînement. Cependant, plus la taille des lots est importante, plus le modèle a besoin de mémoire pour s'exécuter. La taille des lots est donc limitée par le matériel utilisé.

C’est là que l’on observe le compromis entre coût et efficacité. Une puissance de calcul plus importante permet un réglage plus rapide.

À l'heure actuelle, la puissance de calcul reste un facteur limitant pour le réglage fin. Souvent, les modèles sont si volumineux et la mémoire si restreinte que seules de petites tailles de lots peuvent être utilisées. Cela peut entraîner des mises à jour instables des poids du modèle. Pour y remédier, au lieu de mettre à jour les poids du modèle après chaque lot, il est possible d'accumuler les gradients sur plusieurs lots et de mettre à jour les poids du modèle une fois qu'un nombre suffisant de gradients fiables a été accumulé. Cette technique est appelée _accumulation de gradients_ . <sup> [37</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1498)

Lorsque le coût de calcul n'est pas le facteur le plus important, vous pouvez expérimenter avec différentes tailles de lots pour voir laquelle offre les meilleures performances du modèle.

#### Nombre d'époques

Une époque correspond à un passage sur les données d'entraînement. Le nombre d'époques détermine le nombre de fois où chaque exemple d'entraînement est répété.

Les petits ensembles de données peuvent nécessiter plus d'époques que les grands. Pour un ensemble de données contenant des millions d'exemples, 1 à 2 époques peuvent suffire. Un ensemble de données contenant des milliers d'exemples peut encore présenter une amélioration des performances après 4 à 10 époques.

La différence entre la perte d'entraînement et la perte de validation peut vous donner des indications sur le nombre d'époques. Si les deux pertes continuent de diminuer régulièrement, le modèle gagnerait à avoir plus d'époques (et plus de données). Si la perte d'entraînement continue de diminuer mais que la perte de validation augmente, le modèle est en surapprentissage ; vous pourriez alors essayer de réduire le nombre d'époques.

#### Perte de poids rapide

Pour l'ajustement fin des instructions, chaque exemple comprend une invite et une réponse, qui contribuent toutes deux à la perte du modèle pendant l'entraînement. En revanche, lors de l'inférence, les invites sont généralement fournies par les utilisateurs et le modèle n'a besoin de générer que les réponses. Par conséquent, les jetons de réponse devraient contribuer davantage à la perte du modèle pendant l'entraînement que les jetons d'invite.

Le poids du modèle d'invite détermine la contribution respective des invites et des réponses à la perte. Si ce poids est de 100 %, les invites contribuent autant que les réponses, ce qui signifie que le modèle apprend de manière égale des deux. Si ce poids est de 0 %, le modèle apprend uniquement des réponses. Généralement, ce poids est fixé à 10 % par défaut, ce qui signifie que le modèle doit apprendre en partie des invites, mais principalement des réponses.réponses.

# Résumé

Hormis les chapitres consacrés à l'évaluation, celui sur le réglage fin a été le plus difficile à rédiger. Il abordait un large éventail de concepts, à la fois anciens (apprentissage par transfert) et nouveaux (PEFT), fondamentaux (factorisation de faible rang) et expérimentaux (fusion de modèles), mathématiques (calcul de la mémoire) et tactiques (optimisation des hyperparamètres). Organiser tous ces aspects différents en une structure cohérente tout en les rendant accessibles s'est avéré complexe.

Le processus de réglage fin en lui-même n'est pas difficile. De nombreux frameworks de réglage fin prennent en charge l'entraînement. Ces frameworks peuvent même suggérer des méthodes de réglage fin courantes avec des hyperparamètres par défaut pertinents.

Cependant, le contexte du réglage fin est complexe. Tout commence par la question de savoir s'il est même judicieux de procéder à un réglage fin. Ce chapitre a débuté par l'examen des raisons justifiant et de celles s'opposant au réglage fin. Il a également abordé une question qui m'a été posée à maintes reprises : quand effectuer un réglage fin et quand utiliser la méthode RAG (Real Aggregation, Analysis, Analysis).

À ses débuts, le finetuning était similaire au pré-entraînement : les deux consistaient à mettre à jour l’ensemble des poids du modèle. Cependant, avec l’augmentation de la taille des modèles, le finetuning complet est devenu impraticable pour la plupart des praticiens. Plus le nombre de paramètres à mettre à jour est élevé lors du finetuning, plus les besoins en mémoire sont importants. La plupart des praticiens ne disposent pas des ressources suffisantes (matériel, temps et données) pour effectuer un finetuning complet avec les modèles de base.

De nombreuses techniques d'ajustement fin ont été développées avec la même motivation : obtenir des performances élevées avec une empreinte mémoire minimale. Par exemple, PEFT réduit les besoins en mémoire de l'ajustement fin en diminuant le nombre de paramètres entraînables. L'entraînement quantifié, quant à lui, atténue ce goulot d'étranglement mémoire en réduisant le nombre de bits nécessaires pour représenter chaque valeur.

Après avoir présenté PEFT, le chapitre s'est concentré sur LoRA : son fonctionnement et ses avantages. LoRA possède de nombreuses qualités qui expliquent sa popularité auprès des praticiens. Outre son efficacité en termes de paramètres et de données, sa modularité facilite grandement le déploiement et la combinaison de plusieurs modèles LoRA.

L'idée de combiner des modèles affinés a conduit ce chapitre à aborder la fusion de modèles ; son objectif est de combiner plusieurs modèles en un seul, plus performant que chacun pris séparément. Ce chapitre a examiné les nombreux cas d'utilisation de la fusion de modèles, du déploiement sur appareil à la mise à l'échelle des modèles, ainsi que les approches générales en la matière.

J'entends souvent dire par les praticiens que le réglage fin est facile, mais que l'obtention des données nécessaires est difficile. Obtenir des données annotées de haute qualité, notamment des données d'instructions, représente un véritable défi. Le chapitre suivant abordera ces difficultés en détail.

[1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1369-marker)Certains appellent ce phénomène une taxe d’alignement ( [Bai et al., 2020](https://arxiv.org/abs/2204.05862) ), mais ce terme peut être confondu avec les sanctions contre l’alignement des préférences humaines.

[2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1370-marker)Nombre d'entreprises résistent au changement de technologies qu'elles jugent « suffisantes ». Si toutes les entreprises adoptaient rapidement des solutions plus optimales, les télécopieurs seraient déjà obsolètes.

[3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1371-marker)J'ai également constaté quelques cas où des ingénieurs savent que le réglage fin n'est pas strictement nécessaire, mais insistent pour le faire car ils souhaitent apprendre à le maîtriser. En tant qu'ingénieur qui apprécie l'acquisition de nouvelles compétences, je comprends cet état d'esprit. Cependant, lorsqu'on occupe un poste de direction, il peut être difficile de faire la distinction entre un réglage fin nécessaire et un réglage fin souhaité.

[4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1374-marker)0314 indique la date de sortie de cette version de GPT-4, soit le 14 mars 2024. Cette date précise est importante car les performances varient considérablement d'une version à l'autre.

[5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1377-marker)Certaines personnes, comme les auteurs de l'article Llama 3.1 ( [Dubey et al., 2024](https://arxiv.org/abs/2407.21783) ), adhèrent au « principe selon lequel la post-formation devrait aligner le modèle sur "savoir ce qu'il sait" plutôt que d'ajouter des connaissances ».

[6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1382-marker)Outre la rétropropagation, une approche prometteuse pour l'entraînement des réseaux de neurones est la stratégie évolutionnaire. Un exemple, décrit par [Maheswaranathan et al.](https://oreil.ly/B59ci) , combine une recherche aléatoire avec des gradients de substitution, au lieu d'utiliser les gradients réels, pour mettre à jour les poids du modèle. Une autre approche intéressante est l'alignement direct par rétroaction ( [Arild Nøkland, 2016](https://arxiv.org/abs/1609.01596) ).

[7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1383-marker)Si un paramètre n'est pas entraînable, il n'est pas nécessaire de le mettre à jour et, par conséquent, il n'est pas nécessaire de calculer son gradient.

[8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1389-marker)Certains pourraient dire que vous ne faites pas d'IA tant que vous n'avez pas vu une erreur « RuntimeError : CUDA out of memory ».

[9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1390-marker)Pour en savoir plus sur le calcul de la mémoire d'inférence, consultez l'article de Carol Chen [intitulé « Transformer Inference Arithmetic »](https://oreil.ly/u7wYx) , sur le blog de kipply (mars 2022).

[10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1395-marker)Pour en savoir plus sur le calcul de la mémoire d'entraînement, consultez [« Transformer Math 101 »](https://oreil.ly/Xe7h6) d'EleutherAI (Anthony et al., avril 2023).

[11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1396-marker)Google a présenté BFloat16 comme [« le secret des hautes performances sur les TPU Cloud »](https://oreil.ly/atIgi) .

[12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1397-marker)Les formats entiers sont également appelés formats _à virgule fixe_ .

[13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1398-marker)Les bits de plage sont appelés _exposants_ . Les bits de précision sont appelés _mantisses_ .

[14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1401-marker)Notez que généralement, le nombre à la fin du nom d'un format indique le nombre de bits qu'il occupe, mais TF32 possède en réalité 19 bits, et non 32. Je pense que ce nom a été choisi pour suggérer sa compatibilité fonctionnelle avec FP32. Mais honnêtement, je me demande encore pourquoi on l'appelle TF32 et non TF19. Un ancien collègue chez NVIDIA a émis l'hypothèse que les gens pourraient être sceptiques face à des formats inhabituels (19 bits), et que le nom TF32 rendrait ce format plus accessible.

[15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1404-marker)La confusion entre FP16 et BF16 s'est poursuivie avec Llama 3.1. Voir les discussions X et Threads : [1](https://en.wikipedia.org/wiki/IEEE_754) ; [2](https://x.com/abacaj/status/1695334296792264792?s=20) , [3](https://oreil.ly/U8L4d) , [4](https://oreil.ly/8ush1) ; et [le benchmark de llama.cpp entre BF16 et FP16](https://github.com/ggerganov/llama.cpp/pull/7150) , [le compte rendu de Bloke](https://oreil.ly/0vuze) et [le compte rendu de Raschka](https://oreil.ly/WK_zT) .

[16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1405-marker)La conception de formats numériques est une discipline passionnante. La possibilité de créer un format de moindre précision sans compromettre la qualité d'un système peut le rendre beaucoup moins cher et plus rapide, ouvrant ainsi la voie à de nouveaux cas d'utilisation.

[17](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1406-marker)Un autre facteur important contribuant à l'empreinte mémoire des modèles à base de transformateurs est le cache KV, qui est abordé au [chapitre 9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301) .

[18](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1407-marker)La plus petite taille de nombre flottant possible qui respecte tous les principes IEEE est de 4 bits.

[19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1408-marker)Les auteurs de l'article sur Xnor-Net ont fondé Xnor.ai, une start-up spécialisée dans la compression de modèles. [Début 2020, elle a été rachetée par Apple pour un montant estimé à 200 millions de dollars](https://oreil.ly/V4pma) .

[20](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1415-marker)Durant l'entraînement, les poids du modèle sont mis à jour en plusieurs étapes. De petites erreurs d'arrondi peuvent s'accumuler au cours de ce processus, rendant difficile l'obtention des performances souhaitées. De plus, le calcul des valeurs de perte exige une grande précision. De faibles variations de ces valeurs peuvent orienter les mises à jour des paramètres dans la mauvaise direction.

[21](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1416-marker)Anecdote personnelle : une grande partie du travail de mon équipe chez NVIDIA portait sur l’entraînement en précision mixte. Voir [« Entraînement en précision mixte pour le traitement automatique du langage naturel et la reconnaissance vocale avec OpenSeq2Seq »](https://oreil.ly/QL2gL) (Huyen et al., blog technique des développeurs NVIDIA, octobre 2018).

[22](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1429-marker)Dans le réglage fin partiel, il est courant de régler les couches les plus proches de la couche de sortie, car ces couches sont généralement plus spécifiques à la tâche, tandis que les couches précédentes ont tendance à capturer des caractéristiques plus générales.

[23](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1431-marker)Je n'ai jamais rencontré une seule personne capable de m'expliquer, sur-le-champ, les différences entre ces techniques.

[24](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1439-marker)Pour utiliser efficacement LoRA avec un modèle, il est nécessaire de comprendre son architecture. [Le chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) a déjà abordé la composition des poids de certains modèles basés sur les transformateurs. Pour connaître la composition exacte des poids d'un modèle, veuillez vous référer à l'article correspondant.

[25](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1441-marker)À l'heure actuelle, certains frameworks de réglage fin comme [Fireworks](https://oreil.ly/82-jJ) n'autorisent qu'un rang LoRA maximal de 32. Cependant, cette limitation est peu susceptible d'être due à des problèmes de performance et plus probablement à une limitation de mémoire de leur matériel.

[26](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1444-marker)Recherchez ces adaptateurs par les mots-clés « adapter », « peft » ou « LoRA ».

[27](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1447-marker)QLoRA n'est pas le seul projet de LoRA quantifié. De nombreux laboratoires de recherche travaillent sur le LoRA quantifié sans en parler publiquement.

[28](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1463-marker)Mon livre, [_Designing Machine Learning Systems,_](https://oreil.ly/u_cVP) comporte une section sur « L’apprentissage automatique dans le cloud et en périphérie ».

[29](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1465-marker)Vous pouvez en savoir plus sur les méthodes d'ensemble dans mon livre [_Designing Machine Learning Systems_](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) .

[30](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1466-marker)La moyenne fonctionne non seulement avec les poids, mais aussi avec les plongements lexicaux. Par exemple, pour une phrase donnée, on peut utiliser un algorithme de plongement de mots pour générer un vecteur de plongement pour chaque mot, puis faire la moyenne de ces plongements pour obtenir un plongement de la phrase. Quand j'ai débuté en apprentissage automatique, j'étais sidéré de voir à quel point la moyenne fonctionnait si bien. C'est magique de constater comment des composants simples, utilisés à bon escient, peuvent créer quelque chose d'aussi fascinant et complexe que l'intelligence artificielle.

[31](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1473-marker)L'hypothèse est que les paramètres qui subissent les changements les plus importants lors du réglage fin sont ceux qui sont les plus cruciaux pour la tâche visée.

[32](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1474-marker)TIES est l'abréviation de « Trim, Elect Sign, and merge », tandis que DARE vient de « Drop And REscale ». Je sais, ces abréviations me font aussi souffrir.

[33](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1477-marker)Lorsque les vecteurs de tâches sont élagués, ils deviennent plus clairsemés, mais le modèle affiné, lui, ne l'est pas. Dans ce cas précis, l'élagage ne vise pas à réduire l'empreinte mémoire ni la latence d'inférence, mais à améliorer les performances.

[34](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1487-marker)J'ai longtemps hésité à inclure la technique de concaténation dans cet ouvrage, et j'ai finalement décidé de l'inclure par souci d'exhaustivité.

[35](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1489-marker)À la fac, j'ai fait l'erreur fatale de laisser mon train miniature tourner toute la nuit, pour le voir planter au bout de huit heures parce que j'avais essayé de sauvegarder la partie dans un dossier inexistant. J'ai perdu toute ma progression.

[36](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1497-marker)Bien qu'il soit généralement admis que les petits lots entraînent une instabilité de l'entraînement, je n'ai pas trouvé d'explications satisfaisantes à ce sujet. Si vous avez des références à ce propos, n'hésitez pas à me les communiquer.

[37](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#id1498-marker)J'ai cherché en vain le premier article introduisant l'accumulation de gradients. Son utilisation en apprentissage profond a été mentionnée dès 2016 dans [« Ako : Apprentissage profond décentralisé avec échange partiel de gradients »](https://oreil.ly/GFeC7) (Watcharapichat et al., _Actes du septième symposium ACM sur le cloud computing_ , 2016). Ce concept semble provenir de l'entraînement distribué, où les gradients calculés sur différentes machines doivent être accumulés et utilisés pour mettre à jour les poids du modèle.