def fib( x):
    if (x<2):
        return x
    else:
        return fib(x-1)+fib(x-2)

def fib_dyn(n):
    if n<=2:
        return [0, 1]
    fTab = [0] * (n+1)    # Tablica na wyniki
    fTab[1] = 1
    for i in range (2, n+1):
        fTab[i]=fTab[i-1] + fTab[i-2]
    return fTab

# Testujemy:
N=12
f=fib_dyn(N)    # Oblicza N-1 kolejnych elementów ciągu Fibonacciego
print("Tablica wyników:", f)
print("Wyniki:")
for i in range(N+1):
    print(f"fib({i:2})={f[i]:>10} \t metoda klasyczna: {fib(i):>10}")


