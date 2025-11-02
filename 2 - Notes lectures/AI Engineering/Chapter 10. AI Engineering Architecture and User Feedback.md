Jusqu'à présent, cet ouvrage a abordé un large éventail de techniques permettant d'adapter les modèles de base à des applications spécifiques. Ce chapitre expliquera comment combiner ces techniques pour concevoir des produits performants.

Face à la multitude de techniques et d'outils d'ingénierie de l'IA disponibles, choisir les plus adaptés peut s'avérer complexe. Pour simplifier ce processus, ce chapitre propose une approche progressive. Il part de l'architecture la plus simple pour une application de modèle de base, met en lumière ses limites et ajoute graduellement des composants pour y remédier.

On pourrait passer une éternité à réfléchir à la manière de concevoir une application performante, mais le seul moyen de savoir si elle atteint réellement son objectif est de la mettre à l'épreuve auprès des utilisateurs. Les retours des utilisateurs ont toujours été essentiels au développement de produits, mais pour les applications d'IA, ils jouent un rôle encore plus crucial en tant que source de données pour l'amélioration des modèles. L'interface conversationnelle facilite la transmission des commentaires par les utilisateurs, mais complexifie l'interprétation des données par les développeurs. Ce chapitre abordera différents types de retours d'information en IA conversationnelle et expliquera comment concevoir un système permettant de recueillir les retours pertinents sans nuire à l'expérience utilisateur.

# Architecture d'ingénierie de l'IA

Une architecture d'IA complète peut s'avérer complexe. Cette section décrit le processus qu'une équipe pourrait suivre en production, en partant de l'architecture la plus simple et en ajoutant progressivement des composants. Malgré la diversité des applications d'IA, elles partagent de nombreux éléments communs. L'architecture proposée ici a été validée dans plusieurs entreprises et s'avère applicable à un large éventail d'applications, mais certaines applications peuvent présenter des spécificités.

Dans sa forme la plus simple, votre application reçoit une requête et l'envoie au modèle. Ce dernier génère une réponse, qui est renvoyée à l'utilisateur, comme illustré dans [la figure 10-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_1_1730130985262508) . Il n'y a ni enrichissement du contexte, ni garde-fous, ni optimisation. L' encadré _« API du modèle »_ désigne à la fois les API tierces (par exemple, OpenAI, Google, Anthropic) et les modèles auto-hébergés. La création d'un serveur d'inférence pour les modèles auto-hébergés est abordée au [chapitre 9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301) .

![Diagramme d'un modèle. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1001.png)

###### Figure 10-1. L'architecture la plus simple pour exécuter une application d'IA.

À partir de cette architecture simple, vous pouvez ajouter des composants supplémentaires au fur et à mesure des besoins. Le processus pourrait se dérouler comme suit :

1. Améliorer l'intégration du contexte dans un modèle en lui donnant accès à des sources de données externes et à des outils de collecte d'informations.
    
2. Mettez en place des garde-fous pour protéger votre système et vos utilisateurs.
    
3. Ajouter un routeur et une passerelle modèles pour prendre en charge les pipelines complexes et renforcer la sécurité.
    
4. Optimisez la latence et les coûts grâce à la mise en cache.
    
5. Ajoutez une logique complexe et écrivez des actions pour maximiser les capacités de votre système.
    

Ce chapitre suit la progression que j'observe généralement en production. Cependant, les besoins varient d'une application à l'autre. Il est donc conseillé de suivre l'ordre le plus adapté à votre cas.

Le suivi et l'observabilité, éléments essentiels à toute application de contrôle qualité et d'amélioration des performances, seront abordés à la fin de ce processus. L'orchestration, qui consiste à enchaîner tous ces composants, sera traitée ensuite.

## Étape 1. Améliorer le contexte

L'extension initiale d'une plateforme implique généralement l'ajout de mécanismes permettant au système de construire le contexte pertinent nécessaire au modèle pour répondre à chaque requête. Comme expliqué au [chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) , le contexte peut être construit grâce à divers mécanismes de recherche, notamment la recherche de texte, d'images et de données tabulaires. Il peut également être enrichi à l'aide d'outils permettant au modèle de collecter automatiquement des informations via des API telles que la recherche web, les actualités, la météo, les événements, etc.

_La construction du contexte est comparable à l'ingénierie des caractéristiques pour les modèles de base._ Elle fournit au modèle les informations nécessaires à la production d'un résultat. De par son rôle central dans la qualité des résultats d'un système, la construction du contexte est presque systématiquement prise en charge par les fournisseurs d'API de modèles. Par exemple, des fournisseurs comme OpenAI, Claude et Gemini permettent aux utilisateurs de télécharger des fichiers et d'utiliser des outils avec leurs modèles.

Cependant, tout comme les modèles diffèrent par leurs capacités, ces fournisseurs diffèrent également par leur prise en charge de la construction du contexte. Par exemple, ils peuvent imposer des limitations quant aux types de documents et à leur nombre. Une solution RAG spécialisée peut permettre d'importer autant de documents que votre base de données vectorielle peut en contenir, tandis qu'une API de modèle générique peut limiter le nombre de documents importés. Les différents frameworks diffèrent également par leurs algorithmes de recherche et autres configurations de recherche, comme la taille des segments. De même, en matière d'outils, les solutions diffèrent aussi par les types d'outils pris en charge et les modes d'exécution, notamment la prise en charge de l'exécution parallèle de fonctions ou des tâches de longue durée.

Avec la construction du contexte, l'architecture ressemble maintenant à [la figure 10-2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_2_1730130985262560) .

![Diagramme d'une base de données. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1002.png)

###### Figure 10-2. Une architecture de plateforme avec construction de contexte.

## Étape 2. Installer les  Guardrails

Les garde-fous contribuent à atténuer les risques et à protéger vos utilisateurs et vous-même. Ils doivent être mis en place dès qu'il existe un risque d'exposition. De manière générale, on peut les classer en deux catégories : les garde-fous relatifs aux entrées et ceux relatifs aux sorties.

### Guardrails d'entrée

Les garde-fous de saisie protègent généralement contre deux types de risques : la fuite d’informations privées vers des API externes et l’exécution de requêtes malveillantes compromettant votre système. [Le chapitre 5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) aborde différentes méthodes d’exploitation d’une application par des attaquants exploitant les requêtes malveillantes et explique comment s’en prémunir. Bien qu’il soit possible d’atténuer les risques, ils ne peuvent jamais être totalement éliminés, en raison de la nature même des réponses générées par les modèles et des erreurs humaines inévitables.

La divulgation d'informations privées à des API externes est un risque spécifique à l'utilisation d'API de modèles externes lorsque vous devez envoyer vos données en dehors de votre organisation. Cela peut se produire pour de nombreuses raisons, notamment les suivantes :

- Un employé copie des informations confidentielles de l'entreprise ou des informations privées d'un utilisateur dans une invite et les envoie à une API tierce [.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1761)
    
- Un développeur d'applications intègre les politiques et les données internes de l'entreprise dans l'invite de commandes du système de l'application.
    
- Un outil récupère des informations privées à partir d'une base de données interne et les ajoute au contexte.
    

Il n'existe aucune méthode infaillible pour éliminer les fuites potentielles lors de l'utilisation d'API tierces. Cependant, vous pouvez les atténuer en mettant en place des garde-fous. Vous pouvez utiliser l'un des nombreux outils disponibles qui détectent automatiquement les données sensibles. Vous spécifiez les données sensibles à détecter. Voici quelques exemples de classes de données sensibles courantes :

- Informations personnelles (numéros d'identification, numéros de téléphone, comptes bancaires)
    
- Visages humains
    
- Mots clés et expressions spécifiques associés à la propriété intellectuelle ou aux informations privilégiées de l'entreprise
    

De nombreux outils de détection de données sensibles utilisent l'IA pour identifier les informations potentiellement sensibles, par exemple pour déterminer si une chaîne de caractères ressemble à une adresse postale valide. Si une requête contient des informations sensibles, deux options s'offrent à vous : bloquer la requête entière ou supprimer les informations sensibles. Par exemple, vous pouvez masquer le numéro de téléphone d'un utilisateur avec l'espace réservé [NUMÉRO DE TÉLÉPHONE]. Si la réponse générée contient cet espace réservé, utilisez un dictionnaire inversé d'informations personnelles identifiables (IPI) qui associe cet espace réservé aux informations d'origine afin de pouvoir les démasquer, comme illustré.dans [la figure 10-3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_3_1730130985262586) .

![Capture d'écran d'une erreur informatique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1003.png)

###### Figure 10-3. Un exemple de masquage et de démasquage d'informations PII à l'aide d'une table de correspondance PII inversée pour éviter de les envoyer à des API externes.

## Guardrails de sortie

Un modèle peut échouer de multiples façons. Les garde-fous de sortie ont deux fonctions principales :

- Détection des échecs de sortie
    
- Spécifiez la politique de gestion des différents modes de défaillance
    

Pour détecter les résultats non conformes à vos normes, il est essentiel de comprendre la nature des défaillances. La défaillance la plus facile à repérer est celle où un modèle renvoie une réponse vide alors qu'il ne le devrait pas. Les [défaillances](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1763) varient selon les applications. Voici quelques défaillances courantes, réparties en deux grandes catégories : qualité et sécurité. Les défaillances de qualité sont abordées au [chapitre 4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) et les défaillances de sécurité au [chapitre 5.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) Pour rappel, voici quelques exemples :

- Qualité
    
    - Réponses mal formatées ne respectant pas le format de sortie attendu. Par exemple, l'application attend du JSON, mais le modèle génère un JSON invalide.
        
    - Réponses factuellement incohérentes hallucinées par le modèle.
        
    - En général, les réponses sont mauvaises. Par exemple, vous demandez au mannequin de rédiger une dissertation, et cette dissertation est tout simplement mauvaise.
        
- Sécurité
    
    - Réponses toxiques contenant des propos racistes, à caractère sexuel ou faisant référence à des activités illégales.
        
    - Réponses contenant des informations privées et sensibles.
        
    - Réponses déclenchant l'exécution d'outils et de codes à distance.
        
    - Réponses aux risques liés à l'image de marque qui donnent une image erronée de votre entreprise ou de vos concurrents.
        

Comme indiqué au [chapitre 5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) , pour les mesures de sécurité, il est important de suivre non seulement les failles de sécurité, mais aussi le taux de faux positifs. Il est possible d'avoir des systèmes trop sécurisés, par exemple un système qui bloque même les requêtes légitimes, perturbant ainsi le travail des utilisateurs et provoquant leur frustration.

De nombreux échecs peuvent être atténués par une simple logique de nouvelle tentative. Les modèles d'IA sont probabilistes ; ainsi, si vous relancez une requête, vous obtiendrez probablement une réponse différente. Par exemple, si la réponse est vide, réessayez X fois, ou jusqu'à obtenir une réponse non vide. De même, si la réponse est mal formatée, réessayez jusqu'à ce qu'elle soit correctement formatée.

Cette politique de nouvelle tentative peut toutefois engendrer une latence et un coût supplémentaires. Chaque nouvelle tentative implique une nouvelle série d'appels API. Si la nouvelle tentative a lieu après un échec, la latence perçue par l'utilisateur double. Pour réduire la latence, vous pouvez effectuer des appels en parallèle. Par exemple, pour chaque requête, au lieu d'attendre l'échec de la première avant de réessayer, vous envoyez cette requête deux fois simultanément au modèle, vous obtenez deux réponses et vous sélectionnez la meilleure. Cela augmente le nombre d'appels API redondants tout en maintenant une latence acceptable.

Il est également courant de faire appel à des humains pour les demandes complexes. Par exemple, les requêtes contenant certaines expressions spécifiques peuvent être transférées à des opérateurs humains. Certaines équipes utilisent un modèle spécialisé pour déterminer quand transférer une conversation à un humain. Une équipe, par exemple, transfère une conversation à des opérateurs humains lorsque son modèle d'analyse des sentiments détecte de la colère dans les messages des utilisateurs. Une autre équipe transfère une conversation après un certain nombre d'échanges afin d'éviter que les utilisateurs ne se retrouvent bloqués dans une boucle.

### Mise en œuvre des garde-fous

Les garde-fous impliquent des compromis. L'un d'eux est le _compromis entre fiabilité et latence . Tout en reconnaissant l'importance des garde-fous, certaines équipes m'ont indiqué que la latence était plus importante. Ces équipes ont décidé de ne pas implémenter de garde-fous car ceux_ [-](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1769) ci peuvent augmenter considérablement la latence de l'application.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1769)

Les garde-fous de sortie peuvent ne pas fonctionner correctement en mode de complétion de flux. Par défaut, la réponse complète est générée avant d'être affichée à l'utilisateur, ce qui peut prendre beaucoup de temps. En mode de complétion de flux, les nouveaux jetons sont transmis à l'utilisateur au fur et à mesure de leur génération, réduisant ainsi son temps d'attente. L'inconvénient est qu'il est difficile d'évaluer les réponses partielles ; des réponses non sécurisées peuvent donc être transmises aux utilisateurs avant que les garde-fous du système ne puissent déterminer qu'elles doivent être bloquées.

Le nombre de garde-fous à implémenter dépend également de l'utilisation de vos modèles : auto-hébergés ou via des API tierces. Bien qu'il soit possible d'en ajouter dans les deux cas, les API tierces permettent de réduire leur nombre, car les fournisseurs d'API en proposent généralement de nombreux prêts à l'emploi. Par ailleurs, l'auto-hébergement vous dispense d'envoyer des requêtes externes, ce qui réduit le besoin de nombreux types de garde-fous d'entrée.

Étant donné la multitude de points de défaillance potentiels d'une application, des garde-fous peuvent être mis en œuvre à différents niveaux. Les fournisseurs de modèles intègrent ces garde-fous à leurs modèles afin de les rendre plus performants et plus sûrs. Toutefois, ils doivent trouver un équilibre entre sécurité et flexibilité. Des restrictions peuvent certes renforcer la sécurité d'un modèle, mais aussi le rendre moins utilisable dans certains cas d'usage.

Les garde-fous peuvent également être mis en œuvre par les développeurs d'applications. De nombreuses techniques sont présentées dans la section [« Défenses contre les attaques par prompt »](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_defense_against_prompt_attacks_1730156991196455) . Parmi les solutions de garde-fous prêtes à l'emploi, citons [Purple Llama de Meta](https://github.com/meta-llama/PurpleLlama) , [NeMo Guardrails de NVIDIA](https://github.com/NVIDIA/NeMo-Guardrails) , [PyRIT d'Azure](https://github.com/Azure/PyRIT) , [les filtres de contenu IA d'Azure](https://oreil.ly/CxwLn) , l' [API Perspective](https://oreil.ly/d2_sL) et [l'API de modération de contenu d'OpenAI](https://oreil.ly/-kOHE) . Compte tenu du chevauchement des risques entre les entrées et les sorties, une solution de garde-fous offrira probablement une protection à la fois pour les entrées et les sorties. Certaines passerelles de modèles proposent également des fonctionnalités de garde-fous, comme expliqué dans la section suivante.

Avec les garde-fous, l'architecture ressemble à [la figure 10-4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_4_1730130985262606) . J'ai placé les scoreurs sous les API du modèle, car ils sont souvent basés sur l'IA, même s'ils sont généralement plus petits et plus rapides que les modèles génératifs. Cependant, les scoreurs peuvent également être placés dans la zone des garde-fous de sortie.

![Diagramme d'un diagramme. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1004.png)

###### Figure 10-4. Architecture de l'application avec l'ajout de garde-fous d'entrée et de sortie.

## Étape 3. Ajouter le routeur et la passerelle modèles

À mesure que les applications s'étendent et intègrent davantage de modèles, des routeurs et des passerelles apparaissent pour vous aider à gérer la complexité et les coûts liés à la prise en charge de plusieurs modèles.

### Routeur

Au lieu d'utiliser un seul modèle pour toutes les requêtes, vous pouvez opter pour des solutions différentes selon le type de requête. Cette approche présente plusieurs avantages. Premièrement, elle permet d'utiliser des modèles spécialisés, potentiellement plus performants qu'un modèle généraliste pour des requêtes spécifiques. Par exemple, vous pouvez avoir un modèle spécialisé dans le dépannage technique et un autre dans la facturation. Deuxièmement, cela permet de réaliser des économies. Au lieu d'utiliser un modèle coûteux pour toutes les requêtes, vous pouvez acheminer les requêtes les plus simples vers des modèles moins onéreux.

Un routeur se compose généralement d' _un classificateur d'intention_ qui prédit l'action que l'utilisateur souhaite entreprendre. En fonction de cette intention prédite, la requête est acheminée vers la solution appropriée. Prenons l'exemple de différentes intentions pertinentes pour un chatbot de support client :

- Si l'utilisateur souhaite réinitialiser son mot de passe, redirigez-le vers la FAQ concernant la récupération du mot de passe.
    
- Si la demande vise à corriger une erreur de facturation, veuillez la transmettre à un opérateur humain.
    
- Si la demande concerne le dépannage d'un problème technique, redirigez-la vers un chatbot spécialisé dans le dépannage.
    

Un classificateur d'intention peut empêcher votre système d'entamer des conversations hors sujet. Si la requête est jugée inappropriée, le chatbot peut poliment refuser de répondre en utilisant une réponse prédéfinie, sans consommer inutilement d'appel API. Par exemple, si l'utilisateur demande pour qui il voterait aux prochaines élections, le chatbot peut répondre : « En tant que chatbot, je ne peux pas voter. Si vous avez des questions sur nos produits, je serai ravi de vous aider. »

Un classificateur d'intention peut aider le système à détecter les requêtes ambiguës et à demander des précisions. Par exemple, en réponse à la requête « Gel », le système pourrait demander : « Souhaitez-vous geler votre compte ou parlez-vous de la météo ? » ou simplement : « Excusez-moi. Pouvez-vous préciser ? »

D'autres routeurs peuvent aider le modèle à décider de la prochaine action à entreprendre. Par exemple, pour un agent capable d'effectuer plusieurs actions, un routeur peut prendre la forme d'un _prédicteur d'action suivante_ : le modèle doit-il utiliser un interpréteur de code ou une API de recherche ? Pour un modèle doté d'un système de mémoire, un routeur peut prédire quelle partie de la hiérarchie de mémoire le modèle doit consulter. Imaginons qu'un utilisateur ajoute à la conversation un document mentionnant Melbourne. Plus tard, il demande : « Quel est l'animal le plus mignon de Melbourne ? » Le modèle doit alors décider s'il doit se fier à l'information contenue dans le document joint ou effectuer une recherche sur Internet.

Les classificateurs d'intention et les prédicteurs d'actions suivantes peuvent être implémentés sur des modèles de base. De nombreuses équipes adaptent des modèles de langage plus petits, tels que GPT-2, BERT et Llama 7B, comme classificateurs d'intention. D'autres choisissent d'entraîner des classificateurs encore plus petits à partir de zéro. Les routeurs doivent être rapides et peu coûteux afin de pouvoir en utiliser plusieurs sans engendrer de latence ni de surcoût significatifs.

Lors du routage de requêtes vers des modèles aux limites de contexte variables, il peut être nécessaire d'ajuster le contexte de la requête en conséquence. Prenons l'exemple d'une requête de 1 000 jetons destinée à un modèle dont la limite de contexte est de 4 000 jetons. Si le système effectue ensuite une action, par exemple une recherche web, qui renvoie un contexte de 8 000 jetons, vous pouvez soit tronquer le contexte de la requête pour qu'il corresponde au modèle initialement prévu, soit la router vers un modèle dont la limite de contexte est plus élevée.

Le routage étant généralement effectué par les modèles, je l'ai placé dans l'encadré « API Modèle » de la [figure 10-5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_5_1730130985262626) . À l'instar des scoreurs, les routeurs sont généralement plus petits que les modèles utilisés pour la génération.

Le regroupement des routeurs avec d'autres modèles facilite leur gestion. Il est toutefois important de noter que le routage intervient souvent _avant_ la récupération des données. Par exemple, avant la récupération, un routeur peut déterminer si une requête est pertinente et, le cas échéant, si elle nécessite une récupération. Le routage peut également intervenir après la récupération, par exemple pour déterminer si une requête doit être transmise à un opérateur humain. Cependant, le schéma routage – récupération – génération – évaluation est beaucoup plus fréquent dans les applications d'IA.

![Schéma d'un système. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1005.png)

###### Figure 10-5. Le routage aide le système à utiliser la solution optimale pour chaque requête.

### Gateway

Une passerelle de modèles est une couche intermédiaire permettant à votre organisation d'interagir avec différents modèles de manière unifiée et sécurisée. Sa fonction principale est de fournir une interface unifiée à ces différents modèles, qu'ils soient hébergés sur votre serveur ou accessibles via des API commerciales. Une passerelle de modèles simplifie la maintenance de votre code. En cas de modification de l'API d'un modèle, il vous suffit de mettre à jour la passerelle, sans avoir à modifier toutes les applications qui dépendent de cette API. [La figure 10-6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_6_1730130985262644) présente une représentation schématique d'une passerelle de modèles.

![Schéma d'une passerelle modèle. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1006.png)

###### Figure 10-6. Une passerelle de modèle fournit une interface unifiée pour travailler avec différents modèles.

Dans sa forme la plus simple, une passerelle de modèle est un wrapper unifié. L'exemple de code suivant illustre comment une passerelle de modèle peut être implémentée. Il n'est pas fonctionnel, car il ne contient aucune vérification d'erreurs ni optimisation :

```python
import google.generativeai as genai
import openai

  

def openai_model(input_data, model_name, max_tokens):

	openai.api_key = os.environ["OPENAI_API_KEY"]
	response = openai.Completion.create(
	engine=model_name,
	prompt=input_data,
	max_tokens=max_tokens

)
return {"response": response.choices[0].text.strip()}

def gemini_model(input_data, model_name, max_tokens):

	genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
	model = genai.GenerativeModel(model_name=model_name)
	response = model.generate_content(input_data, max_tokens=max_tokens)
	return {"response": response["choices"][0]["message"]["content"]}

  

@app.route('/model', methods=['POST'])
def model_gateway():
	data = request.get_json()
	model_type = data.get("model_type")
	model_name = data.get("model_name")
	input_data = data.get("input_data")
	max_tokens = data.get("max_tokens")

  

if model_type == "openai":
	result = openai_model(input_data, model_name, max_tokens)
elif model_type == "gemini":
	result = gemini_model(input_data, model_name, max_tokens)
return jsonify(result)
```

Une passerelle de modèles assure _le contrôle d'accès et la gestion des coûts_ . Au lieu de distribuer vos jetons d'identification à tous les utilisateurs souhaitant accéder à l'API OpenAI, ce qui peut entraîner des fuites, vous leur donnez accès uniquement à la passerelle de modèles, créant ainsi un point d'accès centralisé et contrôlé. La passerelle permet également de mettre en œuvre des contrôles d'accès précis, en spécifiant quel utilisateur ou application doit accéder à quel modèle. De plus, elle peut surveiller et limiter l'utilisation des appels API, prévenant ainsi les abus et optimisant les coûts.

Une passerelle de modèles peut également servir à implémenter des politiques de repli pour pallier les limitations de débit ou les pannes d'API (ces dernières étant malheureusement fréquentes). Lorsque l'API principale est indisponible, la passerelle peut rediriger les requêtes vers des modèles alternatifs, réessayer après un court délai ou gérer les pannes de manière appropriée. Ainsi, votre application fonctionne sans interruption.

Puisque les requêtes et les réponses transitent déjà par la passerelle, celle-ci constitue un emplacement idéal pour implémenter d'autres fonctionnalités, telles que l'équilibrage de charge, la journalisation et l'analyse. Certaines passerelles proposent même la mise en cache et des mécanismes de protection.

Étant donné que les passerelles sont relativement simples à mettre en œuvre, il existe de nombreuses passerelles prêtes à l'emploi. Citons par exemple [la passerelle IA de Portkey](https://github.com/Portkey-AI/gateway) , [la passerelle IA de MLflow](https://oreil.ly/D2X_Y) , [la passerelle LLM de Wealthsimple](https://github.com/wealthsimple/llm-gateway) , [TrueFoundry](https://oreil.ly/ICRRA) , [Kong](https://oreil.ly/St4W6) et [Cloudflare](https://oreil.ly/0NuNb) .

Dans notre architecture, la passerelle remplace désormais le boîtier API du modèle, comme illustré dans [la figure 10-7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_7_1730130985262661) .

![Diagramme de flux de données. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1007.png)

###### Figure 10-7. L'architecture avec les modules de routage et de passerelle ajoutés.

###### Note

Une couche d'abstraction similaire, telle qu'une passerelle d'outils, peut également s'avérer utile pour accéder à un large éventail d'outils. Elle n'est pas abordée dans cet ouvrage car, à l'heure actuelle, ce modèle n'est pas courant..

## Étape 4. Réduire la latence grâce aux caches

La mise en cache est depuis longtemps un élément essentiel des applications logicielles pour réduire la latence et les coûts. De nombreux principes de mise en cache logicielle peuvent être appliqués aux applications d'IA. Les techniques de mise en cache d'inférence, notamment la mise en cache clé-valeur et la mise en cache d'invite, sont abordées au [chapitre 9.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301) Cette section est consacrée à la mise en cache système. La mise en cache étant une technologie ancienne et largement documentée, cet ouvrage n'en donnera qu'un aperçu général. On distingue généralement deux mécanismes principaux de mise en cache système : la mise en cache exacte et la mise en cache sémantique.

### Mise en cache exacte

Grâce à la mise en cache exacte, les éléments mis en cache ne sont utilisés que lorsque ces éléments précis sont demandés. Par exemple, si un utilisateur demande à un modèle de résumer un produit, le système vérifie dans le cache si un résumé de ce produit existe. Si c'est le cas, il le récupère. Sinon, il résume le produit et met le résumé en cache.

La mise en cache exacte est également utilisée pour la recherche par plongement afin d'éviter les recherches vectorielles redondantes. Si une requête entrante est déjà présente dans le cache de recherche vectorielle, le résultat mis en cache est récupéré. Sinon, une recherche vectorielle est effectuée pour cette requête et le résultat est mis en cache.

La mise en cache est particulièrement intéressante pour les requêtes qui impliquent plusieurs étapes (par exemple, une chaîne de pensée) et/ou des actions chronophages (par exemple, la récupération, l'exécution SQL ou la recherche Web).

Un cache exact peut être implémenté en mémoire vive pour une récupération rapide. Cependant, la mémoire vive étant limitée, un cache peut également être implémenté à l'aide de bases de données comme PostgreSQL, Redis ou d'un stockage hiérarchisé afin d'optimiser le compromis entre vitesse et capacité de stockage.La politique d'éviction est essentielle pour gérer la taille du cache et maintenir les performances. Les politiques d'éviction courantes incluent LRU (Least Recently Used), LFU (Least Frequently Used) et FIFO (First In, First Out).

La durée de conservation d'une requête en cache dépend de sa probabilité d'être réutilisée. Les requêtes spécifiques à un utilisateur, telles que « Quel est le statut de ma dernière commande ? », sont moins susceptibles d'être réutilisées et ne devraient donc pas être mises en cache. De même, il est moins pertinent de mettre en cache les requêtes urgentes comme « Quel temps fait-il ? ». De nombreuses équipes entraînent un classificateur pour prédire si une requête doit être mise en cache.

---
###### Avertissement

La mise en cache, mal gérée, peut entraîner des fuites de données. Imaginez que vous travaillez pour un site de commerce électronique et que l'utilisateur X pose une question apparemment banale : « Quelle est la politique de retour pour les produits électroniques ? » Comme votre politique de retour dépend du statut de l'utilisateur, le système récupère d'abord les informations de l'utilisateur X, puis génère une réponse contenant ces informations. Prenant cette requête pour une question générique, le système met la réponse en cache. Plus tard, lorsque l'utilisateur Y pose la même question, le résultat mis en cache est renvoyé, révélant ainsi les informations de X à Y.

---
### Mise en cache sémantique

Contrairement à la mise en cache exacte, les éléments mis en cache sont utilisés même s'ils ne sont que sémantiquement similaires, et non identiques, à la requête entrante. Imaginons qu'un utilisateur demande : « Quelle est la capitale du Vietnam ? » et que le modèle réponde : « Hanoï ». Plus tard, un autre utilisateur demande : « Quelle est la capitale _du_ Vietnam ? », ce qui est sémantiquement la même question, formulée légèrement différemment. Grâce à la mise en cache sémantique, le système peut réutiliser la réponse de la première requête au lieu de calculer la nouvelle requête à partir de zéro. La réutilisation des requêtes similaires augmente le taux d'accès au cache et peut potentiellement réduire les coûts. Cependant, la mise en cache sémantique peut dégrader les performances de votre modèle.

La mise en cache sémantique ne fonctionne que si vous disposez d'un moyen fiable de déterminer si deux requêtes sont similaires. Une approche courante consiste à utiliser la similarité sémantique, comme expliqué au [chapitre 3.](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) Pour rappel, la similarité sémantique fonctionne comme suit :

1. Pour chaque requête, générez son embedding à l'aide d'un modèle d'embedding.
    
2. Utilisez la recherche vectorielle pour trouver l'embedding mis en cache présentant le score de similarité le plus élevé avec l'embedding de la requête actuelle. Supposons que ce score de similarité soit _X._
    
3. Si _X_ dépasse un certain seuil de similarité, la requête mise en cache est considérée comme similaire et les résultats mis en cache sont renvoyés. Sinon, traitez la requête courante et mettez-la en cache avec son embedding et ses résultats.
    

Cette approche nécessite une base de données vectorielle pour stocker les représentations vectorielles des requêtes mises en cache.

_Comparée à d'autres techniques de mise en cache, la mise en cache sémantique présente un intérêt plus discutable, car nombre de ses composants sont sujets à des défaillances._ Son succès repose sur des représentations vectorielles de haute qualité, une recherche vectorielle fonctionnelle et une métrique de similarité fiable. Définir le seuil de similarité approprié peut également s'avérer complexe et nécessiter de nombreux essais. Si le système confond la requête entrante avec une requête similaire à une autre, la réponse renvoyée par le cache sera incorrecte.

De plus, la mise en cache sémantique peut s'avérer longue et gourmande en ressources de calcul, car elle implique une recherche vectorielle. La vitesse et le coût de cette recherche dépendent de la taille des représentations vectorielles mises en cache.

Le cache sémantique peut s'avérer pertinent si son taux d'accès est élevé, c'est-à-dire si une bonne partie des requêtes peuvent être traitées efficacement grâce aux résultats mis en cache. Toutefois, avant d'intégrer les complexités d'un cache sémantique, il est essentiel d'évaluer les risques associés en termes d'efficacité, de coût et de performances.

Avec l'ajout des systèmes de cache, la plateforme ressemble à [la figure 10-8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_8_1730130985262677) . Les caches KV et les caches d'invites sont généralement implémentés par les fournisseurs d'API de modèle ; ils ne sont donc pas représentés ici. Pour les visualiser, je les placerais dans l'encadré « API de modèle ». Une nouvelle flèche permet d'ajouter les réponses générées au cache.

![](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1008.png)

###### Figure 10-8. Une architecture d'application d'IA avec les caches ajoutés.

## Étape 5. Ajouter des modèles d'agents

Les applications présentées jusqu'ici restent relativement simples. Chaque requête suit un flux séquentiel. Cependant, comme expliqué au [chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) , le flux d'une application peut se complexifier grâce à des boucles, une exécution parallèle et des branchements conditionnels. Les modèles d'agents, également abordés au [chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) , permettent de concevoir des applications complexes. Par exemple, après avoir généré une sortie, le système peut constater que la tâche n'est pas accomplie et qu'une nouvelle requête est nécessaire pour recueillir des informations complémentaires. La réponse initiale, associée au contexte nouvellement obtenu, est alors transmise au même modèle ou à un autre. Ceci crée une boucle, comme illustré dans [la figure 10-9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_9_1730130985262696) .

![Schéma d'un système informatique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1009.png)

###### Figure 10-9. La flèche jaune permet de réinjecter la réponse générée dans le système, permettant des modèles d'application plus complexes.

Les résultats d'un modèle peuvent également servir à déclencher des actions d'écriture, comme la rédaction d'un courriel, la passation d'une commande ou l'initialisation d'un virement bancaire. Ces actions permettent à un système de modifier directement son environnement. Comme expliqué au [chapitre 6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) , elles peuvent considérablement accroître les capacités d'un système, mais aussi l'exposer à des risques bien plus importants. Il convient donc d'accorder à un modèle l'accès aux actions d'écriture avec la plus grande prudence. Avec l'ajout de ces actions, l'architecture est illustrée par [la figure 10-10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_10_1730130985262713) .

Si vous avez suivi toutes les étapes jusqu'ici, votre architecture est probablement devenue assez complexe. Bien que les systèmes complexes puissent résoudre davantage de tâches, ils introduisent également plus de modes de défaillance, ce qui les rend plus difficiles à déboguer en raison des nombreux points de défaillance potentiels. La section suivante abordera les bonnes pratiques pour améliorer l'observabilité du système.

![Schéma d'un système. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1010.png)

###### Figure 10-10. Une architecture d'application qui permet au système d'effectuer des actions d'écriture.

## Surveillance et observabilité

Bien que j'aie consacré une section entière à l'observabilité, celle-ci doit être intégrée à la conception d'un produit et non pas considérée comme une simple réflexion a posteriori. Plus un produit est complexe, plus l'observabilité est cruciale.

L'observabilité est une pratique universelle dans toutes les disciplines du génie logiciel. C'est un secteur important, doté de bonnes pratiques établies et de nombreuses solutions propriétaires et open source prêtes à l'emploi. [4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1786) Afin d'éviter de réinventer la roue, je me concentrerai sur les spécificités des applications construites sur des modèles de base. Le [dépôt GitHub](https://github.com/chiphuyen/aie-book) du livre contient des ressources pour ceux qui souhaitent approfondir leurs connaissances en matière d'observabilité. [5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1787)

L'objectif de la surveillance est le même que celui de l'évaluation : atténuer les risques et identifier les opportunités. Parmi les risques que la surveillance contribue à atténuer figurent les défaillances d'applications, les attaques de sécurité et les dérives. La surveillance permet également d'identifier des pistes d'amélioration des applications et de réduction des coûts. Enfin, elle contribue à responsabiliser le système en offrant une visibilité sur ses performances.

Trois indicateurs issus de la communauté DevOps permettent d'évaluer la qualité de l'observabilité de votre système :

- MTTD (temps moyen de détection) : lorsqu’un problème survient, combien de temps faut-il pour le détecter ?
    
- MTTR (temps moyen de réponse) : après la détection, combien de temps faut-il pour résoudre le problème ?
    
- Taux d'échec des modifications (CFR) : pourcentage de modifications ou de déploiements entraînant des échecs nécessitant des corrections ou des restaurations. Si vous ne connaissez pas votre CFR, il est temps de repenser votre plateforme pour une meilleure visibilité.
    

Un taux de défaillance élevé n'indique pas nécessairement un système de surveillance défaillant. Toutefois, il est conseillé de repenser votre processus d'évaluation afin de détecter les modifications problématiques avant leur déploiement. L'évaluation et la surveillance doivent être étroitement liées. Les indicateurs d'évaluation doivent être facilement transposables aux indicateurs de surveillance ; autrement dit, un modèle performant lors de l'évaluation devrait également l'être lors de la surveillance. Les problèmes détectés lors de la surveillance doivent être intégrés au processus d'évaluation.

# Surveillance versus observabilité

Depuis le milieu des années 2010, le secteur privilégie le terme « observabilité » à celui de « surveillance ». La surveillance ne présuppose aucune relation entre l'état interne d'un système et ses sorties. On surveille les sorties externes du système pour détecter un dysfonctionnement interne ; or, rien ne garantit que ces sorties externes permettront d'identifier la cause du problème.

L'observabilité, en revanche, repose sur une hypothèse plus forte que la surveillance traditionnelle : les états internes d'un système peuvent être déduits de la connaissance de ses sorties externes. Lorsqu'un problème survient dans un système observable, il devrait être possible d'en déterminer la cause en consultant les journaux et les métriques du système, sans avoir à déployer de nouveau code. L'observabilité consiste à instrumenter le système de manière à garantir la collecte et l'analyse d'informations suffisantes sur son fonctionnement, afin de faciliter l'identification de la cause d'un problème.

Dans ce livre, j'utiliserai le terme « surveillance » pour désigner l'action de suivre les informations d'un système et le terme « observabilité » pour désigner l'ensemble du processus d'instrumentation, de suivi et de débogage du système.

### Métrique

Lorsqu'on parle de supervision, on pense souvent aux indicateurs. Pourtant, les indicateurs ne constituent pas l'objectif en soi. En réalité, la plupart des entreprises se soucient peu du score de pertinence des résultats de votre application, sauf si celui-ci a une utilité. Le but d'un indicateur est de signaler les problèmes et d'identifier les pistes d'amélioration.

Avant de lister les indicateurs à suivre, il est important de comprendre les modes de défaillance que vous souhaitez détecter et de concevoir vos indicateurs en fonction de ces défaillances.Par exemple, pour éviter que votre application ne se comporte de manière erratique, définissez des indicateurs permettant de détecter ces anomalies. Un indicateur pertinent pourrait être la possibilité de déduire le résultat de l'application du contexte. Si vous souhaitez éviter que votre application n'épuise votre crédit API, suivez les indicateurs liés aux coûts de l'API, tels que le nombre de jetons d'entrée et de sortie par requête, ou encore le coût et le taux d'accès à votre cache.

Les modèles de base pouvant générer des résultats variés, les risques d'erreur sont nombreux. La conception des indicateurs exige un esprit analytique, des connaissances statistiques et, souvent, de la créativité. Le choix des indicateurs à suivre dépend fortement de l'application.

Ce livre a abordé de nombreux types de métriques de qualité des modèles (chapitres [4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) à [6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch06.html#ch06_rag_and_agents_1730157386571386) , et plus loin dans ce chapitre) ainsi que différentes méthodes pour les calculer (chapitres [3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch03.html#ch03a_evaluation_methodology_1730150757064067) et [5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch05.html#ch05a_prompt_engineering_1730156991195551) ). Je vais ici en faire un bref récapitulatif.

Les erreurs de format sont les plus faciles à repérer car elles sont simples à détecter et à vérifier. Par exemple, si vous attendez des résultats JSON, suivez la fréquence à laquelle le modèle génère des JSON invalides et, parmi ces résultats, déterminez combien peuvent être facilement corrigés (l'absence d'une parenthèse fermante est facile à corriger, mais l'absence de clés attendues est plus complexe).

Pour les générations ouvertes, il est conseillé de surveiller la cohérence des faits et des indicateurs de qualité pertinents tels que la concision, la créativité ou la positivité. Nombre de ces indicateurs peuvent être calculés par des systèmes d'évaluation par intelligence artificielle.

Si la sécurité est un enjeu majeur, vous pouvez suivre les indicateurs de toxicité et détecter les informations privées et sensibles dans les entrées et les sorties. Surveillez la fréquence de déclenchement de vos garde-fous et la fréquence à laquelle votre système refuse de répondre. Détectez également les requêtes anormales adressées à votre système, car elles peuvent révéler des cas limites intéressants ou inciter à des attaques.

La qualité du modèle peut également être déduite des retours en langage naturel des utilisateurs et des signaux conversationnels. Par exemple, voici quelques indicateurs simples à suivre :

- À quelle fréquence les utilisateurs interrompent-ils le développement d'une génération à mi-chemin ?
    
- Quel est le nombre moyen de tours de parole par conversation ?
    
- Quel est le nombre moyen de jetons par saisie ? Les utilisateurs utilisent-ils votre application pour des tâches plus complexes, ou apprennent-ils à être plus concis dans leurs requêtes ?
    
- Quel est le nombre moyen de jetons par résultat ? Certains modèles sont-ils plus verbeux que d’autres ? Certains types de requêtes sont-ils plus susceptibles de générer des réponses longues ?
    
- Quelle est la distribution des jetons de sortie du modèle ? Comment a-t-elle évolué au fil du temps ? Le modèle devient-il plus ou moins diversifié ?
    

Les indicateurs liés à la longueur sont également importants pour le suivi de la latence et des coûts, car des contextes et des réponses plus longs augmentent généralement la latence et entraînent des coûts plus élevés.

Chaque composant d'un pipeline d'application possède ses propres métriques. Par exemple, dans une application RAG (Real Aggregate, Aggregation, Data), la qualité de la récupération est souvent évaluée à l'aide de la pertinence et de la précision du contexte. Une base de données vectorielle peut être évaluée en fonction de l'espace de stockage nécessaire à l'indexation des données et du temps d'exécution des requêtes.

Étant donné que vous disposerez probablement de plusieurs indicateurs, il est utile d'analyser leur corrélation entre eux et, surtout, avec vos indicateurs clés de performance (KPI) principaux, tels que le nombre d'utilisateurs actifs quotidiens (DAU), la durée des sessions (le temps passé par un utilisateur à interagir activement avec l'application) ou les abonnements. Les indicateurs fortement corrélés à vos KPI principaux peuvent vous donner des pistes d'amélioration. À l'inverse, les indicateurs non corrélés peuvent vous indiquer les aspects à éviter lors des optimisations.

Le suivi de la latence est essentiel pour comprendre l'expérience utilisateur. Les indicateurs de latence courants, abordés au [chapitre 9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch09.html#ch09_inference_optimization_1730130963006301) , incluent :

- Délai d'obtention du premier jeton (TTFT) : le temps nécessaire pour que le premier jeton soit généré.
    
- Temps par jeton de sortie (TPOT) : le temps nécessaire pour générer chaque jeton de sortie.
    
- Latence totale : le temps total nécessaire pour obtenir une réponse.
    

Suivez tous ces indicateurs pour chaque utilisateur afin de voir comment votre système évolue avec un nombre croissant d'utilisateurs.

Il est également important de suivre les coûts. Les indicateurs de coûts comprennent le nombre de requêtes et le volume de jetons d'entrée et de sortie, par exemple les jetons par seconde (TPS). Si vous utilisez une API avec des limites de débit, le suivi du nombre de requêtes par seconde est essentiel pour respecter vos limites et éviter d'éventuelles interruptions de service.

Pour le calcul des indicateurs, vous pouvez opter pour des contrôles ponctuels ou exhaustifs. Les contrôles ponctuels consistent à analyser un sous-ensemble de données afin d'identifier rapidement les problèmes, tandis que les contrôles exhaustifs évaluent chaque requête pour une vue d'ensemble complète des performances. Le choix dépend des exigences de votre système et des ressources disponibles ; une combinaison des deux permet d'obtenir une stratégie de surveillance équilibrée.

Lors du calcul des indicateurs, assurez-vous qu'ils puissent être ventilés selon des axes pertinents, tels que les utilisateurs, les versions, les versions d'invites/chaînes, les types d'invites/chaînes et le temps. Cette granularité facilite la compréhension des variations de performance et l'identification des problèmes spécifiques.

### Journaux et traces

Les indicateurs sont généralement agrégés. Ils condensent les informations issues des événements qui se produisent dans votre système au fil du temps. Ils vous permettent de comprendre, en un coup d'œil, le fonctionnement de votre système. Cependant, de nombreuses questions restent sans réponse. Par exemple, face à un pic d'activité, vous pourriez vous demander : « Ce phénomène s'est-il déjà produit ? » Les journaux d'activité peuvent vous aider à répondre à cette question.

Si les métriques sont des mesures numériques représentant des attributs et des événements, les journaux sont un enregistrement des événements en mode ajout uniquement. En production, un processus de débogage pourrait ressembler à ceci :

1. Les indicateurs vous signalent qu'un problème est survenu il y a cinq minutes, mais ils ne vous disent pas ce qui s'est passé.
    
2. Vous consultez les journaux d'événements qui se sont déroulés il y a environ cinq minutes pour comprendre ce qui s'est passé.
    
3. Mettez en corrélation les erreurs des journaux avec les indicateurs pour vous assurer d'avoir identifié le bon problème.
    

Pour une détection rapide, les indicateurs doivent être calculés rapidement. Pour une réponse rapide, les journaux doivent être immédiatement disponibles et accessibles. Si vos journaux accusent un retard de 15 minutes, vous devrez attendre leur arrivée pour résoudre un problème survenu il y a 5 minutes.

Comme vous ne savez pas précisément quels journaux vous devrez consulter ultérieurement, la règle générale est de tout consigner. Enregistrez toutes les configurations, y compris le point de terminaison de l'API du modèle, le nom du modèle, les paramètres d'échantillonnage (température, top-p, top-k, condition d'arrêt, etc.) et le modèle d'invite.

Consignez la requête utilisateur, l'invite finale envoyée au modèle, la sortie et les sorties intermédiaires. Consignez également tout appel d'outil, ainsi que les sorties de cet outil. Enregistrez le démarrage et l'arrêt d'un composant, les plantages, etc. Lors de l'enregistrement d'un journal, veillez à lui attribuer des étiquettes et des identifiants permettant de localiser sa provenance dans le système.

L'enregistrement de toutes les activités peut entraîner une augmentation très rapide du volume de journaux. De nombreux outils d'analyse automatisée et de détection d'anomalies dans les journaux sont basés sur l'intelligence artificielle.

Bien qu'il soit impossible de traiter les journaux manuellement, il est utile d'examiner quotidiennement vos données de production afin de comprendre comment les utilisateurs interagissent avec votre application. [Shankar et al. (2024)](https://arxiv.org/abs/2404.12272) ont constaté que la perception des développeurs quant aux résultats satisfaisants et insatisfaisants évolue au fur et à mesure qu'ils manipulent davantage de données. Cela leur permet à la fois de reformuler leurs invites pour augmenter les chances d'obtenir de bonnes réponses et de mettre à jour leur processus d'évaluation afin de détecter les réponses insatisfaisantes.

Si les journaux d'événements sont une succession d'événements disparates, les traces sont reconstituées en reliant les événements connexes afin de former une chronologie complète d'une transaction ou d'un processus, montrant comment chaque étape s'enchaîne du début à la fin. En bref, une trace est l'enregistrement détaillé du parcours d'exécution d'une requête à travers les différents composants et services du système. Dans une application d'IA, le traçage révèle l'intégralité du processus, depuis l'envoi d'une requête par l'utilisateur jusqu'au retour de la réponse finale, incluant les actions effectuées par le système, les documents récupérés et l'invite finale envoyée au modèle. Il doit également indiquer la durée de chaque étape et son coût associé, si celui-ci est mesurable. [La figure 10-11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_11_1730130985262728) illustre la visualisation de la trace d'une requête dans [LangSmith](https://oreil.ly/Oml_x) .

Idéalement, vous devriez pouvoir suivre la transformation de chaque requête étape par étape au sein du système. En cas d'échec d'une requête, vous devriez pouvoir identifier précisément l'étape où le problème s'est produit : traitement incorrect, contexte récupéré non pertinent ou réponse erronée du modèle.

![Capture d'écran d'une conversation. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1011.png)

###### Figure 10-11. Une trace de requête visualisée par LangSmith.

### Détection de dérive

Plus un système comporte de composants, plus les éléments susceptibles de changer sont nombreux. Dans une application d'IA, il peut s'agir de :

modifications de l'invite système

Il existe de nombreuses raisons pour lesquelles l'invite système de votre application peut changer à votre insu. Elle a peut-être été conçue à partir d'un modèle, et ce modèle a ensuite été mis à jour. Un collègue a peut-être corrigé une faute de frappe. Un mécanisme simple devrait suffire à détecter ces changements.

changements de comportement des utilisateurs

Avec le temps, les utilisateurs adaptent leurs comportements à la technologie. Par exemple, certains ont déjà appris à formuler leurs requêtes pour obtenir de meilleurs résultats sur Google ou à améliorer le classement de leurs articles dans les résultats de recherche. Les habitants des zones où circulent des voitures autonomes ont déjà trouvé des astuces pour obtenir la priorité ( [Liu et al., 2020](https://oreil.ly/AWwkx) ). Il est probable que vos utilisateurs modifient leurs comportements pour optimiser l'utilisation de votre application. Par exemple, ils pourraient apprendre à rédiger des instructions plus concises, ce qui pourrait entraîner une diminution progressive de la longueur des réponses. Si vous vous contentez d'analyser les indicateurs, la cause de cette diminution progressive risque de ne pas être évidente. Une investigation est nécessaire pour en comprendre l'origine.

Modifications du modèle sous-jacent

Lorsqu'on utilise un modèle via une API, il est possible que l'API reste inchangée tandis que le modèle sous-jacent est mis à jour. Comme indiqué au [chapitre 4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch04.html#ch04_evaluate_ai_systems_1730130866187863) , les fournisseurs de modèles ne divulguent pas toujours ces mises à jour, vous laissant ainsi le soin de détecter tout changement. Différentes versions d'une même API peuvent avoir un impact significatif sur les performances. Par exemple, [Chen et al. (2023)](https://arxiv.org/abs/2307.09009) ont observé des différences notables dans les scores de référence entre les versions de mars 2023 et de juin 2023 de GPT-4 et GPT-3.5. De même, Voiceflow a constaté une [baisse de performance de 10 %](https://oreil.ly/vIfkA) lors du passage de l'ancienne version GPT-3.5-turbo-0301 à la plus récente GPT-3.5-turbo-1106.

## Orchestration des pipelines d'IA

Une application d'IA peut devenir très complexe, comprenant plusieurs modèles, récupérant des données de nombreuses bases de données et ayant accès à un large éventail d'outils. Un orchestrateur vous aide à spécifier comment ces différents composants interagissent pour créer un pipeline de bout en bout. Il garantit une circulation fluide des données entre les composants. De manière générale, un orchestrateur fonctionne en deux étapes : la définition des composants et leur chaînage.

Définition des composants

Vous devez indiquer à l'orchestrateur les composants utilisés par votre système, notamment les différents modèles, les sources de données externes pour l'extraction et les outils disponibles. Une passerelle de modèles peut simplifier l'ajout d'un modèle. Vous pouvez également préciser à l' [orchestrateur](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1811) si vous utilisez des outils d'évaluation et de surveillance.

Enchaînement

Le chaînage est fondamentalement une composition de fonctions : il combine différentes fonctions (composants). Dans le chaînage (pipeline), vous indiquez à l'orchestrateur les étapes que votre système suit depuis la réception de la requête utilisateur jusqu'à l'exécution de la tâche. Voici un exemple de ces étapes :

1. Traiter la requête brute.
    
2. Récupérer les données pertinentes en fonction de la requête traitée.
    
3. Combinez la requête d'origine et les données récupérées pour créer une invite au format attendu par le modèle.
    
4. Le modèle génère une réponse en fonction de la consigne.
    
5. Évaluer la réponse.
    
6. Si la réponse est jugée satisfaisante, renvoyez-la à l'utilisateur. Dans le cas contraire, transmettez la requête à un opérateur humain.
    

L'orchestrateur est responsable du transfert des données entre les composants. Il doit fournir les outils nécessaires pour garantir que le résultat de l'étape en cours est au format attendu par l'étape suivante. Idéalement, il devrait vous avertir en cas d'interruption de ce flux de données, par exemple suite à une défaillance d'un composant ou à une incompatibilité de données.

###### Avertissement

Un orchestrateur de pipelines d'IA est différent d'un orchestrateur de flux de travail général, comme Airflow ou Metaflow.

Lors de la conception du pipeline d'une application soumise à des exigences strictes de latence, essayez d'exécuter un maximum de tâches en parallèle. Par exemple, si vous avez un composant de routage (qui détermine la destination d'une requête) et un composant de suppression des données personnelles, les deux peuvent être exécutés simultanément.

Il existe de nombreux outils d'orchestration d'IA, tels que [LangChain](https://github.com/langchain-ai/langchain) , [LlamaIndex](https://github.com/run-llama/llama_index) , [Flowise](https://github.com/FlowiseAI/Flowise) , [Langflow](https://github.com/langflow-ai/langflow) et [Haystack](https://github.com/deepset-ai/haystack) . La recherche et l'utilisation d'outils étant des modèles d'application courants, de nombreux frameworks RAG et d'agents servent également d'outils d'orchestration.

Bien qu'il soit tentant d'utiliser immédiatement un outil d'orchestration au démarrage d'un projet, _il est conseillé de commencer par développer votre application sans._ Tout outil externe complexifie inutilement le système. Un orchestrateur peut masquer des détails essentiels de son fonctionnement, rendant ainsi sa compréhension et son débogage difficiles.

À mesure que vous progressez dans le développement de votre application, vous pourriez décider qu'un orchestrateur peut vous simplifier la tâche. Voici trois aspects à prendre en compte lors de l'évaluation des orchestrateurs :

Intégration et extensibilité

Évaluez si l'orchestrateur prend en charge les composants que vous utilisez déjà ou que vous envisagez d'adopter. Par exemple, si vous souhaitez utiliser un modèle Llama, vérifiez sa compatibilité avec l'orchestrateur. Compte tenu du nombre de modèles, de bases de données et de frameworks existants, il est impossible pour un orchestrateur de tout prendre en charge. Par conséquent, vous devrez également considérer son extensibilité. S'il ne prend pas en charge un composant spécifique, est-il facile de modifier cette compatibilité ?

Prise en charge des pipelines complexes

À mesure que vos applications gagnent en complexité, vous pourriez avoir besoin de gérer des pipelines complexes comportant de multiples étapes et une logique conditionnelle. Un orchestrateur prenant en charge des fonctionnalités avancées telles que le branchement, le traitement parallèle et la gestion des erreurs vous aidera à gérer efficacement ces complexités.

Facilité d'utilisation, performance et évolutivité

Tenez compte de la convivialité de l'orchestrateur. Privilégiez les API intuitives, une documentation complète et un support communautaire actif : ces éléments peuvent considérablement faciliter la prise en main pour vous et votre équipe. Évitez les orchestrateurs qui effectuent des appels API cachés ou qui introduisent de la latence dans vos applications. Enfin, assurez-vous que l'orchestrateur puisse évoluer efficacement avec la croissance du nombre d'applications, de développeurs et du trafic..

# Commentaires des utilisateurs

Les retours des utilisateurs ont toujours joué un rôle crucial dans les applications logicielles, et ce, de deux manières principales : en évaluant les performances de l’application et en orientant son développement. Toutefois, dans les applications d’IA, ces retours revêtent une importance encore plus grande. Les retours des utilisateurs constituent des données propriétaires, et les données représentent un avantage concurrentiel. Un système de retours utilisateurs bien conçu est donc indispensable pour créer le cercle vertueux des données évoqué au [chapitre](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch08.html#ch08_dataset_engineering_1730130932019888) [8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1816) .[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1816)

Les retours des utilisateurs permettent non seulement de personnaliser les modèles pour chaque utilisateur, mais aussi d'améliorer leurs versions ultérieures. Face à la raréfaction croissante des données, les données propriétaires sont plus précieuses que jamais. Un produit lancé rapidement et qui séduit rapidement les utilisateurs peut collecter des données pour améliorer continuellement ses modèles, ce qui complique la tâche de ses concurrents.

Il est important de se rappeler que les commentaires des utilisateurs constituent des données utilisateur. Exploiter ces commentaires exige les mêmes précautions que pour toute autre donnée. Le respect de la vie privée des utilisateurs est primordial. Ils ont le droit de savoir comment leurs données sont utilisées.

## Extraction de retours conversationnels

Traditionnellement, les retours d'information peuvent être _explicites ou implicites_ . Les retours explicites sont les informations fournies par les utilisateurs en réponse à des demandes de retour d'information formulées dans l'application, comme les votes positifs/négatifs, les notes par étoiles ou une réponse par oui/non à la question « Avons-nous résolu votre problème ? ». Les retours explicites sont assez standardisés d'une application à l'autre : il n'existe qu'un nombre limité de façons de demander à une personne si elle apprécie quelque chose. Par conséquent, les retours explicites sont mieux compris.

Le feedback implicite est une information déduite des actions de l'utilisateur. Par exemple, si quelqu'un achète un produit qui lui a été recommandé, cela signifie que la recommandation était pertinente. La nature du feedback implicite dépend des actions possibles de l'utilisateur au sein de chaque application et est donc fortement dépendante de l'application. Les modèles de base ouvrent la voie à un nouvel univers d'applications et, par conséquent, à de nombreux types de feedback implicite.

L'interface conversationnelle utilisée par de nombreuses applications d'IA facilite les retours d'information des utilisateurs. Ces derniers peuvent encourager les bons comportements et corriger les erreurs, comme ils le feraient dans des conversations quotidiennes. Le langage employé pour guider l'IA peut fournir des informations sur _les performances de l'application_ et sur _les préférences de l'utilisateur_ .

Par exemple, imaginez que vous utilisiez un assistant IA pour vous aider à planifier votre voyage en Australie. Vous lui demandez de trouver un hôtel pour trois nuits à Sydney. Il vous propose alors trois hôtels :

Voici trois suggestions d'hôtels à Sydney pour un séjour de 3 nuits :
1. Hôtel boutique historique Rocks (The Rocks)
-Prix : environ 400 $ la nuit
-Quartier : Rues charmantes et proximité de sites emblématiques.
2. Stylish Surry Hills House Hotel (Surry Hills)
-Prix : environ 200 $ la nuit
-Quartier : Branché, avec des cafés animés et des galeries d'art.
3. Hôtel Chill Bondi Beachside (Plage de Bondi)
-Prix : environ 300 $ la nuit
Quartier : En bord de mer, idéal pour la détente et la découverte de la ville.

Vos réponses à ces trois recommandations révèlent vos préférences. Par exemple, si vous répondez « Oui, réservez-moi celle qui est près des galeries », vous manifestez un intérêt pour l'art. En revanche, si vous demandez « N'y a-t-il rien à moins de 200 $ ? », vous êtes sensible au prix et vous pensez que l'assistant n'a pas encore bien cerné vos attentes.

Les retours des utilisateurs, extraits des conversations, peuvent être utilisés pour l'évaluation, le développement et la personnalisation :

- Évaluation : définir des indicateurs pour surveiller l'application
    
- Développement : former les futurs modèles ou guider leur développement
    
- Personnalisation : personnaliser l'application pour chaque utilisateur
    

Les retours conversationnels implicites peuvent être déduits du contenu des messages des utilisateurs et de leurs modes de communication. Comme ces retours sont intégrés aux conversations quotidiennes, leur extraction est complexe. Si l'intuition concernant les indices conversationnels peut aider à identifier une première série de signaux à rechercher, une analyse rigoureuse des données et des études auprès des utilisateurs sont indispensables pour les comprendre pleinement.

Bien que le feedback conversationnel ait bénéficié d'une attention accrue grâce à la popularité des chatbots conversationnels, il constituait déjà un domaine de recherche actif plusieurs années avant l'apparition de ChatGPT. La communauté de l'apprentissage par renforcement s'efforce, depuis la fin des années 2010, de permettre aux algorithmes d'apprentissage par renforcement d'apprendre à partir du feedback en langage naturel, avec des résultats prometteurs (voir [Fu et al., 2019](https://arxiv.org/abs/1902.07742) ; [Goyal et al.,](https://arxiv.org/abs/1903.02020) 2019 ; [Zhou et Small, 2020](https://arxiv.org/abs/2008.06924) ; et [Sumers et al., 2020](https://arxiv.org/abs/2009.14715) ). Le feedback en langage naturel présente également un grand intérêt pour les premières applications d'IA conversationnelle telles qu'Amazon Alexa ( [Ponnusamy et al., 2019](https://arxiv.org/abs/1911.02557) ; [Park et al., 2020](https://arxiv.org/abs/2010.12251) ), la commande vocale de Spotify ( [Xiao et al., 2021](https://oreil.ly/m8o0h) ) et Yahoo! Voice ( [Hashimoto et Sassano, 2018](https://oreil.ly/bGAeG) ).

### Commentaires en langage naturel

Les retours extraits du contenu des messages sont appelés retours en langage naturel. Voici quelques exemples de signaux de retour en langage naturel qui vous indiquent le déroulement d'une conversation. Il est utile de suivre ces signaux en production pour surveiller les performances de votre application.

#### Rupture anticipée

Si un utilisateur interrompt une réponse prématurément, par exemple en arrêtant la génération de la réponse à mi-chemin, en quittant l'application (pour les applications Web et mobiles), en demandant au modèle de s'arrêter (pour les assistants vocaux), ou en laissant simplement l'agent en suspens (par exemple, en ne répondant pas à l'agent avec l'option que vous souhaitez qu'il utilise), il est probable que la conversation ne se déroule pas bien.

#### Correction d'erreurs

Si un utilisateur commence sa demande de suivi par « Non… » ou « Je voulais dire… », la réponse du modèle risque d'être inappropriée.

Pour corriger les erreurs, les utilisateurs peuvent reformuler leurs requêtes. [La figure 10-12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_12_1730130985262750) illustre une tentative de reformulation. Ces tentatives peuvent être détectées par des heuristiques ou des modèles d'apprentissage automatique.

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1012.png)

###### Figure 10-12. Étant donné que l'utilisateur met fin à la génération prématurément et reformule la question, on peut en déduire que le modèle a mal compris l'intention de la requête initiale.

Les utilisateurs peuvent également signaler des points précis que le modèle aurait dû aborder différemment. Par exemple, si un utilisateur demande au modèle de résumer une histoire et que celui-ci confond un personnage, l'utilisateur peut faire un commentaire tel que : « Bill est le suspect, pas la victime. » Le modèle devrait pouvoir prendre en compte ce commentaire et corriger son résumé.

Ce type de retour d'information correctif est particulièrement fréquent dans les cas d'utilisation d'agents, où les utilisateurs peuvent inciter l'agent à réaliser des actions plus optionnelles. Par exemple, si un utilisateur confie à l'agent la tâche d'effectuer une analyse de marché sur l'entreprise XYZ, il pourrait lui suggérer de consulter également la page GitHub de XYZ ou le profil X du PDG.

Il arrive que les utilisateurs souhaitent que le modèle se corrige en demandant une confirmation explicite, par exemple : « Êtes-vous sûr ? », « Vérifiez à nouveau » ou « Affichez-moi les sources ». Cela ne signifie pas forcément que le modèle donne de mauvaises réponses. Toutefois, cela peut indiquer que les réponses de votre modèle manquent de détails. Cela peut également révéler une certaine méfiance envers votre modèle.

Certaines applications permettent aux utilisateurs de modifier directement les réponses du modèle. Par exemple, si un utilisateur demande au modèle de générer du code, puis corrige ce code, cela indique clairement que le code modifié est incorrect.

Les modifications apportées par les utilisateurs constituent également une source précieuse de données sur leurs préférences. Rappelons que ces données, généralement au format (requête, réponse gagnante, réponse perdante), permettent d'adapter un modèle aux préférences humaines. Chaque modification constitue un exemple de préférence : la réponse initiale est la réponse perdante et la réponse modifiée, la réponse gagnante.

#### Plaintes

Souvent, les utilisateurs se plaignent des résultats de votre application sans chercher à les corriger. Par exemple, ils peuvent signaler qu'une réponse est erronée, non pertinente, toxique, trop longue, trop vague ou tout simplement mauvaise. [Le tableau 10-1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_table_1_1730130985279574) présente huit groupes de commentaires en langage naturel issus du regroupement automatique des données FITS (Feedback for Interactive Talk & Search) ( [Xu et al., 2022](https://arxiv.org/abs/2208.03270) ).

Tableau 10-1. Types de rétroaction dérivés du regroupement automatique de l'ensemble de données FITS (Xu et al., 2022). Résultats de [Yuan et al. (2023)](https://arxiv.org/abs/2306.13588) .
|Groupe|Type de retour d'information|Num.|%|
|---|---|---|---|
|1|Clarifiez à nouveau leur demande.|3702|26,54%|
|2|Se plaindre que le bot (1) ne répond pas à la question ou (2) donne des informations non pertinentes ou (3) demande à l'utilisateur de trouver la réponse par lui-même.|2260|16,20%|
|3|Indiquez les résultats de recherche précis qui permettent de répondre à la question.|2255|16,17%|
|4|Suggérer que le bot utilise les résultats de la recherche.|2130|15,27%|
|5|Indiquez que la réponse est (1) factuellement incorrecte, ou (2) non fondée sur les résultats de la recherche.|1572|11,27%|
|6|Faites remarquer que la réponse du bot n'est pas spécifique/exacte/complète/détaillée.|1309|9,39%|
|7|Faites remarquer que le bot n'est pas sûr de ses réponses et commence toujours ses réponses par « Je ne suis pas sûr » ou « Je ne sais pas ».|582|4,17%|
|8|Signalez les répétitions et l'impolitesse des réponses des bots.|137|0,99%|

Comprendre les points faibles du bot est essentiel pour l'améliorer. Par exemple, si vous savez que l'utilisateur n'apprécie pas les réponses trop longues, vous pouvez raccourcir les messages du bot. Si l'utilisateur est insatisfait du manque de détails dans la réponse, vous pouvez inciter le bot à être plus précis.

#### Sentiment

Les plaintes peuvent aussi être de simples expressions de sentiments négatifs (frustration, déception, moqueries, etc.) sans explication, comme un simple « Pfff ». Cela peut paraître dystopique, mais l'analyse des sentiments d'un utilisateur lors de ses conversations avec un chatbot peut révéler des informations précieuses sur le fonctionnement de ce dernier. Certains centres d'appels analysent la voix des utilisateurs pendant les appels. Si un utilisateur hausse le ton, c'est qu'il y a un problème. À l'inverse, si une personne commence une conversation en colère mais la termine positivement, cela signifie probablement que son problème est résolu.

Les réponses du modèle permettent également de déduire un retour d'information en langage naturel. Un indicateur important est son _taux de refus_ . Si le modèle répond par exemple « Désolé, je ne connais pas cette réponse » ou « En tant que modèle de langage, je ne peux pas faire… », l'utilisateur est probablement insatisfait.

### Autres commentaires conversationnels

D'autres types de retours conversationnels peuvent être obtenus à partir des actions de l'utilisateur plutôt que des messages.

#### Régénération

De nombreuses applications permettent aux utilisateurs de générer une autre réponse, parfois avec un modèle différent. Si un utilisateur choisit de régénérer une réponse, c'est peut-être parce qu'il n'est pas satisfait de la première. Cependant, il se peut aussi que la première réponse soit adéquate, mais que l'utilisateur souhaite avoir d'autres options à comparer. C'est particulièrement fréquent pour les demandes créatives telles que la génération d'images ou de récits.

Les signaux de régénération pourraient également être plus forts pour les applications facturées à l'usage que pour celles fonctionnant par abonnement. Avec la facturation à l'usage, les utilisateurs sont moins enclins à régénérer leur compte et à dépenser plus par simple curiosité.

Personnellement, j'opte souvent pour la régénération pour les requêtes complexes afin de garantir la cohérence des réponses du modèle. Si deux réponses sont contradictoires, je ne peux me fier à aucune.

Après régénération, certaines applications peuvent demander explicitement à comparer la nouvelle réponse avec la précédente, comme illustré à [la figure 10-13](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_13_1730130985262768) . Ces données, meilleures ou moins bonnes, peuvent ensuite être utilisées pour affiner les préférences.

![Fond blanc avec un cercle noir. Description générée automatiquement avec un niveau de confiance moyen.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1013.png)

###### Figure 10-13. ChatGPT demande un retour d'information comparatif lorsqu'un utilisateur régénère une autre réponse.

#### Organisation de conversation

Les actions effectuées par un utilisateur pour organiser ses conversations (supprimer, renommer, partager, ajouter aux favoris, etc.) peuvent également être révélatrices. Supprimer une conversation est un signe assez clair qu'elle est problématique, sauf s'il s'agit d'une conversation embarrassante et que l'utilisateur souhaite en effacer toute trace. Renommer une conversation suggère qu'elle est pertinente, mais que le titre généré automatiquement est inapproprié.

#### Durée de la conversation

Un autre signal fréquemment analysé est _le nombre d'échanges par conversation_ . Son interprétation (positive ou négative) dépend de l'application. Pour les assistants vocaux, une conversation longue peut indiquer que l'utilisateur apprécie l'échange. En revanche, pour les chatbots axés sur la productivité, comme le support client, une conversation longue peut révéler une inefficacité du bot pour aider les utilisateurs à résoudre leurs problèmes.

#### Diversité du dialogue

La longueur de la conversation peut être interprétée conjointement avec _la diversité du dialogue_ , mesurable par le nombre de mots distincts ou de sujets abordés. Par exemple, si la conversation est longue mais que le bot répète sans cesse les mêmes phrases, l'utilisateur risque de se retrouver bloqué dans une boucle.

Les retours explicites sont plus faciles à interpréter, mais ils exigent un effort supplémentaire de la part des utilisateurs. Comme beaucoup d'utilisateurs peuvent rechigner à fournir cet effort, les retours explicites peuvent être rares, notamment dans les applications ayant une base d'utilisateurs réduite. Les retours explicites sont également sujets à des biais de réponse. Par exemple, les utilisateurs insatisfaits sont plus susceptibles de se plaindre, ce qui peut donner l'impression que les retours sont plus négatifs qu'ils ne le sont réellement.

Les retours implicites sont plus nombreux — leur définition n'a de limite que votre imagination — mais ils sont plus bruités. Interpréter les signaux implicites peut s'avérer complexe. Par exemple, partager une conversation peut être un signal positif ou négatif. Ainsi, un de mes amis partage surtout les conversations lorsque le modèle a commis des erreurs flagrantes, tandis qu'un autre partage principalement les conversations utiles avec ses collègues. _Il est essentiel d'étudier vos utilisateurs pour comprendre leurs motivations_ .

L'ajout de signaux supplémentaires peut contribuer à clarifier l'intention. Par exemple, si l'utilisateur reformule sa question après avoir partagé un lien, cela peut indiquer que la conversation n'a pas répondu à ses attentes. L'extraction, l'interprétation et l'exploitation des réponses implicites dans les conversations constituent un domaine de recherche encore restreint mais en pleine expansion..[8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1838)

## Conception de retour d'information

Si vous ne saviez pas quel type de commentaires recueillir, j'espère que la section précédente vous aura donné quelques idées.

Cette section explique quand et comment recueillir ces précieux commentaires.

### Quand recueillir des commentaires

Les retours d'information peuvent et doivent être recueillis tout au long du parcours utilisateur. Les utilisateurs doivent avoir la possibilité de donner leur avis, notamment pour signaler des erreurs, dès que le besoin s'en fait sentir. Toutefois, cette option de collecte de retours d'information doit être non intrusive et ne pas perturber le flux de travail de l'utilisateur. Voici quelques exemples de situations où les retours d'information des utilisateurs peuvent s'avérer particulièrement précieux.

#### Au début

Lorsqu'un utilisateur vient de s'inscrire, ses commentaires peuvent aider à adapter l'application à ses besoins. Par exemple, une application de reconnaissance faciale doit d'abord scanner votre visage pour fonctionner. Un assistant vocal peut vous demander de lire une phrase à voix haute afin de reconnaître votre voix et d'utiliser les mots d'activation (comme « OK Google »). Une application d'apprentissage des langues peut vous poser quelques questions pour évaluer votre niveau. Pour certaines applications, comme la reconnaissance faciale, l'adaptation est nécessaire. Pour d'autres, en revanche, les premiers retours devraient être facultatifs, car ils peuvent dissuader les utilisateurs d'essayer votre produit. Si un utilisateur ne précise pas sa préférence, vous pouvez opter pour une solution neutre et procéder à un ajustement au fil du temps.

#### Quand quelque chose de mal arrive

Lorsque le modèle génère une réponse erronée, bloque une requête légitime, produit une image compromettante ou tarde à répondre, les utilisateurs doivent pouvoir vous signaler ces dysfonctionnements. Vous pouvez leur offrir la possibilité de voter contre une réponse, de la faire régénérer avec le même modèle ou d'en choisir un autre. Ils peuvent également fournir des commentaires informels tels que « Vous avez tort », « C'est trop cliché » ou « Je préférerais une réponse plus courte ».

Idéalement, même en cas d'erreur de votre produit, les utilisateurs devraient pouvoir continuer à accomplir leurs tâches. Par exemple, si le modèle classe un produit dans une catégorie erronée, les utilisateurs peuvent la modifier. Permettez aux utilisateurs de collaborer avec l'IA. Si cela s'avère impossible, offrez-leur la possibilité de collaborer avec des humains. De nombreux chatbots de support client proposent de transférer les utilisateurs vers des agents humains si la conversation s'éternise ou si les utilisateurs semblent frustrés.

Un exemple de collaboration homme-IA est la fonctionnalité _de remplissage d'images_ pour la génération d'images. [Si](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1842) une image générée ne correspond pas exactement aux besoins de l'utilisateur, celui-ci peut sélectionner une zone et indiquer, à l'aide d'une invite de commande, comment l'améliorer. [La figure 10-14](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_14_1730130985262784) illustre un exemple de remplissage avec [DALL-E](https://oreil.ly/Edew9) (OpenAI, 2021). Cette fonctionnalité permet aux utilisateurs d'obtenir de meilleurs résultats tout en fournissant aux développeurs un retour d'information de qualité.

![Capture d'écran d'une bande dessinée. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1014.png)

###### Figure 10-14. Un exemple de fonctionnement de l'inpainting dans DALL-E. Image par [OpenAI](https://oreil.ly/nAplp) .

#### Lorsque le modèle a une faible confiance

Lorsqu'un modèle est incertain quant à une action, vous pouvez solliciter l'avis de l'utilisateur afin d'accroître sa confiance. Par exemple, face à une demande de résumé d'un article, si le modèle hésite entre un résumé court et général et un résumé détaillé, section par section, il peut afficher les deux résumés côte à côte, à condition que cela n'augmente pas le temps de réponse pour l'utilisateur. Ce dernier peut alors choisir celui qu'il préfère. Ces signaux comparatifs permettent d'affiner les préférences. Un exemple d'évaluation comparative en production est présenté dans [la figure 10-15](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_15_1730130985262799) .

![Capture d'écran d'une conversation. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1015.png)

###### Figure 10-15. Comparaison côte à côte de deux réponses ChatGPT.

Afficher deux réponses complètes parmi lesquelles choisir revient à solliciter un avis explicite de l'utilisateur. Or, celui-ci n'aura peut-être ni le temps de lire les deux réponses en entier, ni l'envie de donner un avis réfléchi. Cela peut engendrer des votes confus.Certaines applications, comme Google Gemini, n'affichent que le début de chaque réponse, comme illustré dans [la figure 10-16 . Les utilisateurs peuvent cliquer pour développer la réponse qu'ils souhaitent lire. Il n'est cependant pas clair si l'affichage côte à côte de réponses complètes ou partielles fournit un retour d'](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_16_1730130985262822) [information](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1844) plus fiable.[](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1844)

![Capture d'écran d'un ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1016.png)

###### Figure 10-16. Google Gemini présente des réponses partielles côte à côte pour faciliter la comparaison. Les utilisateurs doivent cliquer sur la réponse qui les intéresse et reçoivent un retour d'information sur la réponse qu'ils jugent la plus prometteuse.

Un autre exemple est une application d'organisation de photos qui étiquette automatiquement vos photos afin de pouvoir répondre à des requêtes comme « Afficher toutes les photos de X ». En cas de doute sur l'identité de deux personnes, elle peut vous demander confirmation, comme le fait Google Photos dans [la figure 10-17](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_17_1730130985262838) .

![Capture d'écran d'un chat de dessin animé. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1017.png)

###### Figure 10-17. Google Photos demande l'avis de l'utilisateur en cas de doute. Les deux images de chats ont été générées par ChatGPT.

Vous vous demandez peut-être : comment obtenir des retours lorsqu’un résultat positif est obtenu ? Les utilisateurs peuvent exprimer leur satisfaction en cliquant sur le pouce levé, en ajoutant l’application à leurs favoris ou en la partageant. Cependant, [les recommandations d’Apple concernant l’interface utilisateur](https://oreil.ly/GeZvj) déconseillent de solliciter des retours à la fois positifs et négatifs. Votre application doit produire de bons résultats par défaut. Demander des retours sur des résultats satisfaisants pourrait donner aux utilisateurs l’impression que ces résultats sont exceptionnels. En fin de compte, si les utilisateurs sont satisfaits, ils continueront à utiliser votre application.

Cependant, de nombreuses personnes avec qui j'ai discuté pensent que les utilisateurs devraient avoir la possibilité de donner leur avis lorsqu'ils découvrent une fonctionnalité remarquable. Le chef de produit d'un produit populaire basé sur l'IA a mentionné que son équipe a besoin de retours positifs car ils révèlent les fonctionnalités que les utilisateurs apprécient suffisamment pour exprimer leur enthousiasme. Cela permet à l'équipe de se concentrer sur l'amélioration d'un petit nombre de fonctionnalités à fort impact plutôt que de disperser ses ressources sur de nombreuses fonctionnalités à faible valeur ajoutée.

Certains hésitent à solliciter des retours positifs par crainte d'encombrer l'interface ou d'agacer les utilisateurs. Ce risque peut toutefois être maîtrisé en limitant la fréquence des demandes de retours. Par exemple, si votre base d'utilisateurs est importante, n'envoyer la demande qu'à 1 % d'entre eux à la fois peut permettre de recueillir suffisamment de retours sans perturber l'expérience des autres. Gardez à l'esprit que plus le pourcentage d'utilisateurs sollicités est faible, plus le risque de biais dans les retours est élevé. Néanmoins, avec un échantillon suffisamment important, les retours peuvent fournir des informations précieuses sur le produit.

### Comment recueillir des commentaires

Les retours d'information doivent s'intégrer naturellement au flux de travail de l'utilisateur. Il doit être facile pour les utilisateurs de donner leur avis sans effort supplémentaire. La collecte de retours ne doit pas perturber l'expérience utilisateur et il doit être facile de l'ignorer. Des incitations doivent être mises en place pour encourager les utilisateurs à fournir des retours constructifs.

L'application de génération d'images Midjourney est un exemple souvent cité de conception de retour d'information efficace. Pour chaque invite, Midjourney génère un ensemble de quatre images et propose à l'utilisateur les options suivantes, comme illustré dans [la figure 10-18](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_18_1730130985262861) :

1. Générez une version non redimensionnée de chacune de ces images.
    
2. Générez des variantes pour chacune de ces images.
    
3. Régénérer.
    

Chacune de ces options envoie des signaux différents à Midjourney. Les options 1 et 2 indiquent à Midjourney laquelle des quatre photos est considérée par l'utilisateur comme la plus prometteuse. L'option 1 fournit le signal positif le plus fort concernant la photo choisie. L'option 2 fournit un signal positif plus faible. L'option 3 indique qu'aucune des photos n'est suffisamment satisfaisante. Cependant, les utilisateurs peuvent choisir de régénérer l'image, même si les photos existantes sont bonnes, simplement pour explorer d'autres possibilités.

![Capture d'écran d'un jeu vidéo. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1018.png)

###### Figure 10-18. Le flux de travail de Midjourney permet à l'application de recueillir des commentaires implicites.

Les assistants de code comme GitHub Copilot peuvent afficher leurs brouillons dans des couleurs plus claires que le texte final, comme illustré dans [la figure 10-19](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_19_1730130985262880) . L'utilisateur peut utiliser la touche Tabulation pour accepter une suggestion ou continuer à saisir du texte pour l'ignorer, ce qui permet dans les deux cas de fournir un retour d'information.

![Capture d'écran d'un programme informatique. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1019.png)

###### Figure 10-19. GitHub Copilot facilite à la fois la suggestion et le rejet d'une suggestion.

L'un des principaux défis des applications d'IA autonomes comme ChatGPT et Claude réside dans leur manque d'intégration au flux de travail quotidien de l'utilisateur. Il est donc difficile de recueillir des retours de qualité, contrairement aux solutions intégrées telles que GitHub Copilot. Par exemple, si Gmail suggère un brouillon d'e-mail, il peut suivre son utilisation et ses modifications. En revanche, si vous utilisez ChatGPT pour rédiger un e-mail, ChatGPT ignore si celui-ci a effectivement été envoyé.

Les commentaires, à eux seuls, peuvent être utiles pour l'analyse produit. Par exemple, l'affichage des votes positifs/négatifs permet de calculer la fréquence à laquelle les utilisateurs sont satisfaits ou insatisfaits de votre produit. Toutefois, pour une analyse plus approfondie, il est nécessaire de prendre en compte le contexte des commentaires, comme les 5 à 10 derniers échanges. Ce contexte peut vous aider à identifier les problèmes rencontrés. Cependant, obtenir ce contexte peut s'avérer impossible sans le consentement explicite de l'utilisateur, notamment s'il contient des informations personnelles.

C’est pourquoi certains produits incluent dans leurs contrats de service des clauses leur permettant d’accéder aux données des utilisateurs à des fins d’analyse et d’amélioration du produit. Pour les applications qui n’en comportent pas, les retours des utilisateurs peuvent être liés à un processus de don de données, où il leur est demandé de partager leurs données d’interaction récentes avec leurs commentaires. Par exemple, lors de l’envoi d’un commentaire, il peut vous être demandé de cocher une case pour partager vos données récentes afin de contextualiser ce commentaire.

Expliquer aux utilisateurs comment leurs commentaires sont utilisés peut les inciter à fournir des retours plus nombreux et plus pertinents. Utilisez-vous les commentaires d'un utilisateur pour personnaliser le produit, recueillir des statistiques d'utilisation générale ou entraîner un nouveau modèle ? Si les utilisateurs s'inquiètent de la confidentialité de leurs données, rassurez-les : leurs données ne seront ni utilisées pour entraîner des modèles, ni transférées hors de leur appareil (à condition que ces affirmations soient exactes).

Ne demandez pas l'impossible aux utilisateurs. Par exemple, si vous recueillez des signaux comparatifs, ne leur demandez pas de choisir entre deux options qu'ils ne comprennent pas. J'ai moi-même été déconcerté lorsque ChatGPT m'a demandé de choisir entre deux réponses possibles à une question statistique, comme illustré dans [la figure 10-20](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_20_1730130985262906) . J'aurais aimé pouvoir répondre « Je ne sais pas ».

![Capture d'écran d'une conversation. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1020.png)

###### Figure 10-20. Exemple de ChatGPT demandant à un utilisateur de sélectionner la réponse qu'il préfère. Cependant, pour les questions mathématiques de ce type, la bonne réponse ne devrait pas être une question de préférence.

Ajoutez des icônes et des infobulles à une option si elles facilitent sa compréhension. Évitez une conception susceptible de dérouter les utilisateurs. Des instructions ambiguës peuvent engendrer des retours d'information confus. J'ai animé un atelier d'optimisation GPU et utilisé Luma pour recueillir les commentaires. À la lecture des retours négatifs, j'ai été surpris. Malgré des réponses positives, les notes étaient de 1/5. Après quelques recherches, j'ai constaté que Luma utilisait des émojis pour représenter les nombres dans son formulaire de collecte de commentaires, mais l'émoji de colère, correspondant à une note d'une étoile, était placé à la place de la note de cinq étoiles, comme illustré dans [la figure 10-21](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#ch10_figure_21_1730130985262932) .

Réfléchissez bien à la confidentialité des commentaires des utilisateurs. Par exemple, si un utilisateur apprécie un élément, souhaitez-vous que cette information soit visible par les autres utilisateurs ? À ses débuts, les commentaires de Midjourney (choix d'agrandir une image, de générer des variantes ou de régénérer un autre lot d'images) étaient publics.

![Capture d'écran d'un écran d'ordinateur. Description générée automatiquement.](https://learning.oreilly.com/api/v2/epubs/urn:orm:book:9781098166298/files/assets/aien_1021.png)

###### Figure 10-21. Parce que Luma a placé l'emoji en colère, correspondant à une note d'une étoile, là où une note de cinq étoiles aurait dû être, certains utilisateurs l'ont choisi par erreur pour les avis positifs.

La visibilité d'un signal peut avoir un impact considérable sur le comportement des utilisateurs, leur expérience et la qualité des retours. Les utilisateurs ont tendance à être plus francs en privé (leurs activités ont moins de chances d'être jugées [)](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1846) , ce qui peut générer des signaux de meilleure qualité. En 2024, X (anciennement Twitter) a rendu les « J'aime » [privés](https://x.com/elonmusk/status/1800905349148664295) . Elon Musk, le propriétaire de X, a constaté une augmentation significative [du nombre de « J'aime](https://x.com/elonmusk/status/1801045558318313746) » suite à ce changement.

Cependant, les signaux privés peuvent réduire la visibilité et l'explicabilité. Par exemple, masquer les mentions « J'aime » empêche les utilisateurs de trouver les tweets aimés par leurs contacts. Si X recommande des tweets en fonction des mentions « J'aime » des personnes que vous suivez, masquer ces mentions pourrait semer la confusion chez les utilisateurs quant à la raison pour laquelle certains tweets apparaissent dans leur fil d'actualité..

## Limites des commentaires

L'importance des retours utilisateurs pour un développeur d'applications est indéniable. Cependant, ces retours ne sont pas gratuits et présentent certaines limites.

### Biais

Comme toute donnée, les retours des utilisateurs comportent des biais. Il est important de comprendre ces biais et de concevoir votre système de retour d'information en conséquence. Chaque application a ses propres biais. Voici quelques exemples de biais dans les retours d'information pour vous donner une idée de ce à quoi il faut faire attention :

biais de clémence

Le biais de clémence est la tendance à surévaluer les choses, souvent pour éviter les conflits, par souci de bienveillance ou par facilité. Imaginez : vous êtes pressé et une application vous demande d'évaluer une transaction. Vous n'êtes pas satisfait, mais vous savez qu'une évaluation négative vous obligera à justifier votre avis. Vous choisissez donc simplement « positif » pour en finir. C'est aussi pourquoi il ne faut pas demander d'efforts supplémentaires pour obtenir un avis.

Sur une échelle de cinq étoiles, quatre et cinq étoiles indiquent généralement une expérience positive. Cependant, il arrive souvent que les utilisateurs se sentent obligés d'attribuer cinq étoiles, réservant les quatre étoiles aux situations problématiques. Selon [Uber](https://oreil.ly/18tY4) , en 2015, la note moyenne des chauffeurs était de 4,8, les scores inférieurs à 4,6 exposant les chauffeurs à un risque de désactivation.

Ce biais n'est pas forcément rédhibitoire. L'objectif d'Uber est de distinguer les bons des mauvais chauffeurs. Malgré ce biais, leur système de notation semble contribuer à atteindre cet objectif. Il est essentiel d'analyser la répartition des notes attribuées par les utilisateurs afin de détecter ce biais.

Pour obtenir des retours plus précis, il est utile de supprimer la forte connotation négative associée aux notes faibles afin d'aider les utilisateurs à dépasser ce biais. Par exemple, au lieu d'afficher les chiffres de un à cinq, proposez-leur des options comme :

- « Superbe trajet. Excellent chauffeur. »
    
- "Très bon."
    
- « Rien à redire, mais rien d'exceptionnel non plus. »
    
- « Ça aurait pu être mieux. »
    
- « Ne me mettez plus jamais avec ce chauffeur. » [12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1852)
    

Aléatoire

Les utilisateurs fournissent souvent des commentaires aléatoires, non par malveillance, mais par manque de motivation pour donner un avis plus réfléchi. Par exemple, lorsque deux réponses longues sont affichées côte à côte pour une évaluation comparative, les utilisateurs peuvent ne pas vouloir les lire toutes les deux et cliquer sur l'une au hasard. Dans le cas de Midjourney, les utilisateurs peuvent également choisir une image au hasard pour générer des variations.

Biais de position

L'ordre dans lequel une option est présentée aux utilisateurs influence la façon dont elle est perçue. Les utilisateurs sont généralement plus enclins à cliquer sur la première suggestion que sur la seconde. Cependant, si un utilisateur clique sur la première suggestion, cela ne signifie pas nécessairement qu'il s'agit d'une bonne suggestion.

Lors de la conception de votre système de retour d'information, ce biais peut être atténué en faisant varier aléatoirement la position de vos suggestions ou en élaborant un modèle permettant de calculer le taux de réussite réel d'une suggestion en fonction de sa position.

Biais de préférence

De nombreux autres biais peuvent influencer les réponses, dont certains ont été abordés dans cet ouvrage. Par exemple, lors d'une comparaison directe, on peut être tenté de privilégier la réponse la plus longue, même si elle est moins précise : la longueur est plus facilement repérable que les inexactitudes. Un autre biais est [_le biais de récence_](https://oreil.ly/acfq0) , qui se manifeste par une tendance à privilégier la dernière réponse vue lors d'une comparaison.

Il est important d'analyser les commentaires des utilisateurs afin d'en déceler les biais. Comprendre ces biais vous aidera à interpréter correctement les commentaires et à éviter des décisions produit erronées.

### Boucle de rétroaction dégénérée

N'oubliez pas que les retours des utilisateurs sont incomplets. Vous n'obtenez de retours que sur ce que vous leur montrez.

Dans un système où les retours des utilisateurs servent à modifier le comportement d'un modèle, _des boucles de rétroaction dégénérées_ peuvent apparaître. Une boucle de rétroaction dégénérée se produit lorsque les prédictions elles-mêmes influencent les retours, qui, à leur tour, influencent l'itération suivante du modèle, amplifiant ainsi les biais initiaux.

Imaginez que vous développez un système de recommandation vidéo. Les vidéos les mieux classées apparaissent en premier et reçoivent donc plus de clics, confortant ainsi le système dans sa conviction qu'il s'agit des meilleures. Au départ, la différence entre les deux vidéos, A et B, peut sembler minime, mais comme A était légèrement mieux classée, elle a obtenu plus de clics, et le système a continué à la mettre en avant. Avec le temps, le classement de A a grimpé en flèche, reléguant B au second plan. Ce cercle vicieux explique pourquoi les vidéos populaires le restent, rendant difficile l'émergence de nouvelles vidéos. Ce phénomène est connu sous le nom de « biais d'exposition », « biais de popularité » ou « bulles de filtres », et il a fait l'objet de nombreuses études.

Un cercle vicieux de rétroaction peut modifier l'orientation et la base d'utilisateurs de votre produit. Imaginez qu'au départ, un petit nombre d'utilisateurs indiquent apprécier les photos de chats. Le système s'en inspire et génère davantage de photos de chats. Cela attire les amoureux des chats, qui, à leur tour, apprécient ces photos, incitant le système à en générer encore plus. Rapidement, votre application devient un véritable paradis pour les chats. J'utilise ici l'exemple des photos de chats, mais ce même mécanisme peut amplifier d'autres biais, tels que le racisme, le sexisme et la préférence pour les contenus explicites.

Se baser sur les retours des utilisateurs peut transformer un agent conversationnel en, pour ainsi dire, un menteur. De nombreuses études ont montré que l'entraînement d'un modèle sur les retours des utilisateurs peut l'amener à donner aux utilisateurs ce qu'il croit qu'ils veulent, même si ce n'est pas ce qui est le plus précis ou le plus bénéfique ( [Stray, 2023](https://oreil.ly/jtt2m) ). [Sharma et al. (2023)](https://arxiv.org/abs/2310.13548) montrent que les modèles d'IA entraînés sur les retours humains ont tendance à la flagornerie. Ils sont plus susceptibles de présenter des réponses d'utilisateurs qui correspondent au point de vue de cet utilisateur.

Les retours des utilisateurs sont essentiels pour améliorer l'expérience utilisateur, mais utilisés sans discernement, ils peuvent perpétuer les biais et nuire gravement à votre produit. Avant d'intégrer des retours d'information à votre produit, assurez-vous de bien comprendre leurs limites et leur impact potentiel..

# Résumé

Si chaque chapitre précédent était consacré à un aspect spécifique de l'ingénierie de l'IA, ce chapitre examine le processus de construction d'applications sur des modèles de base dans son ensemble.

Ce chapitre se composait de deux parties. La première abordait une architecture commune pour les applications d'IA. Bien que l'architecture exacte puisse varier d'une application à l'autre, cette architecture générale offre un cadre de compréhension de l'articulation des différents composants. J'ai utilisé une approche progressive pour construire cette architecture et ainsi exposer les difficultés rencontrées à chaque étape, ainsi que les techniques permettant de les surmonter.

Bien qu'il soit nécessaire de séparer les composants pour garantir la modularité et la maintenabilité de votre système, cette séparation est flexible. Les composants peuvent présenter de nombreux chevauchements de fonctionnalités. Par exemple, des garde-fous peuvent être implémentés dans le service d'inférence, la passerelle de modèles ou en tant que composant autonome.

Chaque composant supplémentaire peut potentiellement améliorer les performances, la sécurité ou la rapidité de votre système, mais accroît également sa complexité et l'expose à de nouveaux modes de défaillance. La surveillance et l'observabilité sont essentielles à tout système complexe. L'observabilité implique de comprendre comment le système tombe en panne, de concevoir des indicateurs et des alertes pour ces défaillances, et de s'assurer que sa conception permet de les détecter et de les retracer. Si de nombreuses bonnes pratiques et outils d'observabilité issus du génie logiciel et de l'apprentissage automatique traditionnel sont applicables aux applications d'IA, les modèles de base introduisent de nouveaux modes de défaillance, qui nécessitent des indicateurs et des considérations de conception supplémentaires.

Parallèlement, l'interface conversationnelle permet de recueillir de nouveaux types de retours utilisateurs, exploitables pour l'analyse, l'amélioration des produits et l'enrichissement continu des données. La deuxième partie de ce chapitre aborde différentes formes de retours conversationnels et explique comment concevoir une application pour les collecter efficacement.

Traditionnellement, la conception intégrant les retours utilisateurs relève davantage de la responsabilité du produit que de celle de l'ingénierie, et est donc souvent négligée par les ingénieurs. Or, les retours utilisateurs étant une source de données essentielle à l'amélioration continue des modèles d'IA, de plus en plus d'ingénieurs en IA s'impliquent dans ce processus afin de garantir l'accès aux données nécessaires. Ceci confirme l'idée du [chapitre 1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch01.html#ch01_introduction_to_building_ai_applications_with_foun_1730130814984319) selon laquelle, comparée à l'ingénierie ML traditionnelle, l'ingénierie IA se rapproche de plus en plus du produit. Cette évolution s'explique par l'importance croissante de l'effet d'entraînement des données et de l'expérience utilisateur comme atouts concurrentiels.

De nombreux défis liés à l'IA sont, par essence, des problèmes systémiques. Pour les résoudre, il est souvent nécessaire de prendre du recul et de considérer le système dans son ensemble. Un même problème peut être traité par différents composants fonctionnant indépendamment, ou sa résolution peut nécessiter la collaboration de plusieurs composants. Une compréhension approfondie du système est essentielle pour résoudre des problèmes concrets, explorer de nouvelles possibilités et garantir la sécurité.

[1](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1761-marker)Un exemple en est celui d'un employé de Samsung qui a accidentellement introduit des informations confidentielles de l'entreprise dans ChatGPT, [divulguant ainsi des secrets commerciaux](https://oreil.ly/_5RFN) .

[2](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1763-marker)Il est possible que les utilisateurs demandent au modèle de renvoyer une réponse vide.

[3](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1769-marker)Quelques lecteurs parmi les premiers à l'avoir lu m'ont confié que l'idée d'ignorer les garde-fous au profit de la latence leur donnait des cauchemars.

[4](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1786-marker)Au moment où nous écrivons ces lignes, la capitalisation boursière cumulée de quelques-unes des plus grandes sociétés d'observabilité (Datadog, Splunk, Dynatrace, New Relic) avoisine les 100 milliards de dollars.

[5](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1787-marker)Mon ouvrage, [_*Designing Machine Learning Systems*_](https://www.oreilly.com/library/view/designing-machine-learning/9781098107956/) (O'Reilly, 2022), comporte également un chapitre sur la surveillance. Une première version de ce chapitre est disponible sur mon blog, à l'adresse [« Data Distribution Shifts and Monitoring »](https://huyenchip.com/2022/02/07/data-distribution-shifts-and-monitoring.html) .

[6](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1811-marker)De ce fait, certains outils d'orchestration aspirent à devenir des passerelles. En réalité, nombre d'entre eux semblent vouloir se transformer en plateformes complètes capables de tout faire.

[7](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1816-marker)L'un des principaux inconvénients du lancement d'une application open source par rapport à une application commerciale réside dans la difficulté accrue à recueillir les retours des utilisateurs. Ces derniers peuvent s'approprier votre application open source et la déployer eux-mêmes, vous laissant ainsi sans aucun moyen de savoir comment elle est utilisée.

[8](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1838-marker)Non seulement vous pouvez recueillir des commentaires sur les applications d'IA, mais vous pouvez également utiliser l'IA pour analyser ces commentaires.

[9](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1842-marker)J'aimerais qu'il existe une fonction de remplissage pour la synthèse vocale. Je trouve qu'elle fonctionne bien dans 95 % des cas, mais les 5 % restants peuvent être frustrants. L'IA peut mal prononcer un nom ou oublier de faire une pause pendant les dialogues. J'aimerais qu'il existe des applications qui me permettent de corriger uniquement les erreurs au lieu de devoir régénérer tout l'audio.

[10](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1844-marker)Lorsque je pose cette question lors des événements auxquels je participe, les réponses sont partagées. Certains pensent que présenter les réponses complètes permet d'obtenir un retour d'information plus fiable, car cela donne aux utilisateurs davantage d'éléments pour prendre une décision. D'autres, en revanche, estiment qu'une fois les réponses complètes lues, les utilisateurs n'ont plus aucune raison de cliquer sur la meilleure.

[11](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1846-marker)Voir [« Ted Cruz accuse un membre de son personnel d’avoir « aimé » un tweet pornographique »](https://oreil.ly/xKEVc) (Nelson et Everett, _POLITICO_ , septembre 2017) et [« Le sénateur du Kentucky dont le compte Twitter a « aimé » des tweets obscènes affirme avoir été piraté »](https://oreil.ly/ve1DN) (Liam Niemeyer, WKU Public Radio, mars 2023).

[12](https://learning.oreilly.com/library/view/ai-engineering/9781098166298/ch10.html#id1852-marker)Les options proposées ici ne servent qu'à illustrer comment les options peuvent être reformulées. Elles n'ont pas été validées.