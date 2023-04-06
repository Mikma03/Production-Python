class Wyrazenie: 		# Drzewo binarne zapamiętujące wyrażenia arytmetyczne
	def __init__(self):
		self.val=0	    # Wartość (bez znaczenia w nowym obiekcie, będzie nadpisana)
		self.op='0'	    # Operator, niech wpis '0' tutaj  oznacza, że węzeł
		self.lewy=None	# przechowuje pewną wartość, a nie operator arytmetyczny (uwaga jw.)
		self.prawy=None	# lewy, prawy -potomkowie węzła pełniącego funkcję operatora

	def pisz_prefix(self): # Funkcja wypisuje wyrażenie w postaci prefiksowej
		if self.op=='0':	# Wartość liczbowa
			print( str(self.val), end=" ")
		else:
			print(self.op + " ", end=" ")
			self.lewy.pisz_prefix()
			self.prawy.pisz_prefix()

	def pisz_infix(self):	# Funkcja wypisuje wyrażenie w postaci infiksowej
		if self.op=='0':	# Wartość liczbowa...
			print( str(self.val), end=" ")
		else:
			print("(", end="")
			self.lewy.pisz_infix()
			print(self.op, end=" ")
			self.prawy.pisz_infix()
			print(")", end="")

	def poprawne(self):	# Czy wyrażenie jest poprawne składniowo?
		if self.op=='0':
			return True		# Według naszej konwencji jest to liczba, więc akceptujemy
		if self.op in ['+', '-', '*', ':', '/']:	# Sprawdzimy teraz operator, czy jest nam znany
			return (self.lewy).poprawne() and (self.prawy).poprawne()
		else:
			return False	# Błąd,  nieznany operator lub inny błąd
	def oblicz(self):
		if self.poprawne():	# Wyrażenie poprawne?
			if (self.op=='0'):
				return self.val	# Pojedyncza wartość
			elif self.op=='+':
					return (self.lewy).oblicz()+(self.prawy).oblicz()
			elif self.op=='-':
				return (self.lewy).oblicz()-(self.prawy).oblicz()
			elif self.op=='*':
				return (self.lewy).oblicz()*(self.prawy).oblicz()
			elif (self.op==':' or self.op=='/'):
				if (self.prawy).oblicz()!= 0:
					return (self.lewy).oblicz() / (self.prawy).oblicz()
				else:
					print("\nDzielenie przez zero!")
					return -1	# Uproszczona sygnalizacja błędów
		else:
			print("Błąd składni")
			return -1	# Uproszczona sygnalizacja błędów


wart = [2, 3, 0, 7, 9, 0, 0, 12.5, 0]
oper = ['0', '0', '+', '0', '0', '*', '+', '0'  ,'*']

s=list()	# Lista użyta jako stos roboczy przeznaczony do przechowywania obiektów klasy 'Wyrazenie'
w=None	# Puste wyrazenie

for i in range( len(wart) ):
	w=Wyrazenie()
	if oper[i] in ['+', '-', '*', ':', '/']:
		w.op=oper[i]
	else:
		w.op='0'	# Umowna konwencja oznaczająca wartość, a nie operator
		w.val=wart[i]
	w.lewy  = None
	w.prawy = None

	if oper[i] in ['+', '-', '*', ':', '/']:
		l1=Wyrazenie()
		p1=Wyrazenie()
		l1=s.pop()
		p1=s.pop()
		w.lewy =l1	# "Podwiązanie" pod węzeł x
		w.prawy=p1; # "Podwiązanie" pod węzeł x
	s.append(w)

print("Prefiks: ")
w.pisz_prefix();
print("\nWynik: " + str(w.oblicz()) )
print("Infiks: ")
w.pisz_infix()
