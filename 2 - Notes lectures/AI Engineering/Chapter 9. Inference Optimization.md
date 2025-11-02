Les nouveaux modèles apparaissent et disparaissent, mais une chose demeure essentielle : les rendre meilleurs, moins chers et plus rapides. Jusqu’à présent, cet ouvrage a abordé diverses techniques d’amélioration des modèles. Ce chapitre se concentre sur leur optimisation en termes de vitesse et de coût.

Aussi performant soit votre modèle, s'il est trop lent, vos utilisateurs risquent de s'impatienter, voire pire, ses prédictions pourraient devenir inutiles : imaginez un modèle de prédiction du cours de l'action pour le lendemain qui met deux jours à calculer chaque résultat. Si votre modèle est trop coûteux, son retour sur investissement ne sera pas rentable.

L'optimisation de l'inférence peut être effectuée aux niveaux du modèle, du matériel et du service. Au niveau du modèle, il est possible de réduire la taille d'un modèle entraîné ou de développer des architectures plus efficaces, par exemple sans les goulots d'étranglement de calcul liés au mécanisme d'attention souvent utilisé dans les modèles Transformer. Au niveau du matériel, il est possible de concevoir un matériel plus performant.

Le service d'inférence exécute le modèle sur le matériel spécifié afin de répondre aux requêtes des utilisateurs. Il peut intégrer des techniques d'optimisation des modèles pour des configurations matérielles spécifiques. Il doit également prendre en compte les schémas d'utilisation et de trafic pour allouer efficacement les ressources et ainsi réduire la latence et les coûts.

C’est pourquoi l’optimisation de l’inférence est un domaine interdisciplinaire qui voit souvent une collaboration entre les chercheurs en modélisation, les développeurs d’applications, les ingénieurs système, les concepteurs de compilateurs, les architectes matériels et même les opérateurs de centres de données.

Ce chapitre aborde les obstacles à l'inférence en IA et les techniques permettant de les surmonter. Il se concentrera principalement sur l'optimisation au niveau du modèle et du service, et présentera un aperçu des accélérateurs d'IA.

Ce chapitre aborde également les indicateurs de performance et les compromis nécessaires. Parfois, une technique permettant d'accélérer un modèle peut aussi en réduire le coût. Par exemple, diminuer la précision d'un modèle le rend plus compact et plus rapide. Cependant, l'optimisation implique souvent des compromis. Par exemple, un matériel performant peut accélérer l'exécution du modèle, mais au prix d'un coût plus élevé.

Face à la disponibilité croissante de modèles open source, de plus en plus d'équipes développent leurs propres services d'inférence. Toutefois, même sans implémenter ces techniques d'optimisation, leur compréhension vous aidera à évaluer les services et frameworks d'inférence. Si la latence et le coût de votre application vous pénalisent, poursuivez votre lecture. Ce chapitre pourrait vous aider à diagnostiquer les causes et les solutions potentielles.

# Comprendre l'optimisation de l'inférence

Le cycle de vie d'un modèle d'IA comprend deux phases distinctes : l'entraînement et l'inférence. L'entraînement désigne le processus de construction du modèle. L'inférence désigne le processus d'utilisation du modèle pour calculer une sortie à partir d'une entrée donnée. [À](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1597) moins d'entraîner ou d'affiner un modèle, vous n'aurez principalement à vous soucier de l'inférence [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1598)

Cette section débute par une présentation de l'inférence, introduisant un vocabulaire commun qui servira à aborder le reste du chapitre. Si ces concepts vous sont déjà familiers, vous pouvez passer directement à la section qui vous intéresse.

## Aperçu de l'inférence

En production, le composant qui exécute l'inférence des modèles est appelé serveur d'inférence. Il héberge les modèles disponibles et dispose du matériel nécessaire. En fonction des requêtes des applications (par exemple, les invites des utilisateurs), il alloue les ressources nécessaires à l'exécution des modèles appropriés et renvoie les réponses aux utilisateurs.[Un serveur d'inférence fait partie d'un service d'inférence plus vaste, qui est également chargé de recevoir, d'acheminer et, éventuellement, de prétraiter les requêtes avant qu'elles n'atteignent le serveur d'inférence. La figure 9-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_1_1730130962952524) illustre un service d'inférence simple .

.

![Schéma d'un système matériel informatique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0901.png)

###### Figure 9-1. Un service d'inférence simple.

Les API de modèles, comme celles proposées par OpenAI et Google, sont des services d'inférence. Si vous utilisez l'un de ces services, vous n'aurez pas à implémenter la plupart des techniques présentées dans ce chapitre. En revanche, si vous hébergez vous-même un modèle, il vous incombera de concevoir, d'optimiser et de maintenir son service d'inférence.

### Goulots d'étranglement informatiques

L'optimisation consiste à identifier les goulots d'étranglement et à les résoudre. Par exemple, pour optimiser le trafic, les urbanistes peuvent identifier les points de congestion et prendre des mesures pour les fluidifier. De même, un serveur d'inférence doit être conçu pour pallier les goulots d'étranglement de calcul des charges de travail d'inférence qu'il traite. Il existe deux principaux types de goulots d'étranglement : ceux _liés à la puissance de calcul_ et _ceux liés à la bande passante mémoire_ .

Limité par le calcul

Cela concerne les tâches dont le temps d'exécution est déterminé par la puissance de calcul nécessaire. Par exemple, le déchiffrement d'un mot de passe est généralement limité par la puissance de calcul en raison des calculs mathématiques intensifs requis pour casser les algorithmes de chiffrement.

Limité par la bande passante de la mémoire

Ces tâches sont limitées par le débit de transfert de données au sein du système, notamment la vitesse de déplacement des données entre la mémoire et les processeurs. Par exemple, si vous stockez vos données dans la mémoire du processeur et entraînez un modèle sur des GPU, vous devez transférer les données du processeur vers le GPU, ce qui peut prendre beaucoup de temps. On parle alors de limitation par la bande passante. Dans la littérature, cette limitation est souvent désignée par le terme « limitation par la mémoire ».

---
#### Ambiguïté terminologique : Limité par la mémoire versus limité par la bande passante

_L'expression « Memory-bound »_ est également utilisée par certains pour désigner les tâches dont le temps d'exécution est limité par la capacité de la mémoire plutôt que par sa bande passante. Cela se produit lorsque le matériel ne dispose pas de suffisamment de mémoire pour traiter la tâche, par exemple, si votre ordinateur ne possède pas assez de mémoire pour stocker l'intégralité d'Internet. Ce problème de mémoire se manifeste souvent par l'erreur bien connue des ingénieurs : OOM (mémoire insuffisante) [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1605)

Cependant, il est souvent possible d'atténuer ce problème en divisant la tâche en sous-tâches. Par exemple, si la mémoire du GPU est limitée et qu'il est impossible d'y intégrer un modèle entier, vous pouvez le répartir entre la mémoire du GPU et celle du CPU. Cette répartition ralentira le calcul en raison du temps de transfert des données entre le CPU et le GPU. Toutefois, si ce transfert est suffisamment rapide, ce problème est moins important. Par conséquent, la limitation de capacité mémoire est en réalité davantage liée à la bande passante.

---

Les concepts de limitation par le calcul ou par la bande passante mémoire ont été introduits dans l'article « Roofline » ( [Williams et al., 2009](https://oreil.ly/M_aGR) ). [Mathématiquement](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1606) , une opération peut être classée comme limitée par le calcul ou par la bande passante mémoire en fonction de son [_intensité arithmétique_](https://oreil.ly/K3j6t) , c'est-à-dire le nombre d'opérations arithmétiques par octet d'accès mémoire. Les outils de profilage comme NVIDIA Nsight affichent un graphique en forme de toit (roofline chart) pour indiquer si votre charge de travail est limitée par le calcul ou par la bande passante mémoire, comme illustré dans [la figure 9-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_2_1730130962952613) . Ce graphique est appelé « _roofline_ chart » car sa forme rappelle celle d'un toit. Les graphiques en forme de toit sont couramment utilisés dans l'analyse des performances matérielles.

Différentes techniques d'optimisation visent à atténuer différents goulots d'étranglement. Par exemple, une charge de travail gourmande en calcul peut être accélérée en la répartissant sur un plus grand nombre de puces ou en utilisant des puces plus puissantes (par exemple, un nombre d'opérations en virgule flottante par seconde plus élevé). Une charge de travail gourmande en bande passante mémoire peut être accélérée en utilisant des puces à bande passante plus élevée.

![Graphique avec une ligne et un point. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0902.png)

###### Figure 9-2. Le graphique de la courbe de performance permet de visualiser si une opération est limitée par la puissance de calcul ou par la bande passante mémoire. Ce graphique est à échelle logarithmique.

Les différentes architectures de modèles et les charges de travail entraînent des goulots d'étranglement de calcul différents. Par exemple, l'inférence pour les générateurs d'images comme Stable Diffusion est généralement limitée par la puissance de calcul, tandis que l'inférence pour les modèles de langage autorégressifs est généralement limitée par la bande passante mémoire.

Prenons l'exemple de l'inférence dans un modèle de langage. Rappelons-nous du [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) que l'inférence pour un modèle de langage basé sur les transformeurs se compose de deux étapes : le préremplissage et le décodage.

**Préremplissage**

Le modèle traite les jetons d'entrée en parallèle. Le [nombre](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1607) de jetons pouvant être traités simultanément est limité par le nombre d'opérations que votre matériel peut exécuter dans un laps de temps donné. Par conséquent, le préremplissage est _limité par la puissance de calcul_ .

**Décoder**

Le modèle génère un jeton de sortie à la fois. Concrètement, cette étape consiste généralement à charger de grandes matrices (par exemple, les poids du modèle) dans les GPU, ce qui est limité par la vitesse à laquelle le matériel peut charger les données en mémoire. Le décodage est donc _limité par la bande passante mémoire_ .

[La figure 9-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_3_1730130962952638) visualise le préremplissage et le décodage.

![Schéma d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0903.png)

###### Figure 9-3. Les modèles de langage autorégressifs suivent deux étapes pour l'inférence : le préremplissage et le décodage. `<eos>`désigne la fin du jeton de la séquence.

Étant donné que le préremplissage et le décodage ont des profils de calcul différents, ils sont souvent découplés en production sur des machines distinctes. Cette technique sera abordée dans le cadre de [l’« Optimisation du service d’inférence »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_service_optimization_1730130963008735) .

Les facteurs qui influent sur la quantité de calculs de préremplissage et de décodage dans un serveur d'inférence LLM, et donc sur ses goulots d'étranglement, comprennent la longueur du contexte, la longueur de la sortie et les stratégies de regroupement des requêtes. Un contexte long entraîne généralement une charge de travail limitée par la bande passante mémoire, mais des techniques d'optimisation intelligentes, telles que celles présentées plus loin dans ce chapitre, permettent de lever ce goulot d'étranglement.

À l'heure actuelle, en raison de la prédominance de l'architecture Transformer et des limitations des technologies d'accélération existantes, de nombreuses charges de travail d'IA et de données sont limitées par la bande passante mémoire. Cependant, les progrès futurs en matière de logiciels et de matériels permettront de rendre ces charges de travail limitées par la puissance de calcul.

### API d'inférence en ligne et par lots

De nombreux fournisseurs proposent deux types d'API d'inférence : en ligne et par lots :

- Les API en ligne sont optimisées pour minimiser la latence. Les requêtes sont traitées dès leur arrivée.
    
- Les API par lots optimisent les coûts. Si votre application n'a pas d'exigences de latence strictes, vous pouvez l'envoyer à des API par lots pour un traitement plus efficace. Une latence plus élevée permet un plus large éventail de techniques d'optimisation, notamment le regroupement des requêtes et l'utilisation de matériel moins coûteux. Par exemple, à l'heure actuelle, les deuxGoogle Gemini et OpenAI proposent des API par lots avec une réduction de coût de 50 % et un délai d'exécution nettement plus rapide, c'est-à-dire de l'ordre de quelques heures au lieu de quelques secondes ou minutes. [6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1612)
    

Les API en ligne peuvent toujours regrouper les requêtes tant que cela n'a pas d'impact significatif sur la latence, comme expliqué dans [la section « Traitement par lots »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_batching_1730130963008799) . La seule différence notable est que les API en ligne privilégient une faible latence, tandis que les API par lots privilégient un débit plus élevé.

Les cas d'utilisation orientés client, tels que les chatbots et la génération de code, nécessitent généralement une faible latence et, par conséquent, privilégient les API en ligne. Les cas d'utilisation avec des exigences de latence moins strictes, idéaux pour les API par lots, incluent les suivants :

- génération de données synthétiques
    
- Des rapports périodiques, tels que la synthèse des messages Slack, l'analyse des sentiments exprimés lors des mentions de la marque sur les réseaux sociaux et l'analyse des tickets d'assistance client.
    
- Intégration des nouveaux clients nécessitant le traitement de tous leurs documents téléchargés
    
- Migration vers un nouveau modèle nécessitant le retraitement de toutes les données
    
- Générer des recommandations ou des newsletters personnalisées pour une large clientèle
    
- Mise à jour de la base de connaissances par réindexation des données d'une organisation
    

Les API renvoient généralement des réponses complètes par défaut. Cependant, avec le décodage autorégressif, le traitement d'une réponse par un modèle peut être long, ce qui peut agacer les utilisateurs. De nombreuses API en ligne proposent _un mode de flux continu_ , qui renvoie chaque jeton au fur et à mesure de sa génération. Cela réduit le temps d'attente des utilisateurs avant l'obtention du premier jeton. L'inconvénient de cette approche est qu'il est impossible d'évaluer la qualité d'une réponse avant de l'afficher, ce qui augmente le risque que les utilisateurs reçoivent des réponses erronées. Toutefois, il est toujours possible de modifier ou de supprimer une réponse a posteriori dès qu'un risque est détecté.

---
###### Avertissement

L'API par lots pour les modèles de base diffère de l'inférence par lots pour l'apprentissage automatique traditionnel. En apprentissage automatique traditionnel :

- L'inférence en ligne signifie que les prédictions sont calculées _après_ la réception des requêtes.
    
- L'inférence par lots signifie que les prédictions sont précalculées _avant même_ l'arrivée des requêtes.
    

Le précalcul est possible pour les cas d'utilisation avec des entrées finies et prévisibles, comme les systèmes de recommandation, où des recommandations peuvent être générées à l'avance pour tous les utilisateurs. Ces prédictions précalculées sont récupérées lors de la réception des requêtes, par exemple lorsqu'un utilisateur visite le site web. Cependant, avec les cas d'utilisation du modèle de base où les entrées sont ouvertes, il est difficile de prédire toutes les interactions des utilisateurs..[7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1619)

---
## Métriques de performance d'inférence

Avant de se lancer dans l'optimisation, il est important de comprendre les indicateurs à optimiser. Du point de vue de l'utilisateur, l'axe principal est la latence (la qualité de la réponse dépend du modèle lui-même, et non du service d'inférence). Cependant, les développeurs d'applications doivent également prendre en compte le débit et l'utilisation des ressources pour déterminer le coût de leurs applications.

### Latence, TTFT et TPOT

La latence mesure le temps écoulé entre l'envoi d'une requête par l'utilisateur et la réception de la réponse complète. Pour la génération autorégressive, notamment en mode flux continu, la latence globale peut être décomposée en plusieurs indicateurs :

**Temps d'attente avant le premier jeton**

Le TTFT mesure la rapidité avec laquelle le premier jeton est généré après l'envoi d'une requête par l'utilisateur. Il correspond à la durée de l'étape de préremplissage et dépend de la longueur de la requête. Les attentes des utilisateurs concernant le TTFT peuvent varier selon les applications. Par exemple, pour les chatbots conversationnels, le TTFT devrait être instantané.⁸ [Cependant](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1620) , les utilisateurs peuvent accepter d'attendre plus longtemps pour résumer des documents longs.

**Temps par jeton de sortie**

TPOT mesure la rapidité avec laquelle chaque jeton de sortie est généré après le premier. Si chaque jeton prend 100 ms, une réponse de 1 000 jetons prendra 100 s.

En mode flux continu, où les utilisateurs lisent chaque jeton au fur et à mesure de sa génération, le TPOT doit être plus rapide que la vitesse de lecture humaine, sans toutefois nécessiter une différence significative. Un lecteur très rapide peut lire un jeton en 120 ms ; un TPOT d'environ 120 ms, soit 6 à 8 jetons par seconde, est donc suffisant dans la plupart des cas.

**Délai entre les jetons et latence inter-jetons**

Les variantes de cette métrique incluent _le temps entre les jetons (TBT)_ et _la latence entre les jetons (ITL)_ . [9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1623) Les deux mesurent le temps entre les jetons de sortie.

La latence totale sera égale `TTFT + TPOT` à × `(number of output tokens).`

Deux applications présentant la même latence totale peuvent offrir des expériences utilisateur différentes avec des TTFT et TPOT différents. Vos utilisateurs préféreraient-ils obtenir le premier jeton instantanément, quitte à attendre plus longtemps entre les jetons, ou préféreraient-ils patienter légèrement plus longtemps pour le premier jeton, mais bénéficier d'une génération de jetons plus rapide par la suite ? Des études utilisateurs seront nécessaires pour déterminer l'expérience utilisateur optimale. Il est possible de réduire le TTFT au prix d'un TPOT plus élevé en transférant davantage d'instances de calcul du décodage vers le préremplissage et inversement [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1624)

Il est important de noter que les valeurs TTFT et TPOT observées par les utilisateurs peuvent différer de celles observées par les modèles, notamment dans les scénarios impliquant des requêtes de type « chaîne de pensée » (CoT) ou des requêtes automatisées où les modèles génèrent des étapes intermédiaires non affichées aux utilisateurs. Certaines équipes utilisent la métrique « _temps de publication »_ pour indiquer clairement qu'elle mesure le temps nécessaire à l'affichage du premier jeton pour les utilisateurs.

Prenons l'exemple où, après l'envoi d'une requête par un utilisateur, le modèle effectue les étapes suivantes :

1. Générez un plan, qui consiste en une séquence d'actions. Ce plan n'est pas montré à l'utilisateur.
    
2. Effectuez des actions et consignez leurs résultats. Ces résultats ne sont pas affichés à l'utilisateur.
    
3. À partir de ces résultats, générez une réponse finale à afficher à l'utilisateur.
    

Du point de vue du modèle, le premier jeton est généré à l'étape 1. C'est à ce moment que le modèle entame son processus interne de génération de jetons. L'utilisateur, quant à lui, ne voit que le premier jeton du résultat final généré à l'étape 3. Par conséquent, de son point de vue, le TTFT est beaucoup plus long.

La latence étant une distribution, la moyenne peut être trompeuse. Imaginez 10 requêtes dont les valeurs TTFT sont : 100 ms, 102 ms, 100 ms, 100 ms, 99 ms, 104 ms, 110 ms, 90 ms, 3 000 ms et 95 ms. La valeur TTFT moyenne est de 390 ms, ce qui donne l’impression que votre service d’inférence est plus lent qu’il ne l’est réellement. Il se peut qu’une erreur réseau ait ralenti une requête ou qu’une invite particulièrement longue ait nécessité un temps de pré-remplissage plus important. Dans tous les cas, une investigation s’impose. Avec un volume important de requêtes, les valeurs aberrantes qui faussent la latence moyenne sont quasi inévitables.

Il est plus pertinent d'analyser la latence en percentiles, car ils fournissent des informations sur un certain pourcentage de vos requêtes. Le percentile le plus courant est le 50e percentile, abrégé en p50 (médiane). Si la médiane est de 100 ms, cela signifie que la moitié des requêtes mettent plus de 100 ms pour générer le premier jeton, et l'autre moitié moins de 100 ms. Les percentiles permettent également de détecter les valeurs aberrantes, qui peuvent indiquer un problème. Généralement, les percentiles à surveiller sont p90, p95 et p99. Il est également utile de représenter graphiquement les valeurs TTFT en fonction de la longueur des entrées.

### Débit et débit utile

Le débit mesure le nombre de jetons de sortie par seconde qu'un service d'inférence peut générer pour l'ensemble des utilisateurs et des requêtes.

Certaines équipes prennent en compte à la fois les jetons d'entrée et de sortie dans le calcul du débit. Cependant, comme le traitement des jetons d'entrée (préremplissage) et la génération des jetons de sortie (décodage) présentent des goulots d'étranglement différents et sont souvent découplés sur les serveurs d'inférence modernes, le débit d'entrée et de sortie doit être comptabilisé séparément. Lorsque le terme « débit » est utilisé sans précision, il se réfère généralement aux jetons de sortie.

Le débit est généralement mesuré en jetons par seconde (TPS). Si vous gérez plusieurs utilisateurs, le nombre de jetons par utilisateur est également utilisé pour évaluer la capacité du système à gérer un plus grand nombre d'utilisateurs.

Le débit peut également être mesuré en nombre de requêtes _traitées_ pendant une période donnée. De nombreuses applications utilisent le nombre de requêtes par seconde (RPS). Cependant, pour les applications reposant sur des modèles de base, le traitement d'une requête peut prendre plusieurs secondes ; c'est pourquoi on utilise souvent le nombre de requêtes traitées par minute (RPM). Le suivi de cette métrique est utile pour comprendre comment un service d'inférence gère les requêtes simultanées. Certains fournisseurs peuvent limiter votre débit si vous envoyez trop de requêtes simultanées.

Le débit est directement lié au coût de calcul. Un débit plus élevé signifie généralement un coût plus faible. Si votre système coûte 2 $/h en calcul et que son débit est de 100 jetons/s, le coût est d'environ 5,556 $ par million de jetons de sortie. Si chaque requête génère en moyenne 200 jetons de sortie, le coût de décodage de 1 000 requêtes serait de 1,11 $.

Le coût du préremplissage se calcule de la même manière. Si votre matériel coûte 2 $ de l'heure et qu'il peut préremplir 100 requêtes par minute, le coût du préremplissage de 1 000 requêtes sera de 0,33 $.

Le coût total par requête correspond à la somme des coûts de préremplissage et de décodage. Dans cet exemple, le coût total pour 1 000 requêtes serait de 1,11 $ + 0,33 $ = 1,44 $.

Le débit considéré comme bon dépend du modèle, du matériel et de la charge de travail. Les modèles plus compacts et les puces haut de gamme offrent généralement un débit plus élevé. Les charges de travail dont les longueurs d'entrée et de sortie sont constantes sont plus faciles à optimiser que celles dont les longueurs sont variables.

Même pour des modèles, du matériel et des charges de travail de taille similaire, les comparaisons directes de débit peuvent n'être qu'approximatives, car le nombre de jetons dépend de leur définition et les différents modèles utilisent des tokeniseurs différents. Il est préférable de comparer l'efficacité des serveurs d'inférence à l'aide de métriques telles que le coût par requête.

Comme la plupart des applications logicielles, les applications d'IA présentent un compromis entre latence et débit. Des techniques telles que le traitement par lots permettent d'améliorer le débit tout en réduisant la latence. D'après l'équipe IA de LinkedIn, dans son bilan après un an de déploiement de produits d'IA générative ( [LinkedIn, 2024](https://www.linkedin.com/blog/engineering/generative-ai/musings-on-building-a-generative-ai-product?_l=en_US) ), il est fréquent de doubler, voire de tripler le débit en acceptant de sacrifier le TTFT et le TPOT.

En raison de ce compromis, se concentrer sur un service d'inférence uniquement en fonction de son débit et de son coût peut nuire à l'expérience utilisateur. C'est pourquoi certaines équipes privilégient le [_« goodput »_](https://en.wikipedia.org/wiki/Goodput) , une métrique issue des réseaux et adaptée aux applications LLM. Le « goodput » mesure le nombre de requêtes par seconde qui respectent l'objectif de niveau de service (SLO).

Imaginez que votre application ait les objectifs suivants : un TTFT (temps de réponse avant le test) inférieur ou égal à 200 ms et un TPOT (temps de réponse total) inférieur ou égal à 100 ms. Supposons que votre service d’inférence puisse traiter 100 requêtes par minute. Cependant, parmi ces 100 requêtes, seules 30 satisfont l’objectif de niveau de service (SLO). Le débit utile de ce service est donc de 30 requêtes par minute.Une visualisation de ceci est présentée dans [la figure 9-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_4_1730130962952660) .

![Graphique affichant des barres de différentes couleurs. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0904.png)

###### Figure 9-4. Si un service d'inférence peut effectuer 10 RPS mais que seulement 3 satisfont le SLO, alors son débit utile est de 3 RPS.

### Utilisation, MFU et MBU

Les indicateurs d'utilisation mesurent l'efficacité avec laquelle une ressource est utilisée. Ils quantifient généralement la proportion de la ressource activement utilisée par rapport à sa capacité totale disponible.

_L'utilisation du GPU_ est une mesure courante, mais souvent mal comprise , et NVIDIA est en partie responsable de cette confusion. L'outil officiel NVIDIA de surveillance de l'utilisation du GPU est [`nvidia-smi`](https://oreil.ly/ludJ2)SMI (System Management Interface). Cet outil affiche notamment l'utilisation du GPU, qui représente le pourcentage de temps pendant lequel le GPU est actif et traite des tâches. Par exemple, si vous exécutez une inférence sur un cluster de GPU pendant 10 heures et que les GPU sont actifs pendant 5 de ces heures, l'utilisation du GPU sera de 50 %.

Cependant, le fait de traiter activement des tâches ne signifie pas nécessairement les traiter efficacement. Prenons l'exemple d'un petit GPU capable d'effectuer 100 opérations par seconde. Selon `nvidia-smi`la définition de l'utilisation de [nom du logiciel/outil], ce GPU peut afficher un taux d'utilisation de 100 % même s'il n'effectue qu'une seule opération par seconde.

Si vous payez pour une machine capable d'effectuer 100 opérations et que vous ne l'utilisez que pour une seule, vous gaspillez de l'argent. `nvidia-smi`L'indicateur d'optimisation GPU de [nom de la plateforme] est donc peu pertinent. Un indicateur d'utilisation plus utile, parmi toutes les opérations qu'une machine est capable de calculer, est le nombre d'opérations qu'elle effectue dans un laps de temps donné. Cet indicateur est appelé _MFU (Model FLOP/s Utilization)_ , ce qui le distingue de l'indicateur d'utilisation GPU de NVIDIA.

Le MFU est le rapport entre le débit observé (jetons/s) et le débit maximal théorique d'un système fonctionnant à sa puissance de calcul maximale (FLOP/s). Si, à la puissance de calcul maximale annoncée par le fabricant de la puce, celle-ci peut générer 100 jetons/s, mais que, lors de son utilisation pour votre service d'inférence, elle ne peut en générer que 20, votre MFU est de 20 % [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1637)

De même, la bande passante mémoire étant coûteuse, il est important de connaître l'efficacité de son utilisation. _Le MBU (Model Bandwidth Utilization)_ mesure le pourcentage de bande passante mémoire maximale utilisée. Si la bande passante maximale de la puce est de 1 To/s et que votre inférence n'utilise que 500 Go/s, votre MBU est de 50 %.

Le calcul de la bande passante mémoire utilisée pour l'inférence LLM est simple :
```
nombre de paramètres × octets/paramètre × jetons/s
```
Le MBU est calculé comme suit :
```
(nombre de paramètres × octets/paramètre × jetons/s) / (bande passante théorique)
```
Par exemple, si vous utilisez un modèle à 7 milliards de paramètres en FP16 (deux octets par paramètre) et atteignez 100 jetons/s, la bande passante utilisée est :
```
7B × 2 × 100 = 700 Go/s
```
Ceci souligne l'importance de la quantification (abordée au [chapitre 7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) ). Moins d'octets par paramètre signifie que votre modèle consomme moins de bande passante précieuse.

Si cette opération est effectuée sur un GPU A100-80GB avec une bande passante mémoire théorique de 2 To/s, la MBU est :
```
(700 Go/s) / (2 To/s) = 70 %
```
Les relations entre le débit (jetons/s) et le MBU et entre le débit et le MFU sont linéaires, donc certaines personnes pourraient utiliser le débit pour faire référence au MBU et au MFU.

Les valeurs considérées comme optimales pour la MFU et la MBU dépendent du modèle, du matériel et de la charge de travail. Les charges de travail gourmandes en calcul présentent généralement une MFU plus élevée et une MBU plus faible, tandis que celles gourmandes en bande passante affichent souvent une MFU plus faible et une MBU plus élevée.

L'entraînement bénéficiant d'une optimisation plus efficace (par exemple, un meilleur traitement par lots) grâce à des charges de travail plus prévisibles, le MFU est généralement plus élevé pour l'entraînement que pour l'inférence. Pour l'inférence, le préremplissage étant limité par la puissance de calcul et le décodage par la bande passante mémoire, le MFU est généralement plus élevé lors du préremplissage que lors du décodage. À l'heure actuelle, pour l'entraînement de modèles, un MFU supérieur à 50 % est généralement considéré comme satisfaisant, mais peut être difficile à atteindre sur certains matériels. [Le](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1638) [tableau 9-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_table_1_1730130962971021) présente le MFU pour plusieurs modèles et accélérateurs.

Tableau 9-1. Exemples MFU tirés de « PaLM : Scaling Language Modeling with Pathways » (Chowdhery et al., 2022).

|Modèle|Nombre de paramètres (en milliards)|Puces d'accélération|Utilisation du modèle FLOP/s|
|---|---|---|---|
|GPT-3|175B|V100|21,3%|
|Gopher|280B|4096 TPU v3|32,5%|
|Megatron-Turing NLG|530B|2240 A100|30,2%|
|Palmier|540B|6144 TPU v4|46,2%|

[La figure 9-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_5_1730130962952692) présente le MBU (Modèle de Calcul Basé) pour le processus d'inférence utilisant Llama 2-70B en FP16 sur différentes configurations matérielles. La baisse observée est probablement due à la charge de calcul plus élevée par seconde avec un plus grand nombre d'utilisateurs, ce qui fait passer la charge de travail d'une limitation par la bande passante à une limitation par la puissance de calcul.

![Graphique représentant le nombre d'utilisateurs. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0905.png)

###### Figure 9-5. L’utilisation de la bande passante pour Llama 2-70B en FP16 sur trois puces différentes montre une diminution du MBU à mesure que le nombre d’utilisateurs simultanés augmente. Image tirée de « LLM Training and Inference with Intel Gaudi 2 AI Accelerators » ( [Databricks, 2024](https://oreil.ly/tOOOD) ).

Les indicateurs d'utilisation sont utiles pour suivre l'efficacité de votre système. Des taux d'utilisation plus élevés pour des charges de travail similaires sur le même matériel signifient généralement que vos services gagnent en efficacité. Cependant, _l'objectif n'est pas d'acquérir les puces avec le taux d'utilisation le plus élevé_ . Ce qui compte vraiment, c'est d'effectuer vos tâches plus rapidement et à moindre coût. Un taux d'utilisation plus élevé n'a aucun intérêt si le coût et la latence augmentent simultanément..

## Accélérateurs d'IA

La vitesse et le coût d'exécution d'un logiciel dépendent du matériel sur lequel il s'exécute. Bien qu'il existe des techniques d'optimisation universelles, une compréhension approfondie du matériel permet une optimisation plus poussée. Cette section aborde le matériel du point de vue de l'inférence, mais les concepts présentés peuvent également s'appliquer à l'entraînement.

Le développement des modèles d'IA et du matériel a toujours été étroitement lié. Le manque d'ordinateurs suffisamment puissants a été l'un des facteurs ayant contribué au premier hiver de l'IA dans les années 1970.<sup> [13</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1649)

Le regain d'intérêt pour l'apprentissage profond en 2012 était étroitement lié à la puissance de calcul. L'une des raisons généralement admises de la popularité d'AlexNet ( [Krizhevsky et al., 2012](https://oreil.ly/Yv4V7) ) est qu'il s'agissait du premier article à utiliser avec succès [des GPU (processeurs graphiques](https://en.wikipedia.org/wiki/Graphics_processing_unit) [)](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1650) pour entraîner des réseaux de neurones. Avant l'avènement des GPU, entraîner un modèle à l'échelle d'AlexNet nécessitait des milliers de processeurs, comme celui que [Google avait commercialisé quelques mois auparavant](https://oreil.ly/Xpwco) . Comparés à des milliers de processeurs, quelques GPU étaient bien plus accessibles aux doctorants et aux chercheurs, ce qui a déclenché l'essor de la recherche en apprentissage profond.

### Qu'est-ce qu'un accélérateur ?

Un accélérateur est une puce conçue pour accélérer un type spécifique de calcul. Un accélérateur d'IA est conçu pour les calculs d'IA. Le type d'accélérateur d'IA dominant est le GPU, et le principal moteur économique de l'essor de l'IA au début des années 2020 est sans conteste NVIDIA.

La principale différence entre les CPU et les GPU est que les CPU sont conçus pour une utilisation générale, tandis que les GPU sont conçus pour le traitement parallèle :

- Les processeurs possèdent quelques cœurs puissants, généralement jusqu'à 64 pour les ordinateurs grand public haut de gamme. Si de nombreux cœurs peuvent gérer efficacement les charges de travail multithread, ils excellent dans les tâches exigeant des performances élevées sur un seul thread, comme l'exécution d'un système d'exploitation, la gestion des opérations d'entrée/sortie ou le traitement de processus séquentiels complexes.
    
- [Les GPU possèdent des milliers de cœurs plus petits et moins puissants, optimisés pour les tâches pouvant](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1651) être décomposées en de nombreux calculs indépendants, comme le rendu graphique et l'apprentissage automatique. L'opération qui constitue la majeure partie des charges de travail d'apprentissage automatique est la multiplication matricielle, qui est hautement parallélisable.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1651)
    

Si la recherche d'un traitement parallèle efficace accroît les capacités de calcul, elle pose des défis en matière de conception de la mémoire et de consommation d'énergie.

Le succès des GPU NVIDIA a inspiré de nombreux accélérateurs conçus pour accélérer les charges de travail d'IA, notamment [les nouvelles générations de GPU d'Advanced Micro Devices (AMD) , le TPU (](https://en.wikipedia.org/wiki/List_of_AMD_graphics_processing_units) [Tensor Processing Unit](https://en.wikipedia.org/wiki/Tensor_Processing_Unit) ) de Google , [le Habana Gaudi d'Intel](https://oreil.ly/oDQOk) , [l'Intelligent Processing Unit](https://oreil.ly/6ySTY) (IPU) de Graphcore, le Language Processing Unit (LPU) [de Groq ,](https://oreil.ly/R7gXn) [le Wafer-Scale](https://oreil.ly/ACIty) [Quant Processing Unit](https://en.wikipedia.org/wiki/List_of_quantum_processors) (QPU) de Cerebras, et bien d'autres encore.

Bien que de nombreuses puces puissent gérer à la fois l'entraînement et l'inférence, une tendance majeure se dessine : celle des puces spécialisées pour l'inférence. Une étude de [Desislavov et al. (2023)](https://oreil.ly/qSpMK) révèle que, dans les systèmes couramment utilisés, le coût de l'inférence peut dépasser celui de l'entraînement et qu'il représente jusqu'à 90 % des coûts d'apprentissage automatique des systèmes d'IA déployés.

Comme indiqué au [chapitre 7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) , l'entraînement nécessite beaucoup plus de mémoire en raison de la rétropropagation et est généralement plus difficile à réaliser avec une précision moindre. De plus, l'entraînement privilégie généralement le débit, tandis que l'inférence vise à minimiser la latence.

Par conséquent, les puces conçues pour l'inférence sont souvent optimisées pour une précision moindre et un accès mémoire plus rapide, plutôt que pour une grande capacité de mémoire. On peut citer comme exemples l'Apple [Neural Engine](https://en.wikipedia.org/wiki/Neural_Engine) , [AWS Inferentia](https://oreil.ly/42LSB) et [MTIA](https://oreil.ly/XH2bh) (Meta Training and Inference Accelerator). Les puces conçues pour l'informatique de périphérie, comme [l'Edge TPU de Google](https://oreil.ly/m8daG) et le [NVIDIA Jetson Xavier](https://oreil.ly/PRZSQ) , sont également généralement orientées vers l'inférence.

[Il existe également](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1652) des puces spécialisées pour différentes architectures de modèles, comme celles destinées aux transformateurs. De nombreuses puces sont conçues pour les centres de données, et de plus en plus sont destinées aux appareils grand public (tels que les téléphones et les ordinateurs portables).

Les différentes architectures matérielles présentent des configurations de mémoire et des unités de calcul spécialisées différentes, qui évoluent au fil du temps. Ces unités sont optimisées pour des types de données spécifiques, tels que les scalaires, les vecteurs ou les tenseurs, comme illustré dans [la figure 9-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_6_1730130962952710) .

![Schéma d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0906.png)

###### Figure 9-6. Différentes primitives de calcul. Image inspirée de [Chen et al. (2018)](https://arxiv.org/abs/1802.04799) .

Une puce peut comporter un ensemble d'unités de calcul différentes, optimisées pour divers types de données. Par exemple, les GPU prenaient traditionnellement en charge les opérations vectorielles, mais de nombreux GPU modernes intègrent désormais des cœurs tensoriels optimisés pour les calculs matriciels et tensoriels. Les TPU, quant à eux, sont conçus avec les opérations tensorielles comme primitive de calcul principale. Pour exécuter efficacement un modèle sur une architecture matérielle, il est nécessaire de prendre en compte l'organisation de sa mémoire et ses primitives de calcul.

Les spécifications d'une puce contiennent de nombreux détails utiles pour évaluer son adéquation à chaque cas d'utilisation. Toutefois, les principales caractéristiques pertinentes pour tous les cas d'utilisation sont la capacité de calcul, la taille et la bande passante de la mémoire, ainsi que la consommation d'énergie. Je prendrai les GPU comme exemple pour illustrer ces caractéristiques.

### capacités de calcul

Les capacités de calcul sont généralement mesurées par le nombre d'opérations qu'une puce peut effectuer dans un laps de temps donné. L'unité de mesure la plus courante est _le FLOP/s_ (ou FLOPS), qui correspond au nombre _maximal_ d'opérations en virgule flottante par seconde. En pratique, il est cependant très improbable qu'une application atteigne ce pic de FLOP/s. Le rapport entre le FLOP/s réel et le FLOP/s théorique constitue un indicateur _d'utilisation_ .

Le nombre d'opérations qu'une puce peut effectuer par seconde dépend de sa précision numérique : plus la précision est élevée, moins la puce peut exécuter d'opérations. Par exemple, l'addition de deux nombres de 32 bits nécessite généralement deux fois plus de calculs que l'addition de deux nombres de 16 bits. Le nombre d'opérations 32 bits qu'une puce peut effectuer dans un temps donné n'est pas exactement la moitié de celui des opérations 16 bits, en raison de l'optimisation propre à chaque puce. Pour une présentation générale de la précision numérique, consultez la [section « Représentations numériques »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07b_numerical_representations_1730159634259493) .

[Le tableau 9-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_table_2_1730130962971057) présente les spécifications FLOP/s pour différents formats de précision pour [les puces NVIDIA H100 SXM](https://oreil.ly/bNAOG) .

Tableau 9-2. Spécifications FLOP/s pour les puces NVIDIA H100 SXM.

|Précision numérique|téraFLOP/s (milliard de FLOP/s) avec parcimonie|
|---|---|
|TF32 Tensor Core [a](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1658)|989|
|Noyau Tensor BFLOAT16|1 979|
|Noyau Tensor FP16|1 979|
|Noyau Tensor FP8|3 958|
|[un](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1658-marker)Rappelons du [chapitre 7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) que TF32 est un format 19 bits et non 32 bits.|   |

### Taille et bande passante de la mémoire

Comme un GPU possède de nombreux cœurs fonctionnant en parallèle, les données doivent fréquemment être transférées de la mémoire vers ces cœurs. Par conséquent, la vitesse de transfert des données est primordiale. Ce transfert est crucial pour les modèles d'IA utilisant de grandes matrices de poids et d'importants volumes de données d'entraînement. Ces données doivent être transférées rapidement afin d'optimiser l'utilisation des cœurs. C'est pourquoi la mémoire GPU doit présenter une bande passante plus élevée et une latence plus faible que la mémoire CPU, et requiert donc des technologies de mémoire plus avancées. C'est l'un des facteurs expliquant le coût plus élevé de la mémoire GPU par rapport à celle du CPU.

Plus précisément, les processeurs utilisent généralement de la mémoire [DDR SDRAM](https://en.wikipedia.org/wiki/DDR_SDRAM) (Double Data Rate Synchronous Dynamic Random-Access Memory), qui possède une structure 2D. Les processeurs graphiques, notamment les haut de gamme, utilisent souvent de la mémoire [HBM](https://en.wikipedia.org/wiki/High_Bandwidth_Memory) (High-Bandwidth Memory), qui possède une structure empilée 3D.<sup> [17</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1661)

La mémoire d'un accélérateur est caractérisée par sa _taille et sa bande passante_ . Ces valeurs doivent être évaluées au sein du système auquel l'accélérateur fait partie. Un accélérateur, tel qu'un GPU, interagit généralement avec trois niveaux de mémoire, comme illustré dans [la figure 9-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_7_1730130962952731) :

mémoire du processeur (DRAM)

Les accélérateurs sont généralement déployés aux côtés des processeurs, leur donnant accès à la mémoire du processeur (également appelée mémoire système, mémoire hôte ou simplement DRAM du processeur).

La mémoire CPU offre généralement la plus faible bande passante parmi ces types de mémoire, avec des vitesses de transfert de données comprises entre 25 et 50 Go/s. Sa capacité varie également. Les ordinateurs portables classiques disposent généralement de 16 à 64 Go, tandis que les stations de travail haut de gamme peuvent atteindre 1 To, voire plus.

Mémoire à large bande passante du GPU (HBM)

Il s'agit de la mémoire dédiée au GPU, située à proximité de celui-ci pour un accès plus rapide que la mémoire du processeur.

La mémoire HBM offre une bande passante nettement supérieure, avec des vitesses de transfert de données généralement comprises entre 256 Go/s et plus de 1,5 To/s. Cette vitesse est essentielle pour gérer efficacement les transferts de données volumineux et les tâches à haut débit. Un GPU grand public possède environ 24 à 80 Go de mémoire HBM.

SRAM intégrée au GPU

Intégrée directement à la puce, cette mémoire sert à stocker les données et instructions fréquemment utilisées pour un accès quasi instantané. Elle comprend des caches L1 et L2 composés de SRAM et, dans certaines architectures, des caches L3. Ces caches font partie de la mémoire embarquée globale, qui inclut également d'autres composants tels que les registres et la mémoire partagée.

La RAM possède des vitesses de transfert de données extrêmement élevées, dépassant souvent 10 To/s. La taille de la SRAM du GPU est faible, généralement de 40 Mo ou moins.

![Une pyramide colorée à plusieurs niveaux. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0907.png)

###### Figure 9-7. Hiérarchie de la mémoire d'un accélérateur d'IA. Les valeurs numériques sont données à titre indicatif uniquement. Les valeurs réelles varient selon les puces.

L'optimisation des GPU repose en grande partie sur l'exploitation optimale de la hiérarchie mémoire. Cependant, à l'heure actuelle, les frameworks populaires tels que PyTorch et TensorFlow ne permettent pas encore un contrôle précis des accès mémoire. De ce fait, de nombreux chercheurs et ingénieurs en IA s'intéressent aux langages de programmation GPU comme [CUDA](https://en.wikipedia.org/wiki/CUDA) (Compute Unified Device Architecture), [Triton d'OpenAI](https://github.com/triton-lang/triton) et [ROCm](https://github.com/ROCm/ROCm) (Radeon Open Compute). Ce dernier est l'alternative open source d'AMD à CUDA, le framework propriétaire de NVIDIA.

### Consommation d'énergie

Les puces utilisent des transistors pour effectuer des calculs. Chaque calcul est réalisé par l'activation et la désactivation de transistors, ce qui consomme de l'énergie. Un GPU peut contenir des milliards de transistors : un NVIDIA A100 en compte [54 milliards](https://oreil.ly/5vRsP) , tandis qu'un NVIDIA H100 en compte [80 milliards](https://en.wikipedia.org/wiki/Hopper_\(microarchitecture\)) . Lorsqu'un accélérateur est utilisé efficacement, des milliards de transistors changent rapidement d'état, consommant une quantité considérable d'énergie et générant une chaleur importante. Cette chaleur nécessite des systèmes de refroidissement, qui consomment également de l'électricité, augmentant ainsi la consommation énergétique globale des centres de données.

La consommation énergétique des puces risque d'avoir un impact environnemental considérable [,](https://oreil.ly/RqY-3) accentuant la pression sur les entreprises pour qu'elles investissent dans des technologies permettant de construire [des centres de données écologiques . Un système NVIDIA H100 fonctionnant à pleine capacité pendant un an](https://en.wikipedia.org/wiki/Green_data_center) [consomme](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1669) environ 7 000 kWh. À titre de comparaison, la consommation électrique annuelle moyenne d'un ménage américain est de 10 000 kWh. C'est pourquoi l'électricité constitue un frein à l'augmentation de la puissance de calcul.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1669)

Les accélérateurs spécifient généralement leur consommation d'énergie sous la forme _d'une consommation de puissance maximale_ ou d'une mesure indirecte appelée _TDP (puissance thermique de conception) :_

- La consommation électrique maximale indique la puissance de pointe que la puce peut consommer en pleine charge.
    
- _Le TDP_ représente la chaleur maximale que le système de refroidissement doit dissiper lorsque la puce fonctionne sous des charges de travail typiques. Bien qu'il ne s'agisse pas d'une mesure exacte de la consommation électrique, il donne une indication de la consommation attendue. Pour les CPU et les GPU, la consommation électrique maximale peut être environ 1,1 à 1,5 fois supérieure au TDP, bien que ce rapport varie en fonction de l'architecture et de la charge de travail.
    

En choisissant des fournisseurs de cloud computing, vous n'aurez pas à vous soucier du refroidissement ni de la consommation électrique. Toutefois, ces données peuvent s'avérer utiles pour comprendre l'impact des accélérateurs sur l'environnement et la demande globale en électricité.

---
# Sélection des accélérateurs

Le choix des accélérateurs dépend de votre charge de travail. Si celle-ci est limitée par la puissance de calcul, privilégiez les puces offrant un nombre d'opérations en virgule flottante par seconde (FLOPS) plus élevé. En revanche, si elle est limitée par la mémoire, investir dans des puces avec une bande passante et une capacité de mémoire supérieures vous facilitera grandement la tâche.

Au moment de choisir les puces à acheter, trois questions principales se posent :

- Votre matériel est-il capable de gérer vos charges de travail ?
    
- Combien de temps cela prend-il ?
    
- Combien ça coûte?
    

Les FLOP/s, la taille de la mémoire et la bande passante mémoire sont les trois chiffres clés qui vous permettent de répondre aux deux premières questions. La dernière question est simple. La tarification des fournisseurs de cloud est généralement basée sur l'utilisation et assez similaire d'un fournisseur à l'autre. Si vous achetez votre propre matériel, le coût peut être calculé en fonction du prix initial et de la consommation électrique.consommation.

---
# Optimisation de l'inférence

L'optimisation de l'inférence peut être effectuée au niveau du modèle, du matériel ou du service. Pour illustrer leurs différences, prenons l'exemple du tir à l'arc. L'optimisation au niveau du modèle revient à concevoir de meilleures flèches. L'optimisation au niveau du matériel s'apparente à l'entraînement d'un archer plus performant. L'optimisation au niveau du service consiste à perfectionner l'ensemble du processus de tir, y compris l'arc et les conditions de visée.

Idéalement, l'optimisation d'un modèle en termes de vitesse et de coût ne devrait pas altérer sa qualité. Cependant, de nombreuses techniques peuvent entraîner une dégradation du modèle. [La figure 9-8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_8_1730130962952759) illustre les performances des mêmes modèles Llama sur différents jeux de données, fournis par différents prestataires de services d'inférence.

![Graphique de différents types de nombres. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0908.png)

###### Figure 9-8. Un fournisseur de services d'inférence peut utiliser des techniques d'optimisation susceptibles de modifier le comportement d'un modèle, ce qui entraîne de légères variations de qualité entre les modèles proposés par différents fournisseurs. L'expérience a été menée par [Cerebras (2024)](https://oreil.ly/5hFSF) .

La conception matérielle n'étant pas abordée dans cet ouvrage, je traiterai des techniques relatives aux modèles et aux services. Bien que ces techniques soient présentées séparément, il est important de noter qu'en production, l'optimisation fait généralement appel à des techniques à plusieurs niveaux.

## Optimisation du modèle

L'optimisation au niveau du modèle vise à améliorer son efficacité, souvent en le modifiant lui-même, ce qui peut altérer son comportement. À l'heure actuelle, de nombreux modèles de base suivent l'architecture Transformer et intègrent un composant de modèle de langage autorégressif. Ces modèles présentent trois caractéristiques qui rendent l'inférence gourmande en ressources : leur taille, le décodage autorégressif et le mécanisme d'attention. Examinons des approches permettant de relever ces défis.

### Compression du modèle

La compression de modèles regroupe des techniques permettant de réduire la taille d'un modèle. Un modèle plus petit peut également être plus rapide. Cet ouvrage a déjà abordé deux techniques de compression de modèles : la quantification et la distillation. La quantification, qui consiste à réduire la précision d'un modèle afin de diminuer son empreinte mémoire et d'augmenter son débit, est traitée au [chapitre 7.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) La distillation de modèles, qui consiste à entraîner un petit modèle pour reproduire le comportement du modèle original, est traitée au [chapitre 8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) .

La distillation de modèles suggère qu'il est possible de reproduire le comportement d'un modèle complexe avec un nombre réduit de paramètres. Se pourrait-il qu'au sein de ce modèle complexe, il existe un sous-ensemble de paramètres capable de décrire l'intégralité de son comportement ? C'est le principe fondamental de l'élagage.

Dans le contexte des réseaux de neurones, l'élagage a deux significations. La première consiste à supprimer des nœuds entiers du réseau, ce qui modifie son architecture et réduit le nombre de ses paramètres. La seconde consiste à identifier les paramètres les moins utiles aux prédictions et à les mettre à zéro.Dans ce cas, l'élagage ne réduit pas le nombre total de paramètres, mais seulement le nombre de paramètres non nuls. Le modèle devient ainsi plus clairsemé, ce qui réduit son espace de stockage et accélère les calculs.

Les modèles élagués peuvent être utilisés tels quels ou affinés afin d'ajuster les paramètres restants et de compenser toute dégradation des performances due à l'élagage. L'élagage peut contribuer à la découverte d'architectures de modèles prometteuses ( [Liu et al., 2018](https://arxiv.org/abs/1810.05270) ). Ces architectures élaguées, plus petites que les architectures initiales, peuvent également être entraînées à partir de zéro ( [Zhu et al., 2017](https://arxiv.org/abs/1710.01878) ).

La littérature scientifique fait état de nombreux résultats encourageants concernant l'élagage. Par exemple, [Frankle et Carbin (2019)](https://oreil.ly/qwlHE) ont démontré que les techniques d'élagage peuvent réduire de plus de 90 % le nombre de paramètres non nuls de certains réseaux entraînés, diminuant ainsi l'empreinte mémoire et améliorant la vitesse sans compromettre la précision. Cependant, à l'heure actuelle, l'élagage reste moins fréquent en pratique. Plus complexe à mettre en œuvre, il exige une bonne compréhension de l'architecture du modèle initial, et le gain de performance obtenu est souvent bien moindre que celui d'autres approches. De plus, l'élagage engendre des modèles clairsemés, et toutes les architectures matérielles ne sont pas conçues pour tirer parti de cette clairsemance.

_La quantification basée uniquement sur les poids est de loin l'approche la plus répandue, car elle est simple d'utilisation, fonctionne immédiatement avec de nombreux modèles et est extrêmement efficace._ Réduire la précision d'un modèle de 32 bits à 16 bits divise par deux son empreinte mémoire. Cependant, la quantification atteint ses limites : il est impossible de descendre en dessous d'un bit par valeur. La distillation est également courante, car elle permet d'obtenir un modèle plus petit dont le comportement est comparable à celui d'un modèle beaucoup plus volumineux, adapté à vos besoins.

### Surmonter le goulot d'étranglement du décodage autorégressif

Comme expliqué au [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) , les modèles de langage autorégressifs génèrent les jetons un par un. Si la génération d'un jeton prend 100 ms, une réponse de 100 jetons prendra 10 s . Ce processus est non seulement lent, mais aussi coûteux. Chez les différents fournisseurs d'API de modèles, un jeton de sortie coûte environ deux à quatre fois plus cher qu'un jeton d'entrée. Lors d'une expérience, Anyscale a constaté qu'un seul jeton de sortie pouvait avoir le même impact sur la latence que 100 jetons d'entrée ( [Kadous](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1683) [et al., 2023](https://oreil.ly/QYdG8) ). Améliorer légèrement le processus de génération autorégressif peut considérablement améliorer l'expérience utilisateur.

Face à l'évolution rapide de ce domaine, de nouvelles techniques sont mises au point pour surmonter cet obstacle apparemment insurmontable. Peut-être qu'un jour, certaines architectures seront exemptes de ce goulot d'étranglement. Les techniques présentées ici visent à illustrer une solution possible, mais elles sont encore en développement.

#### Décodage spéculatif

Le décodage spéculatif (ou échantillonnage spéculatif) utilise un modèle plus rapide, mais moins puissant, pour générer une séquence de jetons, qui est ensuite vérifiée par le modèle cible. Le modèle cible est celui que vous souhaitez utiliser. Le modèle plus rapide est appelé modèle préliminaire ou modèle de proposition, car il propose une ébauche du résultat.

Imaginez que les jetons d'entrée soient $x_1 , x_2 , …, x_t$ :

1. Le modèle préliminaire génère une séquence de _K_ jetons : $x_{t+ 1} , x_{t+2} , …, x_{t+K}$ .
    
2. Le modèle cible vérifie ces _K_ jetons générés en parallèle.
    
3. Le modèle cible _accepte_ la plus longue sous-séquence de jetons de brouillon, de gauche à droite, que le modèle cible accepte d'utiliser.
    
4. Supposons que le modèle cible accepte _j_ jetons brouillon, _x_ _t_ + 1 , _x_ _t_ + 2 , …, _x_ _t_ + _j_ . Le modèle cible génère ensuite un jeton supplémentaire, _x_ _t_ + _j_ + 1 .
    

Le processus revient à l'étape 1, le modèle préliminaire générant _K_ jetons conditionnés par _x_ 1 , _x_ 2 , …, _x_ _t_ , _x_ _t_ + 1 , _x_ _t_ + 2 , …, _x_ _t_ + _j_ . Le processus est visualisé dans [la figure 9-9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_9_1730130962952786) .

Si aucun jeton provisoire n'est accepté, cette boucle ne produit qu'un seul jeton généré par le modèle cible. Si tous les jetons provisoires sont acceptés, cette boucle produit _K_ + 1 jetons, dont _K_ générés par le modèle provisoire et un par le modèle cible.

![Diagramme de mots Description généré automatiquement avec un niveau de confiance moyen](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0909.png)

###### Figure 9-9. Un modèle préliminaire génère une séquence de K jetons, et le modèle principal retient la plus longue sous-séquence compatible. Cette image est extraite de « Blockwise Parallel Decoding for Deep Autoregressive Models » ( [Stern et al., 2018](https://arxiv.org/abs/1811.03115) ).

Si toutes les séquences préliminaires sont rejetées, le modèle cible doit générer la réponse complète en plus de la vérifier, ce qui peut entraîner une latence accrue. Cependant, cela peut être évité grâce aux trois points suivants :

1. Le temps nécessaire au modèle cible pour vérifier une séquence de jetons est inférieur au temps nécessaire pour la générer, car la vérification est parallélisable, tandis que la génération est séquentielle. Le décodage spéculatif transforme ainsi le profil de calcul du décodage en celui du préremplissage.
    
2. Dans une séquence de jetons de sortie, certains jetons sont plus faciles à prédire que d'autres. Il est possible de trouver un modèle préliminaire moins performant capable de prédire correctement ces jetons plus faciles à prédire, ce qui conduit à un taux d'acceptation élevé des jetons préliminaires.
    
3. Le décodage est limité par la bande passante mémoire, ce qui signifie que pendant le processus de codage, des opérations en virgule flottante (FLOPs) sont généralement inactives et peuvent être utilisées gratuitement pour la vérification. [20](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1684)
    

Le taux d'acceptation dépend du domaine. Pour les textes structurés, comme le code, il est généralement plus élevé. Plus la valeur de _K_ est grande , moins il y a d'appels de vérification pour le modèle cible, mais le taux d'acceptation des jetons préliminaires est faible. Le modèle préliminaire peut avoir n'importe quelle architecture, mais idéalement, il devrait partager le même vocabulaire et le même tokenizer que le modèle cible. Vous pouvez entraîner un modèle préliminaire personnalisé ou utiliser un modèle existant moins performant.

Par exemple, pour accélérer le décodage du Chinchilla-70B, DeepMind a entraîné un modèle préliminaire à 4 milliards de paramètres de même architecture ( [Chen et al., 2023](https://arxiv.org/abs/2302.01318) ). Ce modèle préliminaire génère un jeton huit fois plus rapidement que le modèle cible (1,8 ms/jeton contre 14,1 ms/jeton). Cela réduit la latence de réponse globale de plus de moitié sans compromettre la qualité de la réponse. Un gain de vitesse similaire a été obtenu pour le T5-XXL ( [Laviathan et al., 2022](https://arxiv.org/abs/2211.17192) ).

Cette approche a gagné en popularité car elle est relativement facile à mettre en œuvre et ne dégrade pas la qualité du modèle. Par exemple, elle peut être implémentée en [50 lignes de code avec PyTorch](https://oreil.ly/IaPOB) . Elle a été intégrée à des frameworks d'inférence populaires tels que [vLLM](https://oreil.ly/uzg1s) , [TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM) et [llama.cpp](https://github.com/ggerganov/llama.cpp/pull/2926) .

#### Inférence avec référence

Souvent, une réponse doit faire référence à des éléments du texte d'entrée. Par exemple, si vous posez une question à votre modèle concernant un document joint, il se peut qu'il répète un extrait de texte mot pour mot. Autre exemple : si vous demandez au modèle de corriger des bogues dans un morceau de code, il pourrait réutiliser la majeure partie du code original avec quelques modifications mineures. Plutôt que de laisser le modèle générer ces éléments répétés, pourquoi ne pas les copier directement depuis le texte d'entrée pour accélérer la génération ? C'est le principe fondamental de l'inférence par référence.

L'inférence par référence est similaire au décodage spéculatif, mais au lieu d'utiliser un modèle pour générer des ébauches de jetons, elle les sélectionne directement dans le texte d'entrée. Le principal défi consiste à développer un algorithme capable d'identifier, à chaque étape de décodage, l'intervalle de texte le plus pertinent dans le contexte. L'option la plus simple est de trouver un intervalle de texte correspondant aux jetons actuels.

Contrairement au décodage spéculatif, l'inférence par référence ne nécessite pas de modèle supplémentaire. Cependant, elle n'est utile que dans les scénarios de génération où il existe un chevauchement important entre les contextes et les sorties, comme dans les systèmes de recherche, le codage ou les conversations à plusieurs tours de parole. Dans « Inference with Reference: Lossless Acceleration of Large Language Models » ( [Yang et al., 2023](https://arxiv.org/abs/2304.04487) ), cette technique permet de doubler la vitesse de génération dans de tels cas d'utilisation.

Des exemples de fonctionnement de l'inférence avec référence sont présentés dans [la figure 9-10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_10_1730130962952808) .

![Capture d'écran d'un diagramme. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0910.png)

###### Figure 9-10. Deux exemples d'inférence avec référence. Les portions de texte correctement copiées à partir de l'entrée sont en rouge et en vert. Image tirée de Yang et al. (2023). Licence CC BY 4.0.

#### Décodage parallèle

_Au lieu_ d'accélérer la génération autorégressive grâce aux jetons provisoires, certaines techniques visent à rompre la dépendance séquentielle. Étant donné une séquence existante de jetons x₁ , _x₂_ _,_ _…, xₜ, ces techniques tentent de générer simultanément xₜ₊₁_ , _xₜ₊₂_ , _…_ , _xₜ₊ₖ_ . _Cela_ signifie que _le_ modèle génère xₜ₊₂ _avant_ même de _savoir_ _que_ le jeton _précédent_ _est_ _xₜ₊₁_ .

Cela fonctionne car la connaissance de la séquence existante suffit souvent à prédire les prochains mots. Par exemple, étant donné « le chat est assis », sans savoir que le mot suivant est « sur », « sous » ou « derrière », on peut tout de même prédire que le mot qui suit est « le ».

Les jetons parallèles peuvent être générés par le même décodeur, comme dans le décodage Lookahead ( [Fu et al., 2024](https://arxiv.org/abs/2402.02057) ), ou par différentes têtes de décodage, comme dans Medusa ( [Cai et al., 2024](https://arxiv.org/abs/2401.10774) ). Dans Medusa, le modèle original est étendu avec plusieurs têtes de décodage, chacune étant une petite couche de réseau neuronal entraînée à prédire un jeton futur à une position spécifique. Si le modèle original est entraîné à prédire le jeton suivant _x <sub>_ _t_ +1</sub> , la _k<sup>_ _e</sup>_ tête prédira le jeton _x<sub>_ _t_ + _k_ +1</sub> . Ces têtes sont entraînées simultanément avec le modèle original, mais ce dernier est figé. NVIDIA a affirmé que Medusa avait permis d'améliorer la génération de jetons Llama 3.1 jusqu'à 1,9 fois sur ses GPU HGX H200 ( [Eassa et al., 2024](https://oreil.ly/FWYf5) ).

Cependant, comme ces jetons ne sont pas générés séquentiellement, il est nécessaire de les vérifier pour s'assurer de leur cohérence. La vérification et l'intégration constituent un aspect essentiel du décodage parallèle. Le décodage par anticipation utilise la [méthode de Jacobi](https://en.wikipedia.org/wiki/Jacobi_method) [pour](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1694) vérifier les jetons générés, selon le principe suivant :

1. K jetons futurs sont générés en parallèle.
    
2. Ces jetons _K_ sont vérifiés quant à leur cohérence et leur conformité au contexte.
    
3. Si un ou plusieurs jetons échouent à la vérification, au lieu d'agréger tous les _K_ jetons futurs, le modèle régénère ou ajuste uniquement ces jetons défaillants.
    

Le modèle affine continuellement les jetons générés jusqu'à ce qu'ils soient tous validés et intégrés au résultat final. Cette famille d'algorithmes de décodage parallèle est également appelée décodage de Jacobi.

En revanche, Medusa utilise un mécanisme d'attention arborescent pour vérifier et intégrer les jetons. Chaque tête de Medusa génère plusieurs options pour chaque position. Ces options sont ensuite organisées en une structure arborescente afin de sélectionner la combinaison la plus prometteuse. Ce processus est illustré dans [la figure 9-11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_11_1730130962952823) .

![Diagramme d'un modèle. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0911.png)

###### Figure 9-11. Dans Medusa (Cai et al., 2024), chaque tête prédit plusieurs options pour la position d'un jeton. La séquence la plus prometteuse parmi ces options est sélectionnée. Image adaptée de l'article, publié sous licence CC BY 4.0.

Bien que la perspective de pouvoir contourner la dépendance séquentielle soit séduisante, le décodage parallèle n'est pas intuitif et certaines techniques, comme Medusa, peuvent être difficiles à mettre en œuvre.

### Optimisation du mécanisme d'attention

Rappelons ( [chapitre 2)](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) que la génération du jeton suivant nécessite les vecteurs clé-valeur de tous les jetons précédents. Cela signifie que ce qui suit s'applique :

- La génération du jeton _x_ _t_ nécessite les vecteurs de clé et de valeur pour les jetons _x_ 1 , _x_ 2 , …, _x_ _t_ – 1 .
    
- La génération du jeton _x_ _t_ + 1 nécessite les vecteurs de clé et de valeur pour les jetons _x_ 1 , _x_ 2 , …, _x_ _t_ – 1 , _x_ _t_ .
    

Lors de la génération du jeton _x<sub>_ _t_ +1</sub> , au lieu de recalculer les vecteurs clé-valeur des jetons _x<sub>_ 1 </sub> , _x<sub>_ 2</sub> , …, _x_ _<sub>t_ –1 </sub>, vous réutilisez ceux de l'étape précédente. Cela signifie que vous n'aurez à recalculer les vecteurs clé-valeur que pour le jeton le plus récent, _x<sub>_ _t_ </sub>. Le cache qui stocke ces vecteurs pour une réutilisation est appelé cache KV.Les vecteurs de clé et de valeur nouvellement calculés sont ensuite ajoutés au cache KV, qui est visualisé dans [la figure 9-12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_12_1730130962952844) .

![Diagramme d'un graphe. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0912.png)

###### Figure 9-12. Pour éviter de recalculer les vecteurs de clé et de valeur à chaque étape de décodage, utilisez un cache KV pour stocker ces vecteurs afin de les réutiliser.

###### Note

Un cache clé-valeur est utilisé uniquement lors de l'inférence, et non lors de l'entraînement. Pendant l'entraînement, puisque tous les jetons d'une séquence sont connus à l'avance, la génération du jeton suivant peut être calculée en une seule fois, et non séquentiellement comme lors de l'inférence. Par conséquent, un cache clé-valeur est inutile.

La génération d'un jeton nécessitant le calcul des scores d'attention pour tous les jetons précédents, le nombre de calculs d'attention croît exponentiellement avec la longueur de la séquence.<sup> [22](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1700) </sup> La taille du cache KV, quant à elle, croît linéairement avec la longueur de la séquence.

La taille du cache clé-valeur augmente également avec la taille des lots. Une étude de Google a calculé que pour un modèle de plus de 500 milliards d'éléments avec attention multi-têtes, une taille de lot de 512 et une longueur de contexte de 2048, le cache clé-valeur atteint 3 To [(Pope et al., 2022)](https://arxiv.org/abs/2211.05102) . Cela représente trois fois la taille des poids de ce modèle.

La taille du cache KV est limitée par la capacité de stockage matérielle disponible, ce qui crée un goulot d'étranglement pour les applications nécessitant un contexte long. Un cache volumineux allonge également le temps de chargement en mémoire, ce qui peut poser problème pour les applications exigeant une latence minimale.

Les besoins en calcul et en mémoire du mécanisme d'attention sont l'une des raisons pour lesquelles il est si difficile d'avoir un contexte plus long.

De nombreuses techniques ont été développées pour améliorer l'efficacité du mécanisme d'attention. Elles se répartissent généralement en trois catégories : la refonte du mécanisme d'attention, l'optimisation du cache clé-valeur et l'écriture de noyaux pour le calcul de l'attention.

---
# Calcul de la taille du cache KV

La mémoire nécessaire pour le cache KV, sans aucune optimisation, est calculée comme suit :

- 2 × _B_ × _S_ × _L_ × _H_ × _M_
    

- _B_ : taille du lot
    
- _S_ : longueur de la séquence
    
- _L_ : nombre de couches du transformateur
    
- _H_ : dimension du modèle
    
- _M_ : mémoire nécessaire à la représentation numérique du cache (par exemple, FP16 ou FP32).
    

Cette valeur peut devenir considérable à mesure que la longueur du contexte augmente. Par exemple, LLama 2 13B possède 40 couches et une dimension de modèle de 5 120. Avec une taille de lot de 32, une longueur de séquence de 2 048 et 2 octets par valeur, la mémoire nécessaire pour son cache KV, sans aucune optimisation, est de 2 × 32 × 2 048 × 40 × 5 120 × 2 = 54 Go.

---
#### Repenser le mécanisme d'attention

Ces techniques consistent à modifier le fonctionnement du mécanisme d'attention. Bien qu'elles contribuent à optimiser l'inférence, comme elles modifient directement l'architecture du modèle, elles ne peuvent être appliquées que lors de l'entraînement ou du réglage fin.

Par exemple, lors de la génération d'un nouveau jeton, au lieu de prendre en compte tous les jetons précédents, _l'attention locale par fenêtre_ se concentre uniquement sur une fenêtre de taille fixe de jetons proches ( [Beltagy et al., 2020](https://arxiv.org/abs/2004.05150v2) ). Cela réduit la longueur effective de la séquence à une fenêtre de taille fixe, diminuant ainsi la taille du cache clé-valeur et le temps de calcul de l'attention. Si la longueur moyenne d'une séquence est de 10 000 jetons, le fait de se concentrer sur une fenêtre de 1 000 jetons réduit la taille du cache clé-valeur d'un facteur 10.

L'attention locale peut être entrelacée avec l'attention globale, l'attention locale capturant le contexte immédiat ; l'attention globale capturant les informations spécifiques à la tâche dans l'ensemble du document.

_L'attention intercouches_ ( [Brandon et al., 2024](https://arxiv.org/abs/2405.12981?ref=research.character.ai) ) et _l'attention multi-requêtes_ ( [Shazeer, 2019](https://arxiv.org/abs/1911.02150?ref=research.character.ai) ) réduisent toutes deux l'empreinte mémoire du cache clé-valeur en diminuant le nombre de paires clé-valeur. L'attention intercouches partage les vecteurs de clés et de valeurs entre les couches adjacentes. Le fait que trois couches partagent les mêmes vecteurs de clés et de valeurs permet de réduire le cache clé-valeur d'un facteur trois. En revanche, l'attention multi-requêtes partage les vecteurs de clés et de valeurs entre les têtes de requête.

_L'attention par requêtes groupées_ ( [Ainslie et al., 2023](https://arxiv.org/abs/2305.13245) ) est une généralisation de l'attention par requêtes multiples. Au lieu d'utiliser un seul ensemble de paires clé-valeur pour toutes les requêtes, l'attention par requêtes groupées répartit les requêtes en groupes plus petits et ne partage les paires clé-valeur qu'entre les requêtes appartenant au même groupe. Ceci permet un équilibre plus flexible entre le nombre de requêtes et le nombre de paires clé-valeur.

Character.AI, une application de chatbot basée sur l'IA, indique que ses conversations moyennes comportent un historique de [180 messages](https://oreil.ly/nLt6A) (2024). Compte tenu de la longueur typique de ces séquences, le principal goulot d'étranglement pour le débit d'inférence est la taille du cache clé-valeur. Trois mécanismes d'attention – l'attention multi-requêtes, l'entrelacement de l'attention locale et globale, et l'attention intercouches – leur permettent _de réduire la taille du cache clé-valeur de plus de 20 fois_ . Plus important encore, cette réduction significative signifie que la mémoire n'est plus un facteur limitant pour le traitement de gros volumes de données.

#### Optimisation de la taille du cache KV

La gestion du cache clé-valeur est cruciale pour atténuer les goulots d'étranglement de la mémoire lors de l'inférence et permettre une taille de lot plus importante, notamment pour les applications nécessitant un contexte long. De nombreuses techniques sont actuellement développées pour réduire et gérer le cache clé-valeur.

L'un des frameworks d'inférence à la croissance la plus rapide, [vLLM](https://github.com/vllm-project/vllm) , a gagné en popularité grâce à l'introduction de PagedAttention, qui optimise la gestion de la mémoire en divisant le cache KV en blocs non contigus, réduisant ainsi la fragmentation et permettant un partage flexible de la mémoire pour améliorer l'efficacité du service LLM ( [Kwon et al., 2023](https://arxiv.org/abs/2309.06180) ).

D'autres techniques incluent la quantification du cache KV ( [Hooper et al., 2024](https://arxiv.org/abs/2401.18079) ; [Kang et al., 2024](https://arxiv.org/abs/2403.05527) ), la compression adaptative du cache KV ( [Ge et al., 2023](https://arxiv.org/abs/2310.01801) ) et le cache KV sélectif ( [Liu et al., 2024](https://oreil.ly/ixtBl) ).

#### Écriture de noyaux pour le calcul de l'attention

Au lieu de modifier la conception du mécanisme ou d'optimiser le stockage, cette approche examine le calcul des scores d'attention et cherche à le rendre plus efficace. Elle est particulièrement performante lorsqu'elle prend en compte le matériel exécutant le calcul. Le code optimisé pour une puce spécifique est appelé noyau. L'écriture de noyaux sera abordée plus en détail dans la section suivante.

L'un des noyaux les plus connus optimisés pour le calcul de l'attention est [FlashAttention](https://github.com/Dao-AILab/flash-attention) (Dao et al., 2022). Ce noyau fusionne de nombreuses opérations couramment utilisées dans un modèle basé sur les transformateurs afin d'accélérer leur exécution, comme illustré dans[Figure 9-13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_13_1730130962952862) .

![Graphique d'un graphique avec description textuelle généré automatiquement avec un niveau de confiance moyen](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0913.png)

###### Figure 9-13. FlashAttention est un noyau qui fusionne plusieurs opérateurs courants. Adapté d'une image originale sous licence BSD 3-Clause.

### Noyaux et compilateurs

Les noyaux sont des portions de code spécialisées, optimisées pour des accélérateurs matériels spécifiques, tels que les GPU ou les TPU. Ils sont généralement conçus pour exécuter des routines gourmandes en calculs qui doivent être exécutées de manière répétée, souvent en parallèle, afin de maximiser les performances de ces accélérateurs.

Les opérations courantes d'IA, telles que la multiplication matricielle, le calcul de l'attention et la convolution, disposent toutes de noyaux spécialisés afin d'optimiser leur calcul sur différents matériels. [23](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1716)

La programmation de noyaux nécessite une compréhension approfondie de l'architecture matérielle sous-jacente. Cela inclut la connaissance de la structure de la hiérarchie mémoire (caches, mémoire globale, mémoire partagée et registres) et des modalités d'accès et de transfert des données entre ces différents niveaux.

De plus, les noyaux sont généralement écrits dans des langages de programmation de bas niveau comme CUDA (pour les GPU NVIDIA), Triton (un langage développé par OpenAI pour écrire des noyaux personnalisés) et ROCm (pour les GPU AMD). Ces langages permettent un contrôle précis de la gestion des threads et de l'accès à la mémoire, mais sont aussi plus difficiles à apprendre que les langages que la plupart des ingénieurs en IA connaissent bien, comme Python.

En raison de cette barrière à l'entrée, la programmation de noyaux était autrefois un art obscur pratiqué par quelques spécialistes. Les fabricants de puces comme NVIDIA et AMD emploient des ingénieurs en optimisation pour écrire des noyaux afin de rendre leur matériel efficace pour les charges de travail d'IA, tandis que les frameworks d'IA comme PyTorch et TensorFlow emploient des ingénieurs en noyaux pour optimiser leurs frameworks sur différents accélérateurs.

Cependant, face à la demande croissante d'optimisation de l'inférence et à l'omniprésence des accélérateurs, de plus en plus d'ingénieurs en IA s'intéressent à la programmation de kernels. De nombreux tutoriels en ligne de qualité traitent de ce sujet. Je présenterai ici quatre techniques courantes permettant d'accélérer les calculs :

**Vectorisation**

Dans une boucle ou une boucle imbriquée, au lieu de traiter un élément de données à la fois, exécutez simultanément plusieurs éléments de données contigus en mémoire. Cela réduit la latence en minimisant les opérations d'entrée/sortie de données.

**Parallélisation**

Divisez un tableau d'entrée (ou un tableau n-dimensionnel) en morceaux indépendants qui peuvent être traités simultanément sur différents cœurs ou threads, accélérant ainsi le calcul.

**pavage en boucle**

Optimisez l'ordre d'accès aux données dans une boucle en fonction de l'architecture mémoire et du cache du matériel. Cette optimisation dépend du matériel. Un modèle de pavage efficace sur le CPU peut ne pas être performant sur les GPU.

**Fusion d'opérateurs**

Combinez plusieurs opérateurs en une seule passe pour éviter les accès mémoire redondants. Par exemple, si deux boucles opèrent sur le même tableau, elles peuvent être fusionnées en une seule, réduisant ainsi le nombre d'accès aux données (lecture et écriture).

Bien que la vectorisation, la parallélisation et le pavage de boucles puissent être largement appliqués à différents modèles, la fusion d'opérateurs exige une compréhension plus approfondie des opérateurs et de l'architecture spécifiques à chaque modèle. Par conséquent, la fusion d'opérateurs requiert une attention accrue de la part des ingénieurs en optimisation.

Les noyaux sont optimisés pour une architecture matérielle. Par conséquent, à chaque nouvelle architecture matérielle, de nouveaux noyaux doivent être développés. Par exemple, [FlashAttention](https://github.com/Dao-AILab/flash-attention) (Dao et al., 2022) a été initialement conçu pour les GPU NVIDIA A100. Plus tard, FlashAttention-3 a été introduit pour les GPU H100 ( [Shah et al., 2024](https://arxiv.org/abs/2407.08608) ).

Un script de modèle spécifie une série d'opérations nécessaires à l'exécution de ce modèle. Pour exécuter ce code sur un matériel, tel qu'un GPU, il doit être converti dans un langage compatible avec ce matériel. Ce processus est appelé _conversion_ .Un compilateur est un outil qui _transforme_ le code pour l'exécuter sur un matériel spécifique. Les compilateurs font le lien entre les modèles d'apprentissage automatique et le matériel sur lequel ils s'exécutent. Lors de la transformation, ces opérations sont converties, dans la mesure du possible, en noyaux spécialisés pour une exécution plus rapide sur le matériel cible.

# Étude de cas d'optimisation de l'inférence avec PyTorch

[La figure 9-14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_14_1730130962952879) montre l'amélioration du débit que l'équipe PyTorch a pu apporter à Llama-7B grâce aux étapes d'optimisation suivantes ( [PyTorch, 2023](https://oreil.ly/_5Nqa) ) :

1. Appelez torch.compile pour compiler le modèle en noyaux plus efficaces.
    
2. Quantifiez les poids du modèle en INT8.
    
3. Quantifiez davantage les poids du modèle à INT4.
    
4. Ajouter un décodage spéculatif.
    

![Un graphique avec des chiffres et une description à barres générée automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0914.png)

###### Figure 9-14. Amélioration du débit grâce à différentes techniques d'optimisation dans PyTorch. Image tirée de PyTorch (2023).

L'expérience a été menée sur un GPU A100 doté de 80 Go de mémoire. L'impact de ces étapes d'optimisation sur la qualité des résultats du modèle reste incertain.

Les compilateurs peuvent être des outils autonomes, tels qu'Apache [TVM](https://github.com/apache/tvm) et [MLIR](https://mlir.llvm.org/) (Multi-Level Intermediate Representation), ou intégrés à des frameworks d'apprentissage automatique et d'inférence, comme [XLA](https://en.wikipedia.org/wiki/Accelerated_Linear_Algebra)[`torch.compile`](https://oreil.ly/6bjVM) (Accelerated Linear Algebra, une fonctionnalité de PyTorch , initialement développé par TensorFlow et disponible en version open source sous le nom d' [OpenXLA](https://github.com/openxla/xla) ), ou encore le compilateur intégré à [TensorRT](https://github.com/NVIDIA/TensorRT) , optimisé pour les GPU NVIDIA. Les entreprises spécialisées en IA peuvent disposer de leurs propres compilateurs, avec des noyaux propriétaires conçus pour accélérer leurs propres charges de travail.[](https://en.wikipedia.org/wiki/Accelerated_Linear_Algebra)[](https://github.com/openxla/xla)[](https://github.com/NVIDIA/TensorRT). [24](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1729)

## Optimisation du service d'inférence

La plupart des techniques d'optimisation au niveau du service se concentrent sur la gestion des ressources. Face à des ressources fixes (calcul et mémoire) et des charges de travail dynamiques (requêtes d'inférence des utilisateurs pouvant impliquer différents modèles), l'objectif est d'allouer efficacement les ressources à ces charges de travail afin d'optimiser la latence et le coût. Contrairement à de nombreuses techniques au niveau du modèle, les techniques au niveau du service ne modifient pas les modèles et ne doivent pas altérer la qualité des résultats.

### Traitement par lots

L'un des moyens les plus simples de réduire vos coûts est le traitement par lots. En production, votre service d'inférence peut recevoir plusieurs requêtes simultanément. Au lieu de traiter chaque requête séparément, le regroupement des requêtes arrivant à peu près en même temps peut réduire considérablement le débit du service. Si traiter chaque requête individuellement revient à comparer chacun au volant de sa propre voiture, le traitement par lots est comparable à un bus. Un bus peut transporter plus de personnes, mais cela peut aussi allonger le trajet de chacun. Cependant, si le traitement par lots est effectué intelligemment, l'impact sur la latence peut être minime.

Les trois principales techniques de traitement par lots sont : le traitement par lots statique, le traitement par lots dynamique et le traitement par lots continu.

La technique de traitement par lots la plus simple est _le traitement par lots statique_ . Le service regroupe un nombre fixe de requêtes dans un lot. C'est comme un bus qui attend que tous les sièges soient occupés avant de partir. L'inconvénient du traitement par lots statique est que toutes les requêtes doivent attendre que le lot soit complet pour être exécutées. Ainsi, la première requête d'un lot est retardée jusqu'à l'arrivée de la dernière requête du lot, quelle que soit la date d'arrivée de cette dernière.

_Le traitement par lots dynamique_ , quant à lui, définit une durée maximale pour chaque lot. Si la taille du lot est de quatre et la durée de 100 ms, le serveur traite le lot soit lorsqu'il a reçu quatre requêtes, soit lorsque 100 ms se sont écoulées, selon la première éventualité. C'est comparable à un bus qui part à heure fixe ou lorsqu'il est plein. Cette approche permet de maîtriser la latence, évitant ainsi que les requêtes précédentes ne soient retardées par les suivantes. L'inconvénient est que les lots peuvent ne pas toujours être complets lors de leur traitement, ce qui peut entraîner un gaspillage de ressources de calcul. Le traitement par lots statique et le traitement par lots dynamique sont illustrés dans [la figure 9-15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_15_1730130962952896) .

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0915.png)

###### Figure 9-15. Le traitement par lots dynamique permet de maintenir une latence gérable, mais peut être moins efficace en termes de calcul.

Dans les implémentations de traitement par lots simples, toutes les requêtes d'un même lot doivent être terminées avant que leurs réponses ne soient renvoyées. Pour les LLM, certaines requêtes peuvent être beaucoup plus longues que d'autres. Si une requête d'un lot ne génère que 10 jetons de réponse et qu'une autre en génère 1 000, la réponse courte doit attendre la fin du traitement de la réponse longue avant d'être renvoyée à l'utilisateur. Cela engendre une latence inutile pour les requêtes courtes.

_Le traitement par lots continu_ permet de renvoyer les réponses d'un lot aux utilisateurs dès qu'elles sont terminées. Il fonctionne en regroupant sélectivement les opérations qui n'empêchent pas la génération d'une réponse d'en retarder une autre, comme présenté dans l'article Orca ( [Yu et al., 2022](https://oreil.ly/SJ7Mb) ). Une fois qu'une requête d'un lot est terminée et que sa réponse est renvoyée, le service peut ajouter une autre requête au lot, rendant ainsi le traitement par lots continu. C'est comme un bus qui, après avoir déposé un passager, peut immédiatement en prendre un autre pour maximiser son taux d'occupation. Le traitement par lots continu, également appelé [_traitement par lots en temps réel_](https://oreil.ly/DlIPs) , est illustré dans [la figure 9-16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_16_1730130962952915) .

![Capture d'écran d'un diagramme. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0916.png)

###### Figure 9-16. Avec le traitement par lots continu, les réponses complètes peuvent être renvoyées immédiatement aux utilisateurs et les nouvelles demandes peuvent être traitées à leur place.

### Découplage du préremplissage et du décodage

L'inférence LLM se compose de deux étapes : le préremplissage et le décodage. Le préremplissage étant limité par la puissance de calcul et le décodage par la bande passante mémoire, l'utilisation de la même machine pour les deux peut entraîner une concurrence inefficace pour les ressources et ralentir considérablement le TTFT et le TPOT. Imaginons un GPU gérant déjà le préremplissage et le décodage à une capacité proche de son maximum. Il pourrait gérer une autre tâche peu gourmande en ressources, comme le décodage. Cependant, l'ajout d'une nouvelle requête à ce GPU implique l'introduction d'une tâche de préremplissage en plus de la tâche de décodage. Cette unique tâche de préremplissage peut accaparer les ressources de calcul des tâches de décodage en cours, ralentissant ainsi le TPOT pour ces requêtes.

Une technique d'optimisation courante pour les serveurs d'inférence consiste à dissocier le préremplissage et le décodage. Les travaux « DistServe » ( [Zhong et al., 2024](https://arxiv.org/html/2401.09670v1) ) et « Inference Without Interference » ( [Hu et al., 2024](https://arxiv.org/abs/2401.11181) ) démontrent que, pour divers modèles linéaires à longue portée (LLM) et applications populaires, l'affectation des opérations de préremplissage et de décodage à des instances distinctes (par exemple, des GPU différents) peut améliorer significativement le volume de requêtes traitées tout en respectant les exigences de latence. Bien que la dissociation nécessite le transfert d'états intermédiaires des instances de préremplissage vers les instances de décodage, l'article montre que la surcharge de communication reste négligeable dans les clusters GPU modernes dotés de connexions à haut débit telles que [NVLink](https://en.wikipedia.org/wiki/NVLink) au sein d'un même nœud.

Le rapport entre les instances de préremplissage et les instances de décodage dépend de nombreux facteurs, tels que les caractéristiques de la charge de travail (par exemple, des séquences d'entrée plus longues nécessitent davantage de calculs de préremplissage) et les exigences de latence (par exemple, si l'on privilégie un TTFT ou un TPOT plus faible). Par exemple, si les séquences d'entrée sont généralement longues et que l'on souhaite privilégier le TTFT, ce rapport peut se situer entre 2:1 et 4:1. Si les séquences d'entrée sont courtes et que l'on souhaite privilégier le TPOT, ce rapport peut être compris entre 1:2 et 1:1 [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1741)

###  Prompt caching

Dans une application, de nombreuses invites contiennent des segments de texte qui se chevauchent. Un cache d'invites stocke ces segments pour une réutilisation ultérieure, ce qui permet de ne les traiter qu'une seule fois. L'invite système est un segment de texte fréquemment utilisé dans différentes invites. Sans cache d'invites, votre modèle doit traiter l'invite système à chaque requête. Avec un cache d'invites, l'invite système n'est traitée qu'une seule fois, lors de la première requête.

La mise en cache des invites est utile pour les requêtes portant sur des documents volumineux. Par exemple, si de nombreuses requêtes utilisateur concernent un même document long (comme un livre ou un code source), ce document peut être mis en cache pour être réutilisé dans d'autres requêtes. C'est également utile pour les longues conversations : le traitement des messages précédents peut être mis en cache et réutilisé pour prédire les messages suivants.

[La figure 9-17](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_17_1730130962952933) illustre le cache d'invites . On l'appelle également cache de contexte ou cache de préfixes.

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0917.png)

###### Figure 9-17. Avec un cache d'invite, les segments qui se chevauchent dans différentes invites peuvent être mis en cache et réutilisés.

Pour les applications affichant de longs messages d'invite système, la mise en cache de ces messages peut réduire considérablement la latence et les coûts. Si votre message d'invite système comporte 1 000 éléments et que votre application génère un million d'appels d'API de modèle par jour, un cache d'invites vous évitera de traiter environ un milliard d'éléments d'entrée répétitifs quotidiennement ! Toutefois, cette solution n'est pas sans coût. À l'instar du cache clé-valeur, la taille du cache d'invites peut être importante et consommer de la mémoire. À moins d'utiliser une API de modèle dotée de cette fonctionnalité, la mise en œuvre d'un cache d'invites peut nécessiter un effort d'ingénierie considérable.

Depuis son introduction en novembre 2023 par [Gim et al.](https://oreil.ly/Pd6Pk) , le cache d'invites a été rapidement intégré aux API des modèles. À l'heure actuelle,Google Gemini offre cette [fonctionnalité](https://oreil.ly/pIHkL) , avec des jetons d'entrée mis en cache bénéficiant d'une réduction de 75 % par rapport aux jetons d'entrée classiques, mais vous devrez payer un supplément pour le stockage du cache (au moment de la rédaction, 1,00 $/un million de jetons par heure).Anthropic propose [une mise en cache rapide](https://oreil.ly/8rtsF) qui promet jusqu'à 90 % d'économies (plus le contexte mis en cache est long, plus les économies sont importantes) et jusqu'à 75 % de réduction de la latence. L'impact de la mise en cache rapide sur le coût et la latence de différents scénarios est présenté.dans [le tableau 9-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_table_3_1730130962971081) . [26](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1747)

Tableau 9-3. Coût et latence réduits grâce à la mise en cache rapide. Informations tirées d'Anthropic (2024).

|Cas d'utilisation|Latence sans mise en cache (temps d'obtention du premier jeton)|Latence avec mise en cache (temps d'obtention du premier jeton)|Réduction des coûts|
|---|---|---|---|
|Discuter avec un livre (invite mise en cache de 100 000 jetons)|11,5 s|2,4 s (–79 %)|–90%|
|Instruction à plusieurs coups (invite de 10 000 jetons)|1,6 s|1,1 s (–31 %)|–86%|
|Conversation à plusieurs tours (conversation à 10 tours avec une longue invite système)|~10 s|~2,5 s (–75%)|–53%|

### Parallélisme

Les accélérateurs sont conçus pour le traitement parallèle, et les stratégies de parallélisation constituent l'épine dorsale du calcul haute performance. De nombreuses nouvelles stratégies de parallélisation sont en cours de développement. Cette section n'en aborde que quelques-unes à titre de référence. Deux familles de stratégies de parallélisation applicables à tous les modèles sont le parallélisme de données et le parallélisme de modèles. Une famille de stratégies spécifiquement appliquées aux modèles linéaires à longue portée (LLM) est le parallélisme de contexte et de séquence. Une technique d'optimisation peut impliquer plusieurs stratégies de parallélisme.

_Le parallélisme par réplication_ est la stratégie la plus simple à mettre en œuvre. Il consiste à créer plusieurs répliques du modèle à servir. [Un](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1749) plus grand nombre de répliques permet de traiter davantage de requêtes simultanément, potentiellement au prix d'une consommation accrue de puces. Tenter d'adapter des modèles de tailles différentes à des puces différentes relève du problème d'empaquetage, qui peut se complexifier avec un nombre croissant de modèles, de répliques et de puces.

Supposons que vous ayez un ensemble de modèles de tailles différentes (par exemple, des paramètres de 8, 13, 34 et 70 bits) et un accès à des GPU de capacités mémoire différentes (par exemple, 24 Go, 40 Go, 48 Go et 80 Go). Par souci de simplicité, supposons que tous les modèles aient la même précision, soit 8 bits :

- Si vous disposez d'un nombre fixe de puces, vous devez déterminer le nombre de répliques à créer pour chaque modèle et les GPU à utiliser pour chaque réplique afin d'optimiser vos performances. Par exemple, faut-il utiliser un GPU de 40 Go pour trois modèles 13B, ou réserver ce GPU à un seul modèle 34B ?
    
- Si vous disposez d'un nombre fixe de répliques de modèles, vous devez choisir les puces à acquérir afin de minimiser les coûts. Cette situation est cependant rare.
    

Souvent, un modèle est si volumineux qu'il ne peut pas être exécuté sur une seule machine. _Le parallélisme de modèles_ consiste à répartir ce même modèle sur plusieurs machines. L'exécution des modèles sur des puces peut devenir un problème encore plus complexe avec le parallélisme de modèles.

Il existe plusieurs façons de décomposer un modèle. L'approche la plus courante pour l'inférence est _le parallélisme tensoriel_ , également appelé _parallélisme intra-opérateur_ . L'inférence implique une séquence d'opérateurs sur des tenseurs multidimensionnels, comme la multiplication matricielle. Dans cette approche, les tenseurs impliqués dans un opérateur sont répartis sur plusieurs dispositifs, ce qui a pour effet de diviser cet opérateur en parties plus petites à exécuter en parallèle, accélérant ainsi le calcul. Par exemple, lors de la multiplication de deux matrices, il est possible de décomposer l'une des matrices par colonnes, comme illustré dans [la figure 9-18](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_18_1730130962952949) .

Le parallélisme tensoriel offre deux avantages. Premièrement, il permet de traiter des modèles volumineux qui ne tiennent pas sur une seule machine. Deuxièmement, il réduit la latence. Toutefois, ce gain en latence peut être atténué par la surcharge de communication supplémentaire.

![Diagramme d'une grille avec des carrés et quelques carrés. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0918.png)

###### Figure 9-18. Parallélisme tensoriel pour la multiplication matricielle.

Une autre méthode pour segmenter un modèle est _le parallélisme par pipeline_ , qui consiste à diviser le calcul du modèle en étapes distinctes et à affecter chaque étape à un dispositif différent. À mesure que les données circulent dans le modèle, chaque étape traite une partie tandis que les autres traitent les parties suivantes, permettant ainsi des calculs simultanés. [La figure 9-19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_19_1730130962952966) illustre le parallélisme par pipeline sur quatre machines.

![Diagramme d'une couche - Description générée automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0919.png)

###### Figure 9-19. Le parallélisme du pipeline permet d'exécuter en parallèle les divisions du modèle.

[La figure 9-19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_figure_19_1730130962952966) montre qu'un lot peut être divisé en micro-lots plus petits. Après le traitement d'un micro-lot sur une machine, son produit est transmis à la partie suivante du modèle sur la machine suivante.

Bien que le parallélisme de pipeline permette de déployer des modèles complexes sur plusieurs machines, il accroît la latence totale de chaque requête en raison des communications supplémentaires entre les différentes étapes du pipeline. Par conséquent, pour les applications exigeant une latence minimale, le parallélisme de pipeline est généralement évité au profit du parallélisme de réplication. Cependant, le parallélisme de pipeline est fréquemment utilisé lors de l'entraînement des données, car il contribue à augmenter le débit.

Deux techniques moins courantes, mais qui méritent d'être brièvement mentionnées pour illustrer la diversité des approches, sont le _parallélisme contextuel_ et _le parallélisme de séquence_ . Toutes deux ont été développées pour optimiser le traitement des longues séquences d'entrée.

En [_parallélisme contextuel_](https://oreil.ly/On2-B) , la séquence d'entrée est répartie sur différents dispositifs pour être traitée séparément. Par exemple, la première moitié de l'entrée est traitée sur la machine 1 et la seconde moitié sur la machine 2.

En _parallélisme séquentiel_ , les opérateurs nécessaires à l'ensemble des données d'entrée sont répartis sur plusieurs machines.Par exemple, si l'entrée nécessite à la fois l'attention et le calcul prédictif, l'attention pourrait être traitée sur la machine 1 tandis que le calcul prédictif serait traité sur la machine 2.2.

# Résumé

L'utilité d'un modèle dépend fortement de son coût d'inférence et de sa latence. Une inférence moins coûteuse rend les décisions basées sur l'IA plus abordables, tandis qu'une inférence plus rapide permet d'intégrer l'IA à un plus grand nombre d'applications. Compte tenu de l'impact potentiel considérable de l'optimisation de l'inférence, ce domaine a attiré de nombreux talents qui proposent sans cesse des approches novatrices.

Avant de chercher à améliorer l'efficacité, il est essentiel de comprendre comment elle se mesure. Ce chapitre a débuté par l'examen des indicateurs d'efficacité courants que sont la latence, le débit et l'utilisation. Dans le cadre de l'inférence basée sur un modèle de langage, la latence se décompose en temps d'obtention du premier jeton (TTFT), influencé par la phase de préremplissage, et en temps de traitement par jeton de sortie (TPOT), influencé par la phase de décodage. Les indicateurs de débit sont directement liés au coût. Il existe un compromis entre latence et débit. On peut potentiellement réduire les coûts en acceptant une latence accrue, mais réduire la latence implique souvent une augmentation des coûts.

L'efficacité d'un modèle dépend du matériel sur lequel il s'exécute. C'est pourquoi ce chapitre propose également un aperçu du matériel dédié à l'IA et des techniques d'optimisation des modèles sur différents accélérateurs.

Le chapitre abordait ensuite différentes techniques d'optimisation de l'inférence. Compte tenu de la disponibilité des API de modèles, la plupart des développeurs d'applications privilégieront ces API et leurs fonctions d'optimisation intégrées plutôt que d'implémenter eux-mêmes ces techniques. Bien que ces dernières ne soient pas pertinentes pour tous les développeurs, il me semble utile de comprendre les techniques possibles pour évaluer l'efficacité des API de modèles.

Ce chapitre s'est également intéressé à l'optimisation au niveau du modèle et au niveau du service d'inférence. L'optimisation au niveau du modèle nécessite souvent de modifier le modèle lui-même, ce qui peut entraîner des changements dans son comportement. L'optimisation au niveau du service d'inférence, quant à elle, conserve généralement le modèle intact et modifie uniquement la manière dont il est mis à disposition.

Les techniques au niveau du modèle incluent des techniques indépendantes du modèle, telles que la quantification et la distillation. Chaque architecture de modèle requiert sa propre optimisation. Par exemple, le mécanisme d'attention constituant un goulot d'étranglement majeur des modèles Transformer, de nombreuses techniques d'optimisation visent à améliorer son efficacité, notamment par la gestion du cache clé-valeur et l'écriture des noyaux d'attention. Le décodage autorégressif représente également un goulot d'étranglement important pour les modèles de langage autorégressifs ; de nombreuses techniques ont donc été développées pour y remédier.

Les techniques d'inférence au niveau du service comprennent diverses stratégies de traitement par lots et de parallélisme. Il existe également des techniques développées spécifiquement pour les modèles de langage autorégressifs, telles que le découplage pré-remplissage/décodage et la mise en cache des prompts.

Le choix des techniques d'optimisation dépend de vos charges de travail. Par exemple, la mise en cache clé-valeur est bien plus importante pour les charges de travail avec des contextes longs que pour celles avec des contextes courts. La mise en cache des invites, quant à elle, est cruciale pour les charges de travail impliquant des segments d'invites longs et chevauchants ou des conversations à plusieurs tours de parole. Ce choix dépend également de vos exigences de performance. Par exemple, si une faible latence est plus importante que le coût, vous pourriez envisager d'augmenter le parallélisme des réplicas. Bien que davantage de réplicas nécessitent des machines supplémentaires, chaque machine traite moins de requêtes, ce qui lui permet d'allouer plus de ressources par requête et, par conséquent, d'améliorer le temps de réponse.

Cependant, dans divers cas d'utilisation, les techniques les plus efficaces sont généralement la quantification (qui fonctionne généralement bien sur tous les modèles), le parallélisme tensoriel (qui réduit la latence et permet de traiter des modèles plus volumineux), le parallélisme de répliques (relativement simple à mettre en œuvre) et l'optimisation du mécanisme d'attention (qui peut accélérer considérablement les modèles de transformateurs).

L'optimisation de l'inférence clôt la liste des techniques d'adaptation de modèles présentées dans cet ouvrage. Le chapitre suivant explorera comment intégrer ces techniques au sein d'un système cohérent.

[1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1597-marker)Comme expliqué au [chapitre 7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) , l'inférence implique la passe avant tandis que l'entraînement implique à la fois les passes avant et arrière.

[2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1598-marker)Un ami, Mark Saroufim, m'a fait découvrir une relation intéressante entre le coût d'entraînement et le coût d'inférence d'un modèle. Imaginez que vous soyez un fournisseur de modèles. Soit _T_ le coût total d'entraînement, _p_ le coût facturé par inférence et _N_ le nombre d'inférences que vous pouvez vendre. Développer un modèle n'est rentable que si les revenus générés par l'inférence sont supérieurs à son coût d'entraînement, c'est-à-dire _T_ ≤ _p_ × _N._ Plus un modèle est utilisé en production, plus les fournisseurs de modèles peuvent réduire le coût d'inférence. Cependant, cela ne s'applique pas aux fournisseurs d'API tiers qui vendent des inférences pour des modèles open source.

[3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1605-marker)De manière anecdotique, je constate que les personnes issues du domaine des systèmes (par exemple, les ingénieurs en optimisation et les ingénieurs GPU) utilisent _l'expression « limité par la mémoire »_ pour désigner _une limitation par la bande passante_ , tandis que les personnes issues du domaine de l'IA (par exemple, les ingénieurs en apprentissage automatique et en IA) utilisent l'expression « limité par la mémoire » pour désigner une limitation par la capacité de mémoire.

[4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1606-marker)L'article de Roofline utilise le terme « limite de mémoire » pour désigner une limite de bande passante mémoire.

[5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1607-marker)Le préremplissage remplit efficacement le cache KV initial pour le modèle de transformateur.

[6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1612-marker)Si vous gérez un service d'inférence, séparer vos API d'inférence en requêtes en ligne et par lots vous permet de prioriser la latence pour les requêtes les plus critiques. Imaginons que votre serveur d'inférence ne puisse traiter qu'un maximum de X requêtes par seconde sans dégradation de la latence, que vous deviez en traiter Y par seconde (Y étant supérieur à X). Dans l'idéal, les utilisateurs ayant des requêtes moins urgentes pourraient les envoyer à l'API par lots, afin que votre service puisse se concentrer sur le traitement prioritaire des requêtes de l'API en ligne.

[7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1619-marker)Comme expliqué dans [la section « Mise en cache des invites »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_prompt_caching_1730130963008914) , il est courant de connaître à l'avance l'invite système d'une application. Seules les requêtes exactes de l'utilisateur sont difficiles à prévoir.

[8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1620-marker)Au début de l'ère des chatbots, certains se plaignaient de leur rapidité de réponse, jugée artificielle. (Voir [« Lufthansa Delays Chatbot's Responses to Make It More 'Human' »](https://oreil.ly/jD5Pj) (Ry Crozier, iTnews, mai 2017)). Cependant, à mesure que le public s'est familiarisé avec les chatbots, ce n'est plus le cas.

[9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1623-marker)[LinkedIn](https://www.linkedin.com/blog/engineering/generative-ai/musings-on-building-a-generative-ai-product?_l=en_US) utilise le Time between tokens (TBT) et [NVIDIA](https://oreil.ly/zHsb8) utilise l'inter-token latency (ITL) .

[10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1624-marker)Une expérience menée par Anyscale montre que 100 jetons d'entrée ont à peu près le même impact sur la latence globale qu'un seul jeton de sortie.

[11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1637-marker)L’utilisation des FLOP/s intéresse les gens depuis longtemps, mais le terme MFU a été introduit dans l’article PaLM ( [Chowdhery et al., 2022](https://arxiv.org/abs/2204.02311) ).

[12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1638-marker)Les fabricants de puces pourraient également recourir à ce que j'appelle _le « piratage du pic FLOP/s »_ . Cela pourrait consister à mener des expériences dans certaines conditions, par exemple en utilisant des matrices creuses de formes spécifiques, afin d'augmenter leur pic FLOP/s. Des pics FLOP/s plus élevés rendent leurs puces plus attractives, mais il peut être plus difficile pour les utilisateurs d'atteindre un MFU élevé.

[13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1649-marker)Dans les années 1960, les ordinateurs ne pouvaient exécuter que des réseaux de neurones à une seule couche, aux capacités très limitées. Dans leur ouvrage de référence de 1969, [_*Perceptrons : An Introduction to Computational Geometry*_](https://en.wikipedia.org/wiki/Perceptrons_\(book\)) (MIT Press), deux pionniers de l'IA, Marvin Minsky et Seymour Papert, affirmaient que les réseaux de neurones à couches cachées resteraient très limités. Ils déclaraient : « On ne sait pratiquement rien des capacités de calcul de ce dernier type de machine. Nous pensons qu'elle ne peut guère faire plus qu'un perceptron d'ordre inférieur _._ » L'insuffisance de puissance de calcul de l'époque ne permettait pas de réfuter leur argument, qui fut par la suite cité par beaucoup comme une des principales raisons du tarissement des financements alloués à l'IA dans les années 1970.

[14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1650-marker)La question d'un [éventuel changement de nom du GPU](https://oreil.ly/mRNCP) a été soulevée , compte tenu de ses nombreuses autres applications (Jon Peddie, « Chasing Pixels », juillet 2018). Jensen Huang, PDG de NVIDIA, a déclaré dans une [interview](https://oreil.ly/iK0tN) ( _Stratechery_ , mars 2022) qu'une fois le GPU lancé et ses fonctionnalités étendues, l'entreprise avait envisagé de le renommer avec une appellation plus générique comme GPGPU (GPU à usage général) ou XGU. Elle a finalement renoncé à ce changement, partant du principe que les acheteurs de GPU seraient suffisamment compétents pour comprendre l'étendue de ses capacités, au-delà de son simple nom.

[15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1651-marker)La multiplication matricielle, affectueusement appelée matmul, représenterait plus de 90 % de toutes les opérations en virgule flottante dans un réseau neuronal, selon [« Data Movement Is All You Need: A Case Study on Optimizing Transformers »](https://arxiv.org/abs/2007.00072) (Ivanov et al., _arXiv_ , v3, novembre 2021) et [« Scalable MatMul-free Language Modeling »](https://arxiv.org/abs/1802.04799) (Zhu et al., _arXiv_ , juin 2024).

[16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1652-marker)Bien qu'une puce puisse être conçue pour exécuter une architecture de modèle donnée, une architecture de modèle peut également être développée pour optimiser les performances d'une puce. Par exemple, le processeur Transformer a été initialement conçu par Google pour [fonctionner rapidement sur des TPU](https://oreil.ly/y45q6) et n'a été optimisé que plus tard pour les GPU.

[17](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1661-marker)Les GPU d'entrée et de milieu de gamme peuvent utiliser de la mémoire [GDDR](https://en.wikipedia.org/wiki/GDDR_SDRAM) (Graphics Double Data Rate).

[18](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1669-marker)L'un des principaux défis liés à la construction de centres de données équipés de dizaines de milliers de GPU est de trouver un emplacement garantissant l'approvisionnement en électricité nécessaire. La construction de centres de données à grande échelle implique de composer avec les contraintes d'approvisionnement, de débit et géopolitiques. Par exemple, les régions isolées peuvent offrir une électricité moins chère, mais risquent d'accroître la latence du réseau, rendant ces centres de données moins intéressants pour les cas d'utilisation exigeant une faible latence, comme l'inférence.

[19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1683-marker)Chaque étape de génération de jetons nécessite le transfert de l'ensemble des paramètres du modèle depuis la mémoire à large bande passante de l'accélérateur vers ses unités de calcul. Cette opération est donc gourmande en bande passante. Comme le modèle ne peut produire qu'un seul jeton à la fois, le processus ne consomme qu'un faible nombre d'opérations en virgule flottante par seconde (FLOP/s), ce qui entraîne une inefficacité de calcul.

[20](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1684-marker)Cela signifie également que si votre MFU est déjà saturée, le décodage spéculatif a moins de sens.

[21](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1694-marker)La méthode de Jacobi est un algorithme itératif permettant de mettre à jour simultanément et indépendamment plusieurs parties d'une solution.

[22](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1700-marker)Le nombre de calculs d'attention pour un modèle autorégressif est _O_ ( _n_ 2 ).

[23](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1716-marker)Les opérations de convolution sont souvent utilisées dans les modèles de génération d'images comme la diffusion stable.

[24](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1729-marker)De nombreuses entreprises considèrent leurs noyaux de calcul comme des secrets commerciaux. Disposer de noyaux leur permettant d'exécuter des modèles plus rapidement et à moindre coût que leurs concurrents constitue un avantage concurrentiel.

[25](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1741-marker)Les conférences mentionnant le ratio de préremplissage à décoder incluent [« Llama Inference at Meta »](https://oreil.ly/eMQ_P) (Meta, 2024).

[26](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1747-marker)Bien que llama.cpp gère également [la mise en cache des invites](https://github.com/ggerganov/llama.cpp/blob/master/examples/main/README.md#prompt-caching) , il semble, à l'heure actuelle, qu'elle ne mette en cache que les invites complètes et qu'elle fonctionne uniquement pour les requêtes effectuées au sein d'une même session de chat. Sa documentation est limitée, mais d'après le code source, je suppose que lors d'une longue conversation, elle met en cache les messages précédents et ne traite que le plus récent.

[27](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#id1749-marker)Lors de l'entraînement, cette même technique est appelée parallélisme des données.