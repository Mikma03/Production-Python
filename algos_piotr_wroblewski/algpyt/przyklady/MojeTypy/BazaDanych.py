from MojeTypy import Kartoteka as k
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
class IndeksNazwisk:        # Klasa pomocnicza, realizuje sortowanie wg nazwisk
    def __init__(self):     # Lista będzie zawiera referencje do obiektów klasy Osoba
        self.ref=None
        self.nastepny=None  # Odsyłacz do  kolejnego elementu listy IndeksNazwisk

    def wypiszKolejne(self, s):
        tmp = self
        while (tmp != None):
            print("[", tmp.ref.nazwisko, " zarabia ", tmp.ref.zarobek, "]")
            tmp=tmp.nastepny;
        print()
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
class IndeksZarobkow:  # Klasa pomocnicza, realizuje sortowanie wg nazwisk
    def __init__(self):
        self.ref=None
        self.nastepny=None  # Do kolejnego elementu IndeksZarobkow

    def wypiszKolejne(self, s):
        tmp = self
        while (tmp != None):
            print("[", tmp.ref.nazwisko, " zarabia ", tmp.ref.zarobek, "]")
            tmp=tmp.nastepny;
        print()
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
class BazaDanych:
    def __init__(self):
        self.dane=k.Kartoteka()       # Własciwa lista danych (nieposortowana)
        # Lista indeksująca zarobki:
        self.glowaZ = None
        self.ogonZ  = None
        # Lista indeksująca nazwiska
        self.glowaN = None
        self.ogonN  = None
    # ---------------------------------------------------------------------------------
    def wstawSortNazw(self, nowaref):  # Wstaw nowy element do listy indeksowej
        # Wstawiamy odsyłacz'nowaref' zwrócony przez  wstawNaKoniec()!
        nazw = nowaref.nazwisko
        nowy =  IndeksNazwisk()  # Tworzymy nowy element na liście indeksu
        nowy.ref = nowaref
        # Poszukiwanie właściwej pozycji na wstawienie elementu:
        if (self.glowaN == None):  # Lista pusta
            self.glowaN = nowy
            self.ogonN = nowy
            return  # Pozwala na szybkie opuszczenie funkcji
        # Poszukiwanie miejsca na wstawienie:
        szukamy = True  # Stan poszukiwania miejsca na wstawienie
        przed = None  # 'przed' i 'po' określą miejsce wstawiania nowego elementu
        po = self.glowaN
        while (szukamy and (po != None)):
            if (po.ref.nazwisko >= nazw):  # Kryterium sortowania (*)
                szukamy = False  # Znaleźliśmy właściwe miejsce!
            else:  # Szukamy dalej
                przed = po
                po = po.nastepny
        # Wstawiamy, analizując wartości zapamiętane w 'przed' i 'po'
        if (przed == None):  # Na początek listy
            self.glowaN = nowy
            nowy.nastepny = po
        else:
            if (po == None):  # Na koniec listy
                przed.nastepny = nowy
                self.ogonN = nowy  # Nowy koniec listy!
            else:  # Wstawiamy gdzieś w środku "rozpinając" łańcuszek danych
                przed.nastepny = nowy
                nowy.nastepny = po
    # ---------------------------------------------------------------------------------
    def wstawSortZarobk(self, nowaref):   # Wstaw nowy element do listy indeksowej
        # Wstawiamy odsyłacz'nowaref' zwrócony przez  wstawNaKoniec()!
        zar = nowaref.zarobek
        nowy = IndeksZarobkow()  # Tworzymy nowy element na liście indeksu
        nowy.ref = nowaref
        # Poszukiwanie właściwej pozycji na wstawienie elementu:
        if (self.glowaZ == None):  # Lista pusta
            self.glowaZ = nowy
            self.ogonZ = nowy
            return  # Pozwala na szybkie opuszczenie funkcji
        # Poszukiwanie miejsca na wstawienie:
        szukamy = True  # Stan poszukiwania miejsca na wstawienie
        przed = None  # 'przed' i 'po' określą miejsce wstawiania nowego elementu
        po = self.glowaZ
        while (szukamy and (po != None)):
            if (po.ref.zarobek >= zar):  # Kryterium sortowania (*)
                szukamy = False  # Znaleźliśmy właściwe miejsce!
            else:  # Szukamy dalej
                przed = po
                po = po.nastepny
        # Wstawiamy, analizując wartości zapamiętane w 'przed' i 'po'
        if (przed == None):  # Na początek listy
            self.glowaZ = nowy
            nowy.nastepny = po
        else:
            if (po == None):  # Na koniec listy
                przed.nastepny = nowy
                self.ogonZ = nowy  # Nowy koniec listy!
            else:  # Wstawiamy gdzieś w środku "rozpinając" łańcuszek danych
                przed.nastepny = nowy
                nowy.nastepny = po
    # ---------------------------------------------------------------------------------
    def wstawSort(self, nazw, zar):
        nowaref = self.dane.wstawNaKoniec(nazw, zar)  # Tworzymy nowy rekord danych
        self.wstawSortZarobk(nowaref)  # Przebudowa indeksu 'zarobki'
        self.wstawSortNazw(nowaref)  # Przebudowa indeksu 'nazwiska'
    # ---------------------------------------------------------------------------------
    def wypiszSortZarobk(self, s):    # Wypisz listę wg indeksu zarobków
     print(s)
     if self.glowaZ != None:
        self.glowaZ.wypiszKolejne(s)
     else:
         print("Indeks pusty")
# ---------------------------------------------------------------------------------
    def wypiszSortNazw(self, s):  # Wypisz listę wg indeksu nazwisk
         print(s)
         if self.glowaN != None:
             self.glowaN.wypiszKolejne(s)
         else:
             print("Indeks pusty")
    # ---------------------------------------------------------------------------------
    def wypiszNieposortowane(self, s):    # Wypisz listę pierwotną
     print(s)
     if self.dane != None:
        self.dane.wypisz()
     else:
         print("Baza jest pusta")

# Proba bezpośredniego wywołania modułu
if __name__ == "__main__":
	print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "BazaDanychMain.py!")
