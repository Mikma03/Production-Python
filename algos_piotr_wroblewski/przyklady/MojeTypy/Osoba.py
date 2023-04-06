class Osoba:      # Ta klasa realizuje element składowy listy danych (rekord informacyjny)
    def __init__(self, pNazwisko, pZarobek, pNastepny=None):
        self.nazwisko = pNazwisko
        self.zarobek = pZarobek
        self.nastepny = pNastepny   # Referencja do następnego elementu listy