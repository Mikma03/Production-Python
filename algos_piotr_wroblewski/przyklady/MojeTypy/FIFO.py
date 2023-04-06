class FIFO:	# Kolejka
	def __init__(self, pRozmiar):
		self._kolejka = list()  # Właściwa kolekcja danych
		self._MaxElt = pRozmiar # Maksymalny rozmiar kolejki
		self._licznik=0		    #   Bieżąca liczba elementów
		print("Tworzę kolejkę o pojemności " + str(self._MaxElt) )

	def wstaw(self, obj):		# Dołóż tu kontrolę poprawności operacji, kontrolę typu
		if self._licznik < self._MaxElt:	# Jest miejsce
			self._kolejka.append(obj)		# Dołóż element NA KONIEC
			self._licznik=self._licznik+1
		else:
			print(f"* Gdzie się Pan {obj} wpycha? Tu obowiązuje lista kolejkowa! *")

	def obsluz(self):
		if self._licznik != 0:		# "Ktoś" stoi jest w kolejce...
			temp = self._kolejka.pop(0)	#	Pobierz wartość Z PRZODU
			self._licznik = self._licznik - 1
			return temp
		else:
			print("** Kolejka pusta **")

	def wypisz(self, s):
		print(s)
		if self._licznik != 0:
			print(" Zawartość kolejki:[", end=" ")
			for x in self._kolejka:  # Wywołajmy iterator klasy list()
				print(x, end=" ")
			print("]")

	def pusta(self):	# Czy kolejka jest pusta?
		return self._licznik==0


# Proba bezpośredniego wywołania modułu
if __name__ == "__main__":
	print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "kolejkaMain.py!")
