import tkinter as tk
from EnterPage import ConnexionPage
from MainMenu import MainMenuPage
from TableShow import TableShowPage
from SearchPage import SearchPage
from TableUpdatePage import TableUpdatePage
from DataUpdatePage import DataUpdatePage
from JsonViewerPage import JsonViewerPage
import database as dt
#import de tous les modules necessaires

#verifier modif (recherceh avec id, cle primaire avec Eleve par exe)
#commentaires
#passer en .exe
#rendre plus joli
#00000 D1D1D1 002147 28344d 3f2621

class NSI_BDDapp(tk.Tk):
    """
    classe principale lancement du programme tktinter
    """
    def __init__(self):
        super().__init__()
        self.title("NSI BDD Platform") #titre de la fenetre
        self.geometry("1200x720")  #def la taille initiale de la fenetre
        self.minsize(width=1200, height=720)  #taille minimale
        self.attributes('-zoomed', True)  #plein écran
        self.frames = {}
        self.database_name = "membres.db" #nom de la base de donnée (peut etre changee cf l50)
        self.datamanager = dt.Datamanager(self.database_name, dt.Requestmanager()) #creation du gestionnaire de donnee
        for F in (TableShowPage,SearchPage,DataUpdatePage,TableUpdatePage,JsonViewerPage):
            #Loop dans les differentes pages et les initialise
            frame = F(self, self.show_frame, self.datamanager)
            self.frames[F.__name__] = frame #en les stockant dans un dico, clé : nom de la page, valeur : son instance
        #cas a part ne necessitant pas de datamanager mais de la fct reset_frame
        self.frames[MainMenuPage.__name__] = MainMenuPage(self, self.show_frame, self.reset_frame)
        self.frames[ConnexionPage.__name__] = ConnexionPage(self, self.show_frame, self.get_datamanager)

        self.show_frame("ConnexionPage") #Affichage initiale de la page de connexion

    def show_frame(self, frame_name):
        """
        Masquer toutes les frames et afficher celle demandée
        In : le nom de la page (frame) demandee
        """
        for frame in self.frames.values():
            frame.pack_forget() #"enlève" de l affichage toutes les frames
        self.frames[frame_name].pack(expand=True, fill="both")#affiche seulement la frame demandée

    def reset_frame(self, frame_name):
        """
        Permet de reinitialiser les frames et leurs valeurs
        En quelque sorte un bidouillage pour toujours afficher la derniere version de
        la base de donnee en reconfigurant les widgets
        In: le nom de page a reset
        """
        self.frames.pop(frame_name) #enleve l ancienne frame
        frame = eval(frame_name)(self, self.show_frame, self.datamanager) #reconfigure une instance identique
        self.frames[frame_name] = frame #la rajoute au dico

    def get_datamanager(self, name):
        """
        Permet d'éventuellement changer de base de donnée et
        donc de datamanager
        In : nom de la base de donnee autre que membres.db
        """
        try: #on essaie de voir si le fichier existe (peut etre fait autrement try/except ici...)
            database = open(f"{name}.db") #eventuelle ouverture du fichier
            database.close()
        except FileNotFoundError: #si le fichier n existe pas
            # on ouvre par defaut membres.db et utilise le datamanager deja cree
            print("La base de donnée n'existe pas, ouverture par défaut de", self.database_name)
            return None #arret de la fct (return simple marche mais plus visuel avec le None)
        #sinon on creer un nouveau datamanager pour cette autre base de donnee (cf classe Requestmanager)
        self.datamanager = dt.Datamanager(f"{name}.db", dt.Requestmanager(False))

    def closing(self):
        """
        Permet de fermet convenablement la fenetre tkinter
        et aussi la liaison avec la base de donnees
        """
        self.datamanager.commit(True) #on commit et ferme la liaison
        self.destroy() #arret de la boucle tktinter

if __name__ == "__main__":
    #lancement du programme tktiner en tant que main
    app = NSI_BDDapp()
    app.protocol("WM_DELETE_WINDOW", app.closing) #fonction pour clore le prgrmm ci dessus
    app.mainloop()
