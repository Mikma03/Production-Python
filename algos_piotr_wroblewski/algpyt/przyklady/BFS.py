from MojeTypy import GrafTabl as gt
from MojeTypy import FIFO as f

def szukaj(G, i, N):    # Rozpoczynamy od wierzchołka 'i'
    kolejka=f.FIFO(N)
    V= [0] * N  # Tablica N-elementowa
    for z in range(N):
        V[z]=0  # Wierzchołek nie był jeszcze badany
    kolejka.wstaw(i)
    while not kolejka.pusta():
        s=kolejka.obsluz()     # Bierzemy z kolejki pewien wierzchołek 's'
        print("Obsługujemy: ", s)
        V[s]=1  # Zaznaczamy wierzchołek 's' jako „badany”
        for k in range(N):
            if G.get(s, k) !=0: # Istnieje przejście
                if V[k]==0:     # k' nie był jeszcze badany
                    V[k]=1      # Zaznaczamy wierzchołek 'k' jako „badany”
                    kolejka.wstaw(k)

# ---------------------------------------------------------------------
# Testujemy algorytm przeszukiwania BFS

N=7
G = gt.GrafTabl(N, "G")
G.zeruj()
G.add(0, 3, 1), G.add(3, 0, 1), G.add(0, 4, 1), G.add(4, 0, 1), G.add(0, 1, 1)
G.add(1, 0, 1), G.add(1, 4, 1), G.add(4, 1, 1), G.add(1, 2, 1), G.add(2, 1, 1)
G.add(3, 6, 1), G.add(6, 3, 1), G.add(3, 4, 1), G.add(4, 3, 1)
G.add(4, 5, 1), G.add(5, 4, 1), G.add(2, 6, 1), G.add(6, 2, 1)
G.wypisz()
szukaj(G, 0, N)

"""
Graf: G
  0   1   0   1   1   0   0 
  1   0   1   0   1   0   0 
  0   1   0   0   0   0   1 
  1   0   0   0   1   0   1 
  1   1   0   1   0   1   0 
  0   0   0   0   1   0   0 
  0   0   1   1   0   0   0 

Tworzę kolejkę o pojemności 7

Obsługujemy:  0
Obsługujemy:  1
Obsługujemy:  3
Obsługujemy:  4
Obsługujemy:  2
Obsługujemy:  6
Obsługujemy:  5
"""