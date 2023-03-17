# Funkcja pomocnicza zamieniająca napis w Pythonie (niemodyfikowalny) na tablicę (listę) znaków
def str2list(napis):
    return [c for c in napis] # Lub prościej: return list(s)
# Funkcja pomocnicza zamieniająca listę znaków na napis w Pythonie (obiekt klasy 'str')
def list2str(lista):
    res=""
    for x in lista:
        res = res + x
    return res

def Xor(lista_znakow, xor_key):    # Metoda 1. Parametr wejściowy to lista znaków wchodzących w skład napisu
    for i in range ( len(lista_znakow) ):
        lista_znakow[i]= chr( ( ord(lista_znakow[i]) ^ ord(xor_key)) )

def odejmij(lista_znakow): # Metoda 2. Parametr wejściowy to lista znaków wchodzących w skład napisu
    for i in range( len(lista_znakow) ):
        lista_znakow[i]=chr ( 255 - ord( lista_znakow[i]) )

# Testujemy
print("Klasyczna metoda XOR")
s1= "Ala ma kota"
s1_lista = str2list(s1)
print("Oryginał: ", s1)
Xor(s1_lista, '#') # Kodujemy...
print("Ciąg zakodowany XOR: ", list2str(s1_lista))
Xor(s1_lista, '#') # Dekodujemy...
print("Ciąg odkodowany XOR: ", list2str(s1_lista))

print("Przesunięcie 255")
s2= "Figo to pies"
s2_lista = str2list(s2)
print("Oryginał: ", s2)
odejmij(s2_lista) # Kodujemy...
print("Ciąg zakodowany XOR: ", list2str(s2_lista))
odejmij(s2_lista) # Dekodujemy...
print("Ciąg odkodowany XOR: ", list2str(s2_lista))