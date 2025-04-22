from coordinates import Coordinates

class Piece:
    def __init__(self, position, player):
        self.position = position  # Coordinates object
        self.player = player      # Player object

    def move_to(self, destination):
        self.position = destination

if __name__ == "__main__":
    from player import Player  # à faire à l'étape suivante
    p = Player("white")
    piece = Piece(Coordinates(3, 3), p)
    print("Initial position:", piece.position)
    piece.move_to(Coordinates(4, 4))
    print("New position:", piece.position)
