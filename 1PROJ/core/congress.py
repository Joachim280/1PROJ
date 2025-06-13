from .game import Game
from .coordinates import Coordinates
from .piece import Piece

class Congress(Game):
    """
    Variante de jeu: Congress
    - Même déplacement des pièces que Katarenga
    - Pas de captures autorisées
    - But: former un bloc connecté orthogonalement
    """
    
    def __init__(self, board, players):
        super().__init__(board, players)
    
    def initialize(self):
        """Place les pions initiaux pour Congress sur les bords du plateau en alternant les couleurs"""
        
        # Pions blancs (8 pions)
        white_positions = [
            (1, 0),  # Gauche - case 2
            (4, 0),  # Gauche - case 5
            (7, 1),  # Bas - case 2
            (7, 4),  # Bas - case 5
            (6, 7),  # Droit - case 2
            (3, 7),  # Droit - case 5
            (0, 6),  # Haut - case 2
            (0, 3)   # Haut - case 5
        ]
        
        # Pions noirs (8 pions)
        black_positions = [
            (3, 0),  # Gauche - case 4
            (6, 0),  # Gauche - case 7
            (7, 3),  # Bas - case 4
            (7, 6),  # Bas - case 7
            (4, 7),  # Droit - case 4
            (1, 7),  # Droit - case 7
            (0, 4),  # Haut - case 4
            (0, 1)   # Haut - case 7
        ]
        
        # pions blancs
        for x, y in white_positions:
            self._place_piece(x, y, self.players[0])
            
        # on place les noirs
        for x, y in black_positions:
            self._place_piece(x, y, self.players[1])
    
    def _place_piece(self, x, y, player):
        """Place un pion à la position x,y"""
        coord = Coordinates(x, y)
        piece = Piece(coord, player)
        self.board.place_piece(coord, piece)
        player.add_piece(piece)
    
    def get_valid_moves(self, piece):
        """Renvoie tous les mouvements valides pour une pièce (sans captures)"""
        x, y = piece.position.x, piece.position.y
        tile_color = self.board.get_tile_color(x, y)
        
        if tile_color == 'B': moves = self._king_moves(x, y)
        elif tile_color == 'V': moves = self._knight_moves(x, y)
        elif tile_color == 'J': moves = self._yellow_moves(x, y)
        elif tile_color == 'R': moves = self._red_moves(x, y)
        else: return []
        
        # on filtre les mouvements pour ne garder que les cases libres
        return [move for move in moves if not self.board.is_occupied(move)]
    
    def _king_moves(self, x, y):
        """Mouvements de type roi (8 directions, 1 pas)"""
        directions = [(-1,-1), (-1,0), (-1,1), (0,-1),
                     (0,1), (1,-1), (1,0), (1,1)]
        return self._calculate_moves(x, y, directions, max_steps=1)
    
    def _knight_moves(self, x, y):
        """Mouvements de type cavalier (en L)"""
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
                
                # détection des limites
                if not self.board.is_valid(new_x, new_y):
                    break
                
                # ici, on s'arrête dès qu'on rencontre une pièce
                if self.board.is_occupied(Coordinates(new_x, new_y)):
                    break
                
                # si la case libre, déplacement possible
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
                
                # détection des limites
                if not self.board.is_valid(new_x, new_y):
                    break
                
                # on s'arrête si case occupée
                coord = Coordinates(new_x, new_y)
                if self.board.is_occupied(coord):
                    break
                
                # on ajoute la case aux mouvements possibles
                moves.append(coord)
                
                # on s'arrête si la couleur d'arrêt est atteinte
                if self.board.get_tile_color(new_x, new_y) == stop_color:
                    break
                    
                step += 1
        return moves
    
    def check_victory(self):
        """
        Vérifie si un joueur a créé un bloc connecté
        Un bloc connecté signifie que tous les pions d'un joueur forment 
        un seul groupe où chaque pion est adjacent orthogonalement 
        à au moins un autre pion du même joueur
        """
        for player in self.players:
            # si le joueur n'a pas de pièces on passe
            if not player.pieces:
                continue
                
            # on vérifie si tous les pions forment un seul groupe connecté
            if self._is_connected_group(player):
                return player
                
        return None
    
    def _is_connected_group(self, player):
        """Vérifie si tous les pions du joueur forment un groupe connecté"""
        # moins de 2 pièces, toujours connecté
        if len(player.pieces) < 2:
            return True
            
        # commencons par une pièce quelconque
        start_piece = player.pieces[0]
        
        # on fait un parcours en profondeur à partir de cette pièce
        visited = set()
        self._dfs(start_piece.position, player, visited)
        
        # si toutes les pièces ont été visitées, le groupe est connecté
        return len(visited) == len(player.pieces)
    
    def _dfs(self, position, player, visited):
        """
        Parcours en profondeur pour trouver les pièces connectées
        Deux pièces sont connectées si elles sont adjacentes orthogonalement
        """
        # marquer cette position comme visitée
        visited.add(position)
        
        # directions orthogonales
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        
        for dx, dy in directions:
            new_x, new_y = position.x + dx, position.y + dy
            
            # on check les limites
            if not self.board.is_valid(new_x, new_y):
                continue
                
            # new position
            new_pos = Coordinates(new_x, new_y)
            
            # s'il y a une pièce du même joueur
            if (self.board.is_occupied_by(new_pos, player) and 
                new_pos not in visited):
                self._dfs(new_pos, player, visited)
