tabl=[1,2,6,18,20,23,29,32,34,39,40,41]

def binary_search (tab, x, left, right):
    if (left==right):
        if (tab[left]==x):
            return left
        else:              # Element znaleziony
            return -1      # Element nieodnaleziony
    else:
       mid=(left+right) // 2
       if (tab[mid]==x):
            return mid       # Element znaleziony!
       else:
            if (x<tab[mid]):
                return binary_search(tab, x, left, mid)
            else:
                return binary_search(tab, x, mid+1, right)
# Przetestujmy algorytm:
print ("Tablica:", tabl)
print("Wynik poszukiwania liczby 23: ", binary_search(tabl, 23, 0, len(tabl)) ) # len() zwraca rozmiar tablicy
print("Wynik poszukiwania liczby  3: ", binary_search(tabl, 3,0,   len(tabl)) )

