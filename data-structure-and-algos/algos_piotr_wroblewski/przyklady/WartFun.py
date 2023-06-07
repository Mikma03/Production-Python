epsilon=0.00000001

def wart(x, yn):
	yn1=2*yn-x*yn*yn
	if abs(yn-yn1) < epsilon:
		return yn1
	else:
		return wart(x,yn1)
# Testujemy:
print("Wartość funkcji y=1/x dla x=7 wynosi ", wart(7,0.1) ) # Wynik: 0.14285714285714285
