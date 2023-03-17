# Deficje klas Element i Lista w formie biblioteki (modułu)
# ---------------------------------------------------------------------------------
class Element:
    def __init__(self, pDane, pNastepny=None):
        self.dane = pDane
        self.nastepny = pNastepny

    def wypiszElementy(self):
        tmp = self
        while tmp != None:
            print(tmp.dane, end=" ")
            tmp = tmp.nastepny
    print("\n")  # Znak końca linii
# ---------------------------------------------------------------------------------
class Lista:  # Nowa lista jest pusta (referencja 'None')
    def __init__(self):
        self.glowa = None
        self.ogon = None
        self.dlugosc = 0

    def wstawNaKoniec(self, pDane):
        x = Element(pDane)
        if (self.glowa == None):  # Lista pusta
            self.glowa = x
            self.ogon = x
        else:
            self.ogon.nastepny = x
            self.ogon = x
        self.dlugosc = self.dlugosc + 1

    def wypisz(self):
        tmp=self.glowa
        if tmp == None:
            print("\n *Lista pusta*")
            return
        while tmp != None:
            print(tmp.dane, end=" ")
            tmp = tmp.nastepny
        print("\n")  # Znak końca linii

    def szukaj(self, x):
        tmp = self.glowa
        while tmp != None:
            if tmp.dane == x:
                print("\nZnalazłem poszukiwany element ", x)
                return
            tmp = tmp.nastepny
        if tmp == None:
            print("\nNie znaleziono poszukiwanego elementu ", x)

    def szukajRef(self, x):  # Odszukaj element na liście i zwróć jego pozycję
        biezacy = self.glowa
        poprzedni = None
        while biezacy != None:
            if biezacy.dane == x:
                return poprzedni, biezacy, True  # Znaleziono element
            poprzedni = biezacy
            biezacy = biezacy.nastepny
        return poprzedni, biezacy, False  # Nie znaleziono elementu

    def UsunPierwszy(self):  # Usuń pierwszy element z listy
        if self.glowa != None:
            self.glowa = self.glowa.nastepny
            self.dlugosc = self.dlugosc - 1  # "Skracamy" parametr opisujący długość listy o 1

    def usunWybrany(self, x):  # Odszukaj i usuń element na liście

        poprzedni, biezacy, znaleziono = self.szukajRef(x)  # Szukamy elementu i jego pozycji:

        if znaleziono == False:
            print("Nie znaleziono elementu")
            return
        self.dlugosc = self.dlugosc - 1  # "Skracamy" parametr opisujący długość listy o 1

        if self.dlugosc == 0:  # Przypadek a). - lista jednoelementowa
            self.glowa = None
            self.ogon = None
            self.dlugosc = 0
            # print("Usuwamy z listy 1-elementowej")
            return

        if self.glowa == biezacy:  # Przypadek b). - Usuwamy z przodu
            # print("Usuwamy z przodu")
            self.glowa = biezacy.nastepny  # Przestawiamy wskaźnik "glowa"
            return

        if self.ogon == biezacy:  # Przypadek c). - Usuwamy z tyłu
            # print("Usuwamy z tyłu")
            self.ogon = poprzedni  # Przestawiamy wskaźnik "ogon"
            poprzedni.nastepny = None  # Zaznaczamy nowy koniec listy
            return
            # Przypadek d). - Usuwamy ze środka
        poprzedni.nastepny = biezacy.nastepny  # Przestawiamy wskaźnik "ogon"
        # print("Usuwamy ze środka")

    def wstawSort(self, x):
        nowy = Element(x)
        self.dlugosc = self.dlugosc + 1
        # Poszukiwanie właściwej pozycji na wstawienie elementu:
        if (self.glowa == None):  # Lista pusta
            self.glowa = nowy
            self.ogon = nowy
            return  # Pozwala na szybkie opuszczenie funkcji
        # Poszukiwanie miejsca na wstawienie:
        szukamy = True  # Stan poszukiwania miejsca na wstawienie
        przed = None  # 'przed' i 'po' określą miejsce wstawiania nowego elementu
        po = self.glowa
        while (szukamy and (po != None)):
            if (po.dane >= x):  # Kryterium sortowania (*)
                szukamy = False  # Znaleźliśmy właściwe miejsce!
            else:  # Szukamy dalej
                przed = po
                po = po.nastepny
        # Wstawiamy, analizując wartości zapamiętane w 'przed' i 'po'
        if (przed == None):  # Na początek listy
            self.glowa = nowy
            nowy.nastepny = po
        else:
            if (po == None):  # Na koniec listy
                przed.nastepny = nowy
                self.ogon = nowy  # Nowy koniec listy!
            else:  # Wstawiamy gdzieś w środku "rozpinając" łańcuszek danych
                przed.nastepny = nowy
                nowy.nastepny = po

    # -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
    # Złączanie list - metoda nieoptymalna
    def __add__(self, x2):  # Ta metoda zwraca obiekt będący sumą dwóch list w wyniku
        suma = Lista()  # operacji x1+x2, gdzie x1 jest bieżącym obiektem (self)
        q1 = self.glowa
        q2 = x2.glowa
        while (q1 != None):  # Przekopiowanie elementów z bieżącego obiektu do listy 'suma'
            suma.wstawSort(q1.dane)
            q1 = q1.nastepny
        while (q2 != None):  # Przekopiowanie elementów z drugiej listy ‘x’ do listy 'suma'
            suma.wstawSort(q2.dane)
            q2 = q2.nastepny
        return suma
# ---------------------------------------------------------------------------------
# Złączanie list – funkcja (nie metoda klasy) operująca na liście obiektów klasy Element

def sortuj(a, b):
    if a == None:
        return b
    if b == None:
        return a
    if a.dane <= b.dane:  # Porównywanie wartości - tutaj zmień ew. kryterium lub wbuduj funkcję porównującą
        a.nastepny = sortuj(a.nastepny, b)
        return a
    else:
        b.nastepny = sortuj(b.nastepny, a)
        return b

# Fuzja list x1, y1 – funkcja (nie metoda klasy) zwracają nowy obiekt klasy Lista będący złączeniem x2 i y1

def fuzja(x1, y1):  # Zakładamy, że x1 i y1 są obiektami klasy Lista
    nowaLista = Lista()
    nowaLista.dlugosc = x1.dlugosc + y1.dlugosc
    nowaLista.glowa = sortuj(x1.glowa, y1.glowa)  # Sekwencja złączonych elementów danych (obiekty klasy Element)
    #
    if x1.glowa == None:
        nowaLista.ogon = y1.ogon
    elif y1.glowa == None:
        nowaLista.ogon = x1.ogon
    else:
        if x1.ogon == None:  # Prawy skrajny element, za nim "nie ma już nic" (cytując klasyka)
            nowaLista.ogon = x1.ogon
        else:
            nowaLista.ogon = y1.ogon
    return nowaLista


# Proba bezpośredniego wywołania modułu
if __name__ == "__main__":
	print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "listaMain.py!")
