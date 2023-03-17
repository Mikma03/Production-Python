class StosOgraniczony:
    def __init__(self, pRozmiar):
        self._stos = list()         # Właściwa kolekcja danych
        self._MaxElt=pRozmiar        # Maksymalny rozmiar stosu

    def zeruj(self):   # Zerowanie stosu
        self._stos.clear()

    def wypisz(self, s):
        print(s)
        if self._stos!=None:
            print(" Zawartość stosu: [", end=" ")
            for x in self._stos:    # Wywołajmy iterator klasy list()
                print(x, end=" ")
            print("]")

    def push(self, obj):
      print("Odkładam: ", str(obj))   # Konwersja do postaci tekstowej
      if len(self._stos) < self._MaxElt:
        self._stos.append(obj)        # Dokładamy kolejny element na koniec
      else:
        print("* POJEMNOŚĆ PRZEKROCZONA *")

    def pop(self):
        if len(self._stos_)>0:
          tmp=self._stos.pop()  # Pobiera ostatni element
        return tmp  # Usuwamy ze stosu ale nie tracimy dostępu do elementu usuwanego

    def rozmiar():    # Zwraca stan zajętości stosu
        return stos.size()

    def pojemnosc():  # Zwraca pojemność stosu
	    return self._MaxElt


# Proba bezpośredniego wywołania modułu
if __name__ == "__main__":
	print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "StosMain.py!")
