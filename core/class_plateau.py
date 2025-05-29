from .class_case import Case
from .class_cadran import Quadrant, QUADRANTS

class Plateau:
    def __init__(self):
        self.cases = [[None for _ in range(8)] for _ in range(8)]

    # ------------------------------------------------------------------
    #  indications des pièces utilisée par Katarenga
    # ------------------------------------------------------------------
    def place_piece(self, coord, piece):
        """Dépose la pièce dans la Case située à `coord`"""
        cell = self.cases[coord.x][coord.y]

        # la case n’existe pas encore, on en crée une neutre
        if cell is None:
            cell = Case('B')          # lettre quelconque
            self.cases[coord.x][coord.y] = cell

        # on place la pièce dans l’attribut .pion
        cell.pion = piece

        # synchronisation
        if hasattr(piece, "move_to"):
            piece.move_to(coord)
        elif hasattr(piece, "_position"):
            piece._position = coord

        piece.board = self


    def is_occupied(self, coord):
        cell = self.cases[coord.x][coord.y]
        return cell is not None and getattr(cell, "pion", None) is not None
        
    def is_occupied_by(self, coord, player):
        """on voie si la case est occupée par un pion du joueur spécifié"""
        cell = self.cases[coord.x][coord.y]
        if cell is None or getattr(cell, "pion", None) is None:
            return False
        return cell.pion.player == player
    
    def get_piece(self, coord):
        """on doit retourner le pion à la position spécifiée ou None"""
        cell = self.cases[coord.x][coord.y]
        if cell is None:
            return None
        return getattr(cell, "pion", None)
        
    def move_piece(self, from_coord, to_coord):
        """bouge le pion d'une case à l'autre"""
        from_cell = self.cases[from_coord.x][from_coord.y]
        to_cell = self.cases[to_coord.x][to_coord.y]
        
        if from_cell is None or getattr(from_cell, "pion", None) is None:
            return
            
        # on crée la case destination si nécessaire
        if to_cell is None:
            to_cell = Case('B')
            self.cases[to_coord.x][to_coord.y] = to_cell
            
        # on transfert le pion
        to_cell.pion = from_cell.pion
        from_cell.pion = None


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
    
    def get_enemy_camps(self, player):
        """Renvoie les coordonnées des camps ennemis pour un joueur"""
        from .coordinates import Coordinates
        if player.color == "white":
            # camps adverses de white = coins noirs (haut gauche et haut droite)
            return [Coordinates(0, 0), Coordinates(0, 7)]
        else:
            # camps adverses de black = coins blancs (bas gauche et bas droite)
            return [Coordinates(7, 0), Coordinates(7, 7)]
            
    def is_valid(self, x, y):
        """Vérifie si les coordonnées sont dans les limites du plateau"""
        return 0 <= x < 8 and 0 <= y < 8
        
    def get_tile_color(self, x, y):
        """Renvoie la lettre correspondant à la couleur de la case (B, R, V, J)"""
        cell = self.cases[x][y]
        if cell is None:
            return None
        return cell.lettre

    def afficher(self):
        for ligne in self.cases:
            print(" ".join(case.lettre if case else '.' for case in ligne))


# méthode pour créer un plateau directement depuis les 4 matrices 4x4
    @classmethod
    def from_quadrants(cls, quad_mats):
        """Construit un Plateau 8x8 à partir d'une liste de 4 matrices 4x4"""
        p = cls()
        positions = ["haut_gauche", "haut_droite", "bas_gauche", "bas_droite"]
        for mat, pos in zip(quad_mats, positions):
            Quadrant(mat).placer_sur_plateau(p, pos)
        return p


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
            print("Ce quadrant a déjà été utilisé ou est invalide. Choisis un autre")

        while True:
            reponse = input("Souhaites-tu le verso ? (o/n) > ").lower()
            if reponse in ['o', 'n']:
                verso = (reponse == 'o')
                break
            print("Réponse invalide. Tu dois taper 'o' ou 'n'")

        while True:
            try:
                angle = int(input("Rotation ? (0 / 90 / 180 / 270) > "))
                if angle in [0, 90, 180, 270]:
                    break
                else:
                    print("Choix invalide. Rotation possible uniquement : 0, 90, 180, 270")
            except ValueError:
                print("Tu dois entrer un nombre (0, 90, 180, 270)")

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
