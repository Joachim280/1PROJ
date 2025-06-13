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
        # callback pour mettre à jour l'aperçu quand on change de sélection
        self.selected_board_index.trace("w", self._update_preview)

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

        # frame pour stocker les radiobuttons (pour pouvoir les recréer)
        self.board_selection_frame = tk.Frame(board_frame)
        self.board_selection_frame.pack(fill="x")

        # charge la liste des plateaux et crée les options
        self._refresh_board_list()
        
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
        board_index = self.selected_board_index.get()
        board = self.available_boards[board_index]
        
        # stocke les quadrants ET l'index dans le state
        self.controller.state.selected_quadrants = board["quadrants"]
        self.controller.state.selected_board_index = board_index
        
        # passe à l'écran d'orientation
        self.controller.show("orientation")
    
    def _goto_editor(self):
        """passe à l'éditeur de quadrants"""
        self.controller.show("editor")
    
    def _quick_start(self):
        """démarre une partie avec le plateau sélectionné sans modifier l'orientation"""
        # récupère le plateau sélectionné
        board_index = self.selected_board_index.get()
        board = self.available_boards[board_index]
        
        # stocke l'index du plateau dans le state pour la sauvegarde
        self.controller.state.selected_board_index = board_index
        
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

    def _update_preview(self, *args):
        """met à jour l'aperçu du plateau quand on change de sélection"""
        try:
            board_index = self.selected_board_index.get()
            if 0 <= board_index < len(self.available_boards):
                board = self.available_boards[board_index]
                # convertit les quadrants en matrices pour l'affichage
                quad_mats = self._convert_quadrants_to_matrices(board["quadrants"])
                # met à jour le canvas avec le nouveau plateau
                self.canvas.quad_mats = quad_mats
                self.canvas.draw_quadrants()
                self.canvas.draw_grid()
        except Exception as e:
            # en cas d'erreur, on utilise le plateau par défaut
            print(f"erreur preview: {e}")
            self._show_default_preview()

    def _convert_quadrants_to_matrices(self, quadrants):
        """convertit une liste de quadrants en matrices pour l'affichage"""
        quad_mats = []
        for quadrant in quadrants:
            mat = []
            for row in range(4):
                mat_row = []
                for col in range(4):
                    # adapte selon le format (objet Case ou lettre directe)
                    if hasattr(quadrant.cases[row][col], 'lettre'):
                        mat_row.append(quadrant.cases[row][col].lettre)
                    else:
                        mat_row.append(quadrant.cases[row][col])
                mat.append(mat_row)
            quad_mats.append(mat)
        return quad_mats

    def _show_default_preview(self):
        """affiche l'aperçu du plateau par défaut en cas d'erreur"""
        default_quadrants = [Quadrant(QUADRANTS[i+1]) for i in range(4)]
        quad_mats = self._convert_quadrants_to_matrices(default_quadrants)
        self.canvas.quad_mats = quad_mats
        self.canvas.draw_quadrants()
        self.canvas.draw_grid()

    def _refresh_board_list(self):
        """recharge la liste des plateaux depuis le manager et recrée les radiobuttons"""
        # on supprime tous les anciens radiobuttons
        for widget in self.board_selection_frame.winfo_children():
            widget.destroy()
        
        # on recharge la liste des plateaux
        self.available_boards = plateau_manager.get_all_boards()
        
        # on ajoute une option pour chaque plateau
        for i, board in enumerate(self.available_boards):
            tk.Radiobutton(
                self.board_selection_frame,
                text=board["name"],
                variable=self.selected_board_index,
                value=i,
                font=("Helvetica", 12)
            ).pack(anchor="w", pady=5, padx=10)

    def refresh_after_edit(self):
        """méthode appelée après édition d'un plateau pour rafraîchir l'affichage"""
        # on recharge la liste des plateaux
        self._refresh_board_list()
        
        # on sélectionne automatiquement le dernier plateau créé (index le plus élevé)
        if len(self.available_boards) > 1:  # s'il y a des plateaux perso
            self.selected_board_index.set(len(self.available_boards) - 1)
        
        
