import tkinter as tk
from tkinter import ttk,font, messagebox
import sqlite3

class DataUpdatePage(tk.Frame):
    """
    Page de la modification de donnees
    """
    def __init__(self, parent, show_frame, datamanager):
        super().__init__(parent)
        self.show_frame = show_frame
        self.datamanager = datamanager

        # Titre de la page
        tk.Label(self, text="Modifier les données", font=("Arial", 28),bg="#F4FEFE",fg="#002147").pack(pady=20)
        self.style = ttk.Style(self)
        self.configure(bg="#F4FEFE")


        

         # Style pour les champs de saisie
        self.title_font = font.Font(family="Helvetica", size=29, weight="bold")
        self.used_font = font.Font(family="Helvetica", size=16)

        # Styles des widgets cf TableUpdatePage
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
            background=[
                ("active", "#28344d"),  
                ("disabled", "#808080")  
            ],
            foreground=[
                ("active", "#faefdc"),  
                ("disabled", "#ffffff")  
            ],
            relief=[
                ("pressed", "sunken"),  
                ("active", "raised")  
            ]
        )
        self.style.configure(
            "TCombobox",
            relief="flat",
            background="#ffffff",
            foreground="#002147",
            fieldbackground="#ffffff",
            font=(self.title_font, 14),
            padding=(5,)
        )
        self.style.configure(
            "TCombobox",
            relief="flat",
            background="#ffffff",
            foreground="#002147",
            fieldbackground="#ffffff",
            font=(self.title_font, 14),
            padding=(5,)
        )

        #################################################
        padding_x = 50
        padding_y = 20
        y_start = 100

        # Section Ajouter des données
        tk.Label(self, text="Ajouter des données (format : donné1,donné2,...)", font=self.used_font, bg="#F4FEFE",fg="#002147").place(x=padding_x, y=y_start)
        self.data_entry = ttk.Entry(self, style="Rounded.TEntry", width=50)  # Réduit la largeur de l'Entry
        self.data_entry.place(x=padding_x, y=y_start + 30)

        self.table_var_add_data = tk.StringVar(self)
        self.table_dropdown_add = ttk.Combobox(self, textvariable=self.table_var_add_data, state="readonly", style="TCombobox")
        self.table_dropdown_add.place(x=padding_x, y=y_start + 70)

        self.add_data_button = ttk.Button(self, text="Ajouter Des données", command=self.add_values, style="TButton")
        self.add_data_button.place(x=padding_x, y=y_start + 110)

        # Section Modifier des données
        y_start_update = y_start + 200
        tk.Label(self, text="Sélectionner une table :", font=("Arial", 12), bg="#F4FEFE",fg="#002147").place(x=padding_x, y=y_start_update)

        self.table_var_update = tk.StringVar(self)
        self.table_dropdown_update = ttk.Combobox(self, textvariable=self.table_var_update, state="readonly", style="TCombobox")
        self.table_dropdown_update.bind("<<ComboboxSelected>>", self.load_columns_update)
        self.table_dropdown_update.place(x=padding_x, y=y_start_update + 30)

        '''self.choose_table_button_update = ttk.Button(self, text="Choisir la table", command=self.load_columns_update, style="TButton")
        self.choose_table_button_update.place(x=padding_x, y=y_start_update + 70)'''

        tk.Label(self, text="Sélectionner une colonne :", font=("Arial", 12), bg="#F4FEFE",fg="#002147").place(x=padding_x, y=y_start_update + 70)

        self.column_var_update = tk.StringVar(self)
        self.column_dropdown_update = ttk.Combobox(self, textvariable=self.column_var_update, state="readonly", style="TCombobox")
        self.column_dropdown_update.bind("<<ComboboxSelected>>", self.display_column_values_update)
        self.column_dropdown_update.place(x=padding_x, y=y_start_update + 100)

        tk.Label(self, text="Valeurs de la colonne :", font=("Arial", 12), bg="#F4FEFE",fg="#002147").place(x=padding_x, y=y_start_update + 130)

        self.value_var_update = tk.StringVar(self)
        self.value_dropdown_update = ttk.Combobox(self, textvariable=self.value_var_update, state="readonly", style="TCombobox")
        self.value_dropdown_update.place(x=padding_x, y=y_start_update + 160)

        tk.Label(self, text="Entrez la valeur à remplacer :", font=("Arial", 12), bg="#F4FEFE",fg="#002147").place(x=padding_x, y=y_start_update + 190)
        self.replace_data_entry = ttk.Entry(self, style="Rounded.TEntry", width=25)
        self.replace_data_entry.place(x=padding_x, y=y_start_update + 220)

        self.button_update = ttk.Button(self, text="Remplacer par cette valeur", command=self.update_data, style="TButton")
        self.button_update.place(x=padding_x, y=y_start_update + 270)

        # Section Supprimer des données
        x_start_delete = 800
        y_start_delete = y_start
        tk.Label(self, text="Sélectionner une table :", font=("Arial", 12), bg="#F4FEFE",fg="#002147").place(x=x_start_delete, y=y_start_delete)

        self.table_var_delete = tk.StringVar(self)
        self.table_dropdown_delete = ttk.Combobox(self, textvariable=self.table_var_delete, state="readonly", style="TCombobox")
        self.table_dropdown_delete.bind("<<ComboboxSelected>>", self.load_columns_delete)
        self.table_dropdown_delete.place(x=x_start_delete, y=y_start_delete + 30)

        tk.Label(self, text="Sélectionner une colonne :", font=("Arial", 12), bg="#F4FEFE").place(x=x_start_delete, y=y_start_delete + 70)

        self.column_var_delete = tk.StringVar(self)
        self.column_dropdown_delete = ttk.Combobox(self, textvariable=self.column_var_delete, state="readonly", style="TCombobox")
        self.column_dropdown_delete.bind("<<ComboboxSelected>>", self.display_column_values_delete)
        self.column_dropdown_delete.place(x=x_start_delete, y=y_start_delete + 120)

        tk.Label(self, text="Valeurs de la colonne :", font=("Arial", 12), bg="#F4FEFE").place(x=x_start_delete, y=y_start_delete + 160)

        self.value_var_delete = tk.StringVar(self)
        self.value_dropdown_delete = ttk.Combobox(self, textvariable=self.value_var_delete, state="readonly", style="TCombobox")
        self.value_dropdown_delete.place(x=x_start_delete, y=y_start_delete + 190)

        self.button_delete = ttk.Button(self, text="Supprimer cette valeur", command=self.delete_data, style="TButton")
        self.button_delete.place(x=x_start_delete, y=y_start_delete + 230)

        # Bouton Retour
        self.back_button = ttk.Button(self, text="Retour", command=lambda: self.show_frame("MainMenuPage"), style="TButton")
        self.back_button.pack(side="bottom", pady=30)  # Positionné au bas de la fenêtre

        # Charger les tables dans les menus déroulants
        self.load_and_update_tables()

    def add_values(self):
        """
        Permet d'ajouter des valeurs
        :return:
        """
        table_name = self.table_var_add_data.get() #table concernee
        if table_name =="": #si table inexistante on arrete
            return None #idem, pour visuel
        values = self.data_entry.get().strip() #.strip() enleve les espace inutiles autour des valeurs a ajouter
        values_list = []
        #on creer une liste contenant les valeurs a ajouter sans espaces genants autour
        for val in values.split(","):
            value = val.strip()
            values_list.append(value)

        column_names = self.datamanager.get_column_names(table_name) #on recupere les colonnes de la table

        try: #on verifie que l action est possible : Contraintes + nbr de valeurs a ajouter
            if len(column_names) == len(values_list): #nbr de valeurs corrects
                for i in range(len(column_names)): #parcours la liste des colonnes
                    #on en verifie le domaine et le respect de celui ci par la valeur
                    check = self.datamanager.check_domain(table_name, column_names[i], values_list[i])
                    if not check: #si la contrainte nest pas respecte
                        raise ValueError("vérifier le domaine des données") #erreur ;)
            else: #si pas le bon nbr de valeur par rprt au colonnes
                self.datamanager.add_values_to_table(table_name, values_list, column_names) #erreur ;)
            self.datamanager.add_values_to_table(table_name, values_list, column_names)
            #ajoute potentiellement les donnees si pas dautres erreurs

        except sqlite3.OperationalError as sqe: #souvent erreur de nbr
            #message derreur, idem pour les autres label en rouge
            messagebox.showerror("Erreur", f"Un problème est survenu avec les valeurs :\n{sqe}")
            #message derreurs avec message box, par forcement plus joli mais plus intuitif
            return None

        except ValueError as dme: #erreur de domaines
            messagebox.showerror("Erreur", f"Un problème est survenu avec le domaine des valeurs :\n{dme}")
            return None

        #label en vert soit la reussite de l action (idem pour les autres), les valeurs sont ajoutees
        messagebox.showinfo("Succès", "Les valeurs ont bien été ajoutées")
        self.load_and_update_tables() #on actualise les valeurs et tables, idem pour la suite

    def update_data(self):
        """
        Permet de mettre a jour une donnee
        :return:
        """
        #table, colonne et valeur concernee
        selected_table = self.table_var_update.get()
        selected_column = self.column_var_update.get()
        selected_value = self.value_var_update.get()

        #nouvelle valeur
        changed_value = self.replace_data_entry.get().strip() #idem pour le .strip()

        try: #on verifie les eventuelles contraintes : domaines surtout
            check = self.datamanager.check_domain(selected_table, selected_column, changed_value)
            if not check:
                raise ValueError("vérifier le domaine des données") #si domaine non respecte alors erreur
            self.datamanager.update_database(selected_table, selected_column, selected_value, changed_value)
            #mise a jour de la base de donnee

        except ValueError as dme: #si ereur de domaine
            messagebox.showerror("Erreur", f"Un problème est survenu avec la saisie :\n{dme}")
            return None

        except sqlite3.OperationalError as sqe: #autre erreur potentielle de sqlite
            messagebox.showerror("Erreur", f"Un problème est survenu avec la saisie :\n{sqe}")
            return None

        messagebox.showinfo("Succès", "Les modifications ont été prises en compte")
        self.load_and_update_tables() #idem

    def delete_data(self):
        """
        Supprime une donnee et sa ligne
        :return:
        """
        #table, colonne et valeur concernee
        selected_table = self.table_var_delete.get()
        selected_column = self.column_var_delete.get()
        selected_value = self.value_var_delete.get()
        try: #on verifie si il n y a pas d erreur venant de sqlite
            self.datamanager.delete_value(selected_table, selected_column, selected_value)
            #supprime une valeur
        except sqlite3.OperationalError as sqe:
            messagebox.showerror("Erreur", f"Un problème est survenu avec la saisie :\n{sqe}")
            return None

        messagebox.showinfo("Succès", f"La donnée : {selected_value} a bien été supprimée")
        self.load_and_update_tables()

    def load_columns_update(self, event=""):
        """
        Permet de charger les colonnes dans le menu deroulant
        servant la mise à jour de donnees
        :return:
        """
        self.load_columns("update")#appelle une autre fonction avec lutilite concernee

    def load_columns_delete(self, event=""):
        """
        Permet de charger les colonnes dans le menu deroulant
        servant la mise à jour de donnees
        :return:
        """
        self.load_columns("delete")#idem avec utilite de supprimer

    def load_columns(self, utility):
        """
        Charge les colonnes dans le menu deroulant concerne
        :param utility: menu deroulant concerne
        :return:
        """
        table_name = eval(f"self.table_var_{utility}.get()") #table selectionne
        try: #on essaie d obtenir les colonnes de la table selectionnee
            columns = self.datamanager.get_column_names(table_name)
        except: #si jamais erreur (table inexistante par exe)
            return None
        dropdown = eval(f"self.column_dropdown_{utility}") #on met a jour le menu deroulant
        dropdown["values"] = columns

        if columns:
            eval(f"self.column_var_{utility}.set(columns[0])") #idem

    def display_column_values_update(self, event=""):
        """
        meme principe que pour les colonnes mais cette fois pour les valeurs
        ici pour le menu servant a la mise a jour
        :return:
        """
        self.display_column_values("update")

    def display_column_values_delete(self, event=""):
        """
        servant ici a la suppression
        :return:
        """
        self.display_column_values("delete")

    def display_column_values(self, utility):
        """
        Permet de mettre a jour les menus deroulants en fct de
        leur utilite quant a des valeurs de colonnes selectionnees
        :param utility: type du menu deroulant
        :return:
        """
        #table et colonne selectionees
        table_name = eval(f"self.table_var_{utility}.get()")
        column_name = eval(f"self.column_var_{utility}.get()")

        try: #on essaie de voir si la colonne existe et sans erreur
            values = self.datamanager.get_column_values(table_name, column_name)
        except:
            return None
        dropdown = eval(f"self.value_dropdown_{utility}") #on met a jour le menu deroulant des valeurs
        dropdown["values"] = values

        if values:
            eval(f"self.value_var_{utility}.set(values[0])") #idem
        else:
            eval(f"self.value_var_{utility}.set('')") #si pas de valeurs

    def load_and_update_tables(self):
        """
        Permet de mettre a jour les differents widgets apres
        une modification de la base de donnees
        Charge les noms des tables les affiche dans les menus déroulants.
        :return:
        """
        tables = self.datamanager.get_tables() #obtention des tables
        table_names = []
        for table in tables:
            table_names.append(table[0]) #recupere les noms de table

        # Mise à jour des menus déroulants
        for command in ("add", "update", "delete"): #en fonction des differents widgets et leurs utilite
            dropdown = eval(f"self.table_dropdown_{command}") #on les met a jour avec les nouvelles valeurs
            dropdown["values"] = table_names

        if table_names:
            for command in ("add_data", "update", "delete"): #idem avec la premiere valeur affichee du menu deroulant
                var = eval(f"self.table_var_{command}")
                var.set("")

            for command in ("update", "delete"): #idem avec les menu deroulant des valeurs et colonnes
                var = eval(f"self.column_var_{command}")
                var.set("")
                var = eval(f"self.value_var_{command}")
                var.set("")

        for command in ("data", "replace_data"): #et enfin idem pour les champs de texte
            entry = eval(f"self.{command}_entry") #les vide
            entry.delete(0, tk.END)