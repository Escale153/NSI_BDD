import tkinter as tk
from tkinter import ttk,font, messagebox
import sqlite3

class TableUpdatePage(tk.Frame):
    """
    Classe de la page de modification des tables
    """
    def __init__(self, parent, show_frame, datamanager):
        super().__init__(parent)
        self.show_frame = show_frame
        self.datamanager = datamanager

        # Titre de la page
        tk.Label(self, text="Modifier les tables", font=("Arial", 24),bg="#F4FEFE").pack(pady=20)

        self.title_font = font.Font(family="Helvetica", size=29, weight="bold")
        self.used_font = font.Font(family="Helvetica", size=14)

        self.style = ttk.Style(self)
        self.configure(bg="#F4FEFE")

        # Styles des widgets
        #Style Entry 
        self.style.configure(
            "Rounded.TEntry",
            relief="flat",
            borderwidth=2,
            fieldbackground="#ffffff",  
            foreground="#002147",   
            insertcolor="#002147",  
            padding=2,
            font=self.used_font
        )
        #Style Bouton
        self.style.configure(
            "TButton",
            relief="flat",
            background="#002147",
            foreground="#FAEFDC",
            font=(self.used_font, 14),
            padding=(10, 5)
        )
        #Map sert a donner de la vie aux boutons
        self.style.map(
            "TButton",
            background=[("active", "#3f2204")],
            foreground=[("active", "#FAEFDC")]
        )
        #Style du combobox
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
        padding_x = 30
        padding_y = 10
        y_start = 0

        # Ajouter une table
        tk.Label(self, text="Ajouter une table", font=self.used_font, bg="#F4FEFE").place(x=padding_x, y=y_start + 170)

        self.add_entry = ttk.Entry(self, width=18, style="Rounded.TEntry")
        self.add_entry.place(x=padding_x, y=y_start + 190)

        tk.Label(self, text="Ajouter des colonnes", font=self.used_font, bg="#F4FEFE").place(x=padding_x, y=y_start + 220)
        tk.Label(self, text="Colonnes (ex: id INTEGER, fonction TEXT):", font=self.used_font, bg="#F4FEFE").place(x=padding_x, y=y_start + 240)

        self.columns_entry = ttk.Entry(self, width=18, style="Rounded.TEntry")
        self.columns_entry.place(x=padding_x, y=y_start + 260)

        self.add_button = ttk.Button(self, text="Ajouter une table", command=self.add_table, style="TButton")
        self.add_button.place(x=padding_x, y=y_start + 290)

        # Supprimer une table
        tk.Label(self, text="Supprimer une table", font=self.used_font, background="#F4FEFE").place(x=padding_x, y=y_start + 360)
        self.table_var_erase_data = tk.StringVar(self)
        self.table_dropdown_erase = ttk.Combobox(self, textvariable=self.table_var_erase_data, state="readonly", style="TCombobox")
        self.table_dropdown_erase.place(x=padding_x, y=y_start + 380)

        self.erase_button = ttk.Button(self, text="Supprimer", command=self.erase_table, style="TButton")
        self.erase_button.place(x=padding_x, y=y_start + 430)

        # Renommer une table
        tk.Label(self, text="Renommer une table", font=self.used_font, bg="#F4FEFE").place(x=padding_x, y=y_start + 500)
        self.table_var_rename = tk.StringVar(self)
        self.table_dropdown_rename = ttk.Combobox(self, textvariable=self.table_var_rename, state="readonly", style="TCombobox")
        self.table_dropdown_rename.place(x=padding_x, y=y_start + 520)

        tk.Label(self, text="Nouveau nom:", font=self.used_font, bg="#F4FEFE").place(x=padding_x, y=y_start + 550)
        self.table_entry = ttk.Entry(self, width=18, style="Rounded.TEntry")
        self.table_entry.place(x=padding_x, y=y_start + 570)

        self.rename_button = ttk.Button(self, text="Renommer", command=self.rename_table, style="TButton")
        self.rename_button.place(x=padding_x, y=y_start + 600)

        # Ajouter une colonne
        tk.Label(self, text="Ajouter une colonne", font=self.used_font, bg="#F4FEFE").place(x=500, y=150)
        self.table_var_append = tk.StringVar(self)
        self.table_dropdown_append = ttk.Combobox(self, textvariable=self.table_var_append, state="readonly", style="TCombobox")
        self.table_dropdown_append.place(x=500, y=190)

        tk.Label(self, text="Nouvelle colonne (ex: ID INTEGER):", font=self.used_font, bg="#F4FEFE").place(x=500, y=230)
        self.add_column_entry = ttk.Entry(self, width=22, style="Rounded.TEntry")
        self.add_column_entry.place(x=500, y=250)

        self.add_column_button = ttk.Button(self, text="Ajouter", command=self.add_column, style="TButton")
        self.add_column_button.place(x=500, y=290)

        # Supprimer une colonne
        tk.Label(self, text="Supprimer une colonne", font=self.used_font, bg="#F4FEFE").place(x=500, y=350)
        self.table_var_delete = tk.StringVar(self)
        self.table_dropdown_delete = ttk.Combobox(self, textvariable=self.table_var_delete, state="readonly", style="TCombobox")
        self.table_dropdown_delete.place(x=500, y=390)

        self.pop_button = ttk.Button(self, text="Selectionner", command=self.load_column_erase, style="TButton")
        self.pop_button.place(x=500, y=430)

        self.column_var_delete = tk.StringVar(self)
        self.column_dropdown_delete = ttk.Combobox(self, textvariable=self.column_var_delete, state="readonly", style="TCombobox")
        self.column_dropdown_delete.place(x=500, y=470)

        self.erase_column_button = ttk.Button(self, text="Supprimer", command=self.erase_column, style="TButton")
        self.erase_column_button.place(x=500, y=500)

        # Renommer une colonne
        tk.Label(self, text="Renommer une colonne", font=self.used_font, bg="#F4FEFE").place(x=950, y=190)
        self.table_var_renamecol = tk.StringVar(self)
        self.table_dropdown_renamecol = ttk.Combobox(self, textvariable=self.table_var_renamecol, state="readonly", style="TCombobox")
        self.table_dropdown_renamecol.place(x=950, y=210)

        self.renamecolumn_button = ttk.Button(self, text="Selectionner", command=self.load_column_rename, style="TButton")
        self.renamecolumn_button.place(x=950, y=250)

        self.column_var_renamecol = tk.StringVar(self)
        self.column_dropdown_renamecol = ttk.Combobox(self, textvariable=self.column_var_renamecol, state="readonly", style="TCombobox")
        self.column_dropdown_renamecol.place(x=950, y=290)

        tk.Label(self, text="Nouveau nom:", font=self.used_font, bg="#F4FEFE").place(x=950, y=320)
        self.columnrename_entry = ttk.Entry(self, width=22, style="Rounded.TEntry")
        self.columnrename_entry.place(x=950, y=360)

        self.rename_column_button = ttk.Button(self, text="Renommer", command=self.rename_column, style="TButton")
        self.rename_column_button.place(x=950, y=400)

        #################################################
        # Bouton retour
        ttk.Button(self, text="Retour", command=lambda: self.show_frame("MainMenuPage"),style="TButton").pack(side="bottom", pady=30)

        # Charger les tables dans les menus déroulants
        self.load_and_update_tables()

    def add_table(self):
        """
        Permet d'ajouter une table
        :return:
        """
        table_name = self.add_entry.get().strip() #idem pour .strip()
        columns = self.columns_entry.get().strip()
        
        columns_list = []
        for col in columns.split(","): #separe et met en forme le nom des nouvelles colonnes
            columns_list.append(col.strip())

        try: #avec try/except on evite certaines erreurs
            self.datamanager.create_table(table_name, columns_list) #creation de la table
        except sqlite3.OperationalError as e: #potentielles erreurs dues a sqlite
            messagebox.showerror("Erreur", f"Un problème est survenu :\n{e}")
            return None
        messagebox.showinfo("Succès", f"La table {table_name} a bien été ajoutée")
        self.load_and_update_tables()

    def erase_table(self):
        """
        Permet de supprimer une table
        :return:
        """
        table_name = self.table_var_erase_data.get()  #table selectionnee
        try: #evite les erreurs dues a sqlite
            self.datamanager.drop_table(table_name) #supprime la table
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erreur", f"Un problème est survenu :\n{e}")
            return None
        messagebox.showinfo("Succès", f"La table {table_name} a bien été supprimée")
        self.load_and_update_tables()

    def rename_table(self):
        """
        Permet de renommer une table
        :return:
        """
        selected_table = self.table_var_rename.get() #table selectionnee
        new_name = self.table_entry.get().strip() #nouveau nom de la table
        try: #evite les erreurs
            self.datamanager.rename_table(selected_table, new_name)
        except sqlite3.OperationalError as e:
                messagebox.showerror("Erreur", f"Un problème est survenu :\n{e}")
                return None
        messagebox.showinfo("Succès", f"La table {selected_table} a bien été renommée en {new_name}")
        self.load_and_update_tables()

    def add_column(self):
        """
        Permet d'ajouter une colonne
        :return:
        """
        selected_table = self.table_var_append.get() #table concernee
        column = self.add_column_entry.get().strip() #nom de la colonne + .strip() deja explique
        name = column.split(" ")[0] #si nom + domaine permet de separer et de retenir le nom pour le label
        try: #idem
            self.datamanager.add_column(selected_table, column)
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erreur", f"Le format de la saisie est incorrect :\n{e}")
            return None
        messagebox.showinfo("Succès", f"La colonne : {column} a bien été ajoutée à la table : {selected_table}")
        self.load_and_update_tables()

    def erase_column(self):
        """
        permet de supprimer une colonne
        :return:
        """
        selected_table = self.table_var_delete.get() #table selectionnee
        selected_column = self.column_var_delete.get() #colonne selectionnee
        try: #toujours pareil
            self.datamanager.drop_column(selected_table, selected_column) #supprime la colonne
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erreur", f"Un problème est survenu :\n{e}")
            return None
        messagebox.showinfo("Succès", f"La colonne {selected_column} a bien été supprimée")
        self.load_and_update_tables()

    def rename_column(self):
        """
        Permet de renommer une colonne
        :return:
        """
        selected_table = self.table_var_renamecol.get() #table concernee
        selected_column = self.column_dropdown_renamecol.get() #colonne concernee
        new_name = self.columnrename_entry.get().strip() #nouveau nom
        try: #iiiiiiiiiidem
            self.datamanager.rename_column(selected_table, selected_column, new_name) #renomme la colonne
        except sqlite3.OperationalError as e:
            messagebox.showerror("Erreur", f"Un problème est survenu :\n{e}")
            return None
        messagebox.showinfo("Succès", f"La colonne : {selected_column} a bien été renommée en {new_name}")
        self.load_and_update_tables()

    def load_column_erase(self):
        """
        cf DataUpdatePage
        :return:
        """
        self.load_columns("delete")

    def load_column_rename(self):
        """
        Cf DataUpdatePage
        :return:
        """
        self.load_columns("renamecol")

    def load_columns(self, utility):
        """
        Cf DataUpdatePage
        Permet de charger les colonnes dans différents menus déroulants
        :param utility: utilité du menu déroulant
        :return:
        """
        table_name = eval(f"self.table_var_{utility}.get()")
        try:
            columns = self.datamanager.get_column_names(table_name)
        except Exception:
            return None
        dropdown = eval(f"self.column_dropdown_{utility}")
        dropdown["values"] = columns

        if columns:
            eval(f"self.column_var_{utility}.set(columns[0])")

    def load_and_update_tables(self):
            """
            cf DataUpdatePage
            Charge les noms des tables les affiche dans les menus déroulants.
            """
            tables = self.datamanager.get_tables()
            table_names = []
            for table in tables:
                table_names.append(table[0])

            # Mise à jour des menus déroulants
            for command in ("erase","rename","append","delete","renamecol"):
                dropdown = eval(f"self.table_dropdown_{command}")
                dropdown["values"] = table_names

            if table_names:
                for command in ("erase_data", "rename", "append", "delete", "renamecol"):
                    var = eval(f"self.table_var_{command}")
                    var.set("")

                for command in ("delete", "renamecol"):
                    var = eval(f"self.column_var_{command}")
                    var.set("")

            for command in ("add", "columns", "table", "add_column", "columnrename"):
                entry = eval(f"self.{command}_entry")
                entry.delete(0, tk.END)