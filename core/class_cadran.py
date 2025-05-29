from .class_case import Case

q1 = [
    ['J', 'B', 'V', 'R'],
    ['R', 'V', 'J', 'J'],
    ['V', 'R', 'B', 'B'],
    ['B', 'J', 'R', 'V']
]

q2 = [
    ['V', 'B', 'J', 'R'],
    ['R', 'B', 'J', 'V'],
    ['J', 'R', 'V', 'B'],
    ['B', 'V', 'R', 'J']
]

q3 = [
    ['V', 'B', 'R', 'J'],
    ['B', 'V', 'B', 'R'],
    ['J', 'R', 'J', 'V'],
    ['R', 'V', 'J', 'B']
]

q4 = [
    ['J', 'B', 'V', 'R'],
    ['R', 'B', 'J', 'J'],
    ['B', 'V', 'R', 'V'],
    ['V', 'R', 'J', 'B']
]

QUADRANTS = {
    1: q1,
    2: q2,
    3: q3,
    4: q4
}

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

    # pour garder la responsabilité dans Plateau, on ajoute une méthode pour délégation
    def placer_sur_plateau(self, plateau, position):
        plateau.placer_quadrant(self, position)