from geraeteliste import GeraeteListe
from mitarbeiterliste import MitarbeiterListe
from bezeichnungen import Bezeichnungen
from typ import Typ
from eigentuemer import Eigentuemer
from raum import Raum

class Main:
    def __init__(self):
        self.geraeteliste = GeraeteListe()
        self.mitarbeiterliste = MitarbeiterListe()
        self.bezeichnungen = Bezeichnungen()
        self.typ = Typ()
        self.eigentuemer = Eigentuemer()
        self.raum = Raum()

    def run(self):
        self.geraeteliste.geraeteliste_methode()
        self.mitarbeiterliste.mitarbeiterliste_methode()
        self.bezeichnungen.bezeichnungen_methode()
        self.typ.typ_methode()
        self.eigentuemer.eigentuemer_methode()
        self.raum.raum_methode()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()