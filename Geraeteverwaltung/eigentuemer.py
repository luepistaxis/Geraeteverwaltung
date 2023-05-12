import sqlite3
import xml.etree.ElementTree as ET
import os

class Eigentuemer:

    def __init__(self):
        pass
    
    #-----------
    #Eigentümerliste 
    #-----------
    def eigentuemer_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\Eigentümer.xml')  

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        cursor.execute("DROP TABLE IF EXISTS Eigentuemer")
        cursor.execute("CREATE TABLE IF NOT EXISTS Eigentuemer ('ID-Eigentümer' TEXT, 'Eigentümer' TEXT)")
        
        eigentuemer_tree = ET.parse(xml_file_path)

        eigentuemer_xml_root = eigentuemer_tree.getroot()

        #Testen, ob Feld gefüllt ist oder nicht
        for child in eigentuemer_xml_root:
            id_eigentuemer_element = child.find('ID-Eigentümer')
            if id_eigentuemer_element is not None:
                id_eigentuemer = id_eigentuemer_element.text
            else:
                id_eigentuemer = None

            eigentuemer_element = child.find('Eigentümer')
            if eigentuemer_element is not None:
                eigentuemer = eigentuemer_element.text
            else:
                eigentuemer = None

            #cursor.execute("ALTER TABLE Ware RENAME COLUMN 'Inventar_x0020_Nr' TO Inventarnr")
            cursor.execute("INSERT INTO Eigentuemer ('ID-Eigentümer', 'Eigentümer') VALUES (?, ?)", (id_eigentuemer, eigentuemer))
            


            #cursor.execute("PRAGMA table_info('Eigentümer')")
            #print(cursor.fetchall())

            #Datenbank Tabelle sperren
            

        conn.commit()
        conn.close()
