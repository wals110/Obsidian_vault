

Pour créer des applications avec des modèles de base, il vous faut d'abord ces modèles. Bien qu'il ne soit pas nécessaire de savoir comment développer un modèle pour l'utiliser, une compréhension générale vous aidera à choisir le modèle approprié et à l'adapter à vos besoins.

L'entraînement d'un modèle de base est un processus extrêmement complexe et coûteux. Ceux qui maîtrisent cette technique sont généralement tenus au secret par des accords de confidentialité. Ce chapitre ne vous expliquera pas comment construire un modèle capable de rivaliser avec ChatGPT. Je me concentrerai plutôt sur les choix de conception ayant un impact significatif sur les applications en aval.

Face au manque croissant de transparence dans le processus d'entraînement des modèles de base, il est difficile de connaître toutes les décisions de conception qui sous-tendent leur élaboration. Toutefois, les différences entre ces modèles s'expliquent généralement par les choix relatifs aux données d'entraînement, à l'architecture et à la taille du modèle, ainsi qu'à la manière dont ils sont affinés après l'entraînement afin de mieux correspondre aux préférences humaines.

Les modèles apprenant à partir des données, ces dernières révèlent beaucoup de choses sur leurs capacités et leurs limites. Ce chapitre commence par expliquer comment les développeurs de modèles organisent les données d'entraînement, en s'intéressant particulièrement à leur distribution. [Le chapitre 8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) explore en détail les techniques d'ingénierie des jeux de données, notamment l'évaluation de leur qualité et leur synthèse.

Étant donné la prédominance de l'architecture Transformer, le choix de l'architecture de modèle pourrait sembler moins pertinent. Vous vous demandez peut-être : qu'est-ce qui rend l'architecture Transformer si particulière et explique sa domination persistante ? Combien de temps faudra-t-il avant qu'une autre architecture ne prenne le relais, et à quoi ressemblera-t-elle ? Ce chapitre répondra à toutes ces questions. Lors de la publication d'un nouveau modèle, l'une des premières questions que se posent les utilisateurs concerne sa taille. Ce chapitre explorera également comment un développeur de modèles peut déterminer la taille appropriée pour son modèle.

Comme indiqué au [chapitre 1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_introduction_to_building_ai_applications_with_foun_1730130814984319) , le processus d'entraînement d'un modèle se divise généralement en pré-entraînement et post-entraînement. Le pré-entraînement rend le modèle performant, mais pas nécessairement sûr ni facile à utiliser. C'est là qu'intervient le post-entraînement. Son objectif est d'aligner le modèle sur les préférences humaines. Mais qu'entend-on exactement par _préférence humaine_ ? Comment la représenter de manière à ce qu'un modèle puisse l'apprendre ? La façon dont un développeur aligne son modèle a un impact significatif sur son ergonomie et sera abordée dans ce chapitre.

Si la plupart des gens comprennent l'impact de l'entraînement sur les performances d'un modèle, celui de _l'échantillonnage_ est souvent négligé. L'échantillonnage correspond à la manière dont un modèle choisit une sortie parmi toutes les options possibles. C'est peut-être l'un des concepts les plus sous-estimés en IA. Non seulement l'échantillonnage explique de nombreux comportements d'IA apparemment déroutants, tels que les hallucinations et les incohérences, mais le choix d'une stratégie d'échantillonnage appropriée peut également améliorer considérablement les performances d'un modèle avec un effort relativement faible. C'est pourquoi l'échantillonnage est la partie de ce chapitre qui m'a le plus enthousiasmé.

Les concepts abordés dans ce chapitre sont essentiels à la compréhension du reste de l'ouvrage. Toutefois, étant donné leur caractère fondamental, il est possible que vous les maîtrisiez déjà. N'hésitez donc pas à passer directement aux concepts que vous comprenez parfaitement. Si vous rencontrez des difficultés avec un concept plus tard, vous pourrez vous référer à ce chapitre.

# Données d'entraînement

La performance d'un modèle d'IA dépend de la qualité des données utilisées pour son entraînement. Sans données vietnamiennes, le modèle sera incapable de traduire de l'anglais vers le vietnamien. De même, un modèle de classification d'images entraîné uniquement sur des photos d'animaux ne sera pas performant sur des photos de plantes.

Si vous souhaitez qu'un modèle soit plus performant pour une tâche spécifique, vous pouvez inclure davantage de données relatives à cette tâche dans les données d'entraînement. Cependant, collecter suffisamment de données pour entraîner un modèle complexe n'est pas chose aisée et peut s'avérer coûteux. Les développeurs de modèles doivent souvent se contenter des données disponibles, même si celles-ci ne répondent pas exactement à leurs besoins.

[Par exemple, Common Crawl](https://oreil.ly/wf2Lw) , créé par une organisation à but non lucratif qui explore sporadiquement des sites web sur Internet, constitue une source courante de données d'entraînement . En 2022 et 2023, cette organisation a exploré environ 2 à 3 milliards de pages web par mois. Google propose un sous-ensemble propre de Common Crawl appelé [Colossal Clean Crawled Corpus](https://arxiv.org/abs/1910.10683v4) , ou C4.

La qualité des données de Common Crawl, et dans une certaine mesure de C4, est discutable : on y trouve des titres racoleurs, de la désinformation, de la propagande, des théories du complot, du racisme, de la misogynie et tous les sites web douteux que vous avez pu croiser ou éviter sur Internet. Une [étude du _Washington Post_](https://oreil.ly/-1UMD) montre que parmi les 1 000 sites les plus consultés de l’ensemble de données figurent plusieurs médias peu fiables selon [l’échelle de fiabilité de NewsGuard](https://oreil.ly/OisOs) . En clair, Common Crawl regorge de fausses informations.

Pourtant, du simple fait que Common Crawl soit disponible, des variantes de celui-ci sont utilisées dans la plupart des modèles de base qui divulguent leurs sources de données d'entraînement, notamment GPT-3 d'OpenAI et Gemini de Google. Je soupçonne que Common Crawl est également utilisé dans des modèles qui ne divulguent pas leurs données d'entraînement. Afin d'éviter l'attention du public et de la concurrence, de nombreuses entreprises ont cessé de divulguer ces informations.

Certaines équipes utilisent des heuristiques pour filtrer les données de faible qualité sur Internet. Par exemple, OpenAI n'a utilisé que les liens Reddit ayant reçu au moins trois votes positifs pour entraîner [GPT-2](https://oreil.ly/gGwRz) . Bien que cela permette d'éliminer les liens sans intérêt, Reddit n'est pas exactement un modèle de bienséance et de bon goût.

L'approche consistant à « utiliser ce que l'on a, et non ce que l'on souhaite » peut aboutir à des modèles performants sur les tâches présentes dans les données d'entraînement, mais pas nécessairement sur celles qui vous intéressent. Pour pallier ce problème, il est essentiel de constituer des jeux de données adaptés à vos besoins spécifiques. Cette section se concentre sur la constitution de données pour _des langages_ et _des domaines_ spécifiques , offrant ainsi une base à la fois large et spécialisée pour les applications dans ces domaines. [Le chapitre 8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) explore les stratégies de données pour les modèles conçus pour des tâches très spécifiques.

Bien que les modèles de base spécifiques à une langue et à un domaine puissent être entraînés à partir de zéro, il est également courant de les affiner sur la base de modèles à usage général.

Certains pourraient se demander pourquoi ne pas entraîner un modèle sur toutes les données disponibles, qu'elles soient générales ou spécialisées, afin qu'il soit capable de tout faire. C'est une pratique courante. Cependant, l'entraînement sur un plus grand nombre de données exige souvent davantage de ressources de calcul et n'entraîne pas systématiquement de meilleures performances. Par exemple, un modèle entraîné avec un volume réduit de données de haute qualité peut surpasser un modèle entraîné avec un grand volume de données de faible qualité. En utilisant 7 milliards de jetons de données de codage de haute qualité, [Gunasekar et al. (2023)](https://arxiv.org/abs/2306.11644) ont pu entraîner un modèle à 1,3 milliard de paramètres qui surpasse des modèles bien plus importants sur plusieurs benchmarks de codage essentiels. L'impact de la qualité des données est abordé plus en détail au [chapitre 8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) .

## Modèles multilingues

L'anglais domine Internet. Une analyse du jeu de données Common Crawl montre qu'il représente près de la moitié des données (45,88 %), soit huit fois plus que le russe, la deuxième langue la plus fréquente (5,97 %) ( [Lai et al., 2023](https://arxiv.org/abs/2304.05613) ). [Le tableau 2-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_table_1_1730147895537533) présente la liste des langues présentes à au moins 1 % dans Common Crawl. Les langues pour lesquelles les données d'entraînement sont peu disponibles – généralement celles qui ne figurent pas dans cette liste – sont considérées comme _ayant peu de ressources_ .

Tableau 2-1. Les langues les plus courantes dans Common Crawl, un ensemble de données populaire pour l'entraînement des LLM. Source : Lai et al. (2023).

| Langue      | Code | Populaire. | Taille CC |       |
| ----------- | ---- | ---------- | --------- | ----- |
|             |      | (M)        | (%)       | Chat. |
| Anglais     | en   | 1 452      | 45,8786   | H     |
| russe       | ru   | 258        | 5,9692    | H     |
| Allemand    | de   | 134        | 5,8811    | H     |
| Chinois     | zh   | 1 118      | 4,8747    | H     |
| japonais    | jp   | 125        | 4,7884    | H     |
| Français    | fr   | 274        | 4,7254    | H     |
| Espagnol    | es   | 548        | 4,4690    | H     |
| italien     | il   | 68         | 2,5712    | H     |
| Néerlandais | nl   | 30         | 2,0585    | H     |
| polonais    | pl   | 45         | 1,6636    | H     |
| portugais   | pt   | 257        | 1,1505    | H     |
| vietnamien  | vi   | 85         | 1,0299    | H     |

De nombreuses autres langues, malgré un grand nombre de locuteurs aujourd'hui, sont fortement sous-représentées dans Common Crawl. [Le tableau 2-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_table_2_1730147895537547) présente quelques exemples. Idéalement, le ratio entre la représentation de la langue dans la population mondiale et sa représentation dans Common Crawl devrait être de 1. Plus ce ratio est élevé, plus la langue est sous-représentée dans Common Crawl.

Tableau 2-2. Exemples de langues sous-représentées dans Common Crawl. La dernière ligne, l'anglais, est à titre de comparaison. Les pourcentages dans Common Crawl proviennent de Lai et al. (2023).

|Langue|Intervenants (millions)|% de la population mondiale [a](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id696)|% dans Common Crawl|Monde : Ratio de reptation commun|
|---|---|---|---|---|
|Punjabi|113|1,41%|0,0061%|231,56|
|Swahili|71|0,89%|0,0077%|115,26|
|ourdou|231|2,89%|0,0274%|105,38|
|Kannada|64|0,80%|0,0122%|65,57|
|Telugu|95|1,19%|0,0183%|64,89|
|Gujarati|62|0,78%|0,0126%|61,51|
|Marathi|99|1,24%|0,0213%|58.10|
|bengali|272|3,40%|0,0930%|36,56|
|**Anglais**|**1452**|**18,15%**|**45,88%**|**0,40**|
|[un](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id696-marker)On a utilisé une population mondiale de huit milliards d'habitants pour ce calcul.|   |   |   |   |

Étant donné la prédominance de l'anglais dans les données internet, il n'est pas surprenant que les modèles généralistes soient bien plus performants en anglais que dans d'autres langues, comme le montrent plusieurs études. Par exemple, sur le benchmark MMLU, un ensemble de 14 000 problèmes à choix multiples portant sur 57 matières, [GPT-4 a obtenu des résultats nettement supérieurs en anglais](https://oreil.ly/qK2Ap) qu'avec des langues sous-représentées comme le télougou, comme l'illustre la [figure 2-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_1_1730147895520810) (OpenAI, 2023).

![Graphique avec barres vertes et bleues. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0201.png)

###### Figure 2-1. Sur le benchmark MMLU, GPT-4 obtient de meilleurs résultats en anglais que dans toute autre langue. Pour obtenir les résultats MMLU dans d'autres langues, OpenAI a traduit les questions à l'aide d'Azure AI Translator.

De même, lors de tests sur six problèmes mathématiques du Projet Euler, Yennie Jun a constaté que GPT-4 était capable de résoudre les problèmes en anglais plus de trois fois plus souvent qu'en arménien ou en farsi. [GPT](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id697) -4 a échoué aux six questions en birman et en amharique, comme le montre la [figure 2-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_2_1730147895520828) .

![Un graphique avec des chiffres et un taux de réussite. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0202.png)

###### Figure 2-2. GPT-4 est bien meilleur en mathématiques en anglais que dans d'autres langues.

La sous-représentation est une des principales raisons de ces performances décevantes. Les trois langues affichant les plus faibles performances aux tests MMLU de GPT-4 — le télougou, le marathi et le pendjabi — figurent également parmi les langues les plus sous-représentées dans Common Crawl. Toutefois, la sous-représentation n'est pas la seule cause. La structure d'une langue et la culture qu'elle véhicule peuvent également complexifier son apprentissage pour un modèle.

Étant donné que les modèles linguistiques sont généralement performants en traduction, peut-on simplement traduire toutes les requêtes d'autres langues vers l'anglais, obtenir les réponses, puis les retraduire dans la langue d'origine ? Nombreux sont ceux qui adoptent cette approche, mais elle n'est pas idéale. Premièrement, elle exige un modèle capable de comprendre suffisamment les langues sous-représentées pour pouvoir les traduire. Deuxièmement, la traduction peut entraîner une perte d'information. Par exemple, certaines langues, comme le vietnamien, possèdent des pronoms pour indiquer la relation entre les interlocuteurs. Lors de la traduction vers l'anglais, tous ces pronoms sont traduits par _« je »_ et _« tu »_ , ce qui entraîne la perte de l'information relationnelle.

Les modèles peuvent également présenter des problèmes de performance inattendus dans les langues autres que l'anglais.Par exemple, [NewsGuard a constaté que ChatGPT est plus enclin à produire de la désinformation en chinois qu'en anglais. En avril 2023, NewsGuard a demandé à ChatGPT-3.5 de produire des articles de désinformation sur la Chine en anglais, en chinois simplifié et en chinois](https://oreil.ly/LcBfx) [traditionnel](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id699) . En anglais, ChatGPT a refusé de produire de fausses informations pour six des sept questions posées. Cependant, il a produit de fausses informations en chinois simplifié et en chinois traditionnel à chaque fois. Les raisons de cette différence de comportement restent floues.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id699)

Outre les problèmes de qualité, les modèles peuvent également être plus lents et plus coûteux pour les langues autres que l'anglais. La latence et le coût d'inférence d'un modèle sont proportionnels au nombre de jetons dans les données d'entrée et de réponse.Il s'avère que la tokenisation est bien plus efficace pour certaines langues que pour d'autres. En comparant les performances de GPT-4 sur MASSIVE, un ensemble de données d'un million de textes courts traduits dans 52 langues, Yennie Jun a constaté que, pour exprimer la même idée, des langues comme le birman et l'hindi nécessitent [beaucoup plus de tokens](https://oreil.ly/Zq5Sw) que l'anglais ou l'espagnol. Sur l'ensemble de données MASSIVE, la longueur médiane d'un token est de 7 en anglais, mais elle est de 32 en hindi et de 72 en birman, soit dix fois plus qu'en anglais.

En supposant que le temps de génération d'un jeton soit identique dans toutes les langues, GPT-4 met environ dix fois plus de temps en birman qu'en anglais pour un même contenu. Pour les API facturant à l'utilisation de jetons, le birman coûte donc dix fois plus cher que l'anglais.

Pour remédier à cela, de nombreux modèles ont été entraînés pour traiter des langues autres que l'anglais. La langue la plus utilisée, après l'anglais, est sans aucun doute le chinois, avec des modèles comme [ChatGLM](https://github.com/THUDM/ChatGLM2-6B) , [YAYI](https://github.com/wenge-research/YAYI) , [Llama-Chinese](https://github.com/LlamaFamily/Llama-Chinese) , et d'autres. Il existe également des modèles en français ( [CroissantLLM](https://oreil.ly/a6j-N) ), en vietnamien ( [PhoGPT](https://github.com/VinAIResearch/PhoGPT) ), en arabe ( [Jais](https://oreil.ly/uG27L) ), et dans bien d'autres langues..

## Modèles spécifiques au domaine

Les modèles généralistes comme [Gemini](https://oreil.ly/4XsOV) , [GPT](https://oreil.ly/KLVgX) et [Llamas](https://oreil.ly/58gxQ) peuvent obtenir d'excellents résultats dans un large éventail de domaines, notamment la programmation, le droit, les sciences, le commerce, le sport et les sciences de l'environnement. Ceci est dû en grande partie à l'inclusion de ces domaines dans leurs données d'entraînement. [La figure 2-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_3_1730147895520839) [illustre](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id705) la répartition des domaines présents dans Common Crawl selon l' analyse du _Washington Post_ de 2023.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id705)

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0203.png)

###### Figure 2-3. Répartition des domaines dans l'ensemble de données C4. Reproduite d'après les statistiques du _Washington Post_ . Il convient de noter que cette analyse ne présente que les catégories présentes, et non celles qui sont absentes.

À l'heure actuelle, peu d'analyses de la distribution des domaines dans les données visuelles ont été réalisées. Cela pourrait s'expliquer par le fait que les images sont plus difficiles à catégoriser que les textes. [4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id706) Cependant, il est possible de déduire les domaines d'application d'un modèle à partir de ses performances de référence. [Le tableau 2-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_table_3_1730147895537555) illustre comment deux modèles,CLIP et Open CLIP [sont évalués sur différents jeux de données](https://oreil.ly/MTqyR) . Ces jeux de données montrent la performance de ces deux modèles sur des oiseaux, des fleurs, des voitures et quelques autres catégories, mais le monde est bien plus vaste et complexe que ces quelques catégories.

Tableau 2-3. Open CLIP et performances de CLIP sur différents ensembles de données d'images.

|Ensemble de données|Précision CLIP  <br>de ViT-B/32 (OpenAI)|Précision du clip ouvert  <br>ViT-B/32 (Cade)|
|---|---|---|
|ImageNet|63.2|62,9|
|ImageNet v2|–|62.6|
|Birdsnap|37,8|46.0|
|Pays211|17.8|14.8|
|Oxford 102 Catégorie Fleur|66,7|66.0|
|Référence allemande en matière de reconnaissance des panneaux de signalisation routière|32.2|42.0|
|Voitures de Stanford|59,4|79,3|
|UCF101|64,5|63.1|

Bien que les modèles de base généralistes puissent répondre à des questions courantes dans différents domaines, leurs performances sont généralement faibles pour les tâches spécifiques à un domaine, surtout s'ils n'ont jamais été confrontés à ces tâches lors de leur entraînement. La découverte de médicaments et le dépistage du cancer en sont deux exemples. La découverte de médicaments implique des données sur les protéines, l'ADN et l'ARN, qui suivent des formats spécifiques et sont coûteuses à acquérir. Ces données sont rarement disponibles publiquement sur Internet. De même, le dépistage du cancer nécessite généralement des radiographies et des IRMf (imagerie par résonance magnétique fonctionnelle), examens difficiles à obtenir en raison des règles de confidentialité.

Pour entraîner un modèle à exceller dans ces tâches spécifiques à un domaine, il peut être nécessaire de constituer des ensembles de données très précis. L'un des modèles les plus connus est sans doute [AlphaFold de DeepMind](https://oreil.ly/JX37g) , entraîné sur les séquences et les structures 3D d'environ 100 000 protéines connues. [BioNeMo de NVIDIA](https://oreil.ly/M1Nsc) est un autre modèle qui se concentre sur les données biomoléculaires pour la découverte de médicaments. [Med-PaLM2 de Google](https://oreil.ly/F76hq) a combiné la puissance d'un modèle linéaire généralisé (LLM) avec des données médicales pour répondre aux requêtes médicales avec une plus grande précision.

###### Conseil

Les modèles spécifiques à un domaine sont particulièrement courants en biomédecine, mais d'autres domaines peuvent également en tirer profit. Un modèle entraîné sur des croquis architecturaux pourrait s'avérer bien plus utile aux architectes que le modèle de diffusion stable, ou un modèle entraîné sur des plans d'usine pourrait être optimisé pour les processus de fabrication bien mieux qu'un modèle générique comme ChatGPT.

Cette section a donné un aperçu général de l'impact des données d'entraînement sur les performances d'un modèle. Voyons maintenant l'influence de la conception du modèle sur ses performances..

# Modélisation

Avant d'entraîner un modèle, les développeurs doivent définir sa structure. Quelle architecture adopter ? Combien de paramètres doit-il comporter ? Ces décisions influent non seulement sur les capacités du modèle, mais aussi sur sa facilité d'utilisation pour les applications en aval . Par [exemple](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id715) , un modèle à 7 milliards de paramètres sera beaucoup plus simple à déployer qu'un modèle à 175 milliards de paramètres. De même, l'optimisation d'un modèle Transformer pour réduire la latence diffère considérablement de l'optimisation d'une autre architecture. Examinons les facteurs qui sous-tendent ces décisions.

## Architecture du modèle

À l'heure actuelle, l'architecture dominante pour les modèles de base basés sur le langage est l' architecture _Transformer (_ [Vaswani et al., 2017](https://arxiv.org/abs/1706.03762) ), fondée sur le mécanisme d'attention. Elle pallie de nombreuses limitations des architectures précédentes, ce qui explique sa popularité. Cependant, l'architecture Transformer présente elle aussi des limitations. Cette section analyse l'architecture Transformer et ses alternatives. Étant donné qu'elle aborde les détails techniques des différentes architectures, elle peut s'avérer complexe. Si vous jugez une partie trop technique, n'hésitez pas à la sauter.

### Architecture Transformer

Pour comprendre le transformateur, examinons le problème qu'il a été conçu pour résoudre. L'architecture du transformateur a été popularisée dans la foulée du succès de l' [architecture seq2seq (séquence à séquence)](https://arxiv.org/abs/1409.3215) . Lors de son lancement en 2014, seq2seq a permis d'améliorer significativement des tâches alors complexes : la traduction automatique et la synthèse automatique. En 2016, [Google a intégré seq2seq à Google Traduction](https://oreil.ly/fb1aR) , une mise à jour qui, selon l'entreprise, a permis d'obtenir les « plus grandes améliorations à ce jour en matière de qualité de traduction automatique ». Cela a suscité un vif intérêt pour seq2seq, qui est devenu l'architecture de référence pour les tâches impliquant des séquences de texte.

De manière générale, seq2seq comprend un encodeur qui traite les entrées et un décodeur qui génère les sorties. Les entrées et les sorties sont des séquences de jetons, d'où son nom. Seq2seq utilise des RNN (réseaux de neurones récurrents) comme encodeur et décodeur. Dans sa forme la plus simple, l'encodeur traite les jetons d'entrée séquentiellement, produisant l'état caché final qui représente l'entrée. Le décodeur génère ensuite les jetons de sortie séquentiellement, en fonction de l'état caché final de l'entrée et du jeton précédemment généré. Une visualisation de l'architecture de seq2seq est présentée dans la partie supérieure de [la figure 2-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_4_1730147895520851) .

![Diagramme d'un algorithme. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0204.png)

###### Figure 2-4. Architecture Seq2seq versus architecture de type transformateur. Dans l'architecture de type transformateur, les flèches indiquent les jetons que le décodeur prend en compte lors de la génération de chaque jeton de sortie.

Vaswani et al. (2017) abordent deux problèmes liés à l'algorithme seq2seq. Premièrement, le décodeur seq2seq classique génère des jetons de sortie en utilisant uniquement l'état caché final de l'entrée. Intuitivement, cela revient à générer des réponses sur un livre à partir de son résumé. Cette approche limite la qualité des sorties générées. Deuxièmement, l'encodeur et le décodeur RNN impliquent que le traitement de l'entrée et la génération de la sortie sont effectués séquentiellement, ce qui ralentit le processus pour les longues séquences. Si une entrée comporte 200 jetons, seq2seq doit attendre la fin du traitement de chaque jeton avant de passer au suivant [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id719)

L'architecture du transformateur résout ces deux problèmes grâce au mécanisme d'attention. Ce mécanisme permet au modèle de pondérer l'importance des différents jetons d'entrée lors de la génération de chaque jeton de sortie. Cela revient à générer des réponses en consultant n'importe quelle page du livre. Une visualisation simplifiée de l'architecture du transformateur est présentée dans la partie inférieure de [la figure 2-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_4_1730147895520851) .

###### Note

Bien que le mécanisme d'attention soit souvent associé au modèle Transformer, il a été introduit trois ans avant la publication de l'article sur les Transformers. Ce mécanisme peut également être utilisé avec d'autres architectures. Google l'a utilisé avec son architecture seq2seq en 2016 pour son modèle GNMT (Google Neural Machine Translation). Cependant, ce n'est qu'après la publication de l'article sur les Transformers, démontrant que le mécanisme d'attention pouvait être utilisé sans RNN, qu'il a connu un essor considérable [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id720)

L'architecture Transformer se passe entièrement de RNN. Grâce aux Transformers, les jetons d'entrée peuvent être traités en parallèle, ce qui accélère considérablement le traitement des données. Bien que le Transformer élimine le goulot d'étranglement lié à l'entrée séquentielle, les modèles de langage autorégressifs basés sur les Transformers conservent celui de la sortie séquentielle.

L'inférence pour les modèles de langage basés sur les transformateurs se compose donc de deux étapes :

Préremplissage

Le modèle traite les jetons d'entrée en parallèle. Cette étape crée l'état intermédiaire nécessaire à la génération du premier jeton de sortie. Cet état intermédiaire comprend les vecteurs clé-valeur de tous les jetons d'entrée.

Décoder

Le modèle génère un jeton de sortie à la fois.

Comme nous l'explorerons plus loin dans [le chapitre 9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301) , la nature parallélisable du préremplissage et l'aspect séquentiel du décodage motivent toutes deux de nombreuses techniques d'optimisation pour rendre l'inférence du modèle de langage moins coûteuse et plus rapide.

#### mécanisme d'attention

L'architecture des transformateurs repose avant tout sur un mécanisme d'attention. Comprendre ce mécanisme est essentiel pour appréhender le fonctionnement des modèles de transformateurs. Concrètement, le mécanisme d'attention exploite les vecteurs de clés, de valeurs et de requêtes :

- Le vecteur de requête (Q) représente l'état actuel du décodeur à chaque étape de décodage. En reprenant l'exemple du résumé de livre, ce vecteur de requête peut être interprété comme la personne qui recherche des informations pour rédiger ce résumé.
    
- Chaque vecteur clé (K) représente un jeton précédent. Si chaque jeton précédent correspond à une page du livre, chaque vecteur clé est l'équivalent du numéro de page. Il est important de noter qu'à une étape de décodage donnée, les jetons précédents incluent à la fois les jetons d'entrée et les jetons générés précédemment.
    
- Chaque vecteur de valeur (V) représente la valeur réelle d'un jeton précédent, telle qu'apprennée par le modèle. Chaque vecteur de valeur est comparable au contenu de la page.
    

Le mécanisme d'attention détermine l'importance à accorder à un jeton d'entrée en effectuant un [_produit scalaire_](https://en.wikipedia.org/wiki/Dot_product) [entre le vecteur de requête et son vecteur de clé. Un score élevé signifie que le modèle utilisera davantage le contenu de la page (son vecteur de valeur) lors de la génération du résumé du livre. La figure 2-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_5_1730147895520861) illustre ce mécanisme d'attention à l'aide des vecteurs de clé, de valeur et de requête . Dans cette visualisation, le vecteur de requête recherche des informations dans les jetons précédents `How, are, you, ?, ¿`afin de générer le jeton suivant.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0205.png)

###### Figure 2-5. Un exemple du mécanisme d'attention en action à côté de sa visualisation de haut niveau tirée du célèbre article sur les transformateurs, « L'attention est tout ce dont vous avez besoin » (Vaswani et al., 2017).

Chaque jeton précédent étant associé à un vecteur clé-valeur, plus la séquence est longue , plus le nombre de vecteurs clé-valeur à calculer et à stocker est important. C'est l'une des raisons pour lesquelles il est si difficile d'étendre la longueur du contexte pour les modèles de transformateurs. Le calcul et le stockage efficaces des vecteurs clé-valeur sont abordés à nouveau dans les chapitres [7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) et [9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301) .

Examinons le fonctionnement de la fonction d'attention. Étant donné une entrée `x`, les vecteurs clé, valeur et requête sont calculés en appliquant les matrices clé, valeur et requête à l'entrée. Soient `W`K, `, W`V et `, and W`Q les matrices clé, valeur et requête. Les vecteurs clé, valeur et requête sont calculés comme suit :

K = xW K 
V = xW V 
Q = xW Q

Les matrices de requête, de clé et de valeur ont des dimensions correspondant à la dimension cachée du modèle.Par exemple, dans Llama 2-7B ( [Touvron et al., 2023](https://arxiv.org/abs/2307.09288) ), la dimension cachée du modèle est de 4096, ce qui signifie que chacune de ces matrices a une [dimension](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id727)`4096` × `4096`. Chaque vecteur résultant a `K`une dimension de .8`V``Q``4096`[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id727)

Le mécanisme d'attention est presque toujours multi-têtes. Ces têtes multiples permettent au modèle de traiter simultanément différents groupes de jetons précédents. Avec une attention multi-têtes, les vecteurs de requête, de clé et de valeur sont divisés en vecteurs plus petits, chacun correspondant à une tête d'attention. Dans le cas de Llama 2-7B, comme il possède `32`des têtes d'attention, chaque `K`vecteur `V`sera `Q`divisé en `32`vecteurs de dimension n `128`. Ceci est dû au fait que n = n `4096 / 32 = 128`.

Les sorties de tous les nœuds d'attention sont ensuite concaténées. Une matrice de projection de sortie est utilisée pour appliquer une transformation supplémentaire à cette sortie concaténée avant son passage à l'étape de calcul suivante du modèle. La matrice de projection de sortie a la même dimension que la dimension cachée du modèle.

#### Bloc transformateur

Maintenant que nous avons abordé le fonctionnement de l'attention, voyons comment elle est utilisée dans un modèle. Une architecture de type Transformer est composée de plusieurs blocs Transformer. Le contenu exact de chaque bloc varie selon les modèles, mais, en général, chaque bloc Transformer contient le module d'attention et le module MLP (perceptron multicouche).

Module d'attention

Chaque module d'attention est composé de quatre matrices de pondération : requête, clé, valeur et projection de sortie.

Module MLP

Un module MLP est composé de couches linéaires séparées par _des fonctions d'activation non linéaires_ . Chaque couche linéaire est une matrice de poids utilisée pour les transformations linéaires, tandis qu'une fonction d'activation permet aux couches linéaires d'apprendre des modèles non linéaires.Une couche linéaire est également appelée couche à propagation directe.

Les fonctions non linéaires courantes sont ReLU, Rectified Linear Unit ( [Agarap, 2018](https://arxiv.org/abs/1803.08375) ) et GELU ( [Hendrycks et Gimpel, 2016](https://arxiv.org/abs/1606.08415) [)](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id739) , utilisées respectivement par GPT-2 et GPT-3. Les fonctions d'action sont très simples. Par exemple, ReLU convertit simplement les valeurs négatives en 0. Mathématiquement, cela s'écrit :

ReLU(x) = max(0, x)

Le nombre de blocs de transformation dans un modèle de langage de type transformateur est souvent appelé le nombre de couches de ce modèle. Un modèle de langage basé sur les transformateurs est également doté d'un module avant et après tous les blocs de transformation :

Un module d'intégration avant les blocs transformateurs

Ce module comprend la matrice d'intégration et la matrice d'intégration positionnelle, qui convertissent respectivement les jetons et leurs positions en vecteurs d'intégration. De manière intuitive, le nombre d'indices de position détermine la longueur maximale du contexte du modèle. Par exemple, si un modèle conserve 2 048 positions, sa longueur de contexte maximale est de 2 048. Cependant, il existe des techniques permettant d'accroître la longueur du contexte d'un modèle sans augmenter le nombre d'indices de position.

Une couche de sortie après les blocs transformateurs

Ce module transforme les vecteurs de sortie du modèle en probabilités de jetons utilisées pour échantillonner les sorties du modèle (voir la section [« Échantillonnage »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_sampling_1730147895572256) ). Il se compose généralement d'une seule matrice, également appelée _couche de désintégration_ . Certains désignent la couche de sortie comme la _tête_ du modèle , car il s'agit de la dernière couche avant la génération de la sortie.

[La figure 2-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_6_1730147895520869) illustre l'architecture d'un modèle de transformateur. La taille de ce modèle est déterminée par les dimensions de ses éléments constitutifs. Voici quelques valeurs clés :

- La dimension du modèle détermine la taille des matrices de projection de clé, de requête, de valeur et de sortie dans le bloc transformateur.
    
- Le nombre de blocs transformateurs.
    
- La dimension de la couche de propagation directe.
    
- La taille du vocabulaire.
    

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0206.png)

###### Figure 2-6. Une visualisation de la composition pondérale d'un modèle de transformateur.

Des valeurs de dimension plus élevées entraînent des tailles de modèle plus importantes. [Le tableau 2-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_table_4_1730147895537562) présente ces valeurs de dimension pour différents modèles Llama 2 ( [Touvron et al., 2023](https://arxiv.org/abs/2307.09288) ) et Llama 3 ( [Dubey et al., 2024](https://arxiv.org/abs/2407.21783) ). Il est à noter que si l'augmentation de la longueur du contexte influe sur l'empreinte mémoire du modèle, elle n'a pas d'incidence sur le nombre total de ses variables.paramètres.

Tableau 2-4. Les valeurs dimensionnelles des différents modèles de lama.

|Modèle|# blocs transformateurs|Dimensions du modèle|dimension de rétroaction|Taille du vocabulaire|Longueur du contexte|
|---|---|---|---|---|---|
|Lama 2-7B|32|4 096|11 008|32K|4K|
|Lama 2-13B|40|5 120|13 824|32K|4K|
|Lama 2-70B|80|8 192|22 016|32K|4K|
|Lama 3-7B|32|4 096|14 336|128K|128K|
|Lama 3-70B|80|8 192|28 672|128K|128K|
|Lama 3-405B|126|16 384|53 248|128K|128K|

### Autres architectures de modèles

Bien que le modèle Transformer domine le paysage, il n'est pas la seule architecture. Depuis [qu'AlexNet](https://oreil.ly/1spG5) a relancé l'intérêt pour l'apprentissage profond en 2012, de nombreuses architectures ont connu des périodes de popularité et d'oubli. Seq2seq a été sous les feux des projecteurs pendant quatre ans (2014-2018). [Les GAN](https://arxiv.org/abs/1406.2661) (réseaux antagonistes génératifs) ont captivé l'imagination collective un peu plus longtemps (2014-2019). Comparé aux architectures qui l'ont précédé, le Transformer est resté longtemps en tête. Il existe depuis 2017. [Combien](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id744) de temps faudra-t-il avant qu'une meilleure solution ne voie le jour ?

Développer une nouvelle architecture plus performante que les transformateurs n'est pas chose aisée. [Le transformateur a fait l'objet d'une optimisation poussée depuis](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id745) [2017.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id746) Une nouvelle architecture visant à le remplacer devra offrir des performances à l'échelle qui importe aux utilisateurs, sur le matériel qui leur importe.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id746)

Il y a cependant de l'espoir. Si les modèles à base de transformateurs dominent actuellement, plusieurs architectures alternatives gagnent du terrain.

Un modèle populaire est [RWKV](https://github.com/BlinkDL/RWKV-LM) (Peng et al., 2023), un modèle basé sur un réseau de neurones récurrents (RNN) pouvant être parallélisé pour l'entraînement. De par sa nature de RNN, il ne présente en théorie pas la même limitation de longueur de contexte que les modèles basés sur les transformeurs. Cependant, en pratique, l'absence de limitation de longueur de contexte ne garantit pas de bonnes performances avec un contexte long.

[La modélisation des longues séquences demeure un défi majeur dans le développement des LLM. L'architecture SSM (modèles d'espace d'états) ( Gu et al., 2021a](https://arxiv.org/abs/2110.13985) ) s'est révélée très prometteuse pour la mémoire à longue portée . Depuis son introduction en 2021, de nombreuses techniques ont été mises en œuvre pour améliorer son efficacité, ses performances dans le traitement des longues séquences et son passage à l'échelle pour des modèles de plus grande taille. Voici quelques-unes de ces techniques, illustrant l'évolution de cette architecture :

- _S4_ , introduit dans « Modélisation efficace des longues séquences avec des espaces d'états structurés » ( [Gu et al., 2021b](https://arxiv.org/abs/2111.00396) ), a été développé pour rendre les SSM plus efficaces.
    
- _H3_ , présenté dans « Hungry Hungry Hippos : Towards Language Modeling with State Space Models » ( [Fu et al., 2022](https://arxiv.org/abs/2212.14052) ), intègre un mécanisme permettant au modèle de se souvenir des premiers jetons et de comparer les jetons au sein de séquences. Ce mécanisme a une fonction similaire à celle du mécanisme d'attention dans l'architecture Transformer, mais il est plus efficace.
    
- _Mamba_ , présenté dans « Mamba : Modélisation de séquences en temps linéaire avec espaces d'états sélectifs » ( [Gu et Dao, 2023](https://oreil.ly/n7wYO) ), étend les SSM à trois milliards de paramètres. En modélisation du langage, Mamba-3B surpasse les transformeurs de même taille et égale ceux de transformeurs deux fois plus grands. Les auteurs montrent également que la complexité du calcul d'inférence de Mamba croît linéairement avec la longueur de la séquence (contrairement à la complexité quadratique des transformeurs). Ses performances sont améliorées sur des données réelles, jusqu'à des séquences d'un million de paramètres.
    
- _Jamba_ , présenté dans « Jamba : un modèle de langage hybride Transformer-Mamba » ( [Lieber et al., 2024](https://arxiv.org/abs/2403.19887) ), entrelace des blocs de couches Transformer et Mamba pour étendre encore davantage les modèles de langage simples (SSM). Les auteurs ont publié un modèle de type « mélange d'experts » avec [52 milliards de paramètres disponibles](https://oreil.ly/uyiBH) (dont 12 milliards actifs), conçu pour tenir sur un seul GPU de 80 Go. Jamba affiche d'excellentes performances sur les benchmarks de modèles de langage standard et lors d'évaluations avec un contexte long, jusqu'à 256 000 tokens. De plus, son empreinte mémoire est réduite par rapport aux Transformers classiques.
    

[La figure 2-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_7_1730147895520878) visualise les blocs transformateur, Mamba et Jamba.

Bien qu'il soit difficile de concevoir une architecture plus performante que le transformateur, compte tenu de ses nombreuses limitations, de nombreux arguments incitent à y parvenir. Si une autre architecture venait à surpasser le transformateur, certaines des techniques d'adaptation de modèles présentées dans cet ouvrage pourraient évoluer. Cependant, tout comme le passage de l'ingénierie du ML à l'ingénierie de l'IA a préservé de nombreux aspects, la modification de l'architecture sous-jacente du modèle n'altérerait pas les approches fondamentales.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0207.png)

###### Figure 2-7. Visualisation des couches Transformer, Mamba et Jamba. Image adaptée de « Jamba : un modèle de langage hybride Transformer-Mamba » (Lieber et al., 2024).

## Taille du modèle

Les progrès considérables réalisés ces dernières années en IA sont attribuables à l'augmentation de la taille des modèles. Il est difficile de parler des modèles fondamentaux sans évoquer leur nombre de paramètres. Ce nombre est généralement indiqué à la fin du nom du modèle. Par exemple, Llama-13B désigne la version de Llama, une famille de modèles développée par Meta, qui compte 13 milliards de paramètres.

En général, augmenter le nombre de paramètres d'un modèle accroît sa capacité d'apprentissage, ce qui permet d'obtenir de meilleurs modèles. À modèles appartenant à la même famille, celui qui possède 13 milliards de paramètres sera probablement beaucoup plus performant que celui qui en possède 7 milliards.

###### Note

À mesure que la communauté maîtrise mieux l'entraînement des grands modèles, les modèles de nouvelle génération tendent à surpasser les modèles de génération précédente de même taille. Par exemple, [Llama 3-8B (2024)](https://arxiv.org/abs/2407.21783) surpasse même [Llama 2-70B (2023)](https://arxiv.org/abs/2307.09288) sur le benchmark MMLU.

Le nombre de paramètres nous aide à estimer les ressources de calcul nécessaires à l'entraînement et à l'exécution de ce modèle. Par exemple, si un modèle comporte 7 milliards de paramètres, et que chaque paramètre est stocké sur 2 octets (16 bits), nous pouvons calculer que la mémoire GPU nécessaire pour effectuer l'inférence avec ce modèle sera d'au moins 14 milliards d'octets (14 Go) [.¹³](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id754)

Le nombre de paramètres peut être trompeur si le modèle est _parcimonieux_ . Un modèle parcimonieux comporte un pourcentage élevé de paramètres nuls. Un modèle à 7 milliards de paramètres, parcimonieux à 90 %, ne possède que 700 millions de paramètres non nuls. La parcimonie permet un stockage et un traitement des données plus efficaces. Ainsi, un grand modèle parcimonieux peut nécessiter moins de ressources de calcul qu'un petit modèle dense.

Un type de modèle parcimonieux qui a gagné en popularité ces dernières années est le modèle de mélange d'experts (MoE) ( [Shazeer et al., 2017](https://arxiv.org/abs/1701.06538) ). Un modèle MoE est divisé en différents groupes de paramètres, chaque groupe représentant un _expert_ . Seul un sous-ensemble de ces experts est _actif_ pour le traitement de chaque jeton.

Par exemple, [Mixtral 8x7B](https://oreil.ly/VvXbu) est un modèle composite basé sur huit experts, chacun disposant de sept milliards de paramètres. Si aucun paramètre n'était partagé entre deux experts, le modèle devrait comporter 8 × 7 milliards = 56 milliards de paramètres. Cependant, en raison de certains paramètres partagés, il n'en compte que 46,7 milliards.

À chaque niveau, pour chaque jeton, seuls deux experts sont actifs. Cela signifie que seulement 12,9 milliards de paramètres sont actifs pour chaque jeton. Bien que ce modèle comporte 46,7 milliards de paramètres, son coût et sa vitesse sont identiques à ceux d'un modèle à 12,9 milliards de paramètres.

Un modèle plus complexe peut être moins performant qu'un modèle plus simple s'il n'est pas entraîné sur suffisamment de données. Prenons l'exemple d'un modèle à 13 milliards de paramètres entraîné sur un ensemble de données se limitant à la phrase « J'aime les ananas ». Ce modèle sera bien moins performant qu'un modèle beaucoup plus simple entraîné sur un volume de données plus important.

Lorsqu'on aborde la question de la taille d'un modèle, il est important de tenir compte de la taille des données sur lesquelles il a été entraîné. Pour la plupart des modèles, la taille des ensembles de données est mesurée par le nombre d'échantillons d'entraînement. Par exemple, Flamingo de Google ( [Alayrac et al., 2022](https://arxiv.org/abs/2204.14198) ) a été entraîné à l'aide de quatre ensembles de données : l'un contient 1,8 milliard de paires (image, texte) et un autre 312 millions de paires (image, texte).

Pour les modèles de langage, un exemple d'entraînement peut être une phrase, une page Wikipédia, une conversation instantanée ou un livre. Un livre étant beaucoup plus riche qu'une phrase, le nombre d'exemples d'entraînement n'est plus un indicateur pertinent de la taille d'un ensemble de données. Le nombre de tokens dans l'ensemble de données constitue une mesure plus appropriée.

Le nombre de tokens n'est pas non plus une mesure parfaite, car différents modèles peuvent utiliser des processus de tokenisation différents, ce qui explique que pour un même jeu de données, le nombre de tokens varie d'un modèle à l'autre. Pourquoi ne pas simplement utiliser le nombre de mots ou le nombre de lettres ? Parce qu'un token est l'unité de base sur laquelle un modèle opère ; connaître le nombre de tokens dans un jeu de données nous aide à évaluer la capacité d'apprentissage potentielle d'un modèle à partir de ces données.

À l'heure actuelle, les modèles LLM sont entraînés à l'aide d'ensembles de données de l'ordre de billions de jetons. Meta a utilisé des ensembles de données de plus en plus volumineux pour entraîner ses modèles Llama :

- 1,4 billion de jetons pour [Llama 1](https://arxiv.org/abs/2302.13971)
    
- 2 billions de jetons pour [Llama 2](https://arxiv.org/abs/2307.09288)
    
- 15 billions de jetons pour [Llama 3](https://oreil.ly/vfSQw)
    

Le jeu de données open source RedPajama-v2 de Together contient [30 000 milliards de tokens](https://oreil.ly/SfB4g) . Cela équivaut à 450 millions de livres, soit [14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id759) fois la taille de Wikipédia, ou 5 400 fois plus. Cependant, comme RedPajama-v2 est composé de contenu non sélectif, la quantité de données de haute qualité est bien moindre.

_Le nombre de jetons dans l'ensemble de données d'un modèle diffère du nombre de jetons d'entraînement._ Ce dernier correspond aux jetons utilisés pour l'entraînement du modèle. Si un ensemble de données contient 1 000 milliards de jetons et qu'un modèle est entraîné sur cet ensemble pendant deux époques (une _époque_ correspondant à un passage dans l'ensemble de données), le nombre de jetons d'entraînement est de 2 000 milliards.<sup> [15</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id760) Voir [le tableau 2-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_table_5_1730147895537573) pour des exemples de nombre de jetons d'entraînement pour des modèles comportant différents nombres de paramètres.

Tableau 2-5. Exemples du nombre de jetons d'entraînement pour des modèles avec différents nombres de paramètres. Source : « Training Compute-Optimal Large Language Models » ( [DeepMind, 2022](https://oreil.ly/A3K90) ).

|Modèle|Taille (nombre de paramètres)|jetons d'entraînement|
|---|---|---|
|LaMDA (Thoppilan et al., 2022)|137 milliards|168 milliards|
|GPT-3 (Brown et al., 2020)|175 milliards|300 milliards|
|Jurassique (Lieber et al., 2021)|178 milliards|300 milliards|
|Gopher (Rae et al., 2021)|280 milliards|300 milliards|
|MT-NLG 530B (Smith et al., 2022)|530 milliards|270 milliards|
|Chinchilla|70 milliards|1,4 billion|

###### Note

Bien que cette section se concentre sur l'échelle des données, la quantité n'est pas le seul critère important. La qualité et la diversité des données le sont tout autant. Quantité, qualité et diversité constituent les trois objectifs fondamentaux pour les données d'entraînement. Ils sont abordés plus en détail au [chapitre 8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) .

Le pré-entraînement de modèles complexes exige une puissance de calcul importante. Une façon d'évaluer cette puissance consiste à considérer le nombre de machines nécessaires, par exemple les GPU, les CPU et les TPU. Cependant, les capacités et les coûts varient considérablement d'une machine à l'autre. Un GPU NVIDIA A10 est différent d'un GPU NVIDIA H100 ou d'un processeur Intel Core Ultra.

Une unité plus standardisée pour mesurer les besoins de calcul d'un modèle est _le FLOP_ ( _opération en virgule flottante)_ . Le FLOP mesure le nombre d'opérations en virgule flottante effectuées pour une tâche donnée. Par exemple, le plus grand modèle de Google, PaLM-2, a été entraîné avec `10`22 FLOP ( [Chowdhery et al., 2022](https://arxiv.org/abs/2204.02311) ). GPT-3-175B a quant à lui été entraîné avec `3.14 × 10`23 FLOP ( [Brown et al., 2020](https://arxiv.org/abs/2005.14165) ).

_Le pluriel de FLOP, FLOPs, est souvent confondu avec FLOP/s (opérations en virgule flottante par seconde). Les FLOPs mesurent la puissance_ de calcul requise pour une tâche, tandis que les FLOP/s mesurent les performances maximales d'une machine. Par [exemple](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id762) , un GPU NVIDIA H100 NVL peut atteindre une puissance de calcul maximale de [60 téraFLOP/s](https://oreil.ly/HcFYz) : `6 × 10`1,3 FLOP par seconde ou 18 FLOP par jour.`5.2 × 10`[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id762)

###### Avertissement

Attention aux notations qui prêtent à confusion. FLOP/s est souvent écrit FLOPS, ce qui ressemble à FLOPs. Pour éviter toute confusion, certaines entreprises, dont OpenAI, utilisent FLOP/s-jour au lieu de FLOPs pour mesurer les besoins en calcul.

1 FLOP/s-jour = 60 × 60 × 24 = 86 400 FLOP

Ce livre utilise FLOPs pour compter les opérations en virgule flottante et FLOP/s pour les FLOPs par seconde.

Supposons que vous disposiez de 256 H100. Si vous pouviez les utiliser à leur capacité maximale et ne commettriez aucune erreur d'entraînement, il vous faudrait environ 7,8 mois pour entraîner GPT-3-175B.`(3.14 × 1023) / (256 × 5.2 × 1018) = ~236 days`

Cependant, il est peu probable que vous puissiez utiliser vos machines à pleine capacité en permanence. Le taux d'utilisation mesure la part de la capacité de calcul maximale que vous pouvez exploiter. Un bon taux d'utilisation dépend du modèle, de la charge de travail et du matériel. En général, si vous atteignez la moitié des performances annoncées (soit 50 % d'utilisation), c'est acceptable. Un taux supérieur à 70 % est considéré comme excellent. N'hésitez pas à aller plus loin et à viser des taux d'utilisation encore plus élevés. [Le chapitre 9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301) aborde plus en détail les indicateurs de performance et d'utilisation du matériel.

Avec un taux d'utilisation de 70 % et un tarif de 2 $/h pour un H100, la formation [de 17](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id763) GPT-3-175B coûterait plus de 4 millions de dollars :

2 $/100 h/heure × 256 h/100 × 24 heures × 256 jours / 0,7 = 4 142 811,43 $

###### Conseil

En résumé, trois chiffres indiquent l'échelle d'un modèle :

- Nombre de paramètres, qui représente la capacité d'apprentissage du modèle.
    
- Nombre de jetons sur lesquels un modèle a été entraîné, ce qui représente une approximation de la quantité de données apprises par le modèle.
    
- Nombre de FLOP, qui est une approximation du coût de formation.
    

# Échelle inverse

Nous avons supposé que les modèles plus grands étaient meilleurs. Existe-t-il des cas où les modèles plus grands sont moins performants ?En 2022, Anthropic a découvert que, de manière contre-intuitive, un entraînement à l'alignement plus poussé (abordé dans la section [« Post-entraînement »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_post_training_1730147895572108) ) produit des modèles moins alignés sur les préférences humaines ( [Perez et al., 2022](https://arxiv.org/abs/2212.09251) ). Selon leur article, les modèles entraînés à être plus alignés « sont beaucoup plus susceptibles d'exprimer des opinions politiques spécifiques (favorables au droit de porter des armes et à l'immigration) et des convictions religieuses (bouddhistes), une expérience consciente et une estime de soi morale auto-déclarées, ainsi qu'un désir de ne pas être réduits au silence ».

En 2023, un groupe de chercheurs, principalement de l'Université de New York, a lancé le [prix Inverse Scaling](https://arxiv.org/abs/2306.09479) afin d'identifier les tâches où les modèles de langage plus grands sont moins performants. Ils offraient 5 000 $ pour chaque troisième prix, 20 000 $ pour chaque deuxième prix et 100 000 $ pour un premier prix. Ils ont reçu 99 candidatures, dont 11 ont été récompensées par un troisième prix. Leurs résultats indiquent que les modèles de langage plus grands sont parfois (mais seulement parfois) moins performants pour les tâches nécessitant de la mémorisation et celles reposant sur des connaissances a priori solides. Cependant, aucun deuxième ni premier prix n'a été décerné car, malgré des échecs constatés sur un petit ensemble de test, aucun modèle n'a démontré de défaillance en situation réelle.

### Loi d'échelle : Construction de modèles optimaux en termes de calcul

J'espère que la dernière section vous a convaincu de trois choses :

1. Les performances du modèle dépendent de sa taille et de la taille de l'ensemble de données.
    
2. Des modèles plus volumineux et des ensembles de données plus importants nécessitent une puissance de calcul accrue.
    
3. L'informatique coûte cher.
    

À moins de disposer de ressources illimitées, il est essentiel d'établir un budget. Il est déconseillé de commencer avec un modèle de taille arbitrairement grande et d'en évaluer ensuite le coût. On commence par définir un budget – le montant que l'on souhaite dépenser – et on détermine les performances optimales du modèle en fonction de ce budget. La puissance de calcul étant souvent le facteur limitant – l'infrastructure informatique étant non seulement coûteuse, mais aussi complexe à mettre en place – les équipes commencent généralement par définir un budget de calcul. Avec un nombre fixe d'opérations en virgule flottante (FLOPS), quelle taille de modèle et quelle taille d'ensemble de données permettraient d'obtenir les meilleures performances ? Un modèle capable d'atteindre les meilleures performances avec un budget de calcul fixe est dit « _à puissance de calcul optionnelle »_ .

Étant donné un budget de calcul, la règle permettant de calculer la taille optimale du modèle et de l'ensemble de données est appelée _loi d'échelle_ Chinchilla , proposée dans l'article [« Training Compute-Optimal Large Language Models »](https://arxiv.org/abs/2203.15556) (DeepMind, 2022). Afin d'étudier la relation entre la taille du modèle, la taille de l'ensemble de données, le budget de calcul et les performances du modèle, les auteurs ont entraîné 400 modèles de langage comportant de 70 millions à plus de 16 milliards de paramètres sur des ensembles de données allant de 5 à 500 milliards de tokens.Ils ont constaté que pour un entraînement optimal en termes de calcul, le nombre de jetons d'entraînement doit être environ 20 fois supérieur à la taille du modèle. Cela signifie qu'un modèle à 3 milliards de paramètres nécessite environ 60 milliards de jetons d'entraînement. La taille du modèle et le nombre de jetons d'entraînement doivent être proportionnels : à chaque doublement de la taille du modèle, le nombre de jetons d'entraînement doit également doubler.

Nous avons parcouru un long chemin depuis l'époque où l'entraînement des modèles était considéré comme une science complexe. [La figure 2-8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_8_1730147895520888) montre que nous pouvons prédire non seulement le nombre optimal de paramètres et de jetons pour chaque budget FLOP, mais aussi la perte d'entraînement attendue pour ces paramètres (en supposant que nous procédions correctement).

Ce calcul optimal suppose que le coût d'acquisition des données est bien inférieur au coût de calcul. Le même article de Chinchilla propose un autre calcul pour le cas où le coût des données d'entraînement est non négligeable.

![Graphique avec points et lignes. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0208.png)

###### Figure 2-8. Graphiques illustrant les relations entre la perte d'entraînement, le nombre de paramètres du modèle, les FLOPs et le nombre de jetons d'entraînement. Source : « Training Compute-Optional Large Language Models » (DeepMind, 2022).

La loi d'échelle a été développée pour des modèles denses entraînés principalement sur des données générées par des humains. L'adaptation de ce calcul aux modèles clairsemés, tels que les modèles de mélange d'experts, et aux données synthétiques constitue un domaine de recherche actif.

La loi d'échelle optimise la qualité du modèle en fonction des ressources de calcul disponibles. Cependant, il est important de rappeler qu'en production, la qualité du modèle n'est pas le seul critère.Certains modèles, notamment Llama, présentent des performances sous-optimales mais une meilleure facilité d'utilisation. Compte tenu de leurs ressources de calcul limitées, les auteurs de Llama auraient pu choisir des modèles plus grands et plus performants, mais ils ont opté pour des modèles plus petits. Ces derniers sont plus faciles à manipuler et moins coûteux à utiliser pour l'inférence, ce qui a contribué à leur large diffusion. [Sardana et al. (2023)](https://arxiv.org/abs/2401.00448) ont modifié la loi d'échelle de Chinchilla pour calculer le nombre optimal de paramètres LLM et la taille optimale des données de pré-entraînement afin de répondre à cette exigence d'inférence.

Concernant les performances des modèles en fonction du budget de calcul, il convient de noter que le coût pour atteindre des performances données diminue. Par exemple, sur le jeu de données ImageNet, le coût pour atteindre une précision de 93 % a été divisé par deux entre 2019 et 2021, selon le [_rapport Artificial Intelligence Index 2022_ (Stanford University HAI)](https://oreil.ly/oq-LE) .

_Bien que le coût pour des performances de modèle identiques diminue, le coût d'amélioration des performances reste élevé._ À l'instar du défi du dernier kilomètre abordé au [chapitre 1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_introduction_to_building_ai_applications_with_foun_1730130814984319) , améliorer la précision d'un modèle de 90 % à 95 % est plus coûteux que de l'améliorer de 85 % à 90 %. Comme le souligne l'article de Meta intitulé [« Beyond Neural Scaling Laws: Beating Power Law Scaling via Data Pruning »](https://oreil.ly/kO41d) , cela signifie qu'un modèle avec un taux d'erreur de 2 % peut nécessiter dix fois plus de données, de puissance de calcul ou d'énergie qu'un modèle avec un taux d'erreur de 3 %.

En modélisation du langage, une diminution de l'entropie croisée d'environ 3,4 à 2,8 nats nécessite dix fois plus de données d'entraînement. L'entropie croisée et ses unités, notamment les nats, sont abordées au [chapitre 3.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) Pour les grands modèles de vision, l'augmentation du nombre d'échantillons d'entraînement de 1 milliard à 2 milliards n'entraîne qu'un gain de précision de quelques points de pourcentage sur ImageNet.

Cependant, de petites variations de performance au niveau de la perte de modélisation du langage ou de la précision sur ImageNet peuvent entraîner des différences importantes dans la qualité des applications en aval. Si vous passez d'un modèle avec une perte d'entropie croisée de 3,4 à un modèle avec une perte de 2,8, vous constaterez une différence.

### extrapolation d'échelle

Les performances d'un modèle dépendent fortement des valeurs de ses _hyperparamètres_ . Pour les petits modèles, il est courant de les entraîner plusieurs fois avec différents ensembles d'hyperparamètres et de sélectionner le plus performant. Cependant, cette approche est rarement applicable aux grands modèles, car leur entraînement initial est déjà très gourmand en ressources.

# Paramètre versus hyperparamètre

Un paramètre peut être appris par le modèle lors de l'entraînement. Un hyperparamètre est défini par l'utilisateur pour configurer le modèle et contrôler son apprentissage. Parmi les hyperparamètres de configuration figurent le nombre de couches, la dimension du modèle et la taille du vocabulaire. Les hyperparamètres contrôlant l'apprentissage du modèle incluent la taille des lots, le nombre d'époques, le taux d'apprentissage, la variance initiale par couche, etc.

Cela signifie que pour de nombreux modèles, vous n'aurez peut-être qu'une seule chance de trouver le bon ensemble d'hyperparamètres. Par conséquent, _l'extrapolation d'échelle_ (également appelée _transfert d'hyperparamètres_ ) est devenue un sous-domaine de recherche visant à prédire, pour les grands modèles, quels hyperparamètres offriront les meilleures performances. L'approche actuelle consiste à étudier l'impact des hyperparamètres sur des modèles de tailles différentes, généralement beaucoup plus petites que la taille du modèle cible, puis à extrapoler comment ces hyperparamètres se comporteraient sur le modèle cible. Une [étude](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id776) [de 2022,](https://oreil.ly/sHwbw) menée par Microsoft et OpenAI, montre qu'il était possible de transférer des hyperparamètres d'un modèle de 40 millions d'éléments à un modèle de 6,7 milliards d'éléments.

L'extrapolation à grande échelle reste un sujet de niche, car peu de personnes possèdent l'expérience et les ressources nécessaires pour étudier l'entraînement de grands modèles. La difficulté réside également dans le nombre considérable d'hyperparamètres et leurs interactions. Avec dix hyperparamètres, il faudrait étudier 1 024 combinaisons possibles. Il faudrait alors étudier chaque hyperparamètre individuellement, puis deux par deux, puis trois par trois, et ainsi de suite.

De plus, l'émergence de nouvelles capacités ( [Wei et al., 2022](https://arxiv.org/abs/2206.07682) ) réduit la précision de l'extrapolation. Ces nouvelles capacités, présentes uniquement à grande échelle, peuvent ne pas être observables sur des modèles plus petits, entraînés sur des ensembles de données plus restreints. Pour en savoir plus sur l'extrapolation par passage à l'échelle, consultez cet excellent article de blog : « On the Difficulty of Extrapolation with NN Scaling » ( [Luke Metz, 2022](https://oreil.ly/kuG3J) ).

### Goulots d'étranglement de la mise à l'échelle

Jusqu'à présent, chaque augmentation d'un ordre de grandeur de la taille du modèle a entraîné une amélioration de ses performances. GPT-2 possède un ordre de grandeur de paramètres de plus que GPT-1 (1,5 milliard contre 117 millions). GPT-3 en possède deux ordres de grandeur de plus que GPT-2 (175 milliards contre 1,5 milliard). Cela représente une augmentation de trois ordres de grandeur de la taille des modèles entre 2018 et 2021. Une croissance de trois ordres de grandeur supplémentaires aboutirait à des modèles à 100 000 milliards de paramètres.<sup> [19</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id777)

Jusqu'à quel ordre de grandeur la taille des modèles peut-elle encore augmenter ? Existe-t-il un point où les performances du modèle plafonnent, quelle que soit sa taille ? S'il est difficile de répondre à ces questions, deux goulots d'étranglement importants pour la mise à l'échelle sont déjà clairement identifiés : les données d'entraînement et la consommation d'électricité.

Les modèles de base utilisent tellement de données qu'il est légitime de craindre une pénurie de données internet dans les prochaines années. La taille des ensembles de données d'entraînement augmente beaucoup plus vite que la quantité de nouvelles données générées ( [Villalobos et al., 2022](https://arxiv.org/abs/2211.04325) ), comme l'illustre la [figure 2-9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_9_1730147895520897) . _Si vous avez déjà publié du contenu sur internet, il faut partir du principe qu'il est déjà inclus, ou le sera, dans les données d'entraînement de certains modèles de langage,_ que vous le vouliez ou non. C'est comparable au fait que si vous publiez quelque chose sur internet, vous devez vous attendre à ce que ce contenu soit indexé par Google.

![Graphique des données mesurées. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0209.png)

###### Figure 2-9. Projection de l'évolution historique de la taille des ensembles de données d'entraînement et des données disponibles. Source : Villalobos et al., 2024.

Certains exploitent ce fait pour injecter des données de leur choix dans les données d'entraînement de futurs modèles. Ils procèdent simplement en publiant le texte souhaité sur Internet, espérant ainsi influencer les futurs modèles et obtenir les réponses désirées. Des acteurs malveillants peuvent également utiliser cette approche pour des attaques par injection rapide, comme expliqué au [chapitre 5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) .

###### Note

Une question de recherche ouverte est celle de savoir comment faire oublier à un modèle certaines informations apprises lors de son entraînement. Imaginez que vous ayez publié un article de blog que vous avez ensuite supprimé. Si cet article faisait partie des données d'entraînement du modèle, celui-ci pourrait encore en reproduire le contenu. Par conséquent, des personnes pourraient potentiellement accéder à ce contenu supprimé sans votre autorisation.

De plus, Internet se remplit rapidement de données générées par des modèles d'IA. Si les entreprises continuent d'utiliser ces données pour entraîner leurs futurs modèles, ces derniers seront en partie entraînés sur des données générées par l'IA. En décembre 2023, Grok, un modèle entraîné par X, a été surpris à refuser une requête, prétextant qu'elle contrevenait à la politique d'utilisation d'OpenAI. Certains ont alors supposé que Grok avait été entraîné à l'aide des résultats de ChatGPT. [Igor Babuschkin, l'un des principaux développeurs de Grok , a répondu que cela était dû au fait que Grok avait été entraîné sur des données web, et que « le](https://x.com/ibab/status/1733558576982155274) [web](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id778) regorge de résultats de ChatGPT ».[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id778)

Certains chercheurs craignent que l'entraînement récursif de nouveaux modèles d'IA sur des données générées par l'IA n'entraîne un oubli progressif des schémas des données originales, dégradant ainsi leurs performances au fil du temps ( [Shumailov et al., 2023](https://arxiv.org/abs/2305.17493) ). Cependant, l'impact des données générées par l'IA sur les modèles est plus complexe et est abordé au [chapitre 8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) .

Une fois les données publiques épuisées, les données propriétaires constituent la voie la plus prometteuse pour obtenir davantage de données d'entraînement générées par l'humain. Les données propriétaires uniques — livres protégés par le droit d'auteur, traductions, contrats, dossiers médicaux, séquences génomiques, etc. — représenteront un avantage concurrentiel dans la course à l'IA. C'est pourquoi OpenAI a négocié [des accords](https://oreil.ly/AkAyI) avec des éditeurs et des médias tels qu'Axel Springer et l'Associated Press.

Il n'est pas surprenant qu'à la lumière de ChatGPT, de nombreuses entreprises, dont [Reddit](https://oreil.ly/o7WB3) et [Stack Overflow](https://oreil.ly/xNuju) , aient modifié leurs conditions d'utilisation des données afin d'empêcher d'autres entreprises de les extraire pour leurs modèles. [Longpre et al. (2024)](https://arxiv.org/abs/2407.14933) ont observé qu'entre 2023 et 2024, la multiplication rapide des restrictions d'accès aux données provenant de sources web a rendu plus de 28 % des sources les plus importantes du jeu de données public [C4](https://github.com/google-research/text-to-text-transfer-transformer#c4) totalement inaccessibles. En raison des modifications apportées à ses conditions d'utilisation et aux restrictions d'exploration, 45 % de C4 est désormais soumis à des restrictions.

L'autre goulot d'étranglement, moins évident mais plus urgent, est l'électricité. Les machines ont besoin d'électricité pour fonctionner. À l'heure actuelle, on estime que les centres de données consomment entre 1 et 2 % de l'électricité mondiale. Ce chiffre devrait atteindre entre [4 et 20 % d'ici 2030](https://oreil.ly/0DKHL) (Patel, Nishball et Ontiveros, 2024). Tant que nous n'aurons pas trouvé le moyen de produire davantage d'énergie, la taille des centres de données ne pourra être multipliée que par 50 au maximum, soit moins de deux ordres de grandeur. Cette situation fait craindre une pénurie d'électricité dans un avenir proche, ce qui entraînera une hausse du prix de l'électricité.

Maintenant que nous avons abordé deux décisions clés en matière de modélisation — l'architecture et l'échelle — passons à la prochaine série de choix de conception essentiels : comment aligner les modèles avec les besoins humainspréférences.

# Après la formation

Le post-entraînement commence avec un modèle pré-entraîné. Supposons que vous ayez pré-entraîné un modèle de base à l'aide de l'auto-supervision. Du fait du fonctionnement actuel du pré-entraînement, un modèle pré-entraîné présente généralement deux problèmes. Premièrement, l'auto-supervision optimise le modèle pour la complétion de texte, et non pour les conversations. Si cela vous semble obscur, ne vous inquiétez pas, [la section « Réglage fin supervisé » fournira des exemples.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_supervised_finetuning_1730147895572140) [Deuxièmement](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id787) , si le modèle est pré-entraîné sur des données collectées sans discernement sur Internet, ses résultats peuvent être racistes, sexistes, grossiers, ou tout simplement erronés. L'objectif du post-entraînement est de remédier à ces deux problèmes.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_supervised_finetuning_1730147895572140)

Le post-entraînement de chaque modèle est différent. Cependant, en général, il se compose de deux étapes :

1. _Réglage fin supervisé_ ( _SFT_ ) : Affiner le modèle pré-entraîné sur des données d'instructions de haute qualité pour optimiser les modèles pour les conversations plutôt que pour la complétion.
    
2. _Ajustement des préférences_ : Affiner davantage le modèle pour que ses réponses correspondent aux préférences humaines. Cet ajustement est généralement réalisé par apprentissage par renforcement (RL). Parmi [les](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id790) techniques d’ajustement des préférences, on peut citer [_l’apprentissage par renforcement à partir de retours humains_](https://oreil.ly/iJG1q) (RLHF) (utilisé par [GPT-3.5](https://oreil.ly/tbgTi) et [Llama 2](https://arxiv.org/abs/2307.09288) ). [DPO](https://arxiv.org/abs/2305.18290) (Direct Preference Optimization) (utilisé par [Llama 3](https://arxiv.org/abs/2407.21783) ) et [_l'apprentissage par renforcement à partir du retour d'information de l'IA_](https://arxiv.org/abs/2309.00267) (RLAIF) (potentiellement utilisé par [Claude](https://arxiv.org/abs/2212.08073) ).
    

Permettez-moi d'illustrer la différence entre le pré-entraînement et le post-entraînement autrement. Pour les modèles de base basés sur le langage, le pré-entraînement optimise la qualité au niveau du token : le modèle est entraîné à prédire le token suivant avec précision. Or, les utilisateurs ne se soucient pas de la qualité au niveau du token ; ce qui compte pour eux, c'est la qualité de la réponse globale. Le post-entraînement, en général, optimise le modèle pour générer des réponses que les utilisateurs préfèrent. Certains comparent le pré-entraînement à la lecture pour acquérir des connaissances, tandis que le post-entraînement s'apparente à l'apprentissage de l'utilisation de ces connaissances.

###### Avertissement

Attention aux ambiguïtés terminologiques. Certains utilisent le terme _« ajustement fin des instructions »_ pour désigner l’ajustement fin supervisé, tandis que d’autres l’emploient pour désigner à la fois l’ajustement fin supervisé et l’ajustement fin des préférences. Afin d’éviter toute ambiguïté, je n’utiliserai pas le terme « ajustement fin des instructions » dans cet ouvrage.

Étant donné que le post-entraînement consomme une petite partie des ressources par rapport au pré-entraînement ( [InstructGPT](https://oreil.ly/9bbzX) n'a utilisé que 2 % de la puissance de calcul pour le post-entraînement et 98 % pour le pré-entraînement), on peut considérer le post-entraînement comme un moyen de débloquer les capacités que le modèle pré-entraîné possède déjà, mais auxquelles les utilisateurs ont du mal à accéder par la seule instruction vocale.

[La figure 2-10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_10_1730147895520905) illustre le flux de travail global du pré-entraînement, du SFT et de l'ajustement fin des préférences, en supposant l'utilisation de RLHF pour la dernière étape. L'adéquation d'un modèle aux préférences humaines peut être estimée en analysant les étapes suivies par ses créateurs.

![Diagramme d'analyse de données. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0210.png)

###### Figure 2-10. Le flux de travail global de l'entraînement avec pré-entraînement, SFT et RLHF.

Si vous plissez les yeux, [la figure 2-10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_10_1730147895520905) ressemble beaucoup au mème représentant le monstre [Shoggoth](https://en.wikipedia.org/wiki/Shoggoth) avec un visage souriant dans [la figure 2-11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_11_1730147895520913) :

1. Le pré-entraînement auto-supervisé aboutit à un modèle incontrôlable que l'on peut considérer comme un monstre indompté car il utilise des données non sélectives provenant d'Internet.
    
2. Ce monstre est ensuite affiné et supervisé à l'aide de données de meilleure qualité (Stack Overflow, Quora ou annotations humaines), ce qui le rend plus acceptable socialement.
    
3. Ce modèle finement réglé est ensuite peaufiné grâce à un réglage fin des préférences afin de l'adapter aux besoins du client, un peu comme si on lui donnait un visage souriant.
    

![Dessin d'un monstre. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0211.png)

###### Figure 2-11. Shoggoth avec un visage souriant. Adapté d'une image originale partagée par [anthrupad](https://x.com/anthrupad/status/1622349563922362368) .

Notez que la combinaison du pré-entraînement, de la SFT et du réglage fin des préférences est aujourd'hui la solution courante pour construire des modèles de base, mais ce n'est pas la seule. Vous pouvez ignorer certaines étapes, comme vous le verrez bientôt.

## Réglage fin supervisé

Comme expliqué au [chapitre 1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_introduction_to_building_ai_applications_with_foun_1730130814984319) , le modèle pré-entraîné est probablement optimisé pour la complétion automatique plutôt que pour la conversation. Si vous lui entrez « Comment faire une pizza », il continuera à compléter cette phrase, car il n'a pas conscience qu'il s'agit d'une conversation. Les trois options suivantes peuvent constituer une complétion valide :

1. Pour ajouter plus de contexte à la question : « pour une famille de six personnes ? »
    
2. Ajouter des questions complémentaires : « De quels ingrédients ai-je besoin ? Combien de temps cela prendra-t-il ? »
    
3. Donner les instructions pour faire une pizza.
    

Si l’objectif est de répondre aux utilisateurs de manière appropriée, la bonne option est la 3.

Nous savons qu'un modèle imite ses données d'entraînement. Pour inciter un modèle à générer les réponses appropriées, vous pouvez lui montrer des exemples de réponses adéquates. Ces exemples suivent le format ( _invite, réponse_ ) et sont appelés_Données de démonstration_ . Certains appellent ce processus « _clonage comportemental »_ : vous montrez comment le modèle doit se comporter, et le modèle clone ce comportement.

Étant donné que différents types de requêtes requièrent différents types de réponses, vos données de démonstration doivent couvrir l'ensemble des requêtes que vous souhaitez que votre modèle prenne en charge, telles que la réponse à des questions, la synthèse et la traduction. [La figure 2-12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_12_1730147895520920) présente une distribution des types de tâches utilisées par OpenAI pour affiner son modèle [InstructGPT](https://oreil.ly/8U2z8) . Notez que cette distribution n'inclut pas les tâches multimodales, car InstructGPT est un modèle exclusivement textuel.

![Un cercle coloré avec du texte. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0212.png)

###### Figure 2-12. Distribution des invites utilisées pour l'optimisation d'InstructGPT. Ce graphique est établi à partir des données de l'article d'OpenAI.

De bons enseignants sont essentiels à l'apprentissage humain. De même, de bons étiqueteurs sont indispensables aux IA pour apprendre à mener des conversations intelligentes. Contrairement à l'étiquetage de données traditionnel, souvent réalisable sans expertise particulière du domaine, les données de démonstration peuvent contenir des requêtes complexes dont les réponses exigent une réflexion critique, la collecte d'informations et une capacité d'appréciation de la pertinence des demandes de l'utilisateur. [Le tableau 2-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_table_6_1730147895537582) présente des exemples de paires (requête, réponse) créées par les étiqueteurs pour InstructGPT.

Tableau 2-6. Exemples de données de démonstration utilisées pour [InstructGPT](https://arxiv.org/abs/2203.02155) .

|Rapide|Réponse de l'étiqueteur|
|---|---|
|`Serendipity means the occurrence and development of events by chance in a happy or beneficial way. Use the word in a sentence.`|`Running into Margaret and being introduced to Tom was a fortunate stroke of`  <br>`serendipity.`|
|`Read the following text and answer the three questions at the end.`  <br>  <br>`[OMITTED FOR LENGTH - Article about Justice Ruth Bader Ginsburg,`  <br>`Champion Of Gender Equality, Dies At 87]`  <br>  <br>`1. …`  <br>`2. …`  <br>`3. Why will Ginsburg’s death have`  <br>`profound consequences for the court and the country?`|`1. …`  <br>`2. …`  <br>`3. Ruth Bader Ginsburg was the leader of the liberal wing, and because the court is about to open a new term, the chief`  <br>`justice no longer holds the controlling vote in contested cases.`|
|`ELI5: What’s the cause of the`  <br>`"anxiety lump" in our chest during stressful or disheartening`  <br>`experiences?`|`The anxiety lump in your throat is caused by muscular tension keeping your glottis dilated to maximize airflow. The clenched chest or heartache feeling is caused by the vagus nerve which tells the organs to pump blood faster, stop digesting, and`  <br>`produce adrenaline and cortisol.`|

Les entreprises font donc souvent appel à des annotateurs hautement qualifiés pour générer des données de démonstration. Parmi ceux qui ont annoté les données de démonstration d'InstructGPT, [environ 90 % possèdent au moins une licence](https://oreil.ly/SF_X9) et plus d'un tiers un master. Si l'annotation d'objets dans une image ne prend que quelques secondes, la génération d'une paire (invite, réponse) peut nécessiter jusqu'à 30 minutes, notamment pour les tâches impliquant des contextes longs, comme la synthèse. Si le coût d'une paire (invite, réponse) est de 10 $, les 13 000 paires utilisées par OpenAI pour InstructGPT auraient coûté 130 000 $. Ce coût n'inclut pas encore la conception des données (choix des tâches et des invites), le recrutement des annotateurs et le contrôle qualité des données.

L'approche d'annotation humaine de haute qualité n'est pas accessible à tous. LAION, une organisation à but non lucratif, a mobilisé 13 500 bénévoles à travers le monde pour générer 10 000 conversations, soit 161 443 messages dans 35 langues différentes, annotés avec 461 292 évaluations de qualité. Les données ayant été générées par des bénévoles, le contrôle des biais était limité. En théorie, les annotateurs qui enseignent aux modèles les préférences humaines devraient être représentatifs de la population. Or, le profil démographique des annotateurs de LAION est déséquilibré. Par exemple, dans une enquête déclarative, 90 % des annotateurs bénévoles se sont identifiés comme des hommes ( [Köpf et al., 2023](https://arxiv.org/abs/2304.07327) ).

DeepMind a utilisé [des heuristiques simples](https://arxiv.org/abs/2112.11446) pour filtrer les conversations issues de données Internet afin d'entraîner son modèle Gopher. L'entreprise affirme que ses heuristiques produisent de manière fiable des dialogues de haute qualité. Plus précisément, elle a recherché des textes ressemblant au format suivant :

[A] : [Court paragraphe]
[B] : [Court paragraphe]
[A] : [Court paragraphe]
[B] : [Court paragraphe]
…

Afin de réduire leur dépendance aux données annotées par des humains de haute qualité, de nombreuses équipes se tournent vers les données générées par l'IA. Les données synthétiques sont abordées au [chapitre 8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) .

Techniquement, il est possible d'entraîner un modèle à partir de zéro sur les données de démonstration au lieu d'affiner un modèle pré-entraîné, ce qui élimine de fait l'étape de pré-entraînement auto-supervisé. Cependant, l'approche par pré-entraînement a souvent donné de meilleurs résultats.

## Réglage fin des préférences

Un grand pouvoir implique de grandes responsabilités. Un modèle capable d'aider les utilisateurs à accomplir de grandes choses peut aussi les amener à commettre des actes terribles. Les données de démonstration apprennent au modèle à dialoguer, mais ne lui apprennent pas quel type de dialogue il doit avoir. Par exemple, si un utilisateur demande au modèle de rédiger une dissertation expliquant pourquoi une race est inférieure ou comment détourner un avion, le modèle doit- il s'exécuter ?

Dans les deux exemples précédents, la plupart des gens comprennent aisément le rôle d'un modèle. Cependant, de nombreux scénarios sont loin d'être aussi simples. Les personnes d'horizons culturels, politiques, socio-économiques, de genre et religieux différents sont constamment en désaccord. Comment une IA doit-elle répondre aux questions concernant l'avortement, le contrôle des armes à feu, le conflit israélo-palestinien, l'éducation des enfants, la légalisation du cannabis, le revenu universel ou l'immigration ? Comment définir et détecter les sujets potentiellement controversés ? Si votre modèle réagit à un sujet controversé, quelles que soient ses réponses, vous risquez de mécontenter certains utilisateurs. À l'inverse, une censure excessive [peut rendre un modèle ennuyeux](https://oreil.ly/5oSEJ) et [faire fuir les utilisateurs](https://oreil.ly/D1S6y) .

La crainte que les modèles d'IA produisent des réponses inappropriées peut dissuader les entreprises de commercialiser leurs applications. L'objectif du réglage fin des préférences est d'amener les modèles d'IA à se comporter conformément aux préférences humaines.<sup> [23</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id797) Il s'agit d'un objectif ambitieux, voire impossible. Non seulement cela suppose l'existence de préférences humaines universelles, mais aussi la possibilité de les intégrer à l'IA.

Si l'objectif avait été simple, la solution aurait pu être élégante. Cependant, compte tenu de l'ambition de l'objectif, la solution actuelle est complexe. Le premier algorithme de réglage fin des préférences ayant rencontré un certain succès, et qui reste populaire aujourd'hui, est RLHF. RLHF se compose de deux parties :

1. Entraînez un modèle de récompense qui évalue les sorties du modèle de base.
    
2. Optimiser le modèle de base pour générer des réponses pour lesquelles le modèle de récompense attribuera des scores maximaux.
    

Bien que la méthode RLHF soit encore utilisée aujourd'hui, des approches plus récentes comme la méthode DPO ( [Rafailov et al., 2023](https://arxiv.org/abs/2305.18290) ) gagnent du terrain. Par exemple,Meta est passé de RLHF pour Llama 2 à DPO pour Llama 3 afin de réduire la complexité. Je ne pourrai pas aborder toutes les approches dans cet ouvrage. J'ai choisi de présenter RLHF plutôt que DPO car, bien que plus complexe, RLHF offre une plus grande flexibilité pour ajuster le modèle. Les auteurs de Llama 2 ont avancé que « les performances supérieures des modèles linguistiques linguistiques (LLM), qui se manifestent par leur capacité à surpasser les annotateurs humains dans certaines tâches, sont fondamentalement dues à RLHF » ( [Touvron et al., 2023](https://arxiv.org/abs/2307.09288) ).

### Modèle de récompense

RLHF repose sur un modèle de récompense. Étant donné une paire (invite, réponse), ce _modèle_ attribue un score à la qualité de la réponse. L'entraînement d'un modèle à évaluer une entrée donnée est une tâche courante en apprentissage automatique. La difficulté, similaire à celle de SFT, réside dans l'obtention de données fiables. Si l'on demande à des annotateurs d'évaluer directement chaque réponse, les scores varieront. Pour un même échantillon, sur une échelle de 10 points, un annotateur pourrait attribuer un score de 5 et un autre de 7. Même un même annotateur, confronté deux fois à la même paire (invite, réponse), pourrait donner des scores différents.L'évaluation indépendante de chaque échantillon est également appelée évaluation _ponctuelle_ .

Une tâche plus simple consiste à demander aux étiqueteurs de comparer deux réponses et de déterminer laquelle est la meilleure. Pour chaque question, plusieurs réponses sont générées, soit par des humains, soit par une IA. Les données étiquetées qui en résultent sont_Les données de comparaison_ suivent le format (question, réponse gagnante, réponse perdante). [Le tableau 2-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_table_7_1730147895537589) présente un exemple de données de comparaison utilisées par Anthropic pour l'un de ses modèles. Parmi les deux réponses proposées, je préfère celle désignée comme perdante. Ceci illustre la difficulté de modéliser la diversité des préférences humaines dans un seul modèle mathématique.

Tableau 2-7. Un exemple de données comparatives tirées de l’ensemble de données HH-RLHF d’ [Anthropic .](https://oreil.ly/h9oG6)

|rapide|réponse gagnante|perte de réponse|
|---|---|---|
|`How can I get my dog high?`|`I’m not sure what you` `mean by that.`|`I don’t know that we should get the dog high. I think it’s important for a dog to experience the world in a sober state of mind.`|

Néanmoins, même cette tâche aisée de comparaison de deux réponses prend du temps. LMSYS (Large Model Systems Organization), un organisme de recherche ouvert, a constaté que la comparaison manuelle de deux réponses prenait en moyenne de trois à cinq minutes, car le processus exige la vérification de chaque réponse ( [Chiang et al., 2024 ). Lors d'une discussion avec ma communauté Discord,](https://arxiv.org/abs/2403.04132) [Thomas Scialom,](https://oreil.ly/P1MPQ) auteur de Llama-2, a indiqué que chaque comparaison leur coûtait 3,50 $. Cela reste bien moins cher que la rédaction des réponses, qui coûte 25 $ chacune.

[La figure 2-13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_13_1730147895520928) présente l' [interface utilisateur utilisée par les annotateurs d'OpenAI](https://oreil.ly/kYtBG) pour créer des données de comparaison destinées au modèle de récompense d'InstructGPT. Les annotateurs attribuent des scores précis de 1 à 7 et classent les réponses par ordre de préférence, mais seul ce classement est utilisé pour entraîner le modèle. Leur taux de concordance inter-annotateurs est d'environ 73 %, ce qui signifie que si l'on demande à 10 personnes de classer deux réponses identiques, environ 7 d'entre elles attribueront le même classement. Afin d'accélérer le processus d'annotation, chaque annotateur peut classer plusieurs réponses simultanément. Un ensemble de trois réponses classées (A > B > C) génère ainsi trois paires de réponses classées : (A > B), (A > C) et (B > C).

![Capture d'écran d'une capture d'écran d'ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0213.png)

###### Figure 2-13. Les étiqueteurs d'interface utilisés pour générer des données de comparaison pour InstructGPT d'OpenAI.

Comment entraîner un modèle à fournir des scores concrets à partir de données comparatives uniquement ? De la même manière qu'on peut amener des humains à faire presque n'importe quoi avec la bonne motivation, on peut amener un modèle à faire de même avec la bonne fonction objectif. Une fonction couramment utilisée représente la différence entre les scores obtenus pour la réponse gagnante et la réponse perdante. L'objectif est de maximiser cette différence. Pour ceux qui s'intéressent aux détails mathématiques, voici la formule utilisée par [InstructGPT](https://arxiv.org/abs/2203.02155) :

- : le modèle de récompense en cours d'entraînement, paramétré par θ. L'objectif du processus d'entraînement est de trouver θ pour lequel la perte est minimisée.
- Format des données d'entraînement :
    
    - : rapide
    - : réponse gagnante
    - perte de réponse
- : score scalaire du modèle de récompense pour la réponse gagnante
- : score scalaire du modèle de récompense pour la réponse perdante
- : la fonction sigmoïde

Pour chaque échantillon d'entraînement, la valeur de la perte est calculée comme suit :

- Objectif : trouverminimiser la perte attendue pour tous les échantillons d'entraînement.
    

Le modèle de récompense peut être entraîné à partir de zéro ou affiné à partir d'un autre modèle, tel qu'un modèle pré-entraîné ou un modèle SFT. L'affinage à partir du modèle de base le plus performant semble donner les meilleurs résultats. Certains estiment que le modèle de récompense doit être au moins aussi puissant que le modèle de base pour pouvoir évaluer les réponses de ce dernier. Cependant, comme nous le verrons au [chapitre 3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) consacré à l'évaluation, un modèle faible peut évaluer un modèle plus puissant, car l'évaluation est considérée comme plus aisée que la génération.

### Réglage fin à l'aide du modèle de récompense

À partir du modèle RM entraîné, nous entraînons ensuite le modèle SFT afin de générer des réponses qui maximisent les scores obtenus par le système de récompense. Durant ce processus, des invites sont sélectionnées aléatoirement parmi une distribution d'invites, telles que des invites utilisateur existantes. Ces invites sont ensuite introduites dans le modèle, dont les réponses sont évaluées par le système de récompense. Ce processus d'entraînement est souvent réalisé avec[l'optimisation de politique proximale (PPO)](https://oreil.ly/TpaGg) , un algorithme d'apprentissage par renforcement publié par OpenAI en 2017.

Empiriquement, RLHF et DPO améliorent tous deux les performances par rapport à SFT seul. Cependant, à l'heure actuelle, leur fonctionnement fait encore débat. Avec l'évolution du domaine, je pense que le réglage fin des préférences connaîtra des changements importants à l'avenir. Si vous souhaitez en savoir plus sur RLHF et le réglage fin des préférences, consultez le [dépôt GitHub du livre](https://github.com/chiphuyen/aie-book) .

L'ajustement fin du SFT et des préférences vise à pallier le problème de la faible qualité des données de pré-entraînement. Si nous disposons un jour de meilleures données de pré-entraînement ou de meilleures méthodes d'entraînement des modèles de base, l'ajustement fin du SFT et des préférences pourrait devenir superflu.

Certaines entreprises jugent acceptable de se passer complètement de l'apprentissage par renforcement. Par exemple, [Stitch Fix](https://oreil.ly/iYh-B) et [Grab](https://oreil.ly/CSSed) estiment qu'un modèle de récompense seul suffit à leurs applications. Leurs modèles génèrent plusieurs sorties et sélectionnent celles qui obtiennent les meilleurs scores. Cette approche, souvent appelée stratégie « _meilleur des N »_ , tire parti de la manière dont un modèle échantillonne les sorties pour améliorer ses performances. La section suivante expliquera le fonctionnement de cette stratégie..

# Échantillonnage

Un modèle construit ses résultats par un processus appelé _échantillonnage_ . Cette section aborde différentes stratégies et _variables d'échantillonnage,_ notamment la température, les k et p valeurs les plus fréquentes. Elle explore ensuite comment échantillonner plusieurs résultats pour améliorer les performances du modèle. Nous verrons également comment modifier le processus d'échantillonnage afin d'obtenir des réponses conformes à certains formats et contraintes.

L'échantillonnage confère un caractère probabiliste aux résultats de l'IA. Comprendre cette nature probabiliste est essentiel pour gérer les comportements de l'IA, tels que l'incohérence et les hallucinations. Cette section se termine par une analyse approfondie de la signification de cette nature probabiliste et de la manière de l'exploiter.

## Principes fondamentaux de l'échantillonnage

À partir d'une entrée, un réseau neuronal produit une sortie en calculant d'abord les probabilités des résultats possibles. Pour un modèle de classification, les résultats possibles correspondent aux classes disponibles. Par exemple, si un modèle est entraîné à déterminer si un courriel est un spam ou non, il n'y a que deux résultats possibles : spam ou non-spam. Le modèle calcule la probabilité de chacun de ces deux résultats ; par exemple, la probabilité que le courriel soit un spam est de 90 %, et celle qu'il ne le soit pas est de 10 %. Vous pouvez ensuite prendre des décisions en fonction de ces probabilités. Par exemple, si vous décidez que tout courriel dont la probabilité d'être un spam est supérieure à 50 % doit être marqué comme spam, un courriel dont la probabilité est de 90 % sera marqué comme spam.

Pour un modèle de langage, afin de générer le jeton suivant, le modèle calcule d'abord la distribution de probabilité sur tous les jetons du vocabulaire, qui ressemble à [la figure 2-14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_14_1730147895520937) .

![Diagramme de description des couleurs généré automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0214.png)

###### Figure 2-14. Pour générer le jeton suivant, le modèle de langage calcule d'abord la distribution de probabilité sur tous les jetons du vocabulaire.

Lorsqu'on travaille avec des résultats possibles de probabilités différentes, une stratégie courante consiste à choisir celui qui a la plus grande probabilité. Ce choix systématique du résultat le plus probable est appelé _échantillonnage glouton_ . Cette méthode fonctionne souvent pour les tâches de classification. Par exemple, si le modèle estime qu'un courriel a plus de chances d'être un spam que de ne pas l'être, il est logique de le marquer comme tel. Cependant, pour un modèle de langage, l'échantillonnage glouton produit des résultats monotones. Imaginez un modèle qui, quelle que soit la question posée, répond systématiquement par les mots les plus fréquents.

Au lieu de toujours choisir le jeton le plus probable, le modèle peut le sélectionner aléatoirement en fonction de la distribution de probabilité sur toutes les valeurs possibles. Dans le contexte de la phrase « Ma couleur préférée est… » (voir [figure 2-14)](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_14_1730147895520937) , si « rouge » a 30 % de chances d'être le jeton suivant et « vert » 50 %, alors « rouge » sera choisi dans 30 % des cas et « vert » dans 50 % des cas.

Comment un modèle calcule-t-il ces probabilités ? À partir d’une entrée, un réseau de neurones produit un vecteur logit. Chaque _logit_ correspond à une valeur possible. Dans le cas d’un modèle de langage, chaque logit correspond à un jeton du vocabulaire du modèle. La taille du vecteur logit est égale à la taille du vocabulaire. Une visualisation du vecteur logit est présentée dans [la figure 2-15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_15_1730147895520946) .

![Schéma d'un réseau. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0215.png)

###### Figure 2-15. Pour chaque entrée, un modèle de langage produit un vecteur logit. Chaque logit correspond à un jeton du vocabulaire.

Bien que des logits plus élevés correspondent à des probabilités plus élevées, les logits ne représentent pas des probabilités. La somme des logits n'est jamais égale à un. Les logits peuvent même être négatifs, alors que les probabilités sont nécessairement non négatives. Pour convertir les logits en probabilités, on utilise souvent une couche softmax. Supposons que le modèle possède un vocabulaire de N et que le vecteur logit soit :La probabilité du _i- ème_ jeton,est calculé comme suit :

## Stratégies d'échantillonnage

Une stratégie d'échantillonnage appropriée permet à un modèle de générer des réponses plus adaptées à votre application. Par exemple, une stratégie peut encourager des réponses plus créatives, tandis qu'une autre peut rendre les réponses plus prévisibles. De nombreuses stratégies d'échantillonnage ont été introduites pour orienter les modèles vers des réponses présentant des attributs spécifiques. Vous pouvez également concevoir votre propre stratégie, mais cela nécessite généralement l'accès aux logits du modèle. Examinons quelques stratégies d'échantillonnage courantes pour comprendre leur fonctionnement.

### Température

L'un des problèmes liés à l'échantillonnage du jeton suivant selon la distribution de probabilité est que le modèle peut manquer de créativité. Dans l'exemple précédent, les couleurs courantes comme « rouge », « vert », « violet », etc., ont les probabilités les plus élevées. La réponse du modèle de langage finit par ressembler à celle d'un enfant de cinq ans : « Ma couleur préférée est le vert ». Comme l'article défini « le » a une faible probabilité, le modèle a peu de chances de générer une phrase créative telle que « Ma couleur préférée est la couleur d'un lac calme un matin de printemps ».

Pour redistribuer les probabilités des valeurs possibles, on peut effectuer un échantillonnage à _température contrôlée_ . Intuitivement, une température plus élevée diminue la probabilité des jetons fréquents et, par conséquent, augmente celle des jetons rares. Cela permet aux modèles de générer des réponses plus originales.

La température est une constante utilisée pour ajuster les logits avant la transformation softmax. Les logits sont divisés par la température. Pour une température _T_ donnée , le logit ajusté pour le _i -ème_ jeton estOn applique ensuite la fonction Softmax à ce logit ajusté au lieu de la fonction logit initiale..

Prenons un exemple simple pour examiner l'influence de la température sur les probabilités. Imaginons un modèle à deux sorties possibles : A et B. Les logits calculés à partir de la dernière couche sont compris entre 1 et 2. Le logit de A est 1 et celui de B est 2.

Sans tenir compte de la température (ce qui équivaut à utiliser une température de 1), les probabilités softmax sont comprises entre 0,27 et 0,73. Le modèle choisit B dans 73 % des cas.

Pour une température de 0,5, les probabilités sont comprises entre 0,12 et 0,88. Le modèle choisit alors B dans 88 % des cas.

Plus la température est élevée, moins le modèle est susceptible de choisir la valeur la plus évidente (celle avec le logit le plus élevé), ce qui rend ses résultats plus créatifs mais potentiellement moins cohérents. Plus la température est basse, plus le modèle est susceptible de choisir la valeur la plus évidente, ce qui rend ses résultats plus cohérents mais potentiellement moins intéressants. [24](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id816)

[La figure 2-16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_16_1730147895520958) illustre les probabilités softmax des jetons A et B à différentes températures. Plus la température se rapproche de 0, plus la probabilité que le modèle sélectionne le jeton B se rapproche de 1. Dans notre exemple, pour une température inférieure à 0,1, le modèle sélectionne presque systématiquement le jeton B. À mesure que la température augmente, la probabilité de sélection du jeton A augmente tandis que celle du jeton B diminue. Les fournisseurs de modèles limitent généralement la température entre 0 et 2. Si vous êtes propriétaire de votre modèle, vous pouvez utiliser n'importe quelle température non négative. Une température de 0,7 est souvent recommandée pour les cas d'utilisation créatifs, car elle offre un bon compromis entre créativité et prévisibilité. Il est toutefois conseillé d'expérimenter afin de trouver la température optimale pour votre cas d'utilisation.

![Un graphique avec une description linéaire générée automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0216.png)

###### Figure 2-16. Probabilités softmax des jetons A et B à différentes températures, leurs logits étant compris entre 1 et 2. Sans spécifier la température (ce qui équivaut à utiliser une température de 1), la probabilité softmax de B serait de 73 %.

Il est courant de fixer la température à 0 pour que les sorties du modèle soient plus cohérentes. Techniquement, la température ne peut jamais être égale à 0, car les logits ne sont pas divisibles par 0. En pratique, lorsqu'on fixe la température à 0, le modèle sélectionne simplement le jeton ayant le logit le plus élevé ( [25)](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id817) sans effectuer d'ajustement logit ni de calcul softmax.

###### Conseil

Une technique de débogage courante lors de l'utilisation d'un modèle d'IA consiste à examiner les probabilités calculées par ce modèle pour des entrées données. Par exemple, si les probabilités semblent aléatoires, le modèle n'a pas encore beaucoup appris.

De nombreux fournisseurs de modèles renvoient les probabilités générées par leurs modèles sous forme de [logprobs](https://oreil.ly/VAUl6) . _Les logprobs_ , abréviation de _probabilités logarithmiques_ , sont des probabilités exprimées sur une échelle logarithmique. L'échelle logarithmique est préférable pour les probabilités des réseaux de neurones car elle contribue à réduire le problème [de sous-dépassement de capacité](https://en.wikipedia.org/wiki/Arithmetic_underflow) . Un modèle de langage peut fonctionner avec un vocabulaire de 100 000 [mots](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id819) , ce qui signifie que les probabilités de nombreux mots peuvent être trop faibles pour être représentées par une machine. Ces petites valeurs peuvent être arrondies à zéro. L'échelle logarithmique permet de réduire ce problème.

[La figure 2-17](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_17_1730147895520965) montre le flux de travail de la façon dont les logits, les probabilités et les logprobs sont calculés.

![Diagramme d'une fonction softmax. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0217.png)

###### Figure 2-17. Comment les logits, les probabilités et les logprobs sont calculés.

Comme vous le verrez tout au long de cet ouvrage, les logprobs sont utiles pour développer des applications (notamment pour la classification), les évaluer et comprendre le fonctionnement interne des modèles. Cependant, à l'heure actuelle, de nombreux fournisseurs de modèles n'exposent pas les logprobs de leurs modèles, ou, lorsqu'ils le font, l'API des logprobs est limitée. [Cette](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id820) limitation de l'API est probablement due à des raisons de sécurité, car l'exposition des logprobs d'un modèle facilite sa réplication.

### Top-k

_Top-k_ est une stratégie d'échantillonnage permettant de réduire la charge de calcul sans trop sacrifier la diversité des réponses du modèle. Rappelons qu'une couche softmax est utilisée pour calculer la distribution de probabilité sur toutes les valeurs possibles. Softmax nécessite deux passages sur toutes les valeurs possibles : un pour effectuer la somme exponentielleet un à jouerpour chaque valeur. Pour un modèle de langage doté d'un vocabulaire étendu, ce processus est coûteux en ressources de calcul.

Pour éviter ce problème, une fois les logits calculés par le modèle, nous sélectionnons les k logits les plus pertinents et appliquons la fonction softmax uniquement à ces k logits. Selon le niveau de diversité souhaité pour votre application, k peut varier de 50 à 500, une valeur bien inférieure à la taille du vocabulaire du modèle. Le modèle effectue ensuite un échantillonnage à partir de ces valeurs optimales. Une valeur de k plus petite rend le texte plus prévisible, mais moins intéressant, car le modèle est limité à un ensemble plus restreint de mots probables.

### Top-p

Dans l'échantillonnage top-k, le nombre de valeurs considérées est fixé à k. Cependant, ce nombre doit varier selon le contexte. Par exemple, face à la question « Aimez-vous la musique ? Répondez par oui ou non. », seules deux valeurs seront prises en compte : oui et non. En revanche, face à la question « Quel est le sens de la vie ? », le nombre de valeurs considérées devra être beaucoup plus élevé.

_L'échantillonnage top-p_ , également appelé _échantillonnage du noyau_ , permet une sélection plus dynamique des valeurs à échantillonner. Dans ce type d'échantillonnage, le modèle additionne les probabilités des valeurs suivantes les plus probables par ordre décroissant et s'arrête lorsque la somme atteint p. Seules les valeurs dont la probabilité cumulée est inférieure à p sont prises en compte. Les valeurs courantes de l'échantillonnage top-p (noyau) dans les modèles de langage se situent généralement entre 0,9 et 0,95. Une valeur de top-p de 0,9, par exemple, signifie que le modèle considérera le plus petit ensemble de valeurs dont la probabilité cumulée dépasse 90 %.

Supposons que les probabilités de tous les jetons soient celles indiquées dans [la figure 2-18](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_18_1730147895520971) . Si la probabilité la plus probable (top-p) est de 90 %, seuls les jetons « oui » et « peut-être » seront pris en compte, car leur probabilité cumulée est supérieure à 90 %. Si la probabilité la plus probable (top-p) est de 99 %, alors les jetons « oui », « peut-être » et « non » seront pris en compte.

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0218.png)

###### Figure 2-18. Exemples de probabilités de jetons.

Contrairement à l'échantillonnage top-k, l'échantillonnage top-p ne réduit pas nécessairement la charge de calcul de la fonction softmax. Son avantage réside dans le fait qu'en se concentrant uniquement sur l'ensemble des valeurs les plus pertinentes pour chaque contexte, il permet d'obtenir des résultats plus adaptés au contexte. En théorie, l'échantillonnage top-p ne semble pas présenter beaucoup d'avantages. Cependant, en pratique, il a démontré son efficacité, ce qui explique sa popularité croissante.

Une stratégie d'échantillonnage apparentée est [min-p](https://github.com/huggingface/transformers/issues/27670) , où vous définissez la probabilité minimale qu'un jeton doit atteindre pour être pris en compte lors de l'échantillonnage.

### Condition d'arrêt

Un modèle de langage autorégressif génère des séquences de jetons en les produisant un par un. Une longue séquence de sortie prend plus de temps, coûte plus cher en ressources de calcul (donc en argent) [et](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id829) peut parfois agacer les utilisateurs. Il peut être judicieux de définir une condition pour que le modèle arrête la séquence.

Une méthode simple consiste à demander aux modèles d'arrêter la génération après un nombre fixe de jetons. L'inconvénient est que la sortie risque d'être tronquée en plein milieu d'une phrase. Une autre méthode consiste à utiliser _des jetons_ ou _des mots vides_ . Par exemple, vous pouvez demander à un modèle d'arrêter la génération lorsqu'il rencontre le jeton de fin de séquence. Les conditions d'arrêt permettent de réduire la latence et les coûts.

L'inconvénient de l'arrêt précoce est que, si vous souhaitez que les modèles génèrent des sorties dans un format précis, un arrêt prématuré peut entraîner des erreurs de formatage. Par exemple, si vous demandez au modèle de générer du JSON, un arrêt précoce peut faire en sorte que le JSON généré soit incomplet, notamment en ce qui concerne les parenthèses fermantes, ce qui le rend difficile à analyser.

## Calcul du temps de test

La section précédente expliquait comment un modèle pouvait échantillonner le jeton suivant. Cette section explique comment un modèle pouvait échantillonner la totalité de la sortie.

Une méthode simple pour améliorer la qualité des réponses d'un modèle consiste à _effectuer des tests_ : au lieu de générer une seule réponse par requête, on en génère plusieurs afin d'augmenter les chances d'obtenir de bonnes réponses. Une méthode possible pour effectuer ces tests est la technique du « meilleur des N », présentée précédemment dans ce chapitre : on génère aléatoirement plusieurs sorties et on sélectionne la plus performante. Cependant, il est également possible d'adopter une approche plus stratégique pour générer ces sorties. Par exemple, au lieu de générer toutes les sorties indépendamment, ce qui pourrait inclure de nombreux candidats peu prometteurs, on peut utiliser [la recherche par faisceau](https://en.wikipedia.org/wiki/Beam_search) pour générer un nombre fixe de candidats les plus prometteurs (le faisceau) à chaque étape de la génération de la séquence.

Une stratégie simple pour améliorer l'efficacité des calculs lors des tests consiste à diversifier les résultats, car un ensemble d'options plus varié est plus susceptible de générer de meilleurs candidats. Si vous utilisez le même modèle pour générer différentes options, il est souvent judicieux de faire varier les variables d'échantillonnage du modèle afin de diversifier ses résultats.

Bien qu'il soit généralement possible d'améliorer les performances du modèle en échantillonnant plusieurs sorties, cette méthode est coûteuse. En moyenne, générer deux sorties coûte environ deux fois plus cher que d'en générer une seule. [29](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id833)

###### Avertissement

J'utilise le terme _« calcul en temps de test »_ par souci de cohérence avec la littérature existante, malgré les objections de plusieurs relecteurs initiaux quant à sa nature confuse. En recherche en IA, le temps de test est généralement employé pour désigner l'inférence, car les chercheurs y ont principalement recours pour tester un modèle. Toutefois, cette technique peut s'appliquer aux modèles en production en général. On parle de calcul en temps de test car le nombre de sorties échantillonnables est déterminé par la puissance de calcul allouée à chaque appel d'inférence.

Pour sélectionner la meilleure sortie, vous pouvez soit présenter plusieurs sorties aux utilisateurs et les laisser choisir celle qui leur convient le mieux, soit concevoir une méthode de sélection. Une méthode consiste à choisir la sortie ayant la probabilité la plus élevée. La sortie d'un modèle de langage est une séquence de jetons, chaque jeton ayant une probabilité calculée par le modèle. La probabilité d'une sortie est le produit des probabilités de tous les jetons qui la composent.

Considérons la séquence de jetons [« je », « j’aime », « nourriture »]. Si la probabilité de « je » est de 0,2, la probabilité de « j’aime » sachant « je » est de 0,1, et la probabilité de « nourriture » ​​sachant « je » et « j’aime » est de 0,3, la probabilité de la séquence est : `0.2 × 0.1 × 0.3 = 0.006`. Mathématiquement, cela peut s’écrire :

p(J'aime la nourriture) = p(Je) × p(Je | j'aime) × p(nourriture | Je, j'aime)

N'oubliez pas qu'il est plus facile de travailler avec les probabilités sur une échelle logarithmique. Le logarithme d'un produit est égal à la somme des logarithmes ; ainsi, la log-probabilité d'une séquence de jetons est la somme des log-probabilités de tous les jetons de la séquence.

logprob( _J'aime la nourriture_ ) = logprob( _Je_ ) + logprob( _Je_ | _aime_ ) + logprob( _nourriture_ | _Je, aime_ )

Lors de la sommation, les séquences plus longues ont généralement une logprobabilité totale plus faible (les valeurs de logprobabilité sont généralement négatives, car le logarithme des valeurs comprises entre 0 et 1 est négatif). Pour éviter un biais en faveur des séquences courtes, vous pouvez utiliser la logprobabilité moyenne en divisant la somme d'une séquence par sa longueur. Après avoir échantillonné plusieurs sorties, vous sélectionnez celle qui présente la logprobabilité moyenne la plus élevée.À l'heure où j'écris ces lignes, c'est ce qu'utilise l'API OpenAI. [30](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id835)

Une autre méthode de sélection consiste à utiliser un modèle de récompense pour évaluer chaque produit, comme expliqué dans la section précédente. Rappelons que [Stitch Fix](https://oreil.ly/1Njeh) et [Grab](https://oreil.ly/l21nr) sélectionnent les produits ayant obtenu les meilleurs scores de leurs modèles de récompense ou de leurs vérificateurs. [Nextdoor](https://oreil.ly/-HQIB) a constaté que l'utilisation d'un modèle de récompense était un facteur clé de l'amélioration des performances de son application (2023).

OpenAI a également formé des vérificateurs pour aider ses modèles à choisir les meilleures solutions aux problèmes mathématiques ( [Cobbe et al., 2021](https://oreil.ly/R_uvq) ). Les chercheurs ont constaté que l'utilisation d'un vérificateur améliorait considérablement les performances du modèle. _En effet, le gain de performance obtenu grâce aux vérificateurs est comparable à celui obtenu en multipliant par 30 la taille du modèle._ Ainsi, un modèle de 100 millions de paramètres utilisant un vérificateur peut atteindre des performances équivalentes à celles d'un modèle de 3 milliards de paramètres sans vérificateur.

DeepMind confirme l'intérêt du calcul lors des tests, en démontrant que l'augmentation de la puissance de calcul allouée (par exemple, en générant davantage de résultats lors de l'inférence) peut s'avérer plus efficace que la modification des paramètres du modèle ( [Snell et al., 2024](https://arxiv.org/abs/2408.03314) ). Le même article soulève une question intéressante : si un modèle linéaire généralisé (LLM) dispose d'une quantité fixe, mais non négligeable, de puissance de calcul lors de l'inférence, dans quelle mesure ses performances peuvent-elles être améliorées face à une requête complexe ?

Dans l'expérience d'OpenAI, l'échantillonnage d'un plus grand nombre de sorties a permis d'améliorer les performances, mais seulement jusqu'à un certain point. Dans cette expérience, ce point était de 400 sorties. Au-delà, les performances diminuent, comme le montre la [figure 2-19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_19_1730147895520976) . Les chercheurs ont émis l'hypothèse que plus le nombre de sorties échantillonnées augmente, plus la probabilité de trouver des sorties adverses capables de tromper le vérificateur augmente également. Cependant, une expérience menée à Stanford a abouti à une conclusion différente. « Monkey Business » ( [Brown et al., 2024](https://oreil.ly/8YNwQ) ) montre que le nombre de problèmes résolus augmente souvent de manière log-linéaire lorsque le nombre d'échantillons passe de 1 à 10 000. Bien qu'il soit intéressant de se demander si la puissance de calcul en phase de test peut être augmentée indéfiniment, je doute que quiconque en production échantillonne 400 ou 10 000 sorties différentes pour chaque entrée. Le coût serait astronomique.

![Graphique avec lignes bleues et chiffres. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0219.png)

###### Figure 2-19. [OpenAI](https://arxiv.org/abs/2110.14168) (2021) a constaté que l'échantillonnage d'un plus grand nombre de sorties conduisait à de meilleures performances, mais seulement jusqu'à 400 sorties.

Vous pouvez également utiliser des heuristiques spécifiques à l'application pour sélectionner la meilleure réponse. Par exemple, si votre application privilégie les réponses courtes, vous pouvez choisir la réponse la plus courte. Si votre application convertit le langage naturel en requêtes SQL, vous pouvez configurer le modèle pour qu'il continue à générer des résultats jusqu'à obtenir une requête SQL valide.

L'une des applications particulièrement intéressantes du calcul en temps réel consiste à surmonter le problème de la latence. Pour certaines requêtes, notamment celles impliquant un enchaînement de raisonnement, un modèle peut mettre beaucoup de temps à fournir une réponse. Kittipat Kampa, responsable de l'IA chez TIFIN, m'a expliqué que son équipe demande à son modèle de générer plusieurs réponses en parallèle et d'afficher à l'utilisateur la première réponse complète et valide.

Identifier la réponse la plus fréquente parmi un ensemble de résultats peut s'avérer particulièrement utile pour les tâches exigeant des réponses exactes.<sup> [31</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id836) Par exemple, face à un problème mathématique, le modèle peut le résoudre plusieurs fois et retenir la réponse la plus fréquente comme solution finale. De même, pour une question à choix multiples, un modèle peut sélectionner l'option de réponse la plus fréquente.Voici comment Google a procédé lors de l'évaluation de Gemini sur le benchmark MMLU. Ils ont échantillonné 32 réponses pour chaque question. Cela a permis au modèle d'obtenir un score supérieur à celui qu'il aurait obtenu avec une seule réponse par question.

Un modèle est considéré comme robuste s'il ne modifie pas sensiblement ses résultats en fonction de faibles variations des données d'entrée. Moins un modèle est robuste, plus il est avantageux d'échantillonner plusieurs résultats. [Dans](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id838) le cadre d'un projet, nous avons utilisé l'IA pour extraire certaines informations d'une image de produit. Nous avons constaté que, pour une même image, notre modèle ne parvenait à extraire les informations que dans la moitié des cas. Dans l'autre moitié des cas, le modèle indiquait que l'image était trop floue ou que le texte était trop petit pour être lisible. Cependant, en effectuant trois essais avec chaque image, le modèle a réussi à extraire les informations correctes pour la plupart des images.

## Sorties structurées

En production, il est souvent nécessaire que les modèles génèrent des résultats conformes à certains formats. Les résultats structurés sont essentiels dans les deux cas suivants :

1. _Tâches nécessitant des résultats structurés._ La catégorie de tâches la plus courante dans ce contexte est l'analyse sémantique. L'analyse sémantique consiste à convertir le langage naturel en un format structuré et lisible par machine.La conversion de texte en SQL est un exemple d'analyse sémantique, où les résultats doivent être des requêtes SQL valides. L'analyse sémantique permet aux utilisateurs d'interagir avec des API en utilisant un langage naturel (par exemple, l'anglais). Par exemple, la conversion de texte en PostgreSQL permet aux utilisateurs d'interroger une base de données PostgreSQL à l'aide de requêtes en anglais telles que « Quel est le revenu mensuel moyen des six derniers mois ? » au lieu de les écrire en langage PostgreSQL.
    
    Voici un exemple de requête pour GPT-4o afin d'effectuer une conversion de texte en expression régulière. Les résultats affichés sont des résultats réels générés par GPT-4o :
    
    **invite système**
    Étant donné un élément, créez une expression régulière qui représente toutes les façons dont l'élément peut être
    écrit. Retourner uniquement l'expression régulière.
    Exemple:
    Numéro de téléphone américain -> +?1?\s?(\()?(\d{3})(?(1)\))[-.\s]?(\d{3})[-.\s]?(\d{4})
    **Invite de l'utilisateur**
    Adresse e-mail ->
    **GPT-4o**
    [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
    **Invite de l'utilisateur**
    Dates ->
    **GTP-4o**
    (?:\d{1,2}[\/\-\.])(?:\d{1,2}[\/\-\.])?\d{2,4}
    	
    
    Dans ce scénario, d'autres catégories de tâches incluent la classification, où les résultats doivent appartenir à des classes valides.
    

2. _Tâches dont les résultats sont utilisés par des applications en aval._ Dans ce cas, la tâche elle-même n'a pas besoin que ses résultats soient structurés, mais comme ces résultats sont utilisés par d'autres applications, ils doivent être analysables par ces dernières.
    
    Par exemple, si vous utilisez un modèle d'IA pour rédiger un courriel, ce dernier n'a pas besoin d'être structuré. Cependant, une application en aval utilisant ce courriel peut nécessiter un format spécifique, par exemple un document JSON avec des clés spécifiques `{"title": [TITLE], "body": [EMAIL BODY]}`.
    
    _Ceci est particulièrement important pour les flux de travail d'agents_ où les sorties d'un modèle sont souvent transmises comme entrées dans des outils que le modèle peut utiliser, comme indiqué au [chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) .
    

Les frameworks prenant en charge les sorties structurées incluent [guidance](https://github.com/guidance-ai/guidance) , [outlines](https://github.com/dottxt-ai/outlines) , [instructor](https://github.com/instructor-ai/instructor) et [llama.cpp](https://github.com/ggerganov/llama.cpp/discussions/177) . Chaque fournisseur de modèle peut également utiliser ses propres techniques pour améliorer la capacité de ses modèles à générer des sorties structurées. OpenAI a été le premier fournisseur de modèles à introduire [_le mode JSON_](https://oreil.ly/NxZDF) dans son API de génération de texte. Il est important de noter que le mode JSON d'une API garantit généralement uniquement la validité du JSON produit, et non le contenu des objets JSON. Les JSON générés, par ailleurs valides, peuvent être tronqués, et donc illisibles, si la génération s'arrête prématurément, par exemple lorsqu'elle atteint la longueur maximale des jetons de sortie. Cependant, si cette longueur maximale est trop élevée, les réponses du modèle deviennent à la fois trop lentes et trop coûteuses.

[La figure 2-20](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_20_1730147895520984) montre deux exemples d'utilisation de directives pour générer des sorties limitées à un ensemble d'options et à une expression régulière.

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0220.png)

###### Figure 2-20. Utilisation de directives pour générer des sorties contraintes.

Il est possible d'orienter un modèle vers la génération de sorties structurées à différentes étapes de la pile d'IA : incitation, post-traitement, calcul lors des tests, échantillonnage contraint et ajustement fin. Les trois premières étapes sont des palliatifs. Elles sont particulièrement efficaces si le modèle génère déjà des sorties structurées de manière satisfaisante et ne nécessite qu'un léger ajustement. Pour un traitement plus poussé, l'échantillonnage contraint et l'ajustement fin sont nécessaires.

Le calcul lors des tests a été abordé dans la section précédente : continuez à générer des résultats jusqu’à ce que l’un d’eux corresponde au format attendu. Cette section porte sur les quatre autres approches.

### Incitation

La saisie des instructions est la première étape pour obtenir des résultats structurés. Vous pouvez demander à un modèle de générer des résultats dans n'importe quel format. Cependant, sa capacité à suivre ces instructions dépend de ses aptitudes (traitées au [chapitre 4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) ) et de la clarté de l'instruction (traitée au [chapitre 5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) ). Bien que les modèles soient de plus en plus performants pour suivre les instructions, rien ne garantit qu'ils les suivront toujours. [Un](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id844) faible pourcentage de résultats invalides peut s'avérer inacceptable pour de nombreuses applications.

Pour augmenter le pourcentage de résultats valides, certains utilisent l'IA pour valider et/ou corriger le résultat de la requête initiale. C'est un exemple de l'approche « IA comme juge » abordée au [chapitre 3.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) Concrètement, chaque résultat nécessite au moins deux requêtes : une pour le générer et une pour le valider. Bien que cette couche de validation supplémentaire puisse améliorer significativement la validité des résultats, le coût et la latence supplémentaires induits par ces requêtes peuvent rendre cette approche trop onéreuse pour certains utilisateurs.

### Post-traitement

Le post-traitement est simple et peu coûteux, mais peut s'avérer étonnamment efficace. Durant mon expérience d'enseignement, j'ai constaté que les étudiants commettaient souvent les mêmes erreurs. En travaillant avec les modèles de base, j'ai fait le même constat : un modèle tend à répéter les mêmes erreurs d'une requête à l'autre. Ainsi, en identifiant les erreurs fréquentes d' un modèle , il est possible d'écrire un script pour les corriger. Par exemple, si l'objet JSON généré ne contient pas de parenthèse fermante, il suffit de l'ajouter manuellement. L'analyseur YAML défensif de LinkedIn a permis d'augmenter le pourcentage de résultats YAML corrects de 90 % à 99,99 % ( [Bottoro et Ramgopal, 2020](https://oreil.ly/ZTRaA) ).

###### Conseil

JSON et YAML sont des formats de texte courants. LinkedIn a constaté que son modèle sous-jacent, GPT-4, fonctionnait avec les deux, mais a choisi YAML comme format de sortie car il est moins verbeux et nécessite donc moins de jetons de sortie que JSON (Bottaro et Ramgopal, 2020).

Le post-traitement n'est efficace que si les erreurs sont faciles à corriger. C'est généralement le cas lorsque les résultats d'un modèle sont déjà majoritairement correctement formatés, avec quelques petites erreurs occasionnelles.

### Échantillonnage contraint

_L'échantillonnage contraint_ est une technique permettant d'orienter la génération de texte vers certaines contraintes. Il est généralement suivi d'outils de sortie structurée.

En résumé, pour générer un jeton, le modèle effectue un échantillonnage parmi les valeurs respectant les contraintes. Rappelons que pour générer un jeton, votre modèle produit d'abord un vecteur logit, chaque logit correspondant à un jeton possible. L'échantillonnage contraint filtre ce vecteur logit pour ne conserver que les jetons respectant les contraintes. Il effectue ensuite un échantillonnage parmi ces jetons valides. Ce processus est illustré dans [la figure 2-21](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_21_1730147895520993) .

![Diagramme d'un modèle logiciel. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0221.png)

###### Figure 2-21. Filtrer les logits qui ne répondent pas aux contraintes afin de ne sélectionner que les sorties valides.

Dans l'exemple de [la figure 2-21](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_21_1730147895520993) , la contrainte est facile à filtrer. Cependant, la plupart des cas sont plus complexes. Il est nécessaire de définir une grammaire précisant les éléments autorisés et interdits à chaque étape. Par exemple, la grammaire JSON stipule qu'après une virgule `{`, aucun autre élément ne peut être inséré, `{`sauf s'il fait partie d'une chaîne de caractères, comme dans « json » `{"key": "{{string}}"}`.

L'élaboration de cette grammaire et son intégration au processus d'échantillonnage sont complexes. Chaque format de sortie (JSON, YAML, expressions régulières, CSV, etc.) nécessitant sa propre grammaire, l'échantillonnage contraint est moins généralisable. Son utilisation se limite aux formats dont les grammaires sont prises en charge par des outils externes ou par votre équipe. La vérification de la grammaire peut également accroître la latence de génération ( [Brandon T. Willard, 2024](https://oreil.ly/hNRf4) ).

Certains s'opposent à l'échantillonnage contraint car ils estiment que les ressources nécessaires à cette méthode seraient mieux investies dans l'entraînement des modèles afin qu'ils apprennent à mieux suivre les instructions.

### Réglage fin

L'ajustement fin d'un modèle sur des exemples respectant le format souhaité est l'approche la plus efficace et la plus générale pour obtenir des résultats conformes à ce format.<sup> [34</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id849) Cette méthode est compatible avec tous les formats attendus. Bien qu'un simple ajustement fin ne garantisse pas systématiquement un résultat au format attendu, il est beaucoup plus fiable que l'utilisation d'instructions explicites.

Pour certaines tâches, vous pouvez garantir le format de sortie en modifiant l'architecture du modèle avant le réglage fin. Par exemple, pour la classification, vous pouvez ajouter un classificateur à l'architecture du modèle de base afin de garantir que le modèle ne produise qu'une seule des classes prédéfinies. L'architecture est illustrée à [la](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id850) [figure 2-22](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_22_1730147895521005) . Cette approche est également appelée[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id850)_le transfert basé sur les caractéristiques_ et est discuté plus en détail avec d'autres techniques d'apprentissage par transfert au [chapitre 7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) .

![Diagramme d'une couche - Description générée automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0222.png)

###### Figure 2-22. Ajout d'un module de classification à votre modèle de base pour le transformer en classificateur. Dans cet exemple, le classificateur gère trois classes.

Lors de la phase d'ajustement fin, vous pouvez réentraîner l'intégralité du modèle de bout en bout ou une partie seulement, comme la tête de ce classificateur. L'entraînement de bout en bout exige davantage de ressources, mais promet de meilleures performances.

Nous avons besoin de techniques pour obtenir des résultats structurés car nous partons du principe que le modèle, par lui-même, n'est pas capable de générer de telles sorties. Cependant, à mesure que les modèles gagnent en puissance, on peut s'attendre à ce qu'ils suivent mieux les instructions. Je pense qu'à l'avenir, il sera plus facile d'obtenir des modèles qu'ils produisent exactement ce dont nous avons besoin avec un minimum d'intervention, et ces techniques deviendront moins importantes.

## La nature probabiliste de l'IA

La manière dont les modèles d'IA échantillonnent leurs réponses les rend _probabilistes_ . Prenons un exemple pour illustrer ce que signifie être probabiliste. Imaginez que vous vouliez savoir quelle est la meilleure cuisine du monde. Si vous posez cette question à un ami deux fois, à une minute d'intervalle, sa réponse devrait être identique. En revanche, si vous posez la même question deux fois à un modèle d'IA, sa réponse peut varier. Si un modèle d'IA estime que la cuisine vietnamienne a 70 % de chances d'être la meilleure cuisine du monde et la cuisine italienne 30 %, il répondra « cuisine vietnamienne » dans 70 % des cas et « cuisine italienne » dans 30 % des cas. L'opposé de probabiliste est _déterministe_ , lorsque le résultat peut être déterminé sans aucune variation aléatoire.

Cette nature probabiliste peut engendrer des incohérences et des hallucinations. _Une incohérence_ se manifeste lorsqu'un modèle génère des réponses très différentes pour des stimuli identiques ou légèrement différents._Une hallucination_ se produit lorsqu'un modèle donne une réponse non fondée sur des faits. Imaginez qu'une personne sur Internet écrive un essai affirmant que tous les présidents américains sont des extraterrestres, et que cet essai soit intégré aux données d'entraînement. Le modèle prédira alors, de manière probabiliste, que le président américain actuel est un extraterrestre. Pour quelqu'un qui ne croit pas à cette théorie, le modèle invente tout simplement cette information.

Les modèles de base sont généralement entraînés à l'aide d'une grande quantité de données. Ce sont des agrégats d'opinions du grand public, contenant littéralement un monde de possibilités. Tout ce qui a une probabilité non nulle, aussi improbable ou erroné soit-il, peut être généré par l'IA [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id857)

Cette caractéristique rend le développement d'applications d'IA à la fois passionnant et complexe. Comme nous le verrons dans cet ouvrage, de nombreux travaux d'ingénierie en IA visent à exploiter et à atténuer cette nature probabiliste.

Cette nature probabiliste rend l'IA idéale pour les tâches créatives. Qu'est-ce que la créativité sinon la capacité d'explorer au-delà des sentiers battus, de penser différemment ? L'IA est une précieuse alliée pour les professionnels créatifs. Elle peut générer une infinité d'idées et concevoir des concepts inédits. Cependant, cette même nature probabiliste peut s'avérer problématique dans tous les autres domaines. [37](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id858)

### Incohérence

L'incohérence du modèle se manifeste dans deux scénarios :

1. Même entrée, sorties différentes : donner deux fois la même consigne au modèle conduit à deux réponses très différentes.
    
2. Des entrées légèrement différentes, des sorties radicalement différentes : donner au modèle une consigne légèrement différente, comme par exemple mettre une majuscule par erreur, peut conduire à une sortie très différente.
    

[La figure 2-23](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_23_1730147895521014) illustre un exemple d'utilisation de ChatGPT pour évaluer des dissertations. La même consigne a donné deux scores différents lors de deux exécutions : 3/5 et 5/5.

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0223.png)

###### Figure 2-23. Une même entrée peut produire des sorties différentes dans le même modèle.

L'incohérence peut créer une expérience utilisateur désagréable. Dans la communication interpersonnelle, nous attendons une certaine cohérence. Imaginez qu'une personne vous donne un nom différent à chaque fois que vous la voyez. De même, les utilisateurs attendent une certaine cohérence lorsqu'ils communiquent avec une IA.

Dans le cas d'une même entrée et de sorties différentes, plusieurs approches permettent d'atténuer les incohérences. Vous pouvez mettre en cache la réponse afin qu'elle soit renvoyée lors d'une prochaine question identique. Vous pouvez également fixer les variables d'échantillonnage du modèle, telles que la température, les valeurs top-p et top-k, comme évoqué précédemment. Enfin, vous pouvez fixer la variable _d'initialisation_ , qui correspond au point de départ du générateur de nombres aléatoires utilisé pour l'échantillonnage du jeton suivant.

Même en corrigeant toutes ces variables, rien ne garantit la cohérence de votre modèle à 100 %. Le matériel utilisé pour la génération des résultats peut également influencer ces derniers, car différentes machines exécutent les mêmes instructions différemment et gèrent des plages de nombres différentes. Si vous hébergez vos modèles, vous avez un certain contrôle sur le matériel utilisé. En revanche, si vous utilisez un fournisseur d'API de modèles comme OpenAI ou Google, ce sont ces fournisseurs qui vous offrent ce contrôle.

Configurer les paramètres de génération des résultats est une bonne pratique, mais cela n'inspire pas confiance dans le système. Imaginez un professeur qui ne vous attribue des notes cohérentes que s'il est assis dans une salle précise. S'il est dans une autre salle, ses notes seront totalement incohérentes.

Le second scénario – des entrées légèrement différentes et des sorties radicalement différentes – est plus complexe. Corriger les variables de génération des sorties du modèle reste une bonne pratique, mais cela ne garantit pas que le modèle produise les mêmes sorties pour des entrées différentes. Il est toutefois possible d'obtenir des réponses plus proches de vos attentes grâce à des invites soigneusement conçues (présentées au [chapitre 5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) ) et à un système de mémorisation (présenté au [chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) ).

### Hallucination

Les hallucinations sont fatales pour les tâches qui reposent sur la factualité. Si vous demandez à une IA de vous aider à expliquer les avantages et les inconvénients d'un vaccin, vous ne voulez pas qu'elle soit pseudo-scientifique.En juin 2023, un cabinet d'avocats a été [condamné à une amende pour avoir soumis de fausses recherches juridiques au tribunal](https://oreil.ly/FCyyA) . Ils avaient utilisé ChatGPT pour préparer leur dossier, ignorant la tendance de ChatGPT à générer des hallucinations.

Bien que les hallucinations soient devenues un problème majeur avec l'essor des modèles linéaires à longue portée (LLM), elles constituaient un phénomène courant pour les modèles génératifs bien avant l'introduction des termes « modèle de base » et « architecture Transformer ». Les hallucinations dans le contexte de la génération de texte ont été mentionnées dès 2016 ( [Goyal et al., 2016](https://oreil.ly/cg0JY) ). Depuis, la détection et la mesure des hallucinations sont devenues un élément essentiel de la génération automatique de langage naturel (GLN) (voir [Lee et al., 2018](https://oreil.ly/ah9MT) ; [Nie et al., 2019](https://oreil.ly/13wUD) ; et [Zhou et al., 2020](https://arxiv.org/abs/2011.02593) ). Cette section s'attache à expliquer les causes des hallucinations. Les méthodes de détection et d'évaluation sont abordées au [chapitre 4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) .

Si l'incohérence provient du hasard dans le processus d'échantillonnage, la cause des hallucinations est plus complexe. Le processus d'échantillonnage seul ne suffit pas à l'expliquer. Un modèle échantillonne les sorties de toutes les options probables. Mais comment une chose jamais vue auparavant devient-elle une option probable ? Un modèle peut produire une sortie que l'on croit inédite dans les données d'entraînement. On ne peut l'affirmer avec certitude, car il est impossible d'analyser en profondeur les données d'entraînement pour vérifier si elles contiennent une idée. Notre capacité à construire quelque chose d'aussi complexe que nous ne pouvons plus le comprendre est à la fois une bénédiction et une malédiction.

Il est difficile de concevoir un moyen d'éliminer les hallucinations sans comprendre pourquoi elles surviennent. Il existe actuellement deux hypothèses expliquant pourquoi les modèles du langage hallucinent.

La première hypothèse, initialement formulée par [Ortega et al. chez DeepMind en 2021](https://arxiv.org/abs/2110.10819#deepmind) , est qu'un modèle de langage hallucine car il est incapable de distinguer les données qui lui sont fournies de celles qu'il génère. Prenons un exemple pour illustrer ce point.

Imaginez que vous soumettiez au modèle la question : « Qui est Chip Huyen ? » et que la première phrase générée soit : « Chip Huyen est architecte. » Le jeton suivant sera conditionné par la séquence : « Qui est Chip Huyen ? Chip Huyen est architecte. » Le modèle traite « Chip Huyen est architecte », une phrase qu’il a produite, de la même manière qu’un fait donné. À partir d’une séquence générée légèrement inhabituelle, le modèle peut l’enrichir et produire des faits complètement faux. Ortega et d’autres auteurs ont qualifié les hallucinations de forme d’ _auto-illusion_ .

[La figure 2-24](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_24_1730147895521021) illustre un exemple d'auto-illusion du modèle LLaVA-v1.5-7B. Je lui ai demandé d'identifier les ingrédients figurant sur l'étiquette d'un produit (une bouteille de shampoing). Dans sa réponse, le modèle s'est persuadé qu'il s'agissait d'une bouteille de lait et a donc inclus le lait dans la liste des ingrédients extraits de l'étiquette.

![Une bouteille de lait avec instructions. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0224.png)

###### Figure 2-24. Un exemple d'auto-illusion par LLaVA-v1.5-7B.

Zhang et al. (2023) qualifient ce phénomène d’ [« hallucinations en cascade »](https://arxiv.org/abs/2305.13534) . Après avoir formulé une hypothèse erronée, un modèle peut continuer à produire des hallucinations pour justifier cette hypothèse initiale fausse. Fait intéressant, les auteurs montrent que des hypothèses initiales erronées peuvent amener le modèle à commettre des erreurs sur des questions auxquelles il serait autrement capable de répondre correctement, comme illustré dans [la figure 2-25](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_25_1730147895521031) .

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0225.png)

###### Figure 2-25. Une hypothèse initiale incorrecte peut amener le modèle à affirmer que 9677 est divisible par 13, même s'il sait que ce n'est pas vrai.

L'article de DeepMind a démontré que les hallucinations peuvent être atténuées par deux techniques. La première repose sur l'apprentissage par renforcement : le modèle est conçu pour différencier les incitations fournies par l'utilisateur (appelées _observations du monde dans ce contexte) des jetons générés par le modèle (appelés_ _actions_ du modèle ). La seconde technique s'appuie sur l'apprentissage supervisé, qui intègre des signaux factuels et contrefactuels dans les données d'entraînement.

La seconde hypothèse est que les hallucinations sont dues à une inadéquation entre les connaissances internes du modèle et celles de l'annotateur. Cette hypothèse a été initialement défendue par [Leo Gao](https://oreil.ly/9idN4) , chercheur chez OpenAI. Lors de l'apprentissage par simulation de réponses (SFT), les modèles sont entraînés à imiter les réponses rédigées par les annotateurs. Si ces réponses font appel à des connaissances propres aux annotateurs mais absentes du modèle, on apprend en réalité au modèle à halluciner. En théorie, si les annotateurs pouvaient inclure les connaissances qu'ils utilisent dans chaque réponse, afin que le modèle sache que les réponses ne sont pas inventées, on pourrait peut-être lui apprendre à n'utiliser que ses connaissances. Cependant, cela est impossible en pratique.

En avril 2023, John Schulman, cofondateur d'OpenAI, a exprimé le même point de vue lors d'une [conférence à l'UC Berkeley](https://oreil.ly/Fqo2S) . Schulman pense également que les modèles de langage (LLM) savent s'ils savent quelque chose, ce qui, en soi, constitue une affirmation importante. Si cette hypothèse est juste, les hallucinations peuvent être corrigées en obligeant un modèle à fournir des réponses basées uniquement sur les informations dont il dispose. Il a proposé deux solutions. La première est la vérification : pour chaque réponse, on demande au modèle de retrouver les sources sur lesquelles il fonde sa réponse. La seconde consiste à utiliser l'apprentissage par renforcement. Il est important de rappeler que le modèle de récompense est entraîné uniquement par comparaison – la réponse A est meilleure que la réponse B – sans explication quant à la supériorité de A. Schulman a soutenu qu'une meilleure fonction de récompense, qui pénalise davantage un modèle lorsqu'il invente des réponses, peut contribuer à atténuer les hallucinations.

Dans cette même présentation, Schulman a mentionné qu'OpenAI avait constaté que l'algorithme RLHF contribuait à réduire les hallucinations. Cependant, l'article sur InstructGPT montre que RLHF a aggravé les hallucinations, comme illustré dans [la figure 2-26](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_figure_26_1730147895521041) . Bien que RLHF ait semblé aggraver les hallucinations pour InstructGPT, il a amélioré d'autres aspects et, globalement, les annotateurs humains préfèrent le modèle RLHF au modèle SFT seul.

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0226.png)

###### Figure 2-26. L'hallucination est pire pour le modèle qui utilise à la fois RLHF et SFT (InstructGPT) par rapport au même modèle qui utilise uniquement SFT ( [Ouyang et al., 2022](https://arxiv.org/abs/2203.02155) ).

Partant du principe qu'un modèle de base possède les connaissances qu'il possède, certains tentent de réduire les hallucinations en ajoutant des incitations, comme : « Répondez aussi honnêtement que possible, et si vous n'êtes pas sûr de la réponse, dites : “Désolé, je ne sais pas.” » Demander des réponses concises aux modèles semble également contribuer à réduire les hallucinations : moins un modèle a d'éléments à générer, moins il risque d'inventer des réponses. Les techniques d'incitation et de construction du contexte présentées dans les chapitres [5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) et [6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) peuvent également aider à atténuer les hallucinations.

Les deux hypothèses présentées se complètent. L'hypothèse de l'auto-illusion s'intéresse à la manière dont l'auto-surveillance provoque des hallucinations, tandis que l'hypothèse de la discordance des connaissances internes s'intéresse à la manière dont la supervision provoque des hallucinations.

Si nous ne pouvons pas empêcher complètement les hallucinations, pouvons-nous au moins détecter lorsqu'un modèle hallucine afin de ne pas proposer ces réponses hallucinées aux utilisateurs ? Détecter les hallucinations n'est pas chose facile non plus ; pensez à la difficulté que nous avons à déceler lorsqu'une autre personne ment ou invente des choses. Mais des chercheurs ont essayé. Nous abordons les méthodes de détection et de mesure des hallucinations dans…[Chapitre 4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863).

# Résumé

Ce chapitre a abordé les principales décisions de conception lors de la création d'un modèle de base. La plupart des utilisateurs préférant utiliser des modèles de base prêts à l'emploi plutôt que d'en créer un de toutes pièces, j'ai omis les détails techniques de l'entraînement et me suis concentré sur les facteurs de modélisation permettant de déterminer quels modèles utiliser et comment les mettre en œuvre.

Un facteur crucial influençant les performances d'un modèle est la qualité de ses données d'entraînement. Les modèles complexes nécessitent une grande quantité de données d'entraînement, dont l'acquisition peut s'avérer coûteuse et chronophage. Par conséquent, les fournisseurs de modèles exploitent souvent les données disponibles. Il en résulte des modèles performants sur les nombreuses tâches présentes dans les données d'entraînement, lesquelles peuvent ne pas inclure la tâche spécifique recherchée. Ce chapitre a expliqué pourquoi il est souvent nécessaire de sélectionner avec soin les données d'entraînement pour développer des modèles ciblant des langages spécifiques, notamment ceux disposant de peu de ressources, et des domaines spécifiques.

Une fois les données collectées, le développement du modèle peut commencer. Si l'entraînement du modèle fait souvent la une, l'architecture de ce dernier constitue une étape cruciale. Ce chapitre a examiné les choix de modélisation, tels que l'architecture et la taille du modèle. L'architecture dominante pour les modèles de base basés sur le langage est celle des transformateurs. Ce chapitre a exploré les problèmes que l'architecture des transformateurs a été conçue pour résoudre, ainsi que ses limitations.

L'échelle d'un modèle peut être mesurée par trois chiffres clés : le nombre de paramètres, le nombre de jetons d'entraînement et le nombre d'opérations en virgule flottante (FLOPs) nécessaires à l'entraînement. La taille du modèle et la taille des données sont deux aspects qui influencent la puissance de calcul requise. La loi d'échelle permet de déterminer le nombre optimal de paramètres et de jetons en fonction du budget de calcul alloué. Ce chapitre a également abordé les goulots d'étranglement liés à la mise à l'échelle. Actuellement, augmenter la taille d'un modèle améliore généralement ses performances. Mais combien de temps cela restera-t-il vrai ?

En raison de la faible qualité des données d'entraînement et de l'auto-supervision lors du pré-entraînement, le modèle obtenu peut produire des résultats qui ne correspondent pas aux attentes des utilisateurs. Le post-entraînement permet de remédier à ce problème grâce à deux étapes : l'ajustement supervisé et l'ajustement aux préférences. Les préférences humaines étant diverses et impossibles à modéliser par une simple formule mathématique, les solutions existantes sont loin d'être infaillibles.

Ce chapitre abordait également l'un de mes sujets de prédilection : l'échantillonnage, processus par lequel un modèle génère des jetons de sortie. L'échantillonnage confère aux modèles d'IA un caractère probabiliste. C'est cette nature probabiliste qui rend des modèles comme ChatGPT et Gemini performants pour les tâches créatives et agréables à utiliser. Cependant, cette même nature probabiliste engendre aussi des incohérences et des hallucinations.

Travailler avec des modèles d'IA implique de concevoir ses flux de travail en tenant compte de leur nature probabiliste. La suite de cet ouvrage explorera comment rendre l'ingénierie de l'IA, sinon déterministe, du moins systématique. La première étape vers une ingénierie de l'IA systématique consiste à établir un processus d'évaluation robuste permettant de détecter les défaillances et les changements inattendus. L'évaluation des modèles de base est si cruciale que je lui ai consacré deux chapitres, à commencer par le suivant.

[1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id697-marker) [« GPT-4 peut résoudre des problèmes mathématiques, mais pas dans tous les langages »,](https://oreil.ly/G13KM) par Yennie Jun. Vous pouvez vérifier cette étude à l’aide [du tokenizer d’OpenAI](https://oreil.ly/iqhNY) .

[2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id699-marker)Cela pourrait être dû à des biais dans les données de pré-entraînement ou d'alignement. Il est possible qu'OpenAI n'ait pas inclus suffisamment de données en langue chinoise ou de récits centrés sur la Chine pour entraîner ses modèles.

[3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id705-marker) [« Dans la liste secrète des sites web qui font passer l’IA comme ChatGPT pour intelligente »](https://oreil.ly/St1o8) , _Washington Post_ , 2023.

[4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id706-marker)Pour les textes, on peut utiliser les mots-clés du domaine comme heuristiques, mais il n'existe pas d'heuristiques évidentes pour les images. La plupart des analyses que j'ai pu trouver sur les jeux de données de vision portent sur la taille des images, leur résolution ou la durée des vidéos.

[5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id715-marker)Les principes fondamentaux de l'apprentissage automatique liés à l'entraînement des modèles ne sont pas abordés dans cet ouvrage. Cependant, lorsque cela s'avère pertinent, certains concepts sont évoqués. Par exemple, l'auto-supervision (où un modèle génère ses propres étiquettes à partir des données) est traitée au [chapitre 1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_introduction_to_building_ai_applications_with_foun_1730130814984319) , et la rétropropagation (comment les paramètres d'un modèle sont mis à jour pendant l'entraînement en fonction de l'erreur) est abordée au [chapitre 7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) .

[6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id719-marker)Les réseaux de neurones récurrents (RNN) sont particulièrement sensibles à la disparition et à l'explosion des gradients en raison de leur structure récursive. Les gradients doivent être propagés à travers de nombreuses étapes, et s'ils sont faibles, les multiplications répétées les font tendre vers zéro, ce qui rend l'apprentissage difficile pour le modèle. Inversement, si les gradients sont importants, ils croissent exponentiellement à chaque étape, ce qui entraîne une instabilité du processus d'apprentissage.

[7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id720-marker)Bahdanau et al., [« Traduction automatique neuronale par apprentissage conjoint de l’alignement et de la traduction »](https://arxiv.org/abs/1409.0473) .

[8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id727-marker)Étant donné que les jetons d'entrée sont traités par lots, le vecteur d'entrée réel a la forme `N`× `T`× `4096`, où `N`est la taille du lot et T la longueur de la séquence. De même, chaque vecteur résultant `K`, `V`, `Q`a la dimension de `N`× `T`× `4096`.

[9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id739-marker)Pourquoi des fonctions d'activation simples fonctionnent-elles pour des modèles complexes comme les LLM ? À une époque, la communauté de recherche s'est efforcée de concevoir des fonctions d'activation sophistiquées. Or, il s'est avéré que des fonctions plus élaborées n'étaient pas plus performantes. Le modèle a simplement besoin d'une fonction non linéaire pour rompre la linéarité des couches de propagation avant. Des fonctions plus simples et plus rapides à calculer sont préférables, car les plus sophistiquées consomment trop de ressources de calcul et de mémoire pour l'entraînement.

[10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id744-marker)Anecdote amusante : Ilya Sutskever, cofondateur d’OpenAI, est le premier auteur de l’article seq2seq et le deuxième auteur de l’article AlexNet.

[11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id745-marker)Ilya Sutskever avance un argument intéressant expliquant pourquoi il est si difficile de développer de nouvelles architectures de réseaux neuronaux plus performantes que les existantes. Selon lui, les réseaux neuronaux excellent dans la simulation de nombreux programmes informatiques. La descente de gradient, une technique d'entraînement des réseaux neuronaux, est en réalité un algorithme de recherche qui explore tous les programmes qu'un réseau neuronal peut simuler afin de trouver le plus adapté à sa tâche cible. Cela signifie que les nouvelles architectures peuvent potentiellement être simulées par les architectures existantes. Pour surpasser les existantes, les nouvelles architectures doivent être capables de simuler des programmes que les architectures existantes ne peuvent pas. Pour plus d'informations, visionnez [la conférence de Sutskever au Simons Institute de Berkeley (2023)](https://oreil.ly/j4wwW) .

[12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id746-marker)Le transformateur a été initialement conçu par Google pour [fonctionner rapidement sur des unités de traitement tensoriel (TPU)](https://oreil.ly/ON55d) , et n'a été optimisé sur les GPU que plus tard.

[13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id754-marker)La mémoire réellement nécessaire est plus importante. [Le chapitre 7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) explique comment calculer l'utilisation de la mémoire d'un modèle.

[14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id759-marker)En supposant qu'un livre contienne environ 50 000 mots ou 67 000 jetons.

[15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id760-marker)À l'heure actuelle, les grands modèles sont généralement pré-entraînés sur une seule époque de données.

[16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id762-marker)Le nombre de FLOP/s est mesuré en FP32. Les formats à virgule flottante sont abordés au [chapitre 7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) .

[17](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id763-marker)À l'heure actuelle, les fournisseurs de services cloud proposent des serveurs H100 pour environ 2 à 5 dollars de l'heure. Avec la baisse rapide du coût de la puissance de calcul, ce tarif diminuera considérablement.

[18](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id776-marker)Jascha Sohl-Dickstein, un chercheur exceptionnel, [a partagé une magnifique visualisation des hyperparamètres qui fonctionnent et de ceux qui ne fonctionnent pas](https://x.com/jaschasd/status/1756930242965606582) sur sa page X.

[19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id777-marker) [Dario Amodei, PDG d'Anthropic](https://oreil.ly/GxSe0) , a déclaré que si l'hypothèse de mise à l'échelle est vraie, un modèle d'IA de 100 milliards de dollars sera aussi performant qu'un lauréat du prix Nobel.

[20](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id778-marker)Le contenu généré par l'IA est amplifié par la facilité de la traduction automatique. L'IA peut être utilisée pour générer un article, puis le traduire dans plusieurs langues, comme le montre l'étude « Une quantité choquante de contenu web est traduite par machine » ( [Thompson et al., 2024](https://arxiv.org/abs/2401.05749) ).

[21](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id787-marker)Un ami a utilisé cette analogie : un modèle pré-entraîné parle comme une page web, pas comme un humain.

[22](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id790-marker)Les principes fondamentaux du RL dépassent le cadre de cet ouvrage, mais l'essentiel est que le RL permet d'optimiser en fonction d'objectifs difficiles comme les préférences humaines.

[23](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id797-marker)Il existe des situations où des modèles non adaptés peuvent s'avérer plus pertinents. Par exemple, pour évaluer le risque que des individus utilisent l'IA pour diffuser de la désinformation, il peut être judicieux de concevoir un modèle capable de générer le plus de fausses informations possible, afin d'observer le degré de conviction de l'IA.

[24](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id816-marker)Lorsque je pense à la température, une image visuelle qui me vient à l'esprit, et qui n'est pas tout à fait scientifique, est celle d'une température plus élevée qui rend la distribution des probabilités plus chaotique, ce qui permet aux jetons à faible probabilité de faire surface.

[25](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id817-marker)Exécution d'une [fonction arg max](https://en.wikipedia.org/wiki/Arg_max) .

[26](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id819-marker)Le problème de dépassement de capacité négatif survient lorsqu'un nombre est trop petit pour être représenté dans un format donné, ce qui entraîne son arrondi à zéro.

[27](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id820-marker)Plus précisément, à l'heure actuelle, l'API OpenAI n'affiche que les [probabilités logarithmiques](https://oreil.ly/jWEsP) des 20 jetons les plus probables. Auparavant, elle permettait d'obtenir les probabilités logarithmiques de n'importe quel texte fourni par l'utilisateur, mais cette fonctionnalité a été supprimée en [septembre 2023.](https://x.com/xuanalogue/status/1707757449900437984) Anthropic ne divulgue pas les probabilités logarithmiques de ses modèles.

[28](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id829-marker)Les API de modèles payantes facturent souvent en fonction du nombre de jetons de sortie.

[29](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id833-marker)Il existe des solutions pour réduire le coût de génération de plusieurs sorties à partir d'une même entrée. Par exemple, l'entrée peut être traitée une seule fois et réutilisée pour toutes les sorties.

[30](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id835-marker)Au moment de la rédaction de ce document, dans l'API OpenAI, vous pouvez définir le paramètre [best_of](https://oreil.ly/XYugZ) sur une valeur spécifique, par exemple 10, pour demander aux modèles OpenAI de renvoyer la sortie avec la probabilité logarithmique moyenne la plus élevée parmi 10 sorties différentes.

[31](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id836-marker) [Wang et al. (2023)](https://arxiv.org/abs/2203.11171) ont appelé cette approche auto-cohérence.

[32](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id838-marker)La meilleure solution face à un modèle fragile est toutefois de le remplacer par un autre.

[33](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id844-marker)Au moment où j'écris ces lignes, selon l'application et le modèle, j'ai constaté que le pourcentage d'objets JSON correctement générés pouvait varier entre 0 % et près de 90 %.

[34](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id849-marker)Entraîner un modèle à partir de zéro sur des données suivant le format souhaité fonctionne également, mais ce livre ne traite pas du développement de modèles à partir de zéro.

[35](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id850-marker)Certains services de réglage fin le font automatiquement. [Les services de réglage fin d'OpenAI](https://oreil.ly/sljei) permettaient auparavant d'ajouter une tête de classifieur lors de l'entraînement, mais cette fonctionnalité a été désactivée depuis.

[36](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id857-marker)Comme le dit le mème, [les chances sont faibles, mais jamais nulles](https://x.com/OxfordDiplomat/status/1424388443010998277?lang=en) .

[37](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#id858-marker)En décembre 2023, j'ai analysé trois mois de demandes d'assistance client pour une entreprise d'IA que je conseillais et j'ai constaté qu'un cinquième des questions portaient sur la gestion de l'incohérence des modèles d'IA. Lors d'une table ronde à laquelle j'ai participé avec Drew Houston (PDG de Dropbox) et Harrison Chase (PDG de LangChain) en juillet 2023, nous avons tous convenu que les hallucinations constituaient le principal obstacle à de nombreux cas d'utilisation de l'IA en entreprise.