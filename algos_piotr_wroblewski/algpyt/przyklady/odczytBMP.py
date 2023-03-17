import sys
print("*** Odczyt pliku BMP w trybie binanym ***")
plik=open("domek.bmp", "rb")
dane = plik.read()  # Czytamy cały plik
dlugosc=len(dane)
print("Otwarto plik: ",plik.name)
print("Tryb otwarcia: ",plik.mode)
print("Plik zajmuje", dlugosc, "bajtów na dysku")
plik.seek(0)    # Ustawiamy się na pozycję 1. (bfType, Ustawione na 'BM' dla plików BMP w Windowsie)

print("6 początkowych bajtów:")
for i in range(0,6):
    c=plik.read(1)
    print("\tBajt nr:", i, ":", c, "hex:", c.hex())

plik.seek(2)    # Ustawiamy kursor na trzeci bajt, czyli parametr bfSize (4 bajty)
bfSize= plik.read(4)
print("bfSize binarnie:", bfSize)

# Dekodujemy wartość całkowita z ciągu bajtów używając funkcji int.from_bytes o następującej składni:
# int.from_bytes (cig binarny, endianness)
# endianness = 'big' lub 'little' (konwencja big lub litte endian)
# # Można użyć przenośnej konstrukcji sys.byteorder, która sama wykryje poprawną wartość:
bfSizeDecymalnie=int.from_bytes(bfSize, byteorder=sys.byteorder)
print("bfSize decymalnie:", bfSizeDecymalnie)

plik.seek(18)           # Ustawiamy kursor na 19. bajt, czyli parametr biWidth (4 bajty)
biWidth=plik.read(4)    # Szerokośc obrazu
plik.seek(22)           # Ustawiamy kursor na 23. bajt, czyli parametr biHeight (4 bajty)
biHeight=plik.read(4)    # Wysokość obrazu

print("biWidth=",  int.from_bytes(biWidth, byteorder=sys.byteorder),  "pikseli")
print("biHeight=", int.from_bytes(biHeight, byteorder=sys.byteorder), "pikseli")

plik.close()
