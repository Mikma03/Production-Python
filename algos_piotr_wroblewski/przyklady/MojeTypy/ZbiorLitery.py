# --------------------------------------------------------------------------------------------------------------
# Funkcja pomocnicza
def do_indeksu(c):  # Konwersja znaku 'c' na wartość 0... 25 dla liter z zakresu A... Z
	if ((c >= 'A') and (c <= 'Z') or (c >= 'a') and (c <= 'z')):
		return ord(c.upper()) -ord('A')	# Zamiana na dużą literę realizowana przez metodę upper(), kod 'A' to 65
	else:
		return -1  # Błąd zakresu (znak spoza alfabetu)
# --------------------------------------------------------------------------------------------------------------
class ZbiorLitery: # Przykładowa implementacja klasy 'ZbiorLitery' (zbiór liter z zakresu A... Z)
	def __init__(self):
		self.zbior=[False for x in range (26)]

	def __add__(self, x2):  # Ta metoda zwraca obiekt będący sumą dwóch zbiorów
		suma = ZbiorLitery()  # operacji x1+x2, gdzie x1 jest bieżącym obiektem (self)
		for i in range (26):
			suma.zbior[i]= self.zbior[i] or x2.zbior[i]
		return suma
	# ---------------------------------------------------------------------------------
	def dodaj(self, c):	# Dodaj znak 'c' do zbioru
		i = do_indeksu(c)
		if i in range(26):
			self.zbior[i]=True
		else:
			print("[Błąd] Znak spoza dozwolonego alfabetu:", c, i)
	# ---------------------------------------------------------------------------------
	def nalezy(self, c):	# Czy 'c' należy do zbioru?
		i= do_indeksu(c)
		if (i!=-1):
			return	self.zbior[i]
		else:
			return False
	# ---------------------------------------------------------------------------------
	def usun(self, c):	# Usuń znak 'c' ze zbioru
		i= do_indeksu(c)
		print("Usuwam", c.upper())
		if  i != -1 and self.zbior[i]==True:
			self.zbior[i]=False
		else:
			print(f"\n[Błąd] Znak nie należy do zbioru:", c)
	# ---------------------------------------------------------------------------------
	def wypisz(self,s):	# Wypisuje zawartość zbioru
		print(s,"= {", end=" ")
		for i in range(26):
			if self.zbior[i] == True:  # Wypisz obecne element
				print( chr(i+65) + " ", end= " ")	#  konwersja indeksu 0... 25 na znaki A... Z
		print("}\n")
	# ---------------------------------------------------------------------------------


# Proba bezpośredniego wywołania modułu
if __name__ == "__main__":
	print("To jest moduł biblioteczny, aby przetestować wywołaj plik:", "ZbiorMain.py!")
