def nwd (a, b):
    if (b==0):
        return a
    else:
      return nwd (b, a % b)     #  operator % w C++ realizuje funkcję modulo
                                #  (reszta z dzielenia liczb całkowitych)
print ("nwd(2,3)=", nwd(12,3) )
