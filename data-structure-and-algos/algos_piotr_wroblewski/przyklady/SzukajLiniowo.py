def szukaj(tab, x): # Szukaj 'x' w tablicy
    if len(tab)==0:
        return len()
    i=0
    while i< len(tab):
        if tab[i]==x:   # (*)
            break
        else:
            i=i+1
    return i # Jeśli 'i' wyjdzie poza zakres tablicy, to nie znaleziono elementu
#-------------------
tab1= [1, 2, "Ala", 3, -7, 44, 'C', 1, 0, -3]
print("tab1: ", tab1, "  Rozmiar:", len(tab1))
print("Szukam 3: ", szukaj(tab1,  3)!=len(tab1))
print("Szukam 99:", szukaj(tab1, 99)!=len(tab1))
tab2= ['A', 'L', 'A', 'M', 'A', 'K', 'O', 'T', 'A']

