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
        beschreibung = "Lagereingang"
        def toggle_frame():
            mask1_frame.destroy()
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
            char = mask1_inventar_NrEntry.get()
            if len(char) >= 6:
                mask1_inventar_NrEntry.config(state='readonly')
            else:
                mask1_inventar_NrEntry.config(state='normal')

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
            mask1_frame.destroy()
            self.wareneingang_btn.configure(state=tk.NORMAL)
            self.wareneingang_btn.state(['!pressed'])
            #global mask1_value 
            #mask1_value = 120

        def speichern():
            inventarString = mask1_inventar_NrEntry.get()
            bezeichnungString = mask1_bezeichnungComboBox.get()
            typString = mask1_typCombobox.get()
            eigentuemerString = mask1_eigentuemerComboBox.get()
            raumString = mask1_raumCombobox.get()
            seriennrString = mask1_seriennrEntry.get()
            weitereString = mask1_weiterenrEntry.get()
            preisString = mask1_preisEntry.get()

            cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarString,))
            result = cursor.fetchall()
            if result == [] and len(inventarString) == 6:
            
                if inventarString == "" or bezeichnungString == "" or typString == "" or eigentuemerString == "" or raumString == "":
                    messagebox.showerror("Fehlermeldung", "Nicht alle Pflichtfelder wurden ausgefüllt.\nAchten Sie darauf, dass alle Pflichtfelder ausgefüllt sind.")
                    return
                cursor.execute("INSERT INTO Ware ('Inventar_x0020_Nr', Bezeichnung, Typ, 'Serien-Nr', Andere_x0020_Nummer, 'Eigentümer', Raum, 'LetzterWertvonWaBewVor-MA_Ausgabe', Status, 'Netto_x0020_Einkaufspreis') VALUES (?, ?, ?, ?, ?, ?, ?, '', 'Freigegeben', ?)", (inventarString, bezeichnungString, typString, seriennrString, weitereString, eigentuemerString, raumString, preisString))
                cursor.execute("CREATE TEMPORARY TABLE TempTable AS SELECT * FROM Ware ORDER BY Inventar_x0020_Nr ASC")
                cursor.execute('UPDATE Ware SET Inventar_x0020_Nr = (SELECT Inventar_x0020_Nr FROM TempTable WHERE TempTable.rowid = Ware.rowid), Bezeichnung = (SELECT Bezeichnung FROM TempTable WHERE TempTable.rowid = Ware.rowid), Typ = (SELECT Typ FROM TempTable WHERE TempTable.rowid = Ware.rowid), "Serien-Nr" = (SELECT "Serien-Nr" FROM TempTable WHERE TempTable.rowid = Ware.rowid), Eigentümer = (SELECT Eigentümer FROM TempTable WHERE TempTable.rowid = Ware.rowid), Raum = (SELECT Raum FROM TempTable WHERE TempTable.rowid = Ware.rowid), "LetzterWertvonWaBewVor-MA_Ausgabe" = (SELECT "LetzterWertvonWaBewVor-MA_Ausgabe" FROM TempTable WHERE TempTable.rowid = Ware.rowid), Status = (SELECT Status FROM TempTable WHERE TempTable.rowid = Ware.rowid), Netto_x0020_Einkaufspreis = (SELECT Netto_x0020_Einkaufspreis FROM TempTable WHERE TempTable.rowid = Ware.rowid)')        
                cursor.execute("DROP TABLE TempTable")
                handle_new_entry()
                cursor.execute("SELECT * FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarString,))
                result = cursor.fetchall()
                cursor.execute("SELECT MAX(Nummer) FROM Vorgang")
                test = cursor.fetchone()
                liste = int(test[0])
                bla = liste + 1
                datumString = mask1_dateEntry.get()
                cursor.execute("INSERT INTO Vorgang (Nummer, 'WaBewVor-Datum', BewArt_KurzBeschreibung, InventarNr, 'WaBewVor-MA_Ausgabe', 'WaBewVor-Benutzer') VALUES(?, ?, ? ,?, ?, ?)", (bla, datumString, beschreibung, inventarString, "" ,self.benutzername,))
                connection.commit()
                mask1_frame.destroy()
                #self.warenausgang_btn.config(state="normal")
                messagebox.showinfo("", "Erfolgreich hinzugefügt!")
                self.open_wareneingang()

            elif len(inventarString) < 6:
                messagebox.showerror("Fehlermeldung", "Die Inventar Nr ist zu kurz\nBitte gib eine 6-stellige Zahl ein.")
            else:
                messagebox.showerror("Fehlermeldung", "Gerät existiert schon!")
            
        mask1_frame = tk.Frame(self.parent, bg="white")
        mask1_frame.place(x=161, y=1, anchor="nw", height=w, width=l)

        mask1_title = tk.Label(mask1_frame, fg="black", bg='white', text="Warenaufnahme", font=('Arial', 14))
        mask1_title.place(x=10, y=10)

        mask1_date = tk.Label(mask1_frame, fg="black", bg='white', text="Datum:", font=('Arial', 12))
        mask1_date.place(x=40, y=50)
        mask1_dateEntry = DateEntry(mask1_frame, date_pattern='dd.mm.yyyy', borderwidth=1, relief='solid', locale='de_DE')
        mask1_dateEntry.place(x=100, y=50)
        mask1_device = tk.Label(mask1_frame, text="Geräte:", fg="black", bg='white', font=('Arial', 12))
        mask1_device.place(x=40, y=90)

        #mask1_hinzufügen = tk.Button(mask1_frame, text="+", font=('Arial', 16), command=open_new_frame)
        #mask1_hinzufügen.place(x=500, y=90, height=30, width=30)

        mask1_speichern = tk.Button(mask1_frame, text="speichern", font=("Arial", 16), command=speichern)
        mask1_speichern.place(x=700, y=500)

        mask1_verwerfen = tk.Button(mask1_frame, text="verwerfen", font=("Arial", 16), command=verwerfen)
        mask1_verwerfen.place(x=700, y=10)

        #Frame zum Eingeben der Geräte Informationen
        mask1_deviceFrame = tk.Frame(mask1_frame, borderwidth=1, relief="solid")
        mask1_deviceFrame.place(width=805, height=120, x=10, y=120)

        mask1_inventar_Nr = tk.Label(mask1_deviceFrame, text="Inventar Nr.:", fg="black", font=('Arial', 12))
        mask1_inventar_Nr.place(x=30, y=10)

        #Überprüfen bei Änderungen im Entry-Feld, Schreiben möglich 
        entry_var = tk.StringVar()
        entry_var.trace_add('write', check_entry)

        mask1_inventar_NrEntry = tk.Entry(mask1_deviceFrame, textvariable=entry_var)
        mask1_inventar_NrEntry.config(validate="key")
        mask1_inventar_NrEntry.config(validatecommand=(mask1_deviceFrame.register(validate_entry), '%P'))
        mask1_inventar_NrEntry.config(state='normal')
        mask1_inventar_NrEntry.place(x=120, y=10)

        mask1_bezeichnung = tk.Label(mask1_deviceFrame, text="Bezeichnung:", fg="black", font=('Arial', 12))
        mask1_bezeichnung.place(x=19, y=35)

        bezeichnung_combo_var = tk.StringVar()
        mask1_bezeichnungComboBox = ttk.Combobox(mask1_deviceFrame, textvariable=bezeichnung_combo_var)
        mask1_bezeichnungComboBox.place(x=120, y=35)

        #Abrufen von Daten aus der Bezeichnungen Tabelle
        cursor.execute("SELECT Bezeichnung FROM Bezeichnungen")
        bezeichnung_data = cursor.fetchall()

        #Daten in Bezeichnung ComboBox einfügen
        mask1_bezeichnungComboBox['values'] = [item[0] for item in bezeichnung_data]
        #Bezeichnung ComboBox Änderungsereignis behandeln
        mask1_bezeichnungComboBox.bind("<<ComboboxSelected>>")

        mask1_typ = tk.Label(mask1_deviceFrame, text="Typ:", fg="black", font=('Arial', 12))
        mask1_typ.place(x=83, y=60)

        typ_combo_var = tk.StringVar()
        mask1_typCombobox = ttk.Combobox(mask1_deviceFrame, textvariable=typ_combo_var)
        mask1_typCombobox.place(x=120, y=60)

        #Abrufen von Daten aus der Typ Tabelle
        cursor.execute("SELECT Bezeichnung FROM Typ")
        typ_data = cursor.fetchall()

        #Daten in Typ ComboBox einfügen
        mask1_typCombobox['values'] = [item[0] for item in typ_data]
        #Typ ComboBox Änderungsereignis behandeln
        mask1_typCombobox.bind("<<ComboboxSelected>>")

        mask1_eigentuemer = tk.Label(mask1_deviceFrame, text="Eigentümer:", fg="black", font=('Arial', 12))
        mask1_eigentuemer.place(x=29, y=85)
        
        eigentuemer_combo_var = tk.StringVar()
        mask1_eigentuemerComboBox = ttk.Combobox(mask1_deviceFrame, textvariable=eigentuemer_combo_var)
        mask1_eigentuemerComboBox.place(x=120, y=85)

        cursor.execute("SELECT Eigentümer FROM Eigentuemer")
        eigentuemer_data = cursor.fetchall()

        mask1_eigentuemerComboBox['values'] = [item[0] for item in eigentuemer_data]

        mask1_eigentuemerComboBox.bind("<<ComboboxSelected>>")
        
        mask1_raum = tk.Label(mask1_deviceFrame, text="Raum:", fg="black", font=('Arial', 12))
        mask1_raum.place(x=337, y=10)
        cursor.execute("SELECT Raum FROM Raum ORDER BY ID_Raum LIMIT 1")
        default_value = cursor.fetchone()[0]
        raum_combo_var = tk.StringVar(value=default_value)
        mask1_raumCombobox = ttk.Combobox(mask1_deviceFrame, textvariable=raum_combo_var)
        mask1_raumCombobox.place(x=390, y=10)

        cursor.execute("SELECT Raum FROM Raum")
        raum_data = cursor.fetchall()

        mask1_raumCombobox['values'] = [item[0] for item in raum_data]

        mask1_raumCombobox.bind("<<ComboboxSelected>>")

        mask1_seriennr = tk.Label(mask1_deviceFrame, text="Seriennr.:", fg="black", font=('Arial', 12))
        mask1_seriennr.place(x=315, y=35)
        mask1_seriennrEntry = tk.Entry(mask1_deviceFrame) 
        mask1_seriennrEntry.place(x=390, y=35)

        mask1_weiterenr = tk.Label(mask1_deviceFrame, text="Weitere:", fg="black", font=('Arial', 12))
        mask1_weiterenr.place(x=323, y=60)
        mask1_weiterenrEntry = tk.Entry(mask1_deviceFrame) 
        mask1_weiterenrEntry.place(x=390, y=60)

        mask1_preis = tk.Label(mask1_deviceFrame, text="Einkaufspreis:", fg="black", font=('Arial', 12))
        mask1_preis.place(x=282, y=85)
        mask1_preisEntry = tk.Entry(mask1_deviceFrame) 
        mask1_preisEntry.place(x=390, y=85)