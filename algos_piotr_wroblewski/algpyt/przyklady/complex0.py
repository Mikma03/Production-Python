# Kod utworzony wyłącznie jako ilustracja tworzenia klasy w Pythonie!
# Jeśli chcesz używać liczb zespolonych w skryptach, to użyj klasy 'complex'
# dostępnej w standardowej bibliotece Pythona!
class Complex:
       # Metoda __init__ to tzw. konstruktor, zostanie ona wywoływaną podczas tworzenia obiektu

       def __init__(self, pRe=0, pIm=0):
              self.re = pRe  # Tworzymy atrybut Re - część rzeczywista
              self.im = pIm  # Tworzymy atrybut Im – część urojona
              print("Narodził się nowy obiekt... Nie zapomnij o deklaracji 500+") # Taki żart...

       def __str__(self): # Zwróć zawartość obiektu jako napis, możesz zatem wypisywać obiekty w funkcji print!
              return str(self.re) + "+" + str(self.im) + "*i"

       def dodaj(self, x2):  # Ta metoda dodaje do bieżącego obiektu inny obiekt 'x2' klasy Complex
              self.im = self.im + x2.im  # x2 podajemy jako parametr wywołania metody
              self.re = self.re + x2.re #  Obiekt x zostanie modyfikowany!

# --------- Kilka przykładów użycia: ------------------------------------------------------------
# W pierwszej linii wywołano konstruktor bez parametrów, co oznacza ustawienie
# wartości domyślnych jego parametrów na pRe=0 oraz pIm=0:
n=Complex()
print(f"Obiekt 'n' to [{n}]")   # Sprawdźmy zawartość - metoda wypisze: 0+0*i
x = Complex(5,8)                # Tworzymy nowy obiekt x = 5 + 8*i
y = Complex(1,2)                # Tworzymy nowy obiekt y = 1 + 2*i
print(f"Obiekt 'x' to [{x}]")
print(f"Obiekt 'y' to [{y}]")
x.dodaj(y)                      # Dodaj do 'x' wartość 'y' (także liczba zespolona)
print(f"Obiekt x=x+y to [{x}]") # Sprawdźmy aktualną wartość 'x'
# Modyfikujemy pole (możemy to zrobić bo atrybut jest "publiczny"):
print("Ustawiamy wartość 're' obiektu x na -3")
x.re=-3
print(f"Obiekt 'x' to [{x}]")   # Sprawdźmy zawartość 'x'
