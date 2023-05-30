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

#Benutzername für die Vorgänge 
benutzername = getpass.getuser()

class Ausgabe(tk.Frame):

    def __init__(self, parent, wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn):
        super().__init__(parent)
        self.parent = parent
        self.wareneingang_btn = wareneingang_btn
        self.ausgabe_btn = ausgabe_btn
        self.warenausgang_btn = warenausgang_btn
        self.vorgaenge_btn = vorgaenge_btn
        self.uebersichtMitarbeiter_btn = uebersichtMitarbeiter_btn
        self.uebersichtGeraete_btn = uebersichtGeraete_btn

    def ausgabe(self):
        def toggle_frame():
            ausgabe_frame.destroy()
            self.ausgabe()

        self.ausgabe_btn.configure(command=toggle_frame)

        beschreibung = "Ausgabe"
    
        buttons = [self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn]
        for button in buttons:
            button.state(['!pressed'])
        self.ausgabe_btn.state(['pressed'])

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

        def verwerfen():
            ausgabe_frame.destroy()
            self.ausgabe_btn.configure(state=tk.NORMAL)
            self.ausgabe_btn.state(['!pressed'])
            global value 
            value = 30

        def update_combobox_choices(*args):
                global auswahl_mitarbeiter
                if auswahl_var.get() == "Mitarbeiter":
                    #Abrufen von Daten aus der Mitarbeiter Tabelle
                    cursor.execute('SELECT "Vor-_x0020_Nachname" FROM Mitarbeiter')
                    auswahl_data = cursor.fetchall()
                    #Daten in Mitarbeiter ComboBox einfügen
                    auswahl['values'] = [item[0] for item in auswahl_data]
                    #global mask2_auswahl_mitarbeiter 
                    auswahl_mitarbeiter = 'mitarbeiter'
                    
                elif auswahl_var.get() == "Arbeitsplatz":
                    #Abrufen von Daten aus der Arbeitsplatz Tabelle
                    cursor.execute("SELECT Raum FROM Raum")
                    auswahl_data = cursor.fetchall()
                    #Daten in Raum ComboBox einfügen
                    auswahl['values'] = [item[0] for item in auswahl_data]
                    
                    auswahl_mitarbeiter = 'arbeitsplatz'
                    
        def speichern():
            global inventarnr_entry_string
            global auswahl_string
            auswahl_string = auswahl.get()
            inventarnr_entry_string = inventarnr_entry.get()
            auswahl_mitarbeiter
            #mask2_bezeichnungInputString = mask2_bezeichnungInput.get()
            cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarnr_entry_string,))
            result = cursor.fetchall()
            #print(result)
            #print(mask2_auswahlString)
            if auswahl_string !="None" and auswahl_string !="Mitarbeiter" and auswahl_string !="Arbeitsplatz":
                if result !=[] and len(inventarnr_entry_string) == 6:
                    if auswahl_mitarbeiter == 'mitarbeiter':
                        #print('Mitarbeiter')
                        cursor.execute("UPDATE Ware SET Raum = '' WHERE Inventar_x0020_Nr = ?", (inventarnr_entry_string,)) 
                        cursor.execute("UPDATE Ware SET 'LetzterWertvonWaBewVor-MA_Ausgabe' = ? WHERE Inventar_x0020_Nr = ?", (auswahl_string, inventarnr_entry_string,))
                        cursor.execute("CREATE TEMPORARY TABLE TempTable AS SELECT * FROM Mitarbeiter ORDER BY 'Vor-_x0020_Nachname' ASC")
                        cursor.execute('UPDATE Mitarbeiter SET "Vor-_x0020_Nachname" = (SELECT "Vor-_x0020_Nachname" FROM TempTable WHERE TempTable.rowid = Mitarbeiter.rowid), "MA-Kürzel" = (SELECT "MA-Kürzel" FROM TempTable WHERE TempTable.rowid = Mitarbeiter.rowid), Anmeldename = (SELECT Anmeldename FROM TempTable WHERE TempTable.rowid = Mitarbeiter.rowid)')        
                        cursor.execute("DROP TABLE TempTable")
                        connection.commit()
                    elif auswahl_mitarbeiter == 'arbeitsplatz':
                        cursor.execute("UPDATE Ware SET 'LetzterWertvonWaBewVor-MA_Ausgabe' = '' WHERE Inventar_x0020_Nr = ?", (inventarnr_entry_string,)) 
                        cursor.execute("UPDATE Ware SET Raum = ? WHERE Inventar_x0020_Nr = ?", (auswahl_string, inventarnr_entry_string,))
                        cursor.execute("CREATE TEMPORARY TABLE TempTable AS SELECT * FROM Raum ORDER BY Raum ASC")
                        cursor.execute("UPDATE Raum SET ID_Raum = (SELECT ID_Raum FROM TempTable WHERE TempTable.rowid = Raum.rowid), Raum = (SELECT Raum FROM TempTable WHERE TempTable.rowid = Raum.rowid)")        
                        cursor.execute("DROP TABLE TempTable")

                    cursor.execute("SELECT * FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarnr_entry_string,))
                    result = cursor.fetchall()
                    
                    handle_new_entry()
                    cursor.execute("SELECT MAX(Nummer) FROM Vorgang")
                    test = cursor.fetchone()
                    liste = int(test[0])
                    next_number = liste + 1
                    datum_string = date_entry.get()
                    cursor.execute("INSERT INTO Vorgang (Nummer, 'WaBewVor-Datum', BewArt_KurzBeschreibung, InventarNr, 'WaBewVor-MA_Ausgabe', 'WaBewVor-Benutzer') VALUES(?, ?, ? ,?, ? ,?)", (next_number, datum_string, beschreibung, inventarnr_entry_string, auswahl_string, benutzername,))
                    connection.commit()
                    ausgabe_frame.destroy()
                else:
                    messagebox.showerror("Fehlermeldung", "Dieses Gerät existiert nicht.")
            else:
                messagebox.showerror("Fehlermeldung", "Sie müssen einen Mitarbeiter oder Arbeitsplatz auswählen.")

        def fillout(event):
            if event.keysym == "Return":
                inventarnr_entry_string = inventarnr_entry.get()
                cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarnr_entry_string,))
                result = cursor.fetchall()

                if result == [] or len(inventarnr_entry_string) < 6:
                    bezeichnung_input.configure(text="")
                    status_input.configure(text="")
                    typ_input.configure(text="")
                else:
                    cursor.execute("SELECT Bezeichnung FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarnr_entry_string,))
                    bezeichnung_inhalt = cursor.fetchone()
                    cursor.execute("SELECT Typ FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarnr_entry_string,))
                    typ_inhalt = cursor.fetchone()
                    typ_inhalt_string = typ_inhalt[0]
                    cursor.execute("SELECT Status FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarnr_entry_string,))
                    status_inhalt = cursor.fetchone()
                    bezeichnung_input.configure(text=bezeichnung_inhalt)
                    typ_input.configure(text=typ_inhalt_string)
                    status_input.configure(text=status_inhalt)

        def handle_new_entry():
            new_entry = auswahl.get()
            if auswahl_mitarbeiter == 'mitarbeiter':

                #Überprüfung ob Eintrag bereits in der Datenbank vorhanden ist
                cursor.execute("SELECT 'Vor-_x0020_Nachname' FROM Mitarbeiter WHERE 'Vor-_x0020_Nachname' = ?", (new_entry,))
                existing_entry = cursor.fetchone()

                if (existing_entry):
                    pass
                else:
                    cursor.execute("INSERT INTO Mitarbeiter ('Vor-_x0020_Nachname') VALUES (?)", (new_entry,))
                    connection.commit()

            elif auswahl_mitarbeiter == 'arbeitsplatz':
                #Überprüfung ob Eintrag bereits in der Datenbank vorhanden ist
                cursor.execute("SELECT Raum FROM Raum WHERE Raum = ?", (new_entry,))
                existing_entry = cursor.fetchone()

                if (existing_entry):
                    pass
                else:
                    cursor.execute("INSERT INTO Raum (Raum) VALUES (?)", (new_entry,))
                    connection.commit()
                    
            current_values = auswahl['values']
            updated_values = sorted(current_values + (new_entry,))
            auswahl['values']= updated_values

        auswahl_var = tk.StringVar(value="")
        auswahl_var.set(None)

        ausgabe_frame = tk.Frame(self.parent, bg="white")
        ausgabe_frame.place(x=161, y=1, anchor="nw", height=w, width=l)

        title = tk.Label(ausgabe_frame, fg="black", bg='white', text="Mitarbeiterausgabe", font=('Arial', 14))
        title.place(x=10, y=10)

        date = tk.Label(ausgabe_frame, fg="black", bg='white', text="Datum:", font=('Arial', 12))
        date.place(x=40, y=50)
        date_entry = DateEntry(ausgabe_frame, date_pattern='dd.mm.yyyy', borderwidth=1, relief='solid', locale='de_DE')
        date_entry.place(x=100, y=50)

        mitarbeiter_radiobtn = tk.Radiobutton(ausgabe_frame, text="Mitarbeiter", font=('Arial', 12), bg="white", variable=auswahl_var, value="Mitarbeiter")
        mitarbeiter_radiobtn.place(x=40, y=80)

        arbeitsplatz_radiobtn = tk.Radiobutton(ausgabe_frame, text="Arbeitsplatz", font=('Arial', 12), bg="white", variable=auswahl_var, value="Arbeitsplatz")
        arbeitsplatz_radiobtn.place(x=140, y=80)

        
        auswahl = ttk.Combobox(ausgabe_frame, textvariable=auswahl_var)
        auswahl.place(x=40, y=130)

        auswahl_var.trace_add('write', update_combobox_choices)

        #Bezeichnung ComboBox Änderungsereignis behandeln
        auswahl.bind("<<ComboboxSelected>>")

        device = tk.Label(ausgabe_frame, text="Geräte:", fg="black", bg='white', font=('Arial', 12))
        device.place(x=40, y=170)

        speichern = tk.Button(ausgabe_frame, text="speichern", font=("Arial", 16), command=speichern)
        speichern.place(x=700, y=500)

        verwerfen = tk.Button(ausgabe_frame, text="verwerfen", font=("Arial", 16), command=verwerfen)
        verwerfen.place(x=700, y=10)

        #hinzufügen = tk.Button(ausgabe_frame, text="+", font=('Arial', 16), command=open_new_frame)
        #hinzufügen.place(x=500, y=170, height=30, width=30)

        #Frame zur Wahl von Geräten
        device_frame = tk.Frame(ausgabe_frame, borderwidth=1, relief="solid")
        device_frame.place(width=805, height=120, x=10, y=200)

        tablename_row = tk.Frame(device_frame, borderwidth=1, relief="solid", bg="white")
        tablename_row.place(x=0, y=0, height=30, width=805)

        inventarnr = tk.Label(tablename_row, text="Inventarnr:", fg="black", font=("Arial", 12), bg="white")
        inventarnr.place(x=5, y=0)

        bezeichnung = tk.Label(tablename_row, text="Bezeichnung:", fg="black", font=("Arial", 12), bg="white")
        bezeichnung.place(x=100, y=0)

        typ = tk.Label(tablename_row, text="Typ:", fg="black", font=("Arial", 12), bg="white")
        typ.place(x=250, y=0)

        status = tk.Label(tablename_row, text="Status:", fg="black", font=("Arial", 12), bg="white")
        status.place(x=360, y=0)

        device_input = tk.Frame(device_frame, borderwidth=1, relief="solid")
        device_input.place(x=0, y=30, height=30, width=805)

        #Überprüfen bei Änderungen im Entry-Feld, Schreiben möglich 
        entry_var = tk.StringVar()
        entry_var.trace_add('write', check_entry)

        inventarnr_entry = tk.Entry(device_input, textvariable=entry_var)
        inventarnr_entry.config(validate="key")
        inventarnr_entry.config(validatecommand=(device_input.register(validate_entry), '%P'))
        inventarnr_entry.config(state='normal')
        inventarnr_entry.place(x=5, y=5, width=60)
        inventarnr_entry.bind("<KeyPress>", fillout)

        bezeichnung_input = tk.Label(device_input, text="", bg="white")
        bezeichnung_input.place(x=100, y=5, width=100)

        typ_input = tk.Label(device_input, text="", bg="white")
        typ_input.place(x=220, y=5, width=100, height=20)

        status_input = tk.Label(device_input, text="", bg="white")
        status_input.place(x=340, y=5, width=100, height=20)