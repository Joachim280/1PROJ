import tkinter as tk
from ui.widgets.board_canvas import BoardCanvas

class OrientationScreen(tk.Frame):
    """écran de configuration de l'orientation des quadrants"""
    
    def __init__(self, master: tk.Tk, controller):
        super().__init__(master)
        self.controller = controller
        
        # récupération des quadrants à partir du state
        self.quadrants = self.controller.state.selected_quadrants
        self.quad_mats = []
        
        # conversion des quadrants en matrices pour le BoardCanvas
        for quadrant in self.quadrants:
            mat = []
            for row in range(4):
                mat_row = []
                for col in range(4):
                    # adapte selon le format (objet Case ou matrice de lettres)
                    if hasattr(quadrant.cases[row][col], 'lettre'):
                        mat_row.append(quadrant.cases[row][col].lettre)
                    else:
                        mat_row.append(quadrant.cases[row][col])
                mat.append(mat_row)
            self.quad_mats.append(mat)
        
        self.build_widgets()
        self.lock_count = 0  # nombre de quadrants verrouillés

    def build_widgets(self):
        tk.Label(
            self,
            text="Configuration de l'orientation",
            font=("Helvetica", 16, "bold"),
        ).pack(pady=20)
        
        # texte explicatif
        tk.Label(
            self,
            text="Cliquez sur chaque quadrant pour configurer son orientation",
            font=("Helvetica", 10)
        ).pack(pady=5)
        
        # canvas du plateau
        self.canvas = BoardCanvas(self)
        self.canvas.pack(pady=10)
        
        # initialisation avec les quadrants sélectionnés
        for i, mat in enumerate(self.quad_mats):
            self.canvas.quad_mats[i] = mat
            
        # redessine le plateau
        self.canvas.draw_quadrants()
        self.canvas.draw_grid()
        
        # bouton pour commencer la partie (je l'active quand tous les quadrant sont verrouillés)
        self.start_btn = tk.Button(
            self,
            text="Commencer la partie",
            font=("Helvetica", 12),
            width=25,
            state="disabled",
            command=self._start_game
        )
        self.start_btn.pack(pady=5)
        
        # bouton de réinitialisation
        tk.Button(
            self,
            text="Réinitialiser les orientations",
            font=("Helvetica", 12),
            width=25,
            command=self._reset_orientations
        ).pack(pady=5)
        
        # bouton de retour
        tk.Button(
            self,
            text="Retour à la configuration",
            font=("Helvetica", 12),
            width=25,
            command=self._goto_build
        ).pack(pady=5)
    
    def quadrant_locked_callback(self):
        """appelé quand un quadrant est verrouillé"""
        self.lock_count += 1
        if self.lock_count == 4:
            self.start_btn.config(state="normal")  # active le bouton
    
    def _reset_orientations(self):
        """réinitialise l'orientation de tous les quadrants"""
        # réinitialise le plateau et le compteur
        self.canvas.reset_board()
        
        # réapplique les quadrants dans leur configuration initiale
        for i, mat in enumerate(self.quad_mats):
            self.canvas.quad_mats[i] = mat
            
        # redessine le plateau
        self.canvas.draw_quadrants()
        self.canvas.draw_grid()
        
        # réinitialise le compteur et désactive le bouton
        self.lock_count = 0
        self.start_btn.config(state="disabled")
    
    def _goto_build(self):
        """retourne à l'écran de configuration du plateau"""
        self.controller.show("build")
    
    def _start_game(self):
        """lance la partie avec les quadrants configurés"""
        # récupère les matrices finales après orientation
        quad_mats = self.canvas.get_quad_mats()
        
        # récupère le type de jeu et le mode à partir du state global
        game_type = getattr(self.controller.state, "game_type", "katarenga")
        game_mode = getattr(self.controller.state, "game_mode", "local")
        
        # si mode réseau et host, envoie d'abord la config au client
        if game_mode == "network":
            network_manager = getattr(self.controller.state, 'network_manager', None)
            network_mode = getattr(self.controller.state, 'network_mode', 'host')
            
            if network_manager and network_mode == "host":
                # envoie la config au client
                network_manager.send_message("setup", {
                    "quadrants": quad_mats,
                    "game_type": game_type
                })
        
        # lance la partie
        self.controller.show("game", quad_mats=quad_mats, game_type=game_type, game_mode=game_mode)
