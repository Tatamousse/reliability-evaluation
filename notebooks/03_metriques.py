"""Bloc 2 - metriques par classe et matrice de confusion sur le jeu de test."""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
import torchvision
import torchvision.transforms as T
from sklearn.metrics import classification_report, confusion_matrix
from torch.utils.data import DataLoader

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from src.reliability.modele import PetitCNN

DATA, MODELS, RESULTS = RACINE / "data", RACINE / "models", RACINE / "results"

CLASSES = ["avion", "automobile", "oiseau", "chat", "cerf",
           "chien", "grenouille", "cheval", "bateau", "camion"]

transfo = T.Compose([
    T.ToTensor(),
    T.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)),
])

test = torchvision.datasets.CIFAR10(root=DATA, train=False, transform=transfo)
charge = DataLoader(test, batch_size=256)

modele = PetitCNN()
modele.load_state_dict(torch.load(MODELS / "cnn_reference.pth", map_location="cpu"))
modele.eval()

vrais, predits = [], []
with torch.no_grad():
    for x, y in charge:
        predits.append(modele(x).argmax(1))
        vrais.append(y)
vrais = torch.cat(vrais).numpy()
predits = torch.cat(predits).numpy()

print(f"Accuracy globale : {(vrais == predits).mean():.4f}\n")
print(classification_report(vrais, predits, target_names=CLASSES, digits=3))

mat = confusion_matrix(vrais, predits)
print("Matrice de confusion (lignes = vraie classe, colonnes = prediction)\n")
print(" " * 14 + "".join(f"{c[:6]:>8}" for c in CLASSES))
for i, c in enumerate(CLASSES):
    print(f"{c:<14}" + "".join(f"{v:>8}" for v in mat[i]))

hors_diag = [(mat[i, j], CLASSES[i], CLASSES[j])
             for i in range(10) for j in range(10) if i != j]
hors_diag.sort(reverse=True)
print("\nCinq confusions les plus frequentes :")
for n, vrai, pred in hors_diag[:5]:
    print(f"  {n:>4}  vrai {vrai} -> predit {pred}")

print("\nCas critique du contexte operationnel :")
i, j = CLASSES.index("avion"), CLASSES.index("oiseau")
print(f"  vrai avion  -> predit oiseau : {mat[i, j]:>3} / 1000  ({mat[i, j]/10:.1f} %)")
print(f"  vrai oiseau -> predit avion  : {mat[j, i]:>3} / 1000  ({mat[j, i]/10:.1f} %)")

norm = mat / mat.sum(axis=1, keepdims=True)
fig, ax = plt.subplots(figsize=(8, 7))
im = ax.imshow(norm, cmap="Blues", vmin=0, vmax=1)
ax.set_xticks(range(10)); ax.set_xticklabels(CLASSES, rotation=45, ha="right")
ax.set_yticks(range(10)); ax.set_yticklabels(CLASSES)
ax.set_xlabel("classe predite"); ax.set_ylabel("vraie classe")
ax.set_title("Matrice de confusion normalisee par ligne (= rappels)")
for a in range(10):
    for b in range(10):
        ax.text(b, a, f"{norm[a, b]:.2f}", ha="center", va="center",
                fontsize=7, color="white" if norm[a, b] > 0.5 else "black")
fig.colorbar(im)
fig.tight_layout()
RESULTS.mkdir(exist_ok=True)
fig.savefig(RESULTS / "03_matrice_confusion.png", dpi=130)
print(f"\nFigure : {RESULTS / '03_matrice_confusion.png'}")
