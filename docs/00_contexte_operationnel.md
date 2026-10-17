# Contexte opérationnel et conditions de défaillance

## 1. Tâche visée

Classification d'images embarquée : identifier la nature de l'objet présent dans
l'image captée par la caméra du drone, parmi dix catégories.

Contexte retenu : **surveillance de l'espace aérien**. La sortie du modèle
alimente un système d'évitement, avec un opérateur en mesure de valider ou
d'écarter l'alerte.

Le modèle ne porte pas l'objectif opérationnel : il produit une distribution de
probabilité sur les classes, et c'est le système autour de lui qui décide d'une
alarme, d'un enregistrement ou d'une manœuvre. C'est précisément pour cela que
le contexte doit être énoncé explicitement : les mêmes performances n'ont pas
la même valeur selon l'usage.

## 2. Données

CIFAR-10 : 50 000 images d'entraînement, 10 000 de test, 32x32 pixels en
couleur, dix classes exactement équilibrées (1 000 images de test par classe).

CIFAR-10 n'est pas une application critique pour la sécurité. Il est retenu
comme substitut pour deux raisons. D'abord, le benchmark de corruptions
CIFAR-10-C existe déjà et fournit des conditions dégradées standardisées et
reproductibles. Ensuite, la faible résolution présente une difficulté
comparable à celle de l'observation aérienne distante, où la cible n'occupe que
peu de pixels.

## 3. Conditions de défaillance plausibles

Énumérées en suivant la chaîne physique entre la scène observée et l'entrée du
modèle :

- **scène** : lumière (survol à midi, surexposition ; au coucher du soleil,
  dérive colorimétrique ; de nuit, sous-exposition), angle de vue, occlusion
- **air traversé** : brouillard, pluie, neige, brume de chaleur
- **optique** : flou de mouvement (le drone avance et vibre), mise au point
  ratée
- **capteur** : bruit électronique en basse lumière
- **transmission** : compression de la vidéo pour la liaison radio,
  pixellisation

Cinq corruptions sont retenues pour le benchmark, une par maillon de la chaîne :
`brightness`, `fog`, `motion_blur`, `gaussian_noise`, `jpeg_compression`.
À cinq niveaux de sévérité chacune, cela donne 25 conditions dégradées,
auxquelles s'ajoute la condition nominale.

**Limite connue du benchmark** : CIFAR-10-C ne contient aucune occlusion. Cet
axe de défaillance reste non couvert et doit être signalé comme tel dans le
rapport de fiabilité.

## 4. Coût des erreurs

Toutes les confusions n'ont pas le même coût, et l'accuracy globale les traite
à l'identique.

**Paire critique : vrai avion prédit comme oiseau.** Un aéronef pris pour un
oiseau, c'est un évitement qui n'a pas lieu. La confusion est asymétrique :
dans l'autre sens, un oiseau pris pour un avion ne produit qu'une manœuvre
inutile. Même paire de classes, deux cases distinctes de la matrice de
confusion, deux conséquences incomparables.

Le critère d'acceptation portera donc sur une case de la matrice, et non sur
l'accuracy globale.

**Paires sans conséquence dans ce contexte : chat / chien, cheval / cerf.** Ces
confusions n'affectent aucune décision d'évitement. Elles seraient en revanche
déterminantes dans un autre contexte — un drone de recensement de faune — ce
qui illustre que le coût d'une erreur est une propriété du contexte
opérationnel et non du modèle.
