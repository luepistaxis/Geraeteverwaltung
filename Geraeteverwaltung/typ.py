import sqlite3
import xml.etree.ElementTree as ET
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
        xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\Typ.xml')  

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        #cursor.execute("DROP TABLE IF EXISTS Typ")
        cursor.execute("CREATE TABLE IF NOT EXISTS Typ ('ID_Typ' INT, Bezeichnung TEXT)")
        
        typ_tree = ET.parse(xml_file_path)

        typ_xml_root = typ_tree.getroot()

        #Testen, ob Feld gefüllt ist oder nicht
        for child in typ_xml_root:
            id_typ_element = child.find('ID_Typ')
            if id_typ_element is not None:
                id_typ = id_typ_element.text
            else:
                id_typ = None

            bezeichnung_element = child.find('Bezeichnung')
            if bezeichnung_element is not None:
                bezeichnung = bezeichnung_element.text
            else:
                bezeichnung = None

            #cursor.execute("ALTER TABLE Ware RENAME COLUMN 'Inventar_x0020_Nr' TO Inventarnr")
            cursor.execute("INSERT INTO Typ ('ID_Typ', Bezeichnung) VALUES (?, ?)", (id_typ, bezeichnung))
            


            #cursor.execute("PRAGMA table_info('Typ')")
            #print(cursor.fetchall())

        conn.commit()
        conn.close()