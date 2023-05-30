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


class UebersichtMitarbeiter(tk.Frame):
    
    def __init__(self, parent, wareneingang_btn, ausgabe_btn, warenausgang_btn, vorgaenge_btn, uebersichtMitarbeiter_btn, uebersichtGeraete_btn):
        super().__init__(parent)
        self.parent = parent
        self.wareneingang_btn = wareneingang_btn
        self.ausgabe_btn = ausgabe_btn
        self.warenausgang_btn = warenausgang_btn
        self.vorgaenge_btn = vorgaenge_btn
        self.uebersichtMitarbeiter_btn = uebersichtMitarbeiter_btn
        self.uebersichtGeraete_btn = uebersichtGeraete_btn

    def open_uebersicht_mitarbeiter(self):
        def toggle_frame():
            if mask5_frame.winfo_ismapped():
                mask5_frame.pack_forget()
                self.open_uebersicht_mitarbeiter()

            else:
                mask5_frame.pack()


        self.uebersichtMitarbeiter_btn.configure(command=toggle_frame)

        buttons = [self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn]
        for button in buttons:
            button.state(['!pressed'])
        self.uebersichtMitarbeiter_btn.state(['pressed'])

        mask5_frame = tk.Frame(self.parent, bg="white")
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
