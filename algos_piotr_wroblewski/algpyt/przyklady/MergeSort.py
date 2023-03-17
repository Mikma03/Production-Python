def scalaj(T1, left,  mid,  right):     # left - początek, right - koniec, mid - środek
# Procedura łączy 2 posortowane tablice T1[left...mid] i T1[mid+1...right]
    left1 =   left # Podtablica 1
    right1  =  mid
    left2 =   mid+1 # Podtablica 2
    right2  = right
    T2 = [None]* len(T1) # T2 - tablica pomocnicza
    i = left1
    # Aż do wyczerpania obu podtablic dokonaj scalenia przy pomocy tablicy pomocniczej:
    while((left1 <= right1) and (left2 <= right2)):
        if T1[left1] < T1[left2]:
            T2[i] = T1[left1]
            left1=left1+1
        else:
            T2[i] = T1[left2]
            left2=left2+1
        i=i+1

    while left1 <= right1:
        T2[i] = T1[left1]
        left1=left1+1
        i=i+1

    while left2 <= right2:
        T2[i] = T1[left2]
        left2=left2+1
        i=i+1

    for i in range(left, right+1): # Skopiuj z tablicy tymczasowej do oryginalnej
        T1[i] = T2[i]

# ---------------------------------------------------------

def MergeSort(T,  left,  right):
    if left < right:
        mid = (left + right) // 2       # Środek
        MergeSort(T, left, mid)         # Sortowanie podtablic lewej i prawej
        MergeSort(T, mid+1, right)      # Sortuj prawą połowę
        scalaj(T, left, mid, right)     # Scalaj


T = [4, -6, 6, 34, 12, -3, 72, 6, -6, 24, 5, 8, 2, -7]
print("Przed sortowaniem")
print(T)
print("Po sortowaniu")
MergeSort(T, 0, len(T)-1)
print(T)    # [-7, -6, -6, -3, 2, 4, 5, 6, 6, 8, 12, 24, 34, 72]

