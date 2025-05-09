from game import Game
from coordinates import Coordinates
from piece import Piece

class Katarenga(Game):
    def __init__(self, board, players):
        super().__init__(board, players)
        self.turn_count = 0  # Track turns for first-turn capture rule

    def initialize(self):
        """Place starting pieces for Katarenga"""
        # White pieces (bottom)
        self._place_pieces(3, 1, self.players[0])
        self._place_pieces(4, 1, self.players[0])
        
        # Black pieces (top)
        self._place_pieces(3, 6, self.players[1])
        self._place_pieces(4, 6, self.players[1])

    def _place_pieces(self, x, y, player):
        """Helper method to place a piece"""
        coord = Coordinates(x, y)
        piece = Piece(coord, player)
        self.board.place_piece(coord, piece)
        player.add_piece(piece)

    def get_valid_moves(self, piece):
        """Return all valid moves for a piece"""
        x, y = piece.position.x, piece.position.y
        tile_color = self.board.get_tile_color(x, y)
        
        if tile_color == 'B': moves = self._king_moves(x, y)
        elif tile_color == 'G': moves = self._knight_moves(x, y)
        elif tile_color == 'Y': moves = self._yellow_moves(x, y)
        elif tile_color == 'R': moves = self._red_moves(x, y)
        else: return []
        
        return [move for move in moves if self._is_move_valid(move, piece.player)]

    def _king_moves(self, x, y):
        """Blue tiles: King moves (8 directions, 1 step)"""
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1),
                     (0,1), (1,-1), (1,0), (1,1)]
        return self._calculate_moves(x, y, directions, max_steps=1)

    def _knight_moves(self, x, y):
        """Green tiles: Knight moves (L-shape)"""
        offsets = [(2,1), (1,2), (-1,2), (-2,1),
                  (-2,-1), (-1,-2), (1,-2), (2,-1)]
        return [Coordinates(x+dx, y+dy) for dx, dy in offsets
                if self.board.is_valid(x+dx, y+dy)]

    def _yellow_moves(self, x, y):
        """Yellow tiles: Diagonal until first yellow tile"""
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
        return self._slide_moves(x, y, directions, stop_color='Y')

    def _red_moves(self, x, y):
        """Red tiles: Straight until first red tile"""
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        return self._slide_moves(x, y, directions, stop_color='R')

    def _slide_moves(self, x, y, directions, stop_color):
        """Generic sliding movement"""
        moves = []
        for dx, dy in directions:
            step = 1
            while True:
                new_x = x + dx * step
                new_y = y + dy * step
                if not self.board.is_valid(new_x, new_y):
                    break
                if self.board.get_tile_color(new_x, new_y) == stop_color:
                    moves.append(Coordinates(new_x, new_y))
                    break
                step += 1
        return moves

    def _is_move_valid(self, coord, player):
        """Check if move is allowed"""
        # Block friendly fire
        if self.board.is_occupied_by(coord, player):
            return False
        # Block first-turn captures
        if self.turn_count == 0 and self.board.is_occupied(coord):
            return False
        return True

    def check_victory(self):
        """Check if current player occupies 2 enemy camps"""
        enemy_camps = self.board.get_enemy_camps(self.current_player)
        occupied = sum(1 for camp in enemy_camps 
                      if self.board.is_occupied_by(camp, self.current_player))
        return self.current_player if occupied >= 2 else None

    def _execute_move(self, piece, destination):
        """Handle special Katarenga rules"""
        if self.turn_count == 0 and self.board.is_occupied(destination):
            return  # Block first-turn captures
        super()._execute_move(piece, destination)
        self.turn_count += 1
