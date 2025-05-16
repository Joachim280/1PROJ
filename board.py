from coordinates import Coordinates
# pour tester
class Board:
    def __init__(self):
        self.grid = {}
    
    def get_piece(self, coord):
        return self.grid.get(coord, None)
    
    def is_valid(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8
    
    def is_occupied(self, coord):
        return coord in self.grid
    
    def place_piece(self, coord, piece):
        self.grid[coord] = piece
    
    def move_piece(self, from_coord, to_coord):
        """Déplace une pièce sur le plateau"""
        piece = self.grid.pop(from_coord, None)
        if piece:
            self.grid[to_coord] = piece
    
    def get_tile_color(self, x, y):
        """Exemple simplifié (à adapter selon vos quadrants)"""
        return 'B'  # Toutes les cases bleues pour les tests