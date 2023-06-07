from MojeTypy import FIFO as f

kolejka = f.FIFO(4)
kolejka.wstaw("Kowalska"), kolejka.wstaw("Fronczak"), kolejka.wstaw("Becki"), kolejka.wstaw("Pigwa")
kolejka.wstaw("Cwaniak"), kolejka.wstaw("Spóźnialski")	  # Te dwie operacje już się nie powiodą!
kolejka.wypisz("1-Stan kolejki")

szczesliwiec=kolejka.obsluz()
print("Obsłużony został klient: " + str(szczesliwiec))
kolejka.wypisz("2-Stan kolejki")

print("Przyszedł Pan 'Spóźnialski'")
kolejka.wstaw("Spóźnialski")
kolejka.wypisz("3-Stan kolejki")

print("Ekspresowa obsługa całej kolejki przed zamknięciem sklepu!")

while not kolejka.pusta():
	k=kolejka.obsluz()
	print("Obsłużony został klient: " + str(k))
print("Kolejka pusta, zamykamy sklep!")
