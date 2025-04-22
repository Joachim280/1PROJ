class Game:
    def __init__(self, board, players):
        self.board = board              # Object from Module 2 (Plateau)
        self.players = players          # List of Player objects
        self.current_player = players[0]

    def initialize(self):
        """Set up the initial pieces (to be implemented per game)"""
        pass

    def play_turn(self):
        """Handle a full turn (to be customized by each game)"""
        pass

    def get_valid_moves(self, piece):
        """Return a list of valid coordinates for the selected piece"""
        return []

    def check_victory(self):
        """Check if current player has won the game"""
        return False

    def switch_player(self):
        """Switch to the other player's turn"""
        self.current_player = self.players[0] if self.current_player == self.players[1] else self.players[1]
