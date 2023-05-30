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
            warenausgang_frame.destroy()
            self.open_warenausgang()

        self.warenausgang_btn.configure(command=toggle_frame)
        
        buttons = [self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn]
        for button in buttons:
            button.state(['!pressed'])
        self.warenausgang_btn.state(['pressed'])

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
            warenausgang_frame.destroy()
            self.warenausgang_btn.configure(state=tk.NORMAL)
            self.warenausgang_btn.state(['!pressed'])
            value = 30
            return value
        
        def speichern():
            inventar_string = inventarnr_entry.get()
            vorgang_string = vorgang_combobox.get()
            cursor.execute("SELECT MAX(Nummer) FROM Vorgang")
            test = cursor.fetchone()
            liste = int(test[0])
            next_number = liste + 1
            datum_string = date_entry.get()
            beschreibung = vorgang_combobox.get()
            cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (inventar_string,))
            result = cursor.fetchall()
            if vorgang_string !="":
                if result !=[] and len(inventar_string) == 6:
                    bestaetigung = messagebox.askokcancel("Bestätigung", "Möchten Sie das Gerät wirklich löschen?")
                    if bestaetigung:
                        cursor.execute("DELETE FROM Ware WHERE Inventar_x0020_Nr = ?", (inventar_string,))
                        cursor.execute("INSERT INTO Vorgang (Nummer, 'WaBewVor-Datum', BewArt_KurzBeschreibung, InventarNr, 'WaBewVor-MA_Ausgabe', 'WaBewVor-Benutzer') VALUES(?, ?, ? ,?, ?, ?)", (next_number, datum_string, beschreibung, inventar_string,"", self.benutzername,))
                        connection.commit()
                        warenausgang_frame.destroy()
                        messagebox.showinfo("Löschen", "Das Gerät wurde erfolgreich gelöscht.")
                        self.open_warenausgang()
                else:
                    messagebox.showerror("Fehlermeldung", "Dieses Gerät existiert nicht.")
            else:
                messagebox.showerror("Fehlermeldung", "Sie müssen einen Vorgang auswählen.")
                
        def fillout(event):
            if event.keysym == "Return":
                inventarnr_entry_string = inventarnr_entry.get()
                cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarnr_entry_string,))
                result = cursor.fetchall()
                #print(result)
                if result == [] or len(inventarnr_entry_string) < 6:
                    print("false")
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
        
        warenausgang_frame = tk.Frame(self.parent, bg="white")
        warenausgang_frame.place(x=161, y=1, anchor="nw", height=w, width=l)

        title = tk.Label(warenausgang_frame, fg="black", bg='white', text="Warenausgang", font=('Arial', 14))
        title.place(x=10, y=10)

        date = tk.Label(warenausgang_frame, fg="black", bg='white', text="Datum:", font=('Arial', 12))
        date.place(x=40, y=50)
        date_entry = DateEntry(warenausgang_frame, date_pattern='dd.mm.yyyy', borderwidth=1, relief='solid', locale='de_DE')
        date_entry.place(x=100, y=50)

        vorgang = tk.Label(warenausgang_frame, text="Vorgang:", fg="black", bg="white", font=('Arial', 12))
        vorgang.place(x=26, y=90)

        vorgang_combobox = ttk.Combobox(warenausgang_frame)
        vorgang_combobox.place(x=100, y=90)

        #Abrufen von Daten aus der Typ Tabelle
        cursor.execute("SELECT Bezeichnung FROM Bewegungsarten")
        typ_data = cursor.fetchall()

        #Daten in Typ ComboBox einfügen
        vorgang_combobox['values'] = [item[0] for item in typ_data]
        #Typ ComboBox Änderungsereignis behandeln
        vorgang_combobox.bind("<<ComboboxSelected>>")

        #mask3_auswahl_var.trace_add('write', update_combobox_choices)

        device = tk.Label(warenausgang_frame, text="Geräte:", fg="black", bg='white', font=('Arial', 12))
        device.place(x=40, y=170)

        speichern = tk.Button(warenausgang_frame, text="speichern", font=("Arial", 16), command=speichern)
        speichern.place(x=700, y=500)

        verwerfen = tk.Button(warenausgang_frame, text="verwerfen", font=("Arial", 16), command=verwerfen)
        verwerfen.place(x=700, y=10)

        #hinzufügen = tk.Button(warenausgang_frame, text="+", font=('Arial', 16), command=open_new_frame)
        #hinzufügen.place(x=500, y=170, height=30, width=30)

        #Frame zur Wahl von Geräten
        device_frame = tk.Frame(warenausgang_frame, borderwidth=1, relief="solid")
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
        status.place(x=350, y=0)

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
        typ_input.place(x=210, y=5, width=100)

        status_input = tk.Label(device_input, text="", bg="white")
        status_input.place(x=350, y=5, width=100, height=20)