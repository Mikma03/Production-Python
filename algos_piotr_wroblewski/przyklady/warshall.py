from MojeTypy import GrafTabl as gt
G = gt.GrafTabl (5, "G")
G.add(0, 1, 1), G.add(0, 3, 1), G.add(1, 3, 1), G.add(2, 1, 1), G.add(3, 2, 1), G.add(4, 1, 1)
G.wypisz();
G.warshall()
print("Po wykonaniu algorytmu Warshalla:")
G.wypisz()
	
	
