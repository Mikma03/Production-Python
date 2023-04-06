# Przykłady formatowania w notacji f"

moje_pi = 3.141592653589793
odchylka = 0.23
x_dec= 146
wielka_liczba=2344456612435.567
roznica=0.46

print(f"Liczba pi to {moje_pi}, co można skrócić do >>>{moje_pi:.4f}<<<")
# Zwykłe zaokrąglenie do 4 cyfr po przecinku:
print(f"Odchyłka pomiarowa wynosi >>>{odchylka:20.4f}<<<")
# Szerokość 20 znaków + rozszerzenie po przecinku:
print(f"Odchyłka pomiarowa wynosi >>>{odchylka:<20.4f}<<<") # Jak wyżej + wyrównanie do lewej
# Ustawienie przecinka jako separatora kolejnych 3 cyfr dużej liczby:
print(f"Wielka liczba: {wielka_liczba:}, wielka liczba z separatorem: {wielka_liczba:,}")
print(f"Różnica w cenie to: {roznica:.0%}") # Zamiana ułamka na procenty
print(f"Liczba w systemie dziesiętnym: {x_dec}, ta sama liczba binarnie: "
      f"{x_dec:b} oraz heksadecymalnie: {x_dec:X}")
# Układ tabelaryczny:
print("Bez formatowania:")
for i in range(99, 105):
    print(f"Liczba {i} do kwadratu: | {pow(i, 2)} |")
print("Z formatowaniem:")
for i in range(99, 105):
    print(f"Liczba {i:3} do kwadratu: | {pow(i, 2) : ^7,}|")