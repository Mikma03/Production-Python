
print("bin(46)=", bin(46))
print("Liczba 5 << 1 to 10 (operacje są wykonywane na bitach!):\n", \
      5<<1, "- binarnie: ", bin(5<<1) )
a=0b1011    # Liczba 11, prefiks 0b oznacza liczbę binarną
b=0b0010    # Liczba 2,  wiodące zera są nieznaczące
print("a=", a, ", binarnie", bin(a))
print("b= ", b, ", binarnie", bin(b))
print("a^b=", bin(a^b))
print("a|b=", bin(a|b))
print("a&b=", bin(a&b))
print("a<<2:", a<<2, ", binarnie:", bin(a<<2))
print("b>>1:", b>>1, ", binarnie:", bin(b>>1))
