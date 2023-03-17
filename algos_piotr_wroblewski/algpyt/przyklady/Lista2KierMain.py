from MojeTypy import Lista2Kier as l

lista = l.Lista2Kier()
lista.wstaw("A", 12), lista.wstaw("B", 34), lista.wstaw("C", 34), lista.wstaw("D", 55), lista.wstaw("E", 67);
lista.wypiszWprzod("Lista od przodu:")
lista.wypiszWstecz("Lista od tyłu:")

s='X'
res, wynik = lista.szukaj(s)
if wynik:
    print("Znalazłem", s)
else:
    print("Brak rekordu", s)

lista.usun("B")
lista.wypiszWprzod("Lista od początku:")


