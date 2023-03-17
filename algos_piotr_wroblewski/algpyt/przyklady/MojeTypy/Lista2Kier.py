# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
class Element:    # Rekord danych
    def __init__(self, pNazwisko="Doe", pWiek=0):
        self.nazwisko = pNazwisko
        self.wiek = pWiek
        self.nastepny = None
        self.poprzedni = None
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
class Lista2Kier:   # Właściwa lista dwukierunkowa
    def __init__(self):
       self.glowa = None
       self.ogon = None

    def wstaw(self, pNazwisko, pWiek):  # Proste wstawianie na koniec listy
       nowy = Element(pNazwisko, pWiek)
       if self.glowa !=None:
            self.ogon.nastepny = nowy
            nowy.poprzedni = self.ogon
            self.ogon=nowy
       else:
            self.glowa = nowy
            self.ogon =  nowy

    def wypiszWprzod(self, s):
        print(s)
        tmp=self.glowa
        while (tmp !=None):
            print(f"[{tmp.nazwisko}, {tmp.wiek}]", end=" ")
            tmp = tmp.nastepny
        print("")

    def wypiszWstecz(self,s ):
        print(s)
        tmp=self.ogon
        while (tmp != None):
            print(f"[{tmp.nazwisko}, {tmp.wiek}]", end=" ")
            tmp = tmp.poprzedni
        print("")

    def szukaj(self, pNazw): # Odszukaj rekord 'pNazw' na liście
        tmp = self.glowa            # Zmienna zapamiętująca status przeszukiwania listy
        znaleziono=False

        while tmp != None:
            if tmp.nazwisko==pNazw:
                znaleziono=True
                break # Wychodzimy z pętli
            else:
                tmp=tmp.nastepny    # Idź dalej
        if znaleziono==True:
            return tmp, True        #  Zwróć wynik poszukiwań (referencja do rekordu)
        else:
            return None, False      # Nic nie znaleziono!

    def usun(self, pNazw): # Odszukaj i usuń rekord pasujący do kryterium wyszukiwania
        res, znaleziono = self.szukaj(pNazw)
        if znaleziono==False:
            print(f"Brak [{pNazw}] na liśie")
            return

        print(f"Usuwam [{pNazw}] z listy")

        if (res.poprzedni) != None and res.nastepny!=None:              # Środek
            (res.poprzedni).nastepny = res.nastepny
            (res.nastepny).poprzedni = (res.poprzedni).nastepny
            return

        if res == self.glowa:                   # Usuwam z przodu
            self.glowa=res.nastepny
            (res.nastepny).poprzedni=None
        else:                                   # Usuwam z tyłu
            (res.poprzedni).nastepny = None
            self.ogon = res.poprzedni

# Proba bezpośredniego wywołania modułu
if __name__ == "__main__":
	print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "Lista2KierMain.py!")
