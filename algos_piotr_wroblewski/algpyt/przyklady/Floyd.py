from MojeTypy import GrafTabl as gt
N=7
G =  gt.GrafTabl(N, "G")
G.initFloyd()   # Inicjacja na użytek algorytmu Floyda - 100000 nie oznacza brak krawędzi (nieskończony koszt przejścia)
G.zerujR()      # Zwykłe zerowanie macierzy R
# Tutaj wpiszmy definicje węzłów i koszty przejścia między nimi:
G.add(0, 3, 30), G.add(0, 1, 10), G.add(1, 2, 15), G.add(1, 4, 40), G.add(2, 3, 5)
G.add(2, 4, 20), G.add(4, 5, 20), G.add(4, 6, 10), G.add(5, 6, 5), G.add(6, 3, 25)
G.wypisz()
G.floydRoute()  # Wywołuje algorytm Floyda w wersji 2
for i in range(N):
    for j in range(N):
        if G.get(i, j) == 100000:
            print(f"{i}-->{j} [drogi nie ma]")
        else:
            if i!=j:
                print(f"{i}-->{j} koszt={G.get(i, j)}. Droga przez: ", end = "")
                G.drogaFloyd(i,j)
                print()

	
