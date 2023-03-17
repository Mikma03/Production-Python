def szukaj(tab, x):# Zwraca indeks poszukiwanej wartości 'x' lub -1
    left=0
    right=len(tab)-1
    mid=0
    znaleziono=False
    while  (left<=right) and ( not znaleziono):
        mid=(left+right)//2
        if(tab[mid] == x):
            znaleziono=True
        else:
            if tab[mid] < x:
                left=mid+1
            else:
                right=mid-1
    if znaleziono==True:
        return mid
    else:
        return -1

# Testujemy algorytm
tabl=[1, 2, 6, 18, 20, 23, 29, 32,34, 39, 40, 41]
for i in range(0, len(tabl) ):
    print(f"t[{i}]={tabl[i]}", end=" ")
print() # t[0]=1 t[1]=2 t[2]=6 t[3]=18 t[4]=20 t[5]=23 t[6]=29 t[7]=32 t[8]=34 t[9]=39 t[10]=40 t[11]=41
print(f"Szukam 23, wynik:  {szukaj(tabl, 23)} ") # Wypisze: 5
print(f"Szukam 3,  wynik:  {szukaj(tabl,  3)} ") # Wypisze: -1






