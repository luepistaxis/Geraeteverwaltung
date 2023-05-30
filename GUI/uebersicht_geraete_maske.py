import sqlite3
import tkinter as tk
import os
from tkinter import ttk

# Datenbank Verbindung
gui_folder = os.path.dirname(os.path.abspath(__file__))
#database_path = "K:\\IT-Assistenz\\Geräteverwaltung\\Geraeteverwaltung\\Geraeteverwaltung\\database.db"
database_path = os.path.join(gui_folder, "..", "Datenbank", "database.db")
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

#Länge und Breite der Frames
l = 1280
w = 720


class UebersichtGeraete(tk.Frame):
    
    def __init__(self, parent, wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn):
        super().__init__(parent)
        self.parent = parent
        self.wareneingang_btn = wareneingang_btn
        self.ausgabe_btn = ausgabe_btn
        self.warenausgang_btn = warenausgang_btn
        self.vorgaenge_btn = vorgaenge_btn
        self.uebersichtMitarbeiter_btn = uebersichtMitarbeiter_btn
        self.uebersichtGeraete_btn = uebersichtGeraete_btn

    def open_uebersicht_geraete(self):
        def toggle_frame():
            if mask6_frame.winfo_ismapped():
                mask6_frame.pack_forget()
                self.open_uebersicht_geraete()

            else:
                mask6_frame.pack()

        self.uebersichtGeraete_btn.configure(command=toggle_frame)

        buttons = [self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn]
        for button in buttons:
            button.state(['!pressed'])
        self.uebersichtGeraete_btn.state(['pressed'])
        mask6_frame = tk.Frame(self.parent, bg="white")
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