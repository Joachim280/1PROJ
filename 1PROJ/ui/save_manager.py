"""gestion des sauvegardes de parties"""

import os
import pickle
from datetime import datetime


class SaveManager:
    """gestionaire des sauvegardes de parties en cours - 3 slots fixes"""
    
    def __init__(self):
        # crée le dossier saves s'il existe pas
        self.save_dir = "saves"
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
        
        # les 3 slots fixes pour chaque jeu
        self.save_files = {
            'katarenga': 'katarenga.sav',
            'congress': 'congress.sav', 
            'isolation': 'isolation.sav'
        }
    
    def save_game(self, game_state):
        """sauvegarde une partie dans le slot correspondant au type de jeu"""
        game_type = game_state.get('game_type', 'katarenga')
        
        if game_type not in self.save_files:
            print(f"type de jeu inconnu : {game_type}")
            return False
            
        save_file = self.save_files[game_type]
        save_path = os.path.join(self.save_dir, save_file)
        
        try:
            with open(save_path, 'wb') as f:
                pickle.dump(game_state, f)
            return True
        except Exception as e:
            print(f"erreur sauvegarde : {e}")
            return False
    
    def load_game(self, game_type):
        """charge la partie sauvegardée pour un type de jeu"""
        if game_type not in self.save_files:
            return None
            
        save_file = self.save_files[game_type]
        save_path = os.path.join(self.save_dir, save_file)
        
        try:
            with open(save_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"erreur chargement : {e}")
            return None
    
    def get_available_saves(self):
        """récupère la liste des jeux qui ont une sauvegarde active"""
        from ui.plateau_manager import plateau_manager
        available = []
        
        for game_type, filename in self.save_files.items():
            save_path = os.path.join(self.save_dir, filename)
            
            if os.path.exists(save_path):
                try:
                    # récupère infos du fichier
                    stat = os.stat(save_path)
                    date_save = datetime.fromtimestamp(stat.st_mtime)
                    
                    # charge l'état pour récupérer infos partie
                    with open(save_path, 'rb') as f:
                        game_state = pickle.load(f)
                    
                    # ignore les parties terminées
                    if game_state.get('game_over', False):
                        # supprime automatiquement la sauvegarde obsolète
                        self.delete_save(game_type)
                        continue
                    
                    # vérifie si le plateau utilisé existe encore
                    board_index = game_state.get('board_index', 0)  # 0 = plateau par défaut
                    if board_index > 0:  # plateau personnalisé
                        total_boards = plateau_manager.get_board_count()
                        if board_index >= total_boards:
                            # plateau personnalisé supprimé par FIFO
                            print(f"supprime sauvegarde {game_type} : plateau perso #{board_index} n'existe plus")
                            self.delete_save(game_type)
                            continue
                    
                    available.append({
                        'game_type': game_type,
                        'display_name': game_type.capitalize(),
                        'date': date_save.strftime("%d/%m/%Y à %H:%M"),
                        'current_player': game_state.get('current_player_color', 'inconnu')
                    })
                except Exception as e:
                    print(f"fichier corrompu pour {game_type}: {e}")
                    continue
        
        return available
    
    def has_any_save(self):
        """vérifie s'il y a au moins une sauvegarde"""
        return len(self.get_available_saves()) > 0
    
    def delete_save(self, game_type):
        """supprime la sauvegarde d'un jeu spécifique"""
        if game_type not in self.save_files:
            return False
            
        save_file = self.save_files[game_type]
        save_path = os.path.join(self.save_dir, save_file)
        
        try:
            if os.path.exists(save_path):
                os.remove(save_path)
                return True
        except Exception as e:
            print(f"erreur suppression : {e}")
        return False


# fonction helper pour sérialiser l'état du jeu
def create_game_state(game_screen):
    """crée un dictionnaire avec tout l'état de la partie"""
    game = game_screen.game
    
    # récupère l'index du plateau utilisé depuis le controller state
    board_index = getattr(game_screen.controller.state, 'selected_board_index', 0)
    
    # récupère les positions de toutes les pièces
    pieces_data = []
    for r, row in enumerate(game.board.cases):
        for c, cell in enumerate(row):
            if cell and hasattr(cell, 'pion') and cell.pion:
                piece = cell.pion
                pieces_data.append({
                    'position': [r, c],
                    'player_color': piece.player.color,
                    'in_camp': piece.in_camp
                })
    
    # état complet du jeu
    state = {
        'game_type': game_screen.game_type,
        'game_mode': game_screen.game_mode,
        'quad_mats': game_screen.board.quad_mats,  # config plateau
        'board_index': board_index,  # index du plateau utilisé
        'pieces': pieces_data,
        'current_player_color': game.current_player.color,
        'current_player_index': 0 if game.current_player.color == 'white' else 1,
        'game_over': game.game_over,
        'save_date': datetime.now().isoformat()
    }
    
    return state


def restore_game_state(game_type, controller):
    """restaure une partie à partir du type de jeu"""
    save_manager = SaveManager()
    state = save_manager.load_game(game_type)
    
    if not state:
        return False
        
    try:
        # recrée le jeu avec les bonnes classes
        from core.katarenga import Katarenga
        from core.congress import Congress
        from core.isolation import Isolation
        from core.class_plateau import Plateau
        from core.player import Player
        from core.piece import Piece
        from core.coordinates import Coordinates
        
        # recrée le plateau
        plateau = Plateau.from_quadrants(state['quad_mats'])
        
        # recrée les joueurs
        players = [Player("white"), Player("black")]
        
        # instancie le bon type de jeu selon l'état sauvé
        saved_game_type = state['game_type']
        if saved_game_type == "congress":
            game = Congress(plateau, players)
        elif saved_game_type == "isolation":
            game = Isolation(plateau, players)
        else:
            game = Katarenga(plateau, players)
        
        # vide le plateau d'abord (au cas où il y aurait des pièces par défaut)
        for r in range(8):
            for c in range(8):
                if plateau.cases[r][c] and hasattr(plateau.cases[r][c], 'pion'):
                    plateau.cases[r][c].pion = None
        
        # vide aussi les listes de pièces des joueurs
        players[0].pieces = []
        players[1].pieces = []
        
        # recrée les pièces selon l'état sauvé
        for piece_data in state['pieces']:
            pos = Coordinates(piece_data['position'][0], piece_data['position'][1])
            player = players[0] if piece_data['player_color'] == 'white' else players[1]
            
            piece = Piece(pos, player)
            piece.in_camp = piece_data['in_camp']
            
            # place la pièce sur le plateau
            cell = plateau.cases[pos.x][pos.y]
            if cell:
                cell.pion = piece
            
            # ajoute la pièce à la liste du joueur
            player.pieces.append(piece)
        
        # restaure l'état du jeu
        game.current_player = players[state['current_player_index']]
        game.game_over = state['game_over']
        
        # lance l'écran de jeu avec l'état restauré
        controller.show("game", 
                       quad_mats=state['quad_mats'],
                       game_type=saved_game_type,
                       game_mode=state['game_mode'],
                       restored_game=game)
        
        return True
        
    except Exception as e:
        print(f"erreur restauration : {e}")
        import traceback
        traceback.print_exc()  # debug plus détaillé
        return False
