import math

def czyPierwsza (a):
    if (a<2):
        return False    # Fałsz
    for i in range (2, int(math.sqrt(a))+1):  # Funkcja sqrt() zwraca pierwiastek kwadratowy
        if (a % i == 0):                      # Funkcja modulo (reszta z dzielenia liczb całkowitych)
            return False
    return True;        # Prawda


def sito(n):
    tp = [True] * (n + 1)
    i = 2
    while i*i <= n:
        if (tp[i] == True):
            for k in range(i * i, n + 1, i): # Oznaczamy wielokrotności i jako liczby niepierwsze
                tp[k] = False
        i = i + 1
    return tp

print("Metoda klasyczna")
for i in range(1, 100):
    if (czyPierwsza(i)==True):
        print(i,  end=" ")
print("\nMetoda SITA Eratostenesa")
wyniki = sito(100)

for i in range(2, 100):
    if wyniki[i]:
        print(i, end=" ")

