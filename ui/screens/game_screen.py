import tkinter as tk
from ui.widgets.board_canvas import BoardCanvas
# --- modèle ---
from core.class_plateau import Plateau
from core.katarenga import Katarenga      # version du jeu original
from core.congress import Congress        # version Congress
from core.isolation import Isolation      # version Isolation
from core.player import Player
from core.class_cadran import q1
from core.coordinates import Coordinates
from core.random_ai import RandomAI       # IA aléatoire

class GameScreen(tk.Frame):
    """Plateau + 16 pions ; surbrillance des coups légaux + déplacements"""

    def __init__(self, master, controller, *, quad_mats=None, game_type="katarenga", game_mode="local"):
        super().__init__(master)
        self.controller = controller
        self.game_type = game_type  # stocke le type de jeu
        self.game_mode = game_mode  # stocke le mode de jeu (local/ai)

        if quad_mats is None:
            quad_mats = [[row[:] for row in q1] for _ in range(4)]

        # --- canvas ---
        self.board = BoardCanvas(self, quad_mats=quad_mats)
        # on s'assure que les indicateurs de verrouillage sont effacés au début du jeu
        self.board.delete("locked")
        self.board.pack(pady=20)

        # --- positions initiales ---
        # 1) on crée le plateau 8×8
        plateau = Plateau.from_quadrants(quad_mats)

        # 2) deux joueurs par défaut
        players = [Player("white"), Player("black")]

        # 3) ici on instancie la partie selon le type choisi et on place les pions
        if game_type == "congress":
            self.game = Congress(plateau, players)
            game_label = "Congress"
        elif game_type == "isolation":
            self.game = Isolation(plateau, players)
            game_label = "Isolation"
        else:  # par défaut: katarenga
            self.game = Katarenga(plateau, players)
            game_label = "Katarenga"
            
        self.game.initialize()            # là on appelle _place_pieces() de la sous-classe
        
        # on lance le mode aléatoire quand mode AI
        self.ai = None
        if game_mode == "ai":
            self.ai = RandomAI(self.game)
            # précision de "(vs IA)" au titre
            game_label += " (vs IA)"

        # --- info joueur actif ---
        player_frame = tk.Frame(self)
        player_frame.pack(pady=5)
        
        # mention du jeu actuel
        tk.Label(self, text=game_label, font=("Arial", 16, "bold")).pack(side="top", pady=5)
        
        # msg + indicateur visuel
        self.player_label = tk.Label(player_frame, text="Au tour du joueur : ", font=("Arial", 12))
        self.player_label.pack(side="left")
        
        self.player_indicator = tk.Canvas(player_frame, width=20, height=20, highlightthickness=0)
        self.player_indicator.pack(side="left")
        self.player_indicator.create_oval(2, 2, 18, 18, fill="white", outline="black", width=1)
        
        # indication du tour IA
        if game_mode == "ai":
            self.ai_thinking_label = tk.Label(player_frame, text="", font=("Arial", 12, "italic"))
            self.ai_thinking_label.pack(side="left", padx=10)
        
        # --- contrôles ---
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Retour au menu",
                  command=lambda: controller.show("menu"),
                  font=("Helvetica", 11)
                  ).pack(side="left", padx=10)
                  
        tk.Button(button_frame, text="Abandonner",
                  command=self._forfeit_game,
                  font=("Helvetica", 11)
                  ).pack(side="left", padx=10)

        # 4) désormais on peut déssiner les pièces depuis le plateau réel
        self._draw_pieces()

        # --- interaction utilisateur --------
        # désactive le handler par défaut de BoardCanvas qui interfère avec nos clics
        self.board.unbind("<Button-1>")
        # puis ajoute notre propre gestionnaire de clic
        self.board.bind("<Button-1>", self._on_click)
        self.selected_piece = None      
        
        # initialise l'indicateur de joueur
        self._update_player_indicator()
        
        # pour Isolation, on affiche directement les cases valides 
        if game_type == "isolation":
            moves = self.game.get_valid_moves(None)
            squares = [(m.x, m.y) for m in moves]
            self.board.highlight_moves(squares)
            
        # Lance le premier coup de l'IA si c'est à son tour
        if game_mode == "ai" and self.game.current_player == self.game.players[1]:
            self._schedule_ai_move()

#-------------------------------------------------------------------
    def _on_click(self, event):
        """Gère les clics sur le plateau : sélection + déplacement des pions ou placement"""
        # ignore si partie terminée
        if self.game.game_over:
            return
            
        # vérifie que c'est le tour du joueur humain si mode AI
        if self.game_mode == "ai" and self.game.current_player == self.game.players[1]:
            return  # c'est au tour de l'IA, ignore le clic
            
        # converti px en coordonnées de grille
        row = event.y // self.board.CELL
        col = event.x // self.board.CELL
        
        # vérifie que les coordonnées sont sur le plateau
        if not (0 <= row < 8 and 0 <= col < 8):
            return
            
        # Gestion spéciale pour le jeu Isolation (mode placement)
        if self.game_type == "isolation":
            self._handle_isolation_click(row, col)
            return
            
        # --- implémentation pour les jeux avec déplacement (Katarenga/Congress) ---
        cell = self.game.board.cases[row][col]
        piece = getattr(cell, "pion", None) if cell else None
        
        # first clic – sélectionner un pion du joueur actuel
        if self.selected_piece is None:
            if piece and piece.player == self.game.current_player:
                self.selected_piece = piece
                # highlight des coups légaux
                moves = self.game.get_valid_moves(piece)
                squares = [(m.x, m.y) for m in moves] 
                self.board.highlight_moves(squares)
                # on badge aussi le pion sélectionné (TODO)
        
        # 2ème clic – tenter le déplacement
        else:
            dest = Coordinates(row, col)
            
            # vérifie si le déplacement est légal
            if dest in self.game.get_valid_moves(self.selected_piece):
                # exécute le coup
                from_coord = self.selected_piece.position
                success = self.game.play_turn(from_coord, dest)
                
                if success:
                    # mise à jour visuelle
                    self.selected_piece = None
                    self.board.delete("hl")
                    self._draw_pieces()
                    
                    # vérifie si le jeu est terminé
                    if self.game.game_over:
                        self._show_victory()
                    else:
                        # mise à jour indicateur joueur actif
                        self._update_player_indicator()
                        
                        # lance le tour de l'IA si nécessaire
                        if self.game_mode == "ai" and self.game.current_player == self.game.players[1]:
                            self._schedule_ai_move()
            else:
                # clic sur une case inaccessible -> désélection
                self.selected_piece = None
                self.board.delete("hl")
                
    def _handle_isolation_click(self, row, col):
        """Gère les clics pour le jeu Isolation (mode placement)"""
        dest = Coordinates(row, col)
        
        # Au démarrage, on affiche les cases valides
        if not self.board.find_withtag("hl"):
            # calcule et affiche tous les emplacements valides
            moves = self.game.get_valid_moves(None)  # car pas de pièce sélectionnée
            squares = [(m.x, m.y) for m in moves]
            self.board.highlight_moves(squares)
        
        # on tente de placer un pion
        if dest in self.game.get_valid_moves(None):
            # pour Isolation, from_coord n'est pas utilisé (None)
            success = self.game.play_turn(None, dest)
            
            if success:
                # mise à jour visuelle
                self.board.delete("hl")
                self._draw_pieces()
                
                # vérifie si le jeu est terminé
                if self.game.game_over:
                    self._show_victory()
                else:
                    # mise à jour indicateur joueur actif
                    self._update_player_indicator()
                    
                    # affiche les nouveaux emplacements valides
                    moves = self.game.get_valid_moves(None)
                    squares = [(m.x, m.y) for m in moves]
                    self.board.highlight_moves(squares)
                    
                    # lance le tour de l'IA si nécessaire
                    if self.game_mode == "ai" and self.game.current_player == self.game.players[1]:
                        self._schedule_ai_move()
     
    def _update_player_indicator(self):
        """Met à jour l'indicateur visuel du joueur actif"""
        color = self.game.current_player.color
        # efface l'ancien indicateur
        self.player_indicator.delete("all")
        # dessine le nouvel indicateur
        fill_color = "white" if color == "white" else "#222222"
        self.player_indicator.create_oval(2, 2, 18, 18, fill=fill_color, outline="black", width=1)
        
        # mise à jour du texte IA quand il faut
        if self.game_mode == "ai":
            if self.game.current_player == self.game.players[1]:  # ici, IA = joueur noir
                self.ai_thinking_label.config(text="(IA réfléchit...)")
            else:
                self.ai_thinking_label.config(text="")
    
    def _schedule_ai_move(self):
        """Planifie un coup de l'IA avec un délai artificiel pour fluidité"""
        # met à jour le label
        if hasattr(self, "ai_thinking_label"):
            self.ai_thinking_label.config(text="(IA réfléchit...)")
            
        # délai manuel pour rendre le jeu plus fluide
        self.after(800, self._execute_ai_move)
        
    def _execute_ai_move(self):
        """Exécute un coup de l'IA"""
        if self.game.game_over:
            return
            
        if self.ai:
            # efface la surbrillance actuelle
            self.board.delete("hl")
            
            # exécute le coup de l'IA
            success = self.ai.make_move()
            
            # mise à jour visuelle
            self._draw_pieces()
            
            if hasattr(self, "ai_thinking_label"):
                self.ai_thinking_label.config(text="")
            
            # on vérifie si le jeu est terminé
            if self.game.game_over:
                self._show_victory()
            else:
                # on met à jour l'indicateur du joueur actif
                self._update_player_indicator()
                
                # si c'est Isolation, affiche les nouveaux emplacements valides
                if self.game_type == "isolation":
                    moves = self.game.get_valid_moves(None)
                    squares = [(m.x, m.y) for m in moves]
                    self.board.highlight_moves(squares)
    
    def _forfeit_game(self):
        """Le joueur actuel abandonne, l'adversaire gagne"""
        if self.game.game_over:
            return
            
        # marque la partie comme terminée
        self.game.game_over = True
        # change le joueur actif pour donner la victoire à l'adversaire
        self.game.switch_player()
        # affiche la victoire
        self._show_victory(forfeit=True)
     
    def _show_victory(self, forfeit=False):
        """Affiche le popup de victoire et propose de rejouer"""
        # popup modal
        popup = tk.Toplevel(self)
        popup.title("Fin de partie")
        popup.geometry("300x250") 
        popup.resizable(False, False)
        popup.transient(self)  # on l'affiche en mode modal pour bloquer ui principale
        
        # message de victoire
        winner = "blanc" if self.game.current_player.color == "white" else "noir"
        if forfeit:
            message = f"Le joueur {winner} a gagné par abandon !"
        else:
            message = f"Le joueur {winner} a gagné !"
        tk.Label(popup, text=message, font=("Arial", 14, "bold")).pack(pady=20)
        
        # boutons en disposition verticale
        button_width = 20 
        
        tk.Button(
            popup, 
            text="Nouvelle partie",
            width=button_width,
            font=("Helvetica", 11),
            command=lambda: [popup.destroy(), self.controller.show("build")]
        ).pack(pady=6)
        
        tk.Button(
            popup, 
            text="Menu principal",
            width=button_width,
            font=("Helvetica", 11),
            command=lambda: [popup.destroy(), self.controller.show("menu")]
        ).pack(pady=6)
        
        tk.Button(
            popup, 
            text="Retour à l'accueil",
            width=button_width,
            font=("Helvetica", 11),
            command=lambda: [popup.destroy(), self.controller.show("welcome")]
        ).pack(pady=6)
     
            
#-------------------------------------------------------------------
    def _draw_pieces(self):
        """Parcourt le plateau et dessine tous les pions présents"""
        positions = []
        
        # parcours toutes les cases du plateau
        for r, row in enumerate(self.game.board.cases):
            for c, cell in enumerate(row):
                if cell is None:
                    continue
                    
                # récupère le pion de la case s'il existe
                piece = getattr(cell, "pion", None)
                if piece is None:
                    continue
                    
                # récupère la couleur du joueur
                color = piece.player.color
                positions.append((r, c, color))
                
        # demande au canvas de dessiner tous les pions
        self.board.draw_pieces(positions)


