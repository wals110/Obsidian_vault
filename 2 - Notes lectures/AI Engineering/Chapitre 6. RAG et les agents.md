

Pour résoudre une tâche, un modèle a besoin à la fois des instructions et des informations nécessaires à son exécution. De même qu'un humain est plus susceptible de donner une mauvaise réponse en cas de manque d'informations, les modèles d'IA sont plus susceptibles de commettre des erreurs et de produire des résultats erronés lorsqu'ils manquent de contexte. Pour une application donnée, les instructions du modèle sont communes à toutes les requêtes, tandis que le contexte est spécifique à chaque requête. Le chapitre précédent expliquait comment rédiger des instructions pertinentes pour le modèle. Ce chapitre se concentre sur la construction du contexte pertinent pour chaque requête.

Deux modèles dominants de construction de contexte sont RAG (génération augmentée par la récupération) et les agents. Le modèle RAG permet au modèle de récupérer des informations pertinentes à partir de sources de données externes. Le modèle agent lui permet d'utiliser des outils tels que les API de recherche web et d'actualités pour collecter des informations.

Alors que le modèle RAG est principalement utilisé pour la construction du contexte, le modèle agentique offre bien plus. Les outils externes permettent aux modèles de pallier leurs lacunes et d'étendre leurs capacités. Surtout, ils leur confèrent la possibilité d'interagir directement avec le monde, leur permettant ainsi d'automatiser de nombreux aspects de notre vie.

Les modèles RAG et agentic sont particulièrement intéressants en raison des fonctionnalités qu'ils apportent à des modèles déjà performants. En peu de temps, ils ont su captiver l'imagination du public, donnant lieu à des démonstrations et des produits impressionnants qui convainquent nombre de personnes qu'ils représentent l'avenir. Ce chapitre détaillera chacun de ces modèles, leur fonctionnement et les raisons de leur potentiel.

# RAG

RAG est une technique qui améliore la génération d'un modèle en récupérant les informations pertinentes à partir de sources de mémoire externes. Ces sources peuvent être une base de données interne, l'historique des conversations d'un utilisateur ou Internet.

Le modèle _« récupérer puis générer »_ a été introduit pour la première fois dans « Lire Wikipédia pour répondre aux questions de domaine ouvert » ( [Chen et al., 2017](https://arxiv.org/abs/1704.00051) ). Dans ce travail, le système récupère d’abord les cinq pages Wikipédia les plus pertinentes pour une question, puis un modèle [1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1227) utilise, ou lit, les informations de ces pages pour générer une réponse, comme illustré dans [la figure 6-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_1_1730157386529219) .

![Diagramme d'un document. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0601.png)

###### Figure 6-1. Le modèle de récupération puis de génération. Le modèle a été appelé _lecteur de documents_ .

Le terme « génération augmentée par la récupération » a été introduit dans l’article « Génération augmentée par la récupération pour les tâches de TALN à forte intensité de connaissances » ( [Lewis et al., 2020 ). Cet article propose la génération augmentée par la récupération (RAG) comme solution pour les tâches nécessitant une forte intensité de connaissances, où toutes les connaissances disponibles ne peuvent être directement intégrées au](https://arxiv.org/abs/2005.11401) [modèle](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1228) . Avec la RAG, seules les informations les plus pertinentes pour la requête, déterminées par l’utilisateur, sont récupérées et intégrées au modèle. Lewis et al. ont constaté que l’accès aux informations pertinentes permet au modèle de générer des réponses plus détaillées tout en réduisant les hallucinations.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1228)

Par exemple, face à la requête « L'imprimante Acme Fancy-Printer-A300 peut-elle imprimer à 100 pages par seconde ? », le modèle sera en mesure de répondre plus efficacement s'il dispose des spécifications de l'imprimante Fancy-Printer-A300. [3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1229)

On peut considérer RAG comme une technique permettant de construire un contexte spécifique à chaque requête, au lieu d'utiliser le même contexte pour toutes les requêtes. Cela facilite la gestion des données utilisateur, car cela permet d'inclure les données spécifiques à un utilisateur uniquement dans les requêtes qui le concernent.

La construction du contexte pour les modèles de base est équivalente à l'ingénierie des caractéristiques pour les modèles d'apprentissage automatique classiques. Elles servent le même objectif : fournir au modèle les informations nécessaires au traitement d'une entrée.

Aux débuts des modèles de base, RAG s'est imposé comme l'un des modèles les plus courants. Son objectif principal était de pallier les limitations contextuelles des modèles. Beaucoup pensent qu'un contexte suffisamment long signera la fin de RAG. Je ne partage pas cet avis. Premièrement, quelle que soit la longueur du contexte d'un modèle, certaines applications nécessiteront un contexte plus étendu. En effet, la quantité de données disponibles ne cesse de croître. On génère et ajoute de nouvelles données, mais on en supprime rarement. La longueur du contexte augmente rapidement, mais pas assez vite pour répondre aux besoins en données de toutes les applications [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1230)

Deuxièmement, un modèle capable de traiter un contexte long ne l'exploite pas nécessairement de manière optimale, comme expliqué dans la section [« Longueur et efficacité](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_context_length_and_context_efficiency_1730156991195850) du contexte ». Plus le contexte est long, plus le modèle risque de se concentrer sur une partie non pertinente. Chaque jeton de contexte supplémentaire engendre un coût additionnel et peut potentiellement augmenter la latence. RAG permet à un modèle d'utiliser uniquement les informations les plus pertinentes pour chaque requête, réduisant ainsi le nombre de jetons d'entrée tout en améliorant potentiellement ses performances.

Les efforts visant à étendre la longueur du contexte se poursuivent en parallèle de ceux déployés pour améliorer l'utilisation du contexte par les modèles. Je ne serais pas surpris qu'un fournisseur de modèles intègre un mécanisme de type recherche ou attention pour aider un modèle à sélectionner les éléments les plus pertinents du contexte.

###### Note

Anthropic suggère que pour les modèles Claude, si « votre base de connaissances contient moins de 200 000 jetons (environ 500 pages de contenu), vous pouvez simplement inclure l’intégralité de la base de connaissances dans l’instruction fournie au modèle, sans avoir recours à RAG ni à des méthodes similaires » ( [Anthropic, 2024](https://oreil.ly/v-T_4) ). Il serait remarquable que d’autres développeurs de modèles proposent des recommandations similaires concernant l’utilisation de RAG par rapport à un contexte plus long pour leurs modèles.

## Architecture RAG

Un système RAG comporte deux composants : un module de récupération qui extrait des informations de sources de mémoire externes et un générateur qui produit une réponse à partir de ces informations. [La figure 6-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_2_1730157386529231) illustre l’architecture générale d’un système RAG.

![Diagramme d'un programme informatique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0602.png)

###### Figure 6-2. Une architecture RAG de base.

Dans l'article original sur les systèmes RAG, [Lewis et al.](https://arxiv.org/abs/2005.11401) ont entraîné conjointement le modèle de récupération et le modèle génératif. Dans les systèmes RAG actuels, ces deux composants sont souvent entraînés séparément, et de nombreuses équipes utilisent des modèles et des modules de récupération prêts à l'emploi pour construire leurs systèmes. Cependant, un réglage fin de l'ensemble du système RAG peut améliorer considérablement ses performances.

Le succès d'un système RAG dépend de la qualité de son rapporteur.Un récupérateur possède deux fonctions principales : l’indexation et l’interrogation.L'indexation consiste à traiter les données afin de pouvoir les retrouver rapidement ultérieurement. L'envoi d'une requête pour récupérer les données pertinentes s'appelle une interrogation. La méthode d'indexation des données dépend de la manière dont vous souhaitez les récupérer par la suite.

Maintenant que nous avons abordé les principaux composants, prenons l'exemple du fonctionnement d'un système RAG. Par souci de simplicité, supposons que la mémoire externe soit une base de données de documents, tels que les notes de service, les contrats et les comptes rendus de réunion d'une entreprise. Un document peut contenir de 10 à 1 million d'éléments. Récupérer directement des documents entiers peut rendre le contexte excessivement long.Pour éviter cela, vous pouvez diviser chaque document en segments plus faciles à gérer. Les stratégies de segmentation seront abordées plus loin dans ce chapitre. Supposons pour l'instant que tous les documents aient été divisés en segments exploitables. Pour chaque requête, notre objectif est de récupérer les segments de données les plus pertinents. Un post-traitement mineur est souvent nécessaire pour associer les segments de données récupérés à l'invite utilisateur afin de générer l'invite finale. Cette invite finale est ensuite intégrée au modèle génératif.

###### Note

Dans ce chapitre, j'utilise le terme « document » pour désigner à la fois un document et un segment de document, car techniquement, un segment de document est aussi un document. Ce choix vise à assurer la cohérence de la terminologie de cet ouvrage avec celle du traitement automatique du langage naturel (TALN) et de la recherche d'information (RI).

## Retrieval Algorithms

[La recherche d'informations n'est pas propre à la RAG (Research Analytics, Analytics, Google )](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1238) . C'est un concept centenaire.⁵ Elle constitue le fondement des moteurs de recherche, des systèmes de recommandation, de l'analyse des journaux, etc. De nombreux algorithmes de recherche développés pour les systèmes traditionnels peuvent également être utilisés pour la RAG. Par exemple, la recherche d'informations est un domaine de recherche fertile, soutenu par une industrie importante, qu'il est difficile de traiter en profondeur en quelques pages. Par conséquent, cette section n'en abordera que les grandes lignes. Pour des ressources plus détaillées sur la recherche d'informations, veuillez consulter [le dépôt GitHub de cet ouvrage.](https://oreil.ly/aie-book)

---
###### Note

La récupération d'informations se limite généralement à une seule base de données ou un seul système, tandis que la recherche implique une récupération d'informations à travers plusieurs systèmes. Dans ce chapitre, les termes « récupération » et « recherche » sont utilisés indifféremment.

Le principe de la recherche d'informations repose sur le classement des documents en fonction de leur pertinence par rapport à une requête donnée. Les algorithmes de recherche diffèrent selon la méthode de calcul des scores de pertinence. Je commencerai par deux mécanismes courants : la recherche par termes et la recherche par plongement lexical.

---
#  Sparse Versus Dense Retrieval

Dans la littérature, on peut rencontrer la classification des algorithmes de recherche en deux catégories : épars et denses. Cet ouvrage, en revanche, privilégie une catégorisation par termes plutôt que par plongement lexical.

Les algorithmes de recherche clairsemée représentent les données à l'aide _de vecteurs clairsemés_ . Un vecteur clairsemé est un vecteur dont la majorité des valeurs sont nulles. La recherche par terme est considérée comme clairsemée, car chaque terme peut être représenté par un _vecteur one-hot_ clairsemé , c'est-à-dire un vecteur qui vaut 0 partout sauf à l'emplacement où il vaut 1. La taille du vecteur correspond à la longueur du vocabulaire. La valeur 1 se trouve à l'indice correspondant à l'indice du terme dans le vocabulaire.

Si nous avons un dictionnaire simple, `{“food”: 0, “banana”: 1, “slug”: 2}`, alors les vecteurs one-hot de « nourriture », « banane » et « limace » sont respectivement `[1, 0, 0]`, `[0, 1, 0]`, et `[0, 0, 1]`.

Les algorithmes de recherche dense représentent les données à l'aide _de vecteurs denses_ . Un vecteur dense est un vecteur dont la majorité des valeurs sont non nulles. La recherche basée sur l'intégration est généralement considérée comme dense, car les intégrations sont généralement des vecteurs denses. Cependant, il existe aussi des intégrations creuses. Par exemple, SPLADE (Sparse Lexical and Expansion) est un algorithme de recherche qui utilise des intégrations creuses ( [Formal et al., 2021](https://arxiv.org/abs/2107.05720) ). Il exploite les intégrations générées par BERT, mais utilise une régularisation pour contraindre la plupart des valeurs d'intégration à zéro. Cette régularisation rend les opérations d'intégration plus efficaces.

La distinction entre algorithmes clairsemés et denses conduit à regrouper SPLADE avec les algorithmes basés sur les termes, alors que ses opérations, ses points forts et ses faiblesses sont bien plus proches de ceux de la recherche par plongement dense que de ceux de la recherche par termes. Une distinction entre algorithmes basés sur les termes et algorithmes basés sur le plongement permet d'éviter cette erreur de catégorisation.

### Recherche par terme

Face à une requête, la méthode la plus simple pour trouver des documents pertinents consiste à utiliser des mots-clés. Cette approche est parfois appelée _recherche lexicale_ . Par exemple, pour la requête « ingénierie IA », le modèle récupérera tous les documents contenant « ingénierie IA ». Cependant, cette approche présente deux problèmes :

- De nombreux documents peuvent contenir le terme donné, et votre modèle risque de ne pas disposer d'un espace contextuel suffisant pour tous les inclure. Une heuristique consiste à inclure les documents qui contiennent le terme le plus fréquemment. On part du principe que plus un terme apparaît dans un document, plus ce document est pertinent pour ce terme. Le nombre d'occurrences d'un terme dans un document est appelé _fréquence du terme_ (FT).
    
- Une consigne peut être longue et contenir de nombreux termes. Certains sont plus importants que d'autres. Par exemple, la consigne « Recettes faciles à suivre pour cuisiner vietnamien à la maison » contient neuf termes : _facile à suivre, recettes, pour, vietnamien, cuisine, à, cuisiner, à, maison_ . Il est préférable de se concentrer sur les termes les plus informatifs comme _« vietnamien »_ et _« recettes »_ , plutôt que sur _« pour_ » et _« à »_ . Il vous faut donc un moyen d'identifier les termes importants.
    
    Intuitivement, on pourrait penser que plus un terme est présent dans les documents, moins il est informatif. Les mots « pour » et « à » apparaissent généralement dans la plupart des documents et sont donc moins informatifs. L’importance d’un terme est donc inversement proportionnelle au nombre de documents dans lesquels il apparaît. Cette mesure est appelée_Fréquence inverse de document_ (IDF). Pour calculer l'IDF d'un terme, comptez le nombre de documents qui le contiennent, puis divisez le nombre total de documents par ce nombre. S'il y a 10 documents et que 5 d'entre eux contiennent un terme donné, alors l'IDF de ce terme est de 10 / 5 = 2. Plus l'IDF d'un terme est élevé, plus il est important.
    

TF-IDF est un algorithme qui combine deux métriques : la fréquence des termes (TF) et la fréquence inverse des documents (IDF). Mathématiquement, le score TF-IDF du document _D_ pour la requête _Q_ est calculé comme suit :

- Laisserêtre les termes de la requête _Q_ .
    
- Étant donné un terme _t_ , la fréquence de ce terme dans le document _D_ est _f(t, D)_ .
    
- Soit _N_ le nombre total de documents, et _C(t)_ le nombre de documents contenant le terme _t_ . La valeur IDF du terme _t_ peut s'écrire comme suit :.
    
- De manière naïve, le score TF-IDF d'un document _D_ par rapport à _Q_ est défini comme.
    

Elasticsearch et BM25 sont deux solutions courantes de recherche par termes. [Elasticsearch](https://github.com/elastic/elasticsearch) (Shay Banon, 2010), basé sur [Lucene](https://github.com/apache/lucene) , utilise une structure de données appelée index inversé. Il s'agit d'un dictionnaire associant les termes aux documents qui les contiennent. Ce dictionnaire permet une recherche rapide des documents à partir d'un terme. L'index peut également stocker des informations supplémentaires, telles que la fréquence du terme et le nombre de documents où il apparaît (nombre de documents contenant ce terme), utiles pour le calcul des scores TF-IDF. [Le tableau 6-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_table_1_1730157386543390) illustre un index inversé.

Tableau 6-1. Un exemple simplifié d'indice inversé.

|Terme|Nombre de documents|(Index des documents, fréquence des termes) pour tous les documents contenant le terme|
|---|---|---|
|banane|2|(10, 3), (5, 2)|
|machine|4|(1, 5), (10, 1), (38, 9), (42, 5)|
|apprentissage|3|(1, 5), (38, 7), (42, 5)|
|…|…|…|

[Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) , la 25e génération de l'algorithme de correspondance optimale, a été développé par Robertson et al. dans les années 1980. Son système de notation est une modification du TF-IDF. Contrairement au TF-IDF classique, BM25 normalise les scores de fréquence des termes en fonction de la longueur du document. Les documents plus longs sont plus susceptibles de contenir un terme donné et présentent donc des valeurs de fréquence de terme plus élevées [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1245)

BM25 et ses variantes (BM25+, BM25F) sont encore largement utilisés dans l'industrie et constituent d'excellentes bases de comparaison avec les algorithmes de recherche modernes et plus sophistiqués, tels que la recherche basée sur l'intégration, que nous aborderons ci-après. [7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1246)

J'ai passé sous silence un processus que j'ai survolé : la tokenisation, c'est-à-dire la décomposition d'une requête en termes individuels. La méthode la plus simple consiste à diviser la requête en mots, en traitant chaque mot comme un terme distinct. Cependant, cela peut conduire à la décomposition de termes composés en mots individuels, leur faisant perdre leur sens initial. Par exemple, « hot dog » serait décomposé en « hot » et « dog ». Dans ce cas, aucun des deux ne conserve le sens du terme original. Une solution pour atténuer ce problème est de traiter les n-grammes les plus fréquents comme des termes. Si le bigramme « hot dog » est fréquent, il sera traité comme un terme.

De plus, vous pouvez convertir tous les caractères en minuscules, supprimer la ponctuation et éliminer les mots vides (comme « le », « et », « est », etc.). Les solutions de recherche par termes gèrent souvent ces opérations automatiquement. Les logiciels de TALN classiques, tels que [NLTK](https://www.nltk.org/) (Natural Language Toolkit), [spaCy](https://github.com/explosion/spaCy) et [CoreNLP de Stanford](https://github.com/stanfordnlp/CoreNLP) , offrent également des fonctionnalités de tokenisation.

[Le chapitre 4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) aborde la mesure de la similarité lexicale entre deux textes à partir de leur chevauchement de n-grammes. Peut-on extraire des documents en fonction de leur degré de chevauchement de n-grammes avec la requête ? Oui. Cette approche est optimale lorsque la requête et les documents ont une longueur similaire. Si les documents sont beaucoup plus longs que la requête, la probabilité qu'ils contiennent les n-grammes de cette dernière augmente, ce qui conduit à des scores de chevauchement élevés pour de nombreux documents. Il devient alors difficile de distinguer les documents pertinents des documents moins pertinents.

### Récupération basée sur l'intégration

La recherche par termes calcule la pertinence au niveau lexical plutôt qu'au niveau sémantique. Comme indiqué au [chapitre 3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) , l'apparence d'un texte ne reflète pas nécessairement son sens. Cela peut entraîner le retour de documents non pertinents. Par exemple, une requête sur « architecture des transformateurs » pourrait renvoyer des documents concernant l'appareil électrique ou le film _Transformers_ . En revanche, _les moteurs de recherche basés sur l'intégration sémantique_ visent à classer les documents en fonction de leur adéquation sémantique à la requête. Cette approche est également connue sous le nom _de recherche sémantique_ .

Avec la récupération basée sur l'intégration, l'indexation a une fonction supplémentaire : convertir les blocs de données originaux en intégrations.La base de données où sont stockés les vecteurs générés est appelée _base de données vectorielles_ . L'interrogation se compose alors de deux étapes, comme illustré à [la figure 6-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_3_1730157386529243) :

1. Modèle d'intégration : convertir la requête en une intégration en utilisant le même modèle d'intégration que celui utilisé lors de l'indexation.
    
2. Récupérateur : extrait _k_ blocs de données dont les représentations vectorielles sont les plus proches de celle de la requête, selon le récupérateur. Le nombre de blocs de données à extraire, _k_ , dépend du cas d’utilisation, du modèle génératif et de la requête.
    

![Diagramme d'un modèle. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0603.png)

###### Figure 6-3. Vue d'ensemble du fonctionnement d'un récupérateur basé sur l'embedding, ou récupérateur sémantique.

Le flux de travail de recherche basé sur l'intégration présenté ici est simplifié. Les systèmes de recherche sémantique réels peuvent contenir d'autres composants, tels qu'un module de réordonnancement pour réordonner tous les candidats récupérés, et des caches pour réduire la latence. [8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1251)

Avec la recherche par plongement, on retrouve les plongements, abordés au [chapitre 3.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) Pour rappel, un plongement est généralement un vecteur qui vise à préserver les propriétés importantes des données originales. Un système de recherche par plongement est inefficace si le modèle de plongement est de mauvaise qualité.

La recherche par plongement introduit également un nouveau composant : les bases de données vectorielles. Une base de données vectorielle stocke des vecteurs. Cependant, le stockage est la partie la plus simple. La difficulté réside dans la recherche vectorielle. À partir d'un plongement de requête, une base de données vectorielle doit trouver les vecteurs les plus proches de la requête et les renvoyer. Les vecteurs doivent être indexés et stockés de manière à optimiser la rapidité et l'efficacité de la recherche.

Comme de nombreux autres mécanismes essentiels aux applications d'IA générative, la recherche vectorielle n'est pas exclusive à l'IA générative. Elle est courante dans toute application utilisant des représentations vectorielles : recherche, recommandation, organisation des données, extraction d'informations, clustering, détection de fraude, etc.

La recherche vectorielle est généralement formulée comme un problème de recherche des plus proches voisins. Par exemple, étant donné une requête, trouver les _k_ vecteurs les plus proches.La solution naïve est celle des k plus proches voisins (k-NN), qui fonctionne comme suit :

1. Calculer les scores de similarité entre l'intégration de la requête et tous les vecteurs de la base de données, en utilisant des métriques telles que la similarité cosinus.
    
2. Classez tous les vecteurs selon leur score de similarité.
    
3. Renvoie _les k_ vecteurs ayant les scores de similarité les plus élevés.
    

Cette solution simpliste garantit des résultats précis, mais elle est gourmande en ressources de calcul et lente. Elle ne devrait être utilisée que pour de petits ensembles de données.

Pour les grands ensembles de données, la recherche vectorielle est généralement effectuée à l'aide d'un algorithme de recherche par plus proches voisins approximatifs (RNA). Compte tenu de l'importance de la recherche vectorielle, de nombreux algorithmes et bibliothèques ont été développés à cet effet. Parmi les bibliothèques de recherche vectorielle les plus populaires, on peut citer _FAISS_ (Facebook AI Similarity Search) ( [Johnson et al., 2017](https://arxiv.org/abs/1702.08734) ), _ScaNN_ (Scalable Nearest Neighbors) de Google ( [Sun et al., 2020](https://oreil.ly/faJqj) ), [_Annoy_](https://github.com/spotify/annoy) [de Spotify](https://github.com/spotify/annoy) (Bernhardsson, 2013) et [_Hnswlib_](https://oreil.ly/4ATBC) ( [Hierarchical Navigable Small World](https://github.com/nmslib/hnswlib) ) (Malkov et Yashunin, 2016).

La plupart des développeurs d'applications n'implémentent pas eux-mêmes la recherche vectorielle ; je me contenterai donc de présenter brièvement les différentes approches. Cet aperçu pourra vous être utile lors de l'évaluation des solutions.

En général, les bases de données vectorielles organisent les vecteurs en compartiments, arbres ou graphes. Les algorithmes de recherche vectorielle diffèrent selon les heuristiques qu'ils utilisent pour maximiser la probabilité que des vecteurs similaires soient proches les uns des autres. Les vecteurs peuvent également être quantifiés (précision réduite) ou rendus creux. L'idée est que les vecteurs quantifiés et creux sont moins gourmands en ressources de calcul. Pour en savoir plus sur la recherche vectorielle, Zilliz propose une excellente [série de](https://oreil.ly/MVsgB) tutoriels. Voici quelques algorithmes de recherche vectorielle importants :

LSH (hachage sensible à la localité) ( [Indyk et Motwani, 1999](https://oreil.ly/slO9x) )

Il s'agit d'un algorithme puissant et polyvalent qui fonctionne avec bien plus que de simples vecteurs. Il consiste à hacher les vecteurs similaires dans les mêmes compartiments afin d'accélérer la recherche de similarités, au détriment de la précision. Il est implémenté dans FAISS et Annoy.

HNSW (Hierarchical Navigable Small World) ( [Malkov et Yashunin, 2016](https://github.com/nmslib/hnswlib) )

HNSW construit un graphe multicouche où les nœuds représentent des vecteurs et les arêtes relient les vecteurs similaires, permettant ainsi la recherche des plus proches voisins par parcours des arêtes. Son implémentation par les auteurs est open source et est également implémentée dans FAISS et Milvus.

Quantification du produit ( [Jégou et al., 2011](https://oreil.ly/VaLf4) )

Cette méthode consiste à réduire chaque vecteur à une représentation beaucoup plus simple et de dimension inférieure en le décomposant en plusieurs sous-vecteurs. Les distances sont ensuite calculées à partir de ces représentations de dimension inférieure, beaucoup plus rapides à manipuler. La quantification par produit est un élément clé de FAISS et est prise en charge par la quasi-totalité des bibliothèques de recherche vectorielle courantes.

FIV (index de fichiers inversé) ( [Sivic et Zisserman, 2003](https://oreil.ly/9BcYN) )

IVF utilise l'algorithme de clustering K-means pour regrouper les vecteurs similaires au sein d'un même cluster. En fonction du nombre de vecteurs dans la base de données, on définit généralement le nombre de clusters de manière à ce que chaque cluster contienne en moyenne entre 100 et 10 000 vecteurs. Lors d'une requête, IVF identifie les centroïdes des clusters les plus proches de l'espace vectoriel de la requête, et les vecteurs appartenant à ces clusters deviennent des voisins potentiels. Associé à la quantification du produit, IVF constitue la base de FAISS.

Agacer (Voisins les plus proches approximatifs Oh oui) ( [Bernhardsson, 2013](https://github.com/spotify/annoy) )

Annoy est une approche arborescente. Elle construit plusieurs arbres binaires, chacun divisant les vecteurs en clusters selon des critères aléatoires, comme le tracé aléatoire d'une ligne et la division des vecteurs en deux branches le long de cette ligne. Lors d'une recherche, elle parcourt ces arbres pour identifier les voisins potentiels. Spotify a publié son implémentation en open source.

Il existe d'autres algorithmes, tels que [SPTAG](https://github.com/microsoft/SPTAG) (Space Partition Tree And Graph) de Microsoft et [FLANN](https://github.com/flann-lib/flann) (Fast Library for Approximate Nearest Neighbors).

Bien que les bases de données vectorielles aient émergé comme une catégorie à part entière avec l'avènement des RAG (Random Aggregation), toute base de données capable de stocker des vecteurs peut être qualifiée de base de données vectorielle. De nombreuses bases de données traditionnelles ont été étendues, ou le seront prochainement, pour prendre en charge le stockage et la recherche de vecteurs.

### Comparaison des algorithmes de recherche

Grâce à sa longue histoire, la recherche d'informations, avec ses nombreuses solutions éprouvées, facilite la mise en œuvre de la recherche par termes et par plongement lexical. Chaque approche présente ses avantages et ses inconvénients.

La recherche par termes est généralement beaucoup plus rapide que la recherche par plongement lexical, tant pour l'indexation que pour l'interrogation. L'extraction des termes est plus rapide que la génération des plongements, et l'association d'un terme aux documents qui le contiennent peut s'avérer moins coûteuse en calcul qu'une recherche par plus proche voisin.

La recherche par termes fonctionne également très bien d'emblée. Des solutions comme Elasticsearch et BM25 ont permis à de nombreuses applications de recherche et d'extraction de données de proscrire. Cependant, leur simplicité implique aussi un nombre réduit de composants personnalisables pour optimiser leurs performances.

En revanche, la recherche par représentation vectorielle peut être considérablement améliorée au fil du temps et surpasser la recherche par termes. Il est possible d'affiner le modèle de représentation vectorielle et le moteur de recherche, séparément, conjointement ou en association avec le modèle génératif. Toutefois, la conversion des données en représentations vectorielles peut masquer certains mots clés, tels que des codes d'erreur spécifiques, par exemple EADDRNOTAVAIL (99), ou des noms de produits, ce qui complique leur recherche ultérieure. Cette limitation peut être surmontée en combinant la recherche par représentation vectorielle avec la recherche par termes, comme expliqué plus loin dans ce chapitre.

La qualité d'un système de récupération peut être évaluée en fonction de la qualité des données qu'il récupère. Deux métriques souvent utilisées par les cadres d'évaluation RAG sont la précision et _le rappel_ _contextuels_ (la précision contextuelle est également appelée _pertinence contextuelle)._
```
Précision du contexte

	Parmi tous les documents récupérés, quel pourcentage est pertinent pour la requête ?

Rappel du contexte

	Parmi tous les documents pertinents pour la requête, quel pourcentage est récupéré ?
```

Pour calculer ces indicateurs, vous constituez un ensemble d'évaluation comprenant une liste de requêtes de test et un ensemble de documents. Pour chaque requête de test, vous annotez chaque document comme étant pertinent ou non. Cette annotation peut être réalisée par des humains ou par une intelligence artificielle. Vous calculez ensuite la précision et le rappel du système de recherche sur cet ensemble d'évaluation.

En production, certains frameworks RAG ne prennent en charge que la précision contextuelle, et non le rappel contextuel. Pour calculer le rappel contextuel d'une requête donnée, il est nécessaire d'annoter la pertinence de tous les documents de la base de données par rapport à cette requête. La précision contextuelle est plus simple à calculer : il suffit de comparer les documents extraits à la requête, ce qui peut être fait par un système d'intelligence artificielle.

Si vous vous souciez du classement des documents récupérés, par exemple si les documents les plus pertinents doivent être classés en premier, vous pouvez utiliser des métriques telles que [NDCG](https://en.wikipedia.org/wiki/Discounted_cumulative_gain) (gain cumulatif actualisé normalisé), [MAP](https://en.wikipedia.org/wiki/Evaluation_measures_\(information_retrieval\)#Mean_average_precision) (précision moyenne) et [MRR](https://en.wikipedia.org/wiki/Mean_reciprocal_rank) (rang réciproque moyen).

Pour la recherche sémantique, il est également nécessaire d'évaluer la qualité des plongements lexicaux. Comme expliqué au [chapitre 3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) , les plongements peuvent être évalués indépendamment : ils sont considérés comme bons si les documents les plus similaires ont des plongements plus proches. On peut aussi évaluer les plongements en fonction de leur performance pour des tâches spécifiques. Le benchmark [MTEB](https://arxiv.org/abs/2210.07316) (Muennighoff et al., 2023) évalue les plongements pour un large éventail de tâches, notamment la recherche, la classification et le clustering.

La qualité d'un outil de recherche doit également être évaluée dans le contexte de l'ensemble du système RAG. En définitive, un outil de recherche est performant s'il contribue à la génération de réponses de haute qualité. L'évaluation des résultats des modèles génératifs est abordée aux chapitres [3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) et [4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) .

L'intérêt d'un système de recherche sémantique performant dépend de l'importance accordée au coût et à la latence, notamment lors de la phase de requête. La latence des générateurs de nombres aléatoires (RAG) étant principalement due à la génération des résultats, surtout pour les résultats longs, _la latence supplémentaire liée à la génération des plongements lexicaux et à la recherche vectorielle peut être minime par rapport à la latence totale des RAG._ Toutefois, cette latence supplémentaire peut impacter l'expérience utilisateur.

Un autre point important est le coût. Générer des plongements lexicaux a un coût. Ce problème est particulièrement préoccupant si vos données évoluent fréquemment et nécessitent une régénération régulière des plongements. Imaginez devoir générer des plongements pour 100 millions de documents chaque jour ! Selon les bases de données vectorielles utilisées, le stockage et la recherche de vecteurs peuvent également s'avérer onéreux. Il n'est pas rare qu'une entreprise consacre un cinquième, voire la moitié, de son budget aux API de modèles vectoriels.

[Le tableau 6-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_table_2_1730157386543401) présente une comparaison côte à côte de la recherche basée sur les termes et de la recherche basée sur l'intégration.

Tableau 6-2. Recherche basée sur les termes et recherche sémantique par vitesse, performance et coût.



|                    | Recherche par terme                                                                                                                                                                   | Embedding-based retrieval                                                                                                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Vitesse de requête | Bien plus rapide que la récupération basée sur l'intégration                                                                                                                          | La génération de plongements de requêtes et la recherche vectorielle peuvent être lentes.                                                                                                      |
| Performance        | Performances généralement excellentes dès la première utilisation, mais difficiles à améliorer.  <br>  <br>Peut récupérer des documents erronés en raison d'une ambiguïté des termes. | Peut surpasser la recherche par termes grâce à un réglage fin.  <br>  <br>Permet l'utilisation de requêtes plus naturelles, car elle se concentre sur la sémantique plutôt que sur les termes. |
| Coût               | Bien moins cher que la recherche basée sur l'intégration                                                                                                                              | Les solutions d'intégration, de stockage vectoriel et de recherche vectorielle peuvent s'avérer coûteuses.                                                                                     |

Avec les systèmes de recherche d'informations, il est possible de faire des compromis entre l'indexation et l'interrogation. Plus l'index est détaillé, plus la recherche sera précise, mais l'indexation sera plus lente et plus gourmande en mémoire. Prenons l'exemple de la création d'un index de clients potentiels. Ajouter des informations (nom, entreprise, courriel, téléphone, centres d'intérêt, etc.) facilite la recherche de personnes pertinentes, mais allonge le temps de création et nécessite davantage d'espace de stockage.

En général, un index détaillé comme HNSW offre une grande précision et des temps de requête rapides, mais sa création est gourmande en temps et en mémoire. À l'inverse, un index plus simple comme LSH est plus rapide et moins gourmand en mémoire à créer, mais les requêtes sont alors plus lentes et moins précises.

Le [site web ANN-Benchmarks](https://oreil.ly/pbh3y) compare différents algorithmes de réseaux de neurones artificiels (RNA) sur plusieurs ensembles de données à l'aide de quatre principaux indicateurs, en tenant compte des compromis entre indexation et interrogation. Ces indicateurs sont les suivants :
```
Rappel

	La fraction des plus proches voisins trouvés par l'algorithme.

Requête par seconde (QPS)

	Le nombre de requêtes que l'algorithme peut traiter par seconde. Ceci est crucial pour les applications à fort trafic.

Temps de construction

	Le temps nécessaire à la création de l'index. Cette métrique est particulièrement importante si vous devez fréquemment mettre à jour votre index (par exemple, en raison de modifications de vos données).

Taille de l'index

	La taille de l'index créé par l'algorithme est cruciale pour évaluer son évolutivité et ses besoins en stockage.
```

De plus, BEIR (Benchmarking IR) ( [Thakur et al., 2021](https://arxiv.org/abs/2104.08663) ) est un outil d'évaluation des systèmes de recherche d'information. Il prend en charge les systèmes de recherche d'information selon 14 référentiels de recherche d'information courants.

En résumé, la qualité d'un système RAG doit être évaluée composant par composant et de bout en bout. Pour ce faire, vous devez procéder comme suit :

1. Évaluer la qualité de la récupération.
    
2. Évaluer les résultats finaux du système RAG.
    
3. Évaluer les plongements (pour la recherche basée sur les plongements).
    

### Combinaison d'algorithmes de recherche

Compte tenu des avantages distincts des différents algorithmes de recherche, un système de recherche en production combine généralement plusieurs approches. La combinaison de la recherche par termes et de la recherche par plongement est appelée _recherche hybride_ .

Différents algorithmes peuvent être utilisés successivement. Tout d'abord, un algorithme de recherche peu coûteux et moins précis, tel qu'un système basé sur les termes, extrait les candidats. Ensuite, un mécanisme plus précis mais plus coûteux, tel que l'algorithme des k plus proches voisins, sélectionne le meilleur de ces candidats. Cette seconde étape est également appelée _réordonnancement_ .

Par exemple, avec le terme « transformateur », vous pouvez récupérer tous les documents contenant ce mot, qu'ils traitent de l'appareil électrique, de l'architecture neuronale ou du film. Ensuite, vous utilisez la recherche vectorielle pour trouver, parmi ces documents, ceux qui sont pertinents pour votre requête. Autre exemple : la requête « Qui est responsable de la plupart des ventes à X ? ». Vous pouvez d'abord récupérer tous les documents associés à X à l'aide du mot-clé X. Ensuite, vous utilisez la recherche vectorielle pour retrouver le contexte associé à la question « Qui est responsable de la plupart des ventes ? ».

Différents algorithmes peuvent être utilisés en parallèle, formant ainsi un ensemble. N'oubliez pas qu'un moteur de recherche classe les documents selon leur pertinence par rapport à la requête. Vous pouvez utiliser plusieurs moteurs de recherche pour extraire simultanément des candidats, puis combiner ces différents classements afin d'obtenir un classement final.

Un algorithme permettant de combiner différents classements est appelé [fusion de classement réciproque (RRF)](https://oreil.ly/3xtwh) (Cormack et al., 2009). Il attribue à chaque document un score en fonction de son classement par un moteur de recherche. Intuitivement, si un document est classé premier, son score est de 1/1 = 1. S'il est classé deuxième, son score est de ½ = 0,5. Plus son classement est élevé, plus son score est élevé.

Le score final d'un document correspond à la somme de ses scores obtenus auprès de tous les moteurs de recherche. Si un document est classé premier par un moteur et deuxième par un autre, son score est de 1 + 0,5 = 1,5. Cet exemple simplifie le principe de la recherche de documents (RRF), mais il en illustre les bases. La formule réelle pour un document _D_ est plus complexe :

$$
Score(D) = \sum^{n}_{i=1} \frac{1}{k+r_i(D)}
$$
- _n_ représente le nombre de listes classées ; chaque liste classée est produite par un récupérateur.
- $r_i$ est le rang du document par le récupérateur _i_ .
- _k_ est une constante permettant d'éviter la division par zéro et de contrôler l'influence des documents de rang inférieur. Une valeur typique de _k_ est 60.

## Optimisation de la récupération

Selon la tâche, certaines tactiques peuvent augmenter les chances de trouver les documents pertinents. Quatre tactiques sont abordées ici : le découpage en segments, le réordonnancement, la réécriture de requêtes et la recherche contextuelle.

### stratégie de découpage

L'indexation de vos données dépend de la manière dont vous comptez les récupérer ultérieurement. La section précédente abordait différents algorithmes de recherche et leurs stratégies d'indexation respectives. Dans cette section, nous partions du principe que les documents étaient déjà découpés en segments gérables. Nous allons maintenant examiner différentes stratégies de découpage. Ce choix est crucial, car la stratégie de découpage utilisée peut avoir un impact significatif sur les performances de votre système de recherche.

La stratégie la plus simple consiste à découper les documents en segments de longueur égale selon une unité de mesure. Les unités courantes sont les caractères, les mots, les phrases et les paragraphes. Par exemple, vous pouvez diviser chaque document en segments de 2 048 caractères ou 512 mots. Vous pouvez également découper chaque document de sorte que chaque segment contienne un nombre fixe de phrases (par exemple, 20 phrases) ou de paragraphes (chaque paragraphe constituant alors un segment distinct).

Vous pouvez également diviser les documents de manière récursive en utilisant des unités de plus en plus petites jusqu'à ce que chaque segment respecte la taille maximale autorisée. Par exemple, vous pouvez commencer par diviser un document en sections. Si une section est trop longue, divisez-la en paragraphes. Si un paragraphe est encore trop long, divisez-le en phrases. Cela réduit le risque que des passages liés soient coupés arbitrairement.

Certains documents peuvent également se prêter à des stratégies de segmentation créatives. Par exemple, il existe [des outils de segmentation](https://github.com/grantjenks/py-tree-sitter-languages#license) conçus spécifiquement pour différents langages de programmation. Les documents de questions-réponses peuvent être segmentés par paires question/réponse, chaque paire constituant un segment. Les textes chinois peuvent nécessiter une segmentation différente de celle des textes anglais.

Lorsqu'un document est divisé en segments sans chevauchement, ces segments peuvent être tronqués en plein milieu d'un contexte important, entraînant la perte d'informations cruciales. Prenons l'exemple du texte « J'ai laissé un mot à ma femme ». S'il est divisé en « J'ai laissé ma femme » et « un mot », aucun de ces deux segments ne transmet l'information clé du texte original. Le chevauchement garantit que les informations importantes relatives aux limites sont incluses dans au moins un segment. Si vous définissez la taille des segments à 2 048 caractères, vous pouvez par exemple définir la taille du chevauchement à 20 caractères.

La taille des segments ne doit pas dépasser la longueur maximale du contexte du modèle génératif. Dans le cas de l'approche par plongement, la taille des segments ne doit pas non plus dépasser la limite de contexte du modèle de plongement.

Vous pouvez également segmenter les documents en utilisant des jetons, déterminés par le tokenizer du modèle génératif. Supposons que vous souhaitiez utiliser Llama 3 comme modèle génératif. Vous commencez alors par tokeniser les documents à l'aide du tokenizer de Llama 3. Vous pouvez ensuite diviser les documents en segments en utilisant les jetons comme limites. Le segmentage par jetons facilite l'utilisation avec les modèles en aval. Cependant, l'inconvénient de cette approche est que si vous passez à un autre modèle génératif avec un tokenizer différent, vous devrez réindexer vos données.

Quelle que soit la stratégie choisie, la taille des segments est importante. Des segments plus petits permettent d'intégrer des informations plus diversifiées. Cela signifie également que vous pouvez en inclure davantage dans le modèle. En divisant par deux la taille des segments, vous pouvez en inclure deux fois plus. Un plus grand nombre de segments fournit au modèle un éventail d'informations plus large, ce qui peut lui permettre de produire une meilleure réponse.

Cependant, des segments trop petits peuvent entraîner la perte d'informations importantes. Prenons l'exemple d'un document contenant des informations essentielles sur le sujet X, mais dont le sujet n'est abordé que dans la première moitié. Si vous divisez ce document en deux segments, la seconde moitié risque de ne pas être récupérée, et le modèle ne pourra donc pas exploiter ses informations.

Des segments de taille réduite peuvent également augmenter la charge de calcul. Ce problème est particulièrement préoccupant pour la recherche par plongement. Diviser par deux la taille des segments signifie qu'il y a deux fois plus de segments à indexer et deux fois plus de vecteurs de plongement à générer et à stocker. L'espace de recherche vectoriel sera donc deux fois plus grand, ce qui peut ralentir les requêtes.

Il n'existe pas de taille de segment ou de chevauchement idéale universelle. Il faut faire des essais pour trouver ce qui vous convient le mieux.

### Reranking

Le classement initial des documents généré par le moteur de recherche peut être affiné pour plus de précision. Ce réordonnancement est particulièrement utile pour réduire le nombre de documents extraits, soit pour les adapter au contexte de votre modèle, soit pour diminuer le nombre de jetons d'entrée.

Un schéma courant de réordonnancement est présenté dans [« Combinaison d'algorithmes de recherche »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_combining_retrieval_algorithms_1730157386571869) . Un algorithme de recherche peu coûteux mais moins précis récupère les candidats, puis un mécanisme plus précis mais plus coûteux réordonne ces candidats.

Les documents peuvent également être réorganisés en fonction de la date, les données les plus récentes étant privilégiées. Cette fonctionnalité est utile pour les applications sensibles au facteur temps, telles que l'agrégation d'actualités, la messagerie instantanée (par exemple, un chatbot capable de répondre à des questions sur vos e-mails) ou l'analyse boursière.

Le réordonnancement contextuel diffère du réordonnancement traditionnel des résultats de recherche en ce que la position exacte des éléments est moins cruciale. Dans la recherche, le rang (par exemple, premier ou cinquième) est essentiel. Dans le réordonnancement contextuel, l'ordre des documents reste important car il influence la capacité du modèle à les traiter. Les modèles peuvent mieux comprendre les documents situés au début et à la fin du contexte, comme expliqué dans la [section « Longueur et efficacité du contexte »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_context_length_and_context_efficiency_1730156991195850) . Cependant, tant qu'un document est inclus, l'impact de son ordre est moins significatif que pour le classement dans la recherche.

### Réécriture de requêtes

_La réécriture de requêtes_ est également appelée reformulation de requêtes, normalisation de requêtes, et parfois expansion de requêtes. Prenons l'exemple de la conversation suivante :
```
_Utilisateur_ : Quand John Doe a-t-il acheté quelque chose chez nous pour la dernière fois ?
 _IA_ : John a acheté un chapeau Fedora Fruity chez nous il y a deux semaines, le 3 janvier.
2030.
_Utilisateur_ : Et Emily Doe ?
 ```           

La dernière question, « Qu'en est-il d'Emily Doe ? », est ambiguë hors contexte. Si vous utilisez cette requête telle quelle pour récupérer des documents, vous obtiendrez probablement des résultats non pertinents. Vous devez la reformuler pour qu'elle reflète la véritable question de l'utilisateur. La nouvelle requête doit être compréhensible par elle-même. Dans ce cas, la requête devrait être reformulée comme suit : « Quand Emily Doe a-t-elle effectué son dernier achat chez nous ? »

Bien que j'aie inclus la réécriture de requêtes dans [« RAG »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_1730157386571628) , cette fonctionnalité n'est pas exclusive à RAG. Dans les moteurs de recherche traditionnels, la réécriture de requêtes repose souvent sur des heuristiques. Dans les applications d'IA, elle peut également être réalisée à l'aide d'autres modèles d'IA, en utilisant une consigne du type : « À partir de la conversation suivante, réécrivez la dernière saisie de l'utilisateur afin qu'elle reflète sa question réelle. »[La figure 6-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_4_1730157386529250) montre comment ChatGPT a réécrit la requête en utilisant cette invite.

![Capture d'écran d'une conversation. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0604.png)

###### Figure 6-4. Vous pouvez utiliser d'autres modèles génératifs pour réécrire les requêtes.

La réécriture de requêtes peut se complexifier, notamment lorsqu'il est nécessaire de résoudre l'identité d'un individu ou d'intégrer d'autres informations. Par exemple, si l'utilisateur demande « Et sa femme ? », il faudra d'abord interroger la base de données pour identifier son épouse. Si cette information est introuvable, le modèle de réécriture doit reconnaître que la requête est insoluble au lieu de proposer un nom, ce qui conduirait à une réponse erronée.

### Récupération contextuelle

Le principe de la recherche contextuelle est d'enrichir chaque segment de données avec un contexte pertinent afin de faciliter sa récupération. Une technique simple consiste à ajouter des métadonnées, comme des étiquettes et des mots-clés, à un segment. Dans le domaine du e-commerce, un produit peut être enrichi par sa description et les avis des utilisateurs. Les images et les vidéos peuvent être recherchées par leurs titres ou leurs légendes.

Les métadonnées peuvent également inclure des entités extraites automatiquement du segment. Si votre document contient des termes spécifiques comme le code d'erreur EADDRNOTAVAIL (99), leur ajout aux métadonnées du document permet au système de le retrouver par ce mot-clé, même après sa conversion en vecteurs.

Vous pouvez également enrichir chaque section avec les questions auxquelles elle peut répondre. Pour le support client, vous pouvez ajouter à chaque article des questions connexes. Par exemple, l'article expliquant comment réinitialiser son mot de passe peut être enrichi de requêtes telles que « Comment réinitialiser mon mot de passe ? », « J'ai oublié mon mot de passe », « Je n'arrive pas à me connecter » ou encore « À l'aide ! Je ne trouve pas mon compte » [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1296)

Si un document est divisé en plusieurs segments, certains d'entre eux peuvent manquer du contexte nécessaire pour permettre au système de recherche de comprendre leur contenu. Pour éviter cela, vous pouvez enrichir chaque segment avec le contexte du document original, comme son titre et son résumé.Anthropic a utilisé des modèles d'IA pour générer un court contexte, généralement de 50 à 100 mots, expliquant le segment de texte et son lien avec le document original. Voici l'invite utilisée par Anthropic à cette fin ( [Anthropic, 2024](https://oreil.ly/-Sny7) ) :

```
<document> 
{{WHOLE_DOCUMENT}} 
</document>

Here is the chunk we want to situate within the whole document: 

<chunk>
{{CHUNK_CONTENT}}
</chunk> 

Please give a short succinct context to situate this chunk within the overall 
document for the purposes of improving search retrieval of the chunk. Answer 
only with the succinct context and nothing else.



```

     

Le contexte généré pour chaque segment est ajouté au début de celui-ci, puis le segment ainsi enrichi est indexé par l'algorithme de recherche. [La figure 6-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_5_1730157386529262) illustre le processus suivi par Anthropic.

![Diagramme d'un processus. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0605.png)

###### Figure 6-5. Anthropic ajoute à chaque segment un bref contexte qui le situe dans le document original, facilitant ainsi la recherche des segments pertinents. Image extraite de « Introducing Contextual Retrieval » (Anthropic, 2024).

# Évaluation des solutions de récupération

Voici quelques facteurs clés à prendre en compte lors de l'évaluation d'une solution de récupération :

- Quels mécanismes de recherche prend-il en charge ? Prend-il en charge la recherche hybride ?
    
- S'il s'agit d'une base de données vectorielles, quels modèles d'intégration et algorithmes de recherche vectorielle prend-elle en charge ?
    
- Dans quelle mesure est-il évolutif, tant en termes de stockage de données que de trafic de requêtes ? Est-il adapté à vos modèles de trafic ?
    
- Combien de temps faut-il pour indexer vos données ? Quelle quantité de données pouvez-vous traiter (ajout/suppression, par exemple) en une seule fois ?
    
- Quel est son temps de latence de requête pour différents algorithmes de récupération ?
    
- S'il s'agit d'une solution gérée, quelle est sa structure tarifaire ? Est-elle basée sur le volume de documents/vecteurs ou sur le volume de requêtes ?
    

Cette liste n'inclut pas les fonctionnalités généralement associées aux solutions d'entreprise telles que le contrôle d'accès, la conformité, la séparation du plan de données et du plan de contrôle, etc..

## RAG Au-delà des textes

La section précédente traitait des systèmes RAG textuels où les sources de données externes sont des documents textuels. Cependant, les sources de données externes peuvent également être des données multimodales et tabulaires.

### RAG multimodal

Si votre générateur est multimodal, ses contextes peuvent être enrichis non seulement de documents textuels, mais aussi d'images, de vidéos, d'audio, etc., provenant de sources externes. J'utiliserai des images dans les exemples pour plus de concision, mais vous pouvez les remplacer par toute autre modalité.Étant donné une requête, le module de recherche récupère à la fois les textes et les images pertinents. Par exemple, pour la requête « Quelle est la couleur de la maison dans le film Pixar Là-haut ? », le module peut récupérer une image de la maison du _film Là-haut_ pour aider le modèle à répondre, comme illustré dans [la figure 6-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_6_1730157386529270) .

![Diagramme d'un diagramme. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0606.png)

###### Figure 6-6. RAG multimodal peut enrichir une requête avec du texte et des images. (*L'image originale du _film Là-haut_ n'est pas utilisée pour des raisons de droits d'auteur.)

Si les images possèdent des métadonnées (titres, étiquettes et légendes, par exemple), elles peuvent être récupérées grâce à ces métadonnées. Ainsi, une image est récupérée si sa légende est jugée pertinente pour la requête.

Pour récupérer des images en fonction de leur contenu, il vous faudra un moyen de comparer ces images aux requêtes. Si les requêtes sont des textes, vous aurez besoin d'un modèle d'intégration multimodal capable de générer des représentations vectorielles pour les images et les textes.Supposons que vous utilisiez CLIP ( [Radford et al., 2021](https://arxiv.org/abs/2103.00020) ) comme modèle d'intégration multimodale. Le processus de récupération fonctionne comme suit :

1. Générez des vecteurs CLIP pour toutes vos données, textes et images, et stockez-les dans une base de données vectorielle.
    
2. Étant donné une requête, générez son embedding CLIP.
    
3. Interroger la base de données vectorielles pour obtenir toutes les images et tous les textes dont les représentations vectorielles sont proches de la représentation vectorielle de la requête.
    

### RAG avec données tabulaires

La plupart des applications fonctionnent non seulement avec des données non structurées comme des textes et des images, mais aussi avec des données tabulaires. De nombreuses requêtes peuvent nécessiter des informations issues de tables de données pour répondre. Le processus d'enrichissement du contexte à l'aide de données tabulaires diffère sensiblement du processus RAG classique.

Imaginez que vous travaillez pour un site de commerce électronique appelé Kitty Vogue, spécialisé dans la mode féline. Ce magasin possède une table de commandes nommée Ventes, comme indiqué dans [le tableau 6-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_table_3_1730157386543408) .

Tableau 6-3. Un exemple de tableau de commandes, Ventes, pour le site de commerce électronique fictif Kitty Vogue.

|Numéro de commande|Horodatage|ID du produit|Produit|Prix ​​unitaire ($)|Unités|Total|
|---|---|---|---|---|---|---|
|1|…|2044|Assaisonnement Meow Mix|10,99|1|10,99|
|2|…|3492|Ronronnement et secousse|25|2|50|
|3|…|2045|Fedora fruité|18|1|18|
|…|…|…|…|…|…|…|

Pour répondre à la question « Combien d'unités de Fruity Fedora ont été vendues ces 7 derniers jours ? », votre système doit interroger cette table pour toutes les commandes contenant du Fruity Fedora et additionner le nombre d'unités vendues. Supposons que cette table puisse être interrogée en SQL. La requête SQL pourrait ressembler à ceci :

```sql
SELECT SUM(units) AS total_units_sold

FROM Sales

WHERE product_name = 'Fruity Fedora'

AND timestamp >= DATE_SUB(CURDATE(), INTERVAL 7 DAY);

```



Le flux de travail est le suivant, illustré dans [la figure 6-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_7_1730157386529276) . Pour exécuter ce flux de travail, votre système doit être capable de générer et d'exécuter la requête SQL :

1. Conversion de texte en SQL : à partir de la requête utilisateur et des schémas de table fournis, déterminer la requête SQL nécessaire. La conversion de texte en SQL est un exemple d’analyse sémantique, comme expliqué au [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) .
    
2. Exécution SQL : exécuter la requête SQL.
    
3. Génération : générer une réponse basée sur le résultat SQL et la requête utilisateur d'origine.
    

![Diagramme d'un produit. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0607.png)

###### Figure 6-7. Un système RAG qui enrichit le contexte avec des données tabulaires.

Pour l'étape de conversion de texte en SQL, si de nombreuses tables sont disponibles et que leurs schémas ne peuvent pas tous s'intégrer au contexte du modèle, une étape intermédiaire peut s'avérer nécessaire pour prédire les tables à utiliser pour chaque requête. Cette conversion peut être effectuée par le même générateur que celui qui produit la réponse finale, ou par un modèle dédié.

Dans cette section, nous avons vu comment des outils tels que les récupérateurs et les exécuteurs SQL permettent aux modèles de traiter davantage de requêtes et de générer des réponses de meilleure qualité. L'accès à davantage d'outils pour un modèle améliorerait-il encore ses capacités ? L'utilisation d'outils est une caractéristique fondamentale du modèle agentique, que nous aborderons dans la section suivante.section.

# Agents

Les agents intelligents sont considérés par beaucoup comme l'objectif ultime de l'IA. L'ouvrage de référence de Stuart Russell et Peter Norvig, * _Artificial Intelligence: A Modern Approach*_ (Prentice Hall, 1995), définit le domaine de _la recherche en intelligence artificielle_ comme « l'étude et la conception d'agents rationnels ».

Les capacités sans précédent des modèles de base ont ouvert la voie à des applications agentielles auparavant inimaginables. Ces nouvelles capacités permettent enfin de développer des agents autonomes et intelligents qui agissent comme nos assistants, collaborateurs et coachs. Ils peuvent nous aider à créer un site web, collecter des données, planifier un voyage, réaliser une étude de marché, gérer un compte client, automatiser la saisie de données, nous préparer aux entretiens d'embauche, interviewer des candidats, négocier un accord, etc. Les possibilités semblent infinies et la valeur économique potentielle de ces agents est considérable.

###### Avertissement

Les agents dotés d'intelligence artificielle constituent un domaine émergent, sans cadre théorique établi pour leur définition, leur développement et leur évaluation. Cette section représente une tentative, aussi ambitieuse soit-elle, d'élaborer un tel cadre à partir de la littérature existante ; toutefois, celui-ci évoluera au rythme des avancées du domaine. Par rapport au reste de l'ouvrage, cette section est plus expérimentale.

Cette section débutera par une présentation des agents, puis abordera deux aspects déterminants de leurs capacités : les outils et la planification. Les agents, avec leurs nouveaux modes de fonctionnement, présentent également de nouveaux modes de défaillance. Cette section se conclura par une discussion sur les méthodes d’évaluation des agents permettant de détecter ces défaillances.

Bien que les agents soient une nouveauté, ils reposent sur des concepts déjà abordés dans cet ouvrage, notamment l'autocritique, le raisonnement logique et les résultats structurés.

## Aperçu de l'agent

Le terme _« agent »_ a été utilisé dans de nombreux contextes d'ingénierie différents, notamment pour désigner un agent logiciel, un agent intelligent, un agent utilisateur, un agent conversationnel et un agent d'apprentissage par renforcement. Mais qu'est-ce qu'un agent, exactement ?

Un agent est tout être capable de percevoir son environnement et d'agir sur celui-ci. [Cela](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1313) signifie qu'un agent est caractérisé par l' _environnement_ dans lequel il évolue et _par l'ensemble des actions_ qu'il peut accomplir.

L' _environnement_ dans lequel un agent peut opérer est défini par son cas d'utilisation. Si un agent est développé pour jouer à un jeu (par exemple, _Minecraft,_ Go, _Dota_ ), ce jeu constitue son environnement. Si vous souhaitez qu'un agent extraie des documents d'Internet, son environnement est Internet. Si votre agent est un robot cuisinier, la cuisine représente son environnement. L'environnement d'un agent de véhicule autonome est le réseau routier et ses abords.

L' _ensemble des actions_ qu'un agent d'IA peut effectuer est enrichi par les _outils_ auxquels il a accès. De nombreuses applications d'IA générative que vous utilisez quotidiennement sont des agents disposant d'outils, même simplissimes. ChatGPT est un agent : il peut effectuer des recherches sur le Web, exécuter du code Python et générer des images. Les systèmes RAG sont des agents, et les extracteurs de texte, d'images et les exécuteurs SQL sont leurs outils.

Il existe une forte interdépendance entre l'environnement d'un agent et son ensemble d'outils. L'environnement détermine les outils qu'un agent peut potentiellement utiliser. Par exemple, dans un jeu d'échecs, les seules actions possibles pour un agent sont les coups valides. Cependant, l'inventaire d'outils d'un agent restreint l'environnement dans lequel il peut opérer. Par exemple, si la seule action d'un robot est la nage, il sera limité à un environnement aquatique.

[La figure 6-8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_8_1730157386529282) présente une visualisation de SWE-agent ( [Yang et al., 2024](https://arxiv.org/abs/2405.15793) ), un agent basé sur GPT-4. Son environnement est l'ordinateur, avec son terminal et son système de fichiers. Ses actions comprennent la navigation dans le dépôt, la recherche de fichiers, la visualisation des fichiers et la modification des lignes de code.

![Capture d'écran d'une interface informatique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0608.png)

###### Figure 6-8. L’agent SWE (Yang et al., 2024) est un agent de programmation dont l’environnement est l’ordinateur et dont les actions comprennent la navigation, la recherche et l’édition. Adapté d’une image originale sous licence CC BY 4.0.

Un agent d'IA est conçu pour accomplir des tâches généralement définies par les utilisateurs dans les entrées. Dans un agent d'IA, l'IA joue le rôle de cerveau : elle traite les informations reçues, notamment la tâche et les retours de l'environnement, planifie une séquence d'actions pour accomplir cette tâche et détermine si celle-ci a été réalisée.

Revenons au système RAG avec des données tabulaires dans l'exemple de Kitty Vogue. Il s'agit d'un agent simple avec trois actions : génération de la réponse, génération de la requête SQL et exécution de la requête SQL. Pour la requête « Projeter le chiffre d'affaires de Fruity Fedora pour les trois prochains mois », l'agent pourrait effectuer la séquence d'actions suivante :

1. Réfléchissez à la manière d'accomplir cette tâche. L'agent pourrait décider que, pour prévoir les ventes futures, il a d'abord besoin des chiffres de vente des cinq dernières années. Notez que son raisonnement est présenté comme sa réponse intermédiaire.
    
2. Lancez la génération de requêtes SQL pour générer la requête permettant d'obtenir les chiffres de vente des cinq dernières années.
    
3. Lancez l'exécution de requête SQL pour exécuter cette requête.
    
4. Analysez les résultats de l'outil et leur contribution à la prévision des ventes. Il se peut qu'il juge ces données insuffisantes pour établir une projection fiable, notamment en raison de valeurs manquantes. Il en déduit alors qu'il a également besoin d'informations sur les campagnes marketing précédentes.
    
5. Lancez la génération de requêtes SQL pour générer les requêtes des campagnes marketing passées.
    
6. Lancer l'exécution de la requête SQL.
    
7. On considère que ces nouvelles informations sont suffisantes pour aider à prévoir les ventes futures. Elles génèrent ensuite une projection.
    
8. Raison pour laquelle la tâche a été accomplie avec succès.
    

Comparativement aux cas d'utilisation sans agent, les agents nécessitent généralement des modèles plus puissants pour deux raisons :

- Erreurs cumulées : un agent doit souvent effectuer plusieurs étapes pour accomplir une tâche, et la précision globale diminue à mesure que le nombre d’étapes augmente. Si la précision du modèle est de 95 % par étape, elle chute à 60 % après 10 étapes et à seulement 0,6 % après 100 étapes.
    
- Enjeux plus importants : grâce à l’accès à des outils, les agents sont capables d’accomplir des tâches à plus fort impact, mais tout échec pourrait avoir des conséquences plus graves.
    

Une tâche complexe peut s'avérer longue et coûteuse. [Toutefois](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1315) , si les agents sont autonomes, ils permettent de gagner un temps précieux, justifiant ainsi leur coût.

Dans un environnement donné, la réussite d'un agent dépend des outils à sa disposition et de la puissance de son système de planification IA. Commençons par examiner les différents types d'outils qu'un modèle peut utiliser.

## Outils

Un système n'a pas besoin d'accéder à des outils externes pour fonctionner comme un agent. Cependant, sans ces outils, ses capacités seraient limitées. Un modèle, par lui-même, ne peut généralement effectuer qu'une seule action : par exemple, un modèle linéaire peut générer du texte et un générateur d'images peut générer des images. Les outils externes décuplent considérablement les capacités d'un agent.

Les outils permettent à un agent de percevoir son environnement et d'agir sur celui-ci. Les actions qui permettent à un agent de percevoir son environnement sont _des actions de lecture seule_ , tandis que celles qui lui permettent d'agir sur celui-ci sont _des actions d'écriture_ .

Cette section présente un aperçu des outils externes. Leur utilisation sera abordée dans [la section « Planification »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_planning_1730157386572280) .

L'ensemble des outils auxquels un agent a accès constitue son inventaire d'outils. Puisque cet inventaire détermine les actions possibles d'un agent, il est essentiel de bien réfléchir aux outils à lui fournir et à leur nombre. Plus un agent dispose d'outils, plus ses capacités sont étendues. Cependant, plus il y a d'outils, plus il est difficile de les comprendre et de les utiliser efficacement. L'expérimentation est donc nécessaire pour trouver l'ensemble d'outils adéquat, comme expliqué dans [la section « Sélection des outils »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_tool_selection_1730157386572520) .

Selon l'environnement de l'agent, de nombreux outils sont envisageables. Voici trois catégories d'outils à considérer : l'enrichissement des connaissances (construction du contexte), l'extension des capacités et les outils permettant à l'agent d'interagir avec son environnement.

### Augmentation des connaissances

J'espère que ce livre vous a jusqu'ici convaincu de l'importance du contexte pour évaluer la qualité des réponses d'un modèle. Parmi les outils essentiels, on trouve ceux qui permettent d'enrichir la connaissance que votre agent a de lui-même. Certains ont déjà été évoqués : la récupération de texte, la récupération d'images et l'exécution de requêtes SQL. D'autres outils potentiels incluent la recherche interne de personnes, une API d'inventaire fournissant le statut des produits, la récupération des conversations Slack, un lecteur de courriels, etc.

De nombreux outils de ce type enrichissent un modèle avec les processus et informations internes à votre organisation. Cependant, ils peuvent également donner accès aux modèles à des informations publiques, notamment sur Internet.

La navigation web figurait parmi les premières fonctionnalités les plus attendues pour les chatbots comme ChatGPT. Elle permet de maintenir un modèle à jour. Un modèle devient obsolète lorsque les données sur lesquelles il a été entraîné sont périmées. Si les données d'entraînement du modèle ont été interrompues la semaine dernière, il ne pourra pas répondre aux questions nécessitant des informations de la semaine en cours, à moins que ces informations ne soient fournies dans leur contexte. Sans navigation web, un modèle ne pourra pas vous renseigner sur la météo, l'actualité, les événements à venir, les cours de la bourse, l'état des vols, etc.

J'utilise le terme « navigation web » comme terme générique pour désigner tous les outils qui accèdent à Internet, y compris les navigateurs web et les API spécifiques telles que les API de recherche, les API d'actualités, les API GitHub ou les API de médias sociaux comme celles de X, LinkedIn et Reddit.

Si la navigation web permet à votre agent de consulter des informations à jour pour générer de meilleures réponses et réduire les hallucinations, elle peut aussi l'exposer aux dangers d'Internet. Choisissez vos API Internet avec soin.

### Extension des capacités

La deuxième catégorie d'outils à considérer concerne ceux qui pallient les limitations inhérentes aux modèles d'IA. Ce sont des moyens simples d'améliorer les performances de votre modèle. Par exemple, les modèles d'IA sont connus pour leurs difficultés en calcul. Si vous demandez à un modèle de calculer la division de 199 999 par 292, il y a de fortes chances qu'il échoue. Or, ce calcul est trivial si le modèle a accès à une calculatrice. Plutôt que d'essayer d'entraîner le modèle à maîtriser l'arithmétique, il est beaucoup plus efficace de lui fournir un outil adapté.

Parmi les autres outils simples qui peuvent considérablement améliorer les capacités d'un modèle, on peut citer un calendrier, un convertisseur de fuseaux horaires, un convertisseur d'unités (par exemple, de livres en kilogrammes) et un traducteur capable de traduire vers et depuis les langues que le modèle ne maîtrise pas.

Les interpréteurs de code constituent des outils plus complexes, mais aussi plus puissants. Au lieu d'entraîner un modèle à comprendre du code, vous pouvez lui donner accès à un interpréteur afin qu'il exécute un fragment de code, renvoie les résultats ou analyse les erreurs d'exécution. Grâce à cette fonctionnalité, vos agents peuvent agir comme assistants de programmation, analystes de données, voire assistants de recherche capables d'écrire du code pour mener des expériences et en rapporter les résultats. Toutefois, l'exécution automatisée de code comporte un risque d'attaques par injection de code, comme expliqué dans [« Ingénierie des invites défensives »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_defensive_prompt_engineering_1730156991196256) . Des mesures de sécurité appropriées sont essentielles pour garantir votre sécurité et celle de vos utilisateurs.

Des outils externes peuvent rendre multimodal un modèle textuel ou image. Par exemple, un modèle générant uniquement du texte peut s'appuyer sur un convertisseur texte-image pour générer à la fois du texte et des images. Face à une requête textuelle, le planificateur IA de l'agent décide de générer du texte, des images, ou les deux. C'est ainsi que ChatGPT génère du texte et des images : il utilise DALL-E comme générateur d'images. Les agents peuvent également utiliser un interpréteur de code pour générer des graphiques, un compilateur LaTeX pour le rendu d'équations mathématiques, ou un navigateur pour l'affichage de pages web à partir de code HTML.

De même, un modèle capable de traiter uniquement des entrées textuelles peut utiliser un outil de légende d'images pour traiter les images et un outil de transcription pour traiter l'audio. Il peut également utiliser un outil de reconnaissance optique de caractères (OCR) pour lire les fichiers PDF.

_L'utilisation d'outils peut considérablement améliorer les performances d'un modèle, comparativement à la simple incitation ou même au réglage fin_ . Chameleon ( [Lu et al., 2023](https://arxiv.org/abs/2304.09842) ) démontre qu'un agent basé sur GPT-4, enrichi de 13 outils, surpasse GPT-4 seul sur plusieurs benchmarks. Parmi les outils utilisés par cet agent, on peut citer la recherche de connaissances, un générateur de requêtes, un générateur de légendes d'images, un détecteur de texte et la recherche Bing.

Sur ScienceQA, un banc d'essai de questions scientifiques, Chameleon améliore de 11,37 % le meilleur résultat publié avec peu d'exemples. Sur TabMWP (Tabular Math Word Problems) (Lu et al., 2022), un banc d'essai portant sur des questions mathématiques tabulaires, Chameleon améliore la précision de 17 %.

### Actions écrites

Jusqu'à présent, nous avons abordé les actions en lecture seule qui permettent à un modèle de lire ses sources de données. Mais les outils peuvent également effectuer des opérations d'écriture, c'est-à-dire modifier les sources de données. Un exécuteur SQL peut récupérer une table de données (lecture) mais aussi la modifier ou la supprimer (écriture). Une API de messagerie peut lire un courriel mais aussi y répondre. Une API bancaire peut consulter votre solde actuel mais aussi initier un virement bancaire.

Les actions d'écriture permettent à un système d'en faire plus. Elles peuvent vous permettre d'automatiser l'ensemble du processus de prospection client : recherche de clients potentiels, identification de leurs coordonnées, rédaction d'e-mails, envoi des premiers e-mails, lecture des réponses, relance, extraction des commandes, mise à jour de vos bases de données avec les nouvelles commandes, etc.

Cependant, la perspective de donner à l'IA le pouvoir de modifier automatiquement nos vies est effrayante. De même qu'il serait impensable de confier à un stagiaire l'autorisation de supprimer une base de données de production, il est impensable de permettre à une IA peu fiable d'effectuer des virements bancaires. La confiance dans les capacités du système et ses mesures de sécurité est cruciale. Il est impératif de garantir la protection du système contre les personnes mal intentionnées qui pourraient tenter de le manipuler pour qu'il commette des actes malveillants.

Lorsque j'évoque les agents d'IA autonomes devant un groupe de personnes, il y a souvent quelqu'un qui parle de voitures autonomes. « Et si quelqu'un piratait la voiture pour vous kidnapper ? » Bien que l'exemple de la voiture autonome paraisse frappant de par sa matérialité, un système d'IA peut causer des dommages sans être physiquement présent dans le monde. Il peut manipuler les marchés boursiers, voler des droits d'auteur, violer la vie privée, renforcer les préjugés, diffuser de la désinformation et de la propagande, et bien plus encore, comme expliqué dans [« Ingénierie proactive défensive »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_defensive_prompt_engineering_1730156991196256) .

Ce sont là des préoccupations légitimes, et toute organisation souhaitant exploiter l'IA se doit de prendre la sûreté et la sécurité au sérieux. Toutefois, cela ne signifie pas que les systèmes d'IA ne devraient jamais avoir la possibilité d'agir dans le monde réel. Si l'on peut amener les gens à faire confiance à une machine pour nous emmener dans l'espace, j'espère qu'un jour, les mesures de sécurité seront suffisantes pour que nous puissions faire confiance aux systèmes d'IA autonomes. Par ailleurs, l'erreur est humaine. Personnellement, je ferais davantage confiance à une voiture autonome qu'à un inconnu pour me conduire.

De même que les bons outils peuvent considérablement accroître la productivité humaine (imaginez-vous faire des affaires sans Excel ou construire un gratte-ciel sans grues ?), les outils permettent aux modèles d’accomplir bien plus de tâches. De nombreux fournisseurs de modèles prennent déjà en charge l’utilisation d’outils avec leurs modèles, une fonctionnalité souvent appelée appel de fonctions. À l’avenir, je m’attends à ce que l’appel de fonctions avec un large éventail d’outils devienne une pratique courante pour la plupart des modèles.

## Planification

Au cœur d'un agent de modèle de base se trouve le modèle chargé de résoudre une tâche. Une tâche est définie par son objectif et ses contraintes. Par exemple, une tâche consiste à organiser un voyage de deux semaines de San Francisco en Inde avec un budget de 5 000 $. L'objectif est le voyage de deux semaines. La contrainte est le budget.

Les tâches complexes nécessitent une planification. Le résultat de ce processus est un plan, véritable feuille de route décrivant les étapes nécessaires à la réalisation de la tâche. Une planification efficace requiert généralement que le modèle comprenne la tâche, envisage différentes options pour la mener à bien et choisisse la plus prometteuse.

Si vous avez déjà participé à une réunion de planification, vous savez que planifier est une tâche complexe. Problème informatique important, la planification a fait l'objet de nombreuses études et son traitement complet exigerait plusieurs volumes. Je ne pourrai ici qu'en aborder les grandes lignes.

### Aperçu de la planification

Face à une tâche, il existe de nombreuses manières de la décomposer, mais toutes ne mènent pas à un résultat satisfaisant. Parmi les solutions correctes, certaines sont plus efficaces que d'autres. Prenons l'exemple de la question : « Combien d'entreprises sans chiffre d'affaires ont levé au moins 1 milliard de dollars ? » Il existe de nombreuses façons d'y répondre, mais à titre d'illustration, considérons les deux options suivantes :

1. Trouvez toutes les entreprises sans chiffre d'affaires, puis filtrez-les par montant levé.
    
2. Trouvez toutes les entreprises qui ont levé au moins 1 milliard de dollars, puis filtrez-les par chiffre d'affaires.
    

La seconde option est plus efficace. Il existe beaucoup plus d'entreprises sans chiffre d'affaires que d'entreprises ayant levé un milliard de dollars. Face à ces deux seules options, un agent intelligent devrait privilégier la seconde.

Il est possible de combiner la planification et l'exécution au sein d'une même instruction. Par exemple, vous soumettez une instruction au modèle, vous lui demandez de raisonner étape par étape (comme avec une instruction de type « chaîne de raisonnement »), puis vous exécutez ces étapes en une seule instruction. Mais que se passe-t-il si le modèle élabore un plan en 1 000 étapes qui n'atteint même pas l'objectif ? Sans supervision, un agent peut exécuter ces étapes pendant des heures, gaspillant du temps et de l'argent en appels API, avant que vous ne réalisiez qu'il est dans une impasse.

Pour éviter les exécutions inutiles, _la planification_ doit être dissociée de _l'exécution_ . L'agent génère d'abord un plan, qui n'est exécuté qu'après _validation_ . Cette validation peut s'effectuer à l'aide d'heuristiques. Par exemple, une heuristique simple consiste à éliminer les plans comportant des actions invalides. Si le plan généré requiert une recherche Google et que l'agent n'y a pas accès, ce plan est invalide. Une autre heuristique simple pourrait consister à éliminer tous les plans comportant plus de X étapes. La validation d'un plan peut également être réalisée par un système d'intelligence artificielle. Un modèle peut être sollicité pour évaluer la pertinence du plan et proposer des pistes d'amélioration.

Si le plan généré est jugé inadéquat, vous pouvez demander au planificateur d'en générer un autre. Si le plan généré est valide, exécutez-le. Si le plan fait appel à des outils externes, des appels de fonction seront effectués. Les résultats de l'exécution de ce plan devront alors être évalués. Notez que le plan généré ne doit pas nécessairement couvrir l' intégralité de la tâche. Il peut s'agir d'un plan simplifié pour une sous-tâche. L'ensemble du processus est illustré par [la figure 6-9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_9_1730157386529290) .

![Schéma d'un outil. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0609.png)

###### Figure 6-9. Découplage de la planification et de l'exécution afin que seuls les plans validés soient exécutés.

[Votre système comporte désormais trois composants : un pour générer](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1324) les plans, un pour les valider et un autre pour les exécuter. Si l’on considère chaque composant comme un agent, il s’agit d’un système multi-agents.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1324)

Pour accélérer le processus, au lieu de générer les plans séquentiellement, vous pouvez en générer plusieurs en parallèle et demander à l'évaluateur de choisir le plus prometteur. Il s'agit d'un autre compromis entre latence et coût, car la génération simultanée de plusieurs plans engendre des coûts supplémentaires.

La planification nécessite de comprendre l'intention derrière une tâche : que cherche à faire l'utilisateur avec cette requête ? Un classificateur d'intention est souvent utilisé pour aider les agents à planifier. Comme illustré dans [« Décomposer les tâches complexes en sous-tâches plus simples »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_break_complex_tasks_into_simpler_subtasks_1730156991196113) , la classification des intentions peut être effectuée à l'aide d'une autre invite ou d'un modèle de classification entraîné spécifiquement pour cette tâche. Le mécanisme de classification des intentions peut être considéré comme un agent supplémentaire au sein de votre système multi-agents.

Comprendre l'intention de l'utilisateur permet à l'agent de choisir les outils les plus adaptés. Par exemple, pour le support client, si la question concerne la facturation, l'agent pourrait avoir besoin d'accéder à un outil permettant de consulter l'historique des paiements récents de l'utilisateur. En revanche, si la question porte sur la réinitialisation d'un mot de passe, l'agent pourrait avoir besoin d'accéder à la documentation.

###### Conseil

Certaines requêtes peuvent être hors du champ d'action de l'agent. Le classificateur d'intentions doit pouvoir identifier les requêtes comme non pertinentes afin que l'agent puisse les rejeter poliment au lieu de gaspiller des ressources (FLOPs) à chercher des solutions impossibles.

Jusqu'à présent, nous avons supposé que l'agent automatisait les trois étapes : la génération, la validation et l'exécution des plans. En réalité, l'intervention humaine est possible à chaque étape pour faciliter le processus et atténuer les risques. Un expert peut fournir un plan, le valider ou en exécuter des parties. Par exemple, pour les tâches complexes où l'agent peine à générer le plan complet, un expert peut fournir un plan général que l'agent pourra ensuite développer. Si un plan implique des opérations risquées, comme la mise à jour d'une base de données ou l'intégration d'une modification de code, le système peut demander une approbation humaine explicite avant exécution ou laisser ces opérations être réalisées par des humains. Pour ce faire, il est nécessaire de définir clairement le niveau d'automatisation autorisé pour chaque action de l'agent.

En résumé, la résolution d'une tâche implique généralement les processus suivants. Notez que la réflexion n'est pas obligatoire pour un agent, mais elle améliorera considérablement ses performances :

1. _Élaboration du plan_ : concevoir un plan pour accomplir cette tâche. Un plan est une suite d’actions réalisables ; ce processus est donc également appelé décomposition des tâches.
    
2. _Réflexion et correction des erreurs_ : évaluer le plan généré. S’il est erroné, en générer un nouveau.
    
3. _Exécution_ : mettre en œuvre les actions décrites dans le plan généré. Cela implique souvent l’appel de fonctions spécifiques.
    
4. _Réflexion et correction des erreurs_ : après avoir pris connaissance des résultats de l’action, évaluez-les et déterminez si l’objectif a été atteint. Identifiez et corrigez les erreurs. Si l’objectif n’est pas atteint, élaborez un nouveau plan.
    

Vous avez déjà découvert dans ce livre des techniques de planification et de réflexion. Lorsque vous demandez à un modèle de « réfléchir étape par étape », vous lui demandez de décomposer une tâche. Lorsque vous lui demandez de « vérifier si votre réponse est correcte », vous lui demandez de réfléchir.

### Les modèles de fondation en tant que planificateurs

Une question demeure : les modèles de base sont-ils capables de planifier ? De nombreux chercheurs estiment que ces modèles, du moins ceux construits sur des modèles de langage autorégressifs, en sont incapables. Yann LeCun, scientifique en chef de Meta en IA, affirme catégoriquement que [les modèles de langage autorégressifs ne peuvent pas planifier](https://x.com/ylecun/status/1702027572077326505) (2023). Dans son article « Les modèles de langage peuvent-ils vraiment raisonner et planifier ? », [Kambhampati (2023)](https://oreil.ly/8_j7E) soutient que les modèles de langage excellent dans l’extraction de connaissances, mais pas dans la planification. Il suggère que les articles qui mettent en avant les capacités de planification des modèles de langage confondent les connaissances générales de planification extraites de ces modèles avec des plans exécutables. « Les plans issus des modèles de langage peuvent sembler raisonnables à l’utilisateur lambda, mais entraîner des interactions et des erreurs lors de l’exécution. »

Cependant, bien qu'il existe de nombreux témoignages anecdotiques selon lesquels les LLM sont de mauvais planificateurs, il est difficile de déterminer si cela est dû à une mauvaise utilisation des LLM ou au fait que, fondamentalement, les LLM sont incapables de planifier.

_La planification est, par essence, un problème de recherche_ . Il s'agit de rechercher parmi différents chemins menant à l'objectif, d'en prédire l'issue (la récompense) et de choisir celui qui offre le résultat le plus prometteur. Souvent, on constate qu'aucun chemin ne permet d'atteindre l'objectif.

La recherche nécessite souvent _de revenir en arrière_ . Par exemple, imaginez que vous vous trouviez à une étape où deux actions sont possibles : A et B. Après avoir effectué l’action A, vous vous retrouvez dans un état incertain ; vous devez donc revenir à l’état précédent pour effectuer l’action B.

Certains affirment qu'un modèle autorégressif ne peut générer que des actions futures. Il est incapable de revenir en arrière pour générer des actions alternatives. De ce fait, ils en concluent que les modèles autorégressifs sont incapables de planifier. Cependant, cela n'est pas nécessairement vrai. Après avoir exécuté un chemin avec l'action A, si le modèle détermine que ce chemin n'est pas pertinent, il peut le modifier en utilisant l'action B à la place, effectuant ainsi un retour en arrière. Le modèle peut également toujours recommencer et choisir un autre chemin.

Il est également possible que les titulaires d'un LLM aient des difficultés à planifier, faute d'outils adaptés. Pour planifier, il est nécessaire de connaître non seulement les actions possibles, mais aussi _les conséquences potentielles de chacune_ . Prenons un exemple simple : vous souhaitez gravir une montagne. Vous pouvez tourner à droite, à gauche, faire demi-tour ou continuer tout droit. Cependant, si tourner à droite risque de vous faire tomber de la falaise, vous préférerez sans doute éviter cette action. Techniquement, une action vous fait passer d'un état à un autre, et il est indispensable de connaître l'état final pour déterminer s'il convient d'agir.

Cela signifie qu'il ne suffit pas d'inciter un modèle à générer uniquement une séquence d'actions, comme le fait la technique courante d'incitation par la chaîne de pensée. L'article « Reasoning with Language Model is Planning with World Model » ( [Hao et al., 2023](https://arxiv.org/abs/2305.14992) ) soutient qu'un modèle de langage, grâce à la richesse de ses informations sur le monde, est capable de prédire le résultat de chaque action. Ce modèle peut ensuite intégrer cette prédiction pour générer des plans cohérents.

Même si l'IA ne peut pas planifier, elle peut néanmoins faire partie d'un système de planification. Il serait possible d'enrichir un modèle linéaire logique (MLL) avec un outil de recherche et un système de suivi d'état pour faciliter sa planification.

# Planificateurs basés sur le modèle de base (FM) versus apprentissage par renforcement (RL)

L' _agent_ est un concept fondamental en RL, qui est défini dans [Wikipédia](https://en.wikipedia.org/wiki/Reinforcement_learning) comme un domaine « qui étudie comment un agent intelligent doit agir dans un environnement dynamique afin de maximiser la récompense cumulative ».

Les agents RL et les agents FM présentent de nombreuses similitudes. Ils sont tous deux caractérisés par leur environnement et leurs actions possibles. La principale différence réside dans le fonctionnement de leur planificateur. Dans un agent RL, le planificateur est entraîné par un algorithme RL. Cet entraînement peut s'avérer long et coûteux en ressources. Dans un agent FM, le modèle fait office de planificateur. Ce modèle peut être guidé ou affiné pour améliorer ses capacités de planification, et requiert généralement moins de temps et de ressources.

Cependant, rien n'empêche un agent FM d'intégrer des algorithmes d'apprentissage par renforcement pour améliorer ses performances. Je pense qu'à terme, les agents FM et les agents RL fusionneront.

### Génération de plans

La méthode la plus simple pour transformer un modèle en générateur de plans consiste à utiliser l'ingénierie des invites. Imaginez que vous souhaitiez créer un agent pour aider les clients à découvrir les produits de Kitty Vogue. Vous donnez à cet agent l'accès à trois outils externes : la recherche de produits par prix, la recherche des produits phares et la recherche d'informations sur les produits. Voici un exemple d'invite pour la génération de plans. Cette invite est fournie à titre indicatif uniquement. Les invites en production sont généralement plus complexes.
```
**SYSTEM PROMPT**
Propose a plan to solve the task. You have access to 5 actions:          
get_today_date()
fetch_top_products(start_date, end_date, num_products)
fetch_product_info(product_name)
generate_query(task_history, tool_output)
generate_response(query)
         
The plan must be a sequence of valid actions.
      
Examples
Task: "Tell me about Fruity Fedora"
Plan: [fetch_product_info, generate_query, generate_response]

Task: "What was the best selling product last week?"
Plan: [fetch_top_products, generate_query, generate_response]
     
Task: {USER INPUT}
Plan:
```

            

Deux points sont à noter concernant cet exemple :

- Le format de plan utilisé ici — une liste de fonctions dont les paramètres sont déduits par l'agent — n'est qu'une des nombreuses façons de structurer le flux de contrôle de l'agent.
    
- Cette `generate_query`fonction utilise l'historique actuel de la tâche et les résultats les plus récents des outils pour générer une requête destinée au générateur de réponses. Les résultats des outils à chaque étape sont ajoutés à l'historique de la tâche.
    

Si l'utilisateur demande « Quel était le prix du produit le plus vendu la semaine dernière ? », un plan généré pourrait ressembler à ceci :
```
1. obtenir_temps()
2. récupérer_les_meilleurs_produits()
3. récupérer_informations_produit()
4. générer_requête()
5. générer_réponse()
```
Vous vous demandez peut-être : « Quels sont les paramètres nécessaires à chaque fonction ? » Il est difficile de prédire avec précision les paramètres à l’avance, car ils sont souvent extraits des résultats précédents de l’outil. Si la première étape `get_time()`renvoie « 2030-09-13 », l’agent peut en déduire que les paramètres de l’étape suivante doivent être utilisés :
```
retrieve_top_products(
      start_date=“2030-09-07”,
      end_date=“2030-09-13”,
      num_products=1
)
```


Souvent, les informations sont insuffisantes pour déterminer les valeurs exactes des paramètres d'une fonction. Par exemple, si un utilisateur demande : « Quel est le prix moyen des produits les plus vendus ? », les réponses aux questions suivantes restent floues :

- Combien de produits les plus vendus l'utilisateur souhaite-t-il consulter ?
    
- L'utilisateur souhaite-t-il voir les produits les plus vendus de la semaine dernière, du mois dernier ou de tous les temps ?
    

Cela signifie que les modèles doivent fréquemment faire des suppositions, et que ces suppositions peuvent être erronées.

Comme la séquence d'actions et les paramètres associés sont générés par des modèles d'IA, des erreurs peuvent survenir. Ces erreurs peuvent amener le modèle à appeler une fonction invalide ou une fonction valide avec des paramètres incorrects. Les techniques d'amélioration des performances générales d'un modèle peuvent être utilisées pour améliorer ses capacités de planification.

Voici quelques pistes pour améliorer les compétences d'un agent en matière de planification :

- Rédigez une invite système plus claire avec davantage d'exemples.
    
- Fournissez des descriptions plus détaillées des outils et de leurs paramètres afin que le modèle les comprenne mieux.
    
- Réécrivez les fonctions elles-mêmes pour les simplifier, par exemple en refactorisant une fonction complexe en deux fonctions plus simples.
    
- Utilisez un modèle plus robuste. En général, les modèles plus robustes sont plus performants en matière de planification.
    
- Affinez un modèle pour la génération de plans.
    

#### Appel de fonction

De nombreux fournisseurs de modèles proposent des outils pour leurs modèles, transformant ainsi ces derniers en agents. Un outil est une fonction. L'invocation d'un outil est donc souvent appelée _appel de fonction_ . Le fonctionnement varie selon les API de modèles, mais en général, un appel de fonction fonctionne comme suit :

1. _Créer un inventaire des outils._
    
    Déclarez tous les outils que vous souhaitez qu'un modèle utilise. Chaque outil est décrit par son point d'entrée d'exécution (par exemple, le nom de sa fonction), ses paramètres et sa documentation (par exemple, ce que fait la fonction et les paramètres dont elle a besoin).
    
2. _Précisez les outils que l'agent peut utiliser._
    
    Étant donné que différentes requêtes peuvent nécessiter différents outils, de nombreuses API permettent de spécifier une liste d'outils déclarés à utiliser pour chaque requête. Certaines permettent de contrôler plus finement l'utilisation des outils grâce aux paramètres suivants :
    
    `required`
    
    Le modèle doit utiliser au moins un outil.
    
    `none`
    
    Le modèle ne doit utiliser aucun outil.
    
    `auto`
    
    Le modèle détermine les outils à utiliser.
    

L'appel de fonctions est illustré dans [la figure 6-10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_10_1730157386529297) . Ce schéma est présenté en pseudocode afin de représenter plusieurs API. Pour utiliser une API spécifique, veuillez consulter sa documentation.

![Capture d'écran d'un programme informatique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0610.png)

###### Figure 6-10. Un exemple de modèle utilisant deux outils simples.

À partir d'une requête, un agent défini comme dans [la figure 6-10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_10_1730157386529297) génère automatiquement les outils à utiliser et leurs paramètres. Certaines API d'appel de fonctions veillent à ce que seules des fonctions valides soient générées, sans toutefois pouvoir garantir l'exactitude des valeurs des paramètres.

Par exemple, si l'utilisateur demande « Combien de kilogrammes font 40 livres ? », l'agent pourrait décider qu'il a besoin de l'outil `lbs_to_kg_tool`avec la valeur 40 pour un paramètre. La réponse de l'agent pourrait ressembler à ceci :

```python
response = ModelResponse(
   finish_reason='tool_calls',
   message=chat.Message(
       content=None,
       role='assistant',
       tool_calls=[
           ToolCall(
               function=Function(
                   arguments='{"lbs":40}',
                   name='lbs_to_kg'),
               type='function')
       ])
)
```

À partir de cette réponse, vous pouvez invoquer la fonction `lbs_to_kg(lbs=40)`et utiliser son résultat pour générer une réponse aux utilisateurs.

###### Conseil

Lorsque vous travaillez avec des agents, demandez systématiquement au système de vous indiquer les valeurs des paramètres utilisés pour chaque appel de fonction. Vérifiez ensuite ces valeurs afin de vous assurer de leur exactitude.

#### granularité de la planification

Un plan est une feuille de route qui décrit les étapes nécessaires à la réalisation d'une tâche. Ce plan peut présenter différents niveaux de détail. Pour planifier une année, un plan trimestriel est plus détaillé qu'un plan mensuel, lui-même plus détaillé qu'un plan hebdomadaire.

Il existe un compromis entre planification et exécution. Un plan détaillé est plus difficile à élaborer, mais plus facile à mettre en œuvre. Un plan de haut niveau est plus facile à élaborer, mais plus difficile à exécuter. Une approche permettant de contourner ce compromis consiste à planifier de manière hiérarchique. Dans un premier temps, utilisez un outil de planification pour élaborer un plan de haut niveau, par exemple un plan trimestriel. Ensuite, pour chaque trimestre, utilisez le même outil ou un outil différent pour élaborer un plan mensuel.

Jusqu'à présent, tous les exemples de plans générés utilisent les noms de fonctions exacts, ce qui est très précis. Cette approche présente toutefois un inconvénient : l'inventaire d'outils d'un agent peut évoluer. Par exemple, la fonction permettant d'obtenir la date actuelle `get_time()`peut être renommée `get_current_time()`. Lorsqu'un outil change, il est nécessaire de mettre à jour l'invite et tous les exemples. De plus, l'utilisation des noms de fonctions exacts complique la réutilisation d'un planificateur pour différents cas d'utilisation avec des API d'outils différentes.

Si vous avez déjà affiné un modèle pour générer des plans basés sur l'ancien inventaire d'outils, vous devrez l'affiner à nouveau sur le nouvel inventaire d'outils.

Pour éviter ce problème, les plans peuvent également être générés en utilisant un langage plus naturel, de plus haut niveau que les noms de fonctions spécifiques au domaine. Par exemple, face à la requête « Quel était le prix du produit le plus vendu la semaine dernière ? », un agent peut être configuré pour générer un plan ressemblant à ceci :
```
1. Obtenir la date actuelle
2. Récupérer le produit le plus vendu de la semaine dernière
3. récupérer les informations sur le produit
4. Générer une requête
5. Générer une réponse
```
L'utilisation d'un langage plus naturel permet à votre générateur de plans de mieux s'adapter aux évolutions des API des outils. Si votre modèle a été principalement entraîné sur du langage naturel, il sera probablement plus à même de comprendre et de générer des plans dans ce langage, et moins susceptible de produire des résultats erronés.

L'inconvénient de cette approche est qu'elle nécessite un traducteur pour convertir chaque action en langage naturel en commandes exécutables.<sup> [13</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1330) Cependant, la traduction est une tâche bien plus simple que la planification et peut être réalisée par des modèles moins complexes, présentant un risque d' hallucination moindre .

#### Plans complexes

Les exemples de plans présentés jusqu'ici étaient séquentiels : l'action suivante est _toujours_ exécutée une fois la précédente terminée. L'ordre d'exécution des actions est appelé _flux de contrôle_ . La forme séquentielle n'est qu'un type de flux de contrôle parmi d'autres. On trouve également les flux de contrôle parallèles, conditionnels (if) et les boucles (for). La liste suivante présente un aperçu de chaque flux de contrôle, y compris le flux séquentiel à titre de comparaison :

Séquentiel

L'exécution de la tâche B a lieu une fois la tâche A terminée, probablement parce que la tâche B dépend de la tâche A. Par exemple, la requête SQL ne peut être exécutée qu'après avoir été traduite à partir de l'entrée en langage naturel.

Parallèle

Exécuter les tâches A et B simultanément. Par exemple, pour la requête « Trouve-moi les produits les plus vendus à moins de 100 $ », un agent pourrait d’abord récupérer les 100 produits les plus vendus, puis, pour chacun d’eux, récupérer son prix.

instruction if

L'exécution de la tâche B ou C dépend du résultat de l'étape précédente. Par exemple, l'agent commence par consulter le rapport sur les résultats financiers de NVIDIA. En fonction de ce rapport, il peut ensuite décider de vendre ou d'acheter des actions NVIDIA.

boucle For

Répétez l'exécution de la tâche A jusqu'à ce qu'une condition spécifique soit remplie. Par exemple, continuez à générer des nombres aléatoires jusqu'à obtenir un nombre premier.

Ces différents flux de contrôle sont visualisés dans [la figure 6-11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_11_1730157386529304) .

![Diagramme d'une tâche. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0611.png)

###### Figure 6-11. Exemples de différents ordres dans lesquels un plan peut être exécuté.

En génie logiciel traditionnel, les conditions des flux de contrôle sont précises. Avec les agents basés sur l'IA, ce sont les modèles d'IA qui déterminent ces flux. Les plans aux flux de contrôle non séquentiels sont plus difficiles à générer et à traduire en commandes exécutables.

Lors de l'évaluation d'un framework d'agents, vérifiez les flux de contrôle qu'il prend en charge. Par exemple, si le système doit consulter dix sites web simultanément, peut-il le faire ? L'exécution parallèle peut réduire considérablement la latence perçue par les utilisateurs.

### Réflexion et correction des erreurs

Même les meilleurs plans doivent être constamment évalués et ajustés pour maximiser leurs chances de succès. Si la réflexion n'est pas strictement nécessaire au fonctionnement d'un agent, elle est en revanche indispensable à sa réussite.

La réflexion peut être utile à de nombreuses étapes du processus d'exécution d'une tâche :

- Après réception d'une requête utilisateur, évaluer la faisabilité de la demande.
    
- Après la génération du plan initial, il s'agit d'évaluer si le plan est pertinent.
    
- Après chaque étape d'exécution, évaluer si le processus est sur la bonne voie.
    
- Une fois le plan entièrement exécuté, déterminer si la tâche a été accomplie.
    

La réflexion et la correction des erreurs sont deux mécanismes différents mais indissociables. La réflexion génère des idées qui permettent de déceler les erreurs à corriger.

La réflexion peut être menée avec le même agent à l'aide d'invites d'auto-évaluation. Elle peut également être menée avec un composant distinct, tel qu'un système d'évaluation spécialisé : un modèle qui attribue un score précis à chaque résultat.

Proposée initialement par ReAct ( [Yao et al., 2022](https://arxiv.org/abs/2210.03629) ), l'entrelacement du raisonnement et de l'action est devenu un modèle courant pour les agents. Yao et al. utilisent le terme « raisonnement » pour désigner à la fois la planification et la réflexion. À chaque étape, l'agent est invité à expliquer son raisonnement (planification), à agir, puis à analyser ses observations (réflexion), jusqu'à ce qu'il considère la tâche comme terminée. L'agent est généralement guidé, à l'aide d'exemples, pour générer des résultats au format suivant :
```
**Thought 1:** …
**Act 1:** …
**Observation 1:** …

… [continue until reflection determines that the task is finished] …

**Thought N:** … 
**Act N: Finish** [Response to query]
```


[La figure 6-12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_12_1730157386529311) montre un exemple d'agent suivant le cadre ReAct répondant à une question de HotpotQA ( [Yang et al., 2018](https://arxiv.org/abs/1809.09600) ), une référence pour la réponse aux questions multi-sauts.

Il est possible d'implémenter la réflexion dans un contexte multi-agents : un agent planifie et exécute des actions, tandis qu'un autre agent évalue le résultat après chaque étape ou après un certain nombre d'étapes. [14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1335)

Si la réponse de l'agent n'a pas permis d'accomplir la tâche, vous pouvez l'inviter à réfléchir aux raisons de cet échec et aux pistes d'amélioration. Sur la base de cette suggestion, l'agent élabore un nouveau plan. Cela lui permet d'apprendre de ses erreurs. Par exemple, lors de la génération de code, un évaluateur peut constater que le code généré échoue à un tiers des tests. L'agent comprend alors que l'échec est dû au fait qu'il n'a pas pris en compte les tableaux contenant uniquement des nombres négatifs. Il génère ensuite un nouveau code intégrant ces tableaux.

![Capture d'écran d'un programme informatique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0612.png)

###### Figure 6-12. Un agent ReAct en action. Image extraite de l'article ReAct (Yao et al., 2022). Cette image est diffusée sous licence CC BY 4.0.

C’est l’approche adoptée par Reflexion ( [Shinn et al., 2023](https://arxiv.org/abs/2303.11366) ). Dans ce cadre, la réflexion est divisée en deux modules : un évaluateur qui analyse le résultat et un module d’auto-réflexion qui examine les causes des erreurs. [La figure 6-13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_13_1730157386529317) illustre des exemples d’agents Reflexion en action. Les auteurs utilisent le terme « trajectoire » pour désigner un plan. À chaque étape, après évaluation et auto-réflexion, l’agent propose une nouvelle trajectoire.

Comparée à la génération de plans, la réflexion est relativement simple à implémenter et peut apporter des gains de performance surprenants. Son principal inconvénient réside dans la latence et le coût. La génération de pensées, d'observations et parfois d'actions peut nécessiter un grand nombre de jetons, ce qui augmente le coût et la latence perçue par l'utilisateur, notamment pour les tâches comportant de nombreuses étapes intermédiaires. Afin d'inciter leurs agents à respecter ce format, les auteurs de ReAct et de Reflexion ont tous deux utilisé de nombreux exemples dans leurs invites. Cela accroît le coût de calcul des jetons d'entrée et réduit l'espace contextuel disponible pour d'autres informations.

![Capture d'écran d'un programme informatique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0613.png)

###### Figure 6-13. Exemples de fonctionnement des agents Reflexion. Images issues du [dépôt GitHub de Reflexion](https://github.com/noahshinn/reflexion) .

### Sélection d'outils

Les outils jouant souvent un rôle crucial dans la réussite d'une tâche, leur choix doit être mûrement réfléchi. Les outils à fournir à votre agent dépendent de l'environnement et de la tâche, mais aussi du modèle d'IA qui le pilote.

Il n'existe pas de méthode infaillible pour choisir le meilleur ensemble d'outils. La littérature sur les agents présente un large éventail d'inventaires d'outils. Par exemple, Toolformer ( [Schick et al., 2023](https://arxiv.org/abs/2302.04761) ) a affiné GPT-J pour apprendre cinq outils. Chameleon ( [Lu et al., 2023](https://arxiv.org/abs/2304.09842) ) en utilise 13. De son côté, Gorilla ( [Patil et al., 2023](https://arxiv.org/abs/2305.15334) ) a tenté d'inciter les agents à sélectionner l'appel API approprié parmi 1 645 API.

Plus d'outils confèrent à l'agent de capacités accrues. Cependant, plus il y a d'outils, plus il est difficile de les utiliser efficacement. C'est comparable à la difficulté pour un humain de maîtriser un grand nombre d'outils. Ajouter des outils implique également d'allonger leurs descriptions, qui peuvent ne pas s'intégrer au contexte du modèle.

Comme pour de nombreuses autres décisions lors du développement d'applications d'IA, le choix des outils nécessite des expérimentations et des analyses. Voici quelques pistes pour vous aider à choisir :

- Comparez les performances d'un agent avec différents ensembles d'outils.
    
- Effectuez une étude d'ablation pour évaluer la baisse de performance de l'agent suite à la suppression d'un outil de son inventaire. Si la suppression d'un outil n'entraîne aucune baisse de performance, supprimez-le.
    
- Identifiez les outils sur lesquels l'agent commet fréquemment des erreurs. Si un outil s'avère trop difficile à utiliser pour l'agent (par exemple, si malgré de nombreuses instructions et un paramétrage précis, le modèle ne parvient pas à apprendre à l'utiliser), changez d'outil.
    
- Représentez graphiquement la distribution des appels d'outils afin d'identifier les outils les plus et les moins utilisés. [La figure 6-14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_14_1730157386529326) illustre les différences dans les profils d'utilisation des outils de GPT-4 et ChatGPT dans Chameleon (Lu et al., 2023).
    

![Capture d'écran d'un graphique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0614.png)

###### Figure 6-14. Différents modèles et tâches présentent différents modes d'utilisation des outils. Image tirée de Lu et al. (2023). Adaptée d'une image originale sous licence CC BY 4.0.

Les expériences de Lu et al. (2023) démontrent également deux points :

1. Des tâches différentes requièrent des outils différents. ScienceQA, la tâche de réponse aux questions scientifiques, s'appuie beaucoup plus sur les outils de récupération des connaissances que TabMWP, une tâche de résolution de problèmes mathématiques tabulaires.
    
2. Les différents modèles ont des préférences d'outils différentes. Par exemple, GPT-4 semble sélectionner un ensemble d'outils plus large que ChatGPT. ChatGPT semble privilégier la génération de légendes d'images, tandis que GPT-4 semble privilégier la recherche d'informations.
    

###### Conseil

Lors de l'évaluation d'un framework d'agents, il convient d'examiner les planificateurs et les outils qu'il prend en charge. Différents frameworks peuvent se concentrer sur différentes catégories d'outils. Par exemple, AutoGPT se concentre sur les API des réseaux sociaux (Reddit, X et Wikipédia), tandis que Composio se concentre sur les API d'entreprise (Google Apps, GitHub et Slack).

Vos besoins étant susceptibles d'évoluer avec le temps, évaluez la facilité avec laquelle vous pouvez étendre votre agent pour y intégrer de nouveaux outils.

En tant qu'êtres humains, nous devenons plus productifs non seulement en utilisant les outils dont nous disposons, mais aussi en créant des outils de plus en plus performants à partir d'outils plus simples. L'IA peut-elle créer de nouveaux outils à partir de ses outils initiaux ?

Chameleon (Lu et al., 2023) propose d'étudier la transition d'outils : après avoir utilisé l'outil _X_ , quelle est la probabilité que l'agent utilise l'outil _Y_ ? [La figure 6-15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_15_1730157386529332) illustre un exemple de transition d'outils. Si deux outils sont fréquemment utilisés ensemble, ils peuvent être combinés pour former un outil plus complexe. Si un agent a connaissance de cette information, il peut combiner des outils initiaux pour construire progressivement des outils plus complexes.

![Diagramme d'un diagramme. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0615.png)

###### Figure 6-15. Arbre de transition d'outils d'après Lu et al. (2023). Adapté d'une image originale sous licence CC BY 4.0.

Vogager ( [Wang et al., 2023](https://arxiv.org/abs/2305.16291) ) propose un gestionnaire de compétences pour assurer le suivi des nouvelles compétences (outils) acquises par un agent en vue de leur réutilisation ultérieure. Chaque compétence est un programme informatique. Lorsque le gestionnaire de compétences détermine qu'une nouvelle compétence est utile (par exemple, parce qu'elle a permis à un agent d'accomplir une tâche), il l'ajoute à la bibliothèque de compétences (conceptuellement similaire à un inventaire d'outils). Cette compétence peut ensuite être utilisée pour d'autres tâches.

Plus tôt dans cette section, nous avons mentionné que le succès d'un agent dans un environnement dépend de son inventaire d'outils et de ses capacités de planification. Toute défaillance dans l'un ou l'autre de ces aspects peut entraîner la défaillance de l'agent. La section suivante abordera les différents modes de défaillance d'un agent et la manière de les évaluer..

## Modes de défaillance des agents et évaluation

L'évaluation consiste à détecter les défaillances. Plus la tâche effectuée par un agent est complexe, plus les risques de défaillance sont élevés. Outre les modes de défaillance communs à toutes les applications d'IA, abordés dans les chapitres [3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) et [4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) , les agents présentent également des défaillances spécifiques liées à la planification, à l'exécution des outils et à l'efficacité. Certaines défaillances sont plus faciles à repérer que d'autres.

Pour évaluer un agent, il faut identifier ses modes de défaillance et mesurer la fréquence d'apparition de chacun de ces modes de défaillance.

[J’ai créé un benchmark simple pour illustrer ces différents modes de défaillance ; vous pouvez le consulter sur le dépôt GitHub](https://github.com/aie-book) du livre . Il existe également des benchmarks et des classements d’agents, tels que le [Berkeley Function Calling Leaderboard](https://oreil.ly/lKB61) , l’ [outil d’évaluation AgentOps](https://github.com/AgentOps-AI/agentops) et le [benchmark TravelPlanner](https://github.com/OSU-NLP-Group/TravelPlanner) .

### échecs de planification

La planification est complexe et peut échouer de multiples façons. L'erreur la plus fréquente est liée à une mauvaise utilisation des outils. L'agent peut générer un plan comportant une ou plusieurs des erreurs suivantes :

Outil invalide

Par exemple, il génère un plan qui contient `bing_search`, mais `bing_search`qui ne figure pas dans l'inventaire d'outils de l'agent.

Outil valide, paramètres invalides.

Par exemple, il est appelé `lbs_to_kg`avec deux paramètres. `lbs_to_kg`est dans l'inventaire des outils mais ne nécessite qu'un seul paramètre, `lbs`.

Outil valide, valeurs de paramètres incorrectes

Par exemple, elle appelle `lbs_to_kg`avec un paramètre, `lbs`, mais utilise la valeur 100 pour lbs alors qu'elle devrait être de 120.

Un autre mode d'échec de la planification est l'échec de l'objectif : l'agent ne parvient pas à atteindre l'objectif. Cela peut être dû au fait que le plan ne résout pas une tâche, ou qu'il la résout sans respecter les contraintes. Pour illustrer ce point, imaginez que vous demandiez au modèle de planifier un voyage de deux semaines de San Francisco à Hanoï avec un budget de 5 000 $. L'agent pourrait planifier un voyage de San Francisco à Hô Chi Minh-Ville, ou planifier un voyage de deux semaines de San Francisco à Hanoï dont le coût dépasserait largement le budget.

Une contrainte courante, souvent négligée lors de l'évaluation des agents, est le temps. Dans de nombreux cas, le temps d'exécution importe peu, car il suffit de confier une tâche à un agent et de vérifier son achèvement une fois celle-ci terminée. Cependant, il arrive fréquemment que l'agent devienne moins utile avec le temps. Par exemple, si vous lui demandez de préparer une demande de subvention et qu'il la termine après la date limite, son utilité s'en trouve réduite.

Un mode intéressant d'échec de planification est dû à des erreurs de raisonnement. L'agent est convaincu d'avoir accompli une tâche alors que ce n'est pas le cas. Par exemple, vous lui demandez d'affecter 50 personnes à 30 chambres d'hôtel. Il pourrait n'en affecter que 40 et prétendre avoir accompli la tâche.

Pour évaluer les erreurs de planification d'un agent, une option consiste à créer un ensemble de données de planification où chaque exemple est un tuple `(task, tool inventory)`. Pour chaque tâche, utilisez l'agent pour générer K plans. Calculez les métriques suivantes :

1. Parmi tous les plans générés, combien sont valides ?
    
2. Pour une tâche donnée, combien de plans l'agent doit-il générer, en moyenne, pour obtenir un plan valide ?
    
3. Parmi tous les appels d'outils, combien sont valides ?
    
4. À quelle fréquence les outils invalides sont-ils appelés ?
    
5. À quelle fréquence des outils valides sont-ils appelés avec des paramètres invalides ?
    
6. À quelle fréquence des outils valides sont-ils appelés avec des valeurs de paramètres incorrectes ?
    

Analysez les résultats de l'agent pour identifier des tendances. Quels types de tâches rencontrent-il le plus de difficultés ? Avez-vous une hypothèse pour expliquer ces difficultés ? Avec quels outils le modèle commet-il fréquemment des erreurs ? Certains outils peuvent être plus difficiles à utiliser pour un agent. Vous pouvez améliorer sa capacité à utiliser un outil complexe en fournissant des instructions plus claires, davantage d'exemples ou en affinant les paramètres. Si toutes ces solutions échouent, vous pourriez envisager de remplacer cet outil par un autre plus facile à utiliser.

### défaillances d'outils

Les dysfonctionnements d'outils surviennent lorsque l'outil utilisé est correct, mais que son résultat est erroné. Un exemple de dysfonctionnement est celui où l'outil fournit des résultats incorrects. Par exemple, un générateur de légendes d'images peut renvoyer une description incorrecte, ou un générateur de requêtes SQL peut renvoyer une requête SQL incorrecte.

Si l'agent ne génère que des plans de haut niveau et qu'un module de traduction intervient pour traduire chaque action planifiée en commandes exécutables, des échecs peuvent survenir en raison d'erreurs de traduction.

Les défaillances d'outils peuvent également survenir lorsque l'agent n'a pas accès aux outils adéquats pour la tâche. Un exemple évident est celui de la tâche consistant à récupérer les cours boursiers actuels sur Internet, alors que l'agent n'a pas accès à Internet.

Les défaillances d'outils sont spécifiques à chaque outil. Chaque outil doit être testé indépendamment. Il est impératif d'afficher systématiquement chaque appel d'outil et son résultat afin de pouvoir les examiner et les évaluer. Si vous utilisez un traducteur, créez des bancs d'essai pour l'évaluer.

Détecter les défaillances d'outils manquants nécessite de comprendre quels outils devraient être utilisés. Si votre agent rencontre fréquemment des défaillances dans un domaine spécifique, cela peut être dû à un manque d'outils adaptés. Collaborez avec des experts du domaine et observez les outils qu'ils utiliseraient.

### Efficacité

Un agent peut générer un plan valide en utilisant les outils appropriés pour accomplir une tâche, mais ce plan peut s'avérer inefficace. Voici quelques éléments à suivre pour évaluer l'efficacité d'un agent :

- De combien d'étapes l'agent a-t-il besoin, en moyenne, pour accomplir une tâche ?
    
- Combien coûte en moyenne à un agent d'accomplir une tâche ?
    
- Combien de temps dure généralement chaque action ? Y a-t-il des actions particulièrement longues ou coûteuses ?
    

Vous pouvez comparer ces indicateurs à votre référence, qui peut être un autre agent ou un opérateur humain. Lors de la comparaison d'agents IA à des agents humains, gardez à l'esprit que leurs modes de fonctionnement sont très différents : ce qui est considéré comme efficace pour les humains peut être inefficace pour l'IA, et inversement. Par exemple, visiter 100 pages web peut s'avérer inefficace pour un agent humain ne pouvant en visiter qu'une à la fois, mais trivial pour un agent IA capable de visiter toutes les pages web simultanément.

Dans ce chapitre, nous avons examiné en détail le fonctionnement des systèmes RAG et des systèmes d'agents. Ces deux modèles traitent souvent des informations qui dépassent les limites du contexte du modèle. Un système de mémoire, qui complète le contexte du modèle pour le traitement de l'information, peut considérablement améliorer ses capacités. Voyons maintenant comment fonctionne un système de mémoire..

# Mémoire

La mémoire désigne les mécanismes permettant à un modèle de conserver et d'utiliser des informations. Un système de mémoire est particulièrement utile pour les applications riches en connaissances comme RAG et les applications multi-étapes comme les agents. Un système RAG s'appuie sur la mémoire pour son contexte augmenté, qui peut s'enrichir au fil des itérations à mesure qu'il récupère de nouvelles informations. Un système d'agents a besoin de mémoire pour stocker les instructions, les exemples, le contexte, l'inventaire des outils, les plans, les résultats des outils, les réflexions, etc. Bien que RAG et les agents soient plus gourmands en mémoire, celle-ci est bénéfique à toute application d'IA nécessitant la conservation d'informations.

Un modèle d'IA possède généralement trois principaux mécanismes de mémoire :

Connaissances internes

Le modèle lui-même constitue un mécanisme de mémoire, car il conserve les connaissances issues des données sur lesquelles il a été entraîné. Ces connaissances constituent son _savoir interne_ . Le savoir interne d'un modèle reste inchangé tant que le modèle n'est pas mis à jour. Il peut accéder à ce savoir lors de toutes les requêtes.

mémoire à court terme

Le contexte d'un modèle est un mécanisme de mémoire. Les messages précédents d'une conversation peuvent y être ajoutés, permettant ainsi au modèle de les utiliser pour générer des réponses ultérieures. Le contexte d'un modèle peut être considéré comme sa _mémoire à court terme,_ car il ne persiste pas d'une tâche (requête) à l'autre. Son accès est rapide, mais sa capacité est limitée. C'est pourquoi il est souvent utilisé pour stocker les informations les plus importantes pour la tâche en cours.

mémoire à long terme

Les sources de données externes auxquelles un modèle peut accéder par récupération, comme dans un système RAG, constituent un mécanisme de mémoire. On peut considérer cette mémoire comme la _mémoire à long terme_ du modèle , car elle est conservée d'une tâche à l'autre. Contrairement aux connaissances internes du modèle, les informations stockées dans la mémoire à long terme peuvent être supprimées sans que le modèle ne soit mis à jour.

Les humains ont accès à des mécanismes de mémoire similaires. Savoir respirer est un savoir inné. On n'oublie généralement pas comment respirer, sauf en cas de grave problème. La mémoire à court terme contient les informations immédiatement pertinentes à l'activité en cours, comme le nom d'une personne que l'on vient de rencontrer. La mémoire à long terme est enrichie par les livres, les ordinateurs, les notes, etc.

Le mécanisme de mémoire à utiliser pour vos données dépend de leur fréquence d'utilisation. Les informations essentielles à toutes les tâches doivent être intégrées à la mémoire interne du modèle par le biais de l'apprentissage ou de l'ajustement fin. Les informations rarement utilisées doivent résider dans sa mémoire à long terme. La mémoire à court terme est réservée aux informations immédiates et contextuelles. Ces trois mécanismes de mémoire sont illustrés dans [la figure 6-16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_figure_16_1730157386529338) .

![Diagramme d'un modèle de mémoire. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0616.png)

###### Figure 6-16. La hiérarchie de l'information pour un agent.

La mémoire est essentielle au fonctionnement humain. Avec l'évolution des applications d'IA, les développeurs ont rapidement compris que la mémoire est tout aussi importante pour les modèles d'IA. De nombreux outils de gestion de la mémoire ont été développés pour ces modèles, et de nombreux fournisseurs de modèles ont intégré de la mémoire externe. L'ajout d'un système de mémoire à un modèle d'IA présente de nombreux avantages. En voici quelques-uns :

Gérer le débordement d'informations au sein d'une session

Lors de l'exécution d'une tâche, un agent acquiert une grande quantité de nouvelles informations, pouvant dépasser la longueur maximale de son contexte. Ces informations excédentaires peuvent être stockées dans un système de mémoire à long terme.

Conserver les informations entre les sessions

Un coach IA est pratiquement inutile si, à chaque fois que vous souhaitez ses conseils, vous devez raconter toute votre vie. Un assistant IA serait agaçant s'il oubliait constamment vos préférences. L'accès à votre historique de conversations permet à un agent de personnaliser ses actions. Par exemple, lorsque vous demandez des recommandations de livres, si le modèle se souvient que vous avez adoré « _Le Problème à trois corps »_ , il peut vous suggérer des ouvrages similaires.

Améliorer la cohérence d'un modèle

Si vous me posez deux fois une question subjective, comme noter une blague de 1 à 5, je serai bien plus enclin à donner une réponse cohérente si je me souviens de ma réponse précédente. De même, si un modèle d'IA peut se référer à ses réponses précédentes, il peut ajuster ses réponses futures pour garantir leur cohérence.

Préserver l'intégrité structurelle des données

Le texte étant par nature non structuré, les données stockées dans le contexte d'un modèle textuel le sont également. Il est possible d'y insérer des données structurées. Par exemple, vous pouvez y insérer un tableau ligne par ligne, mais rien ne garantit que le modèle le reconnaîtra comme tel. Disposer d'un système de mémoire capable de stocker des données structurées contribue à préserver l'intégrité structurelle de vos données. Par exemple, si vous demandez à un agent de trouver des prospects, il peut utiliser une feuille Excel pour les stocker. Il peut également utiliser une file d'attente pour stocker la séquence d'actions à effectuer.

Un système de mémoire pour les modèles d'IA se compose généralement de deux fonctions :

- Gestion de la mémoire : gérer les informations qui doivent être stockées dans la mémoire à court terme et la mémoire à long terme.
    
- Récupération en mémoire : extraire de la mémoire à long terme les informations pertinentes à la tâche.
    

La récupération en mémoire est similaire à la récupération RAG, car la mémoire à long terme est une source de données externe. Dans cette section, je me concentrerai sur la gestion de la mémoire. Celle-ci comprend généralement deux opérations : _l’ajout_ et _la suppression_ d’éléments. Si la capacité de stockage est limitée, la suppression peut s’avérer inutile. Cela peut convenir à la mémoire à long terme, car le stockage externe est relativement peu coûteux et facilement extensible. Cependant, la mémoire à court terme est limitée par la longueur maximale du contexte du modèle et nécessite donc une stratégie pour déterminer les éléments à ajouter et à supprimer.

La mémoire à long terme peut être utilisée pour stocker le surplus de données provenant de la mémoire à court terme. Cette opération dépend de l'espace alloué à la mémoire à court terme. Pour une requête donnée, le contexte d'entrée du modèle comprend à la fois sa mémoire à court terme et les informations extraites de sa mémoire à long terme. La capacité de la mémoire à court terme d'un modèle est donc déterminée par la part du contexte allouée aux informations extraites de la mémoire à long terme. Par exemple, si 30 % du contexte sont réservés, le modèle peut utiliser au maximum 70 % de la limite de contexte pour la mémoire à court terme. Lorsque ce seuil est atteint, le surplus de données peut être déplacé vers la mémoire à long terme.

Comme de nombreux éléments abordés précédemment dans ce chapitre, la gestion de la mémoire n'est pas propre aux applications d'IA. Elle constitue un pilier de tous les systèmes de données, et de nombreuses stratégies ont été développées pour optimiser son utilisation.

La stratégie la plus simple est FIFO (premier entré, premier sorti). Les premiers éléments ajoutés à la mémoire à court terme seront les premiers à être transférés vers le stockage externe. À mesure que la conversation s'allonge, les fournisseurs d'API comme OpenAI peuvent commencer à supprimer le début de la conversation.Des frameworks comme LangChain peuvent permettre la conservation des N derniers messages ou des N derniers jetons. Dans une conversation longue, cette stratégie part du principe que les premiers messages sont moins pertinents pour la discussion en cours. Or, cette hypothèse peut s'avérer erronée. Dans certaines conversations, les premiers messages peuvent contenir le plus d'informations, notamment lorsqu'ils énoncent l'objectif de la conversation.<sup> [15</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1357) Bien que la méthode FIFO soit simple à implémenter, elle peut entraîner la perte d'informations importantes par le modèle.<sup> [16 </sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1358)

Les stratégies plus sophistiquées consistent à éliminer les redondances. Les langues humaines contiennent des redondances pour plus de clarté et pour pallier les éventuels malentendus. Si l'on parvient à détecter automatiquement les redondances, l'empreinte mémoire sera considérablement réduite.

Une façon d'éliminer les redondances consiste à utiliser un résumé de la conversation. Ce résumé peut être généré à l'aide du même modèle ou d'un autre. La synthèse, associée au suivi des entités nommées, peut s'avérer très utile. [Bae et al. (2022)](https://arxiv.org/abs/2210.08750) ont approfondi cette approche. Après avoir obtenu le résumé, les auteurs ont cherché à construire une nouvelle mémoire en y intégrant les informations clés manquantes. Ils ont développé un classificateur qui, pour chaque phrase de la mémoire et chaque phrase du résumé, détermine si une seule, les deux ou aucune ne doit être ajoutée à la nouvelle mémoire.

[Liu et al. (2023)](https://arxiv.org/abs/2311.08719v1) , quant à eux, ont utilisé une approche réflexive. Après chaque action, l'agent est invité à effectuer deux tâches :

1. Réfléchissez aux informations qui viennent d'être générées.
    
2. Déterminez si ces nouvelles informations doivent être insérées dans la mémoire, fusionner avec la mémoire existante ou remplacer d'autres informations, notamment si ces dernières sont obsolètes et contredisent les nouvelles informations.
    

Face à des informations contradictoires, certains privilégient les plus récentes. D'autres font appel à des modèles d'IA pour trancher. La gestion des contradictions dépend du contexte. Si les contradictions peuvent désorienter un agent, elles peuvent aussi l'aider à adopter différents points de vue.

# Résumé

Compte tenu de la popularité de RAG et du potentiel des agents, les premiers lecteurs ont indiqué que c'était le chapitre qui les enthousiasmait le plus.

Ce chapitre s'ouvre sur le modèle RAG, le premier à émerger entre les deux. De nombreuses tâches requièrent des connaissances approfondies qui dépassent souvent le cadre contextuel d'un modèle. Par exemple, les copilotes de code peuvent avoir besoin d'accéder à des bases de code complètes, et les assistants de recherche peuvent être amenés à analyser plusieurs ouvrages. Initialement conçu pour pallier les limitations contextuelles d'un modèle, le modèle RAG permet également une utilisation plus efficace de l'information, améliorant ainsi la qualité des réponses tout en réduisant les coûts. Dès les débuts des modèles de base, il était évident que le modèle RAG serait extrêmement précieux pour un large éventail d'applications, et il a depuis été rapidement adopté, tant par les consommateurs que par les entreprises.

RAG utilise un processus en deux étapes. Il récupère d'abord les informations pertinentes depuis une mémoire externe, puis les exploite pour générer des réponses plus précises. Le succès d'un système RAG dépend de la qualité de son moteur de recherche. Les moteurs de recherche basés sur les termes, tels qu'Elasticsearch et BM25, sont beaucoup plus simples à implémenter et constituent d'excellentes bases de référence. Les moteurs de recherche basés sur les plongements lexicaux sont plus gourmands en ressources de calcul, mais peuvent potentiellement surpasser les algorithmes basés sur les termes.

La recherche par plongement est rendue possible grâce à la recherche vectorielle, qui constitue également la base de nombreuses applications Internet essentielles telles que les moteurs de recherche et les systèmes de recommandation. De nombreux algorithmes de recherche vectorielle développés pour ces applications peuvent être utilisés pour la recherche par agrégation de vecteurs (RAG).

Le modèle RAG peut être considéré comme un cas particulier d'agent, où le récupérateur est un outil utilisable par le modèle. Ces deux modèles permettent à un modèle de s'affranchir des limitations de son contexte et de rester plus à jour, mais le modèle agentique offre des possibilités encore plus étendues. Un agent est défini par son environnement et les outils auxquels il a accès. Dans un agent doté d'IA, l'IA joue le rôle de planificateur : elle analyse la tâche qui lui est confiée, envisage différentes solutions et sélectionne la plus prometteuse. La résolution d'une tâche complexe peut nécessiter de nombreuses étapes, ce qui requiert un modèle puissant pour la planification. La capacité de planification d'un modèle peut être renforcée par la réflexion et un système de mémoire lui permettant de suivre sa progression.

Plus un modèle est doté d'outils, plus ses capacités s'accroissent, lui permettant de résoudre des tâches complexes. Cependant, plus l'agent est automatisé, plus ses défaillances peuvent avoir des conséquences catastrophiques. L'utilisation d'outils expose les agents à de nombreux risques de sécurité, abordés au [chapitre 5.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) Pour que les agents fonctionnent en conditions réelles, des mécanismes de défense rigoureux doivent être mis en place.

RAG et les agents manipulent une grande quantité d'informations, dépassant souvent la longueur maximale du contexte du modèle sous-jacent. Il est donc nécessaire d'introduire un système de mémoire pour gérer et utiliser toutes les informations contenues dans un modèle. Ce chapitre s'est conclu par une brève description de ce composant.

RAG et les agents sont deux méthodes basées sur des incitations, car elles influencent la qualité du modèle uniquement par le biais d'entrées, sans modifier le modèle lui-même. Bien qu'elles permettent de nombreuses applications remarquables, la modification du modèle sous-jacent ouvre des perspectives encore plus vastes. La manière d'y parvenir sera abordée dans le chapitre suivant.

[1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1227-marker)Le modèle utilisé était un type de [réseau neuronal récurrent](https://en.wikipedia.org/wiki/Recurrent_neural_network) appelé [LSTM](https://en.wikipedia.org/wiki/Long_short-term_memory) (Long Short-Term Memory). LSTM était l'architecture dominante de l'apprentissage profond pour le traitement automatique du langage naturel (TALN) avant que l'architecture Transformer ne prenne le relais en 2018.

[2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1228-marker)À peu près au même moment, un autre article, également de Facebook, intitulé « How Context Affects Language Models' Factual Predictions » ( [Petroni et al., _arXiv_ , mai 2020](https://arxiv.org/abs/2005.04611) ), a montré que l'ajout d'un système de récupération à un modèle de langage pré-entraîné pouvait considérablement améliorer les performances du modèle sur les questions factuelles.

[3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1229-marker)Merci à Chetan Tekur pour l'exemple.

[4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1230-marker)La loi de Parkinson est généralement formulée ainsi : « Le travail s’étend de manière à occuper tout le temps disponible pour son achèvement. » J’ai une théorie similaire selon laquelle le contexte d’une application s’étend jusqu’à occuper toute la limite de contexte prise en charge par le modèle qu’elle utilise.

[5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1238-marker)La recherche d'informations a été décrite dès les années 1920 dans les brevets d'Emanuel Goldberg pour une « machine statistique » permettant de rechercher des documents stockés sur films. Voir [« The History of Information Retrieval Research »](https://oreil.ly/-JJYn) (Sanderson et Croft, _Proceedings of the IEEE, 100 : Numéro spécial du centenaire,_ avril 2012).

[6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1245-marker)Pour ceux qui souhaitent en savoir plus sur BM25, je recommande cet article des auteurs de BM25 : [« The Probabilistic Relevance Framework: BM25 and Beyond »](https://oreil.ly/aDmhb) (Robertson et Zaragoza, _Foundations and Trends in Information Retrieval_ 3 No. 4, 2009).

[7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1246-marker) [Aravind Srinivas, le PDG de Perplexity](https://x.com/AravSrinivas/status/1737886080555446552) , a tweeté : « Il est difficile d’apporter une véritable amélioration par rapport à BM25 ou à la recherche en texte intégral. »

[8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1251-marker)Un flux de travail de récupération RAG partage de nombreuses étapes similaires avec le système de recommandation traditionnel.

[9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1296-marker)Certaines équipes m'ont indiqué que leurs systèmes de recherche fonctionnent mieux lorsque les données sont organisées sous forme de questions-réponses.

[10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1313-marker) _L'ouvrage *Artificial Intelligence: A Modern Approach*_ (1995) définit un agent comme tout ce qui peut être considéré comme percevant son environnement grâce à des capteurs et agissant sur cet environnement grâce à des actionneurs.

[11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1315-marker)Au début, on reprochait aux agents de ne servir qu'à épuiser les crédits API.

[12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1324-marker)Étant donné que la plupart des flux de travail multi-agents sont suffisamment complexes pour impliquer plusieurs composants, la plupart des agents sont multi-agents.

[13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1330-marker)Chameleon ( [Lu et al., 2023](https://arxiv.org/abs/2304.09842) ) appelle ce traducteur un générateur de programmes.

[14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1335-marker)Cela me rappelle la méthode de l'agent acteur-critique (AC) ( [Konda et Tsitsiklis, 1999](https://oreil.ly/UziTE) ) dans l'apprentissage par renforcement.

[15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1357-marker)Dans les conversations humaines, l'inverse pourrait être vrai si les premiers messages sont des formules de politesse.

[16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#id1358-marker)Les stratégies basées sur l'utilisation, comme la suppression des informations les moins fréquemment utilisées, sont plus complexes, car il faut pouvoir savoir quand un modèle utilise une information donnée.