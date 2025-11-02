Le livre, intitulé _AI Engineering: Building Applications with Foundation Models_, comporte une structure claire, allant des concepts fondamentaux à l'optimisation en production.

Voici la liste des chapitres traduits en français :

• **Préface**

• **1. Introduction à la construction d'applications d'IA avec des modèles de fondation**

• **2. Comprendre les modèles de fondation**

• **3. Méthodologie d'évaluation**

• **4. Évaluer les systèmes d'IA**

• **5. Ingénierie des invites (Prompt Engineering)**

• **6. RAG (Retrieval-Augmented Generation) et Agents**

• **7. Ajustement fin (Finetuning)**

• **8. Ingénierie des jeux de données (Dataset Engineering)**

• **9. Optimisation de l'inférence**

• **10. Architecture d'ingénierie de l'IA et retour utilisateur**

• **Épilogue**

• **Index**

Le livre de Chip Huyen est structuré pour suivre le processus typique de développement d'une application d'IA, commençant par une compréhension des modèles (Chapitre 2) et se terminant par l'architecture de production et le retour utilisateur (Chapitre 10).

Voici une élaboration détaillée du contenu de ces sections principales :

Sections Liminaires et de Clôture

Le livre est précédé d'une **Préface**, qui introduit l'ingénierie de l'IA comme le processus de construction d'applications avec des modèles de fondation facilement disponibles. Il se termine par un **Épilogue**, suivi d'un **Index**.

Organisation des Chapitres

1. **Introduction à la construction d'applications d'IA avec des modèles de fondation** (p. 1) : Ce chapitre couvre l'essor de l'ingénierie de l'IA, la transition des modèles de langage vers les grands modèles de langage, puis vers les **modèles de fondation**, et présente les cas d'utilisation de ces modèles, tels que le codage, les bots conversationnels et l'automatisation des flux de travail. Il différencie également l'ingénierie de l'IA de l'ingénierie ML traditionnelle.

2. **Comprendre les modèles de fondation** (p. 49) : Ce chapitre est essentiel pour la sélection et l'adaptation des modèles. Il explore la modélisation, incluant l'architecture **Transformer** dominante et la taille des modèles. Il examine également l'impact des données d'entraînement (comme les modèles multilingues et spécifiques à un domaine) sur la performance des modèles.

3. **Méthodologie d'évaluation** (p. 113) : Ce chapitre et le suivant sont dédiés à l'évaluation, un défi crucial en ingénierie de l'IA. Il aborde les défis spécifiques à l'évaluation des modèles de fondation à _réponse ouverte_, les métriques de modélisation du langage comme la **Perplexité** et la **Cross-entropie**, et l'approche de l'**IA comme juge** (AI as a Judge).

4. **Évaluer les systèmes d'IA** (p. 159) : Ce chapitre se concentre sur l'utilisation des méthodes d'évaluation pour la **sélection de modèles** et la construction d'un pipeline d'évaluation fiable, en définissant les critères d'évaluation par catégorie : capacité spécifique au domaine, capacité de génération et capacité à suivre les instructions.

5. **Ingénierie des invites (Prompt Engineering)** (p. 211) : Cette technique est la méthode d'adaptation la plus courante et la plus simple. Elle explique les principes fondamentaux de la sollicitation (_prompting_), y compris l'apprentissage _few-shot_ et _zero-shot_, les meilleures pratiques (comme le _Chain-of-Thought_ ou CoT), et la **défense contre les attaques par injection d'invites**.

6. **RAG et Agents** (p. 253) : Ce chapitre est consacré à la construction de contexte pertinent. Le **RAG (Retrieval-Augmented Generation)** améliore la génération en récupérant des informations externes, tandis que les **Agents** sont des systèmes d'IA qui utilisent des outils et des mécanismes de planification pour accomplir des tâches complexes.

7. **Ajustement fin (Finetuning)** (p. 307) : Il s'agit d'adapter un modèle en ajustant ses poids. Le chapitre explore les **goulots d'étranglement de la mémoire** causés par le grand nombre de paramètres des modèles de fondation et les techniques d'**ajustement fin efficaces en paramètres (PEFT)**, telles que LoRA.

8. **Ingénierie des jeux de données (Dataset Engineering)** (p. 363) : Étant donné que la qualité d'un modèle dépend de ses données d'entraînement, ce chapitre aborde la curation des données (qualité, couverture, quantité), l'**augmentation et la synthèse de données**, ainsi que le traitement des données (inspection, déduplication, formatage).

9. **Optimisation de l'inférence** (p. 405) : Ce chapitre traite des techniques pour rendre l'inférence des modèles **plus rapide et moins coûteuse**, abordant l'optimisation au niveau du modèle (compression, techniques d'accélération du décodage) et l'optimisation au niveau du service (mise en cache, parallélisme).

10. **Architecture d'ingénierie de l'IA et retour utilisateur** (p. 449) : Le chapitre final propose une architecture complète, en intégrant des **garde-fous** (_guardrails_) et des **mécanismes de routage**. Il met également l'accent sur la **surveillance et l'observabilité** et sur la manière de concevoir des systèmes de **retour utilisateur** efficaces, particulièrement via les interfaces conversationnelles.