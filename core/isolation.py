from .game import Game
from .coordinates import Coordinates
from .piece import Piece

class Isolation(Game):
    """
    Variante du jeu : Isolation
    - Plateau initialement vide
    - Placement des pions au lieu de déplacement
    - Interdiction de placer un pion "en prise"
    - Victoire au dernier joueur pouvant placer un pion
    """
    
    def __init__(self, board, players):
        super().__init__(board, players)
    
    def initialize(self):
        """Ne place aucun pion initial - plateau vide"""
        # rien à faire car le plateau doit être vide au départ
        pass
    
    def play_turn(self, from_coord, to_coord):
        """
        Redéfinit play_turn pour y implémenter la logique de placement
        au lieu de déplacement. Le paramètre from_coord est ignoré.
        """
        if self.game_over:
            return False
            
        # vérifie si le placement est valide
        if to_coord not in self.get_valid_moves(None):
            return False
            
        # place un nouveau pion
        self._place_piece(to_coord.x, to_coord.y, self.current_player)
        
        # vérifie conditions de victoire
        winner = self.check_victory()
        if winner:
            self.game_over = True
        else:
            self.switch_player()
            
        return True
    
    def _place_piece(self, x, y, player):
        """Place un nouveau pion à la position indiquée"""
        coord = Coordinates(x, y)
        piece = Piece(coord, player)
        self.board.place_piece(coord, piece)
        player.add_piece(piece)
    
    def is_in_check(self, coord):
        """
        Vérifie si une position serait "en prise" 
        (pourrait être capturée par un pion déjà sur le plateau)
        """
        # parcourt tous les pions présents sur le plateau
        for player in self.players:
            for piece in player.pieces:
                # simule une pièce adverse sur la position
                temp_player = self.players[1] if player == self.players[0] else self.players[0]
                temp_piece = Piece(coord, temp_player)
                
                # vérifie si un pion pourrait capturer cette position
                moves = self._get_piece_attacking_moves(piece)
                if coord in moves:
                    return True
                    
        return False
    
    def _get_piece_attacking_moves(self, piece):
        """
        Calcule les positions qu'une pièce peut attaquer
        en fonction de la couleur de sa case.
        """
        x, y = piece.position.x, piece.position.y
        tile_color = self.board.get_tile_color(x, y)
        
        if tile_color == 'B': moves = self._king_moves(x, y)
        elif tile_color == 'V': moves = self._knight_moves(x, y)
        elif tile_color == 'J': moves = self._yellow_moves(x, y)
        elif tile_color == 'R': moves = self._red_moves(x, y)
        else: return []
        
        return moves
        
    def get_valid_moves(self, piece=None):
        """
        Retourne toutes les cases vides qui ne sont pas en prise.
        Pour Isolation, piece=None car on ne déplace pas de pièce existante.
        """
        valid_moves = []
        
        # parcourt toutes les cases du plateau
        for x in range(8):
            for y in range(8):
                coord = Coordinates(x, y)
                
                # vérifie si la case est libre
                if not self.board.is_occupied(coord):
                    # vérifie si un pion placé ici ne serait pas en prise
                    if not self.is_in_check(coord):
                        valid_moves.append(coord)
                        
        return valid_moves
    
    def _king_moves(self, x, y):
        """Mouvements de type roi (8 directions, 1 pas) - case bleue"""
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1),
                     (0,1), (1,-1), (1,0), (1,1)]
        return self._calculate_moves(x, y, directions, max_steps=1)
    
    def _knight_moves(self, x, y):
        """Mouvements de type cavalier (en L) - case verte"""
        offsets = [(2,1), (1,2), (-1,2), (-2,1),
                  (-2,-1), (-1,-2), (1,-2), (2,-1)]
        return [Coordinates(x+dx, y+dy) for dx, dy in offsets
                if self.board.is_valid(x+dx, y+dy)]
    
    def _yellow_moves(self, x, y):
        """Mouvements diagonaux jusqu'à la première case jaune"""
        directions = [(-1,-1), (-1,1), (1,-1), (1,1)]
        return self._slide_moves(x, y, directions, stop_color='J')
    
    def _red_moves(self, x, y):
        """Mouvements orthogonaux jusqu'à la première case rouge"""
        directions = [(0,1), (1,0), (0,-1), (-1,0)]
        return self._slide_moves(x, y, directions, stop_color='R')
    
    def _calculate_moves(self, x, y, directions, max_steps=8):
        """Calcule les mouvements possibles dans les directions données"""
        moves = []
        
        for dx, dy in directions:
            for step in range(1, max_steps + 1):
                new_x = x + dx * step
                new_y = y + dy * step
                
                # vérification des limites
                if not self.board.is_valid(new_x, new_y):
                    break
                
                # ajoute la position aux mouvements possibles
                moves.append(Coordinates(new_x, new_y))
                
                if step == max_steps:
                    break
                    
        return moves
    
    def _slide_moves(self, x, y, directions, stop_color):
        """Mouvement glissé générique"""
        moves = []
        for dx, dy in directions:
            step = 1
            while True:
                new_x = x + dx * step
                new_y = y + dy * step
                
                # vérification des limites
                if not self.board.is_valid(new_x, new_y):
                    break
                
                # ajoute la position aux mouvements possibles
                moves.append(Coordinates(new_x, new_y))
                
                # s'arrête si couleur d'arrêt atteinte
                if self.board.get_tile_color(new_x, new_y) == stop_color:
                    break
                    
                step += 1
        return moves
    
    def check_victory(self):
        """
        Vérifie si le jeu est terminé (aucun placement possible).
        Le gagnant est le dernier joueur à avoir joué.
        """
        # si aucun coup valide n'est possible pour le joueur actuel
        if not self.get_valid_moves():
            # le gagnant est l'autre joueur (qui a joué en dernier)
            return self.players[1] if self.current_player == self.players[0] else self.players[0]
            
        return None
