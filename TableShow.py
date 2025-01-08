import tkinter as tk
from tkinter import ttk, messagebox,font
import sqlite3

class TableShowPage(tk.Frame):
    def __init__(self, parent, show_frame, datamanager):
        super().__init__(parent)
        self.show_frame = show_frame
        self.datamanager = datamanager

        self.title_font = font.Font(family="Helvetica", size=29, weight="bold")
        self.used_font = font.Font(family="Helvetica", size=16)

        self.style = ttk.Style(self)
        self.configure(bg="#D1D1D1")

        self.style.configure(
            "Treeview",
            background="#F7FBFB",
            foreground="#000000",         
            rowheight=40,
            fieldbackground="#F7FBFB",
            font=self.used_font,
            borderwidth=0                 
        )

        self.style.configure(
            "Treeview.Heading",
            background="#28344d",
            foreground="#ffffff",
            font=(self.title_font, 14, "bold"),
            borderwidth=1
        )

        self.style.configure(
            "TButton",
            relief="flat",
            background="#002147",
            foreground="#FAEFDC",
            font=(self.used_font, 14),
            padding=(10, 5)
        )


        self.style.configure(
            "TCombobox",
            relief="flat",
            background="#ffffff",
            foreground="#002147",
            fieldbackground="#ffffff",
            font=(self.used_font, 14),
            padding=(5,)
        )

        # Map pour les effets de sélection et hover
        self.style.map(
            "Treeview",
            background=[("selected", "#002147")],
            foreground=[("selected", "#ffffff")]
        )
        self.style.map(
            "TButton",
            background=[("active", "#3f2204")],
            foreground=[("active", "#FAEFDC")]
        )
        self.style.map(
            "TCombobox",
            background=[("active", "#3F2621")],
            foreground=[("active", "#FAEFDC")]
        )

        # Titre de la page
        tk.Label(
            self,
            text="Page d'affichage",
            font=self.title_font,
            bg="#D1D1D1",
            fg="#002147"
        ).pack(pady=20)

        # Menu déroulant pour choisir entre les tables
        self.table_var = tk.StringVar(self)
        self.table_dropdown = ttk.Combobox(self, textvariable=self.table_var, style="TCombobox")
        self.table_dropdown.pack(pady=10)

        # Bouton pour afficher la table sélectionnée
        ttk.Button(
            self,
            text="Afficher la table",
            style="TButton",
            command=self.display_selected_table
        ).pack(pady=10)

        # Bouton retour
        ttk.Button(
            self,
            text="Retour",
            style="TButton",
            command=lambda: self.show_frame("MainMenuPage")
        ).pack(pady=10)

        # Tableau pour afficher les données
        self.tree = ttk.Treeview(
            self,
            show="headings",
            style="Treeview"
        )
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        
        
        

        
        

        self.load_tables()

    
    def load_tables(self):
        """Charge la liste des tables dans la base de données et les ajoute au menu déroulant."""

        tables = self.datamanager.get_tables() # importe les tables
        table_names = [table[0] for table in tables]  #transformation de liste de tuple(ex:([('fleurs',), ('categories',)])) en ['fleurs','categorie']
        self.table_dropdown["values"] = table_names# ajout des noms au COmboBox 
        if table_names:
            self.table_var.set(table_names[0])# selection de la table 1 par défaut

    def display_selected_table(self):
        """Affiche le contenu de la table sélectionnée dans le Treeview."""
        # Configuration des colonnes
        self.tree.delete(*self.tree.get_children())  # supprime toutes les données deja presente dans le widget treeview
        selected_table = self.table_var.get()
        rows, description = self.datamanager.show_table(selected_table)

        if rows:
            column_count = len(rows[0])
            self.tree["columns"] = [f"col{i}" for i in range(column_count)] #donne un nom a chaque colone (col1,col2,col3...) et qui ensuite va etre égale a chaque nom de nos collones
        else:
            self.tree["columns"] = []

        for i, description in enumerate(description):# Renvoie les données sur les elements de la table ou chaque element est un tuple contenant des infos comme le nom de la collone
            self.tree.heading(i, text=description[0])#associe chaque collone du treeview avec un nom ex(Nom,Type etc)
            self.tree.column(i, width=100)#largeur des colones

        # Insérer les données
        for row in rows:
            self.tree.insert("", "end", values=row) # insertions des données dans le tableau

