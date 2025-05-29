import tkinter as tk
from ui.widgets.board_canvas import BoardCanvas
from ui.plateau_manager import plateau_manager
from core.class_cadran import Quadrant, QUADRANTS

class BuildScreen(tk.Frame):
    """ Écran de configuration du plateau """

    def __init__(self, master: tk.Tk, controller):
        super().__init__(master)
        self.controller = controller
        self.selected_board_index = tk.IntVar(value=0)  # 0 = plateau standard
        self.build_widgets()
        self.lock_count = 0        # nombre de quadrants verrouillés

    # ------------------------------------------------------------------
    def build_widgets(self):
        tk.Label(
            self,
            text="Configuration du plateau",
            font=("Helvetica", 16, "bold"),
        ).pack(pady=20)

        # --- Section choix du plateau ----------------------------
        board_frame = tk.LabelFrame(self, text="Choix du plateau")
        board_frame.pack(pady=10, padx=50, fill="x")
        
        # obtient tous les plateaux disponibles
        self.available_boards = plateau_manager.get_all_boards()
        
        # ajoute une option pour chaque plateau
        for i, board in enumerate(self.available_boards):
            tk.Radiobutton(
                board_frame,
                text=board["name"],
                variable=self.selected_board_index,
                value=i,
                font=("Helvetica", 12)
            ).pack(anchor="w", pady=5, padx=10)
        
        # --- Aperçu du plateau ---------------------------------
        self.canvas = BoardCanvas(self)
        self.canvas.pack(pady=10)
        
        # --- Boutons d'action ----------------------------------
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        # Démarrage rapide (utilise plateau sélectionné avec orientation par défaut)
        tk.Button(
            button_frame,
            text="Démarrage rapide",
            font=("Helvetica", 12),
            width=20,
            command=self._quick_start
        ).pack(pady=5)
        
        # Configurer l'orientation
        tk.Button(
            button_frame,
            text="Configurer l'orientation",
            font=("Helvetica", 12),
            width=20,
            command=self._goto_orientation
        ).pack(pady=5)
        
        # Éditer nouveau plateau
        tk.Button(
            button_frame,
            text="Éditer un plateau",
            font=("Helvetica", 12),
            width=20,
            command=self._goto_editor
        ).pack(pady=5)
        
        # Retour au menu
        tk.Button(
            button_frame,
            text="Retour au menu",
            font=("Helvetica", 12),
            width=20,
            command=lambda: self.controller.show("menu")
        ).pack(pady=5)
        
        # Retour à l'accueil
        tk.Button(
            button_frame,
            text="Retour à l'accueil",
            font=("Helvetica", 12),
            width=20,
            command=lambda: self.controller.show("welcome")
        ).pack(pady=5)

    def quadrant_locked_callback(self):
        self.lock_count += 1
        if self.lock_count == 4:
            self.start_btn.config(state="normal")   # active le bouton

    def _goto_orientation(self):
        """prépare et passe à l'écran d'orientation"""
        # récupère le plateau sélectionné
        board = self.available_boards[self.selected_board_index.get()]
        
        # stocke les quadrants dans le state
        self.controller.state.selected_quadrants = board["quadrants"]
        
        # passe à l'écran d'orientation
        self.controller.show("orientation")
    
    def _goto_editor(self):
        """passe à l'éditeur de quadrants"""
        self.controller.show("editor")
    
    def _quick_start(self):
        """démarre une partie avec le plateau sélectionné sans modifier l'orientation"""
        # récupère le plateau sélectionné
        board = self.available_boards[self.selected_board_index.get()]
        
        # convertit les quadrants en matrices pour le jeu
        quad_mats = []
        for quadrant in board["quadrants"]:
            mat = []
            for row in range(4):
                mat_row = []
                for col in range(4):
                    # adapte selon le format
                    if hasattr(quadrant.cases[row][col], 'lettre'):
                        mat_row.append(quadrant.cases[row][col].lettre)
                    else:
                        mat_row.append(quadrant.cases[row][col])
                mat.append(mat_row)
            quad_mats.append(mat)
        
        # Récupère le type de jeu et le mode à partir du state global
        game_type = getattr(self.controller.state, "game_type", "katarenga")
        game_mode = getattr(self.controller.state, "game_mode", "local")
        
        # lance la partie
        self.controller.show("game", quad_mats=quad_mats, game_type=game_type, game_mode=game_mode)
