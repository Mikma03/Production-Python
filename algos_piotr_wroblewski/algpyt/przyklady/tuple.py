tupla0=(1, )  # Tak się tworzy obiekt klasy 'tuple' zawierający pojedynczą wartość (przecinek to nie jest błąd)
              # Zapis tupla0=(1) utworzyłby w Pythonie zwykłą zmienną liczbową klasy int

tupla1=(1, 1, 2, 3, 5, 8, 13)             # Najpopularniejsza notacja
# tupla1[3]=100                             # Błąd, tupli nie można modyfikować!
print(len(tupla1))                                                 # Wypisze 7, tj. długość tupli

tupla2=tuple ((1, 1, 2, 3, 5, 8, 13))     # Alternatywna notacja, z użyciem konstruktora klasy 'tuple'
tupla3=("Dr Who", "Dawid Tennant",   10)  # Patrz https://www.examinerlive.co.uk/news/here-full-list-dr-who-13339904
tupla4=("Dr Who", "Jodie Whittaker", 13)
tupla3_plus_tupla4=tupla3+tupla4
print(tupla4)       # Wypisze: ('Dr Who', 'Jodie Whittaker', 13)
print(tupla3_plus_tupla4)       # Wypisze: ('Dr Who', 'Dawid Tennant', 10, 'Dr Who', 'Jodie Whittaker', 13)
print(tupla4[1])    # Wypisze: Jodie Whittaker

print("Ilustracja niebezpośredniego modyfikowania zawartości tupli")
nazwy_skrocone=['pon', 'wt', 'śr', 'czw', 'pt', 'sob'] # Ups, na tej liście brakuje niedzieli!
tupla5=("dni", nazwy_skrocone)
print("Tupla oryginalna, dwuelementowa:", tupla5)
# Modyfikujemy zawartość listy nazwy_skrocone (sama tupla5 jest nienaruszona)
tupla5[1].append("nd")
print("Tupla po dodaniu 'nd' do listy wskazywanej przez drugi element tupli:\n", tupla5)  # Wyświetli aktualną zawartość tupli

print("Modyfikacja tupli poprzez konwersję do listy")
dni_robocze=('pon', 'wt', 'śr', 'czw', 'pt')
print("Dni robocze", dni_robocze)
dni_robocze_lista=list(dni_robocze)
dni_robocze_lista.append('sob')
dni_robocze=tuple(dni_robocze_lista)
print("Dni robocze", dni_robocze)

# Przykład użycia tupli jako statycznej listy referencyjnej:

dozwolone_waluty=('PLN',  'EUR', 'USD')
print ("Dozwolone waluty to:", dozwolone_waluty)
s=input("Podaj walutę: ")           # Program poprosi użytkownika o wpisanie danych
if s in dozwolone_waluty:
    print("Poprawna waluta")
else:
    print("Nieznany kod waluty")
# Metody klasy tuple

dni=[ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
print (dni.count(31)) # Wypisze: 7 (Liczba wystąpień)
print (dni.index(30)) # Wypisze: 3 (Indeks pozycji szukanego elementu)

# Modyfikacja tupli, cd.:

