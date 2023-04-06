tabl=[1, 2, 3, 2, -7, 44, 5, 1, 0, -3]

def szukaj(tab, x):
    n=len(tab)
    pos=0
    while ((pos<n) and (tab[pos]!=x)):
        pos=pos+1
    if(pos < n):
       return pos # Element znaleziony
    else:
       return -1	# Porażka poszukiwań

# Sprawdzamy działanie funkcji:
print ("Tablica:", tabl)
print(" Szukamy 7, wynik", szukaj(tabl, 7) )
print(" Szukamy 5, wynik", szukaj(tabl, 5) )





