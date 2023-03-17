class Element:
    def __init__(self, pWiek, pNazwisko):
        self.wiek= pWiek
        self.nazwisko = pNazwisko

    def __hash__(self):     # Spersonalizowana metoda hash()
       return hash( (self.wiek, self.nazwisko) )

    def __eq__(self, o2):   # Spersonalizowane porównywanie obiektów:
         return self.wiek==o2.wiek and self.nazwisko==o2.nazwisko

o1 = Element(35, "Kowalski")
o2 = Element(35, "Kowalski")
o3 = Element(32, "Kowalska")
print("Prywatna funkcja hash(), obiekt o1:", hash(o1) )
print("Prywatna funkcja hash(), obiekt o2:", hash(o2) )
print("Prywatna funkcja hash(), obiekt o3:", hash(o3) )
print(o1==o2)