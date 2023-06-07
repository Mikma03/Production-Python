"""
Zbiór danych wejściowych znajduje się w pliku seria.csv,  (pary wartości oddzielonych przecinkiem):
data, nazwisko, kwota depozytu. Odczytane wartości wstawimy do:
1) listy o nazwie 'lokaty_lista'
2) słownika o nazwie 'lokaty_slownik', gdzie kluczem będzie data (pamiętaj, klucz jest unikalny!)
   Nie można zatem wstawić dwóch wierszy pod ten sam klucz, kolejne wstawienie pod taki sam klucz
   nadpisują poprzednią wartość
"""

lokaty_slownik={}
lokaty_lista=[]
with open("petenci.csv", "r") as f: # Dane źródłowe znajdziesz w pliku petenci.csv
    for linijka in f:
        odczyt=linijka.split(",")
        data=odczyt[0]
        depozyt=[odczyt[1], float( odczyt[2] ) ]
        lokaty_slownik[data]=depozyt            # Zapis pary wartości do SŁOWNIKA
        lokaty_lista.append([data, depozyt])    # Zapis pary wartości do LISTY

print(lokaty_lista)
print(lokaty_slownik)

klucz="12.03.2022" # Szukamy wpisu dla podanego klucza
print("[Przeszukiwanie liniowe listy]:  Szukam wpisu dla daty ", klucz)
for i in range ( len(lokaty_lista) ) :
    if lokaty_lista[i][0]==klucz:
        print(lokaty_lista[i][1])

print("[Przeszukiwanie bezpośrednie słownika]:  Szukam wpisu dla daty ", klucz)
if lokaty_slownik.get(klucz) !=None:
    print(lokaty_slownik[klucz])
else:
    print("Brak rekordu")