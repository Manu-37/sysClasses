import os
import platform
import inspect
import uuid
import time
from datetime import datetime, timedelta

class Tools:
    # constants
    kREPDONNEES = 'REPDONNEES'  # Répertoire des données    

    @staticmethod
    def list_file(chemin_d_acces, type_fichier=None, prefixe_fichier=None, contient_nom=None) -> list:
        """
        Retourne la liste des fichiers (sans les sous-répertoires) du chemin d'accès,
        éventuellement filtrée par type (extension), préfixe, ou si le nom contient une chaîne.
        """
        if not os.path.exists(chemin_d_acces):
            os.makedirs(chemin_d_acces)
        
        liste_fichiers = os.listdir(chemin_d_acces)
        fichiers_seuls = [f for f in liste_fichiers if os.path.isfile(os.path.join(chemin_d_acces, f))]
        
        # Filtre par extension si précisé (ex: type_fichier='.txt')
        if type_fichier != '*' and type_fichier is not None:
            fichiers_seuls = [f for f in fichiers_seuls if f.endswith(type_fichier)]
        
        # Filtre par préfixe si précisé
        if prefixe_fichier:
            fichiers_seuls = [f for f in fichiers_seuls if f.startswith(prefixe_fichier)]
        
        # Filtre "contient" si précisé
        if contient_nom:
            fichiers_seuls = [f for f in fichiers_seuls if contient_nom in f]
        
        return fichiers_seuls
    
    @staticmethod
    def get_current_directory() -> str:
        """
        Retourne le répertoire de travail actuel. agémenté 
        d'un séparateur de répertoire à la fin.
        """
        repertoire_courant = os.getcwd()
        if repertoire_courant[-1] != os.sep:
            repertoire_courant += os.sep
        return repertoire_courant
    
    @staticmethod
    def get_common_data_dir(app_name):
        system = platform.system()
        if system == "Windows":
            base = os.environ.get('PROGRAMDATA', r'C:\ProgramData')
            return os.path.join(base, app_name)
        elif system == "Darwin":  # macOS
            return f"/Library/Application Support/{app_name}"
        else:  # Linux et autres Unix
            return f"/var/lib/{app_name}"

    @staticmethod
    def date_du_jour() -> str:
        """
        Retourne la date du jour au format 'YYYY-MM-DD'.
        """
        
        return datetime.today().strftime('%Y-%m-%d')
    
    @staticmethod
    def maintenant() -> str:
        """
        Retourne l'heure actuelles au format 'HH:MM:SS'.
        """
        return datetime.now().strftime('%H:%M:%S')
    
    @staticmethod
    def date_en_date(Date_str: str) -> datetime:
        """
        Convertit une chaîne de caractères représentant une date au format 'YYYY-MM-DD'
        en un objet datetime.
        """
        try:
            return datetime.strptime(Date_str, '%Y-%m-%d')
        except ValueError as e:
            return datetime.strptime(Tools.Date_du_jour(), '%Y-%m-%d')

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """
        Retourne la taille du fichier en octets.
        le fichier fourni en paramètre doit être le path complet du fichier.
        Si le fichier n'existe pas, une exception FileNotFoundError est levée.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Le fichier '{file_path}' n'existe pas.")
        
        return os.path.getsize(file_path)
    
    @staticmethod
    def get_function_name() -> str: 
        """
        Retourne le nom du fichier, de la classe et de la fonction appelante sous la forme Fichier/Classe/Méthode.
        """
        frame = inspect.currentframe()
        if frame is not None:
            caller_frame = frame.f_back
            if caller_frame is not None:
                # Nom du fichier
                fichier = os.path.basename(caller_frame.f_code.co_filename)
                # Nom de la classe (si self ou cls dans locals)
                classe = None
                if 'self' in caller_frame.f_locals:
                    classe = caller_frame.f_locals['self'].__class__.__name__
                elif 'cls' in caller_frame.f_locals:
                    classe = caller_frame.f_locals['cls'].__name__
                else:
                    classe = ""
                # Nom de la méthode/fonction
                methode = caller_frame.f_code.co_name
                return f"{fichier}/{classe}/{methode}"
        return "UnknownFunction"
    
    @staticmethod
    def get_function_name_2() -> str: 
        """
        Retourne le nom du fichier, de la classe et de la fonction appelante au niveau -2,
        sous la forme Fichier/Classe/Méthode.
        """
        frame = inspect.currentframe()
        if frame is not None:
            caller_frame = frame.f_back
            if caller_frame is not None:
                caller2_frame = caller_frame.f_back
                if caller2_frame is not None:
                    fichier = os.path.basename(caller2_frame.f_code.co_filename)
                    if 'self' in caller2_frame.f_locals:
                        classe = caller2_frame.f_locals['self'].__class__.__name__
                    elif 'cls' in caller2_frame.f_locals:
                        classe = caller2_frame.f_locals['cls'].__name__
                    else:
                        classe = ""
                    methode = caller2_frame.f_code.co_name
                    return f"{fichier}/{classe}/{methode}"
        return "UnknownFunction"
    
    @staticmethod
    def get_guid() -> str:
        """
        Génère un UUID unique. Avec tirets.
        """
        return str(uuid.uuid4())
        
    @staticmethod
    def get_guid_brut() -> str:
        """
        Retourne un GUID brut (UUID) sans tirets.
        """
        return uuid.uuid4().hex
    
    @staticmethod
    def delete_file(file_path: str):
        """
        Supprime le fichier spécifié par file_path.
        Si le fichier n'existe pas, une exception FileNotFoundError est levée.
        """
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Le fichier '{file_path}' n'existe pas.")
        
        os.remove(file_path)

    @staticmethod
    def delete_directory(directory_path: str):
        """
        Supprime le répertoire spécifié par directory_path.
        Si le répertoire n'existe pas, une exception FileNotFoundError est levée.
        """
        if not os.path.isdir(directory_path):
            raise FileNotFoundError(f"Le répertoire '{directory_path}' n'existe pas.")
        
        os.rmdir(directory_path)

    @staticmethod
    def add_days_to_date(date_date: datetime, days: int) -> datetime:
        """
        Ajoute un nombre de jours à une date donnée.
        La date doit être au format 'YYYY-MM-DD'.
        Retourne la nouvelle date au format 'YYYY-MM-DD'.
        """

        return date_date + timedelta(days=days)
    
    @staticmethod
    def get_nom_reseau() -> str:
        """
        Retourne le nom du réseau de l'ordinateur.
        """
        try:
            return platform.node()
        except Exception as e:
            return None
        
    @staticmethod 
    def get_separator() -> str:
        """
        Retourne le séparateur de répertoire utilisé par le système d'exploitation.
        """
        return os.sep

    @staticmethod
    def cree_fichier_si_inexistant(chemin_fichier: str):
        """
        Crée un fichier s'il n'existe pas déjà.
        Si le répertoire parent n'existe pas, il est créé.
        """
        if not os.path.exists(os.path.dirname(chemin_fichier)):
            os.makedirs(os.path.dirname(chemin_fichier))
        
        if not os.path.isfile(chemin_fichier):
            with open(chemin_fichier, 'w') as f:
                pass

    @staticmethod
    def get_current_time() -> float:
        """
        Retourne l'heure actuelle au format float.
        """
        return time.time()
    
    @staticmethod
    def verifier_methode(objet, nom_methode):
        """
        Vérifie si la méthode passée en paramètre existe et est appelable dans l'instance.
        Retourne True si oui, sinon lève une exception.
        """
        if hasattr(objet, nom_methode):
            methode = getattr(objet, nom_methode)
            if callable(methode):
                return True
            else:
                raise Exception(f"La méthode {nom_methode} n'est pas appelable")
        else:
            raise Exception(f"La méthode {nom_methode} n'existe pas.")
        
    @staticmethod
    def methode_existe(objet,nom_methode) -> bool:
        """
        Vérifie si une méthode existe dans l'objet. Renvoie 
        Vrai si la méthode existe, faux sinon. Ne préjuge pas si la méthode est éxécutable
        """
        if hasattr(objet, nom_methode):
            return True
        else:
            return False