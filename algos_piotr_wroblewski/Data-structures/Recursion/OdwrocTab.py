tabl=[1, 2, 3, 4, 5, 6, 7, 8]

def odwroc(tab, left, right):
    if(left<right):
        tab[left], tab[right] = tab[right], tab[left]   # Zmieniamy elementy skrajne
        odwroc(tab, left+1, right-1); 	                # Odwracamy reszte

print("Tablica=", tabl)         # Wypisze:  [1, 2, 3, 4, 5, 6, 7, 8]
odwroc(tabl, 0, len(tabl)-1 )
print("Tablica=", tabl)         # Wypisze:  [8, 7, 6, 5, 4, 3, 2, 1]
