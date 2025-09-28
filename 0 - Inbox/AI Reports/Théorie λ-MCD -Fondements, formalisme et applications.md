## Historique et origines de la théorie des fonctions de croyance

La **théorie des fonctions de croyance**, également appelée théorie de l’évidence ou théorie de Dempster-Shafer (DST), a été développée dans les années 1960-1970 par Arthur P. **Dempster** et Glenn **Shafer**[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=La%20th%C3%A9orie%20de%20Dempster,croyances%20ou%20th%C3%A9orie%20de%20l%E2%80%99%C3%A9vidence). Dempster introduit initialement le concept pour formuler une généralisation de l’inférence bayésienne, en particulier pour combiner des informations partiellement fiables issues de sources multiples[en.wikipedia.org](https://en.wikipedia.org/wiki/Dempster%E2%80%93Shafer_theory#:~:text=uncertainty%2C%20with%20understood%20connections%20to,account%20all%20the%20available%20evidence). Shafer formalise ensuite cette approche dans _A Mathematical Theory of Evidence_ (1976), établissant un cadre mathématique général pour modéliser l’incertitude épistémique à partir de **fonctions de croyance** plutôt que de probabilités ponctuelles[en.wikipedia.org](https://en.wikipedia.org/wiki/Dempster%E2%80%93Shafer_theory#:~:text=match%20at%20L152%20statistical%20inference%2C,represented%20by%20a). Cette théorie permet notamment de fusionner des **preuves** provenant de sources distinctes et d’obtenir des degrés de croyance quantifiant le soutien en faveur de certaines hypothèses, tout en conservant explicitement la part d’**ignorance** due à l’information incomplète

Au cours des décennies suivantes, la théorie de Dempster-Shafer a suscité de nombreux développements. En particulier, Philippe **Smets** a proposé le **modèle des croyances transférables** (Transferable Belief Model, TBM) comme réponse à certaines limites de l’approche classique[en.wikipedia.org](https://en.wikipedia.org/wiki/Transferable_belief_model#:~:text=probability%20%20that%20a%20given,56%20in%20a%20hypothesis). Smets introduit l’**hypothèse de monde ouvert**, dans laquelle on admet que le vrai état du système peut éventuellement échapper au cadre de discernement envisagé. Concrètement, la règle de combinaison de Dempster n’y est plus normalisée : toute masse de croyance contradictoire est attribuée à l’ensemble vide plutôt que d’être ignorée [en.wikipedia.org](https://en.wikipedia.org/wiki/Transferable_belief_model#:~:text=proposed%20his%20approach%20as%20a,DST%20and%20also%20%2059). La masse ainsi allouée à ∅ représente le **conflit** non résolu ou l’issue « inattendue » se situant hors du cadre supposé [en.wikipedia.org](https://en.wikipedia.org/wiki/Transferable_belief_model#:~:text=proposed%20his%20approach%20as%20a,DST%20and%20also%20%2059). Cette adaptation permet de mieux gérer les cas de forte contradiction entre sources (illustré par le paradoxe de Zadeh) au prix d’une violation de l’hypothèse classique de totalité des probabilités. Par ailleurs, Smets distingue deux niveaux de raisonnement : le **niveau crédal**, où les croyances sont manipulées via des fonctions de croyance, et le **niveau pignistique**, où une distribution de probabilité dite _pignistique_ est construite à partir des croyances pour la prise de **décision**[en.wikipedia.org](https://en.wikipedia.org/wiki/Transferable_belief_model#:~:text=1,are%20quantified%20by%20probability%20functions). Ce passage au niveau pignistique – par la **transformation pignistique** – permet d’appliquer les critères décisionnels classiques (par exemple le calcul d’espérance d’utilité) malgré l’incertitude modélisée au niveau crédal[en.wikipedia.org](https://en.wikipedia.org/wiki/Transferable_belief_model#:~:text=1,are%20quantified%20by%20probability%20functions).

En résumé, la théorie des fonctions de croyance s’est imposée comme un cadre flexible de représentation et de combinaison de l’incertitude en intelligence artificielle. Elle généralise la théorie bayésienne en autorisant l’affectation de poids non seulement aux simples événements atomiques mais aussi à des sous-ensembles d’hypothèses, rendant possible l’expression du doute et de l’ignorance de façon explicite [en.wikipedia.org](https://en.wikipedia.org/wiki/Dempster%E2%80%93Shafer_theory#:~:text=Dempster%E2%80%93Shafer%20theory%20is%20a%20generalization,may%20not%20have%20the%20mathematical)[en.wikipedia.org](https://en.wikipedia.org/wiki/Dempster%E2%80%93Shafer_theory#:~:text=Often%20used%20as%20a%20method,In). Les contributions fondatrices de Dempster, Shafer et Smets constituent le socle historique sur lequel ont émergé de nombreux raffinements et règles de combinaison alternatives (règle de Yager, règle disjonctive de Dubois & Prade, règles de redistribution de conflit, etc.), motivés par le besoin de mieux gérer les conflits et les dépendances entre sources [en.wikipedia.org](https://en.wikipedia.org/wiki/Dempster%E2%80%93Shafer_theory#:~:text=In%20a%20narrow%20sense%2C%20the,6).

## Fondements mathématiques de la théorie λ-MCD

### Définitions formelles : cadre de discernement, masses et croyances

Soit $Ω$ un **univers de discours** (ou _cadre de discernement_) fini représentant l’ensemble des $n$ hypothèses élémentaires mutuellement exclusives sur lesquelles portent nos informations. On note $2^Ω$ l’ensemble de toutes les parties de $Ω$. Chaque élément $A \subseteq Ω$ peut être interprété comme une **proposition** : $A$ représente l’hypothèse « _l’état du monde réel appartient à $A$_ ». En particulier, $Ω$ lui-même signifie « aucune information (ignorance totale) » et l’ensemble vide $\varnothing$ représente l’hypothèse impossible.

Une **fonction de masse** (ou **Basic Belief Assignment**, BBA) est une application $m: 2^Ω \to [0,1]$ qui distribue une unité de masse de croyance sur les sous-ensembles de $Ω$ en respectant les axiomes suivants[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=,vide%20est%200) :

- $m(\varnothing) = 0$ (pour un **monde fermé**, aucune masse n’est initialement allouée à l’hypothèse vide)[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=,vide%20est%200). Dans le modèle de Smets (monde ouvert), on autorise éventuellement $m(\varnothing) > 0$ pour représenter du **conflit non résolu** ou l’éventualité d’une issue non envisagée[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=La%20r%C3%A8gle%20de%20combinaison%20de,alternative%20pour%20les%20mondes%20ouverts). Dans la suite, nous noterons $k = m(\varnothing)$ le **degré de conflit** (ou d’ignorance totale) éventuel.
    
- $\displaystyle \sum_{A \subseteq Ω} m(A) = 1$ (la somme de toutes les masses vaut 1)[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=,vide%20est%200). Ainsi, on répartit la croyance totale sur l’ensemble des propositions d’intérêt.
    

Chaque sous-ensemble $A \subseteq Ω$ tel que $m(A) > 0$ est appelé un **élément focal** de $m$. La valeur $m(A)$ quantifie exactement le **degré de croyance pur** accordé à la proposition $A$ _et à aucune autre plus spécifique_[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=La%20masse%20Image%3A%20,n%E2%80%99apporte%20aucun%20cr%C3%A9dit%20aux%20sous). Intuitivement, $m(A)$ représente la part de l’évidence qui **supporte précisément $A$** (et pas strictement un de ses sous-ensembles). Une fonction de masse $m$ telle que $m(Ω)=1$ est dite _vacuous_ (ignorance totale), tandis qu’une masse _bayésienne_ est un cas particulier où tous les éléments focaux sont des singletons (on retrouve alors une distribution de probabilité classique)[lgi2a.univ-artois.fr](https://www.lgi2a.univ-artois.fr/~lefevre/HDR.pdf#:~:text=D%C3%A9finition%204%20,Une%20fonction%20de%20masse%20m).

À une fonction de masse $m$ sont associées deux mesures dérivées clés : la **fonction de croyance** $bel$ et la **fonction de plausibilité** $pl$. Pour tout $A \subseteq Ω$ :

- La _croyance_ $bel(A)$ (ou **crédibilité** de $A$) est la somme de toutes les masses focales qui _soutiennent entièrement $A$_, c’est-à-dire portées par des sous-ensembles de $A$[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=La%20croyance%20Image%3A%20,ensembles%20%28pas%20n%C3%A9cessairement%20propres%29). Formellement :
    
$$bel(A)=∑_{B⊆A}m(B):contentReference[oaicite:19]index=19.$$

* La _plausibilité_ $pl(A)$, quant à elle, représente le _degré de non-contradiction_ de l’hypothèse $A$ vis-à-vis de l’évidence disponible. Elle s’obtient en sommant les masses de tous les focales $B$ qui **peuvent coexister** avec $A$ (c’est-à-dire qui ont une intersection non vide avec $A$)[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=La%20plausibilit%C3%A9%20Image%3A%20,displaystyle%20A) :

$$pl(A)=∑_{B∩A≠∅}m(B):contentReference[oaicite:21]index=21.$$

Ces deux quantités encadrent la probabilité _a posteriori_ de $A$ si l’on voulait la déduire des croyances : pour toute distribution de probabilité $P$ cohérente avec $m$, on a $bel(A) \le P(A) \le pl(A)$[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=%C3%80%20partir%20de%20la%20valeur,mesures%20appel%C3%A9es%20croyance%20et%20plausibilit%C3%A9). De plus, croyance et plausibilité sont liées par la relation duale :

$$pl(A)=1−bel(\overline{A}):contentReference[oaicite:23]index=23,$$ 

où $\overline{A} = Ω \setminus A$ est le complément de $A$. Cette identité découle du fait que les focales qui ne touchent pas $A$ (et donc qui contribuent à $bel(\overline{A})$) sont exactement celles dont l’absence assure implicitement la plausibilité de $A$. À partir de $m$, on peut calculer $bel$ et $pl$ via les formules ci-dessus, et réciproquement reconstruire $m$ à partir de $bel$ ou $pl$ (par inversion de la transformée de Möbius). En pratique, $bel(A)$ quantifie la _confiance minimale_ en $A$ (support certain), tandis que $pl(A)$ en donne la _confiance maximale_ possible (support potentiel). On a toujours $0 \le bel(A) \le pl(A) \le 1$ pour tout $A$, et en particulier $bel(Ω)=pl(Ω)=1$ et $bel(\varnothing)=pl(\varnothing)=0$.

**Exemple illustratif** : Considérons un univers $Ω={ω_1,ω_2}$ de deux hypothèses possibles (e.g. « signal présent » $ω_1$ ou « signal absent » $ω_2$). Supposons une source d’information nous donnant $m({ω_1})=0.6$, $m(Ω)=0.4$, et $m$ nul ailleurs. Cela signifie qu’on accorde 60% de croyance directement à $ω_1$ et 40% à l’ignorance totale $Ω$. Alors $bel({ω_1}) = 0.6$ (c’est la seule focale incluse dans ${ω_1}$) et $pl({ω_1}) = m({ω_1}) + m(Ω) = 1.0$, car même la masse d’ignorance ne contredit pas $ω_1$. Ici l’intervalle de probabilité possible pour ${ω_1}$ est $[0.6,;1.0]$. De même $bel({ω_2})=0$ (aucune masse dédiée uniquement à $ω_2$) mais $pl({ω_2}) = 0.4$, reflétant que seule la portion non engagée de l’évidence rend $ω_2$ plausible. Naturellement $pl({ω_2}) = 1 - bel({ω_1}) = 0.4$, conformément à la relation duale.

### Règles de combinaison des croyances

Un apport central de Dempster fut de définir une règle de **combinaison de deux fonctions de masse** $m_1$ et $m_2$ provenant de sources **indépendantes**, dans le but de synthétiser l’évidence totale. La _règle de Dempster_ (aussi appelée **conjonction avec normalisation** ou règle orthogonale) s’obtient en affectant de la masse aux intersections des focales des deux sources[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=Image%3A%20). Pour tout $A \subseteq Ω$ non vide :

$$m12​(A)=(m1​⊕m2​)(A)=1/1−K​​∑_{B∩C-A}​m_1​(B)m_2​(C):contentReference[oaicite:25]index=25,$$

où la somme parcourt tous les couples de focales $B$ de $m_1$ et $C$ de $m_2$ qui _s’intersectent exactement_ en $A$. Le coefficient $K$ désigne la **masse de conflit** :


$$K=​∑_{B∩C=∅}​m_1​(B)m_2​(C):contentReference[oaicite:26]index=26.$$

Autrement dit, $K$ est la somme des produits de masses correspondant à des focales **incompatibles** (disjointes) entre les deux sources. Si $K>0$, cela signifie que les deux sources sont en désaccord sur certaines hypothèses. Le facteur de **normalisation** $1-K$ dans la formule de Dempster permet de re-redistribuer proportionnellement la masse conflictuelle sur les autres ensembles, garantissant ainsi que le résultat combiné $m_{12}$ reste un BBA valide (qui satisfait $\sum m_{12}=1$)[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=o%C3%B9). L’effet de cette normalisation est d’**ignorer** purement le conflit en le reportant sur des hypothèses plus larges ; cela peut conduire à des résultats contre-intuitifs lorsque $K$ est grand (fort désaccord entre sources)[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=Image%3A%20,conflits%20significatifs%2C%20dans%20certains%20contextes). En pratique, la règle de Dempster est justifiée lorsque l’on suppose que **toutes les sources sont fiables et cohérentes**, et que le **monde est fermé** (toutes les issues possibles sont dans $Ω$)[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=Image%3A%20,conflits%20significatifs%2C%20dans%20certains%20contextes).

Plusieurs variantes de combinaison ont été proposées pour assouplir ces hypothèses. Par exemple, la **règle conjonctive non normalisée** (ou combinaison de **conjonction pure**) consiste à appliquer la même formule de combinaison **sans** le facteur $(1-K)$[fr.wikipedia.org](https://fr.wikipedia.org/wiki/Th%C3%A9orie_de_Dempster-Shafer#:~:text=La%20r%C3%A8gle%20de%20combinaison%20de,alternative%20pour%20les%20mondes%20ouverts). On obtient alors :

$$m1∩2​(A)=∑​_{B∩C=A​}m1​(B)m2​(C),m_{1∩2}​(∅)=K:contentReference[oaicite:31]index=31.$$


























