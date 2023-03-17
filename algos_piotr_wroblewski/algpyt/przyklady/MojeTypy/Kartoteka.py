# ---------------------------------------------------------------------------------
class Osoba:      # Ta klasa realizuje element składowy listy danych (rekord informacyjny)
    def __init__(self, pNazwisko, pZarobek, pNastepny=None):
        self.nazwisko = pNazwisko
        self.zarobek = pZarobek
        self.nastepny = pNastepny   # Referencja do następnego elementu listy
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
class Kartoteka:    # Ta klasa realizuje podstawową listę jednokierunkową zawierającą rekordy klasy 'Osoba'
    def __init__(self):
        self.glowa = None
        self.ogon = None
        self.dlugosc = 0
    # -------------------------------------------------------------------------
    def wstawNaKoniec(self, pNazwisko, pZarobek):   # Wstawiamy dane w kolejności przychodzenia
        osoba = Osoba(pNazwisko, pZarobek)              # (na koniec listy)
        if (self.glowa == None):  # Kartoteka pusta
            self.glowa = osoba
            self.ogon = osoba
        else:
            self.ogon.nastepny = osoba
            self.ogon = osoba
        self.dlugosc = self.dlugosc + 1
        return osoba
    # -------------------------------------------------------------------------
    def wypisz(self):
        tmp=self.glowa
        if tmp == None:
            print("\n *Kartoteka pusta*")
            return
        while tmp != None:
            print("[", tmp.nazwisko, " zarabia ", tmp.zarobek, "]")
            tmp = tmp.nastepny
        print("\n")  # Znak końca linii
    # -------------------------------------------------------------------------
    def szukajRef(self, pNazwisko):  # Odszukaj Osoba na liście i zwróć jego pozycję
        biezacy = self.glowa
        poprzedni = None
        while biezacy != None:
            if biezacy.dane == pNazwisko:
                return poprzedni, biezacy, True  # Znaleziono rekord danych
            poprzedni = biezacy
            biezacy = biezacy.nastepny
        return poprzedni, biezacy, False        # Nie znaleziono rekordu danych
    # -------------------------------------------------------------------------
    def usunWybrany(self, nazwisko):  # Odszukaj i usuń osobę o nazwisku 'nazw' na liście
        poprzedni, biezacy, znaleziono = self.szukajRef(nazwisko)  # Szukamy rekordu i jego pozycji:
        if znaleziono == False:
            print("Nie znaleziono osoby o nazwisku", s)
            return
        self.dlugosc = self.dlugosc - 1  # "Skracamy" parametr opisujący długość listy o 1

        if self.dlugosc == 0:  # Przypadek a). - Kartoteka jednoosobowa
            self.glowa = None
            self.ogon = None
            self.dlugosc = 0
            return

        if self.glowa == biezacy:  # Przypadek b). - Usuwamy z przodu
            self.glowa = biezacy.nastepny  # Przestawiamy wskaźnik "glowa"
            return

        if self.ogon == biezacy:  # Przypadek c). - Usuwamy z tyłu
            self.ogon = poprzedni  # Przestawiamy wskaźnik "ogon"
            poprzedni.nastepny = None  # Zaznaczamy nowy koniec listy
            return
        poprzedni.nastepny = biezacy.nastepny  # Przestawiamy wskaźnik "ogon"
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --


# Proba bezpośredniego wywołania modułu
if __name__ == "__main__":
	print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "BazaDanychMain.py!")
