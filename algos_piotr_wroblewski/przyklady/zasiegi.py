wynik = 6
print ("wynik =",wynik)

def pi_razy_drzwi(pi, drzwi):
    global x
    x=5
    wynik = pi*drzwi
    print("wynik = ", wynik)


pi_razy_drzwi(3,4)

# print("x=", x)    # Zwróci błąd, x jest zmienną lokalną!

# Ilustracja użycia zmiennej globalnej w ciele funkcji:

v = int()  # Pusta deklarcja zmiennej globalnej typu int
def funkcyjka():
    global v # Poniżej odnosimy się do zmiennej globalnej v
    v=5
    print("Wywołanie w ciele funkcji o nazwie funkcyjka(),  v = ", x)

funkcyjka() # Wywołanie funkcji zmodyfikuje obiekt globalny przypisany do zmiennej v
v=v+1       # Kolejna modyfikacja zmiennej globalnej v, już poza ciałem funkcji
print("Instrukcja w skrypcie głównym, v = ", v)


