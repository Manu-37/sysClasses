import json
import csv
from tools import Tools
import xml


class clsETL:

    def __init__(self):
        pass
    
    def etl_input(self, file_name: str, type_etl: str, separateur: str = ";", entete:list = None) -> list:
        """
        Lit un fichier et retourne les données sous forme de liste.
        
        :param file_name: nom du fichier à lire, il s'agit du chemin complet du fichier.
        :param type_etl: Type of ETL operation (e.g., CSV, JSON).
        :cas du CSV : Il est convenu qu'il existe une première ligne d'entête. Dans le cas contraire,
           il faut passer le paramètre entete une liste des entêtes de colonnes sous forme de liste de chaines de caractères.
        :param separateur: séparateur pour les fichiers CSV : valeur par défaut ";"
           le mot clé TAB est admis et sera remplacé par la valeur ad'hoc antislash t.
        :param entete: liste de chaines contenant les entête de colonnes si le fichier CSV n'en contient pas1. N'a de sens que pour les fichiers CSV.
        :return: Liste des données lues depuis le fichier.

        Ce traitement ne supporte pas une source de données SQL, il est réservé à la lecture de fichiers texte.
        """
        self.file_name = file_name
        self.type_etl = type_etl
        self.separateur = separateur
        self.entete = entete
        self.data_source = []  # Initialize an empty list to hold the data source

        if self.separateur == "TAB":
            self.separateur = "\t"

        with open(file=self.file_name, mode="r", encoding="utf-8") as f:
            match self.type_etl.upper():
                case "CSV":
                    if self.entete is None:
                        olSource = csv.DictReader(f, delimiter=self.separateur)
                    else:
                        olSource = csv.DictReader(f, fieldnames=self.entete, delimiter=self.separateur)
                    self.data_source = list(olSource)
                case "JSON":
                    self.data_source = json.load(f)
                case "XML":
                    # Placeholder for XML parsing logic
                    raise NotImplementedError("XML parsing is not implemented yet.")
                case _:
                    raise ValueError(f"Unsupported ETL type: {self.type_etl}")

        return self.data_source
    
    def etl_transform(self, data_source: list[dict], procedure_ETL: str = None) -> list[dict]:
        """
        Transforme les données source en appliquant une procédure ETL.
        
        :param data_source: données à transformer, il s'agit d'une liste de dictionnaire des données à transformer.
           Si procedure_ETL est défini, data_source doit être une liste de dictionnaires.
        :param procedure_ETL: Procédure ETL personnalisée à appliquer sur chaque ligne de données, par défaut None.
          Dans ce cas le paramètre type_etl est ignoré, les données cibles doivent impérativement être au format cible désiré.
        :return: Liste des données transformées.
        """
        self.data_source = data_source
        self.procedure_ETL = procedure_ETL
        self.data_cible = []

        return self.data_cible

    def etl_output(self, file_name: str, data_source: list[dict], type_etl: str, procedure_ETL: str = None, separateur: str = ";"):
        """
        Execute the ETL process.
        
        :param file_name: nom du fichier ou seront sauvegardées les données, il s'agit du chemin complet du fichier.
        :param data_source: données à transformer, il s'agit d'une liste de dictionnaire des données à transformer.
           Si procedure_ETL est défini, data_source doit être une liste de dictionnaires.
        :param type_etl: Type of ETL operation (e.g., CSV, JSON).
           Cas du JSON et du XML : La requête doit IMPERATIVEMENT retourner l'entête de la table.
           Qui sera utilisée pour la transformation.
           Toutes les dates doivent être au format texte "CONVERT(varchar(10), Date, 23)", 
           les dates doivent être au format ISO 8601 (YYYY-MM-DD).
        :param procedure_ETL: Procédure ETL personnalisée à appliquer sur chaque ligne de données, par défaut None.
          Dans ce cas le paramètre type_etl est ignoré, les données cibles doivent impérativement être au format cible désiré.
          De plus 2 procédures sont déduites et appelées si elles existent dans la classe : {nom_procedure_pre} 
          et {nom_procedure_post} où nom_procedure_pre et nom_procedure_post sont les noms des procédures définies dans la classe.
          et sont appelées respectivement avant et après la boucle de transformation des données, ces méthodes n'acceptent
          pas de paramètres autre que self qui est obligatoire et ne retournent rien. Elles sont destinées à effectuer des
          initialisations ou des nettoyages avant et après la transformation des données.
        :param separateur: séparateur pour les fichiers CSV : valeur par défaut ";"
           le mot clé TAB est admis et sera remplacé par la valeur ad'hoc antislash t.
        """
        self.file_name = file_name
        self.data_source = data_source
        self.type_etl = type_etl
        # self.procedure_ETL = procedure_ETL
        # if self.procedure_ETL != None:
        #     # si procedureETL = None on ne calcule pas les pré et post requis puisque par definition ils n'existent pas
        #     self.procedure_ETL_pre = procedure_ETL+"_pre"
        #     self.procedure_ETL_post = procedure_ETL+"_post"
        self.separateur = separateur
        self.data_cible = []  # Initialize an empty list to hold transformed data        

        self._read_data()
        
        # Save the transformed data
        self._save_data()

    def _read_data(self):
        """
            Boucle de lecture des données depuis la source.
        """
        entete: list = []
        if hasattr(self,'procedure_ETL_pre'):
            if self.procedure_ETL_pre != None:
                procedure_ETL_pre = getattr(self, self.procedure_ETL_pre)
                procedure_ETL_pre()
        i = 0
        for ligne in self.data_source:
            i += 1
            if self.procedure_ETL!= None:
                # Effectue les transformations ETL sur la ligne 
                procedure_ETL = getattr(self, self.procedure_ETL)
                ligne=procedure_ETL(ligne)
                self.data_cible.append(ligne)  # Add newline character for CSV/JSON formatting

            else:
                match self.type_etl.upper():
                    case "CSV":
                        # Transform the line for CSV
                        ligne = self._transform_for_csv(ligne)
                        self.data_cible.append(ligne+ "\n")
                    case "JSON":
                        # Transform the line for JSON
                        ligne = self._transform_for_json(ligne)
                        self.data_cible.append(ligne)  # Add newline character for CSV/JSON formatting
                    case "XML":
                        if i == 1:
                            entete = ligne
                        else:
                            ligne_xml = self._transform_for_xml(ligne, entete)
                            self.data_cible.append(ligne_xml)
                    case _:
                        raise ValueError(f"Unsupported ETL type: {self.type_etl}")
        if self.procedure_ETL == None:
            match self.type_etl.upper():
                case "CSV":
                    pass
                case "JSON":
                    self.data_cible = "[\n" + ",\n".join(self.data_cible) + "\n]"
                case "XML": 
                    pass
                    
        if hasattr(self, self.procedure_ETL_post):
            if self.procedure_ETL_post != None:
                procedure_ETL_post = getattr(self, self.procedure_ETL_post)
                procedure_ETL_post()
        
    def _transform_for_csv(self, ligne):
        """
        Transform the data line for CSV format.
        
        :param ligne: Data line to be transformed.
        """
        # Placeholder for CSV transformation logic
        if self.separateur == "TAB":
            self.separateur = "\t"
        return self.separateur.join([str(colonne) for colonne in ligne])
    
    def _transform_for_json(self, ligne):
        """
        Transform the data line for JSON format.
        
        :param ligne: Data line to be transformed.

        """
        return json.dumps(ligne, ensure_ascii=False)

    def _transform_for_xml(self, ligne, entete):
        """
        Transforme une ligne et son entête en chaîne XML.
        """
        xml = ["  <row>"]
        for k, v in zip(entete, ligne):
            xml.append(f"    <{k}>{v}</{k}>")
        xml.append("  </row>")
        return "\n".join(xml)    

    def _save_data(self):
        # Placeholder for saving data to a destination
        if len(self.data_cible) != 0:
            if self.procedure_ETL == None:
                match self.type_etl.upper():
                    case "JSON":
                    # Convert the data_cible to JSON format
                        self.data_cible = json.dumps(self.data_cible, ensure_ascii=False, indent=4)
                    case "CSV":
                        # Join the data_cible with newlines for CSV format
                        self.data_cible = "\n".join(self.data_cible)
                    case "XML":
                    # Encapsule les lignes XML dans une balise racine
                        self.data_cible = "<root>\n" + "\n".join(self.data_cible) + "\n</root>"            
                    
                    case '_':
                        raise ValueError(f"Unsupported ETL type for saving: {self.type_etl}")
            else:
                    pass # data_cible est déjà au format cible désiré
            with open(file=self.file_name, mode="w", encoding="utf-8") as f:  # "a" pour ajouter à la fin, "w" pour écraser
                f.write(self.data_cible)
    
    def _GestionMethodeTransform(self, methode: str):
        """
        Vérifie si la méthode de transformation existe et est callable.
        Génère les nom des méthodes pré et post requises. Et gère les callables de ces méthodes.
        Toute méthode n'existant pas ou n'étant pas callable déclenche une exception pour la méthode principale et 
        la suppression de la méthode pré et post requises.
        """
        if self.procedure_ETL != None:
            if not Tools.methode_existe(self, methode):
                raise Exception(f"La méthode {methode} n'existe pas.")
            if not Tools.verifier_methode(self, methode):
                raise Exception(f"La méthode {methode} n'est pas callable.")
            self.procedure_ETL_pre = methode + "_pre"
            self.procedure_ETL_post = methode + "_post"
            if Tools.methode_existe(self, self.procedure_ETL_pre):
                Tools.verifier_methode(self, self.procedure_ETL_pre)
            else:
                self.procedure_ETL_pre = None
            if Tools.methode_existe(self, self.procedure_ETL_post):
                Tools.verifier_methode(self, self.procedure_ETL_post)
            else:
                self.procedure_ETL_post = None