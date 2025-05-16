from game import Game
from coordinates import Coordinates
from piece import Piece
from utils import calculate_move

class Congress(Game):
    def __init__(self, board, players):
        super().__init__(board, players)

    def initialize(self):
        black_positions = [(1,7), (4,7), (7,6), (7,3), (6,0), (3,0), (0,1), (0,4)]
        white_positions = [(0,6), (0,3), (1,0), (4,0), (7,1), (7,4), (6,7), (3,7)]
        
        for x, y in black_positions:
            self._create_piece(x, y, self.players[1])
        for x, y in white_positions:
            self._create_piece(x, y, self.players[0])

    def _create_piece(self, x, y, player):
        coord = Coordinates(x, y)
        piece = Piece(coord, player)
        self.board.place_piece(coord, piece)
        player.add_piece(piece)

    def get_valid_moves(self, piece):
        x, y = piece.position.x, piece.position.y
        directions = [(-1,0), (1,0), (0,1), (0,-1)]
        moves = calculate_move(x, y, directions, 1, self.board)
        return [m for m in moves if not self.board.is_occupied(m)]

    def check_victory(self):
        for player in self.players:
            if self._is_connected(player.pieces):
                return player
        return None

    def _is_connected(self, pieces):
        if not pieces:
            return False
            
        visited = set()
        queue = [pieces[0].position]
        
        while queue:
            current = queue.pop(0)
            visited.add(current)
            
            neighbors = [
                Coordinates(current.x+1, current.y), Coordinates(current.x-1, current.y),
                Coordinates(current.x, current.y+1), Coordinates(current.x, current.y-1)
            ]
            
            for neighbor in neighbors:
                if any(p.position == neighbor for p in pieces) and neighbor not in visited:
                    queue.append(neighbor)
        
        return len(visited) == len(pieces)