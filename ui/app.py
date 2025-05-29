"""Infrastructure graphique principale"""

import tkinter as tk
from types import SimpleNamespace  # pour partager le state
from ui.screens.welcome_screen import WelcomeScreen
from ui.screens.menu_screen import MenuScreen
from ui.screens.build_screen import BuildScreen
from ui.screens.game_screen import GameScreen
from ui.screens.quadrant_editor_screen import QuadrantEditorScreen
from ui.screens.orientation_screen import OrientationScreen


class GuiApp:
    """Point d’entrée de l’interface Tkinter
    C'est ici qu'on va ajouter la gestion des différents écrans
    """

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Katarenga")
        self.root.minsize(800, 750)
        
        # dictionnaire des écrans lancés
        self.screens = {}
        self.state = SimpleNamespace(current_screen=None)
        
        # l'écran d'accueil sort dès le départ
        self.show("welcome")

    # ---------- API publique que le reste du code GUI utilisera ----------
    def run(self) -> None:
        """Lance la boucle principale Tkinter"""
        self.root.mainloop()

    def show(self, screen_name: str, **kwargs):
        """Affiche l’écran demandé cliqué/sélectionné

        - screen_name : "menu" | "build" | "game"
        - kwargs : paramètres optionnels passés au nouvel écran (par exemple, quad_mats pour GameScreen)

        Règle de mise en cache :
        - MenuScreen et BuildScreen sont conservés dans self.screens
          pour ne pas recréer leurs widgets à chaque fois
        - GameScreen dépend toujours du plateau transmis : on le
          RECRÉE à chaque appel et on NE le place pas dans le cache
        """
        # 1. d'abord on masque l’écran courant
        if self.state.current_screen is not None:
            self.state.current_screen.pack_forget()

        # 2. ensuite on obtient ou on crée l’écran cible
        if screen_name == "game":
            # toujours une nouvelle partie
            screen = GameScreen(self.root, controller=self, **kwargs)
        else:
            # les écrans persistants (menu / build)
            if screen_name not in self.screens:
                if screen_name == "welcome":
                    self.screens["welcome"] = WelcomeScreen(self.root, controller=self)
                elif screen_name == "menu":
                    self.screens["menu"] = MenuScreen(self.root, controller=self)
                elif screen_name == "build":
                    self.screens["build"] = BuildScreen(self.root, controller=self)
                elif screen_name == "editor":
                    self.screens["editor"] = QuadrantEditorScreen(self.root, controller=self)
                elif screen_name == "orientation":
                    self.screens["orientation"] = OrientationScreen(self.root, controller=self)
                else:
                    raise ValueError(f"Écran inconnu : {screen_name}")
            screen = self.screens[screen_name]

        # 3. puis on afficher l’écran
        screen.pack(fill="both", expand=True)
        self.root.update_idletasks()
        self.root.update()

        # 4. Enfin on mémorise le nouvel écran courant
        self.state.current_screen = screen
        