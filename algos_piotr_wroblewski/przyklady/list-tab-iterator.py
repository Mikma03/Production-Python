class Fiszka:                   # Element składowy listy danych (rekord informacyjny)
    def __init__(self, pNazwisko="", pWiek=0):
        self.nazwisko = pNazwisko
        self.wiek = pWiek
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
class ListaTab:                 # Realizacja listy-tablicy elementów typu 'Fiszka'
    def __init__(self, MaxTab):
        self.tab= [ Fiszka() for x in range(MaxTab)]   # Tworzy "statyczną" tablicę o rozmiarze MaxTab
        self.Licznik = 0    # Liczba wpisów na początku to 0
        self.Rozmiar=MaxTab     # Zapamiętajmy maksymalny rozmiar

    # --------------------------------------------------------------------
    def WstawNaKoniec(self, pNazwisko, pWiek): # Wstawiamy na koniec listy
        if self.Licznik < self.Rozmiar:
            nowy = Fiszka(pNazwisko, pWiek)
            self.tab[self.Licznik]=nowy
            self.Licznik=self.Licznik+1
        else:
            print(f"Tablica pełna, nie wstawiono: ({pNazwisko}{pWiek})!")
    # --------------------------------------------------------------------
    def WstawNaPozycje(self, pNazwisko, pWiek, k): # Wstawiamy na k-tą pozycje listy bieżącej listy
        if (self.Licznik == self.Rozmiar) or ( k not in range(0, self.Licznik) ):
            print(f"-- Tablica pełna/błędny indeks: nie wstawiono: ({pNazwisko}{pWiek})")
            return
        nowy = Fiszka(pNazwisko, pWiek)            # Nowy element danych
        for i in range(self.Licznik, k, -1):
            self.tab[i]=self.tab[i-1] # Robimy miejsce
        self.tab[k]=nowy    # Wstaw nowy obiekt do listy
        self.Licznik=self.Licznik+1 # Lista ma teraz jeden element więcej
    # --------------------------------------------------------------------
    def wypisz(self,s ):
        print(s)
        for i in range(0, self.Licznik):
            print("[",  self.tab[i].nazwisko, ",", self.tab[i].wiek, "]", end=" ")
        print()
    # --------------------------------------------------------------------
    def szukaj(self, pNazwisko):
        for i in range (0, self.Licznik):
            if (self.tab[i].nazwisko == pNazwisko):
                return i
        return -1  # Ujemny indeks niech oznacza brak rekordu
    # --------------------------------------------------------------------
    def usunOsobe(self, pNazwisko):
        k = self.szukaj(pNazwisko)
        if k >= 0:
            for i in range (k, self.Licznik-1 ):
                self.tab[i]=self.tab[i+1]
                #print("SHIFTING")
            self.Licznik = self.Licznik - 1  # Lista ma teraz jeden element mniej
            print(f"Usunięcie [{pNazwisko}] powiodło się")
        else:
            print(f"Usunięcie [{pNazwisko}] NIE powiodło się")

    def __iter__(self):
        #self.x = 10
        return self
    pass

    def __next__(self):
        pass
        # Store current value ofx
        #x = self.x
        #if x > self.limit:
        #   raise StopIteration

        # Else increment and return old value
        #self.x = x + 1;
        #return x
# --- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Przykładowe użycie:

t=ListaTab(4)
t.WstawNaKoniec("1-Kowalski", 30), t.WstawNaKoniec("2-Kowalska", 28)
t.WstawNaKoniec("3-Nowak", 35),    t.WstawNaKoniec("4-Pankracy", 45)
t.WstawNaKoniec("5-Nadmiarowy", 5)
t.wypisz("Lista finalna:")
t.wypisz("Próba wstawienia rekordu '*Newton*' na trzecią pozycję")
t.WstawNaPozycje("*Newton*", 378, 2)
t.usunOsobe("Nie ma mnie")
t.usunOsobe("3-Nowak")
t.wypisz("Po usunięciu rekordu '3-Nowak'")
t.wypisz("Próbie wstawienia rekordu '*Newton*' na drugą pozycję")
t.WstawNaPozycje("*Newton*", 378, 1)
t.wypisz("Lista finalna")



