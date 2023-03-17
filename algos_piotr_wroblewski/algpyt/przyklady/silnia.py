def silnia(x):
    if (x==0):
        return 1
    else:
        return x*silnia(x-1);
# Testujemy funkcję:
for i in range(5, 11): # Silnia liczb 5... 10:
    print(f"silnia({i})={silnia(i)}")


