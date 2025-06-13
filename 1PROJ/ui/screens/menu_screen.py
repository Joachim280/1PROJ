import tkinter as tk

class MenuScreen(tk.Frame):
    """Écran d'accueil : titre + sélection du jeu + boutons"""

    def __init__(self, master: tk.Tk, controller):
        """
        master      → fenêtre principale (root)
        controller  → instance de GuiApp pour appeler controller.show()
        """
        super().__init__(master)
        self.controller = controller
        self.selected_game = tk.StringVar(value="katarenga")
        self.selected_mode = tk.StringVar(value="local")  # mode de jeu par défaut
        self.build_widgets()

    # ------------------------------------------------------------------
    def build_widgets(self):
        # Titre
        tk.Label(self, text="Smart Games", font=("Helvetica", 24, "bold")).pack(pady=20)
        
        # Cadre sélection du jeu
        game_frame = tk.LabelFrame(self, text="Sélectionner un jeu", padx=20, pady=10)
        game_frame.pack(pady=10, fill="x", padx=50)
        
        # Radios options de jeu
        tk.Radiobutton(
            game_frame, 
            text="Katarenga - Occuper deux camps adverses",
            variable=self.selected_game,
            value="katarenga",
            font=("Helvetica", 12)
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            game_frame, 
            text="Congress - Connecter tous vos pions",
            variable=self.selected_game,
            value="congress",
            font=("Helvetica", 12)
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            game_frame, 
            text="Isolation - Placement sans mise en échec",
            variable=self.selected_game,
            value="isolation",
            font=("Helvetica", 12)
        ).pack(anchor="w", pady=5)
        
        # Cadre pour le mode de jeu
        mode_frame = tk.LabelFrame(self, text="Mode de jeu", padx=20, pady=10)
        mode_frame.pack(pady=10, fill="x", padx=50)
        
        # Radios options de mode
        tk.Radiobutton(
            mode_frame,
            text="2 joueurs (local)",
            variable=self.selected_mode,
            value="local",
            font=("Helvetica", 12)
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            mode_frame,
            text="Contre IA (coups aléatoires)",
            variable=self.selected_mode,
            value="ai",
            font=("Helvetica", 12)
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            mode_frame,
            text="2 joueurs (réseau)",
            variable=self.selected_mode,
            value="network",
            font=("Helvetica", 12)
        ).pack(anchor="w", pady=5)

        # Cadre boutons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        # Bouton Configurer plateau
        tk.Button(
            button_frame,
            text="Configurer le plateau",
            width=20,
            font=("Helvetica", 12),
            command=self._goto_build
        ).pack(side="left", padx=10)
        
        # Bouton Retour
        tk.Button(
            button_frame,
            text="Retour à l'accueil",
            width=20,
            font=("Helvetica", 12),
            command=self._goto_welcome
        ).pack(side="left", padx=10)
        
        # Bouton Quitter
        tk.Button(
            button_frame, 
            text="Quitter", 
            width=20,
            font=("Helvetica", 12),
            command=self.controller.root.quit
        ).pack(side="left", padx=10)
        
    def _goto_build(self):
        """Transmet le type de jeu et le mode sélectionnés à BuildScreen via state"""
        # Stocke les paramètres dans le state global
        self.controller.state.game_type = self.selected_game.get()
        self.controller.state.game_mode = self.selected_mode.get()
        
        # si mode réseau, on va d'abord à l'écran network
        if self.selected_mode.get() == "network":
            self.controller.show("network")
        else:
            self.controller.show("build")
        
    def _goto_welcome(self):
        """retourne à l'écran d'accueil"""
        self.controller.show("welcome")