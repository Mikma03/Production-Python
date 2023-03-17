from MojeTypy import TabInt as t
# ----------------------------------------------------------------------------
# Przykłady użycia algorytmu sortowania przez wstawianie

tab = t.TabInt(12)
for element in [40, 2, 1, 6, 18, 20, 29, 32, 23, 34, 39, 41]:
	tab.wstaw(element)
tab.wstaw(100)	# Zobaczymy komunikat: „[BŁĄD] Brak miejsca w tablicy dla 100”
tab.wypisz()
#tab.insertSort()
#tab.bubble()
#tab.ShakerSort()
#tab.QuickSort(0, len(tab)-1)
tab.wypisz()