"""Bloc 1b - definition du CNN de reference et comptage des parametres."""

import torch
import torch.nn as nn


class PetitCNN(nn.Module):
    """Trois blocs de convolution, puis deux couches denses."""

    def __init__(self, n_classes=10):
        super().__init__()
        self.extraction = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),    # 32 x 32 x 32
            nn.ReLU(),
            nn.MaxPool2d(2),                               # 32 x 16 x 16
            nn.Conv2d(32, 64, kernel_size=3, padding=1),   # 64 x 16 x 16
            nn.ReLU(),
            nn.MaxPool2d(2),                               # 64 x  8 x  8
            nn.Conv2d(64, 128, kernel_size=3, padding=1),  # 128 x  8 x  8
            nn.ReLU(),
            nn.MaxPool2d(2),                               # 128 x  4 x  4
        )
        self.classification = nn.Sequential(
            nn.Flatten(),                                  # 2048
            nn.Dropout(0.5),
            nn.Linear(128 * 4 * 4, 256),
            nn.ReLU(),
            nn.Linear(256, n_classes),
        )

    def forward(self, x):
        return self.classification(self.extraction(x))


if __name__ == "__main__":
    modele = PetitCNN()
    print(modele)
    print()

    total = 0
    for nom, p in modele.named_parameters():
        print(f"{nom:<28} {str(tuple(p.shape)):<20} {p.numel():>9}")
        total += p.numel()
    print(f"{'TOTAL':<28} {'':<20} {total:>9}")

    lot = torch.randn(4, 3, 32, 32)
    sortie = modele(lot)
    print()
    print(f"Entree : {tuple(lot.shape)}")
    print(f"Sortie : {tuple(sortie.shape)}")
