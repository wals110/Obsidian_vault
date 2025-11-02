

## Partie I : Paradigmes Fondamentaux des Systèmes d'IA Agentiques

Cette première partie établit les fondations conceptuelles et historiques nécessaires à la compréhension des agents d'intelligence artificielle modernes. Elle retrace leur lignée depuis l'IA symbolique, déconstruit la boucle agentique contemporaine et analyse en profondeur les cadres fondamentaux qui sous-tendent la recherche et le développement actuels.

### 1.1 De l'IA Symbolique aux Agents Linguistiques : Une Lignée Conceptuelle

Pour appréhender la nature profonde des systèmes agentiques modernes basés sur les grands modèles de langage (LLM), il est impératif de comprendre leur héritage intellectuel. Loin d'être une rupture totale avec le passé, l'émergence des agents LLM représente une réinterprétation et une mise à l'échelle spectaculaire de principes établis de longue date dans le domaine de l'intelligence artificielle classique, notamment l'IA symbolique. Cette perspective historique est cruciale, car elle éclaire les choix architecturaux qui prévalent aujourd'hui et fournit un cadre théorique robuste pour la conception de systèmes futurs.

Au cœur de cette lignée se trouve le concept de **systèmes de production**, un paradigme fondamental de l'IA symbolique. Un système de production est composé d'un ensemble de règles, chacune spécifiant une précondition et une action à exécuter si cette précondition est remplie. Ces systèmes modélisent un processus de raisonnement simple mais puissant, où l'état du monde est modifié par des actions déclenchées par des conditions spécifiques. Une analogie pertinente et éclairante peut être établie entre ces systèmes de production et les LLM contemporains. Un article de recherche fondateur, "Cognitive Architectures for Language Agents" (CoALA), développe cette comparaison en profondeur. L'argument central est que, tout comme une production symbolique indique une manière possible de modifier une chaîne de symboles, un LLM définit une distribution de probabilité sur les modifications ou ajouts possibles à un texte.  

Cette analogie n'est pas purement théorique ; elle a des implications pratiques profondes. Elle suggère que les structures de contrôle et les architectures cognitives (telles que les modules de mémoire, de prise de décision et d'apprentissage) qui ont été développées pendant des décennies pour augmenter la puissance des systèmes de production peuvent être adaptées pour transformer les LLM. Seuls, les LLM sont de puissants compléteurs de texte, mais ils manquent des composants nécessaires pour agir de manière autonome et finalisée dans un environnement. En leur adjoignant ces structures de contrôle inspirées des architectures cognitives, il devient possible de les métamorphoser en véritables agents intelligents. Cette perspective offre une justification théorique solide à l'émergence de frameworks comme LangChain ou CrewAI, qui, fondamentalement, "boulonnent" ces composants cognitifs (mémoire, outils, boucles de décision) sur un noyau LLM, lui conférant ainsi des capacités agentiques.  

### 1.2 La Boucle Agentique Moderne : Perception, Cognition, Action

Pour construire des agents efficaces, il est essentiel de maîtriser leur cycle opérationnel fondamental. Ce cycle, souvent conceptualisé comme une boucle Perception-Cognition-Action, constitue l'épine dorsale de tout système autonome. Le projet open-source **AutoGPT** a joué un rôle de pionnier en offrant une démonstration concrète et largement médiatisée de la manière dont cette boucle peut être entièrement orchestrée par un LLM, illustrant ainsi le potentiel des agents autonomes.

Un agent autonome est défini comme un système capable de percevoir son environnement, de prendre des décisions et d'entreprendre des actions pour atteindre des objectifs spécifiques, le tout sans intervention humaine directe et constante. L'architecture d'AutoGPT, qui utilise des modèles comme GPT-4, incarne ce principe à travers une boucle itérative claire :  

1. **Initialisation de l'Objectif** : Le cycle commence lorsqu'un utilisateur assigne à l'agent un objectif de haut niveau formulé en langage naturel.
    
2. **Cognition (Réflexion et Planification)** : Le LLM (le "cerveau" de l'agent) analyse cet objectif et le décompose en une série de sous-tâches plus petites et réalisables. Il formule un plan d'action initial pour aborder la première sous-tâche.  
    
3. **Action** : L'agent exécute l'action planifiée en utilisant une panoplie d'outils mis à sa disposition. Ces outils peuvent inclure la navigation sur internet, la lecture et l'écriture de fichiers sur un disque local, ou même l'exécution de code.  
    
4. **Perception (Feedback)** : L'agent observe le résultat de son action. Ce feedback peut être le contenu d'une page web, le résultat d'un script, ou une erreur. Cette nouvelle information est perçue et stockée dans la mémoire de l'agent, qui est souvent implémentée à l'aide d'une base de données vectorielle (par exemple, Pinecone) pour permettre une recherche sémantique efficace des informations pertinentes.  
    
5. **Itération et Adaptation** : L'agent analyse le feedback reçu. En se basant sur ce nouvel état du monde et sur son objectif global, il apprend de sa performance, met à jour sa compréhension de la situation et raffine son plan. Il peut alors décider de la prochaine action à entreprendre, répétant ainsi la boucle jusqu'à ce que l'objectif final soit atteint.  
    

Cette boucle, bien que conceptuellement simple, met en évidence les composants critiques formalisés dans des cadres plus théoriques : la **Perception** (via les outils qui agissent comme des capteurs), la **Représentation des Connaissances** (la mémoire), la **Prise de Décision** (la planification et la sélection d'actions par le LLM) et l'**Action** (l'exécution via les outils). L'importance historique d'AutoGPT ne réside pas tant dans la sophistication de son implémentation que dans sa démonstration éclatante qu'un LLM pouvait servir de "chef d'orchestre" pour l'ensemble de ce cycle, catalysant ainsi l'intérêt et l'imagination de la communauté pour le potentiel des agents autonomes.  

### 1.3 Le Cadre ReAct : Synergie entre Raisonnement et Action

Alors qu'AutoGPT a popularisé la notion d'agent autonome de manière informelle, le cadre de recherche **ReAct (Reason+Act)** a fourni une formalisation académique rigoureuse du concept, en se concentrant sur l'interaction synergique entre le raisonnement interne et l'action externe. ReAct a été conçu pour pallier deux des faiblesses les plus fondamentales des LLM : leur tendance à l'hallucination (générer des informations factuellement incorrectes) et à la propagation d'erreurs dans les chaînes de raisonnement longues. La solution proposée par ReAct est d'ancrer le raisonnement dans des observations concrètes du monde réel, obtenues par le biais d'actions.

La thèse centrale de ReAct est que les LLM peuvent être incités à générer de manière entrelacée des traces de raisonnement (les "pensées" ou _thoughts_) et des actions spécifiques à une tâche, créant ainsi une boucle de rétroaction vertueuse. Cette synergie se manifeste de deux manières complémentaires :  

1. **Le raisonnement guide l'action (Reason to Act)** : Le modèle ne se contente pas de produire une action de manière abrupte. Il génère d'abord une trace de raisonnement qui explicite sa stratégie. Par exemple, face à une question, il pourrait générer la pensée : "Je dois d'abord chercher la date de naissance de la personne en question, puis chercher les principaux événements de sa vie pour répondre". Cette pensée aide le modèle à induire, suivre et mettre à jour un plan d'action de manière plus robuste.  
    
2. **L'action informe le raisonnement (Act to Reason)** : Une fois l'action exécutée (par exemple, `search("date de naissance de Marie Curie")`), le résultat (l'observation) est réinjecté dans le contexte du modèle. Cette information externe et factuelle permet d'ancrer la prochaine étape de raisonnement, de corriger les erreurs précédentes et de surmonter les hallucinations. Si une recherche ne donne aucun résultat, l'agent peut générer une pensée comme "Ma première recherche a échoué, je vais essayer une requête différente" et ainsi gérer les exceptions de manière dynamique.  
    

Les performances de cette approche sont remarquables. Sur des tâches de question-réponse nécessitant des connaissances factuelles, comme HotpotQA, ReAct surpasse significativement les approches basées uniquement sur le raisonnement interne comme Chain-of-Thought (CoT). En interagissant avec une simple API Wikipedia, ReAct réduit drastiquement les hallucinations et les erreurs de propagation. Sur la tâche de vérification de faits Fever, il diminue le taux de faux positifs de 14% (pour CoT) à seulement 6%. Plus impressionnant encore, sur des tâches de prise de décision interactives comme le jeu textuel ALFWorld ou la navigation web sur WebShop, ReAct, avec seulement un ou deux exemples dans son prompt (one/two-shot), surpasse massivement des méthodes d'apprentissage par imitation ou par renforcement qui nécessitent des milliers d'exemples d'entraînement, avec des améliorations du taux de succès absolu de 34% et 10% respectivement.  

Le paradigme ReAct lui-même continue d'évoluer, la tendance actuelle étant à l'auto-amélioration. Le cadre **A³T (Autonomous Annotation of Agent Trajectories)**, qui se présente comme la rencontre de "ReAct" et "ActRe", illustre cette nouvelle frontière. Le problème identifié est que la création de démonstrations de haute qualité pour ReAct (les exemples dans le prompt) reste une tâche manuelle et coûteuse. A³T propose une solution ingénieuse : un "méta-agent" qui génère de manière autonome des données d'entraînement pour un agent de type ReAct. Un premier agent, "ActRe", est spécialisé dans l'explication du raisonnement derrière une action donnée. Un second agent, de type ReAct, peut alors interroger l'agent ActRe pour obtenir des justifications textuelles pour des actions qu'il explore. En combinant ces justifications avec des actions réussies, l'agent peut synthétiser de nouvelles trajectoires de raisonnement-action de haute qualité et les utiliser pour s'auto-entraîner. Cette approche a permis d'atteindre un taux de succès de 96% dans ALFWorld et d'égaler les performances humaines dans WebShop, surpassant significativement le prompting direct de GPT-4 et les modèles finement ajustés. Cette évolution marque un pas important vers des agents qui non seulement agissent, mais apprennent et s'améliorent de manière autonome.  

### 1.4 Architectures Cognitives pour Agents Linguistiques (CoALA)

Alors que le domaine des agents LLM explosait, un foisonnement de travaux a émergé, chacun utilisant sa propre terminologie pour décrire des concepts similaires : "utilisation d'outils", "ancrage" (grounding), "actions", etc. Cette prolifération a créé une sorte de "Far West" terminologique, rendant difficile la comparaison systématique des différentes approches, la compréhension de leur évolution et la construction de nouveaux agents sur des bases conceptuelles solides. En réponse à ce défi, l'article "Cognitive Architectures for Language Agents" (CoALA) a introduit un cadre conceptuel unificateur. Pour un ingénieur, CoALA n'est pas une implémentation, mais un "plan directeur" (blueprint) ou un ensemble de patrons de conception qui permettent de caractériser, d'analyser et de concevoir n'importe quel agent linguistique de manière structurée et rigoureuse.  

CoALA propose d'organiser l'architecture d'un agent selon trois dimensions clés, inspirées par des décennies de recherche en sciences cognitives et en IA symbolique :  

1. **La Mémoire** : Cette dimension va bien au-delà de la simple fenêtre de contexte du LLM. CoALA opère une distinction cruciale entre différents systèmes de mémoire :
    
    - **Mémoire de Travail (Working Memory)** : Il ne s'agit pas du contexte de l'appel API, mais d'une **structure de données persistante** qui maintient les informations actives et facilement accessibles pour le cycle de décision en cours. Elle contient les entrées perceptuelles (résultats d'outils), les connaissances actives (générées par le raisonnement ou récupérées de la mémoire à long terme) et d'autres informations essentielles comme les objectifs actuels de l'agent. À chaque appel au LLM, le prompt est synthétisé à partir d'un sous-ensemble de cette mémoire de travail.  
        
    - **Mémoire à Long Terme (Long-Term Memory)** : Ce composant stocke les informations de manière durable. CoALA identifie plusieurs types, dont la **Mémoire Épisodique**, qui enregistre les expériences passées de l'agent, comme les trajectoires d'actions réussies ou échouées, les conversations précédentes ou les paires entrée-sortie d'entraînement. Ces épisodes peuvent être récupérés et placés dans la mémoire de travail pour informer les décisions futures.  
        
2. **L'Espace d'Actions** : CoALA sépare les actions en deux catégories distinctes :
    
    - **Actions Externes** : Ce sont les actions qui permettent à l'agent d'interagir avec le monde extérieur. L'utilisation d'un outil, la recherche sur le web, l'envoi d'un email ou l'exécution d'un code sont des exemples d'actions externes.
        
    - **Actions Internes** : Ces actions manipulent l'état interne de l'agent lui-même. Récupérer un souvenir de la mémoire épisodique, mettre à jour un objectif dans la mémoire de travail ou décider de réfléchir davantage avant d'agir sont des actions internes.
        
3. **La Procédure de Prise de Décision** : Il s'agit d'une boucle interactive généralisée qui constitue le "moteur cognitif" de l'agent. Ce cycle est structuré en deux phases principales : la **planification** (où l'agent, en se basant sur le contenu de sa mémoire de travail, décide de la prochaine action à entreprendre) et l'**exécution** (où l'agent réalise l'action choisie, qu'elle soit interne ou externe).  
    

Grâce à ce cadre, il devient possible de disséquer et de comparer systématiquement n'importe quel agent. Par exemple, dans le cadre ReAct, l'interaction avec Wikipedia est une _action externe_. La génération d'une "pensée" fait partie de la phase de _planification_ au sein de la _procédure de prise de décision_, et elle utilise la fenêtre de contexte du LLM comme une forme rudimentaire de _mémoire de travail_. CoALA fournit ainsi un langage commun et une structure conceptuelle pour raisonner sur la conception des agents, transformant un art empirique en une discipline d'ingénierie plus systématique.  

La combinaison de ces paradigmes révèle un plan architectural complet pour les agents modernes. Si l'on considère les agents existants comme AutoGPT, on peut les voir comme des boucles complexes et souvent ad hoc. La recherche académique offre des outils pour structurer cette complexité. Le framework ReAct formalise la logique _dynamique_ de l'agent : la boucle "Raisonner -> Agir -> Observer" qui s'est avérée si efficace pour réduire les hallucinations et améliorer la prise de décision. Parallèlement, le cadre CoALA fournit le plan _statique_ de l'architecture, en s'inspirant de la science cognitive pour définir les composants essentiels avec un vocabulaire précis : mémoire de travail, mémoire à long terme, actions internes et externes.  

La véritable avancée pour un concepteur d'agents réside dans la synthèse de ces deux cadres. ReAct n'est pas une alternative à CoALA ; c'est le _processus_ qui opère sur les _composants_ définis par CoALA. L'étape "Raisonner" de ReAct correspond à la phase de planification de la procédure de décision de CoALA, qui synthétise les informations de la mémoire de travail. L'étape "Agir" correspond à l'exécution d'une action externe. L'observation qui en résulte est une nouvelle entrée perceptive qui vient mettre à jour la mémoire de travail. Cette combinaison offre une approche de conception d'agents à la fois puissante et fondée sur des principes, permettant de dépasser le stade du script ad hoc pour s'engager dans une véritable ingénierie de systèmes cognitifs.

De plus, la progression de ReAct vers des systèmes comme A³T et l'émergence de concepts tels que les "agents bottom-up" qui apprennent des compétences par essais et réflexions, signalent une tendance fondamentale et profonde : le passage d'agents statiques et pré-programmés à des agents dynamiques qui apprennent et s'améliorent de manière autonome. Cela a des implications considérables sur la scalabilité et le coût du développement d'agents performants. Les premiers cadres comme ReAct dépendent de prompts conçus par des humains , ce qui constitue un goulot d'étranglement. Des travaux comme A³T visent précisément à lever ce goulot en permettant à un agent de générer ses propres données d'entraînement de haute qualité. L'objectif ultime, tel qu'envisagé dans certaines recherches, est de créer des "méta-agents" capables de programmer ou d'entraîner d'autres agents. Pour l'ingénieur, cela signifie que le développement d'agents pourrait évoluer de l'implémentation directe vers la conception d'objectifs et de mécanismes d'auto-amélioration, réduisant ainsi considérablement les coûts et accélérant le rythme de l'innovation. C'est la prochaine frontière, bien au-delà du simple prompting.  

## Partie II : L'Art et la Science de l'Ingénierie de Prompts Avancée

Cette partie délaisse l'architecture globale de l'agent pour se concentrer sur le cœur de son moteur cognitif : le prompt. Nous allons disséquer l'évolution des techniques de prompting, en partant de l'apprentissage en contexte (In-Context Learning) pour aboutir à des cadres de raisonnement complexes et structurés qui permettent aux modèles de s'attaquer à des problèmes bien au-delà de leurs capacités initiales.

### 2.1 L'Apprentissage en Contexte (ICL) : La Fondation du Prompting

Toute technique de prompting avancée repose sur les fondations de l'apprentissage en contexte (In-Context Learning, ICL), également connu sous le nom d'apprentissage à quelques exemples (few-shot learning). Comprendre ses mécanismes, ses meilleures pratiques et, surtout, ses biais inhérents est un prérequis indispensable pour la conception de prompts efficaces et robustes.

L'ICL est une capacité remarquable des LLM qui leur permet d'apprendre à effectuer une nouvelle tâche à partir de quelques démonstrations fournies directement dans le prompt, sans nécessiter de mise à jour des poids du modèle. Au lieu d'un réentraînement coûteux, l'ingénieur guide le modèle en lui "montrant" ce qu'il doit faire.  

Pour exploiter efficacement cette capacité, plusieurs bonnes pratiques doivent être respectées. Un prompt ICL efficace doit contenir des instructions claires, un formatage cohérent entre les exemples et une sélection d'exemples diversifiés et de haute qualité qui couvrent bien l'espace du problème. Le choix du nombre d'exemples ("shots") est également un paramètre important ; l'expérimentation est souvent nécessaire, mais des gains significatifs sont généralement observés avec un petit nombre d'exemples (par exemple, 3 à 5), au-delà duquel les performances peuvent plafonner.  

Cependant, l'ICL n'est pas une panacée et présente des biais systématiques que tout praticien doit connaître pour éviter des erreurs de performance subtiles mais critiques :

- **Biais de l'Étiquette Majoritaire (Majority Label Bias)** : Le modèle a tendance à prédire la classe de réponse qui est la plus fréquente parmi les exemples fournis dans le prompt. Si un prompt de classification de sentiment contient quatre exemples positifs et un seul négatif, le modèle sera statistiquement plus enclin à prédire un sentiment positif, indépendamment de la nouvelle entrée à classifier.  
    
- **Biais de Récence (Recency Bias)** : Les LLM accordent souvent plus de poids aux informations qui apparaissent à la fin du contexte. Par conséquent, l'ordre des exemples dans un prompt few-shot n'est pas neutre. L'exemple placé en dernier peut avoir une influence disproportionnée sur la sortie du modèle.  
    

Le choix entre une approche sans exemple (zero-shot) et une approche à quelques exemples (few-shot) dépend de la complexité de la tâche. Pour des tâches simples et généralistes, le zero-shot peut suffire. Cependant, pour des tâches plus spécialisées ou complexes, où l'ambiguïté doit être réduite et le format de sortie est spécifique, le few-shot est nettement préférable car les exemples fournissent un ancrage contextuel indispensable.  

### 2.2 Susciter le Raisonnement : La Révolution de la Chaîne de Pensée (CoT)

La technique de la Chaîne de Pensée (Chain-of-Thought, CoT) a représenté une avancée conceptuelle majeure. Elle a démontré qu'il était possible de prompter un LLM non seulement pour qu'il réponde à une question, mais pour qu'il _raisonne_ explicitement afin d'y parvenir. En externalisant le processus de raisonnement, CoT transforme des problèmes en plusieurs étapes, auparavant insolubles pour les LLM, en tâches réalisables.

L'idée fondamentale de CoT est d'inclure dans les exemples du prompt (en mode few-shot) non seulement la question et la réponse finale, mais aussi les étapes de raisonnement intermédiaires qui mènent à cette réponse. En observant ces démonstrations, le modèle apprend à "penser étape par étape" avant de formuler sa conclusion. Cette approche lui permet de décomposer un problème complexe en une séquence d'étapes plus simples, allouant ainsi une "capacité de calcul" implicite à chaque étape du raisonnement.  

Il est crucial de noter que le raisonnement CoT est une **capacité émergente de l'échelle**. Cette technique est largement inefficace sur les modèles de plus petite taille, qui ont tendance à produire des chaînes de pensée fluides mais logiquement incohérentes. En revanche, elle offre des gains de performance spectaculaires sur les modèles de très grande taille (généralement au-delà de 100 milliards de paramètres). Cela suggère que la capacité de raisonnement sous-jacente est latente dans ces grands modèles et que le prompting CoT agit comme une "clé" pour la déverrouiller.  

Les résultats empiriques sont sans appel. Sur des tâches de raisonnement arithmétique, de bon sens et de manipulation symbolique, CoT surpasse de manière significative le prompting standard. Par exemple, sur le benchmark de problèmes mathématiques GSM8K, CoT a fait passer le score du modèle PaLM 540B de 17.9% à 58.1%, une amélioration remarquable.  

Plusieurs variantes de CoT ont été développées pour en améliorer la praticité :

- **Zero-Shot-CoT** : Cette variante surprenante parvient à susciter le raisonnement sans aucun exemple. Il suffit d'ajouter à la fin du prompt une instruction simple comme "Réfléchissons étape par étape" ("Let's think step by step"). Cette simple phrase incite le modèle à décomposer son processus de pensée.  
    
- **Auto-CoT** : Pour pallier la difficulté de créer manuellement des démonstrations CoT de haute qualité, Auto-CoT automatise ce processus. La méthode consiste à regrouper des questions par similarité sémantique (clustering) puis à utiliser un LLM avec Zero-Shot-CoT pour générer des chaînes de raisonnement pour chaque cluster, créant ainsi automatiquement un ensemble de démonstrations diversifiées.  
    

### 2.3 Au-delà de la Linéarité : Arbre de Pensées (ToT) et Graphe de Pensées (GoT)

Bien que la Chaîne de Pensée (CoT) soit une technique puissante, sa nature intrinsèquement linéaire constitue sa principale limitation. Le raisonnement suit un chemin unique et séquentiel, ce qui le rend inadapté aux problèmes qui nécessitent de l'exploration, de la planification stratégique, de la correction d'erreurs (backtracking) ou la synthèse de plusieurs idées parallèles. L'Arbre de Pensées (Tree of Thoughts, ToT) et le Graphe de Pensées (Graph of Thoughts, GoT) représentent les étapes évolutives suivantes, introduisant des structures de raisonnement non linéaires pour surmonter ces défis.

**Tree of Thoughts (ToT)** généralise CoT en permettant au modèle d'explorer simultanément plusieurs chemins de raisonnement, organisant ces explorations sous la forme d'un arbre. Au lieu de suivre une seule chaîne, le modèle peut générer plusieurs "pensées" alternatives à chaque étape, évaluer leur pertinence et décider quelle branche explorer ensuite. Le processus ToT est plus complexe qu'un simple prompt et s'apparente à un algorithme qui utilise le LLM comme un composant :  

1. **Décomposition de la pensée** : Le problème est divisé en étapes intermédiaires, comme en CoT.
    
2. **Génération de pensées** : À partir d'un état donné (un nœud dans l'arbre), le LLM est prompté pour générer plusieurs pensées candidates pour l'étape suivante, créant ainsi plusieurs branches.
    
3. **Évaluation d'état** : Le LLM est utilisé de manière heuristique pour évaluer la "promesse" de chaque nouvel état (chaque nouvelle pensée). Il peut s'agir d'une note de viabilité ou d'une estimation de la probabilité de succès.
    
4. **Algorithme de recherche** : Un algorithme de recherche classique (par exemple, une recherche en largeur (BFS) ou en profondeur (DFS)) est utilisé pour naviguer dans l'arbre des pensées, permettant au système de regarder en avant (lookahead) et de revenir en arrière (backtracking) si une branche s'avère être une impasse.  
    

Cette capacité d'exploration et d'évaluation délibérée améliore considérablement les performances sur les tâches nécessitant une recherche. L'exemple le plus frappant est celui du "Jeu de 24", un problème mathématique où il faut combiner quatre nombres pour obtenir 24. Avec CoT, GPT-4 ne résout que 4% des tâches, échouant souvent dès les premières étapes. Avec ToT, le même modèle atteint un taux de succès de 74%.  

**Graph of Thoughts (GoT)** pousse la généralisation encore plus loin en modélisant les pensées non pas comme un arbre, mais comme les nœuds d'un graphe arbitraire. Ce passage d'une structure arborescente à une structure de graphe est un changement fondamental. L'avantage principal de GoT est qu'il permet des transformations de pensées qui sont topologiquement impossibles dans un arbre. Les deux transformations les plus importantes sont :  

- **L'Agrégation** : La capacité de fusionner plusieurs chemins de raisonnement distincts en une seule nouvelle pensée synergique. Cela correspond à un nœud dans le graphe qui a plusieurs arêtes entrantes. Par exemple, l'agent peut explorer trois approches différentes pour un sous-problème, puis agréger les résultats partiels pour former une solution globale.  
    
- **Le Raffinement** : La capacité de créer des boucles de rétroaction pour améliorer itérativement une pensée. Un nœud peut pointer vers lui-même ou vers un nœud précédent, permettant au modèle de critiquer et d'affiner sa propre sortie jusqu'à ce qu'elle atteigne un certain standard de qualité.  
    

Cette flexibilité accrue se traduit par des performances et une efficacité supérieures sur certaines tâches. Sur une tâche de tri complexe, GoT a amélioré la qualité de la solution de 62% par rapport à ToT, tout en réduisant les coûts de calcul de plus de 31%.  

La progression de CoT à ToT, puis à GoT, n'est pas simplement une chronologie de découvertes, mais représente une hiérarchie claire de complexité algorithmique et de puissance de raisonnement. Cette hiérarchie impose un arbitrage fondamental en ingénierie. CoT est simple et peu coûteux en calcul : une seule passe de génération auto-régressive. Il est optimal pour les problèmes qui peuvent être décomposés de manière linéaire. Cependant, il échoue sur les problèmes qui nécessitent une exploration, comme le Jeu de 24. ToT résout ce problème en introduisant l'exploration de chemins multiples et l'auto-évaluation, mais au prix d'un nombre beaucoup plus élevé d'appels au LLM, ce qui augmente la latence et les coûts. GoT offre une structure encore plus flexible, permettant la fusion et les boucles, ce qui accroît encore la complexité du code d'orchestration ("scaffolding") mais permet de résoudre des problèmes qui exigent la synthèse de lignes de raisonnement disparates, surpassant ToT dans ces scénarios.  

Pour un ingénieur, le choix de la bonne structure de raisonnement est une décision de conception algorithmique qui dépend de la nature du problème et du budget disponible (temps, coût). Il s'agit d'un arbitrage classique entre le temps de calcul, l'espace mémoire et la complexité, appliqué désormais au domaine du raisonnement des LLM.

|Technique|Concept Fondamental|Structure|Avantage Clé|Limitation Clé|Idéal Pour|Articles Clés|
|---|---|---|---|---|---|---|
|**Chain-of-Thought (CoT)**|Générer des étapes de raisonnement intermédiaires avant la réponse.|Linéaire (séquence)|Simplicité, faible coût de calcul, améliore le raisonnement sur les tâches décomposables.|Ne peut pas explorer, revenir en arrière ou gérer des dépendances complexes. Échoue sur les tâches de planification.|Problèmes de raisonnement arithmétique, de bon sens et symboliques qui suivent une logique séquentielle.|Wei et al., 2022|
|**Tree of Thoughts (ToT)**|Explorer plusieurs chemins de raisonnement en parallèle et les évaluer.|Arborescente|Permet l'exploration, la planification, le lookahead et le backtracking. Surpasse massivement CoT sur les tâches de recherche.|Coût de calcul et latence plus élevés en raison des multiples appels au LLM pour la génération et l'évaluation.|Tâches nécessitant une recherche ou une planification stratégique (par ex., jeux, écriture créative, puzzles).|Yao et al., 2023|
|**Graph of Thoughts (GoT)**|Modéliser les pensées comme un graphe, permettant des transformations complexes.|Graphe (arbitraire)|Permet l'**agrégation** (fusion de chemins) et le **raffinement** (boucles de rétroaction). Plus flexible et puissant que ToT.|Complexité d'implémentation et coût de calcul les plus élevés. L'orchestration du graphe est non triviale.|Problèmes complexes nécessitant la synthèse de plusieurs lignes de raisonnement ou l'amélioration itérative.|Besta et al., 2023|
|**Tableau 1 : Comparaison des Techniques de Prompting de Raisonnement Avancées**|||||||

 

### 2.4 Stratégies de Méta-Niveau : Enchaînement de Prompts et Méta-Prompting

Au-delà des techniques qui structurent le raisonnement au sein d'un seul appel ou d'un algorithme local, il existe des stratégies d'orchestration de plus haut niveau. L'enchaînement de prompts (prompt chaining) structure des flux de travail complexes en plusieurs étapes distinctes, tandis que le méta-prompting (meta-prompting) vise à automatiser la création des prompts eux-mêmes, représentant une application récursive des capacités des LLM.

**L'Enchaînement de Prompts** consiste à lier plusieurs prompts de manière séquentielle, où la sortie d'un prompt sert d'entrée au suivant. Cette approche est une application directe du principe "diviser pour régner" : une tâche complexe est décomposée en un pipeline de sous-tâches plus simples et plus gérables. Par exemple, pour répondre à une question sur un long document, une chaîne pourrait comporter trois prompts : le premier pour extraire les passages pertinents, le deuxième pour résumer ces passages, et le troisième pour synthétiser une réponse finale à partir du résumé. Les types d'enchaînement peuvent être **séquentiels** (flux linéaire A -> B -> C), **ramifiés** (branching, où la sortie de A alimente B et C en parallèle), ou **itératifs** (bouclant sur un prompt pour affiner progressivement une sortie). Les avantages de cette approche sont multiples : elle simplifie les instructions à chaque étape, facilite le débogage ciblé (si une étape échoue, on sait exactement où), permet une validation incrémentale des résultats intermédiaires et peut réduire le nombre de tokens par appel au LLM.  

**Le Méta-Prompting** est une technique plus avancée où un LLM est utilisé pour générer ou optimiser des prompts destinés à être utilisés dans une autre tâche par un LLM (qui peut être le même ou un autre). Cela représente un changement de paradigme : au lieu de se concentrer sur le _contenu_ d'une tâche, le méta-prompting se concentre sur la _structure et la syntaxe_ de la manière dont la tâche est présentée au modèle. La distinction avec le few-shot prompting est fondamentale : le few-shot est piloté par le contenu (on fournit des exemples concrets), tandis que le méta-prompting est orienté vers la structure (on fournit un modèle abstrait ou une syntaxe de résolution de problèmes).  

Plusieurs méthodes de méta-prompting ont été proposées. L'une des plus connues est **Automatic Prompt Engineer (APE)**, où un LLM génère plusieurs prompts candidats à partir de quelques démonstrations, les évalue en fonction de leur performance sur un jeu de données, et affine itérativement les meilleurs candidats. Une autre approche, développée par Stanford et OpenAI, utilise un LLM "chef d'orchestre" pour gérer plusieurs LLM "experts", en leur donnant des instructions et en synthétisant leurs sorties. Les avantages du méta-prompting incluent une meilleure efficacité en termes de tokens (les prompts structurels sont souvent plus courts que de longs exemples) et une meilleure efficacité en mode zero-shot, car l'influence d'exemples spécifiques, potentiellement biaisés, est minimisée.  

L'émergence du méta-prompting et des cadres automatisés comme Auto-CoT ou DSPy signale une tendance claire vers l'automatisation du processus d'ingénierie lui-même. Le travail d'ingénierie de prompts a commencé comme un processus manuel et artisanal de formulation du prompt parfait. Des techniques comme CoT et ToT ont fourni des modèles structurés, mais la conception des exemples et des critères d'évaluation restait souvent humaine. Par la suite, des méthodes comme APE ont utilisé un LLM pour générer des prompts candidats. Le méta-prompting a formalisé cette idée en créant des prompts qui définissent une structure de résolution de problèmes. Enfin, des cadres comme DSPy vont plus loin en créant un modèle de programmation où les prompts sont des modules qui peuvent être automatiquement optimisés (ou "compilés") pour un LLM et une tâche spécifiques.  

Cette évolution indique que le domaine s'éloigne du travail manuel de conception de prompts. Le rôle de l'ingénieur de prompts évolue de celui d'un "rédacteur de prompts" à celui d'un "concepteur de systèmes" qui crée les processus de méta-niveau (comme les programmes APE ou DSPy) qui, à leur tour, génèrent les prompts optimaux. Il s'agit d'une application récursive de l'IA pour résoudre son propre problème d'interface, une étape clé vers des systèmes plus autonomes et auto-optimisants.

## Partie III : Architectures Spécifiques aux Modèles et Nuances de Prompting

Cette partie se plonge dans les spécificités des outils de l'ingénieur : les grands modèles de langage de pointe. Nous analysons leurs architectures divulguées, leurs caractéristiques de performance pratiques et les nuances critiques, souvent non documentées, de la manière de les prompter efficacement.

### 3.1 Analyse Architecturale Comparative des Modèles de Pointe

Les capacités d'un agent sont fondamentalement limitées par son LLM de base. Comprendre les différences architecturales entre les modèles d'OpenAI, Anthropic, Google et Meta est essentiel pour sélectionner le bon outil et adapter les prompts afin d'obtenir des performances optimales.

- **OpenAI (GPT-4, série-o)** : Le rapport technique de GPT-4 est notoirement laconique, confirmant uniquement une architecture multimodale basée sur le Transformer. Cependant, les modèles de "raisonnement" plus récents comme o1 et o3 sont explicitement conçus pour une pensée plus lente de type "Système 2", générant de longues chaînes de pensée avant de donner une réponse. Cela suggère un processus d'inférence ou un objectif de fine-tuning différent, axé sur la délibération.  
    
- **Anthropic (Famille Claude 3)** : La carte de modèle de Claude 3 confirme également une architecture multimodale. Son principal différenciateur est l'utilisation explicite de l'**IA Constitutionnelle (Constitutional AI)** pendant l'entraînement pour aligner le modèle sur des principes de sécurité. Le dernier modèle, Claude 3.7 Sonnet, introduit un mode de "pensée étendue" (extended thinking), entraîné via l'apprentissage par renforcement (RL), où le modèle peut se voir allouer un budget de tokens plus important pour le raisonnement, améliorant ainsi ses performances sur les tâches complexes.  
    
- **Google (Famille Gemini 2.5)** : Le rapport technique de Gemini 2.5 est plus transparent, révélant une architecture de transformeur de type **mélange d'experts épars (sparse mixture-of-experts, MoE)**. Cela leur permet d'augmenter la capacité du modèle tout en gérant les coûts de calcul. Ils sont nativement multimodaux (texte, image, audio, vidéo) et prennent en charge l'utilisation d'outils et un long contexte (plus d'un million de tokens) dès leur conception.  
    
- **Meta (Famille Llama 3)** : Les modèles Llama 3 sont également basés sur l'architecture Transformer et se distinguent par l'utilisation de l'**attention à requêtes groupées (Grouped-Query Attention, GQA)** pour améliorer l'efficacité de l'inférence. Leur nature open-source (sous licence) permet une plus grande personnalisation par la communauté. Ils sont entraînés sur un jeu de données massif de 15 trillions de tokens.  
    

Le paysage des modèles de pointe se divise de plus en plus en deux écosystèmes de développement distincts : le monde fermé, piloté par API, d'OpenAI et d'Anthropic, et le monde plus ouvert et personnalisable de Meta (Llama) et, dans une certaine mesure, de Google (Gemini). C'est sans doute la considération stratégique la plus importante pour un ingénieur en ML. D'un côté, OpenAI et Anthropic fournissent des modèles très performants (comme en témoigne le classement de la Chatbot Arena ) mais publient très peu de détails architecturaux. Ce sont des boîtes noires accessibles via API, dont le principal levier d'innovation est la donnée et l'alignement (par exemple, l'IA Constitutionnelle ). De l'autre côté, Meta publie les poids de ses modèles et davantage de détails architecturaux pour Llama (par exemple, le GQA ), ce qui favorise une immense communauté open-source qui expérimente la quantification, le fine-tuning et des techniques de prompting novatrices. Leur principal levier d'innovation est l'efficacité architecturale et l'habilitation de la communauté. Google se situe entre les deux, révélant certains détails (MoE ) mais sans publier les poids.  

Le choix d'un modèle par un ingénieur est donc une décision qui engage sur une voie. Opter pour OpenAI/Anthropic signifie parier sur leur volant d'inertie en matière de données et d'alignement, mais accepter une dépendance vis-à-vis du fournisseur et une personnalisation limitée. Le prompting devient alors l'outil principal. Choisir Llama signifie assumer une plus grande part de la charge MLOps, mais gagner la capacité de fine-tuner, de modifier et d'inspecter le modèle en profondeur. Ce choix dicte l'ensemble de la pile MLOps, les compétences requises et les types de problèmes qui peuvent être résolus.

|Famille de Modèles|Caractéristique Architecturale Clé|Différenciateur / Philosophie Déclarée|Fenêtre de Contexte (Nominale)|Nuance de Prompting / Meilleure Pratique Connue|
|---|---|---|---|---|
|**OpenAI (GPT-4o/série-o)**|Transformer multimodal, modèles de raisonnement (o-series)|Performance de pointe, raisonnement délibératif de type Système 2.|128K|Les modèles 'o' bénéficient de prompts qui encouragent la délibération. Tous les modèles sont affectés par le problème "Lost in the Middle".|
|**Anthropic (Famille Claude 3.7)**|Transformer multimodal|Sécurité et alignement via l'IA Constitutionnelle, "pensée étendue" contrôlable.|200K|Le mode "pensée étendue" peut être activé pour les tâches complexes. Sensible au biais de confirmation dans le prompt système.|
|**Google (Famille Gemini 2.5)**|Mélange d'Experts Épars (MoE), nativement multimodal|Efficacité à grande échelle, multimodalité native (vidéo, audio), intégration profonde d'outils.|>1M|L'architecture MoE peut offrir un meilleur rapport coût/performance. Support natif de l'utilisation d'outils.|
|**Meta (Famille Llama 3.1)**|Transformer avec Attention à Requêtes Groupées (GQA)|Open-source, efficacité de l'inférence, personnalisation par la communauté.|8K (extensible)|Nécessite un respect strict du format de prompt avec des tokens spéciaux (par ex., `<\|start_header_id\|>`) pour fonctionner correctement.|
|**Tableau 2 : Caractéristiques et Nuances de Prompting des Principaux LLM**|||||

 

### 3.2 Le Défi de la Fenêtre de Contexte : "Perdu au Milieu"

La "course aux armements" marketing pour des fenêtres de contexte toujours plus grandes (100K, 128K, 1M+ de tokens) est trompeuse. L'article de recherche "Lost in the Middle: How Language Models Use Long Contexts" révèle une dégradation critique des performances que tout ingénieur de prompts doit comprendre et contourner.

L'étude démontre que la performance d'un modèle n'est pas uniforme sur l'ensemble de sa fenêtre de contexte. Elle met en évidence une **courbe de performance en forme de U** distincte : les modèles excellent à récupérer et à utiliser les informations situées au tout **début** ou à la toute **fin** du contexte d'entrée. En revanche, la performance se dégrade de manière significative lorsque l'information pertinente se trouve au milieu de longs contextes.  

Cette découverte a des implications profondes pour l'ingénierie de prompts. Pour les prompts en un seul tour, les instructions ou les données les plus cruciales doivent impérativement être placées au début ou à la fin. Pour les systèmes de Génération Augmentée par Récupération (RAG), le simple fait de "bourrer" le contexte avec de nombreux documents est une stratégie sous-optimale. L'ordre des documents récupérés devient primordial : les documents les plus pertinents doivent être placés en haut ou en bas du contexte final envoyé au LLM pour éviter qu'ils ne se retrouvent "perdus au milieu".  

Ce phénomène remet en question l'idée reçue selon laquelle les grandes fenêtres de contexte éliminent le besoin de systèmes RAG sophistiqués. En réalité, il rend les stratégies de récupération et, surtout, de **reclassement (reranking)** encore plus critiques. Le défi de l'ingénierie se déplace du LLM lui-même vers le système de récupération qui le précède. La valeur ne réside plus seulement dans la taille brute de la fenêtre de contexte, mais dans la couche "d'intelligence contextuelle" qui la gère. Cette couche doit être responsable non seulement de la _récupération_ mais aussi de la _structuration_ du contexte. Des techniques comme le reclassement des documents pour placer les plus importants aux extrémités, le résumé des documents moins importants pour réduire leur empreinte en tokens, ou la création d'un contexte structuré (par exemple, un résumé JSON au début) deviennent des pratiques d'ingénierie essentielles. La fenêtre de contexte n'est que la mémoire ; le vrai travail réside dans la gestion de cette mémoire.

### 3.3 Formatage de Prompt Spécifique au Modèle : Un Guide Pratique

Les modèles ne sont pas interchangeables. Ils sont entraînés avec des tokens de contrôle et des structures spécifiques, et l'utilisation d'un format incorrect peut entraîner une dégradation spectaculaire des performances. Cette section fournit un guide pratique, en se concentrant sur le cas bien documenté de Llama 3 pour illustrer l'importance de ce détail technique.

Certaines meilleures pratiques sont universelles : des instructions claires et concises, la fourniture de contexte et l'évitement de l'ambiguïté améliorent les performances de tous les modèles. L'utilisation de formats structurés comme JSON ou Markdown peut également aider à guider la sortie du modèle.  

Cependant, les modèles de Meta, comme Llama 3 et ses successeurs, utilisent un ensemble strict de tokens spéciaux pour délimiter les conversations et les rôles, ce qui est essentiel pour leur bon fonctionnement :  

- `<|begin_of_text|>` et `<|end_of_text|>` encadrent l'ensemble de l'interaction.
    
- `<|start_header_id|>{role}<|end_header_id|>` et `<|eot_id|>` (end of turn) enveloppent chaque message individuel.
    
- Les rôles supportés sont `system` (pour les instructions globales), `user` (pour l'entrée de l'utilisateur) et `assistant` (pour les réponses précédentes du modèle). Llama 3.1 a ajouté le rôle `ipython` pour encapsuler les sorties d'outils.  
    

Le non-respect de ce formatage exact peut amener le modèle à mal interpréter la structure de la conversation et la nature de la tâche. De plus, pour l'utilisation d'outils, Llama 3.1 a introduit un format encore plus spécifique. Lorsque le modèle génère du code à exécuter, il l'enveloppe dans une balise `<|python_tag|>`. Un tour peut se terminer par `<|eom_id|>` (end of message) au lieu de `<|eot_id|>`. Ce token spécial signale que le modèle n'a pas terminé son raisonnement et qu'il attend le résultat de l'exécution de l'outil comme entrée pour le tour suivant. La maîtrise de ces formats structurés est indispensable pour construire des agents fiables basés sur les modèles Llama.  

### 3.4 Performance sur le Terrain : Le Classement de la Chatbot Arena

Bien que les benchmarks académiques standardisés soient utiles pour mesurer des capacités spécifiques, le classement de la **LMSys Chatbot Arena** offre une mesure dynamique et à grande échelle de la préférence humaine. Il capture souvent des nuances de serviabilité, de qualité conversationnelle et de créativité qui sont difficiles à quantifier dans les tests automatisés.

La Chatbot Arena classe les modèles en fonction d'un score Elo, calculé à partir de plus de 3 millions de votes d'utilisateurs anonymes qui comparent à l'aveugle les réponses de deux modèles.  

- **Leaders Actuels** (selon les données de fin 2025) : Le haut du classement montre une course très serrée, dominée par les dernières itérations de la série GPT-4 d'OpenAI (par exemple, `gpt-4.5-preview`, `o3`), la série Gemini de Google (par exemple, `Gemini-2.5-Pro`) et les modèles Claude d'Anthropic (par exemple, `claude-opus-4`). Des modèles open-source très performants comme ceux de DeepSeek (`DeepSeek-R1`) se hissent également dans le peloton de tête, démontrant la compétitivité croissante des alternatives aux modèles propriétaires.  
    
- **Métriques Clés** : La métrique principale est le **score Elo de l'Arena**. Le classement fournit également des intervalles de confiance et le nombre de votes, ce qui permet d'évaluer la robustesse statistique du classement. Des vues spécialisées proposent des classements pour des domaines spécifiques comme le codage, la vision ou la difficulté des prompts ("Arena-Hard").  
    
- **Implication Pratique** : Ce classement constitue une vérification cruciale des performances revendiquées dans le monde réel. Un modèle peut exceller sur un benchmark académique spécifique mais obtenir un score Elo inférieur si les utilisateurs le trouvent moins utile, trop verbeux ou plus évasif en pratique. C'est une ressource indispensable pour sélectionner un modèle destiné à une application en contact avec les utilisateurs, où l'expérience subjective est aussi importante que la précision brute.
    

## Partie IV : La Frontière de la Recherche sur les Systèmes Agentiques

Cette partie explore les avancées les plus récentes de la recherche académique et industrielle, dépassant les techniques établies pour examiner les propriétés fondamentales des LLM et la prochaine génération de capacités cognitives en cours de développement.

### 4.1 L'Énigme des Capacités Émergentes

Le concept selon lequel les LLM développent de nouvelles compétences imprévisibles à mesure qu'ils grandissent est à la fois une source d'enthousiasme et d'inquiétude. Comprendre le débat autour de l'émergence est essentiel pour anticiper les capacités et les risques futurs des modèles de plus en plus puissants.

Une **capacité émergente** est définie comme une aptitude qui n'est pas présente dans les modèles à plus petite échelle mais qui apparaît dans les modèles à grande échelle, souvent de manière abrupte lorsqu'un certain seuil de taille est atteint. Cette apparition soudaine la rend imprévisible par simple extrapolation des performances des modèles plus petits. Le raisonnement en plusieurs étapes (débloqué par CoT) et l'apprentissage en contexte sont des exemples canoniques de ces capacités.  

Le débat scientifique central porte sur la nature de ce phénomène : s'agit-il d'une véritable "transition de phase" dans les capacités du modèle, ou d'un "mirage" causé par le choix des métriques d'évaluation?.  

- **L'argument du "mirage"** : Certains chercheurs soutiennent que l'utilisation de métriques non linéaires et binaires (comme la précision, qui est soit 0, soit 1) crée l'illusion d'un saut de performance brutal. En utilisant des métriques continues qui accordent un crédit partiel (comme la distance d'édition de tokens), la courbe de performance peut sembler plus lisse et plus prévisible.  
    
- **L'argument de la "véritable émergence"** : D'autres études montrent que même avec des métriques continues, des sauts de performance nets persistent pour certaines tâches. De plus, il a été démontré que la perte (loss) de pré-entraînement elle-même est un bon prédicteur du moment où ces capacités émergeront. Cela suggère qu'elles sont liées à la dynamique d'apprentissage interne du modèle, et non simplement à un artefact de la métrique.  
    

L'émergence n'est pas seulement une question de nombre de paramètres. Elle est influencée par un ensemble complexe de facteurs, notamment les **lois d'échelle (scaling laws)**, la **complexité de la tâche**, la **dynamique de la perte de pré-entraînement** et, de manière critique, les **stratégies de prompting** comme CoT, qui peuvent agir comme un déclencheur pour une capacité latente.  

### 4.2 Simuler la Cognition Humaine : Raisonnement de Système 1 et Système 2

Il s'agit d'une frontière de recherche majeure visant à rendre le raisonnement des LLM moins mécanique et plus semblable à celui de l'homme. L'objectif n'est plus seulement de savoir "comment faire raisonner le modèle" (comme avec CoT), mais "comment faire en sorte que le modèle choisisse _comment_ raisonner".

Ce domaine s'inspire directement de la **théorie du double processus** issue des sciences cognitives, qui postule deux modes de pensée humaine :

- **Système 1** : Rapide, automatique, intuitif et heuristique. Il gère les décisions rapides avec un effort minimal.  
    
- **Système 2** : Lent, délibératif, analytique et gourmand en efforts. Il est utilisé pour les raisonnements logiques et la résolution de problèmes complexes.  
    

Dans ce cadre, les LLM de base sont souvent considérés comme fonctionnant de manière analogue au Système 1, fournissant des réponses rapides basées sur la reconnaissance de formes. Les techniques comme CoT, ToT, ou les modes de "pensée étendue" de Claude 3.7 et Gemini 2.5 sont des tentatives pour forcer un comportement de type Système 2.  

La thèse centrale des recherches récentes sur le "Raisonnement sur un Spectre" ("Reasoning on a Spectrum") est qu'un style de raisonnement unique n'est pas toujours optimal. Il est plus efficace d'aligner explicitement les LLM sur les deux styles et de leur apprendre à choisir le plus approprié. La méthodologie employée est la suivante :  

1. **Création de données** : Les chercheurs construisent un jeu de données de questions où chaque question a à la fois une réponse valide de Système 1 (basée sur une heuristique rapide) et une réponse valide de Système 2 (basée sur une délibération étape par étape).
    
2. **Alignement** : Ils utilisent ensuite des techniques d'optimisation par préférence (comme DPO ou SimPO) pour affiner les modèles afin qu'ils préfèrent générer des réponses dans l'un ou l'autre style.  
    

Le résultat clé de ces expériences est la mise en évidence d'un **compromis entre précision et efficacité**. Les modèles alignés sur le Système 2 excellent dans les tâches de raisonnement arithmétique et symbolique, mais sont plus lents et plus coûteux en tokens. Inversement, les modèles alignés sur le Système 1 sont plus efficaces et plus performants sur les tâches de bon sens où les raccourcis heuristiques sont avantageux. Cette découverte remet en question l'hypothèse selon laquelle un raisonnement lent et délibéré est toujours supérieur, et ouvre la voie à des agents plus adaptatifs.  

### 4.3 Le Rôle des Mécanismes d'Attention dans le Raisonnement Agentique

Le mécanisme d'auto-attention de l'architecture Transformer est le composant fondamental qui permet aux LLM de comprendre le contexte. Saisir son fonctionnement et ses limites est crucial pour diagnostiquer les échecs des agents et concevoir des systèmes plus avancés.

L'**auto-attention standard** permet à un modèle, lors du traitement d'un token donné, de pondérer l'importance de tous les autres tokens dans l'entrée. C'est ce qui lui permet de capturer les dépendances à longue distance et les relations contextuelles, et c'est la pierre angulaire de modèles comme GPT et BERT.  

Cependant, dans les contextes agentiques, ce mécanisme peut devenir un goulot d'étranglement. Dans les simulations multi-agents complexes et dynamiques, un agent reçoit des informations de nombreuses sources sur de nombreux tours. Le contexte devient alors très long et bruyant. Le modèle peut avoir du mal à hiérarchiser les informations critiques, ce qui conduit à des actions répétitives ou sous-optimales. Ce problème est exacerbé par l'**asymétrie de l'information**, une situation où différents agents possèdent des connaissances différentes.  

Pour résoudre ce problème, des recherches proposent un **mécanisme d'attention dynamique** au niveau de l'agent, qui se superpose au LLM. Ce mécanisme modélise et pondère explicitement les informations entrantes en fonction de facteurs analogues à la cognition sociale humaine :  

- La source de l'information (par exemple, un collaborateur de confiance a plus de poids qu'un agent inconnu).
    
- La nouveauté ou la complexité de l'information.
    
- Les objectifs actuels de l'agent et ses relations avec les autres.
    

Cette attention dynamique aide les agents à surmonter le "biais de similarité d'action" (Action Similarity Bias) et à mieux percevoir les relations sociales, ce qui conduit à des comportements plus réalistes et efficaces dans les simulations.  

### 4.4 Ouvrir la Boîte Noire : Progrès en Interprétabilité

Pour construire des agents véritablement fiables et sûrs, il est nécessaire de passer de l'observation de leur comportement (corrélation) à la compréhension de leurs mécanismes internes (causalité). L'interprétabilité mécaniste (Mechanistic Interpretability, MI) fournit les outils pour cette rétro-ingénierie des modèles.

L'objectif de la MI est de décomposer les réseaux de neurones en algorithmes compréhensibles par l'homme. Une technique clé dans ce domaine est le **patching d'activation** (ou traçage causal), qui permet de localiser les parties d'un modèle responsables d'un comportement spécifique. Le processus est le suivant :  

1. On exécute le modèle sur un prompt "propre" (clean) qui suscite un comportement d'intérêt (par exemple, "La Tour Eiffel est à Paris").
    
2. On l'exécute sur un prompt "corrompu" (corrupted) qui ne le suscite pas (par exemple, "Le Colisée est à Paris").
    
3. On "patche" (échange) systématiquement les activations du passage propre dans le passage corrompu. Par exemple, on remplace la sortie d'un neurone spécifique à une certaine couche dans le passage corrompu par la sortie du même neurone dans le passage propre.
    
4. Si le fait de patcher une activation spécifique fait que le passage corrompu produit le comportement propre (la sortie devient "Paris"), cela fournit une preuve causale que ce composant (ce neurone, cette tête d'attention) fait partie du circuit responsable de ce comportement.  
    

Le patching peut se faire dans deux directions : le **débruitage** (denoising, clean → corrupt), qui montre la suffisance d'une activation, et le **bruitage** (noising, corrupt → clean), qui montre sa nécessité. Pour les grands modèles où le patching exhaustif est trop coûteux, une approximation basée sur le gradient, le **patching d'attribution**, peut être utilisée pour identifier rapidement les activations intéressantes à étudier plus en détail.  

Pour les agents, ces techniques sont fondamentales. Elles permettent de poser des questions telles que : "Quels neurones dans le LLM de cet agent représentent son objectif?" ou "Quelle tête d'attention est responsable de la récupération du nom du bon outil dans le prompt?". C'est une étape essentielle vers le débogage, le contrôle et l'alignement des systèmes agentiques.

La recherche sur les agents converge de plus en plus avec les sciences cognitives. Le passage de CoT au raisonnement de type Système 1/2, le développement de CoALA basé sur des architectures cognitives, et les mécanismes d'attention dynamique modélisés sur la cognition humaine ne sont pas des tendances isolées. Les premières techniques de prompting étaient purement axées sur l'ingénierie pour améliorer les performances. Les chercheurs ont ensuite remarqué que ces processus ressemblaient à des stratégies cognitives humaines, ce qui a conduit à des travaux comme "Reasoning on a Spectrum" qui utilisent explicitement la théorie de Kahneman. Parallèlement, les concepteurs d'agents, confrontés à des problèmes de mémoire et de contrôle, se sont tournés vers les architectures cognitives classiques pour trouver des solutions, donnant naissance à CoALA. La prochaine génération d'agents d'IA sera probablement explicitement "cognitive". Les avancées les plus significatives viendront des ingénieurs capables de traduire des concepts de la psychologie et des neurosciences en composants architecturaux et en méthodologies d'entraînement concrets.  

Par ailleurs, le phénomène des capacités émergentes crée une "crise de la prévisibilité". Si nous ne pouvons pas prédire quelles capacités apparaîtront à grande échelle, nous ne pouvons pas garantir la sécurité. Cela fait de l'interprétabilité mécaniste non plus une curiosité académique, mais une discipline d'ingénierie et de sécurité essentielle. Sans elle, nous nous contentons de "red-teaming" et de corriger les comportements de l'extérieur (comme avec le RLHF). Avec elle, nous pouvons potentiellement comprendre les mécanismes internes qui _causent_ le comportement et intervenir directement. Un ingénieur visant l'expertise dans les agents doit donc également investir dans la compréhension de l'interprétabilité, car ce sera la discipline de base pour déboguer, contrôler et faire confiance aux agents futurs et plus puissants.  

## Partie V : Implémentation Pratique et Évaluation

Cette partie se concentre sur les aspects pratiques, traduisant la théorie en actions concrètes. Elle couvre les principaux frameworks pour la construction d'agents, le sous-système critique de la Génération Augmentée par Récupération (RAG), et les méthodologies essentielles pour évaluer et renforcer la robustesse des prompts et des agents contre les défaillances.

### 5.1 Frameworks pour la Construction d'Agents : Un Guide Comparatif

Le choix du bon framework est une première étape critique dans tout projet d'agent. Cette section compare les philosophies et les architectures des frameworks d'agents open-source les plus populaires.

- **LangChain** : C'est un framework complet et extrêmement flexible pour la construction de toute application basée sur les LLM. Sa force réside dans sa vaste bibliothèque d'**intégrations** (modèles, outils, bases de données) et son architecture modulaire basée sur des "chaînes". **LangGraph**, une extension plus récente, permet de créer des flux de travail complexes, avec état et multi-agents, incluant des cycles et des branchements conditionnels. Cela le rend très puissant, mais aussi plus complexe à mettre en place et à déboguer. Les composants clés sont l'`Agent` (le moteur de raisonnement), les `Tools` (les fonctions que l'agent peut appeler) et l'`AgentExecutor` (qui exécute la boucle agentique).  
    
- **CrewAI** : Construit sur LangChain, CrewAI adopte une approche plus spécialisée et de plus haut niveau, spécifiquement axée sur la **collaboration multi-agents**. Il utilise un paradigme de jeu de rôle où l'on définit des agents avec des rôles, des objectifs et des histoires spécifiques, et une "équipe" (crew) qui orchestre leur collaboration pour accomplir une tâche complexe. Il sacrifie une partie de la flexibilité de bas niveau de LangChain au profit d'une plus grande facilité d'utilisation et d'une approche plus structurée du travail d'équipe, ce qui en fait un excellent choix pour prototyper rapidement des systèmes multi-agents.  
    
- **AutoGPT** : Il s'agit moins d'un framework de développement que d'une **implémentation spécifique** et populaire d'un agent entièrement autonome. Sa valeur réside dans sa démonstration de ce qui est possible et comme source de patrons architecturaux (par exemple, sa boucle pensée-plan-exécution ). Cependant, il est moins un outil de développement à usage général que LangChain ou CrewAI, qui sont conçus pour être des bibliothèques.  
    

|Framework|Philosophie Fondamentale|Abstraction Principale|Forces|Faiblesses|Cas d'Usage Idéal|
|---|---|---|---|---|---|
|**LangChain**|Flexibilité et intégration maximales. Une "boîte à outils" complète pour les applications LLM.|Chaînes (Chains) et Graphes (LangGraph)|Vaste écosystème d'intégrations, très flexible, contrôle granulaire, supporte les graphes complexes avec états.|Courbe d'apprentissage abrupte, peut être verbeux, la complexité peut devenir difficile à gérer.|Construction de chaînes d'outils complexes pour un agent unique, ou des systèmes multi-agents personnalisés nécessitant un contrôle total du flux.|
|**CrewAI**|Collaboration multi-agents basée sur les rôles. Simplicité et structure.|Équipe (Crew) et Rôles|Très intuitif pour les systèmes multi-agents, mise en place rapide, favorise la spécialisation des tâches.|Moins flexible que LangChain pour les applications générales, plus difficile à personnaliser en profondeur. Complexité de l'orchestration à grande échelle.|Prototypage rapide et déploiement de systèmes où plusieurs agents spécialisés doivent collaborer de manière structurée (par ex., une équipe de recherche et rédaction).|
|**AutoGPT**|Autonomie totale de l'agent. Démonstration de concept.|Boucle Pensée-Plan-Exécution|A popularisé le concept d'agent autonome, bon exemple d'une boucle complète.|N'est pas un framework de développement, monolithique, difficile à adapter ou à intégrer dans d'autres systèmes.|Comme étude de cas pour comprendre les principes des agents autonomes, ou pour des tâches simples et bien définies ne nécessitant pas de personnalisation poussée.|
|**Tableau 3 : Analyse Comparative des Frameworks Agentiques**||||||

 

### 5.2 Génération Augmentée par Récupération (RAG) Avancée pour les Agents

Le raisonnement d'un agent n'est aussi bon que l'information dont il dispose. La RAG est le principal mécanisme pour ancrer les agents dans des connaissances externes, à jour ou propriétaires. La RAG avancée n'est donc pas une option, mais une composante non négociable de tout système agentique sérieux.

Le RAG de base, qui consiste à récupérer quelques morceaux de texte et à les insérer dans un prompt, souffre de limitations, notamment face à des requêtes complexes et au problème du "perdu au milieu". Les techniques avancées visent à améliorer la précision de la récupération et la qualité de la génération.  

- **Fragmentation (Chunking) Avancée** :
    
    - **Fragmentation Sémantique** : Au lieu de couper le texte en morceaux de taille fixe, cette méthode divise le texte en fonction de la similarité sémantique (par exemple, la distance cosinus entre les plongements de phrases), créant ainsi des fragments plus cohérents sur le plan du sens.  
        
    - **Fragmentation Basée sur les Propositions** : Une technique encore plus avancée utilise un LLM pour décomposer le texte en faits atomiques et autonomes appelés "propositions". Ce sont ces propositions qui sont ensuite intégrées (embedded). Cela offre la plus grande précision mais est très coûteux en calcul.  
        
- **Récupération et Reclassement Avancés** :
    
    - **Expansion de Requête** : La requête de l'utilisateur est enrichie de synonymes ou de concepts connexes pour élargir la recherche et améliorer le rappel (recall).  
        
    - **Recherche Hybride** : Combine la recherche par mots-clés (pour les correspondances exactes) et la recherche vectorielle (pour la similarité sémantique) afin d'obtenir le meilleur des deux mondes.  
        
    - **Reclassement (Reranking)** : C'est une étape cruciale. Après une récupération initiale qui "sur-récupère" volontairement de nombreux documents (par exemple, les 50 premiers résultats), un modèle de reclassement plus puissant mais plus lent (généralement un cross-encoder) est utilisé pour réordonner ces documents en fonction de leur pertinence réelle par rapport à la requête, avant de ne transmettre que les meilleurs (par exemple, les 5 premiers) au LLM.  
        
- **Filtrage et Génération** :
    
    - **Autocut** : Une méthode pour filtrer les documents récupérés non pertinents. Elle fonctionne en identifiant une chute brutale dans les scores de similarité des documents récupérés et en coupant tout ce qui se trouve en dessous de ce seuil. Cela évite de "distraire" le LLM avec du bruit.  
        

### 5.3 Mesurer et Assurer la Robustesse des Prompts

Un prompt qui fonctionne parfaitement aujourd'hui peut se briser demain suite à une mise à jour mineure du modèle ou à une légère reformulation de la part de l'utilisateur. La robustesse est la mesure de la capacité d'un prompt à maintenir ses performances face à de telles perturbations. C'est une exigence non fonctionnelle clé pour tout système en production.

Les LLM sont connus pour leur grande sensibilité aux changements superficiels dans le format du prompt, tels que des espaces supplémentaires, des changements de ponctuation ou l'ordre des exemples en few-shot. Il est donc essentiel de mesurer cette sensibilité.  

- **Mesure de la Robustesse** :
    
    - **FormatSpread** : Une méthode proposée pour quantifier la variation de performance en calculant la différence de performance entre le format de prompt le plus performant et le moins performant pour une tâche donnée.  
        
    - **PromptEval** : Une méthode efficace pour évaluer les LLM sur _plusieurs_ prompts au lieu d'un seul, donnant une image plus réaliste et robuste de la performance attendue.  
        
- **Amélioration de la Robustesse et de la Généralisation** :
    
    - **Framework SALAD** : Présenté à l'ACL 2025 , ce cadre vise à améliorer la robustesse contre les corrélations fallacieuses (spurious correlations). Il utilise l'apprentissage contrastif avec deux types de données augmentées :  
        
        1. **Des échantillons positifs conscients de la structure** : Créés en masquant des mots non causals (identifiés via l'étiquetage morpho-syntaxique, POS tagging).
            
        2. **Des échantillons négatifs contrefactuels** : Générés par un LLM pour présenter des schémas de phrases diversifiés avec une étiquette inversée.
            
    - Cette approche force le modèle à apprendre les véritables relations structurelles dans les données plutôt que de se fier à des raccourcis de surface, ce qui le rend plus robuste aux variations.  
        

### 5.4 Le Défi de l'Alignement : Biais et Sécurité

À mesure que les agents deviennent plus autonomes, il est primordial de s'assurer qu'ils sont alignés sur les valeurs humaines et exempts de biais préjudiciables. Cette section examine l'état des biais dans les modèles actuels et les techniques utilisées pour les atténuer.

Des études montrent que même les modèles explicitement alignés sur des valeurs, comme GPT-4 et Claude 3, présentent des **biais stéréotypés sociétaux** envahissants concernant la race, le genre et la religion. GPT-4 a également montré un biais politique persistant en faveur de la gauche dans plusieurs études américaines. Ces biais peuvent provenir des données d'entraînement, mais aussi du processus de tokenisation lui-même, qui peut sous-représenter les langues non anglaises et leurs nuances culturelles.  

- **IA Constitutionnelle (Constitutional AI, CAI)** : C'est la technique d'alignement phare d'Anthropic. C'est un processus en deux phases :  
    
    1. **Phase Supervisée** : Un LLM génère des réponses à des prompts potentiellement dangereux. Ensuite, il est invité à critiquer et à réviser ses propres réponses sur la base d'une "constitution" écrite par des humains (un ensemble de principes éthiques). Le modèle est ensuite affiné (fine-tuned) sur ces réponses auto-révisées et plus sûres.
        
    2. **Phase RL (RLAIF - RL from AI Feedback)** : Un modèle de préférence est entraîné sur des retours générés par l'IA elle-même. Pour ce faire, le LLM compare deux réponses en se basant sur la constitution. Ce modèle de préférence est ensuite utilisé comme signal de récompense pour le RLHF, remplaçant ainsi les évaluateurs humains pour les questions de sécurité. L'objectif est de créer un assistant inoffensif mais _non évasif_, c'est-à-dire un assistant qui explique ses objections au lieu de simplement refuser de répondre.  
        
- **Pilotage de Caractéristiques (Feature Steering)** : Une approche plus récente et plus chirurgicale de l'atténuation des biais, basée sur l'interprétabilité et actuellement en recherche chez Anthropic. Elle consiste à identifier les caractéristiques internes du modèle qui correspondent à des concepts spécifiques (par exemple, une caractéristique "biais de genre") et à manipuler directement leurs activations pendant l'inférence pour orienter le comportement du modèle loin du biais. Bien que prometteuse, cette technique peut avoir des effets hors cible imprévisibles.  
    

La construction d'un agent de production n'est pas une entreprise monolithique. C'est un problème d'intégration de systèmes, où l'ingénieur doit penser en termes de "pile agentique" modulaire. Cette pile comprend un **cadre d'orchestration** (par exemple, LangChain), un **pipeline RAG avancé** (avec fragmentation sémantique, reclassement, etc.), un **moteur de raisonnement** (par exemple, une structure de prompt ToT), un **LLM de base** (par exemple, Claude 3), et une couche d'**évaluation et de vérification de la robustesse**. L'expertise ne consiste pas seulement à savoir écrire un prompt, mais à savoir concevoir, mettre en œuvre et évaluer chaque couche de cette pile. La qualité de l'agent final est déterminée par le maillon le plus faible de cette chaîne.

De même, la présence de biais intrinsèques profonds, même dans les modèles entraînés avec des techniques avancées comme la CAI, montre que l'alignement n'est pas une propriété acquise une fois pour toutes lors de l'entraînement. C'est un processus actif et continu de surveillance, d'évaluation et d'intervention. Pour un praticien, cela signifie qu'on ne peut pas simplement faire confiance à une API pour être "alignée". Il faut supposer que des biais existent et construire ses propres couches d'évaluation et d'atténuation. Cela peut impliquer des atténuations au niveau du prompt (par exemple, "Remettez en question mon cadrage lorsque les preuves le justifient" ), des vérifications post-traitement, ou l'utilisation de plusieurs modèles comme contre-vérification. La responsabilité de l'alignement est partagée entre le fournisseur du modèle et le développeur de l'application.  

## Partie VI : Synthèse et Recommandations pour une Pratique Avancée

Cette dernière partie synthétise les thèmes clés du rapport et fournit une feuille de route concrète et exploitable pour l'ingénieur cherchant à développer une expertise de pointe.

### 6.1 Les Arbitrages Fondamentaux dans la Conception de Systèmes Agentiques

Une analyse approfondie du domaine révèle plusieurs arbitrages récurrents qui sont au cœur de la conception des systèmes agentiques. La maîtrise de ces compromis est la marque d'un praticien expert.

- **Complexité du Raisonnement vs. Performance/Coût** : La hiérarchie CoT → ToT → GoT illustre clairement qu'un raisonnement plus puissant et plus flexible se paie par une latence plus élevée et un plus grand nombre d'appels à l'API. Le choix de la bonne structure de raisonnement est une décision d'ingénierie qui doit équilibrer la complexité du problème avec les contraintes de budget.
    
- **Flexibilité vs. Facilité d'Utilisation** : La comparaison entre LangChain et CrewAI met en évidence le compromis entre un framework très flexible mais complexe, qui offre un contrôle total, et un framework plus spécialisé mais plus facile à utiliser, qui accélère le développement pour des cas d'usage spécifiques.
    
- **Taille du Contexte vs. Intelligence du Contexte** : Le problème du "perdu au milieu" démontre qu'une grande fenêtre de contexte est inutile sans une récupération et un classement intelligents pour la gérer efficacement. L'investissement dans des techniques de RAG avancées est souvent plus rentable que le simple choix du modèle avec la plus grande fenêtre de contexte.
    
- **Autonomie vs. Contrôle** : Les agents entièrement autonomes comme AutoGPT peuvent être puissants mais sont souvent imprévisibles et difficiles à déboguer. Les systèmes plus contrôlés, avec un humain dans la boucle (human-in-the-loop), sont plus fiables et plus sûrs, mais moins autonomes.
    

### 6.2 Feuille de Route vers l'Expertise : Recommandations pour une Étude Approfondie

Pour l'ingénieur en Machine Learning souhaitant acquérir une expertise approfondie, une approche structurée combinant étude théorique, pratique du code et expérimentation est recommandée.

- **Articles Fondamentaux à Maîtriser** : Une lecture approfondie et une compréhension intime des articles de recherche suivants fourniront une base théorique solide :
    
    - _ReAct: Synergizing Reasoning and Acting in Language Models_ (Yao et al., 2022) : Pour comprendre la boucle fondamentale raisonnement-action.  
        
    - _Tree of Thoughts: Deliberate Problem Solving with Large Language Models_ (Yao et al., 2023) : Pour maîtriser le raisonnement exploratoire.  
        
    - _Cognitive Architectures for Language Agents_ (Sumers et al., 2023) : Pour acquérir le vocabulaire et le cadre de conception des agents.  
        
    - _Lost in the Middle: How Language Models Use Long Contexts_ (Liu et al., 2023) : Pour comprendre les limitations critiques des longues fenêtres de contexte.  
        
    - _Reasoning on a Spectrum: Aligning LLMs to System 1 and System 2 Thinking_ (Ziabari et al., 2025) : Pour explorer la frontière de la recherche sur le raisonnement de type humain.  
        
- **Projets Open-Source pour l'Apprentissage Pratique** : L'expertise ne s'acquiert pas seulement par la lecture. Il est recommandé non seulement d'utiliser, mais aussi de lire le code source et de contribuer aux frameworks clés suivants :
    
    - **LangChain / LangGraph** : Pour maîtriser la construction de chaînes d'outils et de graphes complexes.  
        
    - **CrewAI** : Pour acquérir une expérience pratique de l'orchestration multi-agents.  
        
    - **TransformerLens** : Pour s'initier aux techniques d'interprétabilité mécaniste comme le patching d'activation et commencer à "ouvrir la boîte noire".  
        
- **Méthodologie d'Expérimentation Personnelle** : Mettre en place un protocole d'expérimentation personnel pour tester la robustesse des prompts. Cela devrait inclure :
    
    1. La création d'un petit benchmark de tâches pertinentes pour le domaine d'intérêt de l'utilisateur.
        
    2. La définition de métriques claires (par exemple, précision, différence de logit, coût en tokens, latence).
        
    3. Le test systématique de différentes techniques de prompting (CoT, ToT), de variations de format, et de différents modèles de pointe pour développer une intuition profonde des compromis.
        
- **Tendances Émergentes à Surveiller** : Garder un œil attentif sur les domaines de recherche qui façonneront l'avenir des agents en 2025 et au-delà :
    
    - Le développement de **modèles spécialisés dans le raisonnement** (comme la série-o d'OpenAI).
        
    - L'application pratique du **raisonnement basé sur des graphes (GoT)** et l'émergence de frameworks qui le supportent.
        
    - L'**intégration de l'interprétabilité dans le cycle de développement** comme outil de débogage et d'alignement.
        
    - L'évolution des **cadres de collaboration multi-agents** vers des systèmes plus dynamiques et auto-organisés.
        

En suivant cette feuille de route, un ingénieur peut systématiquement construire une expertise qui est non seulement profonde sur le plan technique, mais aussi nuancée, pratique et prête pour l'avenir dans le domaine en évolution rapide des systèmes agentiques.


### Sources et Références

1. Cognitive Architectures for Language Agents - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2309.02427v3](https://arxiv.org/html/2309.02427v3)
    
2. (PDF) Cognitive Architectures for Language Agents - ResearchGate, consulté le juillet 6, 2025, [https://www.researchgate.net/publication/373715148_Cognitive_Architectures_for_Language_Agents](https://www.researchgate.net/publication/373715148_Cognitive_Architectures_for_Language_Agents)
    
3. Cognitive Architectures for Language Agents | OpenReview, consulté le juillet 6, 2025, [https://openreview.net/forum?id=1i6ZCvflQJ](https://openreview.net/forum?id=1i6ZCvflQJ)
    
4. Cognitive Architectures for Language Agents - Casts - ScienceCast, consulté le juillet 6, 2025, [https://sciencecast.org/casts/f639qu0lcp7s](https://sciencecast.org/casts/f639qu0lcp7s)
    
5. Cognitive Architectures for Language Agents (Sumers et al., 2024) - YouTube, consulté le juillet 6, 2025, [https://www.youtube.com/watch?v=jK9jbYOSZvA](https://www.youtube.com/watch?v=jK9jbYOSZvA)
    
6. AutoGPT: Overview, advantages, installation guide, and best practices, consulté le juillet 6, 2025, [https://www.leewayhertz.com/autogpt/](https://www.leewayhertz.com/autogpt/)
    
7. Deep Dive into AutoGPT: The Autonomous AI Revolutionizing the Game | by Peter Chang, consulté le juillet 6, 2025, [https://peter-chang.medium.com/deep-dive-into-autogpt-the-autonomous-ai-revolutionizing-the-game-890bc82e5ec5](https://peter-chang.medium.com/deep-dive-into-autogpt-the-autonomous-ai-revolutionizing-the-game-890bc82e5ec5)
    
8. Exploring Autonomous Agents: A Semi-Technical Dive - Sequoia Capital, consulté le juillet 6, 2025, [https://www.sequoiacap.com/article/autonomous-agents-perspective/](https://www.sequoiacap.com/article/autonomous-agents-perspective/)
    
9. ReAct: Synergizing Reasoning and Acting in Language Models - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/pdf/2210.03629](https://arxiv.org/pdf/2210.03629)
    
10. [2403.14589] ReAct Meets ActRe: When Language Agents Enjoy Training Data Autonomy, consulté le juillet 6, 2025, [https://arxiv.org/abs/2403.14589](https://arxiv.org/abs/2403.14589)
    
11. Rethinking Agent Design: From Top-Down Workflows to Bottom-Up Skill Evolution - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2505.17673v1](https://arxiv.org/html/2505.17673v1)
    
12. Automated Design of Agentic Systems - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/pdf/2408.08435](https://arxiv.org/pdf/2408.08435)
    
13. Few-Shot Prompting - Prompt Engineering Guide, consulté le juillet 6, 2025, [https://www.promptingguide.ai/techniques/fewshot](https://www.promptingguide.ai/techniques/fewshot)
    
14. The Few Shot Prompting Guide - PromptHub, consulté le juillet 6, 2025, [https://www.prompthub.us/blog/the-few-shot-prompting-guide](https://www.prompthub.us/blog/the-few-shot-prompting-guide)
    
15. Mastering Few-Shot Prompting: A Comprehensive Guide | by Software Guide - Medium, consulté le juillet 6, 2025, [https://softwareguide.medium.com/mastering-few-shot-prompting-a-comprehensive-guide-6eda3761538c](https://softwareguide.medium.com/mastering-few-shot-prompting-a-comprehensive-guide-6eda3761538c)
    
16. Few-Shot Prompting: Techniques, Examples, and Best Practices - DigitalOcean, consulté le juillet 6, 2025, [https://www.digitalocean.com/community/tutorials/_few-shot-prompting-techniques-examples-best-practices](https://www.digitalocean.com/community/tutorials/_few-shot-prompting-techniques-examples-best-practices)
    
17. Prompting | How-to guides - Llama, consulté le juillet 6, 2025, [https://www.llama.com/docs/how-to-guides/prompting/](https://www.llama.com/docs/how-to-guides/prompting/)
    
18. How to Choose Your GenAI Prompting Strategy: Zero Shot vs. Few Shot Prompts - Matillion, consulté le juillet 6, 2025, [https://www.matillion.com/blog/gen-ai-prompt-strategy-zero-shot-few-shot-prompt](https://www.matillion.com/blog/gen-ai-prompt-strategy-zero-shot-few-shot-prompt)
    
19. Chain-of-Thought Prompting Elicits Reasoning in Large ... - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/pdf/2201.11903](https://arxiv.org/pdf/2201.11903)
    
20. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models - OpenReview, consulté le juillet 6, 2025, [https://openreview.net/pdf?id=_VjQlMeSB_J](https://openreview.net/pdf?id=_VjQlMeSB_J)
    
21. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models, consulté le juillet 6, 2025, [https://home.cse.ust.hk/~cktang/csit6000s/Password_Only/lec09-csit.pdf](https://home.cse.ust.hk/~cktang/csit6000s/Password_Only/lec09-csit.pdf)
    
22. Advanced Prompt Engineering Techniques - Mercity AI, consulté le juillet 6, 2025, [https://www.mercity.ai/blog-post/advanced-prompt-engineering-techniques](https://www.mercity.ai/blog-post/advanced-prompt-engineering-techniques)
    
23. Chain of Thought Prompting (CoT): Everything you need to know - Vellum AI, consulté le juillet 6, 2025, [https://www.vellum.ai/blog/chain-of-thought-prompting-cot-everything-you-need-to-know](https://www.vellum.ai/blog/chain-of-thought-prompting-cot-everything-you-need-to-know)
    
24. Tree of Thoughts (ToT) - Prompt Engineering Guide, consulté le juillet 6, 2025, [https://www.promptingguide.ai/techniques/tot](https://www.promptingguide.ai/techniques/tot)
    
25. Tree of Thoughts: Deliberate Problem Solving with Large Language Models - NIPS, consulté le juillet 6, 2025, [https://papers.nips.cc/paper_files/paper/2023/hash/271db9922b8d1f4dd7aaef84ed5ac703-Abstract-Conference.html](https://papers.nips.cc/paper_files/paper/2023/hash/271db9922b8d1f4dd7aaef84ed5ac703-Abstract-Conference.html)
    
26. Tree of Thoughts: Deliberate Problem Solving with Large Language ..., consulté le juillet 6, 2025, [https://openreview.net/forum?id=5Xc1ecxO1h](https://openreview.net/forum?id=5Xc1ecxO1h)
    
27. Tree-of-Thought Prompting: Key Techniques and Use Cases - Helicone, consulté le juillet 6, 2025, [https://www.helicone.ai/blog/tree-of-thought-prompting](https://www.helicone.ai/blog/tree-of-thought-prompting)
    
28. Graph of Thoughts: Solving Elaborate Problems with Large ..., consulté le juillet 6, 2025, [https://ojs.aaai.org/index.php/AAAI/article/view/29720/31236](https://ojs.aaai.org/index.php/AAAI/article/view/29720/31236)
    
29. Graph of Thoughts: Solving Elaborate Problems with Large Language Models - HackMD, consulté le juillet 6, 2025, [https://hackmd.io/@machineS/HkhQZlqj0](https://hackmd.io/@machineS/HkhQZlqj0)
    
30. Prompt Chaining Langchain | IBM, consulté le juillet 6, 2025, [https://www.ibm.com/think/tutorials/prompt-chaining-langchain](https://www.ibm.com/think/tutorials/prompt-chaining-langchain)
    
31. Prompt Chaining Tutorial: What Is Prompt Chaining and How to Use It? - DataCamp, consulté le juillet 6, 2025, [https://www.datacamp.com/tutorial/prompt-chaining-llm](https://www.datacamp.com/tutorial/prompt-chaining-llm)
    
32. 4. Prompts Chaining - Chaining Together Multiple Prompts, consulté le juillet 6, 2025, [https://abc-notes.data.tech.gov.sg/notes/topic-3-building-system-with-advanced-prompting-and-chaining/4.-prompts-chaining-chaining-together-multiple-prompts.html](https://abc-notes.data.tech.gov.sg/notes/topic-3-building-system-with-advanced-prompting-and-chaining/4.-prompts-chaining-chaining-together-multiple-prompts.html)
    
33. Prompt Chaining | Prompt Engineering Guide, consulté le juillet 6, 2025, [https://www.promptingguide.ai/techniques/prompt_chaining](https://www.promptingguide.ai/techniques/prompt_chaining)
    
34. Meta-Prompting: LLMs Crafting & Enhancing Their Own Prompts | IntuitionLabs, consulté le juillet 6, 2025, [https://intuitionlabs.ai/articles/meta-prompting-llm-self-optimization](https://intuitionlabs.ai/articles/meta-prompting-llm-self-optimization)
    
35. A Complete Guide to Meta Prompting - PromptHub, consulté le juillet 6, 2025, [https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting](https://www.prompthub.us/blog/a-complete-guide-to-meta-prompting)
    
36. Meta Prompting | Prompt Engineering Guide, consulté le juillet 6, 2025, [https://www.promptingguide.ai/techniques/meta-prompting](https://www.promptingguide.ai/techniques/meta-prompting)
    
37. GPT-4 Technical Report | OpenAI, consulté le juillet 6, 2025, [https://cdn.openai.com/papers/gpt-4.pdf](https://cdn.openai.com/papers/gpt-4.pdf)
    
38. From System 1 to System 2: A Survey of Reasoning Large Language Models - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/pdf/2502.17419?](https://arxiv.org/pdf/2502.17419)
    
39. From System 1 to System 2: A Survey of Reasoning Large Language Models - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2502.17419v1](https://arxiv.org/html/2502.17419v1)
    
40. Large language model - Wikipedia, consulté le juillet 6, 2025, [https://en.wikipedia.org/wiki/Large_language_model](https://en.wikipedia.org/wiki/Large_language_model)
    
41. The Claude 3 Model Family: Opus, Sonnet, Haiku - Anthropic, consulté le juillet 6, 2025, [https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf](https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model_Card_Claude_3.pdf)
    
42. Claude 3.7 Sonnet System Card | Anthropic, consulté le juillet 6, 2025, [https://www.anthropic.com/claude-3-7-sonnet-system-card](https://www.anthropic.com/claude-3-7-sonnet-system-card)
    
43. Gemini 2.5: Pushing the Frontier with Advanced ... - Googleapis.com, consulté le juillet 6, 2025, [https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf](https://storage.googleapis.com/deepmind-media/gemini/gemini_v2_5_report.pdf)
    
44. What Is Meta's Llama 3.3 70B? How It Works, Use Cases & More ..., consulté le juillet 6, 2025, [https://www.datacamp.com/blog/llama-3-3-70b](https://www.datacamp.com/blog/llama-3-3-70b)
    
45. Comparing GPT-4o, LLaMA 3.1, and Claude 3.5 Sonnet - Walturn, consulté le juillet 6, 2025, [https://www.walturn.com/insights/comparing-gpt-4o-llama-3-1-and-claude-3-5-sonnet](https://www.walturn.com/insights/comparing-gpt-4o-llama-3-1-and-claude-3-5-sonnet)
    
46. Introducing Meta Llama 3: The most capable openly available LLM to date, consulté le juillet 6, 2025, [https://ai.meta.com/blog/meta-llama-3/](https://ai.meta.com/blog/meta-llama-3/)
    
47. Chatbot Arena - OpenLM.ai, consulté le juillet 6, 2025, [https://openlm.ai/chatbot-arena/](https://openlm.ai/chatbot-arena/)
    
48. AI Bias by Design: What the Claude Prompt Leak Reveals for Investment Professionals, consulté le juillet 6, 2025, [https://blogs.cfainstitute.org/investor/2025/05/14/ai-bias-by-design-what-the-claude-prompt-leak-reveals-for-investment-professionals/](https://blogs.cfainstitute.org/investor/2025/05/14/ai-bias-by-design-what-the-claude-prompt-leak-reveals-for-investment-professionals/)
    
49. Prompt Engineering with Llama 3.3 | by Tahir | Medium, consulté le juillet 6, 2025, [https://medium.com/@tahirbalarabe2/prompt-engineering-with-llama-3-3-032daa5999f7](https://medium.com/@tahirbalarabe2/prompt-engineering-with-llama-3-3-032daa5999f7)
    
50. Model Cards and Prompt formats - Llama 3.1, consulté le juillet 6, 2025, [https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/](https://www.llama.com/docs/model-cards-and-prompt-formats/llama3_1/)
    
51. Lost in the Middle: How Language Models Use Long Contexts, consulté le juillet 6, 2025, [https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf](https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf)
    
52. Do LLM's get "lost in the middle" during summarization as well? [D] : r/MachineLearning, consulté le juillet 6, 2025, [https://www.reddit.com/r/MachineLearning/comments/1beb7vi/do_llms_get_lost_in_the_middle_during/](https://www.reddit.com/r/MachineLearning/comments/1beb7vi/do_llms_get_lost_in_the_middle_during/)
    
53. Long Context Windows in LLMs are Deceptive (Lost in the Middle problem) - DEV Community, consulté le juillet 6, 2025, [https://dev.to/llmware/why-long-context-windows-for-llms-can-be-deceptive-lost-in-the-middle-problem-oj2](https://dev.to/llmware/why-long-context-windows-for-llms-can-be-deceptive-lost-in-the-middle-problem-oj2)
    
54. How to Use LLM Prompt Format: Tips, Examples, Mistakes, consulté le juillet 6, 2025, [https://futureagi.com/blogs/llm-prompts-best-practices-2025](https://futureagi.com/blogs/llm-prompts-best-practices-2025)
    
55. Chatbot Arena Leaderboard - a Hugging Face Space by lmarena-ai, consulté le juillet 6, 2025, [https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard](https://huggingface.co/spaces/lmarena-ai/chatbot-arena-leaderboard)
    
56. Leaderboard Overview - LMArena, consulté le juillet 6, 2025, [https://lmarena.ai/leaderboard](https://lmarena.ai/leaderboard)
    
57. Large Language Models and Emergence: A Complex Systems Perspective - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2506.11135v1](https://arxiv.org/html/2506.11135v1)
    
58. Emergent Abilities in Large Language Models: A Survey, consulté le juillet 6, 2025, [https://arxiv.org/pdf/2503.05788](https://arxiv.org/pdf/2503.05788)
    
59. Emergent Abilities in Large Language Models: A Survey - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2503.05788v2](https://arxiv.org/html/2503.05788v2)
    
60. Large Language Models: A Survey - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2402.06196v3](https://arxiv.org/html/2402.06196v3)
    
61. [2503.05788] Emergent Abilities in Large Language Models: A Survey - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/abs/2503.05788](https://arxiv.org/abs/2503.05788)
    
62. Emergent Abilities in Large Language Models: A Survey - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2503.05788v1](https://arxiv.org/html/2503.05788v1)
    
63. Reasoning on a Spectrum: Aligning LLMs to System 1 and System 2 Thinking - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2502.12470v1](https://arxiv.org/html/2502.12470v1)
    
64. Reasoning on a Spectrum: Aligning LLMs to System 1 and System 2 ..., consulté le juillet 6, 2025, [https://arxiv.org/pdf/2502.12470?](https://arxiv.org/pdf/2502.12470)
    
65. Reasoning on a Spectrum: Aligning LLMs to System 1 and System 2 Thinking, consulté le juillet 6, 2025, [https://www.researchgate.net/publication/389130936_Reasoning_on_a_Spectrum_Aligning_LLMs_to_System_1_and_System_2_Thinking](https://www.researchgate.net/publication/389130936_Reasoning_on_a_Spectrum_Aligning_LLMs_to_System_1_and_System_2_Thinking)
    
66. Understanding Dynamic Diffusion Process of LLM-based Agents ..., consulté le juillet 6, 2025, [https://arxiv.org/pdf/2502.13160](https://arxiv.org/pdf/2502.13160)
    
67. What are Attention Mechanisms in Language Models? - AI21 Labs, consulté le juillet 6, 2025, [https://www.ai21.com/knowledge/attention-mechanisms-language-models/](https://www.ai21.com/knowledge/attention-mechanisms-language-models/)
    
68. How to understand LLM's Attention Mechanism? How does it affect model performance?, consulté le juillet 6, 2025, [https://www.tencentcloud.com/techpedia/101866](https://www.tencentcloud.com/techpedia/101866)
    
69. Attention Mechanism for LLM-based Agents Dynamic Diffusion under Information Asymmetry - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2502.13160v3](https://arxiv.org/html/2502.13160v3)
    
70. Towards Best Practices of Activation Patching in Language Models: Metrics and Methods - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/pdf/2309.16042](https://arxiv.org/pdf/2309.16042)
    
71. Attribution Patching: Activation Patching At Industrial Scale - Neel Nanda, consulté le juillet 6, 2025, [https://www.neelnanda.io/mechanistic-interpretability/attribution-patching](https://www.neelnanda.io/mechanistic-interpretability/attribution-patching)
    
72. Advanced Interpretability Techniques for Tracing LLM Activations - Dejan AI, consulté le juillet 6, 2025, [https://dejan.ai/blog/advanced-interpretability-techniques-for-tracing-llm-activations/](https://dejan.ai/blog/advanced-interpretability-techniques-for-tracing-llm-activations/)
    
73. How to use and interpret activation patching - LessWrong, consulté le juillet 6, 2025, [https://www.lesswrong.com/posts/FhryNAFknqKAdDcYy/how-to-use-and-interpret-activation-patching](https://www.lesswrong.com/posts/FhryNAFknqKAdDcYy/how-to-use-and-interpret-activation-patching)
    
74. agents — LangChain documentation, consulté le juillet 6, 2025, [https://python.langchain.com/api_reference/langchain/agents.html](https://python.langchain.com/api_reference/langchain/agents.html)
    
75. LangChain, consulté le juillet 6, 2025, [https://www.langchain.com/](https://www.langchain.com/)
    
76. Agent SDK vs CrewAI vs LangChain: Which One to Use When? - Analytics Vidhya, consulté le juillet 6, 2025, [https://www.analyticsvidhya.com/blog/2025/03/agent-sdk-vs-crewai-vs-langchain/](https://www.analyticsvidhya.com/blog/2025/03/agent-sdk-vs-crewai-vs-langchain/)
    
77. LangChain, AutoGen, and CrewAI. Which AI Framework is Right for You in… | by Yashwant Deshmukh | Medium, consulté le juillet 6, 2025, [https://medium.com/@yashwant.deshmukh23/langchain-autogen-and-crewai-2593e7645de7](https://medium.com/@yashwant.deshmukh23/langchain-autogen-and-crewai-2593e7645de7)
    
78. What is CrewAI vs LangChain? | Vstorm Glossary, consulté le juillet 6, 2025, [https://vstorm.co/glossary/crewai-vs-langchain-2/](https://vstorm.co/glossary/crewai-vs-langchain-2/)
    
79. Langchain vs CrewAI: Comparative Framework Analysis ... - Orq.ai, consulté le juillet 6, 2025, [https://orq.ai/blog/langchain-vs-crewai](https://orq.ai/blog/langchain-vs-crewai)
    
80. Advanced RAG Techniques | DataCamp, consulté le juillet 6, 2025, [https://www.datacamp.com/blog/rag-advanced](https://www.datacamp.com/blog/rag-advanced)
    
81. Advanced RAG Techniques | Weaviate, consulté le juillet 6, 2025, [https://weaviate.io/blog/advanced-rag](https://weaviate.io/blog/advanced-rag)
    
82. Towards LLMs Robustness to Changes in Prompt Format Styles - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2504.06969v1](https://arxiv.org/html/2504.06969v1)
    
83. SALAD: Improving Robustness and Generalization ... - ACL Anthology, consulté le juillet 6, 2025, [https://aclanthology.org/2025.naacl-long.634.pdf](https://aclanthology.org/2025.naacl-long.634.pdf)
    
84. Explicitly unbiased large language models still form biased associations - PNAS, consulté le juillet 6, 2025, [https://www.pnas.org/doi/10.1073/pnas.2416228122](https://www.pnas.org/doi/10.1073/pnas.2416228122)
    
85. Is ChatGPT More Biased Than You? - Harvard Data Science Review, consulté le juillet 6, 2025, [https://hdsr.mitpress.mit.edu/pub/qh3dbdm9](https://hdsr.mitpress.mit.edu/pub/qh3dbdm9)
    
86. Large Language Model Tokenizer Bias: A Case Study and Solution on GPT-4o - arXiv, consulté le juillet 6, 2025, [https://arxiv.org/html/2406.11214v2](https://arxiv.org/html/2406.11214v2)
    
87. Constitutional AI: Harmlessness from AI Feedback - Anthropic, consulté le juillet 6, 2025, [https://www-cdn.anthropic.com/7512771452629584566b6303311496c262da1006/Anthropic_ConstitutionalAI_v2.pdf](https://www-cdn.anthropic.com/7512771452629584566b6303311496c262da1006/Anthropic_ConstitutionalAI_v2.pdf)
    
88. Constitutional AI: Harmlessness from AI Feedback - BibBase, consulté le juillet 6, 2025, [https://bibbase.org/network/publication/bai-kadavath-kundu-askell-kernion-jones-chen-goldie-etal-constitutionalaiharmlessnessfromaifeedback-2022](https://bibbase.org/network/publication/bai-kadavath-kundu-askell-kernion-jones-chen-goldie-etal-constitutionalaiharmlessnessfromaifeedback-2022)
    
89. AI-Powered Paper Summarization about the arXiv paper 2212.08073v1, consulté le juillet 6, 2025, [https://www.summarizepaper.com/en/arxiv-id/2212.08073v1/](https://www.summarizepaper.com/en/arxiv-id/2212.08073v1/)
    
90. Evaluating Feature Steering: Anthropic's Exploration of Mitigating Social Bias in AI, consulté le juillet 6, 2025, [https://www.startuphub.ai/evaluating-feature-steering-anthropics-exploration-of-mitigating-social-bias-in-ai/](https://www.startuphub.ai/evaluating-feature-steering-anthropics-exploration-of-mitigating-social-bias-in-ai/)
    
91. Evaluating feature steering: A case study in mitigating social biases - Anthropic, consulté le juillet 6, 2025, [https://www.anthropic.com/research/evaluating-feature-steering](https://www.anthropic.com/research/evaluating-feature-steering)
    
92. Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks. - GitHub, consulté le juillet 6, 2025, [https://github.com/crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)
    
