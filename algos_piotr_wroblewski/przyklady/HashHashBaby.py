"""
Zbiór danych wejściowych znajduje się w pliku seria.csv,  (pary wartości oddzielonych przecinkiem):
data, nazwisko, kwota depozytu. Używając odczytanych wartości budujemy tablicę hashująca:
 - wykorzystamy wbudowanej funkcji hash(), rozkład w tablicy zapewni użycie funkcji modulo
 - rozmiar tablicy danych: 20
 - kolizje będą rozwiązywane metodą próbkowania liniowego
"""

# Własna realizacja tablicy hashującej
RMAX=20
lokaty_lista=[None] * RMAX   # Statyczna tablica wypełniona 'None'

def szukaj(T, klucz):   # Wiersze w tablicy zawierają podtablice o strukturze [data, nazwisko, kwota depozytu]
    print("Szukam...")
    pos=hash(klucz) % RMAX
    while (T[pos] != None) and (T[pos][0] != klucz):
        pos = (pos+1) % RMAX
    return T[pos]   # Zwraca znaleziony element
# --------------------------------------------------------------------------------------------------------
# Kod główny:

with open("petenci.csv", "r") as f: # Dane źródłowe znajdziesz w pliku petenci.csv
    for linijka in f:
        odczyt=linijka.split(",")
        indeksik=hash(odczyt[0]) % RMAX # Niech indeksem będzie data
        # Szukamy miejsca na wstawienie:
        while (lokaty_lista[indeksik] != None): # Ups, mamy kolizję!
            indeksik = (indeksik + 1) % RMAX
        wpis=[odczyt [0], odczyt[1], float( odczyt[2] ) ] # Cała zawartość idzie do tablicy danych
        lokaty_lista[indeksik]=wpis  # Zapis pary wartości do LISTY

# ----------------------------------------------------------------
# W celach kontrolnych wydrukujmy w czytelny sposób zawartość naszej minibazy danych
# print(lokaty_lista)
for i in range(RMAX):
    if lokaty_lista[i] != None:
        print(lokaty_lista[i])
klucz="15.04.2022" # Szukamy wpisu dla podanego klucza
res = szukaj(lokaty_lista, klucz)
print(f"Szukamy rekordu dla klucza {klucz}, wynik: {res}")