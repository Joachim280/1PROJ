from coordinates import Coordinates
from piece import Piece
from player import Player

class Game:
    def __init__(self, board, players):
        self.board = board          # Board object (from Module 2)
        self.players = players      # List of Player objects [Player1, Player2]
        self.current_player = players[0]
        self.game_over = False

    def initialize(self):
        """Set up initial pieces (to be overridden by child classes)"""
        raise NotImplementedError("Subclasses must implement initialize()")

    def play_turn(self, from_coord, to_coord):
        """
        Handle a player's turn:
        1. Validate move
        2. Execute move
        3. Check victory
        Returns True if move succeeded, False otherwise
        """
        if self.game_over:
            return False

        piece = self.board.get_piece(from_coord)
        if not piece or piece.player != self.current_player:
            return False

        valid_moves = self.get_valid_moves(piece)
        if to_coord not in valid_moves:
            return False

        # Execute the move
        self._execute_move(piece, to_coord)

        # Check for winner
        winner = self.check_victory()
        if winner:
            self.game_over = True
        else:
            self.switch_player()

        return True

    def _execute_move(self, piece, destination):
        """Handle movement logic (captures, position updates)"""
        # Remove captured piece (if any)
        if self.board.is_occupied(destination):
            captured_piece = self.board.get_piece(destination)
            captured_piece.player.pieces.remove(captured_piece)

        # Update piece position
        self.board.move_piece(piece.position, destination)
        piece.move_to(destination)

    def get_valid_moves(self, piece):
        """Return list of valid Coordinates (to be overridden by child classes)"""
        raise NotImplementedError("Subclasses must implement get_valid_moves()")

    def check_victory(self):
        """Return winning Player or None (to be overridden)"""
        raise NotImplementedError("Subclasses must implement check_victory()")

    def switch_player(self):
        """Alternate between players"""
        self.current_player = self.players[1] if self.current_player == self.players[0] else self.players[0]

    def __repr__(self):
        return f"Game({self.current_player.color}'s turn)"
