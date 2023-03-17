def silnia(x):
    if (x==0):
        return 1
    else:
        return x*silnia(x-1);

def silnia2(x, tmp=1):
    if x==0:
        return tmp
    else:
        return silnia2( x-1, x*tmp)

# Testujemy funkcję:
for i in range(5, 15): # Silnia liczb 5... 15:
    print(f"silnia({i:2})={silnia(i):20} \t silnia2({i})={silnia2(i):20}")
