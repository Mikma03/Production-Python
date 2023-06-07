def szukaj(w, t):   # Konwencja:  w - wzorzec, t - przeszukiwany tekst
    i, j = 0, 0
    M=len(w)
    N=len(t)
    while j<M and i<N:
        if t[i] != w[j]:    # (*) Poziome przesuwanie sie wzorca
            i = i-(j-1)
            j=-1
        i=i+1               # (**)
        j=j+1
    if j==M:
        return i-M
    else:
        return -1   # Umowna porażka poszukiwania
#-----------------------------------------------------------------
# Testujemy
print("Przeszukiwany ciąg znaków")
t="abrakadabra"
print(t,"\n0123456789...")
w="rak"
print(f" Szukam {w} w {t}: {szukaj(w,t)}")
w="raki"
print(f" Szukam {w} w {t}: {szukaj(w,t)}")

"""
 Szukam rak w abrakadabra: 2
 Szukam raki w abrakadabra: -1
"""