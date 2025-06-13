import tkinter as tk
from core.class_cadran import Quadrant

class QuadrantEditorScreen(tk.Frame):
    """
    Écran d'édition de quadrants personnalisés
    Permet de créer jusqu'à 4 quadrants, chacun avec 4 cases par couleur
    """
    
    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller
        self.current_color = tk.StringVar(value="B")  # couleur sélectionnée (B, R, V, J)
        self.current_quadrant = 0  # quadrant actuellement édité (0 à 3)
        
        # matrice 4x4 pour chaque quadrant - initialement sans couleur
        self.quadrant_data = [
            [['' for _ in range(4)] for _ in range(4)],  # Quadrant 1
            [['' for _ in range(4)] for _ in range(4)],  # Quadrant 2
            [['' for _ in range(4)] for _ in range(4)],  # Quadrant 3
            [['' for _ in range(4)] for _ in range(4)]   # Quadrant 4
        ]
        
        # Compteurs pour chaque couleur par quadrant - initialement tout à zéro
        self.color_counts = [
            {'B': 0, 'R': 0, 'V': 0, 'J': 0},  # Quadrant 1
            {'B': 0, 'R': 0, 'V': 0, 'J': 0},  # Quadrant 2
            {'B': 0, 'R': 0, 'V': 0, 'J': 0},  # Quadrant 3
            {'B': 0, 'R': 0, 'V': 0, 'J': 0}   # Quadrant 4
        ]
        
        self.build_widgets()
        self.update_color_counters()
    
    def build_widgets(self):
        # Titre
        tk.Label(
            self, 
            text="Éditeur de Quadrants", 
            font=("Helvetica", 18, "bold")
        ).pack(pady=10)
        
        # instructions
        tk.Label(
            self,
            text="Chaque quadrant doit contenir exactement 4 cases de chaque couleur",
            font=("Helvetica", 10, "italic")
        ).pack(pady=5)
        
        # cadre principale
        main_frame = tk.Frame(self)
        main_frame.pack(pady=10, padx=20)
        
        # panneau de gauche (quadrants + sélecteur)
        left_panel = tk.Frame(main_frame)
        left_panel.pack(side="left", padx=20)
        
        # sélecteur de quadrant
        selector_frame = tk.Frame(left_panel)
        selector_frame.pack(pady=10)
        
        tk.Label(
            selector_frame,
            text="Quadrant en édition :"
        ).pack(side="left", padx=5)
        
        self.quadrant_selector = tk.Scale(
            selector_frame,
            from_=1,
            to=4,
            orient="horizontal",
            command=self._change_quadrant
        )
        self.quadrant_selector.pack(side="left", padx=5)
        
        # zone d'édition
        edit_frame = tk.Frame(left_panel)
        edit_frame.pack(pady=10)
        
        # grille 4x4 pour l'édition
        self.grid_frame = tk.Frame(edit_frame)
        self.grid_frame.pack(pady=10)
        
        # création initiale des boutons
        self._rebuild_grid()
        
        # les boutons de gestion de quadant
        quad_buttons_frame = tk.Frame(left_panel)
        quad_buttons_frame.pack(pady=10)
        
        tk.Button(
            quad_buttons_frame,
            text="Réinitialiser ce quadrant",
            command=self._reset_current_quadrant
        ).pack(side="left", padx=5)
        
        # les contrôles (à droite)
        control_frame = tk.Frame(main_frame)
        control_frame.pack(side="left", padx=20, fill="y")
        
        # pour la sélection de couleur
        color_frame = tk.LabelFrame(control_frame, text="Sélectionner une couleur")
        color_frame.pack(pady=10, fill="x")
        
        # radios de couleur
        colors = [
            ("Bleu", "B", "#4a90e2"),
            ("Rouge", "R", "#d9534f"),
            ("Vert", "V", "#5cb85c"),
            ("Jaune", "J", "#f0ad4e")
        ]
        
        for text, value, color in colors:
            rb = tk.Radiobutton(
                color_frame,
                text=text,
                variable=self.current_color,
                value=value,
                bg=color,
                selectcolor=color,
                width=15
            )
            rb.pack(anchor="w", pady=3, padx=5)
        
        # compteurs de couleurs par quadrant
        quad_counter_frame = tk.LabelFrame(control_frame, text="Nombre de cases (Quadrant actuel)")
        quad_counter_frame.pack(pady=10, fill="x")
        
        self.quad_counter_labels = {}
        for text, value, color in colors:
            frame = tk.Frame(quad_counter_frame)
            frame.pack(anchor="w", pady=3, fill="x")
            
            tk.Label(frame, text=f"{text}:", width=6, anchor="w").pack(side="left", padx=5)
            lbl = tk.Label(frame, text="0/4", width=3)
            lbl.pack(side="left", padx=5)
            
            self.quad_counter_labels[value] = lbl
        
        # compteurs de couleurs globaux
        global_counter_frame = tk.LabelFrame(control_frame, text="Nombre de cases (Total)")
        global_counter_frame.pack(pady=10, fill="x")
        
        self.global_counter_labels = {}
        for text, value, color in colors:
            frame = tk.Frame(global_counter_frame)
            frame.pack(anchor="w", pady=3, fill="x")
            
            tk.Label(frame, text=f"{text}:", width=6, anchor="w").pack(side="left", padx=5)
            lbl = tk.Label(frame, text="0/16", width=4)
            lbl.pack(side="left", padx=5)
            
            self.global_counter_labels[value] = lbl
        
        # boutons action
        button_frame = tk.Frame(control_frame)
        button_frame.pack(pady=20, fill="x")
        
        tk.Button(
            button_frame,
            text="Réinitialiser tous les quadrants",
            font=("Helvetica", 11),
            command=self._reset_all_quadrants
        ).pack(fill="x", pady=5)
        
        self.save_button = tk.Button(
            button_frame,
            text="Enregistrer les quadrants",
            font=("Helvetica", 11),
            command=self._save_quadrants,
            state="disabled"  # on l'active seulement quand valide
        )
        self.save_button.pack(fill="x", pady=5)
        
        tk.Button(
            button_frame,
            text="Retour à la configuration",
            font=("Helvetica", 11),
            command=lambda: self.controller.show("build")
        ).pack(fill="x", pady=5)
        
        tk.Button(
            button_frame,
            text="Retour au menu principal",
            font=("Helvetica", 11),
            command=lambda: self.controller.show("menu")
        ).pack(fill="x", pady=5)
        
    def _rebuild_grid(self):
        """Reconstruit entièrement la grille avec des canvas au lieu des boutons"""
        # on supprime tous les widgets existants
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        
        # pour recréer ensuite toutes les cellules avec des canvas
        self.cells = []
        for row in range(4):
            cell_row = []
            for col in range(4):
                letter = self.quadrant_data[self.current_quadrant][row][col]
                color = self._letter_to_color(letter) if letter in ['B', 'R', 'V', 'J'] else "#ffffff"
                
                # pour chaque cellule 
                cell = tk.Canvas(
                    self.grid_frame,
                    width=40, height=40,
                    bg=color,
                    highlightthickness=1,
                    highlightbackground="black"
                )
                cell.grid(row=row, column=col, padx=2, pady=2)
                
                # bindage du clic pour changer la couleur
                cell.bind("<Button-1>", 
                         lambda event, r=row, c=col: self._change_cell_color(r, c))
                
                cell_row.append(cell)
            self.cells.append(cell_row)
        
        # renforcer la mise à jour de l'affichage
        self.grid_frame.update()
    
    def _letter_to_color(self, letter):
        """Convertit un code lettre en couleur hexadécimale"""
        color_map = {
            'B': "#4a90e2",  
            'R': "#d9534f",
            'V': "#5cb85c",
            'J': "#f0ad4e"
        }
        return color_map.get(letter, "#ffffff")  # blanc par défaut
    
    def _change_cell_color(self, row, col, event=None):
        """Change la couleur d'une cellule de la grille (version canvas)"""
        # d'abord, obtenir la lettre actuelle et la nouvelle
        current_letter = self.quadrant_data[self.current_quadrant][row][col]
        new_letter = self.current_color.get()
        
        # on a déjà 4 cases de la nouvelle couleur, on bloque
        if self.color_counts[self.current_quadrant][new_letter] >= 4:
            return
            
        # mise à jour les compteurs
        if current_letter in ['B', 'R', 'V', 'J']:  
            self.color_counts[self.current_quadrant][current_letter] -= 1
        
        # ajout de la nouvelle couleur au compteur
        self.color_counts[self.current_quadrant][new_letter] += 1
        
        # mise à jour la matrice
        self.quadrant_data[self.current_quadrant][row][col] = new_letter
        
        # on change directement la couleur du canvas sans reconstruire
        color_hex = self._letter_to_color(new_letter)
        self.cells[row][col].config(bg=color_hex)
        
        # on effectue le rafraîchissement
        self.cells[row][col].update()
        
        # mise à jour les compteurs
        self.update_color_counters()
        
        # enfin on met à jour l'état du bouton Enregistrer
        self._update_save_button()
    
    def _change_quadrant(self, value):
        """Change le quadrant en cours d'édition"""
        # on doit convertir la valeur de l'échelle (1-4) en index (0-3)
        old_quadrant = self.current_quadrant
        self.current_quadrant = int(value) - 1
        
        # reconstruire la grille avec les bonnes vakeurs 
        self._rebuild_grid()
        
        # mise à jour des compteurs
        self.update_color_counters()
    
    def update_color_counters(self):
        """Met à jour l'affichage des compteurs de couleur"""
        # compteurs pour le quadrant actuel
        for color, count in self.color_counts[self.current_quadrant].items():
            self.quad_counter_labels[color].config(
                text=f"{count}/4",
                fg="green" if count == 4 else "red"
            )
        
        # recalcul des compteurs globaux (somme des 4 quadrants)
        global_counts = {'B': 0, 'R': 0, 'V': 0, 'J': 0}
        for q_idx in range(4):
            for color, count in self.color_counts[q_idx].items():
                global_counts[color] += count
        
        # mise à jour des labels pour les compteurs globaux
        for color, count in global_counts.items():
            self.global_counter_labels[color].config(
                text=f"{count}/16",
                fg="green" if count == 16 else "red"
            )
    
    def _reset_current_quadrant(self):
        """Réinitialise le quadrant actuel à un état par défaut (vide/blanc)"""
        # réinitialiser les compteurs du quadrant
        self.color_counts[self.current_quadrant] = {'B': 0, 'R': 0, 'V': 0, 'J': 0}
        
        # réinitialiser la matrice
        for row in range(4):
            for col in range(4):
                self.quadrant_data[self.current_quadrant][row][col] = ''
        
        # reconstruction la grille
        self._rebuild_grid()
        
        # mise à jour de l'affichage des compteurs
        self.update_color_counters()
        
        # mise à jour de l'état du bouton d'enregistrement
        self._update_save_button()
    
    def _reset_all_quadrants(self):
        """Réinitialise tous les quadrants à un état par défaut (vide/blanc)"""
        # compteurs pour tous les quadrants
        for i in range(4):
            self.color_counts[i] = {'B': 0, 'R': 0, 'V': 0, 'J': 0}
            
            # les matrices
            for row in range(4):
                for col in range(4):
                    self.quadrant_data[i][row][col] = ''
        
        # la grille pour le quadrant actuel
        self._rebuild_grid()
        
        # maj de l'affichage des compteurs
        self.update_color_counters()
        
        # on désactive le bouton Enregistrer
        self.save_button.config(state="disabled")
    
    def _update_save_button(self):
        """Active le bouton Enregistrer si la distribution est valide dans tous les quadrants"""
        is_valid = True
        
        # on doit vérifier que chaque quadrant a exactement 4 cases de chaque couleur
        for quad_count in self.color_counts:
            if not all(count == 4 for count in quad_count.values()):
                is_valid = False
                break
        
        self.save_button.config(state="normal" if is_valid else "disabled")
    
    def _save_quadrants(self):
        """Enregistre les quadrants personnalisés via le plateau_manager"""
        from ui.plateau_manager import plateau_manager
        
        # on créee une liste pour stocker les quadrants
        custom_quadrants = []
        
        # crée des objets Quadrant à partir des matrices
        for quad_data in self.quadrant_data:
            quadrant = Quadrant(quad_data)
            custom_quadrants.append(quadrant)
        
        # on enregistre
        success = plateau_manager.save_custom_board(custom_quadrants)

        if success:
            # on notifie le build_screen pour qu'il rafraîchisse sa liste
            self._notify_build_screen_refresh()
        
        # puis afficher le message de confirmation
        popup = tk.Toplevel(self)
        popup.title("Quadrants enregistrés")
        
        tk.Label(
            popup,
            text="Vos quadrants personnalisés ont été enregistrés avec succès !",
            font=("Helvetica", 12)
        ).pack(pady=20, padx=20)
        
        # si on veut passer directement à l'écran d'orientation
        tk.Button(
            popup,
            text="Configurer l'orientation",
            command=lambda: [popup.destroy(), self._goto_orientation(custom_quadrants)]
        ).pack(side="left", padx=10, pady=10)
        
        tk.Button(
            popup,
            text="Continuer l'édition",
            command=popup.destroy
        ).pack(side="left", padx=10, pady=10)
        
        tk.Button(
            popup,
            text="Retour au menu",
            command=lambda: [popup.destroy(), self.controller.show("menu")]
        ).pack(side="right", padx=10, pady=10)
        
    def _goto_orientation(self, quadrants):
        """Passe à l'écran d'orientation avec les quadrants créés"""
        # stockage des quadrants dans le state
        self.controller.state.selected_quadrants = quadrants
        
        # passage à l'écran d'orientation
        self.controller.show("orientation")

    def _notify_build_screen_refresh(self):
        """notifie le build_screen qu'il doit rafraîchir sa liste de plateaux"""
        try:
            # si le build_screen existe dans les écrans, on lui dit de se rafraîchir
            if "build" in self.controller.screens:
                self.controller.screens["build"].refresh_after_edit()
        except Exception as e:
            # pas grave si ça échoue, c'est juste pour l'UX
            print(f"erreur notification build_screen: {e}")
