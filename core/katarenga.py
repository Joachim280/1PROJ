from .game import Game
from .coordinates import Coordinates
from .piece import Piece

class Katarenga(Game):
    def __init__(self, board, players):
        super().__init__(board, players)
        self.turn_count = 0  # Track turns for first-turn capture rule

    def initialize(self):
        """Place starting pieces for Katarenga"""
        # White pieces (bottom)
        for col in range(8):
            self._place_piece(7, col, self.players[0])  # ligne du bas (7)
        
        # Black pieces (top)
        for col in range(8):
            self._place_piece(0, col, self.players[1])  # ligne du haut (0)

    def _place_piece(self, x, y, player):
        """Helper method to place a single piece at x,y"""
        coord = Coordinates(x, y)
        piece = Piece(coord, player)
        self.board.place_piece(coord, piece)
        player.add_piece(piece)

    def get_valid_moves(self, piece):
        """Return all valid moves for a piece"""
        x, y = piece.position.x, piece.position.y
        tile_color = self.board.get_tile_color(x, y)
        
        if tile_color == 'B': moves = self._king_moves(x, y)
        elif tile_color == 'V': moves = self._knight_moves(x, y)
        elif tile_color == 'J': moves = self._yellow_moves(x, y)
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
                    
                # Vérifie si la case est libre
                current_coord = Coordinates(new_x, new_y)
                if self.board.is_occupied(current_coord):
                    # Si c'est une pièce adverse, on peut la capturer
                    if not self.board.is_occupied_by(current_coord, self.current_player):
                        moves.append(current_coord)
                    break
                    
                # Ajoute cette case aux mouvements possibles
                moves.append(current_coord)
                
                # Vérifie si on a atteint une case de la couleur d'arrêt
                if self.board.get_tile_color(new_x, new_y) == stop_color:
                    break
                    
                step += 1
        return moves

    def _calculate_moves(self, x, y, directions, max_steps=8):
        """Helper pour calculer les mouvements possibles dans les directions données.
        
        Args:
            x, y: Coordonnées de départ
            directions: Liste de tuples (dx, dy) représentant les directions
            max_steps: Nombre maximum de pas dans chaque direction
        
        Returns:
            List[Coordinates]: Liste des coordonnées accessibles
        """
        moves = []
        
        for dx, dy in directions:
            for step in range(1, max_steps + 1):
                new_x = x + dx * step
                new_y = y + dy * step
                
                # Vérification si la position est valide
                if not self.board.is_valid(new_x, new_y):
                    break
                
                # Vérifie si la case est occupée
                if self.board.is_occupied(Coordinates(new_x, new_y)):
                    if not self.board.is_occupied_by(Coordinates(new_x, new_y), 
                                                   self.current_player):
                        # Si c'est une pièce adverse, on peut la capturer
                        moves.append(Coordinates(new_x, new_y))
                    break
                
                # Si la case est libre, on peut y aller
                moves.append(Coordinates(new_x, new_y))
                
                # Si on a atteint le nombre max de pas, on s'arrête
                if step == max_steps:
                    break
                    
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
        """Vérifie si le joueur actuel occupe 2 camps ennemis ou si l'adversaire n'a plus de pions"""
        # Victoire par occupation des camps
        enemy_camps = self.board.get_enemy_camps(self.current_player)
        occupied = sum(1 for camp in enemy_camps 
                      if self.board.is_occupied_by(camp, self.current_player))
        if occupied >= 2:
            return self.current_player
            
        # Victoire par élimination (l'adversaire n'a plus de pions)
        next_player = self.players[1] if self.current_player == self.players[0] else self.players[0]
        if len(next_player.pieces) == 0:
            return self.current_player
            
        # Pas de victoire
        return None
        
    def _is_enemy_line(self, coord, player):
        """Vérifie si une coordonnée est sur la ligne adverse (ligne 0 pour blanc, ligne 7 pour noir)"""
        if player.color == "white":
            return coord.x == 0  # Ligne du haut pour les blancs
        else:
            return coord.x == 7  # Ligne du bas pour les noirs

    def _execute_move(self, piece, destination):
        """Handle movement logic (captures, position updates) with camp rules"""
        # vérifie si on entre dans un camp adverse
        is_enemy_camp = destination in self.board.get_enemy_camps(piece.player)
        
        # si on vient de la ligne adverse et qu'on entre dans un camp
        if self._is_enemy_line(piece.position, piece.player) and is_enemy_camp:
            # marquer la pièce comme étant dans un camp (ne pourra plus bouger)
            piece.in_camp = True
            
        # Remove captured piece (if any)
        if self.board.is_occupied(destination):
            captured_piece = self.board.get_piece(destination)
            captured_piece.player.pieces.remove(captured_piece)

        # Update piece position
        self.board.move_piece(piece.position, destination)
        piece.move_to(destination)
        
        # incrémenter compteur de tours
        self.turn_count += 1
