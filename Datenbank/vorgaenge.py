import sqlite3
import xml.etree.ElementTree as ET
import os

class Vorgaenge:

    def __init__(self):
        pass

    def vorgaenge_methode(self):
         # Den absoluten Pfad zum aktuellen Skript erhalten
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Datenbankpfad erstellen
        db_path = os.path.join(script_dir, 'database.db')
        #xml_file_path = os.path.join(script_dir, 'C:\\Users\\luisa.aslanidis\\VisualProjekte\\Test1\\Datenbank\\Eigentümer.xml') 

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS Vorgaenge")

        create_table_query = '''CREATE TABLE IF NOT EXISTS Vorgaenge (Nummer INTEGER NOT NULL, Datum TEXT, Beschreibung TEXT, InventarNr INTEGER, ausgegeben_an TEXT, bearbeitet_durch TEXT NOT NULL)'''
        cursor.execute(create_table_query)


        create_date = '''INSERT INTO Vorgaenge (Nummer, Datum, Beschreibung, InventarNr, ausgegeben_an, bearbeitet_durch) SELECT Vorgang.Nummer, Vorgang.Datum, Vorgang.Beschreibung, Ware.Inventar_x0020_Nr AS InventarNr, Vorgang.ausgegeben_an, Vorgang.bearbeitet_durch FROM Vorgang INNER JOIN Vorgang_erweitert ON Vorgang.Nummer = Vorgang_erweitert.Nummer RIGHT JOIN Ware ON Ware."ID-Ware" = Vorgang_erweitert.InventarNr ORDER BY Vorgang.Nummer DESC;'''
        cursor.execute(create_date)

        conn.commit()
        conn.close()