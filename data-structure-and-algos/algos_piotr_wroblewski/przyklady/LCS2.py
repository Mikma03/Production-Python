def LCSn(X, Y, C):  # Najdłuższy wspólny podnapis
    M = len(X)
    N = len(Y)
    res = 0
    for i in range(M+1):
        for j in range(N + 1):
            if i == 0 or j == 0:
                C[i][j] = 0
            elif X[i-1] == Y[j-1]:
                C[i][j] = C[i-1][j-1] + 1
                res = max(res, C[i][j])
            else:
                C[i][j] = 0
    return res


def wypiszLCSn(X, Y, C):
    M = len(X)
    N = len(Y)
    d = 0    # Długość najdłuższego wspólnego podnapisu
    s = ""
    wiersz, kol = 0, 0
    for i in range(M+1):
        for j in range (N+1):
            if i == 0 or j == 0:
                C[i][j] = 0
            elif X[i - 1] == Y[j - 1]:
                C[i][j] = C[i - 1][j - 1] + 1
                if d < C[i][j]:
                    d = C[i][j]
                    wiersz = i
                    kol = j
            else:
                C[i][j] = 0
    if (d != 0):
        while C[wiersz][kol] != 0:
            s = X[wiersz-1] + s
            wiersz = wiersz -1
            kol=kol-1
            d=d-1
        print(s)
    else:
        print("Brak wspólnego podnapisu")

# Testujemy

X="PIESKI JEST TEN ŚWIAT"
Y="KOT I PIESEK ŚPIĄ OBOK SIEBIE"
print(X)
print(Y)
M = len(X)
N = len(Y)

# Tablica długości LCS C[M+1][N+1]:
C = [0] * (M+1)
for i in range(M+1):
    C[i] = [0] * (N+1)

print("LCSn: Długość najdłuższej wspólnej podsekwencji: ", LCSn(X, Y, C))
print("wypiszLCSn: ")
wypiszLCSn(X, Y, C)