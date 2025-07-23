from clsSQL import clsSQL

class clsMSSQL(clsSQL):
    def __init__(self: str, server: str, database: str, username: str, password: str):
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.connection_string = "Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30"
        self.connection = None
        super().__init__(server, database, username, password, self.connection_string)

        chaine = f"Initialized MSSQL connection with server: {self.server}, database: {self.database}"
        self.log.ecrit_log(10,chaine)
        