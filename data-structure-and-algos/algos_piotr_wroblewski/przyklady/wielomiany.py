def oblicz_wielomian(a, w): # Metoda klasyczna, tablica 'w' zawiera współczynniki wielomianu
    res=0
    pot=1
    for j in range( len(w)-1, -1, -1 ): # Od len(w)-1 do 0
        res=res+pot*w[j]    # Sumy cząstkowe
        pot=pot*a           # Następna potęga a
    return res

def oblicz_wielomian_H(a, w):   # Schemat Hornera
    res=w[0]
    for j in range(1, len(w) ):
        res=res*a+w[j]
    return res

def dodaj_wiel(x, y):   # Zakładamy te same rozmiary
    for i in range(0, len(w) ):
        z[i]=x[i]+y[i]
    return z    # Wielomian z=x+y

def  mnoz_wiel(x, y):   #  z= x * y
    z= [0] *  ( len(x) + len(y) -1) # Zerowanie rezultatu
    for i in range( len(x) ):
        for j in range( len(y) ):
            z[i+j]=z[i+j] + x[i]*y[j]
    return z

def pisz(opis, w):
    print(opis, end=" ")
    for i in range( len(w)-1, -1, -1):  # Od len(w)-1 do 0
        if w[i]>=0:
            print(" +", w[i], end= "")
        else:
            print(w[i], end="")
        if i != 0:  # Stopień zero = wartość liczbowa
            print(f"x^{i}",end="")
        if i != len(w)-1:
            print(end="")
    print()

#  --------------------------------------------------------------------
# Testujemy

w=[1, 4, -2, 0, 7]  # Współczynniki wielomianu 7x^4 + 0x^3 - 2x^2 +4x^1 + 1 = 7x^4 -2x§2 +4x + 1
pisz("w = ", w)
print("Klasycznie w(2) = ", oblicz_wielomian(2, w) )
print("Horner w(2)=", oblicz_wielomian_H(2, w) )
a=[3, 3, 0, 5]
pisz("a = ", a)
b=[2, 3, 1]
pisz("b = ", b)
c=list()    # Pusta tablica na wielomian wynikowy
c=mnoz_wiel(a, b)
pisz("a*b = ", c)

"""
w =   + 7x^ 4 + 0x^ 3-2x^ 2 + 4x^ 1 + 1
Klasycznie w(2) =  47
Horner w(2)= 47
a =   + 5x^ 3 + 0x^ 2 + 3x^ 1 + 3
b =   + 1x^ 2 + 3x^ 1 + 2
a*b =   + 5x^ 5 + 15x^ 4 + 13x^ 3 + 12x^ 2 + 15x^ 1 + 6

"""