"""Bloc 1c - entrainement du CNN de reference."""

import sys
import time
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as T
from torch.utils.data import DataLoader, random_split

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE))
from src.reliability.modele import PetitCNN

DATA, MODELS, RESULTS = RACINE / "data", RACINE / "models", RACINE / "results"

EPOQUES, LOT, PAS, GRAINE = 15, 128, 1e-3, 0
torch.manual_seed(GRAINE)

# statistiques par canal de CIFAR-10 : on centre et on reduit
transfo = T.Compose([
    T.ToTensor(),
    T.Normalize((0.4914, 0.4822, 0.4465), (0.2470, 0.2435, 0.2616)),
])

complet = torchvision.datasets.CIFAR10(root=DATA, train=True, transform=transfo)

# 5000 images mises de cote pour la validation. Le jeu de TEST n'est pas
# charge ici : on n'y touche pas avant la seance 2.
entrainement, validation = random_split(
    complet, [45000, 5000], generator=torch.Generator().manual_seed(GRAINE)
)
charge_tr = DataLoader(entrainement, batch_size=LOT, shuffle=True)
charge_val = DataLoader(validation, batch_size=LOT)

modele = PetitCNN()
cout = nn.CrossEntropyLoss()
optimiseur = torch.optim.Adam(modele.parameters(), lr=PAS)


def evaluer(charge):
    modele.eval()
    perte, justes, n = 0.0, 0, 0
    with torch.no_grad():
        for x, y in charge:
            scores = modele(x)
            perte += cout(scores, y).item() * y.size(0)
            justes += (scores.argmax(1) == y).sum().item()
            n += y.size(0)
    return perte / n, justes / n


depart = time.time()
historique = []
for epoque in range(1, EPOQUES + 1):
    modele.train()
    perte_tr, n = 0.0, 0
    for x, y in charge_tr:
        optimiseur.zero_grad()
        perte = cout(modele(x), y)
        perte.backward()
        optimiseur.step()
        perte_tr += perte.item() * y.size(0)
        n += y.size(0)
    perte_tr /= n
    perte_val, acc_val = evaluer(charge_val)
    historique.append((epoque, perte_tr, perte_val, acc_val))
    print(f"epoque {epoque:2d}  perte_tr {perte_tr:.4f}  "
          f"perte_val {perte_val:.4f}  acc_val {acc_val:.4f}  "
          f"[{time.time() - depart:.0f}s]", flush=True)

MODELS.mkdir(exist_ok=True)
torch.save(modele.state_dict(), MODELS / "cnn_reference.pth")

ep = [h[0] for h in historique]
fig, (g, d) = plt.subplots(1, 2, figsize=(11, 4))
g.plot(ep, [h[1] for h in historique], label="entrainement")
g.plot(ep, [h[2] for h in historique], label="validation")
g.set_xlabel("epoque"); g.set_ylabel("perte"); g.legend(); g.set_title("Perte")
d.plot(ep, [h[3] for h in historique])
d.set_xlabel("epoque"); d.set_ylabel("accuracy"); d.set_title("Accuracy validation")
fig.tight_layout()
RESULTS.mkdir(exist_ok=True)
fig.savefig(RESULTS / "02_courbes_entrainement.png", dpi=120)

print(f"\nModele  : {MODELS / 'cnn_reference.pth'}")
print(f"Courbes : {RESULTS / '02_courbes_entrainement.png'}")
