import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS Ware')
cursor.execute('CREATE TABLE Ware ("Inventar_x0020_Nr" INT, Bezeichnung TEXT, Typ INT, "Serien-Nr" INT)')

tree = ET.parse('GeraeteListe.xml')

xml_root = tree.getroot()

#Testen, ob Feld gefüllt ist oder nicht
for child in xml_root:
    inventar = child.find('Inventar_x0020_Nr')
    bezeichnung = child.find('Bezeichnung').text
    typ = child.find('Typ')
    seriennr = child.find('Serien-Nr')

for child in xml_root:
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

    
    cursor.execute("INSERT INTO Ware (Inventar_x0020_Nr, Bezeichnung, Typ, 'Serien-Nr') VALUES (?, ?, ?, ?)", (inventar, bezeichnung, typ, seriennr))

cursor.execute("SELECT * FROM Ware")


conn.commit()
conn.close()


