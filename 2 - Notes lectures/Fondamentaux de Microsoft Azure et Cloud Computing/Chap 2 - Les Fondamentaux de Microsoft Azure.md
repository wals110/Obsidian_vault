Résumé Exécutif

Ce document synthétise les concepts fondamentaux de Microsoft Azure, la plateforme de cloud public de Microsoft. Azure permet aux organisations de moderniser le déploiement d'applications et de réduire les dépenses d'investissement initiales (CapEx) en faveur d'un modèle de dépenses opérationnelles (OpEx) basé sur le paiement à l'utilisation. La plateforme est construite sur une infrastructure mondiale massive, offrant le plus grand nombre de régions géographiques parmi les principaux fournisseurs de cloud, ce qui garantit une haute disponibilité, une redondance et une conformité réglementaire.

La gestion des ressources dans Azure est structurée de manière hiérarchique, utilisant des groupes de gestion, des abonnements, des groupes de ressources et des ressources individuelles pour organiser et gouverner l'environnement cloud. L'Azure Resource Manager (ARM) est le service central de déploiement et de gestion, prenant en charge l'automatisation via l'Infrastructure as Code (IaC) avec des modèles ARM, Azure Bicep et Terraform.

La sécurité et la gestion des identités sont assurées par Microsoft Entra ID et le contrôle d'accès basé sur les rôles (RBAC), qui permettent une gestion granulaire des permissions. Azure propose un catalogue de services exhaustif, couvrant des domaines clés tels que le calcul, le stockage, la mise en réseau, les bases de données, l'intelligence artificielle, la sécurité et les outils DevOps, offrant ainsi une plateforme complète pour construire des solutions complexes et innovantes.

--------------------------------------------------------------------------------

1. Introduction à Microsoft Azure

Microsoft Azure, initialement lancé sous le nom de **Windows Azure** en 2008, est une plateforme de cloud public conçue pour être ouverte, flexible et de qualité professionnelle. Elle vise à aider les organisations à innover en construisant des solutions modernes qui répondent à leurs besoins spécifiques.

« Le _cloud computing_ a révolutionné la façon dont les entreprises gèrent leurs charges de travail informatiques. [...] Comprendre les fondamentaux est essentiel pour bâtir une excellente connaissance de base de Microsoft Azure que vous pourrez utiliser ultérieurement pour construire et gérer des charges de travail complexes. » [1] — Tiago Costa, Architecte et Conseiller Cloud, Microsoft Azure MVP, Microsoft Certified Trainer

La plateforme est en constante évolution, avec l'ajout régulier de nouvelles fonctionnalités et de nouveaux services, notamment dans les domaines de l'edge computing, de l'intelligence artificielle (IA) et de l'apprentissage automatique (ML).

1.1. Avantages du Modèle Cloud Azure

Azure aide les organisations à **minimiser les dépenses d'investissement initiales (CapEx)** en éliminant le besoin d'acheter et de maintenir du matériel physique, des serveurs ou des centres de données. Il propose des alternatives basées sur les dépenses opérationnelles (OpEx) grâce à son modèle de **paiement à l'utilisation (****pay-as-you-go****)**, où les organisations ne paient que pour les ressources qu'elles consomment. Ce modèle est particulièrement adapté aux charges de travail non constantes.

Le tableau suivant résume les principaux avantages d'Azure par rapport à un environnement sur site traditionnel :

|   |   |
|---|---|
|Avantage|Description|
|**Haute disponibilité**|Azure offre une haute disponibilité et une redondance dans ses centres de données mondiaux, garantissant un accord de niveau de service (SLA) de 99,95 % de disponibilité.|
|**Géo-distribution**|Les fonctionnalités de géo-distribution permettent aux entreprises mondiales de se conformer aux réglementations régionales grâce à des points de terminaison spécifiques à la géographie.|
|**Évolutivité sur demande**|La plateforme offre une manière flexible et rapide de gérer l'augmentation de la complexité, du trafic et des besoins en données.|

1.2. Le Portail Azure

Le **Portail Azure** est l'interface web centrale pour créer, gérer et surveiller toutes les ressources et tous les services cloud Azure. Accessible depuis n'importe quel navigateur web, il offre des fonctionnalités complètes :

• **Gestion centralisée** : Créer, construire, gérer et surveiller tous les services et ressources Azure.

• **Outils de ligne de commande** : Intégration du Cloud Shell pour des déploiements rapides.

• **Gouvernance** : Gérer les abonnements Azure et créer des groupes de gestion pour structurer les ressources.

• **Gestion des identités** : Utiliser **Microsoft Entra ID** pour gérer l'identité, l'accès et les permissions.

• **Conformité et sécurité** : Configurer la confidentialité, les politiques de sécurité et la conformité.

2. Catalogue des Services Microsoft Azure

Au moment de la rédaction, les services Azure sont répartis dans 21 catégories. Chaque service est conçu pour résoudre des problèmes techniques spécifiques et peut être intégré de manière transparente avec d'autres services Azure.

2.1. Catégories de Services Courantes

|   |   |   |
|---|---|---|
|Catégorie|Description|Exemples de services Azure|
|**Intelligence Artificielle (IA) + Apprentissage Automatique (ML)**|Construire des applications cloud modernes avec l'intégration de ML et de services cognitifs.|Azure Bot Service, Azure Cognitive Services, Azure Machine Learning, Azure AI Anomaly Detector, Computer Vision.|
|**Sécurité**|Protéger les ressources, les données et l'identité dans le cloud.|**Microsoft Entra ID**, **Microsoft Defender for Cloud**, Azure Security Center, **Azure Key Vault**, Azure Sentinel, DDoS Protection.|

2.2. Aperçu des Services de Base

Services de Calcul (_Compute_)

Les services de calcul fournissent des ressources informatiques telles que des systèmes d'exploitation, des processeurs, de la mémoire et des réseaux sur demande.

|   |   |
|---|---|
|Service de Calcul Azure|Utilité|
|**Azure App Service**|Construire et développer des applications web et mobiles dans un environnement cloud entièrement géré.|
|**Azure Static Web Apps**|Développer rapidement des applications web full stack modernes à partir d'un dépôt de code.|
|**Azure Virtual Machines (VMs)**|Provisionner rapidement des machines virtuelles sous Windows ou Linux.|
|**Service Fabric**|Construire des microservices et effectuer l'orchestration de conteneurs.|

Services de Mise en Réseau (_Networking_)

Ces services sécurisent et personnalisent l'infrastructure réseau cloud, privée ou publique, avec une sécurité de niveau entreprise basée sur le modèle **Microsoft Zero Trust**.

|   |   |
|---|---|
|Service de Mise en Réseau Azure|Utilité|
|**Azure Virtual Network (VNet)**|Créer un réseau privé dans le cloud et connecter des services VPN.|
|**Azure ExpressRoute**|Créer des connexions réseau privées entre les centres de données Azure et l'infrastructure sur site.|
|**Azure Traffic Manager**|Acheminer le trafic réseau pour optimiser les performances.|
|**Azure VPN Gateway**|Créer des connexions réseau privées sécurisées dans le cloud VPN.|

Services de Stockage (_Storage_)

Azure offre des solutions de stockage hautement disponibles, durables et sécurisées pour divers types de données. Chaque service de stockage doit être associé à un **compte de stockage Azure**, qui agit comme un conteneur logique.

|   |   |
|---|---|
|Service de Stockage Azure|Utilité|
|**Azure Blobs**|Stocker des données binaires évolutives, du texte ou Data Lake Storage Gen2 pour l'analyse de _big data_.|
|**Azure Files**|Partages de fichiers entièrement gérables pour des déploiements sur site ou dans le cloud.|
|**Azure Queues**|Collecter de gros messages accessibles via des appels HTTP authentifiés.|
|**Azure Managed Disks**|Stocker des volumes de niveau bloc pour les Machines Virtuelles Azure.|

Services de Bases de Données (_Database_)

Azure propose une gamme de services de bases de données gérées pour les données relationnelles, NoSQL et en mémoire.

|   |   |
|---|---|
|Service de Base de Données Azure|Utilité|
|**Azure SQL Database**|Bases de données SQL entièrement gérées, intelligentes et sécurisées hébergées dans le cloud.|
|**Azure Cosmos DB**|Créer et migrer des charges de travail NoSQL comme Cassandra, MongoDB et autres.|
|**Azure Cache for Redis DB**|Construire des applications rapides et évolutives avec le magasin de données en mémoire Redis.|
|**Azure Database for PostgreSQL, MySQL, et MariaDB**|Créer des bases de données entièrement gérées et évolutives pour ces moteurs.|
|**Azure SQL Edge**|Construire un moteur de base de données SQL optimisé pour l'edge IoT avec IA intégrée.|

Services de Gestion des Identités et de Sécurité

|   |   |
|---|---|
|Service d'Identité ou de Sécurité Azure|Utilité|
|**Microsoft Entra ID**|Sécuriser les identités des utilisateurs avec le _Single Sign-On_ (SSO).|
|**Azure Key Vault**|Gérer et stocker des clés cryptographiques, des certificats et d'autres secrets.|
|**Azure Firewall**|Fournir une protection de sécurité réseau au niveau des couches 3 et 4 du modèle OSI.|
|**Microsoft Defender for Cloud**|Solution de sécurité native du cloud offrant une protection avancée contre les menaces pour les charges de travail hybrides et multicloud.|

Outils de Développement, Surveillance et Services DevOps

|   |   |
|---|---|
|Outil de Développement ou Service DevOps Azure|Utilité|
|**Azure DevOps Services**|Fournit des outils pour la collaboration d'équipe, la gestion de projet Agile, la gestion du code source, les pipelines CI/CD et les plans de test.|
|**Azure DevTest Labs**|Configurer et gérer des environnements de test et de développement.|
|**Azure Artifacts**|Gérer les paquets binaires pour les logiciels d'entreprise.|
|**Azure Container Registry**|Services de registre Docker privé, géré par Azure, pour le stockage d'images de conteneurs.|

|   |   |
|---|---|
|Outil de Surveillance Azure|Utilité|
|**Azure Monitor**|Collecter, analyser et visualiser les données de télémétrie pour maximiser la performance des applications.|
|**Application Insights**|Fournit des fonctionnalités de gestion des performances des applications (APM), comme la surveillance en direct.|
|**Azure Advisor**|Recommande des solutions pour sécuriser les ressources, économiser des coûts et améliorer les performances.|
|**Log Analytics**|Permet d'exécuter des requêtes de journal et d'analyser les données collectées par Azure Monitor Logs.|

Services de Migration et Cloud Hybride + Multi-Cloud

|                    |                                                                                   |
| ------------------ | --------------------------------------------------------------------------------- |
| Service Azure      | Utilité                                                                           |
| **Azure Data Box** | Solution matérielle pour le transfert de grandes quantités de données vers Azure. |
| **Azure Migrate**  | Ensemble de guides et d'outils pour la migration vers Azure.                      |
| **Azure Arc**      | Combiner et unifier l'infrastructure sur site, hybride et multi-cloud.            |
| **Azure Stack**    | Construire et exécuter des applications hybrides au-delà des limites du cloud.    |

3. Architecture et Gestion des Ressources

La gestion des ressources dans Azure suit une structure hiérarchique qui permet une gouvernance et une organisation efficaces.

1. **Groupes de Gestion Azure** : Conteneurs logiques situés au-dessus des abonnements, permettant d'appliquer des politiques de gouvernance, d'accès et de conformité à grande échelle.

2. **Abonnements Azure** : Un conteneur logique pour les instances de services Azure, associé à un seul tenant **Microsoft Entra ID**. Le choix de l'abonnement affecte la tarification, l'accès et les limites de service.

3. **Groupes de Ressources Azure** : Conteneurs logiques où les ressources Azure sont déployées, gérées et stockées. Toutes les ressources doivent appartenir à un groupe de ressources.

4. **Ressources Azure** : Les instances de services individuelles (VMs, bases de données, applications web, etc.). Des **balises (****tags****)** (paires clé-valeur) peuvent être ajoutées aux ressources pour les catégoriser, notamment à des fins de facturation.

Azure Resource Manager (ARM)

**Azure Resource Manager (ARM)** est le service de déploiement et de gestion central d'Azure. Il permet aux utilisateurs d'ajouter, de modifier et de supprimer des ressources de manière sécurisée et organisée. ARM est essentiel pour mettre en œuvre l'**Infrastructure as Code (IaC)**, en utilisant :

• **Modèles ARM (****ARM templates****)** : Fichiers JSON pour automatiser les déploiements.

• **Azure Bicep** : Un langage spécifique au domaine qui simplifie la création de modèles ARM.

• **Terraform** : Un outil tiers populaire également pris en charge pour le provisionnement d'infrastructure sur Azure.

4. Infrastructure Mondiale d'Azure

L'infrastructure mondiale d'Azure est conçue pour une résilience et une haute disponibilité maximales.

• **Géographies** : Microsoft Azure dispose de centres de données physiques dans **140 pays**.

• **Régions** : Azure possède le plus grand nombre de régions géographiques mondiales parmi tous les fournisseurs de cloud. Le choix d'une région est crucial pour la conformité réglementaire (ex: RGPD en Europe) et la latence.

• **Paires de Régions** : Chaque région Azure est associée à une autre région au sein de la même géographie, avec une distance minimale préférée de 300 miles entre les centres de données. En cas de panne d'une région, les services basculent automatiquement vers la région appariée, assurant la continuité des activités.

• **Zones de Disponibilité** : Ce sont des emplacements physiques uniques (un ou plusieurs centres de données) au sein d'une même région Azure, dotés d'une alimentation, d'un refroidissement et d'un réseau indépendants. Elles offrent un SLA de **99,99 % de temps de disponibilité pour les machines virtuelles** et protègent contre les pannes complètes d'un centre de données. Elles diffèrent des **ensembles de disponibilité (****availability sets****)**, qui protègent contre les pannes matérielles _au sein_ d'un même centre de données.

5. Gestion des Coûts et de l'Identité

Coûts et Facturation

• **Coût total de possession (TCO) d'Azure** : Fournit une estimation des coûts des services en fonction du type de service, de l'abonnement et de l'emplacement.

• **Calculateur de Prix Azure** : Un outil gratuit pour estimer les coûts et planifier les budgets.

Identités et Contrôle d'Accès

• **Microsoft Entra ID** : Le service central de gestion des identités et de l'accès. Il permet de gérer les utilisateurs, les rôles, les connexions et l'accès aux ressources internes et externes (comme Office 365) via des fonctionnalités comme le Single Sign-On (SSO).

• **Contrôle d'Accès Basé sur les Rôles (Azure RBAC)** : Le système d'autorisation d'Azure qui gère les permissions d'accès aux ressources. Une attribution de rôle RBAC est composée de trois éléments :

   1. **Principal de sécurité (Security principal)** : L'identité (utilisateur, groupe, etc.) qui demande l'accès.
   

   2. **Définition de rôle (Role definition)** : Un ensemble de permissions, comme _Contributeur_ ou _Lecteur_.

   3. **Portée (Scope)** : Le niveau auquel l'accès est appliqué, qui suit une hiérarchie parent-enfant (Groupes de gestion > Abonnements > Groupes de ressources > Ressources).