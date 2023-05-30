import tkinter as tk
import locale
import getpass

from tkinter import ttk
from ttkthemes import ThemedStyle
from maske1 import Maske1
from maske2 import Maske2
from maske3 import Maske3
from maske4 import Maske4
from maske5 import Maske5
from maske6 import Maske6

#Kalender auf Deutsche Sprache
locale.setlocale(locale.LC_ALL, 'de_DE')

#Benutzername für die Vorgänge 
benutzername = getpass.getuser()


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Geräteverwaltung")
        self.geometry("1280x720")
        
        # Frame für die senkrechte Menüleiste
        self.menu_frame = tk.Frame(self)
        self.menu_frame.place(x=1, y=1, width=160, height=600)

        # Style für MenüButton
        style = ThemedStyle(self.menu_frame)
        style.set_theme("default")
        style.configure("TButton", borderwidth=1, relief="raised", background="#CCC", foreground="#000", padding=(2, 30), font=("Arial", 12), width=18)
        style.map("TButton", background=[("active", "#AAA")])

        # Buttons für die Menüpunkte
        self.wareneingang_btn = ttk.Button(self.menu_frame, text="Warenaufnahme", command=self.open_maske1, style="TButton")
        self.wareneingang_btn.pack()

        self.ausgabe_btn = ttk.Button(self.menu_frame, text="Ausgabe", command=self.open_maske2, style="TButton")
        self.ausgabe_btn.pack()

        self.warenausgang_btn = ttk.Button(self.menu_frame, text="Warenausgang", command=self.open_maske3, style="TButton")
        self.warenausgang_btn.pack()

        self.vorgaenge_btn = ttk.Button(self.menu_frame, text="Alle Vorgänge", command=self.open_maske4, style="TButton")
        self.vorgaenge_btn.pack()

        self.uebersichtMitarbeiter_btn = ttk.Button(self.menu_frame, text="Übersicht Mitarbeiter", command=self.open_maske5, style="TButton")
        self.uebersichtMitarbeiter_btn.pack()

        self.uebersichtGeraete_btn = ttk.Button(self.menu_frame, text="Übersicht Geräte", command=self.open_maske6, style="TButton")
        self.uebersichtGeraete_btn.pack()

        self.buttonExit = ttk.Button(self.menu_frame, text="Exit", command=self.destroy)
        self.buttonExit.pack(side="bottom")

        self.maske1 = Maske1(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)
        self.maske2 = Maske2(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)
        self.maske3 = Maske3(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)
        self.maske4 = Maske4(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)
        self.maske5 = Maske5(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)
        self.maske6 = Maske6(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)

    def open_maske1(self):
        self.maske1.open_wareneingang()

    def open_maske2(self):
        self.maske2.open_ausgabe()

    def open_maske3(self):
        self.maske3.open_warenausgang()

    def open_maske4(self):
        self.maske4.open_vorgaenge()

    def open_maske5(self):
        self.maske5.open_uebersicht_mitarbeiter()
    
    def open_maske6(self):
        self.maske6.open_uebersicht_geraete()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    mainKlasse = MainWindow()
    mainKlasse.run()