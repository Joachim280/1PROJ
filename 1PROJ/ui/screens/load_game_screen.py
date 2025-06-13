"""écran simple pour continuer les parties sauvegardées"""

import tkinter as tk
from tkinter import messagebox
from ui.save_manager import SaveManager, restore_game_state


class LoadGameScreen(tk.Frame):
    """interface simple pour continuer les jeux sauvegardés"""
    
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.save_manager = SaveManager()
        
        # titre
        title = tk.Label(self, text="Continuer une partie", font=("Arial", 18, "bold"))
        title.pack(pady=30)
        
        # frame pour les boutons de jeux
        games_frame = tk.Frame(self)
        games_frame.pack(pady=20)
        
        self.game_buttons = []
        self._create_game_buttons(games_frame)
        
        # bouton retour
        tk.Button(self, text="Retour à l'accueil",
                  command=lambda: controller.show("welcome"),
                  font=("Helvetica", 12)
                  ).pack(pady=30)
    
    def _create_game_buttons(self, parent):
        """crée les boutons pour chaque jeu sauvegardé"""
        available_saves = self.save_manager.get_available_saves()
        
        if not available_saves:
            # normalement on ne devrait pas arriver ici car le bouton est grisé
            tk.Label(parent, text="Aucune partie sauvegardée", 
                    font=("Arial", 14), fg="gray").pack(pady=20)
            return
        
        for save_info in available_saves:
            game_type = save_info['game_type']
            display_name = save_info['display_name']
            date = save_info['date']
            current_player = save_info['current_player']
            
            # texte du bouton avec infos
            button_text = f"{display_name}\n(tour de {current_player})\nSauvé le {date}"
            
            btn = tk.Button(parent, 
                           text=button_text,
                           font=("Helvetica", 11),
                           width=25, height=4,
                           command=lambda gt=game_type: self._load_game(gt))
            btn.pack(pady=10)
            self.game_buttons.append(btn)
    
    def _load_game(self, game_type):
        """charge la partie du type de jeu spécifié"""
        success = restore_game_state(game_type, self.controller)
        if not success:
            messagebox.showerror("Erreur", f"Impossible de charger la partie {game_type}")

