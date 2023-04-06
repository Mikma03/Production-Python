def A (m, n):
    if (m==0):
        return n+1
    else:
        if (m > 0 and n==0):
            return A(m-1, 1)
        else:
            if(m > 0 and n > 0):
                return A( m-1, A(m,(n-1)) )
# Testujemy program:

while True:
    try:
        m = int(input("Podaj m:"))
        n = int(input("Podaj n:"))
        break
    except ValueError:
        print ("Ups, błąd danych, oczekiwano wprowadzenia liczb... Próbuj dalej.")

print (f" A({m},{n})={A(m, n)}")
