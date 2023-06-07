# Wersja dla systemu DOS/Windows (dla Linux dostosuj składnię komendy 'sort'
import shutil

nazwapliku1="pliki/input1.txt"  # Plik wejściowy 1.
nazwapliku2="pliki/input2.txt"  # Plik wejściowy 2.
nazwapliku3="pliki/input3.txt"  # Plik wyjściowy = złączenie plików 1. i 2.

with open(nazwapliku3, 'wb') as outfile:
    with open(nazwapliku1, 'rb') as readfile:
        shutil.copyfileobj(readfile, outfile)
    with open(nazwapliku2, 'rb') as readfile:
        shutil.copyfileobj(readfile, outfile)

# Wywołujemy sortowanie systemowe, wynik wynik w output.txt:
import subprocess
subprocess.call('sort pliki/input3.txt /O pliki/output.txt')

print("Przykładowa konwersja zawartości pliku do listy zawierającej odczytane wiersze:")
plik = open(nazwapliku3, "r")
wiersze = plik.readlines()
print(wiersze)
print("*** Sortujemy ***")
wiersze.sort()  # Alternatywne kopiowanie do innej listy: wynik=sorted(wiersze)
print(wiersze)
