def fib(x):
    if (x < 2):
        return x
    else:
        return fib(x - 1) + fib(x - 2)
# Testujemy funkcję w zakresie liczb 1... 11 (wynik: 1 1 2 3 5 8 13 21 34 55 89)
for i in range(1, 12):
    print(f"fib({i})={fib(i)}")


