# Ilustracja dziedziczenia klas

class Osoba:              # Klasa "bazowa"
       def __init__(self, pImie, pNazwisko):      # Konstruktor
              print("* Konstruktor klasy bazowej 'Osoba'")
              self.imie=pImie
              self.nazwisko= pNazwisko

       def __str__(self): # Obiekt jako napis
              return self.imie + " "+ self.nazwisko
       def komunikat1(self):
              print("Komunikat 1: metoda klasy 'Osoba'")

       def komunikat2(self):
              print("Komunikat 2: metoda klasy 'Osoba'")

class Uczen(Osoba):         # Klasa pochopdna
       def __init__(self, pImie, pNazwisko, pNrKlasy):    # Konstruktor
              print("** Konstruktor klasy pochodnej 'Uczen'")
              super().__init__(pImie, pNazwisko)        # Wywołujemy konstruktor klasy bazowej
              self.nrklasy=pNrKlasy                     # Tworzymy nowe pole potrzebne w klasie 'Uczen'

       def __str__(self): # Obiekt jako napis
              s = super().__str__()                      # Wykorzystamy częściowo z kodu klasy bazowej!
              return s+",  Klasa: " +self.nrklasy       # Doklejamy informacje specyficzne dla klasy Pomiar

       def komunikat2(self):                             # Nadpisujemy metodę 'konunikat2'
              print("Komunikat 2: nowa metoda klasy 'Uczen'")

# --------- Kilka przykładów użycia: ------------------------------------------------------------

o=Osoba("Janek", "Kowalski")
print("Obiekt klasy bazowej 'Osoba':",o)
o.komunikat1()
o.komunikat2()

u=Uczen("Anna", "Kotecka", "2A")
print("Obiekt klasy pochodnej 'Uczen':",u)

u.komunikat1() # (**)
u.komunikat2() # (***)
