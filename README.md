# Space Invaders — Architecture Orientée Objet (Python / Pygame)

Version en programmation orientée objet (OOP) du jeu classique **Space Invaders**, développée en **Python** avec **Pygame**.

## Prérequis

- **Python** (>= 3.10 ; <= 3.13)
- `pip` (gestionnaire de paquets Python)

## Installation

1. Cloner le dépôt GitHub et accéder au dossier du projet :

   ```bash
   git clone "https://github.com/muneeb-anwar-data-ia/space-invaders-oop"
   cd space-invaders-oop
   ```

2. Créer et activer un environnement virtuel (recommandé) :

   - **Windows (PowerShell / CMD)** :
     ```bash
     python -m venv .venv
     .venv\Scripts\activate
     ```

   - **macOS / Linux** :
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. Installer les dépendances :

   ```bash
   pip install -r requirements.txt
   ```

## Lancement du jeu

Depuis la racine du projet :

   - **Windows (PowerShell / CMD)** :
     ```bash
     python main.py
     ```

   - **macOS / Linux** :
     ```bash
     python3 main.py
     ```

## Commandes du jeu

| Touche | Action |
| :--- | :--- |
| `Flèche Gauche` (`←`) | Déplacer le vaisseau vers la gauche |
| `Flèche Droite` (`→`) | Déplacer le vaisseau vers la droite |
| `Espace` (`Space`) | Tirer un projectile normal |
| `E` | Tirer un projectile spécial, plus rapide |
| Fermeture fenêtre (`×`) | Quitter le jeu |

## Nouveautés ajoutées

### Nouvel ennemi : ennemi rapide

Le jeu contient maintenant deux types d'ennemis :

- **Ennemi normal** : se déplace à la vitesse habituelle.
- **Ennemi rapide** : se déplace plus vite que l'ennemi normal. Il est créé avec la classe `FastEnemy`, qui reprend le fonctionnement de la classe `Enemy`.

Les ennemis rapides apparaissent parmi les ennemis de la partie.

### Nouvelle arme : tir spécial

En plus du projectile normal (touche `Espace`), le joueur peut utiliser un tir spécial avec la touche `E`.

- Le projectile spécial se déplace plus rapidement que le projectile normal.
- Il est affiché sous la forme d'un petit rectangle jaune.
- Lorsqu'il touche un ennemi, il rapporte **2 points** au lieu d'un seul.

Les deux types de tirs peuvent être utilisés séparément.

## Structure du projet

```text
space-invaders-oop/
├── assets/
│   ├── images/
│   │   ├── background.png
│   │   ├── bullet.png
│   │   ├── enemy.png
│   │   ├── player.png
│   │   └── ufo.png
│   └── sounds/
│       └── background.wav
│       └── laser.wav
│       └── explosion.wav
├── space_invaders/
│   ├── __init__.py
│   ├── config.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── entities.py
│   │   └── game.py
│   └── ui/
│       ├── __init__.py
│       ├── input_handler.py
│       └── renderer.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Architecture logicielle

- **`main.py`** : point d'entrée orchestrant la boucle principale du jeu.
- **`space_invaders/config.py`** : centralise les paramètres du jeu et les chemins vers les ressources (`assets/`).
- **`space_invaders/core/`** : contient la logique métier pure (`Entity`, `Player`, `Enemy`, `Bullet`, `Game`), indépendante de l'affichage Pygame.
- **`space_invaders/ui/`** : gère les entrées clavier (`InputHandler`) et le rendu graphique/audio (`PygameRenderer`).