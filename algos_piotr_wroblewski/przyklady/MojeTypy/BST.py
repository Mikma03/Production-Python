# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
class Wezel:
    def __init__(self, pKlucz=None):
        self.klucz = pKlucz  # Tutaj zapamiętamy klucz
        # tutaj może dołożyć inne atrybuty (dane biznesowe)
        self.lewy = None  # Lewy potomek
        self.prawy = None  # Prawy potomek
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
class BST:               # Binarne drzewo poszukiwań – klasa może być dalej rozwijana
    def __init__(self):  # przy ukryciu detali realizacji klasy i służąc jako interfejs dostępowy do węzłów danych
        # tu ew. inne meta-atrybuty
        self.korzen = None  # Korzeń główny drzewa BST

    # ----------------------------------------------------------------------------
    def wstaw(self, k):  # Wersja iteracyjna wstawiania węzła do drzewa BST
        w = Wezel(k)  # Tworzymy nowy węzeł i szukamy miejsca ma wstawienie
        if self.korzen == None:  # Jakoś pusto tutaj (na razie!)
            self.korzen = w
        else:  # Coś tam jest, zatem szukamy aż do końca świata i jeden dzień dłużej!
            tmp = self.korzen
            while True:  # Z pętli wyjdziemy po wstawieniu elementu (*)
                rodzic = tmp
                if k < tmp.klucz:  # Na lewo
                    tmp = tmp.lewy
                    if tmp == None:  # Jeśli koniec ścieżki, to wstaw na lewo
                        rodzic.lewy = w
                        break
                else:  # Kierujemy się na prawo
                    tmp = tmp.prawy
                    if tmp == None:  # Jeśli koniec ścieżki, to wstaw na prawo
                        rodzic.prawy = w
                        break
            # Koniec pętli oznaczonej (*)
    # ----------------------------------------------------------------------------
    def preOrder(self, w):  # przejście "wzdłużne"
        if w != None:
            print("[", w.klucz, "]", end=" ")
            self.preOrder(w.lewy)
            self.preOrder(w.prawy)

    def inOrder(self, w):  # Przejście "poprzeczne"
        if w != None:
            self.inOrder(w.lewy)
            print("[", w.klucz, "]", end=" ")
            self.inOrder(w.prawy)

    def postOrder(self, w):  # Przejście "wsteczne"
        if w != None:
            self.postOrder(w.lewy)
            self.postOrder(w.prawy)
            print("[", w.klucz, "]", end=" ")
    # ----------------------------------------------------------------------------
    def szukaj(self, x):  # Zwraca węzeł o kluczu 'x' lub None
        if self.korzen == None:
            return None
        tmp = self.korzen
        while tmp.klucz != x:
            if x < tmp.klucz:  # Kieruj się na lewo
                tmp = tmp.lewy
            else:  # Kieruj się na prawo
                tmp = tmp.prawy
            if tmp == None:  # Brak potomka
                return None
        return tmp  # Znaleziono
    # ----------------------------------------------------------------------------
    def Min(self, start):  # Odszukaj i zwróć węzeł o najmniejszej wartości klucza
        #tmp = self.korzen
        tmp=start
        while tmp.lewy != None:  # Idź w lewo, aż do końca
            tmp = tmp.lewy
        return tmp

    def Max(self, start):  # Odszukaj i zwróć  węzeł o największej wartości klucza
        #tmp = self.korzen
        tmp = start
        while tmp.prawy != None:  # Idź w prawo, aż do końca
            tmp = tmp.prawy
        return tmp

# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Funkcje zdefiniowane poza ciałem klasy BST
def MinWezel(start):    # Zwraca  wezeł o min. wartości klucza w drzewie (poddrzewie) 'start'
    tmp = start
    while (tmp.lewy != None): # Idziemy skrajnie na lewo!
        tmp = tmp.lewy
    return tmp
# ----------------------------------------------------------------------------
def usunWezel(wierzcholek, klucz):  # Startujemy od węzła 'wierzcholek'
    if wierzcholek == None:
        return wierzcholek
    if klucz < wierzcholek.klucz:           # Idziemy na lewo
        wierzcholek.lewy = usunWezel(wierzcholek.lewy, klucz)
    elif (klucz > wierzcholek.klucz):       # Idziemy na prawo
        wierzcholek.prawy = usunWezel(wierzcholek.prawy, klucz)
    else:  # Usuwamy znaleziony wierzchołek
        if wierzcholek.lewy == None:    # Wierzchołek z tylko jednym potomkiem
            temp = wierzcholek.prawy
            return temp
        elif wierzcholek.prawy == None:
            temp = wierzcholek.lewy
            return temp
        # Wierzchołek z dwoma potomkami
        temp = MinWezel(wierzcholek.prawy) # Szukamy następcy kasowanego węzła, który znajduje się w prawej gałęzi
        wierzcholek.klucz = temp.klucz     # Kopiujemy zawartość następnika w miejsce usuwanego węzła (klucz i ew. inne atrybuty)
        wierzcholek.prawy = usunWezel(wierzcholek.prawy, temp.klucz)  # Usuwamy następnika z podgałęzi
    return wierzcholek
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Próba bezpośredniego wywołania modułu
if __name__ == "__main__":
    print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "BSTMain.py!")
