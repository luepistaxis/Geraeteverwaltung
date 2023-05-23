import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle
from tkcalendar import DateEntry
import locale
import sqlite3
import getpass

#Kalender auf Deutsche Sprache
locale.setlocale(locale.LC_ALL, 'de_DE')

#Hinzufügen von neuem Feld
mask1_value = 120
mask2_value = 30
mask3_value = 30
mask2_auswahl_mitarbeiter = ''

#Länge und Breite der Frames
l = 1280
w = 720





benutzername = getpass.getuser()
#SQLite Datenbank Verbindung
#script_dir = os.path.dirname(__file__)
db_filename = 'database.db'
#db_path1 = os.path.join(script_dir, db_filename)
database_path = "C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\database.db"
connection = sqlite3.connect(database_path)
cursor = connection.cursor()



def open_Wareneingang():
    beschreibung = "Lagereingang"
    def toggle_frame():
        mask1_frame.destroy()
        open_Wareneingang()
        #print('gelöscht')

    wareneingang_btn.configure(command=toggle_frame)

    buttons = [wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn]
    for index, button in enumerate(buttons):
        button.state(['!pressed'])
        if index == 0:
            pass
        else:
            button.configure(style="TButton")
    wareneingang_btn.state(['pressed'])

    #wareneingang_btn.configure(state=tk.DISABLED)

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

    #def bezeichnung_handle_selection(event):
        #selected_option = combo_var.get()
        #print(selected_option)

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
        #cursor.close()
        #connection.close()

    def verwerfen():
        mask1_frame.destroy()
        wareneingang_btn.configure(state=tk.NORMAL)
        wareneingang_btn.state(['!pressed'])
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
        #print(result)
        if result == [] and len(inventarString) == 6:
        
            if inventarString == "" or bezeichnungString == "" or typString == "" or eigentuemerString == "" or raumString == "":
                messagebox.showerror("Fehlermeldung", "Nicht alle Pflichtfelder wurden ausgefüllt.\nAchten Sie darauf, dass alle Pflichtfelder ausgefüllt sind.")
                return
            cursor.execute("INSERT INTO Ware ('Inventar_x0020_Nr', Bezeichnung, Typ, 'Serien-Nr', 'Eigentümer', Raum, 'LetzterWertvonWaBewVor-MA_Ausgabe', Status, 'Netto_x0020_Einkaufspreis') VALUES (?, ?, ?, ?, ?, ?, NULL, 'Freigegeben', ?)", (inventarString, bezeichnungString, typString, seriennrString, eigentuemerString, raumString, preisString))
            #cursor.execute("UPDATE Ware SET Inventar_x0020_Nr = (SELECT Inventar_x0020_Nr FROM Ware ORDER BY Inventar_x0020_Nr ASC)")
            #cursor.execute("CREATE INDEX IF NOT EXISTS indexname ON Ware('Inventar_x0020_Nr')")
            cursor.execute("CREATE TEMPORARY TABLE TempTable AS SELECT * FROM Ware ORDER BY Inventar_x0020_Nr ASC")
            cursor.execute('UPDATE Ware SET Inventar_x0020_Nr = (SELECT Inventar_x0020_Nr FROM TempTable WHERE TempTable.rowid = Ware.rowid), Bezeichnung = (SELECT Bezeichnung FROM TempTable WHERE TempTable.rowid = Ware.rowid), Typ = (SELECT Typ FROM TempTable WHERE TempTable.rowid = Ware.rowid), "Serien-Nr" = (SELECT "Serien-Nr" FROM TempTable WHERE TempTable.rowid = Ware.rowid), Eigentümer = (SELECT Eigentümer FROM TempTable WHERE TempTable.rowid = Ware.rowid), Raum = (SELECT Raum FROM TempTable WHERE TempTable.rowid = Ware.rowid), "LetzterWertvonWaBewVor-MA_Ausgabe" = (SELECT "LetzterWertvonWaBewVor-MA_Ausgabe" FROM TempTable WHERE TempTable.rowid = Ware.rowid), Status = (SELECT Status FROM TempTable WHERE TempTable.rowid = Ware.rowid), Netto_x0020_Einkaufspreis = (SELECT Netto_x0020_Einkaufspreis FROM TempTable WHERE TempTable.rowid = Ware.rowid)')        
            cursor.execute("DROP TABLE TempTable")
            handle_new_entry()
            cursor.execute("SELECT * FROM Ware WHERE Inventar_x0020_Nr = ?", (inventarString,))
            result = cursor.fetchall()
            #print(result)
            cursor.execute("SELECT MAX(Nummer) FROM Vorgang")
            test = cursor.fetchone()
            liste = int(test[0])
            bla = liste + 1
            #test1 = (liste,)
            #print(test1)
            #cursor.execute("SELECT MAX(ID-WaBewVor) FROM Vorgang")
            #wert = cursor.fetchall()
            #print(wert)
            #aktuellWert = wert[0]
            datumString = mask1_dateEntry.get()
            cursor.execute("INSERT INTO Vorgang (Nummer, 'WaBewVor-Datum', BewArt_KurzBeschreibung, InventarNr, 'WaBewVor-MA_Ausgabe', 'WaBewVor-Benutzer') VALUES(?, ?, ? ,?, ?, ?)", (bla, datumString, beschreibung, inventarString, "" ,benutzername,))
            connection.commit()
            mask1_frame.destroy()
            warenausgang_btn.config(state="normal")
            messagebox.showinfo("", "Erfolgreich hinzugefügt! :)")
            open_Wareneingang()

        elif len(inventarString) < 6:
            messagebox.showerror("Fehlermeldung", "Die Inventar Nr ist zu kurz\nBitte gib eine 6-stellige Zahl ein.")

        else:
            messagebox.showerror("Fehlermeldung", "Gerät existiert schon!")
        
        

    def open_new_frame():

        global mask1_value
        mask1_value +=120

        def delete_frame():
            mask1_deviceFrame2.destroy()
            global mask1_value
            mask1_value -= 120

        #Frame zum Eingeben der Geräte Informationen
        mask1_deviceFrame2 = tk.Frame(mask1_frame, borderwidth=1, relief="solid")
        mask1_deviceFrame2.place(width=805, height=120, x=10, y=mask1_value)

        mask1_inventar_Nr = tk.Label(mask1_deviceFrame2, text="Inventar Nr.:", fg="black", font=('Arial', 12))
        mask1_inventar_Nr.place(x=30, y=10)

        #Überprüfen bei Änderungen im Entry-Feld, Schreiben möglich 
        entry_var = tk.StringVar()
        entry_var.trace_add('write', check_entry)

        mask1_inventar_NrEntry = tk.Entry(mask1_deviceFrame2, textvariable=entry_var)
        mask1_inventar_NrEntry.config(validate="key")
        mask1_inventar_NrEntry.config(validatecommand=(mask1_deviceFrame2.register(validate_entry), '%P'))
        mask1_inventar_NrEntry.config(state='normal')
        mask1_inventar_NrEntry.place(x=120, y=10)

        mask1_bezeichnung = tk.Label(mask1_deviceFrame2, text="Bezeichnung:", fg="black", font=('Arial', 12))
        mask1_bezeichnung.place(x=19, y=35)

        bezeichnung_combo_var = tk.StringVar()
        mask1_bezeichnungComboBox = ttk.Combobox(mask1_deviceFrame2, textvariable=bezeichnung_combo_var)
        mask1_bezeichnungComboBox.place(x=120, y=35)

        #Abrufen von Daten aus der Bezeichnungen Tabelle
        cursor.execute("SELECT Bezeichnung FROM Bezeichnungen")
        bezeichnung_data = cursor.fetchall()
        #print(data)

        

        #Daten in Bezeichnung ComboBox einfügen
        mask1_bezeichnungComboBox['values'] = [item[0] for item in bezeichnung_data]
        #Bezeichnung ComboBox Änderungsereignis behandeln
        mask1_bezeichnungComboBox.bind("<<ComboboxSelected>>")

        mask1_typ = tk.Label(mask1_deviceFrame2, text="Typ:", fg="black", font=('Arial', 12))
        mask1_typ.place(x=83, y=60)



        typ_combo_var = tk.StringVar()
        mask1_typCombobox = ttk.Combobox(mask1_deviceFrame2, textvariable=typ_combo_var)
        mask1_typCombobox.place(x=120, y=60)

        #Abrufen von Daten aus der Typ Tabelle
        cursor.execute("SELECT Bezeichnung FROM Typ")
        typ_data = cursor.fetchall()

        #Daten in Typ ComboBox einfügen
        mask1_typCombobox['values'] = [item[0] for item in typ_data]
        #Typ ComboBox Änderungsereignis behandeln
        mask1_typCombobox.bind("<<ComboboxSelected>>")
        #mask1_typCombobox.bind("<KeyPress>", handle_new_entry)

        mask1_eigentuemer = tk.Label(mask1_deviceFrame2, text="Eigentümer:", fg="black", font=('Arial', 12))
        mask1_eigentuemer.place(x=29, y=85)
        
        eigentuemer_combo_var = tk.StringVar()
        mask1_eigentuemerComboBox = ttk.Combobox(mask1_deviceFrame2, textvariable=eigentuemer_combo_var)
        mask1_eigentuemerComboBox.place(x=120, y=85)

        cursor.execute("SELECT Eigentümer FROM Eigentuemer")
        eigentuemer_data = cursor.fetchall()

        mask1_eigentuemerComboBox['values'] = [item[0] for item in eigentuemer_data]

        mask1_eigentuemerComboBox.bind("<<ComboboxSelected>>")
        
        mask1_raum = tk.Label(mask1_deviceFrame2, text="Raum:", fg="black", font=('Arial', 12))
        mask1_raum.place(x=337, y=10)
        cursor.execute("SELECT Raum FROM Raum ORDER BY ID_Raum LIMIT 1")
        default_value = cursor.fetchone()[0]
        raum_combo_var = tk.StringVar(value=default_value)
        mask1_raumCombobox = ttk.Combobox(mask1_deviceFrame2, textvariable=raum_combo_var)
        mask1_raumCombobox.place(x=390, y=10)

        cursor.execute("SELECT Raum FROM Raum")
        raum_data = cursor.fetchall()

        mask1_raumCombobox['values'] = [item[0] for item in raum_data]

        mask1_raumCombobox.bind("<<ComboboxSelected>>")

        mask1_seriennr = tk.Label(mask1_deviceFrame2, text="Seriennr.:", fg="black", font=('Arial', 12))
        mask1_seriennr.place(x=315, y=35)
        mask1_seriennrEntry = tk.Entry(mask1_deviceFrame2) 
        mask1_seriennrEntry.place(x=390, y=35)

        mask1_weiterenr = tk.Label(mask1_deviceFrame2, text="Weitere:", fg="black", font=('Arial', 12))
        mask1_weiterenr.place(x=323, y=60)
        mask1_weiterenrEntry = tk.Entry(mask1_deviceFrame2) 
        mask1_weiterenrEntry.place(x=390, y=60)

        mask1_preis = tk.Label(mask1_deviceFrame2, text="Einkaufspreis:", fg="black", font=('Arial', 12))
        mask1_preis.place(x=282, y=85)
        mask1_preisEntry = tk.Entry(mask1_deviceFrame2) 
        mask1_preisEntry.place(x=390, y=85)

        mask1_delete = tk.Button(mask1_deviceFrame2, text="-", font=('Arial', 16), command=delete_frame)
        mask1_delete.place(x=550, y=10, width=30, height=30)



    #Frame für Geräte
    mask1_frame = tk.Frame(mainwindow, bg="white")
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
    #print(data)

    

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
    #mask1_typCombobox.bind("<KeyPress>", handle_new_entry)

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

    

def open_Ausgabe():
    def toggle_frame():
        mask2_frame.destroy()
        open_Ausgabe()
        print('gelöscht')

    ausgabe_btn.configure(command=toggle_frame)

    beschreibung = "Ausgabe"
 
    buttons = [wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn]
    for button in buttons:
        button.state(['!pressed'])
    ausgabe_btn.state(['pressed'])
    
    #ausgabe_btn.configure(state=tk.DISABLED)

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
        ausgabe_btn.configure(state=tk.NORMAL)
        ausgabe_btn.state(['!pressed'])
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
        global mask2_auswahl_mitarbeiter
        #mask2_bezeichnungInputString = mask2_bezeichnungInput.get()
        cursor.execute("SELECT Inventar_x0020_Nr FROM Ware WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,))
        result = cursor.fetchall()
        #print(result)
        print(mask2_auswahlString)
        if mask2_auswahlString !="None" and mask2_auswahlString !="Mitarbeiter" and mask2_auswahlString !="Arbeitsplatz":
            if result !=[] and len(mask2_inventar_NrEntryString) == 6:
                if mask2_auswahl_mitarbeiter == 'mitarbeiter':
                    #print('Mitarbeiter')
                    cursor.execute("UPDATE Ware SET Raum = '' WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,)) 
                    cursor.execute("UPDATE Ware SET 'LetzterWertvonWaBewVor-MA_Ausgabe' = ? WHERE Inventar_x0020_Nr = ?", (mask2_auswahlString, mask2_inventar_NrEntryString,))
                    #print(type(mask2_inventar_NrEntryString))
                    #print(mask2_auswahlString)
                    connection.commit()
                elif mask2_auswahl_mitarbeiter == 'arbeitsplatz':
                    cursor.execute("UPDATE Ware SET 'LetzterWertvonWaBewVor-MA_Ausgabe' = '' WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,)) 
                    cursor.execute("UPDATE Ware SET Raum = ? WHERE Inventar_x0020_Nr = ?", (mask2_auswahlString, mask2_inventar_NrEntryString,))
                    #print('Arbeitsplatz')
                    #print(mask2_auswahlString)
                    #print(mask2_inventar_NrEntryString)
                
                cursor.execute("SELECT * FROM Ware WHERE Inventar_x0020_Nr = ?", (mask2_inventar_NrEntryString,))
                result = cursor.fetchall()
                #print(result)
                cursor.execute("SELECT MAX(Nummer) FROM Vorgang")
                test = cursor.fetchone()
                liste = int(test[0])
                bla = liste + 1
                #test1 = (liste,)
                #print(test1)
                #cursor.execute("SELECT MAX(ID-WaBewVor) FROM Vorgang")
                #wert = cursor.fetchall()
                #print(wert)
                #aktuellWert = wert[0]
                datumString = mask2_dateEntry.get()
                cursor.execute("INSERT INTO Vorgang (Nummer, 'WaBewVor-Datum', BewArt_KurzBeschreibung, InventarNr, 'WaBewVor-MA_Ausgabe', 'WaBewVor-Benutzer') VALUES(?, ?, ? ,?, ? ,?)", (bla, datumString, beschreibung, mask2_inventar_NrEntryString, mask2_auswahlString, benutzername,))
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

    
    
    mask2_frame = tk.Frame(mainwindow, bg="white")
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

def open_Warenausgang():
    def toggle_frame():
        mask3_frame.destroy()
        open_Warenausgang()
        #print('gelöscht')

    warenausgang_btn.configure(command=toggle_frame)
    
    buttons = [wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn]
    for button in buttons:
        button.state(['!pressed'])
    warenausgang_btn.state(['pressed'])

    #warenausgang_btn.configure(state=tk.DISABLED)

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
        warenausgang_btn.configure(state=tk.NORMAL)
        warenausgang_btn.state(['!pressed'])
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
                    cursor.execute("INSERT INTO Vorgang (Nummer, 'WaBewVor-Datum', BewArt_KurzBeschreibung, InventarNr, 'WaBewVor-MA_Ausgabe', 'WaBewVor-Benutzer') VALUES(?, ?, ? ,?, ?, ?)", (bla, datumString, beschreibung, inventarString,"", benutzername,))
                    connection.commit()
                    mask3_frame.destroy()
                    messagebox.showinfo("Löschen", "Das Gerät wurde erfolgreich gelöscht.")
                    open_Warenausgang()
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
    
    mask3_frame = tk.Frame(mainwindow, bg="white")
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

def open_vorgaenge():
    buttons = [wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn]
    for button in buttons:
        button.state(['!pressed'])
    vorgaenge_btn.state(['pressed'])

    mask4_frame = tk.Frame(mainwindow, bg="white")
    mask4_frame.place(x=161, y=1, anchor="nw", relheight=500, relwidth=805)

    mask5_title = tk.Label(mask4_frame, fg="black", bg='white', text="Alle Vorgänge", font=('Arial', 14))
    mask5_title.place(x=10, y=10)

    cursor.execute('SELECT Nummer, "WaBewVor-Datum", BewArt_KurzBeschreibung AS Beschreibung, InventarNr, "WaBewVor-MA_Ausgabe" AS "ausgegeben an", "WaBewVor-Benutzer" AS "bearbeitet durch" FROM Vorgang ORDER BY Nummer DESC')
    rows = cursor.fetchall()

    tree = ttk.Treeview(mask4_frame)
    scrollbar = tk.Scrollbar(mask4_frame, orient="vertical", command=tree.yview)
    scrollbar.place(x=1081, y=60, height=620)
    tree.configure(yscrollcommand=scrollbar.set, height=30)

    columns = cursor.description
    column_names = [column[0] for column in columns]
    #column_names = column_names[1:]
    tree['columns'] = column_names
    
    tree.column(column_names[0], width=70)
    tree.column(column_names[1], width=150)
    tree.column(column_names[2], width=200)
    tree.column(column_names[3], width=100)
    tree.column(column_names[4], width=180)
    tree.column(column_names[5], width=120)

    for column in column_names:
        tree.heading(column, text=column)

    tree.configure(show="tree headings tree")
    style = ttk.Style()
    #style.configure("Treeview.Heading", background="white", foreground="black")

    for row in rows:
        tree.insert('', 'end', values=row)
    
    scrollbar.config(command=tree.yview)

    tree.configure(xscrollcommand=scrollbar.set)

    tree.place(x=-200, y=60)

def open_uebersichtMitarbeiter():
    def toggle_frame():
        if mask5_frame.winfo_ismapped():
            mask5_frame.pack_forget()
            open_uebersichtMitarbeiter()
            print('gelöscht')

        else:
            mask5_frame.pack()
            print('geöffnet')

    uebersichtMitarbeiter_btn.configure(command=toggle_frame)

    buttons = [wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn]
    for button in buttons:
        button.state(['!pressed'])
    uebersichtMitarbeiter_btn.state(['pressed'])

    mask5_frame = tk.Frame(mainwindow, bg="white")
    mask5_frame.place(x=161, y=1, anchor="nw", relheight=500, relwidth=950)

    #mask5_frame.place(x=161, y=0, anchor="nw", relheight=300, relwidth=150)
    mask5_title = tk.Label(mask5_frame, fg="black", bg='white', text="Übersicht Mitarbeiter", font=('Arial', 14))
    mask5_title.place(x=10, y=10)

    cursor.execute('SELECT "LetzterWertvonWaBewVor-MA_Ausgabe" AS Mitarbeiter, Inventar_x0020_Nr AS InventarNr, Bezeichnung, Typ, "Serien-Nr", Andere_x0020_Nummer AS Weitere FROM Ware WHERE Mitarbeiter !="" ORDER BY Mitarbeiter')
    rows = cursor.fetchall()

    

    tree = ttk.Treeview(mask5_frame)
    scrollbar = tk.Scrollbar(mask5_frame, orient="vertical", command=tree.yview)
    scrollbar.place(x=1081, y=60, height=620)
    tree.configure(yscrollcommand=scrollbar.set, height=30)

    
    columns = cursor.description
    column_names = [column[0] for column in columns]
    #column_names = column_names[1:]
    tree['columns'] = column_names
    
    tree.column(column_names[0], width=180)
    tree.column(column_names[1], width=65)
    tree.column(column_names[2], width=100)
    tree.column(column_names[3], width=250)
    tree.column(column_names[4], width=245)
    tree.column(column_names[5], width=240)


    for column in column_names:
        tree.heading(column, text=column)

    tree.configure(show="tree headings tree")
    style = ttk.Style()
    #style.configure("Treeview.Heading", background="white", foreground="black")

    for row in rows:
        tree.insert('', 'end', values=row)
    
    scrollbar.config(command=tree.yview)

    tree.configure(xscrollcommand=scrollbar.set)

    tree.place(x=-200, y=60)



    

def open_uebersichtGeraete():
    def toggle_frame():
        if mask6_frame.winfo_ismapped():
            mask6_frame.pack_forget()
            open_uebersichtGeraete()
            print('gelöscht')

        else:
            mask6_frame.pack()
            print('geöffnet')

    uebersichtGeraete_btn.configure(command=toggle_frame)

    buttons = [wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn]
    for button in buttons:
        button.state(['!pressed'])
    uebersichtGeraete_btn.state(['pressed'])
    mask6_frame = tk.Frame(mainwindow, bg="white")
    mask6_frame.place(x=161, y=0, anchor="nw", relheight=300, relwidth=150)
    mask6_title = tk.Label(mask6_frame, fg="black", bg='white', text="Übersicht Geräte", font=('Arial', 14))
    mask6_title.place(x=10, y=10)

    cursor.execute('SELECT Inventar_x0020_Nr AS InventarNr, Bezeichnung, Typ, "Serien-Nr", Andere_x0020_Nummer AS Weitere, Eigentümer, Raum, "LetzterWertvonWaBewVor-MA_Ausgabe" AS Mitarbeiter, Status, Netto_x0020_Einkaufspreis AS Preis FROM Ware ORDER BY Inventar_x0020_Nr DESC')
    rows = cursor.fetchall()

    

    tree = ttk.Treeview(mask6_frame)
    scrollbar = tk.Scrollbar(mask6_frame, orient="vertical", command=tree.yview)
    scrollbar.place(x=1081, y=60, height=620)
    tree.configure(yscrollcommand=scrollbar.set, height=30)

    
    columns = cursor.description
    column_names = [column[0] for column in columns]
    #column_names = column_names[1:]
    tree['columns'] = column_names
    
    tree.column(column_names[0], width=65)  #InventarNr
    tree.column(column_names[1], width=75)  #Bezeichnung
    tree.column(column_names[2], width=180) #Typ
    tree.column(column_names[3], width=140) #SerienNr
    tree.column(column_names[4], width=150) #Weitere
    tree.column(column_names[5], width=80)  #Eigentümer
    tree.column(column_names[6], width=100) #Raum
    tree.column(column_names[7], width=160) #Mitarbeiter
    tree.column(column_names[8], width=80)  #Status
    tree.column(column_names[9], width=50)  #Einkaufspreis

    for column in column_names:
        tree.heading(column, text=column)

    tree.configure(show="tree headings tree")
    style = ttk.Style()
    #style.configure("Treeview.Heading", background="white", foreground="black")

    for row in rows:
        tree.insert('', 'end', values=row)
    
    scrollbar.config(command=tree.yview)

    tree.configure(xscrollcommand=scrollbar.set)

    tree.place(x=-200, y=60)



# Hauptfenster erstellen
mainwindow = tk.Tk()
mainwindow.title("Geräteverwaltung")
mainwindow.geometry("1280x720")

# Frame für die senkrechte Menüleiste
menu_frame = tk.Frame(mainwindow)
menu_frame.place(x=1, y=1, width=160, height=600)

# Style für MenüButton
style = ThemedStyle(menu_frame)
style.set_theme("default")
style.configure("TButton", borderwidth=1, relief="raised", background="#CCC", foreground="#000", padding=(2, 30), font=("Arial", 12), width=18)
style.map("TButton", background=[("active", "#AAA")])


# Buttons für die Menüpunkte
wareneingang_btn = ttk.Button(menu_frame, text="Warenaufnahme", command=open_Wareneingang, style="TButton")
wareneingang_btn.pack()

ausgabe_btn = ttk.Button(menu_frame, text="Ausgabe", command=open_Ausgabe, style="TButton")
ausgabe_btn.pack()

warenausgang_btn = ttk.Button(menu_frame, text="Warenausgang", command=open_Warenausgang, style="TButton")
warenausgang_btn.pack()

vorgaenge_btn = ttk.Button(menu_frame, text="Alle Vorgänge", command=open_vorgaenge, style="TButton")
vorgaenge_btn.pack()

uebersichtMitarbeiter_btn = ttk.Button(menu_frame, text="Übersicht Mitarbeiter", command=open_uebersichtMitarbeiter, style="TButton")
uebersichtMitarbeiter_btn.pack()

uebersichtGeraete_btn = ttk.Button(menu_frame, text="Übersicht Geräte", command=open_uebersichtGeraete, style="TButton")
uebersichtGeraete_btn.pack()

buttonExit = ttk.Button(menu_frame, text="Exit", command=mainwindow.destroy)
buttonExit.pack(side="bottom")

# Hauptfenster starten
mainwindow.mainloop()

cursor.close()
connection.close()
