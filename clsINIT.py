import configparser
from tools import Tools

# entrées du fichier INI
# constants
kSETTINGS       = 'Settings'
kVERSION        = 'version'
kDEBUG          = 'debug'
kEXECUTABLE     = 'executable'      # nom de l'exécutable

kINI            = 'INI'

kLOG            = 'LOG'
KLOGLEVEL		= "NIVEAU"			# 10 par défaut
KLOGLEVELMAIL	= "NIVEAUMAIL"      # 5 par défaut
KLOGDIR			= "LOGDIR"			# RepExe par défaut
KLOGSIZE		= "LOGSIZE"			# 10 Mb par défaut
kLOGRETENTION	= "LOGRETENTION"	# 30 Jours par défaut
KDESTINATAIRE	= "DESTINATAIRE"
KLOGSERVEUR		= "SERVEUR"			# Serveur des logs
KLOGUSER		= "USERID"			# UserID de connexion
KLOGPW			= "PW"				# PW
KLOGSERVERTYPE	= "SERVEURTYPE"		# Type de serveur (HFSQL...)
KLOGINTABLE		= "LOGINTABLE"		# Sauve le log dans la base de donnée et pas dans le fichier Log... 


class clsINIT:
    def __init__(self, config_file):
       
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)
        self.init_config()  # Initialisation de la configuration
    
    def init_config(self):
        """
        Vérification et initialisation des sections et options
        Crée les entrées par défaut si elles n'existent pas

        Attention :
        - Si le fichier INI n'existe pas, il sera créé avec les valeurs par défaut.
        - Si le fichier INI existe mais manque de certaines sections ou options,
          elles seront ajoutées avec les valeurs par défaut.
        - seul la variable confi est utilisée pour la configuration  
        - la variable config est un objet de type ConfigParser
          il sera nécesaire de l'écrire dans le fichier INI défini dans le constructeur
        - la méthode save_config doit être appelée pour enregistrer les modifications
        """
        changed: bool = False

        # Settings
        if not self.config.has_section(kSETTINGS):
            self.config.add_section(kSETTINGS)
            changed = True
        if not self.config.has_option(kSETTINGS, kVERSION):
            self.config.set(kSETTINGS, kVERSION, '1.0.0')
            changed = True
        if not self.config.has_option(kSETTINGS, kDEBUG):
            self.config.set(kSETTINGS, kDEBUG, 'False')
            changed = True
        if not self.config.has_option(kSETTINGS, kEXECUTABLE):
            self.config.set(kSETTINGS, kEXECUTABLE, 'RepExe')
            changed = True
        # INI
        if not self.config.has_section(kINI):
            self.config.add_section(kINI)
            changed = True
        # LOG 
        if not self.config.has_section(kLOG):
            self.config.add_section(kLOG)
            changed = True
        if not self.config.has_option(kLOG, KLOGLEVEL):
            self.config.set(kLOG, KLOGLEVEL, '10')
            changed = True
        if not self.config.has_option(kLOG, KLOGLEVELMAIL):
            self.config.set(kLOG, KLOGLEVELMAIL, '5')
            changed = True
        if not self.config.has_option(kLOG, KLOGDIR):
            self.config.set(kLOG, KLOGDIR, 'RepExe')
            changed = True
        if not self.config.has_option(kLOG, KLOGSIZE):
            self.config.set(kLOG, KLOGSIZE, '10')
            changed = True
        if not self.config.has_option(kLOG, kLOGRETENTION):
            self.config.set(kLOG, kLOGRETENTION, '30')
            changed = True
        if not self.config.has_option(kLOG, KDESTINATAIRE):
            self.config.set(kLOG, KDESTINATAIRE, '')
            changed = True
        if not self.config.has_option(kLOG, KLOGSERVEUR):
            self.config.set(kLOG, KLOGSERVEUR, '')
            changed = True
        if not self.config.has_option(kLOG, KLOGUSER):
            self.config.set(kLOG, KLOGUSER, '')

        if not self.config.has_option(kLOG, KLOGPW):
            self.config.set(kLOG, KLOGPW, '')
            changed = True
        if not self.config.has_option(kLOG, KLOGSERVERTYPE):
            self.config.set(kLOG, KLOGSERVERTYPE, '')
            changed = True
        if not self.config.has_option(kLOG, KLOGINTABLE):
            self.config.set(kLOG, KLOGINTABLE, 'False')
            changed = True
        # Enregistrer les modifications si nécessaire
        if changed:
            self.save_config()

    def save_config(self):
        """
        Enregistre la configuration dans le fichier INI
        """
        with open(self.config_file, 'w') as f:
            self.config.write(f)

    def get_ini_value(self, section, option):
        """
        Récupère la valeur d'une option dans une section
        """
        try:
            return self.config.get(section, option)
        except:
            return None
# section Settings
    @property
    def version(self) -> str:
        return self.get_ini_value(kSETTINGS, kVERSION)


    @property
    def debug(self) -> bool:
        return self.get_ini_value(kSETTINGS, kDEBUG).lower() == 'true'
    
    
    @property
    def executable(self) -> str:
        return self.get_ini_value(kSETTINGS, kEXECUTABLE)
    
# section INI
    @property
    def ini(self) -> str:
        return self.get_ini_value(kINI, kINI)
    
# section LOG
    @property
    def log_level(self) -> int:
        return int(self.get_ini_value(kLOG, KLOGLEVEL))

    @property
    def log_level_mail(self) -> int:
        return int(self.get_ini_value(kLOG, KLOGLEVELMAIL))

    @property
    def log_dir(self) -> str:
        repertoire_log = self.get_ini_value(kLOG, KLOGDIR).upper()
        if repertoire_log is None or repertoire_log == '' or repertoire_log == '-1' or repertoire_log == 'RepExe':
            repertoire_log = Tools.get_current_directory()
        elif repertoire_log == Tools.kREPDONNEES:
            repertoire_log = Tools.get_common_data_dir(self.executable)
        if repertoire_log[-1] != Tools.get_separator():
            repertoire_log += Tools.get_separator()
        return repertoire_log

    @property
    def log_size(self) -> int:
        return int(self.get_ini_value(kLOG, KLOGSIZE))

    @property
    def log_retention(self) -> int:
        return int(self.get_ini_value(kLOG, kLOGRETENTION))

    @property
    def log_destinataire(self) -> str:
        return self.get_ini_value(kLOG, KDESTINATAIRE)

    @property
    def log_serveur(self) -> str:
        return self.get_ini_value(kLOG, KLOGSERVEUR)

    @property
    def log_user(self) -> str:
        return self.get_ini_value(kLOG, KLOGUSER)

    @property
    def log_pw(self) -> str:
        return self.get_ini_value(kLOG, KLOGPW)

    @property
    def log_server_type(self) -> str:
        return self.get_ini_value(kLOG, KLOGSERVERTYPE)

    @property
    def log_in_table(self) -> bool:
        return self.get_ini_value(kLOG, KLOGINTABLE).lower() == 'true'
