import sqlite3
import os

class Typ:

    def __init__(self):
        pass
    
    #-----------
    #Typliste 
    #-----------
    def typ_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        #xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\Typ.xml')  

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS Typ")
        cursor.execute("CREATE TABLE IF NOT EXISTS Typ ('ID_Typ' INT, Bezeichnung TEXT)")

        conn.commit()
        conn.close()