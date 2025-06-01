# Projet Katarenga - 1PROJ

## Contexte du Projet

Ce projet est réalisé dans le cadre du cours **1PROJ** à SUPINFO. L'objectif est de développer une adaptation numérique du jeu de plateau abstrait **Katarenga**, ainsi que deux autres variantes, **Congress** et **Isolation**, avec une interface graphique utilisable sur Windows, Linux et Mac OS, en utilisant Python et Tkinter.

---

## Jeux implémentés

### 1. Katarenga

* Chaque joueur possède 8 pions.
* Déplacement des pions déterminé par la couleur de la case :

  * **Bleu** : déplacement comme un roi (8 directions, 1 case)
  * **Vert** : déplacement comme un cavalier
  * **Jaune** : déplacement diagonal limité par la première case jaune
  * **Rouge** : déplacement orthogonal limité par la première case rouge
* Objectif : occuper les deux camps adverses ou empêcher l'adversaire d'atteindre son objectif.

### 2. Congress

* Placement initial prédéfini des pions sur les bords du plateau.
* Pas de captures.
* Objectif : former un bloc connecté orthogonalement.

### 3. Isolation

* Plateau initialement vide.
* Placement des pions sans déplacement ni capture.
* Objectif : être le dernier joueur à placer un pion sans être en prise.

---

## Technologies utilisées

* Python 3.11+
* Tkinter (interface graphique)
* Programmation Orientée Objet (POO)
* Git et GitHub pour la gestion du projet

---

## Structure du Projet

```
     1PROJ/
├── 📂 core
│   ├── 📄 __init__.py
│   ├── 📄 class_plateau.py (gestion du plateau global)
│   ├── 📄 class_case.py (gestion des cases individuelles)
│   ├── 📄 class_cadran.py (gestion des quadrants 4x4)
│   ├── 📄 coordinates.py
│   ├── 📄 game.py (classe abstraite jeu)
│   ├── 📄 player.py (gestion des joueurs)
│   ├── 📄 piece.py (gestion des pièces)
│   ├── 📄 katarenga.py
│   ├── 📄 congress.py
│   └── 📄 isolation.py
│   └── 📄 random_ai.py (IA aléatoire pour les jeux)
├── 📂 ui
│   ├── 📄 __init__.py
│   ├── 📄 app.py (entrée principale Tkinter)
│   ├── 📄 plateau_manager.py (gestion des plateaux personnalisés)
│   ├── 📂 screens
│   │   ├── 📄 menu_screen.py
│   │   ├── 📄 welcome_screen.py
│   │   ├── 📄 build_screen.py
│   │   ├── 📄 game_screen.py
│   │   ├── 📄 quadrant_editor_screen.py
│   │   └── 📄 orientation_screen.py
│   ├── 📂 widgets
│   │   └── board_canvas.py (canvas du plateau)
│   │   └── quadrant_selecetor.py (sélecteur de quadrants)
├── 📄 run_gui.py (lanceur principal)
├── 📄 README.md (documentation)
└── 📂 custom_boards
    └── 📄 boards.pickle (sauvegarde des plateaux personnalisés)
```

---

## Fonctionnalités principales

* **Menu principal** : choix du jeu (Katarenga, Congress, Isolation), mode de jeu (local, réseau, IA), éditeur de quadrants.
* **Édition personnalisée des quadrants** avec sauvegarde jusqu'à 3 plateaux.
* **Interface utilisateur Tkinter** avec gestion des différents écrans.
* **Jeu contre IA** avec coups aléatoires (RandomAI).
* **Jeu en réseau** disponible (implémentation optionnelle selon avancement).

---

## Modules du projet

### Module 1 : Menu

* Classes : GUI (afficher\_menu, demander\_choix\_jeu, demander\_mode), Main (initialiser\_partie).

### Module 2 : Configuration du Plateau

* Classes : Plateau (placer\_quadrant, generer\_grille), Quadrant (pivoter, retourner), Case (couleur, pion, est\_libre), GUI (afficher\_plateau\_configurable).

### Module 3 : Logique du Jeu

* Classes : Jeu (initialiser, jouer\_tour, verifier\_victoire, changer\_tour), Katarenga, Congress, Isolation (verifier\_victoire, règles déplacement), Joueur, Pion, Coordonnées.

### Module 4 : Interface Graphique

* Classes : GUI (afficher\_plateau, afficher\_pions, afficher\_message), Main (lien logique interface-jeu).

---

## Lancement du projet

```bash
python run_gui.py
```

---

## Auteurs

* **Job Cesaire-Dang**
* **Matthew Li-Ching-Ng**
* **Joachim Collot**
