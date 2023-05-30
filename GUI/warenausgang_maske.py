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



class Warenausgang(tk.Frame):
    
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


    def open_warenausgang(self):
        def toggle_frame():
            mask3_frame.destroy()
            self.open_warenausgang()

        self.warenausgang_btn.configure(command=toggle_frame)
        
        buttons = [self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn]
        for button in buttons:
            button.state(['!pressed'])
        self.warenausgang_btn.state(['pressed'])

        def open_new_frame():

            global mask3_value
            mask3_value +=30

            def delete_frame():
                mask3_deviceInput2.destroy()
                mask3_value =- 30
                return mask3_value
            
            mask3_deviceInput2 = tk.Frame(mask3_deviceFrame, borderwidth=1, relief="solid")
            mask3_deviceInput2.place(x=0, y=mask3_value, height=30, width=805)

            #Überprüfen bei Änderungen im Entry-Feld, Schreiben möglich 
            entry_var = tk.StringVar()
            entry_var.trace_add('write', check_entry)

            mask3_inventar_NrEntry = tk.Entry(mask3_deviceInput2, textvariable=entry_var)
            mask3_inventar_NrEntry.config(validate="key")
            mask3_inventar_NrEntry.config(validatecommand=(mask3_deviceInput2.register(validate_entry), '%P'))
            mask3_inventar_NrEntry.config(state='normal')
            mask3_inventar_NrEntry.place(x=5, y=5, width=60)

            mask3_bezeichnungInput = tk.Entry(mask3_deviceInput2)
            mask3_bezeichnungInput.place(x=100, y=5, width=100)

            mask3_typInput = tk.Entry(mask3_deviceInput2)
            mask3_typInput.place(x=210, y=5)

            mask3_statusInput = tk.Label(mask3_deviceInput2, bg="white")
            mask3_statusInput.place(x=350, y=5, width=100, height=20)

            mask3_delete = tk.Button(mask3_deviceInput2, text="-", font=('Arial', 16), command=delete_frame)
            mask3_delete.place(x=500, y=0, height=30, width=30)

        #Funktion Max Länge für Entry
        def validate_entry(char):
            if len(char) > 6 :
                return False
            return True
        
        #Funktion zum Eingabe überprüfen
        def check_entry(*args):
            char = mask3_inventar_NrEntry.get()
            if len(char) >= 6:
                mask3_inventar_NrEntry.config(state='readonly')
            else:
                mask3_inventar_NrEntry.config(state='normal')

        def verwerfen():
            mask3_frame.destroy()
            self.warenausgang_btn.configure(state=tk.NORMAL)
            self.warenausgang_btn.state(['!pressed'])
            mask3_value = 30
            return mask3_value
        
        def speichern():
            inventarString = mask3_inventar_NrEntry.get()
            vorgangString = mask3_vorgangCombobox.get()
            cursor.execute("SELECT MAX(Nummer) FROM Vorgang")
            test = cursor.fetchone()
            liste = int(test[0])
            bla = liste + 1
            datumString = mask3_dateEntry.get()
            beschreibung = mask3_vorgangCombobox.get()
            cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarString,))
            result = cursor.fetchall()
            if vorgangString !="":
                if result !=[] and len(inventarString) == 6:
                    bestaetigung = messagebox.askokcancel("Bestätigung", "Möchten Sie das Gerät wirklich löschen?")
                    if bestaetigung:
                        cursor.execute("DELETE FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarString,))
                        cursor.execute("INSERT INTO Vorgang (Nummer, 'WaBewVor-Datum', BewArt_KurzBeschreibung, InventarNr, 'WaBewVor-MA_Ausgabe', 'WaBewVor-Benutzer') VALUES(?, ?, ? ,?, ?, ?)", (bla, datumString, beschreibung, inventarString,"", self.benutzername,))
                        connection.commit()
                        mask3_frame.destroy()
                        messagebox.showinfo("Löschen", "Das Gerät wurde erfolgreich gelöscht.")
                        self.open_warenausgang()
                else:
                    messagebox.showerror("Fehlermeldung", "Dieses Gerät existiert nicht.")
            else:
                messagebox.showerror("Fehlermeldung", "Sie müssen einen Vorgang auswählen.")
                
        def fillout(event):
            if event.keysym == "Return":
                mask3_inventar_NrEntryString = mask3_inventar_NrEntry.get()
                cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (mask3_inventar_NrEntryString,))
                result = cursor.fetchall()
                #print(result)
                if result == [] or len(mask3_inventar_NrEntryString) < 6:
                    print("false")
                else:
                    cursor.execute("SELECT Bezeichnung FROM Ware WHERE Inventar_x0020_Nr = ?", (mask3_inventar_NrEntryString,))
                    bezeichnung_inhalt = cursor.fetchone()
                    cursor.execute("SELECT Typ FROM Ware WHERE Inventar_x0020_Nr = ?", (mask3_inventar_NrEntryString,))
                    typ_inhalt = cursor.fetchone()
                    typ_inhaltString = typ_inhalt[0]
                    cursor.execute("SELECT Status FROM Ware WHERE Inventar_x0020_Nr = ?", (mask3_inventar_NrEntryString,))
                    status_inhalt = cursor.fetchone()
                    mask3_bezeichnungInput.configure(text=bezeichnung_inhalt)
                    mask3_typInput.configure(text=typ_inhaltString)
                    mask3_statusInput.configure(text=status_inhalt)
                    #print(bezeichnung_inhalt)
        
        mask3_frame = tk.Frame(self.parent, bg="white")
        mask3_frame.place(x=161, y=1, anchor="nw", height=w, width=l)

        mask3_title = tk.Label(mask3_frame, fg="black", bg='white', text="Warenausgang", font=('Arial', 14))
        mask3_title.place(x=10, y=10)

        mask3_date = tk.Label(mask3_frame, fg="black", bg='white', text="Datum:", font=('Arial', 12))
        mask3_date.place(x=40, y=50)
        mask3_dateEntry = DateEntry(mask3_frame, date_pattern='dd.mm.yyyy', borderwidth=1, relief='solid', locale='de_DE')
        mask3_dateEntry.place(x=100, y=50)

        mask3_vorgang = tk.Label(mask3_frame, text="Vorgang:", fg="black", bg="white", font=('Arial', 12))
        mask3_vorgang.place(x=26, y=90)

        mask3_vorgangCombobox = ttk.Combobox(mask3_frame)
        mask3_vorgangCombobox.place(x=100, y=90)

        #Abrufen von Daten aus der Typ Tabelle
        cursor.execute("SELECT Bezeichnung FROM Bewegungsarten")
        typ_data = cursor.fetchall()

        #Daten in Typ ComboBox einfügen
        mask3_vorgangCombobox['values'] = [item[0] for item in typ_data]
        #Typ ComboBox Änderungsereignis behandeln
        mask3_vorgangCombobox.bind("<<ComboboxSelected>>")

        #mask3_auswahl_var.trace_add('write', update_combobox_choices)

        mask3_device = tk.Label(mask3_frame, text="Geräte:", fg="black", bg='white', font=('Arial', 12))
        mask3_device.place(x=40, y=170)

        mask3_speichern = tk.Button(mask3_frame, text="speichern", font=("Arial", 16), command=speichern)
        mask3_speichern.place(x=700, y=500)

        mask3_verwerfen = tk.Button(mask3_frame, text="verwerfen", font=("Arial", 16), command=verwerfen)
        mask3_verwerfen.place(x=700, y=10)

        #mask3_hinzufügen = tk.Button(mask3_frame, text="+", font=('Arial', 16), command=open_new_frame)
        #mask3_hinzufügen.place(x=500, y=170, height=30, width=30)

        #Frame zur Wahl von Geräten
        mask3_deviceFrame = tk.Frame(mask3_frame, borderwidth=1, relief="solid")
        mask3_deviceFrame.place(width=805, height=120, x=10, y=200)

        mask3_tablenameRow = tk.Frame(mask3_deviceFrame, borderwidth=1, relief="solid", bg="white")
        mask3_tablenameRow.place(x=0, y=0, height=30, width=805)

        mask3_inventarnr = tk.Label(mask3_tablenameRow, text="Inventarnr:", fg="black", font=("Arial", 12), bg="white")
        mask3_inventarnr.place(x=5, y=0)

        mask3_bezeichnung = tk.Label(mask3_tablenameRow, text="Bezeichnung:", fg="black", font=("Arial", 12), bg="white")
        mask3_bezeichnung.place(x=100, y=0)

        mask3_typ = tk.Label(mask3_tablenameRow, text="Typ:", fg="black", font=("Arial", 12), bg="white")
        mask3_typ.place(x=250, y=0)

        mask3_status = tk.Label(mask3_tablenameRow, text="Status:", fg="black", font=("Arial", 12), bg="white")
        mask3_status.place(x=350, y=0)

        mask3_deviceInput = tk.Frame(mask3_deviceFrame, borderwidth=1, relief="solid")
        mask3_deviceInput.place(x=0, y=30, height=30, width=805)

        #Überprüfen bei Änderungen im Entry-Feld, Schreiben möglich 
        entry_var = tk.StringVar()
        entry_var.trace_add('write', check_entry)

        mask3_inventar_NrEntry = tk.Entry(mask3_deviceInput, textvariable=entry_var)
        mask3_inventar_NrEntry.config(validate="key")
        mask3_inventar_NrEntry.config(validatecommand=(mask3_deviceInput.register(validate_entry), '%P'))
        mask3_inventar_NrEntry.config(state='normal')
        mask3_inventar_NrEntry.place(x=5, y=5, width=60)
        mask3_inventar_NrEntry.bind("<KeyPress>", fillout)

        mask3_bezeichnungInput = tk.Label(mask3_deviceInput, text="", bg="white")
        mask3_bezeichnungInput.place(x=100, y=5, width=100)

        mask3_typInput = tk.Label(mask3_deviceInput, text="", bg="white")
        mask3_typInput.place(x=210, y=5, width=100)

        mask3_statusInput = tk.Label(mask3_deviceInput, text="", bg="white")
        mask3_statusInput.place(x=350, y=5, width=100, height=20)