import sqlite3
import os
import json
from datetime import datetime
#import des differents modules

class Database(object):
    """
    Classe pour la base de donnees en elle meme
    """
    def __init__(self, name):
        self.name = name #nom de la base de donnees
        self.connection = False #pas de connection initialisee
        self.cursor = False #ni de curseur

    def connect(self):
        """
        Permet de se connecter avec le curseur a la base de donnees
        :return: le curseur
        """
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def disconnect(self):
        """
        Permet de se deconnecter
        """
        self.connection.close()

    def commit(self):
        """
        Enregistre les modifications apportees
        """
        self.connection.commit()


class Requestmanager(object):
    """
    Classe concernant les actions operees sur la base membres.db
    Car l appli est relativement utilisable avec une autre
    mais plus de fonctionnalites avec celle ci
    """
    def __init__(self, real=True):
        self.real = real #vaut True uniquement si le datamanager oppere sur membres.db
        
        self.log_file = 'database_modifications.json' #nom du fichier de commit
        
        # Créer le fichier de log si besoin
        if not os.path.exists(self.log_file): #si le fichier nexiste pas
            with open(self.log_file, 'w') as f: #on le creer
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #heure de creation
                json.dump([{"action":"File opening", "commit_time": current_time}], f) #creation et sauvegarde

    def id_research(self, id, cursor):
        """
        permet de renvoyer toutes les infos sur quelqu un a partir
        de son id dans la table membre lors d une recherche dans SearchPage
        permet SURTOUT de caler un JOIN et d avoir une requete répondant
        a cette demande :)
        :param id: id du membre
        :param cursor: curseur pour les requetes
        """
        tables_names = ("Elèves", "Référents", "Intervenants") #ensemble des tables reliees a membre par un id
        for t in range(len(tables_names)): #on cherche a savoir a quelle table l id appartient
            if id // 100 == t: #soit savoir si 0<id<100 ou 100<id<200 ou 200<id<300 (cf table membres)
                table = tables_names[t] #table concernee
        query = f"SELECT membres.*, {table}.* FROM membres JOIN {table} ON {table}.ID = membres.id WHERE membres.id = {id}"
        cursor.execute(query) #soit toutes les infos sur cet id outre la description precise de son activites

    def global_research(self, search_value, cursor):
        """
        Permet d effectuer une recherche plus globale dans la base de donnees
        Les requetes sont ici complexes et permettent de determiner l emplacement
        d une valeur a partir de celle-ci (table et colonnes donc)
        :param search_value: valeur recherchee
        :param cursor: curseur pour la requete
        :return : la ligne comprenant la valeur avec les colonnes correspondantes
        """
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        #requete pour avoir le nom de toutes les tables
        tables = cursor.fetchall()

        #parcours toutes les tables
        for table in tables:
            table_name = table[0] #nom de la table
            #liste des colonnes de la table
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()

            #requête pour rechercher dans toutes les colonnes de la table
            query = f"SELECT * FROM {table_name} WHERE " #1ere partie de la requete
            #on doit savoir quelle colonne se situe la donnee
            query += " OR ".join([f"{column[1]} LIKE ?" for column in columns]) #soit un OR pour chaque colonne

            #enfin on remplace les ? par la valeur donnee et la requete est prete a etre enfournee a 180°C
            cursor.execute(query, (f"%{search_value}%",) * len(columns)) #il y a autant de ? que de colonne
            rows = cursor.fetchall() #resultat de la requete

            if rows: #on prend en compte les resultats
                #on modifie la liste colonne pour la rendre utilisable par la suite du prgrmm(pour le treeview tkinter)
                columns = [(columns[c][1],columns[c][2]) for c in range(len(columns))]
                return (rows, columns)

    def search(self, search_value, cursor):
        """
        Permet d effectuer une recherche dans la base membres.db
        :param search_value: valeur recherchee
        :param cursor: curseur pour la requete
        :return: eventuellement le resultat de la requete dans toute la table (cf global_search())
        """
        if self.real: #si on utilise bien membres.db
            try: #on cherche a savoir si la valeur est un id
                id = int(search_value) #La valeur est elle un entier ?
                if id > 1000: #si pas d erreur est elle inferieure a 1000 ?
                    raise ValueError #si oui on renvoit une errreur
                self.id_research(id, cursor) #sinon on fait la recherche simple avec le JOIN
            except ValueError: #si erreur renvoyee
                return self.global_research(search_value, cursor)#alors on fait une recherce pas dans les id
            return None #idem : None optionnel mais visuel

    def check_keyvalue(self, table, column, value, cursor):
        """
        Permet de savoir si dans la base de donnee membres.db il n y a pas de doublons
        dans les ID lors d ajout ou de mise a jour de donnees
        Cest un debut vers le respect total des contraintes
        :param table: table concernee
        :param column: colonne concernee
        :param value: valeur entree
        :param cursor: curseur
        :return: Booleen en fonction de potentiels doublons
        """
        #si la colonne est bien une ID, et que la table est bien dans celles prevues initialement
        if self.real and column=="ID" and table in ("Elèves", "Référents", "Intervenants", "Occupation"):
            cursor.execute(f"SELECT {column} FROM {table}") #on cherche tous les ID possible de la table
            key_values = cursor.fetchall()
            key_values = [key_values[i][0] for i in range(len(key_values))] #les stock sous forme de liste
            if int(value) in key_values: #si la nouvelle valeur existe deja
                #alors on fait remonter une erreur au bloc try/except concerne
                raise sqlite3.OperationalError("Déjà une clé primaire semblable existante")
                return False #arret de la fct
        return True #aucune erreur de generee, on renvoie True
	
    def log_modification(self, action, details):
        """
        Enregistre les actions faites sur la base de donnees membres.db uniquementdans un json
        :param action: action effectuees
        :param details: details sur l action (colonne, table, valeur, etc...)
        :return:
        """
        if self.real:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #heure actuelle
            log_entry = {"action": action, "details": details, "commit_time":current_time} #creer le log

            with open(self.log_file, 'r+') as file: #ouvre le fichier
                logs = json.load(file) #importe les dernieres lignes
                logs.append(log_entry) #ajoute le nouveau commit
                file.seek(0) #reprend a la ligne 0
                json.dump(logs, file, indent=4) #ajoute le contenu ancien et nouveau
    	
    def get_logfile(self):
        """
        :return: Chemin du fichier de log
        """
        return self.log_file
    	
class Datamanager(object):
    """
    Classe pour le gestionnaire de base de donnees
    """
    def __init__(self, base_name, request_manager):
        self.data_base = Database(base_name) #Instance de la base de donnees creee
        self.request_manager = request_manager #instance du gestionnaire spécifique pour membres.db
        self.cursor = self.get_cursor() #obtention du curseur
        self.tables = self.get_tables #obtntion des tables


    def get_cursor(self):
        """
        Permet davoir le curseur
        :return:
        """
        return self.data_base.connect() #retourne le curseur

    def commit(self, disconnect=False):
        """
        Permet de faire un commit et d eventuelement se deconnecter (cf app)
        Deconnexion puis reconnexion plus forcement utiles mais evite
        certains rares problemes
        :param disconnect: si True alors deconnection definitive
        :return:
        """
        self.data_base.commit() #commit
        self.data_base.disconnect() #deconnexion
        if not disconnect: #si on ne se deconnecte pas
            self.cursor = self.get_cursor() #on recreer le curseur

    def get_commitfile_path(self):
        """
        chemin du fichier de log
        """
        return self.request_manager.get_logfile()

    def get_tables(self):
        """
        Permet d obtenir les table de la base de donnees
        :return: les tables
        """
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        # sqlite_master : Une table spéciale qui contient des informations sur la structure de la BDD:
        # on prend que les tables
        tables = self.cursor.fetchall()
        return tables

    def show_table(self, selected_table):
        """
        renvoie les Donnees de la table
        :param selected_table: table concernee
        :return: toutes les donnees de la table y compris sa structure
        """
        # Récupérer les données de la table sélectionnée
        self.cursor.execute(f"SELECT * FROM {selected_table}")
        return self.cursor.fetchall(), self.cursor.description

    def create_table(self, table_name, columns):
        """
        Creation et ajout d une table
        :param table_name: Nom de celle ci
        :param columns: colonnes a ajouter
        :return:
        """
        # On assemble les colonnes en une seule chaîne
        columns_table = ", ".join(columns)
        sql_query = f"CREATE TABLE {table_name} ({columns_table})" #creation de la table

        # Exécution de la requête
        self.cursor.execute(sql_query)
        #modele identiques pour enregistrements suivant pour les commit :
        self.request_manager.log_modification("create_table", {"table_name": table_name, "columns": columns})
        self.commit() #enregistrement des modifs pour la base de donnees

    def rename_table(self, selected_table, new_name):
        """
        Permet de renommer une table
        :param selected_table: table a renommer
        :param new_name: nouveau nom
        :return:
        """
        self.cursor.execute(f"ALTER TABLE {selected_table} RENAME TO {new_name}") #renomme une table
        #idem :
        self.request_manager.log_modification("rename_table", {"old_name": selected_table, "new_name": new_name})
        self.commit()

    def drop_table(self, table_name):
        """
        Permet de supprimer une table
        :param table_name: nom de la table concernee
        :return:
        """
        self.cursor.execute(f"DROP TABLE {table_name}") #supprime la table
        #re-idem :)
        self.request_manager.log_modification("drop_table", {"table_name": table_name})
        self.commit()
    
    def add_values_to_table(self, table_name, values, column_names):
        """
        Ajoute les valeurs à la table demandée
        In : table_name : nom de la table a remplir
        values : valeurs a ajouter
        column_names : colonnes concernees par l ajout de donnees
        """
        columns_str = ", ".join(column_names) #jointure des colonnes

        values_str = ""

        #on verifie si la valeur 1 de la colonne 1 (un potentiel id) ne serait pas en doublon pour membres.db
        self.request_manager.check_keyvalue(table_name, column_names[0], values[0], self.cursor)

        for value in values: #on joint les valeurs a ajouter
            if values_str:
                values_str += ", " #valeurs séparées par des ,
            values_str += f"'{value}'"#les valeurs sont ajoutés et donc mis avec des virgules

        self.cursor.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str})") #ajoute les valeurs
        #rere-idem
        self.request_manager.log_modification("add_values_to_table",{"table_name": table_name, "values": values_str, "column_names": columns_str})
        self.commit()

    def delete_value(self, selected_table, selected_column, selected_value):
        """
        Permet de supprimer une valeur et sa ligne
        :param selected_table: table concernee
        :param selected_column: colonne concernee
        :param selected_value: valeur a supprimer
        :return:
        """
        #requete pour la sppression, le ? est dans les faits remplace par le parametre donne apres : selected_value
        self.cursor.execute(f"DELETE FROM {selected_table} WHERE {selected_table}.{selected_column} = ?",(selected_value,))
        #rerere-idem
        self.request_manager.log_modification("delete_value",{"table_name": selected_table, "column": selected_column, "value": selected_value})
        self.commit()

    def update_database(self, selected_table, selected_column, selected_value, new_value):
        """
        Permet de mettre a jour une donnee precise
        Pourrait etre certes ameliorer si besoin
        :param selected_table: table concernee
        :param selected_column: colonne concernee
        :param selected_value: valeur a changer
        :param new_value: nouvelle valeur
        :return:
        """
        #on verifie si cette nouvelle valeur ne serait pas un probleme de cle primaire
        self.request_manager.check_keyvalue(selected_table, selected_column, new_value, self.cursor)

        #mise a jour de la table:
        self.cursor.execute(f"UPDATE {selected_table} SET {selected_column} = ? WHERE {selected_column} = ?",(new_value, selected_value))
        #j arrete de mettre des idem a partir de maintenant :)
        self.request_manager.log_modification("update_database",{"table_name": selected_table, "column": selected_column, "old_value": selected_value, "new_value": new_value})
        self.commit()

    def add_column(self, selected_table, column):
        """
        Permet d ajouter une colonne dans une table
        :param selected_table: table concernee
        :param column: colonne a ajouter
        :return:
        """
        self.cursor.execute(f"ALTER TABLE {selected_table} ADD {column}") #ajout de la colonne
        #j ai dit que j arretais :)
        self.request_manager.log_modification("add_column", {"table_name": selected_table, "column": column})
        self.commit()

    def drop_column(self, selected_table, selected_column):
        """
        Suppression dune colonne
        :param selected_table: table concernee
        :param selected_column: colonne a supprimer
        :return:
        """
        self.cursor.execute(f"ALTER TABLE {selected_table} DROP COLUMN {selected_column}") #suppression de la colonne
        #tentative d humour ratee ? :/
        self.request_manager.log_modification("drop_column", {"table_name": selected_table, "column": selected_column})
        self.commit()

    def rename_column(self, selected_table, selected_column, new_name):
        """
        Permet de renommer une colonne
        :param selected_table: Table concernee
        :param selected_column: colonne a renommer
        :param new_name: nouveau nom de la colonne
        :return:
        """
        # renomme la colonne :
        self.cursor.execute(f"ALTER TABLE {selected_table} RENAME COLUMN {selected_column} TO {new_name}")
        #...
        self.request_manager.log_modification("rename_column",{"table_name": selected_table, "old_name": selected_column, "new_name": new_name})
        self.commit()

    def get_column_names(self,table_name):
        """
        Permet davoir le nom des colonnes dune table
        :param table_name: table concernee
        :return: nom des colonnes de la table
        """
        if table_name!="": #si table existante
            self.cursor.execute(f"PRAGMA table_info({table_name})") #Permet d'avoir les informations sur la table que l'on recherche
            colonnes = []
            for col in self.cursor.fetchall():#fait une loop dans les infos de la table
                colonnes.append(col[1])#les ajoutes aux collones et le 1 veut dire le nom des tables

            return colonnes
    
    def get_column_values(self, table_name, column_name):
        """
        Permet davoir les valeurs dune colonne
        :param table_name: table concernee
        :param column_name: colonne concernee
        :return: les valeurs de la dite colonne
        """
        query = f"SELECT {column_name} FROM {table_name};" #sélectionne les valeurs
        self.cursor.execute(query)

        # Récupérer les résultats sous forme de liste
        results = []
        for row in self.cursor.fetchall():
            results.append(row[0])
        return results

    def get_request(self, selected_table, selected_column, search_value):
        """
        Permet de gerer une recherche (cf SearchPage), d en faire la requete,
        et de renvoyer le resultat de celle ci
        :param selected_table: table concernee
        :param selected_column: colonne concernee
        :param search_value: valeur recherchee
        :return: resultat de la requete
        """
        results = None #resultat potentiel
        if selected_table == "":  # pas de table selectionnee alors valeur entree
            # on cherche dans la base avec la donnee seule
            results = self.request_manager.search(search_value, self.cursor)

        elif selected_column == "":  # pas de donnee specifique
            return self.show_table(selected_table)  # toute la table

        else:
            if search_value == "":  # alors juste la table et la colonne de specifiees
                self.cursor.execute(f"SELECT {selected_column} FROM {selected_table}")  # toute la colonne affichee

            else:  # sinon recherche spécifique
                self.cursor.execute(f"SELECT * FROM {selected_table} WHERE {selected_table}.{selected_column} = ?",(search_value,))
                # juste une info dans une table

        if results!=None: #si la requete avec une seule donnee a marchee (cf Requestmanager)
            return results[0], results[1] #alors affiche/renvoie celle ci
        return self.cursor.fetchall(), self.cursor.description #sinon autre type de recherche

    def check_domain(self, table_name, column_name, value):
        """
        Permet de verifier que les donnees mises a jour ou ajoutees
        repondent a la contrainte de domaine de leurs colonnes
        C est aussi un debut vers un total respect des contraintes
        :param table_name: table concernee
        :param column_name: colonne concernee
        :param value: valeur a verifiee
        :return: Un booleen en fct de si le domaine est respecte
        """
        self.cursor.execute(f"PRAGMA table_info({table_name});") #recupere les colonnes
        columns = self.cursor.fetchall()
        info = columns[self.get_column_names(table_name).index(column_name)] #informations de la colonne
        #recupere dans lensemble des colonnes les infos qui concernent la colonne donne
        #ligne qui pourrait etre simplifiee dans sa complexité, moins pour sa taille
        column_type = info[2] #domain de la colonne
        if column_type == "INTEGER" or column_type=="INT": #type entier
            try:
                nbr = int(value)#on verifie si on peut passer la valeur en entier
            except ValueError: #si erreur alors la valeur nest pas un entier
                return False #retourne False
            return True #sion True

        elif column_type == "REAL": #meme principe pour un reel
            try:
                nbr = int(value)
                real = float(value)
            except ValueError:
                return False
            return True

        elif column_type == "TEXT" or column_type == "VARCHAR": #meme idee pour un texte
            return isinstance(value, str) #permet de savoir si value est une instance de la classe str (soit string)
            #returne Vrai ou Faux

        else:
            return True  #Pour autres types on considère vrai
