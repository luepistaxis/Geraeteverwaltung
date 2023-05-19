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
        xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\GeraeteAktuell.xml') 

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()


        cursor.execute("DROP TABLE IF EXISTS Ware")
        cursor.execute("CREATE TABLE IF NOT EXISTS Ware ('Inventar_x0020_Nr' INT, Bezeichnung TEXT, Typ INT, 'Serien-Nr' TEXT, Andere_x0020_Nummer TEXT, 'Eigentümer' TEXT, Raum TEXT, 'LetzterWertvonWaBewVor-MA_Ausgabe' TEXT, Status TEXT, 'Netto_x0020_Einkaufspreis')")
        
        geraete_tree = ET.parse(xml_file_path)

        geraete_xml_root = geraete_tree.getroot()

        #Testen, ob Feld gefüllt ist oder nicht
        for child in geraete_xml_root:
            inventar_element = child.find('Inventar_x0020_Nr')
            if inventar_element is not None:
                inventar = inventar_element.text
            else:
                inventar = ""

            bezeichnung_element = child.find('Bezeichnung')
            if bezeichnung_element is not None:
                bezeichnung = bezeichnung_element.text
            else:
                bezeichnung = ""

            typ_element = child.find('Typ')
            if typ_element is not None:
                typ = typ_element.text
            else:
                typ = ""

            seriennr_element = child.find('Serien-Nr')
            if seriennr_element is not None:
                seriennr = seriennr_element.text
            else:
                seriennr = ""

            weitere_element = child.find('Andere_x0020_Nummer')
            if weitere_element is not None:
                weitere = weitere_element.text
            else:
                weitere = ""

            eigentuemer_element = child.find('Eigentümer')
            if eigentuemer_element is not None:
                eigentuemer = eigentuemer_element.text
            else:
                eigentuemer = ""

            raum_element = child.find('Raum')
            if raum_element is not None:
                raum = raum_element.text
            else:
                raum = ""

            mitarbeiter_element = child.find('LetzterWertvonWaBewVor-MA_Ausgabe')
            if mitarbeiter_element is not None:
                mitarbeiter = mitarbeiter_element.text
            else:
                mitarbeiter = ""

            status_element = child.find('Status')
            if status_element is not None:
                status = status_element.text
            else:
                status = ""

            preis_element = child.find('Netto_x0020_Einkaufspreis')
            if preis_element is not None:
                preis = preis_element.text
            else:
                preis = ""

            #cursor.execute("ALTER TABLE Ware RENAME COLUMN 'Inventar_x0020_Nr' TO Inventarnr")
            cursor.execute("INSERT INTO Ware ('Inventar_x0020_Nr', Bezeichnung, Typ, 'Serien-Nr', Andere_x0020_Nummer, 'Eigentümer', Raum, 'LetzterWertvonWaBewVor-MA_Ausgabe', Status, 'Netto_x0020_Einkaufspreis') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (inventar, bezeichnung, typ, seriennr, weitere, eigentuemer, raum, mitarbeiter, status, preis))
            


            #cursor.execute("PRAGMA table_info('Ware')")
            #print(cursor.fetchall())



        conn.commit()
        conn.close()


