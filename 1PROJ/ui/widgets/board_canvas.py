
import tkinter as tk
from core.class_cadran import q1

class BoardCanvas(tk.Canvas):
    """Canvas affichant une grille 8x8 fixe (60 px la case)"""

    CELL = 60          # taille d'une case en pixels
    SIZE = CELL * 8    # dimension totale (480 px)

    # --- palette simple (on pourra la modifier plus tard) -------------------------
    Q_COLORS = {                       
        "blue":   "#4a90e2",          
        "green":  "#5cb85c",
        "yellow": "#f0ad4e",
        "red":    "#d9534f",
    }
    # on convertit la lettre du modèle en couleur hex pour Tk
    TILE_COLOR = {
        "B": "#4a90e2",
        "V": "#5cb85c",
        "J": "#f0ad4e",
        "R": "#d9534f",
    }
    
    # --------------------------------------------------------------
    def __init__(self, master: tk.Widget, quad_mats=None):
        super().__init__(
            master,
            width=self.SIZE,
            height=self.SIZE,
            bg="#f0f0f0",      # gris clair d'arrière-plan
            highlightthickness=0
        )
        
        # on initialise les quadrants
        from core.class_cadran import QUADRANTS    # on importe les 4 quadrants
        base = [QUADRANTS[i+1] for i in range(4)]  # j'utilise les 4 quadrants par défaut
        # copie indépendante pour chaque quadrant
        self.quad_mats   = [ [row[:] for row in qm] for qm in (quad_mats or base) ]
        self.locked_quads = [bool(quad_mats)] * 4     # ils sont verrouillés si le quad_mats est fourni
        self.selected_quad = None
        
        self.draw_quadrants()
        self.draw_grid()
        
        # indicateur de verrou pour les quadrants déjà verrouillés
        if quad_mats:  # si fourni en param, tous les quadrants sont bloqué
            for q in range(4):
                self._draw_locked_overlay(q)

        # ecouteur de clic gauche
        self.bind("<Button-1>", self.on_click)

    # ------------------------------------------------------------------
    ########  Gestion du clic sur le plateau  ########
    # ------------------------------------------------------------------
    def on_click(self, event):
        quad = self._coord_to_quadrant(event.x, event.y)
        if quad is None or self.locked_quads[quad]:
            return          # pour les cas où on clique en dehors ou sur un quadrant verrouillé

        # sur-lignage
        if self.selected_quad == quad:
            self.selected_quad = None
            self.delete("highlight")
            return
        else:
            self.selected_quad = quad
            self._draw_highlight(quad)

        # boîte de discussion pour la rotation et le miroir
        from ui.widgets.quadrant_selector import edit_orientation
        edit_orientation(
            controller=self.master,
            quad_index=quad,
            callback=lambda rot, mir: self._apply_orientation(quad, rot, mir)
        )

    def _coord_to_quadrant(self, x, y):
        """Renvoie 0,1,2,3 selon la position pixel, ou None hors plateau"""
        if not (0 <= x < self.SIZE and 0 <= y < self.SIZE):
            return None
        col_quad = x // (4 * self.CELL)   # 0 ou 1
        row_quad = y // (4 * self.CELL)   # 0 ou 1
        return row_quad * 2 + col_quad    # mapping 2x2 vers 0..3

    def _draw_highlight(self, quad: int) -> None:
        """Cadre jaune épais + ombre portée légère sous le quadrant"""
        self.delete("highlight")  

        c = self.CELL
        qx = (quad % 2) * 4 * c
        qy = (quad // 2) * 4 * c
        x2, y2 = qx + 4 * c, qy + 4 * c

        # ombre portée
        self.create_rectangle(
            qx + 3, qy + 3, x2 + 3, y2 + 3,
            outline="#666666", width=4,
            tags="highlight"
        )
        # le cadre principal
        self.create_rectangle(
            qx, qy, x2, y2,
            outline="gold", width=5,
            tags="highlight"
        )


    # ------------------------------------------------------------------
    # Version d'essai : quadrants colorés
    # def draw_quadrants(self):
    #     """Peint chaque quadrant 4x4 en couleur uniforme"""
    #     c = self.CELL
    #     quads = [
    #         (0,      0,      "blue"),
    #         (4 * c,  0,      "green"),
    #         (0,      4 * c,  "yellow"),
    #         (4 * c,  4 * c,  "red"),
    #     ]
    #     for x0, y0, color_key in quads:
    #         self.create_rectangle(
    #             x0, y0, x0 + 4 * c, y0 + 4 * c,
    #             fill=self.Q_COLORS[color_key],
    #             width=0
    #         )
    
    def draw_quadrants(self):
        """Dessine les 4 quadrants à partir de self.quad_mats"""
        self.delete("tiles")
        c = self.CELL
        for q in range(4):
            mat = self.quad_mats[q]
            x0 = (q % 2) * 4 * c
            y0 = (q // 2) * 4 * c
            for r in range(4):
                for col in range(4):
                    letter = mat[r][col]
                    color  = self.TILE_COLOR[letter]
                    x1 = x0 + col * c
                    y1 = y0 + r * c
                    self.create_rectangle(
                        x1, y1, x1 + c, y1 + c,
                        fill=color, width=0,
                        tags="tiles"
                    )

    # ------------------------------------------------------------------
    def draw_grid(self):
        """Trace les lignes de la grille"""
        self.delete("grid")
        for i in range(9): 
            # en vertical
            x = i * self.CELL
            self.create_line(x, 0, x, self.SIZE, tags="grid")
            # horizontalement
            y = i * self.CELL
            self.create_line(0, y, self.SIZE, y, tags="grid")
            
    # ------ ajout de l'ombre ----
        self.create_rectangle(
            0, 0, self.SIZE, self.SIZE,
            width=2
        )
    # -------------------------------------------------------------------
    def _apply_orientation(self, quad, rot: int, mirror: bool):
        """Met à jour self.quad_mats[quad] puis redessine"""
        mat = self.quad_mats[quad]
        mat = self._rotate_matrix(mat, rot)
        if mirror:
            mat = [row[::-1] for row in mat]
        self.quad_mats[quad] = mat
        self.locked_quads[quad] = True         # pour figer le quadrant
        
        # il faut notifier BuildScreen pour incrémenter son compteur
        if hasattr(self.master, "quadrant_locked_callback"):
            self.master.quadrant_locked_callback()

        # maj de l'affichage
        self.draw_quadrants()
        self.draw_grid()
        
        # on redessine les indicateurs pour tous les quadrants verrouillé
        for q in range(4):
            if self.locked_quads[q]:
                self._draw_locked_overlay(q)
                
        # surbrillance du quadrant actif
        if self.selected_quad is not None:
            self._draw_highlight(self.selected_quad)

    def _draw_locked_overlay(self, quad: int):
        """Indicateur visuel pour un quadrant verrouillé (cadenas + contour)"""
        c   = self.CELL
        qx  = (quad % 2) * 4 * c
        qy  = (quad // 2) * 4 * c
        x2, y2 = qx + 4 * c, qy + 4 * c

        self.delete(f"locked{quad}")

        # 1. contour du quadrant
        self.create_rectangle(
            qx, qy, x2, y2,
            outline="black",  
            width=5,
            dash=(8, 4),
            tags=(f"locked{quad}", "locked")
        )
        
        # 2. icône de cadenas
        cx = qx + 2 * c  # centre x du quadrant
        cy = qy + 2 * c  # centre y du quadrant
        
        # arrière-plan du cadenas
        self.create_rectangle(
            cx - 15, cy - 20, cx + 15, cy + 20,
            fill="#333333",
            outline="#000000",
            width=1,
            tags=(f"locked{quad}", "locked")
        )
        
        # base du cadenas
        self.create_rectangle(
            cx - 12, cy - 5, cx + 12, cy + 15,
            fill="#888888",
            outline="black",
            width=2,
            tags=(f"locked{quad}", "locked")
        )
        
        # arc du cadenas
        self.create_arc(
            cx - 12, cy - 15, cx + 12, cy + 5,
            start=0, extent=180,
            style="arc",
            outline="white",
            width=3,
            tags=(f"locked{quad}", "locked")
        )

    def reset_board(self):
        """Déverrouille tout, remet la face q1 et rafraîchit l'affichage"""
        from core.class_cadran import q1
        self.selected_quad = None
        self.locked_quads = [False] * 4
        self.quad_mats = [ [row[:] for row in q1] for _ in range(4) ]
        self.delete("locked")
        self.delete("highlight")
        self.draw_quadrants()
        self.draw_grid()

    # ================================================================
    #   Gestion visuelle des PIONS
    # ================================================================
    PIECE_RADIUS = int(CELL * 0.30) 
    PIECE_FILL  = {"white": "#fafafa", "black": "#222222"}

    def draw_pieces(self, positions):
        """Dessine tous les pions (row, col, 'white' | 'black')"""
        self.delete("piece")
        r = self.PIECE_RADIUS
        for row, col, color in positions:
            cx = col * self.CELL + self.CELL // 2
            cy = row * self.CELL + self.CELL // 2
            self.create_oval(
                cx - r, cy - r, cx + r, cy + r,
                fill=self.PIECE_FILL[color],
                outline="#000", 
                width=2,
                tags=("piece",)
            )

    # --------------------------------------------------------------
    def highlight_moves(self, squares):
        """
        Dessine autour des cases (row,col) un double contour
        noir + or pour être visible quelle que soit la couleur de la case.
        """
        self.delete("hl")
        for row, col in squares:
            x1 = col * self.CELL
            y1 = row * self.CELL
            x2 = x1 + self.CELL
            y2 = y1 + self.CELL

            # ombre noire
            self.create_rectangle(
                x1, y1, x2, y2,
                outline="#000000", width=4, tags=("hl",)
            )
            # fin
            self.create_rectangle(
                x1+2, y1+2, x2-2, y2-2,
                outline="#FFD700", width=2, tags=("hl",)
            )



    # ----------------- utilitaire interne -----------------------------
    @staticmethod
    def _rotate_matrix(mat, k: int):
        """Retourne la matrice tournée de 0,1,2,3 x 90°"""
        for _ in range(k):
            mat = [list(reversed(col)) for col in zip(*mat)]
        return mat

    # -------- interface publique ----------
    def get_quad_mats(self) -> list[list[list[str]]]:
        """Copie profonde des 4 matrices 4x4 actuellement verrouillées"""
        return [ [row[:] for row in quad] for quad in self.quad_mats ]
