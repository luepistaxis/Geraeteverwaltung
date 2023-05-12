from geraeteliste import GeraeteListe
from mitarbeiterliste import MitarbeiterListe
from bezeichnungen import Bezeichnungen

class Main:
    def __init__(self):
        self.geraeteliste = GeraeteListe()
        self.mitarbeiterliste = MitarbeiterListe()
        self.bezeichnungen = Bezeichnungen()

    def run(self):
        self.geraeteliste.geraeteliste_methode()
        self.mitarbeiterliste.mitarbeiterliste_methode()
        self.bezeichnungen.bezeichnungen_methode()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()