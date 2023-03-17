jezyki   = ["C++", "Python", "Java", "Lisp"]      # Prosta lista (tablica napisów)
cyfry = [1, 2, 3, 4, 5, 7, 8, 9, 0]
print("* Kilka przykładów użycia pętli for")

print("Języki programowania:")
for x in range(len(jezyki)):          # wypisz elementy listy oddzielając je od siebie spacjami
    print (jezyki[x], end =" ")       # end =" " zastępuje ostatni, domyślny znak (\n) dowolnym innym (tutaj: spacja)
print()                               # Nowa linia
for x in range(len(cyfry)):           # wypisz elementy listy oddzielając je od siebie spacjami
    print (f"({cyfry[x]})", end =" ") # oraz  otaczając je nawiasami ()
print()                               # Nowa linia
print(*cyfry)                         # Wypisz zawartość listy 'cyfry' rozdzielając elementy spacjami
print(*cyfry, sep ="-")               # Wypisz zawartość listy 'cyfry' rozdzielając elementy kreskami (-), patrz: 'sep'

print("* Kilka przykładów użycia pętli for, modyfikacje zakresów")
for n in range(3, 5):                 # Wyoisz wartości od 3 do 4 (ostatnia wartość, 5 jest pomijana)
    print (n, end =" ")
print()

for n in range(5):                    # Wyoisz wartości od 0 do 4 (ostatnia wartość, 5 jest pomijana)
    print (n, end =" ")
print()

print("* Pętle zagnieżdżone i instrukcja continue")
for p in range(3):                    # przykład pętli zagnieżdżonej (1)
    for q in range(4):
        if q==2:
            print(f"Pomijamy q={q}")
            continue                     # pomiń (instrukcja continue) jeśli wartość q=2
        print (f"(p={p} q={q})", end =" ")

print()

print("* Ilustracja instrukcji break")
for p in range(3):                    # przykład pętli zagnieżdżonej (2)
    for q in range(4):
        if q==2:
            print(f"Wykryto q={q}")
            break                     # wyjdź z iteracji (instrukcja break) jesli wartość q=2
        print (f"(p={p} q={q})", end =" ")

print("* Pzykład użycia pętli while")
# Wylicz sumę liczb od 1 do 100
tmp=0
i=1
while i <= 100:
  tmp=tmp+i
  i = i +1
print("Suma liczb od 1 do 99:", tmp)
print("* Pętla for: modyfikacja inkrementów, przebiegi wsteczne")
for i in range (0, 100, 10):
    print(i, end= " ")
print("\n")
for  i in range (100, 0, -10): # od 100 do 90!
    print(i, end=" ")
print("\n")
for c in "Figo":
    print (c, end=" ... ")


