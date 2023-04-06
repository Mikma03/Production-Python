def nwd1 (a, b):
    if (b==0):
        return a
    else:
      return nwd1 (b, a % b)    #  Operator %  funkcję modulo
                                #  (reszta z dzielenia liczb całkowitych)
def nwd2(a, b):
    if (b > a):
        return nwd1(a, b - a)
    if (b < a):
        return nwd1(a - b, b)
    if (a == b):
        return b

print ("nwd(12,3)= ", nwd1(12,3),  "Druga metoda", nwd1(12,3))
print ("nwd(24,30)=", nwd1(24,30), "Druga metoda", nwd2(24,30))
print ("nwd(5,7)=  ", nwd1(5,7),   "Druga metoda", nwd2(5,7))
print ("nwd(54,69)=", nwd1(54,69), "Druga metoda", nwd2(54,69))
