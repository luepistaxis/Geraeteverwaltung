import sqlite3
import xml.etree.ElementTree as ET
import os

class GeraeteListe:

    def __init__(self):
        pass
    
    #-----------
    #Geräteliste 
    #-----------
    def geraeteliste_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\GeraeteListe.xml') 

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        #cursor.execute("DROP TABLE IF EXISTS Ware")
        cursor.execute("CREATE TABLE IF NOT EXISTS Ware ('Inventar_x0020_Nr' INT, Bezeichnung TEXT, Typ INT, 'Serien-Nr' INT)")
        
        geraete_tree = ET.parse(xml_file_path)

        geraete_xml_root = geraete_tree.getroot()

        #Testen, ob Feld gefüllt ist oder nicht
        for child in geraete_xml_root:
            inventar_element = child.find('Inventar_x0020_Nr')
            if inventar_element is not None:
                inventar = inventar_element.text
            else:
                inventar = None

            bezeichnung_element = child.find('Bezeichnung')
            if bezeichnung_element is not None:
                bezeichnung = bezeichnung_element.text
            else:
                bezeichnung = None

            typ_element = child.find('Typ')
            if typ_element is not None:
                typ = typ_element.text
            else:
                typ = None

            seriennr_element = child.find('Serien-Nr')
            if seriennr_element is not None:
                seriennr = seriennr_element.text
            else:
                seriennr = None

            #cursor.execute("ALTER TABLE Ware RENAME COLUMN 'Inventar_x0020_Nr' TO Inventarnr")
            cursor.execute("INSERT INTO Ware ('Inventar_x0020_Nr', Bezeichnung, Typ, 'Serien-Nr') VALUES (?, ?, ?, ?)", (inventar, bezeichnung, typ, seriennr))
            


            #cursor.execute("PRAGMA table_info('Ware')")
            #print(cursor.fetchall())

        conn.commit()
        conn.close()


