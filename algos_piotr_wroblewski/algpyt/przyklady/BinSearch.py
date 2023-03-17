tabl=[1,2,6,18,20,23,29,32,34,39,40,41]

def szukaj_rec(tab, x, left, right):
    if(left>right):
        return -1; # Element nieznaleziony
    else:
        mid=(left+right) // 2 # Operator // zwraca część całkowitą z dzielenia
        if( tab[mid]==x ):
            return mid      # Element został znaleziony!
        else:
            if (x<tab[mid]): # Szukaj po lewej
                return szukaj_rec(tab,x,left,mid-1)
            else:           # Szukaj po prawej
                return szukaj_rec(tab,x,mid+1,right)
# Przetestujmy algorytm:
print ("Tablica:", tabl)
print("Wynik poszukiwania liczby 23: ", szukaj_rec(tabl, 23, 0, len(tabl)) ) # len() zwraca rozmiar tablicy
print("Wynik poszukiwania liczby  3: ", szukaj_rec(tabl, 3,0,   len(tabl)) )

