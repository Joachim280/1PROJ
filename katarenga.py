from game import Game
from coordinates import Coordinates
from utils import calculate_move
from piece import Piece

class Katarenga(Game):
    def __init__(self, board, players):
        super().__init__(board, players)
        self.turn_count = 0

    def initialize(self):
        for x in range(8):
            self._create_piece(x, 0, self.players[0])  # Blancs en bas
            self._create_piece(x, 7, self.players[1])  # Noirs en haut

    def _create_piece(self, x, y, player):
        coord = Coordinates(x, y)
        piece = Piece(coord, player)
        self.board.place_piece(coord, piece)
        player.add_piece(piece)

    def get_valid_moves(self, piece):
        x, y = piece.position.x, piece.position.y
        tile_color = self.board.get_tile_color(x, y)
        
        if tile_color == 'B':
            directions = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
            moves = calculate_move(x, y, directions, 1, self.board)
        elif tile_color == 'G':
            moves = self._knight_moves(x, y)
        elif tile_color == 'Y':
            moves = calculate_move(x, y, [(-1,-1), (-1,1), (1,-1), (1,1)], 8, self.board)
        elif tile_color == 'R':
            moves = calculate_move(x, y, [(0,1), (1,0), (0,-1), (-1,0)], 8, self.board)
        else:
            return []
        
        return [m for m in moves if not self.board.is_occupied_by(m, piece.player)]

    def _knight_moves(self, x, y):
        offsets = [(2,1), (1,2), (-1,2), (-2,1), (-2,-1), (-1,-2), (1,-2), (2,-1)]
        return [Coordinates(x+dx, y+dy) for dx, dy in offsets if self.board.is_valid(x+dx, y+dy)]

    def _execute_move(self, piece, destination):
        if self.turn_count == 0 and self.board.is_occupied(destination):
            return  # Bloque les captures au premier tour
        
        if self.board.is_occupied(destination):
            captured_piece = self.board.get_piece(destination)
            captured_piece.player.remove_piece(captured_piece)
        
        self.board.move_piece(piece.position, destination)
        piece.move_to(destination, self)
        
        # Correction : Utilisation de is_enemy_camp au lieu de is_enemy_line
        if self.is_enemy_camp(destination, piece.player):
            piece.in_camp = True  # Nécessite l'attribut in_camp dans Piece
        
        self.turn_count += 1

    def is_enemy_camp(self, coord, player):
        """Détermine si la coordonnée est dans le camp ennemi"""
        enemy_camps = [Coordinates(0,7), Coordinates(7,7)] if player.color == "white" \
                      else [Coordinates(0,0), Coordinates(7,0)]
        return coord in enemy_camps

    def check_victory(self):
        """Vérifie si le dernier joueur a gagné"""
        last_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
        enemy_camps = [Coordinates(0,7), Coordinates(7,7)] if last_player.color == "white" \
                      else [Coordinates(0,0), Coordinates(7,0)]
        occupied = sum(1 for camp in enemy_camps if self.board.is_occupied_by(camp, last_player))
        return last_player if occupied >= 2 else None
