import tkinter as tk
from tkinter import messagebox
from ui.network_manager import NetworkManager

class NetworkScreen(tk.Frame):
    """Écran pour configurer une partie réseau (host ou join)"""

    def __init__(self, master: tk.Tk, controller):
        super().__init__(master)
        self.controller = controller
        self.network_mode = tk.StringVar(value="host")  # host ou join
        self.ip_address = tk.StringVar(value="127.0.0.1")  # localhost par défaut
        self.port = tk.StringVar(value="8888")  # port par défaut
        self.network_manager = NetworkManager()
        self.build_widgets()

    def build_widgets(self):
        # titre
        tk.Label(self, text="Configuration réseau", font=("Helvetica", 18, "bold")).pack(pady=20)
        
        # mode réseau (host ou join)
        mode_frame = tk.LabelFrame(self, text="Mode réseau", padx=20, pady=10)
        mode_frame.pack(pady=10, fill="x", padx=50)
        
        tk.Radiobutton(
            mode_frame,
            text="Héberger une partie (attendre connexion)",
            variable=self.network_mode,
            value="host",
            font=("Helvetica", 12),
            command=self._on_mode_change
        ).pack(anchor="w", pady=5)
        
        tk.Radiobutton(
            mode_frame,
            text="Rejoindre une partie",
            variable=self.network_mode,
            value="join",
            font=("Helvetica", 12),
            command=self._on_mode_change
        ).pack(anchor="w", pady=5)
        
        # config connexion
        config_frame = tk.LabelFrame(self, text="Configuration connexion", padx=20, pady=10)
        config_frame.pack(pady=10, fill="x", padx=50)
        
        # adresse IP (seulement pour join)
        self.ip_frame = tk.Frame(config_frame)
        self.ip_frame.pack(fill="x", pady=5)
        tk.Label(self.ip_frame, text="Adresse IP de l'hôte:", font=("Helvetica", 12)).pack(anchor="w")
        self.ip_entry = tk.Entry(self.ip_frame, textvariable=self.ip_address, font=("Helvetica", 12))
        self.ip_entry.pack(fill="x", pady=2)
        
        # port
        port_frame = tk.Frame(config_frame)
        port_frame.pack(fill="x", pady=5)
        tk.Label(port_frame, text="Port:", font=("Helvetica", 12)).pack(anchor="w")
        tk.Entry(port_frame, textvariable=self.port, font=("Helvetica", 12)).pack(fill="x", pady=2)
        
        # statut connexion
        self.status_label = tk.Label(self, text="", font=("Helvetica", 10), fg="blue")
        self.status_label.pack(pady=10)
        
        # boutons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)
        
        self.connect_button = tk.Button(
            button_frame,
            text="Démarrer",
            width=15,
            font=("Helvetica", 12),
            command=self._start_network_game
        )
        self.connect_button.pack(side="left", padx=10)
        
        tk.Button(
            button_frame,
            text="Retour au menu",
            width=15,
            font=("Helvetica", 12),
            command=self._goto_menu
        ).pack(side="left", padx=10)
        
        # ajuste l'affichage initial
        self._on_mode_change()
    
    def _on_mode_change(self):
        """met à jour l'interface selon le mode sélectionné"""
        if self.network_mode.get() == "host":
            self.ip_frame.pack_forget()  # cache l'IP pour host
            self.connect_button.config(text="Héberger")
            self.status_label.config(text="En attente de connexion...")
        else:
            self.ip_frame.pack(fill="x", pady=5)  # montre l'IP pour join
            self.connect_button.config(text="Se connecter")
            self.status_label.config(text="Prêt à se connecter")
    
    def _start_network_game(self):
        """démarre la connexion réseau puis va configurer le plateau"""
        try:
            port_num = int(self.port.get())
            if port_num < 1024 or port_num > 65535:
                raise ValueError("port doit être entre 1024 et 65535")
        except ValueError as e:
            messagebox.showerror("Erreur", f"Port invalide: {e}")
            return
        
        # désactive le bouton pendant la connexion
        self.connect_button.config(state="disabled")
        
        # stocke la config réseau dans state
        self.controller.state.network_mode = self.network_mode.get()
        self.controller.state.network_ip = self.ip_address.get()
        self.controller.state.network_port = port_num
        self.controller.state.network_manager = self.network_manager
        
        # tente la connexion
        if self.network_mode.get() == "host":
            success = self.network_manager.host_game(port_num, self._update_status)
        else:
            success = self.network_manager.join_game(self.ip_address.get(), port_num, self._update_status)
        
        if not success:
            self.connect_button.config(state="normal")
            return
            
        # vérifie périodiquement si connecté
        self._check_connection()
    
    def _update_status(self, message):
        """met à jour le label de statut (appelé par NetworkManager)"""
        self.status_label.config(text=message)
        self.controller.root.update_idletasks()
    
    def _check_connection(self):
        """vérifie si la connexion est établie et passe à l'écran suivant"""
        if self.network_manager.is_connected:
            if self.network_mode.get() == "host":
                # seul le host configure le plateau
                self.status_label.config(text="Connexion établie! Configuration du plateau...", fg="green")
                self.controller.root.after(1000, lambda: self.controller.show("build"))
            else:
                # le client attend la config du host
                self.status_label.config(text="Connexion établie! En attente de la configuration...", fg="green")
                self._wait_for_setup()
        else:
            # revérifie dans 500ms
            self.controller.root.after(500, self._check_connection)
    
    def _wait_for_setup(self):
        """le client attend que le host envoie la config du plateau"""
        # configure callback pour recevoir le setup
        self.network_manager.set_message_callback(self._handle_setup_message)
    
    def _handle_setup_message(self, message):
        """traite le message de setup reçu du host"""
        if message["type"] == "setup":
            # stocke la config reçue
            self.controller.state.network_quad_mats = message["quadrants"]
            self.controller.state.network_game_type = message["game_type"]
            
            self.status_label.config(text="Configuration reçue! Démarrage de la partie...", fg="green")
            # démarre directement la partie avec la config reçue
            self.controller.root.after(500, self._start_game_with_config)
        elif message["type"] == "disconnect":
            self.status_label.config(text="L'hôte s'est déconnecté", fg="red")
            self.connect_button.config(state="normal")
    
    def _start_game_with_config(self):
        """démarre la partie avec la config reçue du host"""
        quad_mats = self.controller.state.network_quad_mats
        game_type = self.controller.state.network_game_type
        
        # nettoie le callback pour éviter interférences
        self.network_manager.set_message_callback(None)
        
        self.controller.show("game", 
                           quad_mats=quad_mats, 
                           game_type=game_type, 
                           game_mode="network")
    
    def _goto_menu(self):
        """retour au menu principal"""
        self.controller.show("menu")
