import sqlite3
import xml.etree.ElementTree as ET
import os

class Vorgang:

    def __init__(self):
        pass
    
    #-----------
    #Vorgangliste 
    #-----------
    def vorgang_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\Vorgaenge1.xml')  

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        cursor.execute("DROP TABLE IF EXISTS Vorgang")
        cursor.execute("CREATE TABLE IF NOT EXISTS Vorgang (Nummer INT, 'WaBewVor-Datum' TEXT, BewArt_KurzBeschreibung TEXT, InventarNr TEXT, 'WaBewVor-MA_Ausgabe' TEXT, 'WaBewVor-Benutzer' TEXT)")
        
        Vorgang_tree = ET.parse(xml_file_path)

        Vorgang_xml_root = Vorgang_tree.getroot()

        #Testen, ob Feld gefüllt ist oder nicht
        for child in Vorgang_xml_root:
            nummer_element = child.find('Nummer')
            
            if nummer_element is not None:
                nummer = nummer_element.text
            else:
                nummer = ""

            datum_element = child.find('WaBewVor-Datum')
            if datum_element is not None:
                datum = datum_element.text
            else:
                datum = ""

            vorgang_element = child.find('BewArt_KurzBeschreibung')
            if vorgang_element is not None:
                vorgang = vorgang_element.text
            else:
                vorgang = ""

            inventarnr_element = child.find('Inventarnr')
            if inventarnr_element is not None:
                inventarnr = inventarnr_element.text
            else:
                inventarnr = ""

            ausgabe_element = child.find('WaBewVor-MA_Ausgabe')
            if ausgabe_element is not None:
                ausgabe = ausgabe_element.text
            else:
                ausgabe = ""

            bearbeitet_element = child.find('WaBewVor-Benutzer')
            if bearbeitet_element is not None:
                bearbeitet = bearbeitet_element.text
            else:
                bearbeitet = ""

            

            #cursor.execute("ALTER TABLE Ware RENAME COLUMN 'Inventar_x0020_Nr' TO Inventarnr")
            cursor.execute("INSERT INTO Vorgang (Nummer, 'WaBewVor-Datum', BewArt_KurzBeschreibung, InventarNr, 'WaBewVor-MA_Ausgabe', 'WaBewVor-Benutzer') VALUES (?, ?, ? ,?, ? ,?)", (nummer, datum, vorgang, inventarnr, ausgabe, bearbeitet))
            


            #cursor.execute("PRAGMA table_info('Ware')")
            #print(cursor.fetchall())

        conn.commit()
        conn.close()
