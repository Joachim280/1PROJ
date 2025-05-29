"""Gestionnaire de plateaux personnalisés - gère le stockage et la récupération de plateaux"""

import pickle
import os
from pathlib import Path
from core.class_cadran import QUADRANTS, Quadrant


class PlateauManager:
    """
    gère les plateaux personnalisés avec sauvegarde/chargement
    stockage: 3 plateaux perso max + plateau par défaut toujours dispo
    """
    
    def __init__(self):
        # dossier pour sauvegarder les plateaux
        self.save_dir = Path("custom_boards")
        self.save_file = self.save_dir / "boards.pickle"
        
        # max 3 plateaux personnalisés + défaut
        self.max_boards = 3
        
        # s'assure que le dossier existe
        self._ensure_save_directory()
        
        # charge les plateaux existants
        self.custom_boards = self._load_boards()
    
    def _ensure_save_directory(self):
        """crée le dossier de sauvegarde s'il n'existe pas"""
        if not self.save_dir.exists():
            self.save_dir.mkdir(parents=True)
    
    def _load_boards(self):
        """charge les plateaux depuis le fichier ou renvoie liste vide si aucun"""
        if not self.save_file.exists():
            return []
        
        try:
            with open(self.save_file, "rb") as f:
                return pickle.load(f)
        except (pickle.PickleError, EOFError, AttributeError) as e:
            # en cas d'erreur, on repart à zéro
            print(f"erreur chargement plateaux: {e}")
            return []
    
    def _save_boards(self):
        """sauvegarde les plateaux dans le fichier pickle"""
        try:
            with open(self.save_file, "wb") as f:
                pickle.dump(self.custom_boards, f)
            return True
        except Exception as e:
            print(f"erreur sauvegarde plateaux: {e}")
            return False
    
    def save_custom_board(self, quadrants):
        """
        sauvegarde un nouveau plateau (ensemble de 4 quadrants)
        applique rotation FIFO (First In First Out) si plus de 3 plateaux
        
        quadrants: liste des 4 objets Quadrant
        """
        # vérifie qu'on a bien 4 quadrants
        if len(quadrants) != 4:
            return False
            
        # ajoute le nouveau plateau
        self.custom_boards.append(quadrants)
        
        # si on dépasse le max, on supprime le plus ancien
        if len(self.custom_boards) > self.max_boards:
            self.custom_boards.pop(0) 
        
        # sauvegarde dans le fichier
        return self._save_boards()
    
    def get_all_boards(self):
        """
        renvoie tous les plateaux disponibles (standard + persos)
        format: liste de dictionnaires avec nom et quadrants
        """
        result = [
            {
                "name": "Plateau standard",
                "quadrants": [Quadrant(QUADRANTS[i+1]) for i in range(4)],
                "is_default": True
            }
        ]
        
        # on ajoute les plateaux personnalisés
        for i, board in enumerate(self.custom_boards):
            result.append({
                "name": f"Plateau personnalisé {i+1}",
                "quadrants": board,
                "is_default": False
            })
        
        return result
    
    def get_board(self, index):
        """
        récupère un plateau spécifique
        index 0 = plateau par défaut
        index 1+ = plateaux personnalisés
        """
        if index == 0:
            # plateau par défaut
            return {
                "name": "Plateau standard",
                "quadrants": [Quadrant(QUADRANTS[i+1]) for i in range(4)],
                "is_default": True
            }
        
        # ajuste l'index pour les plateaux personnalisés
        custom_index = index - 1
        
        if 0 <= custom_index < len(self.custom_boards):
            return {
                "name": f"Plateau personnalisé {custom_index+1}",
                "quadrants": self.custom_boards[custom_index],
                "is_default": False
            }
        
        # fallback au plateau par défaut si l'index est invalide
        return self.get_board(0)
    
    def get_board_count(self):
        """renvoie le nombre total de plateaux disponibles"""
        # +1 pour le plateau par défaut
        return len(self.custom_boards) + 1

# instance singleton
plateau_manager = PlateauManager()
