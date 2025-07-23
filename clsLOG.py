from tools import Tools
import inspect
from clsINIT import clsINIT
# Définitions globales de classe.

class clsLOG:
    def __init__(self):
        self.fichier_init = Tools.get_current_directory() + 'config.ini'
        self.init = clsINIT(self.fichier_init)
        self._id_traitement: str = None
    
    @property
    def _log_file(self) -> str:
        """
        retourne le nom du fichier de log
        """

        # définitions de variables 
        elements_fichier: list[str] = []

        liste_fichiers = Tools.list_file(chemin_d_acces=self.init.log_dir,type_fichier=".log")

        if liste_fichiers== []:
            fichier_log= 'LOG_'+ Tools.date_du_jour() + '_01.log'

        else:
            fichier_log = liste_fichiers[-1]

        path_fichier_log = self.init.log_dir + fichier_log
        Tools.cree_fichier_si_inexistant(path_fichier_log)
        Fichier_court = fichier_log.split('.')[0]
        elements_fichier = Fichier_court.split('_')
        rank = int(elements_fichier[2]) #-1
        taille = Tools.get_file_size(path_fichier_log)
        
        if Tools.date_en_date(elements_fichier[1]) < Tools.date_en_date(Tools.date_du_jour()):
            rank = 1
            elements_fichier[1] = Tools.date_du_jour()
            elements_fichier[2] = str(rank).zfill(2)
        else:
            if taille/1000000 > self.init.log_size:
                rank += 1
                elements_fichier[2] = str(rank).zfill(2)
        
        fichier_log = '_'.join(elements_fichier) + '.log'
        path_fichier_log = self.init.log_dir + fichier_log
        Tools.cree_fichier_si_inexistant(path_fichier_log)

        return path_fichier_log

    @property
    def id_traitement(self) -> str:
        """
        Retourne l'ID du traitement en cours.
        """
        if self._id_traitement is None:
            self._id_traitement = Tools.get_guid_brut()
        return self._id_traitement
        
    def clean_log_history(self):
        """
        Nettoie les anciens fichiers de log.
        """
        Date_du_jour = Tools.date_en_date(Tools.Date_du_jour())
        liste_fichiers = Tools.list_file(self.init.log_dir)
        for fichier in liste_fichiers:
            if fichier.startswith('LOG_') and fichier.endswith('.log'):
                date_fichier = Tools.date_en_date(fichier.split('_')[1])
                date_fichier = Tools.add_days(date_fichier, self.init.log_days)
                if date_fichier < Date_du_jour:
                    # Supprimer le fichier de log
                    path_fichier = self.init.log_dir + fichier  
                    Tools.delete_file(path_fichier)
                    self.datecleaned = Date_du_jour

    def ecrit_log(self, severite: int, message: str):
        """
        Écrit un message dans le fichier de log.
        Note sur la sévérité (level). 
        Les valeurs suivantes sont réservées 
        0 : Exception : Interceptée par un traitement ou par le programme --> Tout cas exception devrait porter ce niveau de sévérité
        1 : ERREUR    : Interceptée par un traitement ou par le programme --> tout cas Erreur devrait porter ce niveau de sévérité
        2/3/4, anomalies grave entrainant l'abandon du traitement Le niveau de sévérité est laissé à la libre apréciation du programmeur
        Le code 2 peut être utilisé pour consigner des lancements ou des fins normales de traitement dans le fichier de LOG. 
        de 5 à 10 : Information devant être consignée dans le log, anomalies n'entrainant PAS la fin du traitement, mais pouvant avoir des conséquences à terme
        11 et au delà, ne devrait être utilisé que pour la mise au point des traitements
        La hiérarchie des sévérité doit correspondre à une stricte progression de la sévérité de l'anomalie consignée.
        Un message de niveau 10 ne devrait être qu'une information que l'on souhaite consigner

        Rappel, la consignation n'est effective que si le niveau maximum de sévérité consigné dans le fichier INI n'est pas dépassé. 
        Le niveau de sévérité maximum ne devrait jamais être inférieur à 5, en tout état de cause la limite absolue est 1, sinon les erreus grave ne seront pas consignées. 

        // Pour faciliter l'extraction des fichiers de log, dans le message d'erreur: les CR sont remplacés par || et les tabulations par |. Un fichier de LOG est par conséquent facilement "importable dans Excel par exemple"
        """

        texte_log: str = (
            f"{severite}/{self.init.log_level}\t"
            f"{Tools.date_du_jour()}\t"
            f"{Tools.maintenant()}\t"
            f"{self.init.executable} ({self.init.version})\t"
            f"{Tools.get_nom_reseau()}\t"
            f"{self.id_traitement}\t"
            f"{Tools.get_function_name_2()}\t"
            f"{message.replace(chr(10), '||').replace(chr(9), '|')}\n"
        )
    
        with open(self._log_file, "a", encoding="utf-8") as f:  # "a" pour ajouter à la fin, "w" pour écraser
            f.write(texte_log)