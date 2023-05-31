import sqlite3
import xml.etree.ElementTree as ET
import os

class Vorgang_erweitert:

    def __init__(self):
        pass
    
    #-----------
    #Vorgangliste 
    #-----------
    def vorgang_erweitert_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Test1\\Datenbank\\Vorgang_erweitert.xml')  

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        cursor.execute("DROP TABLE IF EXISTS Vorgang_erweitert")
        cursor.execute("CREATE TABLE IF NOT EXISTS Vorgang_erweitert (InventarNr TEXT, Nummer INT)")
        
        
        Vorgang_tree = ET.parse(xml_file_path)

        Vorgang_xml_root = Vorgang_tree.getroot()

        #Testen, ob Feld gefüllt ist oder nicht
        for child in Vorgang_xml_root:
            inventarnr_element = child.find('InventarNr')
            
            if inventarnr_element is not None:
                inventarnr = inventarnr_element.text
            else:
                inventarnr = ""

            nummer_element = child.find('Nummer')
            
            if nummer_element is not None:
                nummer = nummer_element.text
            else:
                nummer = ""


            #cursor.execute("ALTER TABLE Ware RENAME COLUMN 'Inventar_x0020_Nr' TO Inventarnr")
            cursor.execute("INSERT INTO Vorgang_erweitert (InventarNr, Nummer) VALUES (?, ?)", (inventarnr, nummer))
            


            #cursor.execute("PRAGMA table_info('Ware')")
            #print(cursor.fetchall())

        conn.commit()
        conn.close()
