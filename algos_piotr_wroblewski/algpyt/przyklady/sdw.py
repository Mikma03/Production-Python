def StadDoWiecznosci(n):
    if (n==1):
        return 1
    else:
        if ( (n %2) == 0 ): # n parzyste
            return StadDoWiecznosci(n-2) * n
        else:
              return StadDoWiecznosci(n-1) * n
# Testujemy wywołanie:
print ( StadDoWiecznosci(2) )
print("Ta linijka nigdy się nie wyświetli...")


