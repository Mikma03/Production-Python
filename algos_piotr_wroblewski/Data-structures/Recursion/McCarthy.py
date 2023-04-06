cpt=0   # Globalna zmienna cpt
def McCarthy(x):
    global cpt    # Odnosimy się do zmiennej globalnej 'cpt'
    cpt=cpt+1     # (bez powyższej deklaracji Python zgłosi wyjątek, sprawdź!)
    if x > 100:
        return (x-10)
    else:
        return  McCarthy( McCarthy(x+11) )

# Testujemy funkcję McCarthy:
x = int (input ("Podaj x:"))# Pobieranie danych. Uwaga: brak obsługi wyjątków, oczekiwana będzie liczba!

print(f"McCarthy({x}) = {McCarthy(x)}")
if (cpt==1):
    print("[Funkcja została wywołana raz]")
else:
    print(f"[Funkcja została wywołana {cpt} razy]")
print ("Do widzenia!")







