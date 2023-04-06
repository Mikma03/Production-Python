def sumaNaturalna(x, y):
    if x > 0 and y > 0:
        return True, x+y
    else:
        return False, -1 # Umowna sygnalizacja błędów
wynik = sumaNaturalna(2,-3)
print(wynik)