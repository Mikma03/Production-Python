#  Deklarowanie tablic wielowymiarowych w Pythonie:
#  https://docs.python.org/3/faq/programming.html#how-do-i-create-a-multidimensional-list

class GrafTabl:
    def __init__(self, N, opis):
        self.N = N
        self.opis = opis
        self.G = [0] * N   # G - graf zamodelowany przy pomocy tablicy [N][N]
        self.R = [0] * N   # R - Matryca kierowania ruchem zamodelowana przy pomocy tablicy [N][N]
        for i in range(N): # Inicjalizacja drugiego wymiaru tablic [N][N]:
            self.G[i] = [0] * N  #
            self.R[i] = [0] * N

        self.V = [0] * N  # Tablica o rozmiarze [N] przechowująca na użytek algorytmu przeszukiwania DFS
        #  informację czy wierzchołek był już badany (wartość: 1), czy nie (wartość: 0)

    def zeruj(self):
        for i in range(self.N):
            for j in range(self.N):
                self.G[i][j] = 0  # Konwencja: 0=brak krawędzi

    def add(self, i, j, val):  # Dopisz węzeł
        if i < self.N and j < self.N:
            self.G[i][j] = val
        else:
            print("Indeks(y) poza zakresem tablicy: " + i + "!")

    def get(self, i, j):  # Zwróć wartość węzła
        if i < self.N and j < self.N:
            return self.G[i][j]
        else:
            return None  # Umowny błąd

    def wypisz (self):  # Wypisz graf G
        print("Graf: " + self.opis)
        for i in range(self.N):
            for j in range(self.N):
                if self.G[i][j] != 100000:   # 100000 niech oznacza brak krawędzi (nieskończony koszt przejścia)
                    print(f"{self.G[i][j]:3}", end=" ")
                else:
                    print(" - ", end=" ")
            print()
        print()

    def zeruj(self):
        for i in range(self.N):
            for j in range(self.N):
                self.G[i][j] = 0    #  Konwencja: 0=brak krawędzi

    def kompozycja(self, G1, G2):   # Ten graf G stanie się kompozycją dwóch innych: G1 i G2
        self.zeruj()
        for x in range(self.N):
            for y in range(self.N):
                z=0
                while True: # Pętla nieskończona
                    if z==self.N:
                        break # Wyjście z pętli
                    if G1.get(x, z)==1 and G2.get(z, y)==1:
                            self.G[x][y]=1
                    z=z+1

    def warshall(self):  # Wykonuje algorym Warshalla na grafie G
        """ Graf musi być odpowiednio zainicjowany: G[x, y] = 0, jeśli nie istnieje krawędź (x, y),
    	                                           G[x, y] = 1 w przeciwnym wypadku"""
        for x in range(self.N):
            for y in range(self.N):
                for z in range(self.N):
                    if self.G[y][z] == 0:
                        self.G[y][z] = self.G[y][x] * self.G[x][z]
    def wypiszDroge(self, x, y):
        # Wypisz drogę od wierzchołka x do y dzięki informacjom zawartym w macierzy kierowania ruchem R
        if self.R[x][y]==0:
            print("Droga nie istnieje")
        else:
            k=self.R[x][y]
            print(k,  "  ", end=" ")
            while k!=y:
                k=self.R[k][y]
                print(k,  "  ", end=" ")
            print()

    def wypiszR (self): # Wypisz macierz kierowania ruchem R
        print("Macierz kierowania ruchem grafu " + self.opis)
        for i in range(self.N):
                for j in range(self.N):
                        print(f"{self.R[i][j]:3}   ", end=" ")
                print()
        print()



    def initFloyd(self):
        # Inicjacja na użytek algorytmu Floyda "100000" oznacza brak krawędzi (nieskończony koszt przejścia)
        for i in range(self.N):
            for j in range(self.N):
                self.G[i][j]=100000


    def floyd(self):    # Najprostsza forma algorytmu Floyda, która oblicza wartość optymalnej drogi, ale jej nie zapamiętuje
        for k in range(self.N):
            for i in range(self.N):
                for j in range(self.N):
                    self.G[i][j]=min( self.G[i][j], self.G[i][k] + self.G[k][j] )

    def floydRoute(self): # Algorytm Floyda, który oblicza wartość optymalnej drogi i zapamiętuje ją w macierzy kierowania ruchem R
        for k in range(self.N):
            for i in range(self.N):
                for j in range(self.N):
                    if self.G[i][k]+self.G[k][j] < self.G[i][j]:
                        self.G[i][j]=self.G[i][k]+self.G[k][j]
                        self.R[i][j]=k  # Zapamiętaj drogę

    def drogaFloyd(self, i, j): # Procedura odtwarza drogę zapisaną w R (efekt zastosowania algorytmu Floyda — metoda floydRoute)
        k = self.R[i][j]
        if k != 0:
            self.drogaFloyd(i, k)
            print (f"{k}  ", end="")
            self.drogaFloyd(k, j)

    def initR(self):    # Tworzy z grafu G macierz kierowania ruchem R
        # R[x, y] = 0 jeśli w G nie istnieje krawędź (x, y), R[x, y] = y w przeciwnym wypadku
        for x in range(self.N):
            for y in range(self.N):
                if self.G[x][y]==0:
                    self.R[x][y]=0
                else:
                    self.R[x][y]=y

    def zerujR(self):   # Zwykłe zerowanie macierzy R
        for x in range(self.N):
            for y in range(self.N):
                self.R[x][y]=0   # Umowny brak drogi

    def budujSciezki(self): # Zbuduj ścieżki dojścia pomiędzy węzłami
        for x in range(self.N):
            for y in range(self.N):
                if self.R[y][x]!=0: # Wiemy, jak dojść z 'y' do 'x'
                    for z in range(self.N):
                        if self.R[y][z]==0 and self.R[x][z]!=0:
                            self.R[y][z] = self.R[y][x]



#-------------------------------------------------------------
# Strategia "w głąb" (ang. depth-first search)
# -------------------------------------------------------------
    def zwiedzajDFS (self, i):
        # Tablica V[N] przechowuje na użytek algorytmu przeszukiwania DFS informację, czy dany
        # wierzchołek był już badany (wartość: 1), czy nie (wartość: 0)
        self.V[i]=1 # Zaznaczamy wierzchołek jako "zbadany"
        print("Badam wierzchołek: ", i)
        for k in range(self.N):
            if self.G[i][k]!=0: # Istnieje przejście
                if self.V[k]==0:
                    self.zwiedzajDFS(k)

    def szukajDFS(self):
        for i in range(self.N):
            self.V[i]=0 # Oznaczmy wierzchołek jako "niezbadany"
        for i in range(self.N):
            if self.V[i]==0:
                self.zwiedzajDFS(i)
