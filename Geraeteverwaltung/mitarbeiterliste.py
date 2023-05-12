import sqlite3
import xml.etree.ElementTree as ET
import os


class MitarbeiterListe:

    def __init__(self):
        pass

    def mitarbeiterliste_methode(self):

        # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\MitarbeiterListe.xml') 

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute('DROP TABLE IF EXISTS Mitarbeiter')
        cursor.execute('CREATE TABLE IF NOT EXISTS Mitarbeiter ("Vor-_x0020_Nachname" TEXT, "MA-Kürzel" TEXT, Anmeldename TEXT)')

        #mitarbeiter_tree = ET.parse('MitarbeiterListe.xml')
        mitarbeiter_tree = ET.parse(xml_file_path)

        mitarbeiter_xml_root = mitarbeiter_tree.getroot()

        #Testen, ob Feld gefüllt ist oder nicht
        for child in mitarbeiter_xml_root:
            name_element = child.find('Vor-_x0020_Nachname')
            if name_element is not None:
                name = name_element.text
            else:
                name = None

            ma_kuerzel_element = child.find('MA-Kürzel')
            if ma_kuerzel_element is not None:
                ma_kuerzel = ma_kuerzel_element.text
            else:
                ma_kuerzel = None

            anmeldename_element = child.find('Anmeldename')
            if anmeldename_element is not None:
                anmeldename = anmeldename_element.text
            else:
                anmeldename = None

            cursor.execute("INSERT INTO Mitarbeiter ('Vor-_x0020_Nachname', 'MA-Kürzel', Anmeldename) VALUES (?, ?, ?)", (name, ma_kuerzel, anmeldename))

        conn.commit()
        conn.close()