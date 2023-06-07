# 1) Sortowanie list Pythona

oryginalna=[4, 6, 8, 2, 12, 7, 0]
print("Lista oryginalna=", oryginalna)
oryginalna.sort() # Sortowanie w miejscu:
print("Efekt sortowania w miejscu=", oryginalna) # [0, 2, 4, 6, 7, 8, 12]
oryginalna.append(5) # Dodajemy na koniec 5
# funkcja sorted() zwracanową  na podstawie listy przekazanej w parametrze wywołania, domyślnie reverse=False
print("Sortowanie wstecznie=", sorted(oryginalna, reverse=True)) # [12, 8, 7, 6, 5, 4, 2, 0]
print("Zmodyfikowana lista posortowana przy pomocy sorted(): ",  sorted(oryginalna))  # [12, 8, 7, 6, 5, 4, 2, 0]

# 2) Sortowanie list zawierających obiekty złożone, np. listy

lokaty=[['20.02.2022', 'Morawski', 5000], ['22.02.2022', 'Blady',    5500], ['23.02.2022', 'Lukaszewski',5500],
        ['12.01.2022', 'Nowak',    2200], ['15.04.2022', 'Pankracy', 6700], ['15.04.2022', 'Witos',      2050] ]

print("Lokaty nieposortowane")
print(lokaty)
print("Lokaty posortowane według nazwiska")
print( sorted(lokaty, key=lambda x: x[1] ) )    # Funkcja "lambda" to funkcja inline, bez nazwy

# 3) Sortowanie list zawierających obiekty złożone, np. listy wpisów słownikowych
print("Kursy walut (nieposortowane):")
kursywalut = [
  {'waluta': 'EUR',   'data': "15.04.2022", 'kurs':4.99},
  {'waluta': 'EUR',   'data': "16.04.2022", 'kurs':5.05},
  {'waluta': 'USD',   'data': "15.05.2022", 'kurs':3.95},
  {'waluta': 'Rubel', 'data': "18.03.2022", 'kurs':0.01}
]
print("Kursy walut posortowane według wartości")
print( sorted(kursywalut, key=lambda x: x.get("kurs")))
