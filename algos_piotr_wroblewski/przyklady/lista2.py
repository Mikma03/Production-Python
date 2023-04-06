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


# ---------------------------------------------------------------------------------
# Przykłady użycia - bez sortowania

print("Lista zwykła, wstawiam kolejno: 3, 5, 7, 0")
l = Lista()  # Tworzymy pustą listę
l.wstawNaKoniec(3)
l.wstawNaKoniec(5)
l.wstawNaKoniec(7)
l.wstawNaKoniec(0)
print("Lista l=", end=" ")  # Lista l= 3 5 7 0
l.wypisz()

l.szukaj(2)
l.szukaj(7)

# Przykład użycia - z sortowaniem
print("Lista zwykła, wstawiam kolejno: 0 1 3 5 6 7 7")
m = Lista()  # Tworzymy pustą listę

m.wstawSort(3)  # 3
m.wstawSort(5)  # 3 5
m.wstawSort(7)  # 3 5 7
m.wstawSort(0)  # 0 3 5 7
m.wstawSort(1)  # 0 1 3 5 7
m.wstawSort(6)  # 0 1 3 5 6 7
m.wstawSort(7)  # 0 1 3 5 6 7 7
print("Lista q=", end=" ")
m.wypisz()  # Lista q= 0 1 3 5 6 7 7

# Przykłady usuwania elementów z listy

print("\nUsuwamy pierwszy element")
m.UsunPierwszy()
m.wypisz()  # 1 3 5 6 7 7

m.usunWybrany(1)  # 3 5 6 7 7

m.wypisz()
m.usunWybrany(7)  # 3 5 6 7
m.wypisz()
m.usunWybrany(7)  # 3 5 6
m.wypisz()
m.usunWybrany(7)  # 3 5 6 (brak akcji)

m.usunWybrany(5),
m.wypisz()
m.usunWybrany(3)  # 5 6
m.wypisz()
m.usunWybrany(6)  # 6
m.wypisz()
m.usunWybrany(6)  # (list pusta)
m.wypisz()

# Sumowanie list (1) - metoda nieoptymalna
print("Sumowanie list (1) - metoda nieoptymalna")
x, y = Lista(), Lista()
x.wstawSort(3), x.wstawSort(2), x.wstawSort(1)
y.wstawSort(6), y.wstawSort(5), y.wstawSort(4), y.wstawSort(0)
suma = x + y  # Zauważ dynamiczne wiązanie typu do zmiennej referencyjnej 'suma'!
suma.wypisz()

# Sumowanie list (2) - fuzja
print("Sumowanie list (2) - fuzja")
x1, y1  = Lista(), Lista()

for n in [3, 6, 2, 5, 12, 0, 19]:
    x1.wstawSort(n)
print("Lista x1=", end=" ")  # 0 2 3 5 6 12 19
x1.wypisz()
for n in [5, 2, 2, 1, 9]:
    y1.wstawSort(n)
print("Lista y1=", end=" ")  # 1 2 2 5 9
y1.wypisz()

pofuzji = fuzja(x1, y1) # Fukcja zwróci obiekt klasy Lista
print("Lista x1+y1 (fuzja)=", end=" ")  # 1 2 2 5 9
pofuzji.wypisz()
