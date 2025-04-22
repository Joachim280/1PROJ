class Player:
    def __init__(self, color, player_type="human"):
        self.color = color                  # "white" or "black"
        self.pieces = []                   # list of Piece objects
        self.player_type = player_type     # "human" or "ai"

    def add_piece(self, piece):
        self.pieces.append(piece)

        
if __name__ == "__main__":
    from piece import Piece
    from coordinates import Coordinates

    player = Player("black")
    piece1 = Piece(Coordinates(2, 2), player)
    player.add_piece(piece1)

    print("Player color:", player.color)
    print("Player pieces:", player.pieces)