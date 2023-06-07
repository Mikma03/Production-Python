epsilon=0.0001
N=3     # Stopień wielomianu interpolującego

def interpol(z, x, y): # Zwraca wartość funkcji w punkcie 'z'
    wnz=0
    om=1
    for i in range(N+1): # Od 0 do N
        om=om*( z-x[i] )
        w=1.0
        for j in range(N+1):
            if i!=j:
                w = w * ( x[i]-x[j] )
        wnz = wnz + y[i] / (w*(z-x[i]) )
    return wnz*om

# Testujemy:

# Tabela wartości funkcji y[i] = f(x[i] (jest to w istocie funkcja y=sqrt(x):
x = [3.0,    5.0,      6.0,   7.0] # Rozmiar: N+1
y = [1.732,  2.236,  2.449, 2.646]
z=4.5
print("Wartość funkcji sqrt(x) w punkcie ", z, " wynosi ", interpol(z, x, y) )
