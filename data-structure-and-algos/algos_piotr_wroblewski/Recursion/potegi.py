def pot1(x, n): #  x = podstawa, n = wykładnik
    if n==0:
        return 1
    else:
        return pot1(x, n-1)*x

def pot2(x, n, temp=1): # x = podstawa, n = wykładnik, zmienną  temp inicjujemy początkowo jako 1
    if n==0:
        return temp
    else:
        return pot2(x, n-1, temp*x)

# Testujemy:

for i in range(1, 20):
    for j in range(15):
        print(f"{i:2} do potęgi {j:2} - \t metoda 1.: "
              f"{pot1(i, j):>17} \tmetoda 2.: {pot2(i, j, 1):>17}")

