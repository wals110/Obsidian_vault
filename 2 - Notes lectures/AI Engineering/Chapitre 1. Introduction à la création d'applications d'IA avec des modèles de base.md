Si je ne devais utiliser qu'un seul mot pour décrire l'IA après 2020, ce serait _« échelle »_ . Les modèles d'IA qui sous-tendent des applications comme ChatGPT, Gemini de Google et Midjourney sont d'une telle ampleur qu'ils consomment [une part non négligeable](https://oreil.ly/J0IyO) de l'électricité mondiale, et nous risquons de [manquer de données publiques disponibles sur Internet](https://arxiv.org/abs/2211.04325) pour les entraîner.

Le passage à l'échelle supérieure des modèles d'IA a deux conséquences majeures. Premièrement, ces modèles deviennent plus puissants et capables d'accomplir davantage de tâches, ce qui permet de multiplier les applications. De plus en plus de personnes et d'équipes tirent parti de l'IA pour accroître leur productivité, créer de la valeur économique et améliorer leur qualité de vie.

Deuxièmement, l'entraînement de grands modèles de langage (GML) exige des données, des ressources de calcul et des talents spécialisés que seules quelques organisations peuvent se permettre. Ceci a conduit à l'émergence du _modèle en tant que service_ (MaaS) : les modèles développés par ces quelques organisations sont mis à la disposition d'autres utilisateurs. Quiconque souhaite exploiter l'IA pour créer des applications peut désormais utiliser ces modèles sans avoir à investir initialement dans leur développement.

En résumé, la demande d'applications d'IA a augmenté tandis que les barrières à l'entrée pour leur développement ont diminué. De ce fait, _l'ingénierie de l'IA_ — le processus de création d'applications à partir de modèles existants — est devenue l'une des disciplines d'ingénierie connaissant la croissance la plus rapide.

Le développement d'applications basées sur des modèles d'apprentissage automatique (ML) n'est pas nouveau. Bien avant l'essor des modèles d'apprentissage automatique (LLM), l'IA était déjà au cœur de nombreuses applications, notamment les recommandations de produits, la détection des fraudes et la prédiction du taux de désabonnement. Si de nombreux principes de mise en production des applications d'IA restent inchangés, la nouvelle génération de modèles à grande échelle et facilement accessibles ouvre de nouvelles perspectives et soulève de nouveaux défis, qui sont au cœur de cet ouvrage.

Ce chapitre débute par une présentation des modèles fondamentaux, catalyseur essentiel de l'essor de l'ingénierie de l'IA. J'aborderai ensuite divers cas d'utilisation réussis de l'IA, illustrant ses points forts et ses limites actuelles. Face à l'expansion quotidienne des capacités de l'IA, prédire ses applications futures devient un défi de plus en plus complexe. Toutefois, l'analyse des applications existantes peut révéler des opportunités dès aujourd'hui et fournir des indications sur les usages futurs possibles de l'IA.

Pour conclure ce chapitre, je présenterai un aperçu de la nouvelle architecture d'IA, notamment les changements apportés aux modèles de base, les éléments restés inchangés et les différences entre le rôle d'un ingénieur en IA aujourd'hui et celui d'un ingénieur en apprentissage automatique traditionnel [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id534)

# L'essor de l'ingénierie de l'IA

Les modèles de base sont issus de grands modèles de langage, eux-mêmes initialement conçus comme de simples modèles de langage. Si des applications comme ChatGPT et Copilot de GitHub peuvent sembler avoir surgi de nulle part, elles sont l'aboutissement de décennies de progrès technologiques, les premiers modèles de langage ayant vu le jour dans les années 1950. Cette section retrace les avancées majeures qui ont permis le passage des modèles de langage à l'ingénierie de l'IA.

## Des modèles de langage aux grands modèles de langage

Bien que les modèles de langage existent depuis un certain temps, leur développement actuel n'a été possible qu'avec _l'auto-supervision._ Cette section présente brièvement les concepts de modèle de langage et d'auto-supervision. Si vous les maîtrisez déjà, vous pouvez passer cette section.

### Modèles de langage

Un _modèle de langage_ encode des informations statistiques sur une ou plusieurs langues. Intuitivement, ces informations nous indiquent la probabilité d'apparition d'un mot dans un contexte donné. Par exemple, dans le contexte « Ma couleur préférée est __ », un modèle de langage qui encode l'anglais devrait prédire « bleu » plus souvent que « voiture ».

La nature statistique des langues a été découverte il y a des siècles. Dans la nouvelle de 1905 [« L'Aventure des hommes dansants »](https://en.wikipedia.org/wiki/The_Adventure_of_the_Dancing_Men) , Sherlock Holmes utilise des informations statistiques simples sur l'anglais pour déchiffrer des séquences de mystérieux bonshommes bâtons. Puisque la lettre la plus fréquente en anglais est _le E_ , Holmes en déduit que le bonhomme bâton le plus fréquent représente forcément le _E._

Plus tard, Claude Shannon a utilisé des statistiques plus sophistiquées pour déchiffrer les messages ennemis pendant la Seconde Guerre mondiale. Ses travaux sur la modélisation de l'anglais ont été publiés en 1951 dans son article fondateur intitulé [« Prediction and Entropy of Printed English »](https://oreil.ly/G_HBp) . De nombreux concepts introduits dans cet article, notamment l'entropie, sont encore utilisés aujourd'hui pour la modélisation du langage.

À l'origine, un modèle de langage ne concernait qu'une seule langue. Cependant, aujourd'hui, un modèle de langage peut en concerner plusieurs.

L'unité de base d'un modèle de langage est _le token_ . Un token peut être un caractère, un mot ou une partie de mot (comme -tion), selon le modèle. Par [exemple](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id536) , GPT-4, un modèle utilisé par ChatGPT, décompose la phrase « I can't wait to build AI applications » en neuf tokens, comme illustré dans [la figure 1-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_1_1730130814919858) . Notez que dans cet exemple, le mot « can't » est décomposé en deux tokens : _« can_ » et _« 't »_ . Vous pouvez observer comment différents modèles OpenAI tokenisent le texte sur le [site web d'OpenAI](https://oreil.ly/0QI91) .

![Gros plan d'un panneau. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0101.png)

###### Figure 1-1. Un exemple de la façon dont GPT-4 tokenise une phrase.

Le processus de décomposition du texte original en jetons est appelé _tokenisation_ . Pour GPT-4, un jeton mesure en moyenne environ [les trois quarts de la longueur d'un mot](https://oreil.ly/EYccr) . Ainsi, 100 jetons correspondent à environ 75 mots.

L'ensemble des jetons qu'un modèle peut traiter constitue son _vocabulaire_ . Un petit nombre de jetons permet de former un grand nombre de mots distincts, à l'instar des quelques lettres de l'alphabet qui permettent de former de nombreux mots. Le modèle [Mixtral 8x7B](https://oreil.ly/bxMcW) possède un vocabulaire de 32 000 jetons. Celui de GPT-4 compte [100 256 jetons](https://github.com/openai/tiktoken/blob/main/tiktoken/model.py) . La méthode de tokenisation et la taille du vocabulaire sont définies par les développeurs du modèle.

###### Note

Pourquoi les modèles de langage utilisent-ils _le token_ comme unité plutôt que _le mot_ ou _le caractère_ ? Il y a trois raisons principales :

1. Contrairement aux caractères, les tokens permettent au modèle de décomposer les mots en composants significatifs. Par exemple, « cooking » peut être décomposé en « cook » et « ing », chacun de ces composants véhiculant une partie du sens du mot original.
    
2. Comme il y a moins de jetons uniques que de mots uniques, cela réduit la taille du vocabulaire du modèle, ce qui rend le modèle plus efficace (comme expliqué au [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) ).
    
3. Les tokens aident également le modèle à traiter les mots inconnus. Par exemple, un mot inventé comme « chatgpting » pourrait être décomposé en « chatgpt » et « ing », ce qui permet au modèle de comprendre sa structure. Les tokens offrent un bon compromis : moins d’unités que les mots, tout en conservant plus de sens que les caractères individuels.
    

Il existe deux principaux types de modèles de langage : _les modèles de langage masqués_ et _les modèles de langage autorégressifs_ . Ils diffèrent selon les informations qu’ils peuvent utiliser pour prédire un jeton :

Modèle de langage masqué

Un modèle de langage masqué est entraîné à prédire les jetons manquants dans une séquence, _en utilisant le contexte des jetons précédents et suivants_ . En d'autres termes, il est entraîné à compléter les blancs. Par exemple, dans le contexte « Ma couleur préférée est bleue », un modèle de langage masqué devrait prédire que le mot manquant est probablement « couleur ». Un exemple bien connu de modèle de langage masqué est BERT ( [Devlin et al., 2018](https://arxiv.org/abs/1810.04805) ).

À l'heure actuelle, les modèles de langage masqués sont couramment utilisés pour des tâches non génératives telles que l'analyse des sentiments et la classification de textes. Ils sont également utiles pour des tâches nécessitant une compréhension du contexte global, comme le débogage de code, où un modèle doit comprendre à la fois le code précédent et suivant pour identifier les erreurs.

Modèle de langage autorégressif

Un modèle de langage autorégressif est entraîné à prédire le jeton suivant dans une séquence, _en utilisant uniquement les jetons précédents_ . Il prédit ce qui suit dans « Ma couleur préférée est __ [»](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id541) .³ _Un modèle autorégressif peut générer continuellement un jeton après l'autre. Aujourd'hui, les modèles de langage autorégressifs sont les modèles de prédilection pour la génération_ [de](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id542) texte et, pour cette raison, ils sont beaucoup plus populaires que les modèles de langage masqués.⁴[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id541)[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id542)

[La figure 1-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_2_1730130814919894) illustre ces deux types de modèles de langage.

![Diagramme d'une grille de mots croisés de poulet. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0102.png)

###### Figure 1-2. Modèle de langage autorégressif et modèle de langage masqué.

###### Note

Dans cet ouvrage, sauf indication contraire, _le terme « modèle de langage »_ désignera un modèle autorégressif.

Les résultats des modèles de langage sont ouverts. Un modèle de langage peut utiliser son vocabulaire fixe et fini pour construire une infinité de résultats possibles. Un modèle capable de générer des résultats ouverts est dit _génératif_ , d'où le terme _d'intelligence artificielle générative_ .

On peut considérer un modèle de langage comme une _machine à compléter_ : étant donné un texte (une invite), il tente de le compléter. Voici un exemple :
	
```
_Invite (de l'utilisateur)_ : "Être ou ne pas être"
 _Complétion (du modèle de langage)_ : ", telle est la question."
```

Il est important de noter que les complétions sont des prédictions, basées sur des probabilités, et ne sont pas garanties correctes. Cette nature probabiliste des modèles de langage les rend à la fois passionnants et frustrants à utiliser. Nous approfondirons ce point au [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) .

Aussi simple que cela puisse paraître, la complétion est incroyablement puissante. De nombreuses tâches, comme la traduction, la synthèse, la programmation et la résolution de problèmes mathématiques, peuvent être formulées comme des tâches de complétion. Par exemple, face à la consigne : « Comment ça va en français ? », un modèle de langage pourrait la compléter par : « Comment ça va ? », traduisant ainsi d’une langue à l’autre.

À titre d'exemple supplémentaire, étant donné l'invite :


```
Question : Ce courriel est-il probablement un spam ? Voici le courriel : <contenu du courriel>
Répondre:
```



Un modèle de langage pourrait le compléter par : « Probablement du spam », ce qui transforme ce modèle de langage en un classificateur de spam.

Bien que la complétion automatique soit un outil puissant, elle ne remplace pas une conversation. Par exemple, si vous posez une question à un système de complétion automatique, celui-ci peut compléter votre propos en ajoutant une autre question au lieu de répondre directement. La section [« Post-entraînement »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_post_training_1730147895572108) explique comment faire en sorte qu'un modèle réponde de manière appropriée à la requête d'un utilisateur.

### Auto-surveillance

La modélisation du langage n'est qu'un algorithme d'apprentissage automatique parmi tant d'autres. Il existe également des modèles pour la détection d'objets, la modélisation thématique, les systèmes de recommandation, les prévisions météorologiques, la prédiction des cours boursiers, etc. Qu'est-ce qui rend les modèles de langage si particuliers et qui les a placés au cœur de l'approche de mise à l'échelle ayant donné naissance au phénomène ChatGPT ?

La réponse est que les modèles de langage peuvent être entraînés par _auto-supervision_ , tandis que de nombreux autres modèles nécessitent _une supervision_ . La supervision désigne le processus d'entraînement des algorithmes d'apprentissage automatique à l'aide de données étiquetées, une opération souvent coûteuse et longue à obtenir. L'auto-supervision permet de surmonter cette difficulté d'étiquetage des données et de créer des ensembles de données plus vastes pour l'apprentissage des modèles, ce qui leur permet d'accroître leur capacité. Voici comment.

L'apprentissage supervisé consiste à étiqueter des exemples pour illustrer les comportements que le modèle doit apprendre, puis à entraîner le modèle sur ces exemples. Une fois entraîné, le modèle peut être appliqué à de nouvelles données. Par exemple, pour entraîner un modèle de détection de fraude, on utilise des exemples de transactions, chacune étiquetée « fraude » ou « non-fraude ». Une fois que le modèle a appris de ces exemples, on peut l'utiliser pour prédire si une transaction est frauduleuse.

Le succès des modèles d'IA dans les années 2010 reposait sur la supervision. AlexNet ( [Krizhevsky et al., 2012](https://oreil.ly/WEQFj) ), le modèle à l'origine de la révolution du deep learning, était supervisé. Il a été entraîné à classifier plus d'un million d'images de la base de données ImageNet, chaque image étant classée dans l'une des 1 000 catégories telles que « voiture », « ballon » ou « singe ».

L'un des inconvénients de la supervision est que l'étiquetage des données est coûteux et chronophage. Si l'étiquetage d'une image coûte 5 centimes par personne, l'étiquetage d'un million d'images pour ImageNet coûterait 50 000 $. [Si](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id545) l'on souhaite que deux personnes différentes étiquettent chaque image – afin de vérifier la qualité des étiquettes – le coût serait doublé. Le monde contenant bien plus de 1 000 objets, étendre les capacités des modèles à un plus grand nombre d'objets nécessiterait d'ajouter des étiquettes à davantage de catégories. Pour atteindre un million de catégories, le coût de l'étiquetage à lui seul atteindrait 50 millions de dollars.

Étiqueter les objets du quotidien est une tâche que la plupart des gens peuvent accomplir sans formation préalable. Par conséquent, elle peut être réalisée à un coût relativement faible. Cependant, toutes les tâches d'étiquetage ne sont pas aussi simples. Générer des traductions latines pour un modèle anglais-latin est plus onéreux. Indiquer si un scanner révèle des signes de cancer coûterait une fortune.

L'auto-supervision permet de surmonter les difficultés liées à l'étiquetage des données. En auto-supervision, au lieu d'exiger des étiquettes explicites, le modèle peut les inférer à partir des données d'entrée. La modélisation du langage est auto-supervisée car chaque séquence d'entrée fournit à la fois les étiquettes (les jetons à prédire) et les contextes que le modèle peut utiliser pour les prédire. Par exemple, la phrase « J'adore la street food » fournit six exemples d'entraînement, comme illustré dans [le tableau 1-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_table_1_1730130814941480) .

Tableau 1-1. Exemples d'entraînement tirés de la phrase « J'adore la street food. » pour la modélisation du langage.

|Entrée (contexte)|Sortie (jeton suivant)|
|---|---|
|`<BOS>`|`I`|
|`<BOS>, I`|`love`|
|`<BOS>, I, love`|`street`|
|`<BOS>, I, love, street`|`food`|
|`<BOS>, I, love, street, food`|`.`|
|`<BOS>, I, love, street, food, .`|`<EOS>`|

Dans le tableau 1-1 , 'BOS' et 'EOS' marquent le début et la fin d'une séquence. Ces marqueurs sont nécessaires au modèle de langage pour traiter plusieurs séquences. Chaque marqueur est généralement traité comme un jeton spécial par le modèle. Le marqueur de fin de séquence est particulièrement important car il aide les modèles de langage à savoir quand terminer leurs réponses.

###### Note

L'apprentissage auto-supervisé diffère de l'apprentissage non supervisé. En apprentissage auto-supervisé, les étiquettes sont déduites des données d'entrée. En apprentissage non supervisé, aucune étiquette n'est nécessaire.

L'apprentissage auto-supervisé permet aux modèles de langage d'apprendre à partir de séquences de texte sans aucun étiquetage préalable. Comme les séquences de texte sont omniprésentes (livres, billets de blog, articles, commentaires Reddit), il est possible de constituer une quantité massive de données d'entraînement, permettant ainsi aux modèles de langage de devenir des LLM (Language Models).

LLM, cependant, n'est pas vraiment un terme scientifique. Quelle doit être la taille d'un modèle de langage pour être considéré _comme « grand »_ ? Ce qui est grand aujourd'hui pourrait être considéré comme minuscule demain. La taille d'un modèle est généralement mesurée par son nombre de paramètres. Un _paramètre_ est une variable au sein d'un modèle d'apprentissage automatique qui est mise à jour au cours du processus d'entraînement. En général, bien que cela ne soit pas toujours vrai, plus un modèle a de paramètres, plus sa capacité à apprendre les comportements souhaités [est](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id547) grande.

Lors de la sortie du premier modèle GPT (Generative Pre-Trained Transformer) d'OpenAI en juin 2018, celui-ci comptait 117 millions de paramètres, un chiffre alors considéré comme important. En février 2019, avec le lancement de GPT-2 et ses 1,5 milliard de paramètres, ce chiffre de 117 millions a été revu à la baisse et est désormais considéré comme faible. À l'heure où j'écris ces lignes, un modèle à 100 milliards de paramètres est considéré comme important. Peut-être qu'un jour, cette taille sera considérée comme faible.

Avant de passer à la section suivante, j'aimerais aborder une question souvent considérée comme allant de soi : _pourquoi les grands modèles ont-ils besoin de plus de données ?_ Les grands modèles ont une plus grande capacité d'apprentissage et, par conséquent, nécessitent davantage de données d'entraînement pour optimiser leurs performances. On peut [certes](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id549) entraîner un grand modèle sur un petit ensemble de données, mais ce serait un gaspillage de ressources de calcul. On aurait pu obtenir des résultats similaires, voire meilleurs, sur cet ensemble de données avec des modèles plus petits..

## Des grands modèles de langage aux modèles de base

Bien que les modèles de langage soient capables de prouesses incroyables, ils se limitent au texte. En tant qu'êtres humains, nous percevons le monde non seulement par le langage, mais aussi par la vue, l'ouïe, le toucher, et bien d'autres moyens. La capacité à traiter des données autres que le texte est essentielle pour que l'IA puisse opérer dans le monde réel.

C’est pourquoi les modèles de langage sont étendus afin d’intégrer davantage de modalités de données. GPT-4V et Claude 3 peuvent comprendre des images et des textes. Certains modèles comprennent même des vidéos, des ressources 3D, des structures protéiques, etc. L’intégration de davantage de modalités de données aux modèles de langage les rend encore plus performants. OpenAI [a noté dans sa fiche système GPT-4V](https://oreil.ly/NoGX7) en 2023 que « l’intégration de modalités supplémentaires (telles que les entrées d’image) aux modèles de langage est considérée par certains comme un axe de recherche et de développement majeur en IA ».

Bien que beaucoup continuent de qualifier Gemini et GPT-4V de modèles linéaires étendus (LLM), il serait plus juste de les considérer comme [_des modèles de base_](https://arxiv.org/abs/2108.07258) . Le terme _« base »_ souligne à la fois l’importance de ces modèles dans les applications d’IA et leur capacité à être développés pour répondre à différents besoins.

Les modèles de base marquent une rupture avec la structure traditionnelle de la recherche en IA. Pendant longtemps, cette recherche a été segmentée selon les modalités de données. Le traitement automatique du langage naturel (TALN) ne traite que du texte, tandis que la vision par ordinateur ne traite que des données visuelles. Les modèles textuels peuvent être utilisés pour des tâches telles que la traduction et la détection de spams. Les modèles d'images peuvent servir à la détection d'objets et à la classification d'images. Enfin, les modèles audio peuvent gérer la reconnaissance vocale (transcription vocale) et la synthèse vocale (synthèse vocale).

Un modèle capable de traiter plusieurs modalités de données est également appelé _modèle multimodal._ Un modèle multimodal génératif est aussi appelé modèle multimodal étendu (LMM). Si un modèle de langage génère le jeton suivant en fonction des jetons textuels uniquement, un modèle multimodal le génère en fonction des jetons textuels et image, ou de toute autre modalité prise en charge par le modèle, comme illustré dans [la figure 1-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_3_1730130814919919) .

![Diagramme d'un modèle. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0103.png)

###### Figure 1-3. Un modèle multimodal peut générer le jeton suivant en utilisant des informations provenant à la fois de jetons textuels et visuels.

Tout comme les modèles de langage, les modèles multimodaux ont besoin de données pour passer à l'échelle supérieure. L'auto-supervision fonctionne également pour les modèles multimodaux.Par exemple, OpenAI a utilisé une variante d'auto-supervision appelée _supervision du langage naturel_ pour entraîner son modèle texte-image [CLIP (OpenAI, 2021)](https://oreil.ly/zcqdu) . Au lieu d'étiqueter manuellement chaque image, ils ont recherché des paires (image, texte) fréquemment rencontrées sur Internet. Ils ont ainsi pu générer un ensemble de données de 400 millions de paires (image, texte), soit 400 fois plus important qu'ImageNet, sans aucun étiquetage manuel. Cet ensemble de données a permis à CLIP de devenir le premier modèle capable de généraliser à de multiples tâches de classification d'images sans nécessiter d'entraînement supplémentaire.

###### Note

Cet ouvrage utilise le terme « modèles de base » pour désigner à la fois les grands modèles de langage et les grands modèles multimodaux.

Notez que CLIP n'est pas un modèle génératif — il n'a pas été entraîné à générer des sorties ouvertes.CLIP est un _modèle d'embedding_ , entraîné à produire des embeddings conjoints de textes et d'images. [L'article « Introduction à l'embedding »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_introduction_to_embedding_1730150757064669) aborde les embeddings en détail. Pour l'instant, considérez les embeddings comme des vecteurs visant à capturer le sens des données originales. Les modèles d'embeddings multimodaux comme CLIP constituent la base des modèles multimodaux génératifs, tels que Flamingo, LLaVA et Gemini (anciennement Bard).

Les modèles de base marquent également la transition des modèles dédiés à une tâche spécifique vers des modèles à usage général. Auparavant, les modèles étaient souvent développés pour des tâches précises, telles que l'analyse des sentiments ou la traduction. Un modèle entraîné pour l'analyse des sentiments ne pouvait pas effectuer de traduction, et inversement.

_Les modèles de base, grâce à leur taille et à leur méthode d'entraînement, sont capables de réaliser un large éventail de tâches._ Dès leur mise en service, les modèles généralistes offrent des performances relativement bonnes pour de nombreuses tâches. Un modèle linéaire généraliste (LLM) peut effectuer à la fois l'analyse des sentiments et la traduction. Cependant, il est souvent possible d'optimiser un modèle généraliste pour maximiser ses performances sur une tâche spécifique.

[La figure 1-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_4_1730130814919937) montre les tâches utilisées par le benchmark Super-NaturalInstructions pour évaluer les modèles de base ( [Wang et al., 2022](https://arxiv.org/abs/2204.07705) ), donnant une idée des types de tâches qu'un modèle de base peut effectuer.

Imaginez que vous collaborez avec un détaillant pour développer une application de génération de descriptions de produits pour son site web. Un modèle standard pourrait certes générer des descriptions précises, mais risquerait de ne pas refléter l'identité de la marque ni de mettre en valeur son message. Les descriptions générées pourraient même être truffées de jargon marketing et de clichés.

![Diagramme de cercles de différentes couleurs. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0104.png)

###### Figure 1-4. La gamme de tâches dans le benchmark Super-NaturalInstructions (Wang et al., 2022).

Il existe plusieurs techniques pour que le modèle génère les descriptions souhaitées. Par exemple, vous pouvez rédiger des instructions détaillées accompagnées d'exemples de descriptions de produits idéales. Cette approche est _appelée ingénierie des instructions_ . Vous pouvez également connecter le modèle à une base de données d'avis clients afin qu'il puisse générer de meilleures descriptions. L'utilisation d'une base de données pour compléter les instructions est appelée _génération augmentée par extraction_ (RAG). Enfin, vous pouvez _affiner_ le modèle (l'entraîner davantage) sur un ensemble de données de descriptions de produits de haute qualité.

L'ingénierie rapide, RAG et le réglage fin sont trois techniques d'ingénierie IA très courantes permettant d'adapter un modèle à vos besoins. La suite de cet ouvrage les abordera en détail.

Adapter un modèle performant existant à votre tâche est généralement beaucoup plus simple que de créer un modèle de toutes pièces : par exemple, dix exemples et un week-end contre un million d’exemples et six mois. Les modèles de base permettent de réduire les coûts de développement des applications d’IA et d’accélérer leur mise sur le marché. La quantité exacte de données nécessaire à l’adaptation d’un modèle dépend de la technique utilisée. Cet ouvrage abordera également cette question lors de la présentation de chaque technique. Toutefois, les modèles spécifiques à une tâche présentent de nombreux avantages : ils sont souvent beaucoup plus petits, ce qui les rend plus rapides et moins coûteux à utiliser.

Le choix entre créer son propre modèle ou utiliser un modèle existant est une question classique d'achat ou de développement interne à laquelle les équipes devront répondre. Les discussions tout au long du livre peuvent les aider à prendre cette décision.

## Des modèles fondamentaux à l'ingénierie de l'IA

_ingénierie de l'IA_ L'ingénierie de l'IA désigne le processus de création d'applications à partir de modèles de base. Le développement d'applications d'IA existe depuis plus de dix ans ; ce processus est souvent appelé ingénierie ML ou MLOps (pour opérations ML). Pourquoi parle-t-on d'ingénierie de l'IA maintenant ?

Si l'ingénierie traditionnelle du ML consiste à développer des modèles de ML, l'ingénierie de l'IA exploite ceux existants. La disponibilité et l'accessibilité de modèles de base performants engendrent trois facteurs qui, ensemble, créent les conditions idéales pour la croissance rapide de l'ingénierie de l'IA en tant que discipline :

Facteur 1 : Capacités d’IA à usage général

Les modèles de base sont puissants non seulement parce qu'ils améliorent les tâches existantes, mais aussi parce qu'ils peuvent en accomplir davantage. Des applications autrefois jugées impossibles sont désormais possibles, et de nouvelles applications inédites émergent. Même des applications considérées comme impossibles aujourd'hui pourraient devenir possibles demain. L'IA devient ainsi plus utile dans de nombreux aspects de la vie, ce qui accroît considérablement le nombre d'utilisateurs et la demande d'applications d'IA.

Par exemple, l'IA étant désormais capable d'écrire aussi bien que les humains, voire mieux, elle peut automatiser, totalement ou partiellement, toutes les tâches nécessitant une communication, c'est-à-dire quasiment tout. Elle est utilisée pour rédiger des courriels, répondre aux demandes des clients et expliquer des contrats complexes. Toute personne possédant un ordinateur a accès à des outils permettant de générer instantanément des images et des vidéos personnalisées de haute qualité pour créer des supports marketing, retoucher des photos professionnelles, visualiser des concepts artistiques, illustrer des livres, etc. L'IA peut même servir à synthétiser des données d'entraînement, à développer des algorithmes et à écrire du code, autant d'éléments qui contribueront à l'entraînement de modèles encore plus performants à l'avenir.

Facteur 2 : Augmentation des investissements dans l’IA

Le succès de ChatGPT a entraîné une forte hausse des investissements dans l'IA, tant de la part des sociétés de capital-risque que des entreprises. À mesure que les applications d'IA deviennent moins coûteuses à développer et plus rapides à commercialiser, le retour sur investissement dans ce domaine devient plus attractif. Les entreprises s'empressent d'intégrer l'IA à leurs produits et processus. Matt Ross, responsable de la recherche appliquée chez Scribd, m'a indiqué que le coût estimé de l'IA pour ses cas d'utilisation a été divisé par cent entre avril 2022 et avril 2023.

[Goldman Sachs Research](https://oreil.ly/okMw6) estime que les investissements dans l'IA pourraient atteindre près de 100 milliards de dollars aux États-Unis et 200 milliards de dollars à l'échelle mondiale d'ici 2025. [L'](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id561) IA est souvent citée comme un avantage concurrentiel. [FactSet](https://oreil.ly/tgm-a) a constaté qu'une entreprise du S&P 500 sur trois a mentionné l'IA lors de sa conférence téléphonique sur les résultats du deuxième trimestre 2023, soit trois fois plus que l'année précédente. [La figure 1-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_5_1730130814919959) illustre le nombre d'entreprises du S&P 500 ayant mentionné l'IA lors de leurs conférences téléphoniques sur les résultats entre 2018 et 2023.

![Un graphique avec des nombres et des lignes. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0105.png)

###### Figure 1-5. Le nombre de sociétés du S&P 500 qui mentionnent l'IA dans leurs conférences téléphoniques sur les résultats a atteint un niveau record en 2023. Données de FactSet.

D'après WallStreetZen, les entreprises ayant évoqué l'IA lors de leurs conférences téléphoniques sur les résultats ont vu leur cours boursier progresser davantage que celles qui ne l'ont pas fait : [une hausse moyenne de 4,6 % contre 2,4 %](https://oreil.ly/fK5uh) . Il est difficile de déterminer s'il s'agit d'une relation de cause à effet (l'IA contribuant au succès de ces entreprises) ou d'une simple corrélation (leur réussite s'explique par leur capacité d'adaptation rapide aux nouvelles technologies).

Facteur 3 : Faible barrière à l’entrée pour le développement d’applications d’IA

L'approche « modèle en tant que service » popularisée par OpenAI et d'autres fournisseurs de modèles facilite l'utilisation de l'IA pour le développement d'applications. Dans ce modèle, les modèles sont exposés via des API qui reçoivent les requêtes des utilisateurs et renvoient les résultats. Sans ces API, l'utilisation d'un modèle d'IA nécessiterait une infrastructure dédiée pour l'héberger et le déployer. Ces API permettent d'accéder à des modèles performants via de simples appels.

De plus, l'IA permet de créer des applications avec un minimum de code. Premièrement, elle peut écrire le code pour vous, permettant ainsi à des personnes sans formation en génie logiciel de transformer rapidement leurs idées en code et de les proposer à leurs utilisateurs. Deuxièmement, vous pouvez interagir avec ces modèles en langage naturel, sans avoir à utiliser de langage de programmation. _N'importe qui, absolument n'importe qui, peut désormais développer des applications d'IA._

En raison des ressources nécessaires au développement des modèles de base, ce processus n'est accessible qu'aux grandes entreprises (Google, Meta, Microsoft, Baidu, Tencent), aux gouvernements ( [Japon](https://oreil.ly/r86Qz) , [Émirats arabes unis](https://oreil.ly/IUcVg) ) et aux jeunes pousses ambitieuses et bien financées (OpenAI, Anthropic, Mistral). Dans une interview de septembre 2022, [Sam Altman, PDG d'OpenAI](https://oreil.ly/D9QBM) , a déclaré que la plus grande opportunité pour la grande majorité des utilisateurs serait d'adapter ces modèles à des applications spécifiques.

Le monde saisit rapidement cette opportunité. L'ingénierie de l'IA s'est imposée comme l'une des disciplines d'ingénierie à la croissance la plus rapide, voire la plus rapide. Les outils d'ingénierie de l'IA gagnent en popularité plus vite que tous les outils de génie logiciel précédents. En seulement deux ans, quatre outils open source d'ingénierie de l'IA (AutoGPT, Stable Diffusion eb UI, LangChain et Ollama) ont déjà accumulé plus d'étoiles sur GitHub que Bitcoin. Ils sont en passe de surpasser même les frameworks de développement web les plus populaires, tels que React et Vue, en termes de nombre d'étoiles. [La figure 1-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_6_1730130814919984) illustre la croissance du nombre d'étoiles des outils d'ingénierie de l'IA sur GitHub, comparée à celle de Bitcoin, Vue et React.

Une étude LinkedIn d'août 2023 révèle que le nombre de professionnels ajoutant des termes tels que « IA générative », « ChatGPT », « Ingénierie des prompts » et « Création de prompts » à leur profil a augmenté [en moyenne de 75 % par mois](https://oreil.ly/m8SvB) . [_ComputerWorld_](https://oreil.ly/47sGE) a déclaré que « la capacité à programmer l'IA est la compétence professionnelle dont la croissance est la plus rapide »..

![Un graphique d'un graphique avec des lignes de différentes couleurs. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0106.png)

###### Figure 1-6. Les outils d'ingénierie d'IA open source croissent plus rapidement que tous les autres outils d'ingénierie logicielle, selon leur nombre d'étoiles sur GitHub.

# Pourquoi le terme « ingénierie de l'IA » ?

De nombreux termes sont utilisés pour décrire le processus de création d'applications à partir de modèles de base, notamment l'ingénierie ML, le MLOps, l'AIOps, le LLMOps, etc. Pourquoi ai-je choisi l'ingénierie IA pour ce livre ?

Je n'ai pas retenu le terme « ingénierie ML » car, comme expliqué dans [« Ingénierie IA versus ingénierie ML »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_ai_engineering_versus_ml_engineering_1730130814986585) , travailler avec des modèles de base diffère de travailler avec des modèles ML traditionnels sur plusieurs points importants. Le terme « ingénierie ML » ne suffirait pas à rendre compte de cette distinction. Cependant, il englobe parfaitement les deux processus.

Je n'ai pas utilisé tous les termes se terminant par « Ops » car, bien que le processus comporte des composantes opérationnelles, l'accent est davantage mis sur l'ajustement (ingénierie) des modèles de base pour obtenir le résultat souhaité.

Finalement, j'ai interrogé 20 personnes développant des applications basées sur des modèles de base afin de savoir quel terme elles utiliseraient pour décrire leur travail. La plupart ont préféré _« ingénierie de l'IA »_ . J'ai donc décidé de suivre leur avis.

La communauté des ingénieurs en IA, en pleine expansion, a fait preuve d'une créativité remarquable, avec une incroyable variété d'applications passionnantes. La section suivante explorera quelques-uns des modèles d'application les plus courants.

# Cas d'utilisation du modèle de base

Si vous ne développez pas encore d'applications d'IA, j'espère que la section précédente vous aura convaincu que le moment est idéal pour vous y mettre. Si vous avez déjà une application en tête, vous pouvez passer directement à la section [« Planification des applications d'IA »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_planning_ai_applications_1730130814985969) . Si vous cherchez l'inspiration, cette section présente un large éventail de cas d'utilisation prometteurs et éprouvés dans l'industrie.

Le nombre d'applications potentielles que l'on pourrait développer à partir de modèles de base semble infini. Quel que soit le cas d'utilisation envisagé, il existe probablement une IA adaptée. Il est impossible de recenser tous les cas d'utilisation potentiels de l'IA [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id566)

La catégorisation de ces cas d'usage s'avère complexe, car les différentes études utilisent des classifications différentes. Par exemple, [Amazon Web Services (AWS)](https://oreil.ly/-k_QX) les répartit en trois catégories : expérience client, productivité des employés et optimisation des processus. Une [étude O'Reilly de 2024](https://oreil.ly/Kul5E) les classe en huit catégories : programmation, analyse de données, support client, rédaction marketing, autres types de rédaction, recherche, conception web et création graphique.

Certaines organisations, comme [Deloitte](https://oreil.ly/T272_) , ont classé les cas d'usage selon la valeur ajoutée qu'ils génèrent, notamment la réduction des coûts, l'amélioration de l'efficacité des processus, la croissance et l'accélération de l'innovation. [Gartner](https://oreil.ly/OyIUP) , quant à lui, propose une catégorie dédiée à _la continuité d'activité_ : une entreprise risque de faire faillite si elle n'adopte pas l'IA générative. Parmi les 2 500 dirigeants interrogés par Gartner en 2023, 7 % ont cité la continuité d'activité comme principale motivation pour adopter l'IA générative.

[L'étude d'Eloundou et al. (2023)](https://arxiv.org/abs/2303.10130) présente une analyse pertinente de l'exposition des différentes professions à l'IA. Les auteurs définissent une tâche comme étant exposée si l'IA et les logiciels basés sur l'IA permettent de réduire d'au moins 50 % le temps nécessaire à son exécution. Une profession est considérée comme exposée à 80 % si 80 % de ses tâches le sont. Selon cette étude, les professions exposées à 100 % ou presque incluent les interprètes et traducteurs, les préparateurs fiscaux, les concepteurs web et les rédacteurs. Certains de ces métiers sont présentés dans [le tableau 1-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_table_2_1730130814941524) . Sans surprise, les professions non exposées à l'IA comprennent les cuisiniers, les tailleurs de pierre et les athlètes. Cette étude donne un bon aperçu des cas d'usage pertinents pour l'IA.

Tableau 1-2. Professions les plus exposées à l'IA, selon les annotations humaines.fait référence à l'exposition directe aux modèles d'IA, tandis queetse référer à l’exposition aux logiciels utilisant l’IA. Tableau tiré de Eloundou et al. (2023).

|Groupe|Professions présentant la plus forte exposition|% Exposition|
|---|---|---|
|Humain|Interprètes et traducteurs  <br>, enquêteurs,  <br>poètes, paroliers et écrivains,  <br>zoologistes,  <br>spécialistes des relations publiques|76,5  <br>75,0  <br>68,8  <br>66,7  <br>66,7|
|Humain|Chercheurs en sondage,  <br>rédacteurs et auteurs,  <br>interprètes et traducteurs,  <br>spécialistes des relations publiques  <br>, zootechniciens|84,4  <br>82,5  <br>82,4  <br>80,6  <br>77,8|
|Humain|Mathématiciens,  <br>préparateurs de déclarations de revenus,  <br>analystes financiers quantitatifs,  <br>écrivains et auteurs,  <br>concepteurs d'interfaces Web et numériques :  <br>_autant de professions qualifiées de « totalement exposées » par l'humanité._|100,0  <br>100,0  <br>100,0  <br>100,0  <br>100,0|

Lors de l'analyse des cas d'usage, j'ai examiné des applications d'entreprise et grand public. Pour comprendre les cas d'usage en entreprise, j'ai interrogé 50 entreprises sur leurs stratégies d'IA et étudié plus de 100 cas pratiques. Concernant les applications grand public, j'ai analysé 205 applications d'IA open source ayant obtenu au moins 500 étoiles sur GitHub. J'ai classé [ces](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id567) applications en huit groupes, comme indiqué dans [le tableau 1-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_table_3_1730130814941550) . Cette liste, bien que non exhaustive, sert avant tout de référence. En découvrant comment construire des modèles de base au [chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) et comment les évaluer au [chapitre 3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) , vous comprendrez mieux les cas d'usage pour lesquels ces modèles peuvent et doivent être utilisés.

Tableau 1-3. Cas d'utilisation courants de l'IA générative dans les applications grand public et d'entreprise.

|Catégorie|Exemples de cas d'utilisation par les consommateurs|Exemples de cas d'utilisation en entreprise|
|---|---|---|
|Codage|Codage|Codage|
|Production d'images et de vidéos|Conception de montage photo et vidéo|Génération de publicités de présentation|
|En écrivant|Courriel,  <br>réseaux sociaux et articles de blog|Rédaction publicitaire, optimisation pour les moteurs de recherche (SEO)  <br>, rapports, notes de service, documents de conception|
|Éducation|Tutorat et  <br>correction de dissertations|Intégration des employés  <br>Formation continue des employés|
|Bots conversationnels|chatbot général  <br>compagnon IA|Assistance clientèle  <br>Copilotes de produits|
|Agrégation d'informations|Résumé  <br>Parlez à vos médecins|Synthèse  <br>des études de marché|
|Organisation des données|Recherche d'images  <br>[Memex](https://en.wikipedia.org/wiki/Memex)|Gestion des connaissances  <br>Traitement des documents|
|Automatisation des flux de travail|Planification de voyages et  <br>d'événements|Extraction, saisie et annotation des données  <br>Génération de prospects|

Comme les modèles de base sont généraux, les applications construites sur ces modèles peuvent résoudre de nombreux problèmes. Ainsi, une application peut appartenir à plusieurs catégories. Par exemple, un chatbot peut offrir de la compagnie et agréger des informations. Une application peut vous aider à extraire des données structurées d'un PDF et à répondre à des questions concernant ce PDF.

[La figure 1-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_7_1730130814920012) illustre la répartition de ces cas d'utilisation parmi les 205 applications open source. Il est important de noter que le faible pourcentage de cas d'utilisation liés à l'éducation, à l'organisation des données et à la rédaction ne signifie pas que ces cas d'utilisation sont impopulaires. Cela signifie simplement que les applications correspondantes ne sont pas open source. Les développeurs de ces applications pourraient les juger plus adaptées aux cas d'utilisation en entreprise.

![Un diagramme circulaire avec des cercles de différentes couleurs. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0107.png)

###### Figure 1-7. Répartition des cas d'utilisation dans les 205 dépôts open source sur GitHub.

Le monde de l'entreprise privilégie généralement les applications à faible risque. Par exemple, un [rapport a16z Growth de 2024](https://oreil.ly/XWeDt) a montré que les entreprises déploient plus rapidement les applications internes (gestion des connaissances internes) que les applications externes (chatbots de support client), comme illustré dans [la figure 1-8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_8_1730130814920037) . Les applications internes permettent aux entreprises de développer leur expertise en ingénierie de l'IA tout en minimisant les risques liés à la confidentialité des données, à la conformité et aux défaillances potentiellement catastrophiques. De même, si les modèles de base sont ouverts et peuvent être utilisés pour n'importe quelle tâche, de nombreuses applications construites sur ces modèles restent fermées, comme la classification. Les tâches de classification sont plus faciles à évaluer, ce qui facilite l'estimation de leurs risques.

![Capture d'écran d'un graphique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0108.png)

###### Figure 1-8. Les entreprises sont plus enclines à déployer des applications internes.

Même après avoir vu des centaines d'applications d'IA, je découvre encore chaque semaine de nouvelles applications surprenantes. Aux débuts d'Internet, rares étaient ceux qui prévoyaient que les réseaux sociaux deviendraient un jour l'usage dominant. À mesure que nous apprenons à exploiter pleinement l'IA, l'usage qui finira par s'imposer pourrait bien nous surprendre. Avec un peu de chance, ce sera une bonne surprise.

## Codage

Dans de nombreuses études sur l'IA générative, la programmation est de loin l'application la plus courante. Les outils de programmation pour l'IA sont populaires à la fois parce que l'IA excelle dans ce domaine et parce que les premiers ingénieurs en IA étaient des programmeurs, donc plus exposés aux défis de la programmation.

L'un des premiers succès des modèles de fondation en production est l'outil de complétion de code GitHub Copilot, dont [les revenus annuels récurrents ont dépassé les 100 millions de dollars](https://oreil.ly/Xamik) seulement deux ans après son lancement. À l'heure actuelle, les startups spécialisées dans le codage assisté par l'IA ont levé des centaines de millions de dollars, [Magic ayant levé 320 millions de dollars](https://oreil.ly/t0xDf) et [Anysphere 60 millions](https://oreil.ly/BW5Hk) , toutes deux en août 2024. Des outils de codage open source comme [gpt-engineer](https://github.com/gpt-engineer-org/gpt-engineer) et [screenshot-to-code](https://github.com/abi/screenshot-to-code) ont tous deux atteint 50 000 étoiles sur GitHub en moins d'un an, et de nombreux autres sont rapidement mis sur le marché.

Outre les outils d'aide à la programmation en général, de nombreux outils se spécialisent dans certaines tâches de programmation. Voici quelques exemples :

- Extraction de données structurées à partir de pages web et de fichiers PDF ( [AgentGPT](https://github.com/reworkd/AgentGPT) )
    
- Conversion de l'anglais en code ( [DB-GPT](https://github.com/eosphoros-ai/DB-GPT) , [SQL Chat](https://github.com/sqlchat/sqlchat) , [PandasAI](https://github.com/Sinaptik-AI/pandas-ai) )
    
- À partir d'un dessin ou d'une capture d'écran, générer du code qui permettra de créer un site web ressemblant à l'image donnée (screenshot-to-code, [draw-a-ui](https://github.com/sawyerhood/draw-a-ui) ).
    
- Traduction d'un langage de programmation ou d'un framework à un autre ( [GPT-Migrate](https://github.com/joshpxyne/gpt-migrate) , [traducteur de code IA](https://github.com/mckaywrigley/ai-code-translator) )
    
- Rédaction de la documentation ( [Autodoc](https://github.com/context-labs/autodoc) )
    
- Création de tests ( [PentestGPT](https://github.com/GreyDGL/PentestGPT) )
    
- Génération de messages de commit ( [commits IA](https://github.com/Nutlope/aicommits) )
    

Il est clair que l'IA peut accomplir de nombreuses tâches d'ingénierie logicielle. La question est de savoir si elle peut automatiser entièrement ce processus. À l'une des extrémités du spectre, [Jensen Huang, PDG de NVIDIA](https://oreil.ly/zUpGu) , prédit que l'IA remplacera les ingénieurs logiciels humains et qu'il est temps d'arrêter d'insister pour que les enfants apprennent à coder. Dans un enregistrement qui a fuité, [Matt Garman, PDG d'AWS,](https://oreil.ly/Hz_3i) a indiqué que, dans un avenir proche, la plupart des développeurs cesseront de coder. Il ne s'agit pas pour autant de la fin des développeurs ; simplement d'une transformation de leur métier.

À l'autre extrémité du spectre se trouvent de nombreux ingénieurs logiciels convaincus qu'ils ne seront jamais remplacés par l'IA, pour des raisons à la fois techniques et émotionnelles (les gens n'aiment pas admettre qu'ils peuvent être remplacés).

Le génie logiciel comprend de nombreuses tâches. L'IA excelle dans certaines d'entre elles. Des chercheurs [de McKinsey](https://oreil.ly/aqUmX) ont constaté que l'IA peut doubler la productivité des développeurs pour la documentation et l'accroître de 25 à 50 % pour la génération et la refactorisation de code. L'amélioration de la productivité reste minime pour les tâches très complexes, comme illustré dans [la figure 1-9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_9_1730130814920060) . Lors de mes échanges avec des développeurs d'outils de codage basés sur l'IA, plusieurs m'ont indiqué avoir observé que l'IA est bien plus performante pour le développement front-end que pour le développement back-end.

![Graphique à barres bleues et blanches. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0109.png)

###### Figure 1-9. L’IA peut considérablement améliorer la productivité des développeurs, notamment pour les tâches simples, mais son impact est moindre pour les tâches très complexes. Données McKinsey.

Que l'IA remplace ou non les ingénieurs logiciels, elle peut assurément accroître leur productivité. Les entreprises peuvent ainsi accomplir davantage avec moins d'ingénieurs. L'IA peut également bouleverser le secteur de l'externalisation, car les tâches externalisées sont généralement plus simples et hors du cœur de métier de l'entreprise.

## Production d'images et de vidéos

Grâce à sa nature probabiliste, l'IA est idéale pour les tâches créatives. Parmi les startups d'IA les plus prospères figurent des applications créatives, comme Midjourney pour la génération d'images, Adobe Firefly pour la retouche photo, et Runway, Pika Labs et Sora pour la création vidéo. Fin 2023, après seulement un an et demi d'existence, [Midjourney](https://oreil.ly/EAzCl) générait déjà 200 millions de dollars de revenus annuels récurrents. En décembre 2023, la moitié des dix meilleures applications gratuites de graphisme et de design sur l'App Store d'Apple intégraient l'IA dans leur nom. Je pense que bientôt, les applications de graphisme et de design intégreront l'IA par défaut et n'auront plus besoin du terme « IA » dans leur appellation. [Le chapitre 2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) aborde plus en détail la nature probabiliste de l'IA.

Il est désormais courant d'utiliser l'IA pour générer des photos de profil sur les réseaux sociaux, de LinkedIn à TikTok. De nombreux candidats pensent que les photos de profil générées par IA peuvent les aider à se mettre en valeur et [à augmenter leurs chances de trouver un emploi](https://oreil.ly/fZLVg) . La perception des photos de profil générées par IA a considérablement évolué. En 2019, [Facebook](https://oreil.ly/WNqUw) a banni les comptes utilisant de telles photos pour des raisons de sécurité. En 2023, de nombreuses applications de réseaux sociaux proposent des outils permettant aux utilisateurs d'utiliser l'IA pour générer des photos de profil.

Pour les entreprises, la publicité et le marketing ont rapidement intégré l'IA. [L'](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id572) IA peut être utilisée pour générer directement des images et des vidéos promotionnelles. Elle peut faciliter le brainstorming ou générer des premières ébauches que les experts pourront ensuite peaufiner. Vous pouvez utiliser l'IA pour créer plusieurs publicités et les tester afin de déterminer laquelle est la plus performante auprès de votre public. L'IA peut également créer des variations de vos publicités en fonction des saisons et des lieux. Par exemple, vous pouvez l'utiliser pour modifier la couleur des feuilles en automne ou ajouter de la neige au sol en hiver.

## En écrivant

L'intelligence artificielle est utilisée depuis longtemps pour faciliter l'écriture. Si vous utilisez un smartphone, vous connaissez probablement la correction automatique et la saisie semi-automatique, deux fonctionnalités basées sur l'IA. L'écriture est une application idéale pour l'IA car nous écrivons fréquemment, cela peut être fastidieux, et nous avons une grande tolérance pour les erreurs. Si un modèle suggère une option qui ne vous convient pas, vous pouvez simplement l'ignorer.

Il n'est pas surprenant que les titulaires d'un LLM soient doués en écriture, étant donné qu'ils sont formés à la complétion de texte.Pour étudier l'impact de ChatGPT sur la rédaction, une étude du MIT ( [Noy et Zhang, 2023](https://oreil.ly/IzQ6F) ) a confié des tâches d'écriture spécifiques à leur profession à 453 professionnels diplômés de l'enseignement supérieur et a exposé aléatoirement la moitié d'entre eux à ChatGPT. Les résultats montrent que, parmi les participants exposés à ChatGPT, le temps moyen de rédaction a diminué de 40 % et la qualité des productions a augmenté de 18 %. ChatGPT contribue à réduire les écarts de qualité de production entre les travailleurs, ce qui signifie qu'il est plus utile à ceux qui ont moins d'affinités pour l'écriture. Les travailleurs exposés à ChatGPT pendant l'expérience étaient deux fois plus susceptibles de déclarer l'utiliser dans leur travail deux semaines après l'expérience et 1,6 fois plus susceptibles deux mois plus tard.

Pour les consommateurs, les cas d'utilisation sont évidents. Nombreux sont ceux qui utilisent l'IA pour améliorer leur communication. On peut exprimer sa colère dans un courriel et demander à l'IA de le rendre plus agréable. On peut lui fournir des listes à puces et obtenir en retour des paragraphes complets. Plusieurs personnes affirment ne plus envoyer de courriel important sans avoir préalablement consulté une IA pour l'améliorer.

Les étudiants utilisent l'IA pour rédiger leurs dissertations. Les écrivains l'utilisent pour écrire des livres. De [nombreuses](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id574) start-ups exploitent déjà l'IA pour générer des livres pour enfants, des fanfictions, des romans d'amour et des ouvrages fantastiques. Contrairement aux livres traditionnels, les livres générés par l'IA peuvent être interactifs : l'intrigue peut évoluer en fonction des préférences du lecteur. Ainsi, les lecteurs peuvent participer activement à la création de l'histoire qu'ils lisent. Une application de lecture pour enfants repère les mots qui posent problème à l'enfant et génère des histoires centrées sur ces mots.

Les applications de prise de notes et de messagerie comme Google Docs, Notion et Gmail utilisent toutes l'IA pour aider les utilisateurs à améliorer leur écriture. [Grammarly](https://arxiv.org/abs/2305.09857) , une application d'aide à la rédaction, affine un modèle pour rendre les écrits des utilisateurs plus fluides, cohérents et clairs.

Les capacités d'écriture de l'IA peuvent aussi être détournées. En 2023, le [New York Times](https://oreil.ly/LB72P) a révélé qu'Amazon était inondé de guides de voyage de piètre qualité, générés par l'IA, chacun agrémenté d'une biographie d'auteur, d'un site web et de critiques dithyrambiques, le tout produit par l'IA.

En entreprise, l'IA est couramment utilisée pour la rédaction de contenu dans les ventes, le marketing et la communication interne. De nombreux responsables m'ont confié utiliser l'IA pour rédiger leurs rapports de performance. L'IA peut contribuer à la création d'e-mails de prospection efficaces, de publicités percutantes et de descriptions de produits pertinentes. Les applications de gestion de la relation client (CRM) comme HubSpot et Salesforce proposent également des outils permettant aux entreprises de générer du contenu web et des e-mails de prospection.

L'IA semble particulièrement performante en matière de référencement (SEO), sans doute parce que de nombreux modèles d'IA sont entraînés avec des données issues d'Internet, un réseau riche en textes optimisés pour le SEO. L'IA excelle tellement en SEO qu'elle a permis l'émergence d'une nouvelle génération de fermes de contenu. Ces fermes créent des sites web de piètre qualité et les remplissent de contenu généré par l'IA afin d'obtenir un bon classement sur Google et d'y générer du trafic. Elles vendent ensuite des espaces publicitaires via des plateformes d'échange publicitaire. En juin 2023, [NewsGuard a recensé près de 400 publicités de 141 marques populaires sur ces sites web de piètre](https://oreil.ly/mZKjr) [qualité](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id575) générés par l'IA. L'un de ces sites produisait jusqu'à 1 200 articles par jour. Si rien n'est fait pour endiguer ce phénomène, l'avenir du contenu internet sera généré par l'IA, et il s'annonce plutôt sombre.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id575)

## Éducation

Lorsque ChatGPT est hors service, le serveur Discord d'OpenAI est submergé de messages d'élèves se plaignant de ne pas pouvoir faire leurs devoirs. Plusieurs commissions scolaires, dont les écoles publiques de New York et le district scolaire unifié de Los Angeles, ont rapidement [interdit ChatGPT](https://oreil.ly/pqI5z) par crainte de tricherie, avant [de revenir sur leur décision](https://oreil.ly/nxtzw) quelques mois plus tard.

Au lieu d'interdire l'IA, les écoles pourraient l'intégrer pour aider les élèves à apprendre plus vite. L'IA peut résumer les manuels scolaires et générer des plans de cours personnalisés pour chaque élève. Il est paradoxal que les publicités soient personnalisées, car nous savons que chaque personne est différente, alors que l'éducation, elle, ne l'est pas. L'IA peut adapter les supports pédagogiques au format le plus adapté à chaque élève. Les élèves à dominante auditive peuvent demander à l'IA de lire les documents à voix haute. Les élèves passionnés d'animaux peuvent utiliser l'IA pour adapter les visualisations et y inclure davantage d'animaux. Ceux qui préfèrent lire du code plutôt que des équations mathématiques peuvent demander à l'IA de traduire ces dernières en code.

L'IA est particulièrement utile pour l'apprentissage des langues, car elle permet de simuler différents scénarios d'entraînement. [Pajak et Bicknell (Duolingo, 2022)](https://oreil.ly/C8kmI) ont constaté que, parmi les quatre étapes de la création d'un cours, la personnalisation des leçons est celle qui peut le plus bénéficier de l'IA, comme illustré dans [la figure 1-10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_10_1730130814920091) .

![Un livre blanc avec une description en bleu générée automatiquement](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0110.png)

###### Figure 1-10. L'IA peut être utilisée à toutes les étapes de la création de cours sur Duolingo, mais elle est particulièrement utile lors de la personnalisation. Image tirée de Pajak et Bicknell (Duolingo, 2022).

L'IA peut générer des questionnaires, à choix multiples ou à questions ouvertes, et évaluer les réponses. Elle peut devenir un partenaire de débat efficace, car elle est bien plus apte que la moyenne des humains à présenter différents points de vue sur un même sujet. Par exemple, [la Khan Academy](https://oreil.ly/tC7-g) propose aux élèves des assistants pédagogiques [basés sur l'IA](https://oreil.ly/_N1JR) et aux enseignants des assistants de cours. Une méthode pédagogique innovante que j'ai pu observer consiste à confier aux élèves des dissertations générées par l'IA, qu'ils doivent ensuite corriger .

Alors que de nombreuses entreprises du secteur de l'éducation adoptent l'IA pour concevoir de meilleurs produits, beaucoup voient leurs parts de marché menacées par cette même IA. Par exemple, Chegg, une entreprise qui aide les élèves à faire leurs devoirs, a vu le cours de son action chuter de 28 dollars lors du lancement de ChatGPT en novembre 2022 à seulement 2 dollars en septembre 2024, [les élèves se tournant de plus en plus vers l'IA pour obtenir de l'aide](https://oreil.ly/Y-hBW) .

Si le risque est que l'IA remplace de nombreuses compétences, l'opportunité réside dans son utilisation comme tuteur pour l'apprentissage de toute compétence. Pour de nombreuses compétences, l'IA peut aider à une prise en main rapide et à poursuivre ensuite son apprentissage de manière autonome pour devenir plus performante que l'IA.

## Bots conversationnels

Les chatbots conversationnels sont polyvalents. Ils peuvent nous aider à trouver des informations, à expliquer des concepts et à générer des idées. L'IA peut être à la fois un compagnon et un thérapeute. Elle peut imiter des personnalités, vous permettant de discuter avec une copie numérique de la personne de votre choix. Les petits amis et petites amies virtuels sont devenus étonnamment populaires en un temps record. Nombreux sont ceux qui passent déjà plus de temps à parler à des chatbots qu'à des humains (voir les discussions [ici](https://oreil.ly/dZbym) et [ici](https://oreil.ly/svWj8) ). Certains craignent que l'IA ne [ruine](https://oreil.ly/SNme7) [les relations amoureuses](https://oreil.ly/Jbt4R) .

Dans le cadre de recherches, des personnes ont également découvert qu'elles pouvaient utiliser un groupe de robots conversationnels pour simuler une société, ce qui leur permettait de mener des études sur la dynamique sociale ( [Park et al., 2023](https://arxiv.org/abs/2304.03442) ).

Pour les entreprises, les bots les plus populaires sont les bots de support client. Ils permettent de réduire les coûts tout en améliorant l'expérience client, car ils répondent plus rapidement aux utilisateurs que les agents humains. L'IA peut également servir de copilote produit, guidant les clients dans des tâches complexes et fastidieuses comme la déclaration de sinistre, la déclaration d'impôts ou la consultation des politiques de l'entreprise.

Le succès de ChatGPT a engendré une vague de chatbots conversationnels textuels. Cependant, le texte n'est pas la seule interface pour les agents conversationnels. Les assistants vocaux tels que Google Assistant, Siri et Alexa existent depuis des années. [Quinze](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id584) chatbots conversationnels 3D sont déjà courants dans les jeux vidéo et gagnent du terrain dans le commerce de détail et le marketing.

L'une des applications des personnages 3D dotés d'IA concerne les PNJ intelligents (personnages non-joueurs), comme le montrent les démonstrations d' [Inworld](https://oreil.ly/yn-DN) et [de Convai](https://oreil.ly/zAHwz) par NVIDIA . [Les](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id585) PNJ sont essentiels au développement de l'histoire de nombreux jeux. Sans IA, leurs actions sont généralement programmées et limitées à un nombre restreint de dialogues. L'IA permet de les rendre beaucoup plus intelligents. Ces bots intelligents peuvent transformer la dynamique de jeux existants comme _Les Sims_ et _Skyrim,_ et même rendre possible la création de nouveaux jeux jusqu'alors impossibles.

## Agrégation d'informations

Nombreux sont ceux qui pensent que notre réussite repose sur notre capacité à filtrer et à assimiler les informations utiles. Or, jongler avec les e-mails, les messages Slack et l'actualité peut parfois s'avérer complexe. Heureusement, l'IA est là pour nous aider. Elle a démontré sa capacité à agréger et à synthétiser les informations. D'après l'étude [Salesforce « Generative AI Snapshot Research](https://oreil.ly/74soT) 2023 » , 74 % des utilisateurs d'IA générative s'en servent pour extraire des idées complexes et résumer des informations.

Pour les consommateurs, de nombreuses applications peuvent traiter vos documents (contrats, déclarations, articles) et vous permettre d'obtenir des informations de manière conversationnelle. Ce type d'utilisation est également appelé « _dialogue avec vos documents »_ . L'IA peut vous aider à résumer des sites web, à effectuer des recherches et à créer des rapports sur les sujets de votre choix. Lors de la rédaction de ce livre, j'ai trouvé l'IA utile pour résumer et comparer des articles.

L'agrégation et la synthèse de l'information sont essentielles au bon fonctionnement des entreprises. Une agrégation et une diffusion plus efficaces de l'information permettent à une organisation de gagner en efficacité, en allégeant la charge de travail des cadres intermédiaires. Lors du lancement d'une plateforme interne de synthèse, [Instacart](https://oreil.ly/Qq5-g) a constaté que le modèle « Synthèse rapide » était particulièrement apprécié. Ce modèle sollicite l'intelligence artificielle pour résumer les comptes rendus de réunion, les e-mails et les conversations Slack en identifiant les faits, les questions ouvertes et les actions à entreprendre. Ces actions peuvent ensuite être automatiquement intégrées à un outil de suivi de projet et attribuées aux responsables concernés.

L'IA peut vous aider à faire émerger les informations cruciales sur vos clients potentiels et à analyser vos concurrents.

Plus vous recueillez d'informations, plus il est important de les organiser. L'agrégation des informations est indissociable de l'organisation des données.

## Organisation des données

Une chose est sûre : nous continuerons à produire toujours plus de données. Les utilisateurs de smartphones continueront à prendre des photos et des vidéos. Les entreprises continueront à tout consigner sur leurs produits, leurs employés et leurs clients. Des milliards de contrats sont créés chaque année.Photos, vidéos, journaux et fichiers PDF sont autant de données non structurées ou semi-structurées. Il est essentiel d'organiser ces données de manière à pouvoir les rechercher ultérieurement.

L'IA peut précisément nous aider. Elle peut générer automatiquement des descriptions textuelles pour les images et les vidéos, ou encore associer des requêtes textuelles à des images correspondantes. Des services comme Google Photos utilisent déjà l'IA pour proposer des images correspondant aux requêtes de recherche. [Google](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id592) Images va encore plus loin : si aucune image ne correspond aux besoins de l'utilisateur, il peut en générer.

L'IA excelle dans l'analyse des données. Elle peut écrire des programmes pour générer des visualisations de données, identifier les valeurs aberrantes et effectuer des prédictions, comme des prévisions de revenus [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id593)

Les entreprises peuvent utiliser l'IA pour extraire des informations structurées à partir de données non structurées, ce qui permet d'organiser et de rechercher ces données. Parmi les cas d'utilisation simples, on peut citer l'extraction automatique d'informations à partir de cartes de crédit, de permis de conduire, de reçus, de billets, d'informations de contact figurant en bas de page d'e-mails, etc. Des cas d'utilisation plus complexes incluent l'extraction de données à partir de contrats, de rapports, de graphiques, et bien plus encore. On estime que le marché du traitement intelligent des données (IDP) atteindra [12,81 milliards de dollars d'ici 2030](https://oreil.ly/vnDNK) , avec une croissance annuelle de 32,9 %.

## Automatisation des flux de travail

À terme, l'IA devrait automatiser un maximum de tâches. Pour les utilisateurs finaux, l'automatisation peut faciliter les tâches quotidiennes fastidieuses comme réserver des restaurants, demander des remboursements, planifier des voyages et remplir des formulaires.

Pour les entreprises, l'IA peut automatiser les tâches répétitives telles que la gestion des prospects, la facturation, les remboursements, la gestion des demandes clients, la saisie de données, etc. Un cas d'utilisation particulièrement prometteur consiste à utiliser des modèles d'IA pour synthétiser des données, afin d'améliorer ensuite ces mêmes modèles. L'IA permet de créer des étiquettes pour vos données, puis d'y intégrer des interventions humaines pour affiner ces étiquettes. La synthèse des données est abordée au [chapitre 8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) .

L'accès à des outils externes est nécessaire pour accomplir de nombreuses tâches. Pour réserver un restaurant, une application peut avoir besoin de l'autorisation d'ouvrir un moteur de recherche pour trouver le numéro du restaurant, d'utiliser votre téléphone pour passer des appels et d'ajouter des rendez-vous à votre agenda. Les IA capables de planifier et d'utiliser des outils sont appelées _agents_ . L'intérêt suscité par les agents frôle l'obsession, mais il n'est pas totalement injustifié. Les agents d'IA ont le potentiel d'accroître considérablement la productivité de chacun et de générer une valeur économique bien plus importante. Les agents sont un thème central du [chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) .

J'ai pris beaucoup de plaisir à explorer différentes applications d'IA. J'aime particulièrement rêver aux diverses applications que je pourrais créer. Cependant, toutes les applications ne sont pas pertinentes. La section suivante aborde les points à prendre en compte avant de se lancer dans la création d'une application d'IA.

# Applications de planification de l'IA

Face au potentiel apparemment illimité de l'IA, la tentation est grande de se lancer directement dans le développement d'applications. Si votre objectif est d'apprendre et de vous amuser, n'hésitez pas ! Créer est l'une des meilleures façons d'apprendre. Aux débuts des modèles de base, plusieurs responsables de l'IA m'ont confié qu'ils encourageaient leurs équipes à expérimenter des applications d'IA pour développer leurs compétences.

Cependant, si vous en vivez, il peut être judicieux de prendre du recul et de réfléchir aux raisons qui vous poussent à développer ce projet et à la manière de procéder. Créer une démo attrayante avec des modèles de base est facile. En revanche, développer un produit rentable est beaucoup plus complexe.

## Évaluation des cas d'utilisation

La première question à se poser est : pourquoi souhaitez-vous développer cette application ? Comme pour de nombreuses décisions commerciales, la création d’une application d’IA est souvent une réponse aux risques et aux opportunités. Voici quelques exemples de différents niveaux de risques, classés du plus élevé au plus faible :

1. _Si vous ne prenez pas les mesures nécessaires, vos concurrents maîtrisant l'IA risquent de vous rendre obsolète._ Si l'IA représente une menace existentielle majeure pour votre entreprise, son intégration doit devenir une priorité absolue. Selon une [étude Gartner](https://oreil.ly/gqi3d) de 2023 , 7 % des entreprises ont cité la continuité de leurs activités comme principale raison d'adopter l'IA. Ce phénomène est plus fréquent dans les secteurs d'activité liés au traitement de documents et à l'agrégation d'informations, tels que l'analyse financière, l'assurance et le traitement de données. Il est également courant dans les domaines créatifs comme la publicité, la conception web et la production d'images. Pour connaître le classement des différents secteurs d'activité en fonction de leur exposition à l'IA, vous pouvez consulter l'étude OpenAI de 2023, « GPTs are GPTs » ( [Eloundou et al., 2023](https://arxiv.org/abs/2303.10130) ).
    
2. _Si vous ne le faites pas, vous passerez à côté d'opportunités d'accroître vos profits et votre productivité._ La plupart des entreprises adoptent l'IA pour les opportunités qu'elle offre. L'IA peut être utile dans la quasi-totalité des opérations commerciales. Elle permet de réduire les coûts d'acquisition d'utilisateurs grâce à des textes publicitaires, des descriptions de produits et des contenus visuels promotionnels plus efficaces. L'IA peut améliorer la fidélisation des utilisateurs en optimisant le support client et en personnalisant l'expérience utilisateur. Elle peut également faciliter la génération de prospects, la communication interne, les études de marché et la veille concurrentielle.
    
3. _Vous ne savez pas encore quelle place occupera l'IA dans votre entreprise, mais vous ne voulez pas être à la traîne. Si une entreprise ne doit pas se laisser emporter par toutes les tendances, beaucoup ont échoué en attendant trop longtemps avant de franchir le pas (Kodak, Blockbuster et BlackBerry en sont des_ [exemples](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id599) ). Investir des ressources pour comprendre l'impact d'une nouvelle technologie transformatrice sur votre activité est une bonne idée si vous en avez les moyens. Dans les grandes entreprises, cela peut relever du département R&D.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id599)
    

Une fois que vous avez identifié une raison valable de développer ce cas d'usage, vous pouvez vous demander s'il est nécessaire de le développer vous-même. Si l'IA représente une menace existentielle pour votre entreprise, il peut être judicieux de gérer l'IA en interne plutôt que de l'externaliser auprès d'un concurrent. En revanche, si vous utilisez l'IA pour accroître vos profits et votre productivité, vous disposez probablement de nombreuses solutions d'achat qui vous permettront de gagner du temps et de l'argent tout en bénéficiant de meilleures performances.

### Le rôle de l'IA et des humains dans l'application

Le rôle de l'IA dans un produit d'IA influence le développement de l'application et ses exigences. [Apple](https://oreil.ly/Dz1HE) propose un excellent document expliquant les différentes manières d'utiliser l'IA dans un produit. Voici trois points clés pertinents pour notre discussion :

Critique ou complémentaire

Si une application peut fonctionner sans IA, alors l'IA est complémentaire à l'application. Par exemple, Face ID ne fonctionnerait pas sans la reconnaissance faciale basée sur l'IA, tandis que Gmail fonctionnerait sans la fonction de saisie intelligente.

Plus l'IA est essentielle à l'application, plus elle doit être précise et fiable. Les utilisateurs tolèrent mieux les erreurs lorsque l'IA n'est pas au cœur de l'application.

Réactif ou proactif

Une fonctionnalité réactive répond aux requêtes ou actions spécifiques des utilisateurs, tandis qu'une fonctionnalité proactive répond lorsqu'une opportunité se présente. Par exemple, un chatbot est réactif, tandis que les alertes trafic sur Google Maps sont proactives.

Les fonctionnalités réactives étant générées en réponse à des événements, elles doivent généralement, mais pas toujours, s'exécuter rapidement. En revanche, les fonctionnalités proactives peuvent être précalculées et affichées de manière opportuniste, ce qui rend la latence moins critique.

Comme les utilisateurs ne sollicitent pas les fonctionnalités proactives, ils peuvent les percevoir comme intrusives ou agaçantes si leur qualité est médiocre. C'est pourquoi les prédictions et les générations proactives sont généralement soumises à des exigences de qualité plus élevées.

Dynamique ou statique

Les fonctionnalités dynamiques sont mises à jour en continu grâce aux retours des utilisateurs, tandis que les fonctionnalités statiques sont mises à jour périodiquement. Par exemple, Face ID doit être mis à jour car les visages évoluent avec le temps. En revanche, la détection d'objets dans Google Photos n'est probablement mise à jour que lors des mises à jour de Google Photos.

Dans le domaine de l'IA, les fonctionnalités dynamiques peuvent signifier que chaque utilisateur possède son propre modèle, continuellement affiné grâce à ses données, ou d'autres mécanismes de personnalisation comme la fonction de mémoire de ChatGPT, qui permet à ChatGPT de se souvenir des préférences de chaque utilisateur. En revanche, les fonctionnalités statiques peuvent reposer sur un seul modèle pour un groupe d'utilisateurs. Dans ce cas, ces fonctionnalités ne sont mises à jour que lorsque le modèle partagé est modifié.

Il est également important de clarifier le rôle des humains dans l'application. L'IA fournira-t-elle un soutien en arrière-plan, prendra-t-elle des décisions directement, ou les deux ? Par exemple, pour un chatbot de service client, les réponses de l'IA peuvent être utilisées de différentes manières :

- L'IA propose plusieurs réponses auxquelles les agents humains peuvent se référer pour rédiger des réponses plus rapides.
    
- L'IA ne répond qu'aux requêtes simples et transmet les requêtes plus complexes aux humains.
    
- L'IA répond directement à toutes les requêtes, sans intervention humaine.
    

L'implication des humains dans les processus de prise de décision de l'IA est appelée _« intervention humaine dans la boucle »_ .

Microsoft (2023) a proposé un cadre pour accroître progressivement l'automatisation de l'IA dans les produits, qu'ils appellent [Crawl-Walk-Run](https://oreil.ly/JW4_A) :

1. Le crawling implique une intervention humaine obligatoire.
    
2. Walk signifie que l'IA peut interagir directement avec les employés internes.
    
3. L'exécution implique une automatisation accrue, pouvant inclure des interactions directes entre l'IA et des utilisateurs externes.
    

Le rôle des humains peut évoluer au fil du temps, à mesure que la qualité du système d'IA s'améliore. Par exemple, au début, lors de l'évaluation des capacités de l'IA, vous pourriez l'utiliser pour générer des suggestions à destination des agents humains. Si le taux d'acceptation par ces derniers est élevé (par exemple, si 95 % des réponses suggérées par l'IA à des requêtes simples sont utilisées telles quelles), vous pouvez permettre aux clients d'interagir directement avec l'IA pour ces requêtes simples.

### défense des produits d'IA

Si vous commercialisez des applications d'IA comme des produits autonomes, il est crucial de prendre en compte leur protection. La facilité d'accès au marché est à la fois un atout et un inconvénient. Si un produit est facile à développer pour vous, il l'est aussi pour vos concurrents. Quels avantages concurrentiels possédez-vous pour protéger votre produit ?

En quelque sorte, construire des applications à partir de modèles de base revient à ajouter une couche d'abstraction à ces modèles. [Cela](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id607) signifie également que si les modèles sous-jacents gagnent en fonctionnalités, la couche que vous fournissez risque d'être absorbée par ces modèles, rendant votre application obsolète. Imaginez développer une application d'analyse de PDF basée sur ChatGPT en supposant que ChatGPT ne peut pas analyser correctement les PDF ou à grande échelle. Votre compétitivité s'en trouvera affaiblie si cette hypothèse s'avère fausse. Cependant, même dans ce cas, une application d'analyse de PDF peut rester pertinente si elle est construite sur des modèles open source, en orientant votre solution vers les utilisateurs qui souhaitent héberger leurs modèles en interne.

Une associée d'un grand fonds de capital-risque m'a confié avoir vu de nombreuses startups dont les produits pourraient être intégrés à Google Docs ou Microsoft Office. Si leurs produits rencontrent un franc succès, qu'est-ce qui empêcherait Google ou Microsoft d'affecter trois ingénieurs à leur reproduction en deux semaines ?

En IA, on distingue généralement trois types d'avantages concurrentiels : la technologie, les données et la distribution (c'est-à-dire la capacité à présenter son produit aux utilisateurs). Avec des modèles de base, les technologies fondamentales de la plupart des entreprises sont similaires. L'avantage en matière de distribution est généralement détenu par les grandes entreprises.

L’avantage lié aux données est plus nuancé. Les grandes entreprises disposent probablement de davantage de données existantes. Cependant, si une startup parvient à être la première sur le marché et à collecter suffisamment de données d’utilisation pour améliorer continuellement ses produits, les données constitueront son principal atout. Même dans les cas où les données utilisateur ne peuvent être utilisées directement pour entraîner les modèles, les informations d’utilisation peuvent fournir des indications précieuses sur les comportements des utilisateurs et les lacunes des produits, permettant ainsi d’orienter le processus de collecte et d’entraînement des données. [21](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id608)

De nombreuses entreprises prospères ont vu leurs produits initiaux devenir des fonctionnalités de produits plus importants. Calendly aurait pu être une fonctionnalité de Google Agenda, Mailchimp de Gmail et Photoroom de Google Photos. De [nombreuses](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id609) startups finissent par surpasser leurs concurrents plus importants en développant une fonctionnalité que ces derniers avaient négligée. Votre startup sera peut-être la prochaine.

## Établir les attentes

Une fois que vous avez décidé de créer vous-même cette application d'IA exceptionnelle, l'étape suivante consiste à définir ce que signifie le succès : comment le mesurerez-vous ? L'indicateur le plus important est son impact sur votre activité. Par exemple, s'il s'agit d'un chatbot de support client, les indicateurs de performance peuvent inclure les éléments suivants :

- Quel pourcentage des messages clients souhaitez-vous que le chatbot automatise ?
    
- Combien de messages supplémentaires le chatbot devrait-il vous permettre de traiter ?
    
- À quel point pouvez-vous gagner du temps en utilisant le chatbot ?
    
- Combien de travail humain le chatbot peut-il vous faire économiser ?
    

Un chatbot peut répondre à davantage de messages, mais cela ne garantit pas la satisfaction des utilisateurs. Il est donc essentiel de suivre la satisfaction client et de recueillir leurs commentaires. La section [« Commentaires des utilisateurs »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_user_feedback_1730130985313500) explique comment concevoir un système de retour d'information.

Pour éviter de proposer un produit aux clients avant qu'il ne soit prêt, définissez clairement son seuil d'utilité : le niveau de qualité requis pour qu'il soit utile. Ce seuil peut s'appuyer sur les groupes de métriques suivants :

- Indicateurs de qualité pour mesurer la qualité des réponses du chatbot.
    
- Les indicateurs de latence comprennent le TTFT (temps d'obtention du premier jeton), le TPOT (temps d'envoi par jeton) et la latence totale. Le seuil de latence acceptable dépend de votre cas d'utilisation. Si toutes les requêtes de vos clients sont actuellement traitées manuellement avec un temps de réponse médian d'une heure, une latence plus rapide peut être suffisante.
    
- Métriques de coût : combien coûte chaque requête d’inférence.
    
- D'autres indicateurs tels que l'interprétabilité et l'équité.
    

Si vous n'êtes pas encore certain des indicateurs que vous souhaitez utiliser, ne vous inquiétez pas. La suite de cet ouvrage abordera bon nombre d'entre eux.

## Planification des étapes clés

Une fois vos objectifs mesurables définis, il vous faut un plan pour les atteindre. La manière d'y parvenir dépend de votre point de départ. Évaluez les modèles existants pour comprendre leurs capacités. Plus les modèles prêts à l'emploi sont performants, moins vous aurez d'efforts à fournir. Par exemple, si votre objectif est d'automatiser 60 % des tickets de support client et que le modèle prêt à l'emploi que vous souhaitez utiliser peut déjà en automatiser 30 %, l'effort nécessaire sera probablement moindre que s'il ne permettait d'automatiser aucun ticket.

Il est probable que vos objectifs évoluent après l'évaluation. Par exemple, vous pourriez vous rendre compte que les ressources nécessaires pour que l'application atteigne le seuil d'utilité requis seront supérieures à son retour sur investissement potentiel et, par conséquent, renoncer au projet.

La planification d'un produit d'IA doit tenir compte du défi de sa finalisation. Le succès initial des modèles de base peut être trompeur. Leurs capacités étant déjà impressionnantes, la création d'une démo attrayante peut être rapide. Cependant, une bonne démo initiale ne garantit pas un bon produit final. Créer une démo peut prendre un week-end, mais développer un produit peut nécessiter des mois, voire des années.

Dans leur article sur UltraChat, [Ding et al. (2023)](https://arxiv.org/abs/2305.14233) ont constaté que « passer de 0 à 60 est facile, mais atteindre 100 est extrêmement difficile ». [LinkedIn (2024)](https://www.linkedin.com/blog/engineering/generative-ai/musings-on-building-a-generative-ai-product) partageait ce constat. Il leur a fallu un mois pour atteindre 80 % de l’expérience souhaitée. Ce succès initial les a conduits à sous-estimer considérablement le temps nécessaire à l’amélioration du produit. Ils ont finalement mis quatre mois supplémentaires pour dépasser les 95 %. Ils ont consacré beaucoup de temps à corriger les défauts du produit et à gérer des situations complexes. La lenteur des progrès, même pour chaque gain de 1 %, était décourageante.

## Entretien

La planification produit ne s'arrête pas à l'atteinte des objectifs. Il faut anticiper l'évolution du produit et sa maintenance. La maintenance d'un produit d'IA est d'autant plus complexe compte tenu du rythme d'évolution rapide de l'IA. Le domaine de l'IA a connu une croissance fulgurante ces dix dernières années et continuera probablement sur cette lancée au cours des dix prochaines. S'appuyer aujourd'hui sur des modèles de base, c'est s'engager à suivre cette évolution à grande vitesse.

De nombreux changements sont positifs. Par exemple, les limitations de nombreux modèles sont prises en compte. La durée des contextes s'allonge. Les résultats des modèles s'améliorent._L'inférence_ de modèles , c'est-à-dire le processus de calcul d'une sortie à partir d'une entrée, devient plus rapide et moins coûteuse. [La figure 1-11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_11_1730130814920109) illustre l'évolution du coût d'inférence et des performances des modèles sur MMLU (Massive Multitask Language Understanding) ( [Hendrycks et al., 2020](https://arxiv.org/abs/2009.03300) ), un banc d'essai de modèles de base largement utilisé, entre 2022 et 2024.

![Graphique avec des nombres et un certain nombre de points. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0111.png)

###### Figure 1-11. Le coût du raisonnement en IA diminue rapidement avec le temps. Image tirée de [Katrina Nguyen](https://oreil.ly/UyL8r) (2024).

Cependant, même ces changements positifs peuvent engendrer des frictions dans vos flux de travail. Il vous faudra rester vigilant et réaliser une analyse coûts-avantages de chaque investissement technologique. La meilleure option aujourd'hui pourrait se révéler la pire demain. Vous pourriez décider de développer un modèle en interne, car cela semble moins coûteux que de faire appel à des prestataires, pour vous apercevoir trois mois plus tard que ces prestataires ont divisé leurs prix par deux, rendant ainsi le développement interne onéreux. Vous pourriez investir dans une solution tierce et adapter votre infrastructure en conséquence, pour finalement voir le fournisseur faire faillite faute de financement.

Certains changements sont plus faciles à appréhender. Par exemple, la convergence des fournisseurs de modèles vers une même API simplifie le passage d'une API à une autre. Cependant, chaque modèle présentant ses spécificités, ses points forts et ses faiblesses, les développeurs utilisant le nouveau modèle devront adapter leurs flux de travail, leurs invites et leurs données. Sans infrastructure adéquate de gestion des versions et d'évaluation, ce processus peut s'avérer complexe.

Certains changements sont plus difficiles à appréhender, notamment ceux liés à la réglementation. Les technologies d'IA sont considérées comme des enjeux de sécurité nationale par de nombreux pays, ce qui signifie que les ressources dédiées à l'IA, y compris la puissance de calcul, les talents et les données, sont soumises à une réglementation stricte. L'entrée en vigueur du Règlement général sur la protection des données (RGPD) en Europe, par exemple, aurait coûté aux entreprises environ [9 milliards de dollars](https://oreil.ly/eDfB8) pour se conformer à la réglementation. La disponibilité de la puissance de calcul peut évoluer du jour au lendemain, de nouvelles lois imposant des restrictions accrues sur les acteurs autorisés à acheter et à vendre des ressources de calcul (voir le [décret présidentiel américain d'octobre 2023](https://oreil.ly/eYTmr) ). Si votre fournisseur de GPU est soudainement interdit de vente dans votre pays, vous risquez de rencontrer des difficultés.

Certains changements peuvent même être fatals. Par exemple, la réglementation relative à la propriété intellectuelle (PI) et à l'utilisation de l'IA est encore en pleine évolution. Si vous développez votre produit à partir d'un modèle entraîné avec des données tierces, pouvez-vous être certain que la PI de votre produit vous appartiendra toujours ? De nombreuses entreprises fortement dépendantes de la PI, comme les studios de jeux vidéo, hésitent à utiliser l'IA par crainte de perdre leurs droits de propriété intellectuelle ultérieurement.

Une fois que vous vous êtes engagé à développer un produit d'IA, examinons la pile technologique nécessaire à la création de ces applications.

# La pile d'ingénierie de l'IA

La croissance fulgurante de l'ingénierie de l'IA a également engendré un engouement considérable et une forte peur de rater quelque chose (FOMO). Le nombre de nouveaux outils, techniques, modèles et applications introduits chaque jour peut être vertigineux. Plutôt que de tenter de suivre le rythme effréné de ce domaine en constante évolution, penchons-nous sur les fondements de l'ingénierie de l'IA.

Pour comprendre l'ingénierie de l'IA, il est important de savoir qu'elle découle de l'ingénierie du ML. Lorsqu'une entreprise commence à expérimenter avec des modèles de base, il est naturel que son équipe de ML existante prenne la tête de ce projet. Certaines entreprises traitent l'ingénierie de l'IA de la même manière que l'ingénierie du ML, comme le montre la [figure 1-12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_12_1730130814920130) .

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0112.png)

###### Figure 1-12. De nombreuses entreprises regroupent l'ingénierie de l'IA et l'ingénierie du ML sous une même bannière, comme le montrent les titres des offres d'emploi sur LinkedIn du 17 décembre 2023.

Certaines entreprises ont des descriptions de poste distinctes pour l'ingénierie de l'IA, comme le montre [la figure 1-13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_13_1730130814920151) .

Quelle que soit la place qu'occupent les ingénieurs en IA et les ingénieurs en apprentissage automatique au sein des organisations, leurs rôles présentent de nombreuses similitudes. Les ingénieurs en apprentissage automatique peuvent ajouter l'ingénierie de l'IA à leurs compétences pour élargir leurs perspectives d'emploi. Cependant, certains ingénieurs en IA n'ont aucune expérience préalable en apprentissage automatique.

Pour mieux comprendre l'ingénierie de l'IA et en quoi elle diffère de l'ingénierie ML traditionnelle, la section suivante détaille les différentes couches du processus de création d'applications d'IA et examine le rôle que joue chaque couche dans l'ingénierie de l'IA et l'ingénierie ML.

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0113.png)

###### Figure 1-13. Certaines entreprises ont des descriptions de poste distinctes pour l'ingénierie de l'IA, comme le montrent les titres d'offres d'emploi sur LinkedIn du 17 décembre 2023.

## Les trois couches de la pile d'IA

Toute architecture d'application d'IA comporte trois couches : le développement de l'application, le développement du modèle et l'infrastructure. Lors du développement d'une application d'IA, vous commencerez généralement par la couche supérieure et descendrez ensuite dans les couches inférieures selon les besoins.

Développement d'applications

Grâce à la disponibilité des modèles, chacun peut les utiliser pour développer des applications. C'est la couche qui a connu le plus d'activité ces deux dernières années et qui continue d'évoluer rapidement. Le développement d'applications consiste à fournir un modèle accompagné d'instructions pertinentes et du contexte nécessaire. Cette couche exige une évaluation rigoureuse. De bonnes applications requièrent également de bonnes interfaces.

Développement de modèles

Cette couche fournit les outils nécessaires au développement de modèles, notamment des frameworks pour la modélisation, l'entraînement, l'ajustement fin et l'optimisation de l'inférence. Les données étant essentielles au développement de modèles, cette couche inclut également l'ingénierie des jeux de données. Le développement de modèles requiert par ailleurs une évaluation rigoureuse.

Infrastructure

À la base de la pile se trouve l'infrastructure, qui comprend les outils pour le déploiement des modèles, la gestion des données et des calculs, et la surveillance.

Ces trois niveaux et des exemples de responsabilités pour chaque niveau sont illustrés dans [la figure 1-14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_14_1730130814920166) .

![Diagramme de développement logiciel. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0114.png)

###### Figure 1-14. Trois couches de la pile d'ingénierie de l'IA.

Pour appréhender l'évolution du paysage des modèles de base, j'ai effectué, en mars 2024, une recherche sur GitHub afin de recenser tous les dépôts liés à l'IA ayant au moins 500 étoiles. Compte tenu de l'importance de GitHub, ces données me semblent un bon indicateur de l'écosystème. Mon analyse a également inclus les dépôts d'applications et de modèles, qui sont respectivement le fruit des phases de développement d'applications et de modélisation. J'ai ainsi identifié 920 dépôts. [La figure 1-15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_15_1730130814920182) présente le nombre cumulé de dépôts dans chaque catégorie, mois après mois.

![Graphique représentant un certain nombre de personnes. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0115.png)

###### Figure 1-15. Nombre cumulatif de dépôts par catégorie au fil du temps.

Les données révèlent une forte augmentation du nombre d'outils d'IA en 2023, suite à l'introduction de Stable Diffusion et de ChatGPT. Cette année-là, les catégories ayant connu les plus fortes progressions étaient les applications et leur développement. La couche infrastructure a également enregistré une certaine croissance, mais bien moindre que celle des autres couches. Ce résultat est conforme aux attentes. Malgré l'évolution des modèles et des applications, les besoins fondamentaux en infrastructure – gestion des ressources, diffusion, supervision, etc. – demeurent inchangés.

Ceci nous amène au point suivant. Si l'enthousiasme et la créativité autour des modèles de base sont sans précédent, de nombreux principes de développement d'applications d'IA demeurent inchangés. Dans le contexte des entreprises, les applications d'IA doivent toujours résoudre des problèmes métiers ; il est donc essentiel d'établir une correspondance entre les indicateurs métiers et les indicateurs d'apprentissage automatique. L'expérimentation systématique reste indispensable. En ingénierie d'apprentissage automatique classique, on teste différents hyperparamètres. Avec les modèles de base, on teste différents modèles, invites, algorithmes de récupération, variables d'échantillonnage, etc. (Les variables d'échantillonnage sont abordées au [chapitre 2.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) ) Notre objectif reste d'optimiser la vitesse et le coût d'exécution des modèles. Il est toujours important de mettre en place une boucle de rétroaction afin d'améliorer itérativement nos applications grâce aux données de production.

Cela signifie qu'une grande partie des connaissances acquises et partagées par les ingénieurs en apprentissage automatique au cours de la dernière décennie reste pertinente. Cette expérience collective facilite la création d'applications d'IA pour tous. Toutefois, ces principes fondamentaux s'appuient sur de nombreuses innovations propres à l'ingénierie de l'IA, que nous explorerons dans cet ouvrage.

## Ingénierie de l'IA versus ingénierie du ML

Si les principes immuables du déploiement d'applications d'IA sont rassurants, il est tout aussi important de comprendre les évolutions récentes. Cette compréhension est précieuse pour les équipes souhaitant adapter leurs plateformes existantes à de nouveaux cas d'usage de l'IA, ainsi que pour les développeurs désireux d'acquérir les compétences nécessaires pour rester compétitifs sur un marché en pleine mutation.

De manière générale, la création d'applications à l'aide de modèles de base diffère aujourd'hui de l'ingénierie ML traditionnelle de trois manières majeures :

1. Sans modèles de base, vous devez entraîner vos propres modèles pour vos applications. Avec l'ingénierie de l'IA, vous utilisez un modèle déjà entraîné. Cela signifie que l'ingénierie de l'IA se concentre moins sur la modélisation et l'entraînement, et davantage sur l'adaptation du modèle.
    
2. L'ingénierie de l'IA travaille avec des modèles plus volumineux, plus gourmands en ressources de calcul et présentant une latence plus élevée que l'ingénierie ML traditionnelle. Il en résulte une pression accrue pour une optimisation efficace de l'entraînement et de l'inférence. L'utilisation intensive des modèles de calcul implique que de nombreuses entreprises ont désormais besoin de plus de GPU et travaillent avec des clusters de calcul plus importants qu'auparavant, ce qui engendre un besoin accru d'ingénieurs maîtrisant l'utilisation des GPU et des grands clusters.<sup> [23 </sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id640)
    
3. L'ingénierie de l'IA utilise des modèles capables de produire des résultats ouverts. Ces résultats ouverts confèrent aux modèles la flexibilité nécessaire pour accomplir davantage de tâches, mais les rendent également plus difficiles à évaluer. C'est pourquoi l'évaluation constitue un problème majeur en ingénierie de l'IA.
    

En résumé, l'ingénierie de l'IA se distingue de l'ingénierie du ML par le fait qu'elle se concentre moins sur le développement de modèles et davantage sur leur adaptation et leur évaluation. J'ai évoqué l'adaptation de modèles à plusieurs reprises dans ce chapitre ; avant de poursuivre, je tiens à m'assurer que nous partageons la même définition. De manière générale, les techniques d'adaptation de modèles se divisent en deux catégories, selon qu'elles nécessitent ou non la mise à jour des poids du modèle.

_Les techniques basées sur les instructions, comme l'ingénierie des instructions, adaptent un modèle sans modifier ses pondérations._ L'adaptation consiste à fournir des instructions et un contexte au modèle lui-même. L'ingénierie des instructions est plus facile à mettre en œuvre et nécessite moins de données. De nombreuses applications performantes ont été développées uniquement grâce à cette technique. Sa simplicité d'utilisation permet d'expérimenter avec davantage de modèles, augmentant ainsi les chances de trouver un modèle particulièrement adapté à vos applications. Cependant, l'ingénierie des instructions peut s'avérer insuffisante pour les tâches complexes ou les applications aux exigences de performance strictes.

_Le finetuning, quant à lui, nécessite la mise à jour des poids du modèle._ Il s'agit d'adapter un modèle en modifiant le modèle lui-même. En général, les techniques de finetuning sont plus complexes et requièrent davantage de données, mais elles peuvent améliorer considérablement la qualité, la latence et le coût du modèle. De nombreuses opérations sont impossibles sans modifier les poids du modèle, comme son adaptation à une nouvelle tâche à laquelle il n'a pas été exposé lors de l'entraînement.

À présent, examinons de plus près les couches de développement d'applications et de modèles pour voir comment chacune a évolué avec l'ingénierie de l'IA, en commençant par ce que les ingénieurs en apprentissage automatique connaissent déjà bien. Cette section présente les différents processus impliqués dans le développement d'une application d'IA. Leur fonctionnement sera détaillé tout au long de cet ouvrage.

### Développement de modèles

_Le développement de modèles_ est la couche la plus souvent associée à l'ingénierie traditionnelle du machine learning. Il comporte trois responsabilités principales : la modélisation et l'entraînement, l'ingénierie des jeux de données et l'optimisation de l'inférence. L'évaluation est également nécessaire, mais comme la plupart des développeurs la découvrent d'abord au niveau du développement applicatif, je l'aborderai dans la section suivante.

#### Modélisation et formation

_La modélisation et l'entraînement_ désignent le processus de conception d'une architecture de modèle, son entraînement et son optimisation. Parmi les outils de cette catégorie, on peut citer TensorFlow de Google, Transformers de Hugging Face et PyTorch de Meta.

Le développement de modèles d'apprentissage automatique exige des connaissances spécialisées. Il nécessite la maîtrise de différents types d'algorithmes (tels que le clustering, la régression logistique, les arbres de décision et le filtrage collaboratif) et d'architectures de réseaux de neurones (comme les réseaux à propagation avant, récurrents, convolutionnels et transformeurs). Il requiert également la compréhension du fonctionnement de l'apprentissage d'un modèle, notamment des concepts tels que la descente de gradient, la fonction de perte et la régularisation.

Grâce aux modèles de base disponibles, la maîtrise du machine learning n'est plus indispensable au développement d'applications d'IA. J'ai rencontré de nombreux développeurs d'applications d'IA talentueux et performants qui ne s'intéressent absolument pas à l'apprentissage de la descente de gradient. Cependant, cette maîtrise reste extrêmement précieuse, car elle élargit la palette d'outils disponibles et facilite le dépannage lorsqu'un modèle ne fonctionne pas comme prévu.

# Sur les différences entre l'entraînement, le pré-entraînement, le réglage fin et le post-entraînement

L'entraînement implique toujours une modification des poids du modèle, mais toutes les modifications apportées à ces poids ne constituent pas un entraînement. Par exemple, la quantification, qui consiste à réduire la précision des poids du modèle, modifie techniquement les valeurs de ces poids, mais n'est pas considérée comme un entraînement.

Le terme « entraînement » peut souvent être utilisé à la place de « pré-entraînement », « mise au point » et « post-entraînement », qui font référence à différentes phases de l’entraînement :

Pré-formation

_Le pré-entraînement consiste à_ entraîner un modèle à partir de zéro, c'est-à-dire à initialiser aléatoirement ses poids. Pour les modèles linéaires à longue portée (LLM), le pré-entraînement implique souvent l'entraînement d'un modèle pour la complétion de texte. De toutes les étapes d'entraînement, le pré-entraînement est de loin la plus gourmande en ressources. Pour le modèle InstructGPT, il peut absorber jusqu'à [98 % des ressources de calcul et de données totales](https://oreil.ly/G3LUh) . Le pré-entraînement est également long. Une petite erreur lors de cette étape peut engendrer des pertes financières importantes et retarder considérablement le projet. Du fait de son caractère gourmand en ressources, le pré-entraînement est devenu un art maîtrisé par peu de personnes. Les experts en pré-entraînement de grands modèles sont, quant à eux, très recherchés.<sup> [24</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id642)

Réglage fin

Le fine-tuning consiste à poursuivre l'entraînement d'un modèle préalablement entraîné ; les poids du modèle sont issus de la phase d'entraînement précédente. Comme le modèle possède déjà certaines connaissances acquises lors du pré-entraînement, le fine-tuning requiert généralement moins de ressources (données et puissance de calcul, par exemple) que le pré-entraînement.

Après la formation

_Le terme « post-entraînement »_ désigne souvent le processus d'entraînement d'un modèle après la phase de pré-entraînement. Conceptuellement, post-entraînement et ajustement fin sont synonymes et peuvent être utilisés indifféremment. Cependant, on les emploie parfois différemment pour souligner des objectifs distincts. On parle généralement de post-entraînement lorsqu'il est effectué par les développeurs du modèle. Par exemple, OpenAI peut post-entraîner un modèle pour améliorer sa capacité à suivre des instructions avant sa publication. On parle d'ajustement fin lorsqu'il est effectué par les développeurs d'applications. Par exemple, vous pouvez ajuster un modèle OpenAI (qui a peut-être lui-même été post-entraîné) pour l'adapter à vos besoins.

La préformation et la postformation forment un continuum. [Leurs](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id645) processus et outils sont très similaires. Leurs différences sont explorées plus en détail dans les chapitres [2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch02.html#ch02_understanding_foundation_models_1730147895571359) et [7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) .

Certaines personnes utilisent le terme « entraînement » pour désigner l'ingénierie des prompts, ce qui est incorrect. J'ai lu un [article](https://oreil.ly/0VqmX) [_de Business Insider_](https://oreil.ly/0VqmX) où l'auteure expliquait avoir entraîné ChatGPT à imiter sa jeune personnalité. Pour ce faire, elle a intégré à ChatGPT les entrées de son journal intime d'enfance. Dans le langage courant, l'utilisation du terme « _entraînement »_ par l'auteure est correcte, puisqu'elle apprend au modèle à faire quelque chose. Mais techniquement, si l'on apprend à un modèle ce qu'il doit faire grâce au contexte qu'il reçoit en entrée, on pratique l'ingénierie des prompts. De même, j'ai vu des personnes utiliser le terme « _ajustement fin »_ pour désigner une véritable ingénierie des prompts.

#### Ingénierie des ensembles de données

_L'ingénierie des jeux de données_ consiste à organiser, générer et annoter les données nécessaires à l'entraînement et à l'adaptation des modèles d'IA.

En ingénierie ML traditionnelle, la plupart des cas d'utilisation sont fermés : la sortie d'un modèle ne peut prendre que des valeurs prédéfinies. Par exemple, la classification des spams, avec seulement deux sorties possibles (« spam » et « non-spam »), est un cas fermé. Les modèles de base, en revanche, sont ouverts. Annoter des requêtes ouvertes est bien plus complexe qu'annoter des requêtes fermées : il est plus facile de déterminer si un courriel est un spam que de rédiger une dissertation. L'annotation des données représente donc un défi bien plus important pour l'ingénierie de l'IA.

Une autre différence réside dans le fait que l'ingénierie ML traditionnelle travaille davantage avec des données tabulaires, tandis que les modèles de base fonctionnent avec des données non structurées. En ingénierie IA, la manipulation des données porte principalement sur la déduplication, la tokenisation, la récupération du contexte et le contrôle qualité, incluant la suppression des informations sensibles et des données toxiques. L'ingénierie des jeux de données est le sujet du [chapitre 8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) .

De nombreux experts affirment que, les modèles étant désormais des produits de base, les données deviendront le principal facteur de différenciation, rendant l'ingénierie des jeux de données plus importante que jamais. La quantité de données nécessaire dépend de la technique d'adaptation utilisée. L'entraînement d'un modèle à partir de zéro requiert généralement plus de données que le fine-tuning, qui, à son tour, en requiert davantage que l'ingénierie rapide.

Quelle que soit la quantité de données dont vous avez besoin, une expertise en matière de données est utile lors de l'examen d'un modèle, car ses données d'entraînement fournissent des indications importantes sur les forces et les faiblesses de ce modèle.

#### Optimisation de l'inférence

_L'optimisation de l'inférence_ vise à rendre les modèles plus rapides et moins coûteux. Elle a toujours été essentielle en ingénierie du machine learning. Les utilisateurs apprécient les modèles plus rapides, et les entreprises ont toujours intérêt à réduire les coûts d'inférence. Cependant, à mesure que les modèles de base évoluent et engendrent des coûts et une latence d'inférence encore plus élevés, l'optimisation de l'inférence devient cruciale.

L'un des problèmes des modèles de base réside dans leur caractère souvent _autorégressif_ : les jetons sont générés séquentiellement. Si la génération d'un jeton prend 10 ms, il faudra une seconde pour générer une sortie de 100 jetons, et davantage pour des sorties plus longues. Face à l'impatience croissante des utilisateurs, réduire la latence des applications d'IA à [100 ms,](https://oreil.ly/gGXZ-) seuil attendu pour une application Internet classique, représente un défi majeur. L'optimisation de l'inférence est devenue un domaine de recherche très actif, tant dans l'industrie que dans le monde académique.

Un résumé de la façon dont l’importance des différentes catégories de développement de modèles évolue avec l’ingénierie de l’IA est présenté dans [le tableau 1-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_table_4_1730130814941579) .

Tableau 1-4. Comment les différentes responsabilités liées au développement de modèles ont évolué avec les modèles de base.
|Catégorie|Construction avec l'apprentissage automatique traditionnel|Construire avec des modèles de fondation|
|---|---|---|
|Modélisation et formation|Des connaissances en apprentissage automatique sont nécessaires pour entraîner un modèle à partir de zéro.|Les connaissances en apprentissage automatique sont un atout, mais pas une nécessité [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id652)|
|Ingénierie des ensembles de données|Plus d'informations sur l'ingénierie des caractéristiques, notamment avec les données tabulaires|Moins axé sur l'ingénierie des caractéristiques et davantage sur la déduplication des données, la tokenisation, la récupération du contexte et le contrôle qualité.|
|Optimisation de l'inférence|Important|Plus important encore|
|[un](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id652-marker)Nombreux sont ceux qui contesteraient cette affirmation, arguant que la connaissance du ML est indispensable.|   |   |

Les techniques d'optimisation de l'inférence, notamment la quantification, la distillation et le parallélisme, sont abordées dans les chapitres [7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch07.html#ch07) à [9.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301).

### Développement d'applications

En ingénierie ML traditionnelle, où les équipes développent des applications à l'aide de leurs modèles propriétaires, la qualité du modèle constitue un facteur de différenciation. Avec les modèles de base, où de nombreuses équipes utilisent le même modèle, la différenciation doit provenir du processus de développement de l'application.

La couche de développement d'applications comprend les responsabilités suivantes : évaluation, ingénierie rapide et interface IA.

#### Évaluation

_L'évaluation_ vise à atténuer les risques et à identifier les opportunités. Elle est essentielle tout au long du processus d'adaptation des modèles. Elle est nécessaire pour sélectionner les modèles, mesurer les progrès, déterminer si une application est prête à être déployée et détecter les problèmes et les pistes d'amélioration en production.

Bien que l'évaluation ait toujours été importante en ingénierie du ML, elle l'est d'autant plus pour les modèles de base, et ce pour de nombreuses raisons. Les difficultés liées à l'évaluation de ces modèles sont abordées au [chapitre 3.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) En résumé, ces difficultés découlent principalement de la nature ouverte et des capacités étendues des modèles de base. Par exemple, pour des tâches de ML fermées comme la détection de fraude, il existe généralement des valeurs de référence attendues auxquelles comparer les résultats du modèle. Si un résultat diffère de la valeur attendue, on sait que le modèle est erroné. En revanche, pour une tâche comme celle des chatbots, le nombre de réponses possibles à chaque requête est tellement important qu'il est impossible de constituer une liste exhaustive de valeurs de référence pour comparer la réponse d'un modèle.

L'existence de nombreuses techniques d'adaptation complique également l'évaluation. Un système peu performant avec une technique donnée peut être bien plus performant avec une autre.Lors du lancement de Gemini en décembre 2023, Google a affirmé queGemini surpasse ChatGPT dans le benchmark MMLU ( [Hendrycks et al., 2020](https://arxiv.org/abs/2009.03300) ). Google a évalué Gemini à l'aide d'une technique d'ingénierie des prompts appelée [CoT@32](https://oreil.ly/VDwaR) . Dans cette technique, Gemini a été confronté à 32 exemples, tandis que ChatGPT n'en a été confronté qu'à 5. Lorsque les deux modèles ont été confrontés à cinq exemples, ChatGPT a obtenu de meilleurs résultats, comme le montre le [tableau 1-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_table_5_1730130814941611) .

Tableau 1-5. Différentes invites peuvent entraîner des performances très différentes des modèles, comme on peut le constater dans le rapport technique de Gemini (décembre 2023).


| Gémeaux Ultra         | Gemini Pro            | GPT-4                                       | GPT-3.5                            | PaLM 2-L          | Claude 2              | Inflexion-2               | Grok 1                | Lama-2              |       |
| --------------------- | --------------------- | ------------------------------------------- | ---------------------------------- | ----------------- | --------------------- | ------------------------- | --------------------- | ------------------- | ----- |
| Performances MMLU     | 90,04 %  <br>CoT@32   | 79,13 %  <br>CoT@8                          | 87,29 %  <br>CoT@32  <br>(via API) | 70 %  <br>5 coups | 78,4 %  <br>(5 coups) | 78,5 %  <br>CoT à 5 coups | 79,6 %  <br>(5 coups) | 73,0 %  <br>5 coups | 68,0% |
| 83,7 %  <br>(5 coups) | 71,8 %  <br>(5 coups) | 86,4 % (  <br>5 coups) (données rapportées) |                                    |                   |                       |                           |                       |                     |       |

#### Ingénierie rapide et construction du contexte

_L'ingénierie de la réponse_ consiste à faire en sorte que les modèles d'IA adoptent les comportements souhaités à partir des seules données d'entrée, sans modifier les pondérations du modèle. L'évaluation de Gemini met en évidence l'impact de cette ingénierie sur les performances du modèle. Grâce à une technique d'ingénierie de la réponse différente, les performances de Gemini Ultra sur MMLU sont passées de 83,7 % à 90,04 %.

Il est possible d'obtenir des résultats remarquables avec un modèle grâce à de simples instructions. Avec les bonnes instructions, un modèle peut exécuter la tâche souhaitée, dans le format de votre choix. L'ingénierie des instructions ne se limite pas à indiquer au modèle ce qu'il doit faire. Il s'agit également de lui fournir le contexte et les outils nécessaires à l'exécution d'une tâche donnée. Pour les tâches complexes avec un contexte étendu, il peut être nécessaire de doter le modèle d'un système de gestion de la mémoire afin qu'il puisse conserver la trace de son historique. [Le chapitre 5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) traite de l'ingénierie des instructions et [le chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) de la construction du contexte.

#### Interface IA

_L'interface IA_ consiste à créer une interface permettant aux utilisateurs finaux d'interagir avec vos applications d'IA. Avant l'avènement des modèles de base, seules les organisations disposant des ressources nécessaires au développement de modèles d'IA pouvaient développer des applications d'IA. Ces applications étaient souvent intégrées aux produits existants des organisations. Par exemple, la détection de fraude était intégrée à Stripe, Venmo et PayPal. Les systèmes de recommandation faisaient partie des réseaux sociaux et des applications multimédias comme Netflix, TikTok et Spotify.

Grâce aux modèles de base, chacun peut créer des applications d'IA. Ces applications peuvent être déployées comme des produits autonomes ou intégrées à d'autres produits, y compris ceux développés par des tiers. Par exemple, ChatGPT et Perplexity sont des produits autonomes, tandis que Copilot de GitHub est couramment utilisé comme extension pour VSCode et Grammarly comme extension pour Google Docs. Midjourney peut être utilisé via son application web indépendante ou via son intégration à Discord.

Il est nécessaire de disposer d'outils offrant des interfaces pour les applications d'IA autonomes ou facilitant l'intégration de l'IA dans les produits existants. Voici quelques exemples d'interfaces qui gagnent en popularité pour les applications d'IA :

- Applications web, de bureau et mobiles autonomes. [26](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id668)
    
- Extensions de navigateur permettant aux utilisateurs d'interroger rapidement des modèles d'IA pendant leur navigation.
    
- Des chatbots intégrés aux applications de messagerie instantanée comme Slack, Discord, WeChat et WhatsApp.
    
- De nombreux produits, tels que VSCode, Shopify et Microsoft 365, proposent des API permettant aux développeurs d'intégrer l'IA à leurs produits sous forme de plugins et d'extensions. Ces API peuvent également être utilisées par des agents d'IA pour interagir avec le monde, comme expliqué au [chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) .
    

Bien que l'interface de chat soit la plus couramment utilisée, les interfaces d'IA peuvent également être vocales (comme avec les assistants vocaux) ou incarnées (comme dans la réalité augmentée et virtuelle).

Ces nouvelles interfaces d'IA offrent également de nouvelles méthodes de collecte et d'analyse des retours utilisateurs. L'interface conversationnelle facilite grandement la transmission de commentaires en langage naturel, mais l'extraction de ces retours s'avère plus complexe. La conception des systèmes de retours utilisateurs est abordée dans [référence manquante].[Chapitre 10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_ai_engineering_architecture_and_user_feedback_1730130985311851) .

Un résumé de la façon dont l'importance des différentes catégories de développement d'applications évolue avec l'ingénierie de l'IA est présenté dans [le tableau 1-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_table_6_1730130814941642) .

Tableau 1-6. L'importance des différentes catégories dans le développement d'applications pour l'ingénierie de l'IA et l'ingénierie du ML.
|Catégorie|Construction avec l'apprentissage automatique traditionnel|Construire avec des modèles de fondation|
|---|---|---|
|Interface IA|Moins important|Important|
|Ingénierie rapide|Non applicable|Important|
|Évaluation|Important|Plus important encore|

## Ingénierie en IA versus ingénierie full-stack

L'importance accrue accordée au développement d'applications, notamment aux interfaces, rapproche l'ingénierie de l'IA du développement full-stack.<sup> [27</sup>](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id675) Cette importance grandissante des interfaces entraîne une évolution de la conception des outils d'IA afin d'attirer davantage d'ingénieurs front-end. Traditionnellement, l'ingénierie du ML est centrée sur Python. Avant l'avènement des modèles de base, les frameworks de ML les plus populaires prenaient principalement en charge les API Python. Aujourd'hui, Python reste populaire, mais on observe également une prise en charge croissante des API JavaScript, avec [LangChain.js](https://github.com/langchain-ai/langchainjs) , [Transformers.js](https://github.com/huggingface/transformers.js) , [la bibliothèque Node d'OpenAI](https://github.com/openai/openai-node) et [le SDK d'IA de Vercel](https://github.com/vercel/ai) .

Si de nombreux ingénieurs en IA sont issus du ML traditionnel, ils sont de plus en plus nombreux à provenir du développement web ou du développement full-stack. Un avantage des ingénieurs full-stack par rapport aux ingénieurs en ML traditionnels réside dans leur capacité à transformer rapidement des idées en démonstrations, à recueillir des retours et à itérer.

En ingénierie ML traditionnelle, on commence généralement par la collecte de données et l'entraînement d'un modèle. La construction du produit intervient en dernier. Cependant, grâce aux modèles d'IA facilement disponibles aujourd'hui, il est possible de commencer par la construction du produit et d'investir dans les données et les modèles uniquement lorsque le produit s'avère prometteur, comme illustré dans [la figure 1-16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_figure_16_1730130814920205) .

![Gros plan sur des flèches. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_0116.png)

###### Figure 1-16. Le nouveau flux de travail d'ingénierie en IA récompense ceux qui savent itérer rapidement. Image reproduite à partir de « The Rise of the AI ​​Engineer » ( [Shawn Wang, 2023](https://oreil.ly/OOZK-) ).

En ingénierie ML traditionnelle, le développement de modèles et le développement de produits sont souvent des processus disjoints, les ingénieurs ML étant rarement impliqués dans les décisions relatives aux produits au sein de nombreuses organisations. Cependant, avec les modèles de base, les ingénieurs en IA ont tendance à être beaucoup plus impliqués dans la conception du produit.

# Résumé

Ce chapitre poursuit un double objectif. Premièrement, expliquer l'émergence de l'ingénierie de l'IA en tant que discipline, grâce à la disponibilité de modèles fondamentaux. Deuxièmement, présenter le processus nécessaire au développement d'applications basées sur ces modèles. J'espère que ce chapitre a atteint cet objectif. Étant un chapitre introductif, il n'a fait qu'effleurer de nombreux concepts, qui seront approfondis dans la suite de l'ouvrage.

Ce chapitre abordait l'évolution rapide de l'IA ces dernières années. Il retraçait certaines des transformations les plus marquantes, à commencer par le passage des modèles de langage aux grands modèles de langage, grâce à une approche d'apprentissage appelée auto-supervision. Il expliquait ensuite comment les modèles de langage ont intégré d'autres modalités de données pour devenir des modèles de base, et comment ces derniers ont donné naissance à l'ingénierie de l'IA.

La croissance rapide de l'ingénierie de l'IA est motivée par les nombreuses applications rendues possibles par les capacités émergentes des modèles de base. Ce chapitre a présenté quelques-uns des exemples d'applications les plus réussis, tant pour les consommateurs que pour les entreprises. Malgré le nombre impressionnant d'applications d'IA déjà en production, nous n'en sommes qu'aux prémices de l'ingénierie de l'IA, et d'innombrables innovations restent à développer.

Avant de développer une application, une question importante, mais souvent négligée, se pose : faut-il la développer ? Ce chapitre aborde cette question ainsi que les principaux éléments à prendre en compte pour le développement d’applications d’IA.

Bien que l'ingénierie de l'IA soit un terme récent, elle découle de l'ingénierie du ML, discipline englobant la conception d'applications à l'aide de modèles de ML. De nombreux principes du ML restent applicables à l'ingénierie de l'IA. Toutefois, cette dernière soulève également de nouveaux défis et apporte des solutions inédites. La dernière section de ce chapitre aborde l'architecture de l'ingénierie de l'IA et son évolution par rapport au ML.

Un aspect de l'ingénierie de l'IA particulièrement difficile à retranscrire par écrit réside dans l'incroyable énergie collective, la créativité et le talent d'ingénierie que déploie la communauté. Cet enthousiasme collectif peut souvent être déroutant, tant il est impossible de se tenir au courant des nouvelles techniques, découvertes et prouesses d'ingénierie qui semblent se succéder sans cesse.

L'un des avantages est que, l'IA excellant dans l'agrégation d'informations, elle peut nous aider à rassembler et à synthétiser toutes ces nouveautés. Cependant, les outils ont leurs limites. Plus un domaine est vaste et complexe, plus il est crucial de disposer d'un cadre de référence pour s'y repérer. Cet ouvrage vise précisément à fournir un tel cadre.

Le reste du livre explorera ce cadre étape par étape, en commençant par l'élément fondamental de l'ingénierie de l'IA : les modèles de base qui rendent possibles tant d'applications étonnantes.

[1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id534-marker)Dans ce livre, j'utilise _le terme ML traditionnel_ pour désigner tout ML antérieur aux modèles de base.

[2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id536-marker)Pour les langues autres que l'anglais, un seul caractère Unicode peut parfois être représenté par plusieurs jetons.

[3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id541-marker)Les modèles de langage autorégressifs sont parfois appelés [modèles de langage causaux](https://oreil.ly/h0Y8x) .

[4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id542-marker)Techniquement, un modèle de langage masqué comme BERT peut également être utilisé pour la génération de texte si on s'y prend vraiment bien.

[5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id545-marker)Le coût réel de l'étiquetage des données varie en fonction de plusieurs facteurs, notamment la complexité de la tâche, son volume (les grands ensembles de données entraînent généralement des coûts par échantillon plus faibles) et le prestataire de services d'étiquetage. Par exemple, en septembre 2024, [Amazon SageMaker Ground Truth](https://oreil.ly/EVXJl) facturait 8 centimes par image pour l'étiquetage de moins de 50 000 images, mais seulement 2 centimes par image pour l'étiquetage de plus d'un million d'images.

[6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id546-marker)C'est un peu comme pour les humains : il est important de savoir quand se taire.

[7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id547-marker)À l'école, on m'a appris que les paramètres d'un modèle incluaient à la fois les poids et les biais du modèle. Cependant, aujourd'hui, on utilise généralement le terme « poids du modèle » pour désigner l'ensemble des paramètres.

[8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id549-marker)Il peut sembler paradoxal que des modèles plus grands nécessitent davantage de données d'entraînement. Si un modèle est plus performant, ne devrait-il pas nécessiter moins d'exemples pour apprendre ? Cependant, notre objectif n'est pas d'obtenir des performances équivalentes entre un grand modèle et un petit modèle utilisant les mêmes données, mais d'optimiser les performances globales du modèle.

[9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id561-marker)À titre de comparaison, les dépenses totales des États-Unis pour les écoles primaires et secondaires publiques s'élèvent à environ 900 milliards de dollars, soit seulement neuf fois les investissements dans l'IA aux États-Unis.

[10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id566-marker)Anecdote amusante : au 16 septembre 2024, le site web [_theresanaiforthat.com_](https://theresanaiforthat.com/) recense 16 814 IA pour 14 688 tâches et 4 803 emplois.

[11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id567-marker)Explorer différentes applications d'IA est sans doute l'un des aspects que j'ai le plus appréciés dans l'écriture de ce livre. C'est passionnant de voir ce que les gens développent. Vous trouverez ici la [liste des applications d'IA open source](https://huyenchip.com/llama-police) que je suis. Cette liste est mise à jour toutes les 12 heures.

[12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id572-marker)Les entreprises consacrent généralement des sommes importantes à la publicité et au marketing ; l’automatisation de ces processus peut donc engendrer des économies considérables. En moyenne, 11 % du budget d’une entreprise est alloué au marketing. Voir [« Les budgets marketing varient selon le secteur d’activité »](https://oreil.ly/D0-yA) (Christine Moorman, _WSJ_ , 2017).

[13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id574-marker)J'ai trouvé l'IA très utile lors de l'écriture de ce livre, et je suis convaincu qu'elle pourra automatiser de nombreuses étapes du processus. Lorsque j'écris de la fiction, je demande souvent à l'IA de me suggérer des idées sur la suite des événements ou sur la réaction d'un personnage face à une situation. Je suis encore en train d'évaluer quels types d'écriture peuvent être automatisés et lesquels ne le peuvent pas.

[14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id575-marker)Mon hypothèse est que nous deviendrons tellement méfiants envers le contenu sur Internet que nous ne lirons que le contenu généré par des personnes ou des marques en lesquelles nous avons confiance.

[15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id584-marker)Je suis surpris du temps qu'il faut à Apple et Amazon pour intégrer les avancées de l'IA générative à Siri et Alexa. Un ami pense que cela tient au fait que ces entreprises ont des exigences plus élevées en matière de qualité et de conformité, et que le développement d'interfaces vocales est plus long que celui des interfaces de chat.

[16](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id585-marker)Avertissement : Je suis conseiller chez Convai.

[17](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id592-marker)J'ai actuellement plus de 40 000 photos et vidéos dans Google Photos. Sans intelligence artificielle, il me serait quasiment impossible de retrouver les photos que je souhaite, quand je le souhaite.

[18](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id593-marker)Personnellement, je trouve aussi que l'IA est performante pour expliquer les données et les graphiques. Face à un graphique complexe contenant trop d'informations, je demande à ChatGPT de me l'expliquer.

[19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id599-marker)Les petites startups, en revanche, doivent souvent privilégier le développement de leur produit et ne peuvent pas se permettre d'avoir ne serait-ce qu'une seule personne pour « observer les alentours ».

[20](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id607-marker)Une blague récurrente aux débuts de l'IA générative est que les startups spécialisées en IA ne sont que des wrappers d'OpenAI ou de Claude.

[21](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id608-marker)Pendant la rédaction de ce livre, je pouvais à peine parler à une start-up spécialisée en IA sans entendre l'expression « cercle vertueux des données ».

[22](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id609-marker)Avertissement : Je suis investisseur chez Photoroom.

[23](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id640-marker)Comme me l'a confié le responsable de l'IA d'une entreprise figurant au classement Fortune 500 : son équipe sait comment travailler avec 10 GPU, mais elle ne sait pas comment travailler avec 1 000 GPU.

[24](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id642-marker)Et on leur propose [des rémunérations incroyables](https://oreil.ly/AhANP) .

[25](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id645-marker)Si vous trouvez les termes « pré-entraînement » et « post-entraînement » peu inspirés, vous n'êtes pas seul. La communauté de recherche en IA excelle dans bien des domaines, mais la terminologie n'en fait pas partie. Nous avons déjà évoqué le fait que l'expression « grands modèles de langage » manque de pertinence scientifique en raison de l'ambiguïté du mot « grand ». Et j'aimerais vraiment que l'on cesse de publier des articles intitulés « X est tout ce dont vous avez besoin ».

[26](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id668-marker)Streamlit, Gradio et Plotly Dash sont des outils couramment utilisés pour créer des applications web d'IA.

[27](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#id675-marker)Anton Bacaj m'a dit que « l'ingénierie de l'IA n'est rien d'autre que de l'ingénierie logicielle à laquelle on a ajouté des modèles d'IA ».