import tkinter as tk
from tkinter import ttk, font
import json
import os
from datetime import datetime

class SearchPage(tk.Frame):
    def __init__(self, parent, show_frame, datamanager):
        super().__init__(parent)
        self.show_frame = show_frame
        self.datamanager = datamanager

        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
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

        #titre de la page
        tk.Label(self, text="Recherche de données", font=self.title_font,
            bg="#D1D1D1",
            fg="#002147").pack(pady=20)

        # Variable pour stocker le nom de la table sélectionnée
        self.table_var = tk.StringVar(self)
        #menu déroulant pour choisir la tbale
        self.table_dropdown = ttk.Combobox(self, textvariable=self.table_var, style="TCombobox", state="readonly")
        self.table_dropdown.pack(pady=10)
        self.table_dropdown.bind("<<ComboboxSelected>>", self.on_table_select)

        #idem pour la colonne
        self.column_var = tk.StringVar(self)
        self.column_dropdown = ttk.Combobox(self, textvariable=self.column_var, style="TCombobox", state="readonly")
        self.column_dropdown.pack(pady=10)

        #champs de texte pour entrer une valeur specifique
        tk.Label(self, text="Rechercher une valeur :", font=self.used_font,
            bg="#D1D1D1",
            fg="#002147").pack(pady=10)
        self.search_entry = tk.Entry(self, width=30)  # Entrée pour le search
        self.search_entry.pack(pady=10)

        #bouton pour lancer une recherche
        self.search_button = ttk.Button(self, text="Chercher", style="TButton", command=self.search_data)
        self.search_button.pack(pady=20)

        #bouton pour enregistrer la recherche
        self.save_button = ttk.Button(self, text="Enregistrer les résultats", style="TButton", command=self.load_results)
        self.save_button.place(x= 20, y=100)

        #bouton retour
        ttk.Button(self, text="Retour", style="TButton", command=lambda: self.show_frame("MainMenuPage")).place(x=20, y=20)

        #widget treeview qui permet d'afficher les tables et leurs valeurs
        self.tree = ttk.Treeview(self, show="headings", style="Treeview")  # TreeView = vue en forme d'abre montre les entetes
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)  # affichage de l'arbre

        #fichier de recherche
        self.searchdata_file = 'researchdump.json'

        # Créer le fichier de recherche si besoin
        if not os.path.exists(self.searchdata_file):
            with open(self.searchdata_file, 'w') as f:
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #date de creation
                json.dump([{"Opening_time": current_time}], f)

        self.load_tables()

    def load_tables(self):
        """
        Charge les noms des tables disponibles dans la base de données et les affiche dans le menu déroulant.
        """
        tables = self.datamanager.get_tables()  # Appelle la méthode pour obtenir les tables
        table_names = []  # Liste pour stocker les noms des tables

        for table in tables:
            table_names.append(table[0])

        self.table_dropdown["values"] = table_names #menu déroulant mis a jour

        if table_names:
            self.table_var.set("") #valeur inititiale

    # chaque fois qu'il y a 0 c'est juste que c'est la valeur dans la data base(nom de la colonne)

    def on_table_select(self, event=""):
        """
        Met a jour quel table est utilisé
        """
        #event est pour eviter une erreur du mechant tkinter, bidouillage
        selected_table = self.table_var.get()  # Obtenir la table sélectionnée
        table_data, description = self.datamanager.show_table(selected_table)
        # Récupérer uniquement la description des colonnes
        column_names = []
        for col in description:
            column_names.append(col[0])

        self.column_dropdown["values"] = column_names #mis a jour du menu deroulant des colonnes

        if column_names:
            self.column_var.set(column_names[0]) #valeur initiale

    def display_selected_values(self, selected_table="", selected_column="", search_value=""):
        """
        Affiche les valeurs sélectionnées sélectionnée dans le Treeview.
        In : selected_table : table sélectionnée pour la recherche
        selected_column : de meme pour la colonne
        search_value : valeur a rechercher
        """
        self.tree.delete(*self.tree.get_children()) #contenu present surpprime
        self.tree["columns"] = [] #creer les colonnes

        check_in = not (selected_table == "" and search_value == "") #on verifie que la recherche ne soit pas incohérente
        #si juste une colonne alors aucun interet et pas possible
        if check_in:
            # resultat de la recherche cf datamanager/requestmanager
            rows, description = self.datamanager.get_request(selected_table, selected_column, search_value)
            if rows:
                column_count = len(rows[0]) #nombre de colonne
                self.tree["columns"] = [f"col{i}" for i in range(column_count)] #creer le nombre de colonnes necessaires

                for i, description in enumerate(description): #met a jour les colonnes
                    # (1, 2 ... i ... nombre de colonnes) toutes colonnes traitees
                    self.tree.heading(i, text=description[0]) #ici les en tetes soit les noms de colonnes
                    self.tree.column(i, width=100) #ici gere la forme de la colonne en elle meme

                for row in rows: #idem mais insere les valeurs dans les les colonnes
                    #bien qu'ici c'est une insertion par lignes de valeurs, l idee est la meme
                    self.tree.insert("", "end", values=row)

    def search_data(self):
        """
        Permet de lancer la recherche et l affichage de celle ci
        :return:
        """
        #Parametre selectionnes
        selected_table = self.table_var.get()
        selected_column = self.column_var.get()
        search_value = self.search_entry.get()
        #affichage des donnees dans le tree view
        self.display_selected_values(selected_table, selected_column, search_value)

    def load_results(self):
        """
        Permet de telecharger les resultats affiches dans un fichier json
        Fonctionnalite assez peu utile en verite mais parfois interressante
        :return:
        """
        results = []
        headers = [self.tree.heading(col)["text"] for col in self.tree["columns"]]
        #on recupere ici les noms de colonnes du tree-view

        for child in self.tree.get_children(): #on parcours les donnees presentes dans le tree view
            row_data = self.tree.item(child)["values"] #recupere les donnees
            # les associes a chaque colonnes de la ligne
            row_dict = {headers[i]: row_data[i] for i in range(len(headers))}
            results.append(row_dict) #on stock les donnees d une ligne dans la liste de la recherche

        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #temps de la recherche
        research = {"research":results, "research_time":current_time} #caracteristique de la recherche
        with open(self.searchdata_file, 'r+') as file: #on ouvre le fichier
            data = json.load(file) #on recupere les anciennes donnees
            data.append(research) #on ajoute la nouvelles recherche
            file.seek(0) #curzseur ligne 0
            json.dump(data, file, indent=4) #sauvegarde

