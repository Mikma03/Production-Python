from MojeTypy import Lista as l
# Przykłady użycia - bez sortowania
print("Lista zwykła, wstawiam kolejno: 3, 5, 7, 0")
l1 = l.Lista()  # Tworzymy pustą listę
l1.wstawNaKoniec(3)
l1.wstawNaKoniec(5)
l1.wstawNaKoniec(7)
l1.wstawNaKoniec(0)
print("Lista l1=", end=" ")  # Lista l= 3 5 7 0
l1.wypisz()

l1.szukaj(2)
l1.szukaj(7)

# Przykład użycia - z sortowaniem
print("Lista zwykła, wstawiam kolejno: 0 1 3 5 6 7 7")
m1 = l.Lista()  # Tworzymy pustą listę

m1.wstawSort(3)  # 3
m1.wstawSort(5)  # 3 5
m1.wstawSort(7)  # 3 5 7
m1.wstawSort(0)  # 0 3 5 7
m1.wstawSort(1)  # 0 1 3 5 7
m1.wstawSort(6)  # 0 1 3 5 6 7
m1.wstawSort(7)  # 0 1 3 5 6 7 7
print("Lista m1=", end=" ")
m1.wypisz()  # Lista q= 0 1 3 5 6 7 7

# Przykłady usuwania elementów z listy

print("\nUsuwamy pierwszy element")
m1.UsunPierwszy()
m1.wypisz()  # 1 3 5 6 7 7

m1.usunWybrany(1)  # 3 5 6 7 7

m1.wypisz()
m1.usunWybrany(7)  # 3 5 6 7
m1.wypisz()
m1.usunWybrany(7)  # 3 5 6
m1.wypisz()
m1.usunWybrany(7)  # 3 5 6 (brak akcji)

m1.usunWybrany(5),
m1.wypisz()
m1.usunWybrany(3)  # 5 6
m1.wypisz()
m1.usunWybrany(6)  # 6
m1.wypisz()
m1.usunWybrany(6)  # (list pusta)
m1.wypisz()

# Sumowanie list (1) - metoda nieoptymalna
print("Sumowanie list (1) - metoda nieoptymalna")
x, y = l.Lista(), l.Lista()
x.wstawSort(3), x.wstawSort(2), x.wstawSort(1)
y.wstawSort(6), y.wstawSort(5), y.wstawSort(4), y.wstawSort(0)
suma = x + y  # Zauważ dynamiczne wiązanie typu do zmiennej referencyjnej 'suma'!
suma.wypisz()

# Sumowanie list (2) - fuzja
print("Sumowanie list (2) - fuzja")
x1, y1  = l.Lista(), l.Lista()

for n in [3, 6, 2, 5, 12, 0, 19]:
    x1.wstawSort(n)
print("Lista x1=", end=" ")  # 0 2 3 5 6 12 19
x1.wypisz()
for n in [5, 2, 2, 1, 9]:
    y1.wstawSort(n)
print("Lista y1=", end=" ")  # 1 2 2 5 9
y1.wypisz()

pofuzji = l.fuzja(x1, y1) # Fukcja zwróci obiekt klasy Lista
print("Lista x1+y1 (fuzja)=", end=" ")  # 1 2 2 5 9
pofuzji.wypisz()
