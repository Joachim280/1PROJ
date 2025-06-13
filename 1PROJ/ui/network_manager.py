import socket
import threading
import json
import tkinter as tk
from tkinter import messagebox

class NetworkManager:
    """Gestion simple des connexions réseau pour parties multi-joueurs
    
    Principe basique :
    - Host : crée un serveur, attend 1 connexion
    - Client : se connecte à l'IP du host
    - Messages JSON simples : move, setup, game_over
    """
    
    def __init__(self):
        self.socket = None
        self.connection = None  # pour le serveur
        self.is_host = False
        self.is_connected = False
        self.message_callback = None  # fonction appelée à réception message
        
    def host_game(self, port, status_callback=None):
        """démarre un serveur et attend une connexion
        
        port : port d'écoute 
        status_callback : fonction(message) pour mettre à jour l'UI
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(('0.0.0.0', port))
            self.socket.listen(1)
            self.is_host = True
            
            if status_callback:
                status_callback(f"Serveur démarré sur port {port}, en attente...")
            
            # attend connexion en arrière-plan
            def wait_connection():
                try:
                    self.connection, addr = self.socket.accept()
                    # supprime timeout pour communication continue
                    self.connection.settimeout(None)
                    self.is_connected = True
                    if status_callback:
                        status_callback(f"Joueur connecté depuis {addr[0]}")
                    self._start_listening()
                except Exception as e:
                    if status_callback:
                        status_callback(f"Erreur serveur: {e}")
            
            thread = threading.Thread(target=wait_connection, daemon=True)
            thread.start()
            return True
            
        except Exception as e:
            if status_callback:
                status_callback(f"Impossible de démarrer serveur: {e}")
            return False
    
    def join_game(self, ip, port, status_callback=None):
        """se connecte à un serveur host
        
        ip : adresse IP du host
        port : port de connexion
        status_callback : fonction(message) pour mettre à jour l'UI
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # timeout 10 sec pour connexion seulement
            
            if status_callback:
                status_callback(f"Connexion à {ip}:{port}...")
                
            self.socket.connect((ip, port))
            self.socket.settimeout(None)  # supprime timeout après connexion réussie
            self.is_connected = True
            self.is_host = False
            
            if status_callback:
                status_callback("Connecté avec succès!")
            
            self._start_listening()
            return True
            
        except Exception as e:
            if status_callback:
                status_callback(f"Connexion échouée: {e}")
            return False
    
    def send_message(self, message_type, data=None):
        """envoie un message JSON à l'autre joueur
        
        message_type : "move", "setup", "game_over"
        data : dict avec les données du message
        """
        if not self.is_connected:
            return False
            
        try:
            message = {"type": message_type}
            if data:
                message.update(data)
            
            json_msg = json.dumps(message) + "\n"
            
            # envoie selon mode (host ou client)
            if self.is_host and self.connection:
                self.connection.send(json_msg.encode('utf-8'))
            elif not self.is_host and self.socket:
                self.socket.send(json_msg.encode('utf-8'))
            
            return True
            
        except Exception as e:
            print(f"erreur envoi message: {e}")
            return False
    
    def _start_listening(self):
        """démarre l'écoute des messages en arrière-plan"""
        def listen():
            buffer = ""
            while self.is_connected:
                try:
                    # configure un timeout court pour check régulièrement is_connected
                    if self.is_host and self.connection:
                        self.connection.settimeout(1.0)  # timeout 1 sec
                        data = self.connection.recv(1024).decode('utf-8')
                    elif not self.is_host and self.socket:
                        self.socket.settimeout(1.0)  # timeout 1 sec
                        data = self.socket.recv(1024).decode('utf-8')
                    else:
                        break
                    
                    if not data:
                        self._handle_disconnect()
                        break
                    
                    buffer += data
                    # traite les messages complets (terminés par \n)
                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        if line.strip():
                            try:
                                message = json.loads(line)
                                if self.message_callback:
                                    self.message_callback(message)
                            except json.JSONDecodeError:
                                print(f"message JSON invalide: {line}")
                
                except socket.timeout:
                    # timeout normal, continue l'écoute
                    continue
                except Exception as e:
                    print(f"erreur réception: {e}")
                    self._handle_disconnect()
                    break
        
        thread = threading.Thread(target=listen, daemon=True)
        thread.start()
    
    def _handle_disconnect(self):
        """gère la déconnexion de l'autre joueur"""
        self.is_connected = False
        # on pourrait ici déclencher une popup dans l'UI
        if self.message_callback:
            self.message_callback({"type": "disconnect"})
    
    def disconnect(self):
        """ferme proprement la connexion"""
        self.is_connected = False
        try:
            if self.connection:
                self.connection.close()
            if self.socket:
                self.socket.close()
        except:
            pass
        self.socket = None
        self.connection = None
    
    def set_message_callback(self, callback):
        """définit la fonction appelée à réception d'un message
        
        callback : fonction(message_dict)
        """
        self.message_callback = callback
