from geraeteliste import GeraeteListe
from mitarbeiterliste import MitarbeiterListe
from bezeichnungen import Bezeichnungen
from typ import Typ
from eigentuemer import Eigentuemer
from raum import Raum
from bewegungsarten import Bewegungsarten
from vorgang import Vorgang
from vorgang_erweitert import Vorgang_erweitert
from vorgaenge import Vorgaenge

class Main:
    def __init__(self):
        self.geraeteliste = GeraeteListe()
        self.mitarbeiterliste = MitarbeiterListe()
        self.bezeichnungen = Bezeichnungen()
        self.typ = Typ()
        self.eigentuemer = Eigentuemer()
        self.raum = Raum()
        self.bewegungsarten = Bewegungsarten()
        self.vorgang = Vorgang()
        self.vorgang_erweitert = Vorgang_erweitert()
        self.vorgaenge = Vorgaenge()

    def run(self):
        self.geraeteliste.geraeteliste_methode()
        self.mitarbeiterliste.mitarbeiterliste_methode()
        self.bezeichnungen.bezeichnungen_methode()
        self.typ.typ_methode()
        self.eigentuemer.eigentuemer_methode()
        self.raum.raum_methode()
        self.bewegungsarten.bewegungsarten_methode()
        self.vorgang.vorgang_methode()
        self.vorgang_erweitert.vorgang_erweitert_methode()
        self.vorgaenge.vorgaenge_methode()

if __name__ == "__main__":
    main_instance = Main()
    main_instance.run()