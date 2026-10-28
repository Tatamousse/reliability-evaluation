# Critères d'acceptation

## Principe

L'exigence est **allouée selon la criticité**, et non uniformément sur les dix
classes. Le contexte opérationnel retenu — surveillance de l'espace aérien, la
sortie alimentant un système d'évitement — détermine quelles classes comptent.

| Niveau | Classes | Justification |
|---|---|---|
| Critique | avion | Seul objet des dix avec lequel une collision est possible |
| Secondaire | oiseau | Non pas son rappel : le confondre avec un avion déclenche des manœuvres inutiles, dont le coût est la charge de l'opérateur et son désintérêt progressif pour les alertes |
| Non critique | les huit autres | Aucune collision possible ; aucun seuil, et cette absence est un choix documenté, non un oubli |

## Critères

| | Critère | Seuil provisoire | Mesuré | Verdict |
|---|---|---|---|---|
| C1 | Rappel de la classe `avion` | ≥ 90 % | 82,5 % | **échec** |
| C2 | Taux `vrai avion → prédit oiseau` | ≤ 1 % | 2,6 % | **échec** |
| C3 | P(avion→oiseau) < P(oiseau→avion) | — | 2,6 % < 7,2 % | **satisfait** |

C3 exige que le biais du modèle reste du côté sûr : sur-déclarer « avion »
produit des manœuvres inutiles, le sous-déclarer produit des collisions
manquées. Cette asymétrie est aujourd'hui favorable, mais **elle n'a pas été
conçue** : elle est le produit d'un entraînement particulier et pourrait
s'inverser au prochain réentraînement sans qu'aucune alerte ne le signale.
D'où sa présence comme critère explicite.

L'accuracy globale (78,74 %) n'est volontairement pas un critère. Elle masque
une plage de rappels allant de 62,2 % (chat) à 89,3 % (bateau), soit 27 points
d'écart, et traite toutes les confusions comme équivalentes.

## Limite de ces seuils

Les valeurs de C1 et C2 sont **provisoires et non dérivées**. Les seuils réels
se déduisent d'une exigence système — un taux d'événement dangereux jugé
acceptable — répartie entre les éléments qui contribuent à la fonction
d'évitement : capteurs, modèle, opérateur. Cette exigence n'était pas
disponible dans le cadre de ce travail préparatoire.

Deux facteurs la rendraient probablement moins stricte que les seuils ci-dessus :

- Les taux mesurés sont **par image**, alors que la caméra observe une même
  cible sur de nombreuses images successives. Ces observations ne sont pas
  indépendantes, donc leurs probabilités ne se multiplient pas, mais le système
  dispose de plusieurs regards là où le critère n'en compte qu'un.
- Le modèle n'est pas seul : un opérateur et d'éventuels autres capteurs
  portent une part de l'exigence.

## Conséquence

Le modèle **échoue** sur deux des trois critères. Ce résultat est l'objet du
travail : des critères qui valident par construction le modèle déjà fabriqué ne
mesurent rien.
