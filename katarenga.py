from game import Game
from coordinates import Coordinates

class Katarenga(Game):
    def get_valid_moves(self, piece):
        x, y = piece.position.x, piece.position.y
        tile_color = self.board.get_color(x, y)

        if tile_color == 'B':  # Blue = King movement
            return self.get_king_moves(x, y)

       # a ajouter plus tard
        return []

    def get_king_moves(self, x, y):
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0),  (1, 1)
        ]

        moves = []
        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                moves.append(Coordinates(new_x, new_y))
        return moves

    def check_victory(self):
        pass  # a ajouter plus tard
