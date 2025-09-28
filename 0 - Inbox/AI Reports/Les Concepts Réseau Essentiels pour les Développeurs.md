
Ce document de synthèse examine les concepts réseau fondamentaux qui sont cruciaux pour les développeurs, afin de les aider à "level up" et à mieux comprendre le fonctionnement des applications distribuées. Il s'appuie sur le document source "Le minimum de réseau à savoir pour un Dev".

### I. Notations d'Adresses IP et Plages (CIDR)

Le document souligne l'importance pour les développeurs de comprendre les notations de plages d'adresses IP, souvent appelées CIDR (Classless Inter-Domain Routing), car elles sont utilisées pour configurer des firewalls ou des groupes de sécurité dans le cloud.

- **/32 (Adresse Unique) :** Représente une seule adresse IP. "C'est-à-dire que là 1 2 3 4/32 c'est la plage qui commence à 1 2 3 4 et qui finit à 1 2 3 4 donc elle contient juste une seule adresse". Bien que souvent omise, cette notation est parfois requise dans certains systèmes ou outils cloud.
- **/24 (256 Adresses) :** Inclut toutes les adresses IP où les trois premiers octets sont fixes et le dernier varie de 0 à 255. Par exemple, "10.0.0.0/24" couvre de 10.0.0.0 à 10.0.0.255.
- **/16 (65 536 Adresses) :** Désigne une plage où les deux premiers octets sont fixes, et les deux derniers varient. "10.0.0.0/16" s'étend de 10.0.0.0 à 10.0.255.255.
- **/8 (16 Millions d'Adresses) :** Représente toutes les adresses commençant par un octet spécifique. "10.0.0.0/8" couvre de 10.0.0.0 à 10.255.255.255. Cette plage est "assez rare qu'on l'utilise parce que ça contient 16 millions d'adresse IP".

### II. IPs Publiques vs. IPs Privées

Il est essentiel de différencier les adresses IP publiques et privées.

- **IPs Privées :** Fonctionnent uniquement au sein d'un réseau local et ne sont pas accessibles depuis Internet. "Une IP privée c'est quelque chose qui va fonctionner juste dans notre réseau local". Elles peuvent être identiques dans différents réseaux privés sans conflit.
- **Plages reconnues pour les IPs privées** :192.168.0.0/16 (souvent utilisée par les box internet) : "C'est très probablement l'adresse IP qu'à ton ordinateur ou ton téléphone en ce moment même".
- 10.0.0.0/8 (fréquente dans les réseaux d'entreprise).
- 172.16.0.0/12 (le deuxième octet varie de 16 à 31).
- **IPs Publiques :** Toute adresse IP qui n'est pas une adresse privée est publique et "peut être atteinte par l'Internet".

### III. Adresses IP Spéciales

Certaines adresses IP ont des usages spécifiques :

- **127.0.0.1 (Localhost) :** L'adresse de bouclage, interne à la machine elle-même, utilisée pour la communication entre processus sur la même machine. "Toutes les machines que ce soit un téléphone un ordi un serveur il a une adresse IP qui est 127.0.0.1". D'autres adresses dans la plage 127.0.0.0/8 fonctionnent de la même manière.
- **169.254.0.0/16 (APIPA / Link-Local) :** Adresse auto-attribuée par un ordinateur s'il ne peut pas obtenir d'adresse IP via un serveur DHCP (par exemple, si le câble est débranché ou le routeur défaillant). "Si ton ordi ou ton serveur il a adresse IP 169.254 c'est probablement qu'il a pas accès à internet et qu'il a pas accès au réseau".
- **100.64.0.0/10 (CGNAT - Carrier Grade NAT) :** Utilisée pour le partage d'adresses IP publiques par les opérateurs (par exemple, pour le "tethering" mobile ou via un VPN).

### IV. Le Système de Noms de Domaine (DNS)

Le DNS est crucial pour traduire les noms de domaine lisibles par l'homme en adresses IP que les machines peuvent comprendre.

- **Fonctionnement :** Un serveur DNS répond à la question "à quelle adresse IP ce nom de domaine correspond-il ?". "Les noms de domaines c'est vraiment juste pour nous les humains pouvoir facilement se souvenir de google.com".
- **Processus de Résolution :** Lorsqu'une machine demande l'IP d'un domaine, le routeur local peut avoir la réponse en cache ou interroger d'autres serveurs DNS (serveurs racines, TLD, puis serveurs autoritaires) jusqu'à obtenir l'adresse IP.
- **Types d'enregistrements DNS courants :A (Address) :** Mappe un nom de domaine à une adresse IPv4. "C'est quoi serve.com serveur.com = 1.2.3.4".
- **AAAA (Quad-A) :** Mappe un nom de domaine à une adresse IPv6.
- **CNAME (Canonical Name) :** Crée un alias, faisant pointer un nom de domaine vers un autre nom de domaine. "Un nom de domaine et ben en fait il va pointer vers un autre nom de domaine".
- **MX (Mail Exchange) :** Spécifie les serveurs de messagerie responsables de recevoir les e-mails pour un domaine.
- **TXT (Text) :** Enregistrement polyvalent pour stocker du texte arbitraire, souvent utilisé pour la vérification de domaine (ex: SSL/TLS challenges) et la prévention du spam (DKIM, DMARC, SPF).

### V. Protocoles de Transport : TCP vs. UDP

Comprendre les protocoles de transport est vital pour le débogage et l'optimisation des applications.

- **TCP (Transmission Control Protocol) :**
- **Fiable :** Assure la livraison ordonnée et sans erreur des paquets, avec des mécanismes de retransmission. "TCP qui est le plus fiable et qui est le plus utilisé".
- **Utilisation :** HTTP, SSH, FTP, POP, IMAP – tout ce qui nécessite une intégrité des données (ex: transfert de fichiers).
- **Overhead :** Plus important en raison des informations supplémentaires pour garantir la fiabilité (headers de 20 à 60 octets).
- **UDP (User Datagram Protocol)**
- **Rapide / Orienté Latence** :Moins de contrôle d'erreurs et pas de garantie de livraison ni d'ordre. "UDP qui lui va plus être optimisé pour la rapidité pour la latence".
- **Utilisation :** Voix sur IP (VoIP), jeux en ligne, DNS – où la rapidité est plus critique que la perte occasionnelle de paquets.
- **Overhead :** Minimal, ce qui le rend efficace pour de petites requêtes.

### VI. Protocole ICMP (Internet Control Message Protocol)

- **Diagnostic :** Utilisé principalement pour des fonctions de diagnostic du réseau, comme l'outil ping. "ICMP c'est le protocole du PIN".
- **Attention :** Le fait de pouvoir ping une machine ne signifie pas qu'on peut y accéder via d'autres protocoles comme HTTP, car ils opèrent à des niveaux différents.

### VII. Ports Réseau

- **Fonction :** Les ports, de 1 à 65535, identifient des applications ou services spécifiques sur une machine.
- **Ports Réservés (0-1023) :** "Les 1000 premiers ils sont réservés", nécessitant des privilèges root sur les systèmes Linux (ex: 80 pour HTTP, 22 pour SSH, 53 pour DNS).
- **Ports Non Réservés (1024-65535) :** N'importe quelle application peut les utiliser.
- **Importance :** Les développeurs doivent comprendre les ports pour configurer la communication entre différents services (backend/API, frontend/backend, load balancer).

### VIII. Le Protocole HTTP (Hypertext Transfer Protocol)

Le protocole HTTP est fondamental pour le développement web et API.

- **Fonctionnement :** Une requête HTTP inclut un verbe (GET, POST, etc.), une ressource (ex: /), une version du protocole (HTTP/1.1), et un entête Host spécifiant le site web désiré.
- **Entête Host :** Essentiel car le serveur se connecte à une adresse IP et a besoin du Host pour savoir quel site web servir, surtout s'il héberge plusieurs domaines. "Le paquet que je vais envoyer à aucun moment le serveur de Google il sait que je veux google.com".
- **Codes de Réponse :** Le serveur répond avec un code d'état (ex: 200 OK pour succès, 301 Moved Permanently pour une redirection permanente).
- **Redirections HTTP (ex: 301) :** Elles demandent au navigateur de faire une nouvelle requête vers une autre URL. Il est crucial de ne pas les confondre avec les enregistrements CNAME du DNS, qui sont des redirections au niveau DNS (résolution IP).

### IX. HTTPS et Certificats SSL/TLS

Le HTTPS est la version sécurisée de HTTP.

- **Principe :** HTTP est encapsulé dans une couche chiffrée (TLS, anciennement SSL) pour sécuriser la communication sur un réseau potentiellement non sécurisé.
- **Objectifs :Chiffrement :** Empêche l'interception et la lecture des données par des tiers.
- **Authentification :** Garantit que le client communique avec le serveur légitime. Les certificats, émis par des autorités de certification (CA), confirment la propriété du nom de domaine par le serveur. "Je suis sûr de communiquer avec la bonne personne quand je vois le petit cadel".
- **SSL/TLS Offloading :** Une pratique courante avec les load balancers où le load balancer gère le chiffrement HTTPS (possède le certificat), et la communication entre le load balancer et les serveurs web backend se fait en HTTP non chiffré, car elle est interne au réseau privé. Cela réduit la charge sur les serveurs backend.

### X. Load Balancers (Équilibreurs de Charge / Reverse Proxies)

Les load balancers sont des composants réseau qui distribuent les requêtes entrantes entre plusieurs serveurs pour améliorer la disponibilité et la performance.

- **Rôle :** Ils sont le point d'entrée public vers un groupe de serveurs qui résident dans un réseau privé. "Notre nom de domaines pointent vers notre balanceur notre utilisateur envoie notre quête HTTP à notre lo balanceur et notre balanceur lui il va pouvoir choisir sur quel serveur ou quel groupe de serveur il va envoyer notre quête".
- **Types :Load Balancers de Niveau 4 (NLB) :** Opèrent au niveau de la couche transport (TCP/UDP). Ils inspectent des informations basiques comme l'adresse IP et le port source/destination.
- **Avantages :** Très performants et simples, car ils n'inspectent qu'une petite partie du paquet.
- **Load Balancers de Niveau 7 (ALB / Smart Load Balancers) :** Opèrent au niveau de la couche applicative (HTTP). Ils inspectent le contenu de la requête HTTP (verbe, ressource, et surtout l'entête Host).
- **Avantages :** Permettent des règles de routage intelligentes basées sur le nom de domaine, l'URL, etc., et peuvent gérer le SSL offloading.
- **Inconvénients :** Légèrement plus lents que les NLB en raison de l'inspection plus approfondie des paquets, mais "un lo balancer de niveau 7 c'est quand même 100 fois plus rapide que un serveur web à répondre".

### XI. Outils de Débogage Réseau

Le document mentionne plusieurs outils essentiels pour le diagnostic réseau :

- **DNS :NS Lookup :** Pour résoudre les noms de domaine en adresses IP.
- **Dig** : Similaire à NS Lookup, mais avec une syntaxe différente.
- **TCP/Général :Netstat** : Affiche les connexions réseau, les tables de routage, les statistiques d'interface. "Netstat T [...] pour pouvoir lui dire affiche-moi les connexions TCP seulement".
- **SS** : Outil similaire à Netstat.
- **Ping** : Teste la connectivité de base (niveau ICMP) entre deux machines.
- **Traceroute (Tracert sur Windows, Trf sur Linux, Traceroute sur Mac/Linux)** : Trace le chemin qu'un paquet prend pour atteindre une destination.
- **Telnet** : Client TCP générique permettant d'établir des connexions et de communiquer manuellement avec des services via leurs protocoles applicatifs (HTTP, FTP, mail).
- **Netcat** : Similaire à Telnet.
- **TCPDump** : Outil avancé pour capturer et analyser le trafic réseau.
- **HTTP :Curl** : Client HTTP en ligne de commande pour envoyer des requêtes HTTP/HTTPS et examiner les réponses. Très utile pour le débogage HTTP. "Curl c'est un client http il va se connecter il va faire la requête DNS il va se connecter à.com".
- **Wget** : Similaire à Curl, pour télécharger des fichiers depuis le web.

