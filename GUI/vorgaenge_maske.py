import sqlite3
import tkinter as tk
import getpass
import os
from tkinter import ttk


#Länge und Breite der Frames
l = 1280
w = 720

#Benutzername für die Vorgänge 
benutzername = getpass.getuser()

class Vorgaenge(tk.Frame):

    # Datenbank Verbindung
    gui_folder = os.path.dirname(os.path.abspath(__file__))
    #database_path = "K:\\IT-Assistenz\\Geräteverwaltung\\Geraeteverwaltung\\Geraeteverwaltung\\database.db"
    database_path = os.path.join(gui_folder, "..", "Datenbank", "database.db")
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    def __init__(self, parent, wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn):
        super().__init__(parent)
        self.parent = parent
        self.wareneingang_btn = wareneingang_btn
        self.ausgabe_btn = ausgabe_btn
        self.warenausgang_btn = warenausgang_btn
        self.vorgaenge_btn = vorgaenge_btn
        self.uebersichtMitarbeiter_btn = uebersichtMitarbeiter_btn
        self.uebersichtGeraete_btn = uebersichtGeraete_btn

    def open_vorgaenge(self):
        self.buttons = [self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn]
        for button in self.buttons:
            button.state(['!pressed'])
        self.vorgaenge_btn.state(['pressed'])

        self.vorgaenge_frame = tk.Frame(self.parent, bg="white")
        self.vorgaenge_frame.place(x=161, y=1, anchor="nw", relheight=500, relwidth=805)

        title = tk.Label(self.vorgaenge_frame, fg="black", bg='white', text="Alle Vorgänge", font=('Arial', 14))
        title.place(x=10, y=10)

        self.cursor.execute('SELECT * FROM Vorgaenge ORDER BY Nummer DESC')
        self.rows = self.cursor.fetchall()
        
        self.tree = ttk.Treeview(self.vorgaenge_frame)
        scrollbar = tk.Scrollbar(self.vorgaenge_frame, orient="vertical", command=self.tree.yview)
        scrollbar.place(x=1081, y=60, height=620)
        self.tree.configure(yscrollcommand=scrollbar.set, height=30)

        columns = self.cursor.description
        column_names = [column[0] for column in columns]
        #column_names = column_names[1:]
        self.tree['columns'] = column_names
        
        self.tree.column(column_names[0], width=70)
        self.tree.column(column_names[1], width=150)
        self.tree.column(column_names[2], width=200)
        self.tree.column(column_names[3], width=100)
        self.tree.column(column_names[4], width=180)
        self.tree.column(column_names[5], width=120)

        for column in column_names:
            self.tree.heading(column, text=column)

        self.tree.configure(show="tree headings tree")

        for row in self.rows:
            self.tree.insert('', 'end', values=row)
        
        scrollbar.config(command=self.tree.yview)

        self.tree.configure(xscrollcommand=scrollbar.set)

        self.tree.place(x=-200, y=60)