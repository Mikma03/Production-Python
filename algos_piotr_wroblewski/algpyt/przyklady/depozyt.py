# Realizacja klasy zapisującej depozyty bankowe od klientów
# Bank nałożył limit depozytów złożonych od klientów na kwotę 50 000 PLN
# Klasa została wyposażona w tzw. właściwości (ang. properties), oraz zmienne klasowe

class Depozyt:
       Limit=50_000    # Zmienna klasowa (limit sumy  depozytów)
                       # Zmienna klasowa jest dostępny nawet, gdy nie utworzymy obiektów!
       Suma=0          # Zmienna klasowa (suma złożonych depozytów)

       def __init__(self, pWlasciciel, pDepozyt):      # Konstruktor
              self.__wlasciciel=pWlasciciel            # Według uznanej konwencji, atrybut prywatny poprzedzamy __
              if pDepozyt + Depozyt.Suma <= Depozyt.Limit:
                     self.__zdeponowano = pDepozyt
                     Depozyt.Suma = Depozyt.Suma + pDepozyt  # Dodajemy kolejny depozyt kliencki...
              else:
                     raise Exception("Odmowa! Depozyty przekroczyły limit promocyjny " + str(Depozyt.Limit) + " PLN")

       def __str__(self): # Zwracamy obiekt sformatowany do postaci napisu
              return "[ Właściciel: " + self.__wlasciciel +", Kwota depozytu: " + str(self.__zdeponowano) + " ]"
       # Realizacja koncepcji "właściwości":

       # Właściwość przeznaczone tylko do odczytu:
       @property
       def wlasciciel(self):
              return self.__wlasciciel
       # Kolejna właściwość będzie przeznaczona do odczytu lub modyfikacji:∂
       @property
       def depozyt(self):
              return self.__zdeponowano
       @depozyt.setter
       def depozyt(self, korekta):
              staraWartosc=self.__zdeponowano
              if korekta+Depozyt.Suma -staraWartosc <= Depozyt.Limit:
                     self.__zdeponowano = korekta
              else:
                     raise Exception("Odmowa! Depozyty przekroczyły limit promocyjny " + str(Depozyt.Limit) + " PLN")
              Depozyt.Suma = Depozyt.Suma - staraWartosc + korekta  # Dodajemy kolejny depozyt kliencki...

       def komunikat(self):
              print("Cześć, jestem obiektem klasy Depozyt!")
# --------- Kilka przykładów użycia: ------------------------------------------------------------
d1=Depozyt("Kowalski",  30_000)
print("Depozyt 'p1' to ", d1)
print("Suma depozytów to :", Depozyt.Suma)

d2=Depozyt("Nowak", 10_000)
print("Depozyt 'd2' to ", d2)
print("Suma depozytów to:", Depozyt.Suma)

d3=Depozyt("Wróbel", 10_000)
print("Depozyt 'd3' to ", d3)
print("Suma depozytów to:", Depozyt.Suma)

#d1.wlasciciel="Kowalska"  # AttributeError: can't set attribute 'wlasciciel' (*)

print("Depozyt 'd3' utworzył ", d3.wlasciciel)
# print("Depozyt 'd3' utworzył ", d3.__wlasciciel) # (**) AttributeError: 'Depozyt' object has no attribute '__wlasciciel'. Did you mean: 'wlasciciel'?

print("Modyfikujemy depozyt d3 - wartość zmieniona na 5000:")
d3.depozyt=5000
print("Suma depozytów to:", Depozyt.Suma)
print("Depozyt 'd3' to teraz ", d3)

#d3.depozyt=40_000  # Exception: Odmowa! Depozyty przekroczyły limit promocyjny 50000 PLN (***)


d3.komunikat() # Przykładowa metoda klasy

# Przechwytywanie wyjątków:
try:
       d3.depozyt=40_000
except:
       print ("Ups, przekroczono limit depozytów... Próbuj dalej.")
