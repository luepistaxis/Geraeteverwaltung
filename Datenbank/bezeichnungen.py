import sqlite3
import xml.etree.ElementTree as ET
import os

class Bezeichnungen:

    def __init__(self):
        pass
    
    #-----------
    #BezeichnungenListe 
    #-----------
    def bezeichnungen_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\Bezeichnungen.xml')  

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        cursor.execute("DROP TABLE IF EXISTS Bezeichnungen")
        cursor.execute("CREATE TABLE IF NOT EXISTS Bezeichnungen ('ID_Bezeichnung' TEXT, Bezeichnung TEXT)")
        
        bezeichnungen_tree = ET.parse(xml_file_path)

        bezeichnungen_xml_root = bezeichnungen_tree.getroot()

        #Testen, ob Feld gefüllt ist oder nicht
        for child in bezeichnungen_xml_root:
            id_bezeichnung_element = child.find('ID_Bezeichnung')
            if id_bezeichnung_element is not None:
                id_bezeichnung = id_bezeichnung_element.text
            else:
                id_bezeichnung = None

            bezeichnung_element = child.find('Bezeichnung')
            if bezeichnung_element is not None:
                bezeichnung = bezeichnung_element.text
            else:
                bezeichnung = None

            #cursor.execute("ALTER TABLE Ware RENAME COLUMN 'Inventar_x0020_Nr' TO Inventarnr")
            cursor.execute("INSERT INTO Bezeichnungen ('ID_Bezeichnung', Bezeichnung) VALUES (?, ?)", (id_bezeichnung, bezeichnung))
            


            #cursor.execute("PRAGMA table_info('Ware')")
            #print(cursor.fetchall())

        conn.commit()
        conn.close()
