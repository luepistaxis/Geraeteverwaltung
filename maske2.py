import sqlite3
import locale
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedStyle
from tkcalendar import DateEntry
import getpass

#SQLite Datenbank Verbindung
db_filename = 'database.db'
#database_path = "K:\\IT-Assistenz\\Geräteverwaltung\\Geraeteverwaltung\\Geraeteverwaltung\\database.db"
database_path = "C:\\Users\\luisa.aslanidis\\VisualProjekte\\Test1\\Datenbank\\database.db"
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

#Länge und Breite der Frames
l = 1280
w = 720

#Benutzername für die Vorgänge 
benutzername = getpass.getuser()

class Maske2(tk.Frame):

    def __init__(self, parent, wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn):
        super().__init__(parent)
        self.parent = parent
        self.wareneingang_btn = wareneingang_btn
        self.ausgabe_btn = ausgabe_btn
        self.warenausgang_btn = warenausgang_btn
        self.vorgaenge_btn = vorgaenge_btn
        self.uebersichtMitarbeiter_btn = uebersichtMitarbeiter_btn
        self.uebersichtGeraete_btn = uebersichtGeraete_btn

    def open_ausgabe(self):
        def toggle_frame():
            mask2_frame.destroy()
            self.open_ausgabe()

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
            char = mask2_inventar_NrEntry.get()
            if len(char) >= 6:
                mask2_inventar_NrEntry.config(state='readonly')
            else:
                mask2_inventar_NrEntry.config(state='normal')

        def verwerfen():
            mask2_frame.destroy()
            self.ausgabe_btn.configure(state=tk.NORMAL)
            self.ausgabe_btn.state(['!pressed'])
            global mask2_value 
            mask2_value = 30

        def update_combobox_choices(*args):
                global mask2_auswahl_mitarbeiter
                if mask2_auswahl_var.get() == "Mitarbeiter":
                    #Abrufen von Daten aus der Mitarbeiter Tabelle
                    cursor.execute('SELECT "Vor-_x0020_Nachname" FROM Mitarbeiter')
                    auswahl_data = cursor.fetchall()
                    #Daten in Mitarbeiter ComboBox einfügen
                    mask2_auswahl['values'] = [item[0] for item in auswahl_data]
                    #global mask2_auswahl_mitarbeiter 
                    mask2_auswahl_mitarbeiter = 'mitarbeiter'
                    
                elif mask2_auswahl_var.get() == "Arbeitsplatz":
                    #Abrufen von Daten aus der Arbeitsplatz Tabelle
                    cursor.execute("SELECT Raum FROM Raum")
                    auswahl_data = cursor.fetchall()
                    #Daten in Raum ComboBox einfügen
                    mask2_auswahl['values'] = [item[0] for item in auswahl_data]
                    
                    mask2_auswahl_mitarbeiter = 'arbeitsplatz'
                    
        def speichern():
            global mask2_inventar_NrEntryString
            global mask2_auswahlString
            mask2_auswahlString = mask2_auswahl.get()
            mask2_inventar_NrEntryString = mask2_inventar_NrEntry.get()
            mask2_auswahl_mitarbeiter
            #mask2_bezeichnungInputString = mask2_bezeichnungInput.get()
            cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,))
            result = cursor.fetchall()
            #print(result)
            #print(mask2_auswahlString)
            if mask2_auswahlString !="None" and mask2_auswahlString !="Mitarbeiter" and mask2_auswahlString !="Arbeitsplatz":
                if result !=[] and len(mask2_inventar_NrEntryString) == 6:
                    if mask2_auswahl_mitarbeiter == 'mitarbeiter':
                        #print('Mitarbeiter')
                        cursor.execute("UPDATE Ware SET Raum = '' WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,)) 
                        cursor.execute("UPDATE Ware SET 'LetzterWertvonWaBewVor-MA_Ausgabe' = ? WHERE Inventar_x0020_Nr = ?", (mask2_auswahlString, mask2_inventar_NrEntryString,))
                        cursor.execute("CREATE TEMPORARY TABLE TempTable AS SELECT * FROM Mitarbeiter ORDER BY 'Vor-_x0020_Nachname' ASC")
                        cursor.execute('UPDATE Mitarbeiter SET "Vor-_x0020_Nachname" = (SELECT "Vor-_x0020_Nachname" FROM TempTable WHERE TempTable.rowid = Mitarbeiter.rowid), "MA-Kürzel" = (SELECT "MA-Kürzel" FROM TempTable WHERE TempTable.rowid = Mitarbeiter.rowid), Anmeldename = (SELECT Anmeldename FROM TempTable WHERE TempTable.rowid = Mitarbeiter.rowid)')        
                        cursor.execute("DROP TABLE TempTable")
                        connection.commit()
                    elif mask2_auswahl_mitarbeiter == 'arbeitsplatz':
                        cursor.execute("UPDATE Ware SET 'LetzterWertvonWaBewVor-MA_Ausgabe' = '' WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,)) 
                        cursor.execute("UPDATE Ware SET Raum = ? WHERE Inventar_x0020_Nr = ?", (mask2_auswahlString, mask2_inventar_NrEntryString,))
                        cursor.execute("CREATE TEMPORARY TABLE TempTable AS SELECT * FROM Raum ORDER BY Raum ASC")
                        cursor.execute("UPDATE Raum SET ID_Raum = (SELECT ID_Raum FROM TempTable WHERE TempTable.rowid = Raum.rowid), Raum = (SELECT Raum FROM TempTable WHERE TempTable.rowid = Raum.rowid)")        
                        cursor.execute("DROP TABLE TempTable")

                    cursor.execute("SELECT * FROM Ware WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,))
                    result = cursor.fetchall()
                    
                    handle_new_entry()
                    cursor.execute("SELECT MAX(Nummer) FROM Vorgang")
                    test = cursor.fetchone()
                    liste = int(test[0])
                    test1 = liste + 1
                    datumString = mask2_dateEntry.get()
                    cursor.execute("INSERT INTO Vorgang (Nummer, 'WaBewVor-Datum', BewArt_KurzBeschreibung, InventarNr, 'WaBewVor-MA_Ausgabe', 'WaBewVor-Benutzer') VALUES(?, ?, ? ,?, ? ,?)", (test1, datumString, beschreibung, mask2_inventar_NrEntryString, mask2_auswahlString, benutzername,))
                    connection.commit()
                    mask2_frame.destroy()
                else:
                    messagebox.showerror("Fehlermeldung", "Dieses Gerät existiert nicht.")
            else:
                messagebox.showerror("Fehlermeldung", "Sie müssen einen Mitarbeiter oder Arbeitsplatz auswählen.")

        def fillout(event):
            if event.keysym == "Return":
                mask2_inventar_NrEntryString = mask2_inventar_NrEntry.get()
                cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,))
                result = cursor.fetchall()
                #print(result)
                if result == [] or len(mask2_inventar_NrEntryString) < 6:
                    #print("false")
                    mask2_bezeichnungInput.configure(text="")
                    mask2_statusInput.configure(text="")
                    mask2_typInput.configure(text="")
                else:
                    cursor.execute("SELECT Bezeichnung FROM Ware WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,))
                    bezeichnung_inhalt = cursor.fetchone()
                    cursor.execute("SELECT Typ FROM Ware WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,))
                    typ_inhalt = cursor.fetchone()
                    typ_inhaltString = typ_inhalt[0]
                    cursor.execute("SELECT Status FROM Ware WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,))
                    status_inhalt = cursor.fetchone()
                    mask2_bezeichnungInput.configure(text=bezeichnung_inhalt)
                    mask2_typInput.configure(text=typ_inhaltString)
                    mask2_statusInput.configure(text=status_inhalt)
                    #print(bezeichnung_inhalt)

        def handle_new_entry():
            new_entry = mask2_auswahl.get()
            if mask2_auswahl_mitarbeiter == 'mitarbeiter':

                #Überprüfung ob Eintrag bereits in der Datenbank vorhanden ist
                cursor.execute("SELECT 'Vor-_x0020_Nachname' FROM Mitarbeiter WHERE 'Vor-_x0020_Nachname' = ?", (new_entry,))
                existing_entry = cursor.fetchone()

                if (existing_entry):
                    pass
                else:
                    cursor.execute("INSERT INTO Mitarbeiter ('Vor-_x0020_Nachname') VALUES (?)", (new_entry,))
                    connection.commit()

            elif mask2_auswahl_mitarbeiter == 'arbeitsplatz':
                #Überprüfung ob Eintrag bereits in der Datenbank vorhanden ist
                cursor.execute("SELECT Raum FROM Raum WHERE Raum = ?", (new_entry,))
                existing_entry = cursor.fetchone()

                if (existing_entry):
                    pass
                else:
                    cursor.execute("INSERT INTO Raum (Raum) VALUES (?)", (new_entry,))
                    connection.commit()
            current_values = mask2_auswahl['values']
            updated_values = sorted(current_values + (new_entry,))
            mask2_auswahl['values']= updated_values

        def open_new_frame():

            global mask2_value
            mask2_value +=30

            def delete_frame():
                global mask2_value
                mask2_deviceInput2.destroy()
                mask2_value -= 30
                
            
            mask2_deviceInput2 = tk.Frame(mask2_deviceFrame, borderwidth=1, relief="solid")
            mask2_deviceInput2.place(x=0, y=mask2_value, height=30, width=805)

            #Überprüfen bei Änderungen im Entry-Feld, Schreiben möglich 
            entry_var = tk.StringVar()
            entry_var.trace_add('write', check_entry)

            mask2_inventar_NrEntry = tk.Entry(mask2_deviceInput2, textvariable=entry_var)
            mask2_inventar_NrEntry.config(validate="key")
            mask2_inventar_NrEntry.config(validatecommand=(mask2_deviceInput2.register(validate_entry), '%P'))
            mask2_inventar_NrEntry.config(state='normal')
            mask2_inventar_NrEntry.place(x=5, y=5, width=60)

            mask2_bezeichnungInput = tk.Entry(mask2_deviceInput2)
            mask2_bezeichnungInput.place(x=100, y=5, width=100)

            mask2_typInput = tk.Entry(mask2_deviceInput2)
            mask2_typInput.place(x=210, y=5)

            mask2_statusInput = tk.Label(mask2_deviceInput2, bg="white")
            mask2_statusInput.place(x=350, y=5, width=100, height=20)

            mask2_delete = tk.Button(mask2_deviceInput2, text="-", font=('Arial', 16), command=delete_frame)
            mask2_delete.place(x=500, y=0, height=30, width=30)

        mask2_auswahl_var = tk.StringVar(value="")
        mask2_auswahl_var.set(None)

        mask2_frame = tk.Frame(self.parent, bg="white")
        mask2_frame.place(x=161, y=1, anchor="nw", height=w, width=l)

        mask2_title = tk.Label(mask2_frame, fg="black", bg='white', text="Mitarbeiterausgabe", font=('Arial', 14))
        mask2_title.place(x=10, y=10)

        mask2_date = tk.Label(mask2_frame, fg="black", bg='white', text="Datum:", font=('Arial', 12))
        mask2_date.place(x=40, y=50)
        mask2_dateEntry = DateEntry(mask2_frame, date_pattern='dd.mm.yyyy', borderwidth=1, relief='solid', locale='de_DE')
        mask2_dateEntry.place(x=100, y=50)

        mask2_mitarbeiterRadioBtn = tk.Radiobutton(mask2_frame, text="Mitarbeiter", font=('Arial', 12), bg="white", variable=mask2_auswahl_var, value="Mitarbeiter")
        mask2_mitarbeiterRadioBtn.place(x=40, y=80)

        mask2_arbeitsplatzRadioBtn = tk.Radiobutton(mask2_frame, text="Arbeitsplatz", font=('Arial', 12), bg="white", variable=mask2_auswahl_var, value="Arbeitsplatz")
        mask2_arbeitsplatzRadioBtn.place(x=140, y=80)

        
        mask2_auswahl = ttk.Combobox(mask2_frame, textvariable=mask2_auswahl_var)
        mask2_auswahl.place(x=40, y=130)

        mask2_auswahl_var.trace_add('write', update_combobox_choices)

        #Bezeichnung ComboBox Änderungsereignis behandeln
        mask2_auswahl.bind("<<ComboboxSelected>>")

        mask2_device = tk.Label(mask2_frame, text="Geräte:", fg="black", bg='white', font=('Arial', 12))
        mask2_device.place(x=40, y=170)

        mask2_speichern = tk.Button(mask2_frame, text="speichern", font=("Arial", 16), command=speichern)
        mask2_speichern.place(x=700, y=500)

        mask2_verwerfen = tk.Button(mask2_frame, text="verwerfen", font=("Arial", 16), command=verwerfen)
        mask2_verwerfen.place(x=700, y=10)

        #mask2_hinzufügen = tk.Button(mask2_frame, text="+", font=('Arial', 16), command=open_new_frame)
        #mask2_hinzufügen.place(x=500, y=170, height=30, width=30)

        #Frame zur Wahl von Geräten
        mask2_deviceFrame = tk.Frame(mask2_frame, borderwidth=1, relief="solid")
        mask2_deviceFrame.place(width=805, height=120, x=10, y=200)

        mask2_tablenameRow = tk.Frame(mask2_deviceFrame, borderwidth=1, relief="solid", bg="white")
        mask2_tablenameRow.place(x=0, y=0, height=30, width=805)

        mask2_inventarnr = tk.Label(mask2_tablenameRow, text="Inventarnr:", fg="black", font=("Arial", 12), bg="white")
        mask2_inventarnr.place(x=5, y=0)

        mask2_bezeichnung = tk.Label(mask2_tablenameRow, text="Bezeichnung:", fg="black", font=("Arial", 12), bg="white")
        mask2_bezeichnung.place(x=100, y=0)

        mask2_typ = tk.Label(mask2_tablenameRow, text="Typ:", fg="black", font=("Arial", 12), bg="white")
        mask2_typ.place(x=250, y=0)

        mask2_status = tk.Label(mask2_tablenameRow, text="Status:", fg="black", font=("Arial", 12), bg="white")
        mask2_status.place(x=360, y=0)

        mask2_deviceInput = tk.Frame(mask2_deviceFrame, borderwidth=1, relief="solid")
        mask2_deviceInput.place(x=0, y=30, height=30, width=805)

        #Überprüfen bei Änderungen im Entry-Feld, Schreiben möglich 
        entry_var = tk.StringVar()
        entry_var.trace_add('write', check_entry)

        mask2_inventar_NrEntry = tk.Entry(mask2_deviceInput, textvariable=entry_var)
        mask2_inventar_NrEntry.config(validate="key")
        mask2_inventar_NrEntry.config(validatecommand=(mask2_deviceInput.register(validate_entry), '%P'))
        mask2_inventar_NrEntry.config(state='normal')
        mask2_inventar_NrEntry.place(x=5, y=5, width=60)
        mask2_inventar_NrEntry.bind("<KeyPress>", fillout)

        mask2_bezeichnungInput = tk.Label(mask2_deviceInput, text="", bg="white")
        mask2_bezeichnungInput.place(x=100, y=5, width=100)

        mask2_typInput = tk.Label(mask2_deviceInput, text="", bg="white")
        mask2_typInput.place(x=220, y=5, width=100, height=20)

        mask2_statusInput = tk.Label(mask2_deviceInput, text="", bg="white")
        mask2_statusInput.place(x=340, y=5, width=100, height=20)