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
# **********************************
# Tutaj dodajemy obsługę iteratora:
# **********************************
    def __iter__(self):
        # Zwracam obiekt klasy realizującej iterator
        # Metoda zostanie wywołana podczas wywołania iteracji
        return MojIterator(self)

class MojIterator:
   def __init__(self, pLista):
       self._kursor = pLista.glowa # Tu zapiszemy bieżącą wartość pozycji iteratora

   def __next__(self): # Zwraca kolejny element z kolekcji obsługiwanej przez iterator
       if self._kursor !=None:
           res= "["+ str(self._kursor.dane)+"]"
           self._kursor=self._kursor.nastepny
           return res
       else:
            raise StopIteration # Kończymy iterowanie
# ---------------------------------------------------------------------------------
# Przykłady użycia
lista = Lista()  # Tworzymy pustą listę
for x in [1, 3, 5, 6, 12, 9]:
    lista.wstawNaKoniec(x)
print("Lista lista=", end=" ")
lista.wypisz()
print("Wywołujemy iterator poprzez użycie pętli 'for'")
for x in lista:
    print(x, end = " ")
print()

print("# Ręczne wywołanie iteratora:")
iterator = iter(lista)
while True: # Pętla nieskończona
    try: # Pobierz kolejny element:
        res=next(iterator)
        print (res, end= " ") # W tym miejscu przetwarzamy wartość "wyłuskaną" z kolekcji
    except StopIteration:
        break