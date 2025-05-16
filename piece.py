from coordinates import Coordinates

class Piece:
    def __init__(self, position, player):
        self._position = position
        self.player = player
        self.in_camp = False
        self.on_enemy_line = False

    @property
    def position(self):
        return self._position

    def move_to(self, destination, game):
        if self.in_camp:
            return  # Blocage
        
        self._position = destination
        self.on_enemy_line = game.is_enemy_line(destination, self.player)
        self.in_camp = game.is_enemy_camp(destination, self.player)


if __name__ == "__main__":
    # Test basic functionality
    from player import Player
    player = Player("white")
    
    # Create a piece and move it
    piece = Piece(Coordinates(3, 3), player)
    print(f"Initial position: {piece.position}")  # (3, 3)
    
    piece.move_to(Coordinates(4, 4))
    print(f"New position: {piece.position}")      # (4, 4)
    
    # Test camp blocking
    piece.in_camp = True
    piece.move_to(Coordinates(5, 5))
    print(f"Position after camp block: {piece.position}")  # Still (4, 4)
