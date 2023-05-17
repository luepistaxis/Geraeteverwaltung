import sqlite3
import xml.etree.ElementTree as ET
import os

class Bewegungsarten:

    def __init__(self):
        pass
    
    #-----------
    #BezeichnungenListe 
    #-----------
    def bewegungsarten_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\Bewegungsarten.xml')  

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        cursor.execute("DROP TABLE IF EXISTS Bewegungsarten")
        cursor.execute("CREATE TABLE IF NOT EXISTS Bewegungsarten ('ID_Bewegungsart' TEXT, Bezeichnung TEXT)")
        
        bewegungsarten_tree = ET.parse(xml_file_path)

        bewegungsarten_xml_root = bewegungsarten_tree.getroot()

        #Testen, ob Feld gefüllt ist oder nicht
        for child in bewegungsarten_xml_root:
            id_bewegungsarten_element = child.find('ID_Bewegungsart')
            if id_bewegungsarten_element is not None:
                id_bewegungsart = id_bewegungsarten_element.text
            else:
                id_bewegungsart = None

            bezeichnung_element = child.find('Bezeichnung')
            if bezeichnung_element is not None:
                bezeichnung = bezeichnung_element.text
            else:
                bezeichnung = None

            cursor.execute("INSERT INTO Bewegungsarten ('ID_Bewegungsart', Bezeichnung) VALUES (?, ?)", (id_bewegungsart, bezeichnung))
            


            #cursor.execute("PRAGMA table_info('Bewegungsart')")
            #print(cursor.fetchall())

        conn.commit()
        conn.close()
