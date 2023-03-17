import matplotlib.pyplot as plt
import numpy as np
""" Plik danedowykresu.csv zawiera pewne dane do wykresów rozdzielone przecinkami (X, Y1, Y2):
10,5,3
20,5.6,3
...
100,9.5,12
"""
osX, osY, osY2 = np.loadtxt('danedowykresu.csv',delimiter=',', unpack=True)
seria1,=plt.plot(osX, osY,  marker='*', linestyle='--', color='k',
                 ms=10, linewidth = '1', label='Seria 1.') # Seria 1.
seria2,=plt.plot(osX, osY2, marker='o', linestyle='-',  color='k',
                 ms=10, linewidth = '1', label='Seria 2.') # Seria 2.
plt.title("Wykresy - dane pobrane z pliku CSV")
plt.legend(handles=[seria1, seria2])
plt.legend()
plt.show()