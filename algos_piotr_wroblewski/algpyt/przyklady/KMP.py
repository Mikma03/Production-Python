shift=list()    # Tablica przesunięć

def init_shifts(w):
    M = len(w)
    global shift
    shift = [0] * len(w) # Inicjalizacja pustej tablicy przesunięć
    shift[0]=-1
    i, j = 0, -1
    while i < M-1:
        shift[i] = j
        while j>=0 and w[i]!=w[j]:
            j=shift[j]
        i = i + 1
        j = j + 1

def kmp(w, t):      # Konwencja:  w - wzorzec, t - przeszukiwany tekst
    N=len(t)
    M=len(w)
    i, j = 0, 0
    while i<N and j<M:
        while j>=0 and t[i]!=w[j]:
            j=shift[j]
        i=i+1
        j=j+1
    if j==M:
        return i-M
    else:
         return -1


# Testujemy
print("Przeszukiwany ciąg znaków")
t="abcd1010def"
print(t,"\n0123456789...")
w="1010"
init_shifts(w)
print(f" Szukam {w} w {t}: {kmp(w,t)}")
w="kotek"
init_shifts(w)
print(f" Szukam {w} w {t}: {kmp(w,t)}")