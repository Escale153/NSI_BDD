import tkinter as tk
from tkinter import font, ttk

class ConnexionPage(tk.Frame):
    """
    Page de connexion à la base de données
    """
    def __init__(self, parent, show_frame, get_datamanager):
        super().__init__(parent)

        # Référence vers les fonctions passées en paramètre
        self.show_frame = show_frame
        self.get_datamanager = get_datamanager

        # Chargement de la police personnalisée
        self.title_font = font.Font(family="Helvetica", size=29, weight="bold")
        self.used_font = font.Font(family="Helevetica", size=16)

        self.configure(bg="#F4FEFE")

        self.style = ttk.Style()
        

        # Style pour les champs de saisie
        self.style.configure(
            "Rounded.TEntry",
            relief="flat",
            borderwidth=2,
            fieldbackground="#ffffff",  
            foreground="#002147",  
            insertcolor="#002147",  
            padding=5,
            font=self.used_font
        )

        # Style pour les boutons
        self.style.configure(
            "TButton",
            relief="flat",
            background="#002147",
            foreground="#FAEFDC",
            font=(self.title_font, 14),
            padding=(10, 5)
        )

        self.style.map(
            "TButton",
            background=[("active", "#3f2204")],
            foreground=[("active", "#FAEFDC")]
        )

        # Titre principal
        tk.Label(
            self,
            text="Page de Connexion",
            font=self.title_font,
            bg="#F4FEFE",
            fg="#002147"
        ).pack(pady=(50, 20))

        # Sous-titre
        tk.Label(
            self,
            text="Choisir la base de données à laquelle se connecter",
            font=self.used_font,
            bg="#F4FEFE",
            fg="#28344d"
        ).pack(pady=(20, 20))

        self.database_entry = ttk.Entry(self, width=30, style="Rounded.TEntry")
        self.database_entry.pack(pady=(20, 20))

        ttk.Button(self,text="Connexion",style="TButton",command=lambda: (self.get_datamanager(self.database_entry.get()),self.show_frame("MainMenuPage"))).pack(pady=20)

