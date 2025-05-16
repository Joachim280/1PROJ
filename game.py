from coordinates import Coordinates
from piece import Piece
from player import Player
from utils import is_enemy_line

class Game:
    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.current_player = players[0]
        self.game_over = False

    def initialize(self):
        raise NotImplementedError("À implémenter dans les sous-classes")

    def play_turn(self, from_coord, to_coord):
        if from_coord is None:  # Mode Isolation
            valid_moves = self.get_valid_moves(self.current_player)
            if to_coord not in valid_moves:
                return False
            self._execute_move(None, to_coord)
            return True
        else:  # Mode Katarenga/Congress
            piece = self.board.get_piece(from_coord)
            if not piece or piece.player != self.current_player:
                return False
            
            valid_moves = self.get_valid_moves(piece)
            if to_coord not in valid_moves:
                return False
            
            self._execute_move(piece, to_coord)
            return True

    def _execute_move(self, piece, destination):
        raise NotImplementedError("À implémenter dans les sous-classes")

    def switch_player(self):
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def is_enemy_line(self, coord, player):
        return is_enemy_line(coord, player)
    
