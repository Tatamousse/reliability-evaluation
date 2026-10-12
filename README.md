# Reliability Evaluation Pipeline for Neural Networks

Pipeline d'évaluation de la fiabilité d'un réseau de neurones de classification
d'images : performance, robustesse, calibration, incertitude, détection
hors-distribution, et refus de prédiction.

Travail de préparation mené en amont d'un stage de fin d'études au
**Institut für Luftfahrtsysteme, Universität Stuttgart**, sur le sujet
*Practical Reliability Evaluation Pipeline for Safety-Critical Neural Networks*.

## Cadre

Le modèle évalué est un petit CNN entraîné sur **CIFAR-10**. CIFAR-10 n'est pas
une application critique pour la sécurité : il sert de substitut, choisi parce
que le benchmark de corruptions **CIFAR-10-C** existe déjà et fournit des
conditions dégradées standardisées. Le contexte opérationnel retenu et les
conditions de défaillance envisagées sont décrits dans
`docs/00_contexte_operationnel.md`.

## Étapes

- [ ] 0 — Contexte opérationnel et conditions de défaillance
- [ ] 1 — Entraînement du modèle de référence
- [ ] 2 — Performance : métriques globales et par classe, matrice de confusion
- [ ] 3 — Calibration : reliability diagram, ECE
- [ ] 4 — Calibration : temperature scaling
- [ ] 5 — Robustesse aux corruptions (CIFAR-10-C)
- [ ] 6 — Incertitude : ensembles, MC dropout
- [ ] 7 — Détection hors-distribution, AUROC
- [ ] 8 — Refus de prédiction, courbe risque-couverture
- [ ] 9 — Module réutilisable et rapport de fiabilité

## Organisation

    docs/        contexte opérationnel, critères d'acceptation, rapport
    notebooks/   exploration, un notebook par étape
    src/         module réutilisable (fonctions extraites des notebooks)
    results/     figures et tableaux produits
    data/        jeux de données (non versionnés)
    models/      poids entraînés (non versionnés)

## Installation

    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt

PyTorch en version CPU suffit pour ce projet :

    pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
