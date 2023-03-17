import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2, 2, 100)	# Tablica (wektor) wartości zakresu (-2,2) na osi X
y1 = -5 / x 				# Pierwsza funkcja matematyczna - hiperbola
y2 = np.sin(x)*80-50           # Druga funkcja matematyczna - 80*sin(x)+3
fig = plt.figure(figsize=(10, 5))
plt.plot(x, y1, label ='HIPERBOLA', linestyle='--')      # Wykres y1.
plt.plot(x, y2, label ='80*sin(x)-50')   # Wykres y2.

plt.legend()    # Opis (tzw. legenda)

plt.grid(alpha =.6, linestyle ='-') # Siatka

plt.yticks([-200, -150, -100, 0, 100, 100, 150, 200])                   # Normalizacja wartości na osi Y

plt.xlabel('Oś X')
plt.ylabel('Oś Y')
plt.title("Wykresy funkcji")
plt.show()      # Wyświetl wykres na ekranie