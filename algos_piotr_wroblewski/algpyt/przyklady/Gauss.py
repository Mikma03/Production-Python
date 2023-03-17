N=3
def gauss(a, x):    # a[N][N+1], x[N]
    for i in range(N):  # Eliminacja
        max=i
        for j in range (i+1, N):
            if abs( a[j][i]) > abs(a[max][i]):
                max=j
        for k in range (i, N+1): # Zamiana wierszy wartościami
            tmp = a[i][k]
            a[i][k] = a[max][k]
            a[max][k] = tmp
        if a[i][i]==0:
            return False;  # Układ sprzeczny!
        for j in range(i+1, N):
            for k in range(N, i-1, -1): # Od N do i, co -1, mnożenie wiersza j przez współczynnik "zerujący"
                a[j][k] = a[j][k] - a[i][k]*a[j][i]/a[i][i]
    for j in range (N-1, -1, -1): # j od N-1 do 0, redukcja wsteczna
        tmp=0
        for k in range(j+1, N):
            tmp = tmp + a[j][k]*x[k]
        x[j]=(a[j][N]-tmp)/a[j][j]
    return True # Wszystko w porządku

# Testujemy
x = [0.] * N # Tablica wyników

u1=[ [ 5 ,  0,  1, 9], # Rozmiar N*(N+1)
    [1 ,  1,-1,  6],
    [2,  -1, 1,  0] ]

u2 =[ [1 ,  1,  1, 9],
      [0 ,  1, 1,  6],
      [0,   1, 1,  4]]

if gauss(u1,x)==False:
    print("Układ (1) jest sprzeczny!")
else:
    print("Rozwiązanie:")
    for i in range(N):
        print(f"x[{i:1}]={x[i]:2.4f}")
if gauss(u2,x) == False:
    print("Układ (2) jest sprzeczny!")