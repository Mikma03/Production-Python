import numpy as np

tab1Da = np.array( [1, 2, 3, 4, 5] )               # 1-wymiarowa, zastosowano typ domyślny

print("tab1Da:", tab1Da)
print("Wycinek tab1Da[-3, -1]:", tab1Da[-3:-1])
print ("tab1D[1]=", tab1Da[1])

tab1Db = np.arange(1,10)                           # 1-wymiarowa, typ domyślny, seria liczb od 1. do 9. włącznie
print("tab1Db:", tab1Db)
tab1Dc = np.array( np.arange(1,10), dtype='U')     # 1-wymiarowa, typ 'napis Unicode', tj.  seria napisów od "1" do "9"
print("tab1Dc:", tab1Dc)
print("Typ danych w tablicy tab1Dc to:", type(tab1Dc[5]) )


tab2Da = np.array( [ [1, 2, 3], [ 4,  5,  6] ] )  # 2-wymiarowa
tab2Db = np.array( [ [7, 8, 9], [10, 11, 12] ] )  # jw.

print("Tablica 2D:\n", tab2Da)
print ("tab2Da[1,2]=", tab2Da[1, 2])  # Trzeci element z drugiego wiersza (liczymy od zera!)
print ("tab2Da[1][2]=", tab2Da[1][2])  # Alternatywna składnia

tab3Da = np.array( [ [[1, 2, 3], [4, 5, 6]],  [[7, 8, 9], [10, 11, 12]]] )
tab3Db = np.array( [tab2Da, tab2Db] ) # Taka sama zawartość jak dla tab3Da

print("Tablica 3D:\n", tab3Da)
print("Tablica 3D:\n", tab3Db)

