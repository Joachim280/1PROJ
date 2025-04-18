from class_case import Case

class Quadrant:
    def __init__(self, grille_lettres):
        self.grille_lettres = grille_lettres
        self.cases = self.generer_cases()

    def generer_cases(self):
        resultat = []
        for ligne in self.grille_lettres:
            ligne_cases = []
            for lettre in ligne:
                ligne_cases.append(Case(lettre))
            resultat.append(ligne_cases)
        return resultat

    def afficher(self):
        for ligne in self.cases:
            print(" ".join(case.lettre for case in ligne))

    def pivoter(self):
        taille = len(self.cases)
        nouvelle_grille = []
        for col in range(taille):
            nouvelle_ligne = []
            for row in reversed(range(taille)):
                nouvelle_ligne.append(self.cases[row][col])
            nouvelle_grille.append(nouvelle_ligne)
        self.cases = nouvelle_grille

    def retourner(self):
        self.cases = [list(reversed(ligne)) for ligne in self.cases]

if __name__ == "__main__":
    q1 = [
        ['J', 'B', 'V', 'R'],
        ['R', 'V', 'J', 'J'],
        ['V', 'R', 'B', 'B'],
        ['B', 'J', 'R', 'V']
    ]

    quadrant_test = Quadrant(q1)

    print("Face recto originale :")
    quadrant_test.afficher()

    print("\nAprès rotation 90° :")
    quadrant_test.pivoter()
    quadrant_test.afficher()

    print("\nAprès effet miroir (verso) :")
    quadrant_test.retourner()
    quadrant_test.afficher()
