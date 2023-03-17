from MojeTypy import GrafTabl as gt
G =  gt.GrafTabl(6, "G")
G.add(0, 3, 1), G.add(0, 5, 1), G.add(1, 2, 1), G.add(2, 4, 1)
G.add(3, 1, 1), G.add(3, 4, 1), G.add(5, 4, 1), G.add(4, 5, 1), G.add(5, 2, 1)
G.wypisz()
G.initR()
print("WARSHALL")
G.warshall()
G.wypisz()
print("Wstępna inicjacja macierzy R na podstawie G")
G.wypiszR()
G.budujSciezki()
G.wypiszR()
for i in range(6):
	for j in range(6):
		print("Droga od wierzchołka ", i, " do ", j,  ": ", end=" ")
		G.wypiszDroge(i,j)
