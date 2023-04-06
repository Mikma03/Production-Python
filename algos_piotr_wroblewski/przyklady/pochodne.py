N=5     # Rząd obliczanych różnic centralnych wynosi n-1
def stirling(t):
    # Funkcja zwraca wartości f'(z) i f''(z) gdzie z jest elementem centralnym (tutaj t[2][0])
    # Tablica 't' musi być uprzednio centralnie zainicjowana, jej poprawność nie jest sprawdzana!
    #res= new double [2]
    h=(t[4][0]-t[0][0]) / (N-1)   # Krok argumentu 'x'
    for j in range(2, N+1):         # Od 2 do N
        for i in range(0, N-j+1):   # Od 0 do N-j
            t[i][j] = t[i+1][j-1]-t[i][j-1]
    res0= ((t[1][2]+t[2][2])/2.0-(t[0][4]+t[1][4])/12.0)/h  # f
    res1= (t[1][3]-t[0][5]/12.0)/(h*h)                      # f''
    return res0, res1



# Testujemy:
t=[ [0.8, 4.80, 0, 0, 0, 0], # Pary (x[i], y[i]) dla y = 5x^2+2x
    [0.9, 5.85, 0, 0, 0, 0], # wpisane są w dwie pierwsze kolumny
    [1,   7.00, 0, 0, 0, 0],
    [1.1, 8.25, 0, 0, 0, 0],
    [1.2, 9.60, 0, 0, 0, 0] ]
f0, f1 =stirling(t)

print("y=5x*x+2*x  f'=",  f0, ", f''=", f1 ) # f'= 12.000000000000005 , f''= 9.999999999999963
