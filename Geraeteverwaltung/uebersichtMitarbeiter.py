import sqlite3
import xml.etree.ElementTree as ET
import os

class UebersichtMitarbeiter:

    def __init__(self):
        pass
    
    #-----------
    #Eigentümerliste 
    #-----------
    def uebersichtMitarbeiter_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        #xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\Eigentümer.xml')  

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        cursor.execute("DROP TABLE IF EXISTS 'Uebersicht_Mitarbeiter'")
        cursor.execute("CREATE TABLE IF NOT EXISTS 'Uebersicht_Mitarbeiter' ('Mitarbeiter' TEXT, 'Inventarnr' TEXT, Bezeichnung TEXT, Typ TEXT, Seriennr TEXT)")
        cursor.execute("INSERT INTO 'Uebersicht_Mitarbeiter' (Mitarbeiter, Inventarnr, Bezeichnung, Typ, Seriennr) VALUES ('Test', 'Test', 'Test', 'Test', 'Test')")
        #cursor.execute("INSERT INTO Eigentuemer ('ID-Eigentümer', 'Eigentümer') VALUES (?, ?)", (id_eigentuemer, eigentuemer))
            


            #cursor.execute("PRAGMA table_info('Eigentümer')")
            #print(cursor.fetchall())

            #Datenbank Tabelle sperren
            

        conn.commit()
        conn.close()
