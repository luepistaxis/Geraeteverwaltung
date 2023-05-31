import sqlite3
import tkinter as tk
import getpass
import os
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry

# Datenbank Verbindung
gui_folder = os.path.dirname(os.path.abspath(__file__))
#database_path = "K:\\IT-Assistenz\\Geräteverwaltung\\Geraeteverwaltung\\Geraeteverwaltung\\database.db"
database_path = os.path.join(gui_folder, "..", "Datenbank", "database.db")
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

#Länge und Breite der Frames
l = 1280
w = 720

class Wareneingang(tk.Frame):
    def __init__(self, parent, wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn):
        super().__init__(parent)
        self.parent = parent
        self.wareneingang_btn = wareneingang_btn
        self.ausgabe_btn = ausgabe_btn
        self.warenausgang_btn = warenausgang_btn
        self.vorgaenge_btn = vorgaenge_btn
        self.uebersichtMitarbeiter_btn = uebersichtMitarbeiter_btn
        self.uebersichtGeraete_btn = uebersichtGeraete_btn
        #Benutzername für die Vorgänge 
        self.benutzername = getpass.getuser()
        
    def open_wareneingang(self):
        self.beschreibung = "Lagereingang"
        def toggle_frame():
            wareneingang_frame.destroy()
            self.open_wareneingang()

        self.wareneingang_btn.configure(command=toggle_frame)

        buttons = [self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn]
        for button in buttons:
            button.state(['!pressed'])
        self.wareneingang_btn.state(['pressed'])

        #Funktion Max Länge für Entry
        def validate_entry(char):
            if len(char) > 6 :
                return False
            return True
        
        #Funktion zum Eingabe überprüfen
        def check_entry(*args):
            char = inventarnr_entry.get()
            if len(char) >= 6:
                inventarnr_entry.config(state='readonly')
            else:
                inventarnr_entry.config(state='normal')

        def handle_new_entry():
            #if event.keysym == "Return":
            new_entry = typ_combo_var.get()
                #if new_entry:
    
            cursor.execute("SELECT MAX(ID_Typ) FROM Typ")
            max_id = cursor.fetchone()[0]

            new_id = max_id + 1 if max_id is not None else 1

            #Überprüfung ob Eintrag bereits in der Datenbank vorhanden ist
            cursor.execute("SELECT Bezeichnung FROM Typ WHERE Bezeichnung = ?", (new_entry,))
            existing_entry = cursor.fetchone()

            if (existing_entry):
                pass
            else:
                cursor.execute("INSERT INTO Typ (ID_Typ, Bezeichnung) VALUES (?, ?)", (new_id, new_entry,))
                connection.commit()

        def verwerfen():
            wareneingang_frame.destroy()
            self.wareneingang_btn.configure(state=tk.NORMAL)
            self.wareneingang_btn.state(['!pressed'])
            #global mask1_value 
            #mask1_value = 120

        def speichern():
            inventar_string = inventarnr_entry.get()
            bezeichnung_string = bezeichnung_combobox.get()
            typ_string = typ_combobox.get()
            eigentuemer_string = eigentuemer_combobox.get()
            raum_string = raum_combobox.get()
            seriennr_string = seriennr_entry.get()
            weitere_string = weiterenr_entry.get()
            preis_string = preis_entry.get()

            cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (inventar_string,))
            result = cursor.fetchall()
            if result == [] and len(inventar_string) == 6:
                if inventar_string == "" or bezeichnung_string == "" or typ_string == "" or eigentuemer_string == "" or raum_string == "":
                    messagebox.showerror("Fehlermeldung", "Nicht alle Pflichtfelder wurden ausgefüllt.\nAchten Sie darauf, dass alle Pflichtfelder ausgefüllt sind.")
                    return
                cursor.execute("INSERT INTO Ware ('Inventar_x0020_Nr', Bezeichnung, Typ, 'Serien-Nr', Andere_x0020_Nummer, 'Eigentümer', Raum, 'LetzterWertvonWaBewVor-MA_Ausgabe', Status, 'Netto_x0020_Einkaufspreis') VALUES (?, ?, ?, ?, ?, ?, ?, '', 'Freigegeben', ?)", (inventar_string, bezeichnung_string, typ_string, seriennr_string, weitere_string, eigentuemer_string, raum_string, preis_string))
                cursor.execute("CREATE TEMPORARY TABLE TempTable AS SELECT * FROM Ware ORDER BY Inventar_x0020_Nr ASC")
                cursor.execute('UPDATE Ware SET Inventar_x0020_Nr = (SELECT Inventar_x0020_Nr FROM TempTable WHERE TempTable.rowid = Ware.rowid), Bezeichnung = (SELECT Bezeichnung FROM TempTable WHERE TempTable.rowid = Ware.rowid), Typ = (SELECT Typ FROM TempTable WHERE TempTable.rowid = Ware.rowid), "Serien-Nr" = (SELECT "Serien-Nr" FROM TempTable WHERE TempTable.rowid = Ware.rowid), Eigentümer = (SELECT Eigentümer FROM TempTable WHERE TempTable.rowid = Ware.rowid), Raum = (SELECT Raum FROM TempTable WHERE TempTable.rowid = Ware.rowid), "LetzterWertvonWaBewVor-MA_Ausgabe" = (SELECT "LetzterWertvonWaBewVor-MA_Ausgabe" FROM TempTable WHERE TempTable.rowid = Ware.rowid), Status = (SELECT Status FROM TempTable WHERE TempTable.rowid = Ware.rowid), Netto_x0020_Einkaufspreis = (SELECT Netto_x0020_Einkaufspreis FROM TempTable WHERE TempTable.rowid = Ware.rowid)')        
                cursor.execute("DROP TABLE TempTable")
                handle_new_entry()
                cursor.execute("SELECT * FROM Ware WHERE Inventar_x0020_Nr = ?", (inventar_string,))
                result = cursor.fetchall()
                cursor.execute("SELECT MAX(Nummer) FROM Vorgang")
                test = cursor.fetchone()
                print(test)
                liste = int(test[0])
                print(liste)
                next_number = liste + 1
                datum_string = date_entry.get()
                cursor.execute("INSERT INTO Vorgaenge (Nummer, Datum, Beschreibung, InventarNr, ausgegeben_an, bearbeitet_durch) VALUES(?, ?, ? ,?, ?, ?)", (next_number, datum_string, self.beschreibung, inventar_string, "" ,self.benutzername,))
                test14 = cursor.fetchall()
                print(test14)
                connection.commit()
                wareneingang_frame.destroy()
                #self.warenausgang_btn.config(state="normal")
                messagebox.showinfo("", "Erfolgreich hinzugefügt!")
                self.open_wareneingang()

            elif len(inventar_string) < 6:
                messagebox.showerror("Fehlermeldung", "Die Inventar Nr ist zu kurz\nBitte gib eine 6-stellige Zahl ein.")
            else:
                messagebox.showerror("Fehlermeldung", "Gerät existiert schon!")
            
        wareneingang_frame = tk.Frame(self.parent, bg="white")
        wareneingang_frame.place(x=161, y=1, anchor="nw", height=w, width=l)

        title = tk.Label(wareneingang_frame, fg="black", bg='white', text="Warenaufnahme", font=('Arial', 14))
        title.place(x=10, y=10)

        date = tk.Label(wareneingang_frame, fg="black", bg='white', text="Datum:", font=('Arial', 12))
        date.place(x=40, y=50)
        date_entry = DateEntry(wareneingang_frame, date_pattern='dd.mm.yyyy', borderwidth=1, relief='solid', locale='de_DE')
        date_entry.place(x=100, y=50)
        device = tk.Label(wareneingang_frame, text="Geräte:", fg="black", bg='white', font=('Arial', 12))
        device.place(x=40, y=90)

        #hinzufügen = tk.Button(mask1_frame, text="+", font=('Arial', 16), command=open_new_frame)
        #hinzufügen.place(x=500, y=90, height=30, width=30)

        speichern = tk.Button(wareneingang_frame, text="speichern", font=("Arial", 16), command=speichern)
        speichern.place(x=700, y=500)

        verwerfen = tk.Button(wareneingang_frame, text="verwerfen", font=("Arial", 16), command=verwerfen)
        verwerfen.place(x=700, y=10)

        #Frame zum Eingeben der Geräte Informationen
        device_frame = tk.Frame(wareneingang_frame, borderwidth=1, relief="solid")
        device_frame.place(width=805, height=120, x=10, y=120)

        inventarnr = tk.Label(device_frame, text="Inventar Nr.:", fg="black", font=('Arial', 12))
        inventarnr.place(x=30, y=10)

        #Überprüfen bei Änderungen im Entry-Feld, Schreiben möglich 
        entry_var = tk.StringVar()
        entry_var.trace_add('write', check_entry)

        inventarnr_entry = tk.Entry(device_frame, textvariable=entry_var)
        inventarnr_entry.config(validate="key")
        inventarnr_entry.config(validatecommand=(device_frame.register(validate_entry), '%P'))
        inventarnr_entry.config(state='normal')
        inventarnr_entry.place(x=120, y=10)

        bezeichnung = tk.Label(device_frame, text="Bezeichnung:", fg="black", font=('Arial', 12))
        bezeichnung.place(x=19, y=35)

        bezeichnung_combo_var = tk.StringVar()
        bezeichnung_combobox = ttk.Combobox(device_frame, textvariable=bezeichnung_combo_var)
        bezeichnung_combobox.place(x=120, y=35)

        #Abrufen von Daten aus der Bezeichnungen Tabelle
        cursor.execute("SELECT Bezeichnung FROM Bezeichnungen")
        bezeichnung_data = cursor.fetchall()

        #Daten in Bezeichnung ComboBox einfügen
        bezeichnung_combobox['values'] = [item[0] for item in bezeichnung_data]
        #Bezeichnung ComboBox Änderungsereignis behandeln
        bezeichnung_combobox.bind("<<ComboboxSelected>>")

        typ = tk.Label(device_frame, text="Typ:", fg="black", font=('Arial', 12))
        typ.place(x=83, y=60)

        typ_combo_var = tk.StringVar()
        typ_combobox = ttk.Combobox(device_frame, textvariable=typ_combo_var)
        typ_combobox.place(x=120, y=60)

        #Abrufen von Daten aus der Typ Tabelle
        cursor.execute("SELECT Bezeichnung FROM Typ")
        typ_data = cursor.fetchall()

        #Daten in Typ ComboBox einfügen
        typ_combobox['values'] = [item[0] for item in typ_data]
        #Typ ComboBox Änderungsereignis behandeln
        typ_combobox.bind("<<ComboboxSelected>>")

        eigentuemer = tk.Label(device_frame, text="Eigentümer:", fg="black", font=('Arial', 12))
        eigentuemer.place(x=29, y=85)
        
        eigentuemer_combo_var = tk.StringVar()
        eigentuemer_combobox = ttk.Combobox(device_frame, textvariable=eigentuemer_combo_var)
        eigentuemer_combobox.place(x=120, y=85)

        cursor.execute("SELECT Eigentümer FROM Eigentuemer")
        eigentuemer_data = cursor.fetchall()

        eigentuemer_combobox['values'] = [item[0] for item in eigentuemer_data]

        eigentuemer_combobox.bind("<<ComboboxSelected>>")
        
        raum = tk.Label(device_frame, text="Raum:", fg="black", font=('Arial', 12))
        raum.place(x=337, y=10)
        cursor.execute("SELECT Raum FROM Raum ORDER BY ID_Raum LIMIT 1")
        default_value = cursor.fetchone()[0]
        raum_combo_var = tk.StringVar(value=default_value)
        raum_combobox = ttk.Combobox(device_frame, textvariable=raum_combo_var)
        raum_combobox.place(x=390, y=10)

        cursor.execute("SELECT Raum FROM Raum")
        raum_data = cursor.fetchall()

        raum_combobox['values'] = [item[0] for item in raum_data]

        raum_combobox.bind("<<ComboboxSelected>>")

        seriennr = tk.Label(device_frame, text="Seriennr.:", fg="black", font=('Arial', 12))
        seriennr.place(x=315, y=35)
        seriennr_entry = tk.Entry(device_frame) 
        seriennr_entry.place(x=390, y=35)

        weiterenr = tk.Label(device_frame, text="Weitere:", fg="black", font=('Arial', 12))
        weiterenr.place(x=323, y=60)
        weiterenr_entry = tk.Entry(device_frame) 
        weiterenr_entry.place(x=390, y=60)

        preis = tk.Label(device_frame, text="Einkaufspreis:", fg="black", font=('Arial', 12))
        preis.place(x=282, y=85)
        preis_entry = tk.Entry(device_frame) 
        preis_entry.place(x=390, y=85)