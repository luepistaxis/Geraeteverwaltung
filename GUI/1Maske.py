import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from tkcalendar import DateEntry
from tkcalendar import Calendar
import locale
import sqlite3

locale.setlocale(locale.LC_ALL, 'de_DE')



def open_mask1():

    #SQLite Datenbank Verbindung
    database_path = "C:\\Users\\luisa.aslanidis\\VisualProjekte\\Geraeteverwaltung\\Geraeteverwaltung\\database.db"
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    buttons = [button1, button2, button3, button4, button5, button6]
    for index, button in enumerate(buttons):
        button.state(['!pressed'])
        if index == 0:
            pass
        else:
            button.configure(style="TButton")
    button1.state(['pressed'])

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

    def handle_new_entry(event):
        if event.keysym == "Return":
            new_entry = typ_combo_var.get()
            if new_entry:

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

    #Frame für Geräte
    mask1_frame = tk.Frame(mainwindow, width=950, height=500, bg="white")
    mask1_frame.pack(side="right", fill="both")
    mask1_title = tk.Label(mask1_frame, fg="black", bg='white', text="Warenaufnahme", font=('Arial', 14))
    mask1_title.place(x=10, y=10)

    mask1_date = tk.Label(mask1_frame, fg="black", bg='white', text="Datum:", font=('Arial', 12))
    mask1_date.place(x=40, y=50)
    mask1_dateEntry = DateEntry(mask1_frame, date_pattern='dd.mm.yyyy', borderwidth=1, relief='solid', locale='de_DE')
    mask1_dateEntry.place(x=100, y=50)
    mask1_device = tk.Label(mask1_frame, text="Geräte:", fg="black", bg='white', font=('Arial', 12))
    mask1_device.place(x=40, y=90)

    #Frame zum Eingeben der Geräte Informationen
    mask1_deviceFrame = tk.Frame(mask1_frame)
    mask1_deviceFrame.place(width=805, height=200, x=10, y=120)

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
    mask1_typCombobox.bind("<KeyPress>", handle_new_entry)

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
    mask1_raum.place(x=300, y=10)
    cursor.execute("SELECT Raum FROM Raum ORDER BY ID_Raum LIMIT 1")
    default_value = cursor.fetchone()[0]
    raum_combo_var = tk.StringVar(value=default_value)
    mask1_raumCombobox = ttk.Combobox(mask1_deviceFrame, textvariable=raum_combo_var)
    mask1_raumCombobox.place(x=350, y=10)

    cursor.execute("SELECT Raum FROM Raum")
    raum_data = cursor.fetchall()

    mask1_raumCombobox['values'] = [item[0] for item in raum_data]

    mask1_raumCombobox.bind("<<ComboboxSelected>>")

    mask1_seriennr = tk.Label(mask1_deviceFrame, text="Seriennr.:", fg="black", font=('Arial', 12))
    mask1_seriennr.place(x=278, y=35)
    mask1_seriennrEntry = tk.Entry(mask1_deviceFrame) 
    mask1_seriennrEntry.place(x=350, y=35)

def open_mask2():
    buttons = [button1, button2, button3, button4, button5, button6]
    for button in buttons:
        button.state(['!pressed'])
    button2.state(['pressed'])
    
    mask2_frame = tk.Frame(mainwindow, width=550, height=1000)
    mask2_frame.pack(side="right", fill="both")

def open_mask3():
    buttons = [button1, button2, button3, button4, button5, button6]
    for button in buttons:
        button.state(['!pressed'])
    button3.state(['pressed'])
    
    mask3_frame = tk.Frame(mainwindow, width=950, height=500)
    mask3_frame.pack(side="right", fill="both")

def open_mask4():
    buttons = [button1, button2, button3, button4, button5, button6]
    for button in buttons:
        button.state(['!pressed'])
    button4.state(['pressed'])
    mask4_frame = tk.Frame(mainwindow, width=950, height=500)
    mask4_frame.pack(side="right", fill="both")

def open_mask5():
    buttons = [button1, button2, button3, button4, button5, button6]
    for button in buttons:
        button.state(['!pressed'])
    button5.state(['pressed'])
    mask5_frame = tk.Frame(mainwindow, width=950, height=500)
    mask5_frame.pack(side="right", fill="both")

def open_mask6():
    buttons = [button1, button2, button3, button4, button5, button6]
    for button in buttons:
        button.state(['!pressed'])
    button6.state(['pressed'])
    mask6_frame = tk.Frame(mainwindow, width=950, height=500)
    mask6_frame.pack(side="right", fill="both")





# Hauptfenster erstellen
mainwindow = tk.Tk()
mainwindow.title("Geräteverwaltung")
mainwindow.geometry("1000x600")

# Frame für die senkrechte Menüleiste
menu_frame = tk.Frame(mainwindow, width=18, height=600)
menu_frame.pack(side="left", fill="y")

# Style für MenüButton
style = ThemedStyle(menu_frame)
style.set_theme("default")
style.configure("TButton", borderwidth=1, relief="raised", background="#CCC", foreground="#000", padding=(2, 30), font=("Arial", 12), width=18)
style.map("TButton", background=[("active", "#AAA")])


# Buttons für die Menüpunkte
button1 = ttk.Button(menu_frame, text="Warenaufnahme", command=open_mask1, style="TButton")
button1.pack()

button2 = ttk.Button(menu_frame, text="Ausgabe", command=open_mask2, style="TButton")
button2.pack()

button3 = ttk.Button(menu_frame, text="Warenausgang", command=open_mask3, style="TButton")
button3.pack()

button4 = ttk.Button(menu_frame, text="Alle Vorgänge", command=open_mask4, style="TButton")
button4.pack()

button5 = ttk.Button(menu_frame, text="Übersicht Mitarbeiter", command=open_mask5, style="TButton")
button5.pack()

button6 = ttk.Button(menu_frame, text="Übersicht Geräte", command=open_mask6, style="TButton")
button6.pack()

# Hauptfenster starten
mainwindow.mainloop()


