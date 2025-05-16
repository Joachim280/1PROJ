from random import choice

class Player:
    def __init__(self, color, player_type="human"):
        self.color = color
        self.pieces = []
        self.player_type = player_type

    def add_piece(self, piece):
        self.pieces.append(piece)

    def remove_piece(self, piece):
        if piece in self.pieces:
            self.pieces.remove(piece)

    def choose_move(self, game):
        if self.player_type != "ai":
            return None
            
        valid_moves = []
        for piece in self.pieces:
            if piece.in_camp:
                continue
            moves = game.get_valid_moves(piece)
            valid_moves.extend([(piece, move) for move in moves])
        
        return choice(valid_moves) if valid_moves else None

if __name__ == "__main__":
    from piece import Piece
    from coordinates import Coordinates

    # Test basic functionality
    player = Player("black", player_type="ai")
    piece1 = Piece(Coordinates(2, 2), player)
    player.add_piece(piece1)

    print("Player color:", player.color)  # Output: "black"
    print("Player type:", player.player_type)  # Output: "ai"
    print("Pieces:", player.pieces)  # Output: [Piece(Coordinates(2, 2), ...)]
