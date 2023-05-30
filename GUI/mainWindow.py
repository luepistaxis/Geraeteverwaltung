import tkinter as tk
import locale
import getpass

from tkinter import ttk
from ttkthemes import ThemedStyle
from wareneingang_maske import Wareneingang
from ausgabe_maske import Ausgabe
from warenausgang_maske import Warenausgang
from vorgaenge_maske import Vorgaenge
from uebersicht_mitarbeiter_maske import UebersichtMitarbeiter
from uebersicht_geraete_maske import UebersichtGeraete

# Kalender auf Deutsche Sprache
locale.setlocale(locale.LC_ALL, 'de_DE')

# Benutzername für die Vorgänge 
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
        self.wareneingang_btn = ttk.Button(self.menu_frame, text="Warenaufnahme", command=self.open_wareneingang, style="TButton")
        self.wareneingang_btn.pack()

        self.ausgabe_btn = ttk.Button(self.menu_frame, text="Ausgabe", command=self.open_ausgabe, style="TButton")
        self.ausgabe_btn.pack()

        self.warenausgang_btn = ttk.Button(self.menu_frame, text="Warenausgang", command=self.open_warenausgang, style="TButton")
        self.warenausgang_btn.pack()

        self.vorgaenge_btn = ttk.Button(self.menu_frame, text="Alle Vorgänge", command=self.open_vorgaenge, style="TButton")
        self.vorgaenge_btn.pack()

        self.uebersichtMitarbeiter_btn = ttk.Button(self.menu_frame, text="Übersicht Mitarbeiter", command=self.open_uebersicht_mitarbeiter, style="TButton")
        self.uebersichtMitarbeiter_btn.pack()

        self.uebersichtGeraete_btn = ttk.Button(self.menu_frame, text="Übersicht Geräte", command=self.open_uebersicht_geraete, style="TButton")
        self.uebersichtGeraete_btn.pack()

        self.buttonExit = ttk.Button(self.menu_frame, text="Exit", command=self.destroy)
        self.buttonExit.pack(side="bottom")

        self.wareneingang = Wareneingang(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)
        self.ausgabe = Ausgabe(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)
        self.warenausgang = Warenausgang(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)
        self.vorgaenge = Vorgaenge(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)
        self.uebersicht_mitarbeiter = UebersichtMitarbeiter(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)
        self.uebersicht_geraete = UebersichtGeraete(self, self.wareneingang_btn, self.ausgabe_btn, self.warenausgang_btn, self.vorgaenge_btn, self.uebersichtMitarbeiter_btn, self.uebersichtGeraete_btn)

    def open_wareneingang(self):
        self.wareneingang.open_wareneingang()

    def open_ausgabe(self):
        self.ausgabe.ausgabe()

    def open_warenausgang(self):
        self.warenausgang.open_warenausgang()

    def open_vorgaenge(self):
        self.vorgaenge.open_vorgaenge()

    def open_uebersicht_mitarbeiter(self):
        self.uebersicht_mitarbeiter.open_uebersicht_mitarbeiter()
    
    def open_uebersicht_geraete(self):
        self.uebersicht_geraete.open_uebersicht_geraete()

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    mainKlasse = MainWindow()
    mainKlasse.run()