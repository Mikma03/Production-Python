from MojeTypy import GrafTabl as gt

N=7

G=gt.GrafTabl (N, "G")
G.zeruj()
G.add(0, 3, 1), G.add(3, 0, 1), G.add(0, 4, 1), G.add(4, 0, 1), G.add(0, 1, 1), G.add(1, 0, 1)
G.add(1, 4, 1), G.add(4, 1, 1), G.add(1, 2, 1), G.add(2, 1, 1), G.add(3, 6, 1), G.add(6, 3, 1)
G.add(3, 4, 1), G.add(4, 3, 1), G.add(4, 5, 1), G.add(5, 4, 1), G.add(2, 6, 1), G.add(6, 2, 1)
G.wypisz()
G.szukajDFS()

	
	
	
