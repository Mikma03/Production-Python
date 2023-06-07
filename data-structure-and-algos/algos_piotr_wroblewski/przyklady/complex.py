# Realizacja klasy Complex() w której zabezpieczono pola wewnętrzne __re, __im
# realizując dostęp do nich przez właściwości Re, Im. Ponadto zrealizowano dwier operacje
# arytmetyczne, używając techniki "przeciążania" operatorów + oraz *
class Complex:
       def __init__(self, pRe=0, pIm=0): # Konstruktor
              self.__re = pRe  # Tworzymy atrybut __re - część rzeczywista
              self.__im = pIm  # Tworzymy atrybut __im – część urojona

       def __str__(self): # Zwracamy obiekt jako napis nadający się do wydruku w funkcji print
              return str(self.__re) + "+" + str(self.__im) + "*i"

       def __add__(self, x2):  # Ta metoda zwraca obiekt będący sumą dwóch liczb zespolonych (np.x+y)
              # x1=a+b·i,x2=c+d·i
              # x1+x2 = (a+c) + (b + d)·i
              return Complex(self.__re + x2.__re, self.__im + x2.__im)

       def __mul__(self, x2):  # Ta metoda zwraca obiekt będący iloczynem dwóch liczb zespolonych (np.x·y)
              # x1=a+b·i,x2=c+d·i
              # x1·x2 = (ac-bd) + (ad + bc)·i
              return Complex( self.__re * x2.__re - self.__im * x2.__im,
                              self.__re * x2.__im + self.__im * x2.__re)
       @property
       def re(self):
              return self.__re
       @property
       def im(self):
              return self.__im

# --------- Kilka przykładów użycia: ------------------------------------------------------------
x = Complex(5,8)                # Tworzymy nowy obiekt x = 5 + 8*i
y = Complex(1,2)                # Tworzymy nowy obiekt y = 1 + 2*i
# x.re=2  #--> Python zgłosi błąd "AttributeError: can't set attribute"
print(f"Obiekt 'x' to [{x}]")
print(f"Obiekt 'y' to [{y}]")
z=x+y
q=x*y
print(f"Obiekt z=x+y to [{z}]") # Sprawdźmy wynik dodawania x+y
print(f"Obiekt q=x*y to [{q}]") # Sprawdźmy wynik mnożenia x*y


