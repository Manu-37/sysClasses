import pyodbc
import warnings
from clsLOG import clsLOG

class clsSQL:
    def __init__(self, server: str, database: str, username: str, password: str, connection_string: str):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection_string = connection_string
        self.connection = None
        self.log = clsLOG()  # Assuming clsLOG is defined in another module
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password};connection_string={self.connection_string}'
            )
            self.log.ecrit_log(10,"Connection successful")
            self.__EstConnecte = True
            return True
        except Exception as e:
            self.log.ecrit_log(0,f"Error connecting to database: {e}")
            self.__EstConnecte = False
            return False

    def close(self):
        if self.connection:
            self.connection.close()
            self.log.ecrit_log(10,"Connection closed")

    def execute_query(self, query: str, header: bool = True) -> list:
        warnings.warn("execute_query est obsolète, utilisez execute_select à la place",
            DeprecationWarning,
            stacklevel=2)
        
        return self.execute_select(query, header)
    
    def execute_select(self, query: str, header: bool = True) -> list:
        if not self.connection:
            self.log.ecrit_log(3,"No active connection to execute query.")
            return None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            
            # data set vide on retourne une liste vide
            if not results:
                self.log.ecrit_log(6,"No results returned from the query.")
                return []
            
            # recupère la liste des colonnes de la requête
            if header:
                columns = [column[0] for column in cursor.description]
                results = [columns] + results
            
            cursor.close()
            self.log.ecrit_log(10,f"Query executed successfully: {query}")
            
            return results
        except Exception as e:
            self.log.ecrit_log(0,f"Error executing query: {e}")
            return None
        
    def execute_DictSelect(self, query: str) -> list[dict]:    
        """
        Exécute une requête SQL et retourne les résultats sous forme de liste de dictionnaires.
        Chaque dictionnaire représente une ligne du résultat, avec les noms de colonnes comme clés.
        """
        Resultats = self.execute_select(query, header=True)
        if Resultats is None or len(Resultats) == 0:
            self.log.ecrit_log(6,"No results returned from the query.")
            return []
        
        entetes = Resultats[0]
        donnees = Resultats[1:]
        return [dict(zip(entetes, ligne)) for ligne in donnees]
    
    def Execute_Insert(self, query: str) -> bool:
        """
        Exécute une requête d'insertion dans la base de données.
        Retourne True si l'insertion a réussi, sinon False.
        """
        if not self.connection:
            self.log.ecrit_log(3,"No active connection to execute insert.")
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            self.log.ecrit_log(10,f"Insert executed successfully: {query}")
            return True
        except Exception as e:
            self.log.ecrit_log(0,f"Error executing insert: {e}")
            return False
    def Execute_Update(self, query: str) -> bool:
        """
        Exécute une requête de mise à jour dans la base de données.
        Retourne True si la mise à jour a réussi, sinon False.
        """
        if not self.connection:
            self.log.ecrit_log(3,"No active connection to execute update.")
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            self.log.ecrit_log(10,f"Update executed successfully: {query}")
            return True
        except Exception as e:
            self.log.ecrit_log(0,f"Error executing update: {e}")
            return False
    def Execute_Delete(self, query: str) -> bool:
        """
        Exécute une requête de suppression dans la base de données.
        Retourne True si la suppression a réussi, sinon False.
        """
        if not self.connection:
            self.log.ecrit_log(3,"No active connection to execute delete.")
            return False
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            self.log.ecrit_log(10,f"Delete executed successfully: {query}")
            return True
        except Exception as e:
            self.log.ecrit_log(0,f"Error executing delete: {e}")
            return False
        
    @property
    def EstConnecte(self) -> bool:
        """
        Propriété pour vérifier si la connexion est active.
        """
        return self.__EstConnecte if hasattr(self, '__EstConnecte') else False
    # La propriété n'a pas de setter par définition car elle ne peut être modifiée en dehors de la classe.
    
    def begin(self):
        """
        Démarre une transaction.
        """
        if not self.EstConnecte:
            self.log.ecrit_log(3,"No active connection to begin transaction.")
            Exception("La connexion n'est pas active.")
            return False
        try:
            self.connection.autocommit = False
            self.cursor = self.connection.cursor().execute("BEGIN TRANSACTION")
            self.log.ecrit_log(11,"Transaction started successfully.")
            return True
        except Exception as e:
            self.log.ecrit_log(0,f"Error starting transaction: {e}")
            return False
        
    def commit(self):
        """
        Commit la transaction en cours.
        """
        if not self.EstConnecte:
            self.log.ecrit_log(3,"No active connection to commit transaction.")
            Exception("La connexion n'est pas active.")
            return False
        try:
            self.connection.commit()
            self.connection.autocommit = True
            self.log.ecrit_log(11,"Transaction committed successfully.")
            return True
        except Exception as e:
            self.log.ecrit_log(0,f"Error committing transaction: {e}")
            return False
    def rollback(self):
        """
        Annule la transaction en cours.
        """
        if not self.EstConnecte:
            self.log.ecrit_log(3,"No active connection to rollback transaction.")
            Exception("La connexion n'est pas active.")
            return False
        try:
            self.connection.rollback()
            self.connection.autocommit = True
            self.log.ecrit_log(11,"Transaction rolled back successfully.")
            return True
        except Exception as e:
            self.log.ecrit_log(0,f"Error rolling back transaction: {e}")
            return False

class Transaction:
    """ Classe pour gérer les transactions avec un contexte de gestion.
    Utilise le gestionnaire de contexte pour assurer que les transactions sont correctement gérées.
    Exemple d'utilisation :
    with Transaction(connexion, logger) as conn:
        # Effectuer des opérations sur la connexion
        conn.execute_query("INSERT INTO table_name (column1, column2) VALUES (value1, value2)")
        Très pratique parce que tout est automatisé, si une erreur survient, la transaction est annulée (rollback),
        sinon elle est validée (commit). Sans avoir besoin de définir explicitemrent les méthodes commit et rollback.
        Applicable là ou les opération d'E/S sont centralisées sur un court segment de code.

        Dans le cas ou une grande quantité de code est exécutée, il est préférable de gérer les transactions
        manuellement en utilisant les méthodes begin, commit et rollback de la classe clsSQL.
        Nb : Le logger est inutilisable en l'état, il ne faut pas passer d'objet clsLOG du tout.
    """
    def __init__(self, connexion, logger=None):
        self.connexion = connexion
        self.logger = logger or getattr(connexion, "logger", None)  # Fallback

    def __enter__(self):
        if self.logger:
            self.logger.info("Début de transaction.")
        self.connexion.begin()
        return self.connexion  # Optionnel mais pratique

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            if self.logger:
                self.logger.info("Transaction validée (commit).")
            self.connexion.commit()
        else:
            if self.logger:
                self.logger.error(
                    f"Erreur détectée, annulation de la transaction (rollback) : {exc_type.__name__} - {exc_val}"
                )
            self.connexion.rollback()
