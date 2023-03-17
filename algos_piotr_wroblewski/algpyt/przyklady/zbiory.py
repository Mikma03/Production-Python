zbiornik = {"żaba", "komar", "insekt"}

print ("Zbiór: ", zbiornik)
print ("Spóbujmy dodać do zbiornika kolejną żabę...")
zbiornik.add("żaba")
print ("Aktualny stan zbiornika:")
print ("Zbiór: ", zbiornik)

lista1=[2,3,4,5,6,6,6,9,9,0]
print ("Budowanie zbioru na podstawie listy:", lista1)

print ("Lista 'lista1'=", lista1)
zbior2=set(lista1) # Alternatywna metoda budowania zbiorów z użyciem konstruktora 'set' załądowanego listą elementw
print ("Zbiór 'zbior2' utworzony z 'lista1'=", zbior2)
print ("Zbiory zawierające elementy różnych typów:")
kodHEX={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F'}
print ("Dozwolone znaki kodu szesnastkowego:\n", kodHEX)

# Przykładowe operacje na zbiorach
zb={9, 5, 7, 8, 7, 7} # Zbiór będzie zawierał tylko: 8, 5 i 7
zb.remove(7) # Usuwamy 7
print(zb)

# Suma zbiorów:
zb1={5, 6, 7}
zb2={6, 7, 8, 9}
zb3=zb1.union(zb2)  # Uwaga: w nawiasie możesz podać więcej zbiorów, oddzielając je przecinkami
print(zb1|zb2)      # Wypisze {5, 6, 7, 8, 9}
print(zb3)          # Wypisze {5, 6, 7, 8, 9} - jest to analogiczna operacja

# Przecięcie 2 zbiorów:
zb3=zb1.intersection(zb2)
print(zb1&zb2)      # Wypisze {6, 7}
print(zb3)          # Wypisze {6, 7} - jest to analogiczna operacja

# Przecięcie 3 zbiorów:
zb1={2, 4, 6, 8}
zb2={1, 4, 6, 10}
zb3={0, 4, 6, 11}
print(zb1&zb2&zb3)                  # Wypisze {4, 6}
print(zb1.intersection(zb2, zb3))   # Wypisze {4, 6} - jest to analogiczna operacja

# Różnica zbiorów:
zb1={2, 4, 6, 8}
zb2={1, 4, 6, 10}
print(zb1-zb2)               # Wypisze {8, 2}
print(zb1.difference(zb2))   # Wypisze {8, 2} - jest to analogiczna operacja

zb1={2, 4}
zb2={5, 4, 2, 10}
print(zb1.issubset(zb2))     # Wypisze True

zb1={2, 4, 6, 8}
zb2={4, 6, 8}
print(zb1.issuperset(zb2))     # Wypisze Trueś




