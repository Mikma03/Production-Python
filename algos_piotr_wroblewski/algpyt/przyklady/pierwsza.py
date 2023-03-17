import math

def czyPierwsza (a):
    if (a<2):
        return False    # Fałsz
    for i in range (2, int(math.sqrt(a))+1):  # Funkcja sqrt() zwraca pierwiastek kwadratowy
        if (a % i == 0):                      # Funkcja modulo (reszta z dzielenia liczb całkowitych)
            return False
    return True        # Prawda

for i in range (2, 100):
    if (czyPierwsza(i) ):
        print(i, end=" ")
