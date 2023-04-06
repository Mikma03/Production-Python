class TabInt:	# Klasa zarządzająca umowną tablicą używana w rozdziale "Algorytmy sortowania"
	def __init__(self, pNMAX):
		self.t = [None] * pNMAX	# Wstępna inicjacja listy pełniącej rolę tablicy
		self.rozmiar=pNMAX	    # Maksymalny rozmiar tablicy danych
		self.licznik=0		    # Faktyczny rozmiar tablicy danych

	def __len__(self):
		return self.licznik

	def wstaw(self, x):	# Dodaj nowy element do tablicy
		if self.licznik < self.rozmiar:
			self.t[self.licznik] = x
			self.licznik=self.licznik+1
		else:
			print("[Błąd] Brak miejsca w tablicy dla elementu:", x)

	def wypisz(self):	# Wypisz zawartość tablicy
		print("[", end=" ")
		for i in range (0, self.licznik):
			print(f"{self.t[i]} ", end=" ")
		print("]")

	# ALGORYTMY SORTOWANIA

	def insertSort(self):	# Algorytm sortowania przez wstawianie
		for i in range (1, self.rozmiar):
			j=i	# Fragment [0..., i–1] jest już posortowany
			temp=self.t[j]
			while (j>0) and (self.t[j-1]>temp):
				self.t[j] = self.t[j-1]
				j=j-1
			self.t[j]=temp

	def bubble(self):
		for i in range(1, self.rozmiar):
			for j in range(self.rozmiar - 1, i - 1, -1):  # Od j=rozmiar-1 do i (pętla wsteczna)
				if self.t[j] < self.t[j - 1]:  # Zamiana, gdy następny jest większy
					tmp = self.t[j - 1]
					self.t[j - 1] = self.t[j]
					self.t[j] = tmp
		# self.wypisz() # Odblokuj, aby sprawdzić zawartość tablicy na danym etapie sortowania

	def ShakerSort(self):	# Algorytm sortowania przez wytrząsanie
		left=1
		right=self.rozmiar-1
		k=self.rozmiar-1
		while True:
			for j in range(right, left - 1, -1):  # Od j=right do left (pętla wsteczna)
				if self.t[j-1] > self.t[j]:
					temp=self.t[j-1]
					self.t[j-1]=self.t[j]
					self.t[j]=temp		# Zamiana t[j-1] i t[j]
					k=j
			left=k+1
			for j in range(left, right+1):
				if self.t[j-1] > self.t[j]:
					temp=self.t[j-1]
					self.t[j-1]=self.t[j]
					self.t[j]=temp		# Zamiana t[j-1] i t[j]
					k=j
			right=k-1
			if left>right:
				break

	def QuickSort(self, left, right): # Algorytm sortowania QuickSort
		if (left < right):
			m=left
			for i in range(left+1, right+1):
				if self.t[i] < self.t[left]:
					m=m+1				# Zamiana komórek tablicy t[++m] oraz t[i]
					temp=self.t[m]
					self.t[m]=self.t[i]
					self.t[i]=temp

			temp=self.t[left]		# Zamiana komórek tablicy t[left] oraz t[m]
			self.t[left]=self.t[m]
			self. t[m]=temp
			self.QuickSort(left, m-1)
			self.QuickSort(m+1, right)

# Próba bezpośredniego wywołania modułu
if __name__ == "__main__":
    print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "BSTMain.py!")
