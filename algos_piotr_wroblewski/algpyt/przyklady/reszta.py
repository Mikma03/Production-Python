N = [100, 50, 20, 10, 5, 2, 1] # N - tablica nominałów

def reszta(r, N): 			# r-kwota reszty do wydania klientowi
	print("Kwota: ", r)
	i=0
	while r>0: # Wydawaj aż do końca
		if r >= N[i]:	# Czy nominał pasuje?
			x = r // N[i]   # Oblicz krotność
			r = r - x*N[i] 	# Reszta do wydania...
			print("Wydano ", x, " razy ", N[i])
		i=i+1			# Kolejny nominał
# Testujemy:
reszta(91, N)

"""
Kwota:  91
Wydano  1  razy  50
Wydano  2  razy  20
Wydano  1  razy  1
"""
