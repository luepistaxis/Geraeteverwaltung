import sqlite3
import tkinter as tk
from tkinter import messagebox
from getpass import getpass
import os
from mainWindow import MainWindow

# Datenbank Verbindung
gui_folder = os.path.dirname(os.path.abspath(__file__))
#database_path = "K:\\IT-Assistenz\\Geräteverwaltung\\Geraeteverwaltung\\Geraeteverwaltung\\database.db"
database_path = os.path.join(gui_folder, "..", "Datenbank", "database.db")
connection = sqlite3.connect(database_path)
cursor = connection.cursor()

class LoginWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Anmeldung")
        self.geometry("300x150")

        self.username_label = tk.Label(self, text="Benutzername:")
        self.username_label.pack()

        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Passwort:")
        self.password_label.pack()

        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_btn = tk.Button(self, text="Anmelden", command=self.login)
        self.login_btn.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT benutzer_id FROM Benutzer WHERE benutzer_id = ?", (username,))
        username_table = cursor.fetchone()

        if username_table is not None:
            cursor.execute("SELECT password FROM Benutzer WHERE benutzer_id = ?", (username,))
            password_table = cursor.fetchone()
            if username == username_table[0] and password == password_table[0]:
                self.destroy()
                window = MainWindow()
                window.mainloop()
            else:
                messagebox.showerror("Fehler", "Ungültige Anmeldedaten")
        else:
            messagebox.showerror("Fehler", "Benutzer nicht gefunden")

login_window = LoginWindow()
login_window.mainloop()