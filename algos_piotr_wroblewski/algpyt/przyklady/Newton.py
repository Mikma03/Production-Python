epsilon=0.0001

def f(x): # Funkcja f(x) = 3x^2 – 2
   return 3*x*x-2
def fp(x): # Pochodna f'(x) = (3x^2 – 2)' = 6x
   return 6*x

def zero(x0):
   if abs( f(x0) ) < epsilon: # abs() - wartość absolutna (bez znaku)
       return x0
   else:
       return zero( x0 - f(x0) / fp(x0) )
 # Testujemy:
print("Zero funkcji 3x*x-2 wynosi ", zero(1) ) # Wynik 0.8164965986394558