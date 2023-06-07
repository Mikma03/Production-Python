class Sterta:
    def __init__(self, nMax):  # Sterta będzie zawierała liczby całkowite (priorytety)
                                # Ewentualne obiekty złożone, zawierające pewne atrybuty + pole 'priorytet'
                                # można łatwo zaimplementować osobno, jako strukturę skojarzoną (słownik)

        self._Licznik = 0                         # Liczba elementów
        self._sterta=[0 for x in range(nMax+1)]   # Tworzymy statyczną tablicę o rozmiarze nMax+1

    def DoGory(self):
        tmp = self._sterta[self._Licznik]
        n = self._Licznik
        while ((n != 1) and (self._sterta[n // 2] <= tmp)): # Operator // realizuje dzielenie całkowite
            self._sterta[n] = self._sterta[n // 2]
            n = n // 2
        self._sterta[n] = tmp

    def wstaw(self, x):
        self._Licznik=self._Licznik+1
        self._sterta[self._Licznik] = x
        self.DoGory()

    def obsluz(self):
        x=self._sterta[1]
        self._sterta[1]=self._sterta[self._Licznik]
        self._Licznik=self._Licznik-1
        self.NaDol()
        return x

    def NaDol(self):
        i=1
        while(True):
            p=2*i   # Lewy potomek węzła 'i' to (p), prawy to (p+1)
            if p>self._Licznik:
                break
            if p+1 <= self._Licznik:   # Prawy potomek niekoniecznie musi istnieć!
                if self._sterta[p] < self._sterta[p+1]:
                    p=p+1      # Przesuwamy się do następnego
            if self._sterta[i] >= self._sterta[p]:
                break
            tmp=self._sterta[p]   # Zamiana
            self._sterta[p]=self._sterta[i]
            self._sterta[i]=tmp
            i=p

    def wypisz(self, s):
        print(s)
        for i in range(1, (self._Licznik // 2) +1):
            print(" Wierzchołek: "+ str(self._sterta[i]), end=" ")
            print(" lewy potomek: " + str(self._sterta[2*i]), end=" ")
            # Prawy potomek niekoniecznie musi istnieć!
            if 2 * i +1 <= self._Licznik:
                print(" prawy potomek: " + str(self._sterta[2*i+1]) , end=" ")
            print()

# Próba bezpośredniego wywołania modułu
if __name__ == "__main__":
   print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "StertaMain.py!")

