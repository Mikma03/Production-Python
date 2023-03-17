# Skrypt niemal identyczny z analizaWWW.py ale wzbogacony o:

# Lista kodów błędów: patrz https://pl.wikipedia.org/wiki/Kod_odpowiedzi_HTTP:

slownikBledow={
    '400' : 'Bad Request',
  # '401' : 'Unauthorized', # Świadomie pominięty!
    '408' : 'Request Timeout',
    '410' : 'Gone',
    '413' : 'Request Entity Too Large',
    '415' : 'Unsupported Media Type',
    '414' : 'Request-URI Too Long',
    '422' : 'Unprocessable entity',
    '425' : 'Too Early',
    '429' : 'Too Many Requests',
    '431' : 'Request Header Fields Too Large'}

# Tabela zawierająca otrzymane kody błędów z 3 serii testowania

wyniki_surowe=list()
wyniki_surowe.append(list())  # Seria 1.
wyniki_surowe.append(list())  # Seria 2.
wyniki_surowe.append(list())  # Seria 3.

wyniki_surowe[0]=["400", "401", "401", "401", "401", "410", "410", "425", "400", "429", "431", "431", "400", "431",\
                  "413", "414", "425", "401", "410", "410", "401", "408", "408", "408", "400", "400", "400"]
wyniki_surowe[1]=["408", "408", "408", "400", "401", "401", "410", "425", "400",  "429", "431", "431", "415", "408",\
                  "408", "400", "425", "401", "410", "410", "401", "408", "408", "408", "422", "400", "400"]
wyniki_surowe[2]=["400", "400", "401", "401", "401", "400", "400", "425", "400"]

# Sprawdźmy zawartość

print("Wszystkie wyniki serii 1.:", wyniki_surowe[0])
print("Wszystkie wyniki serii 2.:", wyniki_surowe[1])
print("Wszystkie wyniki serii 3.:", wyniki_surowe[2])

# Tabela zawierająca otrzymane kody błędów z 3 serii testowania przekształcone na zbiory

wyniki_zbiory=list()

wyniki_zbiory.append(set(wyniki_surowe[0]))  # Seria 1. przekształcona do postaci zbioru
wyniki_zbiory.append(set(wyniki_surowe[1]))  # Seria 2. przekształcona do postaci zbioru
wyniki_zbiory.append(set(wyniki_surowe[2]))  # Seria 3. przekształcona do postaci zbioru

print("Znormalizowana lista wyników (bez duplikatów)")

print("  Seria 1.:", wyniki_zbiory[0])
print("  Seria 2.:", wyniki_zbiory[1])
print("  Seria 1.:", wyniki_zbiory[2])

# A teraz analiza danych (w tym miejscu wprowadzono zmiany w porównaniu z analizaWWW.py):

print("Lista wszystkich wykrytych błędów:")
wszystkie=wyniki_zbiory[0] |  wyniki_zbiory[1] | wyniki_zbiory[2]

for kod in wszystkie:
    print(kod, " ", slownikBledow.get(kod, "Nieznany kod błędu!"))

print("Te same kody błędów wykryte w każdej z serii:")
wspolne=wyniki_zbiory[0] &  wyniki_zbiory[1] & wyniki_zbiory[2]
for kod in wspolne:
    print(kod, " ", slownikBledow.get(kod, "Nieznany kod błędu!"))

