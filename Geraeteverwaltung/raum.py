import sqlite3
import xml.etree.ElementTree as ET
import os

class Raum:

    def __init__(self):
        pass
    
    #-----------
    #Raumliste 
    #-----------
    def raum_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\Raum.xml')  

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        cursor.execute("DROP TABLE IF EXISTS Raum")
        cursor.execute("CREATE TABLE IF NOT EXISTS Raum ('ID_Raum' TEXT, Raum TEXT)")
        
        raum_tree = ET.parse(xml_file_path)

        raum_xml_root = raum_tree.getroot()

        #Testen, ob Feld gefüllt ist oder nicht
        for child in raum_xml_root:
            id_raum_element = child.find('ID_Raum')
            if id_raum_element is not None:
                id_raum = id_raum_element.text
            else:
                id_raum = None

            raum_element = child.find('Raum')
            if raum_element is not None:
                raum = raum_element.text
            else:
                raum = None

            #cursor.execute("ALTER TABLE Ware RENAME COLUMN 'Inventar_x0020_Nr' TO Inventarnr")
            cursor.execute("INSERT INTO Raum ('ID_Raum', Raum) VALUES (?, ?)", (id_raum, raum))
            


            #cursor.execute("PRAGMA table_info('Ware')")
            #print(cursor.fetchall())

        conn.commit()
        conn.close()
