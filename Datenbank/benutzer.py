import sqlite3
import xml.etree.ElementTree as ET
import os

class Benutzer:

    def __init__(self):
        pass
    
    #-----------
    #Benutzer 
    #-----------
    def benutzer_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        cursor.execute("DROP TABLE IF EXISTS Benutzer")
        cursor.execute("CREATE TABLE IF NOT EXISTS Benutzer (benutzer_id TEXT, password TEXT)")
        cursor.execute("INSERT INTO Benutzer (benutzer_id, password) VALUES ('luisa.aslanidis', '1234qwer')")

        conn.commit()
        conn.close()