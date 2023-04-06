# Przykłady użycia klasy BST

from MojeTypy import BST as b

drzewo = b.BST()
for x in [19, 4, 25, 3, 12, 14, 8, 27, 26, 31]:
    drzewo.wstaw(x)
print(" Pre-order")
drzewo.preOrder(drzewo.korzen)
print("\n In-order")
drzewo.inOrder(drzewo.korzen)
print("\n Post-order")
drzewo.postOrder(drzewo.korzen)

print("\nMin=", drzewo.Min(drzewo.korzen).klucz)
print("Max=", drzewo.Max(drzewo.korzen).klucz)

print("Usuwam 12:")
drzewo.korzen = b.usunWezel(drzewo.korzen, 12)

print("Nowy In-order")
drzewo.inOrder(drzewo.korzen)

for x in [3, 6, 25, 27]:
    res=drzewo.szukaj(x)
    if res!=None:
        print("Znalazłem ", res.klucz)
    else:
        print("Nie znaleziono ", x)

