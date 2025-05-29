import tkinter as tk

class WelcomeScreen(tk.Frame):
    """écran d'accueil initial avec choix nouvelle partie ou continuation"""

    def __init__(self, master: tk.Tk, controller):
        """
        master      → fenêtre principale (root)
        controller  → instance de GuiApp pour appeler controller.show()
        """
        super().__init__(master)
        self.controller = controller
        self.build_widgets()

    def build_widgets(self):
        # conteneur principal et centrage
        main_container = tk.Frame(self)
        main_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # titre en gros et gras
        tk.Label(
            main_container, 
            text="KATARENGA",
            font=("Helvetica", 42, "bold")
        ).pack(pady=20)
        
        # sous-titre descriptif
        tk.Label(
            main_container,
            text="Un jeu de stratégie combinatoire abstrait",
            font=("Helvetica", 14)
        ).pack(pady=5)
        
        # cadre pour les boutons 
        button_frame = tk.Frame(main_container, padx=30, pady=30)
        button_frame.pack(pady=20)
        
        # boutons centrés et de même taille
        button_width = 25
        button_font = ("Helvetica", 12)
        
        # nouvelle partie → menu principal
        tk.Button(
            button_frame,
            text="Nouvelle partie",
            width=button_width,
            font=button_font,
            command=self._goto_menu
        ).pack(pady=10)
        
        # continuer (désactivé pour l'instant)
        tk.Button(
            button_frame,
            text="Continuer une partie",
            width=button_width,
            font=button_font,
            state="disabled"
        ).pack(pady=10)
        
        # quitter
        tk.Button(
            button_frame,
            text="Quitter",
            width=button_width,
            font=button_font,
            command=self.controller.root.quit
        ).pack(pady=10)
        
        # signature projet
        tk.Label(
            self,
            text="© 2025 - Projet GUI - Joachim, Mathiew, Job",
            font=("Helvetica", 8)
        ).pack(side="bottom", pady=10)
        
    def _goto_menu(self):
        """passe au menu principal"""
        self.controller.show("menu")
