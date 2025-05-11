# class_plateau.py
from class_case import Case
from class_cadran import Quadrant, QUADRANTS

class Plateau:
    def __init__(self):
        self.cases = [[None for _ in range(8)] for _ in range(8)]

    def placer_quadrant(self, quadrant, position):
        if position == "haut_gauche":
            start_row, start_col = 0, 0
        elif position == "haut_droite":
            start_row, start_col = 0, 4
        elif position == "bas_gauche":
            start_row, start_col = 4, 0
        elif position == "bas_droite":
            start_row, start_col = 4, 4
        else:
            return

        for i in range(4):
            for j in range(4):
                self.cases[start_row + i][start_col + j] = quadrant.cases[i][j]

    def afficher(self):
        for ligne in self.cases:
            print(" ".join(case.lettre if case else '.' for case in ligne))

if __name__ == "__main__":
    print("Quadrants disponibles :")
    for i in range(1, 5):
        print(f"\nQuadrant {i} :")
        Quadrant(QUADRANTS[i]).afficher()

    positions = ["haut_gauche", "haut_droite", "bas_gauche", "bas_droite"]
    disponibles = [1, 2, 3, 4]
    plateau = Plateau()

    for pos in positions:
        print(f"\n=== Configuration pour le quadrant {pos.replace('_', ' ')} ===")
        print(f"Quadrants encore disponibles : {disponibles}")

        while True:
            choix = int(input("Quel quadrant veux-tu utiliser ? > "))
            if choix in disponibles:
                break
            print("Ce quadrant a déjà été utilisé ou est invalide. Choisis un autre.")

        while True:
            reponse = input("Souhaites-tu le verso ? (o/n) > ").lower()
            if reponse in ['o', 'n']:
                verso = (reponse == 'o')
                break
            print("Réponse invalide. Tu dois taper 'o' ou 'n'.")

        while True:
            try:
                angle = int(input("Rotation ? (0 / 90 / 180 / 270) > "))
                if angle in [0, 90, 180, 270]:
                    break
                else:
                    print("Choix invalide. Rotation possible uniquement : 0, 90, 180, 270.")
            except ValueError:
                print("Tu dois entrer un nombre (0, 90, 180, 270).")

        grille = QUADRANTS[choix]
        quadrant = Quadrant(grille)
        disponibles.remove(choix)

        print("\nQuadrant choisi (original) :")
        quadrant.afficher()

        if verso:
            quadrant.retourner()
            print("\nAprès effet miroir (verso) :")
            quadrant.afficher()

        for _ in range((angle % 360) // 90):
            quadrant.pivoter()

        print("\nQuadrant final après rotation :")
        quadrant.afficher()

        plateau.placer_quadrant(quadrant, pos)

    print("\n===== Plateau complet 8x8 =====")
    plateau.afficher()
