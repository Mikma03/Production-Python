tabl = [1, 2, 3, 2, -7, 44, 5, 1, 0, -3]

def szukaj(tabl, left, right, x):
# x = wartość do odnalezienia, left i right = lewa i prawa granica obszaru poszukiwań
    if left > right:
        print("Element ", x, " nie został odnaleziony")
    else:
        if tabl[left] == x:
            print("Znaleziono poszukiwany element")
        else:
            szukaj(tabl, left+1, right, x)

# Sprawdzamy działanie funkcji:
print ("Tablica:", tabl)
szukaj(tabl, 0, len(tabl)-1, 7)
szukaj(tabl, 0, len(tabl)-1, 5)
