"""Bloc 1a - chargement de CIFAR-10 et verification du jeu de donnees."""

from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")          # pas d'affichage : on ecrit un fichier
import matplotlib.pyplot as plt
import torchvision

RACINE = Path(__file__).resolve().parents[1]
DATA = RACINE / "data"
RESULTS = RACINE / "results"

CLASSES = ["avion", "automobile", "oiseau", "chat", "cerf",
           "chien", "grenouille", "cheval", "bateau", "camion"]

train = torchvision.datasets.CIFAR10(root=DATA, train=True, download=True)
test = torchvision.datasets.CIFAR10(root=DATA, train=False, download=True)

print(f"Entrainement : {len(train)} images")
print(f"Test         : {len(test)} images")
print(f"Une image    : {train[0][0].size} pixels, mode {train[0][0].mode}")
print()

for nom, jeu in [("entrainement", train), ("test", test)]:
    compte = Counter(jeu.targets)
    print(f"Repartition {nom} :")
    for i, classe in enumerate(CLASSES):
        print(f"  {classe:<12} {compte[i]}")
    print()

fig, axes = plt.subplots(5, 5, figsize=(8, 8))
for ax, (image, cible) in zip(axes.ravel(), test):
    ax.imshow(image)
    ax.set_title(CLASSES[cible], fontsize=9)
    ax.axis("off")
fig.suptitle("CIFAR-10 - 25 premieres images du jeu de test", fontsize=12)
fig.tight_layout()
RESULTS.mkdir(exist_ok=True)
chemin = RESULTS / "01_echantillon_cifar10.png"
fig.savefig(chemin, dpi=120)
print(f"Figure ecrite : {chemin}")
