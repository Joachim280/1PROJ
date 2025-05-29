import random
from core.coordinates import Coordinates

class RandomAI:
    """
    IA de base qui sélectionne un coup aléatoire parmi les coups possibles suivant le jeu
    """
    
    def __init__(self, game):
        self.game = game
    
    def make_move(self):
        """
        Effectue un coup aléatoire et retourne True si le coup a été joué avec succès
        """
        if self.game.game_over:
            return False
            
        # on récupère le joueur actuel
        player = self.game.current_player
        
        # réglage du comportement spécifique pour Isolation car pas de pièce à déplacer
        if hasattr(self.game, "is_in_check"):
            return self._make_isolation_move()
        else:
            return self._make_movement_game_move()
    
    def _make_isolation_move(self):
        """Coup spécifique pour le jeu Isolation"""
        # d'abord récupérer toutes les positions valides pour un placement
        valid_moves = self.game.get_valid_moves(None)
        
        if not valid_moves:
            return False
            
        # puis il sélectionne une position aléatoire
        destination = random.choice(valid_moves)
        
        # et il exécute le coup sauf cas particulier Isolation
        return self.game.play_turn(None, destination)
    
    def _make_movement_game_move(self):
        """Coup pour les jeux avec déplacement (Katarenga/Congress)"""
        # comme précédemmnent on commence par récupérer toutes les pièces du joueur courant
        player_pieces = self.game.current_player.pieces
        
        if not player_pieces:
            return False
            
        # l'astuce, c'est d'essayer de trouver une pièce qui peut bouger, mélanger toutes ces pièces pour une sélection aléatoire
        random.shuffle(player_pieces)
        
        for piece in player_pieces:
            # il trouve les mouvements valides pour cette pièce
            valid_moves = self.game.get_valid_moves(piece)
            
            if valid_moves:
                # il sélectionne un mouvement aléatoire
                destination = random.choice(valid_moves)
                # il exécute le coup
                return self.game.play_turn(piece.position, destination)
        
        # si aucun coup possible
        return False
