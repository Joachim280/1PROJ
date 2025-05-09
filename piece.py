from coordinates import Coordinates

class Piece:
    def __init__(self, position, player):
        self._position = position  # Coordinates object
        self.player = player       # Player object
        self.in_camp = False       # Track if the piece is in a camp

    @property
    def position(self):
        """Read-only access to position (safety)"""
        return self._position

    def move_to(self, destination):
        """Update position and reset camp status if leaving a camp"""
        if not self.in_camp:
            self._position = destination
        # Else: Prevent movement if already in a camp (Katarenga rule)

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
