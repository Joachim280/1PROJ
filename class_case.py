# Re-définir les classes et les données après le reset de l'environnement

# Dictionnaire pour convertir les lettres en noms de couleurs
COULEURS_CODES = {
    'B': 'bleu',
    'V': 'vert',
    'J': 'jaune',
    'R': 'rouge'
}

class Case:
    def __init__(self, lettre_couleur):
        self.lettre = lettre_couleur
        self.couleur = COULEURS_CODES.get(lettre_couleur, "inconnue")
        self.pion = None

    def est_libre(self):
        return self.pion is None

    def __repr__(self):
        return self.lettre


