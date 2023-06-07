import numpy as np
t0 = np.linspace(0, 10, 5) # Przedział od 0 do 10 podzielony na 5 wartości
print("t0=", t0)
# t1 = np.arange(1,11)    # 1-wymiarowa, typ domyślny, seria liczb od 1. do 10.
t2 = np.arange(1,11, 3)  # 1-wymiarowa, typ domyślny, seria liczb od 1. do 10., co 3
t3 = np.zeros(9)          # 1-wymiarowa, rozmiar 9, wypełniona zerami (float)
#1-wymiarowa, rozmiar 9, wypełniona 1 (tu:int, typ domyślny to numpy.float64):
t4 = np.ones(9, dtype='i' )
# 1-wymiarowa, rozmiar 4,  wypełniona wartościami pseudolosowymi z przedziału [0.0, 1.0):
t5=  np.random.random(4)
# 1-wymiarowa, rozmiar 9,  wypełniona wartościami pseudolosowymi int (przedział [5,10)
t6=  np.random.randint(5,10, 9)
# Tablica 3x5, wypełniona losowymi wartościami z przedziału [0, 3)
t7=  np.random.randint(3, size=(3, 5))

print("t1=", t1)
t1=t1.reshape( (2,5) )             #  Zmiana kształtu z 1D na 2D (konkretnie 2x5) (*)
print("t1 po reshape(2,5)=", t1)   # Metoda reshape zwraca nową tablicę, ze zmodyfikowanym kształtem i identyczną zawartością
print("t2=", t2)
print("t3=", t3)
print("t4=", t4)
print("t5=", t5)
print("t6=", t6)
print("t7=", t7)

print("Demonstracja 'resize':")

t8 = np.arange(1,11) # 1-wymiarowa, typ domyślny, seria liczb od 1. do 10.
print("t8=", t8)
t8.resize(4,5) # Rozszerzenie z 10 elementów na 4x5
print("t8 po resize (4,5) =", t8)

