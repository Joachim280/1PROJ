from game import Game
from coordinates import Coordinates
from piece import Piece

class Isolation(Game):
    def initialize(self):
        pass  # Plateau vide

    def get_valid_moves(self, player):
        valid = []
        for x in range(8):
            for y in range(8):
                coord = Coordinates(x, y)
                if self._is_valid_placement(coord):
                    valid.append(coord)
        return valid

    def _is_valid_placement(self, coord):
        if self.board.is_occupied(coord):
            return False
            
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                neighbor = Coordinates(coord.x + dx, coord.y + dy)
                if self.board.is_occupied(neighbor):
                    return False
                    
        return self.board.is_valid(coord.x, coord.y)

    def _execute_move(self, piece, destination):
        new_piece = Piece(destination, self.current_player)
        self.board.place_piece(destination, new_piece)
        self.current_player.add_piece(new_piece)
        self.switch_player()

    def check_victory(self):
        opponent = self.players[1] if self.current_player == self.players[0] else self.players[0]
        return self.current_player if not self.get_valid_moves(opponent) else None