import tkinter as tk
from tkinter import ttk,font
import sqlite3

class MainMenuPage(tk.Frame):
    """
    Page du menu principal
    """
    def __init__(self, parent, show_frame, reset_frame):
        super().__init__(parent)
        #deux fct (cf app)
        self.show_frame = show_frame
        self.reset_frame = reset_frame

        self.title_font = font.Font(family="Helvetica", size=29, weight="bold")
        self.used_font = font.Font(family="Helvetica", size=16)

        self.style = ttk.Style(self)
        self.configure(bg="#F4FEFE")

        self.style.configure(
            "TButton",
            relief="flat",
            background="#002147",
            foreground="#FAEFDC",
            font=(self.used_font, 14),
            padding=(10, 5)
        )

        self.style.map(
            "TButton",
            background=[("active", "#3f2204")],
            foreground=[("active", "#FAEFDC")]
        )

	    #titre principal
        tk.Label(self, text="Menu principal", font=self.title_font,bg="#F4FEFE",fg="#002147").pack(pady=50)
        
        # Bouton pour naviguer vers l'affichage des différentes pages
        #reset d'abord la page puis l affiche avec les deux fct ci dessus
        ttk.Button(self, text="Afficher les tables",style='TButton', command=lambda: (self.reset_frame("TableShowPage"), self.show_frame("TableShowPage"))).pack(pady=20) #Quand appui sur le bouton "Afficher les tables " alors redirection vers 'Table show page'
        ttk.Button(self, text="Rechercher des données",style='TButton', command=lambda: (self.reset_frame("SearchPage"), self.show_frame("SearchPage"))).pack(pady=20)
        ttk.Button(self, text="Modifications de données",style='TButton', command=lambda: (self.reset_frame("DataUpdatePage"), self.show_frame("DataUpdatePage"))).pack(pady=20)
        ttk.Button(self, text="Modifications de Tables",style='TButton', command=lambda: (self.reset_frame("TableUpdatePage"), self.show_frame("TableUpdatePage"))).pack(pady=20)
        ttk.Button(self, text="Afficher les modifications",style='TButton', command=lambda: (self.reset_frame("JsonViewerPage"), self.show_frame("JsonViewerPage"))).pack(side="bottom", pady=30)
        #lambda permet d utiliser les fcts temporairement sans les declarer
        
        #charge un theme qui sera donc utilisé dans toutes les pages grace au app
        
