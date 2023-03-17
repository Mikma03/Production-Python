#--------------------------------------------------------------------------------
class Element:
    def __init__(self, pImie, pWiek):
        self.imie = pImie
        self.wiek=pWiek
#--------------------------------------------------------------------------------
# Funkcje pomocnicze (nie są to metody!)
def porownaj_imiona(obj, pImie):
    if obj.imie==pImie:
        return True
    else:
        return  False
def porownaj_wiek(obj, pWiek):
    if obj.wiek==pWiek:
        return True
    else:
        return  False
#--------------------------------------------------------------------------------
# Uniwersalna funkcja wyszukująca obiekt według kryterium podanego jako parametr:
def szukaj(tab, x, porownywarka): # Szukaj 'x' w tablicy, zmienna ‘porownywarka’ jest referencją do funkcji!
    if len(tab)==0:
        return len()
    i=0
    while i< len(tab):
        if porownywarka(tab[i], x):   # (*)
            break
        else:
            i=i+1
    return i # jeśli 'i' wyjdzie poza zakres tablicy, to nie znaleziono elementu
#--------------------------------------------------------------------------------

tab= [Element("Jan", 20), Element("Marek", 10), Element("Maria", 15), Element("Zośka", 13)]
print("Szukam imię='Maria' ", szukaj(tab, "Maria", porownaj_imiona) != len(tab) )
print("Szukam imię='Marja' ", szukaj(tab, "Marja", porownaj_imiona) != len(tab) )

print("Szukam wiek=132 ", szukaj(tab, 132, porownaj_wiek) !=len(tab) )
print("Szukam wiek=13 ", szukaj(tab, 13,   porownaj_wiek) !=len(tab) )

