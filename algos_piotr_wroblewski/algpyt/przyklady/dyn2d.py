
def dynam(P):   # Tablica 2-wymiarowa
    n=len(P)
    for i in range(1, n):
        P[i][0] = 0.0
        P[0][i] = 1.0
    for j in range(1, n):
        for i in range(1, n):
            P[i][j]=(P[i-1][j] + P[i][j-1]) / 2.0

# Testujemy
N=5

# Deklarujemy tablicę 2-wymiarową N*N (pozornie poprawna konstrukcja P = [ [0]*N] * N powieliłaby
# tylko referencje do tej samej listy w kolejnych wierszach, co doprowadziłoby do błędów obliczeniowych!
# Patrz: https://docs.python.org/3/faq/programming.html#how-do-i-create-a-multidimensional-list

P = [0] * N
for i in range(N):
    P[i] = [0] * N


dynam(P)
print(P)