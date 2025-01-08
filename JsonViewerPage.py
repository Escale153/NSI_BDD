import tkinter as tk
from tkinter import ttk, font
import json

class JsonViewerPage(tk.Frame):
    """
    Classe pour la page d'affichage du fichier de logs
    """
    def __init__(self, parent, show_frame, datamanager):
        super().__init__(parent)

        self.show_frame = show_frame
        self.datamanager = datamanager

        self.title_font = font.Font(family="Helvetica", size=29, weight="bold")
        self.used_font = font.Font(family="Helvetica", size=16)

        self.style = ttk.Style(self)
        self.configure(bg="#D1D1D1")

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
            foreground=[("active", "#FAEFDC")],
        )

        # Titre de la page
        tk.Label(
            self,
            text="Page d'affichage des modifications",
            font=self.title_font,
            bg="#D1D1D1",
            fg="#002147"
        ).pack(pady=(50, 20))

        self.open_button = ttk.Button(self, text="Afficher les commit", style="TButton", command=self.open_file)
        self.open_button.pack(pady=10)

        # Bouton retour
        ttk.Button(self, text="Retour", style="TButton", command=lambda: self.show_frame("MainMenuPage")).pack(pady=10)

        #zone de texte pour afficher les logs
        self.text_area = tk.Text(self, wrap=tk.WORD, height=30, width=80, padx=10, pady=10)
        self.text_area.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        #barre de navigation verticale
        self.scrollbar = ttk.Scrollbar(self.text_area, orient="vertical", command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=self.scrollbar.set) #permet laction de defilement
        self.scrollbar.pack(side="right", fill="y")

    def open_file(self):
        """
        Ouvre le fichier json des logs
        :return:
        """
        file_path = self.datamanager.get_commitfile_path() #permet davoir le chemin du fichier de logs
        if file_path:
            try: #si le fichier json existe, on l'affiche
                with open(file_path, 'r') as file:
                    json_data = json.load(file) #chargement des donnees
                    self.display_json(json_data) #affichage
            except Exception: #si probleme avec le fichier json alors rien ne se passe
                return None

    def display_json(self, json_data):
        """
        Permet dafficher le contenu du fichier json
        :param json_data: donnees a afficher
        :return:
        """
        self.text_area.delete(1.0, tk.END) #on reinitialise la zone de texte

        for idx, entry in enumerate(json_data): #on recupere les differents elements dans les donnees a afficher
            #differents parametres dun commit
            action = entry.get("action", "Unknown Action")
            details = entry.get("details", {})
            commit_time = entry.get("commit_time", "Unknown Time")

            #on insere lelement principal du commit dans la zone de texte
            self.text_area.insert(tk.END, f"Action: {action}\n", ("bold",))
            self.text_area.insert(tk.END, f"Details:\n")

            #suivant les differents details on fait une serie de if/elif/else en fct des differentes configurations
            #puis on insere les details dans la zone de texte
            if "table_name" in details:
                self.text_area.insert(tk.END, f"  Table Name: {details.get('table_name', 'Unknown Table')}\n")

            if "columns" in details:
                columns = details.get("columns", [])
                self.text_area.insert(tk.END, f"  Columns: {', '.join(columns)}\n")

            if "old_name" in details and "new_name" in details:
                old_name = details.get("old_name", "Unknown Old Name")
                new_name = details.get("new_name", "Unknown New Name")
                self.text_area.insert(tk.END, f"  Old Name: {old_name}, New Name: {new_name}\n")

            if "column" in details:
                column = details.get("column", "Unknown Column")
                self.text_area.insert(tk.END, f"  Column: {column}\n")

            if "values" in details:
                values = details.get("values", "")
                self.text_area.insert(tk.END, f"  Values: {values}\n")

            if "column_names" in details:
                column_names = details.get("column_names", "")
                self.text_area.insert(tk.END, f"  Column Names: {column_names}\n")

            if "old_value" in details and "new_value" in details:
                old_value = details.get("old_value", "Unknown Old Value")
                new_value = details.get("new_value", "Unknown New Value")
                self.text_area.insert(tk.END, f"  Old Value: {old_value}, New Value: {new_value}\n")

            if "value" in details:
                value = details.get("value", "Unknown Value")
                self.text_area.insert(tk.END, f"  Value: {value}\n")

            #enfin on insere lheure du commit
            self.text_area.insert(tk.END, f"Commit Time: {commit_time}\n\n")
            self.text_area.insert(tk.END, "#" * 40 + "\n\n")

        #parametre de la zone de texte
        self.text_area.tag_configure("bold", font=("Helvetica", 12, "bold"))
